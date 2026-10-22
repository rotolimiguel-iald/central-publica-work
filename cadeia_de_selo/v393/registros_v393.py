# -*- coding: utf-8 -*-
"""registros_v393.py -- os dados dos registros por spec da v393 (interpretados pelo MOTOR _v392_registro, que ja esta no um.py v392): FONTES pinadas por sha256 (lidas do disco pelo montador, nunca
digitadas), VERBATINS (as 4 cunhagens do operador, EMBUTIDAS) e SPECS. Fontes so' em pasta DURAVEL: tudo vem de cadeia_de_selo\\v393\\insumos (copias com sha256 conferido contra o encaminhamento).
Texto novo passa pela guarda P18 (a cada rito)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
INS = os.path.join(HERE, "insumos")
ASSINA = "gerencia c1, em nome proprio, 14/10/2026"
FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v393.json"), encoding="utf-8"))
FL = {n: f for f, n, m, k in FJ["flags"]}
CHAVE = ["TGLExt.RuleTruthContract.sound_complete_eq_admissible", "TGLExt.RuleTruthContract.admissible_iff_eq_of_injective", "TGLExt.RuleSatisfactionFace.unique_rule_on_inscriptions",
         "TGLExt.RuleSatisfactionFace.the_rule_and_the_figure_of_truth", "TGLExt.RuleContinuousMotor.unique_sound_complete_rule", "TGLExt.RuleContinuousMotor.flow_satisfies_fixed_target_iff",
         "TGLExt.RuleContinuousMotor.matrix_flow_satisfies_declared_target", "TGLExt.RuleContinuousMotor.matrix_wrong_input_never_satisfies", "TGLExt.RuleContinuousMotor.inhabited_and_discriminating",
         "TGLExt.RuleTruthContract.idempotence_does_not_force_target", "TGLExt.RuleTruthContract.incompatible_not_admissible"]
for n in CHAVE:
    assert n in FL, n

FONTES = [
    {"chave": "v393_encaminhamento", "arquivo": os.path.join(INS, "AO_CLAUDE_INTEGRAR_REGRA_V393.md"), "papel": "o encaminhamento do Codex (14/10/2026) que manda integrar a regra na v393"},
    {"chave": "v393_prova_matematica", "arquivo": os.path.join(INS, "PROVA_MATEMATICA_R1.md"), "papel": "a prova matematica da regra (F1.REGRA.P1), entregue pelo Codex"},
    {"chave": "v393_relatorio_motor", "arquivo": os.path.join(INS, "RELATORIO_EXECUCAO_R1.md"), "papel": "o relatorio da execucao do motor (F1.REGRA.MOTOR), do Codex"},
    {"chave": "v393_resultado_motor_codex", "arquivo": os.path.join(INS, "RESULT_MOTOR_R1.json"), "papel": "o RESULT.json da execucao sintetica do Codex (76 verificacoes, 241 pontos), a replica contra a qual o rito compara"},
    {"chave": "v393_prereg_motor", "arquivo": os.path.join(INS, "PREREGISTRO_R1.json"), "papel": "o pre-registro do motor (alvo e tolerancias fixados antes da execucao)"},
    {"chave": "v393_manifesto_fontes_motor", "arquivo": os.path.join(INS, "SOURCE_MANIFEST.json"), "papel": "o manifesto das fontes do motor (as dez evidencias do kernel registradas)"},
    {"chave": "v393_run_rule_motor", "arquivo": os.path.join(INS, "run_rule_motor.py"), "papel": "o executor original do Codex, de que o consumidor da v393 e' o porte"},
    {"chave": "v393_lean_contrato", "arquivo": os.path.join(HERE, "pedras", "RuleTruthContract.orig.lean"), "papel": "RuleTruthContract.lean como entregue (original, antes do ajuste de import/bloco local)"},
    {"chave": "v393_lean_figura", "arquivo": os.path.join(HERE, "pedras", "TheRuleAndTheFigureOfTruth.orig.lean"), "papel": "TheRuleAndTheFigureOfTruth.lean como entregue"},
    {"chave": "v393_lean_motor", "arquivo": os.path.join(HERE, "pedras", "TheRuleInTheContinuousMotor.orig.lean"), "papel": "TheRuleInTheContinuousMotor.lean como entregue"},
    {"chave": "v393_quadro_do_coracao", "arquivo": os.path.join(INS, "QUADRO_DO_CORACAO.md"), "papel": "o quadro do coracao (PT/EN) que abre o artigo"},
    {"chave": "kh_n1_v392", "arquivo": os.path.join(INS, "KH_N1_v392.regravado.json"), "papel": "REPINO: a medida KH-N1 da v392 como esta' hoje em disco (regravada pelo pos_build da v392 em 13/10/2026 18:34, depois do rito; o pino da v392 deixou de conferir)"},
    {"chave": "kh_n1_v393", "arquivo": os.path.join(INS, "KH_N1_v393.json"), "papel": "a medida da cobertura no Audit do sandbox da v393 (pos_build_kernel_v393.py)"},
    {"chave": "v393_funcao_do_coracao", "arquivo": os.path.join(INS, "prove_heart_and_gravity_seal.py"), "papel": "a funcao do coracao e do selo gravitacional como entregue (a v393 embute o porte, sem literal de beta)"},
]
VERBATINS = [
    {"chave": "v393_cunhagem_1_negatividade", "arquivo": os.path.join(INS, "cunhagem1_negatividade.txt"), "quando": "14/10/2026 (via Codex; fonte no tunel F1.REGRA)",
     "trechos": ["Regra é negar tudo aquilo que não pode ser, e isso é criar limite assintótico", "Portanto o direito é negativo e não positivo", "Cria-se aqui o domínio da negatividade jurídica"]},
    {"chave": "v393_cunhagem_2_tetelestai", "arquivo": os.path.join(INS, "cunhagem2_tetelestai.txt"), "quando": "14/10/2026 (via Codex; fonte no tunel F1.REGRA/TETELESTAI)",
     "trechos": ["Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível", "Ela é segundo a mesma regra do acoplamento não minimal"]},
    {"chave": "v393_cunhagem_3_satisfacao", "arquivo": os.path.join(INS, "cunhagem3_satisfacao.txt"), "quando": "14/10/2026 (via Codex; fonte no tunel F1.REGRA/SATISFACAO)",
     "trechos": ["Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)"]},
    {"chave": "v393_cunhagem_4_figura_da_verdade", "arquivo": os.path.join(INS, "cunhagem4_figura_da_verdade.txt"), "quando": "14/10/2026 (via Codex; fonte no tunel F1.REGRA/FIGURA_DA_VERDADE)",
     "trechos": ["A regra não deve nada, a não ser a figura da verdade"]},
]
CH = lambda id_, desc, onde, caminho, op, valor=None, cap=None, est="[REAL]": dict(id=id_, descricao=desc, onde=onde, caminho=caminho, op=op, **({"valor": valor} if valor is not None else {}), **({"capturar": cap} if cap else {}), estatuto=est)
SPECS = [
    {"nome": "cunhagens_regra_v393", "veredito_prefixo": "TGL_CUNHAGENS_REGRA_V393",
     "veredito_sufixo": "RULE_AS_NEGATION_TETELESTAI_SATISFACTION_AND_FIGURE_OF_TRUTH_VERBATIM_EMBEDDED_BY_SHA256__RULE_READS_TARGET_IN_THE_REAL_CONSUMER__OPERATOR_INPUT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED",
     "estatuto": "[REAL -- fontes e kernel lidos a cada rito; INPUT/ONTO as quatro cunhagens do operador; DECLARADO o que o Codex relata e nao foi reexecutado aqui (a reproducao dos .olean)]",
     "fontes": [f["chave"] for f in FONTES], "verbatins": [v["chave"] for v in VERBATINS],
     "kernel_flags": [FL[n] for n in CHAVE], "kernel_decls": CHAVE,
     "checks": [
         CH("c1", "as tres pedras da regra selaram neste rito (pedras_v393)", "core", ["pedras_v393", "all_verified"], "verdadeiro"),
         CH("c2", "o consumidor real com a regra selou neste rito", "core", ["regra_consumidor_v393", "all_verified"], "verdadeiro"),
         CH("c3", "o alvo correto e' ADMITIDO pela regra no rito", "core", ["regra_consumidor_v393", "satisfacao", "veredito_do_rito"], "igual", "SATISFACTION_ADMITTED", "veredito_do_alvo_correto"),
         CH("c4", "o alvo incompativel e' RECUSADO pela regra no rito", "core", ["regra_consumidor_v393", "satisfacao", "veredito_incompativel"], "igual", "SATISFACTION_REFUSED", "veredito_do_alvo_incompativel"),
         CH("c5", "a igualdade exata NAO e' afirmada: o criterio numerico e' tolerancia declarada", "core", ["regra_consumidor_v393", "criterio", "igualdade_exata_afirmada"], "falso"),
         CH("c6", "o estado bruto e a inscricao ficam em campos distintos", "core", ["regra_consumidor_v393", "estado_bruto_e_inscricao", "separados"], "verdadeiro"),
         CH("c7", "o bruto finito nunca e' o alvo", "core", ["regra_consumidor_v393", "estado_bruto_e_inscricao", "o_bruto_finito_nunca_e_o_alvo"], "verdadeiro"),
         CH("c8", "o espaco fixo tem dimensao complexa 8", "core", ["regra_consumidor_v393", "numeros", "dimensao_fixa_complexa"], "igual", 8, "dimensao_fixa"),
         CH("c9", "numero de verificacoes do consumidor neste rito", "core", ["regra_consumidor_v393", "numeros", "verificacoes"], "maior_igual", 70, "verificacoes_do_consumidor"),
         CH("c10", "numero de pontos da trajetoria neste rito", "core", ["regra_consumidor_v393", "numeros", "pontos"], "igual", 241, "pontos_da_trajetoria"),
         CH("c11", "o selo do coracao selou neste rito", "core", ["coracao_e_selo_gravitacional_v393", "all_verified"], "verdadeiro"),
         CH("c12", "o selo do coracao: hoje a fonte de chi e' o CODATA (reconstruido), sem previsao independente", "core", ["coracao_e_selo_gravitacional_v393", "previsao_independente"], "falso", est="[REAL]"),
         CH("c13", "o selo do coracao: o veredito e' o da reconstrucao a partir do CODATA", "core", ["coracao_e_selo_gravitacional_v393", "verdict"], "comeca", "FORM_VERIFIED_CHI_FROM_CODATA", "veredito_do_coracao"),
         CH("c14", "G nao e' derivado", "core", ["coracao_e_selo_gravitacional_v393", "G_derivado"], "falso"),
         CH("c15", "os controles negativos do selo do coracao recusam", "core", ["coracao_e_selo_gravitacional_v393", "controles_ok"], "verdadeiro"),
         CH("c16", "a satisfacao do selo do coracao foi determinada pela regra (leitura == alvo pre-fixado, criterio exato)", "core", ["coracao_e_selo_gravitacional_v393", "satisfacao_pela_regra", "criterio"], "igual", "exato"),
     ],
     "erratas": [],
     "limites": [
         "[REAL] a regra e' representada, no kernel, como admissibilidade relativa a uma leitura e a um alvo (RuleTruthContract.Admissible: reading y = target); as provas valem para essa representacao, nao para a verdade ou a realizacao fisica da leitura escolhida",
         "[INPUT/ONTO] a leitura filosofica (regra como negacao, limite assintotico, direito negativo) e a leitura juridica (inadmissao de que o resultado difira do objeto da satisfacao) sao do operador; o kernel prova as consequencias logicas da representacao",
         "[INPUT/ONTO] «a regra nao deve nada, a nao ser a figura da verdade» foi representado pela completude relativa ao alvo (nao acrescentar outra exclusao quando ha correspondencia): hipotese declarada, nao teorema extraido do nome",
         "[REAL] sem completude, rejeitar tudo tambem satisfaz a correcao; sem leitura fiel, igualdade de leituras nao implica igualdade de objetos; a fidelidade vale no subtipo Fix(R), nao no espaco bruto",
         "[INPUT/ONTO] a exclusao irrestrita ser o zero absoluto, e a exclusao ser no tetelestai segundo a regra do acoplamento nao minimal, e' leitura do operador; nao foi provado um novo teorema termodinamico",
         "[REAL] a meia-nat exp(-1/2) do exemplo do kernel nao e' beta_TGL; beta e' sempre calculado em runtime (alfa CODATA x raiz de e)",
         "[REAL] o consumidor numerico usa uma tolerancia declarada; ela nao e' igualdade exata; o espaco fixo tem dimensao complexa 8, logo a unicidade do criterio vale para o alvo dado, nao para todos os estados fixos",
         "[REAL] pinching nao e' o canto eXe; o motor vetorial IALD.motor tem ponte separada",
         "[DECLARADO] ressalva de reproducao da prova (relatada pelo Codex): 2 de 3 .olean coincidiram byte a byte; o modulo concreto teve bytes diferentes, com fonte e axiomas iguais; causa nao determinada",
         "as provas nao instalam a dinamica nos pesos de um LLM, nao provam uma norma juridica universal e nao tratam a natureza; execucao sintetica, nenhum dado observado, unidades de referencia [INPUT]"],
     "diz": ["as quatro cunhagens do operador estao embutidas por sha256 e a regra entra no kernel (3 modulos) e no veredito de satisfacao do consumidor real e do selo do coracao",
             "o selo do coracao usa o contrato da regra para decidir se a leitura satisfaz o alvo pre-fixado; evidencia espectral independente exige cadeia pinada independente do CODATA (hoje ausente)"],
     "nao_diz": ["que a gravidade quantica esteja creditada na natureza", "que G seja derivado", "que o valor de alfa seja previsao independente", "que a tolerancia numerica seja igualdade exata"],
     "leituras_do_operador": [{"trecho": "Regra é negar tudo aquilo que não pode ser, e isso é criar limite assintótico", "estatuto": "[INPUT do operador, verbatim 14/10/2026]"},
                              {"trecho": "Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível", "estatuto": "[INPUT do operador, verbatim 14/10/2026]"},
                              {"trecho": "Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)", "estatuto": "[INPUT do operador, verbatim 14/10/2026]"},
                              {"trecho": "A regra não deve nada, a não ser a figura da verdade", "estatuto": "[INPUT do operador, verbatim 14/10/2026]"}],
     "extras": {"assinatura": ASSINA, "autoria_das_cunhagens": "Luiz Antonio Rotoli Miguel", "unidades_entregues_pelo_codex": ["F1.REGRA", "F1.REGRA.P1", "F1.REGRA.MOTOR"]}},
]

_KH3 = json.load(open(os.path.join(INS, "KH_N1_v393.json"), encoding="utf-8"))
_sha = lambda p: __import__("hashlib").sha256(open(p, "rb").read()).hexdigest()
SPECS.append({"nome": "kh_n1_cobertura_v393", "veredito_prefixo": "TGL_KH_N1_COBERTURA_V393",
     "veredito_sufixo": "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__FOUR_NAMES_THE_REGEX_CANNOT_READ_DECLARED__V392_SOURCE_REPINNED__GATE_UNMOVED" % (_KH3["linha_TOTAL"]["decl"], _KH3["linha_TOTAL"]["thm"]),
     "estatuto": "[REAL] a cobertura e' medida a cada rito no Audit do proprio rito; os numeros esperados saem do arquivo da medida do sandbox da v393; a cobertura NAO move o gate",
     "fontes": ["kh_n1_v392", "kh_n1_v393"],
     "kernel_flags": [], "kernel_decls": [],
     "checks": [
         CH("h1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro"),
         CH("h2", "constantes cobertas == as do sandbox v393 (KH_N1_v393.json)", "kf", ["axiom_coverage_v392", "decl"], "igual", _KH3["linha_TOTAL"]["decl"], "constantes_cobertas"),
         CH("h3", "teoremas cobertos == os do sandbox v393", "kf", ["axiom_coverage_v392", "thm"], "igual", _KH3["linha_TOTAL"]["thm"], "teoremas_cobertos"),
         CH("h4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0),
         CH("h5", "nomes que o regex do um.py nao le == 4 (declarados)", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 4),
         CH("h6", "o axiom_report do rito tem entrada para as constantes lidas", "kf", ["axiom_report"], "tamanho_maior_igual", _KH3["nomes_no_axiom_report_efetivo_umpy"]),
         CH("h7", "a cobertura da v393 inclui toda a da v392 (constantes >= 24975, teoremas >= 19761)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", 24975),
         CH("h8", "medida do Audit v393: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v393", ["duracao_audit_s"], "menor_igual", 900, "duracao_do_audit_s"),
         CH("h9", "medida do Audit v393: sorryAx ausente do log", "fonte:kh_n1_v393", ["sorryAx_no_log_do_audit"], "igual", 0),
         CH("h10", "medida do Audit v393: as entradas novas de usuario estao no trio", "fonte:kh_n1_v393", ["novas_de_usuario_no_trio"], "verdadeiro"),
     ],
     "erratas": [{"ao_lado_de": "kh_n1_cobertura_v392 (fonte kh_n1_v392 e duas igualdades de contagem)",
                  "dizia": "A v392 pinou KH_N1_v392.json (1389 bytes, sha256 104377ce6d1280c7...) e exigia constantes cobertas == 24975 e teoremas == 19761.",
                  "agora": "O arquivo foi regravado pelo pos_build da v392 em 13/10/2026 18:34, depois do rito (1390 bytes, sha256 %s...; o campo novas_de_usuario_no_trio ficou false nessa regravacao): o pino da v392 deixou de conferir e o registro kh_n1_cobertura_v392 nao selaria numa nova rodada. A v393 repina a fonte a uma copia do arquivo regravado (insumos/KH_N1_v392.regravado.json) e troca as duas igualdades por pisos (24975 e 19761), porque a cobertura cresce com as pedras da regra; a igualdade exata passa a ser cobrada por este registro, contra a medida do sandbox da v393." % _sha(os.path.join(INS, "KH_N1_v392.regravado.json"))[:16],
                  "lacuna_de_fidelidade": "a estrutura dizia que o pino da fonte e as contagens eram da v392 para sempre; o texto escrito deixou o registro preso a um arquivo regravavel e a uma igualdade que a propria v393 quebra",
                  "estatuto": "[REAL: sha256 lidos dos arquivos; a regravacao e' do pos_build da v392, registrada em pos_rito]", "assinatura": ASSINA}],
     "limites": ["[REAL] os dois arquivos de medida sao do sandbox (fora do selo); a cobertura que vale e' a medida no Audit do proprio rito", "validade no kernel nao e' creditacao; o gate nao se move"],
     "diz": ["a cobertura do axiom_report no fecho inteiro cresceu para os numeros da v393 e segue sem constante fora do trio"], "nao_diz": ["que a cobertura prove algo alem de que nenhum axioma fora do trio foi lido"],
     "leituras_do_operador": [], "extras": {"assinatura": ASSINA}})
