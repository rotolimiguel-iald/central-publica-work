"""Reviewer (sonnet-app-v404-revisor): independent, READ-ONLY review of the v404 DEPLOY.
psutil is used only for queries (no process touched); the runtime tree is swept with os.scandir/os.stat only (no file opened, .env and .iald_secret_key included);
plan destinations are hashed; the only network access is one GET http://127.0.0.1:8082/login. Output: JSON on stdout."""
import os,sys,json,hashlib,re,time,datetime,subprocess,http.client
from pathlib import Path
import psutil
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027');R=Path(r'C:\IALD\projetos_pyhton\IALD')
RV=W/'review/revisor_sonnet-app-v404-revisor';ME='sonnet-app-v404-revisor'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
checks=[]
def chk(group,desc,ok,achado=None):
    checks.append({'n':len(checks)+1,'grupo':group,'descricao':desc,'ok':bool(ok),'achado':achado})
plan_path=W/'install_plan.json';plan=rd(plan_path);dep=rd(W/'deployment.json');mt=rd(W/'maintenance.json');rs=rd(W/'restart.json')
rel=rd(W/'app/RELEASE.json');rf=rd(W/'validation/review_final.json');fc=rd(W/'validation/final_checks.json')
installed_at=datetime.datetime.fromisoformat(dep['installed_at']).timestamp()
t_m=(W/'maintenance.json').stat().st_mtime
# ---------------- A_RECIBO
sub=rd(W/'receipts/v404-deploy-submit.json')['task']
bad=[Path(e['path']).name for e in sub['evidence'] if sha(e['path'])!=e['sha256']]
chk('A_RECIBO','recibo v404-deploy-submit: deploy review_pending, submetido por claude-gerencia-a7 (distinto do revisor); as 4 evidencias (deployment, maintenance, restart, install_plan) tem sha256 = bytes ATUAIS',
    sub['status']=='review_pending' and sub['submitted_by']=='claude-gerencia-a7' and sub['submitted_by']!=ME and len(sub['evidence'])==4 and not bad,{'status':sub['status'],'by':sub['submitted_by'],'stale':bad})
pj=json.loads(subprocess.check_output([r'C:\Python314\python.exe','-B','-X','utf8',str(W/'mission_step.py'),'project'],cwd=str(W)))
act={t['id']:t['status'] for t in pj['active']}
acc={n:rd(W/f'receipts/v404-{n}-accept-r2.json')['task'] for n in('app','sources')}
accbad=[Path(e['path']).name for n in acc for e in acc[n]['evidence']+acc[n]['review_evidence'] if sha(e['path'])!=e['sha256']]
chk('A_RECIBO','missao (project, somente leitura): deploy review_pending, verify needs_revalidation (ainda nao reclamado); app e sources SATISFEITOS pela minha revisao independente da r2 (reviewed_by = eu, submitted_by = construtor) com todas as evidencias pinadas = bytes atuais',
    act=={'deploy':'review_pending','verify':'needs_revalidation'} and all(acc[n]['status']=='satisfied' and acc[n]['reviewed_by']==ME and acc[n]['submitted_by']=='sonnet-app-v404-construtor' for n in acc) and not accbad,{'active':act,'revision':pj['revision'],'accept_evidence_stale':accbad})
