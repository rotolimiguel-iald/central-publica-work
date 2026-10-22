"""Install the approved and tested core with a complete preflight and byte backups."""
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

if __name__ == '__main__':
    assert not (WORK/'code_installed.json').exists()
    approval = json.loads((WORK/'explicit_approval.json').read_bytes())
    assert approval['user_reply_verbatim'] == 'Sim, autorizo esses arquivos para api.openai.com e o teste'
    probes = sorted(WORK.glob('model_response_*.json'))
    response = json.loads(probes[-1].read_bytes())
    assert response['http_status'] == 200 and response['finish_reason'] == 'stop'
    assert response['single_call_cap_usd'] <= approval['max_test_usd']
    baseline = json.loads((WORK/'prepared.json').read_bytes())['baseline']
    test_baseline = json.loads((WORK/'test_baseline.json').read_bytes())
    plan = [(ROOT/name,(WORK/name).read_bytes(),expected) for name,expected in baseline.items()]
    plan += [(ROOT/'tests'/name,(WORK/'tests'/name).read_bytes(),expected) for name,expected in test_baseline.items()]
    # Check every target before the first mutation, including user parallel changes.
    for target,data,expected in plan:
        current = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
        assert current == expected, 'Concurrent edit: '+str(target)
        assert data
        if target.suffix == '.py':
            compile(data,str(target),'exec')
    rows = []
    try:
        for target,data,expected in plan:
            rows.append(helpers.install(target,data,expected))
    except BaseException:
        # A partial installation must remain visible; byte backups support recovery.
        helpers.create(WORK/'partial_installation.json',json.dumps({'files':rows},indent=2).encode())
        raise
    receipt = {'at':datetime.now().astimezone().isoformat(),
               'status':'INSTALLED__REGRESSION_AND_WEB_RESTART_PENDING','files':rows,
               'env_modified':False,'native_model_modified':False,'scientific_originals_modified':False}
    helpers.create(WORK/'code_installed.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'installed_files':len(rows),'status':receipt['status']}))
