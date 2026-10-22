from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
pins=json.loads((R/'inputpins.json').read_bytes())
changed=[p for p,v in pins.items() if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=v['sha256']]
assert not changed,changed
tests=json.loads((R/'tests.json').read_bytes());semantic=json.loads((R/'semantic_tests.json').read_bytes())
assert tests['passed']==tests['total'] and semantic['passed']==semantic['total']
names=['ORIGEM.txt','unit.json','memory_reference.json','REVIEW.txt','review_science.py','review_semantics.py','package_review.py','inputpins.json','tests.json','test_details.json','semantic_tests.json']
names += [p.name for p in sorted(R.glob('capture_*.py'))]
data={'unit':'F9.APP_STACK_20261014.SCIENCE_REVIEW','verdict':'PASS_WITH_SCOPE',
      'scope':'Scientific package fidelity only; not deployment or new custody',
      'checks_passed':tests['passed']+semantic['passed'],'inputs_rechecked':len(pins),
      'input_drift':changed,'provider_calls':0,'HTTP_repeated':False,
      'files':[{'path':n,'sha256':hashlib.sha256((R/n).read_bytes()).hexdigest(),'bytes':(R/n).stat().st_size} for n in names]}
p=R/'DELIVERY.json';assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'verdict':data['verdict'],'checks_passed':data['checks_passed'],'inputs_rechecked':len(pins)}))
