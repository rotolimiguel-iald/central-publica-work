# -*- coding: utf-8 -*-
"""Gerador UNICO do V1 da Fase 9 — a razao de Hubble (06/10/2026, gerencia, sessao 946c4deb).

Le TUDO do disco por script (alfa do um.py por regex; beta = alfa*sqrt(e) em runtime, nunca literal; z*, fundo nu, leitores
de sombra, R22 e o ensaio do desenho por sha256), aplica as decisoes D-A..D-K pelo PADRAO da gerencia (delegacao do operador
de 05/10: «o resto vc consegue responder tudo agroa»; «prossiga»), fixa UMA funcao de veredito (F1 da critica) como TEXTO
FONTE com sha256 (o runner e a v387 a executam byte a byte), testa os ramos so com casos SINTETICOS (nenhum composto aberto),
e grava JSON (autoridade) + MD + V1_FASE9_HASHES.json. O hash do V1 =
sha256(json.dumps(SPEC, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).
Nenhum valor central de leitor local entra em calculo aqui: o poder previo usa SO sigmas publicas, K e o fundo.
NOT_FALSIFIED nunca e a palavra proibida; a RG/LCDM e o limite classico; nada aqui move beta nem o gate.
"""
import os, re, sys, json, math, hashlib, ast, shutil, datetime, stat
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UM = os.path.join(NOS, "um.py")
SELO = os.path.join(NOS, "um_absoluto_selo.json")
BANC = r"C:\IALD\Bancada_Um\investigacao"
F3PRE = os.path.join(BANC, "fase3_leitores_h0", "PREREGISTRO_FASE3_LEITORES_20260930.json")
F4RES = os.path.join(BANC, "fase4_desvio_30set", "RESULTADO_FASE4_DESVIO_20260930.json")
F5RES = os.path.join(BANC, "fase5_sh0es_01out", "RESULTADO_FASE5_SH0ES_20261001.json")
F9 = os.path.dirname(HERE)  # ...\fase9_hubble
EVID = {
    "CRONOLOGIA_NOVIDADE_DE_USO.json": os.path.join(F9, "novidade_de_uso", "CRONOLOGIA_NOVIDADE_DE_USO.json"),
    "CRONOLOGIA_NOVIDADE_DE_USO.md": os.path.join(F9, "novidade_de_uso", "CRONOLOGIA_NOVIDADE_DE_USO.md"),
    "FASE9_DESENHO_RESULTADO.json": os.path.join(F9, "desenho", "FASE9_DESENHO_RESULTADO.json"),
    "FASE9_DESENHO_TABELA.md": os.path.join(F9, "desenho", "FASE9_DESENHO_TABELA.md"),
    "fase9_desenho_estatistico.py": os.path.join(F9, "desenho", "fase9_desenho_estatistico.py"),
    "CRITICA_FASE9.md": os.path.join(F9, "critico", "CRITICA_FASE9.md"),
    "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.json": os.path.join(F9, "pre_registro", "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.json"),
    "INVENTARIO_DADOS_NA_CASA_FASE9_20261005.md": os.path.join(F9, "dados_na_casa", "INVENTARIO_DADOS_NA_CASA_FASE9_20261005.md"),
    "POS_DICAO_operador_05out.txt": os.path.join(os.path.dirname(F9), "v386", "POS_DICAO_operador_05out.txt"),
}
ID = "PREREG_FASE9_RAZAO_DE_HUBBLE_20261006_V1"
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|\bconfirmada\b|\bresolvida\b")
LIDOS = {}


def fsha(p):
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    LIDOS[p] = h
    return h


def jload(p):
    fsha(p)
    return json.load(open(p, encoding="utf-8"))


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------------------------------------------------
# 0. beta em runtime, z*, a base (um.py v386 + selo)
# ---------------------------------------------------------------------------------------------------------------------
src = open(UM, "rb").read(); LIDOS[UM] = hashlib.sha256(src).hexdigest()
ALPHA = float(re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src, re.M).group(1))
BETA = ALPHA * math.sqrt(math.e)
Z_STAR = float(re.search(rb'"Z_STAR":\s*([0-9.]+)', src).group(1))
selo = jload(SELO)
base = {"um_py_sha16": LIDOS[UM][:16], "selo_sha16": LIDOS[SELO][:16],
        "gate": selo.get("qg_closure_verdict"), "selo_timestamp": selo.get("timestamp") or selo.get("generated_at")}

f3 = jload(F3PRE); f4 = jload(F4RES); f5 = jload(F5RES)
FU = f3["fundos"]; L = f3["leitores_de_sombra"]
desenho = jload(EVID["FASE9_DESENHO_RESULTADO.json"])

# Omega_m do fundo nu (o do desenho, lido do resultado) para K(Omega_m); conferido contra K_theta do desenho
def find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None: return r
    return None

