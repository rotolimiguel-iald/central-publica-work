# -*- coding: utf-8 -*-
"""f9v2_runner.py -- O RUNNER DO MODO OBSERVADO da Fase 9 V2-c1, «O Teste da Unica Palavra» (beta_TGL, a voz unica da razao de Hubble).

ESTE ARQUIVO NAO FOI EXECUTADO SOBRE DADO REAL. Ele RECUSA abrir sem (1) RECIBO DE CONGELAMENTO emitido pela gerencia e (2) RECIBO DE ABERTURA (ato proprio).

Ordem do modo observado (E5), nao negociavel:
  0 recibos + pinos que NAO sao fonte (spec, funcao, runner, registro D-H, recibo de calibracao, Bancada); ABERTURA UNICA (B4): o marcador freeze/ABERTURA_CONSUMIDA.json
    nasce (O_EXCL) ANTES da primeira fonte ser lida; so entao cada fonte e' lida UMA vez e conferida por sha256. Recusa apos a abertura grava freeze/REGISTRO_DE_RECUSA_*.json;
  1 beta = ALPHA_FINE_CODATA_2018 x sqrt(e) em runtime (alpha lido do um.py instalado); K recalculado e comparado ao K congelado;
  2 E1/E2 o fundo BG1 REAL (Bancada: Planck comprimido + DESI DR2, sem escada) e a reproducao |H0 - 68,531| < 0,01 (diverge => INTERROMPE, nunca calibra);
  3 PODER_FASE9_ANTES_DE_ABRIR.json: SO sigmas e o fundo; gravado e hasheado ANTES de qualquer centro local ser lido (os centros ficam num cofre lacrado);
  4 os centros saem das FONTES (E4: registro D-H pinado; regra de extracao pinada); proibido ALVOS_FASE9_LIDOS.json montado a mao (a presenca de um RECUSA);
  5 estatistica do executor (X13), S5 (fundo propagado), E3 (quadraturas 100/200 com tolerancia e recusa), calibracao de cauda (z -> p calibrado -> z);
  6 a funcao de veredito PINADA, executada do TEXTO; resultado inteiro gravado, tambem abaixo de 5 sigma. NOT_FALSIFIED nunca é a palavra da creditação. O gate não se move.
"""
import argparse
import json
import math
import os
import re
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import f9v2_background as BG  # noqa: E402
import f9v2_calibration as CAL  # noqa: E402
import f9v2_extract as EXT  # noqa: E402
import f9v2_freeze as FRZ  # noqa: E402
import f9v2_stats as ST  # noqa: E402
import f9v2_verdict as VER  # noqa: E402

Refusal = FRZ.Refusal
UM_PY_DEFAULT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"


def _write_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    if os.path.getsize(tmp) != len(data):
        raise Refusal("REFUSE__WRITE_SIZE_MISMATCH", path)
    os.replace(tmp, path)
    return FRZ.sha256_bytes(data)


class CenterVault:
    """Cofre lacrado dos centros locais declarados: nenhum codigo le H0 antes de unseal(); unseal exige o PODER ja' gravado."""

    def __init__(self, declared, log):
        self._d = dict(declared)
        self._log = log
        self._power_written = False

    def mark_power_written(self):
        self._power_written = True

    def unseal(self):
        if not self._power_written:
            raise Refusal("REFUSE__CENTERS_BEFORE_POWER", "os centros locais nao podem ser lidos antes do PODER_FASE9_ANTES_DE_ABRIR")
        self._log.append("CENTERS_UNSEALED")
        return dict(self._d)


def seal_spec_readers(spec, log):
    """Retira H0 de spec['leitores'] (guardando-os no cofre): qualquer acesso antecipado levanta KeyError."""
    declared = {}
    for rid, r in spec["leitores"].items():
        declared[rid] = {"H0": float(r.pop("H0")), "sigma": float(r["sigma"])}
    return CenterVault(declared, log)


