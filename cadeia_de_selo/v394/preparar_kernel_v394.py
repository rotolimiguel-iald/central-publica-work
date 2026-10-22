# -*- coding: utf-8 -*-
"""preparar_kernel_v394.py -- monta o SANDBOX do kernel da v394 em C:\\t\\k394d\\final (delta_19out: a integracao final; nunca toca o Nos nem C:\\t\\k394).
Parte do tgl_kernel do Nos (v393 instalada, com .lake/build), acrescenta os 189 modulos Lean do Codex (4 TimeGraviton*, RuleQuadraticResidual, 184 F1Fecho394/*) copiados da arvore candidate_r8\\tgl_kernel DO CODEX
(cada um conferido contra o embutido no candidato r8 do Codex e contra a arvore) MAIS a pedra candidata do delta de 19/10 (TheBinaryReadingAtTheFixedPoint: 190 modulos novos), e GERA (nao copia) a raiz TGLExt.lean
e o TGL/Audit.lean a partir dos da v393 embutida: raiz = v393 + os imports do Codex + o import da pedra; Audit = imports do Codex no topo + o import da pedra + a linha TGL_DECL_SOURCE no laco do KH-N1. A raiz e o Audit
SEM a pedra sao comparados byte a byte com os da arvore do Codex (a diferenca, se houver, aborta); com a pedra sao os do delta (delta19_v394.py define as linhas acrescentadas). Molde: preparar_kernel_v393.py.
uso: python -I -B -X utf8 preparar_kernel_v394.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = os 190 + raiz + Audit; conferir = so' verifica)"""
import ast, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402
C = "C:" + os.sep
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CXT = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015")
CXK = os.path.join(CXT, "candidate_r8", "tgl_kernel")
R8 = os.path.join(CXT, "coverage_candidate_r8", "um_v394_prechecked.py")
SB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()


def embutido(path_py, nomes):
    t = open(path_py, "rb").read().decode("utf-8"); tr = ast.parse(t)
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in nomes:
            return ast.literal_eval(n.value)


mode = sys.argv[1] if len(sys.argv) > 1 else "conferir"
if mode == "copiar":
    os.makedirs(DL.SANDBOX_PAI, exist_ok=True)
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    rc = subprocess.run(["robocopy", os.path.join(NOS, "tgl_kernel"), SB, "/E", "/COPY:DAT", "/DCOPY:DAT", "/MT:32", "/R:1", "/W:1", "/NFL", "/NDL", "/NP", "/XF", "TGLExt.lean.bak_*",
                         "/LOG:" + os.path.join(DL.SANDBOX_PAI, "robocopy_final.log")], env=env).returncode
    print("robocopy rc", rc); sys.exit(0 if rc < 8 else 8)

v393 = embutido(os.path.join(NOS, "um.py"), {"_EMBEDDED_KERNEL_FILES"})     # a v393 instalada (so' leitura)
r8 = embutido(R8, {"_EMBEDDED_KERNEL_FILES"})
NOVOS_CODEX = [k for k in r8 if k not in v393]
assert len(NOVOS_CODEX) == 189 and all(k.endswith(".lean") for k in NOVOS_CODEX)
assert [k for k in v393 if k not in r8] == [] and [k for k in v393 if k in r8 and v393[k] != r8[k]] == ["TGLExt.lean", "TGL/Audit.lean"] or sorted([k for k in v393 if k in r8 and v393[k] != r8[k]]) == ["TGL/Audit.lean", "TGLExt.lean"]
# --- a pedra do delta: a fonte autoral (bytes), sem sorry/axiom no codigo
STONE = rd(DL.STONE_SRC)
assert DL.STONE_REL not in r8 and DL.STONE_REL not in v393, "a pedra do delta ja' existe no Nos ou no r8"
NOVOS = NOVOS_CODEX + [DL.STONE_REL]
# --- os 189: o embutido do r8 == a arvore do Codex (bytes)
for k in NOVOS_CODEX:
    assert rd(os.path.join(CXK, *k.split("/"))) == r8[k], ("arvore do Codex != embutido r8", k)
