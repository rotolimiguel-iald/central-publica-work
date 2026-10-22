# -*- coding: utf-8 -*-
# Rodada 3 (5_R3) — copia (somente leitura na origem) o necessario do toolchain Lean v4.31.0 do elan para
# 3_KERNEL\rodada2\toolchain_v4.31.0. Mesmo metodo da rodada 1 (3_KERNEL\sandbox_toolchain.py): bin/ inteiro e
# lib/lean/{Init,Std,Lean,Lake} (+ arquivos de topo desses modulos). Uso: sandbox_toolchain.py copiar | apagar
# apagar remove SO o toolchain copiado, as pastas de build dos dois sandboxes da rodada 3 e qualquer .lake que tenha
# aparecido dentro da rodada 2 (os .olean gerados ficam registrados por sha256 e copiados para rodada2\olean antes).
import os, sys, shutil, json, time
ORIG = os.path.expanduser("~") + "\\.elan\\toolchains\\leanprover--lean4---v4.31.0"
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = "\\\\?\\" + os.path.join(R2, "toolchain_v4.31.0")
MODS = ("Init", "Std", "Lean", "Lake")


def L(p):
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def copiar():
    t0 = time.time()
    if os.path.exists(DEST):
        print(json.dumps({"ja_existe": DEST}))
        return
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
    nf = 0
    for dp, dns, fns in os.walk(DEST):
        for f in fns:
            tot += os.path.getsize(os.path.join(dp, f))
            nf += 1
    print(json.dumps({"copiado_de": ORIG, "copiado_para": DEST, "entradas_lib": n, "arquivos": nf, "bytes": tot,
                      "segundos": round(time.time() - t0, 1)}, ensure_ascii=False))


def apagar():
    out = {}
    alvos = [os.path.join(R2, "toolchain_v4.31.0"), os.path.join(R2, "sandbox", "build"),
             os.path.join(R2, "sandbox_r2", "build")]
    for a in alvos:
        raiz = L(a)
        if os.path.exists(raiz):
            shutil.rmtree(raiz)
        out[a] = {"existe_depois": os.path.exists(raiz)}
    for dp, dns, fns in os.walk(L(R2)):
        for d in list(dns):
            if d == ".lake":
                p = os.path.join(dp, d)
                shutil.rmtree(p)
                out.setdefault("lake_apagados", []).append(p)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"copiar": copiar, "apagar": apagar}[sys.argv[1]]()
