from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
spec = importlib.util.spec_from_file_location('byte_installer',WORK.parent/'iald_hypotheses_20260915/install_code.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
rows = []
for name, count in [('test_residuos_finais.py',1),('test_residuos_servidor.py',2)]:
    target = ROOT/'tests'/name
    before = target.read_bytes()
    old = b'def prompt(self, legado, catalogo):'
    assert before.count(old) == count
    after = before.replace(old,b'def prompt(self, legado, catalogo, public=False):')
    compile(after,str(target),'exec')
    rows.append(helpers.install(target,after,hashlib.sha256(before).hexdigest()))
helpers.create(WORK/'additional_test_fixtures.json',json.dumps({'at':datetime.now().astimezone().isoformat(),
    'change':'Only mock prompt signatures updated; assertions unchanged','files':rows},indent=2).encode())
print('Three remaining mock signatures updated; no assertions changed.')
