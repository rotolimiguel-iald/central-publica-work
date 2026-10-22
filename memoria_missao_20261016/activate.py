"""Reconcile this session's existing mission without constructing new science."""
from pathlib import Path
import hashlib, json, os, sqlite3, subprocess, sys, uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CORE = Path(r'C:\IALD\MEMORIA_IALD')
CENTRAL = ROOT.parent.parent
OUT = CENTRAL/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
OLD = CENTRAL/'work/rede_quantica_20261013/ACOM_REFERENCE.json'
ACTOR = {'id':'codex-gerente-tgl','kind':'agent'}
SCOPE = {'house':'IALD','principal':'luiz-antonio-rotoli-miguel'}
REF = ROOT/'FECHO_MISSION_REFERENCE.json'

def new_bytes(path, raw):
    path=Path(path)
    if path.exists():
        if path.read_bytes()==raw:return
        raise FileExistsError(path)
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.stat().st_size==len(raw)
    os.link(tmp,path);tmp.unlink()

def save(name,value):
    path=ROOT/name
    new_bytes(path,(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8'))
    return path

def pin(path):
    path=Path(path).resolve();raw=path.read_bytes()
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}

def call(cli,payload,name):
    req=ROOT/(name+'_REQUEST.json')
    if req.exists():
        assert json.loads(req.read_bytes())==payload
    else: save(req.name,payload)
    receipt=ROOT/(name+'_RECEIPT.json')
    if receipt.exists():return json.loads(receipt.read_bytes())['result']
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(CORE/cli)],
        input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
    value=json.loads(r.stdout);save(receipt.name,value)
    if r.returncode or not value.get('ok'):raise RuntimeError(value)
    return value['result']

def source(path):
    v=pin(path);return {'kind':'artifact','ref':v['path'],'sha256':v['sha256']}

