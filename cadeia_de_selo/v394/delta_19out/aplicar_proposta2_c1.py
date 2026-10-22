import datetime
import hashlib
import os

P = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v394/pos_rito/textos_v394.py"
sh = lambda b: hashlib.sha256(b).hexdigest()[:16]
b = open(P, "rb").read()
assert sh(b) == "3175c59f35c1ec3b", sh(b)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts + "_c1p2", "wb").write(b)
old = b'    ex = [k for k in V["registros_novos"] if k not in V["reg_todos"]]\n'
new = (b'    # d19 (proposta 2): os registros novos ALEM DOS CINCO FIXOS (V["reg394"] tem so\' os cinco), ditos pelo nome: '
       b'o sexto, criterio_binario_de_parada_v394, entra aqui\n'
       b'    ex = [k for k in V["registros_novos"] if k not in V["reg394"]]\n')
assert b.count(old) == 1
nb = b.replace(old, new)
tmp = P + ".tmp_" + ts
open(tmp, "wb").write(nb)
assert os.path.getsize(tmp) > len(b)
os.replace(tmp, P)
print("ok", sh(b), "->", sh(nb), "(proposta dizia b4c31af18c1bbc94)")
