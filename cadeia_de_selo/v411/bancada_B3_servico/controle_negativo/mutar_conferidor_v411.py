# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] a ORDEM da v411 (12/11/2026): M4, M5 (a data da ordem da v410, 06/11/2026, de volta no script) e M6 (o nome da fala de 12/11 com um rotulo enfiado) e as condicoes esperadas com o texto novo do conferidor; a copia do conferidor roda sem a variavel do ensaio (grava so' na pasta temporaria); no ensaio do topo proposto o resultado vai a pasta de ensaio
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] controle negativo do conferidor do servico: M4 a M6 sobre a ORDEM da v410 (06/11/2026); M5 com a data da ordem da v409 (05/11/2026); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida de versao a versao) molde v410/bancada_B3_servico/controle_negativo/mutar_conferidor_v410.py (rotulos subidos por _bump_copia_v411.py; diff em bump/). Adaptado (v411, 12/11/2026, fork B): M4 e M6 falam da ORDEM da v411 (fala de 12/11); M5 volta a data da autorizacao anterior (06/11/2026, a da v410) como texto; o sandbox curto C:\t\vb22 que esta corrida cria
# so' para as pastas temporarias e' REMOVIDO no fim se ficou vazio (o molde o deixava vazio, e o B(n) pre-selo recusa rodar com C:\t\vb22 existente: a ordem das etapas da cadeia ficava refem disso); o resultado registra isso em `sandbox_curto`.
"""mutar_conferidor_v411.py -- CONTROLE NEGATIVO do conferidor estatico (conferir_exigencias_servico_v411.py). NADA do servico e' executado e nenhum script real e' alterado.
Adaptado em 04/11/2026 da v410 (que o herdou da v406): cada mutacao roda SOZINHA numa pasta TEMPORARIA nova (copia dos tres scripts derivados da v411 + a mutacao + uma copia do conferidor apontada para elas); antes, o controle sem mutacao (os tres scripts reais) tem de dar rc 0,
e depois o conferidor tem de FALHAR (rc 1) em cada mutacao, e a condicao que falha tem de ser a que aquela mutacao fere:
  M1  recibo_parada_v411.py      : o `assert AUT` passa para DEPOIS da criacao do socket (E/S antes da exigencia da autorizacao);
  M2  recibo_religamento_v411.py : a leitura da variavel de ambiente volta a V410_AUTORIZACAO_OPERADOR (nome da versao anterior sobrando);
  M3  evento_c1_b3_v411.py       : o `assert os.path.isfile(ESP)` passa para o FIM, depois do subprocess.run que anota no quadro;
  M4  recibo_parada_v411.py      : sai a conferencia da ordem de 12/11 (a ordem da v411: o assert com a fala e o ORDEM_SHA16): qualquer texto de autorizacao passaria;
  M5  recibo_religamento_v411.py : volta a data da ordem anterior (06/11/2026, a da v410) como texto no script (autorizacao anterior sobrando).
  M6  recibo_parada_v411.py      : o caminho do arquivo da fala de 12/11 vira um nome que NAO existe (um rotulo de versao enfiado no nome: o tipo de defeito que uma subida mecanica de rotulo introduz).
Grava RESULTADO_CONTROLE_NEGATIVO_v411.json ao lado (no modo de ensaio do topo proposto, em <pasta de ensaio>\\bancada_B3_servico\\controle_negativo, fora de work; nao sobrescreve) com os diffs das mutacoes e as condicoes que falharam. Nao deixa nenhum script mutado em disco (as pastas temporarias somem).
uso: python -I -B -X utf8 mutar_conferidor_v411.py   (a variavel V411_MUTAR_TEMP muda a pasta temporaria; o padrao e' o sandbox curto da cadeia, C:\\t\\vb22, que a cadeia limpa depois)"""
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
SRV = os.path.dirname(HERE)                         # ...\v411\bancada_B3_servico
V = os.path.dirname(SRV)                            # ...\cadeia_de_selo\v411
V14 = os.path.join(os.path.dirname(V), "v410")
sha = lambda b: hashlib.sha256(b).hexdigest()
NOMES = ("evento_c1_b3_v411.py", "recibo_parada_v411.py", "recibo_religamento_v411.py")
TEMP_DIR = os.environ.get("V411_MUTAR_TEMP") or "C:" + os.sep + "t" + os.sep + "vb22"   # o sandbox curto da cadeia (some ao sair do with)


def ler(p):
    return open(p, encoding="utf-8").read()


def gravar(p, t):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)


