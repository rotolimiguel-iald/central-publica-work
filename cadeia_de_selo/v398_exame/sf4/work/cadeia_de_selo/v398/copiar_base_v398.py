# -*- coding: utf-8 -*-
"""copiar_base_v398.py -- copia de BYTES do Nos v397 SELADO para v398\\base_v397 (um.py, selo, core, manifesto do kernel, resultado do pilar), com a conferencia por script:
o sha256 do um.py == o que o SELO pina; o selo diz v397; o sha16 == o candidato_sha16 de v397\\ESPERADOS_v397.json (lido do arquivo, nunca digitado) == o que a ordem da gerencia deu (388cc3742323421c; o arquivo manda).
So' LE o Nos; escreve so' em v398\\base_v397. Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve em silencio). Molde: copiar_base_v397.py.
uso: python -I -B -X utf8 copiar_base_v398.py"""
import hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
ARQ = ["um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json"]
dst = os.path.join(HERE, DL.BASE_DIR); os.makedirs(dst, exist_ok=True)
raw = open(os.path.join(DL.NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(DL.NOS, "um_absoluto_selo.json"), encoding="utf-8"))
esp = json.load(open(os.path.join(DL.V397, "ESPERADOS_v397.json"), encoding="utf-8"))
assert selo.get("um_version") == DL.BASE_VERSION, ("o selo do Nos nao e' a v397", selo.get("um_version"))
assert sha(raw) == selo["sha256"]["um.py"], "o um.py do Nos nao e' o que o selo pina"
assert sha(raw)[:16] == esp["candidato_sha16"], ("o um.py do Nos nao e' o candidato selado da v397 (ESPERADOS_v397)", sha(raw)[:16], esp["candidato_sha16"])
assert sha(raw)[:16] == DL.BASE_SHA16_DA_ORDEM, ("o um.py do Nos NAO e' o que a ordem da gerencia deu", sha(raw)[:16], DL.BASE_SHA16_DA_ORDEM)
rep = {"base_sha16": sha(raw)[:16], "selo_um_version": selo["um_version"], "arquivos": {}}
for f in ARQ:
    b = open(os.path.join(DL.NOS, f), "rb").read(); p = os.path.join(dst, f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v397 e DIFERE do Nos: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == b
    rep["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
# o manifesto do kernel e o resultado do pilar sao os que o selo pina (so' registra; nao gateia se o selo nao os traz)
rep["selo_pina_manifesto_do_kernel"] = (selo.get("kernel_manifest_sha256") or (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json"))
json.dump(rep, open(os.path.join(HERE, "BASE_V397_COPIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"base_sha16": rep["base_sha16"], "selo": rep["selo_um_version"], "arquivos": {k: v["sha256"][:16] for k, v in rep["arquivos"].items()}}, ensure_ascii=False))
