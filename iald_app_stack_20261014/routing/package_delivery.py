from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
names=['ORIGEM.txt','baseline.json','routing.patch','REPORT.txt','testreport.json',
       'testreport.txt','runtime_verification.json','build_patch.py','test_routing.py',
       'package_delivery.py','memory_reference.json']
names += ['patched/'+p.name for p in sorted((ROOT/'patched').glob('*.py'))]
report=json.loads((ROOT/'testreport.json').read_text(encoding='utf-8'))
assert report['passed'] and report['tests']==22
checks=json.loads((ROOT/'runtime_verification.json').read_text(encoding='utf-8-sig'))
assert all(r['baseline_sha256']==r['current_sha256'] for r in checks)
data={'unit':'F9.APP_STACK_20261014.ROUTING','actor':'codex-app-routing',
      'scope':'staging only; independent review and deployment pending',
      'tests':report,'runtime_sources_unchanged':True,
      'files':[{'path':n,'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest(),
                'bytes':(ROOT/n).stat().st_size} for n in names]}
(ROOT/'DELIVERY.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('DELIVERY.json ready')
