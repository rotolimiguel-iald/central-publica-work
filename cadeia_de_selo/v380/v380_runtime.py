# ====================== v380: AS FASES 5, 6 (ECO V3 + EMENDAS V4 E V5) E 7 DA BANCADA UM, O BANCO DE GW E AS ERRATAS AO LADO -- LIDAS POR HASH ======================
# Ordens do operador (01/10/2026, verbatim em _V380_OPERATOR_VERBATIM): o SH0ES na Bancada; «o teste da transformada radical com as ondas gravitacionais e
# ecos»; «todo esse banco de dados novo (gweco) ... ja o vincule a bancada para vc poder trabalhar com eles em tempo real»; «estude tudo que eu ja fiz e ja
# escrevemos e resolva os problemas que faltam». O que entra, SEM kernel novo e SEM mover o gate: (5) a Fase 5 (Pantheon+SH0ES com 77 calibradores Cefeida,
# cov 1701x1701, M profilado; as tres leituras da lei nas distancias); (6) a Fase 6 -- ECO V3 «a transformada radical»: a raiz como AMPLITUDE pre-registrada da
# resposta da fronteira (tres leituras: sqrt(beta) peso 1; sin 2theta_M = 2 sqrt(beta(1-beta)) o graviton le a 2theta [CONJECTURE]; beta o quadrado), duas leis de
# atraso [INPUT/ONTO] (MAY: 2GM_f/c^3 ln(1/beta); KMS: 2pi/kappa(M_f, a_f) por evento), 244 BBH O1-O4 (67 do cache de maio + 177 de O4 baixados do GWOSC),
# estimador ancorado corrigido pela auditoria de 28/09 (GWECO-01/06/07/08/09/V-N1, CT-03), poder gravado ANTES de abrir, subamostra CEGA de O4 (173 dos 240,
# nao uma replica independente); a EMENDA V4 (grade +-2 sigma, NAO cega, pre-registrada depois da autopsia) e o diagnostico post hoc dos controles; a EMENDA V5
# (CEGA so quanto a lei nova: a lei de atraso de 24/12/2025 do acervo, 2GM_f/(beta c^3), [DECLARADO -- derivacao por IA sob direcao do operador, nao derivada do
# axioma]); (7) a Fase 7 -- os 32 cronometros com a covariancia completa de Moresco+2020 (IMF + SPS correlacionados nos 15 pontos de Moresco com os valores da
# fonte; 17 outros diagonais; variante conservadora em todos); o BANCO residente de GW (manifesto do O4: 354 series sobre 352 arquivos de 4096 s do GWOSC,
# sha256; 14 series NaN na janela e 4 janelas fora do arquivo, ditas); e as ERRATAS AO LADO: SEIS da auditoria de 28/09 (CT-03/GWECO-04, GWECO-05, GWECO-03,
# RD-06, VV-N1, RNC-06) + UMA errata da v378 (a linha diagonal) + UMA nota (o banco). O que NAO e: uma falsificacao do PAR (leitura, lei) nao falsifica a teoria;
# NOT_FALSIFIED nunca e CONFIRMADA; a RG e o limite classico; o «100 sigma» de dezembro segue retirado (v340). Hash de BYTES e de TEXTO normalizado a LF lado a
# lado (EV-08): onde diferem (CRLF), a diferenca e dita no veredito, nao escondida. Dois desvios do pipeline da Bancada ditos aqui, nao corrigidos por cima: a
# bandeira DELAY_CONTROL_RESPONDS da V3 (MAY, tau/2, |z| >= 5) nao foi gravada; a clausula V5 (poder de R3 < 5 sigma -> NOT_FALSIFIED_UNDERPOWERED) nao foi
# aplicada -- o par (beta, DEC) saiu INCONCLUSIVE_SYSTEMATICS pela regra geral 2.

_V380_OPERATOR_VERBATIM = {
    "sh0es_20261001": "Agora vamos melhorar nossa bancada inserindo shoes nela. Por favor e quero que vc a manipule para realizar os testes que são mais promissores,",
    "radical_20261001": ("Ainda vamos investigar mais a bancada, eu quero realizar o teste da transformada radical com as ondas gravitacionais e ecos, eu fiz um teste anterior "
                         "que deu 100 sigma, quando aplicamos a fórmula da gravidade radicalizada, acontece que naquela ocasião o teste acabou ficando tautológico porque não "
                         "tínhamos derivado tudo, como o que fizemos agora, então parecia tautologia, embora misturamos os sinais e demonstramos que a transformada não "
                         "funcionava, portanto, só funcionava com as ondas gravitacionais, eu penso que esse é o melhor teste"),
    "bank_20261001": ("ótimo e todo esse banco de dados novo (gweco) que vc está baixando já o vincule à bancada para vc poder trabalhar com eles em tempo real dentro do "
                      "sistema carregado com os dados reais"),
    "solve_20261001": "estude tudo que eu já fiz e já escrevemos e resolva os provlemas que faltam",
}
_V380_FILES = {
    "f5_pre": ("bancada_01out", "PREREGISTRO_FASE5_SH0ES_20261001.json"), "f5_res": ("bancada_01out", "RESULTADO_FASE5_SH0ES_20261001.json"),
    "f6_pre": ("bancada_01out", "PREREGISTRO_FASE6_ECO_RADICAL_20261001.json"), "f6_poder": ("bancada_01out", "PODER_FASE6_ANTES_DE_ABRIR.json"),
    "f6_res": ("gw", "ECHO_ANCHORED_V3_RESULT.json"), "f6_diag": ("bancada_01out", "DIAG_CONTROLES_POSTHOC.json"), "f6_amostra": ("bancada_01out", "AMOSTRA_FASE6.json"),
    "f6_rem": ("bancada_01out", "remanescentes_v3.json"), "v4_emenda": ("bancada_01out", "EMENDA_V4_FASE6_20261001.json"), "v4_poder": ("bancada_01out", "PODER_V4_ANTES_DE_ABRIR.json"),
    "v4_res": ("bancada_01out", "RESULTADO_V4_FASE6_20261001.json"),
    "f7_pre": ("bancada_01out", "PREREGISTRO_FASE7_CC_COVARIANCIA_20261001.json"), "f7_res": ("bancada_01out", "RESULTADO_FASE7_CC_COVARIANCIA_20261001.json"),
    "cc_cov": ("bancada_01out", "moresco_2020_cov.json"), "gw_bank": ("gw", "GWOSC_O4_32S_V1.manifest.json"),
    "v5_emenda": ("bancada_01out", "EMENDA_V5_FASE6_20261001.json"), "v5_poder": ("bancada_01out", "PODER_V5_ANTES_DE_ABRIR.json"), "v5_res": ("bancada_01out", "RESULTADO_V5_FASE6_20261001.json"),
}
_V380_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
_V380_ERRATAS_AUDITORIA = ("gw_echo_rites_v341_v348__AMPLITUDE_SQRT_BETA_FROM_KERNEL", "gw_echo_kms_law__period_in_imaginary_time", "echo_pe_v2__GW190412_border",
                           "ringdown_dephasing_v2__docstring", "neutrino_m2_v2__nufit_contains_juno", "neutrino_m2_v2__kill_line")
