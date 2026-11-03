# -*- coding: utf-8 -*-
"""registros_v406.py -- os dados dos registros da v406: FONTES pinadas por sha256 (lidas do disco pelo montador, nunca digitadas), VERBATINS (TODAS as falas do operador de 02/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo),
o CONTRATO e o TEXTO do registro com FUNCAO fechamento_v406 (gerar_candidato_v406.py os emite a partir de runtime_v406.py; o contrato sai de contrato() abaixo, DERIVADO do build do sandbox k406c) e os DOIS SPECS interpretados pelo MOTOR _v392_registro
(`cunhagens_v406` e `kh_n1_cobertura_v406`). A MOLDURA de todo texto daqui: o certificado de Fock esta' habitado por construcao no kernel do rito (physicalFockCertificate, bancada do ChatGPT, 16/10/2026; recompilado do fonte em 02/11); as quatro chaves de testemunha
sao lidas do kernel, nao literais; as ressalvas (K(O) != bot so' na cunha; «nucleo II_inf» [KNOWN/DECLARADO]; traco ENNReal ciclico, nao linear; R7 Codex x Codex; R4/R5 fora; duas chaves False por teorema; nome provisorio) vao ditas; validade no kernel nao e' creditacao;
o gate nao se move. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v406\\insumos. Texto novo passa pela guarda P18 e pela guarda das frases (v406) a cada rito. Molde: registros_v405.py."""
import hashlib
import json
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v406 as DL  # noqa: E402

