# -*- coding: utf-8 -*-
"""copiar_base_v400.py -- copia de BYTES do Nos v399 SELADO para v400\\base_v399 (um.py, selo, core, manifesto do kernel, resultado do pilar e o SIDECAR um_absoluto_selo_acom.json),
mais as copias de bytes do selo e do manifesto do kernel da v398 (a versao que a Bancada de producao AINDA pina) para v400\\base_v398 (o B(n) as exige: --selo-anterior e --kernel-manifesto-anterior).
Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v399; o sha16 == o candidato_sha16 de v399\\ESPERADOS_v399.json == o que a ordem da gerencia deu (a5aacfa4e5be9b12; o arquivo manda);
o manifesto do kernel e o resultado do pilar == o que o selo pina; o sidecar existe, e' o da v399 e pina o um.py (objeto `um.py`) com o mesmo sha256.
So' LE o Nos; escreve so' em v400\\base_v399 e v400\\base_v398. Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve em silencio). Molde: copiar_base_v399.py.
uso: python -I -B -X utf8 copiar_base_v400.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
ARQ = ["um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json"]
dst = os.path.join(HERE, DL.BASE_DIR); os.makedirs(dst, exist_ok=True)
raw = open(os.path.join(DL.NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(DL.NOS, "um_absoluto_selo.json"), encoding="utf-8"))
esp = json.load(open(os.path.join(DL.V399, "ESPERADOS_v399.json"), encoding="utf-8"))
assert selo.get("um_version") == DL.BASE_VERSION, ("o selo do Nos nao e' a v399", selo.get("um_version"))
assert sha(raw) == selo["sha256"]["um.py"], "o um.py do Nos nao e' o que o selo pina"
assert sha(raw)[:16] == esp["candidato_sha16"], ("o um.py do Nos nao e' o candidato selado da v399 (ESPERADOS_v399)", sha(raw)[:16], esp["candidato_sha16"])
assert sha(raw)[:16] == DL.BASE_SHA16_DA_ORDEM, ("o um.py do Nos NAO e' o que a ordem da gerencia deu", sha(raw)[:16], DL.BASE_SHA16_DA_ORDEM)
rep = {"base_sha16": sha(raw)[:16], "selo_um_version": selo["um_version"], "arquivos": {}}
for f in ARQ:
    b = open(os.path.join(DL.NOS, f), "rb").read(); p = os.path.join(dst, f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v399 e DIFERE do Nos: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == b
    rep["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
pin_k = (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")
assert pin_k == rep["arquivos"]["tgl_kernel_proof_manifest.json"]["sha256"], "o manifesto do kernel copiado nao e' o que o selo pina"
rep["selo_pina_manifesto_do_kernel"] = pin_k
sc = json.load(open(os.path.join(dst, "um_absoluto_selo_acom.json"), encoding="utf-8"))
objs = {o["nome"]: o for o in sc["objetos"]}
assert sc["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and objs["um.py"]["sha256"] == sha(raw), "o sidecar da base nao e' o da v399 selada"
rep["sidecar_v399"] = {"veredito": sc["veredito"], "objetos": sorted(objs), "um_py_sha256": objs["um.py"]["sha256"]}
json.dump(rep, open(os.path.join(HERE, "BASE_V399_COPIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# a v398 -- a que a Bancada de producao ainda pina: so' o selo e o manifesto do kernel (copias de bytes da custodia da v399, base_v398), lidos e pinados
d8 = os.path.join(HERE, DL.BASE98_DIR); os.makedirs(d8, exist_ok=True)
rep8 = {"origem": DL.V399_BASE98, "arquivos": {}}
b98 = json.load(open(os.path.join(DL.V399, "BASE_V398_COPIA.json"), encoding="utf-8"))
for f in ("um_absoluto_selo.json", "tgl_kernel_proof_manifest.json"):
    b = open(os.path.join(DL.V399_BASE98, f), "rb").read(); p = os.path.join(d8, f)
    assert sha(b) == b98["arquivos"][f]["sha256"], ("a copia da v398 em v399\\base_v398 nao e' a que BASE_V398_COPIA.json registra", f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v398 e DIFERE: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    rep8["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
rep8["selo_v398_um_version"] = json.loads(open(os.path.join(d8, "um_absoluto_selo.json"), "rb").read())["um_version"]
assert rep8["selo_v398_um_version"] == "v398"
json.dump(rep8, open(os.path.join(HERE, "BASE_V398_COPIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"base_sha16": rep["base_sha16"], "selo": rep["selo_um_version"], "arquivos": {k: v["sha256"][:16] for k, v in rep["arquivos"].items()}, "base_v398": {k: v["sha256"][:16] for k, v in rep8["arquivos"].items()}}, ensure_ascii=False))
