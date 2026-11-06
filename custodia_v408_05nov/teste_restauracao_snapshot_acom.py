# -*- coding: utf-8 -*-
"""Teste de RESTAURACAO isolada do instantaneo ACOM mais velho, antes de move-lo ao arquivo (decisao do operador, 05/11/2026:
«Testar e depois mover»). So leitura no instantaneo e no banco vivo: copia de BYTES para uma pasta isolada (argumento), confere o
sha256 contra o sidecar .sha256, abre a copia em modo somente-leitura e roda PRAGMA integrity_check e contagens. Grava o recibo
em work\\custodia_v408_05nov\\RESTAURACAO_SNAPSHOT_ACOM_v408.json. Apaga so a copia isolada que ele mesmo criou."""
import datetime as dt
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path

SNAP = Path(r"C:\IALD\MEMORIA_IALD\state\snapshots")
W = Path(r"C:\IALD\Central de Patentes\work\custodia_v408_05nov")
iso = Path(sys.argv[1])
iso.mkdir(parents=True, exist_ok=True)
# (05/11, ao lado) quando o teste ia rodar, uma transicao ACOM de outra sessao (10:06) ja tinha movido os 2 mais velhos ao arquivo D:;
# o alvo passa a ser o instantaneo ARQUIVADO indicado no 2o argumento (testa-se a restauracao do que esta no arquivo).
alvo = Path(sys.argv[2])
assert alvo.is_file() and alvo.name.startswith("memory.sqlite3.snap_"), alvo
side = alvo.with_name(alvo.name + ".sha256").read_text(encoding="utf-8").strip()
esperado = side.split()[0].lower()
assert len(esperado) == 64, side


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


r = {"quando": dt.datetime.now().isoformat(timespec="seconds"), "instantaneo": str(alvo), "bytes": alvo.stat().st_size,
     "sha256_sidecar": esperado, "sha256_original": sha(alvo)}
copia = iso / alvo.name
shutil.copyfile(alvo, copia)
r["sha256_copia_isolada"] = sha(copia)
r["copia_bate_com_sidecar"] = r["sha256_copia_isolada"] == esperado == r["sha256_original"]
con = sqlite3.connect("file:%s?mode=ro" % copia.as_posix(), uri=True)
try:
    r["integrity_check"] = [x[0] for x in con.execute("PRAGMA integrity_check").fetchall()][:5]
    tabelas = [x[0] for x in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    r["tabelas"] = {t: con.execute('SELECT COUNT(*) FROM "%s"' % t.replace('"', '""')).fetchone()[0] for t in tabelas}
finally:
    con.close()
r["restaura_integro"] = r["copia_bate_com_sidecar"] and r["integrity_check"] == ["ok"] and len(r["tabelas"]) > 0
copia.unlink()
r["copia_isolada_removida"] = not copia.exists()
out = W / "RESTAURACAO_SNAPSHOT_ACOM_v408.json"
out.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps({k: r[k] for k in ("instantaneo", "bytes", "copia_bate_com_sidecar", "integrity_check", "restaura_integro", "copia_isolada_removida")}, ensure_ascii=False, indent=1))
print("tabelas:", len(r["tabelas"]), "| linhas:", sum(r["tabelas"].values()))
