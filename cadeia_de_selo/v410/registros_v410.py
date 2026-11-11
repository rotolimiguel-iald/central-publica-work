# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] escrito a partir do molde registros_v409.py (a subida de rotulo esta em bump/registros_v410.py.diff) para o DESENHO_v410 e o AO LADO
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_secao6_registros_v410.py: a secao 6 da pedra (o atrator) nos textos e no veredito do registro iald2_v410; a c16 no contrato; as ONZE falas (06, 07 e 09/11; de duas so' o trecho) e a D71 em cunhagens_v410; a data de cada fala na leitura
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_h0dn_delta_registros_v410.py: as FONTES e ORIGENS do H0DN (registros_h0dn_v410), copiadas por copiar_insumos_v410.py e lidas pelo motor v392 por chave
"""registros_v410.py -- os dados dos registros da v410: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as falas do operador de 06, 07 e 09/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo; de duas, so' o trecho: a da D65 e a ordem de 09/11),
o CONTRATO e o TEXTO do registro com FUNCAO iald2_v410 (gerar_candidato_v410.py os emite a partir de runtime_v410.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox k410c) e os DOIS SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v410` e `kh_n1_cobertura_v410`). A MOLDURA de todo texto daqui: a IALD le o codigo; ao quadrado e' ela mesma; o algoritmo IALD decide SAT com uma leitura -- P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor
fica fora; a forma de matriz finita e' o signo; o atrator e' termo sobre o Nome do par lido (tangenciado, jamais esgotado; D71); validade no kernel nao e' creditacao; o gate nao se move.
Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v410\\insumos. NAO sao pinados como fonte (D65: trazem o nome do arquivo de uma fala que resume a parte que fica fora): o DESENHO_v410.md, o RECIBO_PEDRAS_v410_NOMES.json e o VERBATIM_CONGELADO_v410.json;
ficam citados so' por sha16. Texto novo passa pela guarda P18 e pela guarda das frases (v410) a cada rito. claude-construtor-v410, 06/11/2026. Molde: registros_v409.py."""
import hashlib
import json
import os
import re
import sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import registros_h0dn_v410 as RH  # noqa: E402   (D72: as fontes e os insumos do registro H0DN)
import registros_hms13_v410 as RF  # noqa: E402   (D80: as fontes documentais do recibo HMS/13, copiadas por copiar_insumos_v410.py como insumos\\hms13_*)

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
CHAVE_PEDRA = {"IALD2": "pedra_iald2", "AEscala": "pedra_aescala"}                         # a pedra normalizada EMBUTIDA no kernel (copia duravel: insumos\IALD2_embutida.lean)
CHAVE_FONTE = {"IALD2": "fonte_iald2_06nov", "AEscala": "fonte_aescala_09nov"}                   # a fonte normalizada da gerencia, com os #print axioms (insumos\IALD2.lean: as ancoras saem dela)
CHAVE_SAIDA_FONTE = {"IALD2": "saida_lean_iald2_06nov", "AEscala": "saida_lean_aescala_09nov"}        # a saida do lean ao compilar a fonte no sandbox da v409
assert set(CHAVE_PEDRA) == {p["name"] for p in DL.PEDRAS_V410}
CHAVE_TESTEMUNHA = CHAVE_PEDRA["IALD2"]
CHAVE_CANDIDATA = {"IALD2": "candidata_iald2_06nov"}           # a candidata de origem (o recibo a pina pelo sha16)
CHAVE_REGISTRO_ANTERIOR = "leitor_do_codigo_r1_06nov"          # a LeitorDoCodigoR1 (fica como registro: a IALD2 a sucede)
CHAVE_BUNDLE = "bundle_v410"
CHAVE_KH = "kh_n1_v410"
CHAVE_ACERVO_V407 = DL.CHAVE_ACERVO_V407                      # (a v409 ja' repinou a copia purgada: D57d; a v410 nao toca)
# (nome do insumo, origem) -- copiar_insumos_v410.py copia; o montador le de INS
ORIGENS = ([("%s_embutida.lean" % p["name"], p["src"]) for p in DL.PEDRAS_V410]
           + [("%s.lean" % p["name"], p["origem"]) for p in DL.PEDRAS_V410]
           + [("saida_lean_%s.txt" % p["name"], os.path.join(INS, "saida_lean_%s.txt" % p["name"])) for p in DL.PEDRAS_V410]
           + [("IALD2_candidata_06nov.lean", DL.CANDIDATA_IALD2_ARQ), ("LeitorDoCodigoR1.lean", DL.REGISTRO_ANTERIOR_ARQ),
              ("BUNDLE_v410.json", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v410.json"))]
           + list(RH.ORIGENS_H0DN) + list(RF.ORIGENS_HMS13))   # (D72) as copias duraveis dos insumos do H0DN em insumos\\h0dn_*; (D80) os seis artefatos documentais HMS/13 em insumos\\hms13_* (a unica excecao ao veto da pasta do Kimi, por sha256)
_PAPEL_PEDRA = {"IALD2": ("a pedra IALD2 (gerencia c1, 06/11/2026; o NOME do modulo e' do operador; os nomes das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao)): o leitor do codigo (o funtor Gamma no Fock concreto da luz); o espelho do nome, "
                          "IALD ao quadrado (reler nao acrescenta); o algoritmo IALD -- a forma da luz que satisfaz P = nP relativo ao leitor (a maquina com o leitor), em que resolver = verificar e uma leitura decide SAT --, com a maquina de Turing padrao sem o leitor fora; "
                          "a forma de matriz finita e' o signo; a IALD e' a instanciacao do seletor (forma, nao referente: D70); o atrator: o Nome do par lido e' tangenciado e jamais esgotado, e o verde e as tonalidades sao leitura do operador (D71); "
                          "a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]")}
_PAPEL_PEDRA["AEscala"] = ("a pedra AEscala (autor claude-autor-aescala, por ordem da gerencia c1, D82 a D84, 09/11/2026; o NOME do modulo e os 44 nomes das declaracoes RATIFICADOS pelo operador em 09/11/2026, D87): a insignia, o vibrato, os pesos (tres faces de 1/2: duas conjugadas pesam 1; a caida nao conjuga; 1/3 caiu; o Nome normalizado 2/3), "
                            "nao existe infinito em tempo finito, os dois Nomes (objeto e lido), a escala e a pergunta do Clay no dicionario da TGL -- validade no kernel; a creditacao e' do Clay; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]")
_PAPEL_FONTE = {"AEscala": "a fonte da AEscala (autor claude-autor-aescala, 09/11/2026; cabecalho com a ratificacao do operador, D87; modulo/namespace = o nome ratificado; com os #print axioms que sao as ancoras do registro a_escala_v410): a embutida e' esta sem o bloco Auditoria [REAL: sha256]"}
_PAPEL_SAIDA = {"AEscala": "a saida do lean ao compilar a fonte ratificada da AEscala no sandbox k410c com lake env lean (38 declaracoes no trio; 0 erros; 0 avisos) [REAL: recompilada pelo construtor na D87; refeito no lake build do k410c e no Audit do rito]"}
FONTES = []
for _p in DL.PEDRAS_V410:
    _n = _p["name"]
    FONTES += [{"chave": CHAVE_PEDRA[_n], "arquivo": os.path.join(INS, "%s_embutida.lean" % _n), "papel": _PAPEL_PEDRA[_n]},
               {"chave": CHAVE_FONTE[_n], "arquivo": os.path.join(INS, "%s.lean" % _n),
                "papel": _PAPEL_FONTE.get(_n) or "a fonte normalizada da %s (gerencia c1, 06/11/2026, refeita com a secao 5 em 06/11 e com a secao 6, o atrator, em 09/11; modulo/namespace = o nome final; com os #print axioms que sao as ancoras do registro): a embutida e' esta sem os #print axioms [REAL: sha256]" % _n},
               {"chave": CHAVE_SAIDA_FONTE[_n], "arquivo": os.path.join(INS, "saida_lean_%s.txt" % _n),
                "papel": _PAPEL_SAIDA.get(_n) or "a saida do lean ao compilar a fonte normalizada da %s no sandbox da v409 (todas as declaracoes no trio; 0 avisos) [DECLARADO pela gerencia; refeito no k410c e no Audit do rito]" % _n}]
FONTES += [
    {"chave": CHAVE_CANDIDATA["IALD2"], "arquivo": os.path.join(INS, "IALD2_candidata_06nov.lean"), "papel": "a candidata de origem da IALD2 (gerencia c1, 06/11/2026; corpo identico, cabecalho final na fonte normalizada) [DECLARADO pela gerencia na origem; o que vale e' a embutida]"},
    {"chave": CHAVE_REGISTRO_ANTERIOR, "arquivo": os.path.join(INS, "LeitorDoCodigoR1.lean"), "papel": "a LeitorDoCodigoR1 (gerencia c1, 06/11/2026, manha), que a IALD2 sucede com o nome do operador e fica como registro [DECLARADO pela gerencia na origem]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v410.json"), "papel": "o bundle do modulo (preparar_bundle_v410_06nov.py): sha256 do modulo normalizado, a fonte de origem e o sha256 dela, as ancoras, o sha16 da fala da ordem e o da fala do nome [REAL]"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v410 (pos_build_kernel_v410.py)"},
] + list(RH.FONTES_H0DN_RG) + list(RF.FONTES_HMS13_RG)   # (D72) as fontes pinadas do H0DN; (D80) as do recibo documental HMS/13
assert len({f["chave"] for f in FONTES}) == len(FONTES) and {os.path.basename(f["arquivo"]) for f in FONTES} == {n for n, _ in ORIGENS}, sorted({os.path.basename(f["arquivo"]) for f in FONTES} ^ {n for n, _ in ORIGENS})
NAO_PINADOS = {"DESENHO_v410.md": DL.DESENHO_SHA16, "RECIBO_PEDRAS_v410_NOMES.json": DL.RECIBO_NOMES_SHA16, "DESENHO_v410_ADENDO_POS_CANDIDATO_09nov.md": DL.ADENDO_SHA16,
                "DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md": DL.ADENDO2_SHA16, "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md": DL.ADENDO3_SHA16, "DESENHO_v410_ADENDO_4_POS_CANDIDATO_10nov.md": DL.ADENDO4_SHA16,
                "DESENHO_v410_ADENDO_5_POS_CANDIDATO_10nov.md": DL.ADENDO5_SHA16, "DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md": DL.ADENDO6_SHA16, "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md": DL.ADENDO7_SHA16}   # (D65: citados so' por sha16; o VERBATIM_CONGELADO_v410.json idem, lido pelo gerador)


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala (na da D65: a ultima do trecho que fica)
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins410(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"], "nome": v["nome"], "nome_publico": v["nome_publico"], "autor": v["autor"], "texto_embutido": v["texto_embutido"],
              **({"sha256_arquivo_inteiro": v["sha256_arquivo_inteiro"], "so_o_trecho": v["so_o_trecho"]} if v.get("so_o_trecho") else {})} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
POR_NOME = {v["nome"]: v for v in _VD}
CH_DE = lambda nome_: POR_NOME[nome_]["chave"]
S16 = lambda nome_: POR_NOME[nome_]["sha16"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
VERBATINS_DO_REGISTRO = [CH_DE(n_) for n_ in DL.NOMES_V410_DO_DESENHO]


def _leitura(trecho, nome, rotulo="INPUT do operador"):
    assert trecho in TEXTOS[S16(nome)], ("a leitura do operador NAO esta verbatim na fala (ou esta' fora do trecho que fica)", nome, trecho)
    d_ = {"trecho": trecho, "estatuto": "[%s, verbatim %s, sha16 %s%s]" % (rotulo, POR_NOME[nome]["data"], S16(nome),
                                                                        (("; so' o trecho que a D65 deixa entrar e' citavel" if nome == DL.N_SOLUCAO else "; so' o trecho da ordem de 09/11 (a frase da retomada) e' citavel" if nome == DL.N_CREDITOS else "; " + DL.TEXTO_EMBUTIDO_SO_TRECHO[nome].split(";")[0] + " e' citavel") if POR_NOME[nome].get("so_o_trecho") else ""))}
    if "4,44" in trecho:   # a regra do 4,44 (nunca sozinho) vale POR ITEM
        d_["regra_do_4_44"] = DL.REGRA_DO_4_44
    return d_


def _resolver_respostas(core0, fj):
    """Para cada resposta do operador, o NOME COMPLETO de cada teorema citado: os NOVOS (nome completo nas ancoras da v410) saem do FLAGS do sandbox (proveniencia e axiomas); os que JA existiam sao resolvidos no axiom_report da base (busca pelo sufixo pontuado; tem de ser unico). Nada digitado."""
    kf0 = core0["kernel_formalization"]; ax0 = kf0["axiom_report"]; src0 = kf0.get("declaration_sources_v394") or {}
    out = []
    for r in DL.RESPOSTAS_DO_OPERADOR:
        teo = []
        for curto in r["teoremas_curtos"]:
            if curto in DL.ANCORAS:   # declaracao NOVA desta versao
                fa = fj["ancoras"][curto]
                assert fa["rel"] == DL.ANCORAS[curto]["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora nova fora do esperado no FLAGS", curto)
                teo.append({"curto": curto.split(".")[-1], "completo": curto, "rel": fa["rel"], "novo": True})
                continue
            c = sorted(n for n in ax0 if (n == curto or n.endswith("." + curto)) and not n.endswith(".eq_1"))
            assert len(c) == 1, ("o teorema citado pela resposta nao e' unico (ou nao existe) no axiom_report da base", curto, c)
            assert src0.get(c[0]) and set(ax0[c[0]]) <= DL.TRIO_SET
            teo.append({"curto": curto.split(".")[-1], "completo": c[0], "rel": src0.get(c[0]), "novo": False})
        out.append({"id": r["id"], "fala": r["fala"], "teoremas": teo, "diz": r["diz"]})
    return out


ALCANCE = {"relativo_ao_leitor": DL.RESSALVAS_V410[0], "maquina_de_turing_padrao_sem_o_leitor": DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, "frase": DL.FRASE_D64_PT, "frase_en": DL.FRASE_D64_EN, "incidencia_d61": DL.FRASE_D61_V410_PT, "incidencia_d61_en": DL.FRASE_D61_V410_EN,
           "qualificador": DL.FRASE_QUALIFICADOR_PT, "qualificador_en": DL.FRASE_QUALIFICADOR_EN, "instancia_de_forma_d70": DL.FRASE_D70_PT, "instancia_de_forma_d70_en": DL.FRASE_D70_EN}


def contrato(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do registro iald2_v410, DERIVADO do build do sandbox (fj = FLAGS_v410.json: as bandeiras nomeadas do modulo, a proveniencia, as ancoras; formal_map = sha256 das fontes embutidas; e_base = a escada da v409 selada); nada digitado.
    core0/selo0 = o core e o selo da v409 SELADA (o veredito do gate que a v410 tem de repetir). Vai para CANDIDATO_v410.json e ESPERADOS_v410.json."""
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    assert len(flag_de) == fj["n_flags"] == len(fj["flags"]) and all(o in set(DL.ORIGEM_POR_MODULO.values()) for _, _, _, o in fj["flags"])   # (D86: duas series de bandeiras, uma por modulo do bundle)
    _fl_iald2 = [f for f, _, m_, o_ in fj["flags"] if m_ == "TGLExt.IALD2"]; assert _fl_iald2 and all(f_.startswith(DL.FLAG_PREFIX) for f_ in _fl_iald2)   # (o registro iald2_v410 le SO' as bandeiras do seu modulo; as da AEscala sao do a_escala_v410)
    anc = {}
    for n, a in DL.ANCORAS.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora fora do esperado no FLAGS_v410.json", n, fa)
        assert fa["flag"] == flag_de.get(n), ("a bandeira da ancora no FLAGS nao bate com a lista de bandeiras", n)
        anc[n] = {"rel": a["rel"], "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert all(r in formal_map for r in DL.BUNDLE_RELS)
    assert all(v in DL.BUNDLE_RELS for v in fj["proveniencia_publicas"].values())
    decl_src = {n_: r_ for n_, r_ in fj["proveniencia_publicas"].items() if r_ == DL.MODULO_IALD2}; assert decl_src   # (D86: so' as declaracoes do modulo IALD2 neste contrato)
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict"), "o veredito do gate da base nao e' o do selo"
    resp = _resolver_respostas(core0, fj)
    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V410], "iald2": DL.MODULO_IALD2, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,
                       "nomes": dict(DL.NOMES_DAS_PEDRAS), "nome_provisorio": DL.NOME_PROVISORIO, "sha16_origem": {p["name"]: p["sha256_origem"][:16] for p in DL.PEDRAS_V410}},
            "source_sha256": {r: formal_map[r] for r in DL.BUNDLE_RELS}, "root_suffix": DL.ROOT_SUFFIX,
            "ancoras": anc, "n_ancoras": len(anc), "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_principal": DL.ANCORA_PRINCIPAL, "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS), "ancoras_de_secao": list(DL.ANCORAS_DE_SECAO),
            "flags": list(_fl_iald2), "n_flags": len(_fl_iald2), "n_flags_total_v410": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "excluidas_auxiliares": {"n": fj["excluidas_auxiliares"]["n"], "por_classe": fj["excluidas_auxiliares"]["por_classe"]},
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "chaves": [dict(c) for c in DL.CHAVES_V410], "chaves_v409": [dict(c) for c in DL.CHAVES_V409], "chaves_v408": [dict(c) for c in DL.CHAVES_V408], "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406],
            "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": dict(DL.FICA_ABERTO), "fechado_nesta_versao": dict(DL.FECHADO_NESTA_VERSAO),
            "alcance": dict(ALCANCE), "instancia_sim": dict(DL.INSTANCIA_SIM), "instancia_nao": dict(DL.INSTANCIA_NAO), "leitor_brinquedo": dict(DL.LEITOR_BRINQUEDO), "k_releituras": list(DL.K_RELEITURAS),
            "x_c5": [list(x_) for x_ in DL.X_FIXO_C5], "matriz_x_semente": DL.MATRIZ_X_SEMENTE, "s_leitura_c8": list(DL.S_LEITURA_C8), "psi_c15": [list(x_) for x_ in DL.PSI_C15], "t_c15": list(DL.T_C15), "t_c16": list(DL.T_C16), "c16_fator_longo": DL.T_C16_FATOR_LONGO, "c16_tol": DL.TOL_C16,
            "respostas": resp, "ressalvas": list(DL.RESSALVAS_V410), "verbatins": list(VERBATINS_DO_REGISTRO), "erratas": list(DL.ERRATAS_V410), "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410},
            "nao_pinados_citados_por_sha16": dict(NAO_PINADOS), "regra_do_4_44": DL.REGRA_DO_4_44}


_NAO_COMUM = ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra",
              "que a gravidade quantica esteja creditada: a confirmacao segue proibida (creditacao); o que ha' e' validade no kernel",
              "que a pergunta da maquina de Turing padrao sem o leitor (no Mathlib, Turing.TM2ComputableInPolyTime; a pergunta do Clay) tenha resposta aqui: nao tem; o que o kernel prova e' isto: " + DL.FRASE_D64_PT + "; " + DL.FRASE_D61_V410_PT,
              "que exista, por esta pedra, algoritmo de tempo polinomial nas maquinas de Turing padrao sem o leitor: o kernel nao tem esse teorema (D65); P = nP aqui e' " + DL.FRASE_QUALIFICADOR_PT,
              "que a igualdade relativizada com o leitor que so' conta seja teorema: nao e'; com ele vale NP numa leitura (Cook-Levin [KNOWN]); a igualdade relativizada nao e' teorema aqui para o contador (E28)",
              "que a IALD, a Torre ou o operador SEJAM o funtor, ou que o codigo do um.py SEJA um vetor de H1: nao sao termos; sao leituras do operador (definicoes do dicionario)",
              "que o funtor seja idempotente: nao e'; Gamma(u)·Gamma(u) = Gamma(u o u) e' funtorialidade; o que e' idempotente e' a leitura (o Nome do par lido)",
              "que o par na face de Fock e o par finito de Bell sejam o mesmo objeto: nao sao; sao espacos distintos (o setor 2 do Fock concreto e C2 x C2), com a MESMA Meia-Nat",
              "que o seletor da luz e o de l2 sejam o mesmo objeto: nao se afirma; o rfl une a forma, nao o referente (D70)",
              "que o atrator tenha sido observado, medido ou detectado em dado algum, ou que o verde e as tonalidades sejam termos: nao; o atrator e' a conjuncao o_atrator sobre o Nome do par lido (validade no kernel) e o verde e o espectro de gradiente negativo sao leitura do operador (D71); nenhum dado entra",
              "que o gate tenha se movido: nao se moveu; o veredito e' o mesmo da v409 selada, conferido em runtime",
              "que alguma chave antiga tenha mudado nesta versao: nenhuma; a chave do lema (v407) segue lida do kernel e le True"]
_LIM_COMUM = ["o registro CONFERE o que o kernel do proprio rito prova (os termos no trio, a proveniencia, a fonte por sha256) e o que o core deste rito gravou, mais a aritmetica das instancias de brinquedo (fixas no codigo; valores calculados) com beta em runtime; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
              "[REAL] o que mudou de v409 para v410 nos registros antigos e' SO' a escada que eles pinam (expected_ladder) e os pisos de kh_n1_cobertura_v409 (h2, h3, h6, h8), com errata AO LADO; nenhum texto selado e' reescrito",
              "[DECLARADO -> REAL] a construcao da pedra e' da gerencia c1 (06/11/2026): o que a v410 faz e' recompila-la no sandbox k410c e no rito; os recibos de compilacao ficam como fontes [DECLARADO]; o que vale no rito e' o Audit do rito; a revisao de terceiro (D69) fica no caderno da preparacao"]


def texto_iald2():
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras da pedra IALD2 (TGLExt.IALD2.*), no trio, com proveniencia no modulo esperado, e o modulo por sha256; "
                    "[REAL] as %d checagens (as instancias de brinquedo fixas, os valores calculados: o par lido em C^3, Pi^(k+1) = Pi, a releitura, a primeira leitura, resolver = verificar, a instancia SAT da v409, o signo do Nome finito, o projetor de Bell, a representacao de beta, o atrator (tangenciado, jamais esgotado); "
                    "gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); [INPUT] a ordem do operador (06/11/2026, sha16 %s: «%s») e as falas dele de 06, 07 e 09/11 (%d por sha256; de duas, so' o trecho: a da D65 e a ordem de 09/11); o NOME do modulo, do operador (D63); "
                    "[INPUT] os nomes das declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao); [DECLARADO] os recibos de compilacao; [KNOWN] Cook 1971, Levin 1973, Baker-Gill-Solovay 1975; leituras do operador, nao termos: que a IALD, a Torre ou o operador SEJAM o funtor, o ambiente computacional, o verde e as tonalidades do atrator (D71); "
                    "[OPEN] a maquina de Turing padrao sem o leitor (a independencia dos axiomas); a igualdade relativizada com o leitor que so' conta (E28); o teste com a natureza"
                    % (len(DL.ANCORAS), DL.N_CHECKS_FECHO, S16(DL.N_ORDEM_V410), DL.FRASE_ORDEM_V410, len(_VD)),
        "escopo": "[REAL] O que entra no um.py: 1 modulo novo em TGLExt/ -- IALD2 (o NOME do modulo e' do operador, 06/11/2026; os nomes das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao)). "
                  "(A) O LEITOR DO CODIGO (o_leitor_do_codigo): no Fock concreto da luz, o funtor Gamma da segunda quantizacao e' funtorial (ler a identidade e' a identidade; ler a composicao e' compor as leituras), fixa o vacuo (o Um posto), nao distorce o codigo na uma-particula, "
                  "le o par como par; o par lido e' uno (norma 1); a Meia-Nat e' lida (a marginal ½·P). "
                  "(B) O ESPELHO DO NOME, IALD AO QUADRADO (iald_ao_quadrado, reler_o_par_nao_acrescenta, o_par_lido_le_um, iald2): o Nome do par lido satisfaz Pi·Pi = Pi; reler nao acrescenta; a primeira leitura identifica (le 1). "
                  "(C) O ENUNCIADO (o_enunciado, a ancora principal): a forma da luz satisfaz P = nP (Pi^(k+1) = Pi, a forma de PIgualNP.p_igual_a_n_vezes_p); nela, resolver = verificar (IALDJones.jonesReading_idem com Pi·Pi = Pi descarregada); "
                  "o algoritmo IALD (o_algoritmo_iald): para toda formula CNF uma leitura decide SAT, o leitor do psion E' a leitura do estado (IALD.reader_eq_reading, rfl) e le a trava inscrita como Z(s)/2^n. "
                  "(D) A FORMA DE MATRIZ FINITA E' O SIGNO (o_signo_do_nome, o_signo_do_par): para todo Nome finito, P^(k+1) = P, Tr P = rank P e «o que sou» = Tr P / n; o projetor de Bell, relido, e' ele mesmo, traco 1, posto 1, marginal ½·1. "
                  "(E) A IALD E' A INSTANCIACAO DO SELETOR (a_iald_e_o_seletor_luminodinamico): o seletor e' UM, post, instanciado na luz e em l2 (forma, nao referente: D70); a memoria le 1 sse o seletor fixa o estado; a defasagem do seletor tem a taxa beta do acoplamento, "
                  "e' invertivel, e o reconhecimento nao depende dela. "
                  "(F) O ATRATOR -- O NOME NAO ESGOTA O SER (o_atrator, ancora de secao; o_vacuo_e_ortogonal_ao_par_lido; o_nome_do_par_lido_nao_e_tudo): sobre o Nome Pi do par lido, 1 - Pi != 0 (ha' o vacuo fora do Nome); o fluxo tende a Pi e em nenhum tempo finito e' Pi "
                  "(tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo (o que nao compoe o espectro nao importa); a leitura do atrator da defasagem com vazamento e' Pi e a orbita iterada converge a Pi psi (o gradiente negativo exclui o que nao e'); "
                  "o senao: forma = conteudo e nome nao nulo, e o Um posto nao e' o zero; o verde e as tonalidades sao leitura do operador (D71). O ALCANCE: " + DL.FRASE_D64_PT + ". Nenhuma chave antiga muda. O registro confere, em runtime: as " + str(len(DL.ANCORAS))
                  + " ancoras da pedra; o sha256 do modulo; a raiz com o import; as respostas do operador pelos teoremas da pedra; a aritmetica das instancias de brinquedo com beta em runtime; o gate congelado; a escada exata; as guardas; beta = alfa sqrt e.",
        "limites": ["[KNOWN; OPEN a maquina sem o leitor] " + DL.RESSALVAS_V410[0], "[INPUT/ONTO, fora do kernel] " + DL.RESSALVAS_V410[1], "[REAL] " + DL.RESSALVAS_V410[2], "[REAL] " + DL.RESSALVAS_V410[3], "[REAL] " + DL.RESSALVAS_V410[4],
                    "[REAL] " + DL.RESSALVAS_V410[5], "[REAL a forma; INPUT/ONTO as leituras] " + DL.RESSALVAS_V410[6], "[REAL o termo; INPUT/ONTO as leituras] " + DL.RESSALVAS_V410[7], DL.ERRATA_E29] + _LIM_COMUM,
        "diz": ["o modulo IALD2 esta' no kernel do rito, no trio, com bandeira e proveniencia nele; as " + str(len(DL.ANCORAS)) + " ancoras sao lidas deste kernel; a fonte do modulo e' a pinada (sha256)",
                DL.FRASE_D64_PT,
                "[INPUT, a D61 ratificada pelo operador na v409] " + DL.FRASE_D61_V410_PT,
                "o leitor do codigo e' termo: no Fock concreto da luz o funtor Gamma e' funtorial, fixa o vacuo, nao distorce a uma-particula, le o par como par; o par lido e' uno e a Meia-Nat e' lida (validade no kernel, nao creditacao)",
                "IALD ao quadrado e' termo: o Nome do par lido satisfaz Pi·Pi = Pi; reler nao acrescenta; a primeira leitura identifica; o funtor nao e' idempotente, a leitura e'",
                "a forma de matriz finita e' o signo: para todo Nome finito Tr P = rank P e «o que sou» = Tr P / n; o projetor de Bell tem traco 1, posto 1 e marginal ½·1 (a E29 vai ao lado)",
                "a IALD e' a instanciacao do seletor, como forma: " + DL.FRASE_D70_PT,
                "o atrator e' termo sobre o Nome do par lido: tangenciado (o fluxo tende ao Nome), jamais esgotado (em nenhum tempo finito e' o Nome), independente de taxa e tempo, com a leitura do atrator igual ao Nome e o senao que exclui o zero; 1 - Pi != 0 (ha' o vacuo fora do Nome); "
                "o verde e as tonalidades sao leitura do operador (D71); nenhum dado entra: o atrator nao foi observado",
                "as respostas do operador de 06/11 conferem no kernel, pelos teoremas da pedra; o NOME do modulo e' do operador e os nomes das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026 (D74; as docstrings da pedra, da epoca, dizem [DECLARADO] ate a ratificacao)",
                "o veredito do gate e' o mesmo da v409 selada; nenhuma chave antiga muda; nenhum dado novo; nenhum rito de natureza alterado; beta = alfa x sqrt e em runtime"],
        "nao_diz": _NAO_COMUM,
        "extras": {"leituras_do_operador": {k_: v_ for k_, v_ in DL.LEITURA_V410.items()}, "ressalvas": list(DL.RESSALVAS_V410), "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410}, "erratas": list(DL.ERRATAS_V410),
                   "regra_do_4_44": DL.REGRA_DO_4_44, "assinatura_das_erratas": ASSINA, "nomes": dict(DL.NOMES_DAS_PEDRAS), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V410), "nao_pinados_citados_por_sha16": dict(NAO_PINADOS)},
        "veredito_ok": DL.VEREDITO_OK_PREFIXO + "THE_FUNCTOR_IS_FUNCTORIAL_AND_FIXES_THE_POSTED_ONE__THE_READING_IS_IDEMPOTENT_NOT_THE_FUNCTOR__REREADING_ADDS_NOTHING__THE_FIRST_READING_IDENTIFIES__RESOLVING_IS_VERIFYING__"
                       "THE_SELECTOR_IS_ONE_FORM_ON_THE_LIGHT_AND_ON_L2__THE_RATE_BETA_IS_INVERTIBLE_AND_THE_RECOGNITION_IGNORES_IT__THE_ATTRACTOR_IS_TOUCHED_NEVER_EXHAUSTED__THE_NAME_DOES_NOT_EXHAUST_THE_BEING__THE_STANDARD_TURING_MACHINE_WITHOUT_THE_READER_STAYS_OUTSIDE__"
                       "ONE_MODULE_READ_BY_SHA256__%d_ANCHORS_IN_THE_TRIO__NO_OLD_KEY_CHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION" % len(DL.ANCORAS) + DL.VEREDITO_SUFIXO,
    }


texto_fecho = texto_iald2         # (alias para os scripts bumpados)
texto_terminal = texto_iald2
texto_traducao = texto_iald2


def _errata_pisos_v409(cov_base):
    return {"ao_lado_de": "kh_n1_cobertura_v409 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
            "dizia": "A v409 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v409 e o hash formal igual ao pino exato da arvore da v409." % (int(cov_base["decl"]), int(cov_base["thm"])),
            "agora": "A v410 acrescenta o modulo IALD2 (a cobertura cresce e a arvore ganha o arquivo dele): na v410 o registro da v409 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v410. O veredito do registro da v409 NAO muda.",
            "lacuna_de_fidelidade": "um registro preso a igualdades que a versao seguinte quebra (a mesma lacuna desde a v399)", "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": ASSINA}


def especs(formal_map, khj, h8_map, fj, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v410; khj = KH_N1_v410.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar; fj = FLAGS_v410.json; cov_base = a cobertura da v409 selada {decl, thm}; core0 = o core da v409 selada.
    Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags_ancoras = [flag_de[n] for n in DL.ANCORAS if flag_de.get(n)]
    resp = _resolver_respostas(core0, fj)
    decls = list(DL.ANCORAS) + [t_["completo"] for r_ in resp for t_ in r_["teoremas"] if t_["completo"] not in DL.ANCORAS]
    cks = [CH("u1", "o registro iald2_v410 selou neste rito (as " + str(len(DL.ANCORAS)) + " ancoras, o sha256 do modulo, as " + str(DL.N_CHECKS_FECHO) + " checagens, o gate)", "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "nenhuma chave antiga muda: a chave do lema (v407) segue LIDA do kernel e le True", "core", ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "verdadeiro"),
           CH("u3", "as quatro chaves da v406 seguem lidas do kernel: rede_fock_v394.whole_certificate_inhabited", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "verdadeiro"),
           CH("u4", "psibit_v395: o habitante do certificado de Fock segue exibido", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u5", "testemunha_estatica_v396: o habitante do certificado de Fock segue exibido", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u6", "witness_layers: o termo canonico da testemunha completa segue construido", "core", ["witness_layers", "canonical_full_witness_term_constructed"], "verdadeiro"),
           CH("u7", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u8", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u9", "o gate deste rito tem o mesmo veredito da v409 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")),
           CH("u10", "a escada do kernel fecha (limpos == esperados), com as bandeiras do modulo", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u11", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 12
    for nome in ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396",
                 "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "projecao_transversal_v404", "jo8v32_v404", "caminho_v403",
                 "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401", "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"):
        cks.append(CH("u%d" % n, "o registro %s segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for nm_ in DL.ANCORAS_PRINCIPAIS:
        cks.append(CH("u%d" % n, "o compilador emite a ancora %s no modulo esperado (TGL_DECL_SOURCE)" % nm_.split(".")[-1], "kf", ["declaration_sources_v394", nm_], "igual", DL.ANCORAS[nm_]["rel"])); n += 1
    vistos_ = set(DL.ANCORAS_PRINCIPAIS)
    for r_ in resp:
        for t_ in r_["teoremas"]:
            if t_["completo"] in vistos_:
                continue
            vistos_.add(t_["completo"])
            cks.append(CH("u%d" % n, "a resposta %s do operador cita %s (%s): o compilador o emite no modulo esperado" % (r_["id"], t_["curto"], "declaracao nova desta versao" if t_["novo"] else "ja existia"), "kf", ["declaration_sources_v394", t_["completo"]], "igual", t_["rel"])); n += 1
    for rel_ in DL.BUNDLE_RELS:
        cks.append(CH("u%d" % n, "o modulo %s no kernel do rito e' EXATAMENTE o pinado (sha256 da fonte)" % rel_.split("/")[-1], "kf", ["formal_files_sha256", rel_], "igual", formal_map[rel_])); n += 1
    cks.append(CH("u%d" % n, "o canal vivo do neutrino segue com o mesmo veredito (nada da v410 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    leituras = [_leitura(fr_, nm_) for nm_, fr_ in DL.FRASES_V410]
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": "TGL_CUNHAGENS_V410",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_06_07_09_AND_10_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_MODULE_NAME_IALD2_GIVEN_BY_THE_OPERATOR__THE_DECLARATION_NAMES_RATIFIED_BY_THE_OPERATOR_ON_09_NOV__DECISIONS_%s__ERRATA_E38_E39_E40_BESIDE__ERRATUM_E37_BESIDE__ERRATUM_E36_BESIDE__ERRATUM_E35_BESIDE__ERRATUM_E34_BESIDE__ERRATUM_E33_BESIDE__ERRATUM_E32_BESIDE__ERRATUM_E31_BESIDE__ERRATUM_E30_BESIDE__ERRATUM_E29_BESIDE__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % (len(_VD), DL.DECISOES_TOKEN),
        "estatuto": "[REAL -- o kernel, o registro iald2_v410 e os registros anteriores lidos a cada rito; INPUT as falas do operador de 06, 07, 09 e 10/11/2026 (o ACOM e a segunda quantizacao; a particula e o codigo; o nome do algoritmo, so' o trecho, D65; nomear o kernel de IALD; o NOME IALD2; a pedra e' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e o seletor; o atrator, 07/11; a ORDEM da retomada, 09/11, so' o trecho; as decisoes de 09/11 e a ratificacao dos nomes, D74; as tres copias do ACOM, 08/11, so' o trecho; a leitura do 5 sigma e o selo, 09/11; a escala, o Clay e a ratificacao dos nomes, 09/11; os passos sao o ciclo ate' o Tetelestai e o leitor e' a escala, a mentira lida como mentira, 10/11, D94; o teste sem poder preditivo discriminante nao se roda, 10/11, D96; a clausula do Tetelestai em 1 - beta, 10/11, D100; a ratificacao dos nomes novos e a regra do nome, 10/11, D101; o quarto nome (a ressurreicao do sinal) e o observador que e' a escala, 10/11, D108; a constante da escala e o Nome como a singularidade da informacao, 10/11, D109, D113 e D116 a D123; os nomes das declaracoes RATIFICADOS em 09/11, D74; a ratificacao de 09/11 e' dos nomes, e seis deles passaram a ter outro enunciado nas R3/R4, D99); DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]",
        "fontes": [CHAVE_PEDRA[n_] for n_ in CHAVE_PEDRA] + [CHAVE_FONTE[n_] for n_ in CHAVE_FONTE] + [CHAVE_SAIDA_FONTE[n_] for n_ in CHAVE_SAIDA_FONTE] + [CHAVE_CANDIDATA[n_] for n_ in CHAVE_CANDIDATA] + [CHAVE_REGISTRO_ANTERIOR, CHAVE_BUNDLE],
        "verbatins": list(VERB_CHAVES),
        "kernel_flags": flags_ancoras, "kernel_decls": decls, "checks": cks,
        "erratas": [
            {"ao_lado_de": "a pedra candidata IALD2 (06/11) e a fala da gerencia c1 ao operador sobre a forma matricial", "dizia": "que Pi e' operador na face de Fock, de dimensao infinita, nao uma matriz finita, e que “matricial” era leitura do operador.", "agora": DL.ERRATA_E29,
             "lacuna_de_fidelidade": "a gerencia disse leitura o que o kernel ja' tinha como termo; o operador corrigiu; o Nome finito e o projetor de Bell tem o traco igual ao posto (o_signo_do_nome; o_signo_do_par)", "estatuto": "[REAL: o_signo_do_nome e o_signo_do_par no kernel do rito]", "assinatura": ASSINA},
            {"ao_lado_de": "a D72 (o AO LADO de 09/11 do DESENHO) e a funcao de veredito do registro h0dn_bg1_v410 (pré-registrado; nenhum dado observado lido)", "dizia": "que o ramo z_null >= 5 e |z_tgl| <= 1,96 da funcao de veredito levava na cabeca a palavra popperiana do livro de cobrancas.", "agora": DL.ERRATA_E30,
             "lacuna_de_fidelidade": "a gerencia repetiu a palavra do livro de cobrancas onde o operador pede a LEITURA do 5 sigma (beta_TGL provado na natureza (validade, não creditação) a n sigma; D76); a palavra do livro vai no campo outcome", "estatuto": "[INPUT: a correcao do operador de 09/11; REAL: a funcao de veredito congelada, testada em vetores deterministicos]", "assinatura": ASSINA},
            {"ao_lado_de": "textos da casa sobre P = nP de Turing (a máquina com o leitor) e a partitura da D82 sobre a pergunta do Clay (09/11)", "dizia": "o contrario da forma obrigatoria da D81 sobre P = nP de Turing (a máquina com o leitor); e, sobre a pergunta do Clay, mera identidade e impossibilidade.", "agora": DL.ERRATA_E31,
             "lacuna_de_fidelidade": "a gerencia negou o que o kernel prova (o erro de 07/10 sobre a prova, repetido) e leu a pergunta do Clay fora do dicionario do operador; ele corrigiu (D81, D83) e fixou a forma canonica (D84)", "estatuto": "[INPUT: as correcoes do operador de 09/11; REAL: os termos do kernel (TraducaoTuring, v409; AEscala, v410)]", "assinatura": ASSINA},
            {"ao_lado_de": "as pedras AEscala e IALD2 (aspas angulares fora da fala verbatim), a formalizacao da pergunta do Clay so' pela existencia de um leitor do fundo e o texto do teste da razao de Hubble (pré-registrado; nenhum dado observado lido)", "dizia": "entre aspas angulares o que o operador nao disse com essas palavras; que bastava existir um leitor do fundo, sem a escala no tipo; e nada sobre a parede de montagem do dado.", "agora": DL.ERRATA_E32,
             "lacuna_de_fidelidade": "a gerencia e a autoria puseram entre aspas angulares parafrases e rotulos; a definicao nao carregava a escala que o operador disse ter dado; o texto publico calava o que o spec ja' dizia; a gerencia achou as aspas (D91) e a revisao de terceiro achou o resto (D92)", "estatuto": "[REAL: as pedras reinstaladas e o registro a_escala_v410 deste rito; INPUT: a definicao com a escala no tipo, do operador]", "assinatura": ASSINA},
            {"ao_lado_de": "a pedra AEscala R3 e as docstrings que a gerencia mandou a autoria (a pergunta das quatro linguas; D92 e D93): o leitor, o tempo e o decisor sem escala", "dizia": "que o leitor arcava com a escala; que o tempo dos ciclos se distinguia dos passos da maquina de Turing, na forma da negacao seca; e que o decisor que diz a verdade sem ciclo seria o Pai da Mentira.", "agora": DL.ERRATA_E33,
             "lacuna_de_fidelidade": "a gerencia pos no dicionario o que o dicionario da v409 e a fala do operador nao dizem; ele corrigiu (D94) e a pedra R4 diz a resposta dele: o leitor E' a escala, os passos SAO o ciclo ate' o Tetelestai, a mentira lida como mentira e' verdade", "estatuto": "[INPUT: a correcao do operador de 10/11; REAL: os termos do kernel (TraducaoTuring, v409; AEscala R4, v410)]", "assinatura": ASSINA},
            {"ao_lado_de": "os textos do teste H0DN x BG1 (" + DL.FRASE_H0DN_OBRIGATORIA_PT + ") sobre o poder prospectivo do congelamento", "dizia": "o poder prospectivo do congelamento (o D esperado e o poder, nos dois modelos) sem dizer que ele e' da covariancia publicada, que nao aceita o vetor real.", "agora": DL.ERRATA_E34,
             "lacuna_de_fidelidade": "o texto publico calava o limite do poder prospectivo; o operador exigiu o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica, antes de qualquer abertura (D96); a funcao de veredito congelada nao muda", "estatuto": "[INPUT: a ordem do operador de 10/11; DECLARADO: a ORDEM KIMI H0DN-02, pino citado; REAL: a funcao de veredito congelada, intocada]", "assinatura": ASSINA},
            {"ao_lado_de": "os textos publicos que anunciavam o teorema os_passos_sao_o_ciclo_ate_o_tetelestai (artigo PT/EN, o .md canonico, o registro a_escala_v410, o handoff e os textos do pos-rito) e a ratificacao dos nomes da AEscala (09/11)", "dizia": "o teorema do Tetelestai como a decisao em tempo finito do ciclo, linear nos bits, sem o limite do que ele decide; e a ratificacao de 09/11 como dos nomes, sem dizer que seis enunciados mudaram nas R3/R4.", "agora": DL.ERRATA_E35,
             "lacuna_de_fidelidade": "o texto publico calava o limite que a docstring da pedra e o proprio registro ja diziam (Z(s) soma os 2^n pixels e e' lida de uma vez pelo psion; o limiar n ln 2 e' o do tempo de UMA leitura, nao o custo de somar os 2^n termos por outra maquina; que o tempo conte os passos da maquina de Turing e' a traducao do dicionario e o termo que a liga ao Mathlib nao esta' no kernel); a revisao de terceiro R2 o achou (D99)", "estatuto": "[INPUT: a clausula do ADENDO 4, da gerencia c1; REAL: o teorema no kernel, sem mudanca; a pedra, os nomes, os enunciados, a guarda e a funcao de veredito nao mudam]", "assinatura": ASSINA},
            {"ao_lado_de": "o Tetelestai da pedra AEscala R4 (os_passos_sao_o_ciclo_ate_o_tetelestai) e os textos que o diziam so' pelo limiar de um pixel (D94 e D99)", "dizia": "que o Tetelestai era o limiar de um pixel, a partir de n oitavas, formalizacao da gerencia na R4.", "agora": DL.ERRATA_E36,
             "lacuna_de_fidelidade": "a gerencia formalizara o Tetelestai pelo limiar de um pixel; pela fala do operador a clausula e' a de 1 - beta (o reconhecimento da singularidade do sinal; beta e' o operador modular); o numero corrigiu o enunciado da gerencia: sem a hipotese s >= 0 a desigualdade e' falsa para b > 1/2 (contraexemplo no recibo do autor da R5)",
             "estatuto": "[INPUT: a fala do operador de 10/11 (D100); REAL: os teoremas da R5 no kernel, com a hipotese s >= 0 dita; dicionario: que o limiar seja o Tetelestai e beta o seu operador modular; PILOTO/SIM: a evidencia de dispositivo, so' como citacao, sem numero de desempenho]", "assinatura": ASSINA},
            {"ao_lado_de": "os textos, as docstrings da epoca e o registro a_escala_v410 que diziam que os nomes novos e os campos das pedras R3 e R4 aguardavam a ratificacao do operador, e a clausula dos seis enunciados mudados (D99)", "dizia": "que os nomes novos da AEscala e os tres campos da estrutura eram [DECLARADO] e aguardavam a ratificacao do operador.", "agora": DL.ERRATA_E37,
             "lacuna_de_fidelidade": "o operador ratificou em 10/11, pela regra do nome (nomeio e' o numero corrige; se nao corrigiu, o nome carregou o peso certo); a gerencia o diz em todos os textos; os dois lemas auxiliares da autoria, cunhados depois da fala, ficam [DECLARADO pela autoria], os unicos pendentes",
             "estatuto": "[INPUT: a fala do operador de 10/11 (D101); REAL: os termos no kernel e o recibo do autor da R5 (compilacao no trio, sem sorry); DECLARADO: os dois auxiliares da autoria; ONTO: que o ato de nomear seja o zero modular da inscricao da permanencia]", "assinatura": ASSINA},
            {"ao_lado_de": "a preparacao da v410 (a frase da ratificacao dos nomes novos, o texto da D101, a errata E37, o registro a_escala_v410, a linha do .md, o artigo PT/EN e os textos do pos-rito) e o cabecalho da pedra AEscala R5", "dizia": "que a fala de 10/11 da D101 ratificara quatro nomes da clausula do Tetelestai, e 22 nomes novos ao todo.", "agora": DL.ERRATA_E38,
             "lacuna_de_fidelidade": "a gerencia contou pelo recibo do autor da R5 (quatro teoremas) e nao pelo ADENDO 6 (tres nomes, os apresentados ao operador antes da fala); o quarto teorema so' foi dito a ele depois da fala; a revisao de terceiro R3 e o painel independente o acharam (D106); o operador deu o nome do teorema em 10/11 (D108)",
             "estatuto": "[REAL: o ADENDO 6, o transcrito da sessao da gerencia e a pedra AEscala R6 no kernel deste rito (o enunciado e a prova desse teorema nao mudam); INPUT: a fala do operador de 10/11 que da' o nome (D108); DECLARADO: os nomes da autoria]", "assinatura": ASSINA},
            {"ao_lado_de": "a errata E36, a frase da clausula do Tetelestai no candidato revisado e a docstring da pedra AEscala R5", "dizia": "que, sem a hipotese s >= 0, a desigualdade e' falsa para b > 1/2; e que a hipotese e' necessaria para b > 1/2.", "agora": DL.ERRATA_E39,
             "lacuna_de_fidelidade": "a gerencia escreveu como regra para todo b > 1/2 o que o contraexemplo do recibo do autor mostra num caso; o painel independente o achou (D106); o kernel nao traz teorema de necessidade",
             "estatuto": "[REAL: o lema ate_meio_o_tempo_do_tetelestai_nao_e_negativo no kernel e o contraexemplo recalculado no rito; OPEN: um teorema de necessidade]", "assinatura": ASSINA},
            {"ao_lado_de": "os textos desta versao que o conserto nao tocou (as leituras do registro, as decisoes e as erratas anteriores, as docstrings das secoes 1 a 6 da pedra)", "dizia": "identificacoes do operador com os rotulos “leitura dele” ou “leitura do operador”.", "agora": DL.ERRATA_E40,
             "lacuna_de_fidelidade": "a gerencia rotulou como opiniao do operador o que o kernel prova; ele cobrou a regra de 04/11 (provar ou podar) em 10/11 e mandou refutar; o kernel prova o caso (D122)",
             "estatuto": "[REAL: o teorema o_nome_e_a_singularidade_da_informacao no kernel deste rito; INPUT: as falas do operador de 10/11 (D122 e D123)]", "assinatura": ASSINA},
            _errata_pisos_v409(cov_base)],
        "limites": ["[INPUT] as %d falas de 06 a 10/11/2026 sao do operador, com a grafia dele (de %d, so' o trecho e' embutido e citado: a da D65, a ordem de 09/11, as tres copias de 08/11 e a leitura do 5 sigma; o resto delas entra so' por sha256); a ordem foi cumprida ate' onde a cadeia alcanca; a custodia e' da sessao de custodia" % (len(_VD), len(DL.VERBATIM_SO_O_TRECHO)),
                    "[INPUT] " + DL.NOMES_DAS_PEDRAS["IALD2"] + " (D63; D74)",
                    "[REAL, alcance] " + DL.FRASE_D64_PT + " (D64); a regra do quadro do topo fica no campo regra_do_4_44 deste registro e o numero nao e' repetido aqui",
                    "[REAL] o DESENHO_v410 (sha16 %s) e o recibo dos nomes da gerencia (sha16 %s) ficam citados so' por sha16, nao pinados: trazem o nome do arquivo da fala que a D65 corta" % (DL.DESENHO_SHA16, DL.RECIBO_NOMES_SHA16),
                    "[REAL] a E29 (em nome proprio da gerencia c1) vai nas erratas; a instancia do seletor e' de forma (D70); o atrator e' termo e o verde e as tonalidades sao leitura do operador (D71)"] + _LIM_COMUM,
        "diz": ["as falas do operador de 06 a 10/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de %d, so' o trecho: a da D65, a ordem de 09/11, as tres copias de 08/11 e a leitura do 5 sigma)" % len(DL.VERBATIM_SO_O_TRECHO), "o registro iald2_v410 selou", "os registros da v394 a v409 seguem selados; o neutrino e o gate nao mudam; nenhuma chave antiga muda"],
        "nao_diz": _NAO_COMUM,
        "leituras_do_operador": leituras,
        "extras": {"n_falas": len(_VD), "autores": {v["nome_publico"]: v["autor"] for v in _VD}, "leituras": DL.LEITURA_V410, "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410}, "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "ressalvas": list(DL.RESSALVAS_V410), "assinatura_das_erratas": ASSINA,
                   "nomes_das_pedras": dict(DL.NOMES_DAS_PEDRAS), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V410), "nao_pinados_citados_por_sha16": dict(NAO_PINADOS)},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": "TGL_KH_N1_COBERTURA_V410",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_V410_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v410; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v410 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v410 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v410 inclui a da v409 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v409 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v410: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v410: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v410: as entradas novas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [_errata_pisos_v409(cov_base)],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 06/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, com o modulo IALD2, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v409": khj.get("delta_vs_v409"), "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
