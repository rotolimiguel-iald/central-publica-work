"""Reviewer (sonnet-app-v405-revisor-d): independent READ-ONLY review of the v405 VERIFY step (declared scope: loaders + hashes + login + live process).
Adapted from the v404 reviewer's v1_verify_review.py. Limits as before: psutil queries only (no process touched), stat-only sweep of R (no file opened by the
sweep), hashes of installed files, ONE GET http://127.0.0.1:8082/login. The runtime loaders are NOT re-run (coordinator's order): the fresh-process loader
measurement of the deploy review (d2_out.json) is reused, and its inputs (1472 destinations, 7 backups, 171 runtime-code files, active manifest) are re-hashed NOW,
so the earlier measurement still describes the files that exist today. Output: JSON on stdout."""
import os,sys,json,hashlib,re,datetime,subprocess,http.client,collections
from pathlib import Path
import psutil
PY=r'C:\Python314\python.exe'
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');R=Path(r'C:\IALD\projetos_pyhton\IALD')
RV=W/'review/revisor_sonnet-app-v405-revisor-d';ME='sonnet-app-v405-revisor-d';SUBMITTER='claude-gerencia-a7'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
fmt=lambda t:datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S.%f')[:12]
checks=[]
def chk(V,g,d,ok,a=None):checks.append({'n':len(checks)+1,'V':V,'grupo':g,'descricao':d,'ok':bool(ok),'achado':a})
plan=rd(W/'install_plan.json');dep=rd(W/'deployment.json');rs=rd(W/'restart.json');rel=rd(W/'app/RELEASE.json');mt=rd(W/'maintenance.json')
t_m=(W/'maintenance.json').stat().st_mtime;installed_at=datetime.datetime.fromisoformat(dep['installed_at']).timestamp();t_r=(W/'restart.json').stat().st_mtime
d1=rd(RV/'d1_out.json');L=rd(RV/'d2_out.json');rdep=rd(W/'validation/review_deploy.json')
t_rev=datetime.datetime.fromisoformat(rdep['timestamp_utc']).timestamp()
pd=[r['destination'] for r in plan['files']];pdset=set(pd)
# ===================== A_SUBMISSAO (V1)
sub=rd(W/'receipts/v405-verify-submit.json')['task'];clm=rd(W/'receipts/v405-verify-claim.json')['task']
pins={Path(e['path']).name:e['sha256'] for e in sub['evidence']};now={n:sha(W/n) for n in pins}
stale=[n for n in pins if pins[n]!=now[n]]
chk('V1','A_SUBMISSAO','recibo v405-verify-submit: verify review_pending, submetido por claude-gerencia-a7 (distinto de mim), depende de deploy; as evidencias sao exatamente INSTALLED_VERIFICATION.json e LOGIN_CHECK_v405.json e o sha256 PINADO na missao = sha256 dos bytes de hoje (recomputado agora)',
    sub['status']=='review_pending' and sub['submitted_by']==SUBMITTER and sub['submitted_by']!=ME and sub['depends_on']==['deploy'] and set(pins)=={'INSTALLED_VERIFICATION.json','LOGIN_CHECK_v405.json'} and not stale and clm['lease'] is not None and clm['lease']['owner']==SUBMITTER,
    {'pinado':pins,'bytes_hoje':now,'stale':stale,'claim_lease_owner':(clm.get('lease') or {}).get('owner'),'note_do_submit':sub.get('note'),'note_do_claim':clm.get('note')})
da=rd(W/'receipts/v405-deploy-accept.json')['task'];dstale=[Path(e['path']).name for e in da['evidence']+da['review_evidence'] if sha(e['path'])!=e['sha256']]
pj=json.loads(subprocess.check_output([PY,'-B','-X','utf8',str(W/'mission_step.py'),'project'],cwd=str(W)));act={t['id']:t['status'] for t in pj['active']}
chk('V1','A_SUBMISSAO','pre-condicao: deploy SATISFEITO pela minha revisao (reviewed_by = eu; submitted_by = gerencia) e TODAS as evidencias pinadas do aceite (deployment/maintenance/restart/plano e meu review_deploy.json) continuam com os bytes de quando foram aceitas; verify e a unica etapa ativa; revisao da missao %d'%pj['revision'],
    da['status']=='satisfied' and da['reviewed_by']==ME and da['submitted_by']==SUBMITTER and not dstale and act=={'verify':'review_pending'},{'deploy':da['status'],'reviewed_by':da['reviewed_by'],'stale':dstale,'active':act,'revision':pj['revision'],'review_deploy_sha256':sha(W/'validation/review_deploy.json')})
