# -*- coding: utf-8 -*-
"""Inventario 'OS DADOS NA CASA' para o pre-registro do ramo B (tau* = k GM/c^3) do ringdown — v386.
Lente de aferidor: cada hash/bytes abaixo e LIDO do artefato por este script; nada vem de memoria.
Nada se baixa; nada se escreve fora desta pasta. Estatutos marcados por item."""
import hashlib, json, os, glob, io, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(AQUI, "INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.json")
OUT_MD = os.path.join(AQUI, "INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.md")

def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()[:16]

def arq(p, papel, conteudo, uso, estatuto, extra=None):
    """uso: REUTILIZAVEL_JA | REUTILIZAVEL_APOS_EXTRACAO | PRECISA_DADO_NOVO | AUSENTE | HISTORICO"""
    d = {"caminho": p, "papel": papel, "conteudo": conteudo, "uso": uso, "estatuto": estatuto}
    if os.path.isfile(p):
        d["bytes"] = os.path.getsize(p); d["sha16"] = sha16(p); d["existe"] = True
    else:
        d["existe"] = False; d["bytes"] = None; d["sha16"] = None
    if extra: d.update(extra)
    return d

def pasta(p, padrao, papel, conteudo, uso, estatuto, extra=None):
    fs = [f for f in glob.glob(os.path.join(p, padrao), recursive=True) if os.path.isfile(f)]
    d = {"caminho": p, "padrao": padrao, "papel": papel, "conteudo": conteudo, "uso": uso, "estatuto": estatuto,
         "existe": os.path.isdir(p), "n_arquivos": len(fs), "bytes_total": sum(os.path.getsize(f) for f in fs)}
    if extra: d.update(extra)
    return d

PONTE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um"
NOS = PONTE + r"\Nós"
CACHE = PONTE + r"\cache"
BANC = r"C:\IALD\Bancada_Um"
ORD = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
TUN = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
SCR = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"

inv = {"gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
       "lente": "dados_na_casa (v386, ramo B do ringdown)",
       "regra": "hash/bytes lidos do artefato por este script; nada baixado; nada escrito fora da pasta da lente; PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMED",
       "beta_tgl_runtime": None, "secoes": {}}
import math
ALPHA = 7.2973525693e-3
inv["beta_tgl_runtime"] = ALPHA * math.sqrt(math.e)

# ---------- (1) catalogos com M_f, a_f por evento ----------
S1 = []
S1.append(arq(BANC + r"\investigacao\fase6_eco_radical_01out\catalogo_v3.csv",
    "catalogo da amostra pre-registrada da Fase 6 (244 BBH O1-O4)",
    "commonName, version, catalog.shortName, GPS, mass_1/2_source (+-), network_matched_filter_snr, chi_eff (+-), final_mass_source, redshift, p_astro, far, era, src, files_4k (URLs GWOSC H1/L1). 244 linhas + cabecalho. Sem a_f, sem posteriors.",
    "REUTILIZAVEL_JA", "[REAL — lido; conteudo GWOSC = KNOWN]"))
S1.append(arq(CACHE + r"\bancada_01out\remanescentes_v3.json",
    "remanescentes por evento (244) exportados do WSL para a Fase 6",
    "por evento: Mf_det (catalogo final_mass_source*(1+z); UIB2016 se faltar), a_f_HBR2016 (lalinference nrutils de m1_det,m2_det,chi_eff,chi_eff), m1_det, m2_det, chi_eff, z, snr_net, era, src, f_qnm_220_hz e tau_d_220_ms (Berti+2006), tau MAY/KMS. Medianas, nao posteriors. Inclui GW250114_082203.",
    "REUTILIZAVEL_JA", "[REAL — lido; a_f e Kerr-fit KNOWN sobre medianas]"))
S1.append(arq(BANC + r"\investigacao\fase6_eco_radical_01out\GWOSC_ALLEVENTS_20261001.json",
    "dump do eventapi do GWOSC (todos os catalogos) em 01/10/2026",
    "671 evento-versoes (GWTC-1..5.0, O4_Discovery_Papers, IAS-O3a…): mass_1/2_source, chi_eff, total_mass_source, chirp_mass(_source), luminosity_distance, redshift, far, p_astro, network_matched_filter_snr, final_mass_source (415 nao nulos). Sem a_f.",
    "REUTILIZAVEL_JA", "[REAL — lido; KNOWN]"))
S1.append(arq(BANC + r"\investigacao\fase6_eco_radical_01out\GWOSC_INVENTARIO_20261001.json",
    "inventario por evento (chave -> cat, gps, snr, m1, m2, Mf, Mtot, z, chi_eff, far, p_astro, dets_4k, files_4k)",
    "um registro por evento com URLs dos HDF5 de 4 kHz por detector", "REUTILIZAVEL_JA", "[REAL — lido]"))
S1.append(arq(r"C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv",
    "catalogo GWTC-1..3 da cache de maio (usado pelo ringdown V1/V2, H2, eco PE/search)",
    "89 eventos; colunas incluem mass_1/2_source(+-), chi_eff(+-), total_mass_source, chirp_mass_source, luminosity_distance, redshift, far, final_mass_source(+-) (colunas 41-43). Sem a_f.",
    "REUTILIZAVEL_JA", "[REAL — lido; KNOWN]"))
S1.append(arq(CACHE + r"\gw\GWOSC_ECHO_WINDOWS_V1.manifest.json",
    "manifesto das janelas de eco da cache de maio (v341)",
    "89 eventos com M_f_source, M_f_detector, redshift, network_snr, catalog, version; 178 series com sha256 do npz-fonte; npz GWOSC_ECHO_WINDOWS_V1.npz (170 chaves).",
    "REUTILIZAVEL_JA", "[REAL — lido]"))
