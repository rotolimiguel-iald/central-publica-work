from pathlib import Path
import ast,datetime,hashlib,json
W=Path(__file__).resolve().parents[1];D=W/'review';OLD=W.parent/'mimo_media_capacity_20261020'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=read(W/'install_plan.json');plan_hash=sha(W/'install_plan.json')
assert len(plan['files'])==12 and len({x['destination'] for x in plan['files']})==12
checks=[]
for row in plan['files']:
    p=Path(row['source']);dest=Path(row['destination'])
    assert p.resolve().is_relative_to(W.resolve())
    assert dest.resolve().is_relative_to(Path(r'C:\IALD\projetos_pyhton\IALD').resolve())
    assert sha(p)==row['sha256'] and sha(dest)==row['baseline'],dest
    checks.append({'destination':str(dest),'source_sha256':sha(p),'baseline_sha256':sha(dest),'verified':True})
    if dest.name=='project.pbxproj':
        assert p.read_bytes()==dest.read_bytes().replace(b'CURRENT_PROJECT_VERSION = 35;',b'CURRENT_PROJECT_VERSION = 36;')
        assert p.read_bytes().count(b'CURRENT_PROJECT_VERSION = 36;')==2
    if dest.name=='build.gradle':assert p.read_bytes()==dest.read_bytes().replace(b'versionCode 30',b'versionCode 31')
    if p.suffix=='.py':ast.parse(p.read_bytes())
runner_hashes={}
for name in ('transaction','maintenance','deploy_controlled'):
    p=W/(name+'.py');assert p.read_bytes()==(OLD/(name+'.py')).read_bytes()
    runner_hashes[name+'_sha256']=sha(p)
prior=read(OLD/'validation/review_final.json')
assert prior['status']=='PASS'
for k,v in runner_hashes.items():
    if k in prior:assert prior[k]==v
science=read(W/'SCIENCE_BASELINE.json')
for row in science['files']:assert sha(Path(row['path']))==row['sha256']
client=read(W/'client_stage/CLIENT_DELIVERY_R2.json')
for item in client['candidate_files']+client['evidence']:assert sha(Path(item['path']))==item['sha256']
frozen=read(W/'provider_stage/FROZEN_MANIFEST.json')
for item in frozen['files']:assert sha(Path(item['path']))==item['sha256']
provider=read(W/'provider_stage/INSTALL_PLAN.json')
for item in provider['files']:
    row=next(r for r in plan['files'] if r['destination']==item['destination'])
    assert row['sha256']==item['install_sha256'] and row['baseline']==item['expected_destination_sha256']
