"""Connect the CLI to the same read-only Costs API as the running panel."""
from datetime import datetime
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
from goal16_records import ROOT, WORK, record, write_new

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
path = ROOT / 'ferramentas_openai/registrar_saldo_openai.py'
before = path.read_bytes()
memory_before = (ROOT / 'CLAUDE.md').read_bytes()
text = before.decode('utf-8').replace('\r\n', '\n')
assert text.count('Não lê nem imprime chave nenhuma.') == 1
text = text.replace('Não lê nem imprime chave nenhuma.',
                    'Lê a chave administrativa somente para consultar custos; nunca a imprime.')
text = text.replace('import sys\n', 'import sys\nimport requests\n')
anchor = '\n\ndef main():\n'
addition = '''

def read_setting(name, default=""):
    """Read current configuration without importing the production server."""
    value = os.environ.get(name)
    if value:
        return value.strip()
    try:
        with open(os.path.join(RAIZ, ".env"), encoding="utf-8-sig") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                if key.strip() == name:
                    return value.strip().strip('"').strip("'")
    except OSError:
        pass
    return default


def configured_balance():
    ledger = iald_motores.RazaoDeUso(os.path.join(RAIZ, "iald_uso_openai.json"))
    thresholds = {}
    for field, default in (("critico_usd", 5.0), ("atencao_usd", 15.0),
                           ("critico_dias", 3.0), ("atencao_dias", 7.0)):
        try:
            value = float(read_setting("IALD_OPENAI_SALDO_" + field.upper(), str(default)))
            thresholds[field] = value if value >= 0 else default
        except ValueError:
            thresholds[field] = default
    return iald_saldo_openai.SaldoOpenAI(
        os.path.join(RAIZ, "iald_saldo_openai.json"), ledger,
        chave_admin=lambda: read_setting("IALD_OPENAI_ADMIN_KEY"),
        obter=requests.get, **thresholds)


def main():
'''
assert text.count(anchor) == 1
text = text.replace(anchor, addition)
old = '''    razao = iald_motores.RazaoDeUso(os.path.join(RAIZ, "iald_uso_openai.json"))
    saldo = iald_saldo_openai.SaldoOpenAI(os.path.join(RAIZ, "iald_saldo_openai.json"), razao)'''
assert text.count(old) == 1
text = text.replace(old, '    saldo = configured_balance()')
after = text.replace('\n', '\r\n' if b'\r\n' in before else '\n').encode('utf-8')
compile(after, str(path), 'exec')

# Isolated evaluation: only temporary configuration/ledger and a fake HTTP function.
sys.path.insert(0, str(ROOT))
import types
module = types.ModuleType('balance_cli_candidate')
module.__file__ = str(path)
exec(compile(after, str(path), 'exec'), module.__dict__)
checks = []
with tempfile.TemporaryDirectory() as directory:
    module.RAIZ = directory
    env = Path(directory) / '.env'
    env.write_bytes(b'IALD_OPENAI_ADMIN_KEY=local-test-only\nIALD_OPENAI_SALDO_CRITICO_USD=4\n')
    anchor_time = datetime.now().astimezone().isoformat()
    (Path(directory) / 'iald_saldo_openai.json').write_bytes(json.dumps({
        'versao': 1, 'ancora': {'valor_usd': 10, 'em': anchor_time, 'por': 'test'},
        'compras': [], 'limites': {}, 'esgotado': None}).encode())
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return types.SimpleNamespace(status_code=200, json=lambda: {'data': [], 'has_more': False})

    with patch.dict(os.environ, {}, clear=True), patch.object(module.requests, 'get', fake_get):
        balance = module.configured_balance()
        state = balance.estado(forcar=True)
        assert len(calls) == 1 and calls[0][0] == 'https://api.openai.com/v1/organization/costs'
        assert calls[0][1]['headers']['Authorization'] == 'Bearer local-test-only'
        assert 'Costs API' in state['fonte_gasto']
        assert state['limites']['critico_usd'] == 4
        assert 'local-test-only' not in json.dumps(state)
        checks.append('CLI reads Costs API with protected configuration; secret omitted from output')
        env.write_bytes(b'# no admin key\n')
        balance = module.configured_balance()
        calls.clear()
        state = balance.estado(forcar=True)
        assert not calls and state['avisos']
        checks.append('Missing key produces visible warning without network call')

assert path.read_bytes() == before, 'Parallel helper edit'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
write_new(path.with_name(path.name + '.bak_' + stamp), before)
temporary = path.with_name(path.name + '.tmp_' + stamp)
write_new(temporary, after)
assert path.read_bytes() == before, 'Parallel helper edit'
temporary.replace(path)
assert path.read_bytes() == after
receipt = record('balance_cli_fix_20260915.json', {
    'task': 'T2 — correção do verificador CLI', 'status': '[REAL]',
    'path': str(path), 'sha256_before': hashlib.sha256(before).hexdigest(),
    'sha256_after': hashlib.sha256(after).hexdigest(), 'isolated_checks': checks,
    'server_restarted': False, 'credentials_modified': False,
}, '[REAL] Corrigido registrar_saldo_openai.py: o CLI agora injeta a leitura atual da chave admin '
   'e requests.get em SaldoOpenAI, como o servidor já faz. Antes, --mostrar sempre ignorava '
   'a Costs API mesmo com chave salva. Dois cenários isolados passaram: API de custos com chave '
   'de teste e ausência de chave sem rede; nenhum segredo no resumo. Backup byte a byte/CAS, '
   'sem alteração do .env ou reinício. [OPEN] Conciliação real aguarda a criação autorizada da chave.',
   memory_before)
print(json.dumps({'receipt': str(receipt), 'checks': checks}, ensure_ascii=False))
