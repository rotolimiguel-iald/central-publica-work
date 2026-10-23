# -*- coding: utf-8 -*-
"""copiar_insumos_v397.py -- copia de BYTES, para a pasta DURAVEL v397\\insumos, das fontes que os registros da v397 pinam por sha256: a pedra Token, a medida do Audit (KH_N1), os QUATRO arquivos do Teste da Unica Palavra
(o resultado e os tres recibos, de work\\fase9_v2_c1_23out, que fica SO' LEITURA) em insumos\\fase9\\, e as QUATRO falas do operador de 23/10 (insumos\\cunhagens\\<sha16>_<nome>); grava MANIFESTO_INSUMOS_v397.json
(sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve). Roda DEPOIS do pos_build_kernel_v397.py (que gera kernel\\KH_N1_v397.json).
Molde: copiar_insumos_v396.py.  uso: python -I -B -X utf8 copiar_insumos_v397.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens"); F9D = os.path.join(INS, "fase9")
os.makedirs(CUN, exist_ok=True); os.makedirs(F9D, exist_ok=True)
ORIGENS = [(DL.STONE_INSUMO, DL.STONE_SRC), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v397.json"))]
man = {}


def copia(destino, origem):
    b = open(origem, "rb").read()
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem, "sha256": sha(b), "bytes": len(b)}


for nome, orig in ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
# a pedra duravel == a embutida/sandbox (o sandbox e' conferido por preparar_kernel_v397.py conferir)
assert man[DL.STONE_INSUMO]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *DL.STONE_REL.split("/")), "rb").read()), "a pedra duravel difere da do sandbox"
for f in DL.f9_fontes(F9D):   # o sha256 do resultado e' conferido contra o da ORDEM da gerencia dentro de f9_fontes
    man["fase9/" + os.path.basename(f["arquivo"])] = copia(f["arquivo"], f["origem"])
    assert man["fase9/" + os.path.basename(f["arquivo"])]["sha256"] == f["sha256"]
for v in DL.verbatins(CUN):
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha256"][:16] for k, v in man.items()}, ensure_ascii=False, indent=1))