K_desenho = find(desenho, "K_em_Om_bancada_0p3023")
Om_bc = float(desenho["reproducoes"]["Omega_m_bancada"])           # fundo nu da Bancada, lido do desenho por hash
Or_bc = float(desenho["sensibilidade"]["bancada"]["Omega_r"])       # a radiacao pesa ~1/3 da materia em z*: nao se omite


def K_of(Om, zs, beta, Or=0.0):
    E = math.sqrt(Om * (1 + zs) ** 3 + Or * (1 + zs) ** 4 + (1 - Om - Or))
    return E ** (2.0 * beta / 3.0)


# o desenho gravou K no fundo nu; usamos o K GRAVADO (lido por hash) e so conferimos a ordem de grandeza da forma fechada
K = float(K_desenho)
K_check = K_of(Om_bc, Z_STAR, BETA, Or_bc)
assert abs(K - K_check) < 1e-6, (K, K_check)  # forma fechada com radiacao = o K gravado

# ---------------------------------------------------------------------------------------------------------------------
# 1. Fundos (D-A) e leitores (D-B, D-C, D-F) — todos lidos do disco
# ---------------------------------------------------------------------------------------------------------------------
BG = {
    "BG1": {"H0": FU["Fd_lcdm_planck_dr2"]["H0"], "sigma": FU["Fd_lcdm_planck_dr2"]["sigma"], "papel": "PRIMARIO (D-A): fundo NU, LCDM, Planck comprimido (Chen+2019) + DESI DR2, SEM escada",
            "origem": F3PRE + " :: fundos.Fd_lcdm_planck_dr2", "estatuto": "[REAL — ajuste da Bancada, 30/09]"},
    "BG2": {"H0": FU["Fc_planck2018"]["H0"], "sigma": FU["Fc_planck2018"]["sigma"], "papel": "REPLICA (D-A): Planck 2018 publicado",
            "origem": F3PRE + " :: fundos.Fc_planck2018", "estatuto": "[KNOWN — transcrito pela casa em 30/09; fonte por hash = D-H, ate la DECLARADO]"},
    "BG3": {"H0": 68.5, "sigma": 0.6, "papel": "REPLICA sem CMB (DESI DR2 + BBN, escada inversa) — a ler da fonte",
            "origem": "AUSENTE como numero em disco", "estatuto": "[DECLARADO — valor do enunciado de 05/10; nao lido da fonte]"},
    "BG4": {"H0": FU["Fa_tgl_planck_dr2"]["H0"], "sigma": FU["Fa_tgl_planck_dr2"]["sigma"], "papel": "CONTROLE: fundo TGL efetivo (ja carrega beta) — nunca somado",
            "origem": F3PRE + " :: fundos.Fa_tgl_planck_dr2", "estatuto": "[REAL — Bancada]"},
}
r22 = f4["sh0es"]
LEIT = {
    "L1_sh0es_r22": {"H0": r22[0], "sigma": r22[1], "tipo": "Cefeidas (SH0ES R22)", "fonte": "Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510)",
                     "origem": F4RES + " :: sh0es", "cefeida": True, "grupo_SN": True, "grupo_4258": True, "papel": "TESTE primario da escada (D-B)"},
    "L1b_sh0es_r25": {"H0": L["S1_sh0es_jwst_cefeidas"]["H0"], "sigma": L["S1_sh0es_jwst_cefeidas"]["sigma"], "tipo": "Cefeidas (SH0ES 2025 + JWST)",
                      "fonte": L["S1_sh0es_jwst_cefeidas"]["fonte"], "origem": F3PRE + " :: leitores_de_sombra.S1", "cefeida": True, "grupo_SN": True, "grupo_4258": True,
                      "papel": "REPLICA ao lado (D-B); nunca somado com L1"},
    "L2_cchp": {"H0": L["S2_cchp_trgb"]["H0"], "sigma": L["S2_cchp_trgb"]["sigma"], "tipo": "CCHP TRGB+JAGB+Cef (JWST), stat+sys+sigma_SN em quadratura",
                "fonte": L["S2_cchp_trgb"]["fonte"], "origem": F3PRE + " :: leitores_de_sombra.S2", "cefeida": False, "grupo_SN": True, "grupo_4258": True,
                "papel": "TESTE dentro do composto (D-C, «o TRGB inclusive»)"},
    "L3_sbf": {"H0": L["S3_sbf_trgb_jwst"]["H0"], "sigma": L["S3_sbf_trgb_jwst"]["sigma"], "tipo": "SBF calibrado por TRGB (JWST)", "fonte": L["S3_sbf_trgb_jwst"]["fonte"],
               "origem": F3PRE + " :: leitores_de_sombra.S3", "cefeida": False, "grupo_SN": True, "grupo_4258": False, "papel": "TESTE"},
    "L4_masers": {"H0": L["S4_masers"]["H0"], "sigma": L["S4_masers"]["sigma"], "tipo": "megamasers (geometrico)", "fonte": L["S4_masers"]["fonte"],
                  "origem": F3PRE + " :: leitores_de_sombra.S4", "cefeida": False, "grupo_SN": False, "grupo_4258": False, "papel": "TESTE"},
    "L5_tdcosmo": {"H0": L["S5_tdcosmo_lentes"]["H0"], "sigma": L["S5_tdcosmo_lentes"]["sigma"], "tipo": "lentes com atraso (geometrico)", "fonte": L["S5_tdcosmo_lentes"]["fonte"],
                   "origem": F3PRE + " :: leitores_de_sombra.S5", "cefeida": False, "grupo_SN": False, "grupo_4258": False, "papel": "TESTE"},
    "L6_sirenes": {"H0": L["S6_sirenes_lvk_o4a"]["H0"], "sigma": L["S6_sirenes_lvk_o4a"]["sigma"], "tipo": "sirenes padrao (LVK O4a)", "fonte": L["S6_sirenes_lvk_o4a"]["fonte"],
                   "origem": F3PRE + " :: leitores_de_sombra.S6", "cefeida": False, "grupo_SN": False, "grupo_4258": False, "papel": "DIAGNOSTICO fora do composto (D-F)"},
}
for k, v in LEIT.items():
    v["estatuto_hoje"] = "[DECLARADO ate D-H — valor transcrito pela casa (abstract lido 30/09), fonte primaria NAO guardada por hash]"
