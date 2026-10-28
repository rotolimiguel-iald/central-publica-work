# -*- coding: utf-8 -*-
"""derivar_servico_v403.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v403 (evento_c1_b3_v403.py, recibo_parada_v403.py, recibo_religamento_v403.py), o conferidor estatico deles
e o controle negativo do conferidor, a partir dos da v402 (v402\\bancada_B3_servico, a cadeia que RODOU de verdade em 27/10: RECIBO_PARADA_v402.json e RECIBO_RELIGAMENTO_v402.json existem; o controle negativo,
que a v402 derivou da v400, tem agora o proprio da v402). Historico: a v402 derivou da v401 com a subida simultanea 401 -> 402 e 400 -> 401 (a Bancada pinava a v401; o B(n) da v402 gravou a B11). Agora o B(n) da v402 FOI aplicado (B11; passos 10-bis-a e 10-ter da v402 feitos em 27/10/2026),
a Bancada pina a v402 e o ultimo B(n), o ultimo religamento e a geracao dela sao os da v402. Logo a subida e' SIMULTANEA e de uma passada so': 402 -> 403 (a versao DESTA cadeia) e 401 -> 402 (o B(n) anterior, o que a Bancada pina).
O B(n) da v403 grava a B12. Nao ha digitos 400 nas fontes (medido pelo proprio derivador: sobrar 400 aborta).
Regras especiais, cada uma com contagem exata (aborta se casar menos ou mais): (1) o conferidor e o controle negativo: a variavel V11 (caminho da cadeia anterior) passa a V12 (5 usos em cada um);
(2) o controle negativo (mutar_conferidor) usa uma pasta temporaria DENTRO de C:\\t\\vb20 (vb19 -> vb20, 3 usos; nao no TEMP do sistema); (3) a condicao do ESPERADOS no conferidor (que vale nos DOIS estados:
ESPERADOS_v403.json ausente, o evento aborta no isfile; presente com o um.py do Nos ainda diferente do candidato, aborta no assert do candidato) JA' vem do molde v402, sem troca. NAO executa nenhum dos
scripts derivados. So' escreve em v403\\bancada_B3_servico. uso: python -I -B -X utf8 derivar_servico_v403.py"""
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
S402 = os.path.join(CS, "v402", "bancada_B3_servico")
NUM = re.compile(r"(?<![0-9])(400|401|402)(?![0-9])")
RE_V11 = re.compile(r"(?<![0-9A-Za-z_])V11(?![0-9A-Za-z_])")
RE_V12 = re.compile(r"(?<![0-9A-Za-z_])V12(?![0-9A-Za-z_])")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb19(?![0-9])")
sha = lambda b: hashlib.sha256(b).hexdigest()

# (pasta da fonte, nome na fonte, mapa de digitos, contagem esperada por digito, contagem de V11, contagem de vb19, trocas especificas [(velho, novo, n)], subpasta de saida)
# o mapa de digitos e' aplicado de uma so' vez (402 -> 403, 401 -> 402): sem encadear
M = {"402": "403", "401": "402"}
ITENS = [
    (S402, "evento_c1_b3_v402.py", M, {"402": 7, "401": 1}, 0, 0, [], "."),
    (S402, "recibo_parada_v402.py", M, {"402": 4, "401": 10}, 0, 0, [], "."),
    (S402, "recibo_religamento_v402.py", M, {"402": 8, "401": 6}, 0, 0, [], "."),
    (S402, "conferir_exigencias_servico_v402.py", M, {"402": 49, "401": 20}, 5, 0, [], "."),
    (os.path.join(S402, "controle_negativo"), "mutar_conferidor_v402.py", M, {"402": 28, "401": 5}, 5, 3, [], "controle_negativo"),
]
rel = {"contrato": "DERIVACAO_SERVICO_v403", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "executado": False,
       "regra": "402 -> 403 e 401 -> 402 (uma passada, simultanea); V11 -> V12 no conferidor e no controle negativo; vb19 -> vb20 no controle negativo; contagem exata por digito e por arquivo", "script": None, "arquivos": {}}
prontos = []
for pasta, nome, mapa, esp, esp_v10, esp_vb, trocas, sub in ITENS:
    src = os.path.join(pasta, nome)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    t = raw.decode("utf-8")
    assert not RE_V12.search(t) and "vb20" not in t and "403" not in t, ("a fonte ja cita V12, vb20 ou 403", nome)
    cont = {}

    def f(m):
        cont[m.group(1)] = cont.get(m.group(1), 0) + 1
        return mapa[m.group(1)] if m.group(1) in mapa else m.group(1)

    nome_novo = NUM.sub(lambda m: mapa[m.group(1)], nome)
    t, n = NUM.subn(f, t)
    assert cont == esp, (nome, "contagem de digitos", cont, esp)
    assert set(NUM.findall(t)) <= {"402"}, ("sobrou 400/401 em " + nome_novo, set(NUM.findall(t)))
    t, n10 = RE_V11.subn("V12", t)
    assert n10 == esp_v10, (nome, "V11", n10, esp_v10)
    t, nvb = RE_VB.subn("vb20", t)
    assert nvb == esp_vb and "vb19" not in t, (nome, "vb19", nvb, esp_vb)
    cont_t = []
    for velho, novo, c in trocas:
        assert t.count(velho) == c, ("troca especifica nao casou", nome_novo, velho[:70], t.count(velho))
        t = t.replace(velho, novo)
        cont_t.append(c)
    if nome.startswith("mutar"):
        # a mutacao M2 grava o nome da versao ANTERIOR (agora V402_AUTORIZACAO_OPERADOR) onde o religamento le V403_AUTORIZACAO_OPERADOR
        assert t.count('os.environ.get("V403_AUTORIZACAO_OPERADOR"') == 1 and t.count('os.environ.get("V402_AUTORIZACAO_OPERADOR"') == 1
        assert t.count("C:\\t\\vb20") == 3, t.count("C:\\t\\vb20")
    ast.parse(t)
    out = t.encode("utf-8")
    dst = os.path.join(HERE, sub, nome_novo)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    prontos.append((nome_novo, src, dst, raw, out, {"digitos": cont, "V11_para_V12": n10, "vb19_para_vb20": nvb, "trocas_especificas": cont_t}))
for nome_novo, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: todas as saidas ja passaram nas regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["arquivos"][nome_novo] = {"origem": src, "origem_sha256": sha(raw), "sha256": sha(open(dst, "rb").read()), "bytes": len(out), "contagens": cont}
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dest = os.path.join(HERE, "DERIVACAO_SERVICO_v403.json")
if os.path.exists(dest):
    raise SystemExit("ja existe: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print({k: v["sha256"][:16] for k, v in rel["arquivos"].items()})
