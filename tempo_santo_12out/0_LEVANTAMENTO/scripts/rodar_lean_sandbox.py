"""Roda (no sandbox) o lean.exe COPIADO para o sandbox sobre um arquivo de conferencia, com LEAN_PATH so-leitura no .lake
do Nos. Nao passa -o (nao grava .olean). Grava saida e recibo no sandbox. Uso: python -I rodar_lean_sandbox.py <arquivo.lean> <saida.txt> <recibo.json>"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

SANDBOX = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\0_LEVANTAMENTO\sandbox"
LEAN = os.path.join(SANDBOX, "toolchain", "leanprover--lean4---v4.31.0", "bin", "lean.exe")
K = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PKGS = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq"]
LEAN_PATH = ";".join([os.path.join(K, "build", "lib", "lean")] +
                     [os.path.join(K, "packages", p, ".lake", "build", "lib", "lean") for p in PKGS])


def main(src, saida, recibo):
    env = dict(os.environ)
    env["LEAN_PATH"] = LEAN_PATH
    env.pop("LEAN_SYSROOT", None)
    t0 = time.time()
    s0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run([LEAN, src], capture_output=True, env=env, cwd=SANDBOX)
    t1 = time.time()
    out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
    with open(saida, "wb") as fo:
        fo.write(out)
    txt = r.stdout.decode("utf-8", "replace")
    axiom_lines = [l for l in txt.splitlines() if "depends on axioms" in l or "does not depend on any axioms" in l]
    trio = {"propext", "Classical.choice", "Quot.sound"}
    fora_do_trio = []
    for l in axiom_lines:
        if "depends on axioms" in l:
            inside = l.split("[", 1)[1].rsplit("]", 1)[0]
            axs = {a.strip() for a in inside.split(",") if a.strip()}
            if not axs <= trio:
                fora_do_trio.append(l)
    rec = dict(command=[LEAN, src], LEAN_PATH=LEAN_PATH, cwd=SANDBOX, start_utc=s0,
               end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), seconds=round(t1 - t0, 3),
               exit_code=r.returncode, source_sha256=hashlib.sha256(open(src, "rb").read()).hexdigest(),
               output_sha256=hashlib.sha256(out).hexdigest(), n_axiom_lines=len(axiom_lines),
               n_sorryAx=txt.count("sorryAx"), n_error=txt.count("error"), fora_do_trio=fora_do_trio,
               lean_version=subprocess.run([LEAN, "--version"], capture_output=True).stdout.decode().strip())
    with open(recibo, "w", encoding="utf-8") as fo:
        json.dump(rec, fo, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("LEAN_PATH",)}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