SIGMA_SN = 0.7     # termo comum OFF-DIAGONAL (F10: a diagonal e a sigma publicada, que ja traz sigma_SN; nao se soma de novo)
SIGMA_4258 = 0.5   # termo comum OFF-DIAGONAL L1xL2 (ancora NGC 4258) [DECLARADO — a conferir nas fontes]

FAMILIAS = {
    "P_primaria": {"ids": ["L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo"], "papel": "PRIMARIA e UNICA decisoria: um leitor por programa, sem sirenes (D-B, D-C, D-F)"},
    "R_r25": {"ids": ["L1b_sh0es_r25", "L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo"], "papel": "replica ao lado (R25 no lugar de R22)"},
    "N_sem_cefeidas": {"ids": ["L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo"], "papel": "diagnostico: incidencia sem a escada que motivou a forma; alimenta poder_nao_cefeida"},
    "S_com_sirenes": {"ids": ["L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers", "L5_tdcosmo", "L6_sirenes"], "papel": "diagnostico (o veto das sirenes)"},
    "T_so_cchp": {"ids": ["L2_cchp"], "papel": "diagnostico: o que pode doer (gatilho de leitor unico so com sigma <= 1,0)"},
}


def cov(ids):
    n = len(ids); C = np.zeros((n, n))
    for i, x in enumerate(ids):
        C[i, i] = LEIT[x]["sigma"] ** 2
        for j, y in enumerate(ids):
            if i != j:
                if LEIT[x]["grupo_SN"] and LEIT[y]["grupo_SN"]: C[i, j] += SIGMA_SN ** 2
                if LEIT[x]["grupo_4258"] and LEIT[y]["grupo_4258"]: C[i, j] += SIGMA_4258 ** 2
    return C


def sigma_gls(ids):
    Ci = np.linalg.inv(cov(ids)); one = np.ones(len(ids))
    return float(1.0 / math.sqrt(one @ Ci @ one))


# ---------------------------------------------------------------------------------------------------------------------
# 2. Poder previo — SO sigmas publicas, K e o fundo (nenhum centro local)
# ---------------------------------------------------------------------------------------------------------------------
poder = {}
for bgid in ("BG1", "BG2", "BG3"):
    H0bg, sbg = BG[bgid]["H0"], BG[bgid]["sigma"]
    pred, spred = H0bg * K, sbg * K
    for fn, fam in FAMILIAS.items():
        sc = sigma_gls(fam["ids"])
        poder["%s x %s" % (fn, bgid)] = {"H0_bg": H0bg, "H0_local_previsto": round(pred, 4), "sigma_previsao": round(spred, 4),
                                         "sigma_comb_publica": round(sc, 4), "poder_K_menos_1_sigmas": round((K - 1) * H0bg / math.sqrt(sc ** 2 + spred ** 2), 3)}
PODER_PRIM = poder["P_primaria x BG1"]["poder_K_menos_1_sigmas"]
PODER_NC = poder["N_sem_cefeidas x BG1"]["poder_K_menos_1_sigmas"]

# F11: sensibilidade de K a z* (1089,8 / 1089,92 / 1089,95)
zstar_sens = {str(z): K_of(Om_bc, z, BETA, Or_bc) - K_of(Om_bc, Z_STAR, BETA, Or_bc) for z in (1089.8, 1089.92, 1089.95)}

