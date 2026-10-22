# -*- coding: utf-8 -*-
# Copia (somente leitura na origem) o necessario do toolchain Lean v4.31.0 do elan para o sandbox do levantamento.
# bin/ inteiro (executaveis + DLLs) e lib/lean/{Init,Std,Lean,Lake} + arquivos de topo desses modulos (sem .a).
# Uso: sandbox_toolchain.py copiar | apagar
import os, sys, shutil, hashlib, json, time
ORIG = os.path.expanduser("~") + "\\.elan\\toolchains\\leanprover--lean4---v4.31.0"
AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = "\\\\?\\" + os.path.join(AQUI, "sandbox", "toolchain_v4.31.0")
MODS = ("Init", "Std", "Lean", "Lake")


def L(p):
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def copiar():
    t0 = time.time()
    os.makedirs(DEST, exist_ok=True)
    shutil.copytree(L(os.path.join(ORIG, "bin")), os.path.join(DEST, "bin"), dirs_exist_ok=True)
    lib_o = L(os.path.join(ORIG, "lib", "lean"))
    lib_d = os.path.join(DEST, "lib", "lean")
    os.makedirs(lib_d, exist_ok=True)
    n = 0
    for fn in os.listdir(lib_o):
        p = os.path.join(lib_o, fn)
        base = fn.split(".")[0]
        if base not in MODS:
            continue
        if os.path.isdir(p):
            shutil.copytree(p, os.path.join(lib_d, fn), dirs_exist_ok=True)
        else:
            shutil.copy2(p, os.path.join(lib_d, fn))
        n += 1
    tot = 0
    for dp, dns, fns in os.walk(DEST):
        for f in fns:
            tot += os.path.getsize(os.path.join(dp, f))
    print(json.dumps({"copiado_para": DEST, "entradas_lib": n, "bytes": tot, "segundos": round(time.time() - t0, 1)}))


def apagar():
    raiz = "\\\\?\\" + os.path.join(AQUI, "sandbox")
    if os.path.exists(raiz):
        shutil.rmtree(raiz)
    print(json.dumps({"apagado": raiz, "existe_depois": os.path.exists(raiz)}))


if __name__ == "__main__":
    {"copiar": copiar, "apagar": apagar}[sys.argv[1]]()
