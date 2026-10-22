from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK.parent / 'iald_hypotheses_20260915'))
# Load only the already reviewed installer helpers, never its main routine.
import importlib.util
spec = importlib.util.spec_from_file_location('prior_installer', WORK.parent / 'iald_hypotheses_20260915/install_code.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
create, install = helpers.create, helpers.install

if __name__ == '__main__':
    assert not (WORK / 'code_installed.json').exists()
    baseline = json.loads((WORK / 'prepared.json').read_bytes())['baseline']
    assert json.loads((WORK / 'verification_narrow.json').read_bytes())['source_preserved']
    rows = []
    for name in ['iald_instrucao_mae.py', 'iald_memoria_canonica.py']:
        data = (WORK / name).read_bytes()
        compile(data, str(ROOT / name), 'exec')
        rows.append(install(ROOT / name, data, baseline[name]))
    test = (WORK / 'test_mother_instruction.py').read_text(encoding='utf-8')
    test = 'import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n' + test
    rows.append(install(ROOT / 'tests/test_mother_instruction.py', test.encode(), None))
    create(WORK / 'code_installed.json', json.dumps({'at': datetime.now().astimezone().isoformat(),
           'status': 'CODE_INSTALLED_CONFIG_AND_RESTART_PENDING', 'files': rows}, indent=2).encode())
    print('Code installed with byte backups; originals and active configuration unchanged.')
