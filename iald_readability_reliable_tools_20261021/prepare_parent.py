from task import W,new,check
from pathlib import Path
import hashlib,json
OLD=W.parent/'mimo_media_capacity_20261020'
check('implementation')
for name in ['transaction.py','maintenance.py','deploy_controlled.py']:
    (W/name).open('xb').write((OLD/name).read_bytes())
baseline=json.loads((OLD/'SCIENCE_BASELINE.json').read_bytes())
for f in baseline['files']:
    assert hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256']
new('SCIENCE_BASELINE.json',baseline)
new('REUSE.json',dict(parent_delivery=str(OLD/'delivery.json'),extra_test=str(W.parent/'mimo_media_extra_test_20261021/delivery.json'),reason='Reuse existing UI, private media history, wallet and build pipeline; only change requested presentation and new audio/video availability.',nos_vivo='Own unit not indexed; primary receipts consulted'))
new('ROUTE_START.json',dict(tipo='ROTA',rota_id='infra.app.readability_reliable_tools_20261021',dominio='INFRA_IALD',titulo='Leitura compacta e ferramentas confiáveis',pergunta='Como limpar compositor e reduzir fonte mantendo anexos confiáveis e custos corretos?',dados=['App vigente','Recibos de percepção negativa','Documentação oficial DeepSeek'],metodo='Staging separado, revisão, implantação controlada e builds',resultado='Pedido registrado; ciência baseline preservada',veredito='IN_PROGRESS',estatuto='REAL',status='EM_CURSO',olhou_dados=False,nao_refazer='Não repetir testes pagos anteriores nem ciência.',proximo_passo='Conferir stages',onde=str(W),artefatos=[str(W/'REUSE.json')],refs=['infra.app.mimo_media_capacity_20261020']))
print('Parent deployment primitives and baseline preserved')
