import hashlib
import json
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
OUT=ROOT/'revisao/runtime_seals_preliminary_20260913_100700_656494'
prior=json.loads((OUT/'final_inspection.json').read_bytes())
report=json.loads((OUT/'final_proof.json').read_bytes())['axiom_report']
allowed={'propext','Classical.choice','Quot.sound'}
def parse(raw):
    txt=raw.decode('utf-8-sig')
    maps={}; conflicts=[]; messages=0
    for m in re.finditer(r"'([\w.']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",txt):
        messages+=1
        val=[x.strip() for x in (m.group(2) or '').split(',') if x.strip()]
        if m[1] in maps and set(maps[m[1]])!=set(val):conflicts.append(m[1])
        maps[m[1]]=val
    return maps,conflicts,messages
parts={};pins={}
for kind in ['build','audit']:
    p=ROOT/f'r/tgl_kernel_{kind}_capture.txt'; raw=p.read_bytes()
    pins[kind]={'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    amap,conflicts,n=parse(raw)
    parts[kind]={'map':amap,'conflicts':conflicts,'messages':n}
build=parts['build']['map']; audit=parts['audit']['map']; union={**build,**audit}
conflicts=[n for n in build.keys()&audit.keys() if set(build[n])!=set(audit[n])]
extra=sorted(set(union)-set(audit))
restored={}
for kind in ['build','audit']:
    restored.update(parse((OUT/f'final_{kind}_restored.txt').read_bytes())[0])
result={
    'previous_comparison':'final_inspection.json: formal_axiom_map_reused_matches_proof_manifest=False',
    'classification':'SCOPE_DIFFERENCE_RESOLVED__BUILD_UNION_AUDIT_NOT_AUDIT_ONLY',
    'code_reference':'um.py:134443-134461', 'pins':pins,
    'audit_messages':parts['audit']['messages'],'audit_unique':len(audit),
    'build_messages':parts['build']['messages'],'build_unique':len(build),
    'union_unique':len(union),'report_entries':len(report),
    'build_only_names':extra,'build_only_count':len(extra),
    'conflicts':conflicts+parts['build']['conflicts']+parts['audit']['conflicts'],
    'json_exact_union':report==union,'all_union_axioms_allowed':all(set(a)<=allowed for a in union.values()),
    'missing_in_report':sorted(set(union)-set(report)),
    'unsupported_report_names':sorted(set(report)-set(union)),
    'restored_union_matches_principal':restored==union,
    'examples':{k:union[k] for k in extra[:8]},
    'no_author_parser_or_report_modified':True}
dest=OUT/'axiom_scope_resolution.json'; assert not dest.exists()
dest.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in result.items() if k!='build_only_names'},ensure_ascii=False,indent=2))
