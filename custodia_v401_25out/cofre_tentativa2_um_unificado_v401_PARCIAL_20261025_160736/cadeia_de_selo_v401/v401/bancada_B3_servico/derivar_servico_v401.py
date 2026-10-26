# -*- coding: utf-8 -*-
"""derivar_servico_v401.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v401 (evento_c1_b3_v401.py, recibo_parada_v401.py, recibo_religamento_v401.py), o conferidor estatico deles
e o controle negativo do conferidor, a partir dos da v400 (v400\\bancada_B3_servico; o controle negativo, que a v400 nao teve, vem do da v399). Diferenca para a derivacao da v400: la a Bancada AINDA pinava a v398 e
so' o 399 -> 400 subia; agora o B(n) da v400 FOI aplicado (B9, passo 10-bis-a e 10-ter da v400 feitos: RECIBO_PARADA_v400.json, RECIBO_RELIGAMENTO_v400.json), a Bancada pina a v400 e o ultimo B(n), o ultimo
religamento e a geracao dela sao os da v400. Logo a subida e' SIMULTANEA e de uma passada so': 400 -> 401 (a versao DESTA cadeia) e 398 -> 400 (o B(n) anterior, o que a Bancada pina). O B(n) da v401 grava a B10.
Regras especiais, cada uma com contagem exata (aborta se casar menos ou mais): (1) o conferidor: a variavel V8 (caminho da cadeia anterior) passa a V10 (5 usos); (2) a condicao do ESPERADOS passa a valer nos DOIS
estados (ESPERADOS_v401.json ausente: o evento aborta no isfile; presente com o um.py do Nos ainda diferente do candidato: aborta no assert do candidato); (3) o controle negativo (mutar_conferidor) usa uma pasta temporaria
DENTRO de C:\\t\\vb18 (nao no TEMP do sistema). NAO executa nenhum dos scripts derivados. So' escreve em v401\\bancada_B3_servico. uso: python -I -B -X utf8 derivar_servico_v401.py"""
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
S400 = os.path.join(CS, "v400", "bancada_B3_servico")
S399 = os.path.join(CS, "v399", "bancada_B3_servico")
NUM = re.compile(r"(?<![0-9])(398|399|400)(?![0-9])")
RE_V8 = re.compile(r"(?<![0-9A-Za-z_])V8(?![0-9A-Za-z_])")
sha = lambda b: hashlib.sha256(b).hexdigest()

# (pasta da fonte, nome na fonte, mapa de digitos, contagem esperada por digito, contagem de V8, trocas especificas [(velho, novo, n)], subpasta de saida)
# o mapa de digitos e' aplicado de uma so' vez (400 -> 401, 398 -> 400): sem encadear
M_400 = {"400": "401", "398": "400"}
M_399 = {"399": "401", "398": "400"}
OLD_CHK = ('chk("ESPERADOS_v401.json existe (gerado pelo ensaio) e o um.py do Nos AINDA NAO e o candidato dele: o evento ABORTARIA hoje no assert do candidato (antes de anotar no quadro)", '
           'bool(cand16_) and um_nos16_ != cand16_, [cand16_, um_nos16_], "diferentes")\n')
NEW_CHK = ('chk("ESPERADOS_v401.json AUSENTE (o evento abortaria no assert os.path.isfile) ou presente com o um.py do Nos AINDA NAO igual ao candidato dele (abortaria no assert do candidato): em qualquer dos dois estados o evento aborta ANTES de anotar no quadro", '
           'cand16_ is None or um_nos16_ != cand16_, [cand16_, um_nos16_], "ausente, ou diferentes")\n')
OLD_TMP = "with tempfile.TemporaryDirectory() as tmp:\n"
NEW_TMP = ('os.makedirs(r"C:\\t\\vb18", exist_ok=True)               # a pasta temporaria do controle negativo fica DENTRO do sandbox curto C:\\t\\vb18 (e some ao sair do with)\n'
           'with tempfile.TemporaryDirectory(dir=r"C:\\t\\vb18") as tmp:\n')
ITENS = [
    (S400, "evento_c1_b3_v400.py", M_400, {"400": 7, "398": 1}, 0, [], "."),
    (S400, "recibo_parada_v400.py", M_400, {"400": 4, "398": 10}, 0, [], "."),
    (S400, "recibo_religamento_v400.py", M_400, {"400": 8, "398": 6}, 0, [], "."),
    (S400, "conferir_exigencias_servico_v400.py", M_400, {"400": 49, "398": 20}, 5, [(OLD_CHK, NEW_CHK, 1)], "."),
    (os.path.join(S399, "controle_negativo"), "mutar_conferidor_v399.py", M_399, {"399": 28, "398": 5}, 5, [(OLD_TMP, NEW_TMP, 1)], "controle_negativo"),
]
rel = {"contrato": "DERIVACAO_SERVICO_v401", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "executado": False,
       "regra": "400 -> 401 e 398 -> 400 (uma passada, simultanea); V8 -> V10 no conferidor e no controle negativo; mais as duas trocas especificas com contagem exata", "script": None, "arquivos": {}}
prontos = []
for pasta, nome, mapa, esp, esp_v8, trocas, sub in ITENS:
    src = os.path.join(pasta, nome)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    t = raw.decode("utf-8")
    cont = {}

    def f(m):
        cont[m.group(1)] = cont.get(m.group(1), 0) + 1
        return mapa[m.group(1)] if m.group(1) in mapa else m.group(1)

    nome_novo = NUM.sub(lambda m: mapa[m.group(1)], nome)
    t, n = NUM.subn(f, t)
    assert cont == esp, (nome, "contagem de digitos", cont, esp)
    assert not set(NUM.findall(t)) - {"400", "401"}, ("sobrou 398/399 em " + nome_novo, set(NUM.findall(t)))
    t, n8 = RE_V8.subn("V10", t)
    assert n8 == esp_v8, (nome, "V8", n8, esp_v8)
    cont_t = []
    for velho, novo, c in trocas:
        assert t.count(velho) == c, ("troca especifica nao casou", nome_novo, velho[:70], t.count(velho))
        t = t.replace(velho, novo)
        cont_t.append(c)
    if nome.startswith("mutar"):
        # a mutacao M2 grava o nome da versao ANTERIOR (agora V400_AUTORIZACAO_OPERADOR) onde o religamento le V401_AUTORIZACAO_OPERADOR
        assert t.count('os.environ.get("V401_AUTORIZACAO_OPERADOR"') == 1 and t.count('os.environ.get("V400_AUTORIZACAO_OPERADOR"') == 1
    ast.parse(t)
    out = t.encode("utf-8")
    dst = os.path.join(HERE, sub, nome_novo)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    prontos.append((nome_novo, src, dst, raw, out, {"digitos": cont, "V8_para_V10": n8, "trocas_especificas": cont_t}))
for nome_novo, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: todas as saidas ja passaram nas regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["arquivos"][nome_novo] = {"origem": src, "origem_sha256": sha(raw), "sha256": sha(open(dst, "rb").read()), "bytes": len(out), "contagens": cont}
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dest = os.path.join(HERE, "DERIVACAO_SERVICO_v401.json")
if os.path.exists(dest):
    raise SystemExit("ja existe: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print({k: v["sha256"][:16] for k, v in rel["arquivos"].items()})
