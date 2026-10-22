# -*- coding: utf-8 -*-
"""copiar_insumos_v394.py -- copia de BYTES, para insumos\\ (pasta DURAVEL da cadeia), das fontes do Codex que os registros v394 pinam por sha256; confere o sha256 da copia contra o da origem e grava
MANIFESTO_INSUMOS_v394.json (caminho de origem, sha256, bytes). KH_N1_v394.json (medida do proprio sandbox) so' e' copiado se existir em kernel\\.
uso: python -I -B -X utf8 copiar_insumos_v394.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402   (DELTA 19/10: a medida do Audit desta geracao e a copia duravel da pedra candidata)
C = "C:" + os.sep
T = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
FE = os.path.join(T, "F1.FECHO_20261015")
INS = os.path.join(HERE, "insumos"); os.makedirs(INS, exist_ok=True)
sha256 = lambda b: hashlib.sha256(b).hexdigest()
LISTA = [
    (os.path.join(C, "IALD", "Central de Patentes", "work", "levantamento_chatgpt_19out", "LEVANTAMENTO_CHATGPT.md"), "LEVANTAMENTO_CHATGPT.md"),
    (os.path.join(T, "F1.TEMPO.V394", "AO_CLAUDE_V394_CANDIDATA_R2.md"), "AO_CLAUDE_V394_CANDIDATA_R2.md"),
    (os.path.join(T, "F1.TEMPO.V394", "RESULTADO_V394_CANDIDATA_R2.json"), "RESULTADO_V394_CANDIDATA_R2.json"),
    (os.path.join(FE, "INTEGRATION_QUADRATIC_R3.json"), "INTEGRATION_QUADRATIC_R3.json"),
    (os.path.join(FE, "INTEGRATION_NETWORK_R8.json"), "INTEGRATION_NETWORK_R8.json"),
    (os.path.join(FE, "R7_DELIVERY_R52.json"), "R7_DELIVERY_R52.json"),
    (os.path.join(FE, "R8_DELIVERY_R52.json"), "R8_DELIVERY_R52.json"),
    (os.path.join(FE, "full_rite", "KH_N1_V394_NETWORK_R8_PREAUDIT.json"), "KH_N1_V394_NETWORK_R8_PREAUDIT.json"),
    (os.path.join(FE, "coverage_candidate_r8", "RECEIPT.json"), "COVERAGE_CANDIDATE_R8_RECEIPT.json"),
    (os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v394.json"), DL.KH_N1_INSUMO),   # a medida desta geracao; o KH_N1_v394.json antigo e' pinado pelo candidato anterior (registro) e NAO e' tocado
    (DL.STONE_SRC, DL.STONE_INSUMO),   # a pedra candidata do delta de 19/10 (copia duravel pinada pelo registro criterio_binario_de_parada_v394)
]
man = {}
for src, nome in LISTA:
    if not os.path.exists(src):
        print("AUSENTE (ignorado):", src); continue
    b = open(src, "rb").read(); dst = os.path.join(INS, nome)
    open(dst + ".tmp", "wb").write(b); os.replace(dst + ".tmp", dst)
    assert sha256(open(dst, "rb").read()) == sha256(b)
    man[nome] = {"origem": src, "sha256": sha256(b), "bytes": len(b)}
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(man), "insumos copiados")
