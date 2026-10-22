"""A5 — compilador do AUDITOR (escrito aqui, nao copiado do construtor).
Compila um .lean do sandbox do auditor com o lean.exe COPIADO do elan para o sandbox; LEAN_PATH = so os
diretorios de build do .lake do tgl_kernel do Nos (leitura). O -o (.olean) fica SO no sandbox do auditor.
Grava saida e recibo: EXIT, sha256 da fonte e do .olean, linhas de #print axioms (com quebra de linha),
fora do trio, contagens de error/warning/sorry.
Uso: python a5_lean.py <fonte.lean> <saida.txt> <recibo.json> [<saida.olean>]"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(AUD, "lean_sandbox")
LEAN = os.path.join(AUD, "t", "l", "bin", "lean.exe")
LAKE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PK = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
LP = [os.path.join(LAKE, "build", "lib", "lean")] + [os.path.join(LAKE, "packages", p, ".lake", "build", "lib", "lean") for p in PK]
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def h(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main(src, saida, recibo, olean=None):
    src = os.path.abspath(src)
    assert os.path.commonpath([src, SB]) == SB, "fonte fora do sandbox do auditor"
    if olean:
        olean = os.path.abspath(olean)
        assert os.path.commonpath([olean, SB]) == SB, "olean fora do sandbox do auditor"
    lp = [p for p in LP if os.path.isdir(p)]
    faltam = [p for p in LP if not os.path.isdir(p)]
    assert os.path.isdir(LP[0]) and any("mathlib" in p for p in lp), "LEAN_PATH essencial inexistente"
    if os.environ.get("AUD_IMPORTA_SANDBOX") == "1":
        lp = [SB] + lp
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(lp)
    env.pop("LEAN_SYSROOT", None)
    cmd = [LEAN, "--root=" + SB, src] + (["-o", olean] if olean else [])
    t0 = time.time()
    ini = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SB)
    dur = time.time() - t0
    out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
    with open(saida, "wb") as fo:
        fo.write(out)
    txt = out.decode("utf-8", "replace")
    recs = []
    L = txt.splitlines()
    i = 0
    while i < len(L):
        m = re.match(r"^'(.+?)' depends on axioms: \[(.*)$", L[i])
        if m:
            rest = m.group(2)
            while "]" not in rest and i + 1 < len(L):
                i += 1
                rest += " " + L[i].strip()
            recs.append({"decl": m.group(1), "axioms": [a.strip() for a in rest.split("]")[0].split(",") if a.strip()]})
        else:
            m2 = re.match(r"^'(.+?)' does not depend on any axioms", L[i])
            if m2:
                recs.append({"decl": m2.group(1), "axioms": []})
        i += 1
    rec = {"cmd": cmd, "LEAN_PATH": env["LEAN_PATH"], "LEAN_PATH_omitidos_inexistentes": faltam, "inicio_utc": ini, "segundos": round(dur, 1),
           "exit": r.returncode, "fonte": src, "fonte_sha256": h(src), "fonte_bytes": os.path.getsize(src),
           "saida": saida, "saida_sha256": hashlib.sha256(out).hexdigest(),
           "n_axiom": len(recs), "fora_do_trio": [x for x in recs if not set(x["axioms"]) <= TRIO],
           "sem_axioma": [x["decl"] for x in recs if not x["axioms"]],
           "n_error": len(re.findall(r":\d+:\d+: error", txt)), "n_warning": len(re.findall(r":\d+:\d+: warning", txt)),
           "sorryAx_na_saida": txt.count("sorryAx"), "declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
           "versao": subprocess.run([LEAN, "--version"], capture_output=True).stdout.decode().strip(),
           "axiom_records": recs}
    if olean and os.path.exists(olean):
        rec["olean_sha256"] = h(olean)
        rec["olean_bytes"] = os.path.getsize(olean)
    with open(recibo, "w", encoding="utf-8") as fo:
        json.dump(rec, fo, indent=1, ensure_ascii=False)
    show = {k: v for k, v in rec.items() if k not in ("LEAN_PATH", "axiom_records", "cmd")}
    print(json.dumps(show, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2], a[3] if len(a) > 3 else None)
