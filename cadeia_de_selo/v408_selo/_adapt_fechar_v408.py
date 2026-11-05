# -*- coding: utf-8 -*-
"""_adapt_fechar_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) adapta fechar_v408.py a v408 por trocas de CONTAGEM EXATA: as notas do cabecalho (a marca da subida mecanica sai; a nota falsa de 03/11 da' lugar a uma verdadeira),
a docstring e os comentarios (o conteudo passa de «o psion, o canto e o par» a «Tetelestai e' o terminal»; a nota ao lado passa de E18 a E21) e o MANIFESTO de incorporacao: as chaves versionadas passam a registros_v408/v407/v406..., registros_funcao_v408/v407/v406,
ancoras/bandeiras_v408/v407/v406, chaves_v407 e chaves_v406 (sem chaves_v408: nenhuma chave antiga muda), funcoes_v407/v406_recriadas, pedras_v407/v406/v405_como_registro; as chaves de V fora do contrato combinado com o fork A entram por .get() (nunca KeyError).
Backup de BYTES (.bak_<TS>_adapt); temporario -> conferir -> substituir; ast.parse; CRLF preservado. Escrito pelo Write (o heredoc do Bash colapsa barras). Fail-closed: contagem errada = nada gravado."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
s16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
P = os.path.join(HERE, "fechar_v408.py")
raw = open(P, "rb").read(); t = raw.decode("utf-8"); NL = "\r\n" if b"\r\n" in raw else "\n"; n = 0


def sub(a, b, k=1):
    global t, n
    a = a.replace("\r\n", "\n").replace("\n", NL); b = b.replace("\r\n", "\n").replace("\n", NL)
    c = t.count(a); assert c == k, "esperava %d ocorrencia(s) e achou %d: %r" % (k, c, a[:90])
    t = t.replace(a, b); n += 1


def linha(prefixo, nova=None):
    global t, n
    ls = t.split(NL); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
    assert len(idx) == 1, "prefixo de linha esperava 1 e achou %d: %r" % (len(idx), prefixo[:80])
    if nova is None:
        del ls[idx[0]]
    else:
        ls[idx[0]] = nova
    t = NL.join(ls); n += 1


linha("# [A ADAPTAR v408]")
linha("# [ADAPTADO v408, 03/11/2026", "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] sobre a subida mecanica da v407 FINAL (_bump_copia_v408.py), por _adapt_fechar_v408.py: o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: os quatro modulos de TGLExt/, o registro com funcao tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408; o psion_canto_v407 e o fechamento_v406 herdados; nenhuma chave antiga muda; erratas E21 a E23 ao lado); o MANIFESTO ganhou as chaves versionadas da v408 (registros_v408/v407/v406, registros_funcao_v408/v407/v406, pedras_v407/v406_como_registro) e os registros das versoes anteriores sao lidos de V (fork A) e do core; conferido por ast.parse e pelo harness do fechar em sandbox; a gerencia revisa antes do rito (nao e' versao selada).")
linha("# v408 (O PSION, O CANTO E O PAR, 03/11/2026): o CONTEUDO v408", "# v408 (TETELESTAI E' O TERMINAL, 04/11/2026): o CONTEUDO v408 (o terminal e' a leitura, nao o fim do decaimento; o tempo e' a moeda de beta; o ponto de contradicao; «P=nP» so' no sentido do operador; os quatro modulos novos e as falas de 04/11) vive em textos_v408.py (fork A) e e' testado pelo harness_textos_ensaio_v408.py; este arquivo trata o MANIFESTO com as chaves de V da v408 (sem chaves_v408: nenhuma chave antiga muda).")
sub("mais os 9 modulos novos do Nos) -> work\\\\cadeia_de_selo\\\\v408_kernel;", "mais os modulos novos do Nos) -> work\\\\cadeia_de_selo\\\\v408_kernel;")
sub("DIFF_KERNEL_v408.txt (o kernel embutido: os 9 modulos novos de TGLExt/, a raiz e o Audit);", "DIFF_KERNEL_v408.txt (o kernel embutido: os modulos novos de TGLExt/ do bundle da v408, a raiz e o Audit);")
sub("(b) o NOVO, o paragrafo da v408 (o psion, o canto e o par), gerado do registro selado psion_canto_v407", "(b) o NOVO, o paragrafo da v408 (Tetelestai e' o terminal), gerado do registro selado tetelestai_terminal_v408")
sub("a ordem e as decisoes do operador de 03/11 verbatim, a moldura e a guarda das frases, sem o 4,44); o handoff traz tambem a NOTA ao lado dos paragrafos anteriores (E18: a chave do lema era literal False e passou a leitura do kernel) e DIZ que os paragrafos do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da massa derivada (v405) e do fechamento (v407) SEGUEM COMO ESTAO,",
    "a ordem e as decisoes do operador de 04/11 verbatim, a moldura e a guarda das frases, sem o 4,44); o handoff traz tambem a NOTA ao lado do paragrafo da v407 (E21: o [OPEN] do par na face de Fock e' de ligacao, nao de ausencia de termo) e DIZ que os paragrafos do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da massa derivada (v405), do fechamento (v406) e do psion, do canto e do par (v407) SEGUEM COMO ESTAO,")
sub("(2) o paragrafo NOVO da v408 (o psion, o canto e o par), gerado dos registros selados e verificado contra o core e contra ESPERADOS", "(2) o paragrafo NOVO da v408 (Tetelestai e' o terminal), gerado dos registros selados e verificado contra o core e contra ESPERADOS")
sub("ou o da v408: o psion, o canto e o par) nao passou nas verificacoes", "ou o da v408: Tetelestai e' o terminal) nao passou nas verificacoes")
linha("# v408: o manifesto lista as fontes pinadas dos registros (insumos/: as nove pedras", "# v408: o manifesto lista as fontes pinadas dos registros (insumos/: os quatro modulos e as candidatas de origem, os recibos de compilacao, a afericao do traco e do dicionario, a copia purgada do insumo do acervo e o recibo da purga, o recibo dos nomes, o desenho, o bundle e a medida KH-N1); as falas ficam em insumos/cunhagens (indexadas no arquivo)")
sub('"registros_v407": V["reg408"], "registros_v406": V["reg407d"], "registros_v405": V["reg407c"], "registros_v404": V.get("reg407b"), "registros_v403": V["reg407_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "registros_funcao_v408": {"psion_canto_v407": V["fecho"]}, "registros_funcao_v407": {"fechamento_v406": V["fecho407"]}, "ancoras_v408": V["ancoras"], "ancoras_v407": V["ancoras407"], "bandeiras_v408": V["bandeiras"], "bandeiras_v407": V["bandeiras407"], "chaves_v408": V["chaves"], "chaves_v406": V["chaves407"], "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v407_recriadas": {"fechamento_v406": V["fecho407"]}, "funcoes_v405_recriadas": V["fun407c"], "funcoes_v404_recriadas": V.get("fun407b"), "funcoes_v403_recriadas": V["fun407"], "funcoes_v402_recriadas": V["fun402"], "pedras_v407_como_registro": V["bundle407"], "pedras_v405_como_registro": V["pedras_v407"], "falsidade_v401": V["fal401"],',
    '"registros_v408": V["reg408"], "registros_v407": V["reg407d"], "registros_v406": V.get("reg406d"), "registros_v405": V["reg407c"], "registros_v404": V.get("reg407b"), "registros_v403": V["reg407_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho"]}, "registros_funcao_v407": {"psion_canto_v407": V["fecho407"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v408": V["ancoras"], "ancoras_v407": V["ancoras407"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v408": V["bandeiras"], "bandeiras_v407": V["bandeiras407"], "bandeiras_v406": V.get("bandeiras406"), "chaves_v407": V["chaves407"], "chaves_v406": V.get("chaves406"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v407_recriadas": {"psion_canto_v407": V["fecho407"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")}, "funcoes_v405_recriadas": V["fun407c"], "funcoes_v404_recriadas": V.get("fun407b"), "funcoes_v403_recriadas": V["fun407"], "funcoes_v402_recriadas": V["fun402"], "pedras_v407_como_registro": V["bundle407"], "pedras_v406_como_registro": V.get("bundle406"), "pedras_v405_como_registro": V["pedras_v407"], "falsidade_v401": V["fal401"],')
sub('"massa_derivada_e_identidade_v405", "o_fechamento_v407"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": True,', '"massa_derivada_e_identidade_v405", "o_fechamento_v406", "o_psion_o_canto_e_o_par_v407"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": True,')
assert "# [A ADAPTAR v408]" not in t and "[ADAPTADO v408, 03/11/2026" not in t and "psion_canto_v407\": V[\"fecho\"]" not in t
novo = t.encode("utf-8"); assert novo != raw
ast.parse(t)
bak = P + ".bak_" + TS + "_adapt"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = P + ".tmp_adapt"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, P); assert open(P, "rb").read() == novo
print("fechar_v408.py %d troca(s): %d B -> %d B sha16 %s -> %s (%s; ast ok; backup %s)" % (n, len(raw), len(novo), s16(raw), s16(novo), "CRLF" if NL == "\r\n" else "LF", os.path.basename(bak)))
