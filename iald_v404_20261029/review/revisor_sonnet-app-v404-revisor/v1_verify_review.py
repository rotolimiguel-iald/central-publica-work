"""Reviewer (sonnet-app-v404-revisor): independent READ-ONLY review of the v404 VERIFY step (declared scope: loaders + hashes + login + live process).
Same limits as d1: psutil queries only, stat-only sweep, hashes, one GET /login, fresh-process loaders with audit hook (d2_loaders.py)."""
import os,sys,json,hashlib,re,datetime,subprocess,http.client
from pathlib import Path
import psutil
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027');R=Path(r'C:\IALD\projetos_pyhton\IALD')
RV=W/'review/revisor_sonnet-app-v404-revisor';ME='sonnet-app-v404-revisor'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
checks=[]
def chk(g,d,ok,a=None):checks.append({'n':len(checks)+1,'grupo':g,'descricao':d,'ok':bool(ok),'achado':a})
plan=rd(W/'install_plan.json');dep=rd(W/'deployment.json');rs=rd(W/'restart.json');rel=rd(W/'app/RELEASE.json')
t_m=(W/'maintenance.json').stat().st_mtime;installed_at=datetime.datetime.fromisoformat(dep['installed_at']).timestamp()
d1=rd(RV/'d1_out.json');rdep=rd(W/'validation/review_deploy.json');t_rev=datetime.datetime.fromisoformat(rdep['timestamp_utc']).timestamp()
sub=rd(W/'receipts/v404-verify-submit.json')['task'];claim=W/'receipts/v404-verify-claim.json'
stale=[Path(e['path']).name for e in sub['evidence'] if sha(e['path'])!=e['sha256']]
chk('A_SUBMISSAO','recibo v404-verify-submit: verify review_pending, submetido por claude-gerencia-a7 (distinto do revisor), depende de deploy; as evidencias (INSTALLED_VERIFICATION.json, LOGIN_CHECK_v404.json) tem sha256 = bytes ATUAIS',
    sub['status']=='review_pending' and sub['submitted_by']=='claude-gerencia-a7' and sub['depends_on']==['deploy'] and {Path(e['path']).name for e in sub['evidence']}=={'INSTALLED_VERIFICATION.json','LOGIN_CHECK_v404.json'} and not stale,{'status':sub['status'],'by':sub['submitted_by'],'depends_on':sub['depends_on'],'stale':stale,'note':sub.get('note')})
da=rd(W/'receipts/v404-deploy-accept.json')['task'];dstale=[Path(e['path']).name for e in da['evidence']+da['review_evidence'] if sha(e['path'])!=e['sha256']]
pj=json.loads(subprocess.check_output([r'C:\Python314\python.exe','-B','-X','utf8',str(W/'mission_step.py'),'project'],cwd=str(W)));act={t['id']:t['status'] for t in pj['active']}
chk('A_SUBMISSAO','pre-condicao: deploy satisfeito pela minha revisao (reviewed_by = eu) e TODAS as evidencias pinadas do deploy (deployment/maintenance/restart/plano e review_deploy.json) continuam com os bytes de quando foram aceitas; verify e a unica etapa ativa',
    da['status']=='satisfied' and da['reviewed_by']==ME and not dstale and act=={'verify':'review_pending'},{'deploy':da['status'],'stale':dstale,'active':act,'revision':pj['revision']})
txt=json.dumps(sub,ensure_ascii=False)+Path(W/'LOGIN_CHECK_v404.json').read_text('utf-8')
lc=rd(W/'LOGIN_CHECK_v404.json')
chk('B_ESCOPO','o escopo declarado (LOGIN_CHECK_v404.json e recibo) exclui explicitamente a resposta viva do modelo (0 chamadas a provedor) e a inspecao fisica do celular; o criterio da missao cita "resposta do app citando a v404" -> essa parte NAO e coberta (declarada, nao escondida)',
    'sem resposta de modelo ao vivo' in lc['escopo'] and 'sem inspeção física do celular' in lc['escopo'] and 'resposta do app citando a v404' in sub['criterion'],{'escopo':lc['escopo'],'criterio':sub['criterion'][:200]})
