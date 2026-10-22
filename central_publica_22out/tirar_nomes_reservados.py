# -*- coding: utf-8 -*-
"""Tira do preparo os arquivos com nome RESERVADO no Windows (lista de listar_nomes_reservados.py): apaga pelo prefixo \\\\?\\ montado À MÃO
(sem resolve(), que trocaria «com1» pelo dispositivo), tira do INDICE_PUBLICO.json e soma o motivo no EXCLUSOES_PUBLICAS.json.
Uso: tirar_nomes_reservados.py <pasta_do_preparo>"""
import json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = sys.argv[1].replace("/", "\\").rstrip("\\")
nome = D.rsplit("\\", 1)[-1]
W = Path(__file__).resolve().parent
rels = [x.strip() for x in (W / ("varredura_reservados_%s.txt" % nome)).read_text(encoding="utf-8").splitlines() if x.strip()]
MOT = "nome reservado do Windows (CON, NUL, COM1…: o git não abre; fixture de teste de nomes)"
apagados = 0
for r in rels:
    p = "\\\\?\\" + D + "\\" + r.replace("/", "\\")
    if os.path.exists(p):
        os.remove(p)
        apagados += 1
IP, EP = os.path.join(D, "INDICE_PUBLICO.json"), os.path.join(D, "EXCLUSOES_PUBLICAS.json")
idx = json.load(open(IP, encoding="utf-8"))
antes = len(idx["arquivos"])
idx["arquivos"] = [a for a in idx["arquivos"] if a["caminho"] not in set(rels)]
idx["n_arquivos"] = len(idx["arquivos"])
exc = json.load(open(EP, encoding="utf-8"))
exc["por_motivo"][MOT] = exc["por_motivo"].get(MOT, 0) + (antes - len(idx["arquivos"]))
for p, obj, ind in ((IP, idx, None), (EP, exc, 1)):
    t = p + ".tmp_res"
    with open(t, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=ind)
    os.replace(t, p)
print("%s: %d apagados, %d tirados do índice | índice agora %d" % (nome, apagados, antes - len(idx["arquivos"]), idx["n_arquivos"]))
