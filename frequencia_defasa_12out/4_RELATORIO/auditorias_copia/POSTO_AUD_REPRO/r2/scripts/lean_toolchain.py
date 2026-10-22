# -*- coding: utf-8 -*-
"""Toolchain Lean v4.31.0 COPIADO para o sandbox do auditor (origem so-leitura: ~/.elan).
Uso: lean_toolchain.py copiar | apagar.  'apagar' remove o toolchain copiado, o build do sandbox e qualquer .lake
que tenha aparecido em <r2>/lean (prefixo \\\\?\\ para caminhos longos)."""
import json, os, shutil, sys, time

ORIG = os.path.join(os.path.expanduser("~"), ".elan", "toolchains", "leanprover--lean4---v4.31.0")
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEANDIR = os.path.join(R2, "lean")
DEST = os.path.join(R2, "T")
MODS = ("Init", "Std", "Lean", "Lake")


def L(p):
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def copiar():
    t0 = time.time()
    if os.path.exists(L(DEST)):
        raise SystemExit("FALHA VISIVEL: toolchain ja existe em " + DEST)
    shutil.copytree(L(os.path.join(ORIG, "bin")), L(os.path.join(DEST, "bin")))
    os.makedirs(L(os.path.join(DEST, "lib", "lean")))
    n = 0
    for fn in os.listdir(L(os.path.join(ORIG, "lib", "lean"))):
        if fn.split(".")[0] not in MODS:
            continue
        s = L(os.path.join(ORIG, "lib", "lean", fn))
        d = L(os.path.join(DEST, "lib", "lean", fn))
        (shutil.copytree if os.path.isdir(s) else shutil.copy2)(s, d)
        n += 1
    nf = tot = 0
    for dp, dns, fns in os.walk(L(DEST)):
        for f in fns:
            nf += 1
            tot += os.path.getsize(os.path.join(dp, f))
    print(json.dumps(dict(de=ORIG, para=DEST, entradas_lib=n, arquivos=nf, bytes=tot, s=round(time.time() - t0, 1))))


def apagar():
    out = {}
    for a in (DEST, os.path.join(LEANDIR, "sb", "build")):
        if os.path.exists(L(a)):
            shutil.rmtree(L(a))
        out[a] = dict(existe_depois=os.path.exists(L(a)))
    lakes = []
    for dp, dns, fns in os.walk(L(R2)):
        for d in list(dns):
            if d == ".lake":
                shutil.rmtree(os.path.join(dp, d))
                lakes.append(os.path.join(dp, d))
    out["lake_apagados"] = lakes
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"copiar": copiar, "apagar": apagar}[sys.argv[1]]()
