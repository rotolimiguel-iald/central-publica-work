# -*- coding: utf-8 -*-
"""derivar_derivador_pre_selo_v403.py -- deriva v403\\bateria_pre_selo\\derivar_pre_selo_v403.py de v402\\bateria_pre_selo\\derivar_pre_selo_v402.py por SUBIDA DE VERSAO com fronteira de digitos,
numa PASSAGEM UNICA e simultanea (sem encadear): v399->v400, v400->v401, v401->v402, v402->v403; vb18->vb19, vb19->vb20; V10->V11, V11->V12 (variaveis de caminho e os identificadores RE_V1x/ESP_V1x);
V399->V400, V400->V401 (SELO_V*/KM_V*); B10->B11 (o pino da Bancada de producao hoje); «25/10»->«26/10» (a data em que os arquivos-fonte RODARAM de verdade).
Nada e' executado aqui (so' ast.parse); a saida nao sobrescreve. Gera DERIVACAO_DO_DERIVADOR_v403.json com sha256 de entrada e saida e as contagens.
uso: python -I -B -X utf8 derivar_derivador_pre_selo_v403.py"""
import ast, hashlib, json, os, re, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE); CS = os.path.dirname(V)
SRC = os.path.join(CS, "v402", "bateria_pre_selo", "derivar_pre_selo_v402.py")
DST = os.path.join(HERE, "derivar_pre_selo_v403.py")
if os.path.exists(DST):
    raise SystemExit("ja existe, nao sobrescrevo: " + DST)
raw = open(SRC, "rb").read(); assert b"\r" not in raw
txt = raw.decode("utf-8")
cont = {}
def bump(pat, grupo_para_novo, nome):
    global txt
    n = [0]
    def f(m):
        n[0] += 1
        return grupo_para_novo(m)
    txt = re.sub(pat, f, txt); cont[nome] = n[0]
# versoes minusculas, simultaneo
assert set(re.findall(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])", txt)) <= {"399", "400", "401", "402"}
bump(r"(?<![0-9A-Za-z])v(399|400|401|402)(?![0-9])", lambda m: "v%d" % (int(m.group(1)) + 1), "v_minusculo")
# sandbox curto
assert "vb20" not in txt
bump(r"(?<![0-9A-Za-z])vb(18|19)(?![0-9])", lambda m: "vb%d" % (int(m.group(1)) + 1), "vb")
# variaveis V10/V11 (e identificadores RE_V10/RE_V11/ESP_V10 e a chave V10_para_V11)
assert "V12" not in txt
bump(r"(?<![0-9A-Za-z])V1(0|1)(?![0-9])", lambda m: "V1%d" % (int(m.group(1)) + 1), "V1x")
# SELO_V399/KM_V399 e SELO_V400/KM_V400
assert "V401" not in txt
bump(r"(?<![0-9A-Za-z])V(399|400)(?![0-9])", lambda m: "V%d" % (int(m.group(1)) + 1), "V_maiusculo")
# os numeros NUS das alternancias v(399|400|401) e dos conjuntos {"399", "400", "401"} / {"400", "401", "402"} (nao vem precedidos de v): +1, simultaneo
bump(r'(?<=[(|"])(399|400|401|402)(?=[|)"])', lambda m: "%d" % (int(m.group(1)) + 1), "numeros_nus")
assert cont["numeros_nus"] == 9, cont
# o pino da Bancada hoje e a data em que as fontes rodaram
assert txt.count("(B10)") == 1 and "B11" not in txt
txt = txt.replace("(B10)", "(B11)"); cont["B10_para_B11"] = 1
assert txt.count("em 25/10") == 2   # a docstring (RODARAM em 25/10) e o comentario do molde citado (RODOU em 25/10): as fontes da v403 rodaram em 26/10
txt = txt.replace("em 25/10", "em 26/10"); cont["data_das_fontes"] = 2
# duas regras que NAO sobem por digito (medidas na fonte v402 em 27/10/2026):
# (a) o gerar_pino da v402 ja' cita o molde certo (a v401, o gerador que rodou em 25/10) -- a regra especial da v402 trocou 2 tokens v400 por v401 DEPOIS da contagem;
#     logo a fonte v402 conta {v402: 27, v401: 11, v400: 0}, nao {27, 9, 2};
velho = '"gerar_pino_recibo_pre_selo_v402.py": {"v402": 27, "v401": 9, "v400": 2},'
assert txt.count(velho) == 1, ("ESP_VER do gerar_pino", txt.count(velho))
txt = txt.replace(velho, '"gerar_pino_recibo_pre_selo_v402.py": {"v402": 27, "v401": 11, "v400": 0},   # medido na fonte v402 (a regra do molde da v402 ja\' havia trocado 2 v400 por v401)')
cont["esp_ver_gerar_pino_medido"] = 1
# (b) a subida simultanea v401->v402 ja' leva o molde citado ao certo («Molde: v402\\...v402.py», o gerador que rodou em 26/10): confere-se, nada se troca
velho = ('        velho = "Molde: v401\\\\\\\\bateria_pre_selo\\\\\\\\gerar_pino_recibo_pre_selo_v401.py"\n'
         '        novo = "Molde: v402\\\\\\\\bateria_pre_selo\\\\\\\\gerar_pino_recibo_pre_selo_v402.py"\n'
         '        assert txt.count(velho) == 1, ("molde citado", txt.count(velho))\n'
         '        txt = txt.replace(velho, novo)\n'
         '        cont["molde_citado_v402"] = 1\n')
