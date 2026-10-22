"""Integrate independently approved runtime synthesis and re-anchor every JSON reference."""
from pathlib import Path
from datetime import datetime
import hashlib,json,sys
from verify_reviewed_draft import verify
from remap_reviewed_interval import remap_interval
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
parent=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else W/'haiku_reviewed_topics_v4_20260922_134657_144992.md'
verify(parent);raw=parent.read_bytes();text=raw.decode()
directory=W/'runtime_synthesis_proposal_20260922_133458_573933'
review_path=directory/'review_v2_20260922_164227_718922.json'
review_raw=review_path.read_bytes();review=json.loads(review_raw)
assert review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL' and not review['remaining_required_changes']
original=(directory/'original.md').read_bytes();capsule=(directory/'capsule_v2.md').read_bytes()
assert sha(original)==review['pins']['original.md']['sha256']
assert sha(capsule)==review['pins']['capsule_v2.md']['sha256']
base=W/'haiku_reviewed_section_20260922_130747_311801.md'
base_record=json.loads(base.with_suffix('.json').read_bytes())
marker='\n## Exposição canônica integral: fórmulas e derivações'
expo_start=text.index(marker)+len(marker)
old_expo=text[expo_start:expo_start+base_record['new_exposition_chars']]
assert sha(old_expo.encode())==base_record['new_exposition_sha256']
assert old_expo.count(original.decode())==1
start=old_expo.index(original.decode());old_length=len(original.decode())
heading,body=capsule.decode().split('\n',1)
label='**Estatutos [runtime_synthesis]**'
replacement=heading+'\n\n'+label+'\n'+body.lstrip('\n')
new_expo=old_expo[:start]+replacement+old_expo[start+old_length:]
summary_start=start+replacement.index(label)
summary_span=[summary_start,len(replacement)-replacement.index(label)]
lines=[];reference_changes=[];pointer=''
for line in text.splitlines(keepends=True):
    if line.startswith('Fonte: resultado_publicado_integral '):
        pointer=line.split('Fonte: resultado_publicado_integral ',1)[1].strip()
    try:node=json.loads(line)
    except (ValueError,TypeError):continue
    changed,changes=remap_interval(node,old_exposition=old_expo,new_exposition=new_expo,
        start=start,old_length=old_length,replacement=replacement,summary_id='runtime_synthesis',
        summary_span=summary_span,source_pointer=pointer)
    if changes:
        nl='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
        after=json.dumps(changed,ensure_ascii=False,separators=(',',':'))+nl
        lines.append({'before':line,'after':after});reference_changes.extend(changes)
text=text.replace(old_expo,new_expo,1)
for r in lines:
    assert text.count(r['before'])==1
    text=text.replace(r['before'],r['after'],1)
result=text.encode();assert parent.read_bytes()==raw
out=W/('haiku_reviewed_runtime_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.md')
record={'status':'REVIEWED_RUNTIME_DRAFT_NOT_DEPLOYED','runtime_synthesis_compaction':True,
 'sha256':sha(result),'parent_path':str(parent),'parent_sha256':sha(raw),
 'review_path':str(review_path),'review_sha256':sha(review_raw),
 'original_path':str(directory/'original.md'),'original_sha256':sha(original),
 'capsule_path':str(directory/'capsule_v2.md'),'capsule_sha256':sha(capsule),
 'replacement':replacement,'section_start':start,'old_length':old_length,
 'old_exposition_chars':len(old_expo),'new_exposition_chars':len(new_expo),
 'old_exposition_sha256':sha(old_expo.encode()),'new_exposition_sha256':sha(new_expo.encode()),
 'reference_lines':lines,'reference_changes':reference_changes,'summary_span':summary_span,
 'anthropic_tokens':None,'scope':'One approved documentary summary; no new formal proof or API-fit assertion.'}
with out.open('xb')as f:f.write(result)
with out.with_suffix('.json').open('xb')as f:f.write(json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps({'path':str(out),'sha256':sha(result),'remapped_references':len(reference_changes)}))
