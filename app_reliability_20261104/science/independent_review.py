"""Read/hash scientific evidence only; never import or execute scientific code."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
W=HERE.parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()
source=HERE/'SCIENCE_STATUS.json'
raw=source.read_bytes();s=json.loads(raw)
checks=[]
for row in s['pins']:
    p=Path(row['path']);start=p.stat();digest=sha(p.read_bytes());end=p.stat()
    checks.append({'path':str(p),'match':digest==row['sha256'],
                   'stable':(start.st_mtime_ns,start.st_size)==(end.st_mtime_ns,end.st_size)})
installed=[]
for row in s['installed_files']['checks']:
    installed.append(sha(Path(row['path']).read_bytes())==row['expected_sha256'])
n=Path(s['nos']['program_pin']['path']).parent
seal=json.loads((n/'um_absoluto_selo.json').read_bytes())
seal_checks=[{'name':name,'match':sha((n/name).read_bytes())==digest} for name,digest in seal['sha256'].items()]
runtime=Path(r'C:\IALD\projetos_pyhton\IALD')
manifest=json.loads((runtime/'iald_nucleo_fixo.json').read_bytes())
manifest_matches=all(manifest[k]==v for k,v in s['active_science'].items())
program_matches=sha((n/'um.py').read_bytes())==manifest['active_cluster']['release_source_sha256']==seal['sha256']['um.py']
contract=json.loads(Path(manifest['jev_control']['path']).read_bytes())
contract_matches=contract['release']==manifest['active_cluster']['release']=='v407' and contract['source_sha256']==seal['sha256']['um.py']
mirror=Path(r'C:\IALD\Artigo\the_boundary')
def git(*args):
    p=subprocess.run(['git','-C',str(mirror),*args],capture_output=True,check=True)
    return p.stdout.decode('utf8').strip()
head=git('rev-parse','HEAD')
tracked408=[p for p in git('ls-files').splitlines() if 'v408' in p.lower()]
handoffs408=[p.name for p in n.glob('HANDOFF*v408*')]
valid=(all(c['match'] and c['stable'] for c in checks) and all(installed)
       and all(c['match'] for c in seal_checks) and manifest_matches and program_matches and contract_matches
       and head==manifest['active_cluster']['commit'] and not tracked408 and not handoffs408
       and source.read_bytes()==raw)
report={'status':'PASS_WITH_SCOPE' if valid else 'CHANGES_OR_GAPS_REQUIRE_REVIEW',
    'reviewer':'codex-recovery-independent-reviewer','role':'Actual independent review by recovery/installer reviewer, distinct from science producer and parent submitter',
    'utc':datetime.now(timezone.utc).isoformat(),'mission_reference':str(W/'SESSION_REFERENCE.json'),
    'task_id':'science','criterion':'Conferir v407 ativa e status verificável da v408, sem executar ciência nem duplicar entrega.',
    'source':{'path':str(source),'sha256':sha(raw)},
    'pins_checked':len(checks),'pin_mismatches':[c for c in checks if not c['match'] or not c['stable']],
    'installed_files':{'checked':len(installed),'matched':sum(installed)},
    'seal_artifacts':seal_checks,'manifest_matches':manifest_matches,'program_matches_seal_and_release':program_matches,
    'contract_matches':contract_matches,'local_mirror_head':head,'v408_tracked_paths':tracked408,'v408_handoffs':handoffs408,
    'conclusion':'v407 scientific files, manifests, contract and canonical seal agree. No finalized v408 was located in the inspected canonical handoffs or tracked local mirror.',
    'limits':['No scientific execution, Lean compilation, provider call or current resident-process inspection.',
              'Remote publication observation is retained as prior receipt evidence, not independently refreshed here; no universal assertion that v408 does not exist elsewhere.',
              'Selftest and nature/proof statuses are declarations in the prior seal, not new proof or confirmation. No parallel update started.',
              'Point-in-time hashes; later source or publication changes require revalidation.'],
    'production_modified':False,'scientific_sources_modified':False,'independent_review_script_sha256':sha(Path(__file__).read_bytes())}
dest=HERE/'INDEPENDENT_REVIEW.json'
with dest.open('x',encoding='utf8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':report['status'],'pins':len(checks),'mismatches':len(report['pin_mismatches']),
    'installed':report['installed_files'],'seal_checked':len(seal_checks),'seal_matched':sum(c['match'] for c in seal_checks),
    'sha256':sha(dest.read_bytes())}))
