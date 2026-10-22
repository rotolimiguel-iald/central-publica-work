"""Local mission client: explicit reference, fresh revision and real caller actor."""
from pathlib import Path
import hashlib,json,subprocess,uuid,sys
W=Path(__file__).resolve().parent; PY=r'C:\Python314\python.exe';REF=W/'SESSION_REFERENCE.json'
UNIT='F9.APP_V394_20261019';OWNER='codex-app-01a094df'
def call(payload,mission=True):
    p=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/('mission_cli.py' if mission else 'session_memory.py'))],input=json.dumps(payload,ensure_ascii=False).encode(),capture_output=True)
    d=json.loads(p.stdout)
    if p.returncode or not d['ok']:raise RuntimeError(d)
    return d['result']
def project():return call({'operation':'project','reference':str(REF),'max_chars':100000})
def act(op,actor=OWNER,**kw):
    current=(call({'operation':'project','reference':str(REF),'max_chars':100000},False) if op=='configure' else project())
    req={'operation':op,'reference':str(REF),'actor':{'id':actor,'kind':'agent'},'expected_revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],**kw}
    return call(req)
def check(task,actor=OWNER):
    p=project();t=next(x for x in p['projection']['active'] if x['id']==task)
    return call({'operation':'check','reference':str(REF),'actor':{'id':actor,'kind':'agent'},'task_id':task,'lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'max_chars':100000})
def new(name,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    with (W/name).open('xb') as f:f.write(raw)
    assert (W/name).read_bytes()==raw
def init():
    source='Nova versão do um.py disponível segundo o que está sendo custodiada agora pelo Claude v394, precisamos atualizar tudo'.encode()
    if not REF.exists():
        new('ORIGINAL.txt',source)
        d=call({'operation':'init','objective_file':str(W/'ORIGINAL.txt'),'objective_sha256':hashlib.sha256(source).hexdigest(),'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':OWNER,'kind':'agent'},'write_reference':str(REF),'constraints':{'unit':UNIT,'scientific_sources_read_only':True,'preserve_accounts_wallet_consents':True,'preserve_activity_memory_and_hajaluz_fix':True}},False)
        new('init_receipt.json',d)
    else:
        assert (W/'ORIGINAL.txt').read_bytes()==source
        call({'operation':'project','reference':str(REF),'max_chars':100000},False)
    requirements=[{'id':'sources','criterion':'Conferir versão394 selada/custodiada, hashes e estatutos, fonte pública sem URL inferida; separar custódia em curso de concluída.','depends_on':[]},{'id':'app','criterion':'Preparar pacote científico394 para todos os motores/JEV, preservando kernelv5 e memória operacional atuais, com proveniência e admissão de contexto medidas. Não instalar nesta etapa.','depends_on':[]},{'id':'queue','criterion':'Preparar/verificar snapshot imutável394 da fila reutilizando rotina existente, sem modificar jobs/generations fixados; ativação fica para deploy.','depends_on':[]},{'id':'deploy','criterion':'Após revisão real independente dos pacotes, ativar fila e app com CAS/backups, instalação/reinício controlados e verificação do carregamento, preservando serviços e tarefas.','depends_on':['sources','app','queue']},{'id':'verify','criterion':'Verificar uso efetivo do pacote394, integridade após implantação, regressão HajaLuz/atividade, matriz web/iOSinterno/externo/Android e memórias atualizadas com recibos; distinguir alteração de backend e necessidade real de build.','depends_on':['deploy']}]
    result=act('configure',requirements=requirements,sources=[{'path':str(W/'ORIGINAL.txt'),'sha256':hashlib.sha256(source).hexdigest()}],event_id='v394-mission-configure')
    new('mission_configured.json',result)
    new('unit.json',[{'id':UNIT,'frente':'F9','titulo':'Atualização conjunta do app, JEV e memória científica para v394','dono':OWNER,'gate':None,'criterio_de_fechado':'Pacotes394 verificados, revisão independente, ativação coordenada e matriz de disponibilidade real.','escopo':'App web/iOS/Android e fila científica; fontes originais somente leitura; preservar carteira, consentimentos, atividade e correção HajaLuz.','consulta':'Mapa INFRA_IALD sem rota394; NósVivo sem unidade; appv392/fila393 medidos. Reutilizar builders e sync existentes, não reconstruir ciência.'}])
    for args in [['nova','--json',str(W/'unit.json'),'--quem',OWNER],['reivindicar',UNIT,'--quem',OWNER,'--nota','Atualização394 autorizada pelo operador; fontes readonly.','--horas','12']]:
        p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True);assert p.returncode==0,p.stdout.decode()+p.stderr.decode()
    print(json.dumps({'status':'REGISTERED','reference':str(REF),'mission_receipt':result.get('receipt')}))
if __name__=='__main__':init()
