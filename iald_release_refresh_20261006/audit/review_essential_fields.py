"""Independent presence check for source-verified essential semantics."""
from pathlib import Path
import json
import review_memory as r
from review_sources import save, walk

m=r.load(r.STAGE/'manifest_staged.json')
source=r.load(m['published_evidence']['result']['path'])
essentials=r.load(r.WORK/'audit/essential_semantics_review.json')['critical_fields']
surfaces={}
for name,marker in [('TGL_CLUSTER_v389.md','DICIONÁRIO DO CLUSTER'),('haiku_prefix.md','DICIONÁRIO DE LITERAIS')]:
    text=r.read(r.STAGE/name).decode('utf8')
    dictionary=r.loads(text.split(marker+'\n',1)[1].split('\n',1)[0])
    if 'DICIONÁRIO DE INDICADORES LITERAIS\n' in text:
        r.BOOLEAN_DICTIONARY.update(r.loads(text.split('DICIONÁRIO DE INDICADORES LITERAIS\n',1)[1].split('\n',1)[0]))
    expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    topics=r.topics(text,source['core'])
    represented={}
    for topic in {row['pointer'].split('/')[2] for row in essentials}:
        body=topics[topic]
        seen={}
        for line in body.splitlines():
            if not line.startswith('{'):
                continue
            node=r.decode(r.loads(line),dictionary,expo,source)
            pointer='/core/'+topic
            r.reconstruct(node,source,pointer,pointer,seen)
        represented.update(seen)
    results=[]
    for row in essentials:
        pointer=row['pointer'];value=r.resolve(source,pointer)
        assert r.same(value,row['value']),pointer
        results.append({'pointer':pointer,'fully_inline':r.covered(pointer,value,represented), 'missing_leaves':[{'pointer':p,'value':v} for p,v in walk(value,pointer) if not r.covered(p,v,represented)]})
    surfaces[name]={'passed':sum(x['fully_inline'] for x in results),'total':len(results),
                    'not_fully_inline':[x['pointer'] for x in results if not x['fully_inline']], 'fields':results}
stable=all(r.sha(Path(p).read_bytes())==v['sha256'] for p,v in r.inputs.items())
report={'status':'PASS' if stable and all(x['passed']==x['total'] for x in surfaces.values()) else 'REVIEW_MISSING',
        'scope':'Presence of exact values in active context after independent dictionary/span decoding. References to external JSON alone are not counted as inline.',
        'inputs_stable':stable,'surfaces':surfaces,'input_pins':r.inputs}
save('essential_fields_result.json',report)
print(json.dumps({'status':report['status'],'surfaces':{k:{'passed':v['passed'],'total':v['total'],'not_fully_inline':v['not_fully_inline']} for k,v in surfaces.items()}},ensure_ascii=False))
