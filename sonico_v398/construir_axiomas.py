# -*- coding: utf-8 -*-
"""construir_axiomas.py -- monta AXIOMAS.json de TGLExt.Sonico a partir do que o LEAN diz (collectAxioms de CADA declaracao do modulo) e do log do
`lake build TGLExt.Sonico`. Nada de hash nem de numero de memoria: tudo lido de arquivo ou da saida do processo.

Processos criados por este script (e esperados por ele): `lake env lean --version`, `lake env lean probe/axioms_dump.lean`,
`lake env lean probe/nomes_citados.lean`. Escreve so em C:\\IALD\\Central de Patentes\\work\\sonico_v398 (e le o sandbox C:\\t\\k398\\final).
Uso: python -I -B -X utf8 construir_axiomas.py
"""
import hashlib
import json
import os
import re
import subprocess

W = r"C:\IALD\Central de Patentes\work\sonico_v398"
SB = r"C:\t\k398\final"
LOG = os.path.join(W, "lake_build_sonico.log")
FONTE_W = os.path.join(W, "Sonico.lean")
FONTE_SB = os.path.join(SB, "TGLExt", "Sonico.lean")
OLEAN = os.path.join(SB, ".lake", "build", "lib", "lean", "TGLExt", "Sonico.olean")
TRIO = ["propext", "Classical.choice", "Quot.sound"]

env = dict(os.environ)
env["PATH"] = r"C:\Users\rotol\.elan\bin;" + env.get("PATH", "")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=SB, env=env, encoding="utf-8", timeout=900)
    return r.returncode, r.stdout + r.stderr


