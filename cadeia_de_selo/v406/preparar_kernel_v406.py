# -*- coding: utf-8 -*-
# [PREPARACAO v406, 02/11/2026 -- ESTADO] SUBIDA MECANICA de preparar_kernel_v405.py (derivar_encanamento_v406.py, lote I). So' o modo `copiar` esta' pronto para a v406 (usa DL.SANDBOX de delta_v406.py e copiar_k406c.sh).
# Os modos `gerar` e `conferir` trazem o corpo da v405 (OITO pedras, ROOT_SUFFIX, STONES...) e dependem do delta completo da v406 (o bundle de ~300 modulos), que a gerencia escreve: NAO os rode antes.
"""preparar_kernel_v406.py -- monta o SANDBOX do kernel da v406 em C:\\t\\k406c\\final (nunca toca o Nos nem C:\\t\\k405c).
Parte da COPIA do kernel do Nos v405 SELADO (copiar_k406c.sh: as fontes da v405 + o .lake/build compilado pelo rito de 28/10; a juncao .lake/packages aponta para a copia da mathlib do k404c, so' leitura; o k405c NAO e' origem nem alvo), e GERA (nao copia) a RAIZ TGLExt.lean a partir da v405 embutida:
raiz = v405 + os OITO imports das pedras novas, na ordem de instalacao (PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion). O Audit NAO muda nesta versao (AUDIT_PREFIX vazio no delta: ele ja' faz `import TGLExt`, a raiz, que traz os modulos novos).
As pedras sao a fonte da ORDEM (v406\\pedra\\*.lean, copias de bytes das fontes de 30/10 a 01/11; o sha16 de cada uma e' LIDO na hora da geracao e conferido contra o que os recibos deram), copiadas para o sandbox quando diferem. Molde: preparar_kernel_v405.py.
uso: python -I -B -X utf8 preparar_kernel_v406.py [copiar|gerar|conferir]   (copiar = chama copiar_k406c.sh; gerar = pedras + raiz [+ Audit se o prefixo nao for vazio]; conferir = so' verifica e escreve kernel_modulos_novos_v406.json)"""
import ast, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v406 as DL  # noqa: E402
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
    rc = subprocess.run(["sh", os.path.join(HERE, "copiar_k406c.sh")], cwd=HERE).returncode
    print("copiar_k406c.sh rc", rc); sys.exit(rc)

base = os.path.join(HERE, DL.BASE_DIR, "um.py")
emb0 = embutido(base, {"_EMBEDDED_KERNEL_FILES"})      # a v405 selada (so' leitura)
PF = DL.pedras_fontes()                                  # le a pedra do disco e confere o sha16 da ordem
STONE = {}
for s, pf in zip(DL.STONES, PF):
    assert os.path.exists(s["src"]) and rb(s["src"]) == rb(s["origem"]), ("a copia v406\\pedra difere da origem: rode copiar_pedras_v406.py", s["name"])
    STONE[s["rel"]] = rd(s["src"])
    assert s["rel"] not in emb0, "a pedra ja' esta' no kernel embutido da v405: " + s["name"]
# (a varredura dos tokens proibidos/sorry e' feita pelo pos_build_kernel_v406.py e pelo gerar_candidato_v406.py, nao aqui)
raiz_old, au_old = emb0["TGLExt.lean"], emb0["TGL/Audit.lean"]
# a raiz e o Audit de partida do sandbox (copia do Nos) == os da v405 embutida == os do Nos
for rel, old in (("TGLExt.lean", raiz_old), ("TGL/Audit.lean", au_old)):
    nos_p = os.path.join(DL.NOS, "tgl_kernel", *rel.split("/")); assert rd(nos_p) == old, ("o arquivo do Nos difere do embutido da v405", rel)
