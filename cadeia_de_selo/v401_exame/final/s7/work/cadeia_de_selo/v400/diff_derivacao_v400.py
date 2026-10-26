# -*- coding: utf-8 -*-
"""diff_derivacao_v400.py -- para cada arquivo derivado cuja versao em disco DIFERE do que o motor+regras produzem hoje, mostra o diff (disco -> derivado de hoje).
Escreve SO' em _tmp_diff\\ (dentro desta pasta). uso: python -I -B -X utf8 diff_derivacao_v400.py [NOME ...]"""
import difflib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derivar_v400_motor as M  # noqa: E402
src_der = open(os.path.join(HERE, "derivar_encanamento_v400.py"), encoding="utf-8").read()
ns = {"__name__": "diff_derivacao", "__file__": os.path.join(HERE, "derivar_encanamento_v400.py")}
cod = src_der.split("def main():")[0]    # so' a parte que define `entrada` e carrega os lotes de regras
exec(compile(cod, "derivar_encanamento_v400.py(topo)", "exec"), ns)
quer = set(sys.argv[1:])
for src, dst, regras, prot_extra, com_bump, autoral in ns["ENTRADAS"]:
    if quer and os.path.basename(dst) not in quer and dst not in quer:
        continue
    tmp = "_tmp_diff/" + dst
    r = M.derivar(src, tmp, regras, prot_extra, com_bump, True)
    atual = open(os.path.join(HERE, *dst.split("/")), "rb").read().decode("utf-8")
    novo = open(os.path.join(HERE, *tmp.split("/")), "rb").read().decode("utf-8")
    if atual == novo:
        print("IGUAL   ", dst); continue
    d = list(difflib.unified_diff(atual.splitlines(), novo.splitlines(), "disco/" + dst, "derivado-de-hoje/" + dst, n=0, lineterm=""))
    print("DIFERE  ", dst, "(%d linhas de diff)" % len(d))
    for l in d[:60]:
        print("   ", l[:330])