_V380_ERRATAS_BESIDE = {
    "gw_echo_rites_v341_v348__AMPLITUDE_SQRT_BETA_FROM_KERNEL": ("[CT-03/GWECO-04, auditoria 28/09] o kernel prova |R| = sin theta da matriz-S abstrata (SMatrix) e theta = theta_M no runtime; a "
                                                                "identificacao de |R| com A_eco/A_primario de um remanescente de Kerr e [ONTO]; o peso 1 (a luz) e [INPUT]; a Fase 6 pre-registrou "
                                                                "tres leituras (sqrt(beta), sin 2theta_M, beta). O rotulo le-se S_MATRIX_REFLECTION_IDENTIFIED_ONTO_AT_WEIGHT_1; os vereditos antigos ficam"),
    "gw_echo_kms_law__period_in_imaginary_time": ("[GWECO-05, auditoria 28/09] 2pi/kappa e a largura da faixa KMS em tempo IMAGINARIO (kmsStrip; unruh_is_kms: beta.kappa = 2pi); usa-la como atraso real e [ONTO]. "
                                                  "A Fase 6 falsificou o PAR (sqrt(beta) ou sin 2theta, 2pi/kappa): o que cai e essa leitura do atraso, nao a periodicidade KMS do kernel"),
    "echo_pe_v2__GW190412_border": "[GWECO-03, auditoria 28/09] na PE V2 o GW190412 ficou na borda do prior com 98,7% do peso IVW; os vereditos da PE V2 (INCONCLUSIVE_SYSTEMATICS) ficam, lidos com esta errata",
    "ringdown_dephasing_v2__docstring": "[RD-06, auditoria 28/09] a docstring do pipeline V2 diz '6 series, ~52% do peso'; a autopsia medida diz 5 de 23 (48,1%): vale o numero medido; o pipeline fica intocado",
    "neutrino_m2_v2__nufit_contains_juno": ("[VV-N1, auditoria 28/09] a entrada 'NuFIT global pos-JUNO (2025-12)' esta marcada 'independente: True' no frozen; ela CONTEM o JUNO e nao e autonoma -- as "
                                            "determinacoes autonomas da kill_rule sao o JUNO (59 d; [DECLARADO: 7,50 +- 0,12 x 1e-5 eV^2, arXiv:2511.14593, numero lido na fonte em 01/10, nao por hash]) e o "
                                            "KamLAND+solar. E a tensao de 2,95 sigma depende de qual ajuste global pos-JUNO se usa: NuFIT 6.1 (arXiv:2601.09791, eq. 11) da 2,95 sigma; o ajuste de "
                                            "Capozzi et al. (arXiv:2511.21650) da 2,44 sigma -- a escolha vale ~0,5 sigma e fica dita, nao herdada em silencio"),
    "neutrino_m2_v2__kill_line": "[RNC-06, auditoria 28/09] 'linha de morte dentro da meta do JUNO' exagera: a kill_rule exige DUAS determinacoes autonomas >= 5 sigma; a segunda nao esta nomeada",
    "bancada_fase4_v378__cc_diagonal": ("[errata da v378, nao da auditoria] a frase 'a covariancia sistematica de Moresco+ 2020 nao entrou' (prove_bancada_fase4_v378, verbatim) ganha a Fase 7: "
                                        "medida com a covariancia completa (abaixo)"),
    "bancada_gw_bank": ("[nota, nao errata] o banco residente de GW (244 BBH, 484 series pre-registradas, 14 delas NaN na janela -- um detector por evento) vive na Bancada Um (/api/gw, "
                        "ferramentas MCP gw_*; recarga sem reiniciar); os moldes (lalsimulation) e o ajuste rodam no WSL e entram por arquivo -- o um.py le o resultado por hash, nunca recalcula"),
}


def _v380_has_str(obj, s):
    """True se a string s ocorre em qualquer chave ou valor (recursivo) de obj -- sem serializar."""
    if isinstance(obj, dict):
        return any(_v380_has_str(k, s) or _v380_has_str(v, s) for k, v in obj.items())
    if isinstance(obj, (list, tuple)):
        return any(_v380_has_str(x, s) for x in obj)
    return s in str(obj)