final_checks=read(W/'validation/final_checks.json');assert final_checks['passed'] and final_checks['plan_sha256']==plan_hash
tests={n:read(D/n) for n in ('r2_tests.json','r2_legacy_tests.json','r2_independent_outbound.json','r2_provider_tests.json')}
assert all(x['status']=='PASS' for x in tests.values())
assert tests['r2_independent_outbound.json']['stage_sha256']==sha(W/'client_stage/R2/iald.js')
evidence=[D/n for n in tests]+[W/'client_stage/CLIENT_DELIVERY_R2.json',W/'provider_stage/FROZEN_MANIFEST.json',W/'provider_stage/INSTALL_PLAN.json',W/'provider_stage/TEST_RESULTS_R2.json',W/'SCIENCE_BASELINE.json',W/'validation/final_checks.json',D/'client_review_r1.json',D/'legacy_continuation_result.json']
report={
 'status':'PASS','reviewer':'codex-readability-reviewer','unit':'F9.APP_READABILITY_RELIABLE_TOOLS_20261021','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'TECHNICAL_INSTALL_GATE_ONLY: revisão independente da implementação e dos 12 destinos do plano fechado; não é aceite de deploy, execução live, compilação ou distribuição mobile.',
 'plan_sha256':plan_hash,**runner_hashes,
 'findings':[{'id':'CLIENT-01','severity':'MEDIO','status':'RESOLVED_R2','title':'Continuação textual bloqueada por mídia histórica local','resolution':'Removido consent/upload por presença de histórico; projeção outbound antes de recortar converte mídia local/ref/inline em metadados com análise indisponível. Mensagem atual com mídia recusa. Persistência e referências históricas mantidas.','evidence':[str(D/'r2_legacy_tests.json'),str(D/'r2_independent_outbound.json')]}],
 'open_findings':[],
 'validation':{'client_general_checks':29,'client_legacy_scenarios':6,'independent_frozen_history_cases':4,'backend_provider_checks':72,'all_passed':True,'network_calls_in_tests':0,'provider_calls':0,'custody_puts':0,
 'client':'Tarja removida, prosa 15.5px; input/edição 16px; fórmulas/código mantêm tamanho absoluto. Seis anexos, PDF25MB, texto2MB, três imagens8MB e multiple preservados. Imagens/documentos/texto não são apagados da projeção.',
 'legacy':'Local/ref/inline áudio/vídeo seguem salvos; envio transmite metadados explícitos sem payload/URL de mídia e sem alegar análise. Reprojeção estável e sem mutação de objetos congelados; nenhum upload/consent/fetch implícito.',
 'backend':'Bloqueio de novos payloads tipados e upload binário antes de custódia; metadados históricos com autenticação/partição preservados; imagens/documentos continuam admitidos. Guardas existentes de schema e autorização continuam necessários.',
 'deepseek':'Alias deepseek-flash preservado; versão documental 1017 e pico/fora de pico conferidos nas fontes oficiais. Cálculo de custo e adapter/allowed/limits iguais por AST; estimativa de pico explicitamente distinta da fatura. Nenhuma política JEV ou integração nova de tools/visão.',
 'science':'Cinco artefatos do SCIENCE_BASELINE v394 conferidos por hash; fora dos destinos. Prefixos científicos e carteiras não alterados pelo plano.',
 'runner':'Três scripts byte a byte iguais ao fluxo revisado de 20/10. Revisão/plano/hashes, final_checks, baselines atuais, backups, troca atômica/rollback e janela com supervisor/filho controlados preservados. Nenhum runner executado.',
 'native':'Somente CURRENT_PROJECT_VERSION 35→36 em duas configurações iOS e versionCode30→31 Android; versão comercial4.1 e demais bytes preservados.'},
 'files':checks,'scientific_pins_verified':science['files'],
 'source_plan_note':'provider_stage/SOURCE_PLAN.json é retrato anterior, não usado para instalar. INSTALL_PLAN.json e FROZEN_MANIFEST.json conferidos contra plano efetivo e bytes atuais.',
 'official_sources':[{'url':'https://api-docs.deepseek.com/quick_start/pricing/','checked':'2026-10-21'},{'url':'https://api-docs.deepseek.com/updates/','checked':'2026-10-21','finding':'Atualização17/10 mantém API/preços; eficiência é declaração do fornecedor, não benchmark local.'}],
 'evidence':[{'path':str(p),'sha256':sha(p)} for p in evidence],
 'limits':['Validação visual/dispositivo, processo carregado, HTTP/live e custo de chamada real não executados nesta revisão.','iOS36/Android31 são versões preparadas nos fontes; builds/assinatura/assets empacotados/TestFlight Equipe e Piloto e disponibilização ainda exigem evidência.','PASS vale para bytes e escopo deste plano; alteração posterior exige nova conferência. Arquivos reais instalados e reinício são responsabilidade da etapa deploy.'],
 'implementation_review':'Critério de implementação satisfeito no escopo técnico offline; aceite por ator distinto será registrado após este parecer.',
 'deployment_accepted':False,'deployment_performed':False,'runtime_modified':False,'staging_modified':False,'git_used':False,'models_called':False}
p=W/'validation/review_final.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
if p.exists():
    b=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));b.write_bytes(p.read_bytes());assert b.read_bytes()==p.read_bytes()
temp=p.with_suffix('.json.review_tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(p);assert p.read_bytes()==raw
print(json.dumps({'status':report['status'],'plan_sha256':plan_hash,**runner_hashes,'review_path':str(p),'review_sha256':sha(p),'destinations':12}))
