from pathlib import Path
import hashlib, json, subprocess

BASE = Path(__file__).resolve().parent
REF = str(BASE.parent / 'SESSION_REFERENCE.json')
PY = r'C:\Python314\python.exe'
CLI = r'C:\IALD\MEMORIA_IALD\mission_cli.py'
ACTOR = {'id': 'codex-astra-bell', 'kind': 'agent'}

def call(op, **kwargs):
    req = dict(operation=op, reference=REF, **kwargs)
    p = subprocess.run([PY, '-B', '-X', 'utf8', CLI], input=json.dumps(req, ensure_ascii=False), text=True, encoding='utf-8', capture_output=True)
    r = json.loads(p.stdout)
    if not r.get('ok'): raise RuntimeError(r)
    return r['result']

def save(name, data):
    path = BASE / name
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    if path.exists():
        if path.read_bytes() != raw: raise RuntimeError('Existing file differs: '+name)
    else:
        tmp = path.with_suffix(path.suffix+'.tmp'); tmp.write_bytes(raw)
        assert tmp.stat().st_size == len(raw); tmp.replace(path)

if __name__ == '__main__':
    order = 'Prossiga na bancada com H0DN × BG1. Monte a covariância completa e rode as injeções cegas pra vermos se os 5 sigma se sustentam. Sobre a travessia do par, me faça a pergunta aqui nas minhas quatro línguas.'
    src = BASE / 'ORDEM_H0DN.txt'
    if not src.exists(): src.write_bytes(order.encode('utf-8'))
    p = call('project', max_chars=50000)
    r = call('extend', actor=ACTOR, expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'], event_id='h0dn-bg1-extend-06nov', requirements=[{'id':'h0dn_bg1','criterion':'Construir A e C da rede H0DN e BG1 com proveniência; congelar e executar injeções com rótulos ocultos; quantificar separação, poder a 5 sigma e limites sistemáticos sem ajuste observado','depends_on':[]}], reason='Continuidade explicitamente ordenada pelo operador', sources=[{'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}])
    save('MISSION_EXTEND.json',r)
    p=call('project', max_chars=50000)
    r=call('claim', actor=ACTOR, expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'],event_id='h0dn-bg1-claim-06nov',task_id='h0dn_bg1',lease_seconds=43200)
    save('MISSION_CLAIM.json',r)
    p=call('project',max_chars=50000); save('MISSION_PROJECT.json',p)
    print(json.dumps(p,ensure_ascii=False))
