"""Reviewer (sonnet-app-v405-revisor-d): independent, READ-ONLY review of the v405 DEPLOY (task `deploy`, unit F9.APP_V405_20261102).
Adapted from the v404 reviewer's d1_deploy_review.py (same method), extended for the v405 questions D1..D5.
psutil is used only for queries (no process touched); the runtime tree is swept with os.scandir/os.stat only (no file opened by the sweep;
.env, .iald_secret_key and iald_psion_state_32B.json included in the stat sweep, never opened); plan destinations are hashed; two server logs are
read on purpose (tail of web-supervisor.log and the first lines of the r3 web log, outside the sweep); the only network access is one
GET http://127.0.0.1:8082/login. The runtime loaders run in a separate fresh process (d2_loaders.py, audit hook). Output: JSON on stdout."""
import os,sys,json,hashlib,re,time,datetime,subprocess,http.client
from pathlib import Path
import psutil
PY=r'C:\Python314\python.exe'
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');V4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027');R=Path(r'C:\IALD\projetos_pyhton\IALD')
RV=W/'review/revisor_sonnet-app-v405-revisor-d';ME='sonnet-app-v405-revisor-d';SUBMITTER='claude-gerencia-a7';PKG_REVIEWER='sonnet-app-v405-revisor';BUILDER='opus-app-v405-construtor'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
fmt=lambda t:datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S.%f')[:12]
checks=[]
def chk(D,group,desc,ok,achado=None):
    checks.append({'n':len(checks)+1,'D':D,'grupo':group,'descricao':desc,'ok':bool(ok),'achado':achado})
plan_path=W/'install_plan.json';plan=rd(plan_path);dep=rd(W/'deployment.json');mt=rd(W/'maintenance.json');rs=rd(W/'restart.json')
rel=rd(W/'app/RELEASE.json');rf=rd(W/'validation/review_final.json');fc=rd(W/'validation/final_checks.json')
installed_at=datetime.datetime.fromisoformat(dep['installed_at']).timestamp()
t_m=(W/'maintenance.json').stat().st_mtime;t_r=(W/'restart.json').stat().st_mtime
pd=[r['destination'] for r in plan['files']];pdset=set(pd)
# =============== A_RECIBO (mission / receipts)  -> D1
sub=rd(W/'receipts/v405-deploy-submit.json')['task']
bad=[Path(e['path']).name for e in sub['evidence'] if sha(e['path'])!=e['sha256']]
chk('D1','A_RECIBO','recibo v405-deploy-submit: deploy review_pending, submetido por claude-gerencia-a7 (distinto de mim); as 4 evidencias (deployment, maintenance, restart, install_plan) tem sha256 = bytes ATUAIS',
    sub['status']=='review_pending' and sub['submitted_by']==SUBMITTER and sub['submitted_by']!=ME and len(sub['evidence'])==4 and not bad,{'status':sub['status'],'by':sub['submitted_by'],'stale':bad,'evidence':[Path(e['path']).name for e in sub['evidence']]})
pj=json.loads(subprocess.check_output([PY,'-B','-X','utf8',str(W/'mission_step.py'),'project'],cwd=str(W)))
act={t['id']:t['status'] for t in pj['active']}
acc={n:rd(W/f'receipts/v405-{n}-accept-r3.json')['task'] for n in('app','sources')}
accbad=[Path(e['path']).name for n in acc for e in acc[n]['evidence']+acc[n]['review_evidence'] if sha(e['path'])!=e['sha256']]
chk('D1','A_RECIBO','missao (project, somente leitura): deploy review_pending; app e sources SATISFEITOS pela revisao independente r3 (reviewed_by=sonnet-app-v405-revisor, submitted_by=opus-app-v405-construtor; nenhum dos dois sou eu nem a gerencia que implantou) com todas as evidencias pinadas = bytes atuais',
    act.get('deploy')=='review_pending' and 'app' not in act and 'sources' not in act and all(acc[n]['status']=='satisfied' and acc[n]['reviewed_by']==PKG_REVIEWER and acc[n]['submitted_by']==BUILDER and PKG_REVIEWER not in(ME,SUBMITTER) for n in acc) and not accbad,
    {'active':act,'revision':pj['revision'],'accept_evidence_stale':accbad,'reviewed_by':{n:acc[n]['reviewed_by'] for n in acc}})
mt_=lambda p:(W/p).stat().st_mtime
order=[('accept app r3',mt_('receipts/v405-app-accept-r3.json')),('claim deploy',mt_('receipts/v405-deploy-claim.json')),('maintenance.json',t_m),('installed_at',installed_at),('restart.json',t_r),('submit deploy',mt_('receipts/v405-deploy-submit.json')),('INSTALLED_VERIFICATION',mt_('INSTALLED_VERIFICATION.json'))]
chk('D1','A_RECIBO','ordem temporal: aceite da revisao do pacote (r3) < claim do deploy < janela de manutencao < instalacao < restart.json < submit < INSTALLED_VERIFICATION (o deploy veio DEPOIS da revisao; evidencias nao regravadas)',
    all(order[i][1]<order[i+1][1] for i in range(len(order)-1)),[(n,fmt(t)) for n,t in order])
baks=[p.name for n in('deployment','maintenance','restart') for p in W.glob(n+'.json.bak_*')]
chk('D1','A_RECIBO','deployment.json, maintenance.json e restart.json existem em UMA versao cada (sem .bak_ ao lado: nao foram regravados)',not baks,baks)
# =============== B_PLANO -> D1
plan_sha=sha(plan_path)
pins={'recomputado':plan_sha,'deployment.plan_sha256':dep['plan_sha256'],'final_checks':fc['plan_sha256'],'review_final':rf['plan_sha256']}
for tag,rc in(('pino_submit_r3_do_pacote','v405-app-submit-r3.json'),('pino_accept_r3_do_pacote','v405-app-accept-r3.json'),('pino_submit_do_deploy','v405-deploy-submit.json')):
    t=rd(W/'receipts'/rc)['task'];pins[tag]=next(e['sha256'] for e in t['evidence'] if e['path'].endswith('install_plan.json'))
