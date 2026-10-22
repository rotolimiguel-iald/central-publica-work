from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
from record import record

WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
read=lambda name:json.loads((WORK/name).read_text(encoding='utf-8'))
runtime=read('runtime_verification.json')
suite=read('suite_gate.json')
publication=read('mobile16_publication.json')
android=read('android16_delivery.json')
assert suite['passed'] and suite['new_failures']==0
assert publication['status']=='PUSH_VERIFIED' and publication['private']
assert android['status']=='DELIVERED_AUTHENTICATED'
for name,digest in runtime['hashes'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, 'Concurrent source update: '+name
for asset in ['iald.js','iald.css']:
    blobs=[(folder/asset).read_bytes() for folder in [ROOT/'app',ROOT/'iald-app/www',ROOT/'iald-app/ios/App/App/public',ROOT/'iald-app/android/app/src/main/assets/public']]
    assert len(set(blobs))==1, 'Different assets: '+asset
health={}
with urllib.request.urlopen('http://localhost:8082/health',timeout=20) as response:
    health['http://localhost:8082/health']=response.status
    assert response.status==200
public_check=subprocess.run(['powershell.exe','-NoProfile','-Command',
    "$ErrorActionPreference='Stop'; $r=Invoke-WebRequest -UseBasicParsing -Uri 'https://demo.iald.ia.br/health' -TimeoutSec 20; [pscustomobject]@{status=[int]$r.StatusCode;content=$r.Content}|ConvertTo-Json -Compress"],
    check=True,capture_output=True,text=True)
public_value=json.loads(public_check.stdout)
assert public_value['status']==200 and json.loads(public_value['content'])['status']=='ok'
health['https://demo.iald.ia.br/health']=public_value['status']
proc=subprocess.run(['powershell.exe','-NoProfile','-Command',
    'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in 34128,75576 } | Select-Object ProcessId,ParentProcessId,Name | ConvertTo-Json -Compress'],
    check=True,capture_output=True,text=True)
processes=json.loads(proc.stdout)
assert {p['ProcessId'] for p in processes}=={34128,75576}
apple={'status':'IN_TESTING','version':'4.1','build':16,
    'cloud_build_id':'54dc3b1b-ff96-4b18-ae12-65057d946e30','cloud_status':'SUCCESS',
    'cloud_commit_verified':publication['commit'],
    'testflight_build_id':'e17eb4d3-241d-428c-8b8e-30498797dadf',
    'url':'https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/apps/6760655636/testflight/ios/e17eb4d3-241d-428c-8b8e-30498797dadf',
    'group':'IALD Equipe','group_kind':'internal','testers':1,'group_builds':[16,14,13],
    'whats_new_saved':True,'saved_ui':'Salvo','verified_by':'App Store Connect visible UI',
    'device_installation':'NOT_VERIFIED'}
requirements={
    'T1_two_models':{'status':'COMPLETE','options':['nativa','openai'],'admin_and_expanded_options':2,'standard_options':0,
        'response_model_server_sse':True,'history_switch_and_reload':'verified real browser conversation with both providers',
        'panel_daily_costs':'actual route and mtLoad tested in isolation; SQLite read-only live spending snapshot recorded'},
    'T2_sol':{'status':'CANCELLED_BY_OPERATOR'},
    'T3_owner_and_quotas':{'status':'COMPLETE','rule':'owner shares US$3 global daily cap; no individual cap',
        'exact_numeric_env_verified':True,'spending_snapshot':'runtime_verification.json'},
    'T4_mobile':{'status':'COMPLETE','android':'authenticated APK published; AAB signed','ios':apple},
    'T5_validation':{'status':'COMPLETE','suite':'24 green, same 9 old red, no new failures','new_python_tests':6,
        'new_javascript_checks':8,'admin_route_and_dom_test':'passed','health':health,'processes':processes}}
note=(
    '[REAL] Concluída a ordem corrigida (errata SEM O SOL). Permanecem somente IALD Nativa e ChatGPT 5.6 Luna. '
    'Rótulo por resposta vem do servidor no SSE e persiste no histórico. Verificação real no app: resposta da Luna, troca para Nativa na mesma conversa, resposta nativa, recarga e ambos os rótulos preservados; seleção de luiz restaurada para OpenAI. '
    'Gasto diário por modelo acrescentado ao painel; rota, autorização, falha visível e renderização mtLoad verificadas isoladamente. Painel de produção é local e o navegador local pediu login; não foi forjada autenticação nem conferida visualmente sua tela administrativa. O razão real foi consultado somente para totais, registrados no recibo de runtime.\n\n'
    '[REAL] luiz mantém somente_limite_global=true, sem cota individual, compartilhando o teto global de US$3/dia com os demais. As oito cotas numéricas da errata conferem com o .env; nenhum outro campo alterado. UI autenticada mostrou explicitamente Sem limite individual e global US$3. Gastos por conta/modelo do primeiro dia estão no runtime_verification.json (US$ estimado local incluindo reservas, não saldo oficial da OpenAI).\n\n'
    '[REAL] Suíte sob guarda concluída: 24 verdes, exatamente os nove vermelhos antigos com resultados preservados, zero novos. Seis testes Python e oito verificações JS novos passaram; teste adicional do painel passou. Regressão transitória de yield no SSE corrigida antes da ativação; metadados unidos ao primeiro chunk original preservam cancelamento do provedor. Somente filho web reiniciado (novo PID75576), supervisor47020 e llama34128 preservados. Health local e público 200.\n\n'
    '[REAL] Android4.1(16): APK e AAB assinados com chave existente; certificado confere diretamente com14/15, assets íntegros, sem backups nos pacotes. APK em https://demo.iald.ia.br/downloads/IALD-4.1-16.apk, exige login. Push dos arquivos auditados somente ao repositório privado autorizado, branch codex/mobile-release. Xcode Cloud16 concluiu com sucesso no commit lido em mobile16_publication.json; TestFlight4.1(16) adicionado ao grupo interno IALD Equipe, 1 tester, agora 3 compilações(16/14/13). Notas O que testar salvas, estado Salvo conferido na UI.\n\n'
    '[OPEN] Instalação física no iPhone/iPad/Android não observada. Google Play depende do cadastro/D-U-N-S; entrega Android desta T4 é APK autenticado. Compatibilidade entre cota gratuita e núcleo integral continua pendente conforme a ordem, sem alterar núcleo/proteções do gratuito. Sol cancelado; Kimi depende de instalação e ordem futura. Nenhuma compra, recarga, chave nova, alteração de limite no painel OpenAI ou mudança de gate físico/formal.'
)
record('completed','Dois modelos ativos, operador com limite global e build 16 entregue',note,
    {'status':'COMPLETED_CORRECTED_ORDER','goal_complete':True,'requirements':requirements,
     'health':health,'processes':processes,'testflight':apple,
     'health_client_note':'Cloudflare rejected urllib with 403/1010; standard Windows HTTP client returned 200 and status ok, without changing any protections.',
     'evidence_files':['runtime_verification.json','suite_gate.json','android16_verification.json','android16_delivery.json','mobile16_publication.json','verify_admin_panel_v2.mjs']})
