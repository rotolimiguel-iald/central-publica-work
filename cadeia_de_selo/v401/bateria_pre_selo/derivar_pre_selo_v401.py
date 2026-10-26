# -*- coding: utf-8 -*-
"""derivar_pre_selo_v401.py -- deriva, dos cinco arquivos da v399 (bateria_pre_selo; os que GERARAM um recibo pre_selo NOVO em ensaio), os da v401 por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea (sem encadear): v399 -> v401 (nome da cadeia/saida), v398 -> v400 (o estado de hoje: o Nos e o pino da Bancada), v397 -> v399 (a versao ANTES da anterior,
do controle negativo "selo anterior errado"), vb16 -> vb18 (sandbox curto), V8 -> V10 (variavel de caminho da cadeia anterior: V<k> = v<39k>/v<4kk>; V10 = ...\\v400), SELO_V397/KM_V397 -> SELO_V399/KM_V399.
Contrato desta rodada (diferente da v400, que REUSOU o recibo da v399): aqui o recibo e' GERADO NOVO, antes da instalacao da v401, em ensaio contra a Bancada de producao que ja' pina a v400 (B9) -- passo simples v400 -> v401.
Regras especiais, cada uma com contagem exata (assert): o selo e o manifesto do kernel ANTERIORES (v400) saem de V\\base_v400 (a raiz da cadeia: pasta existente, copia de bytes do Nos); o selo e o manifesto da versao
ANTES da anterior (v399) saem de V10\\base_v399 (= v400\\base_v399). Tudo ou nada: as saidas sao calculadas e conferidas antes de gravar a primeira.
Entrada: so' a v399\\bateria_pre_selo\\ (leitura). Saida: os arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v401.json com sha256 de entrada e de saida. Nada e' executado aqui (so' ast.parse).
uso: python -I -B -X utf8 derivar_pre_selo_v401.py"""
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
FONTE = os.path.join(CS, "v399", "bateria_pre_selo")

# (nome na fonte, nome na saida, tipo)
ARQ = [("gerar_pino_recibo_pre_selo_v399.py", "gerar_pino_recibo_pre_selo_v401.py"),
       ("conferir_recibo_pre_selo_v399.py", "conferir_recibo_pre_selo_v401.py"),
       ("snap_producao_v399.py", "snap_producao_v401.py"),
       ("rodar_ensaio_1_pre_selo_v399.sh", "rodar_ensaio_1_pre_selo_v401.sh"),
       ("limpar_sandbox_vb16.py", "limpar_sandbox_vb18.py")]
MAPA = {"v399": "v401", "v398": "v400", "v397": "v399"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(39[789])(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])")
RE_V_MAIUSCULO = re.compile(r"V3[0-9][0-9]|V4[0-9][0-9]")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb16(?![0-9])")
RE_V8 = re.compile(r"(?<![0-9A-Za-z_])V8(?![0-9A-Za-z_])")
RE_V10 = re.compile(r"(?<![0-9A-Za-z_])V10(?![0-9A-Za-z_])")
# contagens exatas esperadas (medidas nas fontes v399 por inventario antes de escrever este derivador)
ESP_VER = {"gerar_pino_recibo_pre_selo_v399.py": {"v399": 27, "v398": 11, "v397": 0},
           "conferir_recibo_pre_selo_v399.py": {"v399": 14, "v398": 15, "v397": 3},
           "snap_producao_v399.py": {"v399": 4, "v398": 0, "v397": 0},
           "rodar_ensaio_1_pre_selo_v399.sh": {"v399": 4, "v398": 16, "v397": 0},
           "limpar_sandbox_vb16.py": {"v399": 3, "v398": 0, "v397": 0}}
