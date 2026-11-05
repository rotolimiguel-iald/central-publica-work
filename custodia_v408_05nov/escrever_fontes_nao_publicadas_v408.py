# -*- coding: utf-8 -*-
"""FONTES_NAO_PUBLICADAS_v408.json: a mesma fonte da v407, com o mesmo sha256, fica FORA do espelho (custodia v408, 05/11/2026, claude-site-custodia).
O um.py v408 ainda traz o dicionario _V407_FONTES, que pina o insumo original da v407; a guarda da E03 parou nele (termo-guarda a mais).
Nao e' decisao nova: e' a ordem vigente do operador (08/09) aplicada de novo, como na v407. A guarda nao afrouxa. Hashes lidos por script.
Grava com open('xb'): nunca sobrescreve."""
import hashlib
import json
import datetime as dt
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
DEC = CEN / "work" / "custodia_G1" / "decisoes"
ANT = DEC / "FONTES_NAO_PUBLICADAS_v407.json"
VB = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\protocolo-de-colapso-nunca-publico.md")
VB04 = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"
HO = CEN / "work" / "cadeia_de_selo" / "v408" / "ORDEM_HANDOFF_CUSTODIA_v408.md"
F = CEN / "work" / "cadeia_de_selo" / "v407" / "insumos" / "PSION_NO_ACERVO_03nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


a = json.loads(ANT.read_text(encoding="utf-8"))
ent = a["arquivos"][0]
assert Path(ent["arquivo"]) == F and sha(F) == ent["sha256"], "o arquivo mudou desde a decisao da v407: nao se renova, reexamina-se"
assert sha(VB)[:16] == a["decisao_do_operador"]["sha16"], "o verbatim de 08/09 mudou: reler antes de citar"
assert sha(VB04)[:16] == a["decisao_do_operador"]["sha16_04nov"]
d = {
    "schema": "iald.custodia.fontes_nao_publicadas/v1",
    "versao": "v408",
    "quando": dt.datetime.now().isoformat(timespec="seconds"),
    "por": "claude-site-custodia (sessao de custodia), em nome proprio, aplicando a ordem vigente do operador, como a gerencia c1 na v407",
    "decisao_do_operador": {
        "verbatim": str(VB).replace("\\", "/"),
        "sha16": sha(VB)[:16],
        "o_que_diz": a["decisao_do_operador"]["o_que_diz"],
        "verbatim_04nov": str(VB04).replace("\\", "/"),
        "sha16_04nov": sha(VB04)[:16],
        "decisao_anterior": {"arquivo": str(ANT), "sha16": sha(ANT)[:16]},
        "handoff_v408": {"arquivo": str(HO), "sha16": sha(HO)[:16]},
    },
    "arquivos": [{
        "arquivo": str(F),
        "sha256": sha(F),
        "motivo": ("o mesmo arquivo e o mesmo sha256 da decisao da v407. O um.py v408 ainda traz _V407_FONTES, que o pina; a E03 da v408 parou nele "
                   "(termo-guarda a mais; recibo work\\custodia_G1\\runs\\v408_20261105_053321). A v408 pina a copia PURGADA "
                   "(insumos\\PSION_NO_ACERVO_04nov_purgado.md, 0 ocorrencias), que entra no espelho; esta fica FORA, como na v407 (errata E23 do core v408)."),
    }],
    "nota": "a guarda nao afrouxa: a fonte nao entra; vale so para a v408 e para este sha256; mudou o arquivo, a decisao nao cobre",
}
dst = DEC / "FONTES_NAO_PUBLICADAS_v408.json"
b = (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
with dst.open("xb") as f:
    f.write(b)
assert dst.read_bytes() == b
print(dst.name, hashlib.sha256(b).hexdigest()[:16], len(b))
