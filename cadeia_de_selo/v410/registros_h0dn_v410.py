# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] os dados do SEGUNDO registro com FUNCAO da v410 (D72 + E30 + D76): H0DN x BG1, pre-registrado.
"""registros_h0dn_v410.py -- o CONTRATO, o TEXTO e os INSUMOS EMBUTIDOS (base64, pinados por sha256 LIDO) do registro h0dn_bg1_v410 (gerar_candidato_v410.py os emite com runtime_h0dn_v410.py). Nada digitado: os pinos sao lidos
dos arquivos do desenho do Codex astra-bell (06/11; FREEZE_R2.json, 9 pinos) e da leitura da gerencia (LEITURA_DOSSIE_5SIGMA_09nov.json); os numeros esperados ficam nos proprios insumos (a ENTREGA, o BG1, o npz) e sao
RECOMPUTADOS em runtime; beta nunca literal. Pré-registrado; nenhum dado observado lido: nenhum vetor observado e' embutido nem procurado; o poder e' prospectivo e sintetico; a abertura e' de versao futura, com a covariancia fisica fechada.
As FONTES pinadas (copias duraveis em v410\\insumos\\h0dn_*; copiar_insumos_v410.py as copia) e os insumos EMBUTIDOS sao os mesmos bytes."""
import base64, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

sha256 = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos")
H0DN_DIR = DL.H0DN_DIR
# os insumos EMBUTIDOS (nome -> caminho relativo na pasta do desenho); network.npz NAO e' embutido (so' pinado pelo FREEZE_R2)
EMBUTIDOS = [("estimator_frozen.npz", "estimator_frozen.npz"), ("BG1.json", "background/BG1.json"), ("analysis_plan.json", "analysis_plan.json"), ("FREEZE_R2.json", "FREEZE_R2.json"), ("estimator.py", "estimator.py"), ("ENTREGA_H0DN_BG1.json", "ENTREGA_H0DN_BG1.json")]
SO_NO_DISCO = ["prepare_estimator.py", "network/network.npz", "network/MANIFEST.json", "background/build_bg1.py", "PROSPECTIVE_GEOMETRY.json"]
ORDEM_KIMI = os.path.join(DL.WK, "h0dn_bg1_v410_09nov", "ORDEM_KIMI_H0DN_01_09nov.md")
LEITURA_DOSSIE = os.path.join(HERE, "LEITURA_DOSSIE_5SIGMA_09nov.json")
# as FONTES pinadas (chave -> (nome da copia duravel em insumos\\, origem, papel)); copiar_insumos_v410.py copia por RG.ORIGENS; o motor v392 le por chave
FONTES_H0DN = [
    ("h0dn_freeze_r2", "h0dn_FREEZE_R2.json", os.path.join(H0DN_DIR, "FREEZE_R2.json"), "o congelamento R2 do desenho do Codex astra-bell (06/11): 9 pinos por sha256, ANTES de qualquer injecao mascarada; supersede o FREEZE R1 sem apagar [REAL: sha256]"),
    ("h0dn_analysis_plan", "h0dn_analysis_plan.json", os.path.join(H0DN_DIR, "analysis_plan.json"), "o plano de analise congelado: nulo, alternativa, estatistica Z unilateral, limiar 5, dois modelos sem selecao, not_a_nature_verdict [REAL: sha256; DECLARADO pelo Codex]"),
    ("h0dn_estimator_py", "h0dn_estimator.py", os.path.join(H0DN_DIR, "estimator.py"), "o estimador linear congelado (geometria; evaluate sem acesso a rotulos) [REAL: sha256; DECLARADO pelo Codex]"),
    ("h0dn_estimator_frozen_npz", "h0dn_estimator_frozen.npz", os.path.join(H0DN_DIR, "estimator_frozen.npz"), "o estimador congelado (weights, C_joint, gradient_h/k, sd_null, sd_tgl, logK, H0; sem chave de dado observado) [REAL: sha256]"),
    ("h0dn_bg1_json", "h0dn_BG1.json", os.path.join(H0DN_DIR, "background", "BG1.json"), "o fundo BG1 (Planck comprimido + DESI DR2, restaurado do recibo da F9 v2-c1): H0, covariancia, a lei K com Omega_m/Omega_r congelados [REAL: sha256]"),
    ("h0dn_entrega", "h0dn_ENTREGA_H0DN_BG1.json", os.path.join(H0DN_DIR, "ENTREGA_H0DN_BG1.json"), "a ENTREGA do Codex (06/11): D esperado, poder MC e analitico, cauda nula, cobertura, o que fica aberto (covariancia fisica) [REAL: sha256; DECLARADO pelo Codex nos numeros, RECOMPUTADOS aqui onde a checagem diz]"),
    ("h0dn_ordem_kimi", "h0dn_ORDEM_KIMI_H0DN_01_09nov.md", ORDEM_KIMI, "a ORDEM da gerencia ao Kimi K3 Pro (09/11): montar y_obs e fechar a covariancia fisica (G1-G4) para a abertura futura; nada de abrir, nenhuma semente nova [REAL: sha256]"),
    ("h0dn_leitura_dossie", "h0dn_LEITURA_DOSSIE_5SIGMA_09nov.json", LEITURA_DOSSIE, "a leitura da gerencia do dossie (09/11): o que esta' congelado, o que esta' em disco, o que falta; a aritmetica do agregado publico NAO e' resultado [REAL: sha256]"),
]
ORIGENS_H0DN = [(nome_, orig_) for _, nome_, orig_, _ in FONTES_H0DN]
FONTES_H0DN_RG = [{"chave": ch_, "arquivo": os.path.join(INS, nome_), "papel": papel_} for ch_, nome_, _, papel_ in FONTES_H0DN]
for _c, _n, _o, _p in FONTES_H0DN:
    assert os.path.exists(_o), ("fonte do H0DN ausente", _o)
