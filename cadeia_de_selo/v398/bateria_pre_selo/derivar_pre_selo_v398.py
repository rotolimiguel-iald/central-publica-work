# -*- coding: utf-8 -*-
"""derivar_pre_selo_v398.py -- deriva, dos quatro arquivos da v397 (bateria_pre_selo), os da v398 por SUBIDA DE VERSAO com fronteira de digitos:
v397 -> v398 (nome da cadeia/saida), v396 -> v397 (o estado de hoje: o Nos e o pino da Bancada), v395 -> v396 (versao antes da anterior), vb14 -> vb15 (sandbox curto), V6 -> V7 (variavel de caminho).
Passagem unica (sem encadear), contagem registrada por token. Tudo ou nada: as quatro saidas sao calculadas e conferidas antes de gravar a primeira. Regras especiais, cada uma com contagem exata (assert):
  conferir: as duas leituras do selo e do manifesto do kernel ANTERIORES (v397) saem de v398\\base_v397 (V, a raiz da cadeia: a pasta ja existe, copia de bytes do Nos), nao de
            bateria_pre_selo\\base_v397 (HERE) como no molde (la v397\\base_v396 ainda nao existia): 2 trocas de `os.path.join(HERE, "base_v397"` por `os.path.join(V, "base_v397"`;
  conferir: as variaveis SELO_V394 / KM_V394 (selo e manifesto da versao ANTES da anterior; nome herdado de duas geracoes atras) passam a SELO_V396 / KM_V396 (2 usos cada);
  as variaveis vb14 e V6: contagem exata por arquivo (2/3/0/0 e 3/5/0/5); o lancador chama o esboco com `--versao v397 --fase pre_selo --modo ensaio` (1 vez): a Bancada de producao pina a v397
  = o Nos de hoje, sem salto.
Entrada: so' a v397\\bateria_pre_selo\\ (leitura). Saida: os 4 arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v398.json com sha256 de entrada e de saida. Nada e' executado aqui (so' ast.parse).
uso: python -I -B -X utf8 derivar_pre_selo_v398.py"""
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
V7 = os.path.join(os.path.dirname(V), "v397", "bateria_pre_selo")

ARQ = ["gerar_pino_recibo_pre_selo", "conferir_recibo_pre_selo", "snap_producao", "rodar_ensaio_1_pre_selo"]
EXT = {"gerar_pino_recibo_pre_selo": ".py", "conferir_recibo_pre_selo": ".py", "snap_producao": ".py", "rodar_ensaio_1_pre_selo": ".sh"}
MAPA = {"v397": "v398", "v396": "v397", "v395": "v396"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(39[567])(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9])(?![0-9])")
RE_V_MAIUSCULO = re.compile(r"V3[0-9][0-9]")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb14(?![0-9])")
RE_V6 = re.compile(r"(?<![0-9A-Za-z_])V6(?![0-9A-Za-z_])")
# contagens exatas esperadas (lidas do molde v397 por inspecao e conferidas aqui por assert): vb14 e V6 por arquivo
ESP_VB = {"gerar_pino_recibo_pre_selo": 2, "conferir_recibo_pre_selo": 3, "snap_producao": 0, "rodar_ensaio_1_pre_selo": 0}
ESP_V6 = {"gerar_pino_recibo_pre_selo": 3, "conferir_recibo_pre_selo": 5, "snap_producao": 0, "rodar_ensaio_1_pre_selo": 5}


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v398", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens": {}, "ast_parse": {}}
prontos = []
for nome in ARQ:
    src = os.path.join(V7, nome + "_v397" + EXT[nome])
    dst = os.path.join(HERE, nome + "_v398" + EXT[nome])
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    # entrada: so' v395 / v396 / v397 em minusculo; V3xx maiusculo so' as quatro variaveis SELO_V394 / KM_V394 do conferir
    assert set(RE_V_QUALQUER.findall(txt)) <= {"395", "396", "397"}, (nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    n_mai = len(RE_V_MAIUSCULO.findall(txt))
    assert n_mai == (4 if nome == "conferir_recibo_pre_selo" else 0), (nome, n_mai)
    n_pinos = {p: txt.count(p) for p in ("PINOS_BN_v396.json", "PINOS_BATERIA_v396.json")}
    cont = {}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    txt, cont["versoes"] = RE_V.subn(sub_v, txt)
    cont["versoes_por_token"] = dict(por_token)
    txt, cont["vb14_para_vb15"] = RE_VB.subn("vb15", txt)
    txt, cont["V6_para_V7"] = RE_V6.subn("V7", txt)
    assert cont["vb14_para_vb15"] == ESP_VB[nome], (nome, "vb14", cont["vb14_para_vb15"], ESP_VB[nome])
    assert cont["V6_para_V7"] == ESP_V6[nome], (nome, "V6", cont["V6_para_V7"], ESP_V6[nome])
    assert cont["versoes"] == sum(por_token.values())
    if nome == "conferir_recibo_pre_selo":
        a = 'os.path.join(HERE, "base_v397"'
        assert txt.count(a) == 2, ("base_v397 em HERE", txt.count(a))
        txt = txt.replace(a, 'os.path.join(V, "base_v397"')
        cont["base_v397_em_V"] = 2
        assert txt.count('os.path.join(V7, "base_v396"') == 2, "o selo e o manifesto da versao antes da anterior (v396) saem de V7\\base_v396"
        for velho, novo in (("SELO_V394", "SELO_V396"), ("KM_V394", "KM_V396")):
            assert txt.count(velho) == 2, (velho, txt.count(velho))
            txt = txt.replace(velho, novo)
            cont[velho + "_para_" + novo] = 2
        assert "V394" not in txt
        assert txt.count('os.path.join(HERE, "base_v39') == 0
    if nome == "gerar_pino_recibo_pre_selo":
        a = '"RECIBO_SINCRONIZACAO_v397_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if nome == "conferir_recibo_pre_selo":
        a = '"RECIBO_SINCRONIZACAO_v397_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if nome == "rodar_ensaio_1_pre_selo":
        a = "--versao v397 --fase pre_selo --modo ensaio"
        assert txt.count(a) == 1, ("lancador: versao do ensaio", txt.count(a))
    # saida: nenhuma referencia fora de v396 / v397 / v398, nenhum vb14 nem V6 residual; os pinos da v397 aparecem tantas vezes quanto os da v396 na entrada
    assert set(RE_V_QUALQUER.findall(txt)) <= {"396", "397", "398"}, (nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_VB.search(txt) and not RE_V6.search(txt) and "vb14" not in txt
    for velho, novo in (("PINOS_BN_v396.json", "PINOS_BN_v397.json"), ("PINOS_BATERIA_v396.json", "PINOS_BATERIA_v397.json")):
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
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v398.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens"], ensure_ascii=False))
