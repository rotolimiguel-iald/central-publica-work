# -*- coding: utf-8 -*-
"""preparar_kernel_v396.py -- monta o SANDBOX do kernel da v396 em C:\\t\\k396c\\final (nunca toca o Nos nem C:\\t\\k396).
Parte de C:\\t\\k396\\final (copia do tgl_kernel do Nos v395 com a pedra TestemunhaEstatica ja' compilada em .lake/build numa versao anterior do texto; sem a pasta probe\\ de rascunhos nem as sondas do construtor nem os .bak_ da pedra), e GERA (nao copia) a raiz TGLExt.lean
e o TGL/Audit.lean a partir dos da v395 embutida: raiz = v395 + o import da pedra; Audit = o import da pedra no topo + o Audit da v395. A pedra e' a fonte autoral (work\\testemunha_estatica_v396\\TestemunhaEstatica.lean; so' ajustes de docstring depois do exame independente, que a aprovou), copiada para o sandbox quando difere (o sha16 e' LIDO na hora da geracao). Molde: preparar_kernel_v395.py.
uso: python -I -B -X utf8 preparar_kernel_v396.py [copiar|gerar|conferir]   (copiar = robocopy; gerar = pedra + raiz + Audit; conferir = so' verifica e escreve kernel_modulos_novos_v396.json)"""
import ast, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v396 as DL  # noqa: E402
SB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
rb = lambda p: open(p, "rb").read()


def embutido(path_py, nomes):
    t = open(path_py, "rb").read().decode("utf-8"); tr = ast.parse(t)
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in nomes:
            return ast.literal_eval(n.value)


mode = sys.argv[1] if len(sys.argv) > 1 else "conferir"
if mode == "copiar":
    assert not os.path.exists(SB), "o sandbox ja existe: nao sobrescrevo (apague a pasta pelo operador/gerencia se for refazer)"
    os.makedirs(DL.SANDBOX_PAI, exist_ok=True)
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    rc = subprocess.run(["robocopy", DL.SANDBOX_ORIGEM, SB, "/E", "/COPY:DAT", "/DCOPY:DAT", "/MT:32", "/R:1", "/W:1", "/NFL", "/NDL", "/NP", "/XJ", "/XD", "probe", "/XF", "TestemunhaEstatica*.bak_*", "TGLExt.lean.bak_*",
                         "/LOG:" + os.path.join(DL.SANDBOX_PAI, "robocopy_final.log")], env=env).returncode
    print("robocopy rc", rc); sys.exit(0 if rc < 8 else 8)

base = os.path.join(HERE, DL.BASE_DIR, "um.py")
emb0 = embutido(base, {"_EMBEDDED_KERNEL_FILES"})      # a v395 selada (so' leitura)
STONE = rd(DL.STONE_SRC)
assert DL.STONE_REL not in emb0, "a pedra ja' esta' no kernel embutido da v395"
# (a varredura dos tokens proibidos/sorry e' feita pelo pos_build_kernel_v396.py e pelo gerar_candidato_v396.py, nao aqui)
raiz_old, au_old = emb0["TGLExt.lean"], emb0["TGL/Audit.lean"]
# a raiz e o Audit de partida do sandbox (copia de k396\final) == os da v395 embutida == os do Nos
for rel, old in (("TGLExt.lean", raiz_old), ("TGL/Audit.lean", au_old)):
    nos_p = os.path.join(DL.NOS, "tgl_kernel", *rel.split("/")); assert rd(nos_p) == old, ("o arquivo do Nos difere do embutido da v395", rel)
assert raiz_old.endswith("\n") and DL.IMPORT_LINE not in raiz_old and DL.IMPORT_LINE not in au_old
raiz_new = raiz_old + DL.ROOT_SUFFIX
au_new = DL.AUDIT_PREFIX + au_old
NOVOS = [DL.STONE_REL]
info = {"novos": len(NOVOS), "pedra": {"path": DL.STONE_REL, "sha16": sha256(STONE.encode())[:16], "bytes": len(STONE.encode())},
        "raiz_sha16": sha256(raiz_new.encode())[:16], "audit_sha16": sha256(au_new.encode())[:16], "raiz_v395_sha16": sha256(raiz_old.encode())[:16], "audit_v395_sha16": sha256(au_old.encode())[:16]}
if mode == "gerar":
    assert os.path.isdir(SB), "o sandbox nao existe: rode `copiar` antes"
    p = os.path.join(SB, *DL.STONE_REL.split("/"))
    if not os.path.exists(p) or rd(p) != STONE:
        open(p + ".tmp", "w", encoding="utf-8", newline="").write(STONE); os.replace(p + ".tmp", p)
    for rel, txt in (("TGLExt.lean", raiz_new), ("TGL/Audit.lean", au_new)):
        p = os.path.join(SB, *rel.split("/")); open(p + ".tmp", "w", encoding="utf-8", newline="").write(txt); assert os.path.getsize(p + ".tmp") == len(txt.encode("utf-8")); os.replace(p + ".tmp", p)
# conferir (sempre): a arvore do sandbox
if os.path.exists(os.path.join(SB, "TGLExt.lean")):
    p = os.path.join(SB, *DL.STONE_REL.split("/"))
    info["sandbox_pedra_ok"] = os.path.exists(p) and rd(p) == STONE
    info["sandbox_raiz_ok"] = rd(os.path.join(SB, "TGLExt.lean")) == raiz_new
    info["sandbox_audit_ok"] = rd(os.path.join(SB, "TGL", "Audit.lean")) == au_new
    # todo .lean embutido da v395 (menos raiz e Audit) existe no sandbox e e' igual; nenhum .lean a mais alem da pedra
    dif = []; extra = []
    for rel, c in emb0.items():
        if rel in ("TGLExt.lean", "TGL/Audit.lean"):
            continue
        q = os.path.join(SB, *rel.split("/"))
        if not os.path.exists(q) or rb(q) != c.encode("utf-8"):
            dif.append(rel)
    emb_set = set(emb0) | {DL.STONE_REL}
    for dp, dn, fn in os.walk(SB):
        dn[:] = [d for d in dn if d != ".lake" and d != "probe"]
        for nm in fn:
            if nm.endswith(".lean"):
                rel = os.path.relpath(os.path.join(dp, nm), SB).replace(os.sep, "/")
                if rel not in emb_set and rel not in ("_check_damming.lean", "ExtrairDeps.lean"):
                    extra.append(rel)
    info["sandbox_embutidos_v395_diferentes"] = dif[:5]; info["sandbox_n_embutidos_v395_diferentes"] = len(dif); info["sandbox_lean_a_mais"] = extra[:5]
print(json.dumps(info, ensure_ascii=False, indent=1))
ok = mode == "conferir" and all(info.get(k) is True for k in ("sandbox_pedra_ok", "sandbox_raiz_ok", "sandbox_audit_ok")) and not info.get("sandbox_n_embutidos_v395_diferentes") and not info.get("sandbox_lean_a_mais")
json.dump({**info, "novos": NOVOS}, open(os.path.join(HERE, "kernel_modulos_novos_v396.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # a LISTA vence a contagem (defeito do molde v395 corrigido)
if mode == "conferir":
    print("CONFERIR:", "OK" if ok else "FALHOU"); sys.exit(0 if ok else 1)
