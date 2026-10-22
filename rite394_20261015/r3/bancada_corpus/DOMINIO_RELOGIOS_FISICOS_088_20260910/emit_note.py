from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
def pin(p):
 b=p.read_bytes()
 return {'path':p.as_posix(),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def write_new(p,b):
 assert not p.exists(), str(p)
 t=p.with_name(p.name+'.tmp_new')
 with t.open('xb') as f:
  f.write(b); f.flush(); os.fsync(f.fileno())
 assert t.read_bytes()==b and len(b)>0
 os.replace(t,p)
 assert p.read_bytes()==b
before=json.loads((OUT/'PINS_ENTRADA_088.json').read_text(encoding='utf-8'))['sources']
after=[pin(Path(a['path'])) for a in before]
checks=[{'name':'source_unchanged:'+a['path'],'pass':a==b} for a,b in zip(before,after)]
payload=(OUT/'NOTE.payload.md').read_bytes()
body=payload.decode('utf-8')
links=[]
for raw in re.findall(r'\]\(<([^>]+)>\)',body):
 path=re.sub(r':\d+$','',raw)
 exists=Path(path).is_file()
 links.append({'target':raw,'exists':exists})
 checks.append({'name':'local_link:'+raw,'pass':exists})
checks.extend([
 {'name':'notes_scope_088','pass':'etapa088' in body},
 {'name':'explicit_localization','pass':'localização' in body and 'Δ≠0' in body},
 {'name':'no_universal_promotion','pass':'classe universal regular074' in body},
 {'name':'residual_causal_contract','pass':'D_n' in body and 'acordo perturbativo' in body},
 {'name':'no_mathematical_execution','pass':True},
])
assert all(c['pass'] for c in checks), [c for c in checks if not c['pass']]
note=OUT/'DOMINIO_INVERSA_RELOGIOS_E_CONTRATO_Q2_088.md'
write_new(note,payload)
final=[pin(Path(a['path'])) for a in before]
assert final==before
manifest={
 'utc':datetime.now(timezone.utc).isoformat(),
 'status':'WRITTEN_DOMAIN_AUDIT__DOCUMENTARY_PASS__INDEPENDENT_REVIEW_NOT_CLAIMED',
 'mathematical_status':'DERIVED written domain analysis; KNOWN primary contracts; residual Q2 obligations OPEN',
 'author':'selected_geometry_design',
 'note':pin(note),'sources_before':before,'sources_after':final,
 'checks':checks,'checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),
 'failed_checks':[c for c in checks if not c['pass']],
 'counts':{'sources_preserved':len(before),'local_links':len(links),'cas_executions':0,'lean_executions':0,'mathematical_executions':0},
 'local_links':links,
 'scope':{'um_executed':False,'um_imported':False,'originals_written':False,'canonical_recaptured':False,'prior_mathematics_rerun':False,'own_files_only_new':True,'universal_qme_claimed':False,'review_other_088_sources_claimed':False},
 'primary_sources':[{'url':'https://arxiv.org/pdf/0705.3340v4','consulted':'T2/T4/T5 and section3.6 equations250-256; web only; no local hash'}, {'url':'https://arxiv.org/html/1306.1058v5#S2.SS5','consulted':'section2.5; web only; no local hash'}],
 'helpers':[pin(OUT/'pin_inputs.py'),pin(OUT/'emit_note.py'),pin(OUT/'NOTE.payload.md'),pin(OUT/'PINS_ENTRADA_088.json')],
 'known_search_limitation':'Broad discovery met permission denial in unrelated historic Sympy package directories; all seven required sources were read successfully.',
}
dest=OUT/'MANIFESTO_DOMINIO_RELOGIOS_088.json'
write_new(dest,json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'status':manifest['status'],'note':pin(note),'manifest':pin(dest),'checks_passed':manifest['checks_passed'],'checks_total':manifest['checks_total'],'sources_preserved':len(final)},ensure_ascii=False,indent=2))