INS = os.path.join(HERE, "insumos")
ASSINA = DL.ASSINA
CHAVE_TESTEMUNHA = "candidata_canonical_full_tgl_witness_r1"
CHAVE_RATIFICACAO = "ratificacao_r10_c1_02nov"
CHAVE_REVISAO_SONNET = "revisao_r10_cadeia_do_traco_sonnet_02nov"
CHAVE_DESENHO = "desenho_v406_02nov"
CHAVE_ORDEM_LOGICA = "ordem_logica_do_fechamento_02nov"
CHAVE_LEVANTAMENTO = "levantamento_fronteira_do_traco_02nov"
CHAVE_BUNDLE = "bundle_v406"
CHAVE_MANIFEST_INTEGRACAO = "manifest_integracao_r3_02nov"
CHAVE_SUMMARY_INTEGRACAO = "summary_integracao_r3_02nov_passada_2"
CHAVE_SUMMARY_INTEGRACAO_1 = "summary_integracao_r3_02nov_passada_1"
CHAVE_CHECK_AXIOMS = "check_axioms_integracao_r3_02nov"
CHAVE_DRIVER_INTEGRACAO = "driver_integracao_r3_02nov"
CHAVE_RECEIPT_BANCADA = "receipt_bancada_f1_fecho_16out"
CHAVE_AXIOMS_BANCADA = "axioms_bancada_f1_fecho_16out"
CHAVE_R52 = "parecer_r52_r7_full_review_r1_16out"
CHAVE_TESTEMUNHA_SAIDA = "candidata_saida_lean_02nov"
CHAVE_KH = "kh_n1_v406"
CHAVE_FASE9 = "fase9_v2_resultado_23out"
# (nome do insumo, origem) -- copiar_insumos_v406.py copia; o montador le de INS
ORIGENS = [(DL.TESTEMUNHA["insumo"], DL.TESTEMUNHA["src"]), ("RATIFICACAO_R10_c1_02nov.md", DL.RATIFICACAO_ARQ), ("REVISAO_R10_CADEIA_DO_TRACO_SONNET_02nov.md", DL.REVISAO_SONNET_ARQ), ("DESENHO_v406.md", DL.DESENHO_ARQ),
           ("ORDEM_LOGICA_DO_FECHAMENTO_02nov.md", DL.ORDEM_LOGICA_ARQ), ("LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md", DL.LEVANTAMENTO_ARQ), ("BUNDLE_v406.json", DL.BUNDLE_ARQ),
           ("MANIFEST_integracao_R3_20261102_192452.json", DL.MANIFEST_INTEGRACAO_ARQ), ("SUMMARY_integracao_R3_20261102_192452.json", DL.SUMMARY_INTEGRACAO_ARQ), ("SUMMARY_integracao_R3_20261102_184921.json", DL.SUMMARY_INTEGRACAO_1_ARQ),
           ("CHECK_axioms_integracao_R3_20261102_192452.txt", DL.CHECK_AXIOMS_ARQ), ("integrar_fecho_bancada_02nov.py", DL.DRIVER_INTEGRACAO_ARQ), ("RECEIPT_bancada_20261016T210640_174717Z.json", DL.RECEIPT_BANCADA_ARQ),
           ("AXIOMS_bancada_20261016T210640_174717Z.txt", DL.AXIOMS_BANCADA_ARQ), ("R52_R7_FULL_REVIEW_R1.json", DL.R52_PARECER_ARQ), ("CanonicalFullTGLWitnessR1_saida.txt", DL.TESTEMUNHA_SAIDA_ARQ),
           (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v406.json")), ("RESULTADO_FASE9_V2_C1_20261023_122926.json", DL.FASE9_V2_ARQ)]
FONTES = [
    {"chave": CHAVE_TESTEMUNHA, "arquivo": os.path.join(INS, DL.TESTEMUNHA["insumo"]), "papel": "a candidata CanonicalFullTGLWitnessR1 (gerencia c1, 02/11/2026; nome PROVISORIO: os nomes das pedras sao do operador): canonicalFullTGLWitness := <lightNet physicalFockCertificate, lightRealization physicalFockCertificate>; copia duravel; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v406 (pos_build_kernel_v406.py)"},
    {"chave": CHAVE_RATIFICACAO, "arquivo": os.path.join(INS, "RATIFICACAO_R10_c1_02nov.md"), "papel": "a RATIFICACAO R10 da gerencia c1 (02/11/2026): o que foi lido na fonte (o traco ciclico, o 1 de P_F pela calibracao dual, as metades, o habitante dos 21 campos, a rede fisica, o recibo), as ressalvas e o veredito RATIFICADO como validade [DECLARADO na origem: ato da gerencia; o kernel do rito confere os termos]"},
    {"chave": CHAVE_REVISAO_SONNET, "arquivo": os.path.join(INS, "REVISAO_R10_CADEIA_DO_TRACO_SONNET_02nov.md"), "papel": "a revisao distinta da cadeia do traco pelo Sonnet (02/11/2026; ordem do operador: «designe para o Sonnet revisar tudo»): 21 campos, nenhum SUSPEITO, 17 HONESTO, 4 HONESTO COM RESSALVA (trace, PF, Pp, Pm) [DECLARADO: revisao sem compilacao propria; a compilacao independente e' a integracao R3]"},
    {"chave": CHAVE_DESENHO, "arquivo": os.path.join(INS, "DESENHO_v406.md"), "papel": "o desenho da v406 (gerencia c1, 02/11/2026): o que entra, o contrato do fechamento, as quatro chaves, os textos, os tempos, a ordem de execucao [DECLARADO: plano da gerencia]"},
    {"chave": CHAVE_ORDEM_LOGICA, "arquivo": os.path.join(INS, "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md"), "papel": "a ordem logica do fechamento (gerencia c1, 02/11/2026, com tres erratas ao lado): passagem -> rede -> montagem; a prioridade do operador [DECLARADO]"},
    {"chave": CHAVE_LEVANTAMENTO, "arquivo": os.path.join(INS, "LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md"), "papel": "o levantamento da fronteira do traco do nucleo (02/11/2026): o que ja' estava construido na bancada e a gerencia nao tinha lido (errata E16) [DECLARADO: leitura; conferida nas fontes]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v406.json"), "papel": "o bundle dos 301 modulos (preparar_bundle_v406_02nov.py): sha256 de cada modulo normalizado, a fonte da bancada e o sha256 dela ANTES da normalizacao, os #eval removidos, o status da integracao [REAL: lido dos arquivos; o rito confere cada sha256 em formal_files_sha256]"},
    {"chave": CHAVE_MANIFEST_INTEGRACAO, "arquivo": os.path.join(INS, "MANIFEST_integracao_R3_20261102_192452.json"), "papel": "o MANIFEST da integracao R3 (as duas passadas; 02/11/2026): 475 fontes conferidas por sha256 contra o recibo da bancada; 174 identicas ao kernel; 1 conflito (o kernel prevalece); 300 novos compilados do fonte, 0 falhas, 0 bloqueados [REAL: medido pelo driver]"},
    {"chave": CHAVE_SUMMARY_INTEGRACAO, "arquivo": os.path.join(INS, "SUMMARY_integracao_R3_20261102_192452.json"), "papel": "o resumo da segunda passada da integracao R3 (os 15 restantes, retomando os 285) [REAL]"},
    {"chave": CHAVE_SUMMARY_INTEGRACAO_1, "arquivo": os.path.join(INS, "SUMMARY_integracao_R3_20261102_184921.json"), "papel": "o resumo da primeira passada da integracao R3 (285 compilados; 1 falha por #eval multilinha, corrigida no driver; 14 bloqueados por ela) [REAL]"},
    {"chave": CHAVE_CHECK_AXIOMS, "arquivo": os.path.join(INS, "CHECK_axioms_integracao_R3_20261102_192452.txt"), "papel": "o #print axioms das quatro ancoras do topo no sandbox integrado (rc 0): modularCoreInput, physicalModularCoreInput, physicalFockCertificate e physical_trace dependem so' do trio [REAL: saida do lean]"},
    {"chave": CHAVE_DRIVER_INTEGRACAO, "arquivo": os.path.join(INS, "integrar_fecho_bancada_02nov.py"), "papel": "o driver da integracao R3 (gerencia c1, 02/11/2026): le o recibo da bancada como manifesto, normaliza imports e remove blocos #eval, compila com o lean do sandbox, confere os axiomas [REAL: o codigo que mediu]"},
    {"chave": CHAVE_RECEIPT_BANCADA, "arquivo": os.path.join(INS, "RECEIPT_bancada_20261016T210640_174717Z.json"), "papel": "o recibo da bancada do ChatGPT (16/10/2026): exit_code 0, Lean 4.31.0, 474 modulos compilados listados com sha256 (453 .lean + 1 fonte no recibo); a integracao R3 conferiu 475 fontes .lean (os modulos + a raiz), todas no disco e integras em 02/11 [DECLARADO na origem: o ChatGPT; conferido por sha256 pela integracao]"},
    {"chave": CHAVE_AXIOMS_BANCADA, "arquivo": os.path.join(INS, "AXIOMS_bancada_20261016T210640_174717Z.txt"), "papel": "os axiomas da bancada (16/10/2026): 0 sorryAx; modularCoreInput no trio [DECLARADO na origem; refeito na integracao e no Audit do rito]"},
    {"chave": CHAVE_R52, "arquivo": os.path.join(INS, "R52_R7_FULL_REVIEW_R1.json"), "papel": "o parecer R7 da missao da bancada (Codex revisando Codex, 16/10/2026): PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE, 21 campos, com o escopo declarado (traco ENNReal ciclico, nao linear; sem II_inf; sem Fock-torre) [DECLARADO na origem]"},
    {"chave": CHAVE_TESTEMUNHA_SAIDA, "arquivo": os.path.join(INS, "CanonicalFullTGLWitnessR1_saida.txt"), "papel": "a saida do lean ao compilar a candidata no sandbox integrado (02/11/2026): as tres declaracoes no trio [REAL: saida do lean]"},
    {"chave": CHAVE_FASE9, "arquivo": os.path.join(INS, "RESULTADO_FASE9_V2_C1_20261023_122926.json"), "papel": "o resultado da Fase 9 V2 (23/10/2026): a regra do 4,44 (nunca sozinho) e' lida daqui quando o texto cita o z_disc; nenhum numero deste arquivo entra em veredito da v406 [REAL: resultado selado da Fase 9 V2]"},
]
assert len({f["chave"] for f in FONTES}) == len(FONTES) and {os.path.basename(f["arquivo"]) for f in FONTES} == {n for n, _ in ORIGENS}


def _trecho(t):
    s = t.strip().splitlines()[-1].strip() if t.strip() else ""     # a ultima linha da fala
    s = s[:48].rstrip()
    assert s and s in t, s
    return s


_VD = DL.verbatins406(os.path.join(INS, "cunhagens"))
VERBATINS = [{"chave": v["chave"], "arquivo": v["arquivo"], "quando": v["quando"], "trechos": [_trecho(v["text"])], "papel": v["papel"], "fonte_original": v["fonte_original"], "nome": v["nome"]} for v in _VD]
VERB_CHAVES = [v["chave"] for v in _VD]
POR_NOME = {v["nome"]: v for v in _VD}
CH_DE = lambda nome_: POR_NOME[nome_]["chave"]
S16 = lambda nome_: POR_NOME[nome_]["sha16"]
TEXTOS = {v["sha16"]: v["text"] for v in _VD}
CH = lambda id_, desc_, onde_, caminho_, op_, valor_=None, cap_=None, est_="[REAL]": dict(id=id_, descricao=desc_, onde=onde_, caminho=caminho_, op=op_, **({"valor": valor_} if valor_ is not None else {}), **({"capturar": cap_} if cap_ else {}), estatuto=est_)
VERBATINS_DO_REGISTRO = [CH_DE(DL.N_CONSTRUIR), CH_DE(DL.N_PASSAGEM), CH_DE(DL.N_ESPELHO), CH_DE(DL.N_PONTE_ACOM), CH_DE(DL.N_AUTOVETOR), CH_DE(DL.N_COMPRIMIDA), CH_DE(DL.N_COMPILE), CH_DE(DL.N_SONNET)]


def _leitura(trecho, nome, rotulo="INPUT do operador"):
    assert trecho in TEXTOS[S16(nome)], ("a leitura do operador NAO esta verbatim na fala", nome, trecho)
    d_ = {"trecho": trecho, "estatuto": "[%s, verbatim 02/11/2026, sha16 %s]" % (rotulo, S16(nome))}
    if "4,44" in trecho:   # a regra do 4,44 (nunca sozinho) vale POR ITEM: o trecho dele traz o numero, o item traz as companhias
        d_["regra_do_4_44"] = DL.REGRA_DO_4_44
    return d_


def contrato(fj, formal_map, e_base, base_sha256, core0, selo0):
    """O contrato do fechamento, DERIVADO do build do sandbox (fj = FLAGS_v406.json: as bandeiras nomeadas dos 301 modulos, a proveniencia, as ancoras; formal_map = sha256 das fontes embutidas; e_base = a escada da v405 selada); nada digitado.
    core0/selo0 = o core e o selo da v405 SELADA (o veredito do gate que a v406 tem de repetir). Vai para CANDIDATO_v406.json e ESPERADOS_v406.json."""
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    assert len(flag_de) == fj["n_flags"] == len(fj["flags"]) and all(o == "fecho_nomeada" for _, _, _, o in fj["flags"])
    anc = {}
    for n, a in DL.ANCORAS.items():
        fa = fj["ancoras"][n]
        assert fa["rel"] == a["rel"] and set(fa["axioms"]) <= DL.TRIO_SET and fa["axioms"], ("ancora fora do esperado no FLAGS_v406.json", n, fa)
        assert fa["flag"] == flag_de.get(n), ("a bandeira da ancora no FLAGS nao bate com a lista de bandeiras", n)
        anc[n] = {"rel": a["rel"], "papel": a["papel"], "flag": fa["flag"], "classe": fa["classe"]}
    assert all(r in formal_map for r in DL.BUNDLE_RELS)
    decl_src = dict(fj["proveniencia_publicas"]); assert all(v.startswith("TGLExt/F1Fecho394/") for v in decl_src.values())
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict"), "o veredito do gate da base nao e' o do selo"
    return {"bundle": {"n": DL.N_BUNDLE, "da_bancada": len(DL.BUNDLE_DA_BANCADA), "da_gerencia": DL.BUNDLE_DA_GERENCIA, "topo": DL.MODULO_TOPO, "rede": DL.MODULO_REDE, "candidata": DL.MODULO_TESTEMUNHA,
                       "eval_removidos": {"blocos": DL.N_EVAL_BLOCOS, "modulos": DL.N_EVAL_MODULOS, "marcadores": ["IO.println", "IO.FS.withFile"], "nota": "instrumentacao da bancada removida pela integracao R3; nenhum bloco em prova; contagem LIDA do BUNDLE_v406.json"}},
            "source_sha256": {r: formal_map[r] for r in DL.BUNDLE_RELS}, "root_suffix": DL.ROOT_SUFFIX,
            "ancoras": anc, "ancora_certificado": DL.ANCORA_CERTIFICADO, "ancora_testemunha": DL.ANCORA_TESTEMUNHA, "ancora_testemunha_teorema": DL.ANCORA_TESTEMUNHA_TEOREMA,
            "flags": [f for f, _, _, _ in fj["flags"]], "n_flags": fj["n_flags"], "declarations": sorted(decl_src), "declaration_sources": decl_src, "n_declarations_public": len(decl_src),
            "excluidas_auxiliares": {"n": fj["excluidas_auxiliares"]["n"], "por_classe": fj["excluidas_auxiliares"]["por_classe"]},
            "expected_ladder": e_base + fj["n_flags"], "baseline": {"version": DL.BASE_VERSION, "sha256": base_sha256, "gate_verdict": gate0, "ladder": e_base},
            "chaves": [dict(c) for c in DL.CHAVES_V406], "status_habitado": DL.STATUS_HABITADO, "status_antigo": DL.STATUS_ANTIGO, "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_false_sem_lema": DL.FICA_FALSE_SEM_LEMA,
            "ressalvas": list(DL.RESSALVAS_V406), "candidata": {"rel": DL.MODULO_TESTEMUNHA, "sha16_da_ordem": DL.TESTEMUNHA["sha16_da_ordem"], "nome_provisorio_da_gerencia": DL.TESTEMUNHA["nome_provisorio_da_gerencia"]},
            "verbatins": list(VERBATINS_DO_REGISTRO), "bancada": {"missao": "F1.FECHO_20261015 (ChatGPT, 15 e 16/10/2026)", "recibo": "orbital_rotation/attempts/20261016T210640_174717Z/RECEIPT.json", "parecer": "R52_R7_FULL_REVIEW_R1.json (R7, Codex x Codex)"},
            "integracao_r3": {"passadas": ["20261102_184921", "20261102_192452"], "compilados": 300, "falhas": 0, "bloqueados": 0, "fontes_conferidas_por_sha256": 475},
            "regra_do_4_44": DL.REGRA_DO_4_44}


_NAO_COMUM = ["que isto seja um teste com a natureza: nao ha' desfecho experimental; nenhum dado novo entra", "que a gravidade quantica esteja creditada: a confirmacao segue proibida (creditacao); o que ha' e' validade no kernel",
              "que a condicao posta pelo operador na fala da prioridade («se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ») tenha sido testada: nao ha' teste disso nesta versao (o motor continuo no pilar fica para a v407, com pre-registro)",
              "que o gate tenha se movido: o veredito e' o mesmo da v405 selada, conferido em runtime", "que K(O) != bot valha para O compacto: so' na cunha", "que o traco do nucleo seja um funcional linear: e' ENNReal e ciclico sobre a relacao de deslocamento",
              "que «nucleo II_inf» seja resultado do habitante: e' [KNOWN/DECLARADO] no docstring", "que o nome CanonicalFullTGLWitnessR1 seja do operador: e' provisorio da gerencia; os nomes das pedras sao dele",
              "que as pedras candidatas do dia (APonteDoAtrito, OUmInscrito, KEhATangente e as demais) estejam no kernel desta versao: ficam fora ate' que ele as nomeie", "que o motor continuo tenha entrado no pilar quantico: fica para a v407, com pre-registro"]
_LIM_COMUM = ["o registro CONFERE o que o kernel do proprio rito prova (os termos no trio, a proveniencia, as fontes por sha256) e o que o core deste rito gravou; nao prova nada por si: quem prova e' o kernel; validade no kernel nao e' creditacao; o gate nao se move; nao e' teste: nao acrescenta rito, dado nem desfecho",
              "[REAL] o que mudou de v405 para v406 nos registros antigos e' SO' o que eles leem: whole_certificate_inhabited, inhabitant_exhibited (duas vezes) e o status deixam de ser literal e passam a leitura do kernel (errata E14); os specs que cobravam «falso» ganham a versao (errata E17); nenhum texto selado e' reescrito",
              "[DECLARADO -> REAL] a construcao dos 300 modulos e' da bancada do ChatGPT (16/10/2026): o que a v406 faz e' recompila-los do fonte no sandbox (integracao R3, 0 falhas) e de novo no sandbox k406c e no rito; o parecer R7 (Codex x Codex) e a revisao do Sonnet (02/11) ficam como fontes [DECLARADO]; o que vale no rito e' o Audit do rito"]


def texto_fecho():
    return {
        "estatuto": "[REAL] os termos do kernel do rito: as oito ancoras (modularCoreInput, physicalModularCoreInput, physicalFockCertificate, physical_trace, physicalCanonicalNet, physical_canonical_net_nonzero, canonicalFullTGLWitness, canonical_full_witness_inhabited), no trio, com proveniencia no modulo esperado, e os 301 modulos por sha256; "
                    "[REAL] as quatro chaves de testemunha LIDAS do kernel (nao literais) e o que fica False por teorema conferido False; [REAL] a escada exata e o beta = alfa CODATA 2018 x sqrt(e) em runtime; "
                    "[INPUT] a ordem do operador (02/11/2026, sha16 %s: «%s»), a prioridade (sha16 %s: «%s») e a ordem de compilar (sha16 %s); [ONTO] as leituras dele (o espelhamento tipo I / tipo III; o Um inscrito como o unico vetor fixo da luz; o Um absoluto como a luz comprimida pelo ACOM); "
                    "[DECLARADO] a ratificacao R10 da gerencia, o parecer R7 e a revisao do Sonnet; [KNOWN/OPEN] K(O) != bot para O compacto, Reeh-Schlieder; [OPEN] o teste com a natureza: beta a 5 sigma" % (S16(DL.N_CONSTRUIR), DL.FRASE_CONSTRUIR, S16(DL.N_PASSAGEM), DL.FRASE_PASSAGEM, S16(DL.N_COMPILE)),
        "escopo": "[REAL] O fechamento que entra no um.py: 301 modulos novos em TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, missao F1.FECHO_20261015, recompilados do fonte; e a candidata CanonicalFullTGLWitnessR1). O topo (CanonicalFockModularCoreInputR1) habita, para todo D : CanonicalNetInput, "
                  "os 21 campos de RemainingModularCoreInput D (a passagem para o continuo: o traco ciclico cyclicTraceCandidate; P_F = positiveAsCore (add leftPositive rightPositive) com traco 1 pela calibracao dual; as metades iguais pelo split normalizado; a aditividade por value_add) e, sobre a rede fisica "
                  "physicalCanonicalNet (K := compactPhysicalNet; monotonia, localidade, translacao, boost e a cola da cunha sao teoremas; nao-trivialidade NA CUNHA), o certificado physicalFockCertificate := physicalModularCoreInput.toCertificate, com physical_trace por rfl. A candidata monta o termo canonico "
                  "canonicalFullTGLWitness := <lightNet physicalFockCertificate, lightRealization physicalFockCertificate> : FullTGLWitness, e por ele Nonempty FullTGLWitness. Com isso as QUATRO chaves de testemunha que o um.py trazia como literal False desde a v394 (rede_fock_v394.whole_certificate_inhabited; "
                  "psibit_v395.conditional_psion_face.inhabitant_exhibited; testemunha_estatica_v396.fock_face.inhabitant_exhibited; witness_layers.canonical_full_witness_term_constructed) passam a ser LIDAS do kernel do proprio rito, com errata E14 ao lado. "
                  "O registro confere, em runtime: as oito ancoras; os 301 sha256; a raiz com os dois imports; as quatro chaves; o que fica False por teorema (full_static_witness_exists, trivial_inhabitant_exists) e o lema que falta (linked_to_the_corner_by_a_lemma); a escada; os tres registros antigos selados; as bandeiras; a proveniencia; o beta; o gate com o mesmo veredito da base.",
        "limites": ["[OPEN/KNOWN] " + DL.RESSALVAS_V406[0], "[KNOWN/DECLARADO] " + DL.RESSALVAS_V406[1], "[REAL, escopo] " + DL.RESSALVAS_V406[2], "[DECLARADO] " + DL.RESSALVAS_V406[3], "[REAL] " + DL.RESSALVAS_V406[4], "[INPUT] " + DL.RESSALVAS_V406[5],
                    "[REAL, teorema] " + DL.RESSALVAS_V406[6], "[INPUT] " + DL.RESSALVAS_V406[7], "[DECLARADO/REAL] " + DL.RESSALVAS_V406[8], "[REAL, ao lado] " + DL.RESSALVAS_V406[9], DL.ERRATA_E14, DL.ERRATA_E15, DL.ERRATA_E16, DL.ERRATA_E17] + _LIM_COMUM,
        "diz": ["os 301 modulos do fecho estao no kernel do rito, no trio, com bandeira e proveniencia nos modulos deles; as oito ancoras sao lidas deste kernel; a fonte de cada modulo e' a pinada (sha256)",
                "o certificado de Fock esta' habitado por construcao (physicalFockCertificate) e a passagem para o continuo (modularCoreInput) e' termo para todo CanonicalNetInput: quanto ao TERMO, a chave que o operador pediu para virar («virar essa chave de conjectura para provado») virou validade no kernel; a condicao que ele pos na mesma fala («se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ») NAO e' testada nesta versao; a creditacao segue recusada",
                "as quatro chaves de testemunha sao lidas do kernel e leem True; as duas chaves que ficam False ficam False por teorema; o lema que liga psion C ao psionCorner segue faltando",
                "o veredito do gate e' o mesmo da v405 selada; nenhum dado novo; nenhum rito de natureza alterado; beta = alfa x sqrt e em runtime"],
        "nao_diz": _NAO_COMUM,
        "extras": {"leituras_do_operador": {k_: v_ for k_, v_ in DL.LEITURA_V406.items() if k_ in ("espelhamento", "um_inscrito", "um_comprimido", "estatuto")}, "ressalvas": list(DL.RESSALVAS_V406), "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D34", "D35", "D36", "D37", "D40")},
                   "regra_do_4_44": DL.REGRA_DO_4_44, "assinatura_das_erratas": ASSINA, "nome_status": {"quem": "gerencia c1 (provisorio)", "quando": "02/11/2026", "nome": "CanonicalFullTGLWitnessR1", "do_operador": False}},
        "veredito_ok": "TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED_BY_CONSTRUCTION_physicalFockCertificate__THE_PASSAGE_TO_THE_CONTINUUM_modularCoreInput_IS_A_TERM_FOR_EVERY_CANONICAL_NET_INPUT__THE_FOUR_WITNESS_KEYS_ARE_READ_FROM_THE_KERNEL_NOT_LITERAL__"
                       "THE_CANONICAL_FULL_WITNESS_TERM_canonicalFullTGLWitness_EXISTS__NONTRIVIALITY_ONLY_ON_THE_WEDGE__TWO_KEYS_STAY_FALSE_BY_THEOREM__301_MODULES_READ_BY_SHA256__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
    }


