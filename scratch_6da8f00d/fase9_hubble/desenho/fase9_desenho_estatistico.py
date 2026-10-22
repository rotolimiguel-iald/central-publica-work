# -*- coding: utf-8 -*-
"""
fase9_desenho_estatistico.py — O DESENHO ESTATÍSTICO DO TESTE DISCRIMINANTE (Fase 9: a razão de Hubble).
Lente: «desenho» (05/10/2026). Só leitura fora de scratchpad/fase9_hubble/desenho/. Não roda o um.py; não baixa dado.

Régua: β nunca literal (α lido do um.py por regex × √e em runtime); todo número lido de arquivo com sha256;
NOT_FALSIFIED nunca é CONFIRMED (guarda por regex nas saídas); a RG/ΛCDM é o limite clássico.
Lei da prova da casa (operador, 05/10/2026): «pós-dição» nunca é demérito; o critério é a NOVIDADE DE USO
(nenhum parâmetro da teoria ajustado ao dado); o pré-registro é do TESTE (da FUNÇÃO de veredito), não da ignorância.

O que o script faz:
  (a) recompute K = E(z*)^{2β/3} com o MESMO E(z) do um.py v378 (_v378_lcdm_E) e reproduz 1.083807 (Bancada, θ̂_TGL da Fase 4),
      1.083977 (Planck 2018, core) e 1.083976 (reanálise, og = 2.469e-5/T^4); sensibilidade a Ω_m, z*, h, N_eff, β.
  (b) os ALVOS lidos do disco (pré-registro da Fase 3; resultados das Fases 4–5) com fonte e estatuto; os ausentes ditos «a ler».
  (c) as hipóteses H_TGL (K fixo), H_ΛCDM (K = 1), H_livre (β livre), H_shift (ε livre), H_EDE-like (fundo deslocado s livre):
      χ² com covariância (perfil analítico em H0_fundo), ln B por integração 1-D sob prior uniforme declarado, BIC, Savage–Dickey.
  (d) o poder (separação TGL↔ΛCDM em σ) e a FUNÇÃO de veredito pré-registrável, aplicada aos alvos públicos (ENSAIO NÃO-CEGO).
  (e) o que as Fases 1–2 obrigam (fundo nu; β só na lei; o empilhado como controle, nunca somado).
  (f) sistemáticas: Cefeidas vs TRGB; z* efetivo; Ω_m do fundo nu; a escolha do fundo (a dominante).
"""
import os, re, sys, json, math, hashlib, datetime, ast
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UM = os.path.join(NOS, "um.py")
CORE = os.path.join(NOS, "um_absoluto.json")
SELO = os.path.join(NOS, "um_absoluto_selo.json")
BANC = r"C:\IALD\Bancada_Um\investigacao"
F3PRE = os.path.join(BANC, "fase3_leitores_h0", "PREREGISTRO_FASE3_LEITORES_20260930.json")
F3REAN = os.path.join(BANC, "fase3_leitores_h0", "REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json")
F3RES = os.path.join(BANC, "fase3_leitores_h0", "RESULTADO_FASE3_LEITORES_20260930.json")
F4RES = os.path.join(BANC, "fase4_desvio_30set", "RESULTADO_FASE4_DESVIO_20260930.json")
F4SMOKE = os.path.join(BANC, "fase4_desvio_30set", "SMOKE_FASE4.json")
F5RES = os.path.join(BANC, "fase5_sh0es_01out", "RESULTADO_FASE5_SH0ES_20261001.json")
POSDICAO = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v386\POS_DICAO_operador_05out.txt"
OUT_JSON = os.path.join(HERE, "FASE9_DESENHO_RESULTADO.json")
OUT_MD = os.path.join(HERE, "FASE9_DESENHO_TABELA.md")

GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
LIDOS = {}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    LIDOS[path] = sha256(path)
    return obj


