from datetime import datetime
from pathlib import Path
import tempfile
import os
import json

WORK=Path(__file__).parent
SOURCE=Path(r'C:\IALD\projetos_pyhton\IALD')
now=datetime.now().astimezone()
stamp=now.strftime('%Y%m%d_%H%M%S')
entry=f'''

### {now.strftime('%d/%m/%Y %H:%M %z')} — Errata operacional ao lado: instância final e dependências do objetivo

[REAL] A instância web PID 78304, encerrada na etapa anterior, foi substituída por outro filho do lançador PowerShell 45992: **PID 23260, início 18:08:09**, carregando o código já atualizado. A instância que o Codex havia criado, PID 17604, foi então encerrada para preservar a inicialização existente e remover a duplicidade. Conferência final: **somente PID 23260 corresponde ao servidor web**, ouvindo 127.0.0.1:8082; saúde pública HTTP 200. Modelo nativo continua PID 65624, porta 8081. Isso supersede o PID 17604 registrado acima. O mecanismo interno do lançador não foi auditado integralmente; observar a recriação do filho não autoriza alterar ou encerrar o lançador. Em retomadas, conferir os processos antes de iniciar qualquer instância manual.

[OPEN] Objetivo marcado como aguardando participação do operador (blocked), sem declaração de conclusão: login Apple ainda na tela de autenticação pela terceira rodada consecutiva; painel de publicação da política ainda desconhecido. Builds 15 Android/iOS verificadas no escopo dos recibos, APK disponível, interface sincronizada, núcleo/Atlas/kernel/fontes públicas implantados. Faltam distribuição TestFlight, atualização efetiva da política e ativação geral do motor OpenAI. Não repetir geração de chaves, builds ou testes pagos já concluídos. Retomar com a entrada Apple e a informação do painel do site.
'''
paths=[Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md'),SOURCE/'CLAUDE.md',SOURCE/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',WORK/'HANDOFF_RUNTIME.md',Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
for p in paths:
    old=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+stamp)
    backup.write_bytes(old)
    assert backup.read_bytes()==old
    addition=entry if p.name!='MEMORY.md' else (f'\n\n[{now.strftime("%d/%m/%Y %H:%M %z")} — ERRATA REAL] '
        'Web final PID 23260 (filho do lançador 45992), porta 8082, único após retirar a instância manual 17604. '
        'Nativo PID 65624 preservado. Objetivo aguardando login Apple/painel do site; build 15 pronta. '
        'Detalhes no HANDOFF_RUNTIME.md de work/iald_openai_motor_20260914.\n')
    data=old+addition.encode('utf-8')
    fd,tempname=tempfile.mkstemp(prefix='.'+p.name+'.',dir=p.parent)
    os.close(fd)
    temporary=Path(tempname)
    temporary.write_bytes(data)
    assert temporary.read_bytes()==data and len(data)>len(old) and p.read_bytes()==old
    os.replace(temporary,p)
    assert p.read_bytes()==data
state={'recorded_at':now.isoformat(),'web_pid':23260,'native_pid':65624,'web_parent_pid':45992,
       'web_health_status':200,'goal_complete':False,'waiting_for':['Apple login','Website publishing access and privacy retention details']}
(WORK/'final_runtime_state.json').write_bytes(json.dumps(state,indent=2).encode())
print('FINAL_SINGLE_WEB_INSTANCE_AND_WAITING_STATE_RECORDED')
