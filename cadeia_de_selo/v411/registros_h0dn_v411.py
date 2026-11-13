# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] os dados do registro com FUNCAO da v411 (DESENHO_v411 secao 2): H0DN x BG1 aberto uma vez; o resultado recalculado no rito.
"""registros_h0dn_v411.py -- o CONTRATO, o TEXTO e os INSUMOS EMBUTIDOS (base64, pinados por sha256 LIDO) do registro h0dn_bg1_v411 (gerar_candidato_v411.py os emite com runtime_h0dn_v411.py). Nada digitado: a lista dos
insumos, os citados e os textos das checagens sao LIDOS do DESENHO_v411 (delta_v411) e conferidos contra os arquivos; os papeis dos pinos sao casados pelos NOMES dos arquivos dos PINOS_DE_PRODUCAO.json; a ordem dos modulos e' a
do executor pinado (lida do texto dele); os esperados do recalculo (ramos, numero de pares de coerencia, grade B, ancoras, modelos) sao LIDOS do resultado embutido e do estimador S0; beta nunca literal (runtime, _v398_beta).
Os dois insumos de REUSO (o estimador congelado e o BG1) nao sao duplicados: o um.py os le do blob que a v410 ja' embute (_V410_H0DN_INSUMOS), conferido aqui pelo MESMO sha256. Veto herdado: nada da pasta do Kimi entra como pino."""
import base64, hashlib, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402

sha256 = lambda b: hashlib.sha256(b).hexdigest()
_rb = lambda p: open(p, "rb").read()
NOME_DO = {"pinos": "PINOS_DE_PRODUCAO.json", "resultado": "RESULTADO_DA_ABERTURA_V411.json", "pre_registro": "EMENDA_E_PRE_REGISTRO_V411.md", "rede": "network.npz", "congelado": "estimator_frozen.npz",
           "s0": "estimador_s0_v411.npz", "bg": "BG1.json", "readme": "README.md", "ramos": "RAMOS_V411.json", "vetor": "vetor_y255.npz", "recibo_publicacao": "RECIBO_PUBLICACAO_20261112_074508.json",
           "recibo_publicacao_resultado": "RECIBO_PUBLICACAO_RESULTADO_20261112_075315.json", "pre_voo": "PRE_VOO_DA_ABERTURA_V411.json", "recibo_abertura": "RECIBO_DA_ABERTURA_V411.json", "esperado": "ESPERADO_PELOS_AGREGADOS.json"}
assert set(NOME_DO.values()) | {"estimator_v411.py", "veredito_v411.py", "abertura_v411.py"} == set(DL.INSUMO_POR_NOME), "os papeis do registro nao cobrem exatamente os 18 insumos do DESENHO"
_PALAVRAS = {"dois": 2, "tres": 3, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "treze": 13}


def _do_desenho(rx_, chk_):
    m_ = re.search(rx_, DL.CHECAGENS_DO_DESENHO[chk_]); assert m_, ("o DESENHO nao traz o que a checagem precisa", chk_, rx_)
    return m_.group(1)


def insumos_embutidos(insumos_v410):
    """{nome: {'b64', 'sha256', 'bytes', 'rel'} | {'reuso_v410': nome, 'sha256', 'bytes', 'rel'}} -- os bytes LIDOS dos arquivos do DESENHO; os de reuso apontam o blob da v410 (sha256 conferido contra o contrato da v410)."""
    out = {}
    for i_ in DL.INSUMOS_V411:
        b = _rb(i_["arquivo"]); assert sha256(b) == i_["sha256"]
        if i_["reuso_v410"]:
            p_ = (insumos_v410 or {}).get(i_["nome"])
            assert isinstance(p_, dict) and p_.get("sha256") == i_["sha256"] and p_.get("bytes") == len(b), ("o blob da v410 nao tem o mesmo sha256: nao posso reusar", i_["nome"])
            out[i_["nome"]] = {"reuso_v410": i_["nome"], "sha256": i_["sha256"], "bytes": len(b), "rel": i_["rel"]}
        else:
            out[i_["nome"]] = {"b64": base64.b64encode(b).decode("ascii"), "sha256": i_["sha256"], "bytes": len(b), "rel": i_["rel"]}
    return out