ESP_VB = {"gerar_pino_recibo_pre_selo_v399.py": 2, "conferir_recibo_pre_selo_v399.py": 3, "snap_producao_v399.py": 0, "rodar_ensaio_1_pre_selo_v399.sh": 0, "limpar_sandbox_vb16.py": 11}
ESP_V8 = {"gerar_pino_recibo_pre_selo_v399.py": 3, "conferir_recibo_pre_selo_v399.py": 5, "snap_producao_v399.py": 0, "rodar_ensaio_1_pre_selo_v399.sh": 5, "limpar_sandbox_vb16.py": 0}


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v401", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens": {}, "ast_parse": {}}
prontos = []
for src_nome, dst_nome in ARQ:
    src = os.path.join(FONTE, src_nome)
    dst = os.path.join(HERE, dst_nome)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    # entrada: so' v397 / v398 / v399 em minusculo; V3xx maiusculo so' as quatro variaveis SELO_V397/KM_V397 do conferir; nenhum V10 pre-existente
    assert set(RE_V_QUALQUER.findall(txt)) <= {"397", "398", "399"}, (src_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    n_mai = len(RE_V_MAIUSCULO.findall(txt))
    assert n_mai == (4 if src_nome.startswith("conferir_") else 0), (src_nome, n_mai)
    assert not RE_V10.search(txt), ("ja existe uma variavel V10 na fonte", src_nome)
    n_pinos = {p: txt.count(p) for p in ("PINOS_BN_v398.json", "PINOS_BATERIA_v398.json")}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    cont = {}
    txt, cont["versoes"] = RE_V.subn(sub_v, txt)        # passagem unica e simultanea: v399->v401, v398->v400, v397->v399 sem encadear
    cont["versoes_por_token"] = dict(por_token)
    assert cont["versoes_por_token"] == ESP_VER[src_nome], (src_nome, "versoes por token", cont["versoes_por_token"], ESP_VER[src_nome])
    assert cont["versoes"] == sum(por_token.values())
    txt, cont["vb16_para_vb18"] = RE_VB.subn("vb18", txt)
    assert cont["vb16_para_vb18"] == ESP_VB[src_nome], (src_nome, "vb16", cont["vb16_para_vb18"], ESP_VB[src_nome])
    txt, cont["V8_para_V10"] = RE_V8.subn("V10", txt)
    assert cont["V8_para_V10"] == ESP_V8[src_nome], (src_nome, "V8", cont["V8_para_V10"], ESP_V8[src_nome])
    if src_nome.startswith("conferir_"):
        # o selo e o manifesto do kernel ANTERIORES (v400) saem de V\base_v400 (a raiz da cadeia); nenhum uso de HERE\base_v39x/v40x
        a = 'os.path.join(V, "base_v400"'
        assert txt.count(a) == 2, ("base_v400 em V", txt.count(a))
        assert txt.count('os.path.join(HERE, "base_v') == 0
        cont["base_v400_em_V"] = 2
        # o selo e o manifesto da versao antes da anterior (v399) saem de V10\base_v399 (= v400\base_v399)
        assert txt.count('os.path.join(V10, "base_v399"') == 2, "o selo e o manifesto da versao antes da anterior (v399) saem de V10\\base_v399"
        cont["base_v399_em_V10"] = 2
        for velho, novo in (("SELO_V397", "SELO_V399"), ("KM_V397", "KM_V399")):
            assert txt.count(velho) == 2, (velho, txt.count(velho))
            txt = txt.replace(velho, novo)
            cont[velho + "_para_" + novo] = 2
        assert "V397" not in txt
        a = '"RECIBO_SINCRONIZACAO_v400_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if src_nome.startswith("gerar_pino"):
        a = '"RECIBO_SINCRONIZACAO_v400_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
        # docstring: o molde citado e' o da v399 (a v400 reusou o recibo e nao tem gerador proprio nesta pasta)
        velho = "Molde: v400\\\\bateria_pre_selo\\\\gerar_pino_recibo_pre_selo_v400.py"
        novo = "Molde: v399\\\\bateria_pre_selo\\\\gerar_pino_recibo_pre_selo_v399.py"
        assert txt.count(velho) == 1, ("molde citado", txt.count(velho))
        txt = txt.replace(velho, novo)
        cont["molde_citado_v399"] = 1
    if src_nome.startswith("rodar_ensaio"):
        a = "--versao v400 --fase pre_selo --modo ensaio"
        assert txt.count(a) == 1, ("lancador: versao do ensaio", txt.count(a))
    # saida: nenhuma referencia fora de v399 / v400 / v401, nenhum vb16 nem V8 residual; os pinos da v400 aparecem tantas vezes quanto os da v398 na entrada
    assert set(RE_V_QUALQUER.findall(txt)) <= {"399", "400", "401"}, (dst_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_VB.search(txt) and not RE_V8.search(txt) and "vb16" not in txt
    for velho, novo in (("PINOS_BN_v398.json", "PINOS_BN_v400.json"), ("PINOS_BATERIA_v398.json", "PINOS_BATERIA_v400.json")):
        assert txt.count(novo) == n_pinos[velho], (dst_nome, novo, txt.count(novo), n_pinos[velho])
    if dst_nome.endswith(".py"):
        ast.parse(txt)
        rel["ast_parse"][dst_nome] = "ok"
    out = txt.encode("utf-8")
    prontos.append((dst_nome, src, dst, raw, out, cont))

for nome, src, dst, raw, out, cont in prontos:     # so' aqui comeca a gravar: as saidas ja passaram em todas as regras
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
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v401.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens"], ensure_ascii=False))
