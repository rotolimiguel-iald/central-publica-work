# -*- coding: utf-8 -*-
"""Gera o RASCUNHO do pré-registro da Fase 9 (a razão de Hubble) no formato da casa.
Régua: todo hash calculado do artefato por este script; β nunca literal (α lido do um.py por regex);
nada baixado; nada rodado da casa; só leitura fora desta pasta.
"""
import json, hashlib, re, math, os, sys, datetime
sys.stdout.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
BANCADA = r"C:\IALD\Bancada_Um"
INV = os.path.join(BANCADA, "investigacao")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
SCR = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def fonte(rotulo, p, estatuto):
    if not os.path.isfile(p):
        return {"rotulo": rotulo, "path": p, "sha256": None, "bytes": None, "estatuto": "AUSENTE"}
    return {"rotulo": rotulo, "path": p, "sha256": sha(p), "bytes": os.path.getsize(p), "estatuto": estatuto}

# ---------------- base v386 (lida) ----------------
um_py = os.path.join(NOS, "um.py")
core_p = os.path.join(NOS, "um_absoluto.json")
selo_p = os.path.join(NOS, "um_absoluto_selo.json")
src = open(um_py, "rb").read().decode("utf-8", "replace")
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src)
ALPHA = float(m.group(1)); ALPHA_LINE = src[:m.start()].count("\n") + 1
BETA = ALPHA * math.sqrt(math.e)
UM_VERSION = re.search(r"UM_VERSION\s*=\s*[\"']([^\"']+)", src).group(1)
core = json.load(open(core_p, encoding="utf-8"))["core"]
selo = json.load(open(selo_p, encoding="utf-8"))
H_UM, H_CORE, H_SELO = sha(um_py), sha(core_p), sha(selo_p)

f4 = core["bancada_fase4_v378"]; P = f4["P_ladder_d1b"]
f5 = core["bancada_fases_5_6_7_v380"]["fase5"]
dlc = core["the_dissipation_law_with_contrast_v378"]
wwm = core["what_was_missed_v378"]
ledger = core["the_ledger_of_charges_v383"]["ledger"]
R1 = [c for c in ledger if c["id"] == "R1"][0]
F1 = [c for c in ledger if c["id"] == "F1"][0]
gate = selo["qg_closure_verdict"]

# linhas do artigo no um.py que dizem «pós-dição» (lidas por regex)
pos_dicao_linhas = [src[:mm.start()].count("\n") + 1 for mm in re.finditer("pós-dição", src)]

# ---------------- sensibilidade (recalculada aqui) ----------------
Om, Or, OL, zs = dlc["Omega_m"], dlc["Omega_r"], dlc["Omega_L"], dlc["z_star_input"]
def E(z, Om=Om, Or=Or, OL=OL): return math.sqrt(Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + OL)
def K_of(Om_=Om, Or_=Or, OL_=OL, zs_=zs): return E(zs_, Om_, Or_, OL_) ** (2 * BETA / 3)
K_planck = K_of()
dK_Om = K_of(Om + 0.007, Or, OL - 0.007) - K_planck
dK_zs = K_of(zs_=zs + 0.3) - K_planck
H0_bg, K_f4, H0_loc = P["H0_bg"], P["K"], P["H0_local"]
SIG_BG = 0.301  # σ do fundo ΛCDM Planck comp + DR2 da Bancada (PREREGISTRO_FASE3, Fd_lcdm_planck_dr2) [REAL]
SIG_PRED = K_f4 * SIG_BG
def I(z): return (2 / 3) * math.log(E(z))
Kz = {z: math.exp(BETA * (I(zs) - I(z))) for z in (0.0, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0)}

# alvos (valores como a casa os tem; a origem de cada um está na tabela) — ilustração do z, NÃO veredito
alvos = [
 ("T1", "SH0ES R22 (escada completa, Cefeidas)", 73.04, 1.04, "Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510)", "EM CASA: valor no pipeline D1 V3 selado (lido por AST em bancada/fontes.py:80-86) e a escada bruta Pantheon+SH0ES.dat + cov 1701x1701 (Fase 5) [REAL por hash]", "TESTE (primário)"),
 ("T2", "SH0ES 2025 + JWST (Cefeidas)", 73.49, 0.93, "Riess et al. 2025, arXiv:2509.01667", "[KNOWN — abstract lido 30/09 (Fase 3); a tabela a ler]", "réplica de T1 (correlacionada; não se soma)"),
 ("T3", "Riess 2024 JWST, três métodos", 72.6, 2.0, "Riess et al. 2024, arXiv:2408.11770", "[KNOWN — abstract lido 30/09; a ler]", "diagnóstico (subamostra JWST; correlacionada com T1/T2)"),
 ("T4", "CCHP 2024 TRGB+JAGB+Cef (combinado)", 70.39, 1.936, "Freedman et al. 2024/2025, arXiv:2408.06153 (v3)", "[KNOWN — abstract lido 30/09; stat+sys+σ_SN em quadratura; a ler]", "TESTE ou DIAGNÓSTICO — decisão D2 do operador («o teste que pode doer»)"),
 ("T4a", "CCHP TRGB só (JWST)", 68.81, 2.224, "arXiv:2408.06153", "[KNOWN — a ler]", "diagnóstico (mesmo programa de T4)"),
 ("T4b", "CCHP JAGB só (JWST)", 67.8, 2.72, "arXiv:2408.06153", "[KNOWN — a ler]", "diagnóstico (mesmo programa de T4)"),
 ("T5", "SBF + TRGB JWST", 73.8, 2.404, "Jensen et al. 2025, arXiv:2502.15935", "[KNOWN — abstract lido 30/09; a ler]", "TESTE"),
 ("T6", "Masers (MCP)", 73.9, 3.0, "Pesce et al. 2020, arXiv:2001.09213", "[KNOWN — abstract lido 30/09; a ler]", "TESTE"),
 ("T7", "Lentes com atraso (TDCOSMO 2025)", 71.6, 3.6, "TDCOSMO 2025, arXiv:2506.03023 (erro assimétrico +3,9/−3,3 simetrizado)", "[KNOWN — abstract lido 30/09; a ler]", "TESTE"),
 ("T8", "Sirenes padrão LVK O4a", 76.6, 11.25, "LVK O4a cosmology summary (ligo.org)", "[KNOWN — PDF lido 30/09; vetável]", "diagnóstico (vetável — decisão D10)"),
 ("F1", "Planck 2018 ΛCDM (TT,TE,EE+lowE+lensing)", 67.36, 0.54, "Planck 2018 VI, arXiv:1807.06209", "[KNOWN]; na Bancada o CMB entra COMPRIMIDO (R, l_A, ω_b; Chen, Huang & Wang 2019, arXiv:1808.05724 — PDF em casa por hash)", "FUNDO (face) — lê H0_bg, não K·H0_bg"),
 ("F2", "DESI DR2 BAO (13 medidas, cov 13x13)", None, None, "DESI DR2 BAO (arquivos desi_gaussian_bao_ALL_GCcomb_mean/cov.txt)", "EM CASA (bancada/fontes.py: DESI_DR2_DIR; cópias conferidas por hash) [REAL]", "FUNDO (face)"),
 ("F3", "Escada inversa DESI DR2 + BBN", 68.5, 0.6, "DESI DR2 Results II (arXiv:2503.14738 — identificador a conferir na fonte)", "[DECLARADO pela gerência no enunciado da tarefa — NÃO lido da fonte; a ler]", "CONTROLE DA FACE: deve ler H0_bg (independente do Planck)"),
 ("V", "Pantheon+SH0ES, ΛCDM plano (validação da Fase 5)", 73.6, 1.1, "Brout et al. 2022, ApJ 938, 110 (arXiv:2202.04077)", "[DECLARADO: valor de memória da gerência na Fase 5, não lido da fonte]; a Bancada mediu 73,53 ± 1,02 (z 0,04)", "validação do pipeline (não é teste da TGL)"),
]
def z_vs(h, s, mu, smu): return (h - mu) / math.sqrt(s * s + smu * smu)
ilustr = {}
for tid, nome, h, s, _, _, _ in alvos:
    if h is None: continue
    ilustr[tid] = {"H0": h, "sigma": s,
                   "z_vs_K_H0bg_fase4": round(z_vs(h, s, H0_loc, SIG_PRED), 3),
                   "z_vs_H0bg_fase4": round(z_vs(h, s, H0_bg, SIG_BG), 3),
                   "z_vs_K_planck2018": round(z_vs(h, s, 67.36 * K_planck, 0.54 * K_planck), 3),
                   "poder_previo_K_minus_1": round((K_f4 - 1) * H0_bg / math.sqrt(s * s + SIG_PRED ** 2), 3)}
