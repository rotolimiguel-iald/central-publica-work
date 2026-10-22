"""Audited atomic installation; never print credential contents or their hashes."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WORK = Path(__file__).parent
SOURCE = Path('C:/IALD/projetos_pyhton/IALD')
STAGE = WORK / 'stage'
RUNTIME = SOURCE / '.iald_runtime'
sys.path.insert(0, str(STAGE))
from iald_kernel import KernelCatalog

stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
manifest = json.loads((WORK / 'incoming_20260914_172519/manifest.json').read_bytes())
files = ['iald_web_server.py', 'iald_motores.py', 'requirements.txt', '.env.exemplo',
         'iald_kernel.py', 'iald_memoria_canonica.py', 'iald_retrieval.py', 'iald_orcamento.py',
         'iald_fontes_publicas.py', 'iald_fontes_publicas.json', 'tests/test_public_sources.py',
         'tests/test_kernel_catalog.py', 'tests/test_memory_budget.py',
         'tests/test_retrieval.py']
for name, record in manifest.items():
    if hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() != record['sha256']:
        raise RuntimeError('Concurrent source change; installation refused: ' + name)
for name in files:
    if name not in manifest and (SOURCE / name).exists():
        raise RuntimeError('A new destination already exists: ' + name)
    payload = (STAGE / name).read_bytes()
    if not payload:
        raise RuntimeError('Empty staged source: ' + name)
    if name.endswith('.py'):
        compile(payload, name, 'exec')

bundle = next((WORK / 'bundles').glob('kernel-*'))
catalog = KernelCatalog(bundle, WORK / 'lean_checks_20260914_161846/verification.json')
original = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py')
current_source = hashlib.sha256(original.read_bytes()).hexdigest()
if current_source != catalog.source_sha:
    raise RuntimeError('Canonical um.py changed; rebuild the bundle before installing.')
catalog.verification()
print(json.dumps({'preflight': 'PASS', 'files': files, 'kernel': catalog.status(),
                  'model': 'gpt-5.6-luna', 'memory': 'nucleo_kernel',
                  'daily_global_usd': 1.0, 'operator_motor': 'nativa'}, ensure_ascii=False))
if '--apply' not in sys.argv:
    raise SystemExit(0)

def restricted(path):
    account = subprocess.check_output(['whoami'], text=True).strip()
    subprocess.run(['icacls', str(path), '/inheritance:r', '/grant:r',
                    account + ':(F)', 'SYSTEM:(F)'], check=True, capture_output=True)

def atomic(path, payload, secret=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(temporary)
    if secret:
        restricted(temporary)
    temporary.write_bytes(payload)
    if temporary.read_bytes() != payload:
        raise RuntimeError('Temporary write verification failed')
    os.replace(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError('Installed bytes differ')

# Copy immutable derived sources first; do not copy or fork the canonical Atlas.
RUNTIME.mkdir(exist_ok=True)
destination_bundle = RUNTIME / bundle.name
if not destination_bundle.exists():
    shutil.copytree(bundle, destination_bundle)
KernelCatalog(destination_bundle)
cache = RUNTIME / 'tokenizer_cache'
shutil.copytree(WORK / 'tokenizer_cache', cache, dirs_exist_ok=True)
receipt = RUNTIME / 'kernel_verification.json'
if receipt.exists():
    raise RuntimeError('Existing receipt requires review before replacing')
atomic(receipt, (WORK / 'lean_checks_20260914_161846/verification.json').read_bytes())

env = SOURCE / '.env'
old_env = env.read_bytes()
settings = {
    # Keep existing TestFlight users working until the consent-capable app is distributed.
    'IALD_MOTOR_PADRAO': 'nativa', 'IALD_MOTOR_OPERADOR': 'nativa',
    'IALD_OPENAI_MODELO': 'gpt-5.6-luna', 'IALD_OPENAI_MODELO_OPERADOR': 'gpt-5.6-luna',
    'IALD_OPENAI_ESFORCO': 'none', 'IALD_OPENAI_ESFORCO_PENSAR': 'none',
    'IALD_OPENAI_JANELA': '131072', 'IALD_OPENAI_MAX_SAIDA': '4096',
    'IALD_OPENAI_MAX_SAIDA_PENSAR': '8192', 'IALD_MEMORIA_MODO': 'nucleo_kernel',
    'IALD_ATLAS_PATH': 'C:/IALD/Central de Patentes/memory/TGL_ATLAS.md',
    'IALD_KERNEL_BUNDLE': destination_bundle.as_posix(),
    'IALD_KERNEL_VERIFICATION': receipt.as_posix(),
    'TIKTOKEN_CACHE_DIR': cache.as_posix(),
    'IALD_OPENAI_COTA_USUARIO_USD_DIA': '0.20', 'IALD_OPENAI_COTA_OPERADOR_USD_DIA': '1.00',
    'IALD_OPENAI_COTA_GLOBAL_USD_DIA': '1.00', 'IALD_OPENAI_RESERVA_NATIVA': '0',
    # The explicitly authorized key is restricted to Chat Completions.
    'IALD_MODERACAO': '0',
}
lines = old_env.decode('utf-8-sig').splitlines()
kept = [line for line in lines if not any(re.match(r'^\s*(?:export\s+)?' + re.escape(key) + r'\s*=', line) for key in settings)]
updated_env = ('\r\n'.join(kept) + '\r\n' + '\r\n'.join(
    key + '=' + json.dumps(value, ensure_ascii=False) for key, value in settings.items()) + '\r\n').encode('utf-8')
from dotenv import dotenv_values
import io
if dotenv_values(stream=io.StringIO(old_env.decode('utf-8-sig'))).get('IALD_OPENAI_API_KEY') != dotenv_values(stream=io.StringIO(updated_env.decode())).get('IALD_OPENAI_API_KEY'):
    raise RuntimeError('Credential preservation check failed')

backups = {}
targets = [(SOURCE / name, (STAGE / name).read_bytes(), False) for name in files] + [(env, updated_env, True)]
for path, payload, secret in targets:
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + stamp)
        atomic(backup, path.read_bytes(), secret)
        backups[path] = backup
if env.read_bytes() != old_env:
    raise RuntimeError('Concurrent .env edit; installation refused')
changed = []
try:
    for name, record in manifest.items():
        if hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() != record['sha256']:
            raise RuntimeError('Concurrent source change immediately before installation: ' + name)
    for path, payload, secret in targets:
        if path in backups and path.read_bytes() != backups[path].read_bytes():
            raise RuntimeError('Concurrent edit; installation refused: ' + path.name)
        changed.append((path, secret))
        atomic(path, payload, secret)
except Exception:
    for path, secret in reversed(changed):
        if path in backups:
            atomic(path, backups[path].read_bytes(), secret)
        elif path.is_file() and path.resolve().is_relative_to(SOURCE.resolve()):
            path.unlink()
    raise

report = {'installed_at': datetime.now().astimezone().isoformat(), 'status': 'INSTALLED_NOT_RESTARTED',
          'files': {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() for name in files},
          'backups': [str(path) for path in backups.values()], 'settings': settings,
          'kernel': catalog.status(), 'credential_preserved': True}
atomic(WORK / ('installation_' + stamp + '.json'), json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
print('INSTALLATION=PASS; SERVER_NOT_RESTARTED; CREDENTIAL_PRESERVED')
