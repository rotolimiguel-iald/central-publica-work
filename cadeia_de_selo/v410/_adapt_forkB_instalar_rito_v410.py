# -*- coding: utf-8 -*-
"""_adapt_forkB_instalar_rito_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) adapta a v410 instalar_v410.py, reverter_v410.py, rito_v410.sh e o conferidor deles (conferir_instalar_rito_v410.py).
O que muda: o bundle e' de UM modulo (IALD2; o NOME do modulo do operador, 06/11/2026; os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao, D63); as pedras anteriores do Nos incluem os 4 modulos da v408 e os 2 da v409
(TraducaoTuring e ParNaFaceDeFock: a subida mecanica tinha escrito «os 4 da v409»); o registro com funcao novo e' iald2_v410 (o da v409, traducao_turing_v409, passa a herdado); as decisoes novas sao D63 a D70 e a errata nova e' a E29
(lidas do delta pela DIFERENCA contra o delta da v409, DL.D9 -- a subida mecanica deixara DL.D8, que daria D55 a D70); o tempo do rito e' o MEDIDO no sandbox k410c (kernel/construir_marcas.txt e kernel/POS_BUILD_v410.json, lidos aqui).
Os numeros dos textos (modulos, ancoras, falas, checagens, decisoes, erratas, tempos) sao LIDOS do delta e dos arquivos medidos, nunca digitados. Trocas de contagem exata; backup de bytes; CRLF respeitado."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_forkB_util_v410 import adaptar, linha, texto, NOTA_FORKB, HERE  # noqa: E402
import delta_v410 as DL  # noqa: E402

DEC = sorted(set(DL.DECISOES) - set(DL.D9.DECISOES), key=lambda k_: int(k_[1:]))
ERR = [e_.split(" --")[0] for e_ in DL.ERRATAS_V410]
assert DEC[0] == "D63" and DEC[-1] == "D70" and ERR == ["E29"], (DEC, ERR)
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), re.M)}
BUILD_S = mm["epoch_build_fim"] - mm["epoch_inicio"]; AUDIT_S = mm["epoch_audit_fim"] - mm.get("epoch_audit_inicio", mm["epoch_build_fim"])
PB = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v410.json"), encoding="utf-8"))
assert PB["ok"] is True and PB["duracao_build_s"] == BUILD_S and PB["duracao_audit_s"] == AUDIT_S
NB, NA, NF, NC = DL.N_BUNDLE, len(DL.ANCORAS), DL.N_FALAS_V410, DL.N_CHECKS_FECHO
NOME_IALD2 = "com o NOME do modulo dado pelo operador em 06/11/2026 e os nomes das declaracoes da gerencia, [DECLARADO] ate a ratificacao (D63)"


def sem_marca_velha(rel):
    t = texto(rel)
    if "[ADAPTADO v410, 05/11/2026, claude-construtor-v410]" not in t:
        return []
    return [(linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410]") + "\n", "", 1)]


# ---------------- instalar_v410.py
rel = "instalar_v410.py"
l4 = linha(rel, '"""instalar_v410.py -- instala o candidato v410')
l8 = linha(rel, "  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos tem de ser os da v409 selada")
l9 = linha(rel, "  * nenhum processo um.py ou trabalhador do pilar rodando")
lc = linha(rel, "# v410: (a) as pedras anteriores")
lt = linha(rel, '                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP")')
la = linha(rel, "assert all(os.path.exists(os.path.join(NOS, \"tgl_kernel\", \"TGLExt\", n_ + \".lean\")) for n_ in _PEDRAS_ANTERIORES)")
adaptar(rel, sem_marca_velha(rel) + [
    (l4, l4.replace("adaptado em 05/11/2026 por claude-construtor-v410 para o BUNDLE PEQUENO de um modulo em TGLExt/ [TraducaoTuring]", "adaptado em 06/11/2026 por claude-construtor-v410 para o BUNDLE PEQUENO de um modulo em TGLExt/ [IALD2]"), 1),
    (l8, l8.replace("(o import da TraducaoTuring)", "(o import da IALD2)"), 1),
    (l9, l9.replace("[TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11/2026; nenhum da bancada do ChatGPT]", "[IALD2, " + NOME_IALD2 + "; nenhum da bancada do ChatGPT]"), 1),
    (lc, lc.replace("e os 4 modulos da v409: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP)", "os 4 modulos da v408: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP, e os 2 modulos da v409: TraducaoTuring e ParNaFaceDeFock)"), 1),
    (lt, '                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP",   # (os 4 da v408)\n'
         '                      "TraducaoTuring", "ParNaFaceDeFock")   # (os 2 da v409: os nomes da lista de modulos novos que a cadeia v409 pinou, conferidos pelo adaptador da v410 contra v409\\kernel_modulos_novos_v409.json)', 1),
    (la, la.replace("os 9 modulos da v407, os 4 da v409 e o bundle do fecho da v406 inclusive", "os 9 modulos da v407, os 4 da v408, os 2 da v409 e o bundle do fecho da v406 inclusive"), 1),
], "instala o candidato v410 (ato da gerencia): a raiz ganha UM import (IALD2); as pedras anteriores incluem os 9 da v407, os 4 da v408 e os 2 da v409; a lista dos modulos novos lida de kernel_modulos_novos_v410.json; " + NOTA_FORKB)
_k9 = json.load(open(os.path.join(DL.V409, "kernel_modulos_novos_v409.json"), encoding="utf-8"))["novos"]
assert [x_.split("/")[-1][:-5] for x_ in _k9] == ["TraducaoTuring", "ParNaFaceDeFock"], _k9