def sha(path):
    b = open(path, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    return {"sha256": h, "sha16": h[:16], "bytes": len(b)}


src_b = open(FONTE_W, "rb").read()
assert src_b == open(FONTE_SB, "rb").read(), "fonte do trabalho difere do fonte compilado no sandbox"
src = src_b.decode("utf-8")
linhas = src.split("\n")

# declaracoes nomeadas no fonte (namespace TGLExt.Sonico)
pat = re.compile(r"^(?:@\[[^\]]*\]\s*)?(theorem|def|structure|abbrev|lemma)\s+([A-Za-z0-9_'.]+)")
nomeadas = {}
for i, ln in enumerate(linhas, 1):
    m = pat.match(ln)
    if m:
        nomeadas["TGLExt.Sonico." + m.group(2)] = {"tipo_no_fonte": m.group(1), "linha": i}
print_axioms_no_fonte = re.findall(r"^#print axioms (\S+)", src, flags=re.M)

# versao do Lean e do Mathlib
rc_v, out_v = run(["lake", "env", "lean", "--version"])
manifest = json.load(open(os.path.join(SB, "lake-manifest.json"), encoding="utf-8"))
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
toolchain = open(os.path.join(SB, "lean-toolchain"), encoding="utf-8").read().strip()

# dump: collectAxioms de cada declaracao do modulo
rc_d, out_d = run(["lake", "env", "lean", "probe/axioms_dump.lean"])
open(os.path.join(W, "axioms_dump_raw.txt"), "w", encoding="utf-8", newline="\n").write(out_d)
rows = []
for ln in out_d.split("\n"):
    ln = ln.rstrip("\r")
    if not ln.startswith("DECL|"):
        continue
    _, nome, tipo, interno, axs = ln.split("|", 4)
    rows.append({"nome": nome, "tipo": tipo, "interno": interno == "true", "axiomas": [a for a in axs.split(",") if a]})
dump_names = {r["nome"] for r in rows}
faltando_no_dump = sorted(n for n in nomeadas if n not in dump_names)

decls = []
for r in rows:
    d = {"nome": r["nome"], "tipo": r["tipo"], "origem": "fonte" if r["nome"] in nomeadas else "gerada_pelo_Lean", "axiomas": r["axiomas"]}
    if r["nome"] in nomeadas:
        d["linha_no_fonte"] = nomeadas[r["nome"]]["linha"]
    decls.append(d)
uniao = sorted({a for r in rows for a in r["axiomas"]})
fora_do_trio = sorted(a for a in uniao if a not in TRIO)
por_tipo = {}
for r in rows:
    por_tipo[r["tipo"]] = por_tipo.get(r["tipo"], 0) + 1

# os #print axioms do proprio build (as seis linhas do fonte)
log = open(LOG, encoding="utf-8").read()
blocos = re.findall(r"info: TGLExt/Sonico\.lean:(\d+):0: '([^']+)' depends on axioms: \[(.*?)\]", log, flags=re.S)
print_do_build = {}
for ln, nome, axs in blocos:
    print_do_build[nome] = {"linha_no_fonte": int(ln), "axiomas": [a.strip() for a in axs.replace("\n", " ").split(",") if a.strip()]}
m_built = re.search(r"Built TGLExt\.Sonico \((\d+)s\)", log)
m_jobs = re.search(r"\[(\d+)/(\d+)\] Built TGLExt\.Sonico", log)
m_ok = re.search(r"Build completed successfully \((\d+) jobs\)", log)
avisos_do_modulo = [l for l in log.split("\n") if re.search(r"TGLExt/Sonico\.lean:\d+:\d+: (warning|error)", l)]

# nomes citados (probe #check) e nao-vacuidade (instanciamento)
rc_c, out_c = run(["lake", "env", "lean", "probe/nomes_citados.lean"])
open(os.path.join(W, "nomes_citados_saida.txt"), "w", encoding="utf-8", newline="\n").write(out_c)
erros_c = [l for l in out_c.split("\n") if "error" in l.lower() or "unknown" in l.lower()]

R = {
    "modulo": "TGLExt.Sonico",
    "fonte": {**sha(FONTE_W), "linhas": src.count("\n"), "caminho_trabalho": FONTE_W, "caminho_sandbox": FONTE_SB, "copia_identica": True},
    "olean": {**sha(OLEAN), "caminho": OLEAN},
    "ambiente": {
        "lean_version": out_v.strip(), "lean_toolchain": toolchain, "mathlib_rev": mathlib["rev"], "mathlib_inputRev": mathlib["inputRev"],
        "sandbox": SB, "origem_do_sandbox": r"cópia (robocopy sem /PURGE, /XJ, sem *.bak_*) de C:\t\k397c (kernel v397 compilado); k397c só lido",
    },
    "build": {
        "comando": "lake build TGLExt.Sonico  (cwd C:\\t\\k398\\final)", "returncode": 0 if m_ok else None, "log": LOG,
        "linha_built": m_built.group(0) if m_built else None, "tarefas": (m_ok.group(1) if m_ok else None),
        "avisos_ou_erros_do_modulo": avisos_do_modulo,
    },
    "declaracoes_no_olean": len(rows),
    "declaracoes_nomeadas_no_fonte": len(nomeadas),
    "nomeadas_faltando_no_dump": faltando_no_dump,
    "contagem_por_tipo": por_tipo,
    "print_axioms_no_fonte": print_axioms_no_fonte,
    "print_axioms_do_build": print_do_build,
    "declaracoes": decls,
    "uniao_dos_axiomas": uniao,
    "axiomas_fora_do_trio": fora_do_trio,
    "usa_sorryAx": "sorryAx" in uniao,
    "usa_axioma_proprio": any(r["tipo"] == "axiom" for r in rows),
    "todas_no_trio_e_zero_sorry": (not fora_do_trio) and ("sorryAx" not in uniao) and not faltando_no_dump and rc_d == 0,
    "nomes_citados": {"saida": os.path.join(W, "nomes_citados_saida.txt"), "returncode": rc_c, "linhas_com_erro": erros_c},
    "dump_returncode": rc_d,
}
json.dump(R, open(os.path.join(W, "AXIOMAS.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k not in ("declaracoes", "print_axioms_do_build")}, ensure_ascii=False, indent=1)[:4000])
print("print_axioms_do_build:", {k: v["axiomas"] for k, v in print_do_build.items()})
