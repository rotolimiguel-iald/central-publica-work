"""Numeros DERIVADOS da ESTRATEGIA B, calculados em runtime a partir de numeros LIDOS do acervo
(fontes por hash em medidas/HASHES_FONTES_*.json). beta NUNCA literal: ALPHA_FINE_CODATA_2018 lido dos
bytes do um.py (l.5557) x sqrt(e). Tudo aqui e [DERIVED aqui; informativo]: nenhum veredito, nenhum dado
aberto para veredito; os valores observados sao os ja transcritos pela casa ([DECLARADO ate D-H/D8])."""
import json, math, re, hashlib, datetime

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
raw = open(UM, "rb").read()
lines = raw.split(b"\n")
l5557 = lines[5556].decode("utf-8", "replace").rstrip("\r")
alpha = float(re.match(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$", l5557).group(1))
beta = alpha * math.sqrt(math.e)
out = {"quando": datetime.datetime.now().isoformat(timespec="seconds"),
       "um_py_sha16": hashlib.sha256(raw).hexdigest()[:16],
       "beta_runtime": beta, "alpha_l5557": alpha,
       "estatuto": "[DERIVED aqui; informativo; nao e veredito]"}

# ---- fontes lidas (numeros transcritos; hash das fontes em HASHES_FONTES_02.json)
P9 = r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json"
P8 = r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json"
F9 = json.load(open(P9, encoding="utf-8"))["spec"]
F8 = json.load(open(P8, encoding="utf-8"))["spec"]
K = F9["lei"]["K_no_fundo_nu"]
zstar = F9["lei"]["z_star"]
H0bg, sH0bg = F9["fundos"]["BG1"]["H0"], F9["fundos"]["BG1"]["sigma"]
H0bg_tgl, sH0bg_tgl = F9["fundos"]["BG4"]["H0"], F9["fundos"]["BG4"]["sigma"]
dNdb = F8["mapas"]["A"]["previsao"]["dN_eff_dbeta"]
dN = F8["mapas"]["A"]["previsao"]["delta_N_eff"]
NTGL = F8["mapas"]["A"]["previsao"]["N_eff_TGL"]
NSM = F8["mapas"]["A"]["previsao"]["N_base_SM"]
S_BBN = F8["mapas"]["C"]["S_exato"]
out["lidos"] = {"K_fundo_nu_F9": K, "z_star": zstar, "H0_bg_BG1": [H0bg, sH0bg],
                "H0_bg_TGL_BG4_controle": [H0bg_tgl, sH0bg_tgl],
                "dNeff_dbeta_F8": dNdb, "delta_Neff_F8": dN, "Neff_TGL_F8": NTGL, "N_SM": NSM, "S_BBN_F8": S_BBN}

# ---- 1. a razao fixa entre canais (zero parametro; beta cancela)
lnK = math.log(K)
lnE = lnK / ((2.0 / 3.0) * beta)
R = dN / lnK
F = 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0)
R_forma_fechada = 2.0 * (1.0 + F * NSM) / (F * lnE)
S_check = math.sqrt(1.0 + 4.0 * beta / 3.0)
out["razao_fixa_entre_canais"] = {
    "definicao": "R = Delta N_eff / ln K = [(4/3)(1+F.N_SM)/F . beta] / [(2/3) ln E(z*) . beta] = 2(1+F.N_SM)/(F . ln E(z*)) -- beta CANCELA",
    "lnK": lnK, "lnE_zstar_implicito": lnE, "E_zstar_implicito": math.exp(lnE), "F_7_8_4_11_4_3": F,
    "R_dos_numeros_do_acervo": R, "R_forma_fechada": R_forma_fechada, "dif_rel": abs(R - R_forma_fechada) / R,
    "S_BBN_recalculado_sqrt_1_4beta_3": S_check, "S_BBN_dif_rel_vs_F8": abs(S_check - S_BBN) / S_BBN,
    "sensibilidade_a_beta": "nenhuma (linear em beta nos dois lados); E(z*) do fundo nu [KNOWN]; F e N_SM [KNOWN]",
    "leitura": ("LCDM: 0/0 (ambos nulos). Extensao de 1 parametro: N_eff-livre da Delta N_eff != 0 com ln K ~ 0 "
                "(so o deslocamento do H0 do fundo [KNOWN, ordem de grandeza]); EDE/r_d-livre da ln K != 0 com "
                "Delta N_eff(BBN) = 0. Nenhuma extensao de UM parametro reproduz o par; uma de DOIS reproduz os valores, nunca a razao a priori.")}

# ---- 2. distancias em sigma, HOJE (core.hubble_ratio_opening_v388 481366db97f0ebf1 via levantador C01; F8 V1)
H0loc, sH0loc = 72.88191894244864, 0.9149424231474728   # media GLS dos leitores (C01) [DECLARADO ate D-H]
H0pred = K * H0bg
sPred = K * sH0bg
z_H_TGL = (H0loc - H0pred) / math.sqrt(sH0loc ** 2 + sPred ** 2)
z_H_LCDM = (H0loc - H0bg) / math.sqrt(sH0loc ** 2 + sH0bg ** 2)
H0pred_bg4 = K * H0bg_tgl
z_H_TGL_bg4 = (H0loc - H0pred_bg4) / math.sqrt(sH0loc ** 2 + (K * sH0bg_tgl) ** 2)
out["hubble_hoje_reproduzido"] = {
    "H0_local_previsto_BG1": H0pred, "sigma_previsao": sPred,
    "z_TGL_vs_dado_grosseiro": z_H_TGL, "z_LCDM_vs_dado_grosseiro": z_H_LCDM,
    "z_delta_oficial_core": -1.4243571651630185, "z_disc_oficial_core": 4.283735613863391,
    "H0_local_previsto_se_fundo_TGL_BG4": H0pred_bg4, "z_TGL_vs_dado_se_fundo_BG4": z_H_TGL_bg4,
    "nota": ("o oficial usa perfil de chi2 com fundo perfilado e covariancia dos leitores; aqui so a reproducao grosseira "
             "(GLS + fundo em quadratura). BG4 e CONTROLE no F9 (nunca somado): mostra que a escolha do fundo "
             "move a previsao do par -- item de desenho D-PAR-1")}
neff_meas = {  # [DECLARADO ate D8] -- transcritos do F8 V1 / levantador C06
    "Planck2018_TTTEEE_lowE": (2.92, 0.19), "Planck2018_lensing_BAO": (2.99, 0.17), "ACT_DR6_Planck": (2.86, 0.13),
    "CMB_SPA_v2_Yp_BBN": (2.82, 0.12), "CMB_SPA_v2_Yp_livre": (2.96, 0.225)}
neff_hoje = {}
for k, (c, s) in neff_meas.items():
    zT = (c - NTGL) / s
    zL = (c - NSM) / s
    neff_hoje[k] = {"z_TGL": zT, "z_LCDM": zL, "lnB_TGL_vs_LCDM_gauss": -0.5 * (zT ** 2 - zL ** 2)}
out["neff_hoje"] = neff_hoje

# ---- 3. projecoes (poder previo = separacao TGL-LCDM / sigma; e tensao se o centro atual persistir)
sig_future = {"SO_baseline_~2027": 0.055, "SO_goal_~2029": 0.050, "SO_ASO_~2030": 0.045,
              "CMB_S4_requisito_[DECLARADO_encerrado]": 0.030, "sigma_para_5sigma": dN / 5.0}
proj = {}
for k, s in sig_future.items():
    proj[k] = {"sigma": s, "poder_separacao_TGL_SM": dN / s,
               "tensao_se_centro_2p82_persistir": (NTGL - 2.82) / s,
               "tensao_se_centro_2p96_persistir": (NTGL - 2.96) / s,
               "tensao_se_centro_2p97_persistir": (NTGL - 2.97) / s}
out["neff_projecoes"] = proj
num = abs(H0loc - H0bg)
s_need = math.sqrt((num / 5.0) ** 2 - sH0bg ** 2)
pH = F9["poder_previo"]["por_familia_e_fundo"]["P_primaria x BG1"]["poder_K_menos_1_sigmas"]
out["hubble_projecao"] = {"sigma_local_para_z_disc_5_mesmo_centro": s_need, "sigma_local_hoje": sH0loc,
                          "poder_previo_F9_P_primaria_BG1": pH}

# ---- 4. o PAR (quadratura, independentes): contra LCDM-base, poder previo (se a TGL for verdadeira)
par = {}
for k, s in sig_future.items():
    pN = dN / s
    par[k] = {"poder_previo_par_vs_LCDM_base_quadratura": math.sqrt(pH ** 2 + pN ** 2),
              "perna_H0": pH, "perna_Neff": pN,
              "exclusao_de_LCDM_mais_Neff_livre_1par_decide_a_perna_H0": pH,
              "exclusao_de_LCDM_mais_EDE_ou_rd_livre_1par_decide_a_perna_Neff": pN}
out["par_poder_previo"] = par
for k in ("CMB_SPA_v2_Yp_livre", "CMB_SPA_v2_Yp_BBN"):
    out["par_hoje_" + k] = {"lnB_H0_oficial": 9.166739752963847,
                            "lnB_Neff_gauss": neff_hoje[k]["lnB_TGL_vs_LCDM_gauss"],
                            "lnB_par_soma_se_independentes": 9.166739752963847 + neff_hoje[k]["lnB_TGL_vs_LCDM_gauss"],
                            "nota": ("a perna N_eff puxa CONTRA hoje (centros abaixo de 3,044); a soma so vale se os canais "
                                     "forem independentes e o fundo nao for contado duas vezes (D3 do F8)")}

# ---- 5. Occam: 0 parametros contra 2 (N_eff + amplitude precoce), se ambos pousarem na TGL
occam = {"prior_beta_livre_F9": 0.10, "sigma_beta_H0_hoje": 0.001988374672292904, "prior_Neff_tipico": 1.0}
occam["ln_penalidade_H0_1par"] = math.log(occam["prior_beta_livre_F9"] / occam["sigma_beta_H0_hoje"])
occam["ln_penalidade_Neff_1par_SO_goal"] = math.log(occam["prior_Neff_tipico"] / 0.050)
occam["ln_penalidade_total_2par_estimativa"] = occam["ln_penalidade_H0_1par"] + occam["ln_penalidade_Neff_1par_SO_goal"]
occam["nota"] = ("estimativa grosseira (Occam ~ ln(largura do prior / sigma posterior) por parametro); o lnB oficial "
                 "TGL/beta-livre e 2,24 (largura ao lado: Occam ~ ln 2 por fator 2) -- nunca somar com o oficial")
out["occam_0_vs_2_parametros"] = occam

# ---- 6. m2 (C07) e contorno (sigma_beta por dominio)
m2_pred = beta * math.sin(math.pi / 4) * 1000.0   # meV; 1 eV [NORM]; sin45 [POSTULATE]
juno = (8.6603, 0.0693)
nufit = (8.6776, 0.0576)
pdg = (8.6776, 0.1037)
s_2031 = 0.005 / 2 * juno[0]
out["m2"] = {"m2_pred_meV": m2_pred, "z_juno": (juno[0] - m2_pred) / juno[1],
             "z_nufit_reflexo": (nufit[0] - m2_pred) / nufit[1], "z_pdg2023": (pdg[0] - m2_pred) / pdg[1],
             "sigma_beta_implicita_juno": juno[1] / 1000.0 / math.sin(math.pi / 4),
             "sigma_2031_0p5pct_em_Dm2_meV": s_2031, "z_2031_se_centro_persistir": (juno[0] - m2_pred) / s_2031,
             "nota": "0,5 % em Delta m^2 -> 0,25 % em m2 (raiz); o core cita 7,84 sigma (precisao que mata 0,784 %)"}
out["contorno_sigma_beta_por_dominio"] = {
    "beta_sobre_2": beta / 2, "beta_sobre_5": beta / 5,
    "H0_sigma_beta_hoje": 0.001988374672292904,
    "Neff_sigma_beta": {k: s / dNdb for k, s in {"Planck_0p17": 0.17, "CMB_SPA_0p12": 0.12, "SO_goal_0p050": 0.050,
                                                  "SO_ASO_0p045": 0.045, "S4_0p030": 0.030}.items()},
    "m2_sigma_beta_juno": juno[1] / 1000.0 / math.sin(math.pi / 4),
    "V12_por_lente_sigma": {"KiDS": 0.027322812311748386, "DES_Y3": 0.01582278481012658,
                            "Euclid": 0.005777448110302362, "LSST": 0.0045674615764641855}}

# ---- 7. dephasing: deficits transcritos (nao recalculados)
out["dephasing_transcrito"] = {
    "relogios_Sr_deficit_ordens_5sigma": 12.457634837278354, "th229_hoje_ordens": 18.3, "neutrinos_ordens": 36.7,
    "gw_ordens_aprox": 23, "G10_08ago_229Th_omega2T_necessario": 3.083e45, "G10_08ago_229Th_melhor": 2.804e35,
    "G10_deficit_ordens": 10.04, "beta_MZ_on_shell_core": 0.012785740757659002, "ratio_on_shell": 1.0627064682727432,
    "fonte": "core clock_test_result_v369 / beta_runs_bounded_below_v388 (dump do levantador); Atlas l.23456-23460 (G10)"}

json.dump(out, open("medidas/numeros_estrategia_b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
