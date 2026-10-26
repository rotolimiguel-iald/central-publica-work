from pathlib import Path
import json,hashlib,subprocess,uuid
W=Path(__file__).resolve().parent
PY=r'C:\Python314\python.exe'
REF=W/'SESSION_REFERENCE.json'
OWNER='codex-gerente-tgl'
UNIT='F1.PONTE_NOMEADA'
SOURCE=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_025_a_ponte_nomeada_escala_dual_e_corpo_fisico.md')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(n,d):
    with (W/n).open('xb') as f:f.write(json.dumps(d,ensure_ascii=False,indent=2).encode())
def call(d,mission=True):
    p=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/('mission_cli.py' if mission else 'session_memory.py'))],input=json.dumps(d).encode(),capture_output=True)
    r=json.loads(p.stdout)
    if p.returncode or not r['ok']:raise RuntimeError(r)
    return r['result']
def project():return call({'operation':'project','reference':str(REF),'max_chars':100000})
def act(op,**kw):
    p=call({'operation':'project','reference':str(REF),'max_chars':100000},False) if op=='configure' else project()
    return call({'operation':op,'reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],**kw})
def check():
    p=project();t=next(x for x in p['projection']['active'] if x['id']=='bridge')
    return act('check',task_id='bridge',lease_id=t['lease']['id'])
if __name__=='__main__':
    assert pin(SOURCE)['sha256'].startswith('3fd2b5a801071343')
    new('INIT.json',call({'operation':'init','objective_file':str(SOURCE),'objective_sha256':pin(SOURCE)['sha256'],'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':OWNER,'kind':'agent'},'write_reference':str(REF),'constraints':{'unit':UNIT,'sandbox_only':True,'no_nos_um_git_site_gate_changes':True}},False))
    new('CONFIGURE.json',act('configure',requirements=[{'id':'bridge','criterion':'ORDEM025 A-D: levantamento, instancia DualScalingData e composicao formal compilada em sandbox, normalizacoes e hipoteses explicitas, axiomas no trio, relatorio e mapa para gerencia.','depends_on':[]}],sources=[pin(SOURCE)],event_id='o25-configure'))
    new('UNIT.json',[{'id':UNIT,'frente':'F1','titulo':'ORDEM025 ponte nomeada escala dual e corpo fisico','dono':OWNER,'gate':None,'criterio_de_fechado':'Entrega A-D em sandbox e exame independente pela gerencia','escopo':'Sandbox proprio e entrega ORDEM025; nenhum Nos, um.py, git, site ou gate','consulta':'Nos Vivo nao indexa unidade nova; mapa escala dual localiza kernel.v401_falsidade_da_inercia e formal.f1_rede.concrete_bosonic_kinematics.'}])
    for args in [['nova','--json',str(W/'UNIT.json'),'--quem',OWNER],['reivindicar',UNIT,'--quem',OWNER,'--nota','ORDEM025 sandbox e entrega; memoria propria ACOM apenas.','--horas','12']]:
        p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True)
        if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
    new('CLAIM.json',act('claim',task_id='bridge',lease_seconds=43200,event_id='o25-claim'))
    new('PREFLIGHT.json',check())
    print(json.dumps({'reference':str(REF),'project':project()},ensure_ascii=False))
