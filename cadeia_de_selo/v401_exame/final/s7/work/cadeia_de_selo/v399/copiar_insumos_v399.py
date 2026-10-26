# -*- coding: utf-8 -*-
"""copiar_insumos_v399.py -- copia de BYTES, para a pasta DURAVEL v399\\insumos, das fontes que os registros da v399 pinam por sha256: a pedra (Testemunho), a medida do Audit (KH_N1), as QUATRO inscricoes de 24/10/2026
(todas falas do operador; insumos\\cunhagens\\<sha16>_<nome>), os arquivos do ESTUDO do selo pela propria tecnologia (insumos\\acom: a secao colavel, os trechos, o patch proposto, o manifesto do bloco embutido, o prototipo e o
resultado do estudo) e as SEIS fontes do operador que o bloco embutido cita (insumos\\acom\\fontes_operador: acom_mirror.py, acom_crypto.py, tgl_core.py, run_tests.py, o legado torch e o .tex da patente; so' leitura da origem);
grava MANIFESTO_INSUMOS_v399.json (sha256, origem). O Teste da Unica Palavra (o resultado e os tres recibos) NAO e' copiado de novo: os insumos duraveis dele moram em v397\\insumos\\fase9 (o um.py selado ja' os pina por esse caminho).
Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve). Roda DEPOIS do pos_build_kernel_v399.py (que gera kernel\\KH_N1_v399.json). Molde: copiar_insumos_v398.py.
uso: python -I -B -X utf8 copiar_insumos_v399.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v399 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens"); ACOM = os.path.join(INS, "acom"); FOP = os.path.join(ACOM, "fontes_operador")
for d in (CUN, ACOM, FOP):
    os.makedirs(d, exist_ok=True)
ORIGENS = [(s["insumo"], s["src"]) for s in DL.STONES] + [(DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v399.json"))]
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
# a pedra duravel == a do sandbox (o sandbox e' conferido por preparar_kernel_v399.py conferir) == a fonte aprovada
for s in DL.STONES:
    assert man[s["insumo"]]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *s["rel"].split("/")), "rb").read()) == sha(open(s["origem"], "rb").read()), "a pedra duravel difere da do sandbox ou da fonte aprovada: " + s["name"]
    assert man[s["insumo"]]["sha256"][:16] == s["sha16_da_ordem"]
for v in DL.verbatins(CUN):   # os prefixos de sha256 da ORDEM da gerencia sao conferidos dentro de DL.verbatins
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
# o ESTUDO do selo pela propria tecnologia (aprovado em revisao independente): o sha16 que a revisao leu e' conferido contra o arquivo (o arquivo manda e a divergencia ABORTA)
for nome, (orig, pino16) in DL.ACOM_ESTUDO.items():
    m = copia(os.path.join(ACOM, nome), orig)
    if pino16:
        assert m["sha256"][:16] == pino16, ("o arquivo do estudo NAO e' o que a revisao independente leu", nome, m["sha256"][:16], pino16)
    man["acom/" + nome] = m
# as seis fontes do operador (so' leitura da origem); o sha256 de cada uma e' conferido contra o EMBUTIDO_MANIFESTO.json do estudo
emb = json.load(open(os.path.join(ACOM, "EMBUTIDO_MANIFESTO.json"), encoding="utf-8"))
for nome, orig in DL.ACOM_FONTES_OPERADOR.items():
    m = copia(os.path.join(FOP, nome), orig)
    ch = DL.ACOM_CHAVE_DO_MANIFESTO[nome]
    assert m["sha256"] == emb["fontes"][ch]["sha256"], ("a fonte do operador mudou desde o estudo (EMBUTIDO_MANIFESTO)", nome, m["sha256"][:16], emb["fontes"][ch]["sha256"][:16])
    man["acom/fontes_operador/" + nome] = m
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v399.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha256"][:16] for k, v in man.items()}, ensure_ascii=False, indent=1))
