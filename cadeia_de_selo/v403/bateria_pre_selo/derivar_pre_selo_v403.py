# -*- coding: utf-8 -*-
"""derivar_pre_selo_v403.py -- deriva, dos cinco arquivos da v402 (bateria_pre_selo; os que GERARAM um recibo pre_selo NOVO em ensaio e que RODARAM de verdade em 26/10), os da v403 por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea (sem encadear): v402 -> v403 (nome da cadeia/saida), v401 -> v402 (o estado de hoje: o Nos e o pino da Bancada), v400 -> v401 (a versao ANTES da anterior,
do controle negativo "selo anterior errado"), vb19 -> vb20 (sandbox curto), V11 -> V12 (variavel de caminho da cadeia anterior: V<k> = v<39k>/v<4kk>; V12 = ...\\v402), SELO_V400/KM_V400 -> SELO_V401/KM_V401.
Contrato desta rodada (o mesmo da v402): o recibo e' GERADO NOVO, antes da instalacao da v403, em ensaio contra a Bancada de producao que ja' pina a v402 (B11) -- passo simples v402 -> v403.
Regras especiais, cada uma com contagem exata (assert): o selo e o manifesto do kernel ANTERIORES (v402) saem de V\\base_v402 (a raiz da cadeia: pasta existente, copia de bytes do Nos); o selo e o manifesto da versao
ANTES da anterior (v401) saem de V12\\base_v401 (= v402\\base_v401). Tudo ou nada: as saidas sao calculadas e conferidas antes de gravar a primeira.
Entrada: so' a v402\\bateria_pre_selo\\ (leitura). Saida: os arquivos novos (nao sobrescreve) + DERIVACAO_PRE_SELO_v403.json com sha256 de entrada e de saida. Nada e' executado aqui (so' ast.parse).
uso: python -I -B -X utf8 derivar_pre_selo_v403.py"""
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
FONTE = os.path.join(CS, "v402", "bateria_pre_selo")

# (nome na fonte, nome na saida)
ARQ = [("gerar_pino_recibo_pre_selo_v402.py", "gerar_pino_recibo_pre_selo_v403.py"),
       ("conferir_recibo_pre_selo_v402.py", "conferir_recibo_pre_selo_v403.py"),
       ("snap_producao_v402.py", "snap_producao_v403.py"),
       ("rodar_ensaio_1_pre_selo_v402.sh", "rodar_ensaio_1_pre_selo_v403.sh"),
       ("limpar_sandbox_vb19.py", "limpar_sandbox_vb20.py")]
MAPA = {"v402": "v403", "v401": "v402", "v400": "v401"}
RE_V = re.compile(r"(?<![0-9A-Za-z])v(400|401|402)(?![0-9])")
RE_V_QUALQUER = re.compile(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])")
RE_V_MAIUSCULO = re.compile(r"V3[0-9][0-9]|V4[0-9][0-9]")
RE_VB = re.compile(r"(?<![0-9A-Za-z])vb19(?![0-9])")
RE_V11 = re.compile(r"(?<![0-9A-Za-z_])V11(?![0-9A-Za-z_])")
RE_V12 = re.compile(r"(?<![0-9A-Za-z_])V12(?![0-9A-Za-z_])")
# contagens exatas esperadas (medidas nas fontes v402 por inventario antes de escrever este derivador)
ESP_VER = {"gerar_pino_recibo_pre_selo_v402.py": {"v402": 27, "v401": 11, "v400": 0},   # medido na fonte v402 (a regra do molde da v402 ja' havia trocado 2 v400 por v401)
           "conferir_recibo_pre_selo_v402.py": {"v402": 14, "v401": 15, "v400": 3},
           "snap_producao_v402.py": {"v402": 4, "v401": 0, "v400": 0},
           "rodar_ensaio_1_pre_selo_v402.sh": {"v402": 4, "v401": 16, "v400": 0},
           "limpar_sandbox_vb19.py": {"v402": 3, "v401": 0, "v400": 0}}
ESP_VB = {"gerar_pino_recibo_pre_selo_v402.py": 2, "conferir_recibo_pre_selo_v402.py": 3, "snap_producao_v402.py": 0, "rodar_ensaio_1_pre_selo_v402.sh": 0, "limpar_sandbox_vb19.py": 11}
ESP_V11 = {"gerar_pino_recibo_pre_selo_v402.py": 3, "conferir_recibo_pre_selo_v402.py": 5, "snap_producao_v402.py": 0, "rodar_ensaio_1_pre_selo_v402.sh": 5, "limpar_sandbox_vb19.py": 0}


def sha(b):
    return hashlib.sha256(b).hexdigest()


