# -*- coding: utf-8 -*-
"""derivar_servico_v405.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v405 (evento_c1_b3_v405.py, recibo_parada_v405.py, recibo_religamento_v405.py), o conferidor estatico deles
e o controle negativo do conferidor, a partir dos da v404 (v404/bancada_B3_servico, a cadeia que RODOU de verdade em 28/10: RECIBO_PARADA_v404.json e RECIBO_RELIGAMENTO_v404.json existem; o recibo_parada ja' traz a EMENDA do PID lido da porta).
A Bancada de producao pina a v404 (B13, deployment B13-v404-20261028-R1); o B(n) da v405 grava a B14. A subida e' SIMULTANEA e de uma passada so': 404 -> 405 (a versao DESTA cadeia) e 403 -> 404 (o B(n) anterior, o que a Bancada pina).
O conferidor e o controle negativo: a variavel V13 (caminho da cadeia anterior) passa a V14. O controle negativo usa pasta temporaria dentro de C:/t/vb21 (fica vb21). As contagens sao MEDIDAS nas fontes e gravadas; sai aborto se sobrar token velho.
LICAO DA v403 (recibo de parada): o texto da autorizacao do operador (V405_AUTORIZACAO_OPERADOR) NAO pode citar o nome do script do servico: o recibo de parada conta processos cuja linha de comando cita esse nome, e a
propria linha de comando do ato (que carrega o texto) seria contada. NAO executa nenhum dos scripts derivados. So' escreve em v405/bancada_B3_servico. uso: python -I -B -X utf8 derivar_servico_v405.py"""
import ast
import hashlib
import json
import os
import re
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
CS = os.path.dirname(V)
S404 = os.path.join(CS, "v404", "bancada_B3_servico")
NUM = re.compile(r"(?<![0-9])(403|404)(?![0-9])")
RE_V13 = re.compile(r"(?<![0-9A-Za-z_])V13(?![0-9A-Za-z_])")
RE_V14 = re.compile(r"(?<![0-9A-Za-z_])V14(?![0-9A-Za-z_])")
sha = lambda b: hashlib.sha256(b).hexdigest()
M = {"404": "405", "403": "404"}
ITENS = [(S404, "evento_c1_b3_v404.py", "."), (S404, "recibo_parada_v404.py", "."), (S404, "recibo_religamento_v404.py", "."), (S404, "conferir_exigencias_servico_v404.py", "."), (os.path.join(S404, "controle_negativo"), "mutar_conferidor_v404.py", "controle_negativo")]
rel = {"contrato": "DERIVACAO_SERVICO_v405", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "executado": False, "regra": "404 -> 405 e 403 -> 404 (uma passada, simultanea); V13 -> V14; contagens medidas nas fontes", "script": None, "arquivos": {}}
prontos = []
for pasta, nome, sub in ITENS:
    src = os.path.join(pasta, nome); raw = open(src, "rb").read(); txt = raw.decode("utf-8")
    assert not RE_V14.search(txt) and "405" not in txt, ("a fonte ja cita V14 ou 405", nome)
    med = {d: len(re.findall(r"(?<![0-9])%s(?![0-9])" % d, txt)) for d in M}; med["V13"] = len(RE_V13.findall(txt))
    novo, n = NUM.subn(lambda m_: M[m_.group(1)], txt); assert n == med["403"] + med["404"]
    novo = RE_V13.sub("V14", novo)
    assert not RE_V13.search(novo) and not re.search(r"(?<![0-9])403(?![0-9])", novo), nome
    ast.parse(novo)
    dst_nome = NUM.sub(lambda m_: M[m_.group(1)], nome); dst = os.path.join(HERE, sub, dst_nome)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    prontos.append((nome, src, dst, raw, novo.encode("utf-8"), med))
for nome, src, dst, raw, out, med in prontos:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst + ".tmp", "wb").write(out); assert os.path.getsize(dst + ".tmp") == len(out); os.replace(dst + ".tmp", dst)
    rel["arquivos"][os.path.basename(dst)] = {"entrada": src, "sha256_entrada": sha(raw), "saida": dst, "sha256_saida": sha(out), "bytes": len(out), "contagens_medidas": med}
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
json.dump(rel, open(os.path.join(HERE, "DERIVACAO_SERVICO_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["contagens_medidas"] for k, v in rel["arquivos"].items()}, ensure_ascii=False))
