# -*- coding: utf-8 -*-
"""derivar_pre_selo_v404.py -- deriva, dos cinco arquivos da v403 (v403\\bateria_pre_selo; os que GERARAM um recibo pre_selo NOVO em ensaio e que RODARAM de verdade em 27/10), os da v404 por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea (sem encadear): v403 -> v404 (nome da cadeia/saida), v402 -> v403 (o estado de hoje: o Nos e o pino da Bancada), v401 -> v402 (a versao ANTES da anterior, do controle negativo "selo anterior errado"),
vb20 -> vb21 (sandbox curto), V12 -> V13 (variavel de caminho da cadeia anterior: V<k> = v<39k>/v<4kk>; V13 = ...\\v403), SELO_V401/KM_V401 -> SELO_V402/KM_V402, (B11) -> (B12) (o pino da Bancada de producao hoje: B12-v403-20261028-R1) e «27/10 -> 28/10».
Contrato desta rodada (o mesmo da v403): o recibo e' GERADO NOVO, antes da instalacao da v404, em ensaio contra a Bancada de producao que ja' pina a v403 (B12) -- passo simples v403 -> v404.
CONTAGENS MEDIDAS NA FONTE (licao 1 de 28/10/2026): este derivador NAO afirma numeros digitados; ele MEDE o numero de ocorrencias de cada token em cada arquivo-fonte, grava os numeros medidos no recibo e confere apenas INVARIANTES (a saida so' tem tokens permitidos; nenhum token velho sobra; a contagem de cada token
da saida == a da entrada). Tudo ou nada: as saidas sao calculadas e conferidas antes de gravar a primeira.
Entrada: so' a v403\\bateria_pre_selo\\ (leitura). Saida: os arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v404.json com sha256 de entrada e de saida. Nada e' executado aqui (so' ast.parse). Molde: v403\\bateria_pre_selo\\derivar_pre_selo_v403.py.
uso: python -I -B -X utf8 derivar_pre_selo_v404.py"""
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
CS = os.path.dirname(V)
FONTE = os.path.join(CS, "v403", "bateria_pre_selo")
ARQ = [("gerar_pino_recibo_pre_selo_v403.py", "gerar_pino_recibo_pre_selo_v404.py"),
       ("conferir_recibo_pre_selo_v403.py", "conferir_recibo_pre_selo_v404.py"),
       ("snap_producao_v403.py", "snap_producao_v404.py"),
       ("rodar_ensaio_1_pre_selo_v403.sh", "rodar_ensaio_1_pre_selo_v404.sh"),
       ("limpar_sandbox_vb20.py", "limpar_sandbox_vb21.py")]
