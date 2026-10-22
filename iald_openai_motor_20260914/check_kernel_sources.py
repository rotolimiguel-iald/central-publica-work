"""Compile selected copied sources with the installed pinned Lean toolchain.

Never imports/runs um.py; never runs Lake against the canonical project.
Dependencies use existing objects, explicitly recorded as not rebuilt here.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

WORK = Path(__file__).parent
sys.path.insert(0, str(WORK / 'stage'))
from iald_kernel import KernelCatalog

catalog = KernelCatalog(next((WORK / 'bundles').glob('kernel-*')))
canonical = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
compiler = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
build = WORK / ('lean_checks_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
build.mkdir()
dependency_paths = [canonical / '.lake/build/lib/lean']
dependency_paths += [p / '.lake/build/lib/lean' for p in (canonical / '.lake/packages').iterdir()
                     if (p / '.lake/build/lib/lean').is_dir()]
env = {key: value for key, value in os.environ.items()
       if key.upper() in ('SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'PATH', 'USERPROFILE', 'COMSPEC')}
env['LEAN_PATH'] = os.pathsep.join(map(str, dependency_paths))
version = subprocess.run([str(compiler), '--version'], capture_output=True, timeout=15, check=True).stdout.decode('utf-8').strip()
if 'version 4.31.0,' not in version:
    raise RuntimeError('Compiler does not match the embedded lean-toolchain.')
targets = {'TGLExt/TheIALDSelector.lean': ['TGLExt.iald_is_idempotent', 'TGLExt.iald_selects']}
report = {'source_sha256': catalog.source_sha, 'created_at': datetime.now(timezone.utc).isoformat(),
          'scope': 'SELECTED_SOURCE_COMPILATION__NOT_WHOLE_KERNEL', 'compiler': version,
          'compiler_sha256': hashlib.sha256(compiler.read_bytes()).hexdigest(),
          'dependencies': 'EXISTING_COMPILED_OBJECTS__NOT_REBUILT_IN_THIS_CHECK', 'files': {}}
for name, declarations in targets.items():
    source = catalog._read_checked(name)
    check = build / name
    check.parent.mkdir(parents=True, exist_ok=True)
    check.write_bytes((source + '\n' + '\n'.join('#print axioms ' + d for d in declarations) + '\n').encode('utf-8'))
    result = subprocess.run([str(compiler), '-j', '1', '-M', '16384', '-R', str(build), str(check)],
                            cwd=build, env=env, capture_output=True, timeout=180)
    stdout = result.stdout.decode('utf-8', 'replace')
    stderr = result.stderr.decode('utf-8', 'replace')
    (build / 'stdout.txt').write_bytes(result.stdout)
    (build / 'stderr.txt').write_bytes(result.stderr)
    report['files'][name] = {'file_sha256': catalog.records[name]['sha256'], 'exit_code': result.returncode,
                             'status': 'COMPILED' if result.returncode == 0 else 'COMPILATION_FAILED',
                             'declarations': declarations, 'compiler_output': (stdout + stderr)[:16000]}
(build / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
print('REPORT_PATH=' + str(build / 'verification.json'))
