# -*- coding: utf-8 -*-
# Auditor REPRO: copia (so leitura na origem) o toolchain Lean v4.31.0 do elan para o sandbox do auditor, ou apaga
# o que foi copiado (toolchain, build, .lake e caches). Uso: lean_toolchain.py copiar | apagar
import os, sys, shutil, json, time
ORIG = os.path.expanduser("~") + "\\.elan\\toolchains\\leanprover--lean4---v4.31.0"
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(AUD, "L")
DEST = "\\\\?\\" + os.path.join(SB, "tc")
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
    for fn in sorted(os.listdir(lib_o)):
        p = os.path.join(lib_o, fn)
        if fn.split(".")[0] not in MODS:
            continue
        if os.path.isdir(p):
            shutil.copytree(p, os.path.join(lib_d, fn), dirs_exist_ok=True)
        else:
            shutil.copy2(p, os.path.join(lib_d, fn))
        n += 1
    tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, dns, fns in os.walk(DEST) for f in fns)
    print(json.dumps({"copiado_para": DEST, "entradas_lib": n, "bytes": tot, "segundos": round(time.time() - t0, 1)}))


def apagar():
    out = {}
    for sub in ("tc", "build"):
        raiz = L(os.path.join(SB, sub))
        if os.path.exists(raiz):
            shutil.rmtree(raiz)
        out[sub] = {"existe_depois": os.path.exists(raiz)}
    for dp, dns, fns in os.walk(L(SB)):
        for d in list(dns):
            if d in (".lake", "__pycache__", ".cache"):
                shutil.rmtree(os.path.join(dp, d))
                out.setdefault("caches_apagados", []).append(os.path.join(dp, d))
    restos = [os.path.join(dp, f) for dp, dns, fns in os.walk(L(SB)) for f in fns if f.endswith((".olean", ".ilean", ".olean.private", ".olean.server", ".ir", ".c"))]
    out["oleans_restantes_no_sandbox"] = restos
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    {"copiar": copiar, "apagar": apagar}[sys.argv[1]]()