order=[('installed_at',installed_at),('restart.json',t_r),('INSTALLED_VERIFICATION.json',(W/'INSTALLED_VERIFICATION.json').stat().st_mtime),('LOGIN_CHECK_v405.json',(W/'LOGIN_CHECK_v405.json').stat().st_mtime),('meu accept do deploy',(W/'receipts/v405-deploy-accept.json').stat().st_mtime),('claim do verify',(W/'receipts/v405-verify-claim.json').stat().st_mtime),('submit do verify',(W/'receipts/v405-verify-submit.json').stat().st_mtime)]
chk('V2','A_SUBMISSAO','ordem temporal DECLARADA como fora de ordem: as 2 evidencias foram feitas (08:16:39-40) ANTES do meu aceite do deploy e do claim do verify (21 e 22 min depois), nunca regravadas (sem .bak_); por isso nao as confiei: refiz as medidas (abaixo) e o que bate hoje e o estado de hoje, nao so o de 08:16',
    all(order[i][1]<order[i+1][1] for i in range(len(order)-1)) and not list(W.glob('INSTALLED_VERIFICATION.json.bak_*')) and not list(W.glob('LOGIN_CHECK_v405.json.bak_*')),[(n,fmt(t)) for n,t in order])
# ===================== B_ESCOPO (V2)
iv=rd(W/'INSTALLED_VERIFICATION.json');lc=rd(W/'LOGIN_CHECK_v405.json')
chk('V2','B_ESCOPO','o escopo declarado e honesto no que EXCLUI: LOGIN_CHECK_v405.json ("sem resposta de modelo ao vivo (0 chamadas a provedor...); sem inspecao fisica do celular") e INSTALLED_VERIFICATION.json ("not live model response or physical mobile inspection") dizem o que nao fizeram; o criterio da missao cita "resposta do app citando a v405" e "memorias atualizadas com recibos" e "distinguir backend e build" -> essas 3 partes NAO sao cobertas pelas evidencias (declarado, nao escondido)',
    'sem resposta de modelo ao vivo' in lc['escopo'] and 'sem inspeção física do celular' in lc['escopo'] and 'not live model response' in iv['scope'] and 'physical mobile inspection' in iv['scope'] and 'resposta do app citando a v405' in sub['criterion'] and 'memórias atualizadas com recibos' in sub['criterion'] and 'distinguir alteração de backend' in sub['criterion'],
    {'escopo_login_check':lc['escopo'],'scope_installed_verification':iv['scope'],'criterio':sub['criterion']})
v=(W/'verify_installed.py').read_text('utf-8')
chk('V2','B_ESCOPO','"provider_calls: 0" e "science_executed: false" em INSTALLED_VERIFICATION.json sao CONSTANTES literais do verify_installed.py (nao instrumentadas); a corroboracao independente e que a mesma cadeia de carregadores rodou no meu processo com audit hook (sem socket/subprocess/escrita: 0 eventos bloqueados) e que nenhum livro do app (carteira, gasto publico, jobs, reservas) foi escrito desde 08:16:39 (abaixo); o script nao importa SDK de provedor',
    "'provider_calls':0" in v.replace(' ','') and "'science_executed':False" in v.replace(' ','') and not L['audit']['blocked_events_attempted'] and not re.search(r'anthropic|openai|requests|urllib|httpx|socket',v),{'audit':L['audit'],'verify_installed.py_sha256':sha(W/'verify_installed.py')[:16]})
