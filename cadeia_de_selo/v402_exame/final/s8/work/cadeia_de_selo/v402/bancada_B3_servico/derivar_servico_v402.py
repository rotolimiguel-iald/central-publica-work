# -*- coding: utf-8 -*-
"""derivar_servico_v402.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v402 (evento_c1_b3_v402.py, recibo_parada_v402.py, recibo_religamento_v402.py), o conferidor estatico deles
e o controle negativo do conferidor, a partir dos da v401 (v401\\bancada_B3_servico, a cadeia que RODOU de verdade em 25/10: RECIBO_PARADA_v401.json e RECIBO_RELIGAMENTO_v401.json existem; o controle negativo,
que a v401 derivou da v399, tem agora o proprio da v401). Diferenca para a derivacao da v401: la a Bancada pinava a v400 e a subida simultanea era 400 -> 401 e 398 -> 400 (as duas versoes em jogo eram o B(n) anterior
e o novo); agora o B(n) da v401 FOI aplicado (B10, passo 10-bis-a e 10-ter da v401 feitos), a Bancada pina a v401 e o ultimo B(n), o ultimo religamento e a geracao dela sao os da v401. Logo a subida e'
SIMULTANEA e de uma passada so': 401 -> 402 (a versao DESTA cadeia) e 400 -> 401 (o B(n) anterior, o que a Bancada pina). O B(n) da v402 grava a B11. Nao ha digitos 399 nas fontes (medido).
Regras especiais, cada uma com contagem exata (aborta se casar menos ou mais): (1) o conferidor e o controle negativo: a variavel V10 (caminho da cadeia anterior) passa a V11 (5 usos em cada um);
(2) o controle negativo (mutar_conferidor) usa uma pasta temporaria DENTRO de C:\\t\\vb19 (vb18 -> vb19, 3 usos; nao no TEMP do sistema); (3) a condicao do ESPERADOS no conferidor (que vale nos DOIS estados:
ESPERADOS_v402.json ausente, o evento aborta no isfile; presente com o um.py do Nos ainda diferente do candidato, aborta no assert do candidato) JA' vem do molde v401, sem troca. NAO executa nenhum dos
scripts derivados. So' escreve em v402\\bancada_B3_servico. uso: python -I -B -X utf8 derivar_servico_v402.py"""
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
S401 = os.path.join(CS, "v401", "bancada_B3_servico")
NUM = re.compile(r"(?<![0-9])(399|400|401)(?![0-9])")
RE_V10 = re.compile(r"(?<![0-9A-Za-z_])V10(?![0-9A-Za-z_])")
RE_V11 = re.compile(r"(?<![0-9A-Za-z_])V11(?![0-9A-Za-z_])")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb18(?![0-9])")
sha = lambda b: hashlib.sha256(b).hexdigest()

# (pasta da fonte, nome na fonte, mapa de digitos, contagem esperada por digito, contagem de V10, contagem de vb18, trocas especificas [(velho, novo, n)], subpasta de saida)
# o mapa de digitos e' aplicado de uma so' vez (401 -> 402, 400 -> 401): sem encadear
M = {"401": "402", "400": "401"}
ITENS = [
    (S401, "evento_c1_b3_v401.py", M, {"401": 7, "400": 1}, 0, 0, [], "."),
    (S401, "recibo_parada_v401.py", M, {"401": 4, "400": 10}, 0, 0, [], "."),
    (S401, "recibo_religamento_v401.py", M, {"401": 8, "400": 6}, 0, 0, [], "."),
    (S401, "conferir_exigencias_servico_v401.py", M, {"401": 49, "400": 20}, 5, 0, [], "."),
    (os.path.join(S401, "controle_negativo"), "mutar_conferidor_v401.py", M, {"401": 28, "400": 5}, 5, 3, [], "controle_negativo"),
]
rel = {"contrato": "DERIVACAO_SERVICO_v402", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "executado": False,
       "regra": "401 -> 402 e 400 -> 401 (uma passada, simultanea); V10 -> V11 no conferidor e no controle negativo; vb18 -> vb19 no controle negativo; contagem exata por digito e por arquivo", "script": None, "arquivos": {}}
prontos = []
for pasta, nome, mapa, esp, esp_v10, esp_vb, trocas, sub in ITENS:
    src = os.path.join(pasta, nome)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    t = raw.decode("utf-8")
    assert not RE_V11.search(t) and "vb19" not in t and "402" not in t, ("a fonte ja cita V11, vb19 ou 402", nome)
    cont = {}

    def f(m):
        cont[m.group(1)] = cont.get(m.group(1), 0) + 1
        return mapa[m.group(1)] if m.group(1) in mapa else m.group(1)

    nome_novo = NUM.sub(lambda m: mapa[m.group(1)], nome)
    t, n = NUM.subn(f, t)
    assert cont == esp, (nome, "contagem de digitos", cont, esp)
    assert set(NUM.findall(t)) <= {"401"}, ("sobrou 399/400 em " + nome_novo, set(NUM.findall(t)))
    t, n10 = RE_V10.subn("V11", t)
    assert n10 == esp_v10, (nome, "V10", n10, esp_v10)
    t, nvb = RE_VB.subn("vb19", t)
    assert nvb == esp_vb and "vb18" not in t, (nome, "vb18", nvb, esp_vb)
    cont_t = []
    for velho, novo, c in trocas:
        assert t.count(velho) == c, ("troca especifica nao casou", nome_novo, velho[:70], t.count(velho))
        t = t.replace(velho, novo)
        cont_t.append(c)
    if nome.startswith("mutar"):
        # a mutacao M2 grava o nome da versao ANTERIOR (agora V401_AUTORIZACAO_OPERADOR) onde o religamento le V402_AUTORIZACAO_OPERADOR
        assert t.count('os.environ.get("V402_AUTORIZACAO_OPERADOR"') == 1 and t.count('os.environ.get("V401_AUTORIZACAO_OPERADOR"') == 1
        assert t.count("C:\\t\\vb19") == 3, t.count("C:\\t\\vb19")
    ast.parse(t)
    out = t.encode("utf-8")
    dst = os.path.join(HERE, sub, nome_novo)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    prontos.append((nome_novo, src, dst, raw, out, {"digitos": cont, "V10_para_V11": n10, "vb18_para_vb19": nvb, "trocas_especificas": cont_t}))
for nome_novo, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: todas as saidas ja passaram nas regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["arquivos"][nome_novo] = {"origem": src, "origem_sha256": sha(raw), "sha256": sha(open(dst, "rb").read()), "bytes": len(out), "contagens": cont}
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dest = os.path.join(HERE, "DERIVACAO_SERVICO_v402.json")
if os.path.exists(dest):
    raise SystemExit("ja existe: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print({k: v["sha256"][:16] for k, v in rel["arquivos"].items()})