mt_=lambda p:(W/p).stat().st_mtime
order=[('accept app r2',mt_('receipts/v404-app-accept-r2.json')),('claim deploy',mt_('receipts/v404-deploy-claim.json')),('maintenance.json',t_m),('installed_at',installed_at),('restart.json',mt_('restart.json')),('submit deploy',mt_('receipts/v404-deploy-submit.json')),('INSTALLED_VERIFICATION',mt_('INSTALLED_VERIFICATION.json'))]
chk('A_RECIBO','ordem temporal: aceite da revisao do pacote (r2) < claim do deploy < janela de manutencao < instalacao < restart.json < submit < INSTALLED_VERIFICATION (o deploy veio DEPOIS da revisao; evidencias nao regravadas)',
    all(order[i][1]<order[i+1][1] for i in range(len(order)-1)),[(n,datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S.%f')[:12]) for n,t in order])
baks=[p.name for n in('deployment','maintenance','restart') for p in W.glob(n+'.json.bak_*')]
chk('A_RECIBO','deployment.json, maintenance.json e restart.json existem em UMA versao cada (sem .bak_ ao lado: nao foram regravados)',not baks,baks)
# ---------------- B_PLANO
plan_sha=sha(plan_path)
pins={'recomputado':plan_sha,'deployment.plan_sha256':dep['plan_sha256'],'final_checks':fc['plan_sha256'],'review_final':rf['plan_sha256'],
      'pino_do_submit_r2_do_pacote':next(e['sha256'] for e in rd(W/'receipts/v404-app-submit-r2.json')['task']['evidence'] if e['path'].endswith('install_plan.json'))}
chk('B_PLANO','plano: sha256 recomputado de install_plan.json = deployment.plan_sha256 = final_checks.plan_sha256 = review_final.plan_sha256 = pino do recibo de submit r2 do pacote',len(set(pins.values()))==1,{k:v[:16] for k,v in pins.items()})
chk('B_PLANO','deployment.json: status INSTALLED_RESTART_REQUIRED; accounts_modified=false, bench_restarted=false, client_files_changed=false; runtime_python_changes=0 no plano',
    dep['status']=='INSTALLED_RESTART_REQUIRED' and dep['accounts_modified'] is False and dep['bench_restarted'] is False and dep['client_files_changed'] is False and plan['runtime_python_changes']==0,{'installed_at':dep['installed_at']})
pd=[r['destination'] for r in plan['files']]
chk('B_PLANO','deployment.files tem EXATAMENTE os %d destinos do plano, na mesma ordem, sem duplicata (nada a mais, nada a menos)'%len(pd),list(dep['files'])==pd and len(set(pd))==len(pd),{'n_plan':len(pd),'n_dep':len(dep['files'])})
bh=[d for d,r in zip(pd,plan['files']) if not(dep['files'][d]==r['sha256']==sha(d))]
chk('B_PLANO','para cada um dos %d destinos: sha256 em deployment.files = sha256 do plano = sha256 dos BYTES hoje em disco (recomputado agora)'%len(pd),not bh,{'divergentes':bh[:3]})
pre=[r for r in plan['files'] if r['baseline'] is not None];new=[r for r in plan['files'] if r['baseline'] is None];unch=[r for r in pre if r['baseline']==r['sha256']]
chk('B_PLANO','classificacao do plano: %d destinos pre-existentes que mudam (6 de .iald_runtime + manifesto ativo), %d criados (baseline nulo), %d inalterados'%(len(pre),len(new),len(unch)),len(pre)==7 and len(new)==len(pd)-7 and not unch,{'pre':[Path(r['destination']).name for r in pre]})
bk=dep['backups'];bkbad=[];stamps=set()
for d,r in ((r['destination'],r) for r in pre):
    b=bk.get(d)
    if not b or not Path(b).is_file() or Path(b).parent!=Path(d).parent or sha(b)!=r['baseline'] or sha(b)==r['sha256']:bkbad.append(d);continue
    stamps.add(b.rsplit('.bak_',1)[1])
orph=[]
for d in {Path(r['destination']).parent for r in pre}:
    for p in d.glob('*.bak_*'):
        if p.name.endswith(next(iter(stamps),'~')) and str(p) not in bk.values():orph.append(str(p))
chk('B_PLANO','backups: deployment.backups = exatamente os 7 destinos que mudam; cada .bak_ existe na pasta do destino, tem os BYTES do estado anterior (sha256 = baseline do plano), difere do novo; um unico carimbo; nenhum .bak_ orfao do mesmo carimbo',
    set(bk)=={r['destination'] for r in pre} and not bkbad and len(stamps)==1 and not orph,{'stamps':list(stamps),'bad':bkbad,'orphans':orph})
v2=rd(V2/'deployment.json')['files'];chain=[d for d in bk if sha(bk[d])!=v2.get(d)]
chk('B_PLANO','cadeia com a v402: o conteudo de cada um dos 7 backups = o sha256 que a v402 registrou como instalado em deployment.json (o backup guardou exatamente a v402 aceita, nao um estado intermediario)',not chain and len(bk)==7,{'divergentes':chain})
can=R/'canonical_releases'/('v404_'+rel['espelho_commit'][:12]);ondisk={str(p) for p in can.rglob('*') if p.is_file()};inplan={d for d in pd if Path(d).is_relative_to(can)}
chk('B_PLANO','canonical_releases\\v404_1d3c4cbe3f3c: o conjunto de arquivos em disco = exatamente os destinos do plano sob essa pasta (nenhum arquivo instalado a mais, nenhum a menos)',ondisk==inplan,{'disk':len(ondisk),'plan':len(inplan),'extra':sorted(ondisk-inplan)[:3],'missing':sorted(inplan-ondisk)[:3]})
base=rd(W/'app/RUNTIME_BASELINE.json')['files'];bchg=[b['path'] for b in base if sha(b['path'])!=b['sha256']]
rootpy_now={str(p) for p in R.glob('*.py')};rootpy_base={b['path'] for b in base if Path(b['path']).parent==R and b['path'].endswith('.py')}
nuc=R/'iald_nucleo_fixo.json';nuc_plan=next(r for r in plan['files'] if r['destination']==str(nuc))
chk('B_PLANO','codigo de runtime preservado: todos os %d arquivos de RUNTIME_BASELINE.json (tirado ANTES do deploy) tem o sha256 de antes; o conjunto de .py da raiz nao mudou (so o confidencial iald_stack_v7.py fica fora do baseline por desenho, nunca aberto); o unico arquivo do baseline que muda e o manifesto ativo; o plano nao escreve .py de runtime; o manifesto ativo mudou do baseline para o do plano'%len(base),
    set(bchg)=={str(nuc)} and rootpy_base<=rootpy_now and (rootpy_now-rootpy_base)=={str(R/'iald_stack_v7.py')} and max((R/'iald_stack_v7.py').stat().st_mtime,(R/'iald_stack_v7.py').stat().st_ctime)<t_m and not [d for d in pd if Path(d).parent==R and d.endswith('.py')] and sha(nuc)==nuc_plan['sha256'] and sha(bk[str(nuc)])==nuc_plan['baseline'],{'baseline_files':len(base),'unico_arquivo_do_baseline_que_mudou':[Path(x).name for x in bchg],'root_py_now':len(rootpy_now),'root_py_baseline':len(rootpy_base),'extra_fora_do_baseline':sorted(Path(x).name for x in rootpy_now-rootpy_base),'nota':'iald_stack_v7.py e confidencial: excluido do baseline por desenho, so stat (mtime/ctime anteriores a janela), nunca aberto'})
st=W/'app/science/memory_stage';pk=W/'app/packages'
pairs=[(R/'.iald_runtime/haiku55/prefix.md',pk/'haiku_expanded/prefix.md'),(R/'.iald_runtime/haiku55/manifest.json',pk/'haiku_expanded/manifest_install.json'),(R/'.iald_runtime/haiku55/native_count.json',pk/'haiku_expanded/native_count.json'),
       (R/'.iald_runtime/haiku/prefix.md',pk/'shared/prefix.md'),(R/'.iald_runtime/haiku/manifest.json',pk/'shared/manifest_install.json'),(R/'.iald_runtime/haiku/native_count.json',pk/'shared/native_count.json'),
       (nuc,st/'manifest_install.json'),(R/'core_packet_v404_bound.txt',st/'core_packet_v404_bound.txt')]
pb=[a.name for a,b in pairs if a.read_bytes()!=b.read_bytes()]
chk('B_PLANO','pacotes instalados = pacotes REVISADOS byte a byte (r2): haiku55/{prefix,manifest,native_count} = haiku_expanded; haiku/{...} = shared; manifesto ativo = manifest_install do estagio; pacote do Jev da raiz = o do estagio',not pb,{'pairs':len(pairs),'diff':pb})
code=['transaction.py','maintenance.py','deploy_controlled.py','verify_installed.py'];rec={'transaction.py':rf['transaction_sha256'],'maintenance.py':rf['maintenance_sha256'],'deploy_controlled.py':rf['deploy_controlled_sha256'],'verify_installed.py':rf['verify_installed_sha256']}
cb=[c for c in code if sha(W/c)!=rec[c] or sha(W/c)!=sha(V2/c)]
chk('B_PLANO','o deploy usou o codigo REVISADO: transaction/maintenance/deploy_controlled/verify_installed = bytes que review_final.json registrou = bytes da v402 aceita',not cb,{'divergentes':cb})
# ---------------- C_REINICIO
def web():
    out=[]
    for p in psutil.process_iter(['name']):
        try:
            if (p.info['name'] or '').lower()=='python.exe' and any(a and str(Path(a)).lower()==str(R/'iald_web_server.py').lower() for a in p.cmdline()[1:] if not a.startswith('-')):out.append(p)
        except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
    return out
def listeners(port):return [c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==port]
chk('C_REINICIO','maintenance.json: ADMISSIONS_STOPPED, filho antigo 41280, supervisor 38024; restart.json: PASS, HTTP 200, filho novo 69428 != 41280, MESMA identidade do supervisor (pid e create_time) que maintenance.json',
    mt['status']=='ADMISSIONS_STOPPED' and mt['old_web_pid']==41280 and mt['supervisor_pid']==38024 and rs['status']=='PASS' and rs['http_status']==200 and rs['new_web_pid']==69428!=rs['old_web_pid'] and (rs['supervisor_pid'],rs['supervisor_created'])==(mt['supervisor_pid'],mt['supervisor_created']),{'restart_scope':rs['restart_scope']})
snap=lambda:[(p.pid,p.ppid(),p.create_time()) for p in web()]
w1=web();l1=listeners(8082)
chk('C_REINICIO','AGORA: exatamente UM processo python.exe rodando iald_web_server.py, exatamente UM ouvinte na 8082, e ambos sao o PID new_web_pid do restart.json (69428)',len(w1)==1 and len(l1)==1 and w1[0].pid==l1[0].pid==rs['new_web_pid'],{'web':[p.pid for p in w1],'listeners':[c.pid for c in l1]})
child=w1[0];sup=child.parent()
chk('C_REINICIO','o filho 69428 esta sob o MESMO supervisor: ppid = 38024, create_time do supervisor IDENTICO ao de restart.json/maintenance.json (mesma instancia, nao um supervisor novo), roda start_iald_web.ps1 sem -NoSupervise, e nem ele nem o filho estao suspensos',
    child.ppid()==rs['supervisor_pid'] and sup.create_time()==rs['supervisor_created'] and any(str(Path(a)).lower()==str(R/'start_iald_web.ps1').lower() for a in sup.cmdline()[1:] if a and not a.startswith('-')) and not any(a.lower()=='-nosupervise' for a in sup.cmdline()) and sup.status()!=psutil.STATUS_STOPPED and child.status()!=psutil.STATUS_STOPPED,
    {'ppid':child.ppid(),'sup_created':datetime.datetime.fromtimestamp(sup.create_time()).isoformat(),'sup_status':sup.status(),'child_status':child.status(),'child_created':datetime.datetime.fromtimestamp(child.create_time()).isoformat()})
chk('C_REINICIO','o filho novo nasceu DEPOIS da instalacao (create_time > installed_at: pode ter carregado os arquivos novos) e o PID antigo 41280 nao existe mais',child.create_time()>installed_at and not psutil.pid_exists(mt['old_web_pid']),{'child_minus_installed_s':round(child.create_time()-installed_at,1)})
since=[];bench={}
for p in psutil.process_iter(['pid','name','create_time','status']):
    try:
        cl=' '.join(p.cmdline())
        if p.info['create_time']>=t_m-1 and any(k in cl.lower() for k in('iald','llama','bancada')) and p.pid!=os.getpid():since.append((p.pid,p.info['name'],cl[:110]))
    except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
for port,label in((8081,'llama'),(18777,'Bancada Um'),(18765,'gw'),(18766,'cosmologia')):
    for c in listeners(port):
        p=psutil.Process(c.pid);bench[label]={'port':port,'pid':c.pid,'created_before_window':p.create_time()<t_m,'suspended':p.status()==psutil.STATUS_STOPPED,'created':datetime.datetime.fromtimestamp(p.create_time()).strftime('%m-%d %H:%M:%S')}
chk('C_REINICIO','bench e llama: os servicos que ESCUTAM agora (llama 8081, Bancada Um 18777, e 18765/18766 se existirem) foram criados ANTES da janela do deploy e nao estao suspensos (nao foram reiniciados); processos IALD criados desde a janela listados para a gerencia',
    'llama' in bench and 'Bancada Um' in bench and all(v['created_before_window'] and not v['suspended'] for v in bench.values()),{'bench':bench,'criados_desde_a_janela':since})
conn=http.client.HTTPConnection('127.0.0.1',8082,timeout=20);conn.request('GET','/login');resp=conn.getresponse();status=resp.status;resp.read(1<<20);conn.close()
chk('C_REINICIO','GET local http://127.0.0.1:8082/login = 200 (unico acesso de rede deste revisor; corpo descartado)',status==200,{'http':status})
w2=web();l2=listeners(8082)
chk('C_REINICIO','depois do GET: ainda um unico processo web, mesmo PID, mesmo create_time, mesmo supervisor e o mesmo ouvinte (o servidor nao reiniciou durante a revisao)',
    [(p.pid,p.ppid(),p.create_time()) for p in w2]==[(p.pid,p.ppid(),p.create_time()) for p in w1] and [c.pid for c in l2]==[c.pid for c in l1],{'pid':w2[0].pid})
# ---------------- D_MANIFESTO
m=rd(nuc);old=rd(bk[str(nuc)])
f3=lambda x:(x['active_cluster']['release'],x['operational_core']['current_release'],x['jev_control']['release'])
src=lambda x:(x['active_cluster']['release_source_sha256'],x['operational_core']['release_source_sha256'],x['jev_control']['source_sha256'])
chk('D_MANIFESTO','iald_nucleo_fixo.json de producao AGORA: active_cluster.release, operational_core.current_release e jev_control.release = v404 (backup: v402 nos tres); commit = RELEASE.espelho_commit; release_source_sha256/source_sha256 = RELEASE.um_py_sha256; publication_pending=false',
    f3(m)==('v404',)*3 and f3(old)==('v402',)*3 and m['active_cluster']['commit']==rel['espelho_commit'] and set(src(m))=={rel['um_py_sha256']} and m['active_cluster'].get('publication_pending') is False,{'agora':f3(m),'backup':f3(old),'commit':m['active_cluster']['commit'][:12],'source_sha':rel['um_py_sha256'][:16]})
paths=[];bad=[]
def walk(x):
    if isinstance(x,dict):
        p=x.get('path')
        if isinstance(p,str) and p.startswith(str(R)):
            paths.append(p);s=x.get('sha256') or x.get('public_sha256')
            if not Path(p).exists() or (s and Path(p).is_file() and sha(p)!=s):bad.append(p)
        for v in x.values():walk(v)
    elif isinstance(x,list):
        for v in x:walk(v)
walk(m)
V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v404');pe=m['published_evidence']
cof=[k for k,n in(('program','um.py'),('seal','um_absoluto_selo.json'),('result','um_absoluto.json'),('proof_manifest','tgl_kernel_proof_manifest.json')) if Path(pe[k]['path']).read_bytes()!=(V/n).read_bytes()]
kb=m['active_cluster'];extra=[kb['kernel_bundle'],kb['kernel_verification']]
chk('D_MANIFESTO','todos os caminhos que o manifesto ativo aponta (cluster, kernel, nucleo, Jev, mae, 8 fontes publicas, programa/selo/resultado/prova) existem DENTRO de canonical_releases\\v404_1d3c4cbe3f3c e os sha256 pinados no manifesto = bytes em disco; programa/selo/resultado/prova = os do cofre v404',
    not bad and not cof and all(Path(p).resolve().is_relative_to(can) for p in paths+extra) and all(Path(p).exists() for p in extra),{'caminhos':len(paths)+2,'sha_ruins':bad[:3],'diferem_do_cofre':cof})
# ---------------- D_LOADERS (fresh process output produced by d2_loaders.py)
L=rd(RV/'d2_out.json');iv=rd(W/'INSTALLED_VERIFICATION.json');bp=rd(W/'app/PREPARED_BINDING.json')
want_id=plan['deployment_identity']
okL=(L['identity']==want_id and L['kernel_sources']==1438 and L['kernel_source_sha']==rel['um_py_sha256']
     and L['packages']['haiku55']['prefix_sha256']==sha(pk/'haiku_expanded/prefix.md') and L['packages']['haiku']['prefix_sha256']==sha(pk/'shared/prefix.md')
     and L['packages']['haiku55']['permanent_tokens']==rd(pk/'haiku_expanded/native_count.json')['budget']['permanent_tokens'] and L['packages']['haiku']['permanent_tokens']==rd(pk/'shared/native_count.json')['budget']['permanent_tokens']
     and L['native']['bytes']==len((W/'app/native_prefix.md').read_bytes()) and L['native']['sha256']==sha(W/'app/native_prefix.md') and L['native']['identity_equals_release']
     and L['jev']['release']=='v404' and L['public_prompt']['sha256']==sha(pk/'sonnet_public/prefix.md') and L['public_prompt']['private_atlas_included'] is False and not L['public_prompt']['atlas_marker_in_text'])
chk('D_LOADERS','LOADERS DO RUNTIME, processo novo, escritos pelo revisor (audit hook: sem rede/subprocesso/escrita/segredos): load_release identidade = deployment_identity do plano; KernelCatalog 1438 fontes e source_sha = pino; load_package haiku55 e haiku (tokens permanentes e sha256 do prefixo = os contados e revisados); load_native_context (52.030 B = native_prefix.md, identidade = release); load_contract v404; prompt publico (851.087 B) = sonnet_public revisado, sem atlas privado',okL,
    {'tokens':{k:v['permanent_tokens'] for k,v in L['packages'].items()},'native':L['native']['bytes'],'public':L['public_prompt']['bytes'],'sources':L['kernel_sources']})
chk('D_LOADERS','INSTALLED_VERIFICATION.json da gerencia (nao confiado: comparado) = o que os loaders do revisor mediram: 1464 arquivos, identidade, commit, tokens/bytes dos 2 pacotes, native 52.030 B, prompt publico 851.087 B, Jev v404, 0 chamadas a provedor',
    iv['status']=='PASS' and iv['files_verified']==len(pd) and iv['identity']==L['identity'] and iv['public_commit']==rel['espelho_commit'] and iv['packages']['haiku55']=={'permanent_tokens':L['packages']['haiku55']['permanent_tokens'],'prefix_bytes':L['packages']['haiku55']['prefix_bytes']}
    and iv['packages']['haiku']=={'permanent_tokens':L['packages']['haiku']['permanent_tokens'],'prefix_bytes':L['packages']['haiku']['prefix_bytes']} and iv['native_bytes']==L['native']['bytes'] and iv['public_prompt_bytes']==L['public_prompt']['bytes'] and iv['JEV_release']=='v404' and iv['provider_calls']==0 and iv['science_executed'] is False,{'files_verified':iv['files_verified']})
# ---------------- E_ESCOPO (stat only)
cut=t_m-120;changed=[];n_seen=0;tmp=[]
def sweep(d):
    global n_seen
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):sweep(e.path)
                    else:
                        n_seen+=1;s=e.stat(follow_symlinks=False)
                        if '.tmp_v380_' in e.name:tmp.append(e.path)
                        if max(s.st_mtime,s.st_ctime)>=cut:changed.append(e.path)
                except OSError:pass
    except OSError:pass
sweep(str(R))
allowed=set(pd)|set(bk.values())
rest=sorted(p for p in changed if p not in allowed)
LOG=re.compile(r'^'+re.escape(str(R))+r'\\logs\\(?:web-server_[^\\]+\.log(?:\.err)?|web-supervisor\.log|gpu_[^\\]+\.csv|iald_heartbeat_telemetry\.jsonl)$')
chk('E_ESCOPO','NADA fora das arvores do plano mudou: varredura somente-stat de TODA a arvore de runtime (%d arquivos vistos, nenhum aberto; .env e .iald_secret_key inclusive): os arquivos com mtime/ctime desde a janela sao so os %d destinos do plano, os 7 backups e logs vivos do reinicio do web/telemetria; 0 temporarios .tmp_v380_ orfaos; nenhum .py de runtime, .env, banco sqlite, iald-app ou outra release (o unico .py que aparece e o um.py selado DENTRO de canonical_releases, dado do plano)'%(n_seen,len(pd)),
    allowed<=set(changed) and all(LOG.match(p) for p in rest) and not tmp and not [p for p in rest if p.endswith(('.py','.env','.sqlite3','.db'))],{'vistos':n_seen,'mudados':len(changed),'plano+backups_presentes':len(allowed&set(changed)),'logs_vivos':[p.replace(str(R)+'\\','') for p in rest],'tmp_orfaos':tmp})
v2bad=[d for d,h in v2.items() if d not in set(pd) and sha(d)!=h]
inter=sorted(Path(d).name for d in v2 if d in set(pd))
chk('E_ESCOPO','baseline v402: todos os %d arquivos que a v402 instalou e que o plano v404 NAO reescreve (release v402 inteira, pacote Jev da v402 etc.) continuam com o sha256 que a v402 registrou; a interseccao com o plano v404 sao exatamente os 7 destinos com backup'%len([d for d in v2 if d not in set(pd)]),not v2bad and set(inter)=={Path(r['destination']).name for r in pre},{'interseccao':inter,'divergentes':v2bad[:3]})
rels=sorted(p.name for p in (R/'canonical_releases').iterdir() if p.is_dir())
new_dirs=[x for x in rels if (R/'canonical_releases'/x).stat().st_ctime>=cut]
chk('E_ESCOPO','canonical_releases: surgiu UMA pasta nova (v404_1d3c4cbe3f3c) e nenhum arquivo das releases anteriores (v357..v402) foi tocado (stat + sha da v402)',new_dirs==[can.name] and len([p for p in changed if '\\canonical_releases\\' in p and not Path(p).is_relative_to(can)])==0,{'pastas':rels,'novas':new_dirs})
newb=sorted(p.name for p in W.rglob('*') if p.is_file() and 'review' not in p.parts and 'validation' not in p.parts and p.stat().st_mtime>=cut)
chk('E_ESCOPO','na pasta do build v404, desde a janela so surgiram maintenance.json, deployment.json, restart.json, INSTALLED_VERIFICATION.json, LOGIN_CHECK_v404.json (+ recibos da missao: claim/submit do deploy e os meus dois aceites r2, de 09:12); sem rollback_new_files/mobile_backups',
    set(newb)<={'maintenance.json','deployment.json','restart.json','INSTALLED_VERIFICATION.json','LOGIN_CHECK_v404.json','v404-deploy-claim.json','v404-deploy-submit.json','v404-app-accept-r2.json','v404-sources-accept-r2.json'} and not (W/'rollback_new_files').exists() and not (W/'mobile_backups').exists(),{'novos':newb})
print(json.dumps({'n':len(checks),'ok':sum(c['ok'] for c in checks),'checks':checks,'web_pid':w2[0].pid,'web_created':w2[0].create_time(),'supervisor_pid':sup.pid,'supervisor_created':sup.create_time(),'login':status},ensure_ascii=False,indent=1,default=str))
