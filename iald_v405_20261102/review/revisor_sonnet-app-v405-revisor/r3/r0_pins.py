"""Reviewer r0: the evidence pinned by the builder's two submit receipts still matches the files on disk; mission state (read-only project)."""
import hashlib, json, subprocess
from pathlib import Path

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
out = {}
for f in ('receipts/v405-sources-submit.json', 'receipts/v405-app-submit.json'):
    d = json.loads((W / f).read_bytes())
    t = d['task']
    rows = [{'file': Path(e['path']).name, 'pinned': e['sha256'], 'now': sh(e['path']), 'ok': sh(e['path']) == e['sha256']} for e in t['evidence']]
    out[f] = {'status': t['status'], 'submitted_by': t['submitted_by'], 'revision': d['receipt']['revision'], 'all_pins_match': all(r['ok'] for r in rows), 'pins': rows}
p = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8', str(W / 'mission_step.py'), 'project'], capture_output=True, cwd=str(W))
proj = json.loads(p.stdout.decode('utf-8'))
out['mission_project_readonly'] = {'revision': proj['revision'], 'projection_sha256': proj['projection_sha256'], 'active': proj['active']}
print(json.dumps(out, ensure_ascii=False, indent=1))