assert txt.count(velho) == 1, ("bloco do molde citado", txt.count(velho))
txt = txt.replace(velho, ('        novo = "Molde: v402\\\\\\\\bateria_pre_selo\\\\\\\\gerar_pino_recibo_pre_selo_v402.py"\n'
                          '        assert txt.count(novo) == 1, ("molde citado", txt.count(novo))   # a subida simultanea ja\' cita o molde certo (v402, o gerador que rodou em 26/10); nada a trocar\n'
                          '        cont["molde_citado_v402"] = 1\n'))
cont["regra_do_molde_citado"] = "conferida, nao trocada"
# conferencias da saida
assert set(re.findall(r"(?<![0-9A-Za-z])v(3[0-9][0-9]|4[0-9][0-9])(?![0-9])", txt)) <= {"400", "401", "402", "403"}
assert "vb18" not in txt and "V10" not in txt and "V399" not in txt
assert 'FONTE = os.path.join(CS, "v402", "bateria_pre_selo")' in txt
assert 'MAPA = {"v402": "v403", "v401": "v402", "v400": "v401"}' in txt
assert 'RE_V = re.compile(r"(?<![0-9A-Za-z])v(400|401|402)(?![0-9])")' in txt
assert '("limpar_sandbox_vb19.py", "limpar_sandbox_vb20.py")' in txt
assert 'a = "--versao v402 --fase pre_selo --modo ensaio"' in txt
assert "DERIVACAO_PRE_SELO_v403" in txt and 'os.path.join(V, "base_v402"' in txt and 'os.path.join(V12, "base_v401"' in txt
assert 'for velho, novo in (("SELO_V400", "SELO_V401"), ("KM_V400", "KM_V401")):' in txt and "V399" not in txt   # a tupla de substituicao subiu um degrau; nenhum V399 sobra
cont["SELO_V400_SELO_V401_KM_V400_KM_V401"] = [txt.count(k) for k in ("SELO_V400", "SELO_V401", "KM_V400", "KM_V401")]   # medido, nao presumido
ast.parse(txt)
out = txt.encode("utf-8")
with open(DST + ".tmp", "wb") as fh:
    fh.write(out)
assert os.path.getsize(DST + ".tmp") == len(out)
os.replace(DST + ".tmp", DST)
sha = lambda b: hashlib.sha256(b).hexdigest()
rel = {"contrato": "DERIVACAO_DO_DERIVADOR_v403", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
       "entrada": {"path": SRC, "sha256": sha(raw), "bytes": len(raw)}, "saida": {"path": DST, "sha256": sha(out), "bytes": len(out)},
       "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())}, "contagens": cont, "ast_parse": "ok"}
pj = os.path.join(HERE, "DERIVACAO_DO_DERIVADOR_v403.json")
with open(pj + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
os.replace(pj + ".tmp", pj)
print(json.dumps(rel, ensure_ascii=False))
