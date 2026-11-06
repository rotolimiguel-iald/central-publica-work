# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] as fontes da v409: a pedra (embutida e fonte normalizada), a saida do lean, a candidata R8 e o recibo R8, o BUNDLE, o KH; as 10 falas de 05/11 (de duas, o trecho que fica e o arquivo inteiro so' por sha256); congela a lista das falas
"""copiar_insumos_v409.py -- copia de BYTES, para a pasta DURAVEL v409\\insumos, das fontes que os registros da v409 pinam por sha256: a pedra normalizada EMBUTIDA (v409\\pedra -> insumos\\TraducaoTuring_embutida.lean), a fonte normalizada com #print axioms
(ja' em insumos\\TraducaoTuring.lean), a saida do lean, a candidata de origem (work\\pedras_candidatas_05nov\\TraducaoTuringR8.lean) e o recibo dela, o BUNDLE_v409.json, a medida do Audit (KH_N1_v409.json) e as falas do operador de 05/11/2026
(nas duas da D59, so' o TRECHO QUE FICA e' copiado, com nome neutro quando o nome de origem resume a parte que fica fora; o arquivo inteiro entra so' por sha256 e NAO e' copiado para insumos\\, que a custodia publica).
CONGELA a lista das falas (VERBATIM_CONGELADO_v409.json; lista de trabalho da cadeia, nao pinada como fonte: traz os caminhos de origem). Grava MANIFESTO_INSUMOS_v409.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta.
Roda DEPOIS do pos_build_kernel_v409.py (que gera kernel\\KH_N1_v409.json). Molde: copiar_insumos_v408.py.
uso: python -I -B -X utf8 copiar_insumos_v409.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
# a lista das falas: congelada na PRIMEIRA execucao (as dez do DESENHO_v409 §3); depois, lida (fala que chegar depois fica fora, dita em fora_do_desenho)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v409.json")
if not os.path.exists(CONG):
    arqs = list(DL.VERBATIM_ORIGEM_V409)
    reg = [{"arquivo": p_, "sha256": sha(open(p_, "rb").read()), "bytes": os.path.getsize(p_), "autor": "operador"} for p_ in arqs]
    c = {"contrato": "VERBATIM_CONGELADO_v409", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(arqs), "arquivos": arqs, "registro": reg, "fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V409),
         "nota": "as doze falas de 05/11/2026 que esta versao embute (as dez do DESENHO_v409 §3 e as duas dos AO LADO do fim dele); de tres, so' o trecho e' embutido e citado (duas pela D59; uma porque o resto e' aviso operacional); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)"}
    b = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
    open(CONG + ".tmp", "wb").write(b); assert os.path.getsize(CONG + ".tmp") == len(b); os.replace(CONG + ".tmp", CONG)
    print("VERBATIM_CONGELADO_v409.json: %d falas congeladas" % len(arqs))
import importlib  # noqa: E402
DL = importlib.reload(DL)                                       # (relido com a lista congelada)
import registros_v409 as RG  # noqa: E402
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


# a pedra que carrega a ancora principal: a fonte tem o sha16 do recibo dos nomes; a copia v409\pedra == o bundle == o sandbox
tf = DL.testemunha_fonte()
for p in DL.PEDRAS_V409:
    b = open(p["src"], "rb").read()
    assert sha(b) == DL.BUNDLE_POR_REL[p["rel"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *p["rel"].split("/")), "rb").read()), ("a pedra em v409\\pedra difere do bundle ou do sandbox", p["name"])
    assert sha(open(p["origem"], "rb").read()) == p["sha256_origem"], ("a fonte normalizada em insumos\\ difere do que o bundle pinou", p["name"])
for nome, orig in RG.ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
assert man["TraducaoTuring.lean"]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"] == tf["sha256_origem"][:16]
for p in DL.PEDRAS_V409:
    assert man["%s_embutida.lean" % p["name"]]["sha256"] == DL.BUNDLE_POR_REL[p["rel"]]["sha256"]
for v in DL.verbatins409(CUN):   # os prefixos de sha256 da ORDEM da gerencia (as falas-chave) sao conferidos dentro de DL.verbatins409
    if v.get("so_o_trecho"):
        assert sha(open(v["fonte_original"], "rb").read()) == v["sha256_arquivo_inteiro"]
        man["cunhagens/" + os.path.basename(v["arquivo"])] = grava(v["arquivo"], v["text"].encode("utf-8"), "%s (sha256 do arquivo inteiro %s; %s)" % (v["nome_publico"], v["sha256_arquivo_inteiro"], v["so_o_trecho"]))
    else:
        man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
# D59: nada copiado para insumos\ traz a parte que fica fora (nem o nome do arquivo de origem que a resume)
for n_ in os.listdir(CUN):
    assert "milenio" not in n_.lower() and "kimi" not in n_.lower(), ("D59: nome de arquivo em insumos\\cunhagens resume a parte que fica fora", n_)
b_man = json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8")
open(os.path.join(HERE, "MANIFESTO_INSUMOS_v409.json.tmp"), "wb").write(b_man)
os.replace(os.path.join(HERE, "MANIFESTO_INSUMOS_v409.json.tmp"), os.path.join(HERE, "MANIFESTO_INSUMOS_v409.json"))
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B | TraducaoTuring (fonte):", tf["sha256_origem"][:16])
