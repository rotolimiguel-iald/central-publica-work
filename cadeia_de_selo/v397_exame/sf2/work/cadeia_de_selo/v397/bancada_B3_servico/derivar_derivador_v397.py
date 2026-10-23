# -*- coding: utf-8 -*-
"""derivar_derivador_v397.py -- gera derivar_servico_v397.py a partir de v396\\bancada_B3_servico\\derivar_servico_v396.py por SUBIDA DE VERSAO de uma passada
(fronteira de digitos): v393..v396 -> +1 (tambem V39x_ e rel39x); variaveis de caminho V4S->V5S, V5S->V6S, V5->V6; "21/10" (data do rito real anterior) -> "22/10";
a tupla de restos ("392","393","394","V395_","v397") (apos o +1: V396_) -> ("393","394","395","V396_","v398"). Cada regra com contagem exata (assert). Nao executa o derivador gerado (so ast.parse).
Registra entrada/saida com sha256 em DERIVACAO_DERIVADOR_v397.json. Nao sobrescreve."""
import ast
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CS = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(CS, "v396", "bancada_B3_servico", "derivar_servico_v396.py")
DST = os.path.join(HERE, "derivar_servico_v397.py")
sha = lambda b: hashlib.sha256(b).hexdigest()

bruto = open(SRC, "rb").read()
t = bruto.decode("utf-8")
assert "\r" not in t
cont = {}
RE_VER = re.compile(r"(?<![0-9A-Za-z])(v|V|rel)(39)([3-6])(?![0-9])")
t, cont["versoes_mais_um"] = RE_VER.subn(lambda m: m.group(1) + m.group(2) + str(int(m.group(3)) + 1), t)
RE_VAR = re.compile(r"(?<![0-9A-Za-z_])(V4S|V5S|V5)(?![0-9A-Za-z_])")
VAR = {"V4S": "V5S", "V5S": "V6S", "V5": "V6"}
t, cont["variaveis_de_caminho"] = RE_VAR.subn(lambda m: VAR[m.group(1)], t)
a = "rito REAL de 21/10"
assert t.count(a) == 2, t.count(a)
t = t.replace(a, "rito REAL de 22/10")
cont["data_do_rito_real"] = 2
a = '("392", "393", "394", "V396_", "v397")'   # depois do +1: V395_ virou V396_
assert t.count(a) == 1, t.count(a)
t = t.replace(a, '("393", "394", "395", "V396_", "v398")')
cont["tupla_de_restos"] = 1
# invariantes do resultado: o mapa de versoes do derivador novo tem de ser v396->v397, v395->v396
a = 'MAPA = {"v396": "v397", "v395": "v396", "rel395": "rel396", "V396_AUTORIZACAO_OPERADOR": "V397_AUTORIZACAO_OPERADOR"}'
assert t.count(a) == 1, "mapa de versoes do derivador novo nao e o esperado"
a = 'RE_MAPA = re.compile(r"V396_AUTORIZACAO_OPERADOR|v396|v395|rel395")'
assert t.count(a) == 1
for pad in ('V6S = os.path.join(V6, "bancada_B3_servico")', 'V6 = os.path.join(CS, "v396")', 'V5S = os.path.join(CS, "v395", "bancada_B3_servico")'):
    assert t.count(pad) == 1, pad
assert not re.search(r"(?<![0-9A-Za-z])(v|V|rel)394(?![0-9])", t)
ast.parse(t)
out = t.encode("utf-8")
if os.path.exists(DST):
    raise SystemExit("ja existe: " + DST)
open(DST, "wb").write(out)
rel = {"entrada": {"path": SRC, "sha256": sha(bruto), "bytes": len(bruto)}, "saida": {"path": DST, "sha256": sha(out), "bytes": len(out)}, "contagens": cont, "ast_parse": "ok", "executado": False}
open(os.path.join(HERE, "DERIVACAO_DERIVADOR_v397.json"), "w", encoding="utf-8").write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
print(json.dumps(rel, ensure_ascii=False))
