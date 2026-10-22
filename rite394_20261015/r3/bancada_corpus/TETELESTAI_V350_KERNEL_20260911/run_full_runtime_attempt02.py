"""Supervise the unchanged working program in a fully copied runtime directory."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'r'
PYTHON = Path(r'C:\Users\rotol\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe')
LEAN_BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
TEX = RUN / 'tex_environment'

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def save(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(data)
    assert temp.stat().st_size == len(data)
    os.replace(temp, path)

def environment():
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'TGL_KERNEL_PREBUILT']:
        env.pop(key, None)
    override = {
        'TGL_CACHE_DIR': str(RUN / 'cache'), 'TGL_FORMAL_MODE': 'strict',
        'TGL_LAKE': str(LEAN_BIN / 'lake.exe'), 'TGL_RITE_CHECKPOINT': '0',
        'TGL_SKIP_SELFTEST': '0', 'TGL_NO_NETWORK': '1', 'TGL_VOID_NO_NETWORK': '1',
        'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1', 'PYTHONUTF8': '1',
        'MPLCONFIGDIR': str(RUN / 'runtime_config/matplotlib'),
        'TMP': str(RUN / 'runtime_tmp'), 'TEMP': str(RUN / 'runtime_tmp'),
        'MIKTEX_USERCONFIG': str(TEX / 'config'), 'MIKTEX_USERDATA': str(TEX / 'data'),
        'MIKTEX_USERINSTALL': str(TEX / 'install'),
    }
    for key in ['MPLCONFIGDIR', 'TMP']:
        Path(override[key]).mkdir(parents=True, exist_ok=True)
    env.update(override)
    env['PATH'] = os.pathsep.join([str(TEX / 'install/miktex/bin/x64'), str(LEAN_BIN), env.get('PATH', '')])
    return env, override

def preflight():
    env, override = environment()
    target = RUN / 'environment_preflight'
    target.mkdir(exist_ok=True)
    commands = [[str(PYTHON), '-B', '-c', 'import sys,numpy,matplotlib;print(sys.version);print(numpy.__version__);print(matplotlib.__version__)'],
                [str(TEX / 'install/miktex/bin/x64/initexmf.exe'), '--report'],
                [str(LEAN_BIN / 'lake.exe'), '--version']]
    results = []
    for index, cmd in enumerate(commands):
        r = subprocess.run(cmd, cwd=RUN, env=env, capture_output=True, timeout=60,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        (target / f'command_{index}_stdout.txt').write_bytes(r.stdout)
        (target / f'command_{index}_stderr.txt').write_bytes(r.stderr)
        results.append({'cmd': cmd, 'returncode': r.returncode})
    save(target / 'results.json', {'commands': results, 'overrides': override})
    print(json.dumps(results, ensure_ascii=False), flush=True)
    assert all(x['returncode'] == 0 for x in results), 'Environment preflight failed'

def main():
    if '--preflight' in sys.argv:
        preflight()
        return
    manifest = json.loads((RUN / 'input_manifest.json').read_bytes())
    assert manifest['status'] == 'PREPARED_NOT_EXECUTED'
    assert sha(RUN / 'um.py') == manifest['working_sha256'] == sha(ROOT / 'um.py')
    assert not (RUN / 'runtime_process_02.json').exists(), 'Do not launch duplicate runs'
    env, overrides = environment()
    command = [str(PYTHON), '-B', '-u', str(RUN / 'um.py')]
    started = datetime.now().astimezone().isoformat()
    start_clock = time.monotonic()
    with (RUN / 'runtime_stdout_02.txt').open('xb') as out, (RUN / 'runtime_stderr_02.txt').open('xb') as err:
        proc = subprocess.Popen(command, cwd=RUN, env=env, stdin=subprocess.PIPE,
                                stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
        state = {'status': 'RUNNING', 'pid': proc.pid, 'started': started,
                 'command': command, 'overrides': overrides,
                 'working_sha256': manifest['working_sha256'],
                 'full_runtime_completed': False, 'new_mathematical_requirements': []}
        save(RUN / 'runtime_process_02.json', state)
        proc.stdin.write(b'1\n')
        proc.stdin.close()
        print(json.dumps(state, ensure_ascii=False), flush=True)
        while True:
            try:
                code = proc.wait(timeout=30)
                break
            except subprocess.TimeoutExpired:
                print(json.dumps({'pid': proc.pid, 'elapsed_seconds': round(time.monotonic() - start_clock),
                      'stdout_bytes': (RUN / 'runtime_stdout_02.txt').stat().st_size,
                      'stderr_bytes': (RUN / 'runtime_stderr_02.txt').stat().st_size}), flush=True)
        state.update({'status': 'PROCESS_EXITED', 'returncode': code,
                      'finished': datetime.now().astimezone().isoformat(),
                      'elapsed_seconds': time.monotonic() - start_clock,
                      'program_sha256_after': sha(RUN / 'um.py'),
                      'full_runtime_completed': code == 0,
                      'evidence_validation_pending': True})
        save(RUN / 'runtime_process_02.json', state)
        print(json.dumps(state, ensure_ascii=False), flush=True)
        raise SystemExit(code)

if __name__ == '__main__':
    main()
