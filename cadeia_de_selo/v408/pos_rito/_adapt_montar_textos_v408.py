# -*- coding: utf-8 -*-
"""_adapt_montar_textos_v408.py -- adaptacao EXATA (contagem conferida) de pos_rito\\montar_textos_v408.py para a v408 (04/11/2026, claude-construtor-v408, fork A):
(1) as duas notas do topo (a marca [A ADAPTAR v408] e a nota falsa de 03/11) viram a nota verdadeira; (2) a docstring diz o conteudo da v408; (3) DELETAR ganha _fam_gate (helper das oito pedras da v405 que nenhum texto da v408 usa);
(4) o fragmento (CRLF) e' normalizado para LF ao ser lido (a semente e' LF; o montador corta em "\\n"). Backup de bytes antes de gravar. uso: python -I -B -X utf8 _adapt_montar_textos_v408.py"""
import datetime, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "montar_textos_v408.py")
SUBS = [
    ("# [A ADAPTAR v408] SUBIDA MECANICA DE ROTULO (v407->v408) do molde v407/pos_rito/montar_textos_v407.py; o CORPO e' o da v407 (bundle de 9 modulos, psion_canto_v407, a chave do lema lida do kernel); nada rodou; ver bump/pos_rito__montar_textos_v408.py.diff\r\n"
     "# [ADAPTADO v408, 03/11/2026, claude-prep-v408 / ajudante B1a] sobre a subida mecanica da v407 FINAL: o conteudo e' o da v408 (O PSION, O CANTO E O PAR: 9 modulos de TGLExt/, o registro com funcao psion_canto_v407, a chave do lema lida do kernel); a gerencia revisa antes do rito (nao e' versao selada).\r\n",
     "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v407 FINAL (bump/pos_rito__montar_textos_v408.py.diff fica como registro): o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: 4 modulos de TGLExt/, o registro com funcao tetelestai_terminal_v408, nenhuma chave antiga muda); o fragmento e' CRLF e e' normalizado para LF ao ser lido; a gerencia revisa antes do rito (nao e' versao selada).\r\n", 1),
    ("enxertando as definicoes de textos_v408_novo.pysnip (escritas para a v408, sem prosa nova de conteudo: o psion, o canto e o par) no esqueleto",
     "enxertando as definicoes de textos_v408_novo.pysnip (escritas para a v408, sem prosa nova de conteudo: Tetelestai e' o terminal) no esqueleto", 1),
    ("DELETAR = {\"_caminho\", \"_vida\", \"_verdade_adendo\", \"_bandeiras\", \"_leitura_tripla\", \"_cod025\", \"_projecao\", \"_jo8\", \"_f2b\", \"_TEMAS\", \"N_FALAS\",\r\n           \"_CHAVES\", \"_REG_DE\", \"_NOME_DE\", \"_ponte\", \"_tensao\", \"_lei\", \"_gap\", \"_zero\", \"_disco\", \"_obs\", \"_ident\", \"_ga\", \"_blocos_pedras\", \"_massa\", \"g_flag\"}   # as funcoes das OITO pedras da v405 (REGISTRO recriado, sem texto proprio na v408: o delta e' o bundle dos 9 modulos, nao ha' pedra com texto), as constantes que as indexavam e a leitura da v405 (_massa, trocada por _leituras); mais as velhas",
     "DELETAR = {\"_caminho\", \"_vida\", \"_verdade_adendo\", \"_bandeiras\", \"_leitura_tripla\", \"_cod025\", \"_projecao\", \"_jo8\", \"_f2b\", \"_TEMAS\", \"N_FALAS\",\r\n           \"_CHAVES\", \"_REG_DE\", \"_NOME_DE\", \"_ponte\", \"_tensao\", \"_lei\", \"_gap\", \"_zero\", \"_disco\", \"_obs\", \"_ident\", \"_ga\", \"_blocos_pedras\", \"_massa\", \"g_flag\", \"_fam_gate\"}   # as funcoes das OITO pedras da v405 (REGISTRO recriado, sem texto proprio na v408: o delta e' o bundle dos 4 modulos, nao ha' pedra com texto), as constantes que as indexavam, a leitura da v405 (_massa, trocada por _leituras) e os helpers so' delas (g_flag, _fam_gate); mais as velhas", 1),
    ("    seed = open(SEMENTE, \"rb\").read().decode(\"utf-8\"); novo = open(NOVO, \"rb\").read().decode(\"utf-8\")\r\n",
     "    seed = open(SEMENTE, \"rb\").read().decode(\"utf-8\"); novo = open(NOVO, \"rb\").read().decode(\"utf-8\").replace(\"\\r\\n\", \"\\n\")   # v408: o fragmento e' CRLF (como o molde); a semente e' LF e o montador corta em \"\\n\"\r\n", 1),
]


def main():
    b = open(ALVO, "rb").read(); t = b.decode("utf-8")
    assert "\r\n" in t, "o montar_textos_v408.py deixou de ser CRLF: adaptador escrito para o molde CRLF"
    for velho, novo, vezes in SUBS:
        c = t.count(velho)
        assert c == vezes, ("substituicao nao casou (contagem)", vezes, c, velho[:90])
        t = t.replace(velho, novo)
    assert "[A ADAPTAR v408]" not in t and "03/11/2026" not in t, "sobrou a marca ou a nota falsa"
    compile(t.replace("\r\n", "\n"), ALVO, "exec")
    bak = ALVO + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt"
    open(bak, "wb").write(b)
    tmp = ALVO + ".tmp"; open(tmp, "wb").write(t.encode("utf-8"))
    assert os.path.getsize(tmp) > len(b) - 200, "o montar adaptado encolheu demais"
    os.replace(tmp, ALVO)
    print("ok montar_textos_v408.py %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(ALVO), hashlib.sha256(open(ALVO, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


if __name__ == "__main__":
    main()
