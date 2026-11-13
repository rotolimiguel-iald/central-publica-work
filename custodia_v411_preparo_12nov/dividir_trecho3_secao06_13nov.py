# -*- coding: utf-8 -*-
"""D195/opção (a) (13/11/2026, claude-site-custodia; decisão da gerência c1): o trecho 3 da seção 06 do site («What is NOT proved» do
ESTADO_ATUAL.md) passa de 4425 B (> teto de 4000) a DOIS trechos contíguos e verbatim, cortados em quebra de parágrafo:
  3a = o título + o parágrafo do P2 (o resultado com as obrigações, INTEIRO) + a quebra de parágrafo;
  3b = a lista «Nature's» até o mesmo marcador de fim de hoje.
3a + 3b = o trecho 3 de hoje, byte a byte. O teto não sobe. A fatia fica com aprovado = false até o verificador (agente distinto) decidir:
o valor NÃO é posto à mão (aplicar_veredito_trecho3_13nov.py grava o veredito do verificador).
Backup de bytes; temporário; confere o JSON relido. Uso: python -X utf8 <este> [secoes_fatias.json] [ESTADO_ATUAL.md]"""
import json, os, sys, time
from pathlib import Path

CFG = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools\secoes_fatias.json")
EST = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(r"C:\IALD\Artigo\the_boundary\ESTADO_ATUAL.md")
STAMP = time.strftime("%Y%m%d_%H%M%S")
TETO = 4000
raw = CFG.read_bytes()
cfg = json.loads(raw.decode("utf-8"))
f = [x for x in cfg if x["slug"].startswith("06-")]
assert len(f) == 1
f = f[0]
t3 = f["trechos"][2]
assert t3["arquivo"] == "ESTADO_ATUAL.md" and t3["inicio"].startswith("## What is NOT proved") and len(f["trechos"]) == 4, "a fatia 06 não é a esperada - PARAR"
b = EST.read_bytes()
ini, fim = t3["inicio"].encode("utf-8"), t3["fim"].encode("utf-8")
s0 = b.find(ini); e1 = b.find(fim, s0 + len(ini)) + len(fim)
assert b.count(ini) == 1 and s0 >= 0 and e1 > s0
tre = b[s0:e1]
eol = b"\r\n" if b"\r\n" in tre else b"\n"
sep = eol + eol
p = tre.split(sep)
assert len(p) == 3, "o trecho 3 não tem três parágrafos - PARAR (%d)" % len(p)
fim_a = p[1][-70:] + sep                    # o fim do parágrafo do P2 e a quebra de parágrafo
ini_b = p[2][:60]                           # o começo da lista «Nature's»
a_bytes = tre[:len(p[0]) + len(sep) + len(p[1]) + len(sep)]
b_bytes = tre[len(a_bytes):]
assert a_bytes + b_bytes == tre and a_bytes.endswith(fim_a) and b_bytes.startswith(ini_b)
assert b.count(ini_b) == 1 and b.find(fim_a, s0 + len(ini)) + len(fim_a) == s0 + len(a_bytes)
assert len(a_bytes) <= TETO and len(b_bytes) <= TETO, (len(a_bytes), len(b_bytes))
t3a = {"arquivo": t3["arquivo"], "inicio": t3["inicio"], "fim": fim_a.decode("utf-8"), "bytes_medidos": len(a_bytes),
       "motivo": "O começo da lista canônica do que NÃO está provado: a leitura com a régua e o P2, que traz o resultado do teste H0DN × BG1 com as suas obrigações, inteiro neste trecho. "
                 "(13/11/2026: o trecho 3 de antes, acima de 4000 B, dividido em dois contíguos; decisão da gerência c1.)",
       "estatuto": t3["estatuto"]}
t3b = {"arquivo": t3["arquivo"], "inicio": ini_b.decode("utf-8"), "fim": t3["fim"], "bytes_medidos": len(b_bytes),
       "motivo": "A continuação da lista canônica do que NÃO está provado: H1/H2 na natureza, a identificação física da tela, α, a matemática fora da mathlib, os negativos honestos e as seis folhas, com a nota de linhagem H1–H3 → H1/H2. "
                 "(13/11/2026: a segunda metade do trecho 3 de antes, contígua à primeira.)",
       "estatuto": t3["estatuto"]}
f["trechos"] = f["trechos"][:2] + [t3a, t3b] + f["trechos"][3:]
f["aprovado"] = False
f["divisao_13nov"] = {"de": "o trecho 3 de antes (%d B, acima do teto de %d)" % (len(tre), TETO), "para": [len(a_bytes), len(b_bytes)],
                      "concatenados_iguais": True, "aprovacao": "pendente do verificador (agente distinto); o valor não é posto à mão"}
antes = json.loads(raw.decode("utf-8"))
assert (json.dumps(antes, ensure_ascii=False, indent=1).replace("\n", "\r\n")).encode("utf-8") == raw, "o formato do JSON não é o esperado (indent 1, CRLF, sem fim de linha final) - PARAR"
novo = json.dumps(cfg, ensure_ascii=False, indent=1).replace("\n", "\r\n").encode("utf-8")   # o formato do arquivo, byte a byte
assert [x for x in json.loads(novo.decode("utf-8")) if not x["slug"].startswith("06-")] == [x for x in antes if not x["slug"].startswith("06-")]
bak = CFG.with_name(CFG.name + ".bak_%s_trecho3" % STAMP)
bak.write_bytes(raw)
assert bak.read_bytes() == raw
tmp = CFG.with_name(CFG.name + ".tmp_trecho3")
tmp.write_bytes(novo)
assert json.loads(tmp.read_bytes().decode("utf-8"))[[x["slug"] for x in cfg].index(f["slug"])]["trechos"][2]["fim"] == fim_a.decode("utf-8")
os.replace(tmp, CFG)
print("ok: %s | trecho 3 (%d B) -> 3a %d B + 3b %d B; aprovado = false (pendente do verificador) | backup %s" % (CFG.name, len(tre), len(a_bytes), len(b_bytes), bak.name))