def find_key(obj, key, _path=""):
    """primeira ocorrência (profundidade) de uma chave num JSON aninhado; devolve (valor, caminho)."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key], _path + "/" + key
        for k, v in obj.items():
            r = find_key(v, key, _path + "/" + str(k))
            if r is not None:
                return r
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            r = find_key(v, key, _path + "[%d]" % i)
            if r is not None:
                return r
    return None


# ----------------------------------------------------------------------------------------------------------------------
# 0. β em runtime (α do um.py por regex), o fundo de Planck 2018 do um.py (_V378_PLANCK) e z* [INPUT] do um.py
# ----------------------------------------------------------------------------------------------------------------------
src = open(UM, "rb").read()
LIDOS[UM] = hashlib.sha256(src).hexdigest()
m = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src, re.M)
ALPHA = float(m.group(1))
BETA = ALPHA * math.sqrt(math.e)                       # a regra: α_CODATA2018 · √e, nunca literal
m = re.search(rb"^_V378_PLANCK\s*=\s*(\{[^\n]*\})", src, re.M)
PLANCK = ast.literal_eval(m.group(1).decode("utf-8"))  # {"H0": 67.36, "ombh2": 0.02237, "omch2": 0.12, "mnu_eV": 0.06, "TCMB": 2.7255, "Neff": 3.046}
m = re.search(rb'"Z_STAR":\s*([0-9.]+)', src)
Z_STAR = float(m.group(1))                              # 1089.95 [INPUT: Planck 2018 z*; o nó da lei]
m = re.search(rb"def _v378_lcdm_E\(z, H0, ombh2, omch2, mnu_eV, TCMB, Neff, og_coef=([0-9.eE+-]+)\)", src)
OG_COEF = float(m.group(1))                             # 4.4814e-7 (o mesmo do um.py / Bancada)


def E_lcdm(z, H0, ombh2, omch2, mnu_eV, TCMB, Neff, og_coef=OG_COEF):
    """réplica exata de um.py::_v378_lcdm_E — E(z) do ΛCDM plano com radiação (fótons + N_eff); ν massivo como matéria, m/93.14."""
    h2 = (H0 / 100.0) ** 2
    og = og_coef * TCMB ** 4
    Or = og * (1.0 + Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)) / h2
    Om = (ombh2 + omch2 + mnu_eV / 93.14) / h2
    OL = 1.0 - Om - Or
    z = np.asarray(z, float)
    return np.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + OL), Om, Or, OL


def K_theta(theta, zs=Z_STAR, beta=BETA, og_coef=OG_COEF):
    E, Om, Or, OL = E_lcdm(zs, theta["H0"], theta["ombh2"], theta["omch2"], theta.get("mnu_eV", PLANCK["mnu_eV"]),
                           theta.get("TCMB", PLANCK["TCMB"]), theta.get("Neff", PLANCK["Neff"]), og_coef)
    return float(E) ** (2.0 * beta / 3.0), float(E), Om, Or


def K_omega(Om, Or, zs=Z_STAR, beta=BETA):
    """K em função direta de (Ω_m, Ω_r) plano — para as derivadas."""
    E2 = Om * (1.0 + zs) ** 3 + Or * (1.0 + zs) ** 4 + (1.0 - Om - Or)
    return E2 ** (beta / 3.0)


# ----------------------------------------------------------------------------------------------------------------------
# 1. Reproduções (o número corrige a frase)
# ----------------------------------------------------------------------------------------------------------------------
core = read_json(CORE)
selo = read_json(SELO)
f4 = read_json(F4RES)
f4s = read_json(F4SMOKE)
f3p = read_json(F3PRE)
f3r = read_json(F3REAN)
f3o = read_json(F3RES)
f5 = read_json(F5RES)

core_dlc, core_dlc_path = find_key(core, "K_D1b_runtime")
core_Ez, _ = find_key(core, "E_z_star")
core_beta, _ = find_key(core, "beta_runtime")
core_P, core_P_path = find_key(core, "P_ladder_d1b")
selo_versao = selo.get("um_version") or selo.get("version") or "?"

P = f4["familias"]["P_dr2_escada"]["nucleos"]["d1b"]
theta_tgl = P["theta_tgl"]
K_banc_lido = P["pontos"]["tgl"]["K"]
H0bg_banc_lido = P["pontos"]["tgl"]["H0"]
theta_lcdm_H0 = P["pontos"]["lcdm"]["H0"]

K_pl, E_pl, Om_pl, Or_pl = K_theta(PLANCK)
K_bc, E_bc, Om_bc, Or_bc = K_theta(theta_tgl)
K_re, E_re, Om_re, Or_re = K_theta(PLANCK, og_coef=2.469e-5 / 2.7255 ** 4)
I_b_pl = (2.0 / 3.0) * math.log(E_pl)
N_star = math.log1p(Z_STAR)

reproducoes = {
    "beta_runtime": BETA, "beta_core_v386": core_beta, "beta_fase4": f4["beta_tgl"], "alpha_lido_um_py": ALPHA,
    "diff_beta_core": abs(BETA - core_beta), "diff_beta_fase4": abs(BETA - f4["beta_tgl"]),
    "z_star_input": Z_STAR, "N_star_nats": N_star, "og_coef_um_py": OG_COEF, "planck_input_um_py": PLANCK,
    "K_planck2018_recomputado": K_pl, "K_planck2018_core": core_dlc, "diff_K_planck": abs(K_pl - core_dlc),
    "E_zstar_recomputado": E_pl, "E_zstar_core": core_Ez, "diff_E": abs(E_pl - core_Ez),
    "I_b_planck_recomputado": I_b_pl, "Omega_m_planck": Om_pl, "Omega_r_planck": Or_pl,
    "K_bancada_fase4_recomputado": K_bc, "K_bancada_fase4_lido": K_banc_lido, "diff_K_bancada": abs(K_bc - K_banc_lido),
    "theta_tgl_fase4_lido": theta_tgl, "Omega_m_bancada": Om_bc, "Omega_m_bancada_lido": P["Omega_m_tgl"],
    "K_reanalise_recomputado": K_re, "K_reanalise_lido": f3r["K_D1b"], "diff_K_reanalise": abs(K_re - f3r["K_D1b"]),
    "K_smoke_fase4_lido": f4s["K_b"], "K_D1a_recomputado": (1.0 + Z_STAR) ** BETA, "K_D1a_lido": f4s["K_d1a"],
    "core_v386_P_ladder_d1b": core_P, "core_path": core_P_path,
    "H0_local_previsto_fase4_recomputado": H0bg_banc_lido * K_bc, "H0_local_fase4_lido": P["pontos"]["tgl"]["H0_local"],
    "gate": "K(Planck) e K(θ̂ Bancada) abaixo de 1e-9 ⟹ o modelo E(z) daqui É o do um.py/Bancada; K é reproduzido, não copiado; a reanálise (K por trapézio na grade da Fase 3) confere a 1e-6 (precisão do integrador dela, não deste modelo)",
    "ok": (abs(K_pl - core_dlc) < 1e-9 and abs(K_bc - K_banc_lido) < 1e-9 and abs(K_re - f3r["K_D1b"]) < 1e-6
           and abs(BETA - f4["beta_tgl"]) < 1e-12),
}

# ----------------------------------------------------------------------------------------------------------------------
# 1b. Sensibilidade de K (derivadas numéricas centrais) — em θ̂ da Bancada e em Planck 2018
# ----------------------------------------------------------------------------------------------------------------------
def sens(theta, label):
    K0, E0, Om0, Or0 = K_theta(theta)
    h = 1e-4
    dK_dOm = (K_omega(Om0 + h, Or0) - K_omega(Om0 - h, Or0)) / (2 * h)
    dK_dOr = (K_omega(Om0, Or0 + 1e-7) - K_omega(Om0, Or0 - 1e-7)) / 2e-7
    dz = 1.0
    dK_dz = (K_omega(Om0, Or0, Z_STAR + dz) - K_omega(Om0, Or0, Z_STAR - dz)) / (2 * dz)
    dH = 0.01
    tp = dict(theta); tp["H0"] = theta["H0"] + dH
    tm = dict(theta); tm["H0"] = theta["H0"] - dH
    dK_dH0_fixed_omegas = (K_theta(tp)[0] - K_theta(tm)[0]) / (2 * dH)     # ω_b, ω_c fixos: Ω_m = ω_m/h²
    tp = dict(theta); tp["Neff"] = theta.get("Neff", PLANCK["Neff"]) + 0.01
    tm = dict(theta); tm["Neff"] = theta.get("Neff", PLANCK["Neff"]) - 0.01
    dK_dNeff = (K_theta(tp)[0] - K_theta(tm)[0]) / 0.02
    dlnK_dbeta = (2.0 / 3.0) * math.log(E0)                                   # exato: ln K = β·(2/3)ln E
    f_m = Om0 * (1 + Z_STAR) ** 3 / E0 ** 2                                   # fração da matéria em E² no nó
    f_r = Or0 * (1 + Z_STAR) ** 4 / E0 ** 2
    H0b = theta["H0"]
    return {
        "em": label, "K": K0, "E_zstar": E0, "Omega_m": Om0, "Omega_r": Or0,
        "fracao_materia_em_E2_no_no": f_m, "fracao_radiacao_em_E2_no_no": f_r,
        "dK_dOmega_m": dK_dOm, "dlnK_dlnOmega_m": dK_dOm * Om0 / K0,
        "dK_dOmega_r": dK_dOr, "dlnK_dlnOmega_r": dK_dOr * Or0 / K0,
        "dK_dzstar": dK_dz, "dlnK_dln1pz": dK_dz * (1 + Z_STAR) / K0,
        "dK_dH0_omegas_fixos": dK_dH0_fixed_omegas, "dK_dNeff": dK_dNeff, "dlnK_dbeta": dlnK_dbeta,
        "DeltaH0_local_por_DeltaOmega_m_0p01": 0.01 * dK_dOm * H0b,
        "DeltaH0_local_por_Deltazstar_1": 1.0 * dK_dz * H0b,
        "DeltaH0_local_por_DeltaNeff_0p1": 0.1 * dK_dNeff * H0b,
        "DeltaH0_local_por_sigma_zstar_planck_0p21": 0.21 * dK_dz * H0b,
        "leitura": ("∂lnK/∂lnΩ_m = (β/3)·f_m ≈ %.4f; ∂lnK/∂ln(1+z*) ≈ β·(1 + f_r/3) ≈ %.4f: K varia 1e-4 por 1%% em Ω_m e 1e-5 por "
                    "Δz* = 1; a incerteza da PREVISÃO H0_local = K·H0_fundo é dominada por H0_fundo (σ 0,3–0,6), não por K" % (dK_dOm * Om0 / K0, dK_dz * (1 + Z_STAR) / K0)),
    }


sens_banc = sens(theta_tgl, "θ̂_TGL da Fase 4 (Bancada, H0 = %.4f)" % theta_tgl["H0"])
sens_pl = sens(PLANCK, "Planck 2018 (um.py _V378_PLANCK)")
grade_Om = [{"Omega_m": om, "K": K_omega(om, Or_bc), "H0_local_se_fundo_68p531": 68.531 * K_omega(om, Or_bc)}
            for om in (0.29, 0.30, round(Om_bc, 4), 0.31, round(Om_pl, 4), 0.32, 0.33, 0.34)]
grade_z = [{"z_no": zz, "rotulo": rot, "K": K_omega(Om_bc, Or_bc, zz), "DeltaK_vs_1089p95": K_omega(Om_bc, Or_bc, zz) - K_bc}
           for zz, rot in ((1059.94, "z_drag Planck 2018 [KNOWN — a ler; só como sistemática de «qual registro»]"), (1088.0, "−2"),
                           (1089.80, "z* Planck 2018 TT,TE,EE+lowE+lensing (1089,80 ± 0,21) [KNOWN — a ler]"), (Z_STAR, "z* [INPUT] do um.py"),
                           (1091.0, "+1"), (1100.0, "+10"))]
grade_beta = [{"beta": b, "K": K_omega(Om_bc, Or_bc, Z_STAR, b)} for b in (0.0, 0.5 * BETA, BETA, 1.5 * BETA, 2 * BETA)]

# ----------------------------------------------------------------------------------------------------------------------
# 2. Os ALVOS — lidos do disco quando a casa os tem; «a ler» quando não
# ----------------------------------------------------------------------------------------------------------------------
L = f3p["leitores_de_sombra"]; R = f3p["replicas_reportadas_nao_combinadas"]; FU = f3p["fundos"]
alvos = [
    # --- leitores LOCAIS (sombra) ---
    {"id": "L1_sh0es_r22", "H0": f4["sh0es"][0], "sigma": f4["sh0es"][1], "fonte": "Riess et al. 2022, ApJL 934, L7 (SH0ES; R22) [KNOWN]",
     "em_disco": F4RES + " :: sh0es", "tipo": "Cefeidas (HST), anchors NGC 4258 + LMC + MW", "combinar": True, "grupo_SN": True, "grupo_4258": True,
     "nota": "o leitor do pipeline selado e da Fase 4; MOTIVOU a forma da lei (circularidade declarada na Fase 2) — a forma, não um parâmetro"},
    {"id": "L1b_sh0es_r25_cefeidas", "H0": L["S1_sh0es_jwst_cefeidas"]["H0"], "sigma": L["S1_sh0es_jwst_cefeidas"]["sigma"], "fonte": L["S1_sh0es_jwst_cefeidas"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S1", "tipo": "Cefeidas (HST+JWST)", "combinar": False, "grupo_SN": True, "grupo_4258": True,
     "nota": "RÉPLICA do L1 (mesmo programa): entra em família própria, nunca somado ao R22"},
    {"id": "L1c_sh0es_r25_mais_trgb", "H0": R["sh0es_jwst_mais_trgb"]["H0"], "sigma": R["sh0es_jwst_mais_trgb"]["sigma"], "fonte": R["sh0es_jwst_mais_trgb"]["fonte"] + " [KNOWN]",
     "em_disco": F3PRE + " :: replicas.sh0es_jwst_mais_trgb", "tipo": "Cefeidas + TRGB (SH0ES)", "combinar": False, "grupo_SN": True, "grupo_4258": True, "nota": "réplica, não combinada"},
    {"id": "L1d_riess_jwst_2024_tres_metodos", "H0": R["riess_jwst_tres_metodos"]["H0"], "sigma": R["riess_jwst_tres_metodos"]["sigma"], "fonte": "Riess et al. 2024, ApJ 977, 120; " + R["riess_jwst_tres_metodos"]["fonte"] + " [KNOWN]",
     "em_disco": F3PRE + " :: replicas.riess_jwst_tres_metodos", "tipo": "JWST Cefeidas+TRGB+JAGB (subamostra SH0ES)", "combinar": False, "grupo_SN": True, "grupo_4258": True,
     "nota": "SUBAMOSTRA do SH0ES (hospedeiras JWST): correlacionada com L1; réplica, não combinada"},
    {"id": "L2_cchp_trgb_jagb_cef", "H0": L["S2_cchp_trgb"]["H0"], "sigma": L["S2_cchp_trgb"]["sigma"], "fonte": "Freedman et al. 2024/2025, ApJ 985, 203; " + L["S2_cchp_trgb"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S2", "tipo": "CCHP JWST: TRGB + JAGB + Cefeidas (combinado)", "combinar": True, "grupo_SN": True, "grupo_4258": True,
     "nota": "O QUE PODE DOER: a TGL prevê K·H0_fundo para TODO calibrador local; sub-resultados ao lado"},
    {"id": "L2a_cchp_trgb_so", "H0": R["cchp_jwst_only_trgb"]["H0"], "sigma": R["cchp_jwst_only_trgb"]["sigma"], "fonte": R["cchp_jwst_only_trgb"]["fonte"] + " (TRGB só) [KNOWN]",
     "em_disco": F3PRE + " :: replicas.cchp_jwst_only_trgb", "tipo": "TRGB JWST (CCHP)", "combinar": False, "grupo_SN": True, "grupo_4258": True, "nota": "sub-resultado de L2; não combinado"},
    {"id": "L2b_cchp_jagb_so", "H0": R["cchp_jwst_only_jagb"]["H0"], "sigma": R["cchp_jwst_only_jagb"]["sigma"], "fonte": R["cchp_jwst_only_jagb"]["fonte"] + " (JAGB só) [KNOWN]",
     "em_disco": F3PRE + " :: replicas.cchp_jwst_only_jagb", "tipo": "JAGB JWST (CCHP)", "combinar": False, "grupo_SN": True, "grupo_4258": True, "nota": "sub-resultado de L2; não combinado"},
    {"id": "L2c_cchp_cefeidas_so", "H0": None, "sigma": None, "fonte": "Freedman et al. 2024/2025 (CCHP JWST Cefeidas só) [KNOWN — A LER DA FONTE]",
     "em_disco": "AUSENTE na casa (consulta: pré-registro da Fase 3 só traz TRGB e JAGB)", "tipo": "Cefeidas JWST (CCHP)", "combinar": False, "grupo_SN": True, "grupo_4258": True, "nota": "a ler"},
    {"id": "L3_sbf_jwst", "H0": L["S3_sbf_trgb_jwst"]["H0"], "sigma": L["S3_sbf_trgb_jwst"]["sigma"], "fonte": L["S3_sbf_trgb_jwst"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S3", "tipo": "SBF calibrado por TRGB (JWST)", "combinar": True, "grupo_SN": True, "grupo_4258": False, "nota": "calibração TRGB própria (Virgo)"},
    {"id": "L4_masers", "H0": L["S4_masers"]["H0"], "sigma": L["S4_masers"]["sigma"], "fonte": L["S4_masers"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S4", "tipo": "megamasers (geométrico, sem SNe)", "combinar": True, "grupo_SN": False, "grupo_4258": False, "nota": "σ_v,pec = 250 km/s assumida na fonte"},
    {"id": "L5_tdcosmo_2025", "H0": L["S5_tdcosmo_lentes"]["H0"], "sigma": L["S5_tdcosmo_lentes"]["sigma"], "fonte": L["S5_tdcosmo_lentes"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S5", "tipo": "lentes com atraso temporal (geométrico)", "combinar": True, "grupo_SN": False, "grupo_4258": False, "nota": "erro +3,9/−3,3 simetrizado (3,6)"},
    {"id": "L6_sirenes_o4a", "H0": L["S6_sirenes_lvk_o4a"]["H0"], "sigma": L["S6_sirenes_lvk_o4a"]["sigma"], "fonte": L["S6_sirenes_lvk_o4a"]["fonte"],
     "em_disco": F3PRE + " :: leitores_de_sombra.S6", "tipo": "sirenes padrão (LVK O4a)", "combinar": True, "grupo_SN": False, "grupo_4258": False, "nota": "vetável; peso ~0"},
    {"id": "L6b_gw170817", "H0": 70.0, "sigma": 10.0, "fonte": "Abbott et al. 2017, Nature 551, 85 (GW170817, 70 +12/−8) [KNOWN — A LER DA FONTE; valor do prompt, simetrizado 10]",
     "em_disco": "AUSENTE na casa (consulta: grep GW170817 no acervo → só ensaios de 2025; valor não lido de fonte em disco)", "tipo": "sirene única", "combinar": False, "grupo_SN": False, "grupo_4258": False, "nota": "alternativa ao L6; peso ~0"},
    {"id": "V_bancada_sh0es_so", "H0": f5["validacao"]["H0"], "sigma": f5["validacao"]["sigma_H0"], "fonte": "Bancada Fase 5 (Pantheon+SH0ES completo, ΛCDM, SNe + 77 calibradores) [REAL]",
     "em_disco": F5RES + " :: validacao", "tipo": "escada completa reproduzida na casa", "combinar": False, "grupo_SN": True, "grupo_4258": True,
     "nota": "validação da casa (z 0,04 do publicado 73,6 ± 1,1 [DECLARADO]); mesma escada que L1 — não somado"},
    # --- o FUNDO (face) ---
    {"id": "BG1_bancada_lcdm_planck_dr2", "H0": FU["Fd_lcdm_planck_dr2"]["H0"], "sigma": FU["Fd_lcdm_planck_dr2"]["sigma"], "fonte": FU["Fd_lcdm_planck_dr2"]["origem"],
     "em_disco": F3PRE + " :: fundos.Fd_lcdm_planck_dr2", "tipo": "FUNDO NU (ΛCDM) Planck comprimido Chen+2019 + DESI DR2, SEM escada", "combinar": False, "grupo_SN": False, "grupo_4258": False,
     "nota": "PRIMÁRIO proposto: fundo nu, sem os leitores que a lei prevê"},
    {"id": "BG2_planck2018", "H0": FU["Fc_planck2018"]["H0"], "sigma": FU["Fc_planck2018"]["sigma"], "fonte": FU["Fc_planck2018"]["origem"],
     "em_disco": F3PRE + " :: fundos.Fc_planck2018", "tipo": "FUNDO NU (ΛCDM) Planck só, publicado", "combinar": False, "grupo_SN": False, "grupo_4258": False, "nota": "réplica do fundo (a face sem o ângulo)"},
    {"id": "BG3_desi_dr2_bbn", "H0": 68.5, "sigma": 0.6, "fonte": "DESI Collaboration 2025, DR2 Results II (arXiv:2503.14738), BAO + BBN, sem CMB [KNOWN — A LER DA FONTE; valor do prompt]",
     "em_disco": "AUSENTE na casa como número (a Bancada tem os 13 BAO do DR2 com covariância, não o ajuste BAO+BBN)", "tipo": "escada INVERSA, sem CMB", "combinar": False, "grupo_SN": False, "grupo_4258": False,
     "nota": "réplica do fundo independente do CMB"},
    {"id": "BG4_CONTROLE_tgl_efetivo", "H0": FU["Fa_tgl_planck_dr2"]["H0"], "sigma": FU["Fa_tgl_planck_dr2"]["sigma"], "fonte": FU["Fa_tgl_planck_dr2"]["origem"],
     "em_disco": F3PRE + " :: fundos.Fa_tgl_planck_dr2", "tipo": "fundo TGL EFETIVO (mapa + E1): JÁ carrega β", "combinar": False, "grupo_SN": False, "grupo_4258": False,
     "nota": "CONTROLE: a leitura empilhada das Fases 2–3 (dupla contagem [DERIVED da convenção]); ao lado, nunca somado"},
    {"id": "BG5_ref_tgl_bestfit_fase4", "H0": H0bg_banc_lido, "sigma": P["theta_tgl"] and f4["familias"]["P_dr2_escada"]["posterior_d1b"]["resumo"]["H0"]["std"], "fonte": "Bancada Fase 4, θ̂_TGL com a escada DENTRO do ajuste [REAL]",
     "em_disco": F4RES + " :: familias.P_dr2_escada.nucleos.d1b.pontos.tgl", "tipo": "fundo ajustado COM o leitor previsto", "combinar": False, "grupo_SN": False, "grupo_4258": False,
     "nota": "referência: NÃO serve de fundo para uma previsão (empresta do dado que prevê); é o número da verossimilhança conjunta"},
]
for a in alvos:
    a["estatuto"] = ("[REAL — casa]" if "Bancada" in a["fonte"] else ("[KNOWN — lido do disco da casa]" if "AUSENTE" not in a["em_disco"] else "[KNOWN — a ler da fonte]"))

# ----------------------------------------------------------------------------------------------------------------------
# 3. Covariância declarada entre leitores locais e as famílias
# ----------------------------------------------------------------------------------------------------------------------
SIGMA_SN_FLUXO = 0.7     # km/s/Mpc, termo comum às escadas que partilham as SNe do fluxo de Hubble (pré-registro da Fase 3: «σ_SN ≈ 0,7 comum») [DECLARADO]
SIGMA_ANCORA_4258 = 0.5  # km/s/Mpc, termo comum L1×L2 pela âncora NGC 4258 (estimativa de desenho: ~1/3 do peso de âncora do SH0ES × 1,5 %) [DECLARADO — a conferir nas fontes]


def cov(ids, com_ancora):
    A = {a["id"]: a for a in alvos}
    n = len(ids); C = np.zeros((n, n))
    for i, x in enumerate(ids):
        C[i, i] = A[x]["sigma"] ** 2
        for j, y in enumerate(ids):
            if i != j:
                if A[x]["grupo_SN"] and A[y]["grupo_SN"]:
                    C[i, j] += SIGMA_SN_FLUXO ** 2
                if com_ancora and A[x]["grupo_4258"] and A[y]["grupo_4258"]:
                    C[i, j] += SIGMA_ANCORA_4258 ** 2
    return C


FAMILIAS = {
    "A_seis": {"ids": ["L1_sh0es_r22", "L2_cchp_trgb_jagb_cef", "L3_sbf_jwst", "L4_masers", "L5_tdcosmo_2025", "L6_sirenes_o4a"], "papel": "PRIMÁRIA: um leitor por programa independente"},
    "A_sem_sirenes": {"ids": ["L1_sh0es_r22", "L2_cchp_trgb_jagb_cef", "L3_sbf_jwst", "L4_masers", "L5_tdcosmo_2025"], "papel": "o veto das sirenes"},
    "B_incidencia_nova": {"ids": ["L2_cchp_trgb_jagb_cef", "L3_sbf_jwst", "L4_masers", "L5_tdcosmo_2025", "L6_sirenes_o4a"], "papel": "sem a escada que motivou a forma da lei"},
    "C_r25_no_lugar_do_r22": {"ids": ["L1b_sh0es_r25_cefeidas", "L2_cchp_trgb_jagb_cef", "L3_sbf_jwst", "L4_masers", "L5_tdcosmo_2025", "L6_sirenes_o4a"], "papel": "réplica com o SH0ES 2025"},
    "D_so_escada_r22": {"ids": ["L1_sh0es_r22"], "papel": "o registro da Fase 4 (um leitor)"},
    "E_so_trgb_cchp": {"ids": ["L2_cchp_trgb_jagb_cef"], "papel": "o que pode doer (um leitor)"},
    "F_geometricos": {"ids": ["L4_masers", "L5_tdcosmo_2025", "L6_sirenes_o4a"], "papel": "sem SNe, sem Cefeidas, sem TRGB: a incidência mais limpa (pouco poder)"},
}
FUNDOS = {"BG1_bancada_lcdm_planck_dr2": "PRIMÁRIO (fundo nu, sem escada)", "BG2_planck2018": "réplica (Planck só)",
          "BG3_desi_dr2_bbn": "réplica (sem CMB) — a ler", "BG4_CONTROLE_tgl_efetivo": "CONTROLE (empilhado; nunca somado)"}
PRIORS = {"livre": ("beta", -0.05, 0.05), "shift": ("epsilon", -0.2, 0.2), "ede_like": ("s", 0.8, 1.0)}
PRIOR_NOTA = ("β ∈ U[−0,05, 0,05] é o prior do pipeline da Bancada (lido do pré-registro da Fase 4); ε ∈ U[−0,2, 0,2] e s ∈ U[0,8, 1,0] "
              "são DECLARADOS aqui (largos o bastante para a classe «tensão de Hubble» de 10–15 %); ln B contra modelos de 1 parâmetro "
              "depende dessas larguras pelo fator de Occam (ln da razão das larguras) — dito, e medido abaixo com ×½ e ×2")


def chi2_perfil(Rr, d, Ci, b, sb):
    """χ² mínimo em H0_fundo (analítico): d_i = R·H + ruído (cov C); b = H + ruído (σ_b)."""
    one = np.ones(len(d))
    A = Rr * Rr * (one @ Ci @ one) + 1.0 / sb ** 2
    B = Rr * (one @ Ci @ d) + b / sb ** 2
    H = B / A
    r = d - Rr * H * one
    return float(r @ Ci @ r + (b - H) ** 2 / sb ** 2), float(H)


def analise(fam_ids, bg_id, com_ancora=True, Om=Om_bc, Or=Or_bc):
    A = {a["id"]: a for a in alvos}
    d = np.array([A[x]["H0"] for x in fam_ids]); C = cov(fam_ids, com_ancora); Ci = np.linalg.inv(C)
    b, sb = A[bg_id]["H0"], A[bg_id]["sigma"]
    n = len(d); one = np.ones(n)
    K = K_omega(Om, Or)
    # a razão combinada (GLS com covariância) e a dispersão interna
    w = one @ Ci @ one
    ybar = (one @ Ci @ d) / w; sybar = 1.0 / math.sqrt(w)
    rho = ybar / b; srho = rho * math.sqrt((sybar / ybar) ** 2 + (sb / b) ** 2)
    z_tgl = (rho - K) / srho; z_lcdm = (rho - 1.0) / srho
    chi2_disp = float((d - ybar * one) @ Ci @ (d - ybar * one)); dof = max(n - 1, 1)
    p_disp = float(stats.chi2.sf(chi2_disp, dof)) if n > 1 else None
    # hipóteses: χ² de perfil
    c_tgl, H_tgl = chi2_perfil(K, d, Ci, b, sb)
    c_l, H_l = chi2_perfil(1.0, d, Ci, b, sb)
    out = {"familia": fam_ids, "fundo": bg_id, "H0_fundo": b, "sigma_fundo": sb, "com_ancora_4258": com_ancora, "n_local": n,
           "K": K, "H0_local_previsto_TGL": K * b, "sigma_previsao_pelo_fundo": K * sb,
           "H0_local_combinado": ybar, "sigma_local_combinado": sybar, "razao": rho, "sigma_razao": srho,
           "z_TGL": z_tgl, "z_LCDM": z_lcdm, "chi2_dispersao": chi2_disp, "dof_dispersao": dof, "dispersao_por_gl": chi2_disp / dof, "p_dispersao": p_disp,
           "chi2": {"TGL": c_tgl, "LCDM": c_l}, "H0_fundo_perfil": {"TGL": H_tgl, "LCDM": H_l}, "lnB": {}, "BIC": {}, "params": {}}
    # 1 parâmetro: grade fina, evidência por integração sob prior uniforme
    ndata = n + 1
    for nome, (pn, lo, hi) in PRIORS.items():
        grid = np.linspace(lo, hi, 40001)
        if nome == "livre":
            Rg = np.array([K_omega(Om, Or, Z_STAR, bb) for bb in grid])
        elif nome == "shift":
            Rg = 1.0 + grid
        else:                       # ede_like: locais leem H_true; o fundo lê s·H_true ⟺ R = 1/s
            Rg = 1.0 / grid
        c = np.array([chi2_perfil(float(r_), d, Ci, b, sb)[0] for r_ in Rg])
        k = int(np.argmin(c)); cmin = float(c[k]); phat = float(grid[k])
        # σ por curvatura local (ajuste quadrático nos vizinhos)
        kk = slice(max(k - 200, 0), min(k + 201, len(grid)))
        pc = np.polyfit(grid[kk], c[kk], 2); sig = float(1.0 / math.sqrt(pc[0])) if pc[0] > 0 else None   # χ² = a(p−p̂)² + c ⟹ Δχ² = 1 em 1σ ⟹ σ = 1/√a
        lnZ = float(np.log(np.trapezoid(np.exp(-0.5 * (c - cmin)), grid)) - 0.5 * cmin - math.log(hi - lo))
        out["params"][nome] = {"param": pn, "hat": phat, "sigma": sig, "chi2_min": cmin, "prior": [lo, hi], "no_limite": bool(k in (0, len(grid) - 1)),
                               "lnZ_rel": lnZ}
        out["lnB"]["TGL_vs_" + nome] = -0.5 * c_tgl - lnZ
        out["lnB"]["LCDM_vs_" + nome] = -0.5 * c_l - lnZ
        out["lnB"]["TGL_vs_" + nome + "_prior_x0p5"] = -0.5 * c_tgl - (lnZ + math.log(2.0))
        out["lnB"]["TGL_vs_" + nome + "_prior_x2"] = -0.5 * c_tgl - (lnZ - math.log(2.0))
        out["BIC"][nome] = cmin + 1 * math.log(ndata)
        if nome == "livre" and sig:
            out["params"][nome]["delta_hat"] = phat - BETA; out["params"][nome]["z_delta"] = (phat - BETA) / sig
            out["params"][nome]["z_perfil_beta_tgl"] = math.copysign(math.sqrt(max(c_tgl - cmin, 0.0)), phat - BETA)
            out["params"][nome]["z_perfil_lcdm"] = math.sqrt(max(c_l - cmin, 0.0))
    out["lnB"]["TGL_vs_LCDM"] = -0.5 * (c_tgl - c_l)
    out["BIC"]["TGL"] = c_tgl; out["BIC"]["LCDM"] = c_l
    out["Delta_chi2_TGL_menos_LCDM"] = c_tgl - c_l
    # separação (poder) entre as duas hipóteses de ZERO parâmetro
    out["separacao_TGL_LCDM_sigma"] = (K - 1.0) / srho
    out["sigma_razao_para_5sigma"] = (K - 1.0) / 5.0
    out["sigma_local_para_5sigma_dado_o_fundo"] = (math.sqrt(max(((K - 1.0) * b / 5.0) ** 2 - (K * sb) ** 2, 0.0)))
    # o que cada alvo acrescenta: peso de Fisher na média GLS; z individual; leave-one-out
    pesos = (Ci @ one) / w
    out["leitores"] = []
    for i, x in enumerate(fam_ids):
        zi_t = (d[i] - K * b) / math.sqrt(C[i, i] + (K * sb) ** 2); zi_l = (d[i] - b) / math.sqrt(C[i, i] + sb ** 2)
        rec = {"id": x, "H0": float(d[i]), "sigma": float(math.sqrt(C[i, i])), "peso_GLS": float(pesos[i]), "z_vs_TGL": zi_t, "z_vs_LCDM": zi_l}
        if n > 1:
            rest = [y for y in fam_ids if y != x]
            sub = analise_simples(rest, bg_id, com_ancora, Om, Or)
            rec["loo_z_TGL"] = sub["z_TGL"]; rec["loo_z_LCDM"] = sub["z_LCDM"]
        out["leitores"].append(rec)
    return out


def analise_simples(fam_ids, bg_id, com_ancora, Om, Or):
    A = {a["id"]: a for a in alvos}
    d = np.array([A[x]["H0"] for x in fam_ids]); C = cov(fam_ids, com_ancora); Ci = np.linalg.inv(C)
    b, sb = A[bg_id]["H0"], A[bg_id]["sigma"]; one = np.ones(len(d)); K = K_omega(Om, Or)
    w = one @ Ci @ one; ybar = (one @ Ci @ d) / w; sybar = 1.0 / math.sqrt(w)
    rho = ybar / b; srho = rho * math.sqrt((sybar / ybar) ** 2 + (sb / b) ** 2)
    return {"z_TGL": (rho - K) / srho, "z_LCDM": (rho - 1.0) / srho}


# ----------------------------------------------------------------------------------------------------------------------
# 4. A FUNÇÃO DE VEREDITO (pré-registrável): decide só pelos números; vereditos permitidos listados; CONFIRMED proibido
# ----------------------------------------------------------------------------------------------------------------------
VEREDITOS_PERMITIDOS = [
    "TGL_FASE9_HUBBLE__INCONCLUSIVE_SYSTEMATICS",
    "TGL_FASE9_HUBBLE__FALSIFIED_AT_5SIGMA",
    "TGL_FASE9_HUBBLE__TENSION_3_TO_5_SIGMA",
    "TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED",
    "TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_nSIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL",
    "TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA",
]
VEREDITOS_PROIBIDOS = ["CONF·IRMED (a palavra inteira)", "PROVED·BY / TGL·PROVED", "resolvida", "confirmada", "RESOLVED"]


def veredito(res, limiar_disp=2.0, p_disp_min=0.01):
    """A regra, fixada ANTES de calcular o composto (o poder já é legível: os alvos são públicos):
    1. dispersão interna dos leitores (χ²/gl > 2 ou p < 0,01) → INCONCLUSIVE_SYSTEMATICS (os calibradores discordam além dos erros);
    2. |z_TGL| ≥ 5 → FALSIFIED_AT_5SIGMA (neste registro, sob D1b, com o fundo nomeado);
    3. 3 ≤ |z_TGL| < 5 → TENSION_3_TO_5_SIGMA;
    4. separação (K−1)/σ_razão < 3 → NOT_FALSIFIED_UNDERPOWERED (o registro não distingue K de 1);
    5. |z_TGL| < 3 e |z_LCDM| ≥ 5 → NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_nSIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL
       (n = ⌊|z_LCDM|⌋; USE_NOVEL = nenhum parâmetro da teoria ajustado a este dado: β = α√e, z* [INPUT de Planck], Ω_m do fundo nu);
    6. senão → NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA.
    Sufixos sempre: __D1B__FUNDO_<id>__NOT_A_CONFIRMATION. Nunca a palavra proibida (CONF·IRMED): a RG/ΛCDM é o limite clássico; coincidir é correspondência."""
    base = "TGL_FASE9_HUBBLE__"
    suf = "__D1B__FUNDO_%s__NOT_A_CONFIRMATION" % res["fundo"]
    zt, zl, sep = abs(res["z_TGL"]), abs(res["z_LCDM"]), res["separacao_TGL_LCDM_sigma"]
    if res["n_local"] > 1 and (res["dispersao_por_gl"] > limiar_disp or (res["p_dispersao"] is not None and res["p_dispersao"] < p_disp_min)):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suf
    if zt >= 5:
        return base + "FALSIFIED_AT_5SIGMA" + suf
    if zt >= 3:
        return base + "TENSION_3_TO_5_SIGMA" + suf
    if sep < 3:
        return base + "NOT_FALSIFIED_UNDERPOWERED" + suf
    if zl >= 5:
        return base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL" % int(zl) + suf
    return base + "NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA" + suf


# ----------------------------------------------------------------------------------------------------------------------
# 5. Rodar o ensaio (NÃO-CEGO: os alvos são públicos) sobre todas as famílias × fundos
# ----------------------------------------------------------------------------------------------------------------------
ensaio = {}
for fn, fam in FAMILIAS.items():
    for bg in FUNDOS:
        res = analise(fam["ids"], bg, com_ancora=True)
        res["papel"] = fam["papel"]; res["papel_fundo"] = FUNDOS[bg]
        res["veredito_ensaio"] = veredito(res)
        ensaio["%s × %s" % (fn, bg)] = res
# sensibilidade do primário à âncora comum e ao Ω_m do fundo
prim = ensaio["A_seis × BG1_bancada_lcdm_planck_dr2"]
prim_sem_ancora = analise(FAMILIAS["A_seis"]["ids"], "BG1_bancada_lcdm_planck_dr2", com_ancora=False)
prim_Om_planck = analise(FAMILIAS["A_seis"]["ids"], "BG1_bancada_lcdm_planck_dr2", com_ancora=True, Om=Om_pl, Or=Or_pl)

# ----------------------------------------------------------------------------------------------------------------------
# 6. Sistemáticas: Cefeidas vs TRGB; o TRGB contra a TGL e contra o ΛCDM; z*; Ω_m; o fundo
# ----------------------------------------------------------------------------------------------------------------------
A = {a["id"]: a for a in alvos}
def z_entre(x, y, com_ancora=True):
    C = cov([x, y], com_ancora); dd = A[x]["H0"] - A[y]["H0"]; s = math.sqrt(C[0, 0] + C[1, 1] - 2 * C[0, 1]); return dd / s, s
z_r22_cchp, s_r22_cchp = z_entre("L1_sh0es_r22", "L2_cchp_trgb_jagb_cef")
z_r22_trgbso, s_r22_trgbso = z_entre("L1_sh0es_r22", "L2a_cchp_trgb_so")
z_r25_cchp, s_r25_cchp = z_entre("L1b_sh0es_r25_cefeidas", "L2_cchp_trgb_jagb_cef")
trgb = {}
for bg in ("BG1_bancada_lcdm_planck_dr2", "BG2_planck2018", "BG3_desi_dr2_bbn"):
    b, sb = A[bg]["H0"], A[bg]["sigma"]
    for lid in ("L2_cchp_trgb_jagb_cef", "L2a_cchp_trgb_so", "L2b_cchp_jagb_so"):
        d, s = A[lid]["H0"], A[lid]["sigma"]
        zt = (d - K_bc * b) / math.sqrt(s ** 2 + (K_bc * sb) ** 2); zl = (d - b) / math.sqrt(s ** 2 + sb ** 2)
        delta = abs(d - K_bc * b)
        trgb["%s × %s" % (lid, bg)] = {"H0": d, "sigma": s, "previsto_TGL": K_bc * b, "z_vs_TGL": zt, "z_vs_LCDM": zl,
                                        "sigma_necessaria_para_3sigma_vs_TGL": math.sqrt(max((delta / 3) ** 2 - (K_bc * sb) ** 2, 0)),
                                        "sigma_necessaria_para_5sigma_vs_TGL": math.sqrt(max((delta / 5) ** 2 - (K_bc * sb) ** 2, 0))}
fundos_tab = []
for bg in ("BG1_bancada_lcdm_planck_dr2", "BG2_planck2018", "BG3_desi_dr2_bbn", "BG4_CONTROLE_tgl_efetivo", "BG5_ref_tgl_bestfit_fase4"):
    b = A[bg]["H0"]; fundos_tab.append({"fundo": bg, "H0_fundo": b, "H0_local_previsto": K_bc * b, "estatuto": A[bg]["estatuto"], "papel": A[bg]["nota"]})
spread = max(f["H0_local_previsto"] for f in fundos_tab[:3]) - min(f["H0_local_previsto"] for f in fundos_tab[:3])

sistematicas = {
    "escada_cefeidas_vs_trgb": {
        "z_R22_vs_CCHP_combinado": z_r22_cchp, "sigma_diff": s_r22_cchp, "z_R22_vs_CCHP_TRGB_so": z_r22_trgbso, "z_R25_vs_CCHP": z_r25_cchp,
        "leitura": "a discordância Cefeidas×TRGB fica em 1–2σ com a covariância declarada: não é INCONCLUSIVE por dispersão hoje; é o lugar onde o teste pode doer se σ(TRGB) cair a ~1"},
    "trgb_contra_TGL_e_LCDM": trgb,
    "z_star_efetivo": {"dlnK_dln1pz": sens_banc["dlnK_dln1pz"], "DeltaH0_local_por_sigma_zstar_planck_0p21": sens_banc["DeltaH0_local_por_sigma_zstar_planck_0p21"],
                        "DeltaK_se_no_em_z_drag": grade_z[0]["DeltaK_vs_1089p95"], "leitura": "desprezível (< 0,03 km/s/Mpc mesmo trocando z* por z_drag)"},
    "Omega_m_do_fundo_nu": {"K_em_Om_bancada_0p3023": K_bc, "K_em_Om_planck_0p3152": K_pl, "DeltaK": K_pl - K_bc, "DeltaH0_local_a_68p531": (K_pl - K_bc) * 68.531,
                            "z_TGL_primario_com_Om_planck": prim_Om_planck["z_TGL"], "leitura": "desprezível (ΔH0 ≈ 0,01): K não é onde a previsão incerta"},
    "a_escolha_do_fundo_DOMINANTE": {"tabela": fundos_tab, "spread_H0_local_entre_fundos_nus": spread,
                                     "leitura": ("a previsão H0_local = K·H0_fundo varia %.2f km/s/Mpc entre os fundos nus (Planck só → Planck+DR2): é a decisão «qual fundo é o fundo» "
                                                 "[OPEN, do operador]; o desenho a fixa ANTES (primário BG1; réplicas BG2/BG3); o BG5 (ajuste conjunto com a escada) não é fundo de previsão" % spread)},
    "ancora_comum_L1xL2": {"z_TGL_primario_com_ancora": prim["z_TGL"], "z_TGL_primario_sem_ancora": prim_sem_ancora["z_TGL"],
                           "sigma_razao_com": prim["sigma_razao"], "sigma_razao_sem": prim_sem_ancora["sigma_razao"]},
    "forma_da_lei_D1a_vs_D1b": {"K_D1a": (1.0 + Z_STAR) ** BETA, "K_D1b": K_bc, "DeltaH0_local_a_68p531": ((1.0 + Z_STAR) ** BETA - K_bc) * 68.531,
                                "leitura": "a escolha da forma (duas candidatas, D1b pré-registrada como primária na Fase 4) move a previsão 0,27 km/s/Mpc (~0,25σ da escada): não decide o teste"},
}

# ----------------------------------------------------------------------------------------------------------------------
# 7. O que as Fases 1–2 obrigam a dizer; a lei da prova
# ----------------------------------------------------------------------------------------------------------------------
posdicao = open(POSDICAO, "r", encoding="utf-8").read().strip(); LIDOS[POSDICAO] = sha256(POSDICAO)
obrigacoes = {
    "fundo_nu": "o fundo é ΛCDM nu (β = 0 no fundo; o mapa de R irrelevante); β entra UMA vez, na lei (D1b: K = E(z*)^{2β/3}) — convenção do artigo 1, fixada pelo operador em 30/09 (R1 ratificada 02/10: «β uma vez no reflexo; fundo nu; nó em z*»)",
    "pull_empilhado_nao_se_repete": "o BG4 (fundo TGL efetivo 69,20) entra SÓ como controle ao lado: a Fase 2 (+1,95σ) e a Fase 3 (−2,94σ) empilhavam β (fundo + lei); aqui o controle dá z_TGL = %.2f, nunca somado ao primário" % ensaio["A_seis × BG4_CONTROLE_tgl_efetivo"]["z_TGL"],
    "fase1": "sob o mapa efetivo o fundo comprimido não constrange β: por isso o fundo deste desenho é nu e β não é estimado do fundo",
    "circularidade_da_forma": "a FORMA da lei foi cunhada conhecendo a razão SH0ES/Planck (declarado nas Fases 2–3); pela lei da prova da casa isso não é demérito: nenhum PARÂMETRO foi ajustado (β = α√e; z* de Planck; Ω_m do fundo); a família B (sem a escada) é a incidência nova e fica ao lado",
    "um_registro_uma_cobranca": "a razão H0_local/H0_fundo é UM grau de liberdade: toda alternativa de 1 parâmetro (β livre, ε, s de EDE-like) é DEGENERADA nela — só o fator de Occam (largura do prior) as separa; o que não é degenerado é TGL (0 parâmetros, número previsto) contra ΛCDM (0 parâmetros, K = 1): ln B = −Δχ²/2, sem prior",
    "lei_da_prova_05out_verbatim": posdicao,
}

# ----------------------------------------------------------------------------------------------------------------------
# 8. Saída: JSON + tabela Markdown; guarda contra vereditos proibidos
# ----------------------------------------------------------------------------------------------------------------------
resultado = {
    "protocolo": "FASE9_HUBBLE_DESENHO_ESTATISTICO", "lente": "desenho", "data": datetime.datetime.now().isoformat(timespec="seconds"),
    "ENSAIO_NAO_CEGO": "os alvos são públicos e já olhados (Fases 3–5); o pré-registro fixa a FUNÇÃO de veredito, as famílias, o fundo primário, as covariâncias e os priors — não a ignorância",
    "beta_regra": "α_CODATA2018 (lido do um.py por regex) · √e em runtime; nunca literal", "beta_runtime": BETA, "z_star": Z_STAR,
    "selo_corrente": {"arquivo": SELO, "sha256": LIDOS[SELO], "versao": selo_versao, "qg_closure_verdict": selo.get("qg_closure_verdict")},
    "reproducoes": reproducoes, "sensibilidade": {"bancada": sens_banc, "planck": sens_pl, "grade_Omega_m": grade_Om, "grade_z_no": grade_z, "grade_beta": grade_beta},
    "alvos": alvos, "covariancia_declarada": {"sigma_SN_fluxo_comum": SIGMA_SN_FLUXO, "sigma_ancora_4258_L1xL2": SIGMA_ANCORA_4258,
                                              "regra": "C_ij = σ_i² δ_ij + σ_SN² [i,j partilham SNe do fluxo] + σ_4258² [i,j partilham a âncora NGC 4258]; réplicas do mesmo programa nunca se somam"},
    "familias": FAMILIAS, "fundos": FUNDOS, "priors": PRIORS, "priors_nota": PRIOR_NOTA,
    "vereditos_permitidos": VEREDITOS_PERMITIDOS, "vereditos_proibidos": VEREDITOS_PROIBIDOS, "funcao_de_veredito": veredito.__doc__,
    "ensaio": ensaio, "primario_sem_ancora": prim_sem_ancora, "primario_Om_planck": prim_Om_planck,
    "sistematicas": sistematicas, "obrigacoes_fases_1_2": obrigacoes,
    "arquivos_lidos_sha256": LIDOS,
}
txt = json.dumps(resultado, ensure_ascii=False, indent=1, default=float)
_txt_g = txt.replace("NOT_A_CONFIRMATION", "")
for _m in GUARDA.finditer(_txt_g):
    print("GUARDA:", _txt_g[max(0, _m.start() - 120):_m.end() + 40].replace("\n", " "))
assert not GUARDA.search(_txt_g), "veredito proibido na saída"
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    fh.write(txt)


def f(x, n=3):
    try:
        return ("%." + str(n) + "f") % float(x)
    except Exception:
        return "—"


md = []
md.append("# FASE 9 — a razão de Hubble: o DESENHO ESTATÍSTICO do teste discriminante (lente «desenho», %s)\n" % resultado["data"][:16])
md.append("ENSAIO NÃO-CEGO (alvos públicos). β = α√e = %.15f (α lido do um.py por regex). z* = %s [INPUT]. Selo lido: %s (`%s`).\n" % (BETA, Z_STAR, selo_versao, LIDOS[SELO][:16]))
md.append("## (a) K = E(z*)^{2β/3} — reproduzido, não copiado\n")
md.append("| quantidade | recomputado | lido do disco | diff |\n|---|---|---|---|")
md.append("| K (Planck 2018, core v386 `%s`) | %.9f | %.9f | %.1e |" % (core_dlc_path, K_pl, core_dlc, abs(K_pl - core_dlc)))
md.append("| K (θ̂_TGL Fase 4: H0 %.4f, ω_b %.6f, ω_c %.6f) | %.9f | %.9f | %.1e |" % (theta_tgl["H0"], theta_tgl["ombh2"], theta_tgl["omch2"], K_bc, K_banc_lido, abs(K_bc - K_banc_lido)))
md.append("| K (reanálise D1b, og = 2.469e-5/T⁴) | %.9f | %.9f | %.1e |" % (K_re, f3r["K_D1b"], abs(K_re - f3r["K_D1b"])))
md.append("| E(z*) Planck | %.6f | %.6f | %.1e |" % (E_pl, core_Ez, abs(E_pl - core_Ez)))
md.append("| β runtime vs Fase 4 | %.15f | %.15f | %.1e |" % (BETA, f4["beta_tgl"], abs(BETA - f4["beta_tgl"])))
md.append("| H0_local previsto (Fase 4) | %.4f | %.4f | %.1e |\n" % (H0bg_banc_lido * K_bc, P["pontos"]["tgl"]["H0_local"], abs(H0bg_banc_lido * K_bc - P["pontos"]["tgl"]["H0_local"])))
md.append("Sensibilidade (em θ̂ da Bancada; Ω_m = %.4f, Ω_r = %.3e, f_m = %.3f, f_r = %.3f no nó): ∂lnK/∂lnΩ_m = %.5f; ∂lnK/∂ln(1+z*) = %.5f; ∂K/∂Ω_m = %.5f; ∂K/∂z* = %.2e; ∂K/∂N_eff = %.2e; ∂lnK/∂β = I_b = %.4f. ΔH0_local: por ΔΩ_m = 0,01 → %.4f; por Δz* = 1 → %.5f; por σ(z*) = 0,21 → %.6f; por ΔN_eff = 0,1 → %.4f.\n" % (
    Om_bc, Or_bc, sens_banc["fracao_materia_em_E2_no_no"], sens_banc["fracao_radiacao_em_E2_no_no"], sens_banc["dlnK_dlnOmega_m"], sens_banc["dlnK_dln1pz"], sens_banc["dK_dOmega_m"], sens_banc["dK_dzstar"], sens_banc["dK_dNeff"], sens_banc["dlnK_dbeta"],
    sens_banc["DeltaH0_local_por_DeltaOmega_m_0p01"], sens_banc["DeltaH0_local_por_Deltazstar_1"], sens_banc["DeltaH0_local_por_sigma_zstar_planck_0p21"], sens_banc["DeltaH0_local_por_DeltaNeff_0p1"]))
md.append("| Ω_m | K | H0_local @ 68,531 |\n|---|---|---|")
for g in grade_Om:
    md.append("| %.4f | %.6f | %.3f |" % (g["Omega_m"], g["K"], g["H0_local_se_fundo_68p531"]))
md.append("\n| nó z | K | ΔK vs z* |\n|---|---|---|")
for g in grade_z:
    md.append("| %s (%s) | %.6f | %+.2e |" % (g["z_no"], g["rotulo"], g["K"], g["DeltaK_vs_1089p95"]))
md.append("\n## (b) Os alvos\n")
md.append("| id | H0 | σ | tipo | fonte | estatuto | combinar? |\n|---|---|---|---|---|---|---|")
for a in alvos:
    md.append("| %s | %s | %s | %s | %s | %s | %s |" % (a["id"], f(a["H0"], 2), f(a["sigma"], 2), a["tipo"], a["fonte"], a["estatuto"], "sim" if a["combinar"] else "não"))
md.append("\nCovariância declarada: σ_SN(fluxo) = %.1f comum a L1/L2/L3 (e réplicas da escada); σ_4258 = %.1f comum L1×L2 [DECLARADO — a conferir]. Réplicas do mesmo programa nunca se somam.\n" % (SIGMA_SN_FLUXO, SIGMA_ANCORA_4258))
md.append("## (c)+(d) Hipóteses, estatística, poder e a função de veredito — ensaio sobre os alvos públicos\n")
md.append("| família × fundo | n | H0_bg | previsto TGL | local comb. | razão ± σ | z_TGL | z_ΛCDM | disp/gl (p) | Δχ²(TGL−ΛCDM) | lnB TGL/ΛCDM | lnB TGL/livre | lnB TGL/shift | lnB TGL/EDE | β̂ ± σ (z_δ) | sep (σ) | veredito (ensaio) |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, r in ensaio.items():
    pl = r["params"]["livre"]
    md.append("| %s | %d | %.3f ± %.3f | %.3f | %.3f ± %.3f | %.4f ± %.4f | %+.2f | %+.2f | %.2f (%s) | %+.2f | %+.2f | %+.2f | %+.2f | %+.2f | %.5f ± %s (%s) | %.2f | `%s` |" % (
        k, r["n_local"], r["H0_fundo"], r["sigma_fundo"], r["H0_local_previsto_TGL"], r["H0_local_combinado"], r["sigma_local_combinado"], r["razao"], r["sigma_razao"],
        r["z_TGL"], r["z_LCDM"], r["dispersao_por_gl"], f(r["p_dispersao"], 3), r["Delta_chi2_TGL_menos_LCDM"], r["lnB"]["TGL_vs_LCDM"], r["lnB"]["TGL_vs_livre"], r["lnB"]["TGL_vs_shift"], r["lnB"]["TGL_vs_ede_like"],
        pl["hat"], f(pl["sigma"], 5), f(pl.get("z_delta"), 2), r["separacao_TGL_LCDM_sigma"], r["veredito_ensaio"]))
md.append("\nPriors: %s. Occam medido no primário: lnB TGL/livre = %.2f (prior ×½: %.2f; ×2: %.2f); TGL/shift = %.2f (×½ %.2f; ×2 %.2f); TGL/EDE-like = %.2f.\n" % (
    PRIOR_NOTA, prim["lnB"]["TGL_vs_livre"], prim["lnB"]["TGL_vs_livre_prior_x0p5"], prim["lnB"]["TGL_vs_livre_prior_x2"], prim["lnB"]["TGL_vs_shift"], prim["lnB"]["TGL_vs_shift_prior_x0p5"], prim["lnB"]["TGL_vs_shift_prior_x2"], prim["lnB"]["TGL_vs_ede_like"]))
md.append("O que cada alvo acrescenta (primário A_seis × BG1): peso GLS, z individual vs TGL e vs ΛCDM, e z do composto SEM o alvo (leave-one-out).\n")
md.append("| leitor | H0 ± σ | peso | z vs TGL | z vs ΛCDM | LOO z_TGL | LOO z_ΛCDM |\n|---|---|---|---|---|---|---|")
for r in prim["leitores"]:
    md.append("| %s | %.2f ± %.2f | %.3f | %+.2f | %+.2f | %+.2f | %+.2f |" % (r["id"], r["H0"], r["sigma"], r["peso_GLS"], r["z_vs_TGL"], r["z_vs_LCDM"], r.get("loo_z_TGL", float("nan")), r.get("loo_z_LCDM", float("nan"))))
md.append("\nPoder: separação TGL↔ΛCDM no primário = (K−1)/σ_razão = %.2f σ; σ_razão para 5σ = %.4f (σ_local para 5σ, dado o fundo BG1 = %.3f km/s/Mpc). Sem âncora comum: z_TGL = %+.2f (σ_razão %.4f).\n" % (
    prim["separacao_TGL_LCDM_sigma"], prim["sigma_razao_para_5sigma"], prim["sigma_local_para_5sigma_dado_o_fundo"], prim_sem_ancora["z_TGL"], prim_sem_ancora["sigma_razao"]))
md.append("## (f) Sistemáticas\n")
md.append("- Cefeidas × TRGB: z(R22 − CCHP) = %+.2f (σ_diff %.2f); z(R22 − TRGB só) = %+.2f; z(R25 − CCHP) = %+.2f.\n" % (z_r22_cchp, s_r22_cchp, z_r22_trgbso, z_r25_cchp))
md.append("| TRGB/JAGB × fundo | H0 ± σ | previsto TGL | z vs TGL | z vs ΛCDM | σ p/ 3σ vs TGL | σ p/ 5σ vs TGL |\n|---|---|---|---|---|---|---|")
for k, t in trgb.items():
    md.append("| %s | %.2f ± %.2f | %.3f | %+.2f | %+.2f | %.2f | %.2f |" % (k, t["H0"], t["sigma"], t["previsto_TGL"], t["z_vs_TGL"], t["z_vs_LCDM"], t["sigma_necessaria_para_3sigma_vs_TGL"], t["sigma_necessaria_para_5sigma_vs_TGL"]))
md.append("\n| fundo | H0_fundo | H0_local previsto (K = %.6f) | estatuto | papel |\n|---|---|---|---|---|" % K_bc)
for t in fundos_tab:
    md.append("| %s | %.4f | %.3f | %s | %s |" % (t["fundo"], t["H0_fundo"], t["H0_local_previsto"], t["estatuto"], t["papel"]))
md.append("\n- z* efetivo: ΔH0_local por σ(z*) = 0,21 → %.1e; nó em z_drag: ΔK = %+.1e (desprezível).\n- Ω_m do fundo nu: K(0,3023) − K(0,3152) = %+.1e → ΔH0 = %+.3f (desprezível); z_TGL primário com Ω_m de Planck: %+.2f.\n- Forma D1a vs D1b: ΔH0_local = %+.3f (~0,25σ da escada): não decide.\n- A ESCOLHA DO FUNDO é a sistemática dominante: spread %.2f km/s/Mpc entre fundos nus.\n" % (
    sens_banc["DeltaH0_local_por_sigma_zstar_planck_0p21"], grade_z[0]["DeltaK_vs_1089p95"], K_pl - K_bc, (K_pl - K_bc) * 68.531, prim_Om_planck["z_TGL"], sistematicas["forma_da_lei_D1a_vs_D1b"]["DeltaH0_local_a_68p531"], spread))
md.append("## (e) O que as Fases 1–2 obrigam a dizer\n")
for k, v in obrigacoes.items():
    if k != "lei_da_prova_05out_verbatim":
        md.append("- **%s**: %s" % (k, v))
md.append("\n## Arquivos lidos (sha256)\n")
for p_, h_ in LIDOS.items():
    md.append("- `%s` — `%s`" % (p_, h_))
mdtxt = "\n".join(md) + "\n"
assert not GUARDA.search(mdtxt.replace("NOT_A_CONFIRMATION", "")), "veredito proibido na tabela"
with open(OUT_MD, "w", encoding="utf-8") as fh:
    fh.write(mdtxt)
print(mdtxt)
print("OK reproducoes:", reproducoes["ok"], "| escritos:", OUT_JSON, OUT_MD)