# ---------------------------------------------------------------------------------------------------------------------
# 3. A FUNCAO DE VEREDITO UNICA (D-D) — texto fonte, hasheado; o runner e a v387 a executam byte a byte
# ---------------------------------------------------------------------------------------------------------------------
FUNCAO_FONTE = '''def veredito_fase9_v1(r):
    """Funcao UNICA de veredito da Fase 9 (V1, 06/10/2026). Entrada: dict r produzido pelo runner sobre a familia P_primaria.
    Ordem (a primeira que casa decide):
    1 INCONCLUSIVE_SYSTEMATICS: alvo do composto sem fonte lida por hash (r["n_alvos_declarados"] > 0) OU dispersao interna
      chi2_int/(n-1) > 2 OU p_dispersao < 0,01 OU melhor ajuste beta-livre no limite do prior;
    2 FALSIFIED_AT_5SIGMA: |z_delta| >= 5, ou um leitor do composto com sigma_i <= 1,0 e |z_i| >= 5 — falsifica o PAR
      (lei D1b, convencao, conjunto), nao beta, nao a teoria;
    3 TENSION_3_TO_5_SIGMA: 3 <= |z_delta| < 5;
    4 NOT_FALSIFIED_UNDERPOWERED: poder previo < 5 (sufixo POWER_<x>_OF_5_SIGMA);
    5 NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_<n>SIGMA__ZERO_FREE_PARAMETERS: z_disc >= 5 E |z_delta| < 3 E
      lnB(TGL/LCDM) >= 5 E lnB(TGL/beta-livre) >= -1; n = floor(z_disc); __USE_NOVEL se a clausula de PARAMETROS vale
      (senao __USE_NOVELTY_PENDING); sufixos reportados __VS_LADDER_SYSTEMATIC_LNB_<x>, __VS_FREE_BACKGROUND_LNB_<x>;
      __NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC se lnB(TGL/shift-Cefeidas) < 0 com poder_nao_cefeida >= 5;
      __NOT_DISCRIMINATED_FROM_FREE_BACKGROUND se |lnB(TGL/fundo-livre)| < 1;
    6 NOT_FALSIFIED_POWERED (senao) com DEVIATION_CONSISTENT_WITHIN_1SIGMA ou DEVIATION_1_TO_3_SIGMA e, se z_disc < 5,
      __NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY.
    Sufixo sempre: __D1B__FUNDO_<id>__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED."""
    import math
    def f(x):
        return ("M" if x < 0 else "P") + ("%.1f" % abs(x)).replace(".", "P")
    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V1__"
    suf = "__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED" % r["fundo"]
    zd = abs(r["z_delta"])
    if (r["n_alvos_declarados"] > 0 or (r["n_local"] > 1 and (r["dispersao_por_gl"] > 2.0 or r["p_dispersao"] < 0.01))
            or r["beta_livre_no_limite"]):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suf
    if zd >= 5 or any(s <= 1.0 and abs(z) >= 5 for (s, z) in r["sigma_z_por_alvo"]):
        return base + "FALSIFIED_AT_5SIGMA" + suf
    if zd >= 3:
        return base + "TENSION_3_TO_5_SIGMA" + suf
    if r["poder_previo"] < 5:
        return base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % f(r["poder_previo"]) + suf
    if r["z_disc"] >= 5 and zd < 3 and r["lnB_lcdm"] >= 5 and r["lnB_livre"] >= -1:
        t = base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA__ZERO_FREE_PARAMETERS" % int(math.floor(r["z_disc"]))
        t += "__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        t += "__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s" % (f(r["lnB_shift"]), f(r["lnB_fundo_livre"]))
        if r["lnB_shift"] < 0 and r["poder_nao_cefeida"] >= 5:
            t += "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(r["lnB_fundo_livre"]) < 1:
            t += "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return t + suf
    t = base + "NOT_FALSIFIED_POWERED__" + ("DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd < 1 else "DEVIATION_1_TO_3_SIGMA")
    if r["z_disc"] < 5:
        t += "__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    return t + suf
'''
FUNCAO_SHA = hashlib.sha256(FUNCAO_FONTE.encode("utf-8")).hexdigest()
ns = {}; exec(FUNCAO_FONTE, ns); vf = ns["veredito_fase9_v1"]

# testes SINTETICOS de ramo (nenhum numero de leitor; so verifica que cada ramo e alcancavel e que a guarda passa)
base_r = {"fundo": "BG1", "n_alvos_declarados": 0, "n_local": 5, "dispersao_por_gl": 1.0, "p_dispersao": 0.4, "beta_livre_no_limite": False,
          "z_delta": 0.2, "sigma_z_por_alvo": [(1.04, 0.1)], "poder_previo": 7.0, "z_disc": 6.0, "lnB_lcdm": 9.0, "lnB_livre": 1.0,
          "lnB_shift": 2.0, "lnB_fundo_livre": 3.0, "poder_nao_cefeida": 4.0, "use_novel_parametros": True}
