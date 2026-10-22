from datetime import datetime
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
path = WORK/'explicit_approval.json'
before = path.read_bytes()
record = json.loads(before)
record['previous_interpretation_rejected_by_automatic_review'] = {
    'user_reply_verbatim':record['user_reply_verbatim'],
    'reason':'A resposta anterior não comprovou autorização explícita e inequívoca para o payload e destino específicos.',
    'api_call_executed':False,
}
record['at'] = datetime.now().astimezone().isoformat()
record['user_reply_verbatim'] = 'Sim, autorizo esses arquivos para api.openai.com e o teste'
record['preceding_request'] = 'Você autoriza especificamente enviar o conteúdo integral de IALD_Kernel_v5.txt e IALD_TGL_MEMORY_CORE_v1_20260915.md para api.openai.com, usá-los no app e gastar até US$ 0,03 no teste?'
record['interpretation'] = 'Resposta afirmativa expressa à pergunta que nomeia arquivos, destino, uso no app e teto do teste.'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
with path.with_name(path.name+'.bak_'+stamp).open('xb') as handle:
    handle.write(before)
data = json.dumps(record,ensure_ascii=False,indent=2).encode()
temp = path.with_name(path.name+'.tmp_'+stamp)
with temp.open('xb') as handle:
    handle.write(data)
assert temp.read_bytes() == data and path.read_bytes() == before
temp.replace(path)
print('Specific affirmative approval recorded; previous rejected interpretation preserved.')
