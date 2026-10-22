# -*- coding: utf-8 -*-
"""teste_scanner_r35.py (R3.5) -- ensaio rapido (so leitura) do auditar_fonte_de_auditoria da R3.5: as 3 fontes reais e a fixture passam; as evasoes da revisao independente e as minhas recusam.
uso: python -I -B -X utf8 teste_scanner_r35.py"""
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("esb_r35", AQUI / "sincronizar_bancada.py")
M = importlib.util.module_from_spec(spec)
sys.modules["esb_r35"] = M
spec.loader.exec_module(M)
F = AQUI / "evidencias" / "fontes_reais_v394" / "TGLExt" / "F1Fecho394"
BASE = "import TGLExt.PedraSinteticaC\nimport Lean\n\nopen Lean in\nrun_cmd do\n  let env ← Elab.Command.liftCoreM getEnv\n  let mut n := 0\n  IO.println (\"AUDIT_COUNT \" ++ toString n)\n"
ok = True
for nome in ("NetworkProofAuditR3.lean", "NetworkProofAuditR7.lean", "NetworkProofAuditR8.lean"):
    r = M.auditar_fonte_de_auditoria((F / nome).read_text(encoding="utf-8"))
    print("REAL", nome, r["ok"], r["motivo"], r["contagem"])
    ok &= r["ok"] is True
r = M.auditar_fonte_de_auditoria(BASE)
print("BASE", r["ok"], r["motivo"])
ok &= r["ok"] is True
EVASOES = {
    "Lean.addDecl_qualificado": BASE + "  Lean.addDecl (.axiomDecl default)\n",
    "Lean.modifyEnv_qualificado": BASE + "  Lean.modifyEnv (fun e => e)\n",
    "Lean.Meta.evalExpr_qualificado": BASE + "  let _ ← Lean.Meta.evalExpr Nat (mkConst `Nat) (mkConst `Nat)\n",
    "open_IO.FS_in_writeFile": BASE.replace("open Lean in", "open IO.FS in") + "  writeFile \"x\" \"y\"\n",
    "open_IO_in_Process.output": BASE.replace("open Lean in", "open IO in") + "  let _ ← Process.output { cmd := \"calc\" }\n",
    "addDecl_nu": BASE + "  addDecl (.axiomDecl default)\n",
    "_root_.Lean.addDecl": BASE + "  _root_.Lean.addDecl (.axiomDecl default)\n",
    "IO.FS.writeFile": BASE + "  IO.FS.writeFile \"x\" \"y\"\n",
    "interpolacao_nao_local": BASE + "  throwError \"x {IO.FS.readFile \\\"a\\\"}\"\n",
    "ponto_e_virgula": BASE + "  let k := 1; let j := 2\n",
    "cifrao": BASE + "  let k := $x\n",
    "comentario_na_linha": BASE + "  let k := 1 -- IO.FS.writeFile\n",
    "include_str": BASE + "  let k := include_str \"/etc/hosts\"\n",
    "unsafe": BASE + "  unsafe pure ()\n",
    "open_Lean.Meta": BASE.replace("open Lean in", "open Lean.Meta in"),
    "open_Lean_IO": BASE.replace("open Lean in", "open Lean IO in"),
    "import_Mathlib": BASE.replace("import Lean\n", "import Mathlib\n"),
    "nome_crase_fora": BASE + "  let k := `Foo.bar\n",
    "homoglifo_cirilico": BASE + "  Lеan.addDecl 1\n",
    "local_novo": BASE + "  let defaults := 1\n",
}
for nome, txt in EVASOES.items():
    r = M.auditar_fonte_de_auditoria(txt)
    print("EVASAO", nome, "recusada" if not r["ok"] else "PASSOU!!", "|", r["motivo"])
    ok &= r["ok"] is False
print("TUDO COMO ESPERADO" if ok else "DIVERGENCIA")
sys.exit(0 if ok else 1)
