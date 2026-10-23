# -*- coding: utf-8 -*-
"""Tira da lista LOCAL de exclusões do preparo do work os resultados científicos que a regra larga «^varredura_» barrou (errata ao lado
em construir_regiao_publica.py, 22/10/2026), para que a rodada incremental seguinte os passe pela esteira comum (que decide de novo:
credencial, dado pessoal, Escritório). Acerta a contagem do motivo no EXCLUSOES_PUBLICAS.json. Backup de bytes da lista antes."""
import json, os, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
D = Path(r"C:\IALD\Central_publica\central-publica-work")
LP, EP = W / "varredura_exclusoes_central-publica-work.json", D / "EXCLUSOES_PUBLICAS.json"
NOVA = re.compile(r"(?i)^varredura_(arquivos|buscas|conferencia|convites|dados|escritorio|exclusoes|formatos|miktex|pastas|pdf|reservados|"
                  r"segredos|terceiros|usuarios)")
MOTIVO = "conversa, usuários ou varredura de dado pessoal"
TS = time.strftime("%Y%m%d_%H%M%S")
raw = LP.read_bytes()
(W / (LP.name + ".bak_" + TS)).write_bytes(raw)
local = json.loads(raw.decode("utf-8"))
lst = local.get(MOTIVO) or []
volta = [r for r in lst if r.rsplit("/", 1)[-1].lower().startswith("varredura_") and not NOVA.search(r.rsplit("/", 1)[-1])
         and not r.startswith(("central_publica_22out/", "php_e_v396_22out/"))]
print("voltam à esteira (%d):" % len(volta))
for r in volta:
    print("  ", r)
local[MOTIVO] = [r for r in lst if r not in set(volta)]
exc = json.loads(EP.read_text(encoding="utf-8"))
exc["por_motivo"][MOTIVO] = exc["por_motivo"].get(MOTIVO, 0) - len(volta)
assert exc["por_motivo"][MOTIVO] >= 0
exc.setdefault("atualizacoes", []).append({"em": time.strftime("%Y-%m-%d %H:%M:%S"),
                                            "errata": "a regra «^varredura_» passou a valer só para as listas locais da esteira; %d resultados voltam à esteira comum" % len(volta)})
for p, obj, ind in ((LP, local, 0), (EP, exc, 1)):
    t = p.with_name(p.name + ".tmp_volta")
    t.write_text(json.dumps(obj, ensure_ascii=False, indent=ind), encoding="utf-8")
    os.replace(t, p)
print("lista local e contagem acertadas")
