"""Freeze the concrete root-built KMS chain and its completed exact-module audit."""
from pathlib import Path
import datetime as dt
import json,re
from diary_r1 import ROOT,new,pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base=out/'kms_strip'
names=['StripPhaseBoundsR1','KMSStripIntegralR2','KMSBoundaryExchangeR1',
 'HalfModularStripR3','CanonicalJBoostR3','CanonicalH1StripR3',
 'WedgeOneParticleStripR2','StripMaximumR2','StripUniformLimitR2',
 'StripBoundaryLimitR1','UnitaryCoefficientsUniformR2','KMSGraphClosureR3','CanonicalWedgeKMSR4']
entries=[]
for name in names:
    source=base/(name+'.lean')
    matches=[]
    for folder in [base/'attempts',out/'weyl_net_wiring/attempts']:
        for p in folder.glob('*/'+name+'.olean'):
            r=json.loads((p.parent/'RECEIPT.json').read_bytes())
            if r['exit_code']==0 and pin(p.with_suffix('.lean'))['sha256']==pin(source)['sha256']:
                matches.append(p)
    assert matches,(name,'missing green compilation')
    p=sorted(matches)[-1]
    entries.append(dict(name=name,source=pin(source),build=pin(p.parent/'RECEIPT.json'),
        object=pin(p),output=pin(p.parent/'AXIOMS.txt')))
audit=base/'attempts/20261015T215022_521047Z'
ar=json.loads((audit/'RECEIPT.json').read_bytes())
assert ar['exit_code']==0 and ar['readonly_dependencies_unchanged']
raw=(audit/'AXIOMS.txt').read_text(encoding='utf-8')
rows=[line.split('\t') for line in raw.splitlines() if line.startswith('LOCAL_DECL\t')]
assert len(rows)==int(re.search(r'AUDITED_COUNT\t(\d+)',raw)[1])
assert all(set(row[2].split(','))<={'propext','Classical.choice','Quot.sound',''} for row in rows)
for path in ar['dependencies']:
    assert pin(path['path'])==path
reviews=[base/'review_closure/REVISAO_FECHO_KMS_R1.json',base/'review_concrete/REVISAO_KMS_CONCRETO_R1.json']
receipt=dict(status='PASS_WITH_STATED_SCOPE',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 theorem='F1Fecho.CanonicalWedgeKMS.canonical_bw_kms',
 statement='KMSBody (FieldWeyl.R KWR.toClosedSubmodule.toSubmodule) vacuum (fun t => gamma (B0 (2*pi*t))) 1',
 mathematical_scope='Actual standard wedge on the same canonical Fock. The H1 strip is constructed from the half-modular multiplier domain; finite Weyl sums extend to the full von Neumann algebra via joint graph density and uniform strip limits. No KMS or coefficient-analyticity field is assumed.',
 sign='Physical KMS flow uses +2*pi*t; modular imaginary powers use -2*pi*t. These are distinct conventions, preserved explicitly.',
 modules=entries,all_local_declarations_including_generated=len(rows),
 audit=pin(audit/'RECEIPT.json'),audit_output=pin(audit/'AXIOMS.txt'),
 finite_weyl_chain=pin(base/'FINAL_WEYL_KMS_FINITE_RECEIPT_R1.json'),reviews=[pin(p) for p in reviews],
 review_scope='Independent source/semantic reviews of the root composition; the reviewers did not independently recompile this 13-module chain. Root exact-module audit is a real Lean invocation.',
 remaining=['Full Fock CFC/boost equality is tracked separately','Global all-wedge net and joint certificates are not supplied by this KMS theorem'],
 production_modified=False,gate_moved=False,new_provider_calls=0,script=pin(__file__))
new(base/'FINAL_CONCRETE_WEDGE_KMS_RECEIPT_R1.json',receipt)
print(json.dumps(pin(base/'FINAL_CONCRETE_WEDGE_KMS_RECEIPT_R1.json')))
