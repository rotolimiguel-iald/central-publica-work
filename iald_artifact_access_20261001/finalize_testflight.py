from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
now=datetime.now(timezone.utc).isoformat();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
records=[]
def replace(p,new):
 old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(old);assert bak.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(new);assert tmp.read_bytes()==new and len(new)>0
 assert p.read_bytes()==old,'Concurrent modification: '+str(p)
 os.replace(tmp,p);assert p.read_bytes()==new
 records.append({'path':str(p),'backup':str(bak),'sha256':hashlib.sha256(new).hexdigest()})
def json_bytes(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
p=W/'ios_release.json';ios=json.loads(p.read_bytes());assert ios['build']==27
root='https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/apps/6760655636/testflight/'
ios.update({'cloud_status':'success','verified_at':now,'asc_build_id':'b25af76b-b88b-496e-afb4-d4a4a021f7df','internal':'Em testes','external':'Em testes','internal_url':root+'groups/0f9c8943-18f0-4f10-82ad-89a5832b9dec/builds','external_url':root+'groups/a2f7c246-06e1-4f7c-8fcd-d0c2a79cc345/builds','operator_membership_verified':True,'operator_installed_before_distribution':'4.1 (26)','internal_testers':1,'external_testers':6,'automatic_notify_checked':True,'expires_at':None,'expiry_display':'Expira em 90 dias','uploaded_display':'1 de out. de 2026 às 06:33','physical_installation_verified':False,'evidence_source':'Authenticated App Store Connect UI through CUA; both group rows showed Em testes after adding build27.'})
replace(p,json_bytes(ios))
p=W/'delivery.json';delivery=json.loads(p.read_bytes());delivery['ios']=ios;delivery['status']='WEB_LIVE_ANDROID_READY_IOS_BOTH_GROUPS_TESTING';delivery['ios_distribution_verified_at']=now
replace(p,json_bytes(delivery))
p=R/'iald_deadlines.json';deadlines=json.loads(p.read_bytes());prior=deadlines['items'].copy();deadlines['checked_at']=now
for key,group in [('testflight_internal','IALD Equipe'),('testflight_external','IALD Piloto')]:
 deadlines['items'][key]={'expires_at':None,'label':'IALD 4.1 (27) — '+group,'source':f'App Store Connect {now}: Em testes; Expira em 90 dias; data/hora exatas não exibidas.','build':'4.1 (27)','status':'Em testes'}
for key in prior:
 if not key.startswith('testflight_'):assert deadlines['items'][key]==prior[key]
replace(p,json_bytes(deadlines))
marker='IALD_ARTIFACT_BUILD27_DISTRIBUTED_20261001'
note=f'''

## 01/10/2026 — IALD4.1(27) liberada nos dois grupos do TestFlight
<!-- {marker} -->

[REAL — {now}] Após login do operador, conferido sucesso do Xcode Cloud8287fee6-8e45-405b-b3e8-df417fc63730 (commit preservado em ios_release.json). Build App Store Connect b25af76b-b88b-496e-afb4-d4a4a021f7df, versão4.1(27), adicionada ao IALD Piloto (6 testers) com orientações de teste de prévia/download e Notificar testers automaticamente marcado. Estado posterior Em testes. Adicionada também ao IALD Equipe (1 tester), estado posterior Em testes. Participação Luiz Antonio Rotoli Miguel confirmada; ficha mostrava instalação4.1(26) antes da liberação. Instalação27 em aparelho ainda não confirmada.

[DISPONIBILIDADE] Web ativa, iOS interno e externo27 disponíveis, Android4.1(24) APK assinado no canal autenticado; Google Play permanece cadastro/DUNS pendente. Convite existente https://testflight.apple.com/join/A5XEdy1H. Correção: prévia privada HTML, links antigos recuperáveis e renovação de acesso. Não é hospedagem pública. A verificação visual na conta web real continua pendente de login IALD; a fixture e os testes já foram verificados na entrega anterior. Zero novas chamadas de modelos ou mudanças de código nesta distribuição.

[PRAZOS] Painel interno iald_deadlines.json atualizado para27 em ambos os grupos. Apple exibiu Expira em90dias, sem data/hora exatas; expires_at permanece null, sem inferir vencimento. Nenhum alerta operacional foi acrescentado ao app de conversa. Push permanece desabilitado e depende das aprovações específicas Apple/Firebase já registradas; não confundir esta liberação com notificações prontas.

[EVIDÊNCIA] C:/IALD/Central de Patentes/work/iald_artifact_access_20261001/ios_release.json e delivery.json atualizados com backups imediatos de bytes; recibo distribution_memory_update.json. Este adendo resolve a pendência de distribuição Apple do registro anterior, preservado como história.
'''
paths=[R/'CLAUDE.md',Path(r'C:\IALD\Central de Patentes\work\iald_openai_motor_20260914\HANDOFF_RUNTIME.md'),R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
for p in paths:
 old=p.read_bytes()
 if marker.encode() in old:continue
 new=old+note.encode('utf-8');assert len(new)>len(old);replace(p,new)
(W/'distribution_memory_update.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps({'ios':'4.1 (27)','internal':'Em testes','external':'Em testes','backups_created':len(records),'physical_installation_verified':False}))
