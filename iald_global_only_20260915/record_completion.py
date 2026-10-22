from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import urllib.request

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('record_paths', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)
receipt = WORK / 'completion.json'
assert not receipt.exists()
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
with urllib.request.urlopen('http://127.0.0.1:8082/health', timeout=8) as response:
    assert response.status == 200
users = json.loads((ROOT / 'iald_users.json').read_bytes())
assert users['luiz'].get('admin') is True
assert users['luiz'].get('somente_limite_global') is True
from dotenv import dotenv_values
cap = float(dotenv_values(ROOT / '.env')['IALD_OPENAI_COTA_GLOBAL_USD_DIA'])
assert cap == json.loads((WORK / 'deployment.json').read_text())['global_usd_per_day']
db_path = ROOT / 'iald_uso_openai.json.reservas.sqlite3'
with sqlite3.connect(db_path.as_uri() + '?mode=ro', uri=True) as db:
    used = db.execute('SELECT COALESCE(SUM(COALESCE(actual,cap)),0) FROM calls WHERE day=?',
                      (datetime.now(timezone.utc).date().isoformat(),)).fetchone()[0]
files = []
for name in json.loads((WORK / 'baseline.json').read_text()):
    path = ROOT / name
    assert path.read_bytes() == (WORK / 'stage' / name).read_bytes(), 'Concurrent edit: ' + name
    files.append({'path':str(path), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

marker = 'IALD_LUIZ_GLOBAL_ONLY_20260915'
note = f'''[INPUT] Ordem expressa do operador: durante os testes individuais, a conta luiz não deve ter cota própria; seu limite é o global. A proposta anterior de elevar o teto a US$ 5/dia não foi aplicada. O teto global permanece em US$ {cap:.2f}/dia; .env não foi modificado nesta mudança.

[REAL] Implantado somente_limite_global=true apenas no registro da conta luiz. Configuração isolada por requisição, a partir do cadastro confiável do servidor; JSON enviado pelo cliente não escolhe a isenção. Requer admin booleano verdadeiro e plano operador; administradores em plano gratuito/assinante conservam suas proteções. As outras contas permanecem com suas cotas.

[REAL] A conta luiz deixa de ser bloqueada por gasto diário individual, tokens diários/mensais e frequência individual de mensagens. Permanecem o teto global compartilhado, reservas atômicas por chamada, controles de integridade/cobrança e limites técnicos do provedor e da janela. O uso continua registrado. O estado da cota usa null para ausência de limite individual; zero mantém o significado de bloqueio. A interface mostra “Sem limite individual” e o gasto global incluindo reservas, pelo mesmo SQLite que faz o controle de envio, conciliado com o razão de uso.

[REAL] Verificação: oito testes da isenção/isolamento/fail-closed/concorrência, 218 verificações de motores, 67 de orçamento, sete de retry e sete da interface passaram. Os testes de orçamento exigiram o ambiente do operador para acessar tiktoken; falhas iniciais eram do ambiente isolado e foram resolvidas sem mudar regras de orçamento. Servidor web reativado e /health=200; modelo nativo mantido no processo 34128. Fontes JavaScript sincronizadas em app, www, iOS public e Android assets. Nenhum novo binário foi compilado/publicado. A isenção já atua no servidor, inclusive para os clientes móveis atuais; a apresentação atualizada exige os novos assets.

[REAL] Navegador autenticado confirmou a mensagem “Sua conta usa somente o limite global da IALD” e ausência de teto de tokens. Nenhuma nova inferência paga foi disparada nesta mudança. O teste completo de Hamiltoniano/dephasing permanece sem nova validação de resposta final; isto não afeta a conclusão sobre a isenção de cotas.

Evidências: {WORK} (deployment.json, display_deployment.json, testes e completion.json). Memórias anteriores são históricas; este adendo substitui apenas a proposta de configuração de cotas, sem alterar os estatutos canônicos da TGL.
'''

rows = []
for path in paths.TARGETS:
    before = path.read_bytes()
    assert marker.encode() not in before
    backup = path.with_name(path.name + '.bak_' + stamp)
    paths.create(backup, before)
    newline = '\r\n' if b'\r\n' in before else '\n'
    addition = '\n\n### ' + now.strftime('%d/%m/%Y %H:%M %z') + ' — Conta luiz somente no teto global\n\n'
    addition += '<!-- ' + marker + ' -->\n\n' + note
    after = before + addition.replace('\n',newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    paths.create(temp, after)
    assert path.read_bytes() == before, 'Concurrent memory update: ' + str(path)
    temp.replace(path)
    assert path.read_bytes() == after and len(after) > len(before)
    rows.append({'path':str(path),'backup':str(backup),'before_bytes':len(before),'after_bytes':len(after)})
report = {'status':'ACTIVE_VERIFIED', 'at':now.isoformat(), 'account':'luiz',
          'somente_limite_global':True,'global_usd_per_day':cap,'global_used_with_reservations':round(used,8),
          'health':200,'paid_inferences_in_this_change':0,'mobile_build_published':False,
          'memories':rows,'files':files}
paths.create(receipt, json.dumps(report, ensure_ascii=False, indent=2).encode())
print(json.dumps({k:v for k,v in report.items() if k not in ('memories','files')}, ensure_ascii=True))