MAPA = {"v403": "v404", "v402": "v403", "v401": "v402"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(401|402|403)(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb20(?![0-9])")
RE_V12 = re.compile(r"(?<![0-9A-Za-z_])V12(?![0-9A-Za-z_])")
RE_V13 = re.compile(r"(?<![0-9A-Za-z_])V13(?![0-9A-Za-z_])")


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v404", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens_medidas": {}, "ast_parse": {}}
prontos = []
for src_nome, dst_nome in ARQ:
    src = os.path.join(FONTE, src_nome)
    dst = os.path.join(HERE, dst_nome)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    # entrada: so' v401 / v402 / v403 em minusculo; nenhum V13 pre-existente, nenhum vb21, nenhum v404
    assert set(RE_V_QUALQUER.findall(txt)) <= {"401", "402", "403"}, (src_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_V13.search(txt), ("ja existe uma variavel V13 na fonte", src_nome)
    assert "vb21" not in txt and "v404" not in txt, ("a fonte ja cita vb21 ou v404", src_nome)
    medido = {"versoes_por_token": {k: len(re.findall(r"(?<![0-9A-Za-z])%s(?![0-9])" % k, txt)) for k in MAPA}, "vb20": len(RE_VB.findall(txt)), "V12": len(RE_V12.findall(txt)),
              "SELO_V401": txt.count("SELO_V401"), "KM_V401": txt.count("KM_V401"), "(B11)": txt.count("(B11)"), "em_27/10": txt.count("em 27/10"),
              "PINOS_BN_v402": txt.count("PINOS_BN_v402.json"), "PINOS_BATERIA_v402": txt.count("PINOS_BATERIA_v402.json")}
    cont = {}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    txt, cont["versoes"] = RE_V.subn(sub_v, txt)        # passagem unica e simultanea: v403->v404, v402->v403, v401->v402 sem encadear
    assert por_token == medido["versoes_por_token"] and cont["versoes"] == sum(por_token.values())
    txt, cont["vb20_para_vb21"] = RE_VB.subn("vb21", txt)
    txt, cont["V12_para_V13"] = RE_V12.subn("V13", txt)
    for velho, novo in (("SELO_V401", "SELO_V402"), ("KM_V401", "KM_V402")):
        cont[velho + "_para_" + novo] = txt.count(velho)
        txt = txt.replace(velho, novo)
    cont["(B11)_para_(B12)"] = txt.count("(B11)"); txt = txt.replace("(B11)", "(B12)")
    cont["data_das_fontes_27/10_para_28/10"] = txt.count("em 27/10"); txt = txt.replace("em 27/10", "em 28/10")
    # invariantes da saida
    assert set(RE_V_QUALQUER.findall(txt)) <= {"402", "403", "404"}, (dst_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_VB.search(txt) and "vb20" not in txt and not RE_V12.search(txt) and "SELO_V401" not in txt and "KM_V401" not in txt
    for velho, novo in (("PINOS_BN_v402.json", "PINOS_BN_v403.json"), ("PINOS_BATERIA_v402.json", "PINOS_BATERIA_v403.json")):
        assert txt.count(novo) == medido[velho.replace(".json", "")], (dst_nome, novo, txt.count(novo), medido[velho.replace(".json", "")])
    if src_nome.startswith("conferir_"):
        # o selo e o manifesto do kernel ANTERIORES (v403) saem de V\base_v403 (a raiz da cadeia); o da versao antes da anterior (v402) de V13\base_v402 (= v403\base_v402)
        assert txt.count('os.path.join(V, "base_v403"') == 2 and txt.count('os.path.join(V13, "base_v402"') == 2, ("bases anteriores", txt.count('os.path.join(V, "base_v403"'), txt.count('os.path.join(V13, "base_v402"'))
        assert txt.count('os.path.join(HERE, "base_v') == 0
    if src_nome.startswith("rodar_ensaio"):
        assert txt.count("--versao v403 --fase pre_selo --modo ensaio") == 1, ("lancador: versao do ensaio", txt.count("--versao v403 --fase pre_selo --modo ensaio"))
    if dst_nome.endswith(".py"):
        ast.parse(txt)
        rel["ast_parse"][dst_nome] = "ok"
    out = txt.encode("utf-8")
    prontos.append((dst_nome, src, dst, raw, out, dict(cont, medido=medido)))

for nome, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: as saidas ja passaram em todas as regras
    with open(dst + ".tmp", "wb") as fh:
        fh.write(out)
    assert os.path.getsize(dst + ".tmp") == len(out)
    os.replace(dst + ".tmp", dst)
    rel["entradas"][nome] = {"path": src, "sha256": sha(raw), "bytes": len(raw)}
    rel["saidas"][nome] = {"path": dst, "sha256": sha(open(dst, "rb").read()), "bytes": len(out)}
    assert rel["saidas"][nome]["sha256"] == sha(out)
    rel["contagens_medidas"][nome] = cont
me = os.path.abspath(__file__)
rel["script"] = {"path": me, "sha256": sha(open(me, "rb").read())}
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v404.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens_medidas"], ensure_ascii=False))
