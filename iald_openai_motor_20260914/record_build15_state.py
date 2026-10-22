from datetime import datetime
from pathlib import Path
import json
import os
import tempfile

WORK=Path(__file__).parent
SOURCE=Path(r'C:\IALD\projetos_pyhton\IALD')
now=datetime.now().astimezone()
stamp=now.strftime('%Y%m%d_%H%M%S')
pub=json.loads((WORK/'mobile15_publication.json').read_bytes())
android=json.loads((WORK/'android15_verification.json').read_bytes())
delivery=json.loads((WORK/'android15_delivery.json').read_bytes())
ios=json.loads((WORK/'ios15_compile/verification.json').read_bytes())
assert ios['conclusion']=='success' and ios['headSha']==pub['commit']
entry=f'''

### {now.strftime('%d/%m/%Y %H:%M %z')} — Build 15 incorpora a interface paralela; aguardando Apple e publicação da política

[REAL] Depois da build 14, chegaram novas alterações paralelas na interface: painel de consumo por plano, tratamento de avisos/cotas, denúncia de respostas e ícones β_TGL. Conteúdo preservado e incorporado à build **4.1 (15)**. Node validou a sintaxe, validação de release passou, recursos web/iOS/Android coincidem, 173 arquivos auditados sem caminhos excluídos nem padrões de credenciais. Push no repositório privado confirmado em `{pub['commit']}`; branch `codex/mobile-release`.

[REAL] Corrigida a lista explícita de arquivos do servidor para incluir somente `app/img/betatgl.png` e `app/img/betatgl.ico`, com backup. Teste de recursos e proteção de arquivos: **53 OK / 0 falhas**. A lista não se tornou genérica. Durante a retomada identificaram-se duas instâncias do servidor web. A antiga PID 78304 (início 17:29:53; parent 45992) foi encerrada após conferir sua identidade. **Instância atual: PID 17604**, iniciada 18:04:18, 127.0.0.1:8082; HTTP health 200. Native llama **PID 65624, porta 8081**, preservado. Não inferir supervisão pelo parent 45992: sua linha de comando não demonstrou loop. Não lançar outra instância sem conferir os processos e a porta. `restart_web*.ps1` são recibos/procedimentos históricos de PIDs anteriores; não reaplicar cegamente.

[REAL] Android `assembleRelease` e `bundleRelease` concluídos; APK v2 e AAB verificados, versionCode 15. APK: {delivery['url']} (download autenticado; anônimo recebe redirecionamento ao login). Arquivos preservados em `work/iald_openai_motor_20260914/artifacts/`. Hashes lidos: APK `{android['files'][0]['sha256']}`, AAB `{android['files'][1]['sha256']}`. Instalação em aparelho e Google Play ainda não verificadas.

[REAL] iOS também compilou: run {ios['databaseId']}, `ARCHIVE SUCCEEDED`, escopo **sem assinatura**. Log SHA-256 `{ios['log_sha256']}`; recibos em `ios15_compile/`. URL: {ios['url']}. Isso não confirma build 15 disponível no TestFlight. Ao retornar ao App Store Connect, conferir a compilação/distribuição da revisão mais nova, em vez de presumir que o número do Xcode Cloud coincide com o versionCode Android.

[OPEN — impedimentos restantes] Apple continua exigindo a entrada do operador pelo iPhone; pedido já enviado. Painel de publicação de `iald.ia.br` ainda não identificado; política publicada antiga contradiz o compartilhamento OpenAI. Minuta `privacy_draft.html` preparada, não publicada, incluindo pendência de retenção. Motor padrão permanece nativo até concluir a distribuição compatível e a política; integração OpenAI por conta/plano gratuito foi testada em HTTPS. Não gerar outras chaves, repetir builds prontas nem alterar as permissões da chave existente. A dependência de autenticação Apple já persistiu por três rodadas consecutivas; as melhorias independentes desta etapa foram concluídas. O objetivo inteiro ainda não está cumprido.
'''
checks=[
    {'requirement':'Motor OpenAI real com consentimento e revogação','state':'PROVEN_IN_CONTROLLED_PRODUCTION_TEST','evidence':'production_verification_20260914_173137_utf8.json'},
    {'requirement':'Núcleo TGL permanente, kernel inteiro consultável e índice público','state':'IMPLEMENTED_AND_TESTED','evidence':['installation_20260914_172801.json','behavior_evaluation_20260914_172652.json','behavior_evaluation_20260914_173957.json']},
    {'requirement':'Modelo nativo preservado para o operador','state':'RUNNING_8081','evidence':'PID 65624 measured this turn'},
    {'requirement':'Pacote Android atualizado','state':'BUILT_SIGNED_AND_DELIVERED','evidence':['android15_verification.json','android15_delivery.json']},
    {'requirement':'App iOS atualizado instalado/distribuído','state':'INCOMPLETE_APPLE_AUTHENTICATION_REQUIRED','evidence':'ios15_compile/verification.json proves unsigned compilation only'},
    {'requirement':'Política pública compatível com OpenAI','state':'INCOMPLETE_HOSTING_ACCESS_AND_RETENTION_DETAILS_REQUIRED','evidence':['privacy_public_current.html','privacy_draft.html']},
    {'requirement':'OpenAI padrão para demais contas','state':'INCOMPLETE_PENDING_COMPATIBLE_DISTRIBUTION_AND_POLICY','evidence':'Installed configuration retains nativa default; per-account/free OpenAI works'},
    {'requirement':'Distribuição pelo Google Play','state':'INCOMPLETE_ORGANIZATION_DUNS','evidence':'Existing signup handoff; APK delivery is not store publication'}]
(WORK/'completion_audit_pending.json').write_bytes(json.dumps({'checked_at':now.isoformat(),'complete':False,'checks':checks},ensure_ascii=False,indent=2).encode())
paths=[Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),SOURCE/'CLAUDE.md',SOURCE/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',WORK/'HANDOFF_RUNTIME.md',Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
for p in paths:
    old=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+stamp)
    backup.write_bytes(old)
    assert backup.read_bytes()==old
    addition=entry
    if p.name=='MEMORY.md':
        addition=(f'\n\n[{now.strftime("%d/%m/%Y %H:%M %z")} — REAL] Build 15 incorpora a interface paralela (uso, denúncia, β_TGL): '
            '173 arquivos auditados, 53 testes de assets passaram, Android assinado/disponível, iOS archive sem assinatura passou. '
            'Web ativo PID 17604, nativo PID 65624; instância web duplicada antiga removida. '
            'Apple ainda pede login; política pública aguarda painel/retencão. Objetivo incompleto. '
            'Retomar por `C:/IALD/Central de Patentes/work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md`.\n')
    data=old+addition.encode('utf-8')
    fd,name=tempfile.mkstemp(prefix='.'+p.name+'.',dir=p.parent)
    os.close(fd)
    temp=Path(name)
    temp.write_bytes(data)
    assert temp.read_bytes()==data and len(data)>len(old) and p.read_bytes()==old
    os.replace(temp,p)
    assert p.read_bytes()==data
print('BUILD_15_AND_COMPLETION_GAPS_RECORDED_WITH_BYTE_BACKUPS')
