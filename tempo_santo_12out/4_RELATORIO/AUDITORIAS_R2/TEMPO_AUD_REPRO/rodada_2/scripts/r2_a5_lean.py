"""Auditor de reproducao F1.TEMPO, rodada 2 -- item (4)/(6): compila um .lean no sandbox DO AUDITOR com o lean.exe copiado
para o sandbox (t\\l), LEAN_PATH so-leitura no .lake do tgl_kernel do Nos (+ opcionalmente o proprio sandbox, para sondas que
importam a pedra recompilada). A saida -o fica SO no sandbox do auditor.
Uso: python r2_a5_lean.py <arquivo.lean (no sandbox)> <rotulo> [--olean] [--importa-sandbox]
Grava saidas/lean/<rotulo>_saida.txt e <rotulo>_recibo.json.
"""
import datetime, hashlib, json, os, re, subprocess, sys, time

AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANDBOX = os.path.join(AUD, "lean")
LEAN = os.path.join(AUD, "t", "l", "bin", "lean.exe")
NOS_LAKE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PKGS = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
LP = [os.path.join(NOS_LAKE, "build", "lib", "lean")] + [os.path.join(NOS_LAKE, "packages", p, ".lake", "build", "lib", "lean") for p in PKGS]
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    src = os.path.abspath(sys.argv[1])
    rot = sys.argv[2]
    want_olean = "--olean" in sys.argv
    imp_sb = "--importa-sandbox" in sys.argv
    assert src.startswith(SANDBOX + os.sep), "a fonte tem de estar no sandbox do auditor"
    lp_existe = {p: os.path.isdir(p) for p in LP}  # o construtor passou as 9 entradas; a do Cli nao existe e o Lean a ignora
    env = dict(os.environ)
    env["LEAN_PATH"] = ";".join(([SANDBOX] if imp_sb else []) + LP)
    env.pop("LEAN_SYSROOT", None)
    cmd = [LEAN, "--root=" + SANDBOX, src]
    olean = None
    if want_olean:
        olean = os.path.splitext(src)[0] + ".olean"
        assert olean.startswith(SANDBOX + os.sep)
        cmd += ["-o", olean]
    outdir = os.path.join(AUD, "saidas", "lean")
    os.makedirs(outdir, exist_ok=True)
    s0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SANDBOX)
    dt = time.time() - t0
    out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
    with open(os.path.join(outdir, rot + "_saida.txt"), "wb") as f:
        f.write(out)
    txt = out.decode("utf-8", "replace")
    recs, lines, i = [], txt.splitlines(), 0
    while i < len(lines):
        m = re.search(r"^'(.+)' depends on axioms: \[(.*)", lines[i])
        if m:
            rest = m.group(2)
            while "]" not in rest and i + 1 < len(lines):
                i += 1
                rest += " " + lines[i].strip()
            recs.append({"decl": m.group(1), "axioms": [a.strip() for a in rest.split("]", 1)[0].split(",") if a.strip()]})
        else:
            m2 = re.search(r"^'(.+)' does not depend on any axioms", lines[i])
            if m2:
                recs.append({"decl": m2.group(1), "axioms": []})
        i += 1
    rec = {"rotulo": rot, "command": cmd, "LEAN_PATH": env["LEAN_PATH"], "cwd": SANDBOX, "LEAN_PATH_existe": lp_existe, "inicio_utc": s0, "segundos": round(dt, 1),
           "exit_code": r.returncode, "fonte": src, "fonte_sha256": sha(src), "fonte_bytes": os.path.getsize(src),
           "saida_sha256": hashlib.sha256(out).hexdigest(), "n_print_axioms": len(recs),
           "fora_do_trio": [a for a in recs if not set(a["axioms"]) <= TRIO],
           "uniao_dos_axiomas": sorted(set(x for a in recs for x in a["axioms"])),
           "n_sorryAx_na_saida": txt.count("sorryAx"), "n_declaration_uses_sorry": txt.count("declaration uses 'sorry'"),
           "n_error": len(re.findall(r":\d+:\d+: error", txt)), "n_warning": len(re.findall(r":\d+:\d+: warning", txt)),
           "erros": re.findall(r"[^\n]*:\d+:\d+: error[^\n]*", txt)[:40],
           "avisos": re.findall(r"[^\n]*:\d+:\d+: warning[^\n]*", txt)[:80],
           "lean_version": subprocess.run([LEAN, "--version"], capture_output=True).stdout.decode().strip(),
           "axiom_records": recs}
    if olean and os.path.exists(olean):
        rec["olean"] = olean
        rec["olean_sha256"] = sha(olean)
        rec["olean_bytes"] = os.path.getsize(olean)
    with open(os.path.join(outdir, rot + "_recibo.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rec.items() if k not in ("LEAN_PATH", "axiom_records", "avisos", "command")}, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
