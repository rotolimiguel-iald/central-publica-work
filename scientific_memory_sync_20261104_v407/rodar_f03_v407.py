"""Roda UMA operacao do helper da F0.3 (check | prepare | verify | activate) com os recibos redirecionados para ESTA pasta (work=) e o membro claude-app-orquestrador.
O helper e' o de work\\scientific_memory_sync_20261013 (nao alterado). Uso: python rodar_f03_v407.py <operacao> [epoch] > saida.json
Autorizacao: a do operador no chat (Autorizo a escrita; Vale para a v407); a escrita se esgota com a ativacao."""
import json
import sys
from pathlib import Path

HELPER = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(HELPER))
sys.dont_write_bytecode = True
import scientific_memory_sync as S  # noqa: E402

op = sys.argv[1]
epoch = sys.argv[2] if len(sys.argv) > 2 else None
sync = S.ScientificMemorySync(work=W, member="claude-app-orquestrador", unit="F0.3.MEMORIA_CIENTIFICA_SYNC")
if op in ("verify", "activate"):
    assert epoch, "epoch obrigatorio"
    r = getattr(sync, op)(epoch)
else:
    r = getattr(sync, op)()
print(json.dumps(r, ensure_ascii=False))
