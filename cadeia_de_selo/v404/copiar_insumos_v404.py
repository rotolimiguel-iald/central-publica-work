# -*- coding: utf-8 -*-
"""copiar_insumos_v404.py -- copia de BYTES, para a pasta DURAVEL v404\\insumos, das fontes que os registros da v404 pinam por sha256: as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32), a medida do Audit (KH_N1_v404.json), o levantamento «a transicao para a massa» (28/10/2026, fonte
do registro cunhagens_v404) e as NOVE falas de 28/10/2026 (todas do operador; insumos\\cunhagens\\<sha16>_<nome>). (Nao ha insumo de adendo nesta versao: o ADENDO de 03-04/09 e' da v402.)
Grava MANIFESTO_INSUMOS_v404.json (sha256, origem). As fontes do ACOM (selo pela propria tecnologia) seguem em v399\\insumos (o um.py v403 selado as pina por esse caminho). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v404.py (que gera kernel\\KH_N1_v404.json). uso: python -I -B -X utf8 copiar_insumos_v404.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
for d in (CUN,):
    os.makedirs(d, exist_ok=True)
ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v404.json")), (os.path.basename(DL.LEVANTAMENTO_ARQ), DL.LEVANTAMENTO_ARQ)]
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
# a pedra duravel == a do sandbox (o sandbox e' conferido por preparar_kernel_v404.py conferir) == a fonte da ordem
for s in DL.STONES:
    assert man[s["insumo"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *s["rel"].split("/")), "rb").read()) == sha(open(s["origem"], "rb").read()), "a pedra duravel difere da do sandbox ou da fonte da ordem: " + s["name"]
    assert man[s["insumo"]]["sha256"][:16] == s["sha16_da_ordem"]
for v in DL.verbatins404(CUN):   # os prefixos de sha256 da ORDEM da gerencia sao conferidos dentro de DL.verbatins404
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B")