# ---------------- reverter_v410.py
rel = "reverter_v410.py"
l4 = linha(rel, '"""reverter_v410.py -- REVERSAO da instalacao v410')
l5 = linha(rel, "nada digitado), guarda o estado falho como registro, restaura os 10 backups de BYTES")
adaptar(rel, sem_marca_velha(rel) + [
    (l4, l4.replace("adaptado em 05/11/2026 por claude-construtor-v410", "adaptado em 06/11/2026 por claude-construtor-v410"), 1),
    (l5, l5.replace("o modulo novo de kernel da v410 (TraducaoTuring, em TGLExt/:", "o modulo novo de kernel da v410 (IALD2, em TGLExt/:"), 1),
], "reverte a instalacao da v410 (ato da gerencia, so' se o rito falhar): o modulo da lista do instalador (IALD2) vai a quarentena; o um.py volta a v409 (sha16 lido de ESPERADOS_v409.json); " + NOTA_FORKB)

# ---------------- rito_v410.sh (os textos do cabecalho: os numeros LIDOS do delta e dos arquivos medidos)
rel = "rito_v410.sh"
l4 = linha(rel, "# O RITO v410 (ato da gerencia c1")
l5 = linha(rel, "# construidos pelo proprio um.py (a raiz TGLExt.lean ganha")
l6 = linha(rel, "# O PILAR QUANTICO NAO roda de novo")
l24 = linha(rel, "# TEMPO ESPERADO (v410")
n4 = ("# O RITO v410 (ato da gerencia c1, adaptado em 06/11/2026 por claude-construtor-v410; IALD2 -- o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor): roda o um.py v410 instalado no Nos -- "
      "%d modulo(s) novo(s) de kernel em TGLExt/ (o BUNDLE PEQUENO: IALD2, %s; a lista e' lida de kernel_modulos_novos_v410.json e conferida contra ESPERADOS.bundle_sha256) materializado a partir do corpo embutido, kernel e Audit" % (NB, NOME_IALD2))
