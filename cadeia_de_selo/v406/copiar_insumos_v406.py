# -*- coding: utf-8 -*-
"""copiar_insumos_v406.py -- copia de BYTES, para a pasta DURAVEL v406\\insumos, das fontes que os registros da v406 pinam por sha256: a candidata CanonicalFullTGLWitnessR1, a medida do Audit (KH_N1_v406.json), a ratificacao R10, a revisao do Sonnet, o desenho, a ordem logica,
o levantamento, o BUNDLE_v406.json, o MANIFEST e os SUMMARY da integracao R3, o CHECK_axioms, o driver da integracao, o recibo e os axiomas da bancada do ChatGPT (so' leitura), o parecer R52/R7, a saida do lean da candidata, o resultado da Fase 9 V2 (a regra do 4,44) e TODAS as falas do operador de 02/11/2026.
Grava MANIFESTO_INSUMOS_v406.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. Roda DEPOIS do pos_build_kernel_v406.py (que gera kernel\\KH_N1_v406.json). uso: python -I -B -X utf8 copiar_insumos_v406.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v406 as DL  # noqa: E402
import registros_v406 as RG  # noqa: E402
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


# a candidata: a copia v406\pedra tem de ser a origem (fechamento_02nov) e a do sandbox
tf = DL.testemunha_fonte()
if not os.path.exists(DL.TESTEMUNHA["src"]):
    os.makedirs(os.path.dirname(DL.TESTEMUNHA["src"]), exist_ok=True); copia(DL.TESTEMUNHA["src"], DL.TESTEMUNHA["origem"])
assert sha(open(DL.TESTEMUNHA["src"], "rb").read()) == tf["sha256"] == sha(open(os.path.join(DL.SANDBOX, *DL.MODULO_TESTEMUNHA.split("/")), "rb").read())
for nome, orig in RG.ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
assert man[DL.TESTEMUNHA["insumo"]]["sha256"] == tf["sha256"] and man[DL.TESTEMUNHA["insumo"]]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
assert man["RESULTADO_FASE9_V2_C1_20261023_122926.json"]["sha256"][:16] == DL.FASE9_V2_SHA16_DA_ORDEM
for v in DL.verbatins406(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins406
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v406.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B | candidata:", tf["sha256"][:16])
