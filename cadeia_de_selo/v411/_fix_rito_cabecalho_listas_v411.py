# -*- coding: utf-8 -*-
"""_fix_rito_cabecalho_listas_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
conferir_instalar_rito_v411.py: o cabecalho do rito_v411.sh (o texto que o rito mostra antes de rodar) dizia «9 falas de 11 e 12/11» e «as
decisoes D159 a D170»; a lista cresceu por ordem da gerencia (12/11, D172 e D173: DL.FALAS_V411 com 11, DL.DECISOES_V411 de D159 a D173). A causa:
o cabecalho escrito antes da ordem. O conserto: os dois numeros do cabecalho passam a ser os do delta (lidos aqui por script, nao digitados);
nenhum comando do rito muda (so' o comentario). Backup de BYTES antes; ancoras unicas; `sh -n` depois. uso: python -B -X utf8 _fix_rito_cabecalho_listas_v411.py"""
import datetime, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
P = os.path.join(HERE, "rito_v411.sh")
b = open(P, "rb").read(); t = b.decode("utf-8")
_dec = sorted(DL.DECISOES_V411, key=lambda k_: int(k_[1:]))
PARES = [("9 falas de 11 e 12/11 por sha256", "%d falas de 11 e 12/11 por sha256" % len(DL.FALAS_V411)),
         ("as decisoes D159 a D170 e as erratas E41, E42 e E43 vao nos registros", "as decisoes %s a %s e as erratas E41, E42 e E43 vao nos registros" % (_dec[0], _dec[-1]))]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_, t.count(a_))
    t = t.replace(a_, n_)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_listas"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
r = subprocess.run(["sh", "-n", P], capture_output=True, text=True); assert r.returncode == 0, r.stderr
print("ok", len(b), "->", len(nb), "| sh -n rc", r.returncode)