assert raiz_old.endswith("\n") and not any(il in raiz_old or il in au_old for il in DL.IMPORT_LINES)
raiz_new = raiz_old + DL.ROOT_SUFFIX
au_new = DL.AUDIT_PREFIX + au_old
NOVOS = list(DL.STONE_RELS)
info = {"novos": len(NOVOS), "pedras": {s["rel"]: {"sha16": sha256(STONE[s["rel"]].encode())[:16], "bytes": len(STONE[s["rel"]].encode()), "nome_do_operador": s["nome_do_operador"]} for s in DL.STONES},
        "raiz_sha16": sha256(raiz_new.encode())[:16], "audit_sha16": sha256(au_new.encode())[:16], "raiz_v405_sha16": sha256(raiz_old.encode())[:16], "audit_v405_sha16": sha256(au_old.encode())[:16], "ordem_de_instalacao": DL.ORDEM_DE_INSTALACAO}
if mode == "gerar":
    assert os.path.isdir(SB), "o sandbox nao existe: rode `copiar` antes"
    assert os.path.exists(os.path.join(SB, ".lake", "packages", "mathlib", ".lake", "build", "lib", "lean", "Mathlib.olean")), "a juncao .lake/packages do sandbox nao alcanca a mathlib compilada"
    for s in DL.STONES:
        p = os.path.join(SB, *s["rel"].split("/"))
        if not os.path.exists(p) or rd(p) != STONE[s["rel"]]:
            open(p + ".tmp", "w", encoding="utf-8", newline="").write(STONE[s["rel"]]); os.replace(p + ".tmp", p)
    for rel, txt in (("TGLExt.lean", raiz_new), ("TGL/Audit.lean", au_new)):
        p = os.path.join(SB, *rel.split("/")); open(p + ".tmp", "w", encoding="utf-8", newline="").write(txt); assert os.path.getsize(p + ".tmp") == len(txt.encode("utf-8")); os.replace(p + ".tmp", p)
# conferir (sempre): a arvore do sandbox
if os.path.exists(os.path.join(SB, "TGLExt.lean")):
    info["sandbox_pedras_ok"] = {s["rel"]: (os.path.exists(os.path.join(SB, *s["rel"].split("/"))) and rd(os.path.join(SB, *s["rel"].split("/"))) == STONE[s["rel"]]) for s in DL.STONES}
    info["sandbox_raiz_ok"] = rd(os.path.join(SB, "TGLExt.lean")) == raiz_new
    info["sandbox_audit_ok"] = rd(os.path.join(SB, "TGL", "Audit.lean")) == au_new
    # todo .lean embutido da v405 (menos raiz e Audit) existe no sandbox e e' igual; nenhum .lean a mais alem das pedras
    dif = []; extra = []
    for rel, c in emb0.items():
        if rel in ("TGLExt.lean", "TGL/Audit.lean"):
            continue
        q = os.path.join(SB, *rel.split("/"))
        if not os.path.exists(q) or rb(q) != c.encode("utf-8"):
            dif.append(rel)
    emb_set = set(emb0) | set(DL.STONE_RELS)
    for dp, dn, fn in os.walk(SB):
        dn[:] = [d for d in dn if d != ".lake" and d != "probe"]
        for nm in fn:
            if nm.endswith(".lean"):
                rel = os.path.relpath(os.path.join(dp, nm), SB).replace(os.sep, "/")
                if rel not in emb_set and rel not in ("_check_damming.lean", "ExtrairDeps.lean"):
                    extra.append(rel)
    info["sandbox_embutidos_v405_diferentes"] = dif[:5]; info["sandbox_n_embutidos_v405_diferentes"] = len(dif); info["sandbox_lean_a_mais"] = extra[:5]
    info["sandbox_packages_e_juncao"] = os.path.isjunction(os.path.join(SB, ".lake", "packages")) if hasattr(os.path, "isjunction") else None
print(json.dumps(info, ensure_ascii=False, indent=1))
ok = mode == "conferir" and all(v is True for v in (info.get("sandbox_pedras_ok") or {False: False}).values()) and info.get("sandbox_raiz_ok") is True and info.get("sandbox_audit_ok") is True and not info.get("sandbox_n_embutidos_v405_diferentes") and not info.get("sandbox_lean_a_mais")
json.dump({**info, "novos": NOVOS}, open(os.path.join(HERE, "kernel_modulos_novos_v406.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)   # a LISTA vence a contagem
if mode == "conferir":
    print("CONFERIR:", "OK" if ok else "FALHOU"); sys.exit(0 if ok else 1)
