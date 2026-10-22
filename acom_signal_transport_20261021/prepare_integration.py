"""Reuse verified deployment primitives; no runtime writes or process actions."""
from pathlib import Path
import hashlib,json
import task

task.check('engineering')
old=Path(r'C:\IALD\Central de Patentes\work\iald_readability_reliable_tools_20261021')
sources=[]
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    raw=(old/name).read_bytes()
    if name=='transaction.py':
        assert raw.count(b"SHARED_ALLOW = {SHARED/'store.py'}")==1
        raw=raw.replace(b"SHARED_ALLOW = {SHARED/'store.py'}",b'SHARED_ALLOW = set()  # This release changes only app runtime/client assets.')
    task.new(name,raw)
    sources.append({'source':str(old/name),'source_sha256':hashlib.sha256((old/name).read_bytes()).hexdigest(),
                    'staged':str(task.W/name),'staged_sha256':hashlib.sha256(raw).hexdigest()})
task.new('DEPLOY_PRIMITIVES_REUSE.json',{'status':'PREPARED_NOT_EXECUTED','files':sources})
source=task.W/'CONTINUE_20261021.txt'
task.new('INTEGRATION_EXTENDED.json',task.act('extend',event_id='acom-integration-deploy-extend',
    reason='Operador pediu prosseguir após checkpoint; concluir integração e disponibilização.',
    requirements=[{'id':'deployment','criterion':'Plano integrado revisado, instalação controlada com backups e runtime íntegro; validação web autenticada e matriz de disponibilidade mobile/limites explícitos.','depends_on':[]}],
    sources=[{'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]))
task.new('DEPLOYMENT_CLAIM.json',task.act('claim',event_id='acom-integration-deploy-claim',task_id='deployment',lease_seconds=43200))
print(json.dumps({'prepared':len(sources),'deployment_claimed':True}))
