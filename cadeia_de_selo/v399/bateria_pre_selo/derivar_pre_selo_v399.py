# -*- coding: utf-8 -*-
"""derivar_pre_selo_v399.py -- deriva, dos quatro arquivos da v398 (bateria_pre_selo), os da v399 por SUBIDA DE VERSAO com fronteira de digitos:
v398 -> v399 (nome da cadeia/saida), v397 -> v398 (o estado de hoje: o Nos e o pino da Bancada), v396 -> v397 (versao antes da anterior), vb15 -> vb16 (sandbox curto), V7 -> V8 (variavel de caminho).
Passagem unica (sem encadear), contagem registrada por token. Tudo ou nada: as quatro saidas sao calculadas e conferidas antes de gravar a primeira. Regras especiais, cada uma com contagem exata (assert):
  conferir: o selo e o manifesto do kernel ANTERIORES (agora v398) ja' saem de V\\base_v398 (V, a raiz da cadeia: a pasta existe, copia de bytes do Nos) -- como na v398, nao de
            bateria_pre_selo\\base_* (HERE): a entrada traz 2 usos de `os.path.join(V, "base_v397"` (-> base_v398) e NENHUM de `os.path.join(HERE, "base_v39`;
  conferir: o selo e o manifesto do kernel da versao ANTES da anterior saem de V8\\base_v397 (= v398\\base_v397, que existe): 2 usos de `os.path.join(V7, "base_v396"` (-> `os.path.join(V8, "base_v397"`);
  conferir: as variaveis SELO_V396 / KM_V396 (selo e manifesto da versao ANTES da anterior; nome herdado) passam a SELO_V397 / KM_V397 (2 usos cada; o `V396` maiusculo some);
  as variaveis vb15 e V7: contagem exata por arquivo (2/3/0/0 e 3/5/0/5); a contagem de cada token de versao por arquivo tambem e' conferida por assert (inventario medido nas fontes v398);
  o lancador chama o esboco com `--versao v398 --fase pre_selo --modo ensaio` (1 vez): a Bancada de producao pina a v398 = o Nos de hoje, sem salto.
Entrada: so' a v398\\bateria_pre_selo\\ (leitura). Saida: os 4 arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v399.json com sha256 de entrada e de saida. Nada e' executado aqui (so' ast.parse).
uso: python -I -B -X utf8 derivar_pre_selo_v399.py"""
import ast
import hashlib
import json
import os
import re
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
V8 = os.path.join(os.path.dirname(V), "v398", "bateria_pre_selo")