V4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
a4=rd(V4/'receipts/v404-verify-accept.json');t4=a4['task'];iv4=rd(V4/'INSTALLED_VERIFICATION.json');lc4=rd(V4/'LOGIN_CHECK_v404.json')
chk('V2','B_ESCOPO','precedente (so o que verifiquei): o criterio de verify e textualmente o mesmo da v404 (tirada a versao), aceito la (status satisfied, revisao %d da missao, revisor da v404) com o MESMO escopo declarado: INSTALLED_VERIFICATION.json com as mesmas chaves e o mesmo "scope"; LOGIN_CHECK da v404 exclui resposta viva e celular com as mesmas palavras'%a4['receipt']['revision'],
    t4['status']=='satisfied' and t4['criterion'].replace('v404','vNNN')==sub['criterion'].replace('v405','vNNN') and set(iv4)==set(iv) and iv4['scope']==iv['scope'] and 'sem resposta de modelo ao vivo' in lc4['escopo'] and 'sem inspeção física do celular' in lc4['escopo'],
    {'v404_accept_revisao':a4['receipt']['revision'],'v404_reviewed_by':t4['reviewed_by'],'v404_scope':iv4['scope'],'v405_scope':iv['scope']})
cnt=collections.Counter(Path(d).suffix.lower() or '(sem)' for d in pd)
CLIENT_SFX={'.html','.htm','.js','.mjs','.cjs','.css','.apk','.aab','.ipa','.png','.jpg','.jpeg','.gif','.svg','.ico','.webp','.woff','.woff2','.ttf','.plist','.gradle','.xml','.webmanifest','.swift','.kt','.java','.dex'}
cli=[d for d in pd if Path(d).suffix.lower() in CLIENT_SFX or Path(d).is_relative_to(R/'iald-app') or Path(d).is_relative_to(R/'iald_web') or any(x in Path(d).relative_to(R).parts for x in('static','templates','www','public','assets'))]
roots=sorted({str(Path(d).relative_to(R).parts[0]) if len(Path(d).relative_to(R).parts)>1 else '(raiz de R)' for d in pd})
chk('V2','B_ESCOPO','backend x build: NENHUM dos %d destinos do plano e arquivo de cliente — nenhum sob iald-app (casca Capacitor iOS/Android), iald_web, static/templates/www/public/assets e nenhum com extensao de cliente (.html .js .css .apk .aab .ipa imagem fonte .xml .plist .gradle .java .kt); os destinos sao so dados do servidor (release canonica, pacotes de memoria haiku/haiku55, nucleo, pacote do JEV); runtime_python_changes=0 (171 arquivos de codigo com hash de antes); logo e mudanca de BACKEND compartilhado web/iOS/Android, sem necessidade de build de cliente'%len(pd),
    not cli and plan['runtime_python_changes']==0,{'extensoes_do_plano':dict(cnt),'raizes_de_R_tocadas_pelo_plano':roots,'arquivos_de_cliente_no_plano':cli[:5]})
# ===================== C_EVIDENCIA (V1): evidence vs what I measured
plan_id=plan['deployment_identity']
bad=[d for d,r in zip(pd,plan['files']) if sha(d)!=r['sha256']]
bk=dep['backups'];bkbad=[b for d,b in bk.items() if sha(b)!=next(r['baseline'] for r in plan['files'] if r['destination']==d)]
base=rd(W/'app/RUNTIME_BASELINE.json')['files'];bchg=[Path(b['path']).name for b in base if not Path(b['path']).is_file() or sha(b['path'])!=b['sha256']]
nuc=R/'iald_nucleo_fixo.json'
chk('V1','C_EVIDENCIA','as ENTRADAS das minhas medicoes de carregadores (d2_out.json, 08:32) continuam iguais hoje: os %d destinos tem o sha256 do plano (recomputado agora; "integridade apos a implantacao" que INSTALLED_VERIFICATION declara com files_verified), os 7 backups tem os bytes anteriores, os 171 arquivos de codigo do runtime so diferem no manifesto ativo, e o manifesto ativo e byte a byte o manifest_install revisado'%len(pd),
    not bad and not bkbad and bchg==['iald_nucleo_fixo.json'] and nuc.read_bytes()==(W/'app/science/memory_stage/manifest_install.json').read_bytes() and sha(nuc)==dep['files'][str(nuc)],{'destinos_divergentes':bad[:3],'backups_divergentes':bkbad[:3],'runtime_diff':bchg,'manifesto_sha256':sha(nuc)})
