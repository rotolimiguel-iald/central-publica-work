"""Local mission client: explicit reference, fresh revision and real caller actor."""
from pathlib import Path
import hashlib,json,subprocess,uuid,sys
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W))
import release_cfg
cfg=release_cfg.load()
REL=cfg.release
PY=r'C:\Python314\python.exe';REF=W/'SESSION_REFERENCE.json'
UNIT=cfg.unit;OWNER=cfg.owner
ACTOR=cfg.builder  # v402: a gerencia mandou inscrever (init/configure/quadro) com o id do CONSTRUTOR; OWNER segue sendo o dono da unidade e quem faz o deploy.
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
    # A ordem original e do OPERADOR: a gerencia a grava VERBATIM em ORDEM_DO_OPERADOR.txt; o script nao a inventa.
    order=W/'ORDEM_DO_OPERADOR.txt'
    if not order.is_file():raise SystemExit('PARADA: grave em '+str(order)+' a ordem VERBATIM do operador para a '+REL+' (a gerencia fornece; este script nao a inventa). Nenhuma missao foi criada.')
    source=order.read_bytes()
    if not source.strip():raise SystemExit('PARADA: ORDEM_DO_OPERADOR.txt esta vazio. Nenhuma missao foi criada.')
    if not REF.exists():
        # v402: a gerencia ja gravou ORIGINAL.txt (bytes identicos a ORDEM_DO_OPERADOR.txt); aceita so se identico, nunca sobrescreve.
        if (W/'ORIGINAL.txt').exists():assert (W/'ORIGINAL.txt').read_bytes()==source,'ORIGINAL.txt difere da ordem do operador'
        else:new('ORIGINAL.txt',source)
        d=call({'operation':'init','objective_file':str(W/'ORIGINAL.txt'),'objective_sha256':hashlib.sha256(source).hexdigest(),'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':ACTOR,'kind':'agent'},'write_reference':str(REF),'constraints':{'unit':UNIT,'scientific_sources_read_only':True,'preserve_accounts_wallet_consents':True,'preserve_activity_memory_and_hajaluz_fix':True}},False)
        new('init_receipt.json',d)
    else:
        assert (W/'ORIGINAL.txt').read_bytes()==source
        call({'operation':'project','reference':str(REF),'max_chars':100000},False)
    requirements=[{'id':'sources','criterion':'Conferir a versão '+REL+' selada/custodiada (cofre e Nós), hashes e estatutos, e a fonte pública do espelho no commit PINADO, sem URL inferida; separar custódia em curso de concluída.','depends_on':[]},{'id':'app','criterion':'Preparar o pacote científico '+REL+' para todos os motores/JEV, preservando o kernel v5 e a memória operacional atuais, com proveniência e admissão de contexto medidas. Não instalar nesta etapa.','depends_on':[]},{'id':'deploy','criterion':'Após revisão real independente do pacote, ativar o app com backups/CAS, instalação e reinício controlados do filho web e verificação do carregamento, preservando serviços e tarefas.','depends_on':['sources','app']},{'id':'verify','criterion':'Verificar o uso efetivo do pacote '+REL+' (login 200, release no manifest, resposta do app citando a '+REL+'), integridade após a implantação e memórias atualizadas com recibos; distinguir alteração de backend e necessidade real de build.','depends_on':['deploy']}]
    result=act('configure',requirements=requirements,sources=[{'path':str(W/'ORIGINAL.txt'),'sha256':hashlib.sha256(source).hexdigest()}],event_id=REL+'-mission-configure',actor=ACTOR)
    new('mission_configured.json',result)
    new('unit.json',[{'id':UNIT,'frente':'F9','titulo':'Atualização do app, JEV e memória científica para '+REL,'dono':OWNER,'gate':None,'criterio_de_fechado':'Pacote '+REL+' verificado, revisão independente, implantação controlada do filho web e verificação do carregamento e do uso efetivo.','escopo':'App web/iOS/Android (backend compartilhado); fontes originais somente leitura; preservar carteira, consentimentos, atividade e correção HajaLuz. A fila científica tem unidade própria.','consulta':'Mapa de rotas: consultas "app release" e "app v401" em 27/10 retornaram 0 rotas (1473 registros). Pipeline de referência: work/iald_v401_20261025_s2 (instalada e aceita por revisor independente). Ordem do operador: ORDEM_DO_OPERADOR.txt desta pasta.'}])
    for args in [['nova','--json',str(W/'unit.json'),'--quem',ACTOR],['reivindicar',UNIT,'--quem',ACTOR,'--nota','Construção '+REL+' do app pelo construtor; fontes somente leitura; ordem do operador em ORDEM_DO_OPERADOR.txt; a gerência assume na revisão/deploy.','--horas','6']]:
        p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True);assert p.returncode==0,p.stdout.decode()+p.stderr.decode()
    print(json.dumps({'status':'REGISTERED','reference':str(REF),'mission_receipt':result.get('receipt')}))
if __name__=='__main__':init()
