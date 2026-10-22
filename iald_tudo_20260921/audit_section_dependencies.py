"""Map literal references affected by a proposed section replacement; no edits."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def child(path, key):
    return path + '/' + str(key).replace('~','~0').replace('/','~1')
def resolve(document, path):
    for part in path.split('/')[1:]:
        key = part.replace('~1','/').replace('~0','~')
        document = document[int(key)] if isinstance(document,list) else document[key]
    return document

raw = (WORK/'haiku_candidate.md').read_bytes()
receipt = json.loads((WORK/'haiku_candidate.json').read_bytes())
assert sha(raw) == receipt['sha256']
manifest = json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
entry = next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw = Path(entry['path']).read_bytes()
assert sha(source_raw) == entry['public_sha256']
source = json.loads(source_raw)
text = raw.decode()
marker = '\n## Exposição canônica integral: fórmulas e derivações'
exposition = text.split(marker,1)[1][:receipt['exposition_chars']]
assert sha(exposition.encode()) == receipt['exposition_sha256']
heading = re.search(r'(?m)^## A FORMA CANONICA VIVA[^\n]*',exposition)
assert heading
next_heading = re.search(r'(?m)^## ',exposition[heading.end():])
start = heading.start()
end = heading.end()+next_heading.start() if next_heading else len(exposition)
section = exposition[start:end]
rows = []

def walk(node, pointer, topic_id, topic_pointer):
    if isinstance(node,dict):
        if '@EXPOSITION' in node:
            offset, length = node['span']
            value = exposition[offset:offset+length]
            assert value == resolve(source,pointer)
            if offset < end and offset+length > start:
                assert start <= offset and offset+length <= end, 'Reference crosses section boundary'
                labels = list(re.finditer(r'(?m)^\*\*Estatutos \[([^\]]+)\]',exposition[start:offset]))
                label = labels[-1][1] if labels else None
                rows.append({'topic':topic_id,'source_pointer':pointer,'span':[offset,length],
                             'section_block':label,'literal':value,'literal_sha256':sha(value.encode())})
            return
        if '@' in node:
            for suffix,value in node.get('fields',{}).items():
                walk(value,topic_pointer+node['@']+suffix,topic_id,topic_pointer)
            return
        if '@TGL_LITERAL' in node:
            return
        for key,value in node.items():
            walk(value,child(pointer,key),topic_id,topic_pointer)
    elif isinstance(node,list):
        for index,value in enumerate(node):
            walk(value,child(pointer,index),topic_id,topic_pointer)

matches = list(re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)',text))
assert len(matches)==325
for match in matches:
    walk(json.loads(match[3]),match[2],match[1],match[2])
result = {'status':'DEPENDENCY_AUDIT_ONLY', 'candidate_sha256':sha(raw),
          'source_sha256':sha(source_raw),'exposition_sha256':sha(exposition.encode()),
          'section_sha256':sha(section.encode()),'section_span':[start,end-start],
          'affected_references':len(rows),'affected_topics':len({r['topic'] for r in rows}),
          'affected_blocks':len({r['section_block'] for r in rows}),
          'references_without_named_block':sum(r['section_block'] is None for r in rows),
          'references':rows,
          'requirement':'Do not retain old @EXPOSITION spans after replacing this section. Re-resolve literals or explicitly mark reviewed semantic summaries; never assert exact equivalence for paraphrases.'}
target = WORK/('section_dependencies_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with target.open('xb') as stream:
    stream.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({**{k:v for k,v in result.items() if k!='references'},'receipt':str(target)},ensure_ascii=False))
