# -*- coding: utf-8 -*-
"""Inventário com sha256 LIDO do artefato (nunca de memória). Só leitura fora da lente."""
import hashlib, json, os, sys, re, math

OUT = os.path.dirname(os.path.abspath(__file__))
TA = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1"
N2 = os.path.join(TA, "nivel2_data")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
PONTE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um"
BU = r"C:\IALD\Bancada_Um"
MR = r"C:\IALD\Artigo\MCMC_V2_RAZAO"
TOE = r"C:\IALD\Artigo\BANCADA_TOE\juiz_lA"

PATHS = {
 "um_py_v386": os.path.join(NOS, "um.py"),
 "core_um_absoluto_json": os.path.join(NOS, "um_absoluto.json"),
 "selo_um_absoluto_selo_json": os.path.join(NOS, "um_absoluto_selo.json"),
 "artigo_pt_txt": os.path.join(NOS, "um_absoluto_pt.txt"),
 # Planck 2018 plik_lite + low-ell (teste acústico, original)
 "plik_lite__cl_cmb_plik_v22": os.path.join(N2, "planck2018_plik_lite", "cl_cmb_plik_v22.dat"),
 "plik_lite__c_matrix_plik_v22": os.path.join(N2, "planck2018_plik_lite", "c_matrix_plik_v22.dat"),
 "plik_lite__bweight": os.path.join(N2, "planck2018_plik_lite", "bweight.dat"),
 "plik_lite__blmin": os.path.join(N2, "planck2018_plik_lite", "blmin.dat"),
 "plik_lite__blmax": os.path.join(N2, "planck2018_plik_lite", "blmax.dat"),
 "plik_lite__readme": os.path.join(N2, "planck2018_plik_lite", "readme.txt"),
 "low_ell__CTT_bin_low_ell_2018": os.path.join(N2, "planck2018_low_ell", "CTT_bin_low_ell_2018.dat"),
 "low_ell__bweight": os.path.join(N2, "planck2018_low_ell", "bweight_low_ell.dat"),
 "low_ell__blmin": os.path.join(N2, "planck2018_low_ell", "blmin_low_ell.dat"),
 "low_ell__blmax": os.path.join(N2, "planck2018_low_ell", "blmax_low_ell.dat"),
 "low_ell__plmin": os.path.join(N2, "planck2018_low_ell", "plmin_low_ell.dat"),
 "low_ell__readme": os.path.join(N2, "planck2018_low_ell", "readme.txt"),
 "planck_lite_py": os.path.join(N2, "planck_lite_py.py"),
 "chain_of_custody_nivel2": os.path.join(N2, "CHAIN_OF_CUSTODY_NIVEL2.sha256"),
 # cópias do plik_lite
 "nos_copy__cl_cmb_plik_v22": os.path.join(NOS, "nivel2_mcmc", "nivel2_data", "planck2018_plik_lite", "cl_cmb_plik_v22.dat"),
 "nos_copy__c_matrix_plik_v22": os.path.join(NOS, "nivel2_mcmc", "nivel2_data", "planck2018_plik_lite", "c_matrix_plik_v22.dat"),
 "mr_copy__cl_cmb_plik_v22": os.path.join(MR, "nivel2_data", "planck2018_plik_lite", "cl_cmb_plik_v22.dat"),
 "mr_copy__c_matrix_plik_v22": os.path.join(MR, "nivel2_data", "planck2018_plik_lite", "c_matrix_plik_v22.dat"),
 # Nível 2 (MCMC completo)
 "n2_frozen_py": os.path.join(TA, "12_nivel2_frozen_e_verossimilhanca.py"),
 "n2_frozen_json": os.path.join(TA, "12_nivel2_frozen.json"),
 "n2_rodar_py": os.path.join(TA, "13_rodar_nivel2.py"),
 "n2_chains_h5": os.path.join(TA, "13_nivel2_chains.h5"),
 "n2_resultado_json": os.path.join(TA, "13_nivel2_resultado.json"),
 "n2_analise_md": os.path.join(TA, "14_ANALISE_NIVEL2_FECHADO.md"),
 "n2_nos_chains_h5": os.path.join(NOS, "nivel2_mcmc", "13_nivel2_chains.h5"),
 "n2_nos_resultado_json": os.path.join(NOS, "nivel2_mcmc", "13_nivel2_resultado.json"),
 # N_eff / rho+p / acústico
 "neff_frozen_py": os.path.join(TA, "10_frozen_neff_v1.py"),
 "neff_frozen_resultado_json": os.path.join(TA, "10_frozen_neff_v1_resultado.json"),
 "acustico_prereg_json": os.path.join(TA, "05_prereg.json"),
 "acustico_verossimilhanca_py": os.path.join(TA, "05_verossimilhanca.py"),
 "acustico_resultado_mcmc_json": os.path.join(TA, "06_resultado_mcmc.json"),
 "acustico_analise_final_json": os.path.join(TA, "07_analise_final.json"),
 "previsao_nivel2_json": os.path.join(TA, "08_previsao_nivel2.json"),
 "fisher_nivel2_json": os.path.join(TA, "09_fisher_nivel2.json"),
 "mcmc_definitivo_resultado_json": os.path.join(TA, "11_mcmc_definitivo_resultado.json"),
 "resultados_md": os.path.join(TA, "RESULTADOS.md"),
 "proveniencia_json": os.path.join(TA, "PROVENIENCIA.json"),
 # DESI
 "desi_dr2_mean": os.path.join(TA, "_originais", "desi_gaussian_bao_ALL_GCcomb_mean.txt"),
 "desi_dr2_cov": os.path.join(TA, "_originais", "desi_gaussian_bao_ALL_GCcomb_cov.txt"),
 "desi_frente_alpha_mean": r"C:\IALD\Artigo\frente_alpha\desi_gaussian_bao_ALL_GCcomb_mean.txt",
 "desi_frente_alpha_cov": r"C:\IALD\Artigo\frente_alpha\desi_gaussian_bao_ALL_GCcomb_cov.txt",
 # Planck comprimido / D1
 "chen2019_pdf": os.path.join(BU, "fontes_externas", "chen_huang_wang_2019_1808.05724.pdf"),
 "bancada_fontes_py": os.path.join(BU, "bancada", "fontes.py"),
 "bancada_motor_py": os.path.join(BU, "bancada", "motor.py"),
 "bancada_camb_tabela_py": os.path.join(BU, "bancada", "camb_tabela.py"),
 "bancada_camb_lcdm_v1_json": os.path.join(BU, "tabelas", "camb_lcdm_v1.json"),
 "bancada_camb_lcdm_v1_npz": os.path.join(BU, "tabelas", "camb_lcdm_v1.npz"),
 "bancada_validacao_bancada_json": os.path.join(BU, "estado", "validacao_bancada.json"),
 "fase1_prereg": os.path.join(BU, "investigacao", "fase1_eff_30set", "PREREGISTRO_FASE1_EFF_20260930.json"),
 "fase1_resultado": os.path.join(BU, "investigacao", "fase1_eff_30set", "RESULTADO_FASE1_EFF_20260930.json"),
 "fase1_relatorio": os.path.join(BU, "investigacao", "fase1_eff_30set", "RELATORIO_FASE1_EFF_20260930.md"),
 "inv28set_C1_F1": os.path.join(BU, "investigacao", "C1_F1_calibracao_previsao.json"),
 "inv28set_M1_mapa_de_R": os.path.join(BU, "investigacao", "M1_mapa_de_R.json"),
 "d1v3_pipeline_py": os.path.join(PONTE, "cache", "d1_camb", "v3", "d1_v3_pipeline.py"),
 "d1v3_worker_py": os.path.join(PONTE, "cache", "d1_camb", "v3", "tgl_camb_worker_v3.py"),
 "d1v3_result_json": os.path.join(PONTE, "cache", "d1_camb", "v3", "saida", "D1_CAMB_V3_REAL_RESULT.json"),
 "d1v3_manifesto_json": os.path.join(PONTE, "cache", "d1_camb", "v3", "MANIFESTO_D1_V3.json"),
 "d1_camb_v1_result_json": os.path.join(PONTE, "cache", "d1_camb", "D1_CAMB_RESULT.json"),
 "d1_camb_v2_result_json": os.path.join(PONTE, "cache", "d1_camb", "D1_CAMB_V2_RESULT.json"),
 "juiz_lA_result_json": os.path.join(TOE, "JUIZ_LA_V1_RESULT.json"),
 "juiz_lA_prereg_md": os.path.join(TOE, "JUIZ_LA_V1_PREREG.md"),
 # MCMC_V2_RAZAO (N_eff / Big Bang)
 "mr_22_prereg_SO_S4_json": os.path.join(MR, "22_prereg_SO_S4.json"),
 "mr_23_mapa_de_poder_json": os.path.join(MR, "23_mapa_de_poder.json"),
 "mr_15_fisher_da_razao_json": os.path.join(MR, "15_fisher_da_razao.json"),
 "mr_142_big_bang_v2_json": os.path.join(MR, "142_a_explosao_e_o_big_bang_v2.json"),
 "mr_142_big_bang_v2_py": os.path.join(MR, "142_a_explosao_e_o_big_bang_v2.py"),
 # Planck lensing (não-BBN; registrado por completude)
 "planck_lensing_tgz": os.path.join(PONTE, "cache", "lensing", "planck", "COM_Lensing_4096_R3.00.tgz"),
 "planck_lensing_nlkk": os.path.join(PONTE, "cache", "lensing", "planck", "COM_Lensing_4096_R3.00", "MV", "nlkk.dat"),
 "act_dr6_nlkk": os.path.join(PONTE, "cache", "lensing", "act_dr6", "N_L_kk_act_dr6_lensing_v1_baseline.txt"),
 # CAMB
 "camb_init_tgl_pycbc_env": r"C:\IALD\projetos_pyhton\acom\tgl_pycbc_env\Lib\site-packages\camb\__init__.py",
 "camb_init_unified_env": r"C:\IALD\projetos_pyhton\IALD\unified_env\Lib\site-packages\camb\__init__.py",
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()

inv = {}
for k, p in PATHS.items():
    if os.path.isfile(p):
        s = sha(p)
        inv[k] = {"caminho": p, "bytes": os.path.getsize(p), "sha256": s, "sha16": s[:16], "existe": True}
    else:
        inv[k] = {"caminho": p, "existe": False}

# conferência da cadeia de custódia do plik_lite (hash lido do arquivo .sha256 vs calculado)
cc = {}
try:
    for line in open(PATHS["chain_of_custody_nivel2"], encoding="utf-8"):
        m = re.match(r"([0-9a-f]{64}) \*(.+)$", line.strip())
        if m:
            rel = m.group(2).replace("/", os.sep)
            p = os.path.join(N2, rel)
            cc[rel] = {"declarado": m.group(1)[:16], "calculado": sha(p)[:16] if os.path.isfile(p) else None,
                       "confere": (os.path.isfile(p) and sha(p) == m.group(1))}
except Exception as e:
    cc["erro"] = repr(e)
inv["_conferencia_chain_of_custody_nivel2"] = cc

# cópias idênticas?
def same(a, b):
    return inv[a].get("sha256") == inv[b].get("sha256") if inv[a].get("existe") and inv[b].get("existe") else None
inv["_copias"] = {
 "plik_cl_nos_eq_original": same("plik_lite__cl_cmb_plik_v22", "nos_copy__cl_cmb_plik_v22"),
 "plik_cmat_nos_eq_original": same("plik_lite__c_matrix_plik_v22", "nos_copy__c_matrix_plik_v22"),
 "plik_cl_mr_eq_original": same("plik_lite__cl_cmb_plik_v22", "mr_copy__cl_cmb_plik_v22"),
 "plik_cmat_mr_eq_original": same("plik_lite__c_matrix_plik_v22", "mr_copy__c_matrix_plik_v22"),
 "n2_chains_nos_eq_original": same("n2_chains_h5", "n2_nos_chains_h5"),
 "n2_resultado_nos_eq_original": same("n2_resultado_json", "n2_nos_resultado_json"),
 "desi_frente_alpha_eq_originais_mean": same("desi_dr2_mean", "desi_frente_alpha_mean"),
 "desi_frente_alpha_eq_originais_cov": same("desi_dr2_cov", "desi_frente_alpha_cov"),
}

# beta em runtime (lido do um.py por regex, nunca literal)
src = open(PATHS["um_py_v386"], encoding="utf-8", errors="replace").read()
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src)
alpha = float(m.group(1)) if m else None
beta = alpha * math.sqrt(math.e) if alpha else None
mv = re.search(r"UM_VERSION\s*=\s*['\"]?(v?\d+)", src)
inv["_beta_runtime"] = {"alpha_regex": alpha, "beta_alpha_sqrt_e": beta, "um_version_regex": mv.group(1) if mv else None}
# contagem de linhas-chave no um.py
inv["_um_py_grep"] = {
 "n_linhas": src.count("\n") + 1,
 "prove_rho_plus_p_closure_linha": next((i + 1 for i, l in enumerate(src.splitlines()) if l.startswith("def prove_rho_plus_p_closure")), None),
 "prove_neff_channel_linha": next((i + 1 for i, l in enumerate(src.splitlines()) if l.startswith("def prove_neff_channel")), None),
 "prove_evidence_audit_linha": next((i + 1 for i, l in enumerate(src.splitlines()) if l.startswith("def prove_evidence_audit")), None),
 "OMB_BBN_linhas": [i + 1 for i, l in enumerate(src.splitlines()) if "OMB_BBN, OMB_BBN_ERR" in l],
 "tens_now_linhas": [i + 1 for i, l in enumerate(src.splitlines()) if "tens_now = 1.61" in l],
 "plik_lite_mencoes": src.count("plik_lite"),
 "PRIMAT_mencoes": src.count("PRIMAT"), "AlterBBN_mencoes": src.count("AlterBBN"), "PArthENoPE_mencoes": src.count("PArthENoPE"),
}

json.dump(inv, open(os.path.join(OUT, "inventario_dados_na_casa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k.startswith("_") else {"bytes": v.get("bytes"), "sha16": v.get("sha16"), "existe": v.get("existe")}) for k, v in inv.items()}, ensure_ascii=False, indent=1))