pk55=L['packages']['haiku55'];pk=L['packages']['haiku']
okiv=(iv['status']=='PASS' and iv['files_verified']==len(pd)==1472 and iv['identity']==L['identity']==plan_id and iv['public_commit']==rel['espelho_commit']==rd(nuc)['active_cluster']['commit']
      and iv['packages']['haiku55']=={'permanent_tokens':pk55['permanent_tokens'],'prefix_bytes':pk55['prefix_bytes']} and iv['packages']['haiku']=={'permanent_tokens':pk['permanent_tokens'],'prefix_bytes':pk['prefix_bytes']}
      and iv['native_bytes']==L['native']['bytes'] and iv['public_prompt_bytes']==L['public_prompt']['bytes'] and iv['JEV_release']==L['jev']['release']=='v405' and L['jev']['source_sha256']==rel['um_py_sha256']
      and iv['provider_calls']==0 and iv['science_executed'] is False)
chk('V1','C_EVIDENCIA','INSTALLED_VERIFICATION.json (pinado na missao) = o que MEUS carregadores mediram em processo novo com audit hook (d2_out.json): status PASS, 1472 arquivos, identidade (release v405, source 0030242565cc13f6..., cluster, nucleo) = deployment_identity do plano, commit 6a2138d7..., haiku55 e haiku (tokens permanentes e bytes do prefixo), native 52.409 B, prompt publico 858.881 B, JEV v405 com source_sha256 = pino do programa',okiv,
    {'iv':{k:iv[k] for k in('status','files_verified','public_commit','native_bytes','public_prompt_bytes','JEV_release','provider_calls','science_executed')},'iv_identity':iv['identity'],'iv_packages':iv['packages'],'medido_por_mim':{'haiku55':[pk55['permanent_tokens'],pk55['prefix_bytes']],'haiku':[pk['permanent_tokens'],pk['prefix_bytes']],'native':L['native']['bytes'],'public':L['public_prompt']['bytes'],'jev':L['jev']['release'],'jev_contract_sha256':L['jev']['contract_file_sha256'],'kernel_sources':L['kernel_sources']},'loaders_medidos_em':datetime.datetime.fromtimestamp((RV/'d2_out.json').stat().st_mtime).strftime('%H:%M:%S')})
m=rd(nuc)
chk('V1','C_EVIDENCIA','o manifesto ativo AINDA aponta active_cluster, operational_core e jev_control para v405, com commit e source sha256 de RELEASE.json; jev_control_v405.json presente com o sha pinado no manifesto',
    (m['active_cluster']['release'],m['operational_core']['current_release'],m['jev_control']['release'])==('v405',)*3 and m['active_cluster']['commit']==rel['espelho_commit'] and {m['active_cluster']['release_source_sha256'],m['operational_core']['release_source_sha256'],m['jev_control']['source_sha256']}=={rel['um_py_sha256']} and Path(m['jev_control']['path']).is_file() and sha(m['jev_control']['path'])==m['jev_control']['sha256'],
    {'commit':m['active_cluster']['commit'],'jev_control':Path(m['jev_control']['path']).name,'jev_sha16':m['jev_control']['sha256'][:16]})
# ===================== D_VIVO (V1 login + V3)
def web():
    r=[]
    for p in psutil.process_iter(['name']):
        try:
            if (p.info['name'] or '').lower()=='python.exe' and any(a and str(Path(a)).lower()==str(R/'iald_web_server.py').lower() for a in p.cmdline()[1:] if not a.startswith('-')):r.append(p)
        except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
    return r
lis=lambda port=8082:[c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==port]
w1=web();l1=lis();ch=w1[0];sp=ch.parent()
chk('V3','D_VIVO','AGORA: PID %d e o UNICO processo python.exe iald_web_server.py e o unico ouvinte da 8082, sob o supervisor %d (create_time IDENTICO ao de restart.json/maintenance.json), start_iald_web.ps1 sem -NoSupervise, nenhum suspenso'%(rs['new_web_pid'],rs['supervisor_pid']),
    len(w1)==1 and len(l1)==1 and ch.pid==l1[0].pid==rs['new_web_pid']==92204 and ch.ppid()==rs['supervisor_pid']==38024 and sp.create_time()==rs['supervisor_created'] and any(str(Path(a)).lower()==str(R/'start_iald_web.ps1').lower() for a in sp.cmdline()[1:] if a and not a.startswith('-')) and not any(a.lower()=='-nosupervise' for a in sp.cmdline()) and ch.status()!=psutil.STATUS_STOPPED and sp.status()!=psutil.STATUS_STOPPED,
    {'web':[p.pid for p in w1],'listeners':[c.pid for c in l1],'ppid':ch.ppid(),'status':[ch.status(),sp.status()],'sup_created':datetime.datetime.fromtimestamp(sp.create_time()).isoformat(),'agora':datetime.datetime.now().strftime('%H:%M:%S')})