def prove_bancada_fases_5_6_7_v380(ONE, core):
    """v380 -- AS FASES 5, 6 E 7 DA BANCADA UM, O BANCO DE GW E AS ERRATAS AO LADO, LIDOS POR HASH [ADITIVO; nao move o gate; sem kernel novo].
    Le do cache do rito (bancada_01out e gw) os pre-registros, os poderes gravados antes de abrir (V3, V4 e V5), os resultados, as emendas, o diagnostico, a
    covariancia e o manifesto do banco (18 artefatos); confere beta (alpha.sqrt(e) do core, nunca literal), os hashes que cada RESULTADO declara do seu
    pre-registro e do seu poder, a ausencia de palavra proibida em todo veredito (a MESMA guarda do rito), e os fatos que o veredito desta leitura carrega:
    (5) SH0ES na Bancada (H0 da escada por SNe+calibradores contra um alvo [DECLARADO]; delta da escada na leitura «sombra»); (6) o par (sqrt(beta) ou
    sin 2theta_M, 2pi/kappa) FALSIFIED_AT_DELAY_LAW em 240 BBH e na subamostra CEGA de O4 (173 dos 240), com poder >= 5 sigma e sistematica relativa <= 0,3
    gravados ANTES de abrir; a lei MAY INCONCLUSIVE_SYSTEMATICS -- e o controle tau/2 de MAY acima da bandeira pre-registrada sem a bandeira gravada pelo
    pipeline (dito); a emenda V4 NAO cega (sin 2theta x MAY falsificado com os controles abaixo da bandeira por pouco -- dito; sqrt(beta) x MAY inconclusivo e
    o limite deste estimador); a emenda V5 cega so quanto a lei DEC (24/12/2025, [DECLARADO]): o par (sqrt(beta) ou sin 2theta, DEC) falsificado; o par do
    proprio documento (beta, DEC) INCONCLUSIVE_SYSTEMATICS pela regra geral, com poder < 5 sigma -- a clausula V5 (UNDERPOWERED) nao aplicada pelo pipeline,
    dito; (7) os cronometros com a covariancia completa (o z do ganho da lei acumulada e o ln B sombra/acumulada sob Moresco+2020 contra a diagonal). Seis
    erratas da auditoria + uma da v378 + uma nota ficam registradas no proprio core. Falsificar o PAR nao falsifica a teoria; NOT_FALSIFIED nao e CONFIRMADA;
    a RG e o limite classico; o «100 sigma» de dezembro segue retirado (v340)."""
    beta = float(core.get("beta") or 0.0)
    lidos, hashes = {}, {}
    for k, (sub, fn) in _V380_FILES.items():
        p = os.path.join(CACHE, sub, fn)
        obj, ht, hb = _read_external_json_with_hashes(p)
        try:
            with open(p, "rb") as fh:
                raw = fh.read()
            full = hashlib.sha256(raw).hexdigest()
            n_crlf = raw.count(b"\r\n")
            ht_lf = hashlib.sha256(raw.decode("utf-8").replace("\r\n", "\n").encode("utf-8")).hexdigest()[:16]
        except Exception:
            full, n_crlf, ht_lf = None, None, None
        lidos[k] = obj; hashes[k] = {"file": fn, "dir": sub, "sha16_text": ht, "sha16_bytes": hb, "sha16_text_lf": ht_lf, "crlf": n_crlf, "sha256_bytes": full}
    crlf_differs = sorted(k for k, h in hashes.items() if h.get("sha16_text_lf") and h.get("sha16_bytes") and h["sha16_text_lf"] != h["sha16_bytes"])
    G = lambda k: (lidos.get(k) or {})
    f5p, f5r, f6p, f6po, f6r, f6d, f6a, v4e, v4po, v4r, f7p, f7r, cov, bank, v5e, v5po, v5r = [G(k) for k in ("f5_pre", "f5_res", "f6_pre", "f6_poder", "f6_res", "f6_diag", "f6_amostra", "v4_emenda", "v4_poder", "v4_res", "f7_pre", "f7_res", "cc_cov", "gw_bank", "v5_emenda", "v5_poder", "v5_res")]
    # ---- (5) SH0ES
    val = f5r.get("validacao") or {}; P5 = ((((f5r.get("familias") or {}).get("P_dr2_sh0es") or {}).get("leituras") or {}).get("sombra") or {}); S5 = f5r.get("resumo") or {}
    alvo_H0 = str(((f5p.get("validacao_alvo") or {}).get("H0")) or "")
    # ---- (6) ECO V3
    R6 = f6r.get("resultados") or {}; T6 = R6.get("todos") or {}; O6 = R6.get("o4") or {}
    K6, M6, KO6, MO6 = T6.get("KMS") or {}, T6.get("MAY") or {}, O6.get("KMS") or {}, O6.get("MAY") or {}
    vK = lambda st, rn: str(((st.get("vereditos") or {}).get(rn) or {}).get("veredito") or "")
    pl = lambda st, rn, k: ((st.get("por_leitura") or {}).get(rn) or {}).get(k)
    cz = lambda st: {k: float((c or {}).get("z") or 0.0) for k, c in (st.get("controles") or {}).items()}
    kms_pair_falsified = all(vK(st, rn).endswith("FALSIFIED_AT_DELAY_LAW") for st in (K6, KO6) for rn in ("R1_peso1", "R2_peso2_2theta"))
    kms_power_before = all(((((f6po.get("poder") or {}).get(sub) or {}).get("KMS") or {}).get("por_leitura") or {}).get(rn, {}).get("poder", 0.0) >= 5.0 for sub in ("todos", "o4") for rn in ("R1_peso1", "R2_peso2_2theta"))
    kms_sys_ok = all((pl(st, rn, "sistematica_relativa") or 9.0) <= 0.3 for st in (K6, KO6) for rn in ("R1_peso1", "R2_peso2_2theta"))
    may_inconclusive = all(vK(M6, rn).endswith("INCONCLUSIVE_SYSTEMATICS") for rn in ("R1_peso1", "R2_peso2_2theta", "R3_quadrado"))
    ctrl_mute_kms = bool(K6.get("controles")) and bool(KO6.get("controles")) and all(abs(z) < 3.0 for st in (K6, KO6) for z in cz(st).values())
    may_ctrl_v3 = {"todos": cz(M6), "o4": cz(MO6)}
    may_ctrl_flag_due = all(abs(float(may_ctrl_v3[sub].get("x0.5") or 0.0)) >= 5.0 for sub in ("todos", "o4"))
    flag_written = _v380_has_str(f6r, "DELAY_CONTROL_RESPONDS")
    o4_is_subsample = int(KO6.get("n_eventos") or 0) < int(K6.get("n_eventos") or 0) and int(KO6.get("n_eventos") or 0) >= 150
    # ---- V4 (nao cega)
    V4T = (v4r.get("resultados") or {}).get("todos") or {}; V4M, V4K = V4T.get("MAY") or {}, V4T.get("KMS") or {}
    v4_declared_not_blind = ("NÃO cega" in str(v4e.get("cegueira", "")) or "NAO cega" in str(v4e.get("cegueira", ""))) and ("NÃO cega" in str(v4r.get("fase", "")) or "NAO cega" in str(v4r.get("fase", "")))
    v4_sin2theta_may_falsified = vK(V4M, "R2_peso2_2theta").endswith("FALSIFIED_AT_DELAY_LAW")
    v4_may_ctrl_max = max([abs(z) for z in cz(V4M).values()] or [0.0])
    v4_kms_same = all(vK(V4K, rn).endswith("FALSIFIED_AT_DELAY_LAW") for rn in ("R1_peso1", "R2_peso2_2theta"))
    v4_sqrt_beta_may_inconclusive = vK(V4M, "R1_peso1").endswith("INCONCLUSIVE_SYSTEMATICS")
    v4_third_amendment_rule = any("terceira vez" in str(r) for r in (v4e.get("regra_de_veredito") or []))
    # ---- V5 (a lei de atraso de dezembro/2025 do acervo; CEGA so quanto a lei nova)
    V5T = (v5r.get("resultados") or {}).get("todos") or {}; V5D = V5T.get("DEC") or {}; V5O = ((v5r.get("resultados") or {}).get("o4") or {}).get("DEC") or {}
    _ceg = str(v5e.get("cegueira", "")).upper()
    v5_blind = (_ceg.startswith("CEGA") and "NÃO CEGA" not in _ceg and "NAO CEGA" not in _ceg and "DEC" in str((v5e.get("leis_de_atraso") or {}).keys())
                and "24/12/2025" in str((v5e.get("lei_nova") or {}).get("fonte", "")) and "DECLARADO" in str((v5e.get("lei_nova") or {}).get("estatuto", "")))
    dec_pair_falsified = all(vK(st, rn).endswith("FALSIFIED_AT_DELAY_LAW") for st in (V5D, V5O) for rn in ("R1_peso1", "R2_peso2_2theta"))
    dec_sys_ok = all((pl(st, rn, "sistematica_relativa") or 9.0) <= 0.3 for st in (V5D, V5O) for rn in ("R1_peso1", "R2_peso2_2theta"))
    dec_r3_power = pl(V5D, "R3_quadrado", "poder")
    dec_r3_label = vK(V5D, "R3_quadrado")
    dec_r3_power_blind = ((((((v5po.get("poder") or {}).get("todos") or {}).get("DEC") or {}).get("por_leitura") or {}).get("R3_quadrado") or {}).get("poder"))
    v5_clause_text = any("NOT_FALSIFIED_UNDERPOWERED" in str(r) and "R3" in str(r) for r in (v5e.get("regra_de_veredito") or []))
    v5_clause_applied = dec_r3_label.endswith("NOT_FALSIFIED_UNDERPOWERED")
    ctrl_mute_dec = bool(V5D.get("controles")) and bool(V5O.get("controles")) and all(abs(z) < 3.0 for st in (V5D, V5O) for z in cz(st).values())
    # ---- (7) cronometros com covariancia
    F7 = f7r.get("familias") or {}; T7 = ((F7.get("T_dr2_cc") or {}).get("leituras") or {}).get("acumulada") or {}; S7 = ((F7.get("S_dr2_escada_cc") or {}).get("leituras") or {}).get("acumulada") or {}
    lnB7 = (f7r.get("resumo") or {}).get("lnB_sombra_vs_acumulada") or {}
    tz = lambda d, k: (d.get(k) or {}).get("z_ganho_da_lei")
    # ---- banco
    n_ok_bank, n_jobs_bank = int(bank.get("n_ok") or 0), int(bank.get("n_jobs") or 0)
    bank_status = {}
    for s_ in (bank.get("series") or []):
        bank_status[str((s_ or {}).get("status"))] = bank_status.get(str((s_ or {}).get("status")), 0) + 1
    n_nan_bank, n_out_bank = int(bank_status.get("NAN_IN_WINDOW") or 0), int(bank_status.get("WINDOW_OUTSIDE_FILE") or 0)
    n_hdf5_bank = len({(s_ or {}).get("hdf5") for s_ in (bank.get("series") or [])})
    # ---- os vereditos, guardados
    vereditos = [str(f5r.get("veredito") or ""), str(val.get("veredito") or "")] + [vK(st, rn) for st in (K6, M6, KO6, V4M, V4K, V5D, V5O) for rn in ("R1_peso1", "R2_peso2_2theta", "R3_quadrado")] + [str(f7r.get("veredito") or "")]
    checks = [
        ("Os 18 artefatos das Fases 5, 6 (V3, poder, diagnostico, amostra, remanescentes; emendas V4 e V5 com os seus poderes), 7, a covariancia e o manifesto do banco LIDOS POR HASH (bytes e texto LF) do cache do rito",
         all(lidos.get(k) is not None for k in _V380_FILES) and len(_V380_FILES) == 18),
        ("Cada RESULTADO conferiu o sha256 do SEU pre-registro, e o hash bate com o arquivo lido aqui (F5, F6, V4 e V5 com as emendas, F7)",
         str(f5r.get("preregistro_sha256")) == str(hashes["f5_pre"]["sha256_bytes"]) and str(f6r.get("preregistro_sha256")) == str(hashes["f6_pre"]["sha256_bytes"])
         and str(v4r.get("preregistro_sha256")) == str(hashes["v4_emenda"]["sha256_bytes"]) and str(v5r.get("preregistro_sha256")) == str(hashes["v5_emenda"]["sha256_bytes"])
         and str(f7r.get("preregistro_sha256")) == str(hashes["f7_pre"]["sha256_bytes"])),
        ("Os TRES poderes gravados ANTES de abrir (V3, V4, V5) batem, por sha256, com o que cada RESULTADO declara ter lido",
         str(f6r.get("poder_antes_de_abrir_sha256")) == str(hashes["f6_poder"]["sha256_bytes"]) and str(v4r.get("poder_antes_de_abrir_sha256")) == str(hashes["v4_poder"]["sha256_bytes"])
         and str(v5r.get("poder_antes_de_abrir_sha256")) == str(hashes["v5_poder"]["sha256_bytes"])),
        ("beta_tgl dos tres RESULTADOS e dos pre-registros = alpha.sqrt(e) do core a 1e-9 relativo (nunca literal)",
         beta > 0 and all(abs(float(x) / beta - 1.0) < 1e-9 for x in (f5r.get("beta_tgl"), f6r.get("beta_tgl"), f7r.get("beta_tgl"), f6p.get("beta_runtime"), f7p.get("beta_tgl_runtime")) if x is not None)
         and all(x is not None for x in (f5r.get("beta_tgl"), f6r.get("beta_tgl"), f7r.get("beta_tgl")))),
        ("(5) SH0ES na Bancada: 1657 SNe (1580 + 77 calibradores Cefeida em 37 hospedeiras) e a validacao do H0 da escada presente, com z contra um alvo que o pre-registro marca [DECLARADO] (nao relido na fonte)",
         int((f5r.get("pantheon_sh0es") or {}).get("n") or 0) == 1657 and int((f5r.get("pantheon_sh0es") or {}).get("n_calibradores") or 0) == 77 and val.get("H0") is not None and val.get("z_vs_alvo") is not None
         and "DECLARADO" in alvo_H0),
        ("(6) A amostra pre-registrada: 244 BBH (m2 >= 3 Msun, SNR >= 8, p_astro >= 0,5; H1 e L1), 484 series com sha256 no pre-registro, 4 ausentes ditas",
         int(f6a.get("n") or 0) == 244 and int((f6p.get("amostra") or {}).get("n_series") or 0) == 484 and len((f6p.get("amostra") or {}).get("faltam") or []) == 4),
        ("(6) As TRES leituras da amplitude e as DUAS leis de atraso estao no pre-registro; a raiz entra como amplitude (v379), nao como operacao sobre o strain",
         set((f6p.get("leituras") or {}).keys()) == {"R1_peso1", "R2_peso2_2theta", "R3_quadrado"} and set((f6p.get("leis_de_atraso") or {}).keys()) == {"MAY", "KMS"} and "g = √|h|" in str(f6p.get("o_que_se_testa", ""))),
        ("(6) O PODER foi gravado ANTES de abrir: KMS R1 e R2 >= 5 sigma em «todos» e em «o4»", kms_power_before),
        ("(6) O par (sqrt(beta) ou sin 2theta_M, 2pi/kappa) FALSIFIED_AT_DELAY_LAW em «todos» (240 BBH) e na SUBAMOSTRA cega «o4» (173 dos 240 -- nao uma replica independente), com sistematica relativa <= 0,3 e controles mudos nas duas",
         kms_pair_falsified and kms_sys_ok and ctrl_mute_kms and int(K6.get("n_eventos") or 0) >= 200 and o4_is_subsample),
        ("(6) A lei MAY INCONCLUSIVE_SYSTEMATICS pela regra 2 (descasamento no atraso curto); o diagnostico post hoc esta dito como post hoc", may_inconclusive and "POST HOC" in str(f6d.get("estatuto", "")).upper()),
        ("(6) DESVIO DITO: na V3 o controle tau/2 da lei MAY respondeu ACIMA da bandeira pre-registrada (|z| >= 5 em «todos» e «o4») e o pipeline NAO gravou DELAY_CONTROL_RESPONDS -- o rotulo coincide pela regra 2",
         may_ctrl_flag_due and not flag_written and may_inconclusive),
        ("(V4) A emenda e NAO CEGA, dita no pre-registro da emenda e no resultado; sin 2theta x MAY sai FALSIFIED com os controles abaixo da bandeira de 5 sigma; sqrt(beta) x MAY segue INCONCLUSIVE como limite "
         "deste estimador (regra V4: nao se emenda uma terceira vez); KMS inalterado",
         v4_declared_not_blind and v4_sin2theta_may_falsified and v4_may_ctrl_max < 5.0 and v4_kms_same and v4_sqrt_beta_may_inconclusive and v4_third_amendment_rule),
        ("(V5) A lei de atraso de 24/12/2025 do acervo (2GM_f/(beta c^3), ~14 periodos; [DECLARADO -- derivacao por IA sob direcao do operador; nunca testada nesse atraso]), CEGA SO quanto a lei nova (V3 e V4 "
         "ja abertas): o par (sqrt(beta) ou sin 2theta, DEC) FALSIFIED_AT_DELAY_LAW em «todos» e na subamostra cega «o4» com sistematica <= 0,3 e controles mudos",
         v5_blind and dec_pair_falsified and dec_sys_ok and ctrl_mute_dec),
        ("(V5) DESVIO DITO: o par do proprio documento (beta, DEC) saiu INCONCLUSIVE_SYSTEMATICS pela regra geral 2 (sistematica relativa a amplitude minuscula > 0,3) com poder < 5 sigma; a clausula V5 da "
         "emenda (poder de R3 < 5 sigma -> NOT_FALSIFIED_UNDERPOWERED) esta no pre-registro e NAO foi aplicada pelo pipeline -- sem poder, nao falsificado",
         dec_r3_label.endswith("INCONCLUSIVE_SYSTEMATICS") and dec_r3_power is not None and float(dec_r3_power) < 5.0 and v5_clause_text and not v5_clause_applied),
        ("(7) As tres variantes de covariancia presentes nas familias T, S, U; a covariancia importada com os 4 arquivos do repositorio por sha256 e a receita dita",
         all(v in T7 and v in S7 and v in lnB7 for v in ("diagonal", "moresco2020", "moresco2020_todos")) and len(cov.get("arquivos") or {}) == 4 and "IMF" in str(cov.get("receita", ""))),
        ("(7) Os 15 pontos de Moresco casados com a fonte (sem o arredondamento do artigo); os 17 outros diagonais -- dito na nota", len((cov.get("pontos") or {}).get("casamento") or []) == 15 and "diagonais" in str(cov.get("nota", ""))),
        ("O banco de GW: manifesto do O4 lido por hash; as 354 series somam OK + NaN na janela + janela fora do arquivo (>= 300 OK; os NaN e as janelas fora sao ditos no veredito)",
         n_jobs_bank == 354 and n_ok_bank >= 300 and sum(bank_status.values()) == n_jobs_bank and n_ok_bank + n_nan_bank + n_out_bank == n_jobs_bank),
        ("Nenhuma palavra proibida em nenhum veredito lido (a MESMA guarda do rito); cada veredito de fase existe", all(vereditos) and not any(_V380_GUARDA.search(v) for v in vereditos)),
        ("O «100 sigma» de dezembro NAO foi refeito: o pre-registro da Fase 6 o declara retirado (v340); rota examinada nao se refaz", "v340" in str(f6p.get("o_que_se_testa", "")) and "não se refaz" in str(f6p.get("o_que_se_testa", ""))),
        ("As erratas ao lado deste modulo: SEIS da auditoria de 28/09 + UMA da v378 + UMA nota (8 entradas), sem palavra proibida",
         len(_V380_ERRATAS_BESIDE) == 8 and all(k in _V380_ERRATAS_BESIDE for k in _V380_ERRATAS_AUDITORIA) and len(_V380_ERRATAS_AUDITORIA) == 6
         and not any(_V380_GUARDA.search(s_) for s_ in _V380_ERRATAS_BESIDE.values())),
        ("O operador, verbatim: as quatro ordens de 01/10/2026", all(_V380_OPERATOR_VERBATIM.get(k) for k in ("sh0es_20261001", "radical_20261001", "bank_20261001", "solve_20261001"))),
        ("Hash de BYTES e de TEXTO normalizado a LF lado a lado em cada artefato (EV-08): os artefatos onde diferem sao exatamente os que tem CRLF, e a diferenca e dita no veredito",
         all(h["sha16_text_lf"] and h["sha16_bytes"] for h in hashes.values()) and all((hashes[k]["crlf"] or 0) > 0 for k in crlf_differs) and all((h["crlf"] or 0) == 0 for k, h in hashes.items() if k not in crlf_differs)),
    ]
    ok = all(v for _, v in checks)
    if ok:
        verdict = ("TGL_BANCADA_FASES_5_6_7_V380__READ_BY_HASH_BYTES_AND_LF_TEXT__TEXT_VS_BYTES_DIFFER_%d_CRLF__SH0ES_IN_THE_BENCH_H0_LADDER_%s_PM_%s_Z_%s_VS_DECLARED_TARGET__"
                   "ECHO_V3_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_Z_EXCL_%s_AND_%s__BLIND_O4_SUBSAMPLE_%d_OF_%d_Z_EXCL_%s_AND_%s__"
                   "POWER_RECORDED_BEFORE_OPENING__MAY_INCONCLUSIVE_SYSTEMATICS__MAY_TAU_HALF_CONTROL_RESPONDS_Z_%s_O4_%s_FLAG_NOT_WRITTEN_BY_PIPELINE_STATED__"
                   "AMENDMENT_V4_NOT_BLIND_SIN2THETA_MAY_FALSIFIED_Z_%s_CONTROLS_MAX_Z_%s__SQRT_BETA_MAY_INCONCLUSIVE_IS_THE_ESTIMATOR_LIMIT__"
                   "CC_COVARIANCE_MORESCO2020_T_LAW_GAIN_Z_%s_VS_DIAG_%s__U_LNB_SHADOW_VS_ACCUMULATED_%s_VS_DIAG_%s__"
                   "DEC2025_LAW_FROM_THE_ARCHIVE_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_Z_EXCL_%s_AND_%s_O4_%s_AND_%s__"
                   "DOC_PAIR_BETA_DEC_INCONCLUSIVE_SYSTEMATICS_BY_RULE_2_POWER_%s_BLIND_POWER_%s__V5_CLAUSE_UNDERPOWERED_NOT_APPLIED_STATED__FOURTH_ARCHIVE_LAW_ALPHA_SQUARED_NOT_TESTED_OUTSIDE_SEGMENT__"
                   "GW_BANK_%d_OF_%d_SERIES_OK_%d_NAN_%d_OUTSIDE__PAIR_FALSIFIED_NOT_THE_THEORY__DECEMBER_100SIGMA_STAYS_RETIRED__ERRATA_BESIDE_6_PLUS_V378_1_PLUS_NOTE_1__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
                   % (len(crlf_differs), _v378_tag(val.get("H0", 0.0)), _v378_tag(val.get("sigma_H0", 0.0)), _v378_tag(val.get("z_vs_alvo", 0.0)),
                      _v378_tag(pl(K6, "R1_peso1", "z_excl") or 0.0), _v378_tag(pl(K6, "R2_peso2_2theta", "z_excl") or 0.0), int(KO6.get("n_eventos") or 0), int(K6.get("n_eventos") or 0),
                      _v378_tag(pl(KO6, "R1_peso1", "z_excl") or 0.0), _v378_tag(pl(KO6, "R2_peso2_2theta", "z_excl") or 0.0),
                      _v378_tag(may_ctrl_v3["todos"].get("x0.5") or 0.0), _v378_tag(may_ctrl_v3["o4"].get("x0.5") or 0.0),
                      _v378_tag(pl(V4M, "R2_peso2_2theta", "z_excl") or 0.0), _v378_tag(v4_may_ctrl_max), _v378_tag(tz(T7, "moresco2020") or 0.0), _v378_tag(tz(T7, "diagonal") or 0.0),
                      _v378_tag(lnB7.get("moresco2020", 0.0)), _v378_tag(lnB7.get("diagonal", 0.0)),
                      _v378_tag(pl(V5D, "R1_peso1", "z_excl") or 0.0), _v378_tag(pl(V5D, "R2_peso2_2theta", "z_excl") or 0.0), _v378_tag(pl(V5O, "R1_peso1", "z_excl") or 0.0), _v378_tag(pl(V5O, "R2_peso2_2theta", "z_excl") or 0.0),
                      _v378_tag(dec_r3_power or 0.0), _v378_tag(dec_r3_power_blind or 0.0),
                      n_ok_bank, n_jobs_bank, n_nan_bank, n_out_bank))
    else:
        verdict = "TGL_BANCADA_FASES_5_6_7_V380__NOT_READ_THIS_RUN__%s__GATE_UNTOUCHED" % ("ARTIFACTS_ABSENT" if any(lidos.get(k) is None for k in _V380_FILES) else "CHECKS_FAILED")
    num = lambda x, n=5: _v378_num(x, n)
    return {"operator_verbatim": dict(_V380_OPERATOR_VERBATIM), "checks": checks, "all_verified": ok, "verdict": verdict, "hashes": hashes, "crlf_differs": crlf_differs,
            "fase5": {"veredito": str(f5r.get("veredito") or ""), "validacao": {k: num(val.get(k)) for k in ("H0", "sigma_H0", "Omega_m", "z_vs_alvo")}, "validacao_veredito": str(val.get("veredito") or ""),
                      "alvo_H0": alvo_H0, "P_sombra": {"delta": num(P5.get("delta")), "sigma_delta": num(P5.get("sigma_delta")), "z_delta": num(P5.get("z_delta")), "z_tensao": num(P5.get("z_tensao"))},
                      "lnB_sombra_vs_acumulada_S": num(S5.get("lnB_sombra_vs_acumulada_S")), "n": (f5r.get("pantheon_sh0es") or {}).get("n")},
            "fase6": {"veredito_principal": f6r.get("veredito_principal"), "n_series_cego": f6r.get("n_series_cego"), "faltam": f6r.get("faltam"),
                      "todos_KMS": {"n_eventos": K6.get("n_eventos"), "a": num(K6.get("a")), "sigma_usado": num(K6.get("sigma_usado")), "z_det": num(K6.get("z_det")), "sistematica_abs": num(K6.get("sistematica_abs")),
                                    "z_excl_R1": num(pl(K6, "R1_peso1", "z_excl")), "z_excl_R2": num(pl(K6, "R2_peso2_2theta", "z_excl")), "poder_R1": num(pl(K6, "R1_peso1", "poder")), "poder_R2": num(pl(K6, "R2_peso2_2theta", "poder")),
                                    "sist_rel_R1": num(pl(K6, "R1_peso1", "sistematica_relativa")), "sist_rel_R2": num(pl(K6, "R2_peso2_2theta", "sistematica_relativa")),
                                    "controles_z": {k: num(z) for k, z in cz(K6).items()}},
                      "o4_KMS_cego": {"n_eventos": KO6.get("n_eventos"), "subamostra_de_todos": o4_is_subsample, "a": num(KO6.get("a")), "sigma_usado": num(KO6.get("sigma_usado")),
                                      "z_excl_R1": num(pl(KO6, "R1_peso1", "z_excl")), "z_excl_R2": num(pl(KO6, "R2_peso2_2theta", "z_excl")), "controles_z": {k: num(z) for k, z in cz(KO6).items()}},
                      "maio_KMS_nao_cego": {rn: vK((R6.get("maio") or {}).get("KMS") or {}, rn) for rn in ("R1_peso1", "R2_peso2_2theta")},
                      "todos_MAY": {"a": num(M6.get("a")), "sigma_usado": num(M6.get("sigma_usado")), "sistematica_abs": num(M6.get("sistematica_abs")), "controles_z": {k: num(z) for k, z in cz(M6).items()}},
                      "controles_MAY_v3_z": {sub: {k: num(z) for k, z in d.items()} for sub, d in may_ctrl_v3.items()}, "flag_delay_control_written_by_pipeline": flag_written,
                      "leituras": f6p.get("leituras"), "visto_antes": f6p.get("visto_antes"), "diag_post_hoc": {"estatuto": f6d.get("estatuto"), "MAY_x05": ((f6d.get("stacks") or {}).get("MAY") or {}).get("x0.5")}},
            "emenda_v4": {"cegueira": v4e.get("cegueira"), "o_que_muda": v4e.get("o_que_muda"), "todos_MAY": {"a": num(V4M.get("a")), "sigma_usado": num(V4M.get("sigma_usado")), "sistematica_abs": num(V4M.get("sistematica_abs")),
                          "z_excl_R2": num(pl(V4M, "R2_peso2_2theta", "z_excl")), "sist_rel_R1": num(pl(V4M, "R1_peso1", "sistematica_relativa")), "controles_max_z": num(v4_may_ctrl_max)},
                          "vereditos_todos": {law: {rn: vK(V4T.get(law) or {}, rn) for rn in ("R1_peso1", "R2_peso2_2theta", "R3_quadrado")} for law in ("MAY", "KMS")},
                          "regra_terceira_emenda": v4_third_amendment_rule},
            "emenda_v5": {"cegueira": v5e.get("cegueira"), "lei_nova": (v5e.get("lei_nova") or {}).get("formula"), "fonte": (v5e.get("lei_nova") or {}).get("fonte"), "estatuto": (v5e.get("lei_nova") or {}).get("estatuto"),
                          "todos_DEC": {"n_eventos": V5D.get("n_eventos"), "a": num(V5D.get("a")), "sigma_usado": num(V5D.get("sigma_usado")), "z_det": num(V5D.get("z_det")), "sistematica_abs": num(V5D.get("sistematica_abs")),
                                        "z_excl_R1": num(pl(V5D, "R1_peso1", "z_excl")), "z_excl_R2": num(pl(V5D, "R2_peso2_2theta", "z_excl")), "poder_R3": num(dec_r3_power), "sist_rel_R3": num(pl(V5D, "R3_quadrado", "sistematica_relativa")),
                                        "controles_z": {k: num(z) for k, z in cz(V5D).items()}},
                          "o4_DEC_cego": {"n_eventos": V5O.get("n_eventos"), "a": num(V5O.get("a")), "z_excl_R1": num(pl(V5O, "R1_peso1", "z_excl")), "z_excl_R2": num(pl(V5O, "R2_peso2_2theta", "z_excl")), "controles_z": {k: num(z) for k, z in cz(V5O).items()}},
                          "vereditos_todos_DEC": {rn: vK(V5D, rn) for rn in ("R1_peso1", "R2_peso2_2theta", "R3_quadrado")},
                          "R3_rotulo_emitido": dec_r3_label, "poder_R3_cego": num(dec_r3_power_blind), "clausula_v5_no_preregistro": v5_clause_text, "clausula_v5_aplicada_pelo_pipeline": v5_clause_applied,
                          "leitura": ("o par do documento de 24/12/2025 (amplitude beta) saiu INCONCLUSIVE_SYSTEMATICS pela regra geral 2 (sistematica relativa a amplitude minuscula > 0,3), com poder < 5 sigma; "
                                      "a clausula V5 da emenda (poder de R3 < 5 sigma -> NOT_FALSIFIED_UNDERPOWERED) nao foi aplicada pelo pipeline -- desvio dito, nao corrigido por cima: sem poder, nao falsificado; "
                                      "as leituras radicais sqrt(beta) e sin 2theta nesse atraso estao falsificadas; a quarta lei do acervo, 2GM/(alpha^2 c^3) (4-12 s), nao foi testada: fora do segmento de 2,5 s")},
            "fase7": {"veredito": str(f7r.get("veredito") or ""), "T_z_ganho": {v: num(tz(T7, v)) for v in ("diagonal", "moresco2020", "moresco2020_todos")},
                      "T_delta_moresco2020": {"delta": num((T7.get("moresco2020") or {}).get("delta")), "sigma": num((T7.get("moresco2020") or {}).get("sigma_delta")), "z": num((T7.get("moresco2020") or {}).get("z_delta"))},
                      "U_lnB_sombra_vs_acumulada": {v: num(lnB7.get(v)) for v in ("diagonal", "moresco2020", "moresco2020_todos")},
                      "S_delta": {v: {"delta": num((S7.get(v) or {}).get("delta")), "z": num((S7.get(v) or {}).get("z_delta"))} for v in ("diagonal", "moresco2020")},
                      "poder_previo": (f7p.get("poder_previo") or {}).get("fisher_beta_relogios_fundo_fixo"), "receita": cov.get("receita"), "nota": cov.get("nota")},
            "gw_bank": {"n_ok": n_ok_bank, "n_jobs": n_jobs_bank, "status": bank_status, "n_hdf5_distintos": n_hdf5_bank, "fonte": bank.get("source"), "created": bank.get("created")},
            "errata_beside_v380": dict(_V380_ERRATAS_BESIDE), "errata_beside_v380_da_auditoria": list(_V380_ERRATAS_AUDITORIA),
            "statute": ("Fases 5-7 [REAL, pre-registradas, lidas por hash]; a falsificacao do PAR (leitura, lei de atraso) nao e falsificacao da teoria; as leis de atraso MAY e KMS sao [INPUT/ONTO] e a DEC e "
                        "[DECLARADO -- derivacao por IA sob direcao do operador, nao derivada do axioma, nao escrita na voz dele]; a leitura sin 2theta e [CONJECTURE]; o peso da resposta da fronteira ao "
                        "graviton e a lei de atraso derivada sao decisoes do operador (CT-03); (sqrt(beta), MAY) INCONCLUSIVE_SYSTEMATICS e o limite deste estimador (regra V4); a quarta lei do acervo, "
                        "2GM/(alpha^2 c^3), nao foi testada; a validacao SH0ES compara com um alvo [DECLARADO, nao relido na fonte]; a subamostra cega O4 nao e replica independente; a leitura «sombra» e "
                        "[OPEN/ONTO]; a variante «todos» da covariancia e faixa, nao estimativa; NOT_FALSIFIED nao e CONFIRMADA; PROVADA nao e CONFIRMADA; o gate nao se move"),
            "does_not_gate_core": True}
