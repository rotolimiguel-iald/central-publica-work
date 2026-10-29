# -*- coding: utf-8 -*-
"""mutar_conferidor_v404.py -- CONTROLE NEGATIVO do conferidor estatico (conferir_exigencias_servico_v404.py). NADA do servico e' executado e nenhum script real e' alterado.
Copia os tres scripts derivados da v404 para uma pasta TEMPORARIA, aplica tres mutacoes e roda uma copia do conferidor apontada para elas; o conferidor tem de FALHAR (rc 1) em cada mutacao:
  M1  recibo_parada_v404.py      : o `assert AUT` passa para DEPOIS da criacao do socket (E/S antes da exigencia da autorizacao);
  M2  recibo_religamento_v404.py : a leitura da variavel de ambiente volta a V403_AUTORIZACAO_OPERADOR (nome da versao anterior sobrando);
  M3  evento_c1_b3_v404.py       : o `assert os.path.isfile(ESP)` passa para o FIM, depois do subprocess.run que anota no quadro.
Grava RESULTADO_CONTROLE_NEGATIVO_v404.json ao lado (nao sobrescreve) com os diffs das mutacoes e as condicoes que falharam. Nao deixa nenhum script mutado em disco (a pasta temporaria some).
uso: python -I -B -X utf8 mutar_conferidor_v404.py"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRV = os.path.dirname(HERE)                         # ...\v404\bancada_B3_servico
V = os.path.dirname(SRV)                            # ...\cadeia_de_selo\v404
V13 = os.path.join(os.path.dirname(V), "v403")
sha = lambda b: hashlib.sha256(b).hexdigest()
NOMES = ("evento_c1_b3_v404.py", "recibo_parada_v404.py", "recibo_religamento_v404.py")


def ler(p):
    return open(p, encoding="utf-8").read()


def gravar(p, t):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)


os.makedirs(r"C:\t\vb21", exist_ok=True)               # a pasta temporaria do controle negativo fica DENTRO do sandbox curto C:\t\vb21 (e some ao sair do with)
with tempfile.TemporaryDirectory(dir=r"C:\t\vb21") as tmp:
    for n in NOMES:
        shutil.copyfile(os.path.join(SRV, n), os.path.join(tmp, n))
    originais = {n: ler(os.path.join(tmp, n)) for n in NOMES}
    # M1: o assert AUT depois do socket
    t = originais["recibo_parada_v404.py"]
    linha = [x for x in t.splitlines(True) if x.startswith("assert AUT,")]
    assert len(linha) == 1 and t.count("s.close()\n") == 1
    m1 = t.replace(linha[0], "").replace("s.close()\n", "s.close()\n" + linha[0], 1)
    # M2: nome da versao anterior na leitura da variavel
    t = originais["recibo_religamento_v404.py"]
    a = 'os.environ.get("V404_AUTORIZACAO_OPERADOR"'
    assert t.count(a) == 1
    m2 = t.replace(a, 'os.environ.get("V403_AUTORIZACAO_OPERADOR"', 1)
    # M3: o assert do ESPERADOS no fim
    t = originais["evento_c1_b3_v404.py"]
    linha = [x for x in t.splitlines(True) if x.startswith("assert os.path.isfile(ESP)")]
    assert len(linha) == 1
    m3 = t.replace(linha[0], "") + linha[0]
    muts = {"M1_assert_AUT_depois_do_socket": ("recibo_parada_v404.py", m1), "M2_nome_da_versao_anterior_na_variavel": ("recibo_religamento_v404.py", m2),
            "M3_assert_do_ESPERADOS_depois_do_subprocess": ("evento_c1_b3_v404.py", m3)}
    diffs = {}
    for k, (n, novo) in muts.items():
        gravar(os.path.join(tmp, n), novo)
        diffs[k] = "".join(difflib.unified_diff(originais[n].splitlines(True), novo.splitlines(True), fromfile="real/" + n, tofile="mutado/" + n))
    # o conferidor: copia apontada para a pasta temporaria (HERE) e para as pastas reais v404 (V) e v403 (V13); a saida JSON cai na pasta temporaria
    c = ler(os.path.join(SRV, "conferir_exigencias_servico_v404.py"))
    a = "V = os.path.dirname(HERE)\n"
    assert c.count(a) == 1
    c = c.replace(a, "V = " + repr(V) + "\n")
    a = 'V13 = os.path.join(os.path.dirname(V), "v403")'
    assert c.count(a) == 1
    c = c.replace(a, "V13 = " + repr(V13))
    gravar(os.path.join(tmp, "conferir_mut.py"), c)
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(tmp, "conferir_mut.py")], capture_output=True, text=True, encoding="utf-8")
    saida = json.load(open(os.path.join(tmp, "CONFERENCIA_EXIGENCIAS_SERVICO_v404.json"), encoding="utf-8"))
    falhas = [{"nome": x["nome"], "observado": x["observado"]} for x in saida["condicoes"] if not x["ok"]]
    por_mutacao = {}
    for k, (n, _novo) in muts.items():
        por_mutacao[k] = [f["nome"] for f in falhas if f["nome"].startswith(n.replace("_v404.py", "")) or (n.startswith("evento") and f["nome"].startswith("evento"))]
res = {"contrato": "RESULTADO_CONTROLE_NEGATIVO_v404", "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())},
       "conferidor": {"path": os.path.join(SRV, "conferir_exigencias_servico_v404.py"), "sha256": sha(open(os.path.join(SRV, "conferir_exigencias_servico_v404.py"), "rb").read())},
       "mutacoes": list(muts), "rc_do_conferidor_sobre_as_mutacoes": r.returncode, "esperado_rc": 1, "n_condicoes": saida["n_condicoes"], "n_condicoes_ok": saida["n_condicoes_ok"],
       "condicoes_que_falharam": falhas, "falhas_por_mutacao": por_mutacao, "toda_mutacao_foi_pega": all(len(v) > 0 for v in por_mutacao.values()) and r.returncode == 1,
       "diffs_das_mutacoes": diffs, "escopo": "nada do servico foi executado; nenhum script real foi alterado; a pasta temporaria foi apagada; NOT_FALSIFIED nao e creditacao; o gate nao se move"}
dest = os.path.join(HERE, "RESULTADO_CONTROLE_NEGATIVO_v404.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("rc do conferidor sobre as mutacoes:", r.returncode, "| %d/%d condicoes ok | toda mutacao pega:" % (saida["n_condicoes_ok"], saida["n_condicoes"]), res["toda_mutacao_foi_pega"])
for k, v in por_mutacao.items():
    print(" ", k, "->", len(v), "condicao(oes) falhou(aram)")
print(dest, sha(open(dest, "rb").read())[:16])
sys.exit(0 if res["toda_mutacao_foi_pega"] else 1)
