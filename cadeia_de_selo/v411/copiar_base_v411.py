# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411] do molde copiar_base_v410.py: copia de bytes do Nos v410 SELADO para base_v410 (so' os rotulos sobem; o sha16 da base vem do delta, lido do DESENHO_v411)
"""copiar_base_v411.py -- copia de BYTES do Nos v410 SELADO para v411\\base_v410 (um.py, selo, core, manifesto do kernel, resultado do pilar e o SIDECAR um_absoluto_selo_acom.json).
A Bancada de producao JA pina a v410 (B19, lida do arquivo dela): nao ha salto de versoes. Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v410; o sha16 == o candidato_sha16 de
v410\\ESPERADOS_v410.json == o que o DESENHO_v411 da gerencia deu (delta_v411.BASE_SHA16_DA_ORDEM; o arquivo manda); o manifesto do kernel == o que o selo pina; o sidecar existe, e' o da v410 (esquema v399) e pina o um.py.
So' LE o Nos; escreve so' em v411\\base_v410. Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. Molde: copiar_base_v410.py.
uso: python -B -X utf8 copiar_base_v411.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
ARQ = ["um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json"]
dst = os.path.join(HERE, DL.BASE_DIR); os.makedirs(dst, exist_ok=True)
raw = open(os.path.join(DL.NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(DL.NOS, "um_absoluto_selo.json"), encoding="utf-8"))
esp = json.load(open(os.path.join(DL.V410, "ESPERADOS_v410.json"), encoding="utf-8"))
assert selo.get("um_version") == DL.BASE_VERSION, ("o selo do Nos nao e' a v410", selo.get("um_version"))
assert sha(raw) == selo["sha256"]["um.py"], "o um.py do Nos nao e' o que o selo pina"
assert sha(raw)[:16] == esp["candidato_sha16"], ("o um.py do Nos nao e' o candidato selado da v410 (ESPERADOS_v410)", sha(raw)[:16], esp["candidato_sha16"])
assert sha(raw)[:16] == DL.BASE_SHA16_DA_ORDEM, ("o um.py do Nos NAO e' o que o DESENHO_v411 deu", sha(raw)[:16], DL.BASE_SHA16_DA_ORDEM)
rep = {"base_sha16": sha(raw)[:16], "selo_um_version": selo["um_version"], "arquivos": {}}
for f in ARQ:
    b = open(os.path.join(DL.NOS, f), "rb").read(); p = os.path.join(dst, f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v410 e DIFERE do Nos: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == b
    rep["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
pin_k = (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")
assert pin_k == rep["arquivos"]["tgl_kernel_proof_manifest.json"]["sha256"], "o manifesto do kernel copiado nao e' o que o selo pina"
rep["selo_pina_manifesto_do_kernel"] = pin_k
sc = json.load(open(os.path.join(dst, "um_absoluto_selo_acom.json"), encoding="utf-8"))
objs = {o["nome"]: o for o in sc["objetos"]}
assert sc["veredito"].startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED") and objs["um.py"]["sha256"] == sha(raw), "o sidecar da base nao e' o da v410 selada"
rep["sidecar_v410"] = {"veredito": sc["veredito"], "objetos": sorted(objs), "um_py_sha256": objs["um.py"]["sha256"], "esquema": sc.get("esquema")}
p_ = os.path.join(HERE, "BASE_V410_COPIA.json")
open(p_ + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(p_ + ".tmp", p_)
print(json.dumps({"base_sha16": rep["base_sha16"], "selo": rep["selo_um_version"], "arquivos": {k: v["sha256"][:16] for k, v in rep["arquivos"].items()}}, ensure_ascii=False))
