"""Build hash-only deployment plan without persisting the server preamble."""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json

W = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def staged_bytes():
    spec = importlib.util.spec_from_file_location('reliability_build',W/'recovery/build_staging.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    baseline = json.loads((W/'recovery/BASELINE.json').read_bytes())
    outputs = {}
    for row in baseline:
        path = Path(row['path'])
        assert path.parent == ROOT and sha(path.read_bytes()) == row['sha256'], 'Runtime baseline changed'
        raw = path.read_bytes()
        text = raw.decode('utf-8').replace('\r\n','\n')
        text = (mod.server_patch if path.name == 'iald_web_server.py' else mod.motor_patch)(text)
        expected = mod.preserve_unchanged_bytes(raw,text)
        assert sha(expected) == row['patched_sha256'], 'Recovery patch drift'
        if path.name == 'iald_web_server.py':
            anchor = 'def _segredo(nome: str, legado: str = "") -> str:\n'
            assert text.count(anchor) == 1
            replacement = anchor + '''    if nome == "IALD_OPENAI_API_KEY":
        from iald_openai_credential import load as _load_openai_credential
        dedicated = _load_openai_credential()
        if dedicated is not None:
            return dedicated
'''
            text = text.replace(anchor,replacement,1)
            expected = mod.preserve_unchanged_bytes(raw,text)
        ast.parse(expected)
        outputs[path.name] = expected
    for folder,name in [('recovery','iald_auto_recovery.py'),('credential','iald_openai_credential.py'),('deadlines','iald_deadlines.py')]:
        raw = (W/folder/name).read_bytes()
        if folder == 'deadlines':
            baseline = json.loads((W/'deadlines/BASELINE.json').read_bytes())
            assert sha((ROOT/name).read_bytes()) == baseline['before'], 'Deadline baseline changed'
            assert sha(raw) == baseline['after'], 'Deadline patch drift'
        ast.parse(raw)
        outputs[name] = raw
    return outputs


def plan():
    files = []
    for name, raw in staged_bytes().items():
        dest = ROOT/name
        files.append({'path':str(dest),'before':sha(dest.read_bytes()) if dest.exists() else None,
                      'after':sha(raw),'bytes':len(raw)})
    sources = [W/'prepare_release.py',W/'recovery/build_staging.py',W/'recovery/BASELINE.json',
               W/'credential/iald_openai_credential.py',W/'deadlines/iald_deadlines.py',W/'deadlines/BASELINE.json',W/'recovery/iald_auto_recovery.py',
               W/'maintenance_safe.py',W.parent/'iald_v407_20261104'/'transaction.py']
    return {'status':'PREPARED','files':files,'sources':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in sources],
            'client_files_changed':False,'science_files_changed':False,
            'credential_value_in_plan':False,'credential_rotation_separate':True}


if __name__ == '__main__':
    data = plan()
    p = W/'INSTALL_PLAN.json'
    with p.open('x',encoding='utf-8') as handle:
        json.dump(data,handle,ensure_ascii=False,indent=2)
    print(json.dumps({'files':len(data['files']),'plan_sha256':sha(p.read_bytes())}))
