# -*- coding: utf-8 -*-
"""aplicar_R6d_v405.py -- as duas licoes novas da R6 no deposito da fila (uso unico; nao toca nada que entre no candidato)."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "fechar_preparacao_v405.py")
b = open(p, "rb").read()
s = b.decode("utf-8")
a = "(6) guarda que nao varre a origem deixa o residuo onde ninguem olha.\\n\\n"
c = ("(6) guarda que nao varre a origem deixa o residuo onde ninguem olha; (7) contagem literal envelhece quando um registro entra: a leitura exigia quatro registros por spec depois de o quinto entrar, e so' o harness pegou; "
     "(8) um harness que reprova cedo nao roda os controles negativos: a primeira passada limpa leva muito mais tempo que a reprovada, e nao e' travamento.\\n\\n")
assert s.count(a) == 1, s.count(a)
open(p + ".bak_" + TS + "_R6d", "wb").write(b)
t = p + ".tmp_R6d"
open(t, "wb").write(s.replace(a, c).encode("utf-8"))
os.replace(t, p)
print("ok", TS)
