# -*- coding: utf-8 -*-
"""_fix_esperados_troca_dita_selo_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
gerar_esperados_v411.py sobre o candidato real 21e87eb3df5098f8: a linha 283 reprova porque o selo de estatuto_da_prova_v391 difere do da v410.
Esse registro carrega o HASH PROPRIO do um.py (a troca dita: muda em toda versao; a linha 143 ja' o admite em `troca`, e a 147-148 o tira de
selo_chaves_que_mudam). A causa: na porta da v410 para a v411 a lista EXPLICITA da v410 (gerar_esperados_v410.py, linha 464, que nao traz
estatuto_da_prova_v391) virou "todas as SEL_KEYS menos registros_v410", sem tirar a troca dita. O conserto: tirar tambem `troca` (a medida pelo
ensaio, ja' restrita na linha 143 a {estatuto_da_prova_v391} e a troca da v410), como a linha 147 faz. Nenhum teste relaxado: qualquer outra
chave de versao anterior que mude segue reprovando. Backup de BYTES antes; ancora unica; ast.parse. uso: python -B -X utf8 _fix_esperados_troca_dita_selo_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_esperados_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = 'assert not (set(SEL_KEYS) - {"registros_v410"}) & set(difere_selo), ("o selo de uma versao anterior mudou: os registros anteriores NAO se mexem", sorted((set(SEL_KEYS) - {"registros_v410"}) & set(difere_selo)))\n'
n = ('assert not (set(SEL_KEYS) - {"registros_v410"} - set(troca)) & set(difere_selo), ("o selo de uma versao anterior mudou: os registros anteriores NAO se mexem (fora da troca dita: o hash proprio do um.py)", sorted((set(SEL_KEYS) - {"registros_v410"} - set(troca)) & set(difere_selo)))\n')
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_troca_dita"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
