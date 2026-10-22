# -*- coding: utf-8 -*-
"""Compila UM .lean do sandbox do auditor (<r2>/lean/sb) com o toolchain COPIADO e LEAN_PATH = <sb>/build (escrita)
+ .lake do tgl_kernel do Nos (SO LEITURA: o lean so le .olean dali).
Uso: lean_rodar.py <arquivo relativo a sb> <tag> [--olean <nome em sb/build>] [--root <dir>]
Grava <r2>/saidas/lean_logs/<tag>_SAIDA.txt e _RECIBO.json (nunca sobrescreve)."""
import datetime, hashlib, json, os, subprocess, sys, time

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(R2, "lean", "sb")
BUILD = os.path.join(SB, "build")
LEAN = os.path.join(R2, "T", "bin", "lean.exe")
LOGS = os.path.join(R2, "saidas", "lean_logs")
K = os.path.join(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um", "N\u00f3s", "tgl_kernel", ".lake")
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    alvo, tag = sys.argv[1], sys.argv[2]
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    rec_p = os.path.join(LOGS, tag + "_RECIBO.json")
    if os.path.exists(rec_p):
        raise SystemExit("FALHA VISIVEL: recibo ja existe " + rec_p)
    paths = [BUILD, os.path.join(K, "build", "lib", "lean")] + \
            [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
    paths = [p for p in paths if os.path.isdir(p)]
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(paths)
    for k in ("LEAN_SYSROOT", "ELAN_TOOLCHAIN", "LEAN_SRC_PATH"):
        env.pop(k, None)
    cmd = [LEAN]
    if "--root" in sys.argv:
        cmd.append("--root=" + sys.argv[sys.argv.index("--root") + 1])
    olean = None
    if "--olean" in sys.argv:
        olean = os.path.join(BUILD, sys.argv[sys.argv.index("--olean") + 1])
        cmd += ["-o", olean]
    cmd.append(alvo)
    src = open(os.path.join(SB, alvo), "rb").read()
    t0 = time.time()
    ini = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    saida = (r.stdout or b"") + b"\n--- STDERR ---\n" + (r.stderr or b"")
    open(os.path.join(LOGS, tag + "_SAIDA.txt"), "xb").write(saida)
    txt = saida.decode("utf-8", errors="replace")
    rec = dict(alvo=alvo, tag=tag, source_bytes=len(src), source_sha256=sha(src), inicio_utc=ini,
               segundos=round(time.time() - t0, 2), exit_code=r.returncode, n_erros=txt.count(": error"),
               n_avisos=txt.count(": warning"), sorryAx=txt.count("sorryAx"),
               declaration_uses_sorry=txt.count("declaration uses 'sorry'"), comando=cmd, cwd=SB,
               LEAN_PATH=env["LEAN_PATH"], saida_sha256=sha(saida))
    if olean and os.path.exists(olean):
        ob = open(olean, "rb").read()
        rec.update(olean=olean, olean_bytes=len(ob), olean_sha256=sha(ob))
    json.dump(rec, open(rec_p, "x", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rec.get(k) for k in ("alvo", "exit_code", "segundos", "n_erros", "n_avisos", "sorryAx",
                                              "olean_sha256")}, ensure_ascii=False))
    print(txt[:30000])


if __name__ == "__main__":
    main()