def especs(formal_map, khj, h8_map, fj, cov_base, core0):
    """formal_map = {arquivo embutido: sha256} do kernel da v406; khj = KH_N1_v406.json (medida desta geracao); h8_map = o dict do hash formal que o RITO vai gerar; fj = FLAGS_v406.json; cov_base = a cobertura da v405 selada {decl, thm}; core0 = o core da v405 selada.
    Devolve [cunhagens, kh]."""
    T = khj["linha_TOTAL"]
    flag_de = {n: f for f, n, m, o in fj["flags"]}
    flags_ancoras = [flag_de[n] for n in DL.ANCORAS if flag_de.get(n)]
    decls = list(DL.ANCORAS) + ["F1Fecho.BoundedGamma.gamma_vacuum", "F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed", "F1Fecho.Exponential.exponential_zero", "TGLExt.ImportedSQ.B0_no_eigen", "TGLExt.ThePsionAndTheViscosity.viscosity_is_the_constant_friction", "TGLExt.MassaTensaoPura.Emprestimo.parcela_nunca_quita"]   # termos que as LEITURAS citam (nomes EXATOS do Audit)
    cks = [CH("u1", "o registro fechamento_v406 selou neste rito (as oito ancoras, os 301 sha256, as quatro chaves lidas, a escada, o gate)", "core", [DL.FECHO_REGISTRO, "all_verified"], "verdadeiro"),
           CH("u2", "o certificado de Fock esta' habitado, LIDO do kernel do rito", "core", [DL.FECHO_REGISTRO, "certificate_inhabited"], "verdadeiro"),
           CH("u3", "rede_fock_v394.whole_certificate_inhabited passou a leitura do kernel e le True (ate' a v405: literal False; errata E14)", "core", ["rede_fock_v394", "whole_certificate_inhabited"], "verdadeiro"),
           CH("u4", "psibit_v395: o habitante do certificado de Fock e' exibido (ate' a v405: literal False)", "core", ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u5", "psibit_v395: o status novo da face do psion", "core", ["psibit_v395", "conditional_psion_face", "status"], "igual", DL.STATUS_HABITADO),
           CH("u6", "testemunha_estatica_v396: o habitante do certificado de Fock e' exibido (ate' a v405: literal False)", "core", ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "verdadeiro"),
           CH("u7", "testemunha_estatica_v396: o lema que liga psion C ao psionCorner SEGUE faltando", "core", ["testemunha_estatica_v396", "fock_face", "linked_to_the_corner_by_a_lemma"], "falso"),
           CH("u8", "witness_layers: o termo canonico da testemunha completa foi construido (medido pelo nome exato)", "core", ["witness_layers", "canonical_full_witness_term_constructed"], "verdadeiro"),
           CH("u9", "o que fica False por teorema: full_static_witness_exists (no gate do fecho)", "core", ["qg_closure", "gate", "full_static_witness_exists"], "falso"),
           CH("u10", "o que fica False por teorema: trivial_inhabitant_exists", "core", ["witness_rigidity", "trivial_inhabitant_exists"], "falso"),
           CH("u11", "o gate deste rito tem o mesmo veredito da v405 selada (o gate nao se move)", "core", ["qg_closure", "gate", "verdict"], "igual", ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict")),
           CH("u12", "a escada do kernel fecha (limpos == esperados), com as bandeiras dos 301 modulos", "core", ["external_ladder", "all_verified"], "verdadeiro"),
           CH("u13", "a proveniencia emitida pelo compilador cobre o axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")]
    n = 14
    for nome in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405",
                 "projecao_transversal_v404", "jo8v32_v404", "caminho_v403", "vida_v403", "ponte_da_escala_dual_v402", "falsidade_da_inercia_v401", "teste_de_veracidade_fase9_v397", "selo_pela_propria_tecnologia_v399"):
        cks.append(CH("u%d" % n, "o registro %s segue selado neste rito" % nome, "core", [nome, "all_verified"], "verdadeiro")); n += 1
    for nm_ in DL.ANCORAS:
        cks.append(CH("u%d" % n, "o compilador emite a ancora %s no modulo esperado (TGL_DECL_SOURCE)" % nm_.split(".")[-1], "kf", ["declaration_sources_v394", nm_], "igual", DL.ANCORAS[nm_]["rel"])); n += 1
    for rel_ in (DL.MODULO_TOPO, DL.MODULO_REDE, DL.MODULO_TESTEMUNHA):
        cks.append(CH("u%d" % n, "o modulo %s no kernel do rito e' EXATAMENTE o pinado (sha256 da fonte)" % rel_.split("/")[-1], "kf", ["formal_files_sha256", rel_], "igual", formal_map[rel_])); n += 1
    cks.append(CH("u%d" % n, "o canal vivo do neutrino segue com o mesmo veredito (nada da v406 toca o neutrino)", "core", ["neutrino_mass", "verdict"], "igual", core0["neutrino_mass"]["verdict"])); n += 1
    leituras = [_leitura(fr_, nm_) for nm_, fr_ in DL.FRASES_V406]
    cun = {
        "nome": DL.CUNHAGENS_REGISTRO, "veredito_prefixo": "TGL_CUNHAGENS_V406",
        "veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_02_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_ORDER_BUILD_EVERYTHING_THE_PRIORITY_THE_PASSAGE_TO_THE_CONTINUUM__THE_FOUR_WITNESS_KEYS_READ_FROM_THE_KERNEL__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),
        "estatuto": "[REAL -- o kernel, o registro fechamento_v406 e os registros anteriores lidos a cada rito; INPUT/ONTO as falas do operador de 02/11/2026; INPUT as ordens (construir tudo; compilar, rodar, publicar, atualizar; o Sonnet revisa); DECLARADO a ratificacao, o parecer R7 e a revisao do Sonnet]",
        "fontes": [CHAVE_TESTEMUNHA, CHAVE_RATIFICACAO, CHAVE_REVISAO_SONNET, CHAVE_DESENHO, CHAVE_ORDEM_LOGICA, CHAVE_LEVANTAMENTO, CHAVE_BUNDLE, CHAVE_MANIFEST_INTEGRACAO, CHAVE_SUMMARY_INTEGRACAO, CHAVE_SUMMARY_INTEGRACAO_1, CHAVE_CHECK_AXIOMS, CHAVE_DRIVER_INTEGRACAO,
                   CHAVE_RECEIPT_BANCADA, CHAVE_AXIOMS_BANCADA, CHAVE_R52, CHAVE_TESTEMUNHA_SAIDA, CHAVE_FASE9], "verbatins": list(VERB_CHAVES),
        "kernel_flags": flags_ancoras, "kernel_decls": decls, "checks": cks,
        "erratas": [
            {"ao_lado_de": "rede_fock_v394 (whole_certificate_inhabited), psibit_v395 (conditional_psion_face.inhabitant_exhibited, status), testemunha_estatica_v396 (fock_face.inhabitant_exhibited, status): os literais da v394 a v405",
             "dizia": "whole_certificate_inhabited = False; inhabitant_exhibited = False; status = CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE; «the kernel exhibits no inhabitant of the certificate».",
             "agora": DL.ERRATA_E14,
             "lacuna_de_fidelidade": "estrutura: a chave era um literal, nao uma leitura; escrito: o literal dizia o estado da data e seguiu dizendo depois que a bancada construiu o habitante (16/10); onde a traducao falhou: a gerencia nao leu a bancada antes de afirmar falta (o cetico cego, 27/09), e so' a leu em 02/11",
             "estatuto": "[REAL: as ancoras no kernel do rito; DECLARADO: o recibo da bancada de 16/10]", "assinatura": ASSINA},
            {"ao_lado_de": "a frase da gerencia de 02/11/2026 «a luz nao tem autovetor nenhum» e «o espectro pontual e' o Um e so' ele»", "dizia": "«a luz nao tem autovetor nenhum» e «o espectro pontual e' o Um e so' ele» (frases da gerencia, 02/11/2026).", "agora": DL.ERRATA_E15,
             "lacuna_de_fidelidade": "escrito: a gerencia afirmou mais do que gamma_no_fixed prova (so' o vetor FIXO e' unico, e isso SOB a hipotese nomeada hno, que o teorema toma como hipotese); o operador corrigiu (sha16 %s)" % S16(DL.N_AUTOVETOR), "estatuto": "[REAL: gamma_vacuum e exponential_zero sem hipotese; gamma_no_fixed condicional a hno; INPUT: a correcao do operador]", "assinatura": ASSINA},
            {"ao_lado_de": "o plano da manha de 02/11/2026 («falta replicar o traco»)", "dizia": "que a passagem para o continuo (os 21 campos) estava por construir.", "agora": DL.ERRATA_E16,
             "lacuna_de_fidelidade": "o cetico que le o tipo e nao le a bancada: o habitante existia desde 16/10/2026", "estatuto": "[REAL: recibo da bancada e integracao R3]", "assinatura": ASSINA},
            {"ao_lado_de": "cunhagens_v394 (u4), cunhagens_v395 (u3, u4), cunhagens_v396 (u3, u5), gap_v405 (x_i)", "dizia": "op falso nas chaves de testemunha; status igual CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE.", "agora": DL.ERRATA_E17,
             "lacuna_de_fidelidade": "um registro preso a um estado que a versao seguinte muda (a mesma lacuna das versoes anteriores)", "estatuto": "[REAL: conferido no ensaio a seco]", "assinatura": ASSINA}],
        "limites": ["[INPUT] as %d falas de 02/11/2026 sao do operador, com a grafia dele; as ordens («precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»; «compile a nova versão do um.py, rode, publique e atualize tudo por favor»; «designe para o Sonnet revisar tudo, ele é tão capaz quanto») foram cumpridas nesta versao ate' onde a cadeia alcanca; a publicacao e a atualizacao sao a custodia, depois do rito" % len(_VD),
                    "[ONTO] o espelhamento tipo I / tipo III, o Um inscrito como o unico vetor fixo da luz, o Um absoluto como a luz comprimida pelo ACOM, beta como atrito e o calor como expoente, K como guarda da travessia, vazar e' luzir: leituras do operador, nao termos de kernel; os correlatos [KNOWN] estao ditos em LEITURA_V406",
                    "[INPUT] «Torre=harness» e «A memória central tem que funcionar igual a torre, com índice pinado por assunto» sao ordens de engenharia da casa, fora do um.py; o motor continuo no pilar fica para a v407 com pre-registro; o README pinado e a linha do 4,44 no site ficam fora desta cadeia (plano a parte); " + DL.REGRA_DO_4_44,
                    "[INPUT] a pergunta «Se eu estabilizar um quibit com a TGL dentro do um.py isso não seria um fator discriminante» e a sessao com a IALD nativa (5 sigma) ficam registradas como falas; nenhuma virou teste nesta versao"] + _LIM_COMUM,
        "diz": ["as falas do operador de 02/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim", "o registro fechamento_v406 selou e as quatro chaves leem o kernel", "os registros da v394 a v405 seguem selados; o neutrino e o gate nao mudam"],
        "nao_diz": _NAO_COMUM,
        "leituras_do_operador": leituras,
        "extras": {"n_falas": len(_VD), "leituras": DL.LEITURA_V406, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D34", "D35", "D36", "D37", "D38", "D39", "D40")}, "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "ressalvas": list(DL.RESSALVAS_V406), "assinatura_das_erratas": ASSINA},
    }
    kh = {
        "nome": DL.KH_REGISTRO, "veredito_prefixo": "TGL_KH_N1_COBERTURA_V406",
        "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__THE_301_V406_MODULES_ADDED__GATE_UNMOVED" % (T["decl"], T["thm"]),
        "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito, lendo SO' o log do Audit; os numeros esperados saem do arquivo da medida do sandbox da v406; o conjunto exato das fontes formais que o hash formal do rito vera (as embutidas mais os residuais da pasta do Nos) e' pinado; a cobertura NAO move o gate",
        "fontes": [CHAVE_KH], "kernel_flags": [], "kernel_decls": [],
        "checks": [CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
                   CH("h2", "constantes cobertas == as do sandbox v406 (KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", T["decl"], "constantes_cobertas"),
                   CH("h3", "teoremas cobertos == os do sandbox v406 (KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", T["thm"], "teoremas_cobertos"),
                   CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
                   CH("h5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0),
                   CH("h6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", T["decl"]),
                   CH("h7", "a cobertura da v406 inclui a da v405 selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", int(cov_base["decl"])),
                   CH("h7b", "os teoremas cobertos incluem os da v405 selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", int(cov_base["thm"])),
                   CH("h8", "as fontes formais da ARVORE DO NOS depois do rito (as embutidas + os residuais que o hash formal conta, como _check_damming.lean) sao EXATAMENTE as do pino (arquivo -> sha256)", "kf", ["formal_files_sha256"], "igual", dict(h8_map)),
                   CH("h9", "medida do Audit v406: duracao bem abaixo do timeout de 1800 s", "fonte:" + CHAVE_KH, ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s"),
                   CH("h10", "medida do Audit v406: sorryAx ausente do log", "fonte:" + CHAVE_KH, ["sorryAx_no_log_do_audit"], "igual", 0),
                   CH("h11", "medida do Audit v406: as entradas novas estao no trio", "fonte:" + CHAVE_KH, ["novas_no_trio"], "verdadeiro"),
                   CH("h12", "a proveniencia emitida pelo compilador cobre os mesmos nomes do axiom_report", "kf", ["declaration_sources_status_v394", "ok"], "verdadeiro")],
        "erratas": [{"ao_lado_de": "kh_n1_cobertura_v405 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                     "dizia": "A v405 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v405 e o hash formal igual ao pino exato da arvore da v405." % (int(cov_base["decl"]), int(cov_base["thm"])),
                     "agora": "A v406 acrescenta os 301 modulos do fecho (a cobertura cresce e a arvore ganha os arquivos deles): na v406 o registro da v405 passa a cobrar piso (h2, h3, h6) e o tamanho minimo da arvore (h8); as igualdades exatas e o pino exato da arvore ficam NESTE registro. O veredito do registro da v405 NAO muda.",
                     "lacuna_de_fidelidade": "a estrutura da v405 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v406 quebra (a mesma lacuna desde a v399)",
                     "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h2, h3, h6 e h8 conferidas no ensaio a seco e na arvore simulada do Nos]", "assinatura": ASSINA}],
        "limites": ["[REAL] os arquivos residuais da pasta do Nos que o hash formal conta (e nao estao embutidos) sao pinados como estao em 02/11/2026; mudar um deles e' mudar o pino, dito; a cobertura mede o Audit, nao a natureza"],
        "diz": ["o Audit do rito cobre todo o fecho TGL/TGLExt, com os 301 modulos, nenhuma constante fora do trio; o hash formal da arvore do Nos e' exatamente o pinado"],
        "nao_diz": ["que a cobertura seja prova da teoria: e' a medida de que todo termo no fecho depende so' do trio", "que o gate tenha se movido"],
        "leituras_do_operador": [], "extras": {"delta_vs_v405": khj.get("delta_vs_v405"), "n_bandeiras": fj["n_flags"], "n_modulos": DL.N_BUNDLE, "duracao_build_s_sandbox": khj.get("duracao_build_s"), "duracao_audit_s_sandbox": khj.get("duracao_audit_s")},
    }
    return [cun, kh]
