import hashlib, os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
IALD = r"C:\IALD"
PONTE = os.path.join(IALD, "Artigo", "Haja_Luz", "A Ponte e o Um")
NOS = os.path.join(PONTE, "Nós")
BANC = os.path.join(IALD, "Bancada_Um")
paths = {
 # SNe
 "pantheon_dat": os.path.join(IALD, "observaveis_tgl", "tgl_data_cache", "pantheon", "Pantheon+SH0ES.dat"),
 "pantheon_cov": os.path.join(IALD, "projetos_pyhton", "acom", "tgl_data_cache", "pantheon_covariance.dat"),
 "identidade_pantheon_cov": os.path.join(BANC, "estado", "identidade_pantheon_cov.json"),
 # DESI DR2
 "desi_dr2_mean": os.path.join(IALD, "Artigo", "teste_acustico_beta_tgl_v1", "_originais", "desi_gaussian_bao_ALL_GCcomb_mean.txt"),
 "desi_dr2_cov": os.path.join(IALD, "Artigo", "teste_acustico_beta_tgl_v1", "_originais", "desi_gaussian_bao_ALL_GCcomb_cov.txt"),
 "desi_dr2_mean_copia_frente_alpha": os.path.join(IALD, "Artigo", "frente_alpha", "desi_gaussian_bao_ALL_GCcomb_mean.txt"),
 "desi_dr2_cov_copia_frente_alpha": os.path.join(IALD, "Artigo", "frente_alpha", "desi_gaussian_bao_ALL_GCcomb_cov.txt"),
 "desi_dr2_mean_copia_tetelestai": os.path.join(PONTE, "TETELESTAI", "BANCADA_OFICIAL", "data", "cosmology", "desi_gaussian_bao_ALL_GCcomb_mean.txt"),
 "desi_dr2_cov_copia_tetelestai": os.path.join(PONTE, "TETELESTAI", "BANCADA_OFICIAL", "data", "cosmology", "desi_gaussian_bao_ALL_GCcomb_cov.txt"),
 # Planck comprimido / D1 V3
 "d1v3_pipeline": os.path.join(PONTE, "cache", "d1_camb", "v3", "d1_v3_pipeline.py"),
 "d1v3_manifesto": os.path.join(PONTE, "cache", "d1_camb", "v3", "MANIFESTO_D1_V3.json"),
 "d1v3_result": os.path.join(PONTE, "cache", "d1_camb", "v3", "saida", "D1_CAMB_V3_REAL_RESULT.json"),
 "chen_pdf": os.path.join(BANC, "fontes_externas", "chen_huang_wang_2019_1808.05724.pdf"),
 # cronômetros
 "moresco_2022": os.path.join(BANC, "fontes_externas", "moresco_2022_cc.json"),
 "moresco_2020_cov": os.path.join(BANC, "fontes_externas", "moresco_2020_cov.json"),
 # tabela CAMB
 "camb_tabela": os.path.join(BANC, "tabelas", "camb_lcdm_v1.npz"),
 # Fase 5 (Bancada)
 "f5_pre": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "PREREGISTRO_FASE5_SH0ES_20261001.json"),
 "f5_res": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "RESULTADO_FASE5_SH0ES_20261001.json"),
 "f5_rel": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "RELATORIO_FASE5_SH0ES_20261001.md"),
 "f5_smoke": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "SMOKE_SH0ES.json"),
 # Fase 5 (cache do rito)
 "cache_f5_pre": os.path.join(PONTE, "cache", "bancada_01out", "PREREGISTRO_FASE5_SH0ES_20261001.json"),
 "cache_f5_res": os.path.join(PONTE, "cache", "bancada_01out", "RESULTADO_FASE5_SH0ES_20261001.json"),
 # Fase 4 (cache do rito)
 "cache_f4_pre": os.path.join(PONTE, "cache", "bancada_30set", "PREREGISTRO_FASE4_DESVIO_20260930.json"),
 "cache_f4_res": os.path.join(PONTE, "cache", "bancada_30set", "RESULTADO_FASE4_DESVIO_20260930.json"),
 "cache_f4_smoke": os.path.join(PONTE, "cache", "bancada_30set", "SMOKE_FASE4.json"),
 # Fase 7
 "cache_f7_pre": os.path.join(PONTE, "cache", "bancada_01out", "PREREGISTRO_FASE7_CC_COVARIANCIA_20261001.json"),
 "cache_f7_res": os.path.join(PONTE, "cache", "bancada_01out", "RESULTADO_FASE7_CC_COVARIANCIA_20261001.json"),
 "cache_cc_cov": os.path.join(PONTE, "cache", "bancada_01out", "moresco_2020_cov.json"),
 # Fase 1 / Fase 2 / 3
 "f1_pre": os.path.join(BANC, "investigacao", "fase1_eff_30set", "PREREGISTRO_FASE1_EFF_20260930.json"),
 "f1_res": os.path.join(BANC, "investigacao", "fase1_eff_30set", "RESULTADO_FASE1_EFF_20260930.json"),
 # Bancada scripts
 "um_bancada": os.path.join(BANC, "um_bancada.py"),
 "mcp_um": os.path.join(BANC, "mcp_um.py"),
 "motor": os.path.join(BANC, "bancada", "motor.py"),
 "fontes": os.path.join(BANC, "bancada", "fontes.py"),
 "pantheon_cov_py": os.path.join(BANC, "bancada", "pantheon_cov.py"),
 "fundo_gpu": os.path.join(BANC, "bancada", "fundo_gpu.py"),
 "evidencia": os.path.join(BANC, "bancada", "evidencia.py"),
 "patch_sh0es": os.path.join(BANC, "ferramentas", "patch_sh0es_calibradores.py"),
 "rodar_fase5": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "rodar_fase5.py"),
 "relatorio_fase5": os.path.join(BANC, "investigacao", "fase5_sh0es_01out", "relatorio_fase5.py"),
 # um.py / core / selo v386
 "um_py": os.path.join(NOS, "um.py"),
 "core": os.path.join(NOS, "um_absoluto.json"),
 "selo": os.path.join(NOS, "um_absoluto_selo.json"),
}
out = {}
for k, p in paths.items():
    if os.path.isfile(p):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        out[k] = dict(caminho=p, bytes=os.path.getsize(p), sha16=h[:16], sha256=h, existe=True)
    else:
        out[k] = dict(caminho=p, existe=False)
json.dump(out, open("inventario_medido.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(("%-36s %s" % (k, ("%12d B  sha16 %s  %s" % (v["bytes"], v["sha16"], v["caminho"])) if v["existe"] else "AUSENTE  " + v["caminho"])))