chk('V3','D_VIVO','o filho %d e o MESMO que medi na revisao do deploy (create_time identico ao de d1_out.json: %s): nao reiniciou desde a instalacao, logo e a instancia que nasceu DEPOIS dos arquivos da v405; supervisor identico; nao ha outro processo web'%(ch.pid,fmt(d1['web_created'])),
    ch.pid==d1['web_pid'] and ch.create_time()==d1['web_created'] and sp.create_time()==d1['supervisor_created'] and ch.create_time()>installed_at,{'created':datetime.datetime.fromtimestamp(ch.create_time()).isoformat(),'uptime_min':round((datetime.datetime.now().timestamp()-ch.create_time())/60,1)})
conn=http.client.HTTPConnection('127.0.0.1',8082,timeout=20);conn.request('GET','/login');r=conn.getresponse();status=r.status;r.read(1<<20);conn.close()
chk('V1','D_VIVO','GET NOVO agora (unico acesso de rede deste revisor, corpo descartado) http://127.0.0.1:8082/login = 200 = login_http_status do LOGIN_CHECK_v405.json (200, mesma URL local, "por" a gerencia, feito DEPOIS da instalacao e do restart e ANTES do claim do verify)',
    status==200==lc['login_http_status'] and lc['url']=='http://127.0.0.1:8082/login' and lc['por']==SUBMITTER and installed_at<t_r<(W/'LOGIN_CHECK_v405.json').stat().st_mtime<(W/'receipts/v405-verify-claim.json').stat().st_mtime,{'http_agora':status,'login_check_em':lc['em'],'login_check_http':lc['login_http_status']})
w2=web();l2=lis()
chk('V3','D_VIVO','depois do GET: mesmo PID, mesmo create_time, mesmo supervisor, mesmo ouvinte (o servidor nao reiniciou durante esta revisao)',[(p.pid,p.ppid(),p.create_time()) for p in w2]==[(p.pid,p.ppid(),p.create_time()) for p in w1] and [c.pid for c in l2]==[c.pid for c in l1],{'pid':w2[0].pid})
other={}
for port,label in((8081,'llama (nativa)'),(18777,'Bancada Um')):
    for c in lis(port):
        p=psutil.Process(c.pid);other[label]={'port':port,'pid':c.pid,'created':datetime.datetime.fromtimestamp(p.create_time()).strftime('%m-%d %H:%M:%S'),'created_before_window':p.create_time()<t_m,'suspended':p.status()==psutil.STATUS_STOPPED}
chk('V3','D_VIVO','continuidade dos outros servicos (nao pedido, barato): nativa 8081 e Bancada Um 18777 seguem escutando, criados antes da janela, nenhum suspenso',
    all(v['created_before_window'] and not v['suspended'] for v in other.values()) and set(other)=={'llama (nativa)','Bancada Um'},other)
# ===================== E_ESCOPO / integridade (V2)
cut=t_m-120;changed={};tmpf=[];n=0
def sweep(d):
    global n
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):sweep(e.path)
                    else:
                        n+=1;s=e.stat(follow_symlinks=False)
                        if '.tmp_v380_' in e.name:tmpf.append(e.path)
                        if max(s.st_mtime,s.st_ctime)>=cut:changed[e.path]=max(s.st_mtime,s.st_ctime)
                except OSError:pass
    except OSError:pass
