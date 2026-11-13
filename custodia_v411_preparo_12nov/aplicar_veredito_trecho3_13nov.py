# -*- coding: utf-8 -*-
"""Grava na fatia 06 do secoes_fatias.json o VEREDITO do verificador distinto sobre a divisão do trecho 3 (13/11/2026, claude-site-custodia).
O «aprovado» sai do arquivo do veredito (JSON do verificador), nunca de valor posto à mão; o recibo da divisão (com a exceção D196) fica
citado por sha16. Formato do arquivo preservado (indent 1, CRLF, sem fim de linha final); backup de bytes; temporário; releitura.
Uso: python -X utf8 <este> <VEREDITO.json> <RECIBO_DIVISAO.json>"""
import hashlib, json, os, sys, time
from pathlib import Path

CFG = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\secoes_fatias.json")
VER, REC = Path(sys.argv[1]), Path(sys.argv[2])
STAMP = time.strftime("%Y%m%d_%H%M%S")
v = json.loads(VER.read_text(encoding="utf-8"))
assert isinstance(v.get("aprovado"), bool) and isinstance(v.get("conferencias"), list) and isinstance(v.get("problemas"), list), "veredito fora do formato - PARAR"
raw = CFG.read_bytes()
cfg = json.loads(raw.decode("utf-8"))
assert json.dumps(cfg, ensure_ascii=False, indent=1).replace("\n", "\r\n").encode("utf-8") == raw, "formato inesperado - PARAR"
f = [x for x in cfg if x["slug"].startswith("06-")][0]
assert f.get("aprovado") is False and "divisao_13nov" in f, "a fatia 06 não está pendente do verificador - PARAR"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]  # noqa: E731
f["aprovado"] = v["aprovado"]
f["divisao_13nov"]["aprovacao"] = {"verificador": "agente distinto (Sonnet 5.5, só leitura; não construiu a divisão)", "veredito": str(VER),
                                   "veredito_sha16": sha(VER), "aprovado": v["aprovado"], "problemas": v["problemas"],
                                   "recibo": str(REC), "recibo_sha16": sha(REC), "excecao": "D196 (o portão da G1 no 3b, «never CONFIRMED»), escrita no recibo"}
novo = json.dumps(cfg, ensure_ascii=False, indent=1).replace("\n", "\r\n").encode("utf-8")
bak = CFG.with_name(CFG.name + ".bak_%s_veredito" % STAMP)
bak.write_bytes(raw)
assert bak.read_bytes() == raw
tmp = CFG.with_name(CFG.name + ".tmp_veredito")
tmp.write_bytes(novo)
assert [x for x in json.loads(tmp.read_bytes().decode("utf-8")) if x["slug"].startswith("06-")][0]["aprovado"] is v["aprovado"]
os.replace(tmp, CFG)
print("ok: fatia 06 aprovado = %s (do veredito %s, sha16 %s) | backup %s" % (v["aprovado"], VER.name, sha(VER), bak.name))
