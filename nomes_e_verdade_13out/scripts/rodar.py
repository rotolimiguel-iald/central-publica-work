# -*- coding: utf-8 -*-
"""Nomes e Verdade (13/10): compila UM .lean do sandbox C:/t/nm1 com o lean v4.31.0 COPIADO (sem lake).
LEAN_PATH = [as pastas de saida indicadas, dentro do sandbox] + pacotes do .lake do Nos (mathlib etc.) +
.lake/build/lib/lean do Nos, tudo SO LEITURA. -o so dentro do sandbox. Logs em ../logs.
Uso: rodar.py --src <src_old|src_new|src_base|meta> --alvo <TGLExt/X.lean | meta/Y.lean> --lp <out_a,out_b,...>
             --tag <tag> [--olean <pasta out>]
 --lp lista, em ordem, as pastas do sandbox (ex.: out_old,out_base) que precedem o kernel do Nos no LEAN_PATH.
 --olean grava <pasta out>/TGLExt/<Modulo>.olean (recusa sobrescrever).
Contagem de sorry: o formato REAL (crase) 'declaration uses `sorry`' e tambem o aspas simples e 'sorryAx'."""
import os, sys, subprocess, hashlib, json, time, datetime, re, argparse

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = "C:/t/nm1"
LOGS = os.path.join(AQUI, "logs")
LEAN = SB + "/toolchain/bin/lean.exe"
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--alvo", required=True)
    ap.add_argument("--lp", default="")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--olean", default=None)
    a = ap.parse_args()
    SRC = SB + "/" + a.src
    pastas = [SB + "/" + p for p in a.lp.split(",") if p]
    paths = pastas + [K + "/build/lib/lean"] + [K + "/packages/" + p + "/.lake/build/lib/lean" for p in PK]
    paths = [p for p in paths if os.path.isdir(p)]
    if not os.path.isfile(LEAN):
        print("FALHA VISIVEL: sandbox incompleto")
        sys.exit(2)
    src = SRC + "/" + a.alvo
    sb = open(src, "rb").read()
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(p.replace("/", chr(92)) for p in paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    out_olean = None
    if a.olean:
        assert a.alvo.startswith("TGLExt/") and a.alvo.endswith(".lean")
        out_olean = SB + "/" + a.olean + "/TGLExt/" + os.path.basename(a.alvo)[:-5] + ".olean"
        os.makedirs(os.path.dirname(out_olean), exist_ok=True)
        if os.path.exists(out_olean):
            print("FALHA VISIVEL: .olean ja existe: " + out_olean)
            sys.exit(2)
        cmd += ["--root=" + SRC, "-o", out_olean]
    cmd.append(a.alvo)
    t0 = time.time()
    st = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SRC)
    dt = time.time() - t0
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    os.makedirs(LOGS, exist_ok=True)
    open(os.path.join(LOGS, a.tag + "_SAIDA.txt"), "wb").write(saida)
    txt = saida.decode("utf-8", errors="replace")
    axs = {}
    for decl, vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt, re.S):
        axs[decl] = [v.strip() for v in vals.replace("\n", " ").split(",") if v.strip()]
    for decl in re.findall(r"'([^']+)' does not depend on any axioms", txt):
        axs[decl] = []
    fora = {k: v for k, v in axs.items() if not set(v) <= TRIO}
    sorry_n = txt.count("declaration uses `sorry`") + txt.count("declaration uses 'sorry'") + txt.count("sorryAx")
    rec = {"src": SRC, "alvo": a.alvo, "tag": a.tag, "source_sha256": hashlib.sha256(sb).hexdigest(), "source_bytes": len(sb),
           "inicio_utc": st, "segundos": round(dt, 2), "exit_code": r.returncode,
           "saida_sha256": hashlib.sha256(saida).hexdigest(), "n_erros": len(re.findall(r":\d+:\d+: error", txt)),
           "n_avisos": len(re.findall(r":\d+:\d+: warning", txt)),
           "declaration_uses_sorry_ou_sorryAx": sorry_n,
           "n_print_axioms": len(axs), "fora_do_trio": fora, "axiomas": axs,
           "lean": LEAN, "lean_sha256": sha(LEAN), "LEAN_PATH": paths, "comando": cmd}
    if out_olean and os.path.exists(out_olean):
        rec["olean"] = out_olean
        rec["olean_sha256"] = sha(out_olean)
        rec["olean_bytes"] = os.path.getsize(out_olean)
    elif out_olean:
        rec["olean"] = None
    json.dump(rec, open(os.path.join(LOGS, a.tag + "_RECIBO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos",
                                              "declaration_uses_sorry_ou_sorryAx", "n_print_axioms", "olean_sha256")}))
    print(txt[:6000])
    sys.exit(0 if r.returncode == 0 else 1)


if __name__ == "__main__":
    main()