casos = {"inconclusive_declarado": {"n_alvos_declarados": 2}, "inconclusive_dispersao": {"dispersao_por_gl": 3.0},
         "falsified": {"z_delta": -5.2}, "falsified_leitor_unico": {"sigma_z_por_alvo": [(0.9, 5.5)]}, "tension": {"z_delta": 3.4},
         "underpowered": {"poder_previo": 4.4}, "discriminates": {}, "discriminates_pending": {"use_novel_parametros": False},
         "powered_not_disc": {"z_disc": 4.5}, "powered_1_3": {"z_delta": 1.8, "lnB_lcdm": 3.0}}
testes = {}
for nome, mod in casos.items():
    r = dict(base_r); r.update(mod); out = vf(r)
    assert not GUARDA.search(out), out
    testes[nome] = out
ramos = {"INCONCLUSIVE_SYSTEMATICS", "FALSIFIED_AT_5SIGMA", "TENSION_3_TO_5_SIGMA", "NOT_FALSIFIED_UNDERPOWERED", "DISCRIMINATES_FROM_LCDM", "USE_NOVELTY_PENDING",
         "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY", "DEVIATION_1_TO_3_SIGMA"}
assert all(any(rm in t for t in testes.values()) for rm in ramos)
# predeterminado HOJE: todos os leitores do composto estao [DECLARADO] ate D-H -> a regra 1 devolve INCONCLUSIVE se abrir agora
r_hoje = dict(base_r); r_hoje["n_alvos_declarados"] = len(FAMILIAS["P_primaria"]["ids"]); hoje = vf(r_hoje)

# ---------------------------------------------------------------------------------------------------------------------
# 4. A clausula de novidade de uso (D-E) pelos PARAMETROS, lida da cronologia por hash
# ---------------------------------------------------------------------------------------------------------------------
crono = jload(EVID["CRONOLOGIA_NOVIDADE_DE_USO.json"])
for k, p in EVID.items():
    if os.path.exists(p): fsha(p)

