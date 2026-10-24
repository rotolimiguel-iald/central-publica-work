# -*- coding: utf-8 -*-
"""copiar_insumos_v398.py -- copia de BYTES, para a pasta DURAVEL v398\\insumos, das fontes que os registros da v398 pinam por sha256: as DUAS pedras (Sonico e AfinacaoDasCordas), a medida do Audit (KH_N1) e as SEIS inscricoes de 23/10/2026
(cinco falas do operador e a leitura da gerencia que ele ratificou, esta rotulada como da gerencia; insumos\\cunhagens\\<sha16>_<nome>); grava MANIFESTO_INSUMOS_v398.json (sha256, origem). O Teste da Unica Palavra (o resultado e os tres recibos)
NAO e' copiado de novo: os insumos duraveis dele moram em v397\\insumos\\fase9 (o um.py v397 selado ja' os pina por esse caminho) e a pasta fase9_v2_c1_23out fica SO' LEITURA. Reexecutavel: o que ja existe e e' igual fica; o que difere aborta
(nao sobrescreve). Roda DEPOIS do pos_build_kernel_v398.py (que gera kernel\\KH_N1_v398.json). Molde: copiar_insumos_v397.py.  uso: python -I -B -X utf8 copiar_insumos_v398.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
os.makedirs(CUN, exist_ok=True)
ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v398.json"))]
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
# cada pedra duravel == a do sandbox (o sandbox e' conferido por preparar_kernel_v398.py conferir) == a fonte aprovada
for s in DL.STONES:
    assert man[s["insumo"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *s["rel"].split("/")), "rb").read()) == sha(open(s["origem"], "rb").read()), "a pedra duravel difere da do sandbox ou da fonte aprovada: " + s["name"]
    assert man[s["insumo"]]["sha256"][:16] == s["sha16_da_ordem"]
for v in DL.verbatins(CUN):   # os prefixos de sha256 da ORDEM da gerencia sao conferidos dentro de DL.verbatins
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha256"][:16] for k, v in man.items()}, ensure_ascii=False, indent=1))
