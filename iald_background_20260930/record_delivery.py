"""Record measured delivery and append app memories with immediate byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
checks=json.loads((W/'checks.json').read_bytes())
installed=json.loads((W/'installed_web.json').read_bytes())
assert checks['passed']
for item in installed['files']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
ios=json.loads((W/'ios_release.json').read_bytes())
android=json.loads((W/'android_release.json').read_bytes())
commit=subprocess.check_output(['git','-C',str(ROOT/'iald-app'),'rev-parse','HEAD']).decode().strip()
delivery={
 'utc':datetime.now(timezone.utc).isoformat(),'status':'CONTINUITY_RELEASED_PUSH_PENDING',
 'scope':'Durable server generation, authenticated replay, explicit cancellation; native push not activated',
 'checks':checks,'tests_passed':141,'installed':installed,'commit':commit,
 'ui_verification':{'fixture_provider_calls':2,'reloaded_during_generation':True,
    'answer_recovered_once':True,'explicit_cancel_persisted':True,'katex_formula':'2+2=4',
    'katex_errors':0,'production_conversations_preserved':10,'production_current_messages_preserved':4},
 'restart':{'previous_web_pid':100792,'supervisor_pid':41020,'web_health':200,
    'unauthenticated_new_routes':401,'unauthenticated_assets':'302 /login'},
 'availability':{'web':'LIVE','ios_internal':ios['internal'],'ios_external':ios['external'],
    'android':android,'google_play':'Existing organization/DUNS setup pending'},
 'push':{'ios':False,'android':False,'cloud_project':'iald-app-notificacoes',
    'cloud_project_number':'288651677723','firebase_terms':'Accepted under explicit authorization',
    'firebase_activation':'Pending explicit approval after irreversible IAM/billing linkage warning',
    'apple_capability':'Pending explicit approval after profile invalidation warning',
    'credentials':'No APNs or FCM sender credentials created or stored',
    'staging':'notifications/; native-dependencies/; mobile-review/ (debug build passed)',
    'future_rebase':'Native patch baselines used iOS25/Android22; rebase onto26/23 before installing, never downgrade'},
 'limitations':['No physical phone background/notification test yet.',
    'Server restart interrupts an in-flight model call; never automatically repeats paid generation.',
    'Push callback is not a transactional outbox; provider delivery is not guaranteed.',
    'Public privacy page iald.ia.br/privacidade.html still has old March2026 text; app now displays new retention behavior.',
    'Notification logout requires successful revocation before clearing bearer; failure is visible.'],
 'paid_provider_tests':0,'scientific_sources_modified':False,
 'evidence':['checks.json','installed_web.json','mobile_assets_sync.json','android_release.json','ios_release.json',
    'notifications/validation.json','android-release23.log','mobile-review/android-build.log']}
(W/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2),encoding='utf-8')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
marker='IALD_DURABLE_RESPONSES_20260930'
note=f'''

## 30/09/2026 — Respostas continuam no servidor; avisos nativos pendentes
<!-- {marker} -->

[INPUT] Operador pediu continuar a geração ao trocar de app e avisar quando a resposta estiver pronta. Autorizou projeto IALD App Notificacoes e termos Firebase, sem serviços pagos.

[REAL] Web/servidor implantados: jobs idempotentes por UUID, execução desacoplada da conexão, eventos cifrados por DPAPI do usuário Windows, recuperação autenticada por conta, histórico deduplicado e cancelamento apenas explícito. Respostas disponíveis por até sete dias; expiração retorna 410 terminal. Apagar conversa limpa eventos; excluir conta purga dados. Reinício do servidor marca geração inconclusa interrompida, sem repetir chamada paga. Histórico local recebe escopo derivado da conta/data de criação. Mantidos modelos, consentimentos, limites, fórmulas e selo; nenhum original científico ou gate alterado.

[REAL] 141 testes locais aprovados. Teste UI simulado: reload durante geração recuperou uma resposta com somente uma chamada; segundo teste cancelou explicitamente. KaTeX 2+2=4 sem erro. Produção reaberta preservou dez conversas e quatro mensagens na conversa ativa. Rotas novas recusam anônimos (401). Reiniciado somente filho web anterior100792; supervisor41020 preservado. Sem novas chamadas pagas.

[REAL] Notificações preparadas, DESABILITADAS: APNs/FCM com alerta genérico, sem texto das conversas; tokens DPAPI; consentimento e vinculação por sessão; revogação após saída/troca de senha/expiração. Dependências HTTP2 isoladas, sem upgrade global. Push não é garantia de entrega nem mantém WebView executando. Falha de push não perde resposta. Publicação da continuidade usa plugins/capabilities anteriores.

[DISPONIBILIDADE] Web ativa. iOS4.1(26): interno={ios['internal']}; externo={ios['external']}. Android4.1(23) APK assinado e AAB prontos; APK no canal autenticado https://demo.iald.ia.br/downloads/IALD-4.1-23.apk. Play continua cadastro/DUNS pendente. Commit privado lido: {commit}. Não foi confirmada instalação física.

[PENDÊNCIAS] Revisão automática exigiu autorizações específicas: habilitar PushNotifications Apple br.ia.IALD invalida perfis; ativar Firebase no projeto já criado iald-app-notificacoes (288651677723) é vínculo irreversível com IAM/faturamento. Perguntas já feitas; não presumir resposta. Não criar outro projeto. Sem credenciais APNs/FCM criadas. Depois das aprovações: concluir console, provisionar credenciais restritas no cofre, rebasear patches nativos de25/22 para26/23, compilar nova versão e validar nos aparelhos/grupos. Não aplicar patch antigo que retroceda versão. Política pública antiga ainda requer atualização; a interface mostra a nova retenção.

[EVIDÊNCIA] C:/IALD/Central de Patentes/work/iald_background_20260930/delivery.json; checks.json; notificações e patches em notifications/. Backups imediatos de bytes e escrita atômica. Regra atualizar um/atualizar todos mantida com pendências explícitas.
'''
paths=[ROOT/'CLAUDE.md',
 Path(r'C:\IALD\Central de Patentes\work\iald_openai_motor_20260914\HANDOFF_RUNTIME.md'),
 ROOT/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',
 Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
 Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),
 Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),
 Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
records=[]
for p in paths:
    before=p.read_bytes()
    if marker.encode() in before:continue
    backup=p.with_name(p.name+'.bak_'+stamp);backup.write_bytes(before)
    assert backup.read_bytes()==before
    after=before+note.encode('utf-8');temporary=p.with_name(p.name+'.tmp_'+stamp)
    temporary.write_bytes(after);assert temporary.read_bytes()==after and len(after)>len(before)
    assert p.read_bytes()==before,'Concurrent memory change; preserve both versions'
    os.replace(temporary,p);assert p.read_bytes()==after
    records.append({'path':str(p),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
(W/'memory_update.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps({'memories_updated':len(records),'tests_passed':141,'ios':ios,'android':'4.1 (23)','push':False}))
