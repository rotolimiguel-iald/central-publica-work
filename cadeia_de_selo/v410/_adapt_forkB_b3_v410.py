# -*- coding: utf-8 -*-
"""_adapt_forkB_b3_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) adapta a v410 os scripts do servico da Bancada (B3): recibo_parada, recibo_religamento, evento_c1_b3, o conferidor estatico
das exigencias e o controle negativo dele. O que muda: a ORDEM da v410 e' a fala do operador de 06/11/2026 (DL.N_ORDEM_V410; a frase DL.FRASE_ORDEM_V410, verbatim; o sha16 LIDO do arquivo pelos scripts, nunca digitado);
a data no AUT passa a 06/11/2026 e a da v409 (05/11/2026) passa a ser autorizacao ANTERIOR (proibida como texto nos recibos); o M5 do controle negativo volta a data da v409 e o M6 troca o nome da fala por um inexistente.
O resto (B19, v409 -> v410, RECIBO_RELIGAMENTO_v409.json, o recibo do B(n) da v409) a subida mecanica ja' deixou certo (conferido no diff do bump). Trocas de contagem exata; backup de bytes; CRLF respeitado."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_forkB_util_v410 import adaptar, linha, NOTA_FORKB  # noqa: E402
import delta_v410 as DL  # noqa: E402

N_V409_ARQ = "OPERADOR_05nov_prossigamos_v410_concordo_com_os_nomes_verbatim.txt"   # (o nome que a subida mecanica deixou: nao existe em disco)
N_V409_PROT = "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes"               # (o mesmo nome, que a subida nao tocou num ponto: o da v409)
F_V409 = "Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados"
N_V410 = DL.N_ORDEM_V410
F_V410 = DL.FRASE_ORDEM_V410
assert F_V410 in open(os.path.join(DL._CUN13, N_V410), encoding="utf-8").read(), "a frase da ordem da v410 nao e' verbatim no arquivo da fala"
assert not os.path.exists(os.path.join(DL._CUN13, N_V409_ARQ))

for rel, saida, doc_ordem in (("bancada_B3_servico/recibo_parada_v410.py", "RECIBO_PARADA_v410.json", None),
                              ("bancada_B3_servico/recibo_religamento_v410.py", "RECIBO_RELIGAMENTO_v410.json", "A autorizacao e' a ORDEM da v410, do operador, de 05/11/2026 (a fala e' lida do arquivo e conferida contra o texto passado pelo orquestrador).")):
    l2 = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410] a ORDEM da v410")
    l3 = linha(rel, "# (nota herdada da adaptacao da v409 [fork C da cadeia v409]")
    l17 = linha(rel, "# a autorizacao tem de ser a ORDEM da v410, de 05/11/2026")
    la = linha(rel, "assert FRASE_DA_ORDEM in ORDEM_BYTES")
    n3 = (l3.replace("(nota herdada da adaptacao da v409 [fork C da cadeia v409], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                     "(nota herdada da adaptacao da v408 [fork C da cadeia v408], reconferida pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)")
            .replace("(fala do operador de 05/11/2026, " + N_V409_ARQ + ", sha16 LIDO do arquivo;", "(fala do operador de 06/11/2026, " + N_V410 + ", sha16 LIDO do arquivo;"))
    assert n3 != l3 and "05/11/2026" not in n3 and N_V409_ARQ not in n3, rel
    trocas = [(l2, "", 1), (l3, n3, 1),
              (l17, l17.replace("de 05/11/2026 (nao a de 04/11 da v409 nem as anteriores)", "de 06/11/2026 (nao a de 05/11 da v409 nem as anteriores)"), 1),
              ('"cunhagens_13out", "%s")' % N_V409_ARQ, '"cunhagens_13out", "%s")' % N_V410, 1),
              ('FRASE_DA_ORDEM = "%s"' % F_V409, 'FRASE_DA_ORDEM = "%s"' % F_V410, 1),
              (la, la.replace('"05/11/2026" in AUT', '"06/11/2026" in AUT').replace("a ordem do operador de 05/11/2026 (a ordem da v410", "a ordem do operador de 06/11/2026 (a ordem da v410"), 1)]
    if doc_ordem:
        trocas.append((doc_ordem, doc_ordem.replace("de 05/11/2026", "de 06/11/2026"), 1))
    else:
        l5 = linha(rel, '"""10-bis-a da v410')
        trocas.append((l5, l5.replace("do operador, de 05/11/2026", "do operador, de 06/11/2026"), 1))
    # (a linha 2 antiga sai inteira: a nota nova vai na marca [ADAPTADO v410])
    nota = ("a ORDEM da v410 e' a fala de 06/11/2026 (%s; frase verbatim conferida no arquivo e no AUT; sha16 lido do arquivo); grava so' %s; %s" % (N_V410, saida, NOTA_FORKB))
    adaptar(rel, [(a + ("\n" if a == l2 else ""), b, n) if a == l2 else (a, b, n) for a, b, n in trocas], nota)

