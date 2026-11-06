p = "fechar_revisao.py"
t = open(p, encoding="utf-8").read()
t = t.replace("(2) a paragrafo «As respostas", "(2) o paragrafo «As respostas").replace("o par de psiões na face de Fock (ligacao)", "o par de psíons na face de Fock (ligação)")
t = t.replace("38 nomes iguais por AST e fonte", "%d nomes iguais por AST e fonte' % sum(1 for v in a1['nomes'].values() if v.get('ast_igual') and v.get('fonte_igual')) + '")
t = t.replace("c_fail_closed.py (127 casos)", "c_fail_closed.py (%d casos' % (n_cfc_ok + len(n_cfc_f)) + ")
t = t.replace("f_hashes.py (63 checagens ok)", "f_hashes.py (%d checagens ok' % sum(1 for v in fh['ok'].values() if v) + ")
open(p, "w", encoding="utf-8", newline="\n").write(t)