assert sha256(open(LEITURA_DOSSIE, "rb").read())[:16] == DL.LEITURA_DOSSIE_SHA16_DO_DESENHO, "a LEITURA_DOSSIE_5SIGMA_09nov.json nao tem o sha16 que o DESENHO (D72) deu"


def insumos_embutidos():
    """{nome: {'b64', 'sha256', 'bytes', 'rel'}} -- os bytes LIDOS dos arquivos do desenho, em base64 (o um.py os decodifica e confere a cada rito)."""
    out = {}
    for nome, rel in EMBUTIDOS:
        b = open(os.path.join(H0DN_DIR, *rel.split("/")), "rb").read()
        out[nome] = {"b64": base64.b64encode(b).decode("ascii"), "sha256": sha256(b), "bytes": len(b), "rel": rel}
    return out


def _pinos_do_freeze():
    fz = json.load(open(os.path.join(H0DN_DIR, "FREEZE_R2.json"), encoding="utf-8"))
    assert len(fz["files"]) == DL.N_PINOS_FREEZE_R2, ("o FREEZE_R2 nao traz os 9 pinos", len(fz["files"]))
    por_rel = {}
    for f in fz["files"]:
        p = f["path"].replace("\\", "/"); partes = p.split("/")
        rel = "/".join(partes[-2:]) if partes[-2] in ("network", "background") else partes[-1]
        por_rel[rel] = f
    for nome, rel in EMBUTIDOS:
        if rel in por_rel:
            b = open(os.path.join(H0DN_DIR, *rel.split("/")), "rb").read()
            assert sha256(b) == por_rel[rel]["sha256"] and len(b) == por_rel[rel]["bytes"], ("o arquivo em disco nao bate com o pino do FREEZE_R2", rel)
    assert set(SO_NO_DISCO) <= set(por_rel) and set(SO_NO_DISCO) | {rel for _, rel in EMBUTIDOS if rel in por_rel} == set(por_rel), ("os 9 pinos do FREEZE_R2 nao sao os 4 embutidos + os 5 so' em disco", sorted(por_rel))
    return fz, por_rel


