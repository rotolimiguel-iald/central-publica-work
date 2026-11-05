# -*- coding: utf-8 -*-
"""Parte 4 dos ajustes da v407, depois da PRIMEIRA execucao do prepare.py (prepare_stderr_r1.txt): 'Missing semantic field: /core/specific_free_scalar_aqft_net/tgl_embedding_status'.
Causa: a regra F1 (status_record) passou a declarar PROTEGIDO o dict de estatuto inteiro, mas project() ainda o reduzia a uma capsula '@' cujos 'fields' vem so' das chaves-filhas
-- o registro inteiro nao ficava representado e o proprio guarda do codec (is_represented) parou o prepare, como deve. Correcao: project() devolve o registro de estatuto plano
INTEIRO quando ele e' o valor projetado (profundidade >= 1), como ja faz com WHOLE_FIELD. Uma troca, uma ocorrencia."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent
p = W / "app" / "build" / "haiku_codec.py"
t = p.read_bytes().decode("utf-8")
eol = "\r\n" if "\r\n" in t else "\n"
velho = "    if pointer in ALWAYS_FULL or (depth >= 1 and WHOLE_FIELD.search(field_name)):\n        return value\n".replace("\n", eol)
novo = ("    if pointer in ALWAYS_FULL or (depth >= 1 and (WHOLE_FIELD.search(field_name) or status_record(field_name, value))):   # v407/F1: registro de estatuto plano fica inteiro\n"
        "        return value\n").replace("\n", eol)
assert t.count(velho) == 1, t.count(velho)
p.write_bytes(t.replace(velho, novo).encode("utf-8"))
print(json.dumps({"ajustados": ["app/build/haiku_codec.py"], "trocas": 1}))
