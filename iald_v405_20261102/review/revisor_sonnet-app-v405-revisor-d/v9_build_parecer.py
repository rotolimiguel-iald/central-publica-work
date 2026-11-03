"""Builds W\\validation\\review_verify.json from the reviewer's own measurements (v1_out.json, d2_out.json, d1_out.json).
Numbers/hashes are read from those outputs or recomputed here; nothing typed from memory. Checks are located by a stable phrase of their
description (not by position). Writes once (temp -> verify -> replace). PASS only if every check is ok AND the live web process is still the one measured."""
import json,hashlib,datetime,os
from pathlib import Path
import psutil
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');RV=W/'review/revisor_sonnet-app-v405-revisor-d';R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
v=rd(RV/'v1_out.json');L=rd(RV/'d2_out.json');d1=rd(RV/'d1_out.json')
def F(s):
    r=[c for c in v['checks'] if s in c['descricao']]
    assert len(r)==1,(s,len(r))
    return r[0]
A=F('recibo v405-verify-submit');B=F('pre-condicao: deploy SATISFEITO');T=F('ordem temporal DECLARADA');S=F('o escopo declarado e honesto');K=F('"provider_calls: 0"');P=F('precedente (so o que verifiquei)')
X=F('backend x build');I=F('as ENTRADAS das minhas medicoes');Q=F('INSTALLED_VERIFICATION.json (pinado na missao)');M=F('o manifesto ativo AINDA aponta')
LV=F('AGORA: PID');SC=F('e o MESMO que medi');G=F('GET NOVO agora');AG=F('depois do GET');O=F('continuidade dos outros servicos')
SW=F('varredura somente-stat de TODO R');LG=F('nenhum livro de gasto');WN=F('na pasta do build')
iv=rd(W/'INSTALLED_VERIFICATION.json');lc=rd(W/'LOGIN_CHECK_v405.json');rs=rd(W/'restart.json');plan=rd(W/'install_plan.json')
sub=rd(W/'receipts/v405-verify-submit.json')['task'];pins={Path(e['path']).name:e['sha256'] for e in sub['evidence']}
live=[]
for p in psutil.process_iter(['name']):
    try:
        if (p.info['name'] or '').lower()=='python.exe' and any(a and str(Path(a)).lower()==str(R/'iald_web_server.py').lower() for a in p.cmdline()[1:] if not a.startswith('-')):live.append(p)
    except (psutil.NoSuchProcess,psutil.AccessDenied,OSError):pass
