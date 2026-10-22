# Proposta KH-N1 para a v392, TESTADA: um run_cmd que imprime, para cada constante do fecho, uma linha NO FORMATO do
# `#print axioms` (o que a regex do um.py ja le) -- assim o axiom_report cobre o kernel inteiro sem 24 mil linhas no Audit.
# modo "76": so os 76 modulos sem nenhuma entrada no axiom_report v391; modo "total": o fecho TGL+TGLExt inteiro.
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

F = L.F
KH = os.path.join(F, "kh")
LOG = os.path.join(F, "logs", "KH")
modo = sys.argv[1]
fin = json.load(open(os.path.join(KH, "KH_N1_final.json"), encoding="utf-8"))
SNIP = '''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if FILTRO then
        let axs ← liftCoreM (collectAxioms n)
        n_decl := n_decl + 1
        if ci matches .thmInfo _ then n_thm := n_thm + 1
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do n_fora := n_fora + 1
        if axs.isEmpty then
          IO.println ("'" ++ n.toString ++ "' does not depend on any axioms")
        else
          IO.println ("'" ++ n.toString ++ "' depends on axioms: [" ++ String.intercalate ", " (axs.toList.map Name.toString) ++ "]")
  IO.println ("TGL_AXIOM_COVERAGE_TOTAL decl=" ++ toString n_decl ++ " thm=" ++ toString n_thm ++ " fora_do_trio=" ++ toString n_fora)
'''
if modo == "76":
    mods = fin["modulos_com_teorema_e_zero_entradas"]
    src = ("-- KH-N1 proposta v392 (exame F_KERNEL 12/10/2026, so sandbox): os 76 modulos sem entrada, no formato do #print axioms\n"
           + "".join("import %s\n" % m for m in mods) + "\n"
           + "open Lean in\ndef alvoCobertura : NameSet := ([" + ", ".join("`" + m for m in mods) + "] : List Name).foldl (fun s n => s.insert n) {}\n\n"
           + SNIP.replace("FILTRO", "alvoCobertura.contains m"))
    nome = "KH_formato_umpy_76"
else:
    src = ("-- KH-N1 proposta v392 (exame F_KERNEL 12/10/2026, so sandbox): o fecho TGL+TGLExt INTEIRO, no formato do #print axioms\n"
           "import TGL\nimport TGLExt\n\n" + SNIP.replace("FILTRO", "m.getRoot == `TGL || m.getRoot == `TGLExt"))
    nome = "KH_formato_umpy_total"
p = os.path.join(KH, nome + ".lean")
if not os.path.exists(p):
    open(p, "w", encoding="utf-8", newline="\n").write(src)
r = L.run_lean(nome, p, KH, None, LOG, timeout=14400)
out = open(r["log"], "rb").read().decode("utf-8", "replace")
ax = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", out, re.S):
    ax[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", out):
    ax.setdefault(m.group(1), [])
tot = [l for l in out.splitlines() if l.startswith("TGL_AXIOM_COVERAGE_TOTAL")]
r.update({"lidos_pela_regex_do_umpy": len(ax), "total": tot, "fora": [k for k, v in ax.items() if not set(v) <= L.TRIO]})
print(nome, "rc", r["rc"], "s", r["segundos"], "lidos", len(ax), tot)
print(L.dump(r, os.path.join(F, "RESULTADO_%s.json" % nome)))