chk('D1','B_PLANO','plano: sha256 recomputado de install_plan.json = deployment.plan_sha256 = final_checks.plan_sha256 = review_final.plan_sha256 = pinos dos recibos (submit r3 e accept r3 do pacote, submit do deploy)',len(set(pins.values()))==1,{k:v[:16] for k,v in pins.items()})
chk('D1','B_PLANO','deployment.json: status INSTALLED_RESTART_REQUIRED; accounts_modified=false, bench_restarted=false, client_files_changed=false (CONSTANTES literais em transaction.apply_plan, nao medidas: corroboradas nos grupos C/E); runtime_python_changes=0 no plano; plano staging_only',
    dep['status']=='INSTALLED_RESTART_REQUIRED' and dep['accounts_modified'] is False and dep['bench_restarted'] is False and dep['client_files_changed'] is False and plan['runtime_python_changes']==0 and plan['staging_only'] is True,{'installed_at':dep['installed_at']})
chk('D1','B_PLANO','deployment.files tem EXATAMENTE os %d destinos do plano, na mesma ordem, sem duplicata (nada a mais, nada a menos)'%len(pd),list(dep['files'])==pd and len(set(pd))==len(pd),{'n_plan':len(pd),'n_dep':len(dep['files'])})
t0=time.time();bh=[d for d,r in zip(pd,plan['files']) if not(dep['files'].get(d)==r['sha256']==sha(d))]
chk('D1','B_PLANO','para cada um dos %d destinos: sha256 em deployment.files = sha256 do plano = sha256 dos BYTES hoje em disco (recomputado agora, arquivo a arquivo)'%len(pd),not bh and len(pd)==1472,{'divergentes':bh[:3],'n':len(pd),'segundos':round(time.time()-t0,1)})
pre=[r for r in plan['files'] if r['baseline'] is not None];new=[r for r in plan['files'] if r['baseline'] is None];unch=[r for r in pre if r['baseline']==r['sha256']]
chk('D1','B_PLANO','classificacao do plano: %d destinos pre-existentes que mudam (6 de .iald_runtime + manifesto ativo), %d criados (baseline nulo, inclui core_packet_v405_bound.txt na raiz), %d inalterados'%(len(pre),len(new),len(unch)),len(pre)==7 and len(new)==len(pd)-7 and not unch,{'pre':[str(Path(r['destination']).relative_to(R)) for r in pre],'novos':len(new)})
nuc=R/'iald_nucleo_fixo.json'
chk('D1','B_PLANO','ordem de escrita: o manifesto ativo iald_nucleo_fixo.json e o ULTIMO destino do plano (pacotes e release antes; a troca do manifesto fecha a transacao)',pd[-1]==str(nuc) and pd.index(str(nuc))==len(pd)-1,{'ultimo':Path(pd[-1]).name,'indice_manifesto':pd.index(str(nuc))})
bk=dep['backups'];bkbad=[];stamps=set();bkinfo={}
for d,r in ((r['destination'],r) for r in pre):
    b=bk.get(d)
    if not b or not Path(b).is_file() or Path(b).parent!=Path(d).parent or sha(b)!=r['baseline'] or sha(b)==r['sha256']:bkbad.append(d);continue
    stamps.add(b.rsplit('.bak_',1)[1]);bkinfo[str(Path(d).relative_to(R))]={'backup':Path(b).name,'bytes':Path(b).stat().st_size,'sha256_backup':sha(b)[:16],'baseline_do_plano':r['baseline'][:16],'sha256_novo':r['sha256'][:16]}
orph=[]
for d in {Path(r['destination']).parent for r in pre}:
    for p in d.glob('*.bak_*'):
        if p.name.endswith(next(iter(stamps),'~')) and str(p) not in bk.values():orph.append(str(p))
chk('D1','B_PLANO','backups (TODOS os 7, nao amostra; inclui .iald_runtime\\haiku55\\prefix.md e iald_nucleo_fixo.json): deployment.backups = exatamente os 7 destinos que mudam; cada .bak_ existe na pasta do destino, tem os BYTES do estado anterior (sha256 = baseline do plano), difere do novo; um unico carimbo; nenhum .bak_ orfao do mesmo carimbo',
    set(bk)=={r['destination'] for r in pre} and not bkbad and len(stamps)==1 and not orph,{'stamps':list(stamps),'bad':bkbad,'orphans':orph,'backups':bkinfo})
v4=rd(V4/'deployment.json')['files'];chain=[d for d in bk if sha(bk[d])!=v4.get(d)]
chk('D1','B_PLANO','cadeia com a v404: o conteudo de cada um dos 7 backups = o sha256 que a v404 registrou como instalado em deployment.json (o backup guardou exatamente a v404 aceita, nao um estado intermediario)',not chain and len(bk)==7,{'divergentes':chain})
can=R/'canonical_releases'/('v405_'+rel['espelho_commit'][:12]);ondisk={str(p) for p in can.rglob('*') if p.is_file()};inplan={d for d in pd if Path(d).is_relative_to(can)}
chk('D1','B_PLANO','canonical_releases\\v405_6a2138d73c1a: o conjunto de arquivos em disco = exatamente os destinos do plano sob essa pasta (nenhum arquivo instalado a mais, nenhum a menos)',ondisk==inplan and len(inplan)==1464,{'disk':len(ondisk),'plan':len(inplan),'extra':sorted(ondisk-inplan)[:3],'missing':sorted(inplan-ondisk)[:3]})
base=rd(W/'app/RUNTIME_BASELINE.json')['files'];bchg=[b['path'] for b in base if not Path(b['path']).is_file() or sha(b['path'])!=b['sha256']]
rootpy_now={str(p) for p in R.glob('*.py')};rootpy_base={b['path'] for b in base if Path(b['path']).parent==R and b['path'].endswith('.py')}
nuc_plan=next(r for r in plan['files'] if r['destination']==str(nuc))
chk('D1','B_PLANO','codigo de runtime preservado: todos os %d arquivos de RUNTIME_BASELINE.json (tirado ANTES do deploy) tem o sha256 de antes; o conjunto de .py da raiz nao mudou (so o confidencial iald_stack_v7.py fica fora do baseline por desenho, nunca aberto); o unico arquivo do baseline que muda e o manifesto ativo; o plano nao escreve .py de runtime; o manifesto ativo mudou do baseline para o do plano'%len(base),
    set(bchg)=={str(nuc)} and rootpy_base<=rootpy_now and (rootpy_now-rootpy_base)=={str(R/'iald_stack_v7.py')} and max((R/'iald_stack_v7.py').stat().st_mtime,(R/'iald_stack_v7.py').stat().st_ctime)<t_m and not [d for d in pd if Path(d).parent==R and d.endswith('.py')] and sha(nuc)==nuc_plan['sha256'] and sha(bk[str(nuc)])==nuc_plan['baseline'],
    {'baseline_files':len(base),'unico_arquivo_do_baseline_que_mudou':[Path(x).name for x in bchg],'root_py_now':len(rootpy_now),'root_py_baseline':len(rootpy_base),'extra_fora_do_baseline':sorted(Path(x).name for x in rootpy_now-rootpy_base),'nota':'iald_stack_v7.py e confidencial: so stat (mtime/ctime anteriores a janela), nunca aberto'})
