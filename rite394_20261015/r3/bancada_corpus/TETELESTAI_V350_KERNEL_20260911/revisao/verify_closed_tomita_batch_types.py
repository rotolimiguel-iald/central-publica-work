"""Compare fresh #check universe output against the three prior independent audits."""
from pathlib import Path
import datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'closed_tomita_batch_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
assert C['complete'] and C['all_exit_zero'] and C['exact_99_audited']
sha=lambda b:hashlib.sha256(b).hexdigest()
def extract(text):
    result={};current=None;lines=[]
    for line in text.splitlines():
        match=re.match(r'^(TGLV350\.Regular\.[\w]+)(?:\.\{|\s)',line)
        if match:
            if current:result[current]=' '.join(' '.join(lines).split())
            current=match[1];lines=[line]
        elif line.startswith("'") and ('depends on axioms' in line or 'does not depend' in line):
            if current:result[current]=' '.join(' '.join(lines).split())
            current=None;lines=[]
        elif current:lines.append(line)
    if current:result[current]=' '.join(' '.join(lines).split())
    return result
old={};pins={}
for k,p in M['previous'].items():
    pr=Path(p['run']);c=json.loads((pr/'compilation.json').read_bytes());audit=Path(c['records'][-1]['stdout']);raw=audit.read_bytes()
    pins[k]={'path':str(audit),'sha256':sha(raw)};old.update(extract(raw.decode('utf-8')))
fresh=Path(C['records'][-1]['stdout']);typ=extract(fresh.read_text(encoding='utf-8'))
exact=set(typ)==set(M['declarations']);diff={n:{'before':old.get(n),'after':typ.get(n)} for n in M['declarations'] if old.get(n)!=typ.get(n)}
out={'timestamp':datetime.datetime.now().astimezone().isoformat(),'fresh_auditor_path':str(fresh),'fresh_auditor_sha256':sha(fresh.read_bytes()),'previous_auditors':pins,'exact_99_types':exact,'all_99_types_with_universes_equal_previous':not diff,'differences':diff,'fresh_types':typ,'no_extra_assumptions_in_auditor':(RUN/'sources/ClosedTomitaBatchAudit.lean').read_text(encoding='utf-8').count('#check ')==99,'all_99_axioms_trio':C['all_axioms_allowed']}
p=RUN/'type_comparison.json';assert not p.exists();raw=json.dumps(out,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.json.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
print(json.dumps({k:v for k,v in out.items() if k not in ['fresh_types','previous_auditors']},ensure_ascii=False,indent=2))
