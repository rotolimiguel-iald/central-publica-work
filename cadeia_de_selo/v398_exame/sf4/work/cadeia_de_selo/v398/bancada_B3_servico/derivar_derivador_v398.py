# -*- coding: utf-8 -*-
"""derivar_derivador_v398.py -- gera derivar_servico_v398.py a partir de v397\\bancada_B3_servico\\derivar_servico_v397.py por SUBIDA DE VERSAO de uma passada
(fronteira de digitos): v394..v397 -> +1 (tambem V39x_ e rel39x); variaveis de caminho V5S->V6S, V6S->V7S, V6->V7; "22/10" (data do rito real anterior) -> "23/10";
a tupla de restos ("393","394","395","V396_","v398") (apos o +1: V397_) -> ("394","395","396","V397_","v399").
Duas regras que NAO sao subida de versao, ambas com contagem exata (assert), porque o molde v397 (os tres scripts que RODARAM em 23/10) trazia o bloco do cruzamento com o B(n) anterior
(rb_ant / ger_ant / assert n_esp == ger_ant + 1) DUAS vezes no recibo_religamento (a v396 ja o tinha e a derivacao da v397 o inseriu de novo): (1) a regra SUB do derivador passa a reduzir a UMA copia;
(2) a docstring do derivador registra isso. A fonte dos tres scripts da v398 sao os FINAIS da v397 (os que rodaram em 23/10), derivados num so nivel pelo derivar_servico_v398.py.
Nao executa o derivador gerado (so ast.parse). Registra entrada/saida com sha256 em DERIVACAO_DERIVADOR_v398.json. Nao sobrescreve."""
import ast
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CS = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(CS, "v397", "bancada_B3_servico", "derivar_servico_v397.py")
DST = os.path.join(HERE, "derivar_servico_v398.py")
sha = lambda b: hashlib.sha256(b).hexdigest()

bruto = open(SRC, "rb").read()
t = bruto.decode("utf-8")
assert "\r" not in t
cont = {}
RE_VER = re.compile(r"(?<![0-9A-Za-z])(v|V|rel)(39)([4-7])(?![0-9])")
t, cont["versoes_mais_um"] = RE_VER.subn(lambda m: m.group(1) + m.group(2) + str(int(m.group(3)) + 1), t)
assert cont["versoes_mais_um"] == 148, cont["versoes_mais_um"]        # v397 49 + v396 71 + v395 9 + rel396 5 + rel395 3 + V397 7 + V396 4 (inventario da fonte)
RE_VAR = re.compile(r"(?<![0-9A-Za-z_])(V5S|V6S|V6)(?![0-9A-Za-z_])")
VAR = {"V5S": "V6S", "V6S": "V7S", "V6": "V7"}
t, cont["variaveis_de_caminho"] = RE_VAR.subn(lambda m: VAR[m.group(1)], t)
assert cont["variaveis_de_caminho"] == 14, cont["variaveis_de_caminho"]      # V6 5 + V6S 7 + V5S 2 (inventario da fonte)
a = "rito REAL de 22/10"
assert t.count(a) == 2, t.count(a)
t = t.replace(a, "rito REAL de 23/10")
cont["data_do_rito_real"] = 2
a = '("393", "394", "395", "V397_", "v398")'   # depois do +1: V396_ virou V397_
assert t.count(a) == 1, t.count(a)
t = t.replace(a, '("394", "395", "396", "V397_", "v399")')
cont["tupla_de_restos"] = 1
# (1) o bloco do cruzamento com o B(n) anterior: a fonte (v397 final) o traz DUAS vezes; a regra SUB passa a casar as duas copias e deixar UMA
a = '        ("n_confere_com_o_B_n_da_v397", SUB, r"^" + re.escape(N_ESP_LINHA), CRUZA_BLOCO, 1),'
assert t.count(a) == 1, t.count(a)
t = t.replace(a, '        ("n_confere_com_o_B_n_da_v397__bloco_uma_so_vez", SUB, r"^" + re.escape(CRUZA_BLOCO + CRUZA_BLOCO[len(N_ESP_LINHA):]), CRUZA_BLOCO, 1),')
cont["regra_sub_do_cruzamento_reduz_a_uma_copia"] = 1
# (2) a docstring do derivador registra a mudanca
a = "assert com mensagem clara;\n3) ast.parse de cada saida"
assert t.count(a) == 1, t.count(a)
t = t.replace(a, ("assert com mensagem clara;\n"
                  "     (v398: o molde v397 trazia este bloco DUAS vezes no recibo_religamento -- a v396 ja o tinha e a derivacao da v397 o inseriu de novo --; a regra agora casa as duas copias e deixa UMA, contagem exata 1);\n"
                  "3) ast.parse de cada saida"))
cont["docstring_registra_a_reducao"] = 1
# invariantes do resultado: o mapa de versoes do derivador novo tem de ser v397->v398, v396->v397
a = 'MAPA = {"v397": "v398", "v396": "v397", "rel396": "rel397", "V397_AUTORIZACAO_OPERADOR": "V398_AUTORIZACAO_OPERADOR"}'
assert t.count(a) == 1, "mapa de versoes do derivador novo nao e o esperado"
a = 'RE_MAPA = re.compile(r"V397_AUTORIZACAO_OPERADOR|v397|v396|rel396")'
assert t.count(a) == 1
for pad in ('V7S = os.path.join(V7, "bancada_B3_servico")', 'V7 = os.path.join(CS, "v397")', 'V6S = os.path.join(CS, "v396", "bancada_B3_servico")'):
    assert t.count(pad) == 1, pad
assert not re.search(r"(?<![0-9A-Za-z])(v|V|rel)395(?![0-9])", t)
ast.parse(t)
out = t.encode("utf-8")
if os.path.exists(DST):
    raise SystemExit("ja existe: " + DST)
rp = os.path.join(HERE, "DERIVACAO_DERIVADOR_v398.json")
if os.path.exists(rp):
    raise SystemExit("ja existe: " + rp)
with open(DST + ".tmp", "wb") as fh:
    fh.write(out)
assert os.path.getsize(DST + ".tmp") == len(out)
os.replace(DST + ".tmp", DST)
rel = {"entrada": {"path": SRC, "sha256": sha(bruto), "bytes": len(bruto)}, "saida": {"path": DST, "sha256": sha(out), "bytes": len(out)}, "contagens": cont, "ast_parse": "ok", "executado": False}
with open(rp, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
print(json.dumps(rel, ensure_ascii=False))