st=W/'app/science/memory_stage';pk=W/'app/packages'
pairs=[(R/'.iald_runtime/haiku55/prefix.md',pk/'haiku_expanded/prefix.md'),(R/'.iald_runtime/haiku55/manifest.json',pk/'haiku_expanded/manifest_install.json'),(R/'.iald_runtime/haiku55/native_count.json',pk/'haiku_expanded/native_count.json'),
       (R/'.iald_runtime/haiku/prefix.md',pk/'shared/prefix.md'),(R/'.iald_runtime/haiku/manifest.json',pk/'shared/manifest_install.json'),(R/'.iald_runtime/haiku/native_count.json',pk/'shared/native_count.json'),
       (nuc,st/'manifest_install.json'),(R/'core_packet_v405_bound.txt',st/'core_packet_v405_bound.txt')]
pb=[a.name for a,b in pairs if a.read_bytes()!=b.read_bytes()]
chk('D1','B_PLANO','pacotes instalados = pacotes REVISADOS byte a byte (r3): haiku55/{prefix,manifest,native_count} = haiku_expanded; haiku/{...} = shared; manifesto ativo = manifest_install do estagio; pacote do Jev da raiz = o do estagio',not pb,{'pairs':len(pairs),'diff':pb})
code=['transaction.py','maintenance.py','deploy_controlled.py','verify_installed.py'];rec={'transaction.py':rf['transaction_sha256'],'maintenance.py':rf['maintenance_sha256'],'deploy_controlled.py':rf['deploy_controlled_sha256'],'verify_installed.py':rf['verify_installed_sha256']}
cb=[c for c in code if sha(W/c)!=rec[c] or sha(W/c)!=sha(V4/c)]
chk('D1','B_PLANO','o deploy usou o codigo REVISADO: transaction/maintenance/deploy_controlled/verify_installed = bytes que review_final.json registrou = bytes da v404 aceita',not cb,{'divergentes':cb,'sha16':{c:sha(W/c)[:16] for c in code}})
sb=[d for d,r in zip(pd,plan['files']) if not(Path(r['source']).is_file() and sha(r['source'])==r['sha256'])]
chk('D1','B_PLANO','estagio intacto: para cada um dos %d destinos, o arquivo `source` do plano ainda existe e tem o sha256 do plano (o que foi instalado e exatamente o que foi revisado)'%len(pd),not sb,{'divergentes':sb[:3]})
stamp=next(iter(stamps));stamp_ts=datetime.datetime.strptime(stamp,'%Y%m%d_%H%M%S_%f').timestamp()
mts=[Path(d).stat().st_mtime for d in pd]
chk('D1','B_PLANO','todos os %d destinos foram escritos DENTRO da janela exclusiva: mtime de cada um entre o carimbo dos backups (%s) e installed_at (nenhum escrito antes ou depois)'%(len(pd),stamp),min(mts)>=stamp_ts-0.5 and max(mts)<=installed_at+0.5,{'min_mtime':fmt(min(mts)),'max_mtime':fmt(max(mts)),'stamp':fmt(stamp_ts),'installed_at':fmt(installed_at)})
# =============== D_MANIFESTO -> D1 (+D4)
m=rd(nuc);old=rd(bk[str(nuc)])
f3=lambda x:(x['active_cluster']['release'],x['operational_core']['current_release'],x['jev_control']['release'])
src=lambda x:(x['active_cluster']['release_source_sha256'],x['operational_core']['release_source_sha256'],x['jev_control']['source_sha256'])
chk('D1','D_MANIFESTO','iald_nucleo_fixo.json de producao AGORA: active_cluster.release, operational_core.current_release e jev_control.release = v405 (backup: v404 nos tres); commit = RELEASE.espelho_commit; release_source_sha256/source_sha256 = RELEASE.um_py_sha256; publication_pending=false',
    f3(m)==('v405',)*3 and f3(old)==('v404',)*3 and m['active_cluster']['commit']==rel['espelho_commit'] and set(src(m))=={rel['um_py_sha256']} and m['active_cluster'].get('publication_pending') is False,{'agora':f3(m),'backup':f3(old),'commit':m['active_cluster']['commit'],'source_sha':rel['um_py_sha256']})
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
V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405');pe=m['published_evidence']
cof=[k for k,n in(('program','um.py'),('seal','um_absoluto_selo.json'),('result','um_absoluto.json'),('proof_manifest','tgl_kernel_proof_manifest.json')) if Path(pe[k]['path']).read_bytes()!=(V/n).read_bytes()]
kb=m['active_cluster'];extra=[kb['kernel_bundle'],kb['kernel_verification']]
chk('D1','D_MANIFESTO','todos os caminhos que o manifesto ativo aponta (cluster, kernel, nucleo, Jev, mae, fontes publicas, programa/selo/resultado/prova) existem DENTRO de canonical_releases\\v405_6a2138d73c1a e os sha256 pinados no manifesto = bytes em disco; programa/selo/resultado/prova = os do cofre v405',
    not bad and not cof and all(Path(p).resolve().is_relative_to(can) for p in paths+extra) and all(Path(p).exists() for p in extra),{'caminhos':len(paths)+2,'sha_ruins':bad[:3],'diferem_do_cofre':cof})
um_installed=sha(pe['program']['path']);seal=rd(pe['seal']['path'])
chk('D4','D_MANIFESTO','programa: o um.py INSTALADO (canonical_releases\\v405...\\release\\Um (absoluto) — Grande Atrator\\um.py) tem sha256 recomputado = 0030242565cc13f6... = RELEASE.um_py_sha256 = sha256.um.py do selo instalado; um_version do selo = v405; commit do manifesto = RELEASE.espelho_commit = commit do PUBLIC_GIT_BINDING',
    um_installed==rel['um_py_sha256']==seal['sha256']['um.py'] and seal['um_version']=='v405' and m['active_cluster']['commit']==rel['espelho_commit']==rd(W/'app/PUBLIC_GIT_BINDING.json')['commit'] ,{'um_py_sha256':um_installed,'seal_um_version':seal['um_version'],'commit':m['active_cluster']['commit'],'public_git_binding.commit':rd(W/'app/PUBLIC_GIT_BINDING.json')['commit'],'public_git_binding.remote_http_checked':rd(W/'app/PUBLIC_GIT_BINDING.json')['remote_http_checked']})
