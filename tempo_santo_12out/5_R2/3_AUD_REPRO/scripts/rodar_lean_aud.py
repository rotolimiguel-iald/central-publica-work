# -*- coding: utf-8 -*-
"""Compilador de sandbox do auditor de REPRODUCAO (R2, F1.TEMPO). lean.exe COPIADO para o sandbox (toolchain v4.31.0 do
elan); LEAN_PATH SO-LEITURA no .lake do tgl_kernel do Nos; -o SO para o sandbox. Opcoes:
  AUD_IMPORTA_SANDBOX=1       -> o proprio sandbox entra no LEAN_PATH (importar o .olean da pedra R2 compilado aqui)
  AUD_LEAN_PATH_EXTRA=<dir>   -> diretorio extra SO-LEITURA (o .olean da pedra R1 em 3_KERNEL/sandbox)
Recibo JSON: sha256 da fonte, da saida e do .olean; exit; avisos/erros; #print axioms (fora do trio); sorryAx.
Uso: python -I -X utf8 rodar_lean_aud.py <arquivo.lean> <saida.txt> <recibo.json> [<saida.olean>]"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

A = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\3_AUD_REPRO"
SANDBOX = os.path.join(A, "sandbox")
LEAN = os.path.join(SANDBOX, "toolchain", "leanprover--lean4---v4.31.0", "bin", "lean.exe")
NOS_LAKE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PKGS = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
LEAN_PATH = ";".join([os.path.join(NOS_LAKE, "build", "lib", "lean")] +
                     [os.path.join(NOS_LAKE, "packages", p, ".lake", "build", "lib", "lean") for p in PKGS])
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha_file(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(src, saida, recibo, olean=None):
    src = os.path.abspath(src)
    if not src.startswith(SANDBOX):
        raise SystemExit("RECUSA: a fonte tem de estar no sandbox do auditor")
    if olean is not None:
        olean = os.path.abspath(olean)
        if not olean.startswith(SANDBOX):
            raise SystemExit("RECUSA: o .olean tem de ficar no sandbox do auditor")
    env = dict(os.environ)
    partes = []
    if os.environ.get("AUD_IMPORTA_SANDBOX") == "1":
        partes.append(SANDBOX)
    extra = os.environ.get("AUD_LEAN_PATH_EXTRA")
    if extra:
        partes.append(extra)
    env["LEAN_PATH"] = ";".join(partes + [LEAN_PATH])
    env.pop("LEAN_SYSROOT", None)
    cmd = [LEAN, "--root=" + SANDBOX, src]
    if olean is not None:
        cmd += ["-o", olean]
    t0 = time.time()
    s0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SANDBOX)
    t1 = time.time()
    out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
    with open(saida, "wb") as fo:
        fo.write(out)
    txt = out.decode("utf-8", "replace")
    axiom_records = []
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.search(r"^'(.+)' depends on axioms: \[(.*)", ln)
        if m:
            name, rest = m.group(1), m.group(2)
            while "]" not in rest and i + 1 < len(lines):
                i += 1
                rest += " " + lines[i].strip()
            axs = [a.strip() for a in rest.split("]", 1)[0].split(",") if a.strip()]
            axiom_records.append({"decl": name, "axioms": axs})
        else:
            m2 = re.search(r"^'(.+)' does not depend on any axioms", ln)
            if m2:
                axiom_records.append({"decl": m2.group(1), "axioms": []})
        i += 1
    fora = [a for a in axiom_records if not set(a["axioms"]) <= TRIO]
    rec = dict(command=cmd, LEAN_PATH=env["LEAN_PATH"], cwd=SANDBOX, start_utc=s0,
               end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), seconds=round(t1 - t0, 3),
               exit_code=r.returncode, source=src, source_sha256=sha_file(src), source_bytes=os.path.getsize(src),
               output=saida, output_sha256=hashlib.sha256(out).hexdigest(), n_axiom_lines=len(axiom_records),
               axiom_records=axiom_records, fora_do_trio=fora, sem_axioma_algum=[a["decl"] for a in axiom_records if not a["axioms"]],
               n_sorryAx_na_saida=txt.count("sorryAx"),
               n_warning=len(re.findall(r":\d+:\d+: warning", txt)), n_error=len(re.findall(r":\d+:\d+: error", txt)),
               lean_version=subprocess.run([LEAN, "--version"], capture_output=True).stdout.decode().strip())
    if olean is not None and os.path.exists(olean) and r.returncode == 0:
        rec["olean"] = olean
        rec["olean_sha256"] = sha_file(olean)
        rec["olean_bytes"] = os.path.getsize(olean)
    with open(recibo, "w", encoding="utf-8") as fo:
        json.dump(rec, fo, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("LEAN_PATH", "axiom_records")}, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2], a[3] if len(a) > 3 else None)
