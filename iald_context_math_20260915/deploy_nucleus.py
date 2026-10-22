"""Install reviewed context/rendering changes with byte backups and CAS checks."""
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from dotenv import dotenv_values

WORK = Path(__file__).parent
NATIVE = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(WORK))
from iald_kernel import KernelCatalog


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic(path, payload, secret=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temp = Path(name)
    if secret:
        account = subprocess.check_output(['whoami'], text=True).strip()
        subprocess.run(['icacls', str(temp), '/inheritance:r', '/grant:r',
                        account + ':(F)', 'SYSTEM:(F)'], check=True, capture_output=True)
    temp.write_bytes(payload)
    assert temp.read_bytes() == payload
    os.replace(temp, path)
    assert path.read_bytes() == payload


def main():
    receipt = WORK / 'deployment.json'
    if receipt.exists():
        raise RuntimeError('Already deployed; inspect receipt')
    baseline_path = WORK / 'baseline_reconciled.json'
    baseline = {row['relative']: row['sha256'] for row in json.loads(baseline_path.read_bytes())}
    expected_js = baseline['app\\iald.js']
    paths = [NATIVE / 'app/iald.js', NATIVE / 'iald-app/www/iald.js',
             NATIVE / 'iald-app/ios/App/App/public/iald.js',
             NATIVE / 'iald-app/android/app/src/main/assets/public/iald.js']
    pending = {p: (WORK / 'app/iald.js').read_bytes() for p in paths}
    pending[NATIVE / 'iald_memoria_canonica.py'] = (WORK / 'iald_memoria_canonica.py').read_bytes()
    pending[NATIVE / 'iald_nucleo_fixo.json'] = (WORK / 'iald_nucleo_fixo.json').read_bytes()
    pending[NATIVE / 'tests/test_temporal_context.py'] = (WORK / 'tests/test_temporal_context.py').read_bytes()
    pending[NATIVE / 'tests/test_math.mjs'] = (WORK / 'tests/test_math.mjs').read_bytes()
    originals = {p: p.read_bytes() if p.exists() else None for p in pending}
    for p in paths:
        assert digest(originals[p]) == expected_js, 'Parallel app change: ' + str(p)
    assert digest(originals[NATIVE / 'iald_memoria_canonica.py']) == baseline['iald_memoria_canonica.py'], 'Parallel context change'
    assert originals[NATIVE / 'iald_nucleo_fixo.json'] is None, 'Existing fixed-nucleus configuration'
    report = json.loads((WORK / 'nucleus_prepared.json').read_bytes())
    source_bundle = Path(report['bundle_path'])
    catalog = KernelCatalog(source_bundle)
    destination_bundle = NATIVE / '.iald_runtime' / source_bundle.name
    assert destination_bundle.resolve().is_relative_to((NATIVE / '.iald_runtime').resolve())
    env_path = NATIVE / '.env'
    old_env = env_path.read_bytes()
    before = dotenv_values(stream=io.StringIO(old_env.decode('utf-8-sig')))
    assert before.get('IALD_OPENAI_MODELO') == 'gpt-5.6-luna'
    assert before.get('IALD_OPENAI_JANELA') == '131072', 'Window changed in parallel'
    settings = {'IALD_OPENAI_JANELA': '400000', 'IALD_KERNEL_BUNDLE': destination_bundle.as_posix(),
                'IALD_KERNEL_VERIFICATION': ''}
    text = old_env.decode('utf-8-sig')
    for key, value in settings.items():
        pattern = re.compile(r'(?m)^' + re.escape(key) + r'=[^\r\n]*')
        assert len(pattern.findall(text)) == 1, 'Missing or duplicate setting: ' + key
        text = pattern.sub(lambda m: key + '=' + value, text)
    updated_env = (b'\xef\xbb\xbf' if old_env.startswith(b'\xef\xbb\xbf') else b'') + text.encode('utf-8')
    after = dotenv_values(stream=io.StringIO(text))
    assert {k: v for k, v in before.items() if k not in settings} == {k: v for k, v in after.items() if k not in settings}
    pending[env_path], originals[env_path] = updated_env, old_env
    print(json.dumps({'preflight': 'PASS', 'targets': [str(p.relative_to(NATIVE)) for p in pending],
                      'context_tokens': report['nucleus']['context_tokens'], 'new_window': 400000,
                      'kernel_sources': catalog.status()['files'], 'secrets_unchanged': True,
                      'old_compilation_receipt_retained': True, 'new_compilation_claimed': False}))
    if '--apply' not in sys.argv:
        return
    if not destination_bundle.exists():
        shutil.copytree(source_bundle, destination_bundle)
    assert KernelCatalog(destination_bundle).source_sha == catalog.source_sha
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for p, old in originals.items():
        assert (p.read_bytes() if p.exists() else None) == old, 'Concurrent change before deployment'
    backups = []
    for p, old in originals.items():
        if old is not None:
            backup = p.with_name(p.name + '.bak_' + stamp)
            atomic(backup, old, p == env_path)
            assert backup.read_bytes() == old
            backups.append(str(backup))
    applied = []
    try:
        for p, payload in pending.items():
            assert (p.read_bytes() if p.exists() else None) == originals[p], 'Concurrent change: ' + str(p)
            atomic(p, payload, p == env_path)
            applied.append(p)
    except Exception:
        for p in reversed(applied):
            if originals[p] is not None and p.read_bytes() == pending[p]:
                atomic(p, originals[p], p == env_path)
        raise
    records = [{'path': str(p), 'sha256': digest(payload)} for p, payload in pending.items() if p != env_path]
    atomic(receipt, json.dumps({'recorded_at': datetime.now().astimezone().isoformat(),
        'status': 'FILES_INSTALLED_RESTART_PENDING', 'files': records, 'backups': backups,
        'settings': settings, 'secret_values_unchanged': True, 'kernel': catalog.status(),
        'nucleus': report['nucleus'], 'server_restarted': False, 'mobile_binaries_rebuilt': False,
        'previous_mobile16_binary_no_longer_matches_current_source': True}, ensure_ascii=False, indent=2).encode('utf-8'))
    print('FILES_INSTALLED_WITH_BYTE_BACKUPS; SERVER_RESTART_PENDING')


if __name__ == '__main__':
    main()