# =============== C_REINICIO -> D2
def web():
    out=[]
    for p in psutil.process_iter(['name']):
        try:
            if (p.info['name'] or '').lower()=='python.exe' and any(a and str(Path(a)).lower()==str(R/'iald_web_server.py').lower() for a in p.cmdline()[1:] if not a.startswith('-')):out.append(p)
        except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
    return out
def listeners(port):return [c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==port]
v4rs=rd(V4/'restart.json')
chk('D2','C_REINICIO','maintenance.json: ADMISSIONS_STOPPED, filho antigo %d, supervisor %d; restart.json: PASS, HTTP 200, filho novo %d != %d, MESMA identidade do supervisor (pid e create_time) que maintenance.json; continuidade: o filho antigo da v405 e o filho novo da v404 (%d) e o supervisor e o mesmo da v404'%(mt['old_web_pid'],mt['supervisor_pid'],rs['new_web_pid'],rs['old_web_pid'],v4rs['new_web_pid']),
    mt['status']=='ADMISSIONS_STOPPED' and rs['status']=='PASS' and rs['http_status']==200 and rs['new_web_pid']!=rs['old_web_pid'] and rs['old_web_pid']==mt['old_web_pid']==v4rs['new_web_pid'] and (rs['supervisor_pid'],rs['supervisor_created'])==(mt['supervisor_pid'],mt['supervisor_created'])==(v4rs['supervisor_pid'],v4rs['supervisor_created']),
    {'restart_scope(declarado)':rs['restart_scope'],'old':mt['old_web_pid'],'new':rs['new_web_pid'],'supervisor':mt['supervisor_pid'],'supervisor_created':datetime.datetime.fromtimestamp(mt['supervisor_created']).isoformat()})
w1=web();l1=listeners(8082)
chk('D2','C_REINICIO','AGORA: exatamente UM processo python.exe rodando iald_web_server.py, exatamente UM ouvinte na 8082, e ambos sao o PID new_web_pid do restart.json (%d)'%rs['new_web_pid'],len(w1)==1 and len(l1)==1 and w1[0].pid==l1[0].pid==rs['new_web_pid'],{'web':[p.pid for p in w1],'listeners':[c.pid for c in l1]})
child=w1[0];sup=child.parent()
chk('D2','C_REINICIO','o filho %d esta sob o MESMO supervisor: ppid = %d, create_time do supervisor IDENTICO ao de restart.json/maintenance.json (mesma instancia, nao um supervisor novo), roda start_iald_web.ps1 sem -NoSupervise, e nem ele nem o filho estao suspensos'%(child.pid,rs['supervisor_pid']),
    child.ppid()==rs['supervisor_pid'] and sup.create_time()==rs['supervisor_created'] and any(str(Path(a)).lower()==str(R/'start_iald_web.ps1').lower() for a in sup.cmdline()[1:] if a and not a.startswith('-')) and not any(a.lower()=='-nosupervise' for a in sup.cmdline()) and sup.status()!=psutil.STATUS_STOPPED and child.status()!=psutil.STATUS_STOPPED,
    {'ppid':child.ppid(),'sup_pid':sup.pid,'sup_created':datetime.datetime.fromtimestamp(sup.create_time()).isoformat(),'sup_created_igual_ao_restart_json':sup.create_time()==rs['supervisor_created'],'sup_status':sup.status(),'child_status':child.status(),'child_created':datetime.datetime.fromtimestamp(child.create_time()).isoformat()})
chk('D2','C_REINICIO','o filho novo nasceu DEPOIS da instalacao (create_time > installed_at: pode ter carregado os arquivos novos) e o PID antigo %d nao existe mais'%mt['old_web_pid'],child.create_time()>installed_at and not psutil.pid_exists(mt['old_web_pid']),{'child_minus_installed_s':round(child.create_time()-installed_at,1),'old_pid_exists':psutil.pid_exists(mt['old_web_pid'])})
def tail(path,n=40000):
    b=Path(path).read_bytes();return b[-n:].decode('utf-8','replace')
sl=(R/'logs/web-supervisor.log').read_bytes().decode('utf-8','replace').splitlines()
ev=[l.strip() for l in sl if re.match(r'2026-11-02 08:1[56]:',l)]
bann=[l for l in sl if 'launcher supervisionado' in l]
sup_banner_ok=bann[-1].startswith('2026-10-28 13:38:56') and datetime.datetime.strptime(bann[-1][:19],'%Y-%m-%d %H:%M:%S').timestamp()-rs['supervisor_created']<2
chk('D2','C_REINICIO','log do supervisor (web-supervisor.log, lido; DECLARADO pelo proprio supervisor): 08:15:59 filho morreu (terminado pela janela) e "reiniciando em 5 s"; 08:16:04 "iniciando (tentativa 3)" e "PID %d iniciado"; o ultimo banner "launcher supervisionado" e de 2026-10-28 13:38:56 (= create_time do supervisor): nenhum supervisor novo nasceu'%rs['new_web_pid'],
    any('WEB SERVER MORREU' in l and l.startswith('2026-11-02 08:15:59') for l in ev) and any('iniciando (tentativa 3)' in l and l.startswith('2026-11-02 08:16:04') for l in ev) and any(('PID %d iniciado'%rs['new_web_pid']) in l and l.startswith('2026-11-02 08:16:04') for l in ev) and sup_banner_ok,{'linhas':ev[:8],'ultimo_banner':bann[-1][:60]})
