# -*- coding: utf-8 -*-
"""Reviewer r3 r0: the evidence pinned by the builder's two r3 submit receipts matches the files on disk NOW; mission state (read-only project); plan r3 vs plan r1 by destination;
sources_verified r3 vs r1 (content equal except checked_at); F3 evidence file vs the live G1 plan fields."""
import hashlib, json, subprocess
from pathlib import Path

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
out = {}
for f in ('receipts/v405-sources-submit-r3.json', 'receipts/v405-app-submit-r3.json'):
    d = json.loads((W / f).read_bytes())
    t = d['task']
    rows = [{'file': Path(e['path']).name, 'pinned': e['sha256'], 'now': sh(e['path']), 'ok': sh(e['path']) == e['sha256']} for e in t['evidence']]
    out[f] = {'status': t['status'], 'submitted_by': t['submitted_by'], 'revision': d['receipt']['revision'], 'epoch': t.get('epoch'), 'attempts': t.get('attempts'), 'all_pins_match': all(r['ok'] for r in rows), 'pins': rows}
p = subprocess.run([r'C:\Python314\python.exe', '-B', '-X', 'utf8', str(W / 'mission_step.py'), 'project'], capture_output=True, cwd=str(W))
proj = json.loads(p.stdout.decode('utf-8'))
out['mission_project_readonly'] = {'revision': proj['revision'], 'projection_sha256': proj['projection_sha256'], 'active': proj['active']}
# plan r3 vs r1 by destination
p3 = json.loads((W / 'install_plan.json').read_bytes())
p1 = json.loads((W / 'superseded_r1/install_plan.json').read_bytes())
d3 = {r['destination']: r for r in p3['files']}
d1 = {r['destination']: r for r in p1['files']}
R = Path(r'C:\IALD\projetos_pyhton\IALD')
changed = [str(Path(k).relative_to(R)) for k in d3 if k in d1 and d3[k]['sha256'] != d1[k]['sha256']]
out['plan_r3_vs_r1'] = {'plan_r3_sha256': sh(W / 'install_plan.json'), 'plan_r1_sha256': sh(W / 'superseded_r1/install_plan.json'), 'n_r3': len(d3), 'n_r1': len(d1), 'destinations_only_in_r3': [k for k in d3 if k not in d1], 'destinations_only_in_r1': [k for k in d1 if k not in d3],
                        'destinations_with_changed_sha': changed, 'baseline_changed': [str(Path(k).relative_to(R)) for k in d3 if k in d1 and d3[k]['baseline'] != d1[k]['baseline']]}
# final_checks r3
fc = json.loads((W / 'validation/final_checks.json').read_bytes())
out['final_checks_r3'] = {'passed': fc['passed'], 'plan_sha256_in_file': fc['plan_sha256'], 'equals_current_plan': fc['plan_sha256'] == sh(W / 'install_plan.json'), 'tests': [(t['name'], t['status']) for t in fc['tests']]}
# sources_verified r3 vs r1
s3 = json.loads((W / 'sources_verified.json').read_bytes())
s1 = json.loads((W / 'superseded_r1/sources_verified.json').read_bytes())
a, b = dict(s1), dict(s3)
a.pop('checked_at', None)
b.pop('checked_at', None)
out['sources_verified_r3_vs_r1'] = {'equal_except_checked_at': a == b, 'checked_at_r1': s1['checked_at'], 'checked_at_r3': s3['checked_at'], 'status': s3['status'], 'published': s3['published']}
# F3 evidence vs live G1 plan
ev = json.loads((W / 'CUSTODIA_EM_CURSO_v405.json').read_bytes())
live_path = Path(ev['plano_g1']['path'])
live = json.loads(live_path.read_bytes())
fields = ev['campos_do_plano']
out['custody_evidence'] = {'status': ev['status'], 'file_sha256': sh(W / 'CUSTODIA_EM_CURSO_v405.json'), 'plano_sha256_in_evidence': ev['plano_g1']['sha256'], 'plano_sha256_live_now': sh(live_path), 'plano_unchanged_since': ev['plano_g1']['sha256'] == sh(live_path),
                           'fields_equal_live_now': {k: (fields[k] == live.get(k)) for k in fields}, 'live_contagem': live.get('contagem'), 'live_completo': live.get('completo'), 'live_pendentes': live.get('pendentes'),
                           'evidence_contagem': fields.get('contagem'), 'evidence_completo': fields.get('completo'), 'evidence_pendentes': fields.get('pendentes'), 'leitura': ev['leitura']}
print(json.dumps(out, ensure_ascii=False, indent=1))
