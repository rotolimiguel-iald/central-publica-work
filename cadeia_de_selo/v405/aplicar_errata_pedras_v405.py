# -*- coding: utf-8 -*-
"""aplicar_errata_pedras_v405.py -- abre caminho para a ERRATA DAS PEDRAS da gerencia (RECIBO_ERRATA_PEDRAS_01nov.json, 13:28 de 01/11/2026): os copiadores da cadeia NAO sobrescrevem o que difere (abortam, de proposito), entao as copias derivadas da fonte ANTERIOR saem do caminho
ANTES de regenerar o pino. Nada e' apagado: pedras_sha16_da_ordem.json e PINO_DAS_PEDRAS_DETALHE_v405.json ganham backup de BYTES (.bak_<ts>) e sao removidos do lugar; as copias v405\\pedra\\*.lean e as copias duraveis insumos\\*.lean, insumos\\KH_N1_v405.json e MANIFESTO_INSUMOS_v405.json
vao para antes_da_errata_<ts>\\ (os bytes da primeira construcao, 13:04, ficam como registro). Le o Nos: NADA. Toca so' esta pasta. Grava RECIBO_APLICACAO_ERRATA_<ts>.json. Reexecutavel: o que nao existe e' pulado.
uso: python -I -B -X utf8 aplicar_errata_pedras_v405.py"""
import datetime, glob, hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ARQ = os.path.join(HERE, "antes_da_errata_" + TS)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rec = {"ato": "abre caminho para a errata das pedras (copias derivadas guardadas, nada apagado)", "quando": TS, "movidos": [], "backups": []}
for nome in ("pedras_sha16_da_ordem.json", "PINO_DAS_PEDRAS_DETALHE_v405.json"):
    p = os.path.join(HERE, nome)
    if os.path.exists(p):
        b = open(p, "rb").read(); bak = p + ".bak_" + TS
        open(bak, "wb").write(b); assert open(bak, "rb").read() == b
        rec["backups"].append({"arquivo": nome, "backup": os.path.basename(bak), "sha256": sha(bak), "bytes": len(b)})
        os.remove(p)


def mover(p, sub):
    if not os.path.exists(p):
        return
    d = os.path.join(ARQ, sub); os.makedirs(d, exist_ok=True)
    h = sha(p); alvo = os.path.join(d, os.path.basename(p)); shutil.move(p, alvo)
    assert sha(alvo) == h
    rec["movidos"].append({"de": os.path.relpath(p, HERE), "para": os.path.relpath(alvo, HERE), "sha256": h})


for p in sorted(glob.glob(os.path.join(HERE, "pedra", "*.lean"))):
    mover(p, "pedra")
for p in sorted(glob.glob(os.path.join(HERE, "insumos", "*.lean"))):
    mover(p, "insumos")
mover(os.path.join(HERE, "insumos", "KH_N1_v405.json"), "insumos")
mover(os.path.join(HERE, "MANIFESTO_INSUMOS_v405.json"), ".")
mover(os.path.join(HERE, "PEDRAS_COPIA_v405.json"), ".")
json.dump(rec, open(os.path.join(HERE, "RECIBO_APLICACAO_ERRATA_%s.json" % TS), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("movidos", len(rec["movidos"]), "| backups", len(rec["backups"]), "| guardados em", os.path.basename(ARQ))
