"""No production deployment: fault tests use a private fixture only."""
from pathlib import Path
import importlib.util,hashlib,json
from unittest.mock import patch
V=Path(__file__).resolve().parent;W=V.parent
spec=importlib.util.spec_from_file_location('tx',W/'transaction.py');tx=importlib.util.module_from_spec(spec);spec.loader.exec_module(tx)
sha=lambda b:hashlib.sha256(b).hexdigest()
results=[]
for case in ('changed_source','changed_baseline','partial_write_failure'):
    base=V/'transaction_additional'/case;root=base/'runtime';work=base/'work'
    root.mkdir(parents=True);(work/'validation').mkdir(parents=True)
    rows=[]
    for name in ('a.txt','b.txt'):
        (root/name).write_bytes(b'old');(work/name).write_bytes(b'new')
        rows.append({'source':str(work/name),'destination':str(root/name),'sha256':sha(b'new'),'baseline':sha(b'old')})
    plan=work/'plan.json';plan.write_text(json.dumps({'files':rows}));pin=sha(plan.read_bytes())
    (work/'validation/final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':pin}))
    (work/'validation/review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':pin}))
    if case=='changed_source':(work/'b.txt').write_bytes(b'changed')
    if case=='changed_baseline':(root/'b.txt').write_bytes(b'concurrent')
    atomic=tx.atomic
    def failing(path,raw):
        if Path(path)==root/'b.txt' and raw==b'new':raise OSError('synthetic write failure')
        atomic(path,raw)
    with patch.object(tx,'ROOT',root),patch.object(tx,'WORK',work),patch.object(tx,'quiet',return_value={}),patch.object(tx,'atomic',side_effect=failing if case=='partial_write_failure' else atomic):
        try:tx.apply_plan(plan)
        except (ValueError,OSError):refused=True
        else:refused=False
    assert refused and (root/'a.txt').read_bytes()==b'old'
    assert (root/'b.txt').read_bytes()==(b'concurrent' if case=='changed_baseline' else b'old')
    assert not (work/'deployment.json').exists()
    results.append({'case':case,'passed':True,'originals_restored_or_concurrent_edit_preserved':True})
out=V/'transaction_additional_tests.json';assert not out.exists();out.write_text(json.dumps(results,indent=2));print(json.dumps(results))
