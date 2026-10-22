"""Auditor (lente ESTATUTO E REGRA) da F1.TEMPO: compila um .lean com o lean.exe COPIADO para o sandbox desta
auditoria, LEAN_PATH so-leitura no .lake do tgl_kernel do Nos. A saida -o (.olean) vai SO para o sandbox desta
auditoria, nunca para o Nos. Grava a saida (stdout+stderr) e um recibo JSON com sha256 da fonte, da saida e do
.olean, codigo de saida, avisos/erros, linhas de #print axioms e o que estiver fora do trio.
Uso: python -I rodar_lean_aud.py <arquivo.lean> <saida.txt> <recibo.json> [<saida.olean>] [--importa-sandbox]"""
import datetime, hashlib, json, os, re, subprocess, sys, time

AUD = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12\TEMPO_AUD_ESTATUTO"
SANDBOX = os.path.join(AUD, "sandbox")
LEAN = os.path.join(SANDBOX, "tc", "bin", "lean.exe")  # toolchain v4.31.0 copiado do elan para sandbox	c (caminho curto: < 260)
NOS_LAKE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake"
PKGS = ["aesop", "batteries", "importGraph", "LeanSearchClient", "mathlib", "plausible", "proofwidgets", "Qq", "Cli"]
LEAN_PATH = ";".join([os.path.join(NOS_LAKE, "build", "lib", "lean")] +
                     [os.path.join(NOS_LAKE, "packages", p, ".lake", "build", "lib", "lean") for p in PKGS])
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha_file(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    importa = "--importa-sandbox" in sys.argv
    src, saida, recibo = (os.path.abspath(a) for a in args[:3])
    olean = os.path.abspath(args[3]) if len(args) > 3 else None
    for p in [src, saida, recibo] + ([olean] if olean else []):
        if not p.startswith(AUD):
            raise SystemExit("RECUSA: tudo tem de ficar no sandbox da auditoria: " + p)
    env = dict(os.environ)
    env["LEAN_PATH"] = (SANDBOX + ";" + LEAN_PATH) if importa else LEAN_PATH
    env.pop("LEAN_SYSROOT", None)
    cmd = [LEAN, "--root=" + SANDBOX, src] + (["-o", olean] if olean else [])
    t0 = time.time(); s0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, env=env, cwd=SANDBOX)
    t1 = time.time()
    out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
    with open(saida, "wb") as fo:
        fo.write(out)
    txt = out.decode("utf-8", "replace")
    recs, lines, i = [], txt.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        m = re.search(r"^'(.+)' depends on axioms: \[(.*)", ln)
        if m:
            rest = m.group(2)
            while "]" not in rest and i + 1 < len(lines):
                i += 1; rest += " " + lines[i].strip()
            recs.append({"decl": m.group(1), "axioms": [a.strip() for a in rest.split("]", 1)[0].split(",") if a.strip()]})
        else:
            m2 = re.search(r"^'(.+)' does not depend on any axioms", ln)
            if m2:
                recs.append({"decl": m2.group(1), "axioms": []})
        i += 1
    fora = [a for a in recs if not set(a["axioms"]) <= TRIO]
    rec = dict(command=cmd, LEAN_PATH=env["LEAN_PATH"], start_utc=s0, seconds=round(t1 - t0, 3),
               exit_code=r.returncode, source=src, source_sha256=sha_file(src), saida=saida,
               saida_sha256=sha_file(saida), olean=olean, olean_sha256=(sha_file(olean) if olean and os.path.exists(olean) else None),
               n_print_axioms=len(recs), fora_do_trio=fora, n_sorryAx=txt.count("sorryAx"),
               n_warning=len(re.findall(r":\d+:\d+: warning", txt)), n_error=len(re.findall(r":\d+:\d+: error", txt)))
    with open(recibo, "w", encoding="utf-8") as fo:
        json.dump(rec, fo, indent=1, ensure_ascii=False)
    print(json.dumps({k: rec[k] for k in ("exit_code", "seconds", "n_print_axioms", "n_sorryAx", "n_warning", "n_error", "olean_sha256")}, ensure_ascii=False))
    print("fora_do_trio:", fora)


if __name__ == "__main__":
    main()
