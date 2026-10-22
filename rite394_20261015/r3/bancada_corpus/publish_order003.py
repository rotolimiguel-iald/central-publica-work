"""Assemble immutable local delivery from measured verification records."""
from pathlib import Path
import hashlib
import json
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def publish(path, value):
    assert not path.exists(), str(path)
    payload = value.encode('utf-8')
    temporary = path.with_suffix(path.suffix+'.tmp')
    with temporary.open('xb') as stream:
        stream.write(payload)
    assert temporary.stat().st_size == len(payload)
    temporary.rename(path)

inventory = read_json(ROOT/'ORDEM003_INVENTARIO.json')
modules = [row['module'] for row in inventory]
records = []
failures = []
for module in modules+['Order003Audit']:
    source = ROOT/(module+'.lean')
    entries = []
    for path in sorted(ROOT.glob(module+'.*.json')):
        data = read_json(path)
        if 'exit_code' not in data:
            continue
        log = ROOT/data['log']
        log_text = log.read_text(encoding='utf-8-sig')
        if data['exit_code'] != 0:
            preserved = log.with_suffix('.falha_lean.log')
            if not preserved.exists():
                with preserved.open('xb') as stream:
                    stream.write(log.read_bytes())
            assert preserved.read_bytes() == log.read_bytes()
            failures.append({'metadata':str(path),'log':str(preserved),'sha256':sha(preserved)})
        entries.append((path,data,log_text))
    assert entries, module
    path,data,log_text = entries[-1]
    assert data['exit_code'] == 0 and data['source_stable']
    assert data['proof_sha256'] == sha(source), module
    assert not re.search(r'\b(sorryAx|error|warning)\b',log_text), module
    records.append({'module':module,'source':str(source),'sha256':sha(source),
                    'metadata':str(path),'metadata_sha256':sha(path),
                    'log':str(ROOT/data['log']),'log_sha256':sha(ROOT/data['log'])})

audit_text = Path(records[-1]['log']).read_text(encoding='utf-8-sig')
printed = re.findall(r"'ChatgptAudit\.(\w+)' depends on axioms: \[([^\]]*)\]",audit_text)
expected = [name for row in inventory for name in row['theorems']]
assert sorted(name for name,_ in printed) == sorted(expected)
for name,axioms in printed:
    assert set(axioms.split(', ')) == {'propext','Classical.choice','Quot.sound'},name
for row in inventory:
    assert sha(ROOT/(row['module']+'.lean')) == row['sha256']
source_copies = read_json(ROOT/'manifesto_fontes.json')
changed = [row['copy'] for row in source_copies if sha(Path(row['copy'])) != row['sha256']]
assert not changed, changed
controls = read_json(ROOT/'CADEIA_CONTROLES_EXATOS.json')
assert len(controls['shift_variances']) == 16 and len(controls['volume_checks']) == 16
verification = {'timestamp':datetime.now().isoformat(),'status':'REAL — local verification; independent audit pending',
                'theorem_count':len(expected),'module_count':len(modules),'records':records,
                'axioms':dict(printed),'failures_preserved':failures,
                'source_copy_count':len(source_copies),'source_copies_changed':changed}
publish(ROOT/'ORDEM003_VERIFICACAO_FINAL.json',json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
body = (ROOT/'ORDEM003_ENTREGA_TEXTO.md').read_text(encoding='utf-8')
body += '\n## Reprodução em PowerShell\n\nA partir de C:/IALD/Central de Patentes:\n\n'
quote = chr(96)
body += quote*3+'powershell\n'
for module in modules+['Order003Audit']:
    body += f"& './Chatgpt/verify_stage.ps1' -Module {module}\n"
    body += f"if ($LASTEXITCODE -ne 0) {{ throw 'Falha em {module}' }}\n"
body += quote*3+'\n\n## Fontes, contagens e SHA256 medidos\n\n'
for row in inventory:
    path = ROOT/(row['module']+'.lean')
    body += f'- {quote}{path}{quote} — {len(row["theorems"])} teoremas — {quote}{sha(path)}{quote}.\n'
body += '\n## Outros artefatos e SHA256 medidos\n\n'
for name in ['CADEIA_LOCALIZACAO_VOLUME.md','CADEIA_RESULTADOS_E_LACUNAS.md',
             'CADEIA_CONTROLES_EXATOS.json','prepare_order003_audit.py','Order003Audit.lean',
             'ORDEM003_INVENTARIO.json','ORDEM003_VERIFICACAO_FINAL.json','verify_stage.ps1',
             'ORDEM003_ENTREGA_TEXTO.md','publish_order003.py']:
    body += f'- {quote}{ROOT/name}{quote} — {quote}{sha(ROOT/name)}{quote}.\n'
body += '\n## Logs finais\n\n'
for row in records:
    body += f'- {quote}{row["log"]}{quote} — {quote}{row["log_sha256"]}{quote}; exit 0, fonte estável.\n'
body += f'\nPreservação medida: {len(source_copies)} cópias verificadas; {len(changed)} divergências. '
body += f'{len(failures)} logs falhos preservados com sufixo .falha_lean.log.\n'
target = ROOT/'TUNEL'/'DO_CHATGPT'/'ENTREGA_003_localizacao_na_cadeia_e_ponte_volume.md'
publish(target,body)
print(json.dumps({'delivery':str(target),'sha256':sha(target),'theorems':len(expected),
                  'failed_compilations_preserved':len(failures),'source_copies_verified':len(source_copies)},ensure_ascii=False))
