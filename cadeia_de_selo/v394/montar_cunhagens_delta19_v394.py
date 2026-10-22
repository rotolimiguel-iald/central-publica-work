# -*- coding: utf-8 -*-
"""montar_cunhagens_delta19_v394.py -- DELTA 19/10: acrescenta ao cunhagens_v394_dados.json as DUAS falas do operador de 19/10/2026 (o criterio binario de parada e o «flutuar no ponto fixo»), na ordem do arquivo, SEM regerar as 46 anteriores
(montar_cunhagens_v394.py ficou como esta': ele relê a memoria da gerencia, que pode ter mudado). Copia de BYTES para insumos\\cunhagens (<sha16>_<nome>), sha256 conferido contra o arquivo de origem e contra o sha pinado
no delta19_v394 (os arquivos de origem sao os de work\\cunhagens_13out; o texto de cada fala e' o do arquivo, nunca digitado). Idempotente: re-executar nao duplica. Backup de bytes do JSON antes de escrever.
uso: python -I -B -X utf8 montar_cunhagens_delta19_v394.py"""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402
OUTD = os.path.join(HERE, "insumos", "cunhagens"); os.makedirs(OUTD, exist_ok=True)
P = os.path.join(HERE, "cunhagens_v394_dados.json")
raw = open(P, "rb").read(); dados = json.loads(raw.decode("utf-8"))
novos = DL.verbatins(OUTD)
shas_novos = {v["sha16"] for v in novos}
itens = [i for i in dados["itens"] if i["sha16"] not in shas_novos]          # idempotente: sai o que uma execucao anterior pos
assert itens and all("sha16" in i for i in itens), "o cunhagens_v394_dados.json nao traz itens"
for v in novos:
    b = open(v["origem_arquivo"], "rb").read()
    assert hashlib.sha256(b).hexdigest() == v["sha256"] and len(b) == v["bytes"]
    dst = v["arquivo"]
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        open(dst + ".tmp", "wb").write(b); os.replace(dst + ".tmp", dst)
    assert open(dst, "rb").read() == b
    itens.append({"sha16": v["sha16"], "grupo": DL.VERBATIM_PAPEL, "quando": "19/10", "arquivo": dst, "fonte_original": v["fonte_original"], "sha256": v["sha256"], "bytes": v["bytes"], "text": v["text"],
                  "multiplas_copias_na_origem": 1, "delta_19out": True})
out = dict(dados); out["itens"] = itens; out["n"] = len(itens)
out["delta_19out"] = {"adicionadas": [v["sha16"] for v in novos], "por": "montar_cunhagens_delta19_v394.py", "nota": "as duas falas de 19/10 (criterio binario de parada; flutuar no ponto fixo); as anteriores nao foram regeradas"}
bk = P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1d19"
open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
nb = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print(json.dumps({"n": out["n"], "adicionadas": out["delta_19out"]["adicionadas"], "backup": os.path.basename(bk)}, ensure_ascii=False))