def prepare():
    snap=call('session_memory.py',{'operation':'get','reference':str(OLD)},'LEGACY_READ')
    assert snap['context_id']=='404cb362-730c-5dbd-a0ad-7d0855ffcce4' and snap['revision']==63
    checkpoint=save('LEGACY_CHECKPOINT.json',snap)
    decisions=[r for r in snap['q']['records'] if r['kind']=='decision' and r['statute']=='INPUT']
    assert len(decisions)==8
    order=next(r for r in decisions if r['id']=='full-completion-order-20261015')
    origin=Path(order['sources'][0]['ref'])
    assert pin(origin)['sha256']==order['sources'][0]['sha256']
    new_bytes(ROOT/'FECHO_ORIGINAL_CUSTODIA.txt',origin.read_bytes())
    # Compare actual bytes: a transcript escape is not a defect in the source file.
    raw=(ROOT/'OPERADOR_VERBATIM.txt').read_bytes()
    own=json.loads((ROOT/'INIT_RECEIPT.json').read_bytes())['result']['snapshot']
    assert hashlib.sha256(raw).hexdigest()==own['objective_sha256']
    save('SOURCE_BYTES_CHECK.json',{'author':'codex-gerente-tgl','statute':'REAL',
        'original':pin(ROOT/'OPERADOR_VERBATIM.txt'),'matches_original_anchor':True,
        'note':'Fonte original e inscrição são idênticas; newline final é real. Não houve correção de transcrição.'})
    provenance=json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    assert pin(provenance['program_path'])['sha256']==provenance['program_sha256']
    assert pin(provenance['seal_path'])['sha256']==provenance['seal_sha256']
    if not (ROOT/'CURRENT_BASIS.json').exists():save('CURRENT_BASIS.json',{'at':datetime.now(timezone.utc).isoformat(),'program':pin(provenance['program_path']),
        'seal':pin(provenance['seal_path']),'version':'v393','provenance':pin(OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json'),
        'meaning':'V351 identifica módulos históricos presentes na v393. A candidata v394 é sandbox; esta leitura não executa o programa.'})
    db=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923/state/tasks.sqlite3'
    con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True);con.row_factory=sqlite3.Row
    tables=[x[0] for x in con.execute("select name from sqlite_master where type='table'")]
    table=next(t for t in tables if {'id','stage','execution_task_id','request_id','prompt'}<=
               {x[1] for x in con.execute('pragma table_info("'+t+'")')})
    handles=[];jobs=[]
    for old in snap['p']['handles']:
        row=dict(con.execute('select id as job_id,stage,execution_task_id from "'+table+'" where id=?',(old['job_id'],)).fetchone())
        jobs.append(row);h=dict(old);h['legacy_status']=h['status'];h['status']=row['stage']
        h['no_repeat']=True;h['execution_task_id']=row['execution_task_id'];handles.append(h)
    con.close()
    jobfile=save('QUEUE_READ_ONLY.json',{'at':datetime.now(timezone.utc).isoformat(),'rows':jobs,
        'actions':[],'scope':'Consulta exata de três jobs desta missão; nenhum envio, cancelamento ou repetição.'})
    files={
      'R1':['network_reuse/INVENTARIO_REAPROVEITAMENTO_R1.json','PROGRESS_R34.json'],
      'R2':['INTEGRATION_QUADRATIC_R3.json','quadratic_review/REVISAO_QUADRATICA_R3_R1.json'],
      'R3':['full_rite/FULL_RITE_OUTPUT_REVIEW_R2.json','full_rite/KH_N1_V394_NETWORK_R8_PREAUDIT.json'],
      'R4':['physical_clock_reuse/PHYSICAL_CLOCK_INVENTORY_R4.json'],
      'R5':['global_net_inventory/INVENTARIO_REDE_GLOBAL_R1.json','orbital_rotation/LOCALITY_WEDGE_ROUTE_INVENTORY_R1.json','PROGRESS_R34.json'],
      'R6':['INTEGRATION_NETWORK_R8.json','PROGRESS_R31.json'],
      'R7':['takesaki_reuse/TAKESAKI_INVENTARIO_R7.json','PROGRESS_R33.json','PROGRESS_R34.json'],
      'R8':['matter_h3_inventory/INVENTARIO_R8_R9_R1.md','INTEGRATION_NETWORK_R8.json'],
      'R9':['R9_H3_SCOPE_R1.json','network_review/R9_H3_SCOPE_SEMANTIC_REVIEW_R1.json'],
      'R10':['network_review/POLAR_FLIP_WEDGE_CLOSURE_REVIEW_R1.json','INTEGRATION_NETWORK_R8.json']}
    progress={
      'R1':('DELIVERED_REVIEW_PENDING','Inventários e 34 progressos existentes; consolidar evolução, sem repetir levantamento inicial.'),
      'R2':('DELIVERED_REVIEW_PENDING','Contrato quadrático integrado e revisão existente; recuperar evidências, não reconstruir.'),
      'R3':('OPEN','Execução integral anterior teve controle offline recusado; pré-auditoria posterior não substitui main da candidata final.'),
      'R4':('OPEN','Reaproveitar normalizações e teste da incompatibilidade; falta identificação física do mesmo dispositivo/relógio.'),
      'R5':('OPEN','Poincaré, cunhas e covariâncias já construídas; integrar localidade global compacta e comparação da rede ao contrato conjunto.'),
      'R6':('OPEN_INTEGRATION','Fock, Weyl/CCR, vácuo standard, Gamma(J), BW e KMS construídos; falta conclusão conjunta no mesmo certificado.'),
      'R7':('OPEN','Peso dual, GNS, Tomita fechado, fluxo e polar construídos; falta traço escalado/PF na representação pretendida. Peso não se confunde com traço.'),
      'R8':('OPEN_INTEGRATION','Campos de Maxwell e tensor conservado construídos em etapas; falta charge_link/normalização e habitante do certificado conjunto.'),
      'R9':('DELIVERED_REVIEW_PENDING','Alcance de H3 classificado; a implicação condicional no curvo não é derivação do antecedente físico a partir do estado.'),
      'R10':('OPEN','Revisões de componentes não satisfazem revisão independente da entrega conjunta atual.')}
    inventory=save('CURRENT_REQUIREMENTS_INVENTORY.json',{'at':datetime.now(timezone.utc).isoformat(),
        'statute':'DERIVED','scope':'Reconciliação documental; arquivos/pinos conferidos, sem recompilar ou promover prova nesta entrega.',
        'requirements':{k:{'state':progress[k][0],'remaining':progress[k][1],
          'evidence':[pin(OUT/f) for f in v]} for k,v in files.items()},
        'not_yet_reconciled':'Recibos de builds iniciados antes da prioridade memória devem ser recolhidos antes de retomar. Não repetir uma unidade de resultado incerto.',
        'legacy_pending_correction':'modular-wedge-open-r1 é retrato antigo; não autoriza reconstruir J, T, S e Delta já documentados nas entregas posteriores.',
        'no_new_science':True})
    init={'operation':'init','objective_file':str(ROOT/'FECHO_ORIGINAL_CUSTODIA.txt'),
        'objective_sha256':pin(ROOT/'FECHO_ORIGINAL_CUSTODIA.txt')['sha256'],
        'request_id':str(uuid.uuid5(uuid.NAMESPACE_URL,'iald:404cb362-730c-5dbd-a0ad-7d0855ffcce4:fecho-mission-v1')),
        'scope':SCOPE,'actor':ACTOR,'write_reference':str(REF),
        'constraints':{'unit':'F1.FECHO_20261015','production_changes':False,'basis_receipt':str(ROOT/'CURRENT_BASIS.json'),
           'predecessor_reference':str(OLD),'memory_first_unit':'F9.MEMORIA_MISSAO_20261016'}}
    call('session_memory.py',init,'FECHO_INIT')
    records=decisions+[
       {'id':'migration-origin-v1','kind':'fact','statute':'REAL','text':'Sucessor explícito da mesma missão, com a ordem posterior de conclusão. Original/revisão 63 permanecem íntegros e recuperáveis. Todas as oito decisões INPUT foram preservadas; demais registros estão no checkpoint pinado. Não adota missão alheia.',
        'sources':[source(checkpoint),source(OLD),source(ROOT/'FECHO_ORIGINAL_CUSTODIA.txt')]},
       {'id':'memory-first-v1','kind':'decision','statute':'INPUT','text':(ROOT/'OPERADOR_VERBATIM.txt').read_text(encoding='utf-8'),
        'sources':[source(ROOT/'OPERADOR_VERBATIM.txt')]},
       {'id':'current-basis-v1','kind':'fact','statute':'REAL','text':'Programa/selo correntes v393 conferidos por bytes. V351 é o nome de módulos reaproveitados dentro da v393; v394 é candidata de sandbox.',
        'sources':[source(ROOT/'CURRENT_BASIS.json')]},
       {'id':'inventory-current-v1','kind':'fact','statute':'DERIVED','text':'R1/R2/R9 têm entregas para revisão; R3–R8 e R10 conservam resíduos específicos. Inventário pinado detalha reaproveitamento. A pendência antiga de J/T/S/Delta não descreve a construção posterior. Recolher resultados já em voo antes de qualquer novo build.',
        'sources':[source(inventory),source(checkpoint)]},
       {'id':'queue-current-v1','kind':'fact','statute':'REAL','text':'Um job completed e dois awaiting_dispatch verificados no banco. Nenhum foi enviado, cancelado ou repetido; dois pendentes impedem cláusula de parada.',
        'sources':[source(jobfile)]}]
    assert not any(r.get('supersedes') for r in decisions)
    call('session_memory.py',{'operation':'transition','reference':str(REF),'expected_revision':0,
        'event_id':'fecho-migration-v1','actor':ACTOR,'changes':{'records':records,
        'flow':{'phase':'memory_priority','next_action':'Concluir validação da memória M0; depois integrar apenas resíduos R1–R10 e recuperar execuções pendentes sem repetir.', 'handles':handles}}},'FECHO_MIGRATE')
    req=json.loads((OUT/'REQUISITOS_ORIGINAIS_R1.json').read_bytes())
    requirements=[{'id':'M0_MEMORIA','criterion':'Instalar controlador ACOM/CLI/MCP/instruções, verificar testes e revisão independente, reconciliar a mesma missão preservando ordens/IDs/evidências. Aceite técnico, sem fecho científico.','depends_on':[]}]
    for r in req['requirements']:
        depends=['M0_MEMORIA']
        if r['id']=='R3':depends+=['R2','R4','R5','R6','R7','R8','R9']
        if r['id']=='R10':depends+=[f'R{i}' for i in range(1,10)]
        requirements.append({'id':r['id'],'criterion':r['requirement']+'. '+r['acceptance_evidence'],'depends_on':depends})
    save('MISSION_REQUIREMENTS.json',{'requirements':requirements,'original':pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        'derivation':'Texto original dos dez critérios preservado. Dependências operacionais derivadas pela coordenação; M0 aplica prioridade posterior do operador.'})
    call('mission_cli.py',{'operation':'configure','reference':str(REF),'expected_revision':1,
        'event_id':'fecho-configure-v1','actor':ACTOR,'requirements':requirements,
        'sources':[pin(ROOT/'MISSION_REQUIREMENTS.json'),pin(inventory)]},'FECHO_CONFIGURE')
    v=call('mission_cli.py',{'operation':'project','reference':str(REF),'max_chars':48000},'FECHO_INITIAL_PROJECT')
    print(json.dumps({'reference':str(REF),'chars':v['actual_chars'],'revision':v['receipt']['revision'],
        'next_ready':v['projection']['next_ready'],'tetelestai':v['projection']['tetelestai']}))

if __name__=='__main__':prepare()
