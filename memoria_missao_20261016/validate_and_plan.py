"""Pin measured tests and exact additive deployment candidates before installation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,uuid
P=Path(__file__).resolve().parent
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
CORE=Path(r'C:\IALD\MEMORIA_IALD')
def sha(b):return hashlib.sha256(b).hexdigest()
def create(path,raw):
    with path.open('xb') as f:f.write(raw)
def write(path,obj):create(path,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
if (P/'VALIDATION_FINAL.json').exists():raise SystemExit('Use the existing validation receipt; no overwrite.')
results=[]
for name in ['test_mission.py','test_mcp.py']:
    start=datetime.now(timezone.utc)
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(P/name)],capture_output=True,timeout=90)
    end=datetime.now(timezone.utc);log=P/(name+'.FINAL.log');create(log,r.stdout+r.stderr)
    results.append({'test':name,'start':start.isoformat(),'end':end.isoformat(),'seconds':(end-start).total_seconds(),
        'exit':r.returncode,'log':str(log),'sha256':sha(log.read_bytes())})
    if r.returncode:write(P/'VALIDATION_FAILURE_'+str(uuid.uuid4())+'.json',results);raise SystemExit('Tests failed; no deployment plan')
write(P/'VALIDATION_FINAL.json',{'ok':True,'tests':results,'external_provider_calls':0,'scope':'temporary stores; stdio uses inert queue runtime'})
review=json.loads((P/'SUPPLEMENT_FINAL_PIN.json').read_bytes())
files=[(P/'mission.py',CORE/'lib'/'iald_memory'/'mission.py'),(P/'mission_cli.py',CORE/'mission_cli.py'),
       (P/'MISSION_PROTOCOL.md',CORE/'MISSION_PROTOCOL.md'),(P/'mission_bridge.py',BASE/'iald_orchestrator'/'mission_bridge.py'),
       (P/'mcp_server_candidate.py',BASE/'mcp_server.py')]
candidates=P/'deployment_candidates';candidates.mkdir(exist_ok=True)
for name,target,suffix in [('README',CORE/'README.md','README_APPEND.md'),
                          ('AGENTS',Path(r'C:\Users\rotol\.codex\AGENTS.md'),'GLOBAL_APPEND.md'),
                          ('CLAUDE',Path(r'C:\Users\rotol\.claude\CLAUDE.md'),'GLOBAL_APPEND.md')]:
    source=candidates/(name+target.suffix);old=target.read_bytes()
    create(source,old+(P/suffix).read_bytes());files.append((source,target))
plan=[]
for source,target in files:
    old=target.read_bytes() if target.exists() else None;new=source.read_bytes()
    plan.append({'source':str(source),'target':str(target),'old_sha256':sha(old) if old is not None else None,
                 'new_sha256':sha(new),'bytes':len(new),'append_only':new.startswith(old) if old is not None else None})
write(P/'DEPLOY_PLAN.json',{'unit':'F9.MEMORIA_MISSAO_20261016','files':plan,
    'review':{'path':str(P/'SUPPLEMENT_FINAL_PIN.json'),'sha256':sha((P/'SUPPLEMENT_FINAL_PIN.json').read_bytes())},
    'validation':{'path':str(P/'VALIDATION_FINAL.json'),'sha256':sha((P/'VALIDATION_FINAL.json').read_bytes())}})
print(json.dumps({'validation':'PASS','plan_files':len(plan),'plan_sha256':sha((P/'DEPLOY_PLAN.json').read_bytes())}))