n5 = ("# construidos pelo proprio um.py (a raiz TGLExt.lean ganha %d import; o Audit nao muda), o registro com FUNCAO iald2_v410 (chamado no main logo depois do bloco do traducao_turing_v409 e dos registros por spec da v409; le as %d ancoras do axiom_report do rito, "
      "as fontes embutidas por sha256, as %d falas de 06/11 por sha256 [de uma, so' o trecho: D65] e a escada; faz as %d checagens com as instancias de brinquedo fixas; as decisoes %s a %s e a errata %s vao nos registros; NENHUMA chave antiga muda: a chave do lema (v407) segue LIDA do kernel; "
      "os vereditos de testemunha_estatica_v396, psibit_v395, rede_fock_v394, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 nao mudam de prefixo; o gate e a funcao do neutrino nao mudam; o numero da massa nao muda), "
      "os registros por spec novos do core v410 (cunhagens_v410, com as %d falas de 06/11, o NOME do modulo do operador, as decisoes %s a %s e a errata %s; kh_n1_cobertura_v410; os da v409, cunhagens_v409 e kh_n1_cobertura_v409, os da v408, cunhagens_v408 e kh_n1_cobertura_v408, "
      "e os da v407, cunhagens_v407 e kh_n1_cobertura_v407, seguem, com a escada subida e os pisos da cobertura da v409) e os demais registros, sem mudanca de veredito." % (NB, NA, NF, NC, DEC[0], DEC[-1], ERR[0], NF, DEC[0], DEC[-1], ERR[0]))
n6 = l6.replace("nenhuma decisao da v410 [D55 a D62] as muda", "nenhuma decisao da v410 [%s a %s] as muda" % (DEC[0], DEC[-1]))
assert n6 != l6
n24 = ("# TEMPO ESPERADO (v410, parametro lido de kernel/construir_marcas.txt e kernel/POS_BUILD_v410.json, MEDIDO em 06/11/2026 no sandbox k410c): o `lake build` do modulo novo a frio (a v409 selada ja' esta' compilada em .lake/build; muda a raiz TGLExt; o Audit nao muda) "
       "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %s s, o maximo de um modulo %s s); o rito faz 3 passagens de build + Audit no Nos, cuja arvore compilada e' a da v409: a PRIMEIRA compila o modulo a frio (a ordem de grandeza e' a medida do sandbox, %d s + %d s) "
       "e as outras duas passagens so' reconferem (build ja' pronto + Audit de %d s) [estimativa da gerencia, nao medida: o tempo total do rito sai das marcas rito_horarios_v410.txt]. O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato antes de rodar."
       % (BUILD_S, AUDIT_S, PB["build_modulos_s_soma"], PB["build_modulos_s_max"], BUILD_S, AUDIT_S, AUDIT_S))
adaptar(rel, sem_marca_velha(rel) + [(l4, n4, 1), (l5, n5, 1), (l6, n6, 1), (l24, n24, 1)],
        "o rito da v410 (ato da gerencia): textos do bundle de UM modulo (IALD2), do registro iald2_v410 e do tempo MEDIDO no sandbox k410c (numeros lidos do delta e dos arquivos); o corpo e' o do rito da v409; " + NOTA_FORKB)