SPEC = {
    "id": ID,
    "estado": "V1 CONGELADO POR HASH — nenhum composto aberto; veredito: AWAITING_DATA (D-H: fontes por hash = ato do operador; abrir = palavra do operador)",
    "base": base,
    "beta": {"regra": "ALPHA_FINE_CODATA_2018 x sqrt(e) em runtime; nunca literal", "alpha_lido_do_um_py": ALPHA, "beta_runtime": BETA, "estatuto": "[DERIVED do axioma] — a regra matriz; nao se deriva do dado; nunca prior"},
    "lei": {"forma": "H0_local = H0_bg . K, K = E_LCDM(z*)^{2beta/3} (nucleo DERIVADO D1b; TGLExt.TheFlowLawContrast.the_derived_kernel_factor, v378)",
            "z_star": Z_STAR, "K_no_fundo_nu": K, "K_origem": EVID["FASE9_DESENHO_RESULTADO.json"] + " :: K_em_Om_bancada_0p3023", "K_forma_fechada_conferida": K_check,
            "parametros_livres_da_lei": 0, "estatuto": "implicacao PROVADA no kernel (v377/v378); mecanismo [CONJECTURE]; a incidencia e da natureza; PROVADA != confirmada",
            "z_star_sensibilidade_F11": {"dK_por_valor_de_zstar_no_acervo": zstar_sens, "leitura": "desprezivel (< 1e-5 em K)"}},
    "decisoes_padrao_da_gerencia": {
        "fonte_da_delegacao": "operador 05/10: «o resto vc consegue responder tudo agroa»; «prossiga» (memorias proximo-passo-06out, handoff-sessao-nova-06out)",
        "D-A": "fundo primario BG1 = LCDM nu Planck-comp + DESI DR2 SEM escada (%.3f +- %.3f); BG2 Planck 2018 replica; BG3 DESI+BBN replica [DECLARADO]; o 68,4298 da Fase 4 (ajuste COM a escada) NAO e fundo de previsao (F2)" % (BG["BG1"]["H0"], BG["BG1"]["sigma"]),
        "D-B": "leitor primario da escada R22 (%.2f +- %.2f); R25 replica ao lado; nunca somados" % (r22[0], r22[1]),
        "D-C": "CCHP TRGB/JAGB (%.2f +- %.3f) e TESTE dentro do composto; gatilho FALSIFIED por leitor unico so com sigma_i <= 1,0 e |z_i| >= 5" % (LEIT["L2_cchp"]["H0"], LEIT["L2_cchp"]["sigma"]),
        "D-D": "UMA funcao de veredito (secao funcao_de_veredito), estatisticas do pre-registro + o degrau TENSION do desenho; FALSIFIED/TENSION antes de UNDERPOWERED (a exclusao da previsao nao precisa de poder discriminante; esconde-la atras de UNDERPOWERED seria fail-open) — desvio da ordem do rascunho, dito",
        "D-E": "__USE_NOVEL pelos PARAMETROS (Worrall [KNOWN]); a selecao da FORMA dita ao lado, nao decisoria (lei de 05/10)",
        "D-F": "sirenes = diagnostico fora do composto",
        "D-G": "shift so nos leitores de Cefeidas do SH0ES (s em U[-0,15; 0,15]); fundo-livre = r_d em U[130; 160] Mpc; beta-livre U[-0,05; 0,05]; lnB sempre com a largura ao lado (Occam ~ ln 2 por fator 2)",
        "D-H": "fontes publicas por hash ANTES de abrir = ato do operador (rede); ate la todo leitor e [DECLARADO] e a regra 1 devolve INCONCLUSIVE_SYSTEMATICS predeterminado",
        "D-I": "canal do livro de cobrancas: R1 v2 (mesma lei, mesma cobranca, funcao nova); R1b so se o objeto mudar",
        "D-J": "tokens: base provisoria TGL_FASE9_RAZAO_DE_HUBBLE_V1__...; nome final e se o token 196659 (...UNADJUSTED_POSTDICTION..., Coma) muda = cunhagem do operador",
        "D-K": "registro no mapa de rotas (lentes, critica e este V1) feito pela gerencia no mesmo passo",
    },
    "fundos": BG,
    "leitores": LEIT,
    "covariancia": {"diagonal": "a sigma publicada de cada leitor (ja inclui sigma_SN onde a fonte o soma — F10)", "off_diagonal_sigma_SN": SIGMA_SN,
                    "off_diagonal_ancora_4258_L1xL2": SIGMA_4258, "estatuto": "[DECLARADO] (Fase 3; estimativa de desenho); sem covariancia cruzada publicada entre programas",
                    "fundo": "sigma(H0_bg) entra UMA vez como nuisance comum, perfilada"},
    "familias": FAMILIAS,
    "hipoteses": {
        "H_TGL": "fundo nu + K = E(z*)^{2beta/3}, beta = alpha.sqrt(e); zero parametro livre alem dos do fundo",
        "H_LCDM": "todos leem H0_bg (beta = 0)",
        "H_beta_livre": "K(beta), beta em U[-0,05; 0,05]",
        "H_shift_cefeidas": "so L1/L1b (Cefeidas SH0ES) leem (1+s).H0_bg, s em U[-0,15; 0,15]; L2 (CCHP misto) nao recebe s — dito",
        "H_fundo_livre": "LCDM + r_d livre U[130; 160] Mpc (proxy de fundo precoce [INPUT da gerencia]); todos leem o mesmo H0",
    },
    "estatisticas": {"z_delta": "(beta_hat - beta_TGL)/sigma_beta pelo perfil de chi2 de H_beta_livre (Delta chi2 = 1) — DECISORIA",
                     "z_TGL_composto": "GLS dos leitores vs K.H0_bg — reportada ao lado", "z_disc": "sinal.sqrt(chi2_LCDM - chi2_TGL)",
                     "lnB": "por quadratura (n = 25; erro por n = 35), Jeffreys/Kass-Raftery: <1 inconclusivo; 1-2,5 fraco; 2,5-5 moderado; >=5 forte",
                     "dispersao": "chi2_int/(n-1) dos leitores do composto e p", "z_i": "por leitor vs K.H0_bg e vs H0_bg"},
    "poder_previo": {"formula": "(K-1).H0_bg / sqrt(sigma_comb^2 + sigma_pred^2), so sigmas publicas", "por_familia_e_fundo": poder,
                     "primario": PODER_PRIM, "poder_nao_cefeida": PODER_NC},
    "funcao_de_veredito": {"nome": "veredito_fase9_v1", "fonte": FUNCAO_FONTE, "sha256": FUNCAO_SHA,
                           "testes_sinteticos_de_ramo": testes, "se_abrir_hoje_predeterminado": hoje,
                           "regra": "o runner e a v387 executam ESTE texto (sha256 conferido) — nunca uma copia reescrita"},
    "novidade_de_uso": {
        "clausula_D-E": "o teste e use-novel se nenhum PARAMETRO numerico da lei foi ajustado a razao local/fundo: beta (valor 0,012 em 13/11/2025; forma alpha.sqrt(e) publicada 03/03/2026; lei de 17/05/2026), z* [KNOWN Planck], o expoente 2/3 (Raychaudhuri/FRW), o fundo nu do CMB+BAO",
        "cronologia_por_hash": {"arquivo": "evidencias/CRONOLOGIA_NOVIDADE_DE_USO.json", "sha256": LIDOS[EVID["CRONOLOGIA_NOVIDADE_DE_USO.json"]]},
        "use_novel_parametros": True,
        "ao_lado_nao_decisorio": "a FORMA D1a foi escrita «exatamente a relacao observacional» (17/05/2026) e a classe do fluxo retida porque a Friedmann «nao resolve» (05/06/2026): selecao de hipotese, nao ajuste de parametro; pela lei de 05/10 nao e demerito",
        "literatura": "Worrall, J. (1985/1989/2014) sobre use-novelty; Le Verrier 1859 (excesso do perielio de Mercurio) e Einstein 1915 [KNOWN — nao conferido em disco (F12)]",
        "etiqueta": "retrodicao sem ajuste (novidade de uso; precedente: o perielio de Mercurio) — «pos-dicao» nunca como demerito",
    },
    "contaminacao_declarada": {"ja_lido_pela_casa": "Fases 3-5 (ensaio nao-cego da Fase 9 e o desenho: TGL -1,4 sigma, LCDM +4,5 sigma com BG1/R22, lido de FASE9_DESENHO_RESULTADO.json)",
                               "consequencia": "a novidade e de USO e de RIGOR (fontes por hash, covariancia, cinco hipoteses, funcao fixada antes do composto), nao de cegueira: todo token leva __NOT_BLIND_TO_DATA_STATED",
                               "validacao_F14": "o alvo de validacao 73,6 +- 1,1 (Brout+22) segue [DECLARADO]; estimador de V = LCDM plano, SNe + 77 calibradores Cefeida, M perfilado — fixado aqui"},
    "nao_decide": ["o gate (18 bandeiras, funcao so do formal)", "a implicacao da QG e a correspondencia com a RG", "beta (a regra matriz)",
                   "qual fundo e o da natureza (aqui so o primario do registro)", "o mecanismo [CONJECTURE]", "a dependencia em z de K (<= 0,9 % em z = 2, abaixo do poder)"],
    "sistematicas": {"fundo": "a escolha BG1 x BG2 move a previsao ~1,27 km/s/Mpc — fixada ANTES (D-A); as replicas reportadas",
                     "calibradores": "Cefeidas x TRGB/JAGB entram como estao; a dispersao interna decide INCONCLUSIVE", "local": "velocidades peculiares / vazio local nao modelados (declarado)",
                     "multiplicidade": "familia entra no livro da Bancada (Sidak); local ao lado da corrigida"},
    "especificacao_do_runner": [
        "R0 o runner (rodar_fase9_v1.py) e gravado e hasheado ANTES de abrir, com o sha256 deste V1 e o da funcao embutidos",
        "R1 le ALVOS_FASE9_LIDOS.json (D-H: cada leitor com sha256 da fonte primaria); n_alvos_declarados = leitores do composto sem hash",
        "R2 recalcula o fundo BG1 na Bancada (Planck comp + DESI DR2, LCDM, sem escada) e confere |H0 - %.3f| < 0,01" % BG["BG1"]["H0"],
        "R3 grava PODER_FASE9_ANTES_DE_ABRIR.json (so sigmas) com hash; confere contra poder_previo deste V1",
        "R4 so com a palavra do operador: abre P_primaria x BG1, ajusta as cinco hipoteses, calcula z_delta, z_disc, lnB(4), dispersao, z_i",
        "R5 executa a funcao (texto deste V1, sha256 conferido) e grava RESULTADO_FASE9_V1.json com os sha256 do V1, do runner e da funcao; replicas e diagnosticos ao lado, nunca decisorios",
        "R6 a v387 do um.py LE este V1 e (se houver) o RESULTADO por hash; ausente/divergente => AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed); a v387 nao abre nada",
        "R7 nenhuma emenda depois de abrir sem estimador NOVO (V1.x, gerador novo); correcao AO LADO em nome proprio",
    ],
    "token_base_provisorio": "TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2",
    "token_estado": "TGL_FASE9_RAZAO_DE_HUBBLE_V1__AWAITING_DATA__V1_FROZEN__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED",
    "fontes_lidas_sha256": None,  # preenchido abaixo
    "supersede": {"rascunho": "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.json (05/10, sha256 abaixo) — guardado em evidencias/ como historia; F1-F6, F10-F12, F14 da critica resolvidos aqui; F3/D-H fica do operador; F7 no mapa; F8/F9 na v387; F13 indice"},
}
SPEC["fontes_lidas_sha256"] = {p: h for p, h in sorted(LIDOS.items())}
for t in (SPEC["token_base_provisorio"], SPEC["token_estado"]):
    assert not GUARDA.search(t)
