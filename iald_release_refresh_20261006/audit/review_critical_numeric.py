"""Check only the ten previously identified fields, in both active surfaces."""
from pathlib import Path
import json
from datetime import datetime, timezone
import review_memory as r
from review_sources import save

S=r.STAGE
m=r.load(S/'manifest_staged.json')
source=r.load(m['published_evidence']['result']['path'])
previous=r.load(r.WORK/'audit/critical_numeric_review.json')
minimum=previous['minimum_source_fields']
surfaces={}
for filename,marker in [('TGL_CLUSTER_v389.md','DICIONÁRIO DO CLUSTER'),('haiku_prefix.md','DICIONÁRIO DE LITERAIS')]:
    text=r.read(S/filename).decode('utf8')
    dic=r.loads(text.split(marker+'\n',1)[1].split('\n',1)[0])
    expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    if 'DICIONÁRIO DE INDICADORES LITERAIS\n' in text:
        r.BOOLEAN_DICTIONARY.update(r.loads(text.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0]))
    topics=r.topics(text,source['core']);seen={}
    for name in {x['pointer'].split('/')[2] for x in minimum}:
        p='/core/'+name
        for line in topics[name].splitlines():
            if line.startswith('{'):
                value=r.decode(r.loads(line),dic,expo,source)
                r.reconstruct(value,source,p,p,seen)
    checks=[]
    for row in minimum:
        p=row['pointer'];actual=r.resolve(source,p)
        checks.append({'pointer':p,'value':actual,'passed':r.same(row['value'],actual) and r.covered(p,actual,seen)})
    surfaces[filename]={'sha256':r.sha(text.encode()),'checks':checks,'passed':all(x['passed'] for x in checks)}
stable=all(r.sha(Path(p).read_bytes())==pin['sha256'] for p,pin in r.inputs.items())
report={'status':'PASS' if stable and all(s['passed'] for s in surfaces.values()) else 'CHANGES_REQUIRED',
 'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'prefix_sha256':surfaces['haiku_prefix.md']['sha256'],
 'scope':'Ten essential numerical and negative qualifier fields, exact source values, not entire historical parents.',
 'minimum_source_fields':minimum,'surfaces':surfaces,'inputs_stable':stable,'input_pins':r.inputs,
 'previous_report_sha256':r.inputs[str(r.WORK/'audit/critical_numeric_review.json')]['sha256']}
save('critical_numeric_review.json',report)
print(json.dumps({'status':report['status'],'surfaces':{k:v['passed'] for k,v in surfaces.items()},'missing':[x['pointer'] for s in surfaces.values() for x in s['checks'] if not x['passed']]}))