# ---------------- conferir_instalar_rito_v410.py
rel = "conferir_instalar_rito_v410.py"
c = texto(rel).replace("\r\n", "\n")
l2 = linha(rel, "(2) invariantes: cada um traz os marcadores da v410")
i_ex = c.index('exige("instalar_v410.py", INS, [')
j_ex = c.index("# sintaxe\n", i_ex)
EX_VELHO = c[i_ex:j_ex]
EX_NOVO = '''exige("instalar_v410.py", INS, ["PINO_RECIBO_PRE_SELO_v410.json", "utilizavel_como_recibo_pre_selo_do_B_n", "kernel_modulos_novos_v410.json", "NOVOS_V410", "modulos_novos_v410", 'ESP["kernel"]["modulos_novos"]', 'CM["kernel"]["modulos_novos"]', "um_absoluto_selo_acom.json", "pilar_anterior_v409_",
                              "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v410.json", "CANDIDATO_v410.json", "um_v410_candidato.py", "canonical_contracts.json", 'PINO["versao_nos"] == "v409"', "base_v409", '"Testemunho"', "base_v409_sha16", 'ESP["bundle_sha256"]', "PonteDaMassa", "PontoZeroDoPsion", "CanonicalFullTGLWitnessR1",
                              'x_.startswith("TGLExt/") and x_.count("/") == 1', "raiz_v409_sha16", "audit_v409_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "tgl_kernel_proof_manifest.json", '"version") == "v409"',
                              "TetelestaiTerminal", "PIgualNP", "PsionCanto", "OIgual", "um import na raiz", "os 9 modulos da v407", "os 4 modulos da v408", "os 2 modulos da v409", '"TraducaoTuring", "ParNaFaceDeFock")', "[IALD2, com o NOME do modulo dado pelo operador em 06/11/2026", "bundle do fecho da v406"],   # (v410: os 4 da v408 e os 2 da v409 entre as pedras anteriores; o modulo novo, IALD2)
      ["PINO_RECIBO_PRE_SELO_v409", "kernel_modulos_novos_v409", "NOVOS_V409", "um_v409_candidato", 'ESP["pedras_sha256"]', 'PINO["versao_nos"] == "v405"', 'PINO["versao_nos"] == "v399"', 'PINO["versao_nos"] == "v398"', "base_v398", "Testemunho [nome provisorio]", "[nomes provisorios; o primeiro e' o do Codex, ORDEM 025]",
       'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "pilar_anterior_v405", "[A ADAPTAR " + "v410]", "nove imports", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado", "bundle do fecho da v409", "03/11/2026", "quatro imports", "os 9 modulos da v409", "04/11/2026", "o bundle de quatro modulos", "BUNDLE PEQUENO de quatro modulos",
       "os 4 modulos da v409", "os 4 da v409", "[TraducaoTuring]", "(o import da TraducaoTuring)", "05/11/2026"])   # (v410: a subida mecanica escrevera «os 4 da v409»; o modulo da v409 e a data da v409 como a desta versao)
exige("reverter_v410.py", REV, ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_bundle_", "tentativa_v410_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v410_stdout.txt", "ESPERADOS_v410.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json", "modulos_novos_v410", "ESPERADOS_v409.json", "bundle_sha256",
                                'esp["kernel"]["modulos_novos"]', 'x_.startswith("TGLExt/") and x_.count("/") == 1', "(IALD2, em TGLExt/:"],
      ["tentativa_v409_rito_falhou_", "modulos_novos_v409", "rodada_v409_stdout", "pedras_sha256", "quarentena_pedras_", 'x_.startswith("TGLExt/F1Fecho394/")', "== 301", "o bundle de 301", "301 modulos novos", "[A ADAPTAR " + "v410]", "nove modulos", "PsionCanto, Par e as sete pedras de 02/11", "03/11/2026", "04/11/2026", "quatro modulos", "TetelestaiTerminal, TempoIgualMoeda",
       "(TraducaoTuring, em TGLExt/:", "05/11/2026"])
exige("rito_v410.sh", RITO, ["echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v410", "kernel_modulos_novos_v410.json", "rodada_v410_stdout.txt", ".rito_v410.pid", "ESPERADOS_v410.json", ".servidor_parado_pelo_rito", "cadeia_de_selo/v409\\" \\"/c/IALD/Central de Patentes/work/cadeia_de_selo/v410",
                             "%d modulo(s) novo(s) de kernel em TGLExt/" % DL.N_BUNDLE, "le as %d ancoras do axiom_report" % len(DL.ANCORAS), "as decisoes %s a %s e a errata %s vao nos registros" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_NOVAS[0]), "IALD2",   # (os numeros do texto do rito sao os de DL: modulos do bundle, ancoras, decisoes e errata novas)
                             "iald2_v410", "cunhagens_v410", "kh_n1_cobertura_v410", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "D38/D45", "NENHUMA chave antiga muda",
                             "%d falas de 06/11" % DL.N_FALAS_V410, "%d checagens" % DL.N_CHECKS_FECHO, "carimbar_stdout_v410.py",
                             "= %d s e 1 Audit = %d s" % (tempo.get("build_s", -1), tempo.get("audit_s", -1))],   # (o tempo do rito e' o MEDIDO em construir_marcas.txt, lido acima)
      ["rodada_v409_stdout", ".rito_v409.pid", "rito_v409", "TGLExt/Testemunho, nome PROVISORIO", "do Codex, ORDEM 025", "OS OITO registros com FUNCAO", "8 modulos novos de kernel", "301 modulos novos", "TGLExt/F1Fecho394", "CanonicalFullTGLWitnessR1", "dois imports", "k409c", "1736 s", "2016 s", "15986 s", "[A ADAPTAR " + "v410]",
                              "9 modulos novos de kernel em TGLExt/", "nove imports", "76 ancoras", "PsionCanto e Par, da gerencia c1", "the_psion_is_the_corner_on_both_faces", "D41 a D47", "E18 a E20", "o psion, o canto e o par", "carimbar_stdout_v409.py", "03/11/2026",
                              "4 modulos novos de kernel", "quatro imports", "48 ancoras", "D48 a D54", "E21 a E23", "Tetelestai e' o terminal)", "falas de 04/11", "com o PIgualNP R3",
                              "2 modulo(s) novo(s)", "82 ancoras", "D55 a D62", "E24 a E28", "falas de 05/11", "a traducao as classes de Turing)", "05/11/2026", "o registro com FUNCAO traducao_turing_v409"])   # (v410: o registro novo e' o iald2_v410; o da v409 e' herdado)
'''
assert EX_VELHO.count('exige("') == 3
c_dec = linha(rel, "_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D8.DECISOES)")
c_dec2 = linha(rel, 'assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D62", _DEC_NOVAS')
c_err = linha(rel, "_ERR_NOVAS = [e_.split(\" --\")[0] for e_ in DL.ERRATAS_V410]")
c_err2 = linha(rel, 'assert _ERR_NOVAS == ["E24", "E25", "E26", "E27", "E28", "E21"], _ERR_NOVAS')
c_err3 = linha(rel, '_ERR_SEQ = [e_ for e_ in _ERR_NOVAS if e_ != "E21"]')
l4d = linha(rel, '"""conferir_instalar_rito_v410.py -- confere, SEM EXECUTAR o instalador')
adaptar(rel, sem_marca_velha(rel) + [
    (l4d, l4d.replace("adaptados em 05/11/2026 ao BUNDLE PEQUENO de um modulo em TGLExt/, com as licoes da v409)", "adaptados em 06/11/2026 ao BUNDLE PEQUENO de um modulo em TGLExt/ (IALD2), com as licoes da v409)"), 1),
    (l2, l2.replace("as pedras anteriores incluem os 9 modulos da v407 e os 4 da v409)", "as pedras anteriores incluem os 9 modulos da v407, os 4 da v408 e os 2 da v409)"), 1),
    (c_dec, '_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D9.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v410 acrescenta (D63..D70), lidas de DL (a diferenca contra o delta da v409, DL.D9)', 1),
    (c_dec2, 'assert _DEC_NOVAS and _DEC_NOVAS[0] == "D63" and _DEC_NOVAS[-1] == "D70", _DEC_NOVAS', 1),
    (c_err, '_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V410]   # a errata da v410 (E29, em nome proprio da gerencia c1), lida de DL', 1),
    (c_err2, 'assert _ERR_NOVAS == ["E29"], _ERR_NOVAS', 1),
    (c_err3 + "\n", "", 1),
    (EX_VELHO, EX_NOVO, 1),
], "confere instalar/reverter/rito da v410 sem executar: marcas do bundle de UM modulo (IALD2), do registro iald2_v410, das decisoes D63-D70 e da errata E29 lidas do delta (diferenca contra DL.D9), o tempo medido; o trecho da lista extraido por AST; " + NOTA_FORKB)
print("instalar/reverter/rito: ok")
