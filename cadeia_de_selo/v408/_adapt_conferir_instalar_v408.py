# -*- coding: utf-8 -*-
"""_adapt_conferir_instalar_v408.py -- adapta conferir_instalar_rito_v408.py a v408 (04/11/2026, claude-construtor-v408): a parte do _adapt_instalar_reverter_rito_v408.py que nao gravou, porque a guarda daquele adaptador
recusava QUALQUER ocorrencia de `[A ADAPTAR` no texto e este conferidor traz a marca como LITERAL nas listas de rotulos velhos (e' ele quem a procura nos outros arquivos). Aqui a guarda e': nenhuma LINHA comeca pela marca.
Trocas de contagem EXATA; backup de bytes. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_instalar_rito_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n"); assert len(MARCA_RX.findall(t)) == 1; t = MARCA_RX.sub("", t, count=1)
sub("(derivados dos da v407, adaptados em 03/11/2026 ao BUNDLE PEQUENO de nove modulos em TGLExt/, com as licoes da v407)", "(derivados dos da v407, adaptados em 04/11/2026 ao BUNDLE PEQUENO de quatro modulos em TGLExt/, com as licoes da v407)")
sub("os nove modulos em TGLExt/ e nao mais em TGLExt/F1Fecho394/...)", "os quatro modulos em TGLExt/, nao em TGLExt/F1Fecho394/...; as pedras anteriores incluem os 9 modulos da v407)")
sub("_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D6.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v408 acrescenta (D41..D47), lidas de DL",
    "_DEC_NOVAS = sorted(set(DL.DECISOES) - set(DL.D7.DECISOES), key=lambda k_: int(k_[1:]))   # as decisoes que a v408 acrescenta (D48..D54), lidas de DL (a diferenca contra o delta da v407, nao contra o da v406)\nassert _DEC_NOVAS and _DEC_NOVAS[0] == \"D48\" and _DEC_NOVAS[-1] == \"D54\", _DEC_NOVAS")
sub("_ERR_NOVAS = [e_.split(\" --\")[0] for e_ in DL.ERRATAS_V408]   # as erratas da v408 (E18..E20), lidas de DL", "_ERR_NOVAS = [e_.split(\" --\")[0] for e_ in DL.ERRATAS_V408]   # as erratas da v408 (E21..E23), lidas de DL\nassert _ERR_NOVAS == [\"E21\", \"E22\", \"E23\"], _ERR_NOVAS")
sub("\"FalsidadeDaInercia\", \"PonteDaEscalaDual\", \"QuedaSemGeometria\", \"EsperancaCondicional\", \"ProjecaoTransversalDaMeiaNat\", \"Jo8v32\", \"tgl_kernel_proof_manifest.json\", '\"version\") == \"v407\"'],",
    "\"FalsidadeDaInercia\", \"PonteDaEscalaDual\", \"QuedaSemGeometria\", \"EsperancaCondicional\", \"ProjecaoTransversalDaMeiaNat\", \"Jo8v32\", \"tgl_kernel_proof_manifest.json\", '\"version\") == \"v407\"',\n                              \"TetelestaiTerminal\", \"PIgualNP\", \"PsionCanto\", \"OIgual\", \"quatro imports\", \"os 9 modulos da v407\", \"bundle do fecho da v406\"],")
sub("'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"pilar_anterior_v405\", \"[A ADAPTAR v408]\"])",
    "'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"pilar_anterior_v405\", \"[A ADAPTAR v408]\", \"nove imports\", \"nove modulos\", \"PsionCanto, Par e as sete pedras de 02/11, todos de nome ratificado\", \"bundle do fecho da v407\", \"03/11/2026\"])")
sub("\"pedras_sha256\", \"quarentena_pedras_\", 'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"[A ADAPTAR v408]\"])",
    "\"pedras_sha256\", \"quarentena_pedras_\", 'x_.startswith(\"TGLExt/F1Fecho394/\")', \"== 301\", \"o bundle de 301\", \"301 modulos novos\", \"[A ADAPTAR v408]\", \"nove modulos\", \"PsionCanto, Par e as sete pedras de 02/11\", \"03/11/2026\"])")
sub("\"psion_canto_v407\", \"PsionCanto\", \"the_psion_is_the_corner_on_both_faces\", \"linked_to_the_corner_by_a_lemma\", \"cunhagens_v407\", \"kh_n1_cobertura_v407\", \"fechamento_v406\", \"D44\",",
    "\"tetelestai_terminal_v408\", \"TetelestaiTerminal\", \"TempoIgualMoeda\", \"PontoDeContradicao\", \"PIgualNP\", \"cunhagens_v408\", \"kh_n1_cobertura_v408\", \"psion_canto_v407\", \"cunhagens_v407\", \"kh_n1_cobertura_v407\", \"fechamento_v406\", \"E21\", \"D38/D45\", \"NENHUMA chave antiga muda\", \"12 falas de 04/11\", \"carimbar_stdout_v408.py\",")
sub("[\"rodada_v407_stdout\", \".rito_v407.pid\", \"rito_v407\", \"TGLExt/Testemunho, nome PROVISORIO\", \"do Codex, ORDEM 025\", \"OS OITO registros com FUNCAO\", \"8 modulos novos de kernel\", \"301 modulos novos\", \"TGLExt/F1Fecho394\", \"CanonicalFullTGLWitnessR1\", \"dois imports\", \"k407c\", \"1736 s\", \"2016 s\", \"15986 s\", \"[A ADAPTAR v408]\"])",
    "[\"rodada_v407_stdout\", \".rito_v407.pid\", \"rito_v407\", \"TGLExt/Testemunho, nome PROVISORIO\", \"do Codex, ORDEM 025\", \"OS OITO registros com FUNCAO\", \"8 modulos novos de kernel\", \"301 modulos novos\", \"TGLExt/F1Fecho394\", \"CanonicalFullTGLWitnessR1\", \"dois imports\", \"k407c\", \"1736 s\", \"2016 s\", \"15986 s\", \"[A ADAPTAR v408]\",\n                              \"9 modulos novos de kernel em TGLExt/\", \"nove imports\", \"76 ancoras\", \"PsionCanto e Par, da gerencia c1\", \"the_psion_is_the_corner_on_both_faces\", \"D41 a D47\", \"E18 a E20\", \"o psion, o canto e o par\", \"carimbar_stdout_v407.py\", \"03/11/2026\"])")
sub('("lista_que_nao_e_lista", {"novos": "TGLExt/PsionCanto.lean"})', '("lista_que_nao_e_lista", {"novos": "TGLExt/TetelestaiTerminal.lean"})')
assert not any(l_.startswith("# [A ADAPTAR v408]") for l_ in t.split("\n")), "a marca ficou como linha"
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok conferir_instalar_rito", len(raw), "->", len(t.encode("utf-8")))
