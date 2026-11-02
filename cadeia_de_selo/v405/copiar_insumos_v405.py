# -*- coding: utf-8 -*-
"""copiar_insumos_v405.py -- copia de BYTES, para a pasta DURAVEL v405\\insumos, das fontes que os registros da v405 pinam por sha256: as OITO pedras, a medida do Audit (KH_N1_v405.json), os tres recibos da gerencia (nomeacao de 01/11, Identidade de 01/11, ObservadorTerminal r2 de 31/10), a conferencia da cadeia E0 (31/10),
o TEXTO da secao «A identidade» do artigo (GERADO aqui a partir da revisao r2 ratificada: a secao «## O texto (r2)» com as marcas retiradas; o sha256 e' do texto gerado, e o .md de origem e o original como recebido ficam pinados ao lado) e TODAS as falas do operador de 30/10 a 01/11 mais o ensaio original (insumos\\cunhagens\\<sha16>_<nome>).
Grava MANIFESTO_INSUMOS_v405.json (sha256, origem). As fontes do ACOM (selo pela propria tecnologia) seguem em v399\\insumos (o um.py v404 selado as pina por esse caminho). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v405.py (que gera kernel\\KH_N1_v405.json). uso: python -I -B -X utf8 copiar_insumos_v405.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v405 as DL  # noqa: E402
import registros_v405 as RG  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
for d in (CUN,):
    os.makedirs(d, exist_ok=True)
ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v405.json")),
                                                           (os.path.basename(RG.RECIBO_NOMEACAO_ARQ), RG.RECIBO_NOMEACAO_ARQ), (os.path.basename(RG.RECIBO_ERRATA_ARQ), RG.RECIBO_ERRATA_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R2_ARQ), RG.RECIBO_ERRATA_R2_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R3_ARQ), RG.RECIBO_ERRATA_R3_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R4_ARQ), RG.RECIBO_ERRATA_R4_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R5_ARQ), RG.RECIBO_ERRATA_R5_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R6_ARQ), RG.RECIBO_ERRATA_R6_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R7_ARQ), RG.RECIBO_ERRATA_R7_ARQ), (os.path.basename(DL.ACORDE_KIMI_ARQ), DL.ACORDE_KIMI_ARQ), (os.path.basename(DL.HALF_NAT_ARQ), DL.HALF_NAT_ARQ), (os.path.basename(DL.GA_RECLASS_ARQ), DL.GA_RECLASS_ARQ), (os.path.basename(DL.GA_MEDIDA_ARQ), DL.GA_MEDIDA_ARQ), (os.path.basename(DL.GA_PARECER_ARQ), DL.GA_PARECER_ARQ), (os.path.basename(RG.ENSAIO_EN_ARQ), RG.ENSAIO_EN_ARQ), (os.path.basename(RG.RECIBO_IDENTIDADE_ARQ), RG.RECIBO_IDENTIDADE_ARQ), (os.path.basename(RG.RECIBO_OBSERVADOR_ARQ), RG.RECIBO_OBSERVADOR_ARQ),
                                                           (os.path.basename(RG.CONFERENCIA_E0_ARQ), RG.CONFERENCIA_E0_ARQ), (os.path.basename(DL._ENSAIO_R2_MD), DL._ENSAIO_R2_MD)]
man = {}


def copia(destino, origem=None, dados=None):
    b = open(origem, "rb").read() if dados is None else dados
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem or "(gerado por copiar_insumos_v405.py a partir de %s)" % DL._ENSAIO_R2_MD, "sha256": sha(b), "bytes": len(b)}


for nome, orig in ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
# o TEXTO da secao do artigo: extraido do .md da revisao r2 (gerencia c1, ratificada pelo operador), marcas retiradas; pinado pelo sha256 do texto; a origem (.md) e o original como recebido ficam pinados ao lado
E = DL.ensaio_identidade_r2()
man[RG.ENSAIO_R2_INSUMO] = copia(os.path.join(INS, RG.ENSAIO_R2_INSUMO), dados=E["texto"].encode("utf-8"))
man[RG.ENSAIO_R2_INSUMO].update({"gerado_de": {"md": DL._ENSAIO_R2_MD, "md_sha256": E["sha256_do_md"]}, "original_como_recebido": {"arquivo": E["original_arquivo"], "sha256": E["original_sha256"]}, "primeira_linha": E["primeira_linha"], "ultima_linha": E["ultima_linha"]})
assert man[os.path.basename(DL._ENSAIO_R2_MD)]["sha256"] == E["sha256_do_md"]
# a pedra duravel == a do sandbox (o sandbox e' conferido por preparar_kernel_v405.py conferir) == a fonte da ordem
for s in DL.STONES:
    assert man[s["insumo"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *s["rel"].split("/")), "rb").read()) == sha(open(s["origem"], "rb").read()), "a pedra duravel difere da do sandbox ou da fonte da ordem: " + s["name"]
    assert man[s["insumo"]]["sha256"][:16] == s["sha16_da_ordem"]
for v in DL.verbatins405(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins405
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B", "| ensaio r2:", man[RG.ENSAIO_R2_INSUMO]["sha256"][:16], man[RG.ENSAIO_R2_INSUMO]["bytes"], "B")
