# -*- coding: utf-8 -*-
"""preparar_kernel_v400.py -- CONFERE o sandbox do kernel da v400 (C:\\t\\k400c\\final, COPIA de C:\\t\\k399c\\final) e escreve kernel_modulos_novos_v400.json. A v400 NAO acrescenta modulo ao kernel: a lista dos modulos novos
(sobre a base v399 selada) e' VAZIA, e e' a LISTA que instalar, reverter, o rito, o conferidor e o p00 leem (nunca um numero digitado). A Bancada, que ainda pina a v398, ve o diff v398 -> v400: `pedras_desde_a_bancada` traz a pedra
Testemunho (DL.STONES_DESDE_B8), que o recibo do kernel do B(n) lista. Confere: o corpo embutido do um.py base (v399 selada) == o sandbox, arquivo a arquivo (a raiz TGLExt.lean, o TGL/Audit.lean, a pedra e todos os demais);
o sha256 da raiz/Audit/pedra == o manifesto do kernel que o selo v399 pina (formal_files_sha256). Nada e' escrito no sandbox, no Nos nem na producao.
uso: python -I -B -X utf8 preparar_kernel_v400.py [conferir]"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
KB = DL.SANDBOX
um_src = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")
tree = ast.parse(um_src)
emb = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
man = json.load(open(os.path.join(HERE, DL.BASE_DIR, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
rd = lambda p: open(p, "rb").read()
dif, ausentes = [], []
for rel, txt in emb.items():
    p = os.path.join(KB, *rel.split("/"))
    if not os.path.exists(p):
        ausentes.append(rel); continue
    if rd(p) != txt.encode("utf-8"):
        dif.append(rel)
ok_manifesto = all(sha(emb[r].encode("utf-8")) == ff.get(r) for r in ("TGLExt.lean", "TGL/Audit.lean") + tuple(DL.STONE_RELS_DESDE_B8))
assert not dif and not ausentes, ("o sandbox difere do corpo embutido da v399 selada", dif[:5], ausentes[:5])
assert ok_manifesto, "raiz/Audit/pedra do corpo embutido != formal_files_sha256 do manifesto que o selo v399 pina"
assert not DL.STONES and DL.STONE_RELS == [] and all(r in emb for r in DL.STONE_RELS_DESDE_B8)
info = {"contrato": "KERNEL_MODULOS_NOVOS_v400", "sobre": "base v399 selada (um.py %s)" % DL.BASE_SHA16_DA_ORDEM, "novos": [], "n_novos": 0,
        "pedras_desde_a_bancada": list(DL.STONE_RELS_DESDE_B8), "nota_da_bancada": "a Bancada de producao pina a v398: o recibo do kernel do B(n) lista o diff v398 -> v400 (a pedra Testemunho + a raiz + o Audit), nao o diff v399 -> v400 (vazio)",
        "sandbox": KB.replace(os.sep, "/"), "arquivos_embutidos_conferidos": len(emb), "raiz_sha16": sha(emb["TGLExt.lean"].encode("utf-8"))[:16], "audit_sha16": sha(emb["TGL/Audit.lean"].encode("utf-8"))[:16],
        "estatuto": "[REAL] conferido por script: o kernel da v400 e' o da v399, byte a byte, nos %d arquivos embutidos" % len(emb)}
json.dump(info, open(os.path.join(HERE, "kernel_modulos_novos_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: info[k] for k in ("novos", "pedras_desde_a_bancada", "arquivos_embutidos_conferidos", "raiz_sha16", "audit_sha16")}, ensure_ascii=False))