def so_uma_linha(t, prefixo):
    linha = [x for x in t.splitlines(True) if x.startswith(prefixo)]
    assert len(linha) == 1, (prefixo, len(linha))
    return linha[0]


def m1(t):   # o assert AUT depois do socket
    linha = so_uma_linha(t, "assert AUT,")
    assert t.count("s.close()\n") == 1
    return t.replace(linha, "").replace("s.close()\n", "s.close()\n" + linha, 1)


def m2(t):   # nome da versao anterior na leitura da variavel
    a = 'os.environ.get("V411_AUTORIZACAO_OPERADOR"'
    assert t.count(a) == 1
    return t.replace(a, 'os.environ.get("V410_AUTORIZACAO_OPERADOR"', 1)


def m3(t):   # o assert do ESPERADOS no fim
    linha = so_uma_linha(t, "assert os.path.isfile(ESP)")
    return t.replace(linha, "") + linha


def m4(t):   # sai a conferencia da ordem de 12/11 (a ordem da v411)
    return t.replace(so_uma_linha(t, "assert FRASE_DA_ORDEM in ORDEM_BYTES"), "")


def m5(t):   # a data da ordem anterior de volta, como texto
    a = '"""10-ter da v411'
    assert t.count(a) == 1
    return t.replace(a, a + " (autorizacao de 06/11/2026)", 1)


def m6(t):   # o nome do arquivo da fala vira um inexistente (um rotulo de versao enfiado no nome), o tipo de defeito que uma subida mecanica de rotulo introduz
    a = '"cunhagens_13out", "OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt")'   # (so' o caminho que o script ABRE)
    assert t.count(a) == 1
    return t.replace(a, a.replace("OPERADOR_12nov_", "OPERADOR_12nov_v411_"), 1)


# (nome, script, funcao, o pedaco do nome da condicao do conferidor que aquela mutacao fere)
MUTACOES = [("M1_assert_AUT_depois_do_socket", "recibo_parada_v411.py", m1, "recibo_parada_v411.py: nenhuma chamada de E/S antes do assert AUT"),
            ("M2_nome_da_versao_anterior_na_variavel", "recibo_religamento_v411.py", m2, "recibo_religamento_v411.py: ha a atribuicao AUT"),
            ("M3_assert_do_ESPERADOS_depois_do_subprocess", "evento_c1_b3_v411.py", m3, "evento: assert os.path.isfile(ESP)"),
            ("M4_sem_a_conferencia_da_ordem_de_12nov", "recibo_parada_v411.py", m4, "recibo_parada_v411.py: a ordem de 12/11 (a ordem da v411) e' conferida"),
            ("M5_data_da_ordem_de_06nov_no_script", "recibo_religamento_v411.py", m5, "recibo_religamento_v411.py: nenhum texto, data ou hash de autorizacao anterior"),
            ("M6_arquivo_da_fala_inexistente_no_caminho", "recibo_parada_v411.py", m6, "recibo_parada_v411.py: o arquivo da fala que o script abre (ORDEM) existe")]
CONF = ler(os.path.join(SRV, "conferir_exigencias_servico_v411.py"))
a = "V = os.path.dirname(HERE)\n"
assert CONF.count(a) == 1
CONF = CONF.replace(a, "V = " + repr(V) + "\n")   # o conferidor copiado: HERE = a pasta temporaria (os scripts), V e V14 = as pastas reais v411 e v410
a = 'V14 = os.path.join(os.path.dirname(V), "v410")'
assert CONF.count(a) == 1
CONF = CONF.replace(a, "V14 = " + repr(V14))


def rodar(tmp, nome_do_script=None, novo=None):
    """copia os tres scripts reais para tmp (um deles mutado, se pedido) e roda a copia do conferidor; devolve (rc, condicoes que falharam, n, n_ok)"""
    for n in NOMES:
        shutil.copyfile(os.path.join(SRV, n), os.path.join(tmp, n))
    if nome_do_script:
        gravar(os.path.join(tmp, nome_do_script), novo)
    gravar(os.path.join(tmp, "conferir_mut.py"), CONF)
    env_ = {k_: v_ for k_, v_ in os.environ.items() if k_ != "V411_ENSAIO_TOPO_PROPOSTO"}   # (v411) a copia do conferidor grava na pasta temporaria, nunca na de ensaio
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(tmp, "conferir_mut.py")], capture_output=True, text=True, encoding="utf-8", env=env_)
    saida = json.load(open(os.path.join(tmp, "CONFERENCIA_EXIGENCIAS_SERVICO_v411.json"), encoding="utf-8"))
    return r.returncode, [{"nome": x["nome"], "observado": x["observado"]} for x in saida["condicoes"] if not x["ok"]], saida["n_condicoes"], saida["n_condicoes_ok"]