c402=rd(V2/'receipts/v402-verify-accept.json')['task']['criterion'];iv402=rd(V2/'INSTALLED_VERIFICATION.json');lc402=rd(V2/'LOGIN_CHECK_v402.json')
chk('B_ESCOPO','precedente: o criterio de verify e textualmente o mesmo da v402 (tirada a versao; aceita com o MESMO escopo: loaders + hashes + login; 0 chamadas a provedor; sem resposta viva, memorias nem backend x build); INSTALLED_VERIFICATION.json tem a mesma forma e o mesmo escopo declarado',
    sub['criterion'].replace('v404','vNNN')==c402.replace('v402','vNNN') and set(rd(W/'INSTALLED_VERIFICATION.json'))==set(iv402) and rd(W/'INSTALLED_VERIFICATION.json')['scope']==iv402['scope'],{'criterio_igual_exceto_versao':sub['criterion'].replace('v404','vNNN')==c402.replace('v402','vNNN')})
# C_EVIDENCIA
out=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',str(RV/'d2_loaders.py')],capture_output=True,cwd=str(RV));assert out.returncode==0,out.stderr.decode()[:300]
L=json.loads(out.stdout);iv=rd(W/'INSTALLED_VERIFICATION.json');pk=W/'app/packages'
okL=(iv['status']=='PASS' and iv['identity']==L['identity']==plan['deployment_identity'] and iv['public_commit']==rel['espelho_commit'] and iv['files_verified']==len(plan['files'])==1464
     and iv['packages']['haiku55']=={'permanent_tokens':L['packages']['haiku55']['permanent_tokens'],'prefix_bytes':L['packages']['haiku55']['prefix_bytes']}
     and iv['packages']['haiku']=={'permanent_tokens':L['packages']['haiku']['permanent_tokens'],'prefix_bytes':L['packages']['haiku']['prefix_bytes']}
     and L['packages']['haiku55']['prefix_sha256']==sha(pk/'haiku_expanded/prefix.md') and L['packages']['haiku']['prefix_sha256']==sha(pk/'shared/prefix.md')
     and iv['native_bytes']==L['native']['bytes']==52030 and iv['public_prompt_bytes']==L['public_prompt']['bytes']==851087 and L['public_prompt']['sha256']==sha(pk/'sonnet_public/prefix.md')
     and iv['JEV_release']==L['jev']['release']=='v404' and iv['provider_calls']==0 and iv['science_executed'] is False and L['kernel_sources']==1438)
chk('C_EVIDENCIA','INSTALLED_VERIFICATION.json (gerencia) = o que os MEUS loaders do runtime medem AGORA em processo novo (audit hook): identidade, commit, 2 pacotes (tokens permanentes/bytes/sha do prefixo = os revisados), native 52.030 B, prompt publico 851.087 B, Jev v404, 1438 fontes do kernel',okL,{'tokens':{k:v['permanent_tokens'] for k,v in L['packages'].items()}})
bad=[r['destination'] for r in plan['files'] if sha(r['destination'])!=r['sha256']]
chk('C_EVIDENCIA','os 1464 arquivos instalados continuam com o sha256 do plano (recomputado agora, nao confiado ao PASS da gerencia)',not bad,{'divergentes':bad[:3]})
nuc=R/'iald_nucleo_fixo.json';m=rd(nuc)
chk('C_EVIDENCIA','o nucleo (iald_nucleo_fixo.json) AINDA aponta active_cluster, operational_core e jev_control para v404, com commit e source sha256 de RELEASE.json, e e byte a byte o manifest_install revisado',
    (m['active_cluster']['release'],m['operational_core']['current_release'],m['jev_control']['release'])==('v404',)*3 and m['active_cluster']['commit']==rel['espelho_commit'] and {m['active_cluster']['release_source_sha256'],m['operational_core']['release_source_sha256'],m['jev_control']['source_sha256']}=={rel['um_py_sha256']} and nuc.read_bytes()==(W/'app/science/memory_stage/manifest_install.json').read_bytes(),{'commit':m['active_cluster']['commit'][:12]})
# D_VIVO
def web():
    r=[]
    for p in psutil.process_iter(['name']):
        try:
            if (p.info['name'] or '').lower()=='python.exe' and any(a and str(Path(a)).lower()==str(R/'iald_web_server.py').lower() for a in p.cmdline()[1:] if not a.startswith('-')):r.append(p)
        except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
    return r
lis=lambda:[c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==8082]
w1=web();l1=lis();ch=w1[0];sp=ch.parent()
chk('D_VIVO','AGORA: PID 69428 e o unico processo web e o unico ouvinte da 8082, sob o supervisor 38024 (mesmo create_time do restart.json), nenhum suspenso',
    len(w1)==1 and len(l1)==1 and ch.pid==l1[0].pid==rs['new_web_pid'] and ch.ppid()==rs['supervisor_pid'] and sp.create_time()==rs['supervisor_created'] and ch.status()!=psutil.STATUS_STOPPED and sp.status()!=psutil.STATUS_STOPPED,{'child':ch.pid,'ppid':ch.ppid(),'status':[ch.status(),sp.status()]})