rel = {"contrato": "DERIVACAO_PRE_SELO_v403", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "mapa_de_versoes": MAPA, "script": None, "entradas": {}, "saidas": {}, "contagens": {}, "ast_parse": {}}
prontos = []
for src_nome, dst_nome in ARQ:
    src = os.path.join(FONTE, src_nome)
    dst = os.path.join(HERE, dst_nome)
    if os.path.exists(dst):
        raise SystemExit("ja existe, nao sobrescrevo: " + dst)
    raw = open(src, "rb").read()
    assert b"\r" not in raw, ("a fonte tem CR: " + src)
    txt = raw.decode("utf-8")
    # entrada: so' v400 / v401 / v402 em minusculo; V3xx maiusculo so' as quatro variaveis SELO_V400/KM_V400 do conferir; nenhum V12 pre-existente, nenhum vb20, nenhum v403
    assert set(RE_V_QUALQUER.findall(txt)) <= {"400", "401", "402"}, (src_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    n_mai = len(RE_V_MAIUSCULO.findall(txt))
    assert n_mai == (4 if src_nome.startswith("conferir_") else 0), (src_nome, n_mai)
    assert not RE_V12.search(txt), ("ja existe uma variavel V12 na fonte", src_nome)
    assert "vb20" not in txt and "v403" not in txt, ("a fonte ja cita vb20 ou v403", src_nome)
    n_pinos = {p: txt.count(p) for p in ("PINOS_BN_v401.json", "PINOS_BATERIA_v401.json")}
    por_token = {k: 0 for k in MAPA}

    def sub_v(m):
        k = "v" + m.group(1)
        por_token[k] += 1
        return MAPA[k]

    cont = {}
    txt, cont["versoes"] = RE_V.subn(sub_v, txt)        # passagem unica e simultanea: v402->v403, v401->v402, v400->v401 sem encadear
    cont["versoes_por_token"] = dict(por_token)
    assert cont["versoes_por_token"] == ESP_VER[src_nome], (src_nome, "versoes por token", cont["versoes_por_token"], ESP_VER[src_nome])
    assert cont["versoes"] == sum(por_token.values())
    txt, cont["vb19_para_vb20"] = RE_VB.subn("vb20", txt)
    assert cont["vb19_para_vb20"] == ESP_VB[src_nome], (src_nome, "vb19", cont["vb19_para_vb20"], ESP_VB[src_nome])
    txt, cont["V11_para_V12"] = RE_V11.subn("V12", txt)
    assert cont["V11_para_V12"] == ESP_V11[src_nome], (src_nome, "V11", cont["V11_para_V12"], ESP_V11[src_nome])
    if src_nome.startswith("conferir_"):
        # o selo e o manifesto do kernel ANTERIORES (v402) saem de V\base_v402 (a raiz da cadeia); nenhum uso de HERE\base_v39x/v40x
        a = 'os.path.join(V, "base_v402"'
        assert txt.count(a) == 2, ("base_v402 em V", txt.count(a))
        assert txt.count('os.path.join(HERE, "base_v') == 0
        cont["base_v402_em_V"] = 2
        # o selo e o manifesto da versao antes da anterior (v401) saem de V12\base_v401 (= v402\base_v401)
        assert txt.count('os.path.join(V12, "base_v401"') == 2, "o selo e o manifesto da versao antes da anterior (v401) saem de V12\\base_v401"
        cont["base_v401_em_V12"] = 2
        for velho, novo in (("SELO_V400", "SELO_V401"), ("KM_V400", "KM_V401")):
            assert txt.count(velho) == 2, (velho, txt.count(velho))
            txt = txt.replace(velho, novo)
            cont[velho + "_para_" + novo] = 2
        assert "V400" not in txt
        a = '"RECIBO_SINCRONIZACAO_v402_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
    if src_nome.startswith("gerar_pino"):
        a = '"RECIBO_SINCRONIZACAO_v402_*.json"'
        assert txt.count(a) == 1, ("glob do recibo do esboco", txt.count(a))
        # docstring: o molde citado e' o da v402 (o gerador que RODOU de verdade em 26/10); a subida simultanea o teria levado a v401, que nao existe nesta pasta
        novo = "Molde: v402\\\\bateria_pre_selo\\\\gerar_pino_recibo_pre_selo_v402.py"
        assert txt.count(novo) == 1, ("molde citado", txt.count(novo))   # a subida simultanea ja' cita o molde certo (v402, o gerador que rodou em 26/10); nada a trocar
        cont["molde_citado_v402"] = 1
    if src_nome.startswith("rodar_ensaio"):
        a = "--versao v402 --fase pre_selo --modo ensaio"
        assert txt.count(a) == 1, ("lancador: versao do ensaio", txt.count(a))
    # saida: nenhuma referencia fora de v401 / v402 / v403, nenhum vb19 nem V11 residual; os pinos da v402 aparecem tantas vezes quanto os da v401 na entrada
    assert set(RE_V_QUALQUER.findall(txt)) <= {"401", "402", "403"}, (dst_nome, sorted(set(RE_V_QUALQUER.findall(txt))))
    assert not RE_VB.search(txt) and not RE_V11.search(txt) and "vb19" not in txt
    for velho, novo in (("PINOS_BN_v401.json", "PINOS_BN_v402.json"), ("PINOS_BATERIA_v401.json", "PINOS_BATERIA_v402.json")):
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
dst = os.path.join(HERE, "DERIVACAO_PRE_SELO_v403.json")
if os.path.exists(dst):
    raise SystemExit("ja existe: " + dst)
with open(dst + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(rel["contagens"], ensure_ascii=False))