def read_alpha(um_bytes):
    m = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", um_bytes, re.M)
    if not m:
        raise Refusal("REFUSE__ALPHA_NOT_FOUND", "ALPHA_FINE_CODATA_2018 ausente no um.py")
    return float(m.group(1))


def read_um_E_constants(um_bytes):
    out = {}
    m = re.search(rb"def _v378_lcdm_E\(z, H0, ombh2, omch2, mnu_eV, TCMB, Neff, og_coef=([0-9.eE+-]+)\)", um_bytes)
    if m:
        out["og_coef"] = float(m.group(1))
    m = re.search(rb"^_V378_PLANCK\s*=\s*(\{[^\n]*\})", um_bytes, re.M)
    if m:
        import ast
        P = ast.literal_eval(m.group(1).decode("utf-8"))
        for k in ("TCMB", "Neff", "mnu_eV"):
            if k in P:
                out[k] = float(P[k])
    return out


def inventory_count(inventory_ids, verified_ids, admitted_ids):
    """E4: n_alvos_declarados = |{ i no inventario V1.x INTEIRO : NOT gate_verified AND NOT admitido no registro D-H pinado }|."""
    return sorted(i for i in inventory_ids if (i not in verified_ids) and (i not in admitted_ids))


def eval_family(spec, fam, centers, law, bgfree, bg_label, cal_mode, n_decl, sources_admitted, fn, power_cef, readers_sigma, tol):
    ids = spec["familias"][fam]["ids"]
    amps = spec["covariancia"]["amplitudes_km_s_Mpc"]
    grid = spec["covariancia"]["grid"]
    ep = ST.grid_endpoints(amps, readers_sigma, ids, grid["lambda_N"], grid["lambda_T"])
    y = [centers[i]["H0"] for i in ids]
    st = {side: ST.endpoint_statistics(y, ids, ep[side]["covariance"], law, bgfree) for side in ("minimum", "maximum")}
    VT = law.V(law.beta)
    zread = [(readers_sigma[i], (centers[i]["H0"] - law.K * law.mu) / math.sqrt(readers_sigma[i] ** 2 + VT)) for i in ids]
    edge = any(st[s]["beta"]["at_prior_edge"] or st[s]["z_delta"] is None for s in st)
    zd_raw = st["minimum"]["z_delta"]
    zdisc_raw = st["maximum"]["z_disc"]
    # calibracao de cauda
    zmap = CAL.ZDeltaMap(ep["minimum"]["sigma_comb"], law)
    try:
        zmap.require_monotone()   # B3: mapa nao monotono => RECUSA
    except ST.StatsError as e:
        raise Refusal("REFUSE__CALIBRATION_MAP_NOT_MONOTONE", str(e)) from e
    zdm = CAL.ZDiscMap(ep["maximum"]["sigma_comb"], law)
    tau = CAL.taus(amps, readers_sigma, ids, ep, law, grid["lambda_N"], grid["lambda_T"])
    tf = tau["tau_f_sup"] if cal_mode == "sup_caixa" else tau["tau_f_proprio"]
    td = tau["tau_d_sup"] if cal_mode == "sup_caixa" else tau["tau_d_proprio"]
    if cal_mode == "bruto":
        zd_fed, zdisc_fed = zd_raw, zdisc_raw
        p_zd = None
    else:
        zd_fed = None if (zd_raw is None) else zmap.z_cal(zd_raw, tf)
        zdisc_fed = zdm.z_cal(zdisc_raw, td)
        p_zd = None if zd_raw is None else zmap.p_two_sided(abs(zd_raw), tf)[0]
    p_zdisc = zdm.p_one_sided(max(zdisc_raw, 0.0), td) if zdisc_raw > 0 else None
    # poder (so sigma) com S5
    smax = ep["maximum"]["sigma_comb"]
    poder_prev = ST.power_sigma_only(law.K, law.mu, smax, VT)
    r = {"fundo": bg_label, "n_local": len(ids), "n_alvos_declarados": n_decl, "required_sources_admitted": bool(sources_admitted),
         "beta_livre_no_limite": bool(edge),
         "minimum": {"z_delta": 0.0 if zd_fed is None else float(zd_fed), "sigma_z_por_alvo": zread},
         "maximum": {"poder_previo": poder_prev, "z_disc": float(zdisc_fed), "lnB_lcdm": st["maximum"]["lnB_lcdm"], "lnB_livre": st["maximum"]["lnB_livre"],
                     "lnB_shift": st["maximum"]["lnB_shift"], "lnB_fundo_livre": st["maximum"]["lnB_fundo_livre"], "poder_nao_cefeida": power_cef},
         "use_novel_parametros": bool(spec["novidade_de_uso"]["use_novel_parametros"] is True)}
    if len(ids) > 1:
        r["dispersao_endpoints"] = {s: {"chi2_por_gl": st[s]["dispersao"]["chi2_por_gl"], "p": st[s]["dispersao"]["p"]} for s in ("minimum", "maximum")}
    try:
        token = fn(_deep(r))
    except ValueError as e:
        raise Refusal("REFUSE__INVALID_NUMERIC_INPUT", str(e)) from e
    return {
        "familia": fam, "fundo": bg_label, "veredito": token, "entrada_da_funcao": _jsonable(r),
        "extremos_da_covariancia": {s: {"lambda_N": ep[s]["lambda_N"], "lambda_T": ep[s]["lambda_T"], "sigma_comb": ep[s]["sigma_comb"],
                                        "pesos_GLS": dict(zip(ids, map(float, ep[s]["weights"])))} for s in ("minimum", "maximum")},
        "escores_brutos": {"z_delta_no_ponto_de_menor_sigma": zd_raw, "z_disc_no_ponto_de_maior_sigma": zdisc_raw,
                           "z_disc_com_logdet_ao_lado": st["maximum"]["z_disc_logdet_ao_lado"]},
        "calibracao": {"modo": cal_mode, "tau_f": tf, "tau_d": td, "taus": tau, "p_calibrado_z_delta_bilateral": p_zd, "p_calibrado_z_disc_unilateral": p_zdisc,
                       "z_delta_calibrado": zd_fed, "z_disc_calibrado": zdisc_fed, "mapa_z_delta_monotono": zmap.monotone},
        "estatisticas_por_extremo": _jsonable(st),
        "beta_hat_no_ponto_de_menor_sigma": st["minimum"]["beta"],
        "lnB": {"TGL_vs_LCDM": st["maximum"]["lnB_lcdm"], "TGL_vs_beta_livre": st["maximum"]["lnB_livre"], "TGL_vs_shift_cefeidas": st["maximum"]["lnB_shift"],
                "TGL_vs_fundo_livre": st["maximum"]["lnB_fundo_livre"]},
        "z_por_leitor_contra_TGL": {i: z for i, (_, z) in zip(ids, zread)},
        "poder_previo_so_sigma": poder_prev,
    }


