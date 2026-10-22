"""Reuse existing 28 controller tests against staged core, with private stores."""
from pathlib import Path
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
source = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\test_mission.py')
cli = Path(r'C:\IALD\MEMORIA_IALD\mission_cli.py')
text = source.read_text(encoding='utf-8')
start = text.index("STAGE=ROOT/'stage'")
stop = text.index("sys.path.insert(0,str(STAGE/'lib'))")
text = text[:start] + "STAGE=ROOT.parent/'staging/core'\n" + text[stop:]
text = text.replace("self.store=MemoryStore(self.root/'state')",
                    "self.store=MemoryStore(self.root/'state', snapshot_archive_dir=self.root/'archive')")
cli_text = cli.read_text(encoding='utf-8').replace('store=MemoryStore(root)',
                "store=MemoryStore(root,snapshot_archive_dir=root/'archive')")
for name, value in [('test_mission_regression.py', text), ('mission_cli.py', cli_text)]:
    path = ROOT/name
    raw = value.encode('utf-8')
    with path.with_suffix('.tmp').open('xb') as f:
        f.write(raw)
    os.rename(path.with_suffix('.tmp'), path)
pins = [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in (source, cli, ROOT/'test_mission_regression.py', ROOT/'mission_cli.py')]
record = {'scope': 'Only test plumbing changed: staged import and private snapshot archive; 28 test bodies unchanged.',
          'pins': pins}
with (ROOT/'REGRESSION_PROVENANCE.json').open('x', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False, indent=2)
