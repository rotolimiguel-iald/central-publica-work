# -*- coding: utf-8 -*-
"""A3 (preparo) -- copia SO-LEITURA dos insumos do ensaio otico para <r2>/otico, com conferencia de bytes.
O run_optico.py usa caminhos relativos ao proprio arquivo (AQUI, WORK = pai): por isso a copia replica
1_PREREGISTRO/ (os 30 arquivos congelados) e, em 2_OPTICO/, o script, as consultas do cetico aferidor
(consultas_mapa/) e o RESULTADO da rodada 1 (so para a comparacao de vereditos que o script faz)."""
import hashlib, json, os, shutil, sys

U = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(R2, "otico")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


copias = []
def cp(src_rel, dst_rel=None):
    s = os.path.join(U, src_rel)
    d = os.path.join(DST, dst_rel or src_rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if os.path.exists(d):
        raise SystemExit("FALHA VISIVEL: destino ja existe " + d)
    shutil.copyfile(s, d)
    hs, hd = sha(s), sha(d)
    copias.append(dict(origem=s, destino=d, sha256=hs, confere=(hs == hd)))


for dp, dns, fns in os.walk(os.path.join(U, "1_PREREGISTRO")):
    for fn in fns:
        cp(os.path.relpath(os.path.join(dp, fn), U))
cp(r"2_OPTICO\run_optico.py")
for fn in os.listdir(os.path.join(U, r"2_OPTICO\consultas_mapa")):
    cp(os.path.join(r"2_OPTICO\consultas_mapa", fn))
cp(r"2_OPTICO\rodada1_20261012_1356\RESULTADO_OPTICO.json")
ok = all(c["confere"] for c in copias)
out = dict(n=len(copias), todas_conferem=ok, copias=copias)
with open(os.path.join(R2, "saidas", "A3_COPIA_INSUMOS.json"), "x", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("copias:", len(copias), "todas conferem:", ok)