def contrato_h0dn(core0, selo0):
    """O contrato do registro h0dn_bg1_v410, DERIVADO dos arquivos (pinos lidos) e do core/selo da v409 selada (o gate a repetir); os numeros esperados NAO entram aqui: ficam nos insumos embutidos e sao recomputados em runtime."""
    ins = insumos_embutidos()
    fz, por_rel = _pinos_do_freeze()
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict")
    v387 = core0.get("hubble_ratio_v387") or {}; tr = v387.get("transcribed") or {}
    assert isinstance(tr.get("z_star"), (int, float)) and isinstance(tr.get("K_no_fundo_nu"), (int, float)) and v387.get("all_verified") is True, "a Fase 9 V1 (hubble_ratio_v387) da base nao traz z_star e K transcritos: o c2 nao teria com que conferir"
    bg1 = json.loads(open(os.path.join(H0DN_DIR, "background", "BG1.json"), "rb").read().decode("utf-8"))
    assert bg1["law"]["form"] == "K=E(z_star)^(2 beta/3)" and float(bg1["law"]["z_star"]) == float(tr["z_star"]), "a lei do BG1 nao e' a da Fase 9 (forma ou z*)"
    V = dict(DL.VEREDITOS_H0DN)
    leit = V.pop("leitura"); V.pop("leitura_traz_o_fecho", None)
    i1 = leit.index("VED_IN_NATURE"); i2 = leit.rindex("VED_IS_VALIDITY")   # as partes: nenhuma traz a palavra inteira (a P18 selada da v392 a recusa fora do contexto da validade; D57b)
    V["leitura_partes"] = [leit[:i1], leit[i1:i2], leit[i2:]]
    assert "".join(V["leitura_partes"]) == leit and all(("TGL_PRO" + "VED") not in p_ for p_ in V["leitura_partes"])
    ramos = {"limiar": DL.H0DN_LIMIAR_SIGMA, "compat_95": DL.H0DN_COMPAT_95, "vereditos": V, "outcomes": list(DL.VEREDITOS_H0DN["outcomes"])}
    ok = lambda p: open(p, "rb").read()
    b_ordem = ok(ORDEM_KIMI); b_leit = ok(LEITURA_DOSSIE)
    vetores = [   # DETERMINISTICOS, sem semente; D, z_null e z_tgl referidos ao D esperado do modelo (calculado em runtime), nunca digitados
        {"nome": "covariancia_fisica_aberta_hoje", "z_null": 0.0, "z_tgl": 0.0, "D_de": "published_baseline", "fechada": False, "suporte": True, "ramo": 1, "outcome": "INCONCLUSIVE"},
        {"nome": "fora_do_suporte", "z_null_de": "published_baseline", "z_tgl": 0.0, "D_de": "published_baseline", "fechada": True, "suporte": False, "ramo": 1, "outcome": "INCONCLUSIVE"},
        {"nome": "esperado_tgl_baseline", "z_null_de": "published_baseline", "z_tgl": 0.0, "D_de": "published_baseline", "fechada": True, "suporte": True, "ramo": 4, "outcome": "NOT_FALSIFIED"},
        {"nome": "esperado_tgl_cefeida_livre", "z_null_de": "free_cepheid_host_differential_bias", "z_tgl": 0.0, "D_de": "free_cepheid_host_differential_bias", "fechada": True, "suporte": True, "ramo": 4, "outcome": "NOT_FALSIFIED"},
        {"nome": "esperado_nulo_baseline", "z_null": 0.0, "z_tgl_de": "published_baseline", "z_tgl_fator": -1.0, "D_de": "published_baseline", "fechada": True, "suporte": True, "ramo": 2, "outcome": "FALSIFIED"},
        {"nome": "tgl_mais_3_sigma", "z_null_de": "published_baseline", "z_null_mais": 3.0, "z_tgl": 3.0, "D_de": "published_baseline", "fechada": True, "suporte": True, "ramo": 5, "outcome": "NOT_FALSIFIED"},
        {"nome": "meio_caminho_baseline", "z_null_de": "published_baseline", "z_null_fator": 0.5, "z_tgl_de": "published_baseline", "z_tgl_fator": -0.5, "D_de": "published_baseline", "fechada": True, "suporte": True, "ramo": 6, "outcome": "NOT_FALSIFIED"},
        {"nome": "subpotente_sintetico_D_4", "z_null_de": "published_baseline", "z_tgl": 0.0, "D": 4.0, "fechada": True, "suporte": True, "ramo": 3, "outcome": "INCONCLUSIVE"},
    ]
    return {"registro": DL.H0DN_REGISTRO, "tag": DL.TAG_H0DN, "veredito_ok": DL.VEREDITO_H0DN_OK, "veredito_recusa": DL.VEREDITO_H0DN_RECUSA, "n_checks": DL.N_CHECKS_H0DN, "frase_parede_pt": DL.FRASE_H0DN_PAREDE_PT, "frase_parede_en": DL.FRASE_H0DN_PAREDE_EN, "frase_poder_pt": DL.FRASE_H0DN_PODER_PT, "frase_poder_en": DL.FRASE_H0DN_PODER_EN, "frase_retorno_pt": DL.FRASE_H0DN_RETORNO_PT, "frase_retorno_en": DL.FRASE_H0DN_RETORNO_EN, "frase_alcance_pt": DL.FRASE_H0DN_ALCANCE_PT, "frase_alcance_en": DL.FRASE_H0DN_ALCANCE_EN,
            "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True), "ordem_kimi_03b": dict(DL.H0DN_ORDEM03B, citado_nao_embutido=True, em_rito_nada_e_lido=True),   # (R3 do painel, PAR-01: a ORDEM KIMI H0DN-03B e' PINO CITADO como a 02, conferida contra o ADENDO 7) (D96: a ORDEM KIMI H0DN-02 e' PINO CITADO: nome, sha256 e bytes lidos do arquivo no build e conferidos contra o ADENDO 3)
            "insumos": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "rel": v_["rel"]} for k_, v_ in ins.items()}, "pinos_freeze_r2_so_no_disco": list(SO_NO_DISCO), "n_pinos_freeze": len(fz["files"]), "pasta_origem": H0DN_DIR,
            "freeze_r2": {"status": fz["status"], "null_alpha": fz["null_alpha"], "created_utc": fz["created_utc"], "sha256": ins["FREEZE_R2.json"]["sha256"]},
            "lei": {"form": bg1["law"]["form"], "beta_rule": "ALPHA_FINE_CODATA_2018 * sqrt(e), em runtime (nunca literal)", "z_star_de": "a lei congelada do BG1, conferido contra hubble_ratio_v387.transcribed.z_star (Fase 9 V1, por hash)", "Omega_m_Omega_r_de": "frozen_Omega_m / frozen_Omega_r da lei congelada do BG1 (S5 historica)"},
            "modelos": ["published_baseline", "free_cepheid_host_differential_bias"], "estatistica": "Z = (h_hat_GLS - log10 H_bg) / sd_null, unilateral positiva, limiar 5; z_tgl = (t - log10 K - b_K) / sd_tgl, bilateral, 1,96",
            "ramos": ramos, "vetores_c6": vetores, "tolerancias": {"K": 1e-12, "sd_rel": 1e-9, "D": 1e-9, "poder": 1e-12},
            "observed_vector_read": False, "observed_paths": [], "chaves_observadas_proibidas": ["y", "y_obs", "observed", "local_observed", "data_local"],
            "pasta_vedada": DL.H0DN_PASTA_VEDADA, "nomes_vedados_partes": [[n_[:len(n_) // 2], n_[len(n_) // 2:]] for n_ in DL.H0DN_NOMES_VEDADOS],   # (em PARTES: o candidato nao traz o nome inteiro de nenhum dado observado)   # (AVISO 09/11) a c7 instrumenta o acesso a arquivos durante a mecanica e recusa se tocar a pasta vedada ou um nome vedado
            "tokens_proibidos_partes": [[t_[:-4], t_[-4:]] for t_ in DL.TOKENS_PROIBIDOS_H0DN], "agregado_publico_nao_entra_partes": [[a_[:2], a_[2:]] for a_ in DL.H0DN_AGREGADO_NAO_ENTRA],   # (em PARTES: o um.py nunca traz o token nem o numero inteiros; o runtime os monta)
            "rota_kimi": dict(DL.H0DN_ROTA_KIMI), "ordem_kimi": {"arquivo": ORDEM_KIMI, "sha256": sha256(b_ordem), "bytes": len(b_ordem)}, "leitura_dossie": {"arquivo": LEITURA_DOSSIE, "sha256": sha256(b_leit), "bytes": len(b_leit)},
            "baseline": {"version": DL.BASE_VERSION, "gate_verdict": gate0, "fase9_v1_z_star": tr["z_star"], "fase9_v1_K": tr["K_no_fundo_nu"]}, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76", "D96")}, "erratas": [DL.ERRATA_E30, DL.ERRATA_E34]}


def texto_h0dn():
    Q = DL.FRASE_H0DN_OBRIGATORIA_PT
    return {
        "estatuto": "[REAL] o que o registro CONFERE neste rito: os pinos do FREEZE_R2 nos insumos embutidos; K e log10 K recomputados de beta (alfa CODATA 2018 x sqrt e, runtime) e conferidos contra a Fase 9 V1 do proprio um.py; sd_null, sd_tgl, D esperado e o poder analitico "
                    "reproduzidos; a funcao de veredito congelada (E30 + D76) em vetores deterministicos; o gate. [DERIVED] o poder prospectivo e' condicional ao modelo de covariancia publicado (bloco-diagonal; independencia local/fundo ASSUMIDA). [DECLARADO] os numeros da ENTREGA do Codex "
                    "(recomputados aqui onde a checagem diz) e o poder MC (conferido dentro do IC95). [INPUT] a ordem do operador de 09/11 (a 12a fala) e a sua leitura do 5 sigma (as falas 14 e 15; E30, D76). [OPEN] a covariancia fisica conjunta (G3/G4), o vetor observado (y_obs) e os IDs (G1/G2): "
                    "a abertura e' de versao futura. [INPUT, D96] a regra do poder (a ordem do operador); [OPEN] o certificado de poder: " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + ". H0DN x BG1: " + Q + ".",
        "escopo": "[REAL] O que entra no um.py: o teste H0DN x BG1 da razao de Hubble local/fundo, " + Q + ". A LEI: nulo H_local/H_fundo = 1; alternativa TGL K = E(z*)^(2 beta/3), beta = alfa sqrt e em runtime, z*, Omega_m e Omega_r da lei congelada (z* e K conferidos contra a Fase 9 V1 por hash), "
                  "zero parametro livre. A ESTATISTICA: Z = (h_hat - log10 H_bg)/sigma_nulo, unilateral, limiar 5; dois modelos (o publicado; o vies diferencial Cefeida livre), nenhum selecionado. OS VEREDITOS PERMITIDOS (a funcao congelada veredito_h0dn, a primeira que casa decide): "
                  "inconclusivo por sistematica enquanto a covariancia fisica nao fechar ou o vetor estiver fora do suporte; a lei K falsificada a 5 sigma a esta sensibilidade; subpotente; a LEITURA do 5 sigma -- beta_TGL provado na natureza (validade, não creditação) a n sigma, na lingua da fisica "
                  "academica, discriminando do LCDM, zero parametro livre, novidade de uso --; discrimina do LCDM com K em tensao de 2 a 5 sigma; nao discriminado a sensibilidade disponivel, com a faixa do desvio; a palavra do livro de cobrancas vai no campo outcome, nunca na cabeca. "
                  "O QUE FALTA (a ORDEM ao Kimi, por sha256): o vetor observado y_obs de 255 linhas pelo codigo upstream; a covariancia fisica SN-only/hospedeira/velocidade peculiar sem duplicar a Cefeida (G3/G4); os IDs e aliases (G1/G2). "
                  "O PODER CERTIFICADO [INPUT, D96] (ordem do operador de 10/11): " + DL.FRASE_H0DN_PODER_PT + "; a ORDEM KIMI H0DN-02 (pino citado por sha256, nao embutida) manda fechar a covariancia fisica e entregar o certificado de poder as cegas, sem o vetor observado; " + DL.FRASE_H0DN_RETORNO_PT + " (a ORDEM KIMI H0DN-03B tambem e' pino citado por sha256, nao embutida); a funcao de veredito congelada nao muda. "
                  "A RESSALVA DA NOVIDADE DE USO: o agregado publico do H0DN e' conhecido desde out/2025; K nao tem parametro ajustado; o PRE-REGISTRO nesta versao selada e' o que vale (lei da prova, 05/10: retrodicao sem ajuste). "
                  "A rota Kimi “coerencia espectro x fotometria” consta como NOT_TESTABLE (eta = 1): não é o teste. Nenhum vetor observado e' lido nem procurado nesta versao; o poder e' prospectivo e sintetico.",
        "o_que_falta": ["y_obs: o vetor observado do H0DN (255 linhas, na ordem de row_names, centrado na convencao do estimador), montado pelo codigo upstream sobre os dados brutos [OPEN; ORDEM ao Kimi]. " + DL.FRASE_H0DN_PAREDE_PT,
                        "G3/G4: a covariancia fisica conjunta 258x258 (SN-only, hospedeira-Cefeida, velocidade peculiar), sem duplicar a informacao Cefeida ja' na rede; o bloco cruzado local/fundo zero so' com a independencia condicional demonstrada [OPEN]",
                        "G1/G2: o operador de agregacao das curvas de luz (47 IDs com multiplas curvas), 8 IDs sem correspondencia exata, 2 aliases candidatos [OPEN]",
                        "o certificado de poder, as cegas, sob a covariancia fisica (D96): " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + " [OPEN; ORDEM KIMI H0DN-02, pino citado: sha256 " + DL.H0DN_ORDEM02["sha256"] + ", " + str(DL.H0DN_ORDEM02["bytes"]) + " bytes; ORDEM KIMI H0DN-03B, pino citado: sha256 " + DL.H0DN_ORDEM03B["sha256"] + ", " + str(DL.H0DN_ORDEM03B["bytes"]) + " bytes; o teste segue " + Q + "]"],
        "ressalvas": [DL.FRASE_H0DN_PAREDE_PT + " (o teste segue " + Q + ")", Q + ": " + DL.FRASE_H0DN_PODER_PT + " ([INPUT, D96], ordem do operador de 10/11; E34); " + DL.FRASE_H0DN_RETORNO_PT,
                      "o poder e' PROSPECTIVO e SINTETICO, da covariancia publicada (que nao aceita o vetor real), condicional ao modelo de covariancia publicado (bloco-diagonal; a independencia local/fundo e' assumida, nao medida); nao e' desvio observado nem poder certificado",
                      "a novidade de uso: o agregado publico e' conhecido desde out/2025 e a abertura futura e' retrodicao sem ajuste (K sem parametro ajustado); o pre-registro nesta versao selada e' o que vale (lei da prova, 05/10)",
                      "a cabeca do ramo de 5 sigma e' a leitura do 5 sigma (beta_TGL provado na natureza (validade, não creditação)), nunca a palavra do livro de cobrancas (E30, D76); confirmada = creditacao (o juizo de fora, que o um.py nao da), que segue recusada; o gate nao se move",
                      "a rota Kimi “coerencia espectro x fotometria” e' NOT_TESTABLE (eta = 1; nao e' o teste); a aritmetica do agregado publico nao e' resultado e nao entra em texto",
                      "beta entra so' por nome; nenhum teste com a natureza nesta versao; validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move; a regra do 4,44 vale em qualquer texto que o cite"],
        "limites": ["[OPEN] a covariancia fisica conjunta (G3/G4), o vetor observado e os IDs: ate' la', a funcao de veredito so' pode devolver inconclusivo por sistematica", "[INPUT, D96] a regra do poder, do operador; [OPEN] o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica (o teste H0DN segue " + Q + "): " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + "; o limiar de poder e' do operador e nao esta' decidido", "[DERIVED] o poder e' condicional ao modelo de covariancia publicado", "[DECLARADO] os numeros da ENTREGA do Codex, recomputados aqui onde a checagem diz",
                    "[REAL] o registro CONFERE e nao abre: nenhum vetor observado e' lido; o que a natureza decide segue da natureza; a abertura e' de versao futura, pela funcao de veredito ja' congelada", "[REAL] " + DL.FRASE_DA_MOLDURA_H0DN_PT],
        "diz": ["o teste H0DN x BG1 esta' " + Q + ": os insumos embutidos e pinados por sha256, a lei K = E(z*)^(2 beta/3) com beta em runtime, a estatistica e o limiar congelados, os dois modelos sem selecao, a funcao de veredito congelada com o sha256 do texto-fonte no registro",
                "K e log10 K recomputados de beta batem com o BG1 e com o npz; z* e K batem com a Fase 9 V1 do proprio um.py; sd_null, sd_tgl, D esperado e o poder analitico sao reproduzidos; o poder MC da ENTREGA esta' dentro do IC95 dela",
                "a funcao de veredito congelada cobre os 6 ramos em vetores deterministicos; a cabeca do ramo de 5 sigma e' a leitura (beta_TGL provado na natureza (validade, não creditação) a n sigma); a palavra do livro de cobrancas vai no campo outcome",
                "nenhum vetor observado e' lido nem procurado; o poder e' prospectivo e sintetico; o gate e' o mesmo da v409 selada; nenhuma chave antiga muda"],
        "nao_diz": ["que o teste tenha sido aberto ou que exista desvio observado: " + Q + "; a abertura e' de versao futura, com a covariancia fisica fechada",
                    "que beta_TGL esteja provado na natureza: o ramo da leitura e' PRE-REGISTRADO, nao devolvido; so' a abertura futura pode devolve-lo; e provado na natureza (validade, não creditação) nunca e' TGL confirmada (creditacao: o juizo de fora, que o um.py nao da)",
                    "que a rota “coerencia espectro x fotometria” seja o teste: e' NOT_TESTABLE (eta = 1)", "que a aritmetica do agregado publico seja resultado: nao e', nao e' cega e nao entra em texto",
                    "que o poder prospectivo seja medida da natureza, ou poder certificado: e' da covariancia publicada, que nao aceita o vetor real, e condicional ao modelo de covariancia publicado; o certificado, as cegas, sob a covariancia fisica, nao existe hoje (D96)", "que o gate tenha se movido: nao se moveu"],
        "extras": {"moldura_pt": DL.FRASE_DA_MOLDURA_H0DN_PT, "moldura_en": DL.FRASE_DA_MOLDURA_H0DN_EN, "obrigatoria_pt": DL.FRASE_H0DN_OBRIGATORIA_PT, "obrigatoria_en": DL.FRASE_H0DN_OBRIGATORIA_EN, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76", "D96")}, "erratas": [DL.ERRATA_E30, DL.ERRATA_E34], "poder_pt": DL.FRASE_H0DN_PODER_PT, "poder_en": DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True), "retorno_pt": DL.FRASE_H0DN_RETORNO_PT, "retorno_en": DL.FRASE_H0DN_RETORNO_EN, "ordem_kimi_03b": dict(DL.H0DN_ORDEM03B, citado_nao_embutido=True, em_rito_nada_e_lido=True),
                   "leituras_do_operador": {k_: DL.LEITURA_V410[k_] for k_ in ("as_decisoes_de_09nov", "a_leitura_do_5sigma", "o_selo_diz_beta_tgl_provado", "o_teste_sem_poder_preditivo_nao_se_roda")}, "assinatura_das_erratas": DL.ASSINA, "regra_do_4_44": DL.REGRA_DO_4_44},
    }
