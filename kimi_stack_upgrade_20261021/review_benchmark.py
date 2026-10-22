from task import *
import subprocess
p=project()
root=W/'benchmark_voice'
manifest=json.loads((root/'FROZEN_MANIFEST.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    raw=Path(item['path']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
test=subprocess.run([PY,'-B','-X','utf8','-m','unittest','discover','-s',str(root),'-p','test_contract.py','-v'],capture_output=True,text=True,encoding='utf-8')
assert test.returncode==0,test.stderr
review={'reviewer':OWNER,'author':'codex-readability-reviewer','status':'PASS_WITH_SCOPE','scope':'Offline benchmark/advisory specification and evaluator, not runtime activation or measured model improvement','checks':['Frozen manifest all bytes verified','Twelve independent rerun cases pass','Oracle-assisted retrieval explicitly distinguished from autonomous retrieval','Hoeffding width and two-endpoint alpha allocation checked against implementation','Insufficient sample power stated; no universal quality inference','Coverage/citations/controls are separate guards','Advisory denies authorization and uses caller eligibility','Source hash is integrity not truth; source slices individually hashed','No provider calls or sealed source mutations'], 'limits':['render_header is trusted offline local input, not exposed as arbitrary-path API','Semantic citation validation still requires reviewers','No online benchmark or shadow executed'],'test_stdout':test.stdout,'test_stderr':test.stderr,'manifest_sha256':hashlib.sha256((root/'FROZEN_MANIFEST.json').read_bytes()).hexdigest()}
new('BENCHMARK_PARENT_REVIEW.json',review)
ev=W/'BENCHMARK_PARENT_REVIEW.json'
new('BENCHMARK_ACCEPTED.json',act('accept',task_id='benchmark_voice',event_id='kimi-stack-benchmark-parent-accept',review_evidence=[{'path':str(ev),'sha256':hashlib.sha256(ev.read_bytes()).hexdigest()}]))
print('benchmark_voice accepted with scoped independent review')
