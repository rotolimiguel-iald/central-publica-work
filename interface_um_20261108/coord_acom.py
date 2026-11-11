from pathlib import Path
import hashlib, json, subprocess, sys
root=Path(__file__).resolve().parent
ref=str(root/'SESSION_REFERENCE.json')
actor={'id':'codex-interface-um','kind':'agent'}
def read(op, **fields):
    proc=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(dict(operation=op,reference=ref,**fields)).encode(),stdout=subprocess.PIPE)
    v=json.loads(proc.stdout)
    if not v['ok']: raise RuntimeError(v)
    return v['result']
def pin(name):
    p=root/name
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def snap(): return read('project',max_chars=150000)
def current():
    p=snap();return dict(expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],actor=actor)
if sys.argv[1]=='start':
    read('extend',**current(),event_id='um-acom-native-extend',reason='Telas e instalador de teste solicitados pelo operador.',requirements=[dict(id='acom',criterion='Coordenar a interface com Kimi e entregar instalador de teste por usuário, restauração real e fonte do ACOM não comercial.',depends_on=[])],sources=[pin('ADENDO_ACOM.txt'),pin('ADENDO_INSTALADOR.txt')])
    read('claim',**current(),event_id='um-acom-native-claim',task_id='acom',lease_seconds=43200)
def lease():
    state=read('get')
    for row in reversed(state['q']['records']):
        t=row.get('meta',{}).get('iald_mission_state_v1',{}).get('tasks',{}).get('acom',{})
        if t.get('lease'):return t['lease']['id']
    raise ValueError('missing lease')
if sys.argv[1]=='finish':
    print(read('submit',**current(),task_id='acom',lease_id=lease(),event_id='um-acom-native-candidate',evidence=[pin('REVISAO_ACOM.json')],note='Candidato Windows e telas do Kimi para teste de Luiz.')['receipt']['revision'])
else: print(read('check',**current(),task_id='acom',lease_id=lease())['ready'])
