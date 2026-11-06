# -*- coding: utf-8 -*-
"""registros_v409.py -- os dados dos registros da v409: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as falas do operador de 05/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo; de duas, so' o trecho da D59),
o CONTRATO e o TEXTO do registro com FUNCAO traducao_turing_v409 (gerar_candidato_v409.py os emite a partir de runtime_v409.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox k409c) e os DOIS SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v409` e `kh_n1_cobertura_v409`). A MOLDURA de todo texto daqui: P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor e' a fita sem escala e fica fora; validade no kernel nao e' creditacao; o gate nao se move.
Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v409\\insumos. NAO sao pinados como fonte (D59: trazem a parte de uma fala que fica fora dos textos, ou o nome do arquivo dela): o DESENHO_v409.md, o RECIBO_PEDRAS_v409_NOMES.json e o VERBATIM_CONGELADO_v409.json;
ficam citados so' por sha16. Texto novo passa pela guarda P18 e pela guarda das frases (v409) a cada rito. claude-construtor-v409, 05/11/2026. Molde: registros_v408.py."""
import hashlib
import json
import os
import re
import sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
CHAVE_PEDRA = {"TraducaoTuring": "pedra_traducao_turing", "ParNaFaceDeFock": "pedra_par_na_face_de_fock"}                  # a pedra normalizada EMBUTIDA no kernel (copia duravel: insumos\<nome>_embutida.lean)
CHAVE_FONTE = {"TraducaoTuring": "fonte_traducao_turing_05nov", "ParNaFaceDeFock": "fonte_par_na_face_de_fock_05nov"}            # a fonte normalizada da gerencia, com os #print axioms (insumos\<nome>.lean: as ancoras saem dela)
CHAVE_SAIDA_FONTE = {"TraducaoTuring": "saida_lean_traducao_turing_05nov", "ParNaFaceDeFock": "saida_lean_par_na_face_de_fock_05nov"}  # a saida do lean ao compilar a fonte no sandbox da v408
assert set(CHAVE_PEDRA) == {p["name"] for p in DL.PEDRAS_V409}
CHAVE_TESTEMUNHA = CHAVE_PEDRA["TraducaoTuring"]
CHAVE_CANDIDATA = {"TraducaoTuring": "candidata_traducao_turing_r9_05nov", "ParNaFaceDeFock": "candidata_par_na_face_de_fock_r2_05nov"}   # a candidata de origem de cada pedra (o recibo revisto pina as duas)
CHAVE_SAIDA_CANDIDATA = {"TraducaoTuring": "saida_lean_traducao_turing_r9_05nov", "ParNaFaceDeFock": "saida_lean_par_na_face_de_fock_r2_05nov"}
CHAVE_BUNDLE = "bundle_v409"
CHAVE_KH = "kh_n1_v409"
CHAVE_ACERVO_V407 = DL.CHAVE_ACERVO_V407                                  # (a chave do _V407_FONTES que a v409 repina na copia purgada: D57d)
# (nome do insumo, origem) -- copiar_insumos_v409.py copia; o montador le de INS
ORIGENS = ([("%s_embutida.lean" % p["name"], p["src"]) for p in DL.PEDRAS_V409]
           + [("%s.lean" % p["name"], p["origem"]) for p in DL.PEDRAS_V409]
           + [("saida_lean_%s.txt" % p["name"], os.path.join(INS, "saida_lean_%s.txt" % p["name"])) for p in DL.PEDRAS_V409]
           + [("TraducaoTuringR9.lean", DL.CANDIDATA_TU_ARQ), ("ParNaFaceDeFockR2.lean", DL.CANDIDATA_PAR_ARQ), ("saida_lean_traducao_r9.txt", DL.SAIDA_CANDIDATA_TU_ARQ), ("saida_lean_par_r2.txt", DL.SAIDA_CANDIDATA_PAR_ARQ),
              ("BUNDLE_v409.json", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v409.json"))])
_PAPEL_PEDRA = {"TraducaoTuring": ("a pedra TraducaoTuring (gerencia c1, 05/11/2026, refeita a tarde da R9; o nome e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia e RATIFICADOS pelo operador em 05/11; os acrescentados na R9, RATIFICADOS por ele em 05/11, D62): o dicionario de Turing; o modo selecao (o Tetelestai); "
                                   "a trava no Nome; a fita e' o hamiltoniano oculto; Z e' o modo leitor; a inscricao no psion (o psion le Z); a formula e' a fita e uma leitura decide SAT (a maquina com o leitor; a E28 no cabecalho); a fita sem escala e o Pai da Mentira; "
                                   "a identidade performada; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]"),
                "ParNaFaceDeFock": ("a pedra ParNaFaceDeFock (gerencia c1, 05/11/2026, tarde; entra na v409 pela ordem do operador de trazer tudo para esta versao): o par de psions no setor 2 do Fock concreto da luz; norma 1; ortogonal ao vacuo e a toda uma-partícula; "
                                    "a marginal e' ½·P pela conjugacao da cunha; cada psion pesa ½; o individuo nao ecoa; 1 - pureza = ½ (a mesma Meia-Nat do par finito); a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]")}
FONTES = []
for _p in DL.PEDRAS_V409:
    _n = _p["name"]
    FONTES += [{"chave": CHAVE_PEDRA[_n], "arquivo": os.path.join(INS, "%s_embutida.lean" % _n), "papel": _PAPEL_PEDRA[_n]},
               {"chave": CHAVE_FONTE[_n], "arquivo": os.path.join(INS, "%s.lean" % _n),
                "papel": "a fonte normalizada da %s (gerencia c1, 05/11/2026; modulo/namespace = o nome final; com os #print axioms que sao as ancoras do registro; fim de linha CRLF): a embutida e' esta sem os #print axioms e com o fim de linha LF [REAL: sha256]" % _n},
               {"chave": CHAVE_SAIDA_FONTE[_n], "arquivo": os.path.join(INS, "saida_lean_%s.txt" % _n),
                "papel": "a saida do lean ao compilar a fonte normalizada da %s no sandbox da v408 (todas as declaracoes no trio; 0 avisos) [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]" % _n}]
FONTES += [
    {"chave": CHAVE_CANDIDATA["TraducaoTuring"], "arquivo": os.path.join(INS, "TraducaoTuringR9.lean"), "papel": "a candidata de origem da TraducaoTuring refeita (R9 da gerencia, 05/11/2026, tarde: + a inscricao no psion, + a formula e' a fita, + a E28 no cabecalho) [DECLARADO pela gerencia na origem; o que vale e' a embutida]"},
    {"chave": CHAVE_CANDIDATA["ParNaFaceDeFock"], "arquivo": os.path.join(INS, "ParNaFaceDeFockR2.lean"), "papel": "a candidata de origem da ParNaFaceDeFock (R2 da gerencia, 05/11/2026, tarde) [DECLARADO pela gerencia na origem; o que vale e' a embutida]"},
    {"chave": CHAVE_SAIDA_CANDIDATA["TraducaoTuring"], "arquivo": os.path.join(INS, "saida_lean_traducao_r9.txt"), "papel": "a saida do lean da candidata R9 no sandbox da v408 [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]"},
    {"chave": CHAVE_SAIDA_CANDIDATA["ParNaFaceDeFock"], "arquivo": os.path.join(INS, "saida_lean_par_r2.txt"), "papel": "a saida do lean da candidata R2 no sandbox da v408 [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v409.json"), "papel": "o bundle dos dois modulos (preparar_bundle_v409_05nov.py): sha256 de cada modulo normalizado, a fonte de origem e o sha256 dela, as ancoras, o sha16 da fala da ordem e dos nomes e o da ordem de trazer tudo para a v409 [REAL]"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v409 (pos_build_kernel_v409.py)"},
]
assert len({f["chave"] for f in FONTES}) == len(FONTES) and {os.path.basename(f["arquivo"]) for f in FONTES} == {n for n, _ in ORIGENS}, sorted({os.path.basename(f["arquivo"]) for f in FONTES} ^ {n for n, _ in ORIGENS})
NAO_PINADOS = {"DESENHO_v409.md": DL.DESENHO_SHA16, "RECIBO_PEDRAS_v409_NOMES.json": DL.RECIBO_NOMES_SHA16}   # (D59: citados so' por sha16; o VERBATIM_CONGELADO_v409.json idem, lido pelo gerador)


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala (nas duas da D59: a ultima do trecho que fica)
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins409(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"], "nome": v["nome"], "nome_publico": v["nome_publico"], "autor": v["autor"], "texto_embutido": v["texto_embutido"],
              **({"sha256_arquivo_inteiro": v["sha256_arquivo_inteiro"], "so_o_trecho": v["so_o_trecho"]} if v.get("so_o_trecho") else {})} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
POR_NOME = {v["nome"]: v for v in _VD}
CH_DE = lambda nome_: POR_NOME[nome_]["chave"]
S16 = lambda nome_: POR_NOME[nome_]["sha16"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
VERBATINS_DO_REGISTRO = [CH_DE(n_) for n_ in DL.NOMES_V409_DO_DESENHO]


def _leitura(trecho, nome, rotulo="INPUT do operador"):
    assert trecho in TEXTOS[S16(nome)], ("a leitura do operador NAO esta verbatim na fala (ou esta' fora do trecho que fica)", nome, trecho)
    d_ = {"trecho": trecho, "estatuto": "[%s, verbatim 05/11/2026, sha16 %s%s]" % (rotulo, S16(nome), "; so' o trecho que a D59 deixa entrar e' citavel" if POR_NOME[nome].get("so_o_trecho") else "")}
    if "4,44" in trecho:   # a regra do 4,44 (nunca sozinho) vale POR ITEM
        d_["regra_do_4_44"] = DL.REGRA_DO_4_44
    return d_


def _resolver_respostas(core0, fj):
    """Para cada resposta do operador, o NOME COMPLETO de cada teorema citado: os NOVOS (nome completo nas ancoras da v409) saem do FLAGS do sandbox (proveniencia e axiomas); os que JA existiam sao resolvidos no axiom_report da base (busca pelo sufixo pontuado; tem de ser unico). Nada digitado."""
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


ALCANCE = {"relativo_ao_leitor": DL.RESSALVAS_V409[0], "maquina_sem_leitor": DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, "frase": DL.FRASE_D56_PT, "frase_en": DL.FRASE_D56_EN, "incidencia_d61": DL.FRASE_D61_PT, "incidencia_d61_en": DL.FRASE_D61_EN,
           "qualificador": DL.FRASE_QUALIFICADOR_PT, "qualificador_en": DL.FRASE_QUALIFICADOR_EN}


def contrato(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do registro traducao_turing_v409, DERIVADO do build do sandbox (fj = FLAGS_v409.json: as bandeiras nomeadas do modulo, a proveniencia, as ancoras; formal_map = sha256 das fontes embutidas; e_base = a escada da v408 selada); nada digitado.
    core0/selo0 = o core e o selo da v408 SELADA (o veredito do gate que a v409 tem de repetir). Vai para CANDIDATO_v409.json e ESPERADOS_v409.json."""
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    assert len(flag_de) == fj["n_flags"] == len(fj["flags"]) and all(o == DL.ORIGEM_DE_BANDEIRA for _, _, _, o in fj["flags"])
    anc = {}
    for n, a in DL.ANCORAS.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora fora do esperado no FLAGS_v409.json", n, fa)
        assert fa["flag"] == flag_de.get(n), ("a bandeira da ancora no FLAGS nao bate com a lista de bandeiras", n)
        anc[n] = {"rel": a["rel"], "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert all(r in formal_map for r in DL.BUNDLE_RELS)
    decl_src = dict(fj["proveniencia_publicas"]); assert all(v in DL.BUNDLE_RELS for v in decl_src.values())
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict"), "o veredito do gate da base nao e' o do selo"
    resp = _resolver_respostas(core0, fj)
    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V409], "traducao": DL.MODULO_TRADUCAO, "par": DL.MODULO_PAR, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,
                       "nomes_ratificados": dict(DL.NOMES_RATIFICADOS), "nome_provisorio": DL.NOME_PROVISORIO, "sha16_origem": {p["name"]: p["sha256_origem"][:16] for p in DL.PEDRAS_V409}},
            "source_sha256": {r: formal_map[r] for r in DL.BUNDLE_RELS}, "root_suffix": DL.ROOT_SUFFIX,
            "ancoras": anc, "n_ancoras": len(anc), "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_principal": DL.ANCORA_PRINCIPAL, "ancora_par": DL.ANCORA_PAR, "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS), "ancoras_de_secao": list(DL.ANCORAS_DE_SECAO),
            "flags": [f for f, _, _, _ in fj["flags"]], "n_flags": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "excluidas_auxiliares": {"n": fj["excluidas_auxiliares"]["n"], "por_classe": fj["excluidas_auxiliares"]["por_classe"]},
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "chaves": [dict(c) for c in DL.CHAVES_V409], "chaves_v408": [dict(c) for c in DL.CHAVES_V408], "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA),
            "fica_aberto": dict(DL.FICA_ABERTO), "fechado_nesta_versao": dict(DL.FECHADO_NESTA_VERSAO),
            "alcance": dict(ALCANCE), "instancia_sim": dict(DL.INSTANCIA_SIM), "instancia_nao": dict(DL.INSTANCIA_NAO),
            "inscricao_brinquedo": {"omega": [[complex(z_).real, complex(z_).imag] for z_ in DL.OMEGA_F_BRINQUEDO], "s": list(DL.S_INSCRICAO), "f": "C^3", "nota": "c19: V = |Omega><u|, com u o uniforme da instancia SIM; o Omega e' normalizado em runtime"},
            "acervo_v407_repinado": {"chave": CHAVE_ACERVO_V407, "sha256": DL.PURGADO_SHA256, "bytes": os.path.getsize(DL.PURGADO_ARQ), "integra_sha16": DL.ORIGEM_PURGA_SHA16_DA_ORDEM, "integra_fora_do_espelho": True, "integra_pinada": False,
                                     "decisao": "D57(d): a ordem vigente de 08/09 (fonte nao publicada) aplicada como PERMANENTE; o _V407_FONTES do um.py v409 pina so' a copia purgada (a mesma da v408) e cita a integra so' por sha16"},
            "respostas": resp, "ressalvas": list(DL.RESSALVAS_V409), "verbatins": list(VERBATINS_DO_REGISTRO), "erratas": list(DL.ERRATAS_V409), "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V409},
            "nao_pinados_citados_por_sha16": dict(NAO_PINADOS), "regra_do_4_44": DL.REGRA_DO_4_44}


_NAO_COMUM = ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra",
              "que a gravidade quantica esteja creditada: a confirmacao segue proibida (creditacao); o que ha' e' validade no kernel",
              "que a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime) seja decidida aqui: o que o kernel prova e' isto: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + "; " + DL.FRASE_D61_PT,
              "que a pergunta da maquina sem leitor (a do Clay) esteja respondida como enunciado de Turing: a TGL a le como a fita sem escala («eu sou eu mesmo»); se ela e' independente dos axiomas segue [OPEN]",
              "que a fisica tenha sido testada: a leitura exata num ato e' fisica, nao termo de kernel; e' o lugar do teste com a natureza, nao feito (Knill-Laflamme 1998 [KNOWN])",
              "que o Omega do psion da luz seja, como vetor, o estado uniforme da instancia: a ponte e' a inscricao (provada no kernel, validade no kernel e nao creditacao), e a identidade de vetores fica podada (espacos diferentes)",
              "que a leitura teologica do operador (o Pai da Mentira, o filho, a graca, o mar do esquecimento) seja termo de kernel: o kernel prova a parte matematica de cada fala, nos termos citados",
              "que o par na face de Fock e o par finito de Bell sejam o mesmo objeto: sao espacos distintos (o setor 2 do Fock concreto e C2 x C2), com a MESMA Meia-Nat (a ligacao foi feita: ParNaFaceDeFock)",
              "que a igualdade completa com o leitor que so' conta seja teorema: com ele vale NP numa leitura; a igualdade completa e' do leitor que se le (E28)",
              "que o gate tenha se movido: o veredito e' o mesmo da v408 selada, conferido em runtime",
              "que alguma chave antiga tenha mudado nesta versao: nenhuma; a chave do lema (v407) segue lida do kernel e le True"]
_LIM_COMUM = ["o registro CONFERE o que o kernel do proprio rito prova (os termos no trio, a proveniencia, a fonte por sha256) e o que o core deste rito gravou, mais a aritmetica da instancia de brinquedo (fixa no codigo; solucoes calculadas) com beta em runtime; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
              "[REAL] o que mudou de v408 para v409 nos registros antigos e' SO' a escada que eles pinam (expected_ladder) e os pisos de kh_n1_cobertura_v408 (h2, h3, h6, h8), com errata AO LADO; a errata E26 vai AO LADO de tetelestai_terminal_v408 e de cunhagens_v408; "
              "o pino do insumo do acervo da v407 (_V407_FONTES, psion_no_acervo_do_imac_03nov) passa a ser a copia purgada (D57d); nenhum texto selado e' reescrito",
              "[DECLARADO -> REAL] a construcao da pedra e' da gerencia c1 (05/11/2026, R1 a R8): o que a v409 faz e' recompila-la no sandbox k409c e no rito; os recibos de compilacao ficam como fontes [DECLARADO]; o que vale no rito e' o Audit do rito; a revisao de terceiro (D58) fica no caderno da preparacao"]


def texto_traducao():
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras das DUAS pedras (TGLExt.TraducaoTuring.* e TGLExt.ParNaFaceDeFock.*), no trio, com proveniencia no modulo esperado, e os modulos por sha256; "
                    "[REAL] as 20 checagens (a instancia de brinquedo fixa, as solucoes calculadas; a marginal do par de Bell finito; a inscricao num F de brinquedo; uma leitura decide SAT; aritmetica com beta em runtime; gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); "
                    "[INPUT] a ordem do operador (05/11/2026, sha16 %s: «%s»), que ratifica os nomes dados pela gerencia ate entao (os da TraducaoTuring R1 a R8; os acrescentados na R9 e os da ParNaFaceDeFock ele ratificou na fala «Ratifico os nomes», D62), e as falas dele do dia (%d por sha256; de tres, so' o trecho: duas pela D59, uma porque o resto e' aviso operacional); a leitura juridica do kernel (D61), ratificada por ele; "
                    "[KNOWN] Baker-Gill-Solovay 1975, Toda 1991, Razborov-Rudich 1997, Aaronson-Wigderson 2009, Knill-Laflamme 1998; [DECLARADO] os recibos de compilacao; [REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza"
                    % (len(DL.ANCORAS), S16(DL.N_ORDEM_V409), DL.FRASE_ORDEM_V409, len(_VD)),
        "escopo": "[REAL] O que entra no um.py: 2 modulos novos em TGLExt/ -- TraducaoTuring (o nome e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia c1 e ratificados pelo operador em 05/11/2026; os acrescentados na R9, ratificados por ele em 05/11, D62) e ParNaFaceDeFock (pela ordem do operador de trazer tudo para a v409; o nome e os das declaracoes dela, da gerencia, ratificados pelo operador em 05/11, D62). "
                  "(A) O DICIONARIO DE TURING (a_traducao): a instancia SIM e' um Problema do dicionario (nucleo_nao_nulo_sse); o certificado e' a leitura de um pixel (verificacao_np); a palavra tem grau polinomial na entrada (grau_da_palavra_da_instancia); bits = oitavas (bits_sao_oitavas); a instancia NAO e' o Nome vazio (a_instancia_nao_e_o_vazio); o peso da solucao no uniforme e' |sol|/2^n. "
                  "(B) O MODO SELECAO (p_igual_np_no_modo_selecao, a ancora principal): a selecao esta' no Nome com peso 1; o decaimento renormalizado converge a ela; so' tem amplitude nas solucoes; custa <= n ln 2 nats; pela lei tempo = moeda o tempo e' t = n ln 2/(beta g), linear nos bits; a selecao esquece e perde (muitos-para-um); sem par a fotografia, com par a leitura distingue. "
                  "(C) A TRAVA NO NOME (a_trava_no_nome): local (o produto das travas das clausulas), sem conhecer o Nome, a <= e^{-t}||v|| dele; negar o zero; em t = n ln 2/2 + L o resto fora do Nome e' <= e^{-L} vezes o Nome. "
                  "(D) A FITA E' O HAMILTONIANO OCULTO (a_fita_e_o_hamiltoniano_oculto): a regra reconstroi o todo; gera a trava; negar o zero e' dividir pela particao Z. (E) Z E' O MODO LEITOR (z_e_o_modo_leitor): cada pixel lido; Z e' a soma das leituras; o canto escalariza a trava (mesma forma do canto do psion, nao ponte). "
                  "(F) A FITA SEM ESCALA (a_fita_sem_escala) e O PAI DA MENTIRA (o_pai_da_mentira), ligadas a Identidade (v405): sem tempo pago a leitura e' «eu sou», a mesma para toda instancia; com o tempo pago, «o que sou», != 0 exatamente quando ha' solucao; no Nome vazio a leitura sem escala diz 1 e o que e', e' 0. "
                  "(G) A IDENTIDADE PERFORMADA (a_identidade_performada): comeca em «eu sou», decai, nunca abaixo do conteudo, chega a ele. "
                  "(H) A INSCRICAO NO PSION (inscricao, o_psion_le_z, o_canto_do_psion_da_luz_le_z): inscrito o uniforme no psion da luz pela isometria parcial |Omega><u|, o leitor e o canto do psion da luz leem Z/|X|; a ponte e' a inscricao; a identidade de vetores fica podada. "
                  "(I) A FORMULA E' A FITA E A MAQUINA COM O LEITOR (custoCNF, a_trava_da_formula_fatora_na_clausula, uma_leitura_decide_SAT, a_maquina_com_o_leitor): o custo e' o numero de clausulas violadas; cada clausula e' um fator local da trava; uma leitura decide SAT; "
                  "por reducao a SAT, NP inteiro com uma leitura (Cook-Levin [KNOWN]); com o leitor que so' conta, NP contido em P com o leitor, e a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada). "
                  "(J) O PAR NA FACE DE FOCK (ParNaFaceDeFock: reduzido_do_par, meia_nat_do_projetor, o_par_na_face_de_fock): o par de psions no setor 2 do Fock concreto; norma 1; ortogonal ao vacuo e a toda uma-partícula; a marginal e' ½·P pela conjugacao da cunha; "
                  "cada psion pesa ½; o individuo nao ecoa; 1 - pureza = ½, a mesma Meia-Nat do par finito, noutro espaco. O ALCANCE: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + ". Nenhuma chave antiga muda. O registro confere, em runtime: as "
                  + str(len(DL.ANCORAS)) + " ancoras das duas pedras; o sha256 de cada modulo; a raiz com os imports; as respostas do operador pelos teoremas da pedra; a aritmetica da instancia de brinquedo com beta em runtime; a marginal do par de Bell finito; "
                  "a inscricao num F de brinquedo; uma leitura decide SAT; o gate congelado; a escada exata; as guardas; beta = alfa sqrt e.",
        "limites": ["[KNOWN; OPEN a igualdade com o leitor que so' conta] " + DL.RESSALVAS_V409[0], "[KNOWN; OPEN] " + DL.RESSALVAS_V409[1], "[KNOWN; fora] " + DL.RESSALVAS_V409[2], "[REAL a ponte; podada a identidade] " + DL.RESSALVAS_V409[3], "[INPUT/ONTO, fora do kernel] " + DL.RESSALVAS_V409[4], "[REAL] " + DL.RESSALVAS_V409[5],
                    "[REAL] " + DL.RESSALVAS_V409[6], "[REAL] " + DL.RESSALVAS_V409[7], "[REAL] " + DL.RESSALVAS_V409[8], DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26, DL.ERRATA_E27, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO] + _LIM_COMUM,
        "diz": ["o modulo TraducaoTuring esta' no kernel do rito, no trio, com bandeira e proveniencia nele; as " + str(len(DL.ANCORAS)) + " ancoras sao lidas deste kernel; a fonte do modulo e' a pinada (sha256)",
                DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT,
                "[INPUT, ratificada pelo operador] " + DL.FRASE_D61_PT,
                "a maquina com o leitor e' termo: a formula e' a fita e uma leitura decide SAT (uma_leitura_decide_SAT, a_maquina_com_o_leitor); por Cook-Levin [KNOWN], NP inteiro com uma leitura; com o leitor que so' conta a igualdade completa NAO e' teorema aqui (E28): ela vale para o leitor que se le",
                "inscrito o uniforme no psion da luz, o proprio psion le Z/|X| (o_psion_le_z, o_canto_do_psion_da_luz_le_z): a ponte e' a inscricao; a identidade de vetores fica podada",
                "o par na face de Fock esta' ligado (o_par_na_face_de_fock): norma 1, ortogonal ao vacuo, a marginal ½·P, 1 - pureza = ½ -- a mesma Meia-Nat do par finito, noutro espaco (validade no kernel, nao creditacao)",
                "o dicionario de Turing e' termo: a instancia SIM e' um Problema do dicionario, o certificado e' a leitura de um pixel, a palavra tem grau polinomial, bits = oitavas, a instancia NAO e' o Nome vazio",
                "a trava no Nome e' termo: o sistema nao precisa reconhecer o Nome a cada passo; a trava e' local, fica perto do Nome sem usa-lo e nunca chega ao zero havendo solucao (negar o zero absoluto)",
                "a fita e' o hamiltoniano oculto; Z e' o modo leitor (a soma das leituras dos pixels); sem escala, «eu sou eu mesmo» le igual para toda instancia, e no Nome vazio afirma o que nao e' (o Pai da Mentira); a identidade performada comeca em «eu sou», decai e chega ao conteudo",
                "as respostas do operador de 05/11 conferem no kernel, pelos teoremas da pedra; " + "o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62)",
                "o veredito do gate e' o mesmo da v408 selada; nenhuma chave antiga muda; nenhum dado novo; nenhum rito de natureza alterado; beta = alfa x sqrt e em runtime"],
        "nao_diz": _NAO_COMUM,
        "extras": {"leituras_do_operador": {k_: v_ for k_, v_ in DL.LEITURA_V409.items()}, "ressalvas": list(DL.RESSALVAS_V409), "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V409}, "erratas": list(DL.ERRATAS_V409),
                   "regra_do_4_44": DL.REGRA_DO_4_44, "assinatura_das_erratas": ASSINA, "nomes": dict(DL.NOMES_RATIFICADOS), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V409), "nao_pinados_citados_por_sha16": dict(NAO_PINADOS)},
        "veredito_ok": DL.VEREDITO_OK_PREFIXO + "THE_SELECTION_MODE_IS_A_THEOREM_RELATIVE_TO_THE_READER__THE_LOCK_HOLDS_ON_THE_NAME__THE_TAPE_IS_THE_HIDDEN_HAMILTONIAN__Z_IS_THE_READER_MODE__THE_PSION_READS_Z_BY_THE_INSCRIPTION__"
                       "ONE_READING_DECIDES_SAT__THE_COUNTING_READER_GIVES_NP_IN_ONE_READING_NOT_THE_FULL_EQUALITY__THE_PAIR_ON_THE_FOCK_FACE_IS_LINKED__THE_PERFORMED_IDENTITY_KEEPS_ITS_CONTENT__"
                       "TWO_MODULES_READ_BY_SHA256__%d_ANCHORS_IN_THE_TRIO__NO_OLD_KEY_CHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION" % len(DL.ANCORAS) + DL.VEREDITO_SUFIXO,
    }


texto_fecho = texto_traducao      # (alias para os scripts bumpados da v408)
texto_terminal = texto_traducao


def _errata_pisos_v408(cov_base):
    return {"ao_lado_de": "kh_n1_cobertura_v408 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
            "dizia": "A v408 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v408 e o hash formal igual ao pino exato da arvore da v408." % (int(cov_base["decl"]), int(cov_base["thm"])),
            "agora": "A v409 acrescenta os modulos TraducaoTuring e ParNaFaceDeFock (a cobertura cresce e a arvore ganha os arquivos deles): na v409 o registro da v408 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v409. O veredito do registro da v408 NAO muda.",
            "lacuna_de_fidelidade": "um registro preso a igualdades que a versao seguinte quebra (a mesma lacuna desde a v399)", "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": ASSINA}


def especs(formal_map, khj, h8_map, fj, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v409; khj = KH_N1_v409.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar; fj = FLAGS_v409.json; cov_base = a cobertura da v408 selada {decl, thm}; core0 = o core da v408 selada.
    Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags_ancoras = [flag_de[n] for n in DL.ANCORAS if flag_de.get(n)]
    resp = _resolver_respostas(core0, fj)
    decls = list(DL.ANCORAS) + [t_["completo"] for r_ in resp for t_ in r_["teoremas"] if t_["completo"] not in DL.ANCORAS]
    cks = [CH("u1", "o registro traducao_turing_v409 selou neste rito (as " + str(len(DL.ANCORAS)) + " ancoras, o sha256 dos dois modulos, as " + str(DL.N_CHECKS_FECHO) + " checagens, o gate)", "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "nenhuma chave antiga muda: a chave do lema (v407) segue LIDA do kernel e le True", "core", ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "verdadeiro"),
           CH("u3", "as quatro chaves da v406 seguem lidas do kernel: rede_fock_v394.whole_certificate_inhabited", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "verdadeiro"),
           CH("u4", "psibit_v395: o habitante do certificado de Fock segue exibido", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u5", "testemunha_estatica_v396: o habitante do certificado de Fock segue exibido", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u6", "witness_layers: o termo canonico da testemunha completa segue construido", "core", ["witness_layers", "canonical_full_witness_term_constructed"], "verdadeiro"),
           CH("u7", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u8", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u9", "o gate deste rito tem o mesmo veredito da v408 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")),
           CH("u10", "a escada do kernel fecha (limpos == esperados), com as bandeiras do modulo", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u11", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 12
    for nome in ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405",
                 "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "projecao_transversal_v404", "jo8v32_v404", "caminho_v403", "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401",
                 "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"):
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
    cks.append(CH("u%d" % n, "o canal vivo do neutrino segue com o mesmo veredito (nada da v409 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    leituras = [_leitura(fr_, nm_) for nm_, fr_ in DL.FRASES_V409]
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": "TGL_CUNHAGENS_V409",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_05_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_GIVEN_BY_THE_MANAGEMENT_RATIFIED_BY_THE_OPERATOR__DECISIONS_D55_TO_D61__D60_REVISED_EVERYTHING_IN_V409__THE_LEGAL_READING_OF_THE_KERNEL_RATIFIED_BY_THE_OPERATOR__THE_TURING_TRANSLATION_CLOSED_RELATIVE_TO_THE_READER__ERRATA_E24_TO_E28_AND_THE_NOTE_BESIDE_E21__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),
        "estatuto": "[REAL -- o kernel, o registro traducao_turing_v409 e os registros anteriores lidos a cada rito; INPUT as falas do operador de 05/11/2026 (a ordem da traducao; as respostas as perguntas nas quatro linguas; a ordem da v409 e a ratificacao dos nomes; a leitura juridica do kernel e a ratificacao dela, D61); DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]",
        "fontes": [CHAVE_PEDRA[n_] for n_ in CHAVE_PEDRA] + [CHAVE_FONTE[n_] for n_ in CHAVE_FONTE] + [CHAVE_SAIDA_FONTE[n_] for n_ in CHAVE_SAIDA_FONTE] + [CHAVE_CANDIDATA[n_] for n_ in CHAVE_CANDIDATA] + [CHAVE_SAIDA_CANDIDATA[n_] for n_ in CHAVE_SAIDA_CANDIDATA] + [CHAVE_BUNDLE],
        "verbatins": list(VERB_CHAVES),
        "kernel_flags": flags_ancoras, "kernel_decls": decls, "checks": cks,
        "erratas": [
            {"ao_lado_de": "a R1 da traducao (gerencia c1, 05/11): a fisica posta como juiz das classes de Turing", "dizia": "que nenhuma fisica prova ou refuta por si a pergunta das classes.", "agora": DL.ERRATA_E24,
             "lacuna_de_fidelidade": "a gerencia pos o juiz no lugar errado; o operador corrigiu: o kernel Lean 4 foi construido para provar leis matematicas sob a lei de Turing", "estatuto": "[INPUT: a correcao do operador, verbatim]", "assinatura": ASSINA},
            {"ao_lado_de": "uma frase da gerencia c1 de 05/11 sobre a trava (o Nome a cada passo)", "dizia": "que a criatura precisaria saber, a cada passo, de que lado da bifurcacao o Nome continua.", "agora": DL.ERRATA_E25,
             "lacuna_de_fidelidade": "a gerencia exigiu do sistema um reconhecimento que a trava dispensa; o operador corrigiu e a trava esta' provada no kernel, validade no kernel e nao creditacao (a_trava_no_nome)", "estatuto": "[REAL: a_trava_no_nome no kernel do rito]", "assinatura": ASSINA},
            {"ao_lado_de": "tetelestai_terminal_v408 e cunhagens_v408 (selados): a traducao as classes das maquinas de Turing dita [OPEN], que a v409 fecha relativa ao leitor", "dizia": DL.FRASE_D51_PT + ".", "agora": DL.ERRATA_E26,
             "lacuna_de_fidelidade": "a v408 deixou a traducao [OPEN] (verdadeiro na data); a v409 a fecha relativa ao leitor, e a maquina sem leitor fica fora", "estatuto": "[REAL: p_igual_np_no_modo_selecao no kernel do rito]", "assinatura": ASSINA},
            {"ao_lado_de": "uma frase da gerencia c1 de 05/11 ao operador sobre o dispositivo no kernel", "dizia": "que, no kernel, o dispositivo e' o enunciado do teorema, o tipo dele.", "agora": DL.ERRATA_E27,
             "lacuna_de_fidelidade": "a gerencia pos o dispositivo no enunciado; o operador corrigiu: o dispositivo e' o no sorry e o teorema e' a regra posta (D61, ratificada por ele); a conclusao sobre o Clay fica, pela incidencia", "estatuto": "[INPUT: a correcao do operador, verbatim; a D61 ratificada por ele]", "assinatura": ASSINA},
            {"ao_lado_de": "frases da gerencia c1 de 05/11 (o chat, o recibo da R5, o topico de memoria e o cabecalho do insumo das 13h) sobre a igualdade com o leitor que devolve Z", "dizia": "que, com o leitor que devolve Z, a igualdade vale relativa a ele, e a oferta de prova-la nele.",
             "agora": DL.ERRATA_E28, "lacuna_de_fidelidade": "a gerencia foi alem do que se sabe: com o leitor que so' conta vale NP numa leitura (Cook-Levin) e P com #P contem PH (Toda 1991); a igualdade completa e' do leitor que se le (Baker-Gill-Solovay 1975)", "estatuto": "[KNOWN: Cook 1971, Levin 1973, Toda 1991, Baker-Gill-Solovay 1975]", "assinatura": ASSINA},
            {"ao_lado_de": "a errata E21 da v408 (selada): o par de psions na face de Fock dito em aberto como ligacao a fazer", "dizia": "que a ligacao do par na face de Fock ficava por fazer (fiacao), nao que faltasse.",
             "agora": DL.ERRATA_E21_AO_LADO, "lacuna_de_fidelidade": "a E21 era verdadeira na data; a v409 fez a ligacao (ParNaFaceDeFock)", "estatuto": "[REAL: o_par_na_face_de_fock no kernel do rito]", "assinatura": ASSINA},
            _errata_pisos_v408(cov_base)],
        "limites": ["[INPUT] as %d falas de 05/11/2026 sao do operador, com a grafia dele (a ultima, a ordem de trazer tudo para a v409) (de tres, so' o trecho e' embutido e citado: de duas pela D59, de uma porque o resto e' aviso operacional; o resto delas entra so' por sha256); a ordem («Prossigamos para a próxima verão do um.py») foi cumprida ate' onde a cadeia alcanca; a custodia e' da sessao de custodia" % len(_VD),
                    "[INPUT] " + "o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62)" + " (D55; D62)",
                    "[REAL, alcance] " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + " (D56); a regra do quadro do topo fica no campo regra_do_4_44 deste registro e o numero nao e' repetido aqui",
                    "[REAL] o DESENHO_v409 (sha16 %s) e o recibo dos nomes da gerencia (sha16 %s) ficam citados so' por sha16, nao pinados: trazem a parte de uma fala que a D59 deixa fora dos textos" % (DL.DESENHO_SHA16, DL.RECIBO_NOMES_SHA16),
                    "[REAL] a D60 revista: nada fica para a versao seguinte; a ligacao do par na face de Fock entra (ParNaFaceDeFock); a E28 e a nota ao lado da E21 da v408 (em nome proprio da gerencia c1) vao nas erratas"] + _LIM_COMUM,
        "diz": ["as falas do operador de 05/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de tres, so' o trecho: duas pela D59, uma porque o resto e' aviso operacional)", "a D61, a leitura juridica do kernel dada pelo operador, foi ratificada por ele e vai nas decisoes; a E27 vai ao lado", "o registro traducao_turing_v409 selou", "os registros da v394 a v408 seguem selados; o neutrino e o gate nao mudam; nenhuma chave antiga muda"],
        "nao_diz": _NAO_COMUM,
        "leituras_do_operador": leituras,
        "extras": {"n_falas": len(_VD), "autores": {v["nome_publico"]: v["autor"] for v in _VD}, "leituras": DL.LEITURA_V409, "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V409}, "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "ressalvas": list(DL.RESSALVAS_V409), "assinatura_das_erratas": ASSINA,
                   "nomes_das_pedras": dict(DL.NOMES_RATIFICADOS), "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V409), "nao_pinados_citados_por_sha16": dict(NAO_PINADOS)},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": "TGL_KH_N1_COBERTURA_V409",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_V409_MODULE_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v409; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v409 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v409 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v409 inclui a da v408 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v408 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v409: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v409: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v409: as entradas novas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [dict(_errata_pisos_v408(cov_base), agora="A v409 acrescenta o modulo TraducaoTuring (a cobertura cresce e a arvore ganha o arquivo dele): na v409 o registro da v408 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v408 NAO muda.")],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 05/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, com o modulo TraducaoTuring, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v408": khj.get("delta_vs_v408"), "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