S1.append(arq(CACHE + r"\gw\RINGDOWN_DEPHASING_V2_RESULT.json",
    "resultado V2 do dephasing no ringdown (10/09/2026) — contem a previsao de Kerr por serie",
    "per_series (170): Mf_det, a_f (SimIMREOBFinalMassSpin/SEOBNRv4 das medianas), f_gr, tau_gr_ms, q_gr, delta_pred_A (t_P), delta_pred_B (GM_f/c^3), anchor_snr, starts{3ms,6ms: f_obs, tau_obs_ms, snr, delta_obs, delta_f, on_edge, bias_rel, sigma_rel, used, reason}; stacks 3ms/6ms; instrument lalsuite 7.7.1 WSL /opt/lal_env; catalog sha256 895250e9…; sources_sha256 (169 npz).",
    "REUTILIZAVEL_JA", "[REAL — lido por hash no um.py: ff15f023dd91d8c7]"))
S1.append(arq(ORD + r"\bis\015\t08\IGWN-GWTC4p0-38214bd95_724-GW231206_233901-combined_PEDataRelease.hdf5",
    "unico PE data release completo (GWTC-4.0) de um evento O4 em disco (piloto T08 da ORDEM 015)",
    "posteriors IMR completos (massas, spins; remanescente por fit) de GW231206_233901 — formato PESummary [DECLARADO: nao aberto nesta lente]",
    "REUTILIZAVEL_JA", "[DECLARADO — conteudo; REAL — bytes/hash]"))
inv["secoes"]["1_catalogos_Mf_af_por_evento"] = {
    "itens": S1,
    "ausente_dito": [
        {"o_que": "posteriors IMR (m1, m2, chi, z -> M_f, a_f por amostragem) dos 177 BBH de O4 da amostra da Fase 6 (salvo GW231206_233901 acima e os 33 pSEOB da GWTC-5.0 TGR, que trazem o remanescente pSEOB)",
         "consulta": "find ORDEM_013_RINGDOWN -maxdepth 4 -iname '*.h5' -size +100k; find cache/public -maxdepth 7 …: so 1 PEDataRelease (GW231206_233901) + 33 pSEOB metafiles + 18 rin GWTC-3 + GW250114",
         "fonte_publica": "GWTC-4.0 / GWTC-5.0 PE data releases (IGWN 'combined_PEDataRelease.hdf5' por evento, via GWOSC/Zenodo); censo T08 da ORDEM 015 [DECLARADO]: 74 eventos, 70 com PE publico listado, 40,77 GB, ~7,5 h so de transferencia",
         "estatuto": "AUSENTE (RD-02 pede propagar posteriors ate tau_GR; hoje so medianas)"}]}

# ---------- (2) resultados publicados de testes de ringdown ----------
S2 = []
PUB = ORD + r"\cache\public"
S2.append(arq(PUB + r"\21454847\pSEOB.tar.gz", "GWTC-5.0 TGR (Zenodo 21454847) — pipeline pSEOB (ringdown parametrizado de sinal completo)",
    "arquivo-fonte; extraido em extracted/pSEOB/metafiles (33 metafiles PESummary pSEOB_<evento>_Prod0.h5, com df220/dtau220 e o remanescente)", "REUTILIZAVEL_JA", "[REAL — bytes/hash; KNOWN]"))
S2.append(pasta(PUB + r"\21454847\extracted\pSEOB\metafiles", "*.h5", "GWTC-5.0 TGR pSEOB — posteriors por evento (33)",
    "GW150914_095045 GW170104_101158 GW190519_153544 GW190521_074359 GW190630_185205 GW190828_063405 GW190910_112807 GW191109_010717 GW200129_065458 GW200208_130117 GW200224_222234 GW200311_115853 GW230628_231200 GW230914_111401 GW230927_153832 GW231028_153006 GW231102_071736 GW231206_233901 GW231226_101520 GW240511_031507 GW240514_121713 GW240615_113620 GW240621_195059 GW240705_053215 GW240716_034900 GW240919_061559 GW240920_124024 GW241006_015333 GW241127_061008 GW241129_021832 GW241225_082815 GW250114_082203 GW250119_025138",
    "REUTILIZAVEL_JA", "[REAL — contagem/bytes; KNOWN]",
    {"sha16_pSEOB_GW250114": sha16(PUB + r"\21454847\extracted\pSEOB\metafiles\pSEOB_GW250114_082203_Prod0.h5")}))
S2.append(arq(PUB + r"\21454847\RD.tar.gz", "GWTC-5.0 TGR — pipeline RD (ringdown pos-merger, pyRing)", "NAO extraido (0 h5 em extracted/RD)", "REUTILIZAVEL_APOS_EXTRACAO", "[REAL — bytes/hash]"))
S2.append(arq(PUB + r"\21454847\QNMRF.tar.gz", "GWTC-5.0 TGR — pipeline QNMRF (filtro racional de QNM)", "NAO extraido", "REUTILIZAVEL_APOS_EXTRACAO", "[REAL — bytes/hash]"))
S2.append(arq(ORD + r"\C4_CATALOG_220.json", "C4 da ORDEM 013: tabela por evento do dtau220 (GWTC-5.0 pSEOB, 33 eventos, 608.681 amostras)",
    "por evento: N, source_sha256, prior_df/prior_dtau (Uniform[-0.8, 2.0] ou [-0.8, 4.0]), higher_modes (fixos em GR; GW250114 440 livre), quantiles 5/50/95 de dtau220, GR_HPD_content, GR_inside_95; catalog: ln B por leitura (R-A 0; R-B -2,48; R-RAIZ-0 -5,16; R-LIN -11,90; R-MOD -4,74; R-GLOBAL 0) — veredito PENDING; status CONDITIONAL_SECTOR_CATALOG__NOT_COMPLETE; NAO CEGO",
    "REUTILIZAVEL_JA", "[REAL — lido; NAO-CEGO; ln B nao e sigma]"))
