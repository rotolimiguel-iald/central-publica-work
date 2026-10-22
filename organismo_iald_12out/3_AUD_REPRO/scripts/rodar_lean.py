# -*- coding: utf-8 -*-
"""Compila UM .lean do sandbox de 2_CONSTRUCAO com o binario lean v4.31.0 do elan (chamado DIRETAMENTE, sem lake,
sem copiar toolchain). LEAN_PATH: PRIMEIRO a sobreposicao sandbox/ov (copia verificada dos .olean do kernel do Nos
+ as candidatas compiladas aqui), depois os pacotes do .lake do Nos, SO LEITURA. Nada e escrito fora de 2_CONSTRUCAO.
Com --olean, grava sandbox/ov/TGLExt/<Modulo>.olean (o modulo e TGLExt.<Modulo>, fonte em sandbox/TGLExt/<Modulo>.lean).
Grava logs/<tag>_SAIDA.txt e logs/<tag>_RECIBO.json.
Uso: rodar_lean.py <fonte relativa a sandbox> <tag> [--olean]"""
import os, sys, subprocess, hashlib, json, time, datetime, re
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(AQUI, "sandbox")
OV = os.path.join(SB, "ov")
LOGS = os.path.join(AQUI, "logs")
LEAN = os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe")
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def main():
    alvo, tag = sys.argv[1], sys.argv[2]
    olean = "--olean" in sys.argv[3:]
    paths = [OV] + [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
    paths = [p.replace("/", "\\") for p in paths if os.path.isdir(p)]
    if not os.path.isdir(OV):
        print("FALHA VISIVEL: sobreposicao ov ausente"); sys.exit(2)
    src = os.path.join(SB, alvo)
    sb = open(src, "rb").read()
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    out_olean = None
    if olean:
        rel = alvo.replace("\\", "/")
        assert rel.startswith("TGLExt/") and rel.endswith(".lean"), "so modulos TGLExt/<Nome>.lean recebem .olean"
        out_olean = os.path.join(OV, "TGLExt", os.path.basename(rel)[:-5] + ".olean")
        if os.path.exists(out_olean):
            print("FALHA VISIVEL: .olean ja existe na sobreposicao: " + out_olean); sys.exit(2)
        cmd += ["--root=" + SB, "-o", out_olean]
    cmd.append(alvo)
    t0 = time.time()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    os.makedirs(LOGS, exist_ok=True)
    open(os.path.join(LOGS, tag + "_SAIDA.txt"), "wb").write(saida)
    txt = saida.decode("utf-8", errors="replace")
    axs = {}
    for decl, vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt, re.S):
        axs[decl] = [v.strip() for v in vals.replace("\n", " ").split(",") if v.strip()]
    for decl in re.findall(r"'([^']+)' does not depend on any axioms", txt):
        axs[decl] = []
    fora = {k: v for k, v in axs.items() if not set(v) <= TRIO}
    rec = {"alvo": alvo, "tag": tag, "source_sha256": hashlib.sha256(sb).hexdigest(), "source_bytes": len(sb),
           "inicio_utc": st, "segundos": round(dt, 2), "exit_code": r.returncode,
           "saida_sha256": hashlib.sha256(saida).hexdigest(), "n_erros": len(re.findall(r":\d+:\d+: error", txt)),
           "n_avisos": len(re.findall(r":\d+:\d+: warning", txt)),
           "declaration_uses_sorry": txt.count("declaration uses 'sorry'") + txt.count("sorryAx"),
           "n_print_axioms": len(axs), "fora_do_trio": fora,
           "lean": LEAN, "LEAN_PATH_n": len(paths), "LEAN_PATH_0": paths[0], "comando": cmd}
    if out_olean and os.path.exists(out_olean):
        rec["olean"] = out_olean
        rec["olean_sha256"] = sha(out_olean)
        rec["olean_bytes"] = os.path.getsize(out_olean)
    elif out_olean:
        rec["olean"] = None
    json.dump(rec, open(os.path.join(LOGS, tag + "_RECIBO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos",
                                              "declaration_uses_sorry", "n_print_axioms", "olean_sha256")}))
    print(txt[:14000])


if __name__ == "__main__":
    main()
