"""#print axioms de TODAS as declarações do módulo TGLExt.TestemunhaEstatica (as nomeadas, as geradas pelo Lean e as privadas geradas).

1) lê o dump cru (collectAxioms) e gera C:\\t\\k396\\final\\probe\\print_all.lean: um `#print axioms` textual por declaração de nome
   comum e, para as declarações geradas PRIVADAS (`_private.<módulo>.0....`, cujo nome tem componente numérico e não se escreve como
   identificador), um bloco `run_cmd` que enumera as privadas do módulo e elabora `#print axioms` com o Name exato (mkIdent);
2) roda `lake env lean probe/print_all.lean` no sandbox (processo criado e esperado por este script);
3) confere linha a linha: todo axioma pertence ao trio, nenhum `sorryAx`, e todas as declarações do dump foram impressas;
4) grava print_axioms_todas.txt (saída crua) e print_axioms_todas_resumo.json na pasta de trabalho.
"""
import json
import os
import re
import subprocess

W = r"C:\IALD\Central de Patentes\work\testemunha_estatica_v396"
SB = r"C:\t\k396\final"
DUMP = r"C:\t\k396\axioms_dump_raw.txt"
TRIO = {"propext", "Classical.choice", "Quot.sound"}

nomes = []
for ln in open(DUMP, encoding="utf-8"):
    if ln.startswith("DECL|"):
        nomes.append(ln.split("|")[1])
comuns = [n for n in nomes if not n.startswith("_private")]
privadas = [n for n in nomes if n.startswith("_private")]

lean = "import TGLExt.TestemunhaEstatica\n\n" + "".join(f"#print axioms {n}\n" for n in comuns)
if privadas:
    lean += """
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.TestemunhaEstatica | throwError "modulo ausente"
  let mut raw : Array Name := #[]
  for (n, _) in env.constants.map₁.toList do
    if env.getModuleIdxFor? n == some idx && (n.toString.startsWith "_private") then
      raw := raw.push n
  let sorted := raw.qsort (fun a b => a.toString < b.toString)
  for n in sorted do
    elabCommand (← `(#print axioms $(mkIdent n)))
"""
open(SB + r"\probe\print_all.lean", "w", encoding="utf-8", newline="\n").write(lean)

env = dict(os.environ)
env["PATH"] = r"C:\Users\rotol\.elan\bin;" + env.get("PATH", "")
r = subprocess.run(["lake", "env", "lean", "probe/print_all.lean"], capture_output=True, text=True, cwd=SB, env=env, encoding="utf-8")
saida = r.stdout + r.stderr
open(W + r"\print_axioms_todas.txt", "w", encoding="utf-8", newline="\n").write(saida)

pat_dep = re.compile(r"^'([^']+)' depends on axioms: \[(.*)\]$")
pat_nodep = re.compile(r"^'([^']+)' does not depend on any axioms$")
# a saída pode quebrar a lista em várias linhas: junta linhas de continuação
bloco = []
outras = []
for ln in saida.split("\n"):
    ln = ln.rstrip("\r")
    if ln.startswith("'"):
        bloco.append(ln)
    elif ln.startswith(" ") and ln.strip() and bloco:
        bloco[-1] += " " + ln.strip()
    elif ln.strip():
        outras.append(ln.strip())
vistos = {}
anomalias = []
for ln in bloco:
    m = pat_dep.match(ln)
    if m:
        axs = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
        vistos[m.group(1)] = axs
        continue
    m = pat_nodep.match(ln)
    if m:
        vistos[m.group(1)] = []
        continue
    anomalias.append(ln)
faltam = [n for n in nomes if n not in vistos]
fora = sorted({a for axs in vistos.values() for a in axs if a not in TRIO})
resumo = {
    "comando": "lake env lean probe/print_all.lean  (cwd C:\\t\\k396\\final)",
    "returncode": r.returncode,
    "declaracoes_no_modulo": len(nomes),
    "declaracoes_de_nome_comum": len(comuns),
    "declaracoes_privadas_geradas_(match_1.eq_N/splitter)": len(privadas),
    "declaracoes_impressas": len(vistos),
    "nao_impressas": faltam,
    "anomalias_de_formato": anomalias,
    "avisos_do_linter_auxLemma(nomes_auxiliares_gerados_pelo_Lean)": sum(1 for a in outras if "auto-generated auxiliary declaration" in a),
    "outros_avisos_ou_erros": [a for a in outras
                               if not a.startswith("Note:") and "auto-generated auxiliary declaration" not in a],
    "uniao_dos_axiomas": sorted({a for axs in vistos.values() for a in axs}),
    "axiomas_fora_do_trio": fora,
    "usa_sorryAx": "sorryAx" in {a for axs in vistos.values() for a in axs},
    "todas_no_trio_e_zero_sorry": (not fora) and ("sorryAx" not in {a for axs in vistos.values() for a in axs}) and not faltam and not anomalias and r.returncode == 0,
    "sem_nenhum_axioma": sum(1 for axs in vistos.values() if not axs),
    "arquivo_gerado": SB + r"\probe\print_all.lean",
    "saida_crua": W + r"\print_axioms_todas.txt",
}
json.dump(resumo, open(W + r"\print_axioms_todas_resumo.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps(resumo, ensure_ascii=False, indent=1))
