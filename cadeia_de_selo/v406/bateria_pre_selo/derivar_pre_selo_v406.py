# -*- coding: utf-8 -*-
"""derivar_pre_selo_v406.py -- deriva, dos cinco arquivos da v405 (v405\\bateria_pre_selo; os que GERARAM um recibo pre_selo NOVO em ensaio e que RODARAM de verdade em 28/10), os da v406 por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea (sem encadear): v405 -> v406 (nome da cadeia/saida), v403 -> v405 (o estado de hoje: o Nos e o pino da Bancada), v402 -> v403 (a versao ANTES da anterior, do controle negativo "selo anterior errado"),
V13 -> V14 (variavel de caminho da cadeia anterior), SELO_V402/KM_V402 -> SELO_V403/KM_V403, (B12) -> (B14) (o pino da Bancada de producao hoje: B14-v405-20261102-R1) e «em 28/10 -> em 01/11». O sandbox curto SEGUE vb21 (decisao da v406: o orquestrador cobra esse caminho ausente; ele foi limpo pela v405).
Contrato desta rodada (o mesmo da v405): o recibo e' GERADO NOVO, antes da instalacao da v406, em ensaio contra a Bancada de producao que ja' pina a v405 (B14) -- passo simples v405 -> v406.
CONTAGENS MEDIDAS NA FONTE: este derivador NAO afirma numeros digitados; ele MEDE as ocorrencias de cada token, grava no recibo e confere INVARIANTES (a saida so' tem tokens permitidos; nenhum token velho sobra). Tudo ou nada: as saidas sao calculadas e conferidas antes de gravar a primeira.
Entrada: so' a v405\\bateria_pre_selo\\ (leitura). Saida: os arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v406.json. Nada e' executado aqui (so' ast.parse). Molde: v405\\bateria_pre_selo\\derivar_pre_selo_v405.py.
uso: python -I -B -X utf8 derivar_pre_selo_v406.py"""
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
FONTE = os.path.join(CS, "v405", "bateria_pre_selo")
ARQ = [("gerar_pino_recibo_pre_selo_v405.py", "gerar_pino_recibo_pre_selo_v406.py"),
       ("conferir_recibo_pre_selo_v405.py", "conferir_recibo_pre_selo_v406.py"),
       ("snap_producao_v405.py", "snap_producao_v406.py"),
       ("rodar_ensaio_1_pre_selo_v405.sh", "rodar_ensaio_1_pre_selo_v406.sh"),
       ("limpar_sandbox_vb21.py", "limpar_sandbox_vb21.py")]
MAPA = {"v405": "v406", "v403": "v405", "v402": "v403"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(402|403|405)(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])")
RE_V13 = re.compile(r"(?<![0-9A-Za-z_])V13(?![0-9A-Za-z_])")
RE_V14 = re.compile(r"(?<![0-9A-Za-z_])V14(?![0-9A-Za-z_])")


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v406", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens_medidas": {}, "ast_parse": {}}
prontos = []
for src_nome, dst_nome in ARQ:
    src = os.path.join(FONTE, src_nome)
    dst = os.path.join(HERE, dst_nome)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    assert set(RE_V_QUALQUER.findall(txt)) <= {"402", "403", "405"}, (src_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_V14.search(txt) and "v406" not in txt, ("a fonte ja cita V14 ou v406", src_nome)
    medido = {"versoes_por_token": {k: len(re.findall(r"(?<![0-9A-Za-z])%s(?![0-9])" % k, txt)) for k in MAPA}, "V13": len(RE_V13.findall(txt)), "SELO_V402": txt.count("SELO_V402"), "KM_V402": txt.count("KM_V402"), "(B12)": txt.count("(B12)"), "em_28/10": txt.count("em 28/10"),
              "PINOS_BN_v403": txt.count("PINOS_BN_v403.json"), "PINOS_BATERIA_v403": txt.count("PINOS_BATERIA_v403.json")}
    cont = {}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    txt, cont["versoes"] = RE_V.subn(sub_v, txt)        # passagem unica e simultanea: sem encadear
    assert por_token == medido["versoes_por_token"] and cont["versoes"] == sum(por_token.values())
    txt, cont["V13_para_V14"] = RE_V13.subn("V14", txt)
    for velho, novo in (("SELO_V402", "SELO_V403"), ("KM_V402", "KM_V403")):
        cont[velho + "_para_" + novo] = txt.count(velho)
        txt = txt.replace(velho, novo)
    cont["(B12)_para_(B14)"] = txt.count("(B12)"); txt = txt.replace("(B12)", "(B14)")
    cont["data_das_fontes_28/10_para_01/11"] = txt.count("em 28/10"); txt = txt.replace("em 28/10", "em 01/11")
    # invariantes da saida
    assert set(RE_V_QUALQUER.findall(txt)) <= {"403", "405", "406"}, (dst_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_V13.search(txt) and "SELO_V402" not in txt and "KM_V402" not in txt
    for velho, novo in (("PINOS_BN_v403.json", "PINOS_BN_v405.json"), ("PINOS_BATERIA_v403.json", "PINOS_BATERIA_v405.json")):
        assert txt.count(novo) == medido[velho.replace(".json", "")], (dst_nome, novo, txt.count(novo), medido[velho.replace(".json", "")])
    if src_nome.startswith("conferir_"):
        # o selo e o manifesto do kernel ANTERIORES (v405) saem de V\base_v405 (a raiz da cadeia); o da versao antes da anterior (v403) de V14\base_v403 (= v405\base_v403)
        assert txt.count('os.path.join(V, "base_v405"') == 2 and txt.count('os.path.join(V14, "base_v403"') == 2, ("bases anteriores", txt.count('os.path.join(V, "base_v405"'), txt.count('os.path.join(V14, "base_v403"'))
        assert txt.count('os.path.join(HERE, "base_v') == 0
    if src_nome.startswith("rodar_ensaio"):
        assert txt.count("--versao v405 --fase pre_selo --modo ensaio") == 1, ("lancador: versao do ensaio", txt.count("--versao v405 --fase pre_selo --modo ensaio"))
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
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v406.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens_medidas"], ensure_ascii=False))