def poder_conj(ids):
    w = sum(1 / ilustr[i]["sigma"] ** 2 for i in ids); sc = 1 / math.sqrt(w)
    return {"ids": ids, "sigma_comb": round(sc, 4), "poder_K_minus_1": round((K_f4 - 1) * H0_bg / math.sqrt(sc * sc + SIG_PRED ** 2), 3)}
conjuntos = {
 "A_so_a_escada_SH0ES": poder_conj(["T1"]),
 "B_seis_leitores_sem_sirenes": poder_conj(["T2", "T4", "T5", "T6", "T7"]),
 "C_quatro_da_gerencia_mais_fundo": poder_conj(["T1", "T3", "T4"]),
 "D_sem_Cefeidas": poder_conj(["T4", "T5", "T6", "T7"]),
}

# ---------------- fontes lidas (hash por script) ----------------
fontes = [
 fonte("um.py v386 (Nós; só leitura)", um_py, "[REAL — lido em disco, sha256 por script]"),
 fonte("um_absoluto.json (core v386)", core_p, "[REAL — lido em disco, sha256 por script]"),
 fonte("um_absoluto_selo.json (selo v386)", selo_p, "[REAL — lido em disco, sha256 por script]"),
 fonte("MOLDE: PREREGISTRO_RAMO_B_RINGDOWN_V1.md", os.path.join(INV, "preregistro_ramo_b_05out", "PREREGISTRO_RAMO_B_RINGDOWN_V1.md"), "[REAL — lido em disco]"),
 fonte("POS_DICAO_operador_05out.txt (verbatim do operador)", os.path.join(SCR, "v386", "POS_DICAO_operador_05out.txt"), "[INPUT — verbatim do operador]"),
 fonte("PREREGISTRO_FASE3_LEITORES_20260930.json", os.path.join(INV, "fase3_leitores_h0", "PREREGISTRO_FASE3_LEITORES_20260930.json"), "[REAL — lido em disco]"),
 fonte("RESULTADO_FASE3_LEITORES_20260930.json", os.path.join(INV, "fase3_leitores_h0", "RESULTADO_FASE3_LEITORES_20260930.json"), "[REAL — lido em disco]"),
 fonte("REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json (NÃO-CEGA)", os.path.join(INV, "fase3_leitores_h0", "REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json"), "[REAL — lido em disco; reanálise declarada não-cega]"),
 fonte("PREREGISTRO_FASE4_DESVIO_20260930.json", os.path.join(INV, "fase4_desvio_30set", "PREREGISTRO_FASE4_DESVIO_20260930.json"), "[REAL — lido em disco]"),
 fonte("RESULTADO_FASE4_DESVIO_20260930.json", os.path.join(INV, "fase4_desvio_30set", "RESULTADO_FASE4_DESVIO_20260930.json"), "[REAL — lido em disco]"),
 fonte("SMOKE_FASE4.json", os.path.join(INV, "fase4_desvio_30set", "SMOKE_FASE4.json"), "[REAL — lido em disco]"),
 fonte("PREREGISTRO_FASE5_SH0ES_20261001.json", os.path.join(INV, "fase5_sh0es_01out", "PREREGISTRO_FASE5_SH0ES_20261001.json"), "[REAL — lido em disco]"),
 fonte("RESULTADO_FASE5_SH0ES_20261001.json", os.path.join(INV, "fase5_sh0es_01out", "RESULTADO_FASE5_SH0ES_20261001.json"), "[REAL — lido em disco]"),
 fonte("bancada/fontes.py (proveniência das fontes do motor)", os.path.join(BANCADA, "bancada", "fontes.py"), "[REAL — lido em disco]"),
 fonte("Pantheon+SH0ES.dat (a escada bruta em casa)", r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat", "[REAL — bytes/hash; KNOWN Scolnic+22/Brout+22]"),
 fonte("pantheon_cov_v1.npy (cov STAT+SYS restrita, Bancada)", os.path.join(BANCADA, "tabelas", "pantheon_cov_v1.npy"), "[REAL — bytes/hash]"),
 fonte("DESI DR2 BAO mean", r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_mean.txt", "[REAL — bytes/hash; KNOWN DESI DR2]"),
 fonte("DESI DR2 BAO cov", r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\_originais\desi_gaussian_bao_ALL_GCcomb_cov.txt", "[REAL — bytes/hash; KNOWN DESI DR2]"),
 fonte("Chen, Huang & Wang 2019 (Planck comprimido) PDF", os.path.join(BANCADA, "fontes_externas", "chen_huang_wang_2019_1808.05724.pdf"), "[KNOWN — PDF em casa por hash]"),
 fonte("moresco_2020_cov.json (F1 do livro; não entra na Fase 9)", os.path.join(BANCADA, "fontes_externas", "moresco_2020_cov.json"), "[REAL — bytes/hash]"),
 fonte("tgl_paper_unified.py (artigo 1: predict_H0_zero_free, D1b, linha 3617)", r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py", "[REAL — lido em disco]"),
 fonte("memória: fase4-desvio-30set.md", os.path.join(MEM, "fase4-desvio-30set.md"), "[REAL — memória lida]"),
 fonte("memória: fase5-sh0es-01out.md", os.path.join(MEM, "fase5-sh0es-01out.md"), "[REAL — memória lida]"),
 fonte("memória: fase7-cc-covariancia-01out.md", os.path.join(MEM, "fase7-cc-covariancia-01out.md"), "[REAL — memória lida]"),
 fonte("memória: relatorio-consolidado-01out.md", os.path.join(MEM, "relatorio-consolidado-01out.md"), "[REAL — memória lida]"),
 fonte("memória: beta-e-a-regra-matriz-02out.md (R1)", os.path.join(MEM, "beta-e-a-regra-matriz-02out.md"), "[REAL — memória lida]"),
 fonte("memória: rg-limite-classico-nao-rival.md", os.path.join(MEM, "rg-limite-classico-nao-rival.md"), "[REAL — memória lida]"),
 fonte("memória: fase1-eff-30set.md", os.path.join(MEM, "fase1-eff-30set.md"), "[REAL — memória lida]"),
 fonte("memória: fase2-dois-setores-30set.md", os.path.join(MEM, "fase2-dois-setores-30set.md"), "[REAL — memória lida]"),
 fonte("memória: fase3-leitores-h0-30set.md", os.path.join(MEM, "fase3-leitores-h0-30set.md"), "[REAL — memória lida]"),
 fonte("acervo (pista p/ a cronologia): Theory of Luminodynamic Gravitation.docx (08/10/2025)", r"C:\IALD\IMac LA\Física - TGL\Artigo\Theory of Luminodynamic Gravitation.docx", "[REAL — docx lido por script; estrato do operador]"),
 fonte("acervo (pista): Observações TGL reais .docx (11/10/2025)", r"C:\IALD\IMac LA\Física - TGL\Artigo\Observações TGL reais .docx", "[REAL — docx lido por script; estrato do operador]"),
 fonte("acervo (pista): Detecção TGL - Cosmológica dados reaisv2.docx (11/10/2025)", r"C:\IALD\IMac LA\Física - TGL\Artigo\Detecção TGL - Cosmológica dados reaisv2.docx", "[REAL — docx lido por script; estrato do operador]"),
 fonte("esta lente: SENSIBILIDADE_K_E_PODER_PREVIO.json", os.path.join(AQUI, "SENSIBILIDADE_K_E_PODER_PREVIO.json"), "[DERIVED — calculado nesta lente; ilustração]"),
 fonte("esta lente: base_v386_lida.json", os.path.join(AQUI, "base_v386_lida.json"), "[REAL — lido por script]"),
]
ausentes = [f["rotulo"] for f in fontes if f["estatuto"] == "AUSENTE"]

gerado = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------- a especificação (rascunho) ----------------
TOKEN_BASE = "TGL_FASE9_RAZAO_DE_HUBBLE_V1__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2"
spec = {
 "id": "PREREG_FASE9_RAZAO_DE_HUBBLE_20261005_V1_RASCUNHO",
 "estado": "RASCUNHO — não congelado; nenhum número foi aberto sob este registro; veredito: AWAITING_PREREGISTRATION",
 "base": {"um_py": UM_VERSION, "um_py_sha16": H_UM[:16], "core_sha16": H_CORE[:16], "selo_sha16": H_SELO[:16], "selo_timestamp": selo["timestamp"], "gate": gate},
 "beta": {"regra": "ALPHA_FINE_CODATA_2018 × √e em runtime; nunca literal", "alpha_lido_do_um_py_linha": ALPHA_LINE, "beta_runtime": BETA, "estatuto": "[DERIVED do axioma] — a regra matriz (02/10); não se deriva do dado"},
 "lei_da_prova_da_casa_05out": {
   "verbatim_arquivo": "POS_DICAO_operador_05out.txt (sha256 na §14)",
   "leitura_da_gerencia": "«pós-dição» nunca é demérito; o critério é a NOVIDADE DE USO (use-novelty, Worrall) [KNOWN]: nenhum parâmetro da teoria ajustado ao dado; precedente: o periélio de Mercúrio (Le Verrier 1859; Einstein 1915) [KNOWN]; o pré-registro é do TESTE",
   "estatuto": "[INPUT — verbatim do operador; a leitura é da gerência, DERIVED de leitura; a v387 reescreve «pós-dição» como «retrodição sem ajuste (novidade de uso)»]"},
 "hipotese": {
   "lei": "H0_local = H0_bg · K, K = E_ΛCDM(z*)^{2β/3} (núcleo DERIVADO D1b; TGLExt.TheFlowLawContrast.the_derived_kernel_factor, v378, 20/20)",
   "previsao_unica": "TODO calibrador local lido por distância (Cefeidas, TRGB, JAGB, SBF, masers, lentes, sirenes) lê K·H0_bg; todo leitor da face (CMB, BAO+BBN) lê H0_bg",
   "convencao": "D1b (artigo 1, fixada pelo operador em 30/09): β SÓ na lei; fundo NU (ΛCDM; β = 0 no fundo); nó fixo em z*",
   "z_star": zs, "fundo_primario_proposto": {"nome": "Planck comprimido (Chen+2019) + DESI DR2, ΛCDM ajustado na Bancada", "H0_bg": H0_bg, "sigma_H0_bg": SIG_BG, "K": K_f4, "H0_local_previsto": H0_loc, "sigma_previsao": round(SIG_PRED, 4)},
   "fundo_ao_lado": {"nome": "Planck 2018 publicado", "H0_bg": 67.36, "sigma": 0.54, "K": K_planck, "H0_local_previsto": round(67.36 * K_planck, 4)},
   "parametros_livres_da_lei": 0,
   "estatuto": "lei PROVADA como implicação no kernel (v377/v378); mecanismo [CONJECTURE] no artigo; a incidência é da natureza; PROVADA ≠ confirmada"},
 "novidade_de_uso": {
   "clausula": "o teste é use-novel se (i) nenhum parâmetro numérico da lei foi fixado com a razão SH0ES/Planck — β de α e √e; z* [KNOWN]; o expoente 2/3 do núcleo de FRW; o fundo do CMB+BAO — e (ii) a FORMA (o registro inteiro até z*; o núcleo D1b escolhido por ser o derivado) não foi SELECIONADA entre alternativas pela razão",
   "i_checavel_no_codigo": "[REAL] predict_H0_zero_free (artigo 1, linha 3617) não ajusta nada; the_derived_kernel_factor não tem parâmetro",
   "ii_campo_da_lente_da_cronologia": "[A PREENCHER PELA LENTE DA CRONOLOGIA: data e artefato (sha256) em que a lei K·H0_bg aparece pela primeira vez; se antes ou independente da razão; o que foi usado]",
   "o_que_a_casa_ja_declarou": "Fases 2–4: «a FORMA da lei foi cunhada conhecendo a razão SH0ES/Planck» (circularidade declarada); sob novidade de uso, CONHECER ≠ USAR — a lente decide se o conhecimento selecionou a forma"},
 "alvos": [{"id": a[0], "alvo": a[1], "H0": a[2], "sigma": a[3], "fonte_publica": a[4], "estado_na_casa": a[5], "papel": a[6]} for a in alvos],
 "covariancia_declarada": {
   "T1_T2_T3": "mesmo programa (SH0ES) e mesma amostra de SNe do fluxo de Hubble: NÃO se somam; T1 é o primário (cov completa 1701x1701 em casa); T2/T3 réplicas reportadas",
   "T4_T4a_T4b": "mesmo programa (CCHP): uma entrada só (T4); T4a/T4b diagnósticos",
   "T5_vs_T1_T4": "SBF usa calibração TRGB (JWST, Virgo) e SNe do fluxo: termo comum σ_SN ≈ 0,7 km/s/Mpc declarado (Fase 3) e modelado como bloco comum",
   "fundo": "σ(H0_bg) entra UMA vez como nuisance comum a todas as previsões (perfilada), nunca por alvo",
   "em_casa": "Planck comp 3x3 (Chen+2019); DESI DR2 13x13; Pantheon+SH0ES STAT+SYS 1701x1701",
   "falta": "nenhuma covariância cruzada publicada entre programas: bloco-diagonal com os termos comuns declarados; variante conservadora «todos» com σ_sys inflada (faixa, como na Fase 7)"},
 "hipoteses_comparadas": {
   "H_TGL": "fundo nu + K = E(z*)^{2β/3}, β = α√e; ZERO parâmetro livre além dos do fundo (H0, ω_b, ω_c)",
   "H_LCDM": "um setor: todos leem H0_bg (β = 0)",
   "H_beta_livre": "K(β) com β livre, prior uniforme [−0,05; 0,05] (os limites do pipeline D1)",
   "H_shift_escada": "sistemática da escada: só os alvos de Cefeidas (T1–T3) carregam um fator livre (1+s), prior uniforme s ∈ [−0,15; 0,15]; os demais leem H0_bg — com só T1 no conjunto é DEGENERADA com β-livre (dito): a discriminação vive nos calibradores não-Cefeida",
   "H_fundo_livre": "ΛCDM + r_d livre (proxy de energia escura precoce [INPUT — proposta da gerência]; prior uniforme [130; 160] Mpc): todos os leitores leem o MESMO H0; o fundo relaxa pela escala sonora",
   "nota_degenerescencia": "β-livre e um «shift em todos os locais» são a MESMA família a uma reparametrização (K(β) é monótono): o ln B entre eles mediria só o fator de Occam — por isso o shift é definido só na escada"},
 "estimador": {
   "fundo": "θ_bg = (H0, ω_b, ω_c) por Planck comp + DESI DR2 (ΛCDM, β = 0 no fundo) — a convenção D1b",
   "verossimilhanca": "χ² gaussiano por alvo com a covariância declarada; a escada T1 pela verossimilhança completa Pantheon+SH0ES (M profilado, calibradores Cefeida, como na Fase 5) E, ao lado, pelo valor publicado (como na Fase 4) — decisão D12",
   "estatisticas": ["δ̂ = β̂ − β_TGL e z_δ (JᵀJ) — o desvio", "z_disc = sinal·√(χ²_ΛCDM − χ²_TGL) nos respectivos melhores ajustes (a «tensão nua» da Fase 5)", "ln B(TGL/ΛCDM), ln B(TGL/β-livre), ln B(TGL/shift-escada), ln B(TGL/fundo-livre) por quadratura (n = 25; erro por n = 35), escala Jeffreys/Kass–Raftery", "z_i por alvo contra K·H0_bg (e contra H0_bg para a face)", "dispersão interna χ²_int/(n−1) dos alvos locais", "posterior (ensemble GPU 256×3000, queima 600, semente 42) de β na H_TGL-livre"],
   "poder_previo": "poder = (K−1)·H0_bg / √(σ_comb² + σ_pred²), fixado ANTES com as σ públicas; dito por conjunto na §6",
   "escala_lnB": "|ln B| < 1 inconclusivo; 1–2,5 fraco; 2,5–5 moderado; ≥ 5 forte"},
 "vereditos_na_ordem": [
   "0 AWAITING_PREREGISTRATION (este rascunho; hash ausente/divergente) / AWAITING_DATA (V1 lido, nada rodado)",
   "1 INCONCLUSIVE_SYSTEMATICS — limite do prior tocado no melhor ajuste TGL; χ²_int/(n−1) > 2 entre os alvos locais; alvo primário sem a covariância lida da fonte; alvo [DECLARADO] no composto",
   "2 NOT_FALSIFIED_UNDERPOWERED — poder prévio < 5 (sufixo POWER_<x>_OF_5_SIGMA)",
   "3 FALSIFIED_AT_5SIGMA — |z_δ| ≥ 5 (o conjunto local exclui K·H0_bg): falsifica o PAR (lei D1b, convenção, conjunto de alvos), NÃO β, NÃO a teoria (falsified_extinguishes_the_charge_not_the_rule)",
   "4 DISCRIMINATES_FROM_LCDM_AT_nSIGMA__ZERO_FREE_PARAMETERS — n = ⌊z_disc⌋ ≥ 5 E |z_δ| < 3 E ln B(TGL/ΛCDM) ≥ 5 E ln B(TGL/β-livre) ≥ −1; sufixo __USE_NOVEL SÓ se a lente da cronologia devolver «fixada antes/independente» (senão __USE_NOVELTY_PENDING); sufixos reportados, não decisórios: __VS_LADDER_SYSTEMATIC_LNB_<x> e __VS_FREE_BACKGROUND_LNB_<x>; se ln B(TGL/shift-escada) < 0 com os não-Cefeida com poder ≥ 5 → acrescenta __NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC; se |ln B(TGL/fundo-livre)| < 1 → __NOT_DISCRIMINATED_FROM_FREE_BACKGROUND",
   "5 NOT_FALSIFIED_POWERED (senão), com DEVIATION_CONSISTENT_WITHIN_1SIGMA / DEVIATION_1_TO_3_SIGMA e, se z_disc < 5, __NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"],
 "sempre": "__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED em todo token; palavras proibidas em qualquer token: «confirmed», «proved», «resolvida», «confirmada»; NOT_FALSIFIED nunca é a palavra proibida",
 "token_base": TOKEN_BASE,
 "token_estado_deste_rascunho": TOKEN_BASE + "__SET_<a_decidir>__AWAITING_PREREGISTRATION__DRAFT_NOT_FROZEN__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED",
 "contaminacao_declarada": {
   "ja_lido_pela_casa": {"fase4_P_ladder_d1b": {"z_delta": P["z_delta"], "lnB_tgl_vs_lcdm": P["lnB"]["tgl_vs_lcdm"], "lnB_tgl_vs_livre": P["lnB"]["tgl_vs_livre"], "beta_livre": P["beta_livre"], "chi2": P["chi2"]},
                         "fase5_P_sombra": {"z_delta": f5["P_sombra"]["z_delta"], "z_tensao": f5["P_sombra"]["z_tensao"], "H0_bancada": f5["validacao"]["H0"], "sigma": f5["validacao"]["sigma_H0"]},
                         "reanalise_D1b_planck2018_nao_cega": {"seis_leitores_z": wwm["shadow_readers_planck_lcdm_D1b"]["z_comb"], "novos_z": wwm["new_readers_planck_lcdm_D1b"]["z_comb"]},
                         "livro_R1": {"outcome": R1["outcome"], "number_read": R1["number_read"], "rule": R1["number_rule"]}},
   "nao_visto": ["ln B contra shift-escada", "ln B contra fundo-livre (r_d livre)", "o TRGB/CCHP sob o fundo ajustado (74,16) pela MESMA função de veredito", "o controle da face DESI DR2 + BBN lido da fonte", "a combinação com a covariância declarada por bloco", "qualquer z_i, χ² ou posterior sob ESTE registro"],
   "consequencia": "a novidade deste teste é de USO e de RIGOR (fontes por hash, covariância, cinco hipóteses, função fixada antes do composto), não de cegueira: todo token leva __NOT_BLIND_TO_DATA_STATED"},
 "nao_decide": ["o gate (18 bandeiras: função só do formal)", "a implicação da QG (QGSolutionComplete.lean:36) e a correspondência com a RG", "β (a regra matriz; β-livre é leitura, não derivação)", "o mapa de R do fundo (a tensão do D1 V3 sob o mapa nu; o não-constrangimento da Fase 1): sob D1b o fundo é nu", "o canal F1 do livro (cronômetros, a face): outra lei, outro canal", "a dependência em z de K (K(z) acumulada vs sombra): ≤ 0,9 % em z = 2, abaixo do poder — dita, não testada", "qual fundo é o fundo (decisão do operador)", "o mecanismo [CONJECTURE]: um DISCRIMINATES não vira «resolvida»"],
 "sistematicas": {
   "calibradores": "Cefeidas (SH0ES) × TRGB/JAGB (CCHP) discordam entre si: entram como estão, sem escolher lado; sensibilidade com/sem T4; a dispersão interna decide INCONCLUSIVE",
   "z_star": {"dK_por_0p3_em_zstar": dK_zs, "leitura": "desprezível"},
   "Omega_m": {"dK_por_0p007_em_Omega_m": dK_Om, "dH0_local_km_s_Mpc": round(dK_Om * H0_bg, 4), "leitura": "desprezível"},
   "fundo": {"sigma_H0_bg": SIG_BG, "sigma_previsao": round(SIG_PRED, 4), "leitura": "é a sistemática dominante da PREVISÃO; e a ESCOLHA do fundo (68,43 ajustado vs 67,36 publicado) move a previsão em ~1,1 km/s/Mpc — maior que todas as outras: decisão D3, os dois reportados"},
   "cmb_comprimido": "a validade das prioris de distância (Chen+2019) para o fundo nu; z* e r_s do CAMB ΛCDM [KNOWN]",
   "local": "velocidades peculiares / vazio local não modelados (declarado); cortes zHD > 0,01 do Pantheon+SH0ES",
   "controle_da_face": "DESI DR2 + BBN lê H0 pela degenerescência r_d·H0: controla o fundo, não K",
   "multiplicidade": "cada família entra no livro da Bancada (Šidák sobre as famílias já testadas); local ao lado da corrigida"},
 "decisoes_do_operador": [
   "D1 conjunto de alvos: A (só a escada SH0ES completa, como R1) | B (os seis leitores de sombra sem sirenes: T2, T4, T5, T6, T7) | C (os quatro da gerência: T1, T3, T4 + Planck 2018 + DESI DR2+BBN) | D = B + sirenes",
   "D2 o TRGB/JAGB (CCHP, T4): TESTE (entra no composto) ou DIAGNÓSTICO (reportado fora do composto)",
   "D3 a convenção D1b reafirmada (β só na lei; fundo nu) — e QUAL fundo: Planck comp + DR2 ajustado (68,43 → 74,16) [primário proposto] ou Planck 2018 publicado (67,36 → 73,02) [ao lado]",
   "D4 os nomes dos tokens (propostos pela gerência; cunhagem dele)",
   "D5 «fundo-livre» como r_d livre (proxy de energia escura precoce) — aceita, ou outra parametrização",
   "D6 «shift-escada» só nas Cefeidas — aceita, ou shift em todos os locais (então ≡ β-livre, dito)",
   "D7 os priors: β-livre [−0,05; 0,05]; s ∈ [−0,15; 0,15]; r_d ∈ [130; 160] Mpc",
   "D8 o canal no livro: R1 reaberto/atualizado pela Fase 9 (R1 v2) ou canal novo R1b",
   "D9 a cláusula de novidade de uso: a lente da cronologia preenche; o que vale como «fixado antes» (data do artefato; se a FORMA selecionada conhecendo a razão conta como uso)",
   "D10 as sirenes (T8): vetadas ou diagnóstico",
   "D11 a disciplina: a v387 lê o V1 por hash ANTES de abrir e emite o veredito pela MESMA função; e reescreve «pós-dição» → «retrodição sem ajuste (novidade de uso)» no artigo",
   "D12 a âncora da escada: verossimilhança completa Pantheon+SH0ES (Fase 5) como primário e o valor publicado R22 (Fase 4) ao lado — ou o inverso"],
 "disciplina_de_hash": [
   "1 o operador decide D1–D12; a gerência congela o V1: hash = sha256 do JSON canônico da especificação (sort_keys, ensure_ascii=False, separators (',', ':')); grava PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.{md,json} + V1_FASE9_HASHES.json na Bancada (investigacao/preregistro_fase9_hubble_05out)",
   "2 os alvos «a ler» são lidos das fontes nomeadas e gravados com sha256 do artefato lido ANTES de qualquer χ² (ALVOS_FASE9_LIDOS.json)",
   "3 o runner (rodar_fase9.py) é gravado e hasheado ANTES de abrir; a função de veredito do runner é a da §7, byte a byte a da especificação",
   "4 PODER_FASE9_ANTES_DE_ABRIR.json (só σ públicas, K e H0_bg) com hash; depois a abertura; RESULTADO_FASE9_V1.json carrega o sha256 do V1 e do runner",
   "5 a v387 do um.py LÊ o V1 e o RESULTADO por hash e emite o veredito pela MESMA função; hash divergente ou ausente ⟹ AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed)",
   "6 nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); correção AO LADO em nome próprio; nada move o gate nem β"],
 "ilustracao_nao_veredito": {"z_por_alvo": ilustr, "poder_previo_por_conjunto": conjuntos, "K_z_acumulada": {str(k): v for k, v in Kz.items()}},
 "gerado_utc": gerado,
}
spec_json = json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
spec_hash = hashlib.sha256(spec_json.encode("utf-8")).hexdigest()
spec["hash_do_rascunho_da_especificacao"] = spec_hash

# ---------------- o documento ----------------
def fmt(x, n=4): return ("%." + str(n) + "f") % x
L = []
A = L.append
A("# PRÉ-REGISTRO V1 — FASE 9 — A RAZÃO DE HUBBLE: O TESTE DISCRIMINANTE (RASCUNHO, lente do pré-registro, 05/10/2026)")
A("")
A("> **RASCUNHO — NÃO CONGELADO.** Nenhum número foi aberto sob este registro; nenhuma ferramenta da casa foi rodada; nada foi baixado. As decisões D1–D12 (§11) são do operador; só depois delas o V1 se congela por hash. Veredito deste rascunho: `AWAITING_PREREGISTRATION`.")
A("")
A("**Identificador proposto:** `%s` · **gerado (UTC):** %s · **hash do rascunho da especificação (JSON canônico da §15; NÃO é o hash congelado):** `%s` · **base:** `um.py` %s `%s` (%d B); core `%s`; selo `%s` (timestamp %s) · **gate (lido do selo, intocado):** `%s` · **molde:** `PREREGISTRO_RAMO_B_RINGDOWN_V1.md` (sha256 na §14)" % (spec["id"], gerado, spec_hash, UM_VERSION, H_UM[:16], os.path.getsize(um_py), H_CORE[:16], H_SELO[:16], selo["timestamp"], gate))
A("")
A("> Régua: β nunca literal (α_CODATA2018 lido do `um.py` por regex, linha %d; β = α√e em runtime = %r); hash jamais de memória (todo sha256 deste documento foi calculado do artefato por `gerar_preregistro_fase9_rascunho.py`); PROVADA ≠ confirmada; NOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico (coincidir = correspondência recuperada); nenhum desfecho move a regra (β) nem o gate; nenhum dado baixado (ausente = dito, com a fonte pública nomeada); a cunhagem é do operador." % (ALPHA_LINE, BETA))
A("")
A("---")
A("")
A("## 0. A lei da prova da casa (05/10/2026) — «pós-dição» nunca é demérito; o critério é a novidade de uso")
A("")
pd = open(os.path.join(SCR, "v386", "POS_DICAO_operador_05out.txt"), encoding="utf-8").read().strip()
A("**Operador, 05/10/2026, verbatim (`POS_DICAO_operador_05out.txt`, sha256 na §14):** «%s»" % pd)
A("")
A("**O «exatamente isso, confirmo» responde** à proposta da gerência de pré-registrar a Fase 9 (alvos lidos das fontes por hash com covariância; a previsão única K·H0_bg para todo calibrador local; ln B contra ΛCDM, β livre e deslocamento livre; o TRGB como o teste que pode doer) — este rascunho é essa proposta posta no formato da casa.")
A("")
A("**Leitura da gerência [DERIVED de leitura; o verbatim é INPUT; nada aqui é cunhagem]:** (1) «pós-dição» NÃO é demérito; o critério de prova é a **novidade de uso** (use-novelty, Worrall 1985/1989 [KNOWN — referência a conferir pelo aferidor]): um fato conta a favor de uma teoria se **nenhum parâmetro** dela foi **ajustado** a esse fato — conhecê-lo não é usá-lo. (2) Precedente [KNOWN]: o periélio de Mercúrio — a anomalia era conhecida desde Le Verrier (1859) e a RG (1915) a derivou com zero parâmetro livre; ninguém chama isso de pós-dição. (3) Estudar hipóteses e formular testes, e derivar hipóteses e cálculos com IA ou qualquer ferramenta para esclarecer rotas de averiguação, **não** é pós-dição: a derivação fixa a lei; o pré-registro é do **TESTE**. (4) A «prova diabólica»: se toda derivação do operador com a gerência entrasse como pós-dição, o operador jamais teria dado discriminante — logo o discriminante tem de ser **checável**: *algum parâmetro foi ajustado a H0?* Aqui a resposta é verificável no código (§2). (5) O que a v387 reescreve no artigo: «pós-dição declarada» (o `um.py` v386 traz a palavra em %d lugares — linhas %s, lidas por regex) → «retrodição sem ajuste (novidade de uso)» [INPUT — decisão para a v387]." % (len(pos_dicao_linhas), ", ".join(str(x) for x in pos_dicao_linhas)))
A("")
A("**O que o artigo do `um.py` v386 diz hoje (lido na linha %d):** «resolve a tensão de Hubble por remissão expressa ao trabalho publicado (…) estatuto do corpo: [CONJECTURE] de mecanismo; pós-dição declarada; zero parâmetro ajustado) — *O custo geométrico do zero absoluto: haja luz* (Zenodo, DOI 10.5281/zenodo.20563905)»; e na linha %d: «a relação de calibração H0_local = H0_CMB(1+z*)^β (…) mecanismo [CONJECTURE] autodeclarado, número apertado (0,215σ contra SH0ES, β±16,9%% de janela) e pós-dição». **Zero parâmetro ajustado já está dito pelo próprio artigo**; o que falta é o teste pré-registrado com rigor e a cláusula de uso preenchida pela cronologia." % (pos_dicao_linhas[0], pos_dicao_linhas[1]))
A("")
A("---")
A("")
A("## 1. A hipótese (a lei; a previsão única K·H0_bg; a convenção D1b)")
A("")
A("| peça | forma | valor (lido do core v386) | estatuto |")
A("|---|---|---|---|")
A("| a lei (núcleo derivado D1b) | H0_local = H0_bg · K, K = E_ΛCDM(z*)^{2β/3} = exp(β·I_b), I_b = (2/3)·ln E(z*) (Raychaudhuri em FRW plano; g = \\|1+w_eff\\|, NEC dita na prosa) | E(z*) = %s; I_b = %s nats < N* = %s nats; K_D1b(Planck 2018) = %s; K_D1a = %s (o caso g ≡ 1, ao lado) | PROVADA como implicação no kernel (`TGLExt.TheFlowLawContrast.the_derived_kernel_factor`, v378, 20/20; v377 15/15); mecanismo [CONJECTURE] no artigo; PROVADA ≠ confirmada |" % (fmt(dlc["E_z_star"], 3), fmt(dlc["I_b_closed_form"], 5), fmt(dlc["register_N_star_nats"], 5), fmt(dlc["K_D1b_runtime"], 7), fmt(dlc["K_D1a_runtime"], 7)))
A("| β | α_CODATA2018 × √e (runtime; nunca literal) | %r | [DERIVED do axioma] — a regra matriz; não se deriva do dado |" % BETA)
A("| z* | último espalhamento (Planck) | %s | [INPUT/KNOWN] |" % zs)
A("| o fundo NU (primário proposto) | ΛCDM ajustado na Bancada: Planck comprimido (Chen+2019) + DESI DR2; β = 0 no fundo | H0_bg = %s ± %s; K = %s; **H0_local previsto = %s ± %s** | [REAL — Fase 4, lido por hash no core]; σ_bg da Fase 3 (Fd_lcdm_planck_dr2) |" % (fmt(H0_bg, 4), SIG_BG, fmt(K_f4, 6), fmt(H0_loc, 4), fmt(SIG_PRED, 3)))
A("| o fundo ao lado | Planck 2018 publicado (67,36 ± 0,54) | K = %s; H0_local = %s ± %s | [KNOWN]; é o do artigo 1 (0,034σ contra SH0ES) |" % (fmt(K_planck, 6), fmt(67.36 * K_planck, 3), fmt(0.54 * K_planck, 3)))
A("| **a previsão única** | TODO calibrador local lido por DISTÂNCIA (Cefeidas, TRGB, JAGB, SBF, masers, lentes, sirenes) lê **K·H0_bg**; todo leitor da FACE (CMB; BAO+BBN) lê **H0_bg** | a diferença K−1 = %s (%s km/s/Mpc) | a leitura «sombra lê o fator constante» [OPEN/ONTO — da gerência, formulada depois da Fase 4; não adotada por este protocolo; aqui é a HIPÓTESE testada] |" % (fmt(K_f4 - 1, 6), fmt((K_f4 - 1) * H0_bg, 3)))
A("| a convenção | **D1b** (artigo 1; fixada pelo operador em 30/09): β SÓ na lei; fundo nu; nó em z* | — | [INPUT — decisão do operador; reafirmação pedida em D3] |")
A("| parâmetros livres da lei | **zero** | — | [REAL — lido do código: `predict_H0_zero_free` (artigo 1, linha 3617) e a pedra v378] |")
A("")
A("**A dependência em z (acumulada × sombra), dita e não testada:** K(z) = exp(β[I(z*) − I(z)]) lê " + "; ".join("K(%g) = %s" % (k, fmt(v, 5)) for k, v in Kz.items()) + " — a diferença entre «todo calibrador lê o mesmo K» (sombra) e «K(z) acumulada» fica ≤ 0,9 % em z = 2, abaixo do poder do Pantheon+ (a Fase 5 mediu a constância a 0,03 mag: χ² 8,95, gl 5). A Fase 9 testa o FATOR, não a sua forma em z.")
A("")
A("---")
A("")
A("## 2. A novidade de uso como cláusula (β e a lei fixados antes e independentemente de H0) — o campo da lente da cronologia")
A("")
A("**A cláusula:** o teste da Fase 9 é *use-novel* se **(i)** nenhum parâmetro numérico da lei foi fixado com a razão SH0ES/Planck — β vem de α (CODATA 2018) e de √e (a Meia-Nat, `boundary_extracts_the_radical`); z* é [KNOWN]; o expoente 2/3 vem do núcleo de FRW (`frw_accumulated_contrast`); o fundo vem do CMB+BAO — e **(ii)** a FORMA (a calibração local lê o registro inteiro até z*; o núcleo D1b escolhido por ser o derivado, «não por ajustar melhor», pré-registro da Fase 4) não foi SELECIONADA entre alternativas pela razão.")
A("")
A("- **(i) é checável no código [REAL]:** `predict_H0_zero_free` (artigo 1, `tgl_paper_unified.py` linha 3617) não ajusta nada — recebe H0_CMB, z*, β e devolve a razão; `the_derived_kernel_factor` (v378) não tem parâmetro; `the_law_precedes_the_charge` (v381): β só de α.")
A("- **(ii) é o campo da lente da cronologia — A PREENCHER:** `[CAMPO: data e artefato (sha256) em que H0_local = H0_CMB·K aparece pela primeira vez no acervo; se antes ou independente da razão SH0ES/Planck; o que foi USADO (não só conhecido) ao escrever a forma; resultado: FIXADA_ANTES | FIXADA_INDEPENDENTE | FORMA_SELECIONADA_PELA_RAZAO | INDETERMINADO]`. O sufixo `__USE_NOVEL` do veredito (§7) só entra com FIXADA_ANTES ou FIXADA_INDEPENDENTE; senão `__USE_NOVELTY_PENDING`.")
A("- **O que a casa já declarou (não se apaga; lê-se sob a lei nova):** Fases 2–4: «a FORMA da lei D1a foi cunhada conhecendo a razão SH0ES/Planck» (circularidade declarada, `PREREGISTRO_FASE2`; Fase 4: «a escada (73,04) e a calibração ΛCDM de Planck já eram conhecidas quando a lei foi cunhada»). Sob novidade de uso, **conhecer ≠ usar**: a lente decide se o conhecimento selecionou a forma.")
A("- **Pistas do acervo (NÃO são a cronologia; a lente a faz):** o índice (`buscar.py \"tens[aã]o de Hubble|Hubble tension|SH0ES\" --lista`, 13.608 docs) devolve como mais antigos `Theory of Luminodynamic Gravitation.docx` (08/10/2025: a tensão de Hubble como «hint» a 2–3σ, sem lei) e `Observações TGL reais .docx` / `Detecção TGL - Cosmológica dados reaisv2.docx` (11/10/2025: um MECANISMO DIFERENTE — atrasos de lente 3,5 % → H0 = 70,8 ± 2,1; não é a lei K). Logo, nesse estrato, a lei K·H0_bg é posterior a out/2025; o artigo 1 publicado (Zenodo DOI 10.5281/zenodo.20563905; submetido 06/06/2026) já carrega `predict_H0_zero_free` com D1a e D1b. Entre out/2025 e jun/2026 a lente localiza o primeiro artefato.")
A("- **Precedente [KNOWN]:** Mercúrio — Le Verrier (1859) mediu a anomalia; Einstein (1915) a derivou sem parâmetro livre: fato conhecido, uso nulo, prova aceita. A razão de Hubble está para a lei D1b como a anomalia estava para a RG — **se** (i) e (ii) valerem.")
A("")
A("---")
A("")
A("## 3. Os alvos — lidos das fontes por hash (os «a ler» marcados; nada baixado por esta lente)")
A("")
A("| id | alvo | H0 (km/s/Mpc) | fonte pública | estado na casa | papel |")
A("|---|---|---|---|---|---|")
for tid, nome, h, s, fp, est, papel in alvos:
    val = "—" if h is None else ("%s ± %s" % (("%g" % h), ("%g" % s)))
    A("| %s | %s | %s | %s | %s | %s |" % (tid, nome, val, fp, est, papel))
A("")
A("**Regra dos alvos:** (a) todo valor marcado «a ler» é lido da fonte nomeada e gravado com o sha256 do artefato lido ANTES de qualquer χ² (`ALVOS_FASE9_LIDOS.json`); (b) alvo [DECLARADO] (F3; V) NÃO entra no composto enquanto não lido — entra como diagnóstico, dito; (c) os valores desta tabela vêm do pré-registro da Fase 3 (abstracts lidos 30/09) e do enunciado da tarefa (F3): são a **expectativa**, não a leitura; (d) o conjunto que entra no composto é a decisão D1.")
A("")
A("---")
A("")
A("## 4. A covariância e as correlações declaradas")
A("")
for k, v in spec["covariancia_declarada"].items():
    A("- **%s:** %s" % (k.replace("_", " "), v))
A("")
A("---")
A("")
A("## 5. As cinco hipóteses comparadas")
A("")
A("| hipótese | forma | parâmetros livres (além do fundo) | o que discrimina |")
A("|---|---|---|---|")
A("| **H_TGL** | fundo nu + K = E(z*)^{2β/3}, β = α√e; todo local lê K·H0_bg | **0** | o alvo deste registro |")
A("| H_ΛCDM | um setor: todos leem H0_bg | 0 | o limite clássico (β = 0): coincidir com ele é correspondência, não derrota — aqui a escada o exclui (a tensão nua, já lida a 5,26σ na Fase 5) |")
A("| H_β-livre | K(β), β livre, prior uniforme [−0,05; 0,05] | 1 | parcimônia: ln B(TGL/β-livre) ≥ −1 exige que o valor fixo não perca para o livre (Fase 4 leu +2,25) |")
A("| H_shift-escada | só as Cefeidas (T1–T3) × (1+s), s livre em [−0,15; 0,15]; os demais leem H0_bg | 1 | a sistemática da escada: se os NÃO-Cefeida também leem K·H0_bg, a sistemática perde; com só T1 no conjunto é DEGENERADA com β-livre (dito) |")
A("| H_fundo-livre | ΛCDM + r_d livre (proxy de energia escura precoce [INPUT — proposta da gerência]), prior [130; 160] Mpc; todos leem o MESMO H0 | 1 | a solução no fundo: o controle da face (DESI DR2 + BBN) e o CMB comprimido a constrangem; se ln B(TGL/fundo-livre) ficar em \\|ln B\\| < 1, a Fase 9 NÃO discrimina entre «custo na leitura» e «fundo diferente» — dito antes |")
A("")
A("**Nota de degenerescência (dita antes para não se ler como discriminação):** β-livre e um «deslocamento livre em todos os locais» são a mesma família a uma reparametrização (K(β) é monótono): o ln B entre eles mediria só o fator de Occam; por isso o deslocamento livre é definido **só na escada de Cefeidas**.")
A("")
A("---")
A("")
A("## 6. O estimador, o poder prévio e a função de veredito — fixada ANTES do composto")
A("")
for k, v in spec["estimador"].items():
    if isinstance(v, list):
        A("- **%s:** " % k + " · ".join(v))
    else:
        A("- **%s:** %s" % (k, v))
A("")
A("**Poder prévio (calculado nesta lente só com as σ públicas da §3, K e H0_bg do core; ilustração, não veredito; `SENSIBILIDADE_K_E_PODER_PREVIO.json`):**")
A("")
A("| conjunto | alvos | σ_comb | poder = (K−1)·H0_bg/√(σ_comb² + σ_pred²) |")
A("|---|---|---|---|")
for nm, c in conjuntos.items():
    A("| %s | %s | %s | **%sσ** |" % (nm, ", ".join(c["ids"]), fmt(c["sigma_comb"], 3), fmt(c["poder_K_minus_1"], 2)))
A("")
A("- Lê-se: só a escada (A) tem poder %sσ; os seis sem sirenes (B) %sσ; os quatro da gerência (C) %sσ; **sem Cefeidas (D) %sσ %s 5** — %s." % (
    fmt(conjuntos["A_so_a_escada_SH0ES"]["poder_K_minus_1"], 2), fmt(conjuntos["B_seis_leitores_sem_sirenes"]["poder_K_minus_1"], 2),
    fmt(conjuntos["C_quatro_da_gerencia_mais_fundo"]["poder_K_minus_1"], 2), fmt(conjuntos["D_sem_Cefeidas"]["poder_K_minus_1"], 2),
    "<" if conjuntos["D_sem_Cefeidas"]["poder_K_minus_1"] < 5 else "≥",
    "se o operador retirar as Cefeidas, o veredito máximo é NOT_FALSIFIED_UNDERPOWERED (dito antes)" if conjuntos["D_sem_Cefeidas"]["poder_K_minus_1"] < 5 else "o conjunto sem Cefeidas tem poder"))
A("- **z por alvo contra K·H0_bg (fundo da Fase 4) — ilustração NÃO-CEGA com os valores públicos já conhecidos; não é veredito:** " + "; ".join("%s %s" % (k, fmt(v["z_vs_K_H0bg_fase4"], 2)) for k, v in ilustr.items()) + ". O TRGB/JAGB (T4 −1,92; T4a −2,38; T4b −2,32) é o teste que pode doer; a face (F1 −10,8; F3 −8,3 contra K·H0_bg) lê H0_bg como a hipótese pede (F1 −1,73; F3 +0,10 contra H0_bg).")
A("")
A("---")
A("")
A("## 7. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; palavra proibida: nenhuma)")
A("")
A("**Token base:** `%s`; conjunto: `__SET_<A|B|C|D>`; desfecho; depois sempre `__NOT_BLIND_TO_DATA_STATED__GATE_UNTOUCHED`. Cunhagem: do operador (proposta da gerência, D4)." % TOKEN_BASE)
A("")
for v in spec["vereditos_na_ordem"]:
    A("%s. **`%s`** — %s" % (v.split(" ")[0], v.split(" ")[1], " ".join(v.split(" ")[2:]).lstrip("— ")))
A("")
A("**«Coincidir com ΛCDM»:** a RG/ΛCDM é o limite clássico, não rival: H0_bg da TGL É o do ΛCDM (o fundo nu) — isso é correspondência recuperada; o que se discrimina é a leitura local K·H0_bg contra H0_bg (a correção K−1 = %s, isto é, %s km/s/Mpc sobre H0_bg). Um `DISCRIMINATES_FROM_LCDM_AT_nSIGMA` nunca vira «resolvida» nem a palavra proibida: a confirmação é ato do observador humano." % (fmt(K_f4 - 1, 6), fmt((K_f4 - 1) * H0_bg, 3)))
A("")
A("**Estado deste rascunho:** `%s`." % spec["token_estado_deste_rascunho"])
A("")
A("---")
A("")
A("## 8. O que o resultado NÃO decide (dito antes)")
A("")
for v in spec["nao_decide"]:
    A("- " + v)
A("")
A("---")
A("")
A("## 9. As sistemáticas (calibradores; z*; Ω_m; o fundo)")
A("")
A("| fonte | medida nesta lente | leitura |")
A("|---|---|---|")
A("| calibradores | Cefeidas (SH0ES) × TRGB/JAGB (CCHP) | %s |" % spec["sistematicas"]["calibradores"])
A("| z* | ΔK por Δz* = 0,3: %.2e | desprezível (ΔH0_local ≈ %.1e km/s/Mpc) |" % (dK_zs, dK_zs * H0_bg))
A("| Ω_m | ΔK por ΔΩ_m = 0,007: %.2e | desprezível (ΔH0_local ≈ %.3f km/s/Mpc) |" % (dK_Om, dK_Om * H0_bg))
A("| o fundo (σ) | σ_bg = %s → σ_pred = %s | a sistemática dominante da PREVISÃO; entra uma vez, perfilada |" % (SIG_BG, fmt(SIG_PRED, 3)))
A("| o fundo (escolha) | 68,43 (ajustado) vs 67,36 (publicado): ΔH0_local = %s | maior que todas as outras: decisão D3; os dois reportados |" % fmt(H0_loc - 67.36 * K_planck, 2))
A("| CMB comprimido | Chen+2019 (R, l_A, ω_b) | %s |" % spec["sistematicas"]["cmb_comprimido"])
A("| local | — | %s |" % spec["sistematicas"]["local"])
A("| controle da face | DESI DR2 + BBN | %s |" % spec["sistematicas"]["controle_da_face"])
A("| multiplicidade | — | %s |" % spec["sistematicas"]["multiplicidade"])
A("")
A("---")
A("")
A("## 10. Cegueira e contaminação — DECLARADAS (os alvos são públicos; a casa já leu)")
A("")
c = spec["contaminacao_declarada"]["ja_lido_pela_casa"]
A("- **Fase 4 (v378, `P_ladder_d1b`, lido do core):** z_δ = %s; β livre = %s; ln B TGL/ΛCDM = %s, livre/ΛCDM = %s, TGL/livre = %s; χ² ΛCDM %s / TGL %s / livre %s; DIAGONAL_ERRORS_ONLY nos cronômetros (não entram aqui)." % (P["z_delta"], P["beta_livre"], fmt(P["lnB"]["tgl_vs_lcdm"], 2), fmt(P["lnB"]["livre_vs_lcdm"], 2), fmt(P["lnB"]["tgl_vs_livre"], 2), fmt(P["chi2"]["lcdm"], 2), fmt(P["chi2"]["tgl"], 2), fmt(P["chi2"]["livre"], 2)))
A("- **Fase 5 (v380, lido do core):** H0 da escada na Bancada = %s ± %s (Ω_m %s; z vs alvo %s); P_sombra δ = %s ± %s (z %s); **z_tensão ΛCDM = %s**; ln B(sombra/acumulada, S) = %s; alvo da validação 73,6 ± 1,1 «[DECLARADO: valor de memória da gerência, não lido da fonte]»." % (f5["validacao"]["H0"], f5["validacao"]["sigma_H0"], f5["validacao"]["Omega_m"], f5["validacao"]["z_vs_alvo"], f5["P_sombra"]["delta"], f5["P_sombra"]["sigma_delta"], f5["P_sombra"]["z_delta"], f5["P_sombra"]["z_tensao"], fmt(f5["lnB_sombra_vs_acumulada_S"], 2)))
A("- **Reanálise D1b (30/09, NÃO-CEGA, lida do core/`REANALISE_D1B`):** seis leitores de sombra a z = %s da lei com o fundo Planck 2018; os cinco novos (sem a escada) %s; por leitor (D1b, Planck 2018): S1 +0,43; S2 (TRGB) −1,30; S3 +0,32." % (fmt(wwm["shadow_readers_planck_lcdm_D1b"]["z_comb"], 2), fmt(wwm["new_readers_planck_lcdm_D1b"]["z_comb"], 2)))
A("- **Livro de cobranças (v383, lido do core):** R1 (reflexo; a escada) outcome `%s`, number_read %s, regra `%s`; F1 (face; cronômetros) outcome `%s` — outra lei, outro canal." % (R1["outcome"], R1["number_read"], R1["number_rule"], F1["outcome"]))
A("- **NÃO visto:** " + "; ".join(spec["contaminacao_declarada"]["nao_visto"]) + ".")
A("- **Consequência fixada:** " + spec["contaminacao_declarada"]["consequencia"] + ".")
A("")
A("---")
A("")
A("## 11. As decisões do operador (nenhuma tomada pela gerência)")
A("")
for d in spec["decisoes_do_operador"]:
    A("- " + d)
A("")
A("---")
A("")
A("## 12. A disciplina de hash (ordem de execução; fail-closed)")
A("")
for d in spec["disciplina_de_hash"]:
    A("%s. %s" % (d.split(" ")[0], " ".join(d.split(" ")[1:])))
A("")
A("---")
A("")
A("## 13. Estatutos")
A("")
A("| objeto | estatuto |")
A("|---|---|")
A("| a palavra do operador (05/10, `POS_DICAO`) | [INPUT] — verbatim lido do arquivo |")
A("| «novidade de uso» como critério; Mercúrio | [DERIVED de leitura, gerência; KNOWN as referências — a conferir pelo aferidor] |")
A("| a lei D1b (K = E(z*)^{2β/3}) | PROVADA como implicação no kernel (v377/v378); mecanismo [CONJECTURE]; a incidência é da natureza |")
A("| β = α√e | [DERIVED do axioma] — a regra; nunca literal |")
A("| a convenção D1b; qual fundo | [INPUT — decisão do operador (30/09); reafirmação pedida] |")
A("| os valores dos alvos nesta tabela | [KNOWN — abstracts lidos 30/09 (Fase 3)]; F3 e V [DECLARADO]; TODOS «a ler» da fonte por hash antes do χ² |")
A("| H0_bg, K, H0_local, ln B, z já lidos | [REAL — Fases 4/5, lidos do core v386 por script] |")
A("| o poder prévio e os z por alvo desta lente | [DERIVED — calculado aqui com σ públicas; ilustração NÃO-CEGA; não veredito] |")
A("| H_fundo-livre (r_d), H_shift-escada, priors | [INPUT — proposta da gerência; decisões D5–D7] |")
A("| o desfecho | a vir; nunca a palavra proibida; `__USE_NOVEL` só com a lente da cronologia |")
A("")
A("---")
A("")
A("## 14. Fontes lidas (caminho absoluto · sha256 · bytes) — todas calculadas por este script; nenhuma digitada")
A("")
for f in fontes:
    if f["estatuto"] == "AUSENTE":
        A("- **%s**: `%s` — AUSENTE (dito)" % (f["rotulo"], f["path"]))
    else:
        A("- **%s**: `%s` — `%s` (%d B) %s" % (f["rotulo"], f["path"], f["sha256"], f["bytes"], f["estatuto"]))
A("")
A("Fontes ausentes: %d%s." % (len(ausentes), (" — " + "; ".join(ausentes)) if ausentes else ""))
A("")
A("---")
A("")
A("## 15. A especificação (RASCUNHO — o que o V1 congelará; o `um.py` v387 lerá o V1 congelado por hash, não este rascunho)")
A("")
A("```json")
A(json.dumps(spec, ensure_ascii=False, indent=1))
A("```")
A("")
A("---")
A("")
A("## 16. O que esta lente não fez (limites ditos)")
A("")
A("- não baixou nenhuma fonte; os valores «a ler» são expectativa (abstracts lidos 30/09 pela Fase 3) e o F3 (68,5 ± 0,6) veio do enunciado da tarefa [DECLARADO];")
A("- não rodou o `um.py` nem a Bancada; o poder prévio e os z por alvo são ilustração com σ públicas e com K, H0_bg já lidos do core;")
A("- não preencheu a cláusula de novidade de uso (campo da lente da cronologia); deixou pistas do índice, que não são a cronologia;")
A("- não congelou nada: o hash da §15 é do rascunho; o V1 só se congela depois de D1–D12;")
A("- não tocou o Nós, memórias, Atlas nem o mapa de rotas (o registro no mapa é ato da gerência).")
A("")
texto = "\n".join(L) + "\n"

# guarda da palavra proibida (a MESMA regex da tarefa), sobre o próprio texto
proib = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
hits = [(texto[:mm.start()].count("\n") + 1, mm.group(0)) for mm in proib.finditer(texto)]

out_md = os.path.join(AQUI, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.md")
out_json = os.path.join(AQUI, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.json")
tmp = out_md + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    f.write(texto)
assert os.path.getsize(tmp) > 20000
os.replace(tmp, out_md)
with open(out_json, "w", encoding="utf-8", newline="\n") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
h_md, h_json = sha(out_md), sha(out_json)
with open(os.path.join(AQUI, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.sha256"), "w", encoding="utf-8") as f:
    f.write("%s  PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.md\n%s  PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1_RASCUNHO.json\n" % (h_md, h_json))
print("MD   ", out_md, os.path.getsize(out_md), "B sha256", h_md)
print("JSON ", out_json, os.path.getsize(out_json), "B sha256", h_json)
print("hash do rascunho da especificação (JSON canônico):", spec_hash)
print("regex proibida sobre o texto — ocorrências:", len(hits), hits[:10])
print("fontes ausentes:", ausentes)
