# -*- coding: utf-8 -*-
"""registros_v407.py -- os dados dos registros da v407: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (as falas do operador de 03/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo),
o CONTRATO e o TEXTO do registro com FUNCAO psion_canto_v407 (gerar_candidato_v407.py os emite a partir de runtime_v407.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox k407c) e os DOIS SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v407` e `kh_n1_cobertura_v407`). A MOLDURA de todo texto daqui: o psion e o canto sao a mesma construcao nas duas faces (o lema le-se do kernel; elo de ESTRUTURA, nao de vetores); o par e' ligado e nunca se cancela; a face de Fock do par segue [OPEN]; a ponte Bell-TT nao e' termo;
os nomes das pedras sao do operador; o teste (d) so' por citacao do pre-registro; o motor continuo fora; validade no kernel nao e' creditacao; o gate nao se move. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v407\\insumos. Texto novo passa pela guarda P18 e pela guarda das frases (v407) a cada rito.
Molde: registros_v406.py."""
import hashlib
import json
import os
import re
import sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v407 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
_snake = lambda s: re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
CHAVE_PEDRA = {p["name"]: "pedra_" + _snake(p["name"]) for p in DL.PEDRAS_V407}      # a pedra normalizada que entra no kernel (copia duravel)
CHAVE_TESTEMUNHA = CHAVE_PEDRA["PsionCanto"]                    # (alias: a pedra que carrega a chave)
CHAVE_CANDIDATA_PSION_R1 = "candidata_psion_canto_r1_03nov"
CHAVE_CANDIDATA_PAR_R1 = "candidata_o_par_de_psions_r1_03nov"
CHAVE_RECIBO_PSION = "recibo_psion_canto_r1_03nov"
CHAVE_RECIBO_PAR = "recibo_o_par_r1_03nov"
CHAVE_SAIDA_PSION = "saida_lean_psion_canto_r1_03nov"
CHAVE_SAIDA_PAR = "saida_lean_par_r1_03nov"
CHAVE_RECIBO_PSION_R2 = "recibo_psion_canto_r2_03nov"      # R2 da gerencia (03/11): a fonte corrigida recompilada no sandbox da v406
CHAVE_RECIBO_PAR_R2 = "recibo_o_par_r2_03nov"
CHAVE_SAIDA_PSION_R2 = "saida_lean_psion_canto_r2_03nov"
CHAVE_SAIDA_PAR_R2 = "saida_lean_par_r2_03nov"
CHAVE_ACERVO = "psion_no_acervo_do_imac_03nov"
CHAVE_REVISAO_PEDRAS = "revisao_pedras_candidatas_sonnet_02nov"
CHAVE_PLANO = "plano_v407_gerencia_03nov"
CHAVE_DESENHO = "desenho_v407_03nov"
CHAVE_BUNDLE = "bundle_v407"
CHAVE_KH = "kh_n1_v407"
CHAVE_TESTE_D = "teste_d_manifesto_parametrizacao_03nov"
CHAVE_FASE9 = "fase9_v2_resultado_23out"
# (nome do insumo, origem) -- copiar_insumos_v407.py copia; o montador le de INS
ORIGENS = ([("%s.lean" % p["name"], p["src"]) for p in DL.PEDRAS_V407]
           + [("PsionCantoR1.lean", DL.PEDRAS_V407[0]["origem"]), ("OParDePsionsR1.lean", DL.PEDRAS_V407[1]["origem"]),
              ("RECIBO_PSION_CANTO_R1_03nov.json", DL.RECIBO_PSION_ARQ), ("RECIBO_O_PAR_R1_03nov.json", DL.RECIBO_PAR_ARQ), ("saida_lean_r2.txt", DL.SAIDA_PSION_ARQ), ("saida_lean_par_r1.txt", DL.SAIDA_PAR_ARQ),
              ("RECIBO_PSION_CANTO_R2_03nov.json", DL.RECIBO_PSION_R2_ARQ), ("RECIBO_O_PAR_R2_03nov.json", DL.RECIBO_PAR_R2_ARQ), ("saida_lean_r3.txt", DL.SAIDA_PSION_R2_ARQ), ("saida_lean_par_r2.txt", DL.SAIDA_PAR_R2_ARQ),
              ("PSION_NO_ACERVO_03nov.md", DL.ACERVO_PSION_ARQ), ("REVISAO_PEDRAS_CANDIDATAS_02nov_SONNET.md", DL.REVISAO_PEDRAS_02NOV_ARQ), ("PLANO_v407_GERENCIA.md", DL.PLANO_ARQ), ("DESENHO_v407.md", DL.DESENHO_ARQ),
              ("BUNDLE_v407.json", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v407.json")), ("MANIFESTO_PARAMETRIZACAO_03nov.json", DL.D_TESTE_MANIFESTO),
              ("RESULTADO_FASE9_V2_C1_20261023_122926.json", DL.FASE9_V2_ARQ)])
_PAPEL_PEDRA = {
    "PsionCanto": "a pedra PsionCanto (gerencia c1, 03/11/2026; nome aceito pelo operador): a condicao sob compressao (A) e o lema das duas faces do psion (B); a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256",
    "Par": "a pedra Par (gerencia c1, 03/11/2026; nome dado pelo operador): o par de psions = o graviton, ligado, nunca cancelado, lido pela fase dobrada e pelo retorno de fase; compoe so' termos que o kernel ja tinha",
}
FONTES = [{"chave": CHAVE_PEDRA[p["name"]], "arquivo": os.path.join(INS, "%s.lean" % p["name"]),
           "papel": _PAPEL_PEDRA.get(p["name"], "a pedra %s (candidata da gerencia c1 de 02/11/2026; nome RATIFICADO pelo operador em 03/11/2026): copia duravel normalizada (modulo sem o sufixo Candidata; nenhuma prova tocada); a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256" % p["name"])} for p in DL.PEDRAS_V407]
FONTES += [
    {"chave": CHAVE_CANDIDATA_PSION_R1, "arquivo": os.path.join(INS, "PsionCantoR1.lean"), "papel": "a fonte de origem da PsionCanto (PsionCantoR1.lean; o R1 do nome do arquivo e' marca de revisao da candidata): a versao R2, com as correcoes de docstring da gerencia c1 de 03/11/2026 sobre a revisao de terceiro (nenhuma prova tocada; sha16 3794f8ccbc6be70b), recompilada no sandbox da v406 (saida_lean_r3.txt) e embutida no kernel da v407 como TGLExt.PsionCanto; a R1 (sha16 ae74b8334c3c0c8e) fica como registro em pedra\\antes_de_*_r2\\origem: so' o modulo, o namespace e o cabecalho mudam na normalizacao [REAL: lido do arquivo]"},
    {"chave": CHAVE_CANDIDATA_PAR_R1, "arquivo": os.path.join(INS, "OParDePsionsR1.lean"), "papel": "a fonte de origem da pedra Par (OParDePsionsR1.lean, o nome provisorio que o operador substituiu por «Par»): a versao R2, com as correcoes de docstring da gerencia c1 de 03/11/2026 (nenhuma prova tocada; sha16 49300efd79bb954e), recompilada no sandbox da v406 (saida_lean_par_r2.txt) e embutida no kernel da v407 como TGLExt.Par; a R1 (sha16 444763c0dc8c4bbc) fica como registro) [REAL: lido do arquivo]"},
    {"chave": CHAVE_RECIBO_PSION, "arquivo": os.path.join(INS, "RECIBO_PSION_CANTO_R1_03nov.json"), "papel": "o recibo da compilacao da PsionCanto no sandbox da v406 (LEAN_RC 0; 8 declaracoes no trio) e o que a pedra prova e NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito] [registro R1: a fonte vigente e' a R2, recibo R2 abaixo]"},
    {"chave": CHAVE_RECIBO_PAR, "arquivo": os.path.join(INS, "RECIBO_O_PAR_R1_03nov.json"), "papel": "o recibo da compilacao da pedra do par no sandbox da v406 (LEAN_RC 0; 5 declaracoes no trio) e o que NAO afirma [DECLARADO pela gerencia na origem; refeito no k407c e no Audit do rito] [registro R1: a fonte vigente e' a R2, recibo R2 abaixo]"},
    {"chave": CHAVE_SAIDA_PSION, "arquivo": os.path.join(INS, "saida_lean_r2.txt"), "papel": "a saida do lean ao compilar a PsionCanto (03/11/2026) [REAL: saida do lean] [registro R1: a saida vigente e' a R2, saida_lean_r3.txt]"},
    {"chave": CHAVE_SAIDA_PAR, "arquivo": os.path.join(INS, "saida_lean_par_r1.txt"), "papel": "a saida do lean ao compilar a pedra do par (03/11/2026) [REAL: saida do lean] [registro R1: a saida vigente e' a R2, saida_lean_par_r2.txt]"},
    {"chave": CHAVE_RECIBO_PSION_R2, "arquivo": os.path.join(INS, "RECIBO_PSION_CANTO_R2_03nov.json"), "papel": "o recibo R2 da PsionCanto: a fonte corrigida pela gerencia (03/11/2026, docstring; nenhuma prova tocada) recompilada no sandbox da v406 (LEAN_RC 0; 8 declaracoes no trio); e' a fonte que entra no kernel da v407 [REAL: saida do lean lida]"},
    {"chave": CHAVE_RECIBO_PAR_R2, "arquivo": os.path.join(INS, "RECIBO_O_PAR_R2_03nov.json"), "papel": "o recibo R2 da pedra Par: a fonte corrigida pela gerencia (03/11/2026) recompilada no sandbox da v406 (LEAN_RC 0; 5 declaracoes no trio); e' a fonte que entra no kernel da v407 [REAL: saida do lean lida]"},
    {"chave": CHAVE_SAIDA_PSION_R2, "arquivo": os.path.join(INS, "saida_lean_r3.txt"), "papel": "a saida do lean ao recompilar a PsionCanto corrigida (R2, 03/11/2026) [REAL: saida do lean]"},
    {"chave": CHAVE_SAIDA_PAR_R2, "arquivo": os.path.join(INS, "saida_lean_par_r2.txt"), "papel": "a saida do lean ao recompilar a pedra Par corrigida (R2, 03/11/2026) [REAL: saida do lean]"},
    {"chave": CHAVE_ACERVO, "arquivo": os.path.join(INS, "PSION_NO_ACERVO_03nov.md"), "papel": "o levantamento do psion, do psibit e do par = graviton no acervo antigo do iMac (2025): o psion como a†|0>, o graviton como o par, as contradicoes anotadas (cancelado/ligado; produto/emaranhado) [DECLARADO pelo agente do levantamento; fontes por sha16 no documento]"},
    {"chave": CHAVE_REVISAO_PEDRAS, "arquivo": os.path.join(INS, "REVISAO_PEDRAS_CANDIDATAS_02nov_SONNET.md"), "papel": "a revisao distinta do Sonnet (02/11/2026) das TRES pedras candidatas KEhATangente, APonteDoAtrito e OUmInscrito: nenhuma reprovada; 7 reparos de docstring aplicados [DECLARADO: revisao sem compilacao propria]"},
    {"chave": CHAVE_PLANO, "arquivo": os.path.join(INS, "PLANO_v407_GERENCIA.md"), "papel": "o plano da v407 (gerencia c1, 03/11/2026): o que entra, o que nao muda, as ressalvas [DECLARADO: plano da gerencia]"},
    {"chave": CHAVE_DESENHO, "arquivo": os.path.join(INS, "DESENHO_v407.md"), "papel": "o desenho da v407 (gerencia c1, 03/11/2026) com as decisoes do operador respondidas em §5-bis [DECLARADO: plano da gerencia]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v407.json"), "papel": "o bundle dos 9 modulos (preparar_bundle_v407_03nov.py): sha256 de cada modulo normalizado, a fonte de origem e o sha256 dela [REAL: lido dos arquivos; o rito confere cada sha256 em formal_files_sha256]"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v407 (pos_build_kernel_v407.py)"},
    {"chave": CHAVE_TESTE_D, "arquivo": os.path.join(INS, "MANIFESTO_PARAMETRIZACAO_03nov.json"), "papel": "o manifesto da parametrizacao do teste (d) do ramo B do ringdown (pre-registro V1.1; 37 arquivos com sha256): so' CITADO nesta versao; nenhum dado de D aberto; nenhum resultado [DECLARADO pelo agente da parametrizacao: smoke 20/20 em sintetico]"},
    {"chave": CHAVE_FASE9, "arquivo": os.path.join(INS, "RESULTADO_FASE9_V2_C1_20261023_122926.json"), "papel": "o resultado da Fase 9 V2 (23/10/2026): a regra do 4,44 (nunca sozinho) e' lida daqui quando o texto cita o z_disc; nenhum numero deste arquivo entra em veredito da v407 [REAL: resultado selado da Fase 9 V2]"},
]
assert len({f["chave"] for f in FONTES}) == len(FONTES) and {os.path.basename(f["arquivo"]) for f in FONTES} == {n for n, _ in ORIGENS}


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins407(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"], "nome": v["nome"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
POR_NOME = {v["nome"]: v for v in _VD}
CH_DE = lambda nome_: POR_NOME[nome_]["chave"]
S16 = lambda nome_: POR_NOME[nome_]["sha16"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
VERBATINS_DO_REGISTRO = [CH_DE(DL.N_ORDEM_B89), CH_DE(DL.N_RATIFICA), CH_DE(DL.N_PAR)]


def _leitura(trecho, nome, rotulo="INPUT do operador"):
    assert trecho in TEXTOS[S16(nome)], ("a leitura do operador NAO esta verbatim na fala", nome, trecho)
    d_ = {"trecho": trecho, "estatuto": "[%s, verbatim 03/11/2026, sha16 %s]" % (rotulo, S16(nome))}
    if "4,44" in trecho:   # a regra do 4,44 (nunca sozinho) vale POR ITEM
        d_["regra_do_4_44"] = DL.REGRA_DO_4_44
    return d_


def _resolver_respostas(core0):
    """Para cada resposta do operador, o NOME COMPLETO (no axiom_report da base) de cada teorema que ja existia: busca pelo ultimo componente; tem de ser unico; devolve {curto: (completo, rel)}. Nada digitado."""
    kf0 = core0["kernel_formalization"]; ax0 = kf0["axiom_report"]; src0 = kf0.get("declaration_sources_v394") or {}
    out = []
    for r in DL.RESPOSTAS_DO_OPERADOR:
        teo = []
        for curto in r["teoremas_curtos"]:
            c = sorted(n for n in ax0 if n.split(".")[-1] == curto and not n.endswith(".eq_1"))
            assert len(c) == 1, ("o teorema citado pela resposta nao e' unico no axiom_report da base", curto, c)
            teo.append({"curto": curto, "completo": c[0], "rel": src0.get(c[0])})
            assert src0.get(c[0]) and set(ax0[c[0]]) <= DL.TRIO_SET
        out.append({"id": r["id"], "fala": r["fala"], "teoremas": teo, "diz": r["diz"]})
    return out


def contrato(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do registro psion_canto_v407, DERIVADO do build do sandbox (fj = FLAGS_v407.json: as bandeiras nomeadas dos 9 modulos, a proveniencia, as ancoras; formal_map = sha256 das fontes embutidas; e_base = a escada da v406 selada); nada digitado.
    core0/selo0 = o core e o selo da v406 SELADA (o veredito do gate que a v407 tem de repetir). Vai para CANDIDATO_v407.json e ESPERADOS_v407.json."""
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    assert len(flag_de) == fj["n_flags"] == len(fj["flags"]) and all(o == DL.ORIGEM_DE_BANDEIRA for _, _, _, o in fj["flags"])
    anc = {}
    for n, a in DL.ANCORAS.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora fora do esperado no FLAGS_v407.json", n, fa)
        assert fa["flag"] == flag_de.get(n), ("a bandeira da ancora no FLAGS nao bate com a lista de bandeiras", n)
        anc[n] = {"rel": a["rel"], "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert all(r in formal_map for r in DL.BUNDLE_RELS)
    decl_src = dict(fj["proveniencia_publicas"]); assert all(v in DL.BUNDLE_RELS for v in decl_src.values())
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict"), "o veredito do gate da base nao e' o do selo"
    resp = _resolver_respostas(core0)
    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V407], "psion_canto": DL.MODULO_PSION, "par": DL.MODULO_PAR, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,
                       "nomes_do_operador": dict(DL.NOME_DO_OPERADOR), "sha16_origem": {p["name"]: p["sha256_origem"][:16] for p in DL.PEDRAS_V407}},
            "source_sha256": {r: formal_map[r] for r in DL.BUNDLE_RELS}, "root_suffix": DL.ROOT_SUFFIX,
            "ancoras": anc, "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_lema": DL.ANCORA_LEMA, "ancora_par": DL.ANCORA_PAR,
            "flags": [f for f, _, _, _ in fj["flags"]], "n_flags": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "excluidas_auxiliares": {"n": fj["excluidas_auxiliares"]["n"], "por_classe": fj["excluidas_auxiliares"]["por_classe"]},
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "chaves": [dict(c) for c in DL.CHAVES_V407], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA),
            "fica_aberto": {"par_na_face_de_fock": DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.FICA_ABERTO_PONTE_BELL_TT},
            "respostas": resp, "chaves_v406": [dict(c) for c in DL.CHAVES_V406],
            "ressalvas": list(DL.RESSALVAS_V407), "verbatins": list(VERBATINS_DO_REGISTRO),
            "teste_d": {"fonte_chave": CHAVE_TESTE_D, "manifesto_sha16": DL.D_TESTE_SHA16_DA_ORDEM, "manifesto_sha256": hashlib.sha256(open(DL.D_TESTE_MANIFESTO, "rb").read()).hexdigest(), "so_citado": True, "resultado_no_um_py": None, "opcao_do_operador": "c (uma analise sintetica para a convergencia, depois as 10 cegas; so' entra com poder)"},
            "regra_do_4_44": DL.REGRA_DO_4_44}


_NAO_COMUM = ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra",
              "que a gravidade quantica esteja creditada: a confirmacao segue proibida (creditacao); o que ha' e' validade no kernel",
              "que Omega (o vacuo de Fock) e Phi+ (o vetor de Bell) sejam o mesmo vetor: o elo das duas faces do psion e' de ESTRUTURA (a mesma construcao «canto escalar de um vetor de norma 1»), em espacos distintos",
              "que o par de psions exista na face de Fock: dois psions sobre o vacuo (a†a†|0>) seguem [OPEN]; o FockCertificate nao tem operadores de criacao como termo",
              "que o espaco de Bell (Fin 2 x Fin 2, C) seja identificado com o setor TT do spin 2 (Fin 4, R): a conjuncao das faces nao e' identificacao",
              "que a condicao posta pelo operador («se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ») tenha sido testada com a natureza: o que o kernel entrega e' a leitura de Jones sob compressao (validade); nao ha' teste de natureza nesta versao",
              "que o teste (d) do ramo B tenha rodado, tenha resultado ou tenha poder: so' o pre-registro V1.1 e' citado; nenhuma PE em dado real",
              "que o motor continuo tenha entrado no pilar quantico: fica fora (D38); a fala «quero conteúdo observável … banho holográfico» e' cunhagem [ONTO], sem termo",
              "que o gate tenha se movido: o veredito e' o mesmo da v406 selada, conferido em runtime", "que K(O) != bot valha para O compacto: so' na cunha (herdado da v406)",
              "que as pedras tenham revisao de terceiro POR DENTRO das provas: em 02/11 o Sonnet reviu tres das sete (docstrings e enunciados); em 03/11 o revisor desta preparacao conferiu as nove por #print axioms, diff contra as origens e docstrings, nao as provas linha a linha"]
_LIM_COMUM = ["o registro CONFERE o que o kernel do proprio rito prova (os termos no trio, a proveniencia, as fontes por sha256) e o que o core deste rito gravou; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
              "[REAL] o que mudou de v406 para v407 nos registros antigos e' SO' o que eles leem: linked_to_the_corner_by_a_lemma deixa de ser literal False e passa a leitura do kernel (errata E18); o fechamento_v406 c8 e o cunhagens_v406 u7 ganham a versao (errata E20); nenhum texto selado e' reescrito",
              "[DECLARADO -> REAL] a construcao das nove pedras e' da gerencia c1 (02 e 03/11/2026): o que a v407 faz e' recompila-las no sandbox k407c e no rito; o parecer do Sonnet sobre tres delas (02/11) e a revisao de terceiro desta preparacao ficam como fontes [DECLARADO]; o que vale no rito e' o Audit do rito"]


def texto_psion():
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras das nove pedras (TGLExt.PsionCanto.* e TGLExt.Par.* incluidos), no trio, com proveniencia no modulo esperado, e os 9 modulos por sha256; "
                    "[REAL] a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma LIDA do kernel (nao literal) e o que fica False por teorema conferido False; [REAL] a escada exata e o beta = alfa CODATA 2018 x sqrt(e) em runtime; "
                    "[INPUT] a ordem do operador (03/11/2026, sha16 %s: «%s»), a decisao (sha16 %s: «%s»; «%s») e o nome do par (sha16 %s: %s); [ONTO] as leituras dele (o graviton como o estado ligado de dois psions; o banho holografico); "
                    "[DECLARADO] o acervo de 2025, os recibos de compilacao e o manifesto do teste (d); [KNOWN/OPEN] K(O) != bot para O compacto; [OPEN] o par na face de Fock; o teste com a natureza: beta a 5 sigma" % (len(DL.ANCORAS), S16(DL.N_ORDEM_B89), DL.FRASE_LEMA_PSION, S16(DL.N_RATIFICA), DL.FRASE_NOME, DL.FRASE_NOMES_RATIFICADOS, S16(DL.N_PAR), DL.FRASE_PAR),
        "escopo": "[REAL] O que entra no um.py: 9 modulos novos em TGLExt/ -- PsionCanto (nome aceito), Par (nome dado) e as sete pedras de 02/11 de nome ratificado (APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual). "
                  "(A) A PsionCanto prova, para todo FockCertificate (binder) e sem hipotese no physicalFockCertificate da v406: psionCornerF escalariza, <psi, Delta^{it} psi> = 1, P Delta^{it} P = P (a leitura de Jones do fluxo da luz pelo canto do psion devolve o canto) e a contracao de Jones e o fluxo da luz leem o mesmo no canto. "
                  "(B) O lema das duas faces (the_psion_is_the_corner_on_both_faces): nas duas faces o psion e' o vetor de norma 1 cujo canto e' o projetor sobre ele; o canto escalariza; pesa 1; o motor comprimido devolve o canto; psionCorner.p = |Phi+><Phi+| (cornerOf bellVec). "
                  "(C) A pedra Par compoe, sob a cunhagem do operador de 03/11, so' termos que o kernel ja tinha: o par e' LIGADO (psionCorner = sombra do graviton, CCI = 1/2; o produto tem CCI = 0), nunca se cancela (idempotente, traco 1; o individuo nao ecoa), a leitura e' a fase dobrada da helicidade 2 com retorno em theta = pi, e o canto e' o projetor 4x4. "
                  "Com o lema, a chave que o um.py trazia como literal False desde a v396 passa a ser LIDA do kernel do proprio rito (errata E18). O registro confere, em runtime: as ancoras; os 9 sha256; a raiz com os nove imports; a chave; as respostas do operador pelos teoremas que ja existiam; as sete pedras de 02/11; o que fica False por teorema; a escada; os registros antigos selados; as bandeiras; a proveniencia; o beta; o gate com o mesmo veredito da base; o teste (d) so' por citacao.",
        "limites": ["[REAL, escopo] " + DL.RESSALVAS_V407[0], "[OPEN] " + DL.RESSALVAS_V407[1], "[REAL, escopo] " + DL.RESSALVAS_V407[2], "[DECLARADO/ONTO] " + DL.RESSALVAS_V407[3], "[OPEN/KNOWN] " + DL.RESSALVAS_V407[4], "[DECLARADO] " + DL.RESSALVAS_V407[5], "[INPUT] " + DL.RESSALVAS_V407[6],
                    "[DECLARADO] " + DL.RESSALVAS_V407[7], "[REAL, teorema] " + DL.RESSALVAS_V407[8], "[INPUT] " + DL.RESSALVAS_V407[9], "[REAL] " + DL.RESSALVAS_V407[10], DL.ERRATA_E18, DL.ERRATA_E19, DL.ERRATA_E20] + _LIM_COMUM,
        "diz": ["os 9 modulos estao no kernel do rito, no trio, com bandeira e proveniencia nos modulos deles; as ancoras sao lidas deste kernel; a fonte de cada modulo e' a pinada (sha256)",
                "o psion e o canto sao a mesma construcao nas duas faces: o lema esta' no kernel e a chave que ligava as duas faces e' lida dele (elo de estrutura, nao de vetores); a leitura de Jones comprime o fluxo da luz no canto e devolve o canto",
                "o par e' ligado e nunca se cancela; o individuo nao ecoa; a leitura e' pela fase dobrada e pelo retorno em pi; o canto e' o projetor 4x4: as tres respostas do operador de 03/11 conferem no kernel, pelos teoremas que ja existiam",
                "o veredito do gate e' o mesmo da v406 selada; nenhum dado novo; nenhum rito de natureza alterado; beta = alfa x sqrt e em runtime"],
        "nao_diz": _NAO_COMUM,
        "extras": {"leituras_do_operador": {k_: v_ for k_, v_ in DL.LEITURA_V407.items()}, "ressalvas": list(DL.RESSALVAS_V407), "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D41", "D42", "D43", "D44", "D45", "D46", "D47")},
                   "regra_do_4_44": DL.REGRA_DO_4_44, "assinatura_das_erratas": ASSINA, "nomes": dict(DL.NOME_DO_OPERADOR)},
        "veredito_ok": "TGL_PSION_CANTO_V407__THE_LEMMA_THAT_LINKS_THE_TWO_FACES_OF_THE_PSION_IS_A_KERNEL_TERM__THE_KEY_IS_READ_FROM_THE_KERNEL_NOT_LITERAL__LINK_OF_STRUCTURE_NOT_OF_VECTORS__"
                       "THE_BOUND_PAIR_NEVER_CANCELS_AND_THE_CORNER_IS_THE_FOUR_BY_FOUR__THE_FOCK_FACE_OF_THE_PAIR_STAYS_OPEN__NINE_MODULES_READ_BY_SHA256__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


texto_fecho = texto_psion          # (alias para os scripts bumpados da v406)


def especs(formal_map, khj, h8_map, fj, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v407; khj = KH_N1_v407.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar; fj = FLAGS_v407.json; cov_base = a cobertura da v406 selada {decl, thm}; core0 = o core da v406 selada.
    Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags_ancoras = [flag_de[n] for n in DL.ANCORAS if flag_de.get(n)]
    resp = _resolver_respostas(core0)
    decls = list(DL.ANCORAS) + [t_["completo"] for r_ in resp for t_ in r_["teoremas"]]   # termos que as respostas citam (nomes EXATOS do Audit, resolvidos no axiom_report da base)
    cks = [CH("u1", "o registro psion_canto_v407 selou neste rito (as ancoras, os 9 sha256, a chave lida, as respostas, a escada, o gate)", "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "a chave do lema e' LIDA do kernel do rito (o lema esta' no axiom_report, no trio, no modulo esperado)", "core", [DL.FECHO_REGISTRO, "link_read_from_the_kernel"], "verdadeiro"),
           CH("u3", "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma passou a leitura do kernel e le True (ate' a v406: literal False; errata E18)", "core", ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "verdadeiro"),
           CH("u4", "as quatro chaves da v406 seguem lidas do kernel: rede_fock_v394.whole_certificate_inhabited", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "verdadeiro"),
           CH("u5", "psibit_v395: o habitante do certificado de Fock segue exibido", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u6", "testemunha_estatica_v396: o habitante do certificado de Fock segue exibido", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u7", "witness_layers: o termo canonico da testemunha completa segue construido", "core", ["witness_layers", "canonical_full_witness_term_constructed"], "verdadeiro"),
           CH("u8", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u9", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u10", "o gate deste rito tem o mesmo veredito da v406 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")),
           CH("u11", "a escada do kernel fecha (limpos == esperados), com as bandeiras dos 9 modulos", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u12", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 13
    for nome in ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405",
                 "projecao_transversal_v404", "jo8v32_v404", "caminho_v403", "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401", "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"):
        cks.append(CH("u%d" % n, "o registro %s segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for nm_ in (DL.ANCORA_LEMA, DL.ANCORA_PAR):
        cks.append(CH("u%d" % n, "o compilador emite a ancora %s no modulo esperado (TGL_DECL_SOURCE)" % nm_.split(".")[-1], "kf", ["declaration_sources_v394", nm_], "igual", DL.ANCORAS[nm_]["rel"])); n += 1
    for r_ in resp:
        for t_ in r_["teoremas"]:
            cks.append(CH("u%d" % n, "a resposta %s do operador cita %s, que ja existia: o compilador a emite no modulo de sempre" % (r_["id"], t_["curto"]), "kf", ["declaration_sources_v394", t_["completo"]], "igual", t_["rel"])); n += 1
    for rel_ in DL.BUNDLE_RELS:
        cks.append(CH("u%d" % n, "o modulo %s no kernel do rito e' EXATAMENTE o pinado (sha256 da fonte)" % rel_.split("/")[-1], "kf", ["formal_files_sha256", rel_], "igual", formal_map[rel_])); n += 1
    cks.append(CH("u%d" % n, "o canal vivo do neutrino segue com o mesmo veredito (nada da v407 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    leituras = [_leitura(fr_, nm_) for nm_, fr_ in DL.FRASES_V407]
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": "TGL_CUNHAGENS_V407",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_03_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_OF_THE_STONES__THE_BOUND_PAIR_THE_FOUR_BY_FOUR_CORNER__THE_KEY_READ_FROM_THE_KERNEL__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),
        "estatuto": "[REAL -- o kernel, o registro psion_canto_v407 e os registros anteriores lidos a cada rito; INPUT/ONTO as falas do operador de 03/11/2026; INPUT as ordens (testar a condicao; o lema; prossigamos com tudo; o teste (d) com poder; app e JEV atualizados); DECLARADO o acervo de 2025, os recibos e o manifesto do teste (d)]",
        "fontes": [CHAVE_PEDRA[p["name"]] for p in DL.PEDRAS_V407] + [CHAVE_CANDIDATA_PSION_R1, CHAVE_CANDIDATA_PAR_R1, CHAVE_RECIBO_PSION, CHAVE_RECIBO_PAR, CHAVE_SAIDA_PSION, CHAVE_SAIDA_PAR, CHAVE_RECIBO_PSION_R2, CHAVE_RECIBO_PAR_R2, CHAVE_SAIDA_PSION_R2, CHAVE_SAIDA_PAR_R2, CHAVE_ACERVO, CHAVE_REVISAO_PEDRAS, CHAVE_PLANO, CHAVE_DESENHO, CHAVE_BUNDLE, CHAVE_TESTE_D, CHAVE_FASE9],
        "verbatins": list(VERB_CHAVES),
        "kernel_flags": flags_ancoras, "kernel_decls": decls, "checks": cks,
        "erratas": [
            {"ao_lado_de": "testemunha_estatica_v396 (fock_face.linked_to_the_corner_by_a_lemma): o literal False da v396 a v406; e a frase «nenhum lema liga psion C ao psionCorner» das secoes e registros dessas versoes",
             "dizia": "linked_to_the_corner_by_a_lemma = False; «no lemma identifies psion C with the psionCorner of this stone».", "agora": DL.ERRATA_E18,
             "lacuna_de_fidelidade": "estrutura: a chave era um literal, nao uma leitura; escrito: o literal dizia o estado da data (nenhum lema); a gerencia derivou o lema em 03/11 (a ordem do operador: «o lema que liga o psion ao canto também já pode ser derivado»); onde a traducao falha: o elo e' de ESTRUTURA (canto escalar de um vetor de norma 1), nao identifica Omega com Phi+",
             "estatuto": "[REAL: o lema no kernel do rito; DECLARADO: o recibo da compilacao no sandbox da v406]", "assinatura": ASSINA},
            {"ao_lado_de": "o texto do ACOM/INPI de 2025 («psi+ psi- cancelado = vacuo»; graviton = psi+ psi+) e a frase da Fronteira de 02/2026 («|G> como produto nao emaranhado»)", "dizia": "o par psi+ psi- e' cancelado (= vacuo) / o graviton e' um produto nao emaranhado.", "agora": DL.ERRATA_E19,
             "lacuna_de_fidelidade": "a estratigrafia do acervo: textos de datas diferentes dizem coisas contrarias sobre o mesmo par; a cunhagem do operador de 03/11 decide (o par e' ligado); os textos antigos ficam como registro", "estatuto": "[INPUT: a cunhagem do operador; DECLARADO: o levantamento do acervo; REAL: o par ligado, CCI = 1/2, no kernel]", "assinatura": ASSINA},
            {"ao_lado_de": "fechamento_v406 (c8) e cunhagens_v406 (u7): o lema que falta segue False", "dizia": "c8/u7 cobravam linked_to_the_corner_by_a_lemma == False.", "agora": DL.ERRATA_E20,
             "lacuna_de_fidelidade": "um registro preso a um estado que a versao seguinte muda (a mesma lacuna das versoes anteriores)", "estatuto": "[REAL: conferido no ensaio a seco]", "assinatura": ASSINA}],
        "limites": ["[INPUT] as %d falas de 03/11/2026 sao do operador, com a grafia dele; as ordens («prossigamos com tudo, ratifico tudo»; «concordo com c, porque se o teste não tiver poder não vou inseri-lo no um.py») foram cumpridas nesta versao ate' onde a cadeia alcanca; a publicacao e a atualizacao sao a custodia, depois do rito" % len(_VD),
                    "[ONTO] o graviton como o estado ligado de dois psions (a tensao irresoluvel no plano), o banho holografico como energia escura funcionando: leituras do operador, nao termos de kernel; os correlatos [KNOWN] estao ditos em LEITURA_V407",
                    "[INPUT] o app e o contrato do JEV «sempre atualizados … podia ser até automático» e o orquestrador executar o que a gerencia mandar sao engenharia da casa, fora do um.py (passo S10 do orquestrador); o motor continuo no pilar quantico fica fora; " + DL.REGRA_DO_4_44,
                    "[INPUT] o «Vai» para a Torre (fala sha16 57250bbbaca9fd39) e' ordem de engenharia da casa, fora do um.py"] + _LIM_COMUM,
        "diz": ["as falas do operador de 03/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim", "o registro psion_canto_v407 selou e a chave do lema le o kernel", "os registros da v394 a v406 seguem selados; o neutrino e o gate nao mudam"],
        "nao_diz": _NAO_COMUM,
        "leituras_do_operador": leituras,
        "extras": {"n_falas": len(_VD), "leituras": DL.LEITURA_V407, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D41", "D42", "D43", "D44", "D45", "D46", "D47")}, "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "ressalvas": list(DL.RESSALVAS_V407), "assinatura_das_erratas": ASSINA,
                   "nomes_das_pedras": dict(DL.NOME_DO_OPERADOR)},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": "TGL_KH_N1_COBERTURA_V407",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_9_V407_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v407; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v407 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v407 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v407 inclui a da v406 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v406 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v407: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v407: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v407: as entradas novas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v406 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v406 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v406 e o hash formal igual ao pino exato da arvore da v406." % (int(cov_base["decl"]), int(cov_base["thm"])),
                     "agora": "A v407 acrescenta os 9 modulos (a cobertura cresce e a arvore ganha os arquivos deles): na v407 o registro da v406 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v406 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v406 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v407 quebra (a mesma lacuna desde a v399)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 03/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, com os 9 modulos, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v406": khj.get("delta_vs_v406"), "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