r3=(R/'logs/web-server_20261028_133856_r3.log').read_bytes().decode('utf-8','replace').splitlines()
cat_line=next((l for l in r3 if 'IALD-CANONICAL-CATALOG' in l),'')
chk('D2','C_REINICIO','log do filho novo (web-server_..._r3.log, primeiras linhas; DECLARADO pelo proprio processo, nao autenticado): "[IALD-CANONICAL-CATALOG] release=v405 source_sha256=0030242565cc13f6" — o processo vivo carregou o catalogo v405 ao nascer (o r2 dizia release=v404); GET /login sozinho nao mostra a release',
    'release=v405' in cat_line and ('source_sha256='+rel['um_py_sha256'][:16]) in cat_line,{'linha':cat_line,'lean_files_v402_v404_v405':[next((l.split('lean_files=')[1] for l in (R/('logs/web-server_20261028_133856_r%d.log'%i)).read_bytes().decode('utf-8','replace').splitlines() if 'IALD-CANONICAL-CATALOG' in l),None) for i in(1,2,3)]})
since=[];bench={};me=psutil.Process();ancestry={me.pid}|{p.pid for p in me.parents()}
for p in psutil.process_iter(['pid','name','create_time','status']):
    try:
        nm=(p.info['name'] or '').lower()
        if nm in('python.exe','pythonw.exe','llama-server.exe','powershell.exe','pwsh.exe') and p.info['create_time']>=t_m-1 and p.pid not in ancestry:
            cl=' '.join(p.cmdline())
            if any(k in cl.lower() for k in('iald','llama','bancada')) and 'revisor_sonnet' not in cl:since.append((p.pid,p.info['name'],fmt(p.info['create_time']),cl[:110]))
    except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
for port,label in((8081,'llama (nativa)'),(18777,'Bancada Um'),(18765,'gw'),(18766,'cosmologia')):
    for c in listeners(port):
        p=psutil.Process(c.pid);bench[label]={'port':port,'pid':c.pid,'cmd':' '.join(p.cmdline())[:100],'created_before_window':p.create_time()<t_m,'minutes_before_window':round((t_m-p.create_time())/60,1),'suspended':p.status()==psutil.STATUS_STOPPED,'created':datetime.datetime.fromtimestamp(p.create_time()).strftime('%m-%d %H:%M:%S')}
chk('D2','C_REINICIO','nativa e Bancada: os servicos que ESCUTAM agora (llama 8081, Bancada Um 18777, e 18765/18766 se existirem) foram criados ANTES da janela do deploy (create_time < maintenance.json) e nao estao suspensos (nao foram reiniciados pela implantacao); processos IALD (python/llama/powershell) criados desde a janela listados',
    'llama (nativa)' in bench and 'Bancada Um' in bench and all(v['created_before_window'] and not v['suspended'] for v in bench.values()) and rs['new_web_pid'] in [s[0] for s in since] and not [s for s in since if s[0]!=rs['new_web_pid'] and any(k in s[3].lower() for k in('llama-server','um_bancada','start_iald_llama','start_iald_web','iald_web_server'))],{'bench':bench,'criados_desde_a_janela':since,'18765_18766_escutam_agora':[k for k in('gw','cosmologia') if k in bench]})
conn=http.client.HTTPConnection('127.0.0.1',8082,timeout=20);conn.request('GET','/login');resp=conn.getresponse();status=resp.status;resp.read(1<<20);conn.close()
chk('D2','C_REINICIO','GET local http://127.0.0.1:8082/login = 200 (unico acesso de rede deste revisor; corpo descartado)',status==200,{'http':status})
w2=web();l2=listeners(8082)
chk('D2','C_REINICIO','depois do GET: ainda um unico processo web, mesmo PID, mesmo create_time, mesmo supervisor e o mesmo ouvinte (o servidor nao reiniciou durante a revisao)',
    [(p.pid,p.ppid(),p.create_time()) for p in w2]==[(p.pid,p.ppid(),p.create_time()) for p in w1] and [c.pid for c in l2]==[c.pid for c in l1],{'pid':w2[0].pid})
# =============== D_LOADERS -> D4 / D5 (fresh-process output produced by d2_loaders.py)
p2=subprocess.run([PY,'-B','-X','utf8',str(RV/'d2_loaders.py')],capture_output=True,cwd=str(RV));assert p2.returncode==0,p2.stderr.decode('utf-8','replace')[-2000:]
(RV/'d2_out.json').write_bytes(p2.stdout)
L=json.loads(p2.stdout.decode('utf-8'));iv=rd(W/'INSTALLED_VERIFICATION.json');bp=rd(W/'app/PREPARED_BINDING.json')
want_id=plan['deployment_identity']
okL=(L['identity']==want_id and L['kernel_sources']==bp['formal_sources']==1446 and L['kernel_source_sha']==rel['um_py_sha256']
     and L['packages']['haiku55']['prefix_sha256']==sha(pk/'haiku_expanded/prefix.md') and L['packages']['haiku']['prefix_sha256']==sha(pk/'shared/prefix.md')
     and L['packages']['haiku55']['permanent_tokens']==rd(pk/'haiku_expanded/native_count.json')['budget']['permanent_tokens'] and L['packages']['haiku']['permanent_tokens']==rd(pk/'shared/native_count.json')['budget']['permanent_tokens']
     and L['native']['bytes']==len((W/'app/native_prefix.md').read_bytes()) and L['native']['sha256']==sha(W/'app/native_prefix.md') and L['native']['identity_equals_release']
     and L['jev']['release']=='v405' and L['public_prompt']['sha256']==sha(pk/'sonnet_public/prefix.md') and L['public_prompt']['bytes']==bp['actual_prompts']['public']['bytes'] and L['public_prompt']['private_atlas_included'] is False and not L['public_prompt']['atlas_marker_in_text']
     and not L['audit']['blocked_events_attempted'])
chk('D4','D_LOADERS','LOADERS DO RUNTIME, processo novo, escritos pelo revisor (audit hook: sem rede/subprocesso/escrita/segredos; 0 eventos bloqueados): load_release identidade = deployment_identity do plano (v405); KernelCatalog 1446 fontes e source_sha = pino; load_package haiku55 e haiku (tokens permanentes e sha256 do prefixo = os contados e revisados); load_native_context (52.409 B = native_prefix.md, identidade = release); load_contract v405; prompt publico (858.881 B) = sonnet_public revisado, sem atlas privado',okL,
    {'tokens':{k:v['permanent_tokens'] for k,v in L['packages'].items()},'native':L['native']['bytes'],'public':L['public_prompt']['bytes'],'sources':L['kernel_sources'],'audit':L['audit']})
