"""Exact synthetic checks and full Lean axiom probe; writes only new workspace files."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['TowerTailRigidity','ChainSiteOperators','ChainLocality','ChainPrefix',
           'ChainVolume','ChainSiteFlow','ChainTail','ChainVolumePositive',
           'ChainTailClosure','ChainFaithful']

def publish(name, data):
    target = ROOT / name
    assert not target.exists(), str(target)
    payload = data.encode('utf-8')
    temporary = target.with_suffix(target.suffix + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(payload)
    assert temporary.stat().st_size == len(payload)
    temporary.rename(target)

if __name__ == '__main__':
    rows = []
    for n in range(1,9):
        for p in [F(1,3),F(2,3)]:
            mean = variance = F(0)
            for bits in product((0,1),repeat=n):
                weight = F(1)
                for bit in bits:
                    weight *= p if bit == 0 else 1-p
                value = F(bits.count(0),n)
                mean += weight*value
                variance += weight*(value-p)**2
            assert mean == p and variance == p*(1-p)/n
            rows.append({'n':n,'p':str(p),'mean':str(mean),'variance':str(variance)})
    profile = [F(1,3),F(2,3),F(1,4),F(3,4)]
    volume_checks = []
    for mask in product((0,1),repeat=4):
        sites = [i for i,b in enumerate(mask) if b]
        value = sum((profile[i] for i in sites),F(0))
        normalized = sum((profile[i]/profile[i] for i in sites),F(0))
        assert normalized == len(sites)
        volume_checks.append({'sites':sites,'state_q':str(value),'state_normalized':str(normalized)})
    controls = {'status':'REAL — exact synthetic controls; no observational data',
                'scope':'Finite checks support arithmetic, not a proof of the infinite strong limit.',
                'shift_variances':rows,'volume_checks':volume_checks}
    publish('CADEIA_CONTROLES_EXATOS.json',json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
    probe = ''.join(f'import {m}\n' for m in MODULES)+'\n'
    inventory = []
    for module in MODULES:
        source = ROOT / (module+'.lean')
        content = source.read_text(encoding='utf-8')
        assert not re.search(r'\b(sorry|admit|axiom)\b',content)
        names = re.findall(r'^theorem\s+(\w+)',content,re.M)
        assert names
        probe += ''.join(f'#print axioms ChatgptAudit.{name}\n' for name in names)
        inventory.append({'module':module,'theorems':names,
                          'sha256':hashlib.sha256(source.read_bytes()).hexdigest().upper()})
    publish('Order003Audit.lean',probe)
    publish('ORDEM003_INVENTARIO.json',json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'modules':len(MODULES),'theorems':sum(len(r['theorems']) for r in inventory),
                      'variance_cases':len(rows),'volume_cases':len(volume_checks)}))
