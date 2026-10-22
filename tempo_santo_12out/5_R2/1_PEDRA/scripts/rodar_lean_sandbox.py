"""Compila (no sandbox da PEDRA R2 da F1.TEMPO, construtor da pedra corrigida; copia do executor da R1,
3_KERNEL/scripts/rodar_lean_sandbox.py sha16 81091893c281794d, com KDIR trocado e um caminho extra opcional
SO DE LEITURA no LEAN_PATH) um arquivo .lean com o lean.exe COPIADO para o sandbox, LEAN_PATH so-leitura no .lake
do tgl_kernel do Nos. A saida -o (.olean) vai SO para o sandbox, nunca para o Nos.
Grava a saida (stdout+stderr) e um recibo JSON com sha256 da fonte, da saida e do .olean, codigo de saida, contagem de
avisos/erros, linhas de #print axioms e o que estiver fora do trio {propext, Classical.choice, Quot.sound}.

Variaveis de ambiente:
  TEMPO_IMPORTA_SANDBOX=1   -> o proprio sandbox entra no LEAN_PATH (para importar o .olean da pedra R2);
  TEMPO_LEAN_PATH_EXTRA=dir -> um diretorio extra, SO DE LEITURA, entra no LEAN_PATH (usado uma vez, para importar o
                               .olean da pedra R1 em 3_KERNEL/sandbox e imprimir os seus tipos com #check).
Uso: python -I rodar_lean_sandbox.py <arquivo.lean> <saida.txt> <recibo.json> [<saida.olean>]
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

KDIR = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\1_PEDRA"
SANDBOX = os.path.join(KDIR, "sandbox")
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
        raise SystemExit("RECUSA: a fonte tem de estar no sandbox")
    if olean is not None:
        olean = os.path.abspath(olean)
        if not olean.startswith(SANDBOX):
            raise SystemExit("RECUSA: o .olean tem de ficar no sandbox")
    env = dict(os.environ)
    partes = []
    if os.environ.get("TEMPO_IMPORTA_SANDBOX") == "1":
        partes.append(SANDBOX)
    extra = os.environ.get("TEMPO_LEAN_PATH_EXTRA")
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
    # linhas de #print axioms (podem quebrar linha quando a lista e longa: junta-se ate o ']')
    axiom_records = []
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.search(r"^'(.+)' depends on axioms: \[(.*)", ln)
        if m:
            name = m.group(1)
            rest = m.group(2)
            while "]" not in rest and i + 1 < len(lines):
                i += 1
                rest += " " + lines[i].strip()
            inside = rest.split("]", 1)[0]
            axs = [a.strip() for a in inside.split(",") if a.strip()]
            axiom_records.append({"decl": name, "axioms": axs})
        else:
            m2 = re.search(r"^'(.+)' does not depend on any axioms", ln)
            if m2:
                axiom_records.append({"decl": m2.group(1), "axioms": []})
        i += 1
    fora = [a for a in axiom_records if not set(a["axioms"]) <= TRIO]
    n_warning = len(re.findall(r":\d+:\d+: warning", txt))
    n_error = len(re.findall(r":\d+:\d+: error", txt))
    rec = dict(command=cmd, LEAN_PATH=env["LEAN_PATH"], cwd=SANDBOX, start_utc=s0,
               end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), seconds=round(t1 - t0, 3),
               exit_code=r.returncode, source=src, source_sha256=sha_file(src),
               source_bytes=os.path.getsize(src), output=saida,
               output_sha256=hashlib.sha256(out).hexdigest(), n_axiom_lines=len(axiom_records),
               axiom_records=axiom_records, fora_do_trio=fora,
               n_sorryAx_na_saida=txt.count("sorryAx"), n_warning=n_warning, n_error=n_error,
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