# --- a raiz e o Audit: GERADOS a partir da v393 (primeiro SEM a pedra, igual ao do Codex; depois COM a pedra)
MODS_RAIZ = ["TimeGravitonMatrix", "TimeGravitonScalar", "TimeGravitonFlow", "TimeGravitonKraus", None, "RuleQuadraticResidual", None, "F1Fecho394.NetworkProofAuditR3", None, "F1Fecho394.NetworkProofAuditR7", None, "F1Fecho394.NetworkProofAuditR8"]
suf_raiz = "\n" + "\n".join(("import TGLExt." + m) if m else "" for m in MODS_RAIZ)
raiz_old = v393["TGLExt.lean"]
# o Codex: a raiz termina SEM \n final? comparamos com as variantes
cands = [raiz_old + suf_raiz, raiz_old.rstrip("\n") + "\n" + suf_raiz, raiz_old + suf_raiz.lstrip("\n"), raiz_old + suf_raiz + "\n"]
ok_raiz = [c for c in cands if c == r8["TGLExt.lean"]]
assert ok_raiz, "a raiz gerada nao bate com a do Codex em nenhuma variante de fim de linha"
raiz_r8 = ok_raiz[0]
topo = "import TGLExt.F1Fecho394.NetworkProofAuditR8\n\nimport TGLExt.F1Fecho394.NetworkProofAuditR7\n\nimport TGLExt.F1Fecho394.NetworkProofAuditR3\n\nimport TGLExt.RuleQuadraticResidual\n\nimport TGLExt.TimeGravitonMatrix\nimport TGLExt.TimeGravitonScalar\nimport TGLExt.TimeGravitonFlow\nimport TGLExt.TimeGravitonKraus\n\n"
alvo = "      if m.getRoot == `TGL || m.getRoot == `TGLExt then\n"
au_old = v393["TGL/Audit.lean"]
assert au_old.count(alvo) == 1
au_r8 = topo + au_old.replace(alvo, alvo + "        IO.println (\"TGL_DECL_SOURCE\\t\" ++ n.toString ++ \"\\t\" ++ m.toString)\n")
assert au_r8 == r8["TGL/Audit.lean"], "o Audit gerado nao bate com o do Codex"
assert rd(os.path.join(CXK, "TGLExt.lean")) == raiz_r8 and rd(os.path.join(CXK, "TGL", "Audit.lean")) == au_r8
# --- COM a pedra do delta
assert raiz_r8.endswith("\n") and DL.IMPORT_LINE not in raiz_r8 and DL.IMPORT_LINE not in au_r8
raiz_new = raiz_r8 + DL.ROOT_SUFFIX
au_new = DL.AUDIT_PREFIX + au_r8
info = {"novos": len(NOVOS), "novos_do_codex": len(NOVOS_CODEX), "pedra_do_delta": {"path": DL.STONE_REL, "sha16": sha256(STONE.encode())[:16], "bytes": len(STONE.encode())},
        "raiz_sha16": sha256(raiz_new.encode())[:16], "audit_sha16": sha256(au_new.encode())[:16], "raiz_r8_sha16": sha256(raiz_r8.encode())[:16], "audit_r8_sha16": sha256(au_r8.encode())[:16],
        "raiz_v393_sha16": sha256(raiz_old.encode())[:16], "audit_v393_sha16": sha256(au_old.encode())[:16]}
if mode == "gerar":
    for k in NOVOS_CODEX:
        p = os.path.join(SB, *k.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="").write(r8[k])
    p = os.path.join(SB, *DL.STONE_REL.split("/")); open(p, "w", encoding="utf-8", newline="").write(STONE)
    for rel, txt in (("TGLExt.lean", raiz_new), ("TGL/Audit.lean", au_new)):
        p = os.path.join(SB, *rel.split("/")); open(p + ".tmp", "w", encoding="utf-8", newline="").write(txt); os.replace(p + ".tmp", p)
# conferir (sempre): a arvore do sandbox
if os.path.exists(os.path.join(SB, "TGLExt.lean")):
    st = {}
    for k in NOVOS_CODEX:
        p = os.path.join(SB, *k.split("/")); st[k] = os.path.exists(p) and rd(p) == r8[k]
    p = os.path.join(SB, *DL.STONE_REL.split("/")); st[DL.STONE_REL] = os.path.exists(p) and rd(p) == STONE
    info["sandbox_novos_ok"] = sum(st.values()); info["sandbox_raiz_ok"] = rd(os.path.join(SB, "TGLExt.lean")) == raiz_new; info["sandbox_audit_ok"] = rd(os.path.join(SB, "TGL", "Audit.lean")) == au_new
print(json.dumps(info, ensure_ascii=False, indent=1))
json.dump({**info, "novos": NOVOS}, open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