def _ordem_dos_modulos():
    exe_ = [c_ for c_ in DL.CITADOS_V411 if c_["nome"] == "executar_abertura_v411.py"][0]
    t_ = _rb(exe_["arquivo"]).decode("utf-8")
    m_ = re.search(r"def carregar_codigo\(codigo_raw\):.*?for nome in \(([^)]*)\):", t_, re.S); assert m_
    return [x_.strip().strip('"') for x_ in m_.group(1).split(",") if x_.strip()], exe_


def contrato_h0dn_v411(core0, selo0, c410, base_sha256):
    """O contrato do registro h0dn_bg1_v411, DERIVADO dos arquivos (pinos lidos), do DESENHO (delta) e do core/selo/contrato da v410 selada (o gate, a escada, a tolerancia de K, o veredito antigo a repetir)."""
    P = {k_: DL.INSUMO_POR_NOME[v_]["arquivo"] for k_, v_ in NOME_DO.items()}
    pinos = json.loads(_rb(P["pinos"]).decode("utf-8")); res = json.loads(_rb(P["resultado"]).decode("utf-8"))
    pmap = {}
    for campo_ in ("rede", "congelado", "s0", "bg", "readme", "ramos", "pre_registro", "vetor"):
        nm_ = os.path.basename(pinos[campo_]["path"].replace("\\", os.sep))
        assert nm_ in DL.INSUMO_POR_NOME and DL.INSUMO_POR_NOME[nm_]["sha256"] == pinos[campo_]["sha256"], ("o pino de producao nao casa um insumo embutido", campo_, nm_)
        pmap[campo_] = nm_
    ordem, exe_ = _ordem_dos_modulos()
    assert ordem == ["estimator_v411.py", "veredito_v411.py", "abertura_v411.py"] and all(DL.INSUMO_POR_NOME[o_]["sha256"] == pinos["codigo"][o_] for o_ in ordem)
    assert pinos["codigo"]["executar_abertura_v411.py"] == exe_["sha256"], "o executor citado pelo DESENHO nao e' o dos pinos de producao"
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict")
    E410 = int(core0["external_ladder"]["n_theorems_expected"]); assert E410 == int(core0["external_ladder"]["n_theorems_clean"])
    v410v = (core0.get("h0dn_bg1_v410") or {}).get("values") or {}
    assert isinstance(v410v.get("K"), float) and (core0.get("h0dn_bg1_v410") or {}).get("all_verified") is True, "o registro h0dn_bg1_v410 da base nao selou com K"
    s0_ = __import__("numpy").load(io.BytesIO(_rb(P["s0"])), allow_pickle=False)
    modelos = [str(x_) for x_ in s0_["model_names"]]; ancoras = [str(x_) for x_ in s0_["anchor_names"]]
    r_ = res["resultado"]
    grade_B = sorted(float(k_[2:]) for k_ in r_["estresse"]["iii_vies_por_hospedeira"] if re.fullmatch(r"b_[0-9.]+", k_))
    n_pares = len(r_["coerencia"]); assert n_pares == _PALAVRAS[_do_desenho(r"os (\w+) pares de coer[êe]ncia", "c9")]
    n_pv = int(_do_desenho(r"os (\d+) arquivos pinados do pr[ée]-voo", "c3"))
    estado = _do_desenho(r"o estado `([A-Z_]+)`", "c2")
    m168 = re.findall(r"`(__[A-Z0-9_]+)`", DL.DECISOES_V411["D168"]); assert len(m168) == 2, m168
    bg1 = json.loads(_rb(P["bg"]).decode("utf-8"))
    assert c410["tolerancias"]["K"] == DL.TOL_K
    m_faixa = re.search(r"(<faixa[^>]*>)", DL.VEREDITO_MEIO_MOLDE); assert m_faixa
    assert pinos["saida"]["path"].replace("\\", os.sep).endswith(NOME_DO["resultado"]) and res["pre_registro"]["sha256"] == pinos["pre_registro"]["sha256"]
    assert "kimi" not in json.dumps([i_["arquivo"] for i_ in DL.INSUMOS_V411]).lower().replace("ordem_ao_kimi", ""), "veto: nenhum insumo da pasta do Kimi"
    return {"registro": DL.FECHO_REGISTRO, "tag": DL.TAG_FECHO, "n_checks": DL.N_CHECKS_FECHO, "checagens": dict(DL.CHECAGENS_DO_DESENHO), "mecanica": DL.MECANICA_NOME,
            "veredito_ok_prefixo": DL.VEREDITO_OK_PREFIXO, "veredito_meio_molde": DL.VEREDITO_MEIO_MOLDE, "veredito_sufixo": DL.VEREDITO_SUFIXO, "veredito_recusa": DL.VEREDITO_RECUSA, "marcador_da_faixa": m_faixa.group(1), "prefixo_da_faixa": DL.PREFIXO_DA_FAIXA,
            "insumos": {i_["nome"]: {"sha256": i_["sha256"], "bytes": i_["bytes"], "rel": i_["rel"], "papel": i_["papel"], "reuso_v410": bool(i_["reuso_v410"])} for i_ in DL.INSUMOS_V411},
            "nomes": dict(NOME_DO), "pinos_por_campo": pmap, "ordem_dos_modulos": ordem, "executor": {"nome": exe_["nome"], "sha256": exe_["sha256"], "bytes": exe_["bytes"], "so_como_texto": True},
            "citados": [{"rel": c_["rel"], "nome": c_["nome"], "sha256": c_["sha256"], "bytes": c_["bytes"]} for c_ in DL.CITADOS_V411],
            "pasta_vedada": DL.H0DN_PASTA_VEDADA_V410, "estado_do_pre_registro": estado, "n_pinados_do_pre_voo": n_pv, "convencao_do_vetor": pinos["vetor"]["convencao"],
            "fala_da_ordem_de_abrir": {"quando": DL._quando_da_fala(DL.FALA_ORDEM_V411["nome"]), "sha256": DL.FALA_ORDEM_V411["sha256"], "bytes": DL.FALA_ORDEM_V411["bytes"], "papel": DL.FALA_ORDEM_V411["papel"], "autor": "operador"},   # (D181) so' a citacao: data, sha256, papel e autor; sem o nome do arquivo (carrega as primeiras palavras da fala)
            "modelos": modelos, "ancoras": ancoras, "grade_B": grade_B, "n_pares_de_coerencia": n_pares,
            "esperado_do_resultado": {"ramo_primario": r_["veredito"]["ramo"], "ramo_cefeidas_livres": r_["linha_ao_lado_cefeidas_livres"]["ramo"], "de": "o resultado da abertura embutido (sha256 %s)" % DL.INSUMO_POR_NOME[NOME_DO["resultado"]]["sha256"]},
            "marcas_da_emenda": m168, "tolerancias": {"recalculo": DL.TOL_RECALCULO, "K": c410["tolerancias"]["K"]},
            "lei": {"form": bg1["law"]["form"], "beta_rule": "ALPHA_FINE_CODATA_2018 * sqrt(e), em runtime (nunca literal; _v398_beta)", "parametros_do_fundo_de": "frozen_Omega_m, frozen_Omega_r e z_star do BG1 embutido"},
            "baseline": {"version": DL.BASE_VERSION, "gate_verdict": gate0, "escada": E410, "um_py_sha256": base_sha256, "K_do_registro_v410": v410v["K"], "log10K_do_registro_v410": v410v.get("log10K")},
            "tokens_proibidos_partes": [[t_[:-4], t_[-4:]] for t_ in DL.TOKENS_PROIBIDOS_V411],   # (em PARTES, como na v410: o um.py nunca traz o token inteiro; o runtime os monta)
"contratos_de_registro_fora_da_escada": list(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA),
            "decisoes": dict(DL.DECISOES_V411), "erratas": [dict(e_) for e_ in DL.ERRATAS_V411], "falas": [dict(c_) for c_ in DL.FALAS_CITADAS_V411],   # (D181) citadas por data e sha256 (papel e autor), nao transcritas e sem o nome do arquivo
            "textos_da_gerencia_citados": [{"nome": g_["nome"], "sha256": g_["sha256"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS], "desenho_sha16": DL.DESENHO_SHA16,
            "p2_ao_lado": dict(DL.P2_AO_LADO)}   # (aditivo da gerencia c1, 12/11: o P2 AO LADO da v387; o token selado nao muda)


def texto_h0dn_v411():
    """O texto do registro (estatico no um.py; os NUMEROS sao do recalculo, em values e no veredito). Escrito para passar as duas guardas (P18 e frases da v411): sem a palavra da creditacao, sem “poder certificado”,
    sem o resultado sem as quatro obrigacoes (por isso o texto estatico nao enuncia o Z: o numero so' sai junto da linha das Cefeidas livres, do modelo publicado, da validade e da retrodicao nao cega)."""
    M, V, R, NC, CL = DL.OBRIG_MODELO_PT, DL.OBRIG_VALIDADE_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_CEFEIDAS_PT
    return {
        "estatuto": ("[REAL] o que o registro CONFERE neste rito: os insumos embutidos contra os pinos de producao; a ordem dos atos lida dos recibos (o pre-registro publico antes da abertura); a integridade de desenho do modulo pinado; "
                     "o portao 1 recalculado; o RECALCULO do resultado pela rotina pinada, executada dos bytes embutidos, comparado com o resultado da abertura (numeros a 1e-9, ramos, desfechos e cabecas por igualdade de texto); "
                     "K e log10 K de beta em runtime; a emenda as claras; a guarda de finitude; o esperado pelos agregados relatado ao lado do observado; o gate e a escada da v410. [INPUT] as ordens e ratificacoes do operador de 11 e 12/11 (citadas por data e sha256, nao transcritas) e a cabeca "
                     "do veredito fixada por ele em 09/11. [DECLARADO pelo Kimi] as linhas de estresse S1, S2 e S4, so' como texto do pre-registro, sem numero observado. Retrodicao sem ajuste, com emenda posterior a guarda; teste " + NC + "."),
        "escopo": ("[REAL] O teste pre-registrado da razao de Hubble local/fundo (rede H0DN contra o fundo BG1) foi aberto UMA vez, em 12/11/2026, depois do commit publico do pre-registro; o resultado entra neste registro "
                   "RECALCULADO a partir dos bytes embutidos (o codigo publicado antes da abertura; nada transcrito). A LEI: K = E(z*)^(2 beta/3), beta = alfa sqrt e em runtime, z* e os Omegas do fundo congelado, zero parametro livre. "
                   "AS DUAS LINHAS saem juntas, sempre: o primario, " + M + ", e ao lado, no mesmo item, as " + CL + " (linha ao lado, nao e' veredito). A EMENDA (D162): o ramo (1) deixou de recusar o vetor fora do suporte e passou a ser "
                   "o portao 1; pela funcao congelada da v410 o desfecho seria o ramo (1), e o registro o diz. " + DL.FRASE_SUPORTE_PT + ". Provado, aqui, e' " + V + "; o gate nao se move."),
        "limites": ["[REAL] " + DL.FRASE_SEM_PODER_CERTIFICADO_PT, "[REAL] " + DL.FRASE_ESPECIFICIDADE_PT,
                    "[OPEN] se o orcamento de erros publicado esta' certo: o resultado vale sob ele; a covariancia fisica conjunta segue aberta (o recibo HMS/13 da v410 e' cobertura de fontes)",
                    "[OPEN] a independencia entre a medida local e o fundo e' hipotese nomeada; o cruzamento adverso e' linha de estresse",
                    "[REAL] a creditacao e' ato de quem observa de fora; o um.py nao a da; o gate nao se move"],
        "diz": ["o resultado da abertura e' RECALCULADO a cada rito pela rotina pinada, a partir dos bytes embutidos, e conferido contra o resultado gravado na abertura (sha256 no contrato)",
                "as duas linhas saem juntas em values e no veredito de maquina: o primario, " + M + ", e as " + CL + " ao lado, no mesmo item, cada uma com o seu ramo",
                "a emenda as claras: o que a regra antiga daria com os mesmos Z, que o literal novo so' difere do antigo pela marca, e que os ramos 2 a 6 sao os mesmos da v410",
                "o esperado pelos agregados publicos (" + R + " sem ajuste, teste " + NC + ") vai ao lado do observado, linha a linha; e' relato, nao portao",
                "as sete ressalvas da secao 8 do pre-registro, lidas do texto embutido; o gate e a escada sao os da v410"],
        "nao_diz": ["que a creditacao tenha sido dada: ela e' de quem tem autoridade para creditar; " + V,
                    "que o teste seja cego: e' " + R + " sem ajuste, com emenda posterior a guarda; nao e' cego",
                    "que o numero seja novo: o primario era previsivel por dois agregados publicos; o rito conferiu a conta",
                    "que haja independencia das Fases 4, 5 e 9: nao ha; nao e' evidencia independente delas (os dados locais se sobrepoem)",
                    "que a covariancia fisica conjunta esteja fechada ou que o orcamento de erros publicado esteja certo", "que o gate tenha se movido: nao se moveu"],
        "nao_decide": list(DL.NAO_DECIDE_RESUMO_PT),
        "ressalvas": ["o primario nunca aparece sem a linha das " + CL + " no mesmo item, sem a frase do modelo publicado, sem " + R + " e sem nao cego (DESENHO secao 4)",
                      "as tres linhas de covariancia S1, S2 e S4 do Kimi entram so' como texto do pre-registro [DECLARADO pelo Kimi], sem numero observado; nada da pasta do Kimi e' lido em rito",
                      "beta entra so' por nome (alfa CODATA 2018 x sqrt e em runtime), nunca literal",
                      "E41 (gerencia c1, em nome proprio): o docstring do veredito pinado poe a centragem no portao 1; vale o texto do pre-registro e o codigo de abrir; o modulo pinado nao e' tocado",
                      "E42 (gerencia c1, em nome proprio): o colchete da regra do nome em duas linhas da v410 le-se definicao e nome do operador; o texto selado da v410 nao e' reescrito",
                      "E43 (gerencia c1, em nome proprio): as seis aberturas da secao da Escala, no texto selado da v410, leem-se por definicao e nome do operador; nao sao trocadas na renderizacao (o artigo nao diverge do registro selado); a errata vai ao lado"],
        "extras": {"decisoes": dict(DL.DECISOES_V411), "erratas": [dict(e_) for e_ in DL.ERRATAS_V411], "assinatura_das_erratas": DL.ASSINA,
                   "alcance_de_p_igual_np": "P = nP " + DL.D10.FRASE_QUALIFICADOR_PT + " (D64 e D84 da v410, que valem na v411; a pergunta do Clay, tal qual apresentada pela TGL; a creditação é do Clay)",
                   "obrigatorias_pt": [DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_VALIDADE_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT],
                   "obrigatorias_en": [DL.OBRIG_MODELO_EN, DL.OBRIG_CEFEIDAS_EN, DL.OBRIG_VALIDADE_EN, DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_EN],
                   "rotulos_das_sete_ressalvas": list(DL.RESSALVAS_ROTULOS_PT)},
    }
