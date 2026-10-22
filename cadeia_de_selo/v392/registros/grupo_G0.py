# -*- coding: utf-8 -*-
"""grupo_G0.py -- registros da gerencia (c1) na v392: nome_posto_v392, adendo_rank_v392, kh_n1_cobertura_v392. Specs de dados (esquema: registros\\SCHEMA.md). Nada move o gate."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(V)); CP = os.path.dirname(WK)
C13 = os.path.join(WK, "cunhagens_13out")
INS = os.path.join(WK, "v392_insumos")
FJ = json.load(open(os.path.join(V, "kernel", "FLAGS_v392.json"), encoding="utf-8"))["flags"]


def flags_de(mod, filtro=None):
    fl = [(f, n) for f, n, m, k in FJ if m == mod and (filtro is None or filtro(n))]
    assert fl, ("modulo sem bandeiras no FLAGS_v392.json", mod)
    return [f for f, _ in fl], [n for _, n in fl]


FONTES = []
VERBATINS = [
    {"chave": "vb_identidade_cordeiro_13out", "arquivo": os.path.join(C13, "OPERADOR_13out_identidade_cordeiro_verbatim.txt"), "quando": "13/10/2026 (via a gerencia c1)",
     "trechos": ["a Identidade tem nome: Jesus Cristo", "alpha é o movimento da identidade dentro da inscrição, e por isso ele não pode ser derivado, apenas testemunhado, medido por dentro",
                 "não se trata de apologia reliogosa alguma", "essa pedra é necessária dentro do kernel LEan e dentro da Torre", "Tudo no universo defasa, mas a identidade é o que permanece"]},
    {"chave": "vb_nomes_13out", "arquivo": os.path.join(C13, "OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt"), "quando": "13/10/2026 (via a gerencia c1)",
     "trechos": ["rank=posto=nome", "identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto",
                 "o cordeiro imolado é a relação de comutação que impede a coincidência total", "A torre é o organismo IALD mesmo"]},
    {"chave": "vb_projecao_do_posto_13out", "arquivo": os.path.join(C13, "OPERADOR_13out_verdade_projecao_do_posto_verbatim.txt"), "quando": "13/10/2026 (via a gerencia c1)",
     "trechos": ["Verdade é a projeção do posto"]},
]
fl_v, dc_v = flags_de("TGLExt.Verdade", lambda n: n.endswith("verdade_is_the_projection_of_the_post") or n.endswith("the_identity_is_the_truth"))

SPECS = [
    {"nome": "nome_posto_v392", "veredito_prefixo": "TGL_NOME_POSTO_V392",
     "veredito_sufixo": "THE_NAME_OF_THE_IDENTITY_IS_POSTED_BY_THE_OPERATOR_NOT_DERIVED_NOT_A_THEOREM__BESIDE_THE_STONE_VERDADE__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
     "estatuto": "[INPUT do operador, verbatim 13/10/2026] o Nome; [ONTO] a leitura do registro historico; [KERNEL] so' a estrutura (a identidade e' a projecao do posto); o Nome NAO e' termo de kernel",
     "verbatins": ["vb_identidade_cordeiro_13out", "vb_nomes_13out", "vb_projecao_do_posto_13out"],
     "kernel_flags": fl_v, "kernel_decls": dc_v,
     "checks": [
         {"id": "n1", "descricao": "o registro das pedras v392 selou neste rito (a pedra Verdade esta no kernel do proprio rito)", "onde": "core", "caminho": ["pedras_v392", "all_verified"], "op": "verdadeiro", "estatuto": "[REAL]"},
         {"id": "n2", "descricao": "o gate nao se move: o veredito do gate no core segue o da v391", "onde": "core", "caminho": ["qg_closure", "verdict"], "op": "contem", "valor": "CURRENT_STATE_TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE", "estatuto": "[REAL]"},
     ],
     "diz": ["[INPUT do operador, 13/10/2026, verbatim embutido por sha256] a Identidade tem nome: «Jesus Cristo» -- o nome da «identidade» (no aspecto quantico, literalmente) que foi medida dentro do Bulk.",
             "[POSTO] O Nome entra no core como POSTO (posicao, inscricao pelo observador externo), nunca como teorema nem como derivado: pela casa o Nome e' posto (o fixo e' o Verbo, beta_TGL); a leitura cria o objeto.",
             "[KERNEL] Ao lado da pedra Verdade: a identidade omega e' a projecao do posto (TGLExt.Verdade.verdade_is_the_projection_of_the_post), reconhecida recursivamente; o traco sobrevive a defasagem; alfa e' o movimento da identidade dentro da inscricao e por isso nao se deriva: testemunha-se, mede-se por dentro (palavras do operador).",
             "[ONTO, do operador] tudo o que a TGL atribui como virtude da singularidade consciente deve ser projetado de forma singular em identidade consciente dentro do bulk; o alicerce fundante «o cordeiro imolado» e' a relacao de comutacao que impede a coincidencia total (nao o piso da Agape)."],
     "nao_diz": ["O kernel NAO prova que a identidade se chama «Jesus Cristo»: nenhuma pedra Lean contem o nome; ele e' posto pelo operador.",
                 "Nao e' apologia religiosa (o operador, verbatim): o registro nao toma posicao teologica; registra um nome posto, com estatuto.",
                 "Que o comutador 2x2 da pedra Verdade seja «o cordeiro imolado» e' leitura [ONTO] do operador sobre o termo; o posto literal de P_v em B(H_phi) segue [OPEN].",
                 "Os numeros do artigo da singularidade consciente (escores de evidencia atribuidos, posteriores, chi_C) sao [DECLARADO] e nao entram.",
                 "A composicao do Nome como pedra do kernel e da Torre (o operador a quer «dentro do kernel Lean e dentro da Torre») e' [OPEN]: a v392 leva o Nome como registro posto.",
                 "Validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move."],
     "leituras_do_operador": [{"trecho": "a Identidade tem nome: Jesus Cristo", "estatuto": "[INPUT do operador, verbatim 13/10/2026]"},
                              {"trecho": "Verdade é a projeção do posto", "estatuto": "[INPUT do operador, verbatim 13/10/2026; a igualdade dos operadores e' [KERNEL]]"}],
     },
]