same_live=(len(live)==1 and live[0].pid==v['web_pid']==rs['new_web_pid'] and live[0].create_time()==v['web_created'] and live[0].ppid()==v['supervisor_pid'])
allok=v['n']==v['ok'] and all(c['ok'] for c in v['checks']) and same_live
f=lambda t:datetime.datetime.fromtimestamp(t).strftime('%d/%m %H:%M:%S')
pk55=L['packages']['haiku55'];pk=L['packages']['haiku']
resp={
 'V1':{'ok':all(c['ok'] for c in (A,B,I,Q,M,G)),'checks':[c['n'] for c in (A,B,I,Q,M,G)],'resposta':(
  f"SIM. Os dois arquivos têm hoje exatamente o sha256 PINADO na missão (recibo v405-verify-submit, revisão {v['revision']}): INSTALLED_VERIFICATION.json {pins['INSTALLED_VERIFICATION.json']} e LOGIN_CHECK_v405.json {pins['LOGIN_CHECK_v405.json']}; nenhum foi regravado (sem .bak_). "
  f"INSTALLED_VERIFICATION.json bate campo a campo com o que MEUS carregadores mediram em processo novo, com audit hook (d2_out.json, {Q['achado']['loaders_medidos_em']}): status PASS; {iv['files_verified']} arquivos; identidade v405 (source {iv['identity']['source_sha256']}, cluster {iv['identity']['cluster_sha256'][:16]}…, núcleo {iv['identity']['operational_core_sha256'][:16]}…) = deployment_identity do plano; commit {iv['public_commit']} = manifesto = RELEASE; haiku55 {iv['packages']['haiku55']['permanent_tokens']} tokens/{iv['packages']['haiku55']['prefix_bytes']} B; haiku {iv['packages']['haiku']['permanent_tokens']}/{iv['packages']['haiku']['prefix_bytes']} B; native {iv['native_bytes']} B; prompt público {iv['public_prompt_bytes']} B; JEV {iv['JEV_release']} (jev_control_v405.json presente, sha {L['jev']['contract_file_sha256'][:16]}… = pino do manifesto; {L['kernel_sources']} fontes do kernel). "
  f"Não repeti os carregadores (ordem); como o arquivo foi gerado antes do claim, re-hasheei AGORA as entradas deles: os {len(plan['files'])} destinos = sha do plano, os 7 backups, os 171 arquivos de código do runtime (só o manifesto difere) e o manifesto ativo = manifest_install revisado; logo a medição de {Q['achado']['loaders_medidos_em']} ainda descreve os arquivos de hoje. "
  f"LOGIN_CHECK_v405.json: login_http_status {lc['login_http_status']} em {lc['em']}, depois da instalação e do restart e antes do claim; GET NOVO agora em http://127.0.0.1:8082/login = {v['login']} (igual).")},
 'V2':{'ok':all(c['ok'] for c in (T,S,K,P,X,SW,LG,WN)),'checks':[c['n'] for c in (T,S,K,P,X,SW,LG,WN)],'resposta':(
  "SIM, o escopo declarado é honesto, e ele é ESTREITO. Declarado nas duas evidências: carregadores em processo novo + hashes + login; sem resposta de modelo ao vivo (0 chamadas a provedor); sem inspeção física do celular. Nada nas evidências diz que houve resposta do app, atualização de memória ou distinção backend x build. "
  f"Precedente conferido: o critério de verify é o mesmo da v404 e lá foi aceito com o mesmo escopo declarado (revisão {P['achado']['v404_accept_revisao']} da missão da v404). "
  f"provider_calls=0 e science_executed=false são CONSTANTES literais de verify_installed.py (não instrumentadas); corroboro por: a mesma cadeia de carregadores no meu processo com audit hook não tentou rede/subprocesso/escrita (0 eventos bloqueados) e nenhum livro de gasto/job/carteira/reserva/cadastro foi escrito depois de 08:16:39 (wallet {LG['achado']['lojas'][0][1]}, jobs/gasto público/métricas 30/10 20:19, reservas 07/10 e 02/10, usuários 22/10). "
  "Os logs web não provam 'sem uso': meu GET /login e o da gerência não deixaram linha neles. O heartbeat local (nativa) gravou telemetria às 08:17:48, depois da verificação: não é resposta ao usuário nem chamada paga e não o inspecionei. "
  f"BACKEND x BUILD: nenhum dos {len(plan['files'])} destinos do plano é arquivo de cliente — extensões {X['achado']['extensoes_do_plano']}; raízes tocadas {X['achado']['raizes_de_R_tocadas_pelo_plano']}; nada sob iald-app, iald_web, static/templates/www/public/assets, nenhuma extensão de cliente; runtime_python_changes=0 e a varredura de todo R não achou mudança em iald-app. É mudança de backend compartilhado, sem necessidade de build de cliente; que web/iOS/Android compartilham esse backend é afirmação do coordenador, não verificada por mim. "
  "Ordem: as evidências foram feitas fora de ordem (08:16:39-40, antes do meu aceite do deploy e do claim do verify, 21-22 min), só leitura, e por isso as refiz. Varredura somente-stat de todo R: nenhum destino/backup tocado depois da minha revisão do deploy; só logs vivos mudaram.")},
 'V3':{'ok':all(c['ok'] for c in (LV,SC,AG,O)),'checks':[c['n'] for c in (LV,SC,AG,O)],'resposta':(
  f"SIM. Agora ({LV['achado']['agora']}): o filho web {v['web_pid']} é o único processo python.exe iald_web_server.py e o único ouvinte da 8082, ppid {v['supervisor_pid']}, supervisor com create_time idêntico ao de restart.json/maintenance.json ({LV['achado']['sup_created']}), start_iald_web.ps1 sem -NoSupervise, nenhum suspenso; create_time do filho idêntico ao que registrei na revisão do deploy ({f(v['web_created'])}, uptime {SC['achado']['uptime_min']} min): não reiniciou desde a instalação. O GET não alterou nada. Extra: nativa 8081 (pid {O['achado']['llama (nativa)']['pid']}) e Bancada Um 18777 (pid {O['achado']['Bancada Um']['pid']}) seguem escutando, criadas antes da janela.")}}
nao_cobre=[
 'RESPOSTA VIVA DO APP citando a v405 (0 chamadas a provedor): NÃO coberta. O critério da missão a cita; as evidências a excluem. Ainda não há uso efetivo medido: que o processo web tenha a v405 na memória é indireto (nasceu depois da instalação; o log de partida declara release=v405; carregadores de processo novo aceitam o instalado).',
 'MEMÓRIAS ATUALIZADAS COM RECIBOS: NÃO cobertas. Segundo o coordenador serão feitas depois do aceite; não verifiquei nenhum arquivo de memória nem recibo delas.',
 'DISTINÇÃO BACKEND x BUILD: não consta nas evidências submetidas. Confirmei de forma independente que nenhum destino do plano é arquivo de cliente e que nada em iald-app mudou; a topologia de backend compartilhado é afirmação do coordenador.',
 'INSPEÇÃO FÍSICA DO CELULAR / lojas: NÃO coberta (nenhuma build nova de cliente nesta release).',
 'Esta aceitação vale para o escopo DECLARADO (carregadores + hashes + login + processo vivo), como a da v404 (mesmo critério, mesmo escopo declarado); as partes do critério da missão listadas acima ficam com a gerência e não passam a ser lidas como verificadas por este parecer.']