jv=L['jev'];cjf=Path(jv['contract_file'])
chk('D4','D_LOADERS','contrato JEV: load_contract(R) aceita (valida contrato, pino do manifesto, nucleo, cluster, artefatos cientificos e o pacote de roteamento da raiz); release v405 (schema iald.jev-control.v2), source_sha256 = pino do programa; jev_control_v405.json PRESENTE em canonical_releases\\v405_6a2138d73c1a com sha = pino do manifesto; core_packet_v405_bound.txt da raiz = pino do contrato',
    jv['release']=='v405' and jv['schema']=='iald.jev-control.v2' and jv['source_sha256']==rel['um_py_sha256'] and jv['contract_file_exists'] and cjf.is_file() and cjf.parent==can and cjf.name=='jev_control_v405.json' and jv['contract_file_sha256']==jv['manifest_pin']==next(r['sha256'] for r in plan['files'] if r['destination']==str(cjf)) and jv['core_packet_um_version']=='v405' and jv['core_packet_root_sha256']==jv['core_packet_sha256'],jv)
chk('D4','D_LOADERS','INSTALLED_VERIFICATION.json da gerencia (feito antes do claim de verify, fora de ordem; NAO confiado: comparado) = o que os loaders do revisor mediram AGORA: 1472 arquivos, identidade, commit, tokens/bytes dos 2 pacotes, native 52.409 B, prompt publico 858.881 B, Jev v405, 0 chamadas a provedor, science_executed=false',
    iv['status']=='PASS' and iv['files_verified']==len(pd)==1472 and iv['identity']==L['identity'] and iv['public_commit']==rel['espelho_commit'] and iv['packages']['haiku55']=={'permanent_tokens':L['packages']['haiku55']['permanent_tokens'],'prefix_bytes':L['packages']['haiku55']['prefix_bytes']}
    and iv['packages']['haiku']=={'permanent_tokens':L['packages']['haiku']['permanent_tokens'],'prefix_bytes':L['packages']['haiku']['prefix_bytes']} and iv['native_bytes']==L['native']['bytes'] and iv['public_prompt_bytes']==L['public_prompt']['bytes'] and iv['JEV_release']==L['jev']['release']=='v405' and iv['provider_calls']==0 and iv['science_executed'] is False,
    {'iv':{k:iv[k] for k in('files_verified','public_commit','native_bytes','public_prompt_bytes','JEV_release','provider_calls','science_executed')},'iv_packages':iv['packages'],'medido_agora':{'haiku55':[L['packages']['haiku55']['permanent_tokens'],L['packages']['haiku55']['prefix_bytes']],'haiku':[L['packages']['haiku']['permanent_tokens'],L['packages']['haiku']['prefix_bytes']]}})
# ---------------- D5: native_count / snapshot / profile
h55=L['snapshots']['haiku55'];h=L['snapshots']['haiku']
nc_r=R/'.iald_runtime/haiku55/native_count.json';nc_w=pk/'haiku_expanded/native_count.json';ncd=rd(nc_r);bud=ncd['budget']
mf55=rd(R/'.iald_runtime/haiku55/manifest.json')
chk('D5','D5_NATIVE','native_count.json de R\\.iald_runtime\\haiku55 = W\\app\\packages\\haiku_expanded\\native_count.json BYTE a BYTE (e o de haiku = shared); folga (remaining_tokens) %d = 1.000.000 - %d (entrada de referencia) - %d (saida reservada) - %d (margem), recomputada aqui; piso do carregador remaining >= 10.000; memory_target 180.000 <= permanent_tokens %d'%(bud['remaining_tokens'],bud['request_input_tokens'],bud['reserved_output_tokens'],bud['margin_tokens'],bud['permanent_tokens']),
    nc_r.read_bytes()==nc_w.read_bytes() and (R/'.iald_runtime/haiku/native_count.json').read_bytes()==(pk/'shared/native_count.json').read_bytes() and bud['remaining_tokens']==1000000-bud['request_input_tokens']-bud['reserved_output_tokens']-bud['margin_tokens']==172998 and bud['remaining_tokens']>=10000 and bud['permanent_tokens']>=bud['memory_target'],
    {'sha256_R':sha(nc_r),'sha256_W':sha(nc_w),'folga_tokens':bud['remaining_tokens'],'permanent_tokens':bud['permanent_tokens'],'request_input_tokens':bud['request_input_tokens'],'folga_conta':1000000-bud['request_input_tokens']-bud['reserved_output_tokens']-bud['margin_tokens'],'v404_folga_registrada_pelo_construtor':rd(W/'BUILDER_MEASUREMENTS.json')['installed_haiku55_v404']['remaining_tokens']})
chk('D5','D5_NATIVE','pino: prefix_sha256 do native_count = sha256 do prefix.md INSTALADO (recomputado) = prefix_sha256 do manifest.json instalado = prefix do pacote revisado; deployment do recibo = identidade da release; public_commit = commit; native_tools_sha256 do recibo = counted_scoped_tools_sha256 do manifest; 0 requisicoes de geracao; sem atlas privado nem contexto do operador no recibo',
    ncd['prefix_sha256']==sha(R/'.iald_runtime/haiku55/prefix.md')==mf55['prefix_sha256']==sha(pk/'haiku_expanded/prefix.md') and ncd['deployment']==L['identity'] and ncd['public_commit']==rel['espelho_commit'] and ncd['native_tools_sha256']==mf55['counted_scoped_tools_sha256'] and ncd['generation_requests']==0 and ncd['private_atlas_included'] is False and ncd['operator_context_sent'] is False,
    {'prefix_sha256':ncd['prefix_sha256'],'native_tools_sha256':ncd['native_tools_sha256'],'tools_sha256_manifest':mf55['tools_sha256'],'status':ncd['status'],'utc':ncd['utc'],'count_requests':ncd['count_requests']})
old55=rd(bk[str(R/'.iald_runtime/haiku55/manifest.json')])
chk('D5','D5_NATIVE','o pacote CARREGA sem recusa em claude_context_snapshot.load_snapshot + claude_profiles.context_budget (processo novo, loader real do servidor): HaikuUnavailable nao levantada; snapshot.reference_remaining = folga do recibo; context_metadata.reserva_dinamica_medida = folga; budget do native_count == context_budget recomputado == budget do manifest; mesmo para o pacote haiku (shared); tools_sha256 igual ao da v404 (backup do manifest anterior): as ferramentas nao mudaram',
    h55['loaded'] and h['loaded'] and h55['reference_remaining']==h55['meta_reserva_dinamica_medida']==bud['remaining_tokens'] and h55['native_count_budget_equals_recomputed_context_budget'] and h55['native_count_budget_equals_manifest_budget'] and h['native_count_budget_equals_recomputed_context_budget'] and h['native_count_budget_equals_manifest_budget'] and h55['floor_remaining_ge_10000'] and h['floor_remaining_ge_10000'] and h55['memory_target_met'] and h['memory_target_met'] and h55['tools_sha256']==old55['tools_sha256'],
    {'haiku55':{k:h55[k] for k in('loaded','permanent','reference_input','reference_remaining','margin','output','tools_sha256')},'haiku':{k:h[k] for k in('loaded','permanent','reference_input','reference_remaining')},'tools_sha256_v404':old55['tools_sha256']})