chk('D_VIVO','o filho 69428 e o MESMO de quando revisei o deploy (create_time identico ao que registrei em d1_out.json): nao reiniciou desde a instalacao, logo e a instancia que nasceu depois dos arquivos da v404',
    ch.pid==d1['web_pid'] and ch.create_time()==d1['web_created'] and sp.create_time()==d1['supervisor_created'] and ch.create_time()>installed_at,{'created':datetime.datetime.fromtimestamp(ch.create_time()).isoformat()})
conn=http.client.HTTPConnection('127.0.0.1',8082,timeout=20);conn.request('GET','/login');r=conn.getresponse();status=r.status;r.read(1<<20);conn.close()
chk('D_VIVO','GET local http://127.0.0.1:8082/login = 200 AGORA (unico acesso de rede deste revisor; corpo descartado)',status==200,{'http':status})
t_lc=(W/'LOGIN_CHECK_v404.json').stat().st_mtime
chk('D_VIVO','LOGIN_CHECK_v404.json da gerencia: login_http_status 200, URL local 8082/login, feito DEPOIS da instalacao e do reinicio e antes do submit do verify',
    lc['login_http_status']==200 and lc['url']=='http://127.0.0.1:8082/login' and installed_at<(W/'restart.json').stat().st_mtime<t_lc<(W/'receipts/v404-verify-submit.json').stat().st_mtime and lc['por']=='claude-gerencia-a7',{'em':lc['em']})
w2=web();l2=lis()
chk('D_VIVO','depois do GET: mesmo PID, mesmo create_time, mesmo ouvinte (o servidor nao reiniciou durante a revisao)',[(p.pid,p.ppid(),p.create_time()) for p in w2]==[(p.pid,p.ppid(),p.create_time()) for p in w1] and [c.pid for c in l2]==[c.pid for c in l1],{'pid':w2[0].pid})
# E_ESCOPO
cut=t_m-120;changed=[];tmp=[];n=0
def sweep(d):
    global n
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):sweep(e.path)
                    else:
                        n+=1;s=e.stat(follow_symlinks=False)
                        if '.tmp_v380_' in e.name:tmp.append(e.path)
                        if max(s.st_mtime,s.st_ctime)>=cut:changed.append((e.path,max(s.st_mtime,s.st_ctime)))
                except OSError:pass
    except OSError:pass
sweep(str(R))
allowed=set(r['destination'] for r in plan['files'])|set(dep['backups'].values())
rest=[(p,t) for p,t in changed if p not in allowed]
LOG=re.compile(r'^'+re.escape(str(R))+r'\\logs\\(?:web-server_[^\\]+\.log(?:\.err)?|web-supervisor\.log|gpu_[^\\]+\.csv|iald_heartbeat_telemetry\.jsonl)$')
late=[p for p,t in changed if t>t_rev and p in allowed]
chk('E_ESCOPO','varredura somente-stat da arvore de runtime (%d arquivos, nenhum aberto): desde a janela do deploy so mudaram os 1464 destinos, os 7 backups e logs vivos; NENHUM destino/backup foi tocado depois da minha revisao do deploy (o verify e as evidencias dele nao escreveram nada em producao); 0 temporarios .tmp_v380_'%n,
    set(p for p,_ in changed)>=allowed and all(LOG.match(p) for p,_ in rest) and not late and not tmp,{'vistos':n,'mudados':len(changed),'logs_vivos':sorted(p.replace(str(R)+'\\','') for p,_ in rest),'destinos_tocados_apos_minha_revisao':late[:3]})
newb=sorted(p.name for p in W.rglob('*') if p.is_file() and 'review' not in p.parts and 'validation' not in p.parts and p.stat().st_mtime>t_rev)
chk('E_ESCOPO','na pasta do build, os unicos arquivos novos desde a minha revisao do deploy sao os do verify (LOGIN_CHECK/recibos de claim e submit do verify) e o meu aceite do deploy; INSTALLED_VERIFICATION.json e LOGIN_CHECK_v404.json nao foram regravados (sem .bak_)',
    set(newb)<={'v404-verify-claim.json','v404-verify-submit.json','v404-deploy-accept.json'} and not list(W.glob('INSTALLED_VERIFICATION.json.bak_*')) and not list(W.glob('LOGIN_CHECK_v404.json.bak_*')),{'novos':newb})
print(json.dumps({'n':len(checks),'ok':sum(c['ok'] for c in checks),'checks':checks,'web_pid':w2[0].pid,'web_created':w2[0].create_time(),'login':status},ensure_ascii=False,indent=1,default=str))
