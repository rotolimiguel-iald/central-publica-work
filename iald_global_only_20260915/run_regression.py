from pathlib import Path
import contextlib
import os
import runpy
import sys

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode = True
sys.path[:0] = [str(WORK / 'stage'), str(ROOT)]
os.environ['IALD_TESTE_BASE'] = str(WORK / 'stage')
import iald_motores
import iald_orcamento

name = sys.argv[1]
assert name in ('test_motores.py', 'test_orcamento_reserva.py', 'test_provider_retry.py')
sys.argv = [str(ROOT / 'tests' / name)]
log = WORK / (name + '.log')
with log.open('w', encoding='utf-8') as out, contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
    try:
        runpy.run_path(str(ROOT / 'tests' / name), run_name='__main__')
    except SystemExit as exc:
        status = exc.code or 0
    else:
        status = 0
print(name, 'exit', status)
print('\n'.join(log.read_text(encoding='utf-8').splitlines()[-5:]))
raise SystemExit(status)
