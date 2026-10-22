"""Correct three generated declaration references, retaining original audit attempts."""
import json
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r4'
previous = BUNDLE/'PLAN_R2.json'
plan = json.loads(previous.read_bytes())
probe = BUNDLE/'name_probe_r1'
receipt = json.loads((probe/'RECEIPT.json').read_bytes())
assert receipt['exit_code'] == 0 and pin(receipt['stdout']['path']) == receipt['stdout']
names = {}
for line in (probe/'STDOUT.log').read_text(encoding='utf-8').splitlines():
    cols = line.split('\t')
    if len(cols) == 3 and cols[0] == 'LOCAL_DECL':
        names[cols[1]] = cols[2].split(',') if cols[2] else []
replacements = {name: name.replace('_concreteLightRayNet','') for name in plan['theorems']
                if '_concreteLightRayNet' in name}
assert len(replacements) == 3
for old, corrected in replacements.items():
    assert old not in names and corrected in names
    assert set(names[corrected]) <= {'propext','Classical.choice','Quot.sound'}
theorems = sorted(replacements.get(n,n) for n in plan['theorems'])
assert len(theorems) == len(set(theorems)) == 936
module = 'TGLExt.F1Fecho394.NetworkProofAuditR3'
relative = module.replace('.','/')+'.lean'
body = ''.join('import TGLExt.F1Fecho394.'+n+'\n' for n in plan['roots'])
body += '\n'+'\n'.join('#print axioms '+n for n in theorems)+'\n'
new(BUNDLE/'src'/relative,body)
plan.update(revision='R3', original_plan=pin(previous), script=pin(__file__),
    audit_module=module, audit_relative=relative, audit=pin(BUNDLE/'src'/relative),
    theorems=theorems, generated_name_correction=dict(replacements=replacements,
        discovery=pin(probe/'RECEIPT.json'),
        scope='Generated instance names changed in the shared import environment; all proof bodies remain unchanged.'))
new(BUNDLE/'PLAN_R3.json',plan)
print(json.dumps(dict(plan=pin(BUNDLE/'PLAN_R3.json'),replacements=replacements),ensure_ascii=False))