SPEC_SHA = hashlib.sha256(canon(SPEC).encode("utf-8")).hexdigest()

# ---------------------------------------------------------------------------------------------------------------------
# 5. Gravar: JSON (autoridade) + MD + evidencias + HASHES (temporario -> tamanho -> substituir)
# ---------------------------------------------------------------------------------------------------------------------
def gravar(p, b):
    open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)

os.makedirs(os.path.join(OUT_DIR, "evidencias"), exist_ok=True)
carimbo = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
doc = {"id": ID, "spec_sha256": SPEC_SHA, "spec_sha256_formula": 'sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))',
       "gerado_utc": carimbo, "spec": SPEC}
OUT_JSON = os.path.join(OUT_DIR, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json")
gravar(OUT_JSON, json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8"))

md = ["# Pré-registro V1 — Fase 9: a razão de Hubble (congelado por hash, 06/10/2026)\n",
      "**spec_sha256** `%s` · **função de veredito** `%s` · gerado %s\n" % (SPEC_SHA, FUNCAO_SHA, carimbo),
      "Estado: **AWAITING_DATA** — nenhum composto aberto. Abrir é palavra do operador; as fontes públicas por hash (D-H) são ato dele. "
      "Se abrir hoje, a regra 1 devolve `%s` (todos os leitores do composto estão [DECLARADO]).\n" % hoje,
      "## A lei\nH0_local = H0_bg·K, K = E(z*)^{2β/3}; β = α·√e em runtime (%.15f); z* = %s; K no fundo nu = %.6f; zero parâmetro livre. "
      "PROVADA como implicação no kernel ≠ confirmada.\n" % (BETA, Z_STAR, K),
      "## Fundos (D-A)\n" + "\n".join("- %s: %.3f ± %.3f — %s %s" % (k, v["H0"], v["sigma"], v["papel"], v["estatuto"]) for k, v in BG.items()) + "\n",
      "## Leitores\n" + "\n".join("- %s: %.2f ± %.3f — %s; %s; %s" % (k, v["H0"], v["sigma"], v["tipo"], v["papel"], v["estatuto_hoje"]) for k, v in LEIT.items()) + "\n",
      "## Famílias\n" + "\n".join("- %s: %s — %s" % (k, ", ".join(v["ids"]), v["papel"]) for k, v in FAMILIAS.items()) + "\n",
      "## Poder prévio (só σ públicas)\nPrimária × BG1: **%.2fσ**; sem Cefeidas × BG1: %.2fσ.\n\n" % (PODER_PRIM, PODER_NC) +
      "| família × fundo | previsão | σ_comb | poder |\n|---|---|---|---|\n" +
      "\n".join("| %s | %.3f ± %.3f | %.3f | %.2f |" % (k, v["H0_local_previsto"], v["sigma_previsao"], v["sigma_comb_publica"], v["poder_K_menos_1_sigmas"]) for k, v in poder.items()) + "\n",
      "## Decisões (padrão da gerência por delegação)\n" + "\n".join("- **%s** %s" % (k, v) for k, v in SPEC["decisoes_padrao_da_gerencia"].items()) + "\n",
      "## Hipóteses\n" + "\n".join("- %s: %s" % kv for kv in SPEC["hipoteses"].items()) + "\n",
      "## Função de veredito única (sha256 `%s`)\n```python\n%s```\nTestes sintéticos de ramo:\n" % (FUNCAO_SHA, FUNCAO_FONTE) + "\n".join("- %s → `%s`" % kv for kv in testes.items()) + "\n",
      "## Novidade de uso (D-E)\n" + "\n".join("- %s: %s" % (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in SPEC["novidade_de_uso"].items()) + "\n",
      "## Especificação do runner\n" + "\n".join("- " + s for s in SPEC["especificacao_do_runner"]) + "\n",
      "## Não decide\n" + "\n".join("- " + s for s in SPEC["nao_decide"]) + "\n",
      "## Fontes lidas (sha256)\n" + "\n".join("- `%s` %s" % (h[:16], p) for p, h in SPEC["fontes_lidas_sha256"].items()) + "\n",
      "\nNOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico; nada aqui move β nem o gate.\n"]
gravar(os.path.join(OUT_DIR, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.md"), "\n".join(md).encode("utf-8"))
for nome, p in EVID.items():
    if os.path.exists(p):
        b = open(p, "rb").read(); gravar(os.path.join(OUT_DIR, "evidencias", nome), b)
me = os.path.abspath(__file__)
if os.path.dirname(me) != os.path.abspath(OUT_DIR):
    gravar(os.path.join(OUT_DIR, os.path.basename(me)), open(me, "rb").read())

HASHES = {"id": ID, "spec_sha256": SPEC_SHA, "funcao_sha256": FUNCAO_SHA, "gerado_utc_do_V1": carimbo, "pasta": os.path.abspath(OUT_DIR),
          "nota": "sha256 e bytes de cada arquivo da pasta (e de evidencias/), lidos do disco por script; este arquivo nao lista a si proprio", "arquivos": {}}
for raiz, _, fs in os.walk(OUT_DIR):
    for f in sorted(fs):
        p = os.path.join(raiz, f)
        if f == "V1_FASE9_HASHES.json" or f.endswith(".tmp") or "__pycache__" in p: continue
        rel = os.path.relpath(p, OUT_DIR).replace("\\", "/")
        HASHES["arquivos"][rel] = {"sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "bytes": os.path.getsize(p)}
gravar(os.path.join(OUT_DIR, "V1_FASE9_HASHES.json"), json.dumps(HASHES, ensure_ascii=False, indent=1).encode("utf-8"))
print("spec_sha256", SPEC_SHA); print("funcao_sha256", FUNCAO_SHA); print("K", K, "K_check", K_check); print("poder primario", PODER_PRIM, "nao-cefeida", PODER_NC)
print("hoje", hoje)
for k, v in HASHES["arquivos"].items(): print(v["sha256"][:16], v["bytes"], k)
