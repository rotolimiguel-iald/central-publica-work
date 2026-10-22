from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
checks=json.loads((W/'checks.json').read_bytes());installed=json.loads((W/'installed.json').read_bytes())
assert checks['passed']
for row in installed['files']:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
commit=subprocess.check_output(['git','-C',str(R/'iald-app'),'rev-parse','HEAD']).decode().strip()
android=json.loads((W/'android_release.json').read_bytes());web=json.loads((W/'web_release.json').read_bytes())
ios={'version':'4.1','build':27,'source_commit':commit,'cloud_build_id':'8287fee6-8e45-405b-b3e8-df417fc63730','cloud_status':'pending','status_source':'GitHub commit status IALD | IALD','internal':'Pending Apple login and distribution verification','external':'Pending Apple login and distribution verification','prior_build':26,'invite':'https://testflight.apple.com/join/A5XEdy1H'}
(W/'ios_release.json').write_text(json.dumps(ios,indent=2),encoding='utf-8')
delivery={'utc':datetime.now(timezone.utc).isoformat(),'status':'WEB_LIVE_ANDROID_READY_IOS_BUILD_PENDING_LOGIN','web':web,'android':android,'ios':ios,'checks':checks,'installed':installed,'paid_provider_calls':0,'original_html_modified':False,'scientific_sources_modified':False,'public_hosting_created':False,'stable_url':'https://demo.iald.ia.br/app/index.html?artifact=db64f7c2-3f24-4d8f-8261-baae211d481c','limitations':['Production UI awaits login; synthetic fixture verified at desktop and393x852.','No physical iPhone/Android verification.','Play organization/DUNS pending.','Push remains disabled, separate prior approvals pending.'],'restart':{'previous_web_pid':74560,'new_web_pid':65868,'supervisor_pid':41020,'health':200,'active_jobs':0,'initial_review_rejection':'Substitute process guarantee missing','resolved_by':'Verified supervised restart loop and parent identity; added health check and recovery'}}
(W/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2),encoding='utf-8')
marker='IALD_PRIVATE_ARTIFACT_PREVIEW_20261001'
note=f'''

## 01/10/2026 — Prévia privada de sites e links recuperáveis
<!-- {marker} -->

[INPUT] Operador relatou que TGL_Pagina_de_Apresentacao.html não abria e mencionou a escolha MiMo pelo JEV. MiMo segue preferência econômica configurada para websites/artefatos; modelo e roteamento preservados, sem benchmark alegado.

[REAL] HTML original preservado: 9.229 bytes, SHA-256 {web['original_sha256']}. Causas: ticket expirado, link autenticado sem sessão no navegador externo e falta de prévia HTML. Novas rotas /api/task-artifacts/<id>/view, /access e /task-view/<id>/<ticket>. Propriedade verificada, renovação autenticada com JSON/Origin, ticket de15min. HTML revalidado pela allowlist e isolado em iframe sandbox vazio, sem scripts/formulários/rede. Download original intacto. Tokens mascarados nos logs e ausentes do histórico/localStorage.

[REAL] Cliente reconhece links antigos pelo UUID e abre modal com prévia/download/navegador; ticket antigo é descartado. Link estável /app/index.html?artifact=<UUID>; login preserva somente UUID validado em GET, consumido uma vez. Troca de conta/logout descartam respostas atrasadas. Markdown, streaming, fórmulas e fontes científicas preservados. CSS responsivo somente na cópia exibida. É prévia privada, não publicação de site público.

[REAL] 187 testes aprovados e1skip conhecido Windows; validações sintáticas e mobile aprovadas. Auditoria independente sem bloqueador demonstrado no escopo. Fixture via CUA exibiu o HTML real em desktop e393x852, modal e visualizador externo. Zero chamadas de modelos. Produção health200 e APIs novas401 sem login; original conferido. Reiniciado apenas filho web74560 sob supervisor41020; novo filho65868 saudável. Revisão automática recusou inicialmente reinício sem garantia de substituição; a ação foi aprovada após comprovar supervisor ativo e incluir verificação de saúde/recuperação.

[DISPONIBILIDADE] Web ativa; UI da conta real aguarda login do operador. Android4.1(24): APK assinado/AAB compilados, JS embarcado idêntico ao da web, canal autenticado https://demo.iald.ia.br/downloads/IALD-4.1-24.apk. Google Play permanece cadastro/DUNS pendente. iOS4.1(27): fontes enviadas ao repositório privado autorizado, commit {commit}; Xcode Cloud8287fee6-8e45-405b-b3e8-df417fc63730 pending no GitHub. Sessão Apple expirada; distribuição Equipe/Piloto NÃO confirmada, última entrega confirmada26. Instalação física não verificada.

[PENDÊNCIAS] Login IALD para validar o artefato na conta real; login Apple para conferir build27 e vincular ambos os grupos, verificar operador/convidados e registrar prazos somente na administração. Perguntas já abertas. Push continua desabilitado; conservar pendências Apple/Firebase de30/09 sem criar outro projeto/chave. Rebasear futuros patches para27/24, nunca regredir versões. Nenhuma alteração de kernel/gate/original científico.

[EVIDÊNCIA] C:/IALD/Central de Patentes/work/iald_artifact_access_20261001/delivery.json, checks.json, installed.json, web_release.json, android_release.json, ios_release.json, final_audit_result.json. Acesso: https://demo.iald.ia.br/app/index.html?artifact=db64f7c2-3f24-4d8f-8261-baae211d481c. Backups de bytes e escrita atômica; atualizar um/atualizar todos com pendências explícitas.
'''
paths=[R/'CLAUDE.md',Path(r'C:\IALD\Central de Patentes\work\iald_openai_motor_20260914\HANDOFF_RUNTIME.md'),R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
rows=[];stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for p in paths:
 before=p.read_bytes()
 if marker.encode() in before:continue
 b=p.with_name(p.name+'.bak_'+stamp);b.write_bytes(before);assert b.read_bytes()==before
 after=before+note.encode('utf-8');t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(after)
 assert t.read_bytes()==after and len(after)>len(before);assert p.read_bytes()==before
 os.replace(t,p);assert p.read_bytes()==after
 rows.append({'path':str(p),'backup':str(b),'sha256':hashlib.sha256(after).hexdigest()})
(W/'memory_update.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps({'memories_updated':len(rows),'tests_passed':187,'web':'live','android':'4.1(24)','ios':'4.1(27) pending'}))