# =============== E_ESCOPO (stat only) -> D3
cut_n=t_m-120;cut_w=(W/'app/RUNTIME_BASELINE.json').stat().st_mtime-600
changed={};n_seen=0;tmpf=[]
def sweep(d):
    global n_seen
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):sweep(e.path)
                    else:
                        n_seen+=1;s=e.stat(follow_symlinks=False)
                        if '.tmp_v380_' in e.name:tmpf.append(e.path)
                        if max(s.st_mtime,s.st_ctime)>=cut_w:changed[e.path]=(s.st_mtime,s.st_ctime,s.st_size)
                except OSError:pass
    except OSError:pass
t0=time.time();sweep(str(R));swp=round(time.time()-t0,1)
allowed=pdset|set(bk.values())
LOG=re.compile(r'^'+re.escape(str(R))+r'\\logs\\(?:web-server_[^\\]+\.log(?:\.err)?|web-supervisor\.log|gpu_[^\\]+\.csv|iald_heartbeat_telemetry\.jsonl)$')
NORMAL_WIDE=re.compile(r'^'+re.escape(str(R))+r'\\(?:logs\\llama-server_[^\\]+\.log(?:\.err)?|iald_psion_state_32B\.json)$')
narrow={p:v for p,v in changed.items() if max(v[0],v[1])>=cut_n};rest_n=sorted(p for p in narrow if p not in allowed)
chk('D3','E_ESCOPO','JANELA DA TROCA (varredura somente-stat de TODA a arvore de runtime, %d arquivos vistos, nenhum aberto pela varredura; .env e .iald_secret_key inclusive): desde maintenance.json-120s os arquivos com mtime/ctime sao so os %d destinos do plano, os 7 backups e %d logs vivos do reinicio do web/telemetria/gpu; 0 temporarios .tmp_v380_ orfaos; nenhum .py de runtime, .env, banco sqlite/db, iald-app ou outra release'%(n_seen,len(pd),len(rest_n)),
    allowed<=set(narrow) and all(LOG.match(p) for p in rest_n) and not tmpf and not [p for p in narrow if p.endswith(('.py','.env','.sqlite3','.db')) and p not in pdset] and not [p for p in narrow if '\\iald-app\\' in p],
    {'vistos':n_seen,'mudados':len(narrow),'plano+backups_presentes':len(allowed&set(narrow)),'logs_vivos':[(p.replace(str(R)+'\\',''),fmt(max(narrow[p][0],0))) for p in rest_n],'tmp_orfaos':tmpf,'segundos_varredura':swp})
wide_rest=sorted(p for p in changed if p not in allowed)
chk('D3','E_ESCOPO','JANELA LARGA (desde 10 min antes do RUNTIME_BASELINE, 07:43 — cobre construcao do plano, deploy e depois): alem do plano e dos backups so mudaram %d arquivos, todos de trabalho normal do app: logs web/supervisor/gpu/telemetria e, ANTES da janela (08:08:09, 7 min 39 s antes de maintenance.json), logs do llama e o estado do heartbeat iald_psion_state_32B.json (familia confidencial: stat, nunca aberto); nenhum sqlite, job, carteira, conta, consentimento, iald-app ou .py mudou'%len(wide_rest),
    all(LOG.match(p) or NORMAL_WIDE.match(p) for p in wide_rest) and not [p for p in wide_rest if p.endswith(('.py','.env','.sqlite3','.db','.sqlite3-wal','.sqlite3-shm'))] and not [p for p in wide_rest if '\\iald-app\\' in p or '\\canonical_releases\\' in p],
    {'arquivos':[{'path':p.replace(str(R)+'\\',''),'mtime':datetime.datetime.fromtimestamp(changed[p][0]).strftime('%m-%d %H:%M:%S'),'bytes':changed[p][2],'classe':('log/telemetria (durante ou apos a troca)' if LOG.match(p) and changed[p][0]>=t_m-5 else 'log/estado normal ANTES da janela' if NORMAL_WIDE.match(p) or changed[p][0]<t_m-5 else 'outro')} for p in wide_rest]})
inwin=sorted(p for p,v in changed.items() if p not in allowed and t_m-2<=v[0]<=t_r+1)
chk('D3','E_ESCOPO','DENTRO da janela exclusiva (maintenance.json - 2 s .. restart.json + 1 s) o unico escrito em R fora do plano e dos backups sao os logs do supervisor e do filho novo nascendo (web-supervisor.log, r3.log, r3.log.err); nada de dados do app (sqlite, json de contas, jobs, carteira)',
    all(re.search(r'\\logs\\(web-supervisor\.log|web-server_[^\\]+_r3\.log(\.err)?)$',p) for p in inwin) and len(inwin)>=1,{'dentro_da_janela':[(p.replace(str(R)+'\\',''),fmt(changed[p][0])) for p in inwin]})
v4not=[d for d in v4 if d not in pdset];v4bad=[d for d in v4not if not Path(d).is_file() or sha(d)!=v4[d]]
v2=rd(V2/'deployment.json')['files'];v2not=[d for d in v2 if d not in pdset and d not in v4];v2bad=[d for d in v2not if not Path(d).is_file() or sha(d)!=v2[d]]
chk('D3','E_ESCOPO','nada das releases anteriores foi tocado ou apagado (detecta mudanca com mtime preservado e remocao, que a varredura de mtime nao veria): os %d arquivos que a v404 instalou e que o plano v405 NAO reescreve (release v404 inteira, core_packet_v404_bound.txt da raiz etc.) e os %d da v402 que nem v404 nem v405 reescrevem continuam com o sha256 que o deployment.json de cada uma registrou; a intersecao v404 x plano v405 sao exatamente os 7 destinos com backup'%(len(v4not),len(v2not)),
    not v4bad and not v2bad and sorted(Path(d).name for d in v4 if d in pdset)==sorted(Path(r['destination']).name for r in pre),{'v404_nao_reescritos':len(v4not),'v404_divergentes':v4bad[:3],'v402_so_dela':len(v2not),'v402_divergentes':v2bad[:3]})
