import json,hashlib,datetime
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');RV=W/'review/revisor_sonnet-app-v404-revisor'
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
v=json.loads((RV/'v1_out.json').read_bytes());assert v['n']==v['ok']==14 and v['login']==200
out={'revisor':'sonnet-app-v404-revisor','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'escopo':'Revisao independente do passo `verify` da v404. ACEITA O QUE FOI DECLARADO: carregadores em processo novo + hashes + login + processo vivo. NAO cobre: resposta viva do app citando a v404 (0 chamadas a provedor), memorias atualizadas com recibos, distincao backend x build, inspecao fisica do celular. Somente leitura; unica rede = GET local /login; nenhum processo tocado.',
 'script_revisor_sha256':sh(RV/'v1_verify_review.py'),'auxiliares_sha256':{'d2_loaders.py':sh(RV/'d2_loaders.py'),'v1_out.json':sh(RV/'v1_out.json'),'d1_out.json':sh(RV/'d1_out.json')},
 'veredito':'PASS','n_checks':v['n'],'n_ok':v['ok'],'n_falha':v['n']-v['ok'],'checks':v['checks'],
 'ressalvas':['O criterio da missao cita "resposta do app citando a v404", memorias com recibos e a distincao backend x build; esta aceitacao NAO os cobre (a submissao os exclui, como a v401/v402 aceitas). Ficam com a gerencia.',
  'Que o processo em execucao tem a v404 na MEMORIA continua inobservavel por GET /login; prova-se: filho 69428 nascido 5,1 s depois da instalacao, arquivos = plano, loaders de processo novo aceitam o instalado.',
  'PIDs/create_time sao fotografia do momento da revisao.',
  'Na r2 a janela do MiMo ficou em 96.974 B e a do Kimi em 100.346 B (ressalva registrada na revisao do pacote); isso e capacidade de historico por conversa, nao algo que o verify declarado meca.']}
with (W/'validation/review_verify.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(sh(W/'validation/review_verify.json')[:16])
