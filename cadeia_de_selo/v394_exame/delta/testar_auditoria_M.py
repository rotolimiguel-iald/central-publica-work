# -*- coding: utf-8 -*-
"""testar_auditoria_M.py -- exame da R3.4 (M): extrai por AST do esboco R3.4 a funcao auditar_fonte_de_auditoria e as regex dela (sem importar o esboco)
e a roda (1) nas 3 fontes REAIS dos modulos de auditoria do kernel final (C:\\t\\k394d\\final) e (2) em variantes adversariais que a docstring diz recusar.
So' le; escreve so' em v394_exame\\delta."""
import ast, json, os, re, unicodedata, hashlib
H = os.path.dirname(os.path.abspath(__file__))
ESB = r"C:\IALD\Central de Patentes\work\bancada_vinculo_12out\R3_4\sincronizar_bancada.py"
src = open(ESB, "rb").read().decode("utf-8"); T = ast.parse(src)
pega = {"auditar_fonte_de_auditoria", "RE_AUD_IMPORT", "RE_AUD_OPEN", "RE_AUD_PRINT", "RE_AUD_RUNCMD", "RE_AUD_PROIBIDO"}
nodes = [n for n in T.body if (isinstance(n, ast.FunctionDef) and n.name in pega) or (isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], "id", None) in pega)]
ns = {"re": re, "unicodedata": unicodedata}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "<M>", "exec"), ns)
f = ns["auditar_fonte_de_auditoria"]
R = {"esboco_sha16": hashlib.sha256(src.encode()).hexdigest()[:16], "reais": {}, "adversariais": {}}
K = r"C:\t\k394d\final\TGLExt\F1Fecho394"
for m in ("NetworkProofAuditR3", "NetworkProofAuditR7", "NetworkProofAuditR8"):
    t = open(os.path.join(K, m + ".lean"), encoding="utf-8").read()
    r = f(t); R["reais"][m] = {"ok": r["ok"], "motivo": r["motivo"], "contagem": r["contagem"]}
base = "import TGLExt.F1Fecho394.CanonicalModularCoreAssemblyR1\n"
adv = {
    "addDecl_qualificado": base + "run_cmd do\n  let env <- Lean.getEnv\n  Lean.addDecl (Lean.Declaration.axiomDecl {name := `x, levelParams := [], type := Lean.mkConst `True, isUnsafe := false})\n",
    "modifyEnv_qualificado": base + "run_cmd do\n  Lean.modifyEnv fun e => e\n",
    "escrita_de_arquivo_com_open": base + "open IO.FS in\nrun_cmd do\n  writeFile \"C:/t/x.txt\" \"oi\"\n",
    "processo_com_open": base + "open IO in\nrun_cmd do\n  let _ <- Process.output {cmd := \"cmd\", args := #[\"/c\", \"echo\"]}\n",
    "elabCommand_qualificado": base + "run_cmd do\n  Lean.Elab.Command.elabCommand (<- `(theorem t : True := trivial))\n",
    "evalExpr_qualificado": base + "run_cmd do\n  let _ <- Lean.Meta.evalExpr Nat (Lean.mkConst `Nat) (Lean.mkNatLit 1)\n",
    "controle_addDecl_nu": base + "run_cmd do\n  addDecl d\n",
    "controle_IO_FS_writeFile": base + "run_cmd do\n  IO.FS.writeFile \"x\" \"y\"\n",
    "controle_theorem_no_topo": base + "theorem t : True := trivial\n",
}
for k, t in adv.items():
    r = f(t); R["adversariais"][k] = {"ok_passou": r["ok"], "motivo": r["motivo"]}
json.dump(R, open(os.path.join(H, "TESTE_AUDITORIA_M.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