def _deep(v):
    if isinstance(v, dict):
        return {k: _deep(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_deep(x) for x in v]
    return v


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


def open_test(root, provider=None, *, out_dir=None, now=None, um_py_bytes=None, bancada_pins_fn=None):
    """Abre o teste. Levanta Refusal em qualquer violacao; nao devolve veredito parcial.
    Abertura UNICA (B4): o marcador freeze/ABERTURA_CONSUMIDA.json e' criado (O_EXCL) ANTES de a primeira fonte ser lida; marcador existente => REFUSE__ALREADY_OPENED.
    Toda recusa DEPOIS do marcador (e a tentativa de reabrir) grava freeze/REGISTRO_DE_RECUSA_*.json. Recusas ANTES do marcador (recibos, pinos, spec) nao consomem a abertura."""
    log = ["START"]
    t_start = time.time()
    root = os.path.abspath(root)
    # --- 0. recibos e pinos que NAO sao fonte
    bancada_cur = None
    try:
        raw_rec = json.loads(open(os.path.join(root, *FRZ.FREEZE_REL.split("/")), "rb").read().decode("utf-8")) if os.path.isfile(os.path.join(root, *FRZ.FREEZE_REL.split("/"))) else None
    except (UnicodeError, ValueError):
        raw_rec = None
    if raw_rec is not None and raw_rec.get("package_kind") == "REAL":
        bancada_cur = (bancada_pins_fn or BG.bancada_pins)()
    rec, ver = FRZ.check_freeze_core(root, require_bancada=bancada_cur)
    opening = FRZ.check_opening_act(root, ver["__freeze_raw__"])
    kind = rec["package_kind"]
    log.append("PINS_OK")
    for dirpath, _dirs, files in os.walk(root):
        if "ALVOS_FASE9_LIDOS.json" in files:
            raise Refusal("REFUSE__MANUAL_TARGET_LEDGER", os.path.join(dirpath, "ALVOS_FASE9_LIDOS.json"))
    spec_obj = json.loads(ver["spec_arquivo"].decode("utf-8"))
    spec = spec_obj["spec"]
    if rec["token_base"] != VER.TOKEN_BASE or spec["token"]["base"] != VER.TOKEN_BASE:
        raise Refusal("REFUSE__TOKEN_BASE_DIFFERS")
    fsrc = ver["funcao_arquivo"].decode("utf-8")
    if fsrc != spec["funcao_de_veredito"]["fonte"]:
        raise Refusal("REFUSE__FUNCTION_TEXT_DIFFERS_FROM_SPEC")
    fn, fsha = VER.load_pinned_verdict(fsrc, spec["funcao_de_veredito"]["sha256"])
    register = json.loads(ver["registro_dh"].decode("utf-8"))
    tol = spec["runner_contract"]["tolerancias"]
    if tol["quadratura_ln_abs"] != ST.QUAD_TOL:
        raise Refusal("REFUSE__QUAD_TOL_DIFFERS_FROM_CODE", "%r x %r" % (tol["quadratura_ln_abs"], ST.QUAD_TOL))
    cal_mode = spec["calibracao_de_cauda"]["modo"]
    if cal_mode not in ("sup_caixa", "proprio", "bruto"):
        raise Refusal("REFUSE__CALIBRATION_MODE_UNKNOWN", str(cal_mode))
    inventory = sorted(spec["leitores"])
    if sorted(register["leitores"]) != inventory:
        raise Refusal("REFUSE__INVENTORY_DIFFERS", "registro D-H x spec")
    if spec["registro_dh"]["sha256"] != FRZ.sha256_bytes(ver["registro_dh"]):
        raise Refusal("REFUSE__PIN_MISMATCH", "spec.registro_dh.sha256 difere dos bytes do registro D-H")
    for rid in inventory:
        if spec["leitores"][rid]["documentary_source"]["sha256"] != register["leitores"][rid]["sha256"]:
            raise Refusal("REFUSE__PIN_MISMATCH", "spec.leitores.%s.documentary_source difere do registro D-H" % rid)
    # --- ABERTURA UNICA: o marcador nasce ANTES da primeira fonte ser lida
    try:
        marker_sha = FRZ.consume_opening_marker(root, ver["__freeze_raw__"], opening)
    except Refusal as e:
        if e.code == "REFUSE__ALREADY_OPENED":
            FRZ.write_refusal_record(root, e.code, e.detail, "TENTATIVA_DE_REABRIR", opening["__file_sha256__"])
        raise
    log.append("OPENING_CONSUMED:" + marker_sha[:16])
    try:
        return _open_after_marker(root, provider, out_dir, um_py_bytes, rec, ver, opening, kind, spec, fn, fsha, register, tol, cal_mode, inventory, log, t_start)
    except Exception as e:  # noqa: BLE001 -- toda recusa/erro apos a abertura deixa registro (e re-levanta)
        FRZ.write_refusal_record(root, getattr(e, "code", type(e).__name__), "%s: %s" % (type(e).__name__, e), "APOS_ABERTURA", opening["__file_sha256__"])
        raise


def _open_after_marker(root, provider, out_dir, um_py_bytes, rec, ver, opening, kind, spec, fn, fsha, register, tol, cal_mode, inventory, log, t_start):
    calib_receipt = json.loads(ver["calibracao_recibo"].decode("utf-8"))
    # --- fontes: AGORA (depois do marcador) cada uma e' lida UMA vez e conferida por sha256; nenhum numero e' lido ainda
    FRZ.read_sources(root, rec, ver)
    verified_ids = set(ver["sources"])
    admitted_ids = {i for i, r in register["leitores"].items() if r.get("admitido_pelo_operador") is True}
    declared = inventory_count(inventory, verified_ids, admitted_ids)
    log.append("SOURCES_BYTES_VERIFIED_NO_NUMBER_READ")
    # --- 1. beta em runtime
    if kind == "REAL":
        um_path = spec["beta"].get("um_py_path", UM_PY_DEFAULT)
        try:
            um_raw = um_py_bytes if um_py_bytes is not None else open(um_path, "rb").read()
        except OSError as e:
            raise Refusal("REFUSE__UM_PY_UNREADABLE", "%s: %s" % (um_path, e)) from e
        alpha = read_alpha(um_raw)
        alpha_src = {"fonte": "um.py instalado", "path": um_path, "sha256": FRZ.sha256_bytes(um_raw)}
        E_consts_um = read_um_E_constants(um_raw)
    else:
        alpha = float(spec["beta"]["alpha_read"])
        alpha_src = {"fonte": "SPEC (pacote sintetico; sem um.py)"}
        E_consts_um = {}
    if not abs(alpha - spec["beta"]["alpha_read"]) <= 1e-15 * max(1.0, abs(alpha)):
        raise Refusal("REFUSE__ALPHA_DIFFERS_FROM_SPEC", "%r vs %r" % (alpha, spec["beta"]["alpha_read"]))
    beta = alpha * math.sqrt(math.e)
    if not math.isclose(beta, spec["beta"]["beta_runtime"], rel_tol=1e-12):
        raise Refusal("REFUSE__BETA_DIFFERS_FROM_SPEC")
    consts = dict(spec["S5_propagacao"]["constantes_E"])
    consts.pop("origem", None)
    consts_match = {}
    if kind == "REAL":
        # B5: as constantes do S5 sao COBRADAS contra o um.py instalado (nao so gravadas)
        consts_match = {k: (k in E_consts_um and math.isclose(E_consts_um[k], consts[k], rel_tol=1e-12)) for k in consts}
        if not all(consts_match.values()):
            raise Refusal("REFUSE__S5_CONSTANTS_DIFFER_FROM_UM_PY", "divergentes/ausentes: %s" % sorted(k for k, ok in consts_match.items() if not ok))
    lei = spec["lei"]
    lnE = ST.lnE_pinned(lei["Omega_m"], lei["Omega_r"], lei["z_star"])
    # --- 2. E1/E2 o fundo
    if provider is None:
        if kind != "REAL":
            raise Refusal("REFUSE__NO_PROVIDER_FOR_SYNTHETIC")
        provider = BG.BancadaBackgroundProvider()
    if kind == "REAL" and getattr(provider, "kind", None) != "BANCADA_REAL":
        raise Refusal("REFUSE__PROVIDER_NOT_REAL", str(getattr(provider, "kind", None)))
    bgd = provider.compute()
    pin_bg = spec["fundos"]["BG1"]
    repro = BG.check_reproduction(bgd, pin_bg["H0"], pin_bg["sigma"], tol["BG1_H0_abs"], tol["BG1_sigma_abs"])
    log.append("BACKGROUND_OK")
    law = ST.Law(beta, lei["K_frozen_V1"], lnE, bgd["bg1"]["H0"], bgd["bg1"]["cov_theta"], bgd["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts,
                 s5=bool(spec["S5_propagacao"]["habilitado"]))
    bgfree = bgd["fundo_livre"]
    # guarda do recibo de calibracao (so fundo + sigmas; nenhum centro): reconstroi os limiares brutos equivalentes e RECUSA se divergirem do recibo
    chk = calib_receipt.get("limiares_equivalentes_P_primaria_BG1", {})
    try:
        live = CAL.primary_thresholds(spec, bgd, cal_mode, consts)
    except ST.StatsError as e:
        raise Refusal("REFUSE__CALIBRATION_MAP_NOT_MONOTONE" if "monoton" in str(e).lower() else "REFUSE__STATS_ERROR", str(e)) from e
    guard = {}
    for k, v in live.items():
        ref = chk.get(k)
        guard[k] = {"vivo": v, "recibo": ref, "rel": None if not ref else abs(v - ref) / abs(ref)}
        if not ref or abs(v - ref) / abs(ref) > tol["recibo_calibracao_rel"]:
            raise Refusal("REFUSE__CALIBRATION_RECEIPT_DIFFERS", "%s: vivo %.4f x recibo %r" % (k, v, ref))
    log.append("CALIBRATION_RECEIPT_GUARD_OK")
    # --- 3. PODER ANTES DE ABRIR (so sigmas) -- os centros estao lacrados
    vault = seal_spec_readers(spec, log)
    sig = {i: spec["leitores"][i]["sigma"] for i in spec["leitores"]}
    amps = spec["covariancia"]["amplitudes_km_s_Mpc"]
    grid = spec["covariancia"]["grid"]
    VT = law.V(law.beta)
    poder = {}
    for fam in spec["familias"]:
        ids = spec["familias"][fam]["ids"]
        ep = ST.grid_endpoints(amps, sig, ids, grid["lambda_N"], grid["lambda_T"])
        poder[fam] = {s: {"sigma_comb": ep[s]["sigma_comb"],
                          "D_S5_fundo_vivo": ST.power_sigma_only(law.K, law.mu, ep[s]["sigma_comb"], VT),
                          "D_formula_pinada_BG": {b: ST.power_sigma_only(law.K, spec["fundos"][b]["H0"], ep[s]["sigma_comb"], (law.K * spec["fundos"][b]["sigma"]) ** 2)
                                                 for b in ("BG1", "BG2", "BG3")}} for s in ("minimum", "maximum")}
    pin = spec["poder_previo"]["primary_five"]
    for s in ("minimum", "maximum"):
        for b in ("BG1", "BG2", "BG3"):
            if abs(poder["P_primaria"][s]["D_formula_pinada_BG"][b] - pin[s][b]) > tol["poder_pino_abs"]:
                raise Refusal("REFUSE__POWER_DIFFERS_FROM_PIN", "%s %s" % (s, b))
    pw = {"quando_unix": time.time(), "ordem": "so sigmas, K e o fundo; nenhum centro local de H0 entrou em calculo ate aqui", "kind_do_pacote": kind,
          "fundo_BG1_vivo": {"H0": law.mu, "sigma": law.sigma_bg, "fornecedor": bgd["kind"]}, "K": law.K, "beta_runtime": beta, "V_previsao_TGL_S5": VT,
          "S5_habilitado": law.s5, "poder": poder}
    pw_bytes = json.dumps(pw, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    out_dir = out_dir or os.path.join(root, "saidas" if kind == "REAL" else "saidas_sinteticas")
    os.makedirs(out_dir, exist_ok=True)
    prefix = "" if kind == "REAL" else "SYNTHETIC_"
    power_sha = _write_atomic(os.path.join(out_dir, prefix + "PODER_FASE9_ANTES_DE_ABRIR.json"), pw_bytes)
    vault.mark_power_written()
    log.append("POWER_WRITTEN:" + power_sha[:16])
    # --- 4. os centros: do cofre, so depois, e conferidos contra a FONTE (E5: nunca ALVOS a mao)
    declared_centers = vault.unseal()
    extracted = {}
    for rid, rr in register["leitores"].items():
        rule = {k: rr[k] for k in ("kind", "regex", "H0_group", "sigma_rule")}
        if "page" in rr:
            rule["page"] = rr["page"]
        e = EXT.extract_reader(rule, ver["sources"][rid])
        d = declared_centers[rid]
        if not (abs(e["H0"] - d["H0"]) < tol["extracao_abs"] and abs(e["sigma"] - d["sigma"]) < tol["extracao_abs"]):
            raise Refusal("REFUSE__EXTRACTION_DIFFERS_FROM_DECLARED", "%s: fonte %r/%r x spec %r/%r" % (rid, e["H0"], e["sigma"], d["H0"], d["sigma"]))
        extracted[rid] = {"H0": e["H0"], "sigma": e["sigma"], "onde": e["onde"], "trecho": e["trecho"]}
    centers = {rid: {"H0": v["H0"], "sigma": v["sigma"]} for rid, v in extracted.items()}
    log.append("EXTRACTED_FROM_SOURCE_BYTES")
    # --- 5/6. estatistica, calibracao, funcao
    ids_nc = spec["familias"]["N_sem_cefeidas"]["ids"]
    ep_nc = ST.grid_endpoints(amps, sig, ids_nc, grid["lambda_N"], grid["lambda_T"])
    power_cef = ST.power_sigma_only(law.K, law.mu, ep_nc["maximum"]["sigma_comb"], VT)
    admitted_all = all(i in admitted_ids for i in inventory)
    families = {}
    primary = eval_family(spec, "P_primaria", centers, law, bgfree, "BG1", cal_mode, len(declared), admitted_all, fn, power_cef, sig, tol)
    log.append("PRIMARY_VERDICT")

    def diag(label, thunk):
        # um diagnostico que falha NAO derruba o veredito decisorio ja' calculado: o erro fica dito ao lado
        try:
            families[label] = thunk()
        except (ST.StatsError, Refusal) as e:
            families[label] = {"ERRO_NO_DIAGNOSTICO": "%s: %s" % (type(e).__name__, e), "decisorio": False}

    for fam in ("R_r25", "N_sem_cefeidas", "S_com_sirenes", "T_so_cchp", "M_seis_masers_diagnostico"):
        diag(fam + " x BG1", lambda fam=fam: eval_family(spec, fam, centers, law, bgfree, "BG1", cal_mode, len(declared), admitted_all, fn, power_cef, sig, tol))
    for b in ("BG2", "BG3"):
        pb = spec["fundos"][b]
        lawb = ST.Law(beta, lei["K_frozen_V1"], lnE, pb["H0"], np.diag([pb["sigma"] ** 2, 1e-12, 1e-12]), bgd["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"],
                      consts, s5=False)
        diag("P_primaria x " + b, lambda b=b, lawb=lawb: eval_family(spec, "P_primaria", centers, lawb, bgfree, b, cal_mode, len(declared), admitted_all, fn, power_cef, sig, tol))
    log.append("DIAGNOSTICS_DONE")
    token = primary["veredito"]
    res = {
        "id": "RESULTADO_FASE9_V2_C1_" + time.strftime("%Y%m%d_%H%M%S"), "kind_do_pacote": kind,
        "AVISO": ("RESULTADO SINTETICO DE TESTE DO RUNNER; NAO E' O TESTE DA FASE 9" if kind != "REAL" else
                  "RESULTADO DO TESTE DA UNICA PALAVRA; NOT_FALSIFIED nunca é a palavra da creditação; o gate não se move"),
        "veredito": token, "token_base": VER.TOKEN_BASE,
        "pinos": {"recibo_de_congelamento_sha256": FRZ.sha256_bytes(ver["__freeze_raw__"]), "funcao_sha256": fsha, "spec_canonico_sha256": rec["pins"]["spec_canonico_sha256"],
                  "registro_dh_sha256": rec["pins"]["registro_dh"]["sha256"], "runner": {k: v["sha256"][:16] for k, v in rec["pins"]["runner_modulos"].items()},
                  "poder_antes_de_abrir_sha256": power_sha, "abertura_autohash": opening["autohash"], "recibo_de_abertura_sha256": opening["__file_sha256__"]},
        "beta": {"alpha": alpha, "alpha_fonte": alpha_src, "beta_runtime": beta, "K": law.K, "K_no_theta_do_fundo": law.K_at_theta()[0], "constantes_E_conferem_com_um_py": consts_match},
        "fundo": {"fornecedor": bgd["kind"], "reproducao_E2": repro, "BG1": bgd["bg1"], "fundo_livre": bgfree, "r_d_modelo": bgd["r_d_modelo_no_BG1"]},
        "centros_extraidos_das_fontes": extracted,
        "n_alvos_declarados": len(declared), "alvos_declarados": declared, "admitidos_no_registro_D_H": sorted(admitted_ids),
        "primario": primary, "ao_lado_nao_decisorios": families, "guarda_do_recibo_de_calibracao": guard,
        "ordem_de_acesso": log, "duracao_s": time.time() - t_start,
        "leitura": ("O veredito é o que a função pinada devolveu para P_primaria x BG1. FALSIFIED_AT_5SIGMA, se vier, é β_TGL refutado na natureza pela voz única da lei K, "
                    "sem saída posterior (decisão do operador, 23/10/2026). Resultado abaixo de 5 sigma também é preservado integralmente. Réplicas e diagnósticos ficam ao lado, "
                    "nunca decisórios. NOT_FALSIFIED nunca é a palavra da creditação."),
    }
    log.append("RESULT_WRITTEN")
    res = _jsonable(res)
    b = json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")
    rpath = os.path.join(out_dir, prefix + res["id"] + ".json")
    rsha = _write_atomic(rpath, b)
    res["_arquivo"], res["_sha256"] = rpath, rsha
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--package-root", required=True)
    ap.add_argument("--mode", choices=("observed", "preflight"), required=True)
    ap.add_argument("--out", default=None)  # rodar sempre com: python -B -P -E -X utf8 runner/f9v2_runner.py ...
    a = ap.parse_args(argv)
    try:
        if a.mode == "preflight":
            rec, ver = FRZ.check_freeze(os.path.abspath(a.package_root), require_bancada=None)
            print(json.dumps({"preflight": "FREEZE_RECEIPT_OK", "package_kind": rec["package_kind"], "pinos": sorted(rec["pins"]),
                              "abertura": "NAO VERIFICADA no preflight"}, ensure_ascii=False))
            return 0
        res = open_test(a.package_root, out_dir=a.out)
        print(json.dumps({"veredito": res["veredito"], "arquivo": res["_arquivo"], "sha256": res["_sha256"]}, ensure_ascii=False))
        return 0
    except Refusal as e:
        print(json.dumps({"RECUSA": e.code, "detalhe": e.detail}, ensure_ascii=False), file=sys.stderr)
        return 2
    except BG.BackgroundError as e:
        print(json.dumps({"RECUSA": "REFUSE__BACKGROUND_DIVERGES", "detalhe": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except ST.QuadratureUnstable as e:
        print(json.dumps({"RECUSA": "REFUSE__QUADRATURE_UNSTABLE", "detalhe": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except ST.StatsError as e:
        print(json.dumps({"RECUSA": "REFUSE__STATS_ERROR", "detalhe": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except EXT.ExtractionError as e:
        print(json.dumps({"RECUSA": "REFUSE__EXTRACTION_ERROR", "detalhe": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except VER.VerdictLoadError as e:
        print(json.dumps({"RECUSA": "REFUSE__VERDICT_LOAD_ERROR", "detalhe": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
