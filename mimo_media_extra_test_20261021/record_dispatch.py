from pathlib import Path
import json,subprocess
W=Path(__file__).resolve().parent
old=W.parent/'mimo_media_capacity_20261020/live_stage/capture_manual_audio.py'
s=old.read_text(encoding='utf-8')
before="JOBS={'MANUAL_AUDIO':('d7f3e284-cd11-46f3-aa8d-4a51e60c5d23','c_mvh8g01bjpvy')}"
after="JOBS={'AUTO_AUDIO_EXTRA':('19c04a21-56a4-41da-903b-a9ade95ad327','c_mvh97slgc1s0')}"
assert s.count(before)==1
s=s.replace(before,after);compile(s,'capture','exec')
(W/'capture_extra_audio.py').open('x',encoding='utf-8').write(s)
def call(q):
    p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(q).encode(),capture_output=True)
    d=json.loads(p.stdout);assert d['ok'],d;return d['result']
ref=str(W/'SESSION_REFERENCE.json');c=call(dict(operation='get',reference=ref))
r=call(dict(operation='transition',reference=ref,actor=dict(id='codex-app-01a094df',kind='agent'),expected_revision=c['receipt']['revision'],event_id='extra-audio-dispatched-once',changes=dict(flow=dict(phase='test_running',next_action='Acompanhar mesmo job, nunca reenviar.',handles=[dict(id='auto-audio-extra',provider='IALD_APP',external_id='19c04a21-56a4-41da-903b-a9ade95ad327',status='running')]))))
(W/'DISPATCH_MEMORY.json').open('xb').write(json.dumps(r,indent=2).encode())
print('Job único custodiado; captura somente leitura preparada')