rels=sorted(p.name for p in (R/'canonical_releases').iterdir() if p.is_dir())
new_dirs=[x for x in rels if (R/'canonical_releases'/x).stat().st_ctime>=cut_n]
chk('D3','E_ESCOPO','canonical_releases: surgiu UMA pasta nova (v405_6a2138d73c1a) e nenhum arquivo das releases anteriores (v357..v404) foi tocado (stat + sha da v404/v402 acima)',new_dirs==[can.name] and len([p for p in changed if '\\canonical_releases\\' in p and not Path(p).is_relative_to(can)])==0,{'pastas':rels,'novas':new_dirs})
cut_w2=cut_n
newb=sorted(str(p.relative_to(W)) for p in W.rglob('*') if p.is_file() and 'review' not in p.relative_to(W).parts[:1] and 'validation' not in p.relative_to(W).parts[:1] and p.stat().st_mtime>=cut_w2)
allowedW={'maintenance.json','deployment.json','restart.json','INSTALLED_VERIFICATION.json','LOGIN_CHECK_v405.json','deploy_stdout.txt','deploy_stderr.txt','verify_stdout.txt','verify_stderr.txt','LICOES_v405.md','receipts\\v405-deploy-claim.json','receipts\\v405-deploy-submit.json','receipts\\v405-app-accept-r3.json','receipts\\v405-sources-accept-r3.json'}
chk('D3','E_ESCOPO','na pasta do build v405 (W, fora de R), desde a janela so surgiram maintenance/deployment/restart/INSTALLED_VERIFICATION/LOGIN_CHECK, os stdout/stderr do deploy e do verify, os recibos da missao (claim/submit do deploy e os dois aceites r3 do revisor do pacote) e LICOES_v405.md (nota de licoes da gerencia, escrita 08:18, DEPOIS do deploy; documentacao em W, nao em R); sem rollback_new_files nem mobile_backups',
    set(newb)<=allowedW and not (W/'rollback_new_files').exists() and not (W/'mobile_backups').exists(),{'novos':newb,'rollback_new_files':(W/'rollback_new_files').exists(),'mobile_backups':(W/'mobile_backups').exists()})
STORES=[R/'.iald_runtime/monthly_wallet/wallet.sqlite3',R/'.iald_runtime/chat_jobs/jobs.sqlite3',R/'.iald_runtime/app_evaluation/metrics.sqlite3',R/'.iald_runtime/app_evaluation/public_spend.sqlite3',R/'.iald_runtime/native_push/authorization.sqlite3',R/'.iald_runtime/native_push/native_push.sqlite3',R/'.iald_runtime/private_media/media.sqlite3',R/'iald_users.json',R/'iald_web/data/users.json',R/'owner_private/apple/authorized_activation_receipt.dpapi',R/'iald_uso_claude.json.reservas.sqlite3',R/'iald_uso_openai.json.reservas.sqlite3',Path(r'C:\IALD\bank\tglc_ledger.json')]
stst=[(str(s).replace(str(R)+'\\','R\\'),s.stat().st_mtime) for s in STORES if s.exists()]
okprefix=(can,R/'.iald_runtime'/'haiku55',R/'.iald_runtime'/'haiku')
sensitive_in_plan=[d for d in pd if not(any(Path(d).is_relative_to(x) for x in okprefix) or Path(d) in(nuc,R/'core_packet_v405_bound.txt')) or Path(d).suffix.lower() in('.sqlite3','.sqlite','.db','.env','.key','.dpapi','.pem') or Path(d).is_relative_to(R/'iald-app')]
def startup(i):
    t=(R/('logs/web-server_20261028_133856_r%d.log'%i)).read_bytes().decode('utf-8','replace').splitlines()
    g=lambda pat:next((re.search(pat,l).group(0) for l in t if re.search(pat,l)),None)
    return {'usuarios':g(r'Users: \d+ registered \(\d+ admin\)'),'contas_tglc':g(r'Contas: \d+'),'fatos_operador':g(r'\d+ fatos ativos'),'pedidos_acesso':g(r'Access Engine: \d+ pedidos \(\d+ pendentes\)'),'contratos':g(r'Contract Engine: \d+ contratos \(\d+ pendentes\)'),'ledger':g(r'Ledger: .*')}
s2,s3=startup(2),startup(3)
chk('D3','E_ESCOPO','carteira, consentimentos, contas e atividade preservados (o que e observavel sem abrir banco): (i) nenhum destino do plano esta em area de conta/carteira/sqlite/iald-app/segredo; (ii) cada loja existente (wallet.sqlite3, jobs.sqlite3, iald_users.json, users.json, authorization/native_push/media/app_evaluation/reservas .sqlite3, tglc_ledger.json) tem mtime ANTERIOR a janela (stat); (iii) o banner do filho v404 (r2) e o do filho v405 (r3) contam o MESMO: usuarios, contas TGLC, fatos do operador, pedidos de acesso, contratos e ledger (DECLARADO pelos logs do proprio servidor); nenhum banco foi aberto; deployment.json accounts_modified/bench_restarted/client_files_changed sao constantes: corroboradas por (i)-(iii), pelos processos e pela varredura',
    not sensitive_in_plan and all(m_<t_m-120 for _,m_ in stst) and len(stst)>=10 and s2==s3 and all(v for v in s3.values()),{'plano_em_area_sensivel':sensitive_in_plan,'lojas_stat':[(n,datetime.datetime.fromtimestamp(m_).strftime('%m-%d %H:%M')) for n,m_ in stst],'banner_r2_v404':s2,'banner_r3_v405':s3,'iald_app_mudou':[p for p in changed if '\\iald-app\\' in p]})
print(json.dumps({'n':len(checks),'ok':sum(c['ok'] for c in checks),'checks':checks,'web_pid':w2[0].pid,'web_created':w2[0].create_time(),'supervisor_pid':sup.pid,'supervisor_created':sup.create_time(),'login':status,'files_seen':n_seen,'t_m':t_m,'t_r':t_r,'installed_at':installed_at},ensure_ascii=False,indent=1,default=str))
