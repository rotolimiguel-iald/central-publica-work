# -*- coding: utf-8 -*-
"""Tira arquivos de um preparo público JÁ CONSTRUÍDO (22/10/2026: os logs e inventários que listam caminhos para dentro do acervo do
ESCRITÓRIO — PJ separada — com nomes de partes; achado da varredura varrer_escritorio.py antes de publicar): apaga do preparo, tira do
INDICE_PUBLICO.json, soma o motivo no EXCLUSOES_PUBLICAS.json (só a contagem; os caminhos ficam na lista LOCAL varredura_exclusoes_*.json).
Uso: excluir_do_preparo.py <pasta_do_preparo> "<motivo>" <arquivo_com_um_caminho_relativo_por_linha>"""
import json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
D, MOTIVO, LISTA = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
rels = [x.strip() for x in LISTA.read_text(encoding="utf-8").splitlines() if x.strip()]
IP, EP, LP = D / "INDICE_PUBLICO.json", D / "EXCLUSOES_PUBLICAS.json", W / ("varredura_exclusoes_%s.json" % D.name)
idx = json.loads(IP.read_text(encoding="utf-8"))
exc = json.loads(EP.read_text(encoding="utf-8"))
local = json.loads(LP.read_text(encoding="utf-8")) if LP.is_file() else {}
alvo = set(rels)
antes = len(idx["arquivos"])
idx["arquivos"] = [a for a in idx["arquivos"] if a["caminho"] not in alvo]
tirados = antes - len(idx["arquivos"])
n_apagados = 0
for r in rels:
    p = D / r
    lp = "\\\\?\\" + str(p.resolve())
    if os.path.exists(lp):
        os.remove(lp)
        n_apagados += 1
idx["n_arquivos"] = len(idx["arquivos"])
exc["por_motivo"][MOTIVO] = exc["por_motivo"].get(MOTIVO, 0) + tirados
local.setdefault(MOTIVO, []).extend(rels)
for p, obj in ((IP, idx), (EP, exc), (LP, local)):
    t = p.with_name(p.name + ".tmp_excl")
    t.write_text(json.dumps(obj, ensure_ascii=False, indent=(None if p == IP else 1)), encoding="utf-8")
    os.replace(t, p)
print("%s: %d tirados do índice, %d apagados do disco | motivo: %s | índice agora %d" % (D.name, tirados, n_apagados, MOTIVO, idx["n_arquivos"]))
