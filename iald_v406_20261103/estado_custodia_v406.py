# -*- coding: utf-8 -*-
"""Evidencia irma do estado da custodia (a licao do F3 do parecer r1 da v405: separar custodia EM CURSO de CONCLUIDA). So leitura do plano da G1; grava uma vez."""
import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
plano = Path(r"C:\IALD\Central de Patentes\work\custodia_G1\PLANO_v406.json")
conf = Path(r"C:\IALD\Central de Patentes\work\custodia_v406_03nov\CONFERENCIA_FINAL_v406.json")
d = json.loads(plano.read_bytes())
estado = {
    "status": "CUSTODIA_V406_EM_CURSO_NAO_CONCLUIDA" if not d.get("completo") else "CUSTODIA_V406_COMPLETA",
    "plano_g1": {"path": str(plano), "sha256": hashlib.sha256(plano.read_bytes()).hexdigest()},
    "conferencia_final_da_gerencia": {"path": str(conf), "sha256": hashlib.sha256(conf.read_bytes()).hexdigest()},
    "leitura": "O selo, o cofre e o commit do espelho da v406 estao custodiados e conferidos (sources_verified.json). A custodia como processo segue em curso: o plano da G1 ainda lista pendentes; "
               "o C21 (esta release do app) e' o item que depende deste pacote, e a troca do servico web e' do operador.",
    "campos_do_plano": {k: d.get(k) for k in ("versao", "corrente", "relacao_espelho", "contagem", "completo", "pendentes", "pendentes_do_operador") if k in d},
}
with (W / "CUSTODIA_v406_ESTADO.json").open("xb") as f:
    f.write(json.dumps(estado, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(estado["campos_do_plano"], ensure_ascii=False)[:600])
