"""Run existing regression tests against staged code, using real resource paths.

Test fixtures replace users, billing and network before calling the routes.
The backend __main__ block is never entered.
"""
from datetime import datetime
import os
from pathlib import Path
import re
import runpy
import sys
import types
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORK = Path(__file__).parent
STAGE = WORK / 'stage'
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(STAGE), str(WORK / 'dependencies'), str(SOURCE)]
os.environ['TIKTOKEN_CACHE_DIR'] = str(WORK / 'tokenizer_cache')
os.environ['IALD_CREDITO_USO'] = '0'
os.chdir(SOURCE)
import iald_motores


def load_backend():
    if 'iald_web_server' in sys.modules:
        return sys.modules['iald_web_server']
    module = types.ModuleType('iald_web_server')
    module.__file__ = str(SOURCE / 'iald_web_server.py')
    sys.modules[module.__name__] = module
    exec(compile((STAGE / 'iald_web_server.py').read_bytes(), str(STAGE / 'iald_web_server.py'), 'exec'), module.__dict__)
    return module


if __name__ == '__main__':
    suite = sys.argv[1] if len(sys.argv) > 1 else 'test_motores.py'
    log = WORK / (suite.removesuffix('.py') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.log')
    stdout = sys.stdout
    result = 0
    with log.open('w', encoding='utf-8') as handle:
        sys.stdout = handle
        try:
            if suite != 'test_motores.py':
                load_backend()
            sys.argv = [str(STAGE / 'tests' / suite)]
            runpy.run_path(str(STAGE / 'tests' / suite), run_name='__main__')
        except SystemExit as error:
            result = error.code or 0
        finally:
            sys.stdout = stdout
    text = log.read_text(encoding='utf-8')
    print(re.sub(r'sk-[A-Za-z0-9_-]+', '[REDACTED]', '\n'.join(text.splitlines()[-18:])))
    print('LOG_PATH=' + str(log))
    raise SystemExit(result)