CRIOU_SANDBOX = not os.path.exists(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)
with tempfile.TemporaryDirectory(dir=TEMP_DIR) as tmp:
    rc0, falhas0, n0, nok0 = rodar(tmp)   # o controle SEM mutacao: os scripts reais passam (senao a deteccao abaixo nao prova nada)
resultados = {}; diffs = {}
for k, n, fn, esperada in MUTACOES:
    with tempfile.TemporaryDirectory(dir=TEMP_DIR) as tmp:
        original = ler(os.path.join(SRV, n)); novo = fn(original)
        assert novo != original, ("a mutacao nao mudou nada", k)
        diffs[k] = "".join(difflib.unified_diff(original.splitlines(True), novo.splitlines(True), fromfile="real/" + n, tofile="mutado/" + n))
        rc, falhas, nn, nok = rodar(tmp, n, novo)
    resultados[k] = {"script": n, "rc": rc, "n_condicoes": nn, "n_condicoes_ok": nok, "condicoes_que_falharam": falhas, "condicao_esperada": esperada,
                     "pegou_a_condicao_esperada": any(f["nome"].startswith(esperada) for f in falhas), "pegou": rc == 1 and any(f["nome"].startswith(esperada) for f in falhas)}
SANDBOX = {"caminho": TEMP_DIR, "existia_antes": not CRIOU_SANDBOX, "criado_aqui": CRIOU_SANDBOX, "vazio_no_fim": None, "removido_no_fim": False}
if CRIOU_SANDBOX:   # so' o que ESTA corrida criou, e so' se ficou vazio (os.rmdir recusa pasta com conteudo): o molde deixava C:\t\vb22 vazio e o B(n) pre-selo recusa rodar com ele existente
    SANDBOX["vazio_no_fim"] = not os.listdir(TEMP_DIR)
    if SANDBOX["vazio_no_fim"]:
        os.rmdir(TEMP_DIR)
        SANDBOX["removido_no_fim"] = True
res = {"contrato": "RESULTADO_CONTROLE_NEGATIVO_v411", "sandbox_curto": SANDBOX, "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())},
       "conferidor": {"path": os.path.join(SRV, "conferir_exigencias_servico_v411.py"), "sha256": sha(open(os.path.join(SRV, "conferir_exigencias_servico_v411.py"), "rb").read())},
       "controle_sem_mutacao": {"rc": rc0, "esperado_rc": 0, "n_condicoes": n0, "n_condicoes_ok": nok0, "condicoes_que_falharam": falhas0},
       "mutacoes": list(resultados), "esperado_rc": 1, "resultados": resultados, "rc_do_conferidor_por_mutacao": {k: v["rc"] for k, v in resultados.items()},
       "falhas_por_mutacao": {k: [f["nome"] for f in v["condicoes_que_falharam"]] for k, v in resultados.items()},
       "toda_mutacao_foi_pega": rc0 == 0 and all(v["pegou"] for v in resultados.values()),
       "diffs_das_mutacoes": diffs, "escopo": "nada do servico foi executado; nenhum script real foi alterado; as pastas temporarias foram apagadas; NOT_FALSIFIED nao e creditacao; o gate nao se move"}
import importlib.util as _ilu
_sp_dl = _ilu.spec_from_file_location("delta_v411_mutar", os.path.join(V, "delta_v411.py")); _DLM = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(_DLM)
OUT_DIR = os.path.join(_DLM.SAIDA, "bancada_B3_servico", "controle_negativo") if _DLM.ENSAIO_TOPO_PROPOSTO else HERE   # (v411) no ensaio do topo proposto, a saida vai a pasta de ensaio
os.makedirs(OUT_DIR, exist_ok=True); res.update(_DLM.MARCA_ENSAIO)
dest = os.path.join(OUT_DIR, "RESULTADO_CONTROLE_NEGATIVO_v411.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("controle sem mutacao: rc", rc0, "(%d/%d condicoes ok)" % (nok0, n0), "| toda mutacao pega:", res["toda_mutacao_foi_pega"])
for k, v in resultados.items():
    print(" ", k, "-> rc", v["rc"], "|", len(v["condicoes_que_falharam"]), "condicao(oes) falhou(aram) | pegou a esperada:", v["pegou_a_condicao_esperada"])
print(dest, sha(open(dest, "rb").read())[:16])
sys.exit(0 if res["toda_mutacao_foi_pega"] else 1)
