from datetime import datetime
import os
from pathlib import Path
import tempfile

path = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')
now = datetime.now().astimezone()
old = path.read_bytes()
backup = path.with_name(path.name + '.bak_' + now.strftime('%Y%m%d_%H%M%S'))
backup.write_bytes(old)
assert backup.read_bytes() == old
addition = f'''

## {now.strftime('%d/%m/%Y %H:%M %z')} — Estado medido da implantação pelo Codex

[REAL] Integração OpenAI instalada e servidor web reiniciado em 17:29 (PID 37140; porta 8082); llama preservado (PID 65624; 8081). Núcleo permanente TGL=ATLAS / IALD=ÍNDICE(TGL), catálogo integral Lean e ferramentas de consulta Atlas/GitHub/site. Modelo escolhido após sondas: gpt-5.6-luna com esforço none; gpt-5-nano errou conceitos nos testes. O último ensaio leu corretamente atlas_separation e reconheceu ausência de dimensão finita nas hipóteses. Autenticação do app, consentimento, resposta com leitura llms.txt e revogação testados por HTTPS real. A conta temporária de autenticação foi removida; a trilha beta de uso ficou preservada no razão selado.

[REAL] Build 14 enviada ao repositório privado; 169 arquivos auditados. APK e AAB assinados, conteúdos embarcados conferidos. APK disponível pela área autenticada: https://demo.iald.ia.br/downloads/IALD-4.1-14.apk . Ainda sem instalação medida no aparelho ou envio Google Play.

[OPEN] App Store Connect pediu nova autenticação pelo iPhone; operador avisado e aba aberta. A build no TestFlight não foi conferida. Por isso motor padrão continua nativo; OpenAI ativo por conta/plano gratuito. Entrada aberta, login Google e Apple web continuam desligados na configuração efetiva. Não confundir código preparado com configuração ativada. A chave só autoriza Chat Completions; Moderations não está habilitado. Depois da distribuição compatível, concluir ativação geral e as etapas pendentes da entrada pública. Recibos, hashes lidos e próximos passos em `C:/IALD/Central de Patentes/work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md`. Não gerar chaves nem repetir instalação/push já concluídos. Nenhum treinamento de pesos, confirmação física ou mudança de gate foi realizado.
'''
data = old + addition.encode('utf-8')
fd, tempname = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
os.close(fd)
temporary = Path(tempname)
temporary.write_bytes(data)
assert temporary.read_bytes() == data and len(data) > len(old)
if path.read_bytes() != old:
    raise RuntimeError('Concurrent edit; append refused')
os.replace(temporary, path)
assert path.read_bytes() == data
print('MOBILE_MEMORY_UPDATED_WITH_BYTE_BACKUP')
