import json,hashlib,datetime
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');RV=W/'review/revisor_sonnet-app-v404-revisor'
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d1=json.loads((RV/'d1_out.json').read_bytes());assert d1['n']==d1['ok']==30 and d1['login']==200
out={'revisor':'sonnet-app-v404-revisor','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'escopo':'Revisao independente do DEPLOY da v404 (r2). Somente leitura: psutil de consulta (nenhum processo tocado), varredura somente-stat da arvore de runtime (82.554 arquivos vistos, nenhum aberto; .env e .iald_secret_key inclusive), hash dos bytes dos destinos do plano; unica rede = GET http://127.0.0.1:8082/login; loaders do runtime importados em processo novo com audit hook (sem rede/subprocesso/escrita/segredos). Os PIDs 41280/69428/38024 vieram do pedido da gerencia e dos recibos; o esperado foi comparado com o que o sistema mostra agora.',
 'script_revisor_sha256':sh(RV/'d1_deploy_review.py'),'auxiliares_sha256':{'d2_loaders.py':sh(RV/'d2_loaders.py'),'d2_out.json':sh(RV/'d2_out.json'),'d1_out.json':sh(RV/'d1_out.json')},
 'veredito':'PASS','n_checks':d1['n'],'n_ok':d1['ok'],'n_falha':d1['n']-d1['ok'],'checks':d1['checks'],
 'ressalvas':['Que o processo web em execucao carregou a v404 na MEMORIA nao e observavel por GET /login (200 nao autentica nem mostra a release): prova-se que o filho (69428) nasceu 5,1 s DEPOIS da instalacao, que os arquivos em disco = plano e que os loaders de processo novo aceitam o instalado. O uso efetivo (resposta do app citando a v404) esta fora do escopo declarado do `verify`, como na v402.',
  'bench/llama intocados: verificado so para os servicos que ESCUTAM agora (llama 8081 pid 58196 e Bancada Um 18777 pid 44228, ambos criados em 28/10, antes da janela). As portas 18765/18766 (gw/cosmologia) nao escutam agora; a revisao nao tem como saber se escutavam antes. O recibo da gerencia (restart_scope, bench_restarted=false) e DECLARADO.',
  'PIDs e create_time sao fotografia do momento da revisao; se o supervisor reiniciar o filho depois, os PIDs mudam sem invalidar o deploy.',
  'Os logs vivos da varredura (web-server_*.log e .err, web-supervisor.log, gpu csv, iald_heartbeat_telemetry.jsonl) mudam por serem logs do proprio servidor que reiniciou; nao sao arquivos da release.',
  'iald_stack_v7.py (confidencial) esta na raiz e fora do RUNTIME_BASELINE por desenho: so stat (mtime/ctime de 09/03/2026, anteriores a janela), nunca aberto.',
  'Este revisor NAO aprova o verify; a missao mostra verify needs_revalidation ate a gerencia reclama-lo e submete-lo.']}
with (W/'validation/review_deploy.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(sh(W/'validation/review_deploy.json')[:16])
