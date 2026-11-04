# -*- coding: utf-8 -*-
"""Parte 2 dos ajustes da v406 (a parte 1, em ajustes_v406.py, aplicou RELEASE.json, release_cfg.py, haiku_codec.py, fit_memory.py e prepare.py antes de parar em task.py:
o literal tem acentos). Mesma disciplina: cada troca exige exatamente uma ocorrencia."""
import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
OPERADOR = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt")
feito = []


def troca(arq, pares):
    p = W / arq
    t = p.read_bytes().decode("utf-8")
    for velho, novo in pares:
        assert t.count(velho) == 1, (arq, t.count(velho), velho[:90])
        t = t.replace(velho, novo)
    p.write_bytes(t.encode("utf-8"))
    feito.append(arq)


troca("task.py", [
    ('Mapa de rotas: consulta "app ciencia v405 haiku55 compactacao base" (0 rotas) em 02/11 (1629 registros). Pipeline de referência: work/iald_v404_20261029 (instalada v404, aceita por revisor independente). Mudança desta release: base compacta do haiku55 redesenhada no codec (lição da v404).',
     'Mapa de rotas: consulta "app release v406 ciencia haiku55 janela P2 shared" (0 rotas) em 03/11 (1748 registros). Pipeline de referência: work/iald_v405_20261102 (instalada v405, aceita por revisores distintos do construtor). Mudanças desta release: R3-1 e R3-2 da LICOES_v405, janela P2 do shared deslizada (ORDEM_004 da gerência c1) com limites/diz/nao_diz mantidos na cápsula compacta.'),
])
troca("run_construcao.sh", [
    ("Construcao da release do app (v405)", "Construcao da release do app (v406)"),
    ("BLD=opus-app-v405-construtor", "BLD=claude-app-orquestrador"),
])
troca("exercita_busca.py", [
    ("random.Random(20261102)", "random.Random(20261103)"),
    ('"semente 20261102"', '"semente 20261103"'),
])
raw = OPERADOR.read_bytes()
for n in ("ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"):
    with (W / n).open("xb") as f:
        f.write(raw)
    assert (W / n).read_bytes() == raw
feito += ["ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"]
print(json.dumps({"ajustados_na_parte_2": feito, "ordem_do_operador_sha16": hashlib.sha256(raw).hexdigest()[:16]}, ensure_ascii=False))