# evento: so' as notas (o corpo e' generico; a subida ja' deixou v410/B19/ESPERADOS_v410)
rel = "bancada_B3_servico/evento_c1_b3_v410.py"
l2 = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410] evento do B(n) da v410")
adaptar(rel, [(l2 + "\n", "", 1)], "evento do B(n) da v410 (B19, passo simples v409 -> v410); candidato_sha16 LIDO de ESPERADOS_v410.json e conferido contra o um.py do Nos antes de anotar; " + NOTA_FORKB)

# o conferidor estatico das exigencias
rel = "bancada_B3_servico/conferir_exigencias_servico_v410.py"
l3 = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410] confere a ORDEM da v410")
l4 = linha(rel, "# (nota herdada da adaptacao da v409 [fork C, 04/11/2026]")
le = linha(rel, "  (e) a autorizacao e' a ORDEM da v410, do operador, de 05/11/2026")
lo = linha(rel, "    chk(nome + \": a ordem de 05/11 (a ordem da v410) e' conferida")
ld = linha(rel, "    chk(nome + \": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026 a 04/11/2026")
lf = linha(rel, "chk(\"a fala do operador de 05/11 (a ordem da v410")
lt = linha(rel, "chk(\"o AUT do orquestrador (pos_treino_v410.py) e' a ordem de 05/11")
n4 = (l4.replace("(nota herdada da adaptacao da v409 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                 "(nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)")
        .replace("(fala de 05/11/2026; sha16 calculado do arquivo aqui e nos scripts); nenhuma data de autorizacao anterior (01/11, 02/11, 03/11) pode sobrar nos scripts;",
                 "(fala de 06/11/2026; sha16 calculado do arquivo aqui e nos scripts); nenhuma data de autorizacao anterior (01/11 a 05/11) pode sobrar nos scripts;"))
assert n4 != l4
NOVO_D = ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026", "05/11/2026")
adaptar(rel, [
    (l3 + "\n", "", 1), (l4, n4, 1),
    (le, le.replace("de 05/11/2026 («" + F_V409 + "»)", "de 06/11/2026 («" + F_V410 + "»)").replace("(01/11, 02/11, 03/11)", "(01/11 a 05/11)"), 1),
    ('ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "%s")' % N_V409_ARQ, 'ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", DL_N_ORDEM)', 1),
    ('FRASE_DA_ORDEM = "%s"\n' % F_V409, 'FRASE_DA_ORDEM = DL_FRASE_ORDEM\n', 1),
    (lo, lo.replace("a ordem de 05/11 (a ordem da v410)", "a ordem de 06/11 (a ordem da v410)").replace('"%s" in txt' % N_V409_PROT, "DL_N_ORDEM in txt"), 1),
    (ld, ld.replace("(01/11/2026 a 04/11/2026;", "(01/11/2026 a 05/11/2026, as datas das ordens anteriores;").replace('("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026")', repr(NOVO_D).replace("'", '"')).replace("[[False, False, False, False], []]", "[[False, False, False, False, False], []]"), 1),
    ("# ---- a ordem do operador de 05/11 (a ordem da v410) e o AUT do orquestrador", "# ---- a ordem do operador de 06/11 (a ordem da v410) e o AUT do orquestrador", 1),
    (lf, lf.replace("a fala do operador de 05/11 (a ordem da v410: prossigamos para a proxima versao do um.py; a ratificacao dos nomes)", "a fala do operador de 06/11 (a ordem da v410: a forma da matriz finita e' o signo; tudo entra no um.py)"), 1),
    (lt, lt.replace("e' a ordem de 05/11 (a ordem da v410)", "e' a ordem de 06/11 (a ordem da v410)").replace('"05/11/2026" in aut_orq and "01/11/2026" not in aut_orq', '"06/11/2026" in aut_orq and "05/11/2026" not in aut_orq and "01/11/2026" not in aut_orq').replace("e nenhum texto de 01/11", "e nenhum texto de 01/11 nem de 05/11"), 1),
    ("chk = None if False else chk\n" if False else "def chk(nome, ok, observado, esperado=True):\n", "# (v410) a ORDEM da v410 e a frase dela vem do DELTA desta pasta (sem executar o delta: nome e frase sao lidos do texto dele por ast), conferidos contra o arquivo da fala\n"
     "def _do_delta(nome_):\n    for n_ in ast.parse(open(os.path.join(V, \"delta_v410.py\"), encoding=\"utf-8\").read()).body:\n"
     "        if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == nome_ for t_ in n_.targets) and isinstance(n_.value, ast.Constant):\n            return n_.value.value\n    return None\n\n\n"
     "DL_FRASE_ORDEM = _do_delta(\"FRASE_ORDEM_V410\")\nDL_N_ORDEM = \"" + N_V410 + "\"   # (o nome do arquivo da ORDEM da v410; o delta o le do recibo da gerencia: DL.N_ORDEM_V410)\nassert DL_FRASE_ORDEM, \"a frase da ordem nao foi lida do delta_v410\"\n\n\n"
     "def chk(nome, ok, observado, esperado=True):\n", 1),
], "confere a ORDEM da v410 (06/11/2026, a fala " + N_V410 + "; a frase lida do delta_v410), as datas das ordens anteriores (01 a 05/11) ausentes e o AUT do orquestrador com o sha16 lido, a frase e a data; " + NOTA_FORKB)

# o controle negativo do conferidor
rel = "bancada_B3_servico/controle_negativo/mutar_conferidor_v410.py"
l3 = linha(rel, "# [ADAPTADO v410, 05/11/2026, claude-construtor-v410] controle negativo do conferidor do servico")
l4 = linha(rel, "# (nota herdada da adaptacao da v409 [fork C, 04/11/2026]")
n4 = (l4.replace("(nota herdada da adaptacao da v409 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                 "(nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)")
        .replace("M4 e M6 falam da ORDEM da v410 (fala de 05/11); M5 volta a data da autorizacao anterior (04/11/2026) como texto;", "M4 e M6 falam da ORDEM da v410 (fala de 06/11); M5 volta a data da autorizacao anterior (05/11/2026, a da v409) como texto;"))
assert n4 != l4
m6a = linha(rel, "    a = '\"cunhagens_13out\", \"%s\")'" % N_V409_ARQ)
adaptar(rel, [
    (l3 + "\n", "", 1), (l4, n4, 1),
    ("  M4  recibo_parada_v410.py      : sai a conferencia da ordem de 05/11 (a ordem da v410:", "  M4  recibo_parada_v410.py      : sai a conferencia da ordem de 06/11 (a ordem da v410:", 1),
    ("  M5  recibo_religamento_v410.py : volta a data da ordem anterior (04/11/2026, a da v409) como texto no script (autorizacao anterior sobrando).", "  M5  recibo_religamento_v410.py : volta a data da ordem anterior (05/11/2026, a da v409) como texto no script (autorizacao anterior sobrando).", 1),
    ("  M6  recibo_parada_v410.py      : o caminho do arquivo da fala de 05/11 vira um nome que NAO existe (v410 no lugar de v410: o tipo de defeito que uma subida mecanica de rotulo introduz).",
     "  M6  recibo_parada_v410.py      : o caminho do arquivo da fala de 06/11 vira um nome que NAO existe (um rotulo de versao enfiado no nome: o tipo de defeito que uma subida mecanica de rotulo introduz).", 1),
    ("def m4(t):   # sai a conferencia da ordem de 05/11 (a ordem da v410)", "def m4(t):   # sai a conferencia da ordem de 06/11 (a ordem da v410)", 1),
    ('    return t.replace(a, a + " (autorizacao de 04/11/2026)", 1)', '    return t.replace(a, a + " (autorizacao de 05/11/2026)", 1)', 1),
    ("def m6(t):   # o nome do arquivo da fala vira um inexistente (v410 no lugar de v410), o tipo de defeito que uma subida mecanica de rotulo introduz",
     "def m6(t):   # o nome do arquivo da fala vira um inexistente (um rotulo de versao enfiado no nome), o tipo de defeito que uma subida mecanica de rotulo introduz", 1),
    (m6a, m6a.replace(N_V409_ARQ, N_V410).replace("   # (so' o caminho que o script ABRE; o nome aparece tambem na nota da 2a linha)", "   # (so' o caminho que o script ABRE; o nome aparece tambem na nota da marca)"), 1),
    ('    return t.replace(a, a.replace("_v410_", "_v410_"), 1)', '    return t.replace(a, a.replace("OPERADOR_06nov_", "OPERADOR_06nov_v410_"), 1)', 1),
    ('("M4_sem_a_conferencia_da_ordem_de_05nov", "recibo_parada_v410.py", m4, "recibo_parada_v410.py: a ordem de 05/11 (a ordem da v410) e\' conferida")',
     '("M4_sem_a_conferencia_da_ordem_de_06nov", "recibo_parada_v410.py", m4, "recibo_parada_v410.py: a ordem de 06/11 (a ordem da v410) e\' conferida")', 1),
    ('("M5_data_da_ordem_de_04nov_no_script"', '("M5_data_da_ordem_de_05nov_no_script"', 1),
], "controle negativo do conferidor do servico: M4 a M6 sobre a ORDEM da v410 (06/11/2026); M5 com a data da ordem da v409 (05/11/2026); " + NOTA_FORKB)
print("B3: ok")