ARQ = ["gerar_pino_recibo_pre_selo", "conferir_recibo_pre_selo", "snap_producao", "rodar_ensaio_1_pre_selo"]
EXT = {"gerar_pino_recibo_pre_selo": ".py", "conferir_recibo_pre_selo": ".py", "snap_producao": ".py", "rodar_ensaio_1_pre_selo": ".sh"}
MAPA = {"v398": "v399", "v397": "v398", "v396": "v397"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(39[678])(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9])(?![0-9])")
RE_V_MAIUSCULO = re.compile(r"V3[0-9][0-9]")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb15(?![0-9])")
RE_V7 = re.compile(r"(?<![0-9A-Za-z_])V7(?![0-9A-Za-z_])")
RE_V8 = re.compile(r"(?<![0-9A-Za-z_])V8(?![0-9A-Za-z_])")
# contagens exatas esperadas (medidas nas fontes v398 por inventario e conferidas aqui por assert): vb15, V7 e cada token de versao por arquivo
ESP_VB = {"gerar_pino_recibo_pre_selo": 2, "conferir_recibo_pre_selo": 3, "snap_producao": 0, "rodar_ensaio_1_pre_selo": 0}
ESP_V7 = {"gerar_pino_recibo_pre_selo": 3, "conferir_recibo_pre_selo": 5, "snap_producao": 0, "rodar_ensaio_1_pre_selo": 5}
ESP_VER = {"gerar_pino_recibo_pre_selo": {"v398": 27, "v397": 11, "v396": 0},
           "conferir_recibo_pre_selo": {"v398": 14, "v397": 15, "v396": 3},
           "snap_producao": {"v398": 4, "v397": 0, "v396": 0},
           "rodar_ensaio_1_pre_selo": {"v398": 4, "v397": 16, "v396": 0}}


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v399", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens": {}, "ast_parse": {}}
prontos = []
for nome in ARQ:
    src = os.path.join(V8, nome + "_v398" + EXT[nome])
    dst = os.path.join(HERE, nome + "_v399" + EXT[nome])
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    # entrada: so' v396 / v397 / v398 em minusculo; V3xx maiusculo so' as quatro variaveis SELO_V396 / KM_V396 do conferir; nenhum V8 pre-existente (colidiria com a variavel nova)
    assert set(RE_V_QUALQUER.findall(txt)) <= {"396", "397", "398"}, (nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    n_mai = len(RE_V_MAIUSCULO.findall(txt))
    assert n_mai == (4 if nome == "conferir_recibo_pre_selo" else 0), (nome, n_mai)
    assert not RE_V8.search(txt), ("ja existe uma variavel V8 na fonte", nome)
    n_pinos = {p: txt.count(p) for p in ("PINOS_BN_v397.json", "PINOS_BATERIA_v397.json")}
    cont = {}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    txt, cont["versoes"] = RE_V.subn(sub_v, txt)
    cont["versoes_por_token"] = dict(por_token)
    assert cont["versoes_por_token"] == ESP_VER[nome], (nome, "versoes por token", cont["versoes_por_token"], ESP_VER[nome])
    txt, cont["vb15_para_vb16"] = RE_VB.subn("vb16", txt)
    txt, cont["V7_para_V8"] = RE_V7.subn("V8", txt)
    assert cont["vb15_para_vb16"] == ESP_VB[nome], (nome, "vb15", cont["vb15_para_vb16"], ESP_VB[nome])
    assert cont["V7_para_V8"] == ESP_V7[nome], (nome, "V7", cont["V7_para_V8"], ESP_V7[nome])
    assert cont["versoes"] == sum(por_token.values())
    if nome == "conferir_recibo_pre_selo":
        # o selo e o manifesto do kernel ANTERIORES (v398) saem de V\base_v398 (a raiz da cadeia); nenhum uso de HERE\base_v39x
        a = 'os.path.join(V, "base_v398"'
        assert txt.count(a) == 2, ("base_v398 em V", txt.count(a))
        assert txt.count('os.path.join(HERE, "base_v39') == 0
        cont["base_v398_em_V"] = 2
        # o selo e o manifesto da versao antes da anterior (v397) saem de V8\base_v397 (= v398\base_v397)
        assert txt.count('os.path.join(V8, "base_v397"') == 2, "o selo e o manifesto da versao antes da anterior (v397) saem de V8\\base_v397"
        cont["base_v397_em_V8"] = 2
        for velho, novo in (("SELO_V396", "SELO_V397"), ("KM_V396", "KM_V397")):
            assert txt.count(velho) == 2, (velho, txt.count(velho))
            txt = txt.replace(velho, novo)
            cont[velho + "_para_" + novo] = 2
        assert "V396" not in txt
    if nome == "gerar_pino_recibo_pre_selo":
        a = '"RECIBO_SINCRONIZACAO_v398_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if nome == "conferir_recibo_pre_selo":
        a = '"RECIBO_SINCRONIZACAO_v398_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if nome == "rodar_ensaio_1_pre_selo":
        a = "--versao v398 --fase pre_selo --modo ensaio"
        assert txt.count(a) == 1, ("lancador: versao do ensaio", txt.count(a))
    # saida: nenhuma referencia fora de v397 / v398 / v399, nenhum vb15 nem V7 residual; os pinos da v398 aparecem tantas vezes quanto os da v397 na entrada
    assert set(RE_V_QUALQUER.findall(txt)) <= {"397", "398", "399"}, (nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_VB.search(txt) and not RE_V7.search(txt) and "vb15" not in txt
    for velho, novo in (("PINOS_BN_v397.json", "PINOS_BN_v398.json"), ("PINOS_BATERIA_v397.json", "PINOS_BATERIA_v398.json")):
        assert txt.count(novo) == n_pinos[velho], (nome, novo, txt.count(novo), n_pinos[velho])
    if EXT[nome] == ".py":
        ast.parse(txt)
        rel["ast_parse"][nome] = "ok"
    out = txt.encode("utf-8")
    prontos.append((nome, src, dst, raw, out, cont))

for nome, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: as quatro saidas ja passaram em todas as regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["entradas"][nome] = {"path": src, "sha256": sha(raw), "bytes": len(raw)}
    rel["saidas"][nome] = {"path": dst, "sha256": sha(open(dst, "rb").read()), "bytes": len(out)}
    assert rel["saidas"][nome]["sha256"] == sha(out)
    rel["contagens"][nome] = cont
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v399.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens"], ensure_ascii=False))
