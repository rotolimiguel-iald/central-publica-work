import copy,hashlib,json
from pathlib import Path
from session_ops import W,REF,ACTOR,call,save as create
def save(name,obj):
    if (W/name).exists():
        assert json.loads((W/name).read_bytes())==obj
    else:create(name,obj)
def read(p):return json.loads(p.read_bytes())
def pin(p):
    raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
p=call('project');t=p['projection']['active'][0]
save('FINAL_PREFLIGHT.json',call('check',actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],task_id='staging',lease_id=t['lease']['id']))
prep=read(next(W.glob('PREPARATION_*.json')));base=read(W/'BASELINE_PRODUCTION.json')
src=Path(prep['target']);epoch=prep['epoch']
active=Path(base['check']['active_pin']['path']);target=active.parent/'releases'/epoch
manifest=read(src/'manifest.json');final=copy.deepcopy(manifest)
root=target/'snapshots'/epoch
final['snapshot_root']=str(root)
for d in final['documents']:d['path']=str(root/d['name'])
save('MANIFEST_FINAL_CANDIDATE.json',final)
files=[]
for f in sorted(src.rglob('*')):
    if f.is_file() and '.bak_' not in f.name:
        item=pin(f);item['relative_path']=str(f.relative_to(src));item['destination']=str(target/f.relative_to(src))
        item['planned_sha256']=pin(W/'MANIFEST_FINAL_CANDIDATE.json')['sha256'] if f.name=='manifest.json' else item['sha256']
        files.append(item)
plan={'status':'PLAN_ONLY_OPERATOR_GATE_REQUIRED','release':'v409','epoch':epoch,'generation':prep['generation'],'destination':str(target),'active':base['check']['active_pin'],'files':files,'final_manifest_candidate':pin(W/'MANIFEST_FINAL_CANDIDATE.json'),'path_changes':14,'independent_review':'PENDING','operator_authorization':'PENDING','steps':['Revisão independente real do staging e deste plano, sem autoaceite.','Autorização específica do operador vinculada aos pinos para materializar o diretório inativo e depois ativar pela API. Claim/preflight vigentes; não contornar AGUARDA_OPERADOR.','Revalidar originais e baseline; copiar os 16 arquivos aos destinos listados, com o manifesto remapeado; nunca sobrescrever release divergente.','Nos caminhos definitivos conferir integralmente 13 fontes, hashes, todos os trechos e coordenadas de linha, índice e três modos; revisar independentemente os bytes finais.','Somente após revisão final e autorização: API activate_release com expected_active_sha256 do baseline; backup imediato em bytes e lock/CAS; jamais trocar baseline para vencer conflito.','Em processo novo conferir CURRENT/geração/manifesto/recuperação e preservação; então emitir DELIVERY_TECHNICAL_R1.json no esquema da fila.'],'scope':'Nenhuma escrita protegida ou ativação executada por este plano.'}
assert len(files)==16
save('PROMOTION_PLAN.json',plan)
receipts=[W/'VERIFY_STAGING.json',W/'PRESERVATION.json',W/'PROMOTION_PLAN.json',next(W.glob('PREPARATION_*.json')),W/'PREFLIGHT.json']
inputs=[W/'ORIGINAL.txt',Path(r'C:\IALD\TUNEL_CLAUDE_APP\ORDEM_009_release_v409_do_app.md'),W.parent/'custodia_v406_03nov'/'DESPACHO_CODEX_F03_v406.md',W.parent/'scientific_memory_sync_20261013'/'scientific_memory_sync.py',W.parent/'scientific_memory_sync_20261105_v408'/'stage_v408.py',W/'stage_v409.py']
summary={'status':'STAGING_VERIFIED_NOT_ACTIVATED','release':'v409','builder':ACTOR['id'],'reference':REF,'epoch':epoch,'generation':prep['generation'],'documents':prep['documents'],'chunks':prep['chunks'],'stage_manifest':pin(src/'manifest.json'),'stage_index':pin(src/'index.sqlite3'),'initial_check':base['check'],'production_observed':read(W/'PRESERVATION.json'),'receipts':[pin(f) for f in receipts],'inputs':[pin(f) for f in inputs],'pending':['Revisão independente real','Gate específico de escrita protegida','Verificação integral nos caminhos definitivos antes de CAS','Ativação e geração recebida em processo novo: fora do escopo desta tarefa'],'init_recovery':'Init criou contexto mas hard link recusou no sandbox. Reanexado contexto próprio pela API com context_id explícito; request_id da referência igual ao context_id, pois UUID efêmero inicial não foi retido. Nenhuma segunda inscrição.'}
save('STAGING_R1.json',summary)
p=call('project')
r=call('submit',actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],event_id='v409-staging-submitted',task_id='staging',lease_id=t['lease']['id'],evidence=[{k:v for k,v in pin(f).items() if k!='bytes'} for f in (W/'STAGING_R1.json',W/'PROMOTION_PLAN.json')])
save('SUBMISSION.json',r)
route={'rota_id':'infra.memoria_cientifica.sync.v409.staging_20261106','dominio':'INFRAESTRUTURA','status':'EXAMINADA','titulo':'F0.3 v409 staging integral verificado, produção aguardando gate','estatuto':'REAL','veredito':'STAGING_VERIFIED_NOT_ACTIVATED','resultado':'13 fontes,33036 trechos; verificação integral e três modos; ACTIVE v408 preservado.','defeito':'Revisão independente e autorização específica pendentes; não houve ativação.','nao_refazer':'Reutilizar STAGING_R1.json e snapshot pinado, não reconstruir nem adotar outra missão.','proximo_passo':'Revisar PROMOTION_PLAN.json e obter autorização específica da escrita protegida; conferir caminhos definitivos antes de CAS.','fontes':[str(W/'STAGING_R1.json'),str(W/'PROMOTION_PLAN.json')]}
save('ROTA_ENTREGA.json',route)
print(json.dumps({'stage':pin(W/'STAGING_R1.json'),'plan':pin(W/'PROMOTION_PLAN.json'),'final_manifest':pin(W/'MANIFEST_FINAL_CANDIDATE.json'),'submission':r},ensure_ascii=False))
