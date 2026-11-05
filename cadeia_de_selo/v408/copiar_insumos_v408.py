# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026] as fontes da v408: as 4 pedras (embutida e fonte normalizada), as candidatas e os recibos/saidas de 04/11, o Dicionario superado, a afericao, o recibo dos nomes, o acervo PURGADO e o recibo da purga, o DESENHO, o BUNDLE, o KH, o congelado; as 12 falas de 04/11 (nas duas de autor misto, o arquivo inteiro E o paragrafo do operador)
"""copiar_insumos_v408.py -- copia de BYTES, para a pasta DURAVEL v408\\insumos, das fontes que os registros da v408 pinam por sha256: as 4 pedras normalizadas EMBUTIDAS (v408\\pedra -> insumos\\<Nome>_embutida.lean), as fontes normalizadas com #print axioms (ja' em insumos\\<Nome>.lean),
as candidatas de origem de work\\pedras_candidatas_04nov e os recibos/saidas do lean de 04/11, o Dicionario.lean superado (registro), a afericao no kernel, o recibo dos nomes, o acervo PURGADO e o recibo da purga (E23), o DESENHO_v408.md, o BUNDLE_v408.json, a medida do Audit (KH_N1_v408.json),
o VERBATIM_CONGELADO_v408.json e TODAS as falas do operador de 04/11/2026 (nas duas de autor misto: o arquivo inteiro, por sha256, E o paragrafo do operador, que e' o texto que o um.py embute).
Grava MANIFESTO_INSUMOS_v408.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. Roda DEPOIS do pos_build_kernel_v408.py (que gera kernel\\KH_N1_v408.json). Molde: copiar_insumos_v407.py.
uso: python -I -B -X utf8 copiar_insumos_v408.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v408 as DL  # noqa: E402
import registros_v408 as RG  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
os.makedirs(CUN, exist_ok=True)
man = {}


def grava(destino, b, origem):
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem, "sha256": sha(b), "bytes": len(b)}


def copia(destino, origem):
    return grava(destino, open(origem, "rb").read(), origem)


# a pedra que carrega a ancora principal: a fonte tem o sha16 do recibo dos nomes; a copia v408\pedra == o bundle == o sandbox
tf = DL.testemunha_fonte()
for p in DL.PEDRAS_V408:
    b = open(p["src"], "rb").read()
    assert sha(b) == DL.BUNDLE_POR_REL[p["rel"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *p["rel"].split("/")), "rb").read()), ("a pedra em v408\\pedra difere do bundle ou do sandbox", p["name"])
    assert sha(open(p["origem"], "rb").read()) == p["sha256_origem"], ("a fonte normalizada em insumos\\ difere do que o bundle pinou", p["name"])
for nome, orig in RG.ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
assert man["TetelestaiTerminal.lean"]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] == tf["sha256_origem"][:16]
assert man["PSION_NO_ACERVO_04nov_purgado.md"]["sha256"] == DL.PURGADO_SHA256 and not man["PSION_NO_ACERVO_04nov_purgado.md"]["sha256"].startswith(DL.ORIGEM_PURGA_SHA16_DA_ORDEM)
for p in DL.PEDRAS_V408:
    assert man["%s_embutida.lean" % p["name"]]["sha256"] == DL.BUNDLE_POR_REL[p["rel"]]["sha256"]
for v in DL.verbatins408(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins408
    if v["autor"] == DL.AUTOR_MISTO:
        man["cunhagens/" + os.path.basename(v["arquivo_inteiro"])] = copia(v["arquivo_inteiro"], v["fonte_original"])
        assert man["cunhagens/" + os.path.basename(v["arquivo_inteiro"])]["sha256"] == v["sha256_arquivo_inteiro"]
        man["cunhagens/" + os.path.basename(v["arquivo"])] = grava(v["arquivo"], v["text"].encode("utf-8"), v["fonte_original"] + " (so' o paragrafo do operador, antes do corte «%s»)" % v["corte"])
    else:
        man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v408.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B | TetelestaiTerminal (fonte):", tf["sha256_origem"][:16], "| purgado:", DL.PURGADO_SHA256[:16])