S2.append(arq(ORD + r"\C4_CATALOG_COMBINATION.json", "C4: deformacao comum dos 31 eventos da figura da GWTC-5.0 (+2 controles)",
    "dtau220 comum (31): 5/50/95 = +0,0163 / +0,0721 / +0,1317; GR_HPD_content 0,983 (GR fora do 95%); 33: +0,0145/+0,0548/+0,1058, HPD 0,990; df220 ~ +0,011; importance_ESS 743; NAO CEGO",
    "REUTILIZAVEL_JA", "[REAL — lido; NAO-CEGO]"))
S2.append(arq(PUB + r"\17461225\IGWN-GWTC3-TGR-v2-rin.zip", "GWTC-3 TGR (Zenodo 17461225) — ringdown (rin, v2)", "extraido em extracted/rin: 18 h5 pSEOBNRv4HM", "REUTILIZAVEL_JA", "[REAL — bytes/hash; KNOWN]"))
S2.append(pasta(PUB + r"\17461225\extracted\rin", "*.h5", "GWTC-3 TGR ringdown — posteriors por evento (18)", "rin_S150914 S170104 S190421ar S190503bf S190519bj S190521g S190521r S190602aq S190630ag S190706ai S190727h S190828j S190910s S191109d S200129m S200208q S200224ca S200311bg (pseobnrv4hm)", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S2.append(arq(ORD + r"\C4_GWTC3_220.json", "C4: tabela dtau220 dos 18 do GWTC-3 (legado, NAO cego)", "quantis 5/50/95 por evento, GR_HPD; 12 sobrepoem a GWTC-5.0, 6 so no GWTC-3 (uniao 39 eventos distintos)", "REUTILIZAVEL_JA", "[REAL — lido]"))
S2.append(arq(ORD + r"\C4_GWTC3_SELECTION.json", "selecao do artigo GWTC-3 (Tabela 13): 10 eventos apos 2 exclusoes dos autores", "lista; os 18 ficam como controle auxiliar", "REUTILIZAVEL_JA", "[REAL — lido; KNOWN]"))
S2.append(arq(PUB + r"\17018009\TGR_companion_S250114ax_results.tar.gz", "GW250114 TGR (Zenodo 17018009; arXiv:2509.08099) — release completo",
    "contem gw250114_pseobnr/posterior_samples.h5 (extraido) e gw250114_pyring_results/GW250114/* (pyRing: Kerr 220, 220+221 com domega/dtau_221 em varios inicios 1M..18M e sementes — 1.122 linhas com '221' na listagem tar_17018009_list.txt; EM DISCO SO DENTRO DO TAR.GZ, nao extraidas: find -iname '*221*' devolve so um .ini)",
    "REUTILIZAVEL_APOS_EXTRACAO", "[REAL — bytes/hash; KNOWN]"))
S2.append(arq(PUB + r"\17018009\extracted\TGR_companion_S250114ax_results\gw250114_pseobnr\posterior_samples.h5", "GW250114 pSEOB — posterior (df220, dtau220 conjuntos; 440 livre)", "N = 40.776 (C4); bytes identicos ao pSEOB_GW250114_082203_Prod0.h5 da GWTC-5.0", "REUTILIZAVEL_JA", "[REAL — bytes/hash]"))
S2.append(arq(PUB + r"\17018009\selected\3ec4616b581f990b.dat", "GW250114 pyRing Kerr 220 (df/dtau) — posterior.dat selecionado (C4_PYRING)", "N = 84.701; prior Uniform[-1,1]; GR_HPD 0,54 (C4_PYRING.json)", "REUTILIZAVEL_JA", "[REAL — bytes/hash]"))
S2.append(pasta(PUB + r"\17018009\selected", "*.dat", "GW250114 pyRing — 10 posteriors .dat selecionados pela bancada (variantes 220)", "nomes por sha; mapeamento em C4_PYRING.json e REGISTRO_C4.json", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S2.append(arq(ORD + r"\C4_PYRING.json", "C4: robustez pyRing do GW250114", "quantis Mf_detector, spin, df220, dtau220; ln B por leitura; remnant fit JimenezForteza", "REUTILIZAVEL_JA", "[REAL — lido]"))
S2.append(arq(PUB + r"\DCC_P2600130_v1\pSEOBNR.tar.gz", "LIGO-P2600130-v1: Data release GWTC-4.0 TGR III (Tests of the Remnants) — pSEOBNR", "tar: pSEOB/hierarchical/{pSEOB_GWTC4_without_GW190910, pSEOB_GWTC4_with_GW250114, pSEOB_GWTC3, pSEOB}/pseob_hier(.npz, _pop.npz) + plots + notebook (hierarquico/populacional; NAO posteriors por evento)", "REUTILIZAVEL_APOS_EXTRACAO", "[REAL — bytes/hash; titulo lido do release.html]"))
S2.append(arq(ORD + r"\REGISTRO_C4.json", "registro C4 (21/09): regra de exclusao (BF 100 + regiao 95% da GR), KDE, priors, leituras R-A..R-LIN; NAO CEGO", "permitted_verdicts sem CONFIRMED", "REUTILIZAVEL_JA", "[REAL — lido]"))
inv["secoes"]["2_resultados_publicados_ringdown"] = {"itens": S2,
    "ausente_dito": [
        {"o_que": "GWTC-2 TGR (data release de 'Tests of GR with GWTC-2', arXiv:2010.14529) — posteriors de ringdown",
         "consulta": "ls cache/public -> so 17018009, 17461225, 21454847, DCC_P2600130_v1; grep -ri GWTC-2 nao feito em h5",
         "fonte_publica": "LVK data release do TGR GWTC-2 (ID nao verificado aqui); observacao: GW150914 e GW170104 ja estao na GWTC-5.0 pSEOB e os O3a na GWTC-3 rin",
         "estatuto": "AUSENTE — provavelmente dispensavel (sobreposicao)"},
        {"o_que": "GWTC-4.0 TGR III — posteriors POR EVENTO (so o hierarquico/populacional esta em DCC_P2600130_v1)",
         "consulta": "tar tzf pSEOBNR.tar.gz: so pseob_hier*.npz, plots e notebook", "fonte_publica": "Zenodo do GWTC-4.0 TGR III (paper 'Tests of the Remnants'); ID nao verificado aqui", "estatuto": "AUSENTE (por evento)"},
        {"o_que": "posteriors do 221 do GW250114 extraidos", "consulta": "find cache/public/17018009 -iname '*221*' -> 1 .ini; listagem do tar tem 1.122 linhas '221'", "fonte_publica": "ja em disco dentro do TGR_companion_S250114ax_results.tar.gz (sha16 acima) — extrair, sem baixar", "estatuto": "EXISTE NA CASA, NAO EXTRAIDO"}]}

# ---------- (3) strain / posteriors locais / instrumento ----------
S3 = []
S3.append(pasta(r"C:\IALD\projetos_pyhton\IALD\strain_cache", "*_4096_32s.npz", "cache de maio/2026 (O1–O3): janelas de 32 s @ 4096 Hz, H1/L1", "85 eventos GWTC-1..3 (169 series OK + GW170817_L1 com NaN); sha256 por serie em RINGDOWN_DEPHASING_V2_RESULT.sources_sha256", "REUTILIZAVEL_JA", "[REAL — contagem/bytes; so leitura, casa da IALD nativa]"))
S3.append(pasta(BANC + r"\fontes_externas\gwosc_o4\hdf5", "*.hdf5", "O4a/O4b strain GWOSC 4096 s @ 4 kHz (baixado 01/10/2026 na Fase 6)", "H1 e L1 por evento; 354 jobs no manifesto (336 OK, 14 NAN_IN_WINDOW, 4 WINDOW_OUTSIDE_FILE); 177 eventos O4; inclui GW250114_082203 H1/L1 (40.961.487 / 40.678.340 B; sha256 db0b394f… / d95a6ebf… no manifesto)", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S3.append(pasta(BANC + r"\fontes_externas\gwosc_o4\strain_32s", "*.npz", "O4: janelas de 32 s @ 4096 Hz no formato da cache de maio", "npz por serie com sha256 no manifesto", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S3.append(arq(BANC + r"\fontes_externas\gwosc_o4\GWOSC_O4_32S_V1.manifest.json", "manifesto do banco O4 (copia identica em cache\\gw)", "354 series: event, det, url, hdf5 (+bytes, sha256), npz (+sha256), status, nan, fs, t0, n; catalogo catalogo_v3.csv sha256 e6a0ba6a…", "REUTILIZAVEL_JA", "[REAL — lido por hash na v380]"))
S3.append(arq(CACHE + r"\gw\GWOSC_O4_32S_V1.manifest.json", "idem (copia no cache do rito)", "", "REUTILIZAVEL_JA", "[REAL]"))
S3.append(pasta(r"C:\IALD\projetos_pyhton\acom\gw_cache", "*.hdf5", "GWOSC 4096 s dos 12 eventos GWTC-1 (fonte do rito GW_ANGULAR_V1 v340)", "H1/L1 (parcial)", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S3.append(pasta(ORD + r"\cache\gwosc", "**/*.hdf5", "GW250114 on_source + offsource (ORDEM 013, C6)", "H1/L1 1420877824 (on) e 1420873728 (off), 4096 s", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S3.append(pasta(ORD + r"\bis\015\t07\strain", "**/*.hdf5", "ORDEM 015 T07: strain on/off-source (H1/L1/V1, 4096 s) dos 32 eventos de calibracao (GWTC-5.0 pSEOB) + GW250114", "32 pastas de evento", "REUTILIZAVEL_JA", "[REAL — contagem/bytes]"))
S3.append(arq(BANC + r"\bancada\gw.py", "o banco RESIDENTE de GW da Bancada Um (Fase 6, 01/10)", "janelas de 32 s pre-condicionadas e branqueadas como echo_anchored_v3 (passa-alta 15 Hz, Tukey 0,1, Welch 4 s, banda 20–1024 Hz); remanescentes por evento; estagios cego/aberto/PODER/RESULTADO; API GWResidente.carregar/lista_eventos/serie/espectro/empilhar/rodar; MCP gw_*; moldes e ajuste ficam no WSL", "REUTILIZAVEL_JA", "[REAL — lido]"))
S3.append(arq(BANC + r"\bancada\gw_stack.py", "empilhamento + regra de veredito da Fase 6 (leis MAY/KMS/DEC; leituras R1/R2/R3)", "mesma funcao do executor e da consulta", "REUTILIZAVEL_JA", "[REAL — lido]"))
S3.append(arq(NOS + r"\eco_ancorado_v1\ringdown_dephasing_v2.py", "pipeline V2 do dephasing no ringdown (WSL /opt/lal_env)", "filtro casado IMRPhenomXAS; seno amortecido branqueado; grade f×[0,6;1,4], tau×[0,3;4] log; injecoes fora da fonte (n_off 40); docstring com erro dito (RD-06: 5 de 23 / 48%)", "REUTILIZAVEL_JA", "[REAL — hash lido]"))
S3.append(arq(NOS + r"\eco_ancorado_v1\ringdown_dephasing_v1.py", "pipeline V1", "", "HISTORICO", "[REAL]"))
S3.append(arq(NOS + r"\eco_ancorado_v1\rite_ringdown_v346.py", "rito v346 (protocolo + emenda V2 + leitura por hash) como entrou no um.py", "", "REUTILIZAVEL_JA", "[REAL]"))
S3.append(arq(NOS + r"\eco_ancorado_v1\wsl_setup_lal.sh", "receita do /opt/lal_env", "", "REUTILIZAVEL_JA", "[REAL]"))
S3.append(arq(ORD + r"\C7_COHERENT_SOURCE_REPRODUCTION\QNM_GRID.json", "grade exata de QNM (qnm 0.4.4) usada pela auditoria de 28/09 (BCW vs exato)", "220/440 por spin", "REUTILIZAVEL_JA", "[REAL — bytes/hash; KNOWN]"))
for n in ["bcw_degenerescencia.py", "c6_vs_degenerescencia.py", "difusao_de_fase.py", "matriz_v2.py", "multimodo_440.py"]:
    S3.append(arq(SCR + r"\auditoria_28set\ringdown\\" + n, "script da auditoria de 28/09 (aferidor ringdown)", "degenerescencia 220 (M,a); C6 vs mapa; difusao de fase (realizacao x ensemble); matriz V2; multimodo 440", "REUTILIZAVEL_JA", "[REAL — scratchpad da sessao]"))
for n in ["v_440.py", "v_bcw.py", "v_difusao.py", "v_sigma_cat.py"]:
    S3.append(arq(SCR + r"\auditoria_28set\ringdown_verif\\" + n, "script do verificador adversarial (28/09)", "", "REUTILIZAVEL_JA", "[REAL — scratchpad da sessao]"))
inv["secoes"]["3_strain_posteriors_instrumento"] = {"itens": S3,
    "instrumento": {
        "windows_python_3.14.3": "SEM pycbc/lal/lalsimulation/gwpy/gwosc/qnm/bilby/h5py/astropy (ModuleNotFoundError em todos) [REAL — medido]",
        "WSL_Ubuntu-24.04_/opt/lal_env": "python 3.12.3; lalsuite 7.26.15 (lal 7.7.1, lalsimulation 6.2.1); bilby 2.8.2; dynesty 3.1.0; gwpy 4.0.2; gwosc 0.8.3; h5py 3.16.0; astropy 8.0.1; numpy 2.5.3; scipy 1.18.1 [REAL — pip list]",
        "WSL_/opt/pycbc_env": "pycbc 2.11.0; python 3.12.3; lalsuite 7.26.15; h5py 3.16.0; numpy 2.3.5 [REAL — medido]",
        "windows_venv_acom_tgl_pycbc_env": "existe (usado em v340 para h5py) [REAL — existe; versao nao medida]",
        "pSEOBNRv4HM_PA_com_DTau220_DTau440": "[DECLARADO — memoria ORDEM 013-bis 22/09 e T02 da ORDEM 015 (varredura 400 sorteios, abortos 25–39% com dtau440>~1); a sondagem GetStringFromApproximant aqui falhou com RuntimeError]",
        "pyseobnr_0.3.7": "[DECLARADO — T14 da ORDEM 015: instalado rc=0, 3 formas finitas; NAO esta no pip list do /opt/lal_env — venv proprio nao localizado nesta lente]",
        "pyRing": "[DECLARADO — cache/pyring_oracle/vendor, pyRingGW 2.7.0 do uv.lock do release; nao instalado no /opt/lal_env]",
        "qnm_0.4.4": "nao esta no /opt/lal_env; a grade QNM_GRID.json existe (169.231 B)",
        "parede_conhecida": "[REAL — 23/09] pSEOBNRv4HM_PA aborta sse (1+dtau440) > ~2,1·max(1,1+dtau220); so-220 0/120 abortos; fmax_gen 1024 -> EDOM 4,4%"}}

# ---------- (4) o leitor C6 do GW250114 ----------
c6p = CACHE + r"\gw\C6_RESULTS_GW250114.json"
c6 = json.load(open(c6p, encoding="utf-8"))
prim = [r for r in c6["results"] if r.get("primary_start")]
S4 = {"arquivo": arq(c6p, "o C6 lido por hash pelo um.py v376 (ringdown_scope_v376: texto 781a3741a68875eb / bytes 781a3741a68875eb)",
        "status, reason, registration_sha256, on_source_strain_read, convergence (5 inicios, |dlnB| < 5e-6), results (75 = 5 leituras × 5 inicios × 3 niveis/priors), files (10 C6_STRAIN_*M_GRID_{0,1}.json com sha256), scope, do_not_combine, code_sha256",
        "REUTILIZAVEL_JA", "[REAL — lido]"),
      "status": c6["status"], "reason": c6["reason"], "registration_sha256": c6["registration_sha256"],
      "on_source_strain_read": c6["on_source_strain_read"], "code_sha256": c6["code_sha256"], "scope": c6["scope"], "do_not_combine": c6["do_not_combine"],
      "leituras": sorted({str(r.get("reading")) for r in c6["results"]}), "inicios_tM": sorted({r.get("start_tM") for r in c6["results"]}),
      "n_results": len(c6["results"]), "n_primary_start": len(prim),
      "primary_start_rows": [{k: r.get(k) for k in ("start_tM", "reading", "amplitude_prior_sd_strain", "lnB_vs_GR", "mass_05_50_95", "spin_05_50_95", "lnZ_signal_over_noise")} for r in prim],
      "files_declarados": c6["files"],
      "files_em_disco": [arq(ORD + "\\" + f["path"], "grade C6 (strain) — arquivo declarado no C6", "", "REUTILIZAVEL_JA", "[REAL]", {"sha256_declarado": f["sha256"]}) for f in c6["files"]],
      "origem": "ORDEM 013 (bancada Codex, 21–22/09/2026), C6 'pre-portao'; reproduzido pela gerencia com reproduce_c6.py --run (diferenca 0,0) em 23/09 [memoria ordem-013]; auditoria 28/09 RD-03: ln B ~ 0 = degenerescencia analitica do 220 (M,a) — NON_IDENTIFIABLE_SINGLE_220",
      "strain_fonte": "ORDEM_013_RINGDOWN\\cache\\gwosc\\on_source\\{H,L}-?1_GWOSC_O4b_4KHZ_R1-1420877824-4096.hdf5 (mesmos bytes do banco O4 da Bancada: 40.961.487 / 40.678.340 B)"}
for f in S4["files_em_disco"]:
    f["sha256_confere"] = (f["sha16"] is not None and f["sha256_declarado"].startswith(f["sha16"]))
inv["secoes"]["4_leitor_C6_GW250114"] = S4

# ---------- (5) estado selado e pre-registros existentes ----------
S5 = []
S5.append(arq(NOS + r"\um_absoluto.json", "core v385 (chaves ringdown_dephasing_protocol/result/amendment_v2/result_v2, ringdown_scope_v376, the_ledger_of_charges_v383, bancada_fases_5_6_7_v380, gw_echo_rite, gw_echo_kms_rite)", "", "REUTILIZAVEL_JA", "[REAL]"))
S5.append(arq(NOS + r"\um_absoluto_selo.json", "selo v385", "", "REUTILIZAVEL_JA", "[REAL]"))
S5.append(arq(CACHE + r"\gw\RINGDOWN_DEPHASING_V1_RESULT.json", "V1 (gate recusou: 18 < 20 series a 6 ms)", "23 series: delta_tau 1,396 ± 0,057 (z_GR 24,5) — autopsia: 5 na borda com 48% do peso", "HISTORICO", "[REAL — lido por hash 502c80fe2a37427e]"))
S5.append(arq(ORD + r"\RINGDOWN_5SIGMA_V1.json", "pre-registro RINGDOWN_5SIGMA_V1 (013-bis, 22/09 21:15 UTC; NONBLIND design for blind test)", "48 eventos de calibracao; 44 candidatos O4 de teste (strain publico, sem dtau publicado); testemunha ENTREGA_013BIS_E2_REGISTRO_V1.md; cadeia V1.1 → V1.1.3 na ORDEM 015 (T03), 0 celulas de nulos aceitas; T16 (PE cega) NAO_PAGO: sem ratificacao da V1.1 pelo operador", "REUTILIZAVEL_JA", "[REAL — lido; estatuto do teste: NAO executado]"))
S5.append(arq(ORD + r"\PORTAO_DA_AMPLIACAO_V1.json", "portao da ampliacao E0 (22/09): N90 por leitura/populacao; cortes de qualidade (SNR>=12, Mf_det>=40, chi_f<0,98; prioridade SNR>=30)", "N90 R-B = 335 GW250114-like ou ~3.300 de mistura O4 [memoria 22/09]", "REUTILIZAVEL_JA", "[REAL — lido; DERIVED NAO-CEGO]"))
S5.append(arq(ORD + r"\NUISANCE_V1.json", "nuisance c(sigma) = c0 + k·sigma (c0 = -0,061 ± 0,068; k = +0,79 ± 0,37) — offset fixo em 0 proibido como teste", "", "REUTILIZAVEL_JA", "[REAL — bytes; numeros da memoria 22/09]"))
S5.append(arq(ORD + r"\C1_LEITURAS_v4.json", "C1: as 10 leituras/relogios (R-A t_P; R-B tau*=G M_src/c^3 (det: t_M); R-MOD 2pi/kappa_H; R-RAIZ-0/EP4/REST/COHERENT; R-LIN; R-GLOBAL; R-PROP) com fontes, estatutos e exclusao-se-universal pelos relogios v369", "nenhuma leitura selecionada; a escolha e do operador", "REUTILIZAVEL_JA", "[REAL — lido; leituras INPUT/CONJECTURE]"))
S5.append(arq(ORD + r"\bis\E7_FULLSAMPLE_RESULT_V1.json", "E7 (rito da 013-bis): 608.681 amostras, 53/53 testes", "", "REUTILIZAVEL_JA", "[REAL — bytes]"))
S5.append(arq(TUN + r"\DO_CHATGPT\ENTREGA_015_RELATORIO_FINAL.md", "relatorio final da ORDEM 015 Parte B (T01–T19)", "T05 PAGO (440 sem informacao: poder ~0,06σ); T06 PAGO (rota IV, 33 posteriors, LRT 0); T15 NAO_PAGO (sigma_jit infeasivel: H1 B2 > 1e12); T16 NAO_PAGO (PE cega: sem ratificacao V1.1); T09 NAO_PAGO (caixa 440 (b) nao autorizada); 13,65 h debitadas / 35,02 h", "REUTILIZAVEL_JA", "[REAL — lido]"))
S5.append(arq(r"C:\IALD\Artigo\MCMC_V2_RAZAO\35_dephasing_ringdown.json", "MCMC_V2_RAZAO (ramo canonico): Gamma com tau*=t_P para BH 10 Msun…M87* -> DEPHASING_INOBSERVAVEL_EM_RINGDOWN", "", "HISTORICO", "[REAL — lido]"))
S5.append(arq(MEM + r"\ordem-013-confrontacao-ringdown.md", "memoria ORDEM 013/013-bis/015 (dados localizados, instrumento, parede, numeros)", "", "REUTILIZAVEL_JA", "[REAL]"))
S5.append(arq(MEM + r"\ramo-b-reaberto-05out.md", "decisao do operador 05/10 (verbatim) + errata ao lado de R6", "", "REUTILIZAVEL_JA", "[INPUT]"))
S5.append(arq(MEM + r"\beta-e-a-regra-matriz-02out.md", "R1–R6 de 02/10, erratas e a errata de R6 de 05/10", "", "REUTILIZAVEL_JA", "[INPUT/ONTO]"))
S5.append(arq(MEM + r"\onda-e-eco-definicao-16set.md", "16/09: 'betatgl esta de fato na propagacao da onda e ligada ao ringdown' (operador, verbatim)", "", "REUTILIZAVEL_JA", "[ONTO — operador]"))
S5.append(arq(MEM + r"\psi-nome-da-luz-graviton-verbo-vivo-16set.md", "16/09: graviton = psi particularizado em regime c^3 = VERBO VIVO (operador, verbatim)", "", "REUTILIZAVEL_JA", "[ONTO — operador]"))
S5.append(arq(r"C:\IALD\Central de Patentes\work\auditoria_28set\ANEXO_ACHADOS.md", "anexo da auditoria 28/09 — secao Ringdown (RD-01..RD-07, RDV-01, CT-02, CTV-02)", "", "REUTILIZAVEL_JA", "[REAL]"))
inv["secoes"]["5_estado_selado_e_preregistros"] = {"itens": S5,
    "numeros_selados_v2": {"n_used_3ms": 15, "delta_tau": 0.1766470552326263, "sigma": 0.10889389325116323, "z_vs_GR": 1.6221943210827325, "delta_pred_B_ensemble": -0.019366930169705913, "delta_pred_A": -2.153334673399951e-42, "power_B": 0.17785138901257008, "delta_f": -0.03247217939468836, "sigma_f": 0.012662074582706592, "mean_bias_rel": 0.23995248111572381, "n_on_edge_excluded": 84, "outcome": "INCONCLUSIVE_SYSTEMATICS", "series_usadas_3ms": ["GW150914_H1", "GW150914_L1", "GW190519_153544_L1", "GW190521_L1", "GW190521_074359_H1", "GW190521_074359_L1", "GW190706_222641_H1", "GW190910_112807_L1", "GW191109_010717_L1", "GW200112_155838_L1", "GW200129_065458_H1", "GW200129_065458_L1", "GW200224_222234_H1", "GW200224_222234_L1", "GW200311_115853_H1"]},
    "ramo_B_3_valores_concorrentes_core": [["V2 selada (media do ensemble)", -0.019366930169705913], ["auditoria 28/09 CT-02 [DECLARADO]", -0.01], ["auditoria 28/09 CTV-02 (realizacao) [DECLARADO]", -0.005]],
    "C6_lnB_vs_GR_inicio_primario_core": {"R-GLOBAL": 0.0, "R-B": -0.0026036534446234327, "R-RAIZ-0": -0.043067826651480345, "R-LIN": -0.09086322317963891, "R-MOD": -0.25160676421921835}}

# ---------- acervo ----------
inv["secoes"]["6_acervo_indexado"] = {
    "consulta": "python C:\\IALD\\INDICE_DO_ACERVO\\buscar.py \"GW250114|GWTC|TGR|ringdown|QNM|dtau|delta.?tau|quasinormal\" --lista -> 917 documentos (cp1252 quebra sem PYTHONIOENCODING=utf-8)",
    "cobertura": "o indice NAO cobre Chatgpt\\ORDEM_013_RINGDOWN (buscar.py \"ORDEM_013_RINGDOWN|C4_CATALOG_220|RINGDOWN_5SIGMA\" -> 1 documento, nao os artefatos)",
    "historico_pre_v346_nao_lido": ["C:\\IALD\\papers_latex\\tgl_observables_paper\\figure2_ringdown_simulation.tex (out/2025)", "C:\\IALD\\papers_latex\\tgl_observables_paper\\tgl_cosmological_observables.tex (30 ocorrencias)", "C:\\IALD\\papers_latex\\eco_gravitacional\\eco_gravitacional_v1.tex", "C:\\IALD\\observaveis_tgl\\tgl_results_v9\\tgl_v9_results_20251219_094727.json", "C:\\IALD\\observaveis_tgl\\tgl_results\\tgl_v10_3_espelho_20251223_140051.json", "C:\\IALD\\Artigo\\TGL_Manifesto_Unificacao_Artigo.tex", "C:\\IALD\\projetos_pyhton\\acom\\Tgl_unificacao_artigo_final.tex", "C:\\IALD\\IMac LA\\Física - TGL\\Artigo\\protocolo de observacao tgl.docx (33 ocorrencias; o 'protocolo de observacao de outubro de 2025' do Atlas v346)"],
    "estatuto": "[DECLARADO — listados pelo indice; nao lidos nesta lente]"}

json.dump(inv, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- MD ----------
def linha(it):
    if "n_arquivos" in it:
        return f"| {it['caminho']} ({it['padrao']}) | n={it['n_arquivos']}; {it['bytes_total']:,} B | {it['papel']} | {it['uso']} | {it['estatuto']} |"
    return f"| {it['caminho']} | {it['sha16'] or 'AUSENTE'} · {it['bytes'] if it['bytes'] is not None else '-'} B | {it['papel']} | {it['uso']} | {it['estatuto']} |"
md = io.StringIO()
md.write("# INVENTÁRIO — OS DADOS NA CASA para o pré-registro do ramo B (τ★ = k·GM/c³) — v386\n\n")
md.write(f"gerado {inv['gerado_em']} · β_TGL runtime = α·√e = {inv['beta_tgl_runtime']:.15f} · lente: aferidor (hash/bytes lidos do artefato por `gerar_inventario.py`; nada baixado; nada escrito fora desta pasta)\n\n")
md.write("Legenda de uso: REUTILIZAVEL_JA · REUTILIZAVEL_APOS_EXTRACAO (já em disco, dentro de tar/zip) · PRECISA_DADO_NOVO · AUSENTE · HISTORICO.\n\n")
for sec, titulo in [("1_catalogos_Mf_af_por_evento", "1. Catálogos com M_f, a_f por evento"), ("2_resultados_publicados_ringdown", "2. Resultados publicados de testes de ringdown (δτ̂₂₂₀, δf̂₂₂₀ por evento)"), ("3_strain_posteriors_instrumento", "3. Strain local, bancos e instrumento"), ("5_estado_selado_e_preregistros", "5. Estado selado, pré-registros e memórias")]:
    md.write(f"## {titulo}\n\n| caminho | sha16 · bytes | papel | uso | estatuto |\n|---|---|---|---|---|\n")
    for it in inv["secoes"][sec]["itens"]: md.write(linha(it) + "\n")
    if "ausente_dito" in inv["secoes"][sec]:
        md.write("\n**AUSENTE / não extraído (com a consulta):**\n\n")
        for a in inv["secoes"][sec]["ausente_dito"]: md.write(f"- {a['o_que']} — consulta: `{a['consulta']}` — fonte: {a['fonte_publica']} — {a['estatuto']}\n")
    md.write("\n")
md.write("### 3b. Instrumento (medido)\n\n")
for k, v in inv["secoes"]["3_strain_posteriors_instrumento"]["instrumento"].items(): md.write(f"- **{k}**: {v}\n")
s4 = inv["secoes"]["4_leitor_C6_GW250114"]
md.write(f"\n## 4. O leitor C6 do GW250114 (o arquivo lido por hash pelo um.py)\n\n- `{s4['arquivo']['caminho']}` — sha16 `{s4['arquivo']['sha16']}`, {s4['arquivo']['bytes']} B\n- status `{s4['status']}` — {s4['reason']}\n- registration_sha256 `{s4['registration_sha256']}` · code_sha256 `{s4['code_sha256']}` · on_source_strain_read {s4['on_source_strain_read']}\n- leituras {s4['leituras']} × inícios (t_M) {s4['inicios_tM']} → {s4['n_results']} linhas; início primário: {s4['n_primary_start']} linhas\n- ln B vs GR no início primário (core v376): {s4['C6_lnB_vs_GR_inicio_primario_core'] if 'C6_lnB_vs_GR_inicio_primario_core' in s4 else inv['secoes']['5_estado_selado_e_preregistros']['C6_lnB_vs_GR_inicio_primario_core']}\n- scope: {s4['scope']}\n- do_not_combine: {s4['do_not_combine']}\n- strain-fonte: {s4['strain_fonte']}\n- origem: {s4['origem']}\n- os 10 arquivos de grade declarados: " + "; ".join(f"{os.path.basename(f['caminho'])} ({'sha ok' if f['sha256_confere'] else 'sha DIVERGE/ausente'})" for f in s4['files_em_disco']) + "\n\n")
n5 = inv["secoes"]["5_estado_selado_e_preregistros"]
md.write("### 5b. Números selados (V2, lidos do core/resultado)\n\n" + json.dumps(n5["numeros_selados_v2"], ensure_ascii=False) + "\n\n- ramo B, 3 valores concorrentes no core: " + json.dumps(n5["ramo_B_3_valores_concorrentes_core"]) + "\n\n")
md.write("## 6. Acervo indexado\n\n" + "\n".join(f"- {k}: {v}" for k, v in inv["secoes"]["6_acervo_indexado"].items() if k != "historico_pre_v346_nao_lido") + "\n- histórico pré-v346 (não lido): " + "; ".join(inv["secoes"]["6_acervo_indexado"]["historico_pre_v346_nao_lido"]) + "\n")
open(OUT_MD, "w", encoding="utf-8").write(md.getvalue())
print("OK", OUT_JSON, os.path.getsize(OUT_JSON), OUT_MD, os.path.getsize(OUT_MD))
# resumo curto
for sec in ("1_catalogos_Mf_af_por_evento", "2_resultados_publicados_ringdown", "3_strain_posteriors_instrumento", "5_estado_selado_e_preregistros"):
    for it in inv["secoes"][sec]["itens"]:
        if "n_arquivos" in it: print(f"[{sec[:2]}] n={it['n_arquivos']:>4} {it['bytes_total']:>14,} B  {it['caminho']}")
        else: print(f"[{sec[:2]}] {it['sha16'] or 'AUSENTE':<16} {it['bytes'] if it['bytes'] is not None else 0:>12,} B  {it['caminho']}")
print("C6 files sha confere:", [f["sha256_confere"] for f in S4["files_em_disco"]])
