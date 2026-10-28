# -*- coding: utf-8 -*-
"""derivar_derivador_servico_v403.py -- deriva v403\\bancada_B3_servico\\derivar_servico_v403.py de v402\\bancada_B3_servico\\derivar_servico_v402.py por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea: 399->400, 400->401, 401->402, 402->403 (numeros, identificadores S40x, nomes v40x e V40x_AUTORIZACAO_OPERADOR); V10->V11, V11->V12 (variaveis de caminho e os
identificadores RE_V1x e a chave V1x_para_V1y); vb18->vb19, vb19->vb20 (sandbox curto); B10->B11, B11->B12 (as geracoes da Bancada); «25/10»->«27/10» (a data em que a cadeia-fonte RODOU de verdade:
os recibos da v402 sao de 27/10/2026 02:46-02:48). Nada e' executado aqui (so' ast.parse); a saida nao sobrescreve. Gera DERIVACAO_DO_DERIVADOR_SERVICO_v403.json.
uso: python -I -B -X utf8 derivar_derivador_servico_v403.py"""
import ast, hashlib, json, os, re, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); CS = os.path.dirname(V)
SRC = os.path.join(CS, "v402", "bancada_B3_servico", "derivar_servico_v402.py")
DST = os.path.join(HERE, "derivar_servico_v403.py")
if os.path.exists(DST):
    raise SystemExit("ja existe, nao sobrescrevo: " + DST)
raw = open(SRC, "rb").read(); assert b"\r" not in raw
txt = raw.decode("utf-8"); cont = {}
# a frase HISTORICA da docstring (como a v402 derivou da v401; cita 398/400) nao sobe por digito: sai antes da subida e volta reescrita para a v403 no fim
HIST = re.compile(r"Diferenca para a derivacao da v401:.*?Nao ha digitos 399 nas fontes \(medido\)\.", re.S)
assert len(HIST.findall(txt)) == 1, len(HIST.findall(txt))
txt = HIST.sub("@@HIST@@", txt); cont["frase_historica_substituida"] = 1
HIST_V403 = ("Historico: a v402 derivou da v401 com a subida simultanea 401 -> 402 e 400 -> 401 (a Bancada pinava a v401; o B(n) da v402 gravou a B11). Agora o B(n) da v402 FOI aplicado (B11; passos 10-bis-a e 10-ter da v402 feitos em 27/10/2026),\n"
             "a Bancada pina a v402 e o ultimo B(n), o ultimo religamento e a geracao dela sao os da v402. Logo a subida e' SIMULTANEA e de uma passada so': 402 -> 403 (a versao DESTA cadeia) e 401 -> 402 (o B(n) anterior, o que a Bancada pina).\n"
             "O B(n) da v403 grava a B12. Nao ha digitos 400 nas fontes (medido pelo proprio derivador: sobrar 400 aborta).")
def bump(pat, f, nome):
    global txt
    n = [0]
    def g(m):
        n[0] += 1
        return f(m)
    txt = re.sub(pat, g, txt); cont[nome] = n[0]
assert set(re.findall(r"(?<![0-9])(3[0-9][0-9]|4[0-9][0-9])(?![0-9])", txt)) <= {"399", "400", "401", "402"}, set(re.findall(r"(?<![0-9])(3[0-9][0-9]|4[0-9][0-9])(?![0-9])", txt))
bump(r"(?<![0-9])(399|400|401|402)(?![0-9])", lambda m: "%d" % (int(m.group(1)) + 1), "numeros_399_402")
assert "V12" not in txt
bump(r"(?<![0-9A-Za-z])V1(0|1)(?![0-9])", lambda m: "V1%d" % (int(m.group(1)) + 1), "V1x")
assert "vb20" not in txt
bump(r"(?<![0-9A-Za-z])vb(18|19)(?![0-9])", lambda m: "vb%d" % (int(m.group(1)) + 1), "vb")
assert "B12" not in txt
bump(r"(?<![0-9A-Za-z])B1(0|1)(?![0-9])", lambda m: "B1%d" % (int(m.group(1)) + 1), "B1x")
assert txt.count("em 25/10") == 1, txt.count("em 25/10")
txt = txt.replace("em 25/10", "em 27/10"); cont["data_da_fonte"] = 1
assert txt.count("@@HIST@@") == 1
txt = txt.replace("@@HIST@@", HIST_V403)
# conferencias da saida
assert set(re.findall(r"(?<![0-9])(3[0-9][0-9]|4[0-9][0-9])(?![0-9])", txt)) <= {"400", "401", "402", "403"}
assert 'S402 = os.path.join(CS, "v402", "bancada_B3_servico")' in txt
assert 'M = {"402": "403", "401": "402"}' in txt
assert 'NUM = re.compile(r"(?<![0-9])(400|401|402)(?![0-9])")' in txt
assert "RE_V11 = re.compile" in txt and "RE_V12 = re.compile" in txt and 'subn("V12", t)' in txt
assert 'RE_VB = re.compile(r"(?<![0-9A-Za-z])vb19(?![0-9])")' in txt and 'subn("vb20", t)' in txt and 't.count("C:\\\\t\\\\vb20") == 3' in txt
assert 'os.environ.get("V403_AUTORIZACAO_OPERADOR"' in txt and 'os.environ.get("V402_AUTORIZACAO_OPERADOR"' in txt
assert '"DERIVACAO_SERVICO_v403"' in txt and 'assert set(NUM.findall(t)) <= {"402"}' in txt and '"403" not in t' in txt
assert "B12" in txt and "V10" not in txt and "vb18" not in txt and "B10" not in txt
ast.parse(txt)
out = txt.encode("utf-8")
with open(DST + ".tmp", "wb") as fh:
    fh.write(out)
assert os.path.getsize(DST + ".tmp") == len(out); os.replace(DST + ".tmp", DST)
sha = lambda b: hashlib.sha256(b).hexdigest()
rel = {"contrato": "DERIVACAO_DO_DERIVADOR_SERVICO_v403", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "entrada": {"path": SRC, "sha256": sha(raw), "bytes": len(raw)},
       "saida": {"path": DST, "sha256": sha(out), "bytes": len(out)}, "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())}, "contagens": cont, "ast_parse": "ok"}
pj = os.path.join(HERE, "DERIVACAO_DO_DERIVADOR_SERVICO_v403.json")
with open(pj + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(pj + ".tmp", pj)
print(json.dumps(rel, ensure_ascii=False))
