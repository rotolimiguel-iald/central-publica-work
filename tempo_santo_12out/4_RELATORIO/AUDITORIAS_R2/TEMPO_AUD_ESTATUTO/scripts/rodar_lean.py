"""Auditor de estatuto F1.TEMPO R2: compila no SANDBOX DO AUDITOR com o lean.exe copiado; LEAN_PATH so-leitura no
.lake do tgl_kernel do Nos (+ o sandbox, para importar a pedra compilada aqui). Saida -o so no sandbox.
Uso: python -I rodar_lean.py <fonte.lean> <saida.txt> <recibo.json> [<saida.olean>]"""
import datetime, hashlib, json, os, re, subprocess, sys, time
A = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12\TEMPO_AUD_ESTATUTO"
SANDBOX = os.path.join(A, "sandbox")
LEAN = os.path.join(SANDBOX, "toolchain", "leanprover--lean4---v4.31.0", "bin", "lean.exe")
NOS_LAKE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PKGS = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
LP = ";".join([SANDBOX, os.path.join(NOS_LAKE, "build", "lib", "lean")] +
              [os.path.join(NOS_LAKE, "packages", p, ".lake", "build", "lib", "lean") for p in PKGS])
TRIO = {"propext", "Classical.choice", "Quot.sound"}
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
src, saida, recibo = map(os.path.abspath, sys.argv[1:4])
olean = os.path.abspath(sys.argv[4]) if len(sys.argv) > 4 else None
for p in [src, saida, recibo] + ([olean] if olean else []):
    if not p.startswith(A): raise SystemExit("RECUSA: fora da pasta do auditor: " + p)
env = dict(os.environ); env["LEAN_PATH"] = LP; env.pop("LEAN_SYSROOT", None)
cmd = [LEAN, "--root=" + SANDBOX, src] + (["-o", olean] if olean else [])
t0 = time.time(); s0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
r = subprocess.run(cmd, capture_output=True, env=env, cwd=SANDBOX)
out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
open(saida, "wb").write(out)
txt = out.decode("utf-8", "replace"); lines = txt.splitlines(); recs = []; i = 0
while i < len(lines):
    m = re.search(r"^'(.+)' depends on axioms: \[(.*)", lines[i])
    if m:
        rest = m.group(2)
        while "]" not in rest and i + 1 < len(lines):
            i += 1; rest += " " + lines[i].strip()
        recs.append({"decl": m.group(1), "axioms": [a.strip() for a in rest.split("]", 1)[0].split(",") if a.strip()]})
    else:
        m2 = re.search(r"^'(.+)' does not depend on any axioms", lines[i])
        if m2: recs.append({"decl": m2.group(1), "axioms": []})
    i += 1
rec = dict(command=cmd, start_utc=s0, seconds=round(time.time() - t0, 2), exit_code=r.returncode,
           source=src, source_sha256=sha(src), output_sha256=hashlib.sha256(out).hexdigest(),
           n_axiom_lines=len(recs), fora_do_trio=[x for x in recs if not set(x["axioms"]) <= TRIO],
           n_sorryAx=txt.count("sorryAx"), n_warning=len(re.findall(r":\d+:\d+: warning", txt)),
           n_error=len(re.findall(r":\d+:\d+: error", txt)), axiom_records=recs)
if olean and r.returncode == 0 and os.path.exists(olean):
    rec["olean_sha256"] = sha(olean); rec["olean_bytes"] = os.path.getsize(olean)
json.dump(rec, open(recibo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rec.items() if k not in ("axiom_records", "command")}, ensure_ascii=False))
