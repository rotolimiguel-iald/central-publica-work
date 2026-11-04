# -*- coding: utf-8 -*-
"""copiar_insumos_v407.py -- copia de BYTES, para a pasta DURAVEL v407\\insumos, das fontes que os registros da v407 pinam por sha256: as 9 pedras normalizadas (v407\\pedra), as fontes de origem da PsionCanto e do Par (R1), os recibos e as saidas do lean de 03/11,
o levantamento do acervo, a revisao do Sonnet de 02/11 (tres pedras), o plano e o desenho da v407, o BUNDLE_v407.json, a medida do Audit (KH_N1_v407.json), o manifesto da parametrizacao do teste (d), o resultado da Fase 9 V2 (a regra do 4,44) e TODAS as falas do operador de 03/11/2026.
Grava MANIFESTO_INSUMOS_v407.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. Roda DEPOIS do pos_build_kernel_v407.py (que gera kernel\\KH_N1_v407.json). Molde: copiar_insumos_v406.py.
uso: python -I -B -X utf8 copiar_insumos_v407.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v407 as DL  # noqa: E402
import registros_v407 as RG  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
os.makedirs(CUN, exist_ok=True)
man = {}


def copia(destino, origem):
    b = open(origem, "rb").read()
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem, "sha256": sha(b), "bytes": len(b)}


# a pedra que carrega a chave: a fonte de origem tem o sha16 da ordem; a copia v407\pedra == o bundle == o sandbox
tf = DL.testemunha_fonte()
for p in DL.PEDRAS_V407:
    b = open(p["src"], "rb").read()
    assert sha(b) == DL.BUNDLE_POR_REL[p["rel"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *p["rel"].split("/")), "rb").read()), ("a pedra em v407\\pedra difere do bundle ou do sandbox", p["name"])
for nome, orig in RG.ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
assert man["PsionCantoR1.lean"]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] == tf["sha256_origem"][:16]
assert man["RESULTADO_FASE9_V2_C1_20261023_122926.json"]["sha256"][:16] == DL.FASE9_V2_SHA16_DA_ORDEM
assert man["MANIFESTO_PARAMETRIZACAO_03nov.json"]["sha256"][:16] == DL.D_TESTE_SHA16_DA_ORDEM
for v in DL.verbatins407(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins407
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v407.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B | PsionCanto (origem):", tf["sha256_origem"][:16])
