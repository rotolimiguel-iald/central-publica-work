# -*- coding: utf-8 -*-
"""derivar_servico_v404.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v404 (evento_c1_b3_v404.py, recibo_parada_v404.py, recibo_religamento_v404.py), o conferidor estatico deles
e o controle negativo do conferidor, a partir dos da v403 (v403/bancada_B3_servico, a cadeia que RODOU de verdade em 28/10: RECIBO_PARADA_v403.json e RECIBO_RELIGAMENTO_v403.json existem).
A Bancada de producao pina a v403 (B12, deployment B12-v403-20261028-R1); o B(n) da v404 grava a B13. A subida e' SIMULTANEA e de uma passada so': 403 -> 404 (a versao DESTA cadeia) e 402 -> 403 (o B(n) anterior, o que a Bancada pina).
Regras, cada uma com contagem exata MEDIDA nas fontes da v403 (aborta se casar menos ou mais): (1) o conferidor e o controle negativo: a variavel V12 (caminho da cadeia anterior) passa a V13 (5 usos em cada um);
(2) o controle negativo usa uma pasta temporaria DENTRO de C:/t/vb21 (vb20 -> vb21, 3 usos; nao no TEMP do sistema); (3) a condicao do ESPERADOS no conferidor (que vale nos DOIS estados) ja' vem do molde, sem troca.
LICAO DA v403 (recibo de parada): o texto da autorizacao do operador (V404_AUTORIZACAO_OPERADOR) NAO pode citar o nome do script do servico: o recibo de parada conta processos cuja linha de comando cita esse nome, e a
propria linha de comando do ato (que carrega o texto) seria contada. NAO executa nenhum dos scripts derivados. So' escreve em v404/bancada_B3_servico. uso: python -I -B -X utf8 derivar_servico_v404.py"""
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
S403 = os.path.join(CS, "v403", "bancada_B3_servico")
NUM = re.compile(r"(?<![0-9])(402|403)(?![0-9])")
RE_V12 = re.compile(r"(?<![0-9A-Za-z_])V12(?![0-9A-Za-z_])")
RE_V13 = re.compile(r"(?<![0-9A-Za-z_])V13(?![0-9A-Za-z_])")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb20(?![0-9])")
sha = lambda b: hashlib.sha256(b).hexdigest()

# (pasta da fonte, nome na fonte, mapa de digitos, contagem esperada por digito, contagem de V12, contagem de vb20, trocas especificas [(velho, novo, n)], subpasta de saida)
# o mapa de digitos e' aplicado de uma so' vez (403 -> 404, 402 -> 403): sem encadear
M = {"403": "404", "402": "403"}
ITENS = [
    (S403, "evento_c1_b3_v403.py", M, {"403": 7, "402": 1}, 0, 0, [], "."),
    (S403, "recibo_parada_v403.py", M, {"403": 4, "402": 10}, 0, 0, [], "."),
    (S403, "recibo_religamento_v403.py", M, {"403": 8, "402": 6}, 0, 0, [], "."),
    (S403, "conferir_exigencias_servico_v403.py", M, {"403": 49, "402": 20}, 5, 0, [], "."),
    (os.path.join(S403, "controle_negativo"), "mutar_conferidor_v403.py", M, {"403": 28, "402": 5}, 5, 3, [], "controle_negativo"),
]
rel = {"contrato": "DERIVACAO_SERVICO_v404", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "executado": False,
       "regra": "403 -> 404 e 402 -> 403 (uma passada, simultanea); V12 -> V13 no conferidor e no controle negativo; vb20 -> vb21 no controle negativo; contagem exata por digito e por arquivo (medida nas fontes)", "script": None, "arquivos": {}}
prontos = []
for pasta, nome, mapa, esp, esp_v12, esp_vb, trocas, sub in ITENS:
    src = os.path.join(pasta, nome)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    t = raw.decode("utf-8")
    assert not RE_V13.search(t) and "vb21" not in t and "404" not in t, ("a fonte ja cita V13, vb21 ou 404", nome)
    cont = {}

    def f(m):
        cont[m.group(1)] = cont.get(m.group(1), 0) + 1
        return mapa[m.group(1)]

    nome_novo = NUM.sub(lambda m: mapa[m.group(1)], nome)
    t, n = NUM.subn(f, t)
    assert cont == esp, (nome, "contagem de digitos", cont, esp)
    assert set(NUM.findall(t)) <= {"403"}, ("sobrou 402 em " + nome_novo, set(NUM.findall(t)))
    t, n12 = RE_V12.subn("V13", t)
    assert n12 == esp_v12, (nome, "V12", n12, esp_v12)
    t, nvb = RE_VB.subn("vb21", t)
    assert nvb == esp_vb and "vb20" not in t, (nome, "vb20", nvb, esp_vb)
    cont_t = []
    for velho, novo, c in trocas:
        assert t.count(velho) == c, ("troca especifica nao casou", nome_novo, velho[:70], t.count(velho))
        t = t.replace(velho, novo)
        cont_t.append(c)
    if nome.startswith("mutar"):
        # a mutacao M2 grava o nome da versao ANTERIOR (agora V403_AUTORIZACAO_OPERADOR) onde o religamento le V404_AUTORIZACAO_OPERADOR
        assert t.count('os.environ.get("V404_AUTORIZACAO_OPERADOR"') == 1 and t.count('os.environ.get("V403_AUTORIZACAO_OPERADOR"') == 1
        assert t.count("C:" + chr(92) + "t" + chr(92) + "vb21") == 3, t.count("C:" + chr(92) + "t" + chr(92) + "vb21")
    ast.parse(t)
    out = t.encode("utf-8")
    dst = os.path.join(HERE, sub, nome_novo)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    prontos.append((nome_novo, src, dst, raw, out, {"digitos": cont, "V12_para_V13": n12, "vb20_para_vb21": nvb, "trocas_especificas": cont_t}))
for nome_novo, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: todas as saidas ja passaram nas regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["arquivos"][nome_novo] = {"origem": src, "origem_sha256": sha(raw), "sha256": sha(open(dst, "rb").read()), "bytes": len(out), "contagens": cont}
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dest = os.path.join(HERE, "DERIVACAO_SERVICO_v404.json")
if os.path.exists(dest):
    raise SystemExit("ja existe: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print({k: v["sha256"][:16] for k, v in rel["arquivos"].items()})