ressalvas=[
 'PIDs e create_time são fotografia do momento da revisão; se o supervisor reiniciar o filho depois, os PIDs mudam sem invalidar a verificação.',
 'Os carregadores não foram repetidos (ordem do coordenador): reutilizei a medição de processo novo da revisão do deploy e re-hasheei as entradas agora. A folga/contagem de tokens segue recibo do construtor [DECLARADO].',
 'Os recibos de claim do deploy e do verify trazem uma nota herdada do pacote ("Parecer r1 do revisor independente recusou: a frase da capsula valia so pelo nome (F1)...") que não tem relação com estas tarefas: ruído de rastreabilidade (INFO), sem efeito.',
 'Fora de R só foi visto por stat o tglc_ledger.json (na revisão do deploy). A publicação remota do commit não foi verificada aqui (sem rede), como na revisão do deploy.',
 'Não inscrevi sessão ACOM própria; usei a referência da missão só via mission_step.py.']
body={'revisor':'sonnet-app-v405-revisor-d','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tarefa':'verify','unidade':'F9.APP_V405_20261102',
 'missao_revisao_na_revisao':v['revision'],'status':'PASS' if allok else 'FAIL','veredito':'PASS' if allok else 'FAIL',
 'escopo':("Revisão independente do passo `verify` da v405, pelo mesmo revisor que aceitou o deploy (sonnet-app-v405-revisor-d), distinto de quem submeteu (claude-gerencia-a7), do construtor e do revisor do pacote. ACEITA O QUE FOI DECLARADO: carregadores em processo novo + hashes + login + processo vivo. NÃO cobre: resposta viva do app citando a v405 (0 chamadas a provedor), memórias atualizadas com recibos, distinção backend x build nas evidências, inspeção física do celular. Somente leitura: psutil de consulta (nenhum processo tocado); varredura somente-stat de todo R ("+str(v['files_seen'])+" arquivos, nenhum aberto pela varredura); re-hash dos "+str(len(plan['files']))+" destinos, dos 7 backups e dos 171 arquivos de código; única rede = UM GET http://127.0.0.1:8082/login; carregadores NÃO repetidos (reuso de d2_out.json); nenhuma escrita em R; nenhuma chamada a provedor; sem um.py/Lean. Escrevi só em W\\review\\revisor_sonnet-app-v405-revisor-d\\ e W\\validation\\ (mais o accept da missão, por ordem)."),
 'leitura_para_o_operador':("O que esta revisão decide: os dois arquivos de evidência são os pinados na missão e dizem a verdade sobre o instalado (mesmos números que medi), o login responde 200 agora e o mesmo processo web segue de pé sob o mesmo supervisor. O que NÃO decide: se o app, de fato, responde citando a v405; se as memórias foram atualizadas; nada sobre o celular. Um negativo seria defeito medido da verificação (hash, número ou processo diferentes), não física; aceitar este passo não declara 'uso efetivo' verificado."),
 'respostas':resp,'nao_cobre':nao_cobre,'ressalvas':ressalvas,
 'n_checks':v['n'],'n_ok':v['ok'],'n_falha':v['n']-v['ok'],'checks':v['checks'],
 'processo_vivo_conferido_na_gravacao':{'pid':v['web_pid'],'mesmo_da_medicao':same_live},
 'evidencias_pinadas_na_missao':pins,
 'scripts_sha256':{n:sha(RV/n) for n in('v1_verify_review.py','v9_build_parecer.py','d2_loaders.py','d1_deploy_review.py')},
 'saidas_sha256':{n:sha(RV/n) for n in('v1_out.json','d2_out.json','d1_out.json')},
 'parecer_do_deploy_sha256':sha(W/'validation/review_deploy.json')}
out=json.dumps(body,ensure_ascii=False,indent=2).encode('utf-8')
dest=W/'validation'/('review_verify.json' if allok else 'review_verify_findings.json')
if dest.exists():raise SystemExit('refusing to overwrite existing '+str(dest))
tmp=dest.with_name(dest.name+'.tmp_'+str(os.getpid()))
with tmp.open('xb') as fh:fh.write(out);fh.flush();os.fsync(fh.fileno())
assert tmp.read_bytes()==out and len(out)>0
os.replace(tmp,dest)
print(json.dumps({'written':str(dest),'status':body['status'],'bytes':len(out),'sha256':sha(dest),'n_ok':body['n_ok'],'n_checks':body['n_checks'],'same_live':same_live}))
