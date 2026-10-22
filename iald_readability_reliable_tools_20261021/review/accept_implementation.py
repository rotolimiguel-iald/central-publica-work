from pathlib import Path
import hashlib,importlib.util,json
W=Path(__file__).resolve().parents[1];report=W/'validation/review_final.json'
value=json.loads(report.read_bytes())
assert value['status']=='PASS' and value['plan_sha256']==hashlib.sha256((W/'install_plan.json').read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('readability_mission_task',W/'task.py');task=importlib.util.module_from_spec(spec);spec.loader.exec_module(task)
result=task.act('accept',actor='codex-readability-reviewer',task_id='implementation',event_id='readability-independent-implementation-accept-r2',review_evidence=[{'path':str(report),'sha256':hashlib.sha256(report.read_bytes()).hexdigest()}])
p=W/'review/IMPLEMENTATION_ACCEPTED_R2.json';raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8')
if p.exists():assert p.read_bytes()==raw
else:
    tmp=p.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(json.dumps({'receipt':result.get('receipt'),'task':result.get('task'),'artifact':str(p)},ensure_ascii=False))
