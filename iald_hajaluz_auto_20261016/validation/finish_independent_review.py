from pathlib import Path
import ast,hashlib,json,datetime
W=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
plan=read(W/'install_plan.json');findings=[];files=[]
for row in plan['files']:
    p=Path(row['source']);b=W/'baseline'/p.name;d=Path(row['destination'])
    checks={'stage':sha(p)==row['sha256'],'baseline':(sha(b) if b.exists() else None)==row['baseline'],'runtime':(sha(d) if d.exists() else None)==row['baseline']}
    ast.parse(p.read_bytes())
    files.append({'name':p.name,'sha256':sha(p),'checks':checks})
    if not all(checks.values()):findings.append({'severity':'MEDIO','file':str(p),'reason':'Hash diverge do plano/base; requer nova revisão.'})
prior=read(W.parent/'iald_app_stack_20261014/validation/review_final.json')
reuse={}
for name in ('transaction','maintenance','deploy_controlled'):
    p=W/(name+'.py');old=W.parent/'iald_app_stack_20261014'/(name+'.py')
    reuse[name]={'sha256':sha(p),'byte_equal':p.read_bytes()==old.read_bytes(),'matches_prior_review':sha(p)==prior[name+'_sha256']}
    if not reuse[name]['byte_equal'] or not reuse[name]['matches_prior_review']:findings.append({'severity':'MEDIO','file':str(p),'reason':'Runner difere da revisão precedente.'})
oldtree=ast.parse((W/'baseline/iald_web_server.py').read_bytes());tree=ast.parse((W/'staging/iald_web_server.py').read_bytes())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_automatico_autorizado')
handlers=next(n for n in fn.body if isinstance(n,ast.Try)).handlers
assert isinstance(handlers[0].type,ast.Attribute) and handlers[0].type.attr=='RoutingContextOverflow'
handlers.pop(0)
web_ast_preserved=ast.dump(tree)==ast.dump(oldtree)
if not web_ast_preserved:findings.append({'severity':'MEDIO','reason':'Mudança adicional no servidor além do handler esperado.'})
contract=read(W/'semantic/contract.json')
program=Path(contract['installed_reference']['program'])
semantic_program_verified=sha(program)==contract['installed_reference']['measured_program_sha256']==contract['installed_reference']['manifest_program_sha256']
if not semantic_program_verified:findings.append({'severity':'MEDIO','reason':'Referência científica do contrato não confere.'})
tests=read(W/'validation/independent_tests.json')
if not tests['passed']:findings.append({'severity':'MEDIO','reason':'Testes independentes falharam.'})
before=read(W/'reproduction.json');after=read(W/'reproduction_fixed.json')
assert [r['context_id'] for r in before['results']]==[r['context_id'] for r in after['results']]
report={
 'status':'BLOCK' if findings else 'PASS','reviewer':'codex-independent-review-hajaluz','unit':plan['unit'],
 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'statute':'REAL — inspeção local e testes offline; recibos de reprodução preexistentes identificados separadamente',
 'scope':'Revisão técnica independente de quatro arquivos e runners de implantação. Não é aceite AUDITADA nem execução de produção.',
 'plan_sha256':sha(W/'install_plan.json'),**{k+'_sha256':v['sha256'] for k,v in reuse.items()},
 'findings':findings,'open_findings':findings,'files':files,'reused_runners':reuse,
 'validation':{'offline_tests':tests['tests'],'passed':tests['passed'],'network_calls':0,'provider_calls':0,'web_ast_identical_except_overflow_handler':web_ast_preserved,'semantic_program_hash_verified_without_execution':semantic_program_verified,
  'required_state':'Objetivo, constraints, flow, decisões, pendências e linhagem de correções preservados integralmente pelo core; overflow obrigatório recusa antes do transporte.',
  'revision_isolation':'Recibo comparado em cada reprojeção; mudança simulada recusa. Escopo cruzado recusa com ScopeViolation; segunda conta não recebe decisão da primeira.',
  'consent_wallet':'Consentimentos e revogação pré/pós-JEV permanecem idênticos por AST; admissão carteira recusada bloqueia envio em teste; carteira/operator_context não são reduzidos.',
  'uncertain_retry':'Timeout sintético produz failed_or_uncertain com uma chamada; nenhuma repetição automática adicionada.',
  'executor_context':'project_messages, histórico cliente e pacote do executor não alterados pelo ajuste; somente trechos de recuperação do seletor e candidatos opcionais ACOM.',
  'production_runner':'Cópia integral dos três runners previamente revisados; exige PASS vinculado a hashes, final_checks vinculado ao plano, bases atuais, supervisor/filho identificados e janela quiescente. Não executado.'},
 'existing_reproduction_metadata':{'source_sha256':sha(W/'reproduction.json'),'fixed_sha256':sha(W/'reproduction_fixed.json'),'before_state_bytes':[r['state_bytes'] for r in before['results']],'after_state_bytes':[r['state_bytes'] for r in after['results']],'before_refused':sum(r['status']=='refused' for r in before['results']),'after_selected':sum(r['status']=='selected' for r in after['results']),'scope':'Comparação somente de metadados existentes; reprodução causal independente executada pela suíte sintética. provider_calls nos recibos são transportes simulados, network_calls=0.'},
 'limitations':['Resposta semântica real de JEV/modelo não medida; contrato DERIVED e instruções não garantem comportamento de provedor.','Suspensão/restart de processos e HTTP de produção não executados.','PASS cobre os bytes deste plano; implantação requer final_checks válido e verificações operacionais do runner.'],
 'execution_notes':['Primeira suíte no sandbox falhou com WinError 5 nos temporários; resultado preservado em backup.','Teste independente de escopo inicialmente esperava PermissionError; corrigido para o tipo real ScopeViolation; produção não mudou.','Fonte própria inscrita e project confirmado; não adotada memória principal.'],
 'memory_reference':str(W/'validation/REVIEW_SESSION_REFERENCE.json'),
 'evidence':{str(p.relative_to(W)):sha(p) for p in [W/'test_fix.py',W/'semantic/test_bootstrap_intent.py',W/'semantic/contract.json',W/'validation/run_independent_tests.py',W/'validation/independent_tests.json',W/'validation/independent_review_source.txt']},
 'deployment_performed':False,'runtime_modified':False,'staging_modified':False,'board_audit_advanced':False}
p=W/'validation/review_final.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
if p.exists():
    backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));backup.write_bytes(p.read_bytes());assert backup.read_bytes()==p.read_bytes()
tmp=p.with_suffix('.json.review_tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p);assert p.read_bytes()==raw
print(json.dumps({'status':report['status'],'tests':tests['tests'],'report':str(p),'sha256':sha(p),'plan_sha256':report['plan_sha256']}))