sweep(str(R))
allowed=pdset|set(dep['backups'].values());rest=sorted(p for p in changed if p not in allowed)
LOG=re.compile(r'^'+re.escape(str(R))+r'\\logs\\(?:web-server_[^\\]+\.log(?:\.err)?|web-supervisor\.log|gpu_[^\\]+\.csv|iald_heartbeat_telemetry\.jsonl)$')
late=[p for p in changed if p in allowed and changed[p]>t_rev]
chk('V2','E_ESCOPO','varredura somente-stat de TODO R (%d arquivos, nenhum aberto): desde a janela do deploy so mudaram os %d destinos, os 7 backups e logs vivos; NENHUM destino ou backup foi tocado depois da minha revisao do deploy (o verify e as evidencias dele nao escreveram nada em producao); 0 temporarios .tmp_v380_; nada em iald-app'%(n,len(pd)),
    allowed<=set(changed) and all(LOG.match(p) for p in rest) and not late and not tmpf and not [p for p in changed if '\\iald-app\\' in p],{'vistos':n,'mudados':len(changed),'logs_vivos':[(p.replace(str(R)+'\\',''),fmt(changed[p])) for p in rest],'destinos_ou_backups_tocados_apos_minha_revisao':late[:3]})
STORES=[R/'.iald_runtime/monthly_wallet/wallet.sqlite3',R/'.iald_runtime/chat_jobs/jobs.sqlite3',R/'.iald_runtime/app_evaluation/metrics.sqlite3',R/'.iald_runtime/app_evaluation/public_spend.sqlite3',R/'iald_uso_claude.json.reservas.sqlite3',R/'iald_uso_openai.json.reservas.sqlite3',R/'iald_users.json']
t_iv=(W/'INSTALLED_VERIFICATION.json').stat().st_mtime
stt=[(s.name,datetime.datetime.fromtimestamp(s.stat().st_mtime).strftime('%d/%m %H:%M')) for s in STORES if s.exists()]
chk('V2','E_ESCOPO','nenhum livro de gasto/job/carteira/reserva/cadastro foi escrito depois da verificacao (08:16:39): carteira, gasto publico, jobs, metricas, reservas dos provedores e cadastro de usuarios tem mtime ANTERIOR a INSTALLED_VERIFICATION.json — nenhum gasto pago registrado nem job gravado pelo app desde a troca (corroboracao por ausencia; chat com a nativa local, que nao grava esses livros, nao fica excluido). ATENCAO: os logs web-supervisor.log e r3.log NAO servem de prova de "sem uso": meu GET /login e o da gerencia tambem nao deixaram linha neles (r3.log segue com 2140 B, mtime 08:16:18), logo requisicao HTTP nao e registrada ali',
    len(stt)==len(STORES) and all(s.stat().st_mtime<t_iv for s in STORES),{'lojas':stt,'web-supervisor.log_mtime':fmt((R/'logs/web-supervisor.log').stat().st_mtime),'r3.log_mtime':fmt((R/'logs/web-server_20261028_133856_r3.log').stat().st_mtime),'r3.log_bytes':(R/'logs/web-server_20261028_133856_r3.log').stat().st_size,'heartbeat_telemetry_mtime(local, nativa)':fmt((R/'logs/iald_heartbeat_telemetry.jsonl').stat().st_mtime)})
newb=sorted(str(p.relative_to(W)) for p in W.rglob('*') if p.is_file() and p.relative_to(W).parts[0] not in('review','validation') and p.stat().st_mtime>t_rev)
chk('V2','E_ESCOPO','na pasta do build, os unicos arquivos novos desde a minha revisao do deploy sao o meu aceite do deploy e os recibos de claim e submit do verify; INSTALLED_VERIFICATION.json e LOGIN_CHECK_v405.json nao foram regravados',
    set(newb)<={'receipts\\v405-deploy-accept.json','receipts\\v405-verify-claim.json','receipts\\v405-verify-submit.json'},{'novos':newb,'review_deploy_timestamp':rdep['timestamp_utc']})
print(json.dumps({'n':len(checks),'ok':sum(c['ok'] for c in checks),'checks':checks,'web_pid':w2[0].pid,'web_created':w2[0].create_time(),'supervisor_pid':sp.pid,'supervisor_created':sp.create_time(),'login':status,'files_seen':n,'revision':pj['revision']},ensure_ascii=False,indent=1,default=str))
