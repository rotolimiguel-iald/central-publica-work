"""Independent reversal of the declared section changes, plus reference checks."""
from pathlib import Path
import json,hashlib,re
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def verify_section(path):
 from verify_reviewed_draft import verify
 path=Path(path);raw=path.read_bytes();d=json.loads(path.with_suffix('.json').read_bytes())
 need(sha(raw)==d['sha256'],'Draft drift')
 parent=Path(d['parent_path']);need(parent.parent==W,'Unexpected parent')
 parent_record=json.loads(parent.with_suffix('.json').read_bytes());need(not parent_record.get('section_compaction'),'Nested section changes unsupported')
 verify(parent);parent_raw=parent.read_bytes();need(sha(parent_raw)==d['parent_sha256'],'Parent drift')
 capsule_path=Path(d['capsule_path']);need(capsule_path.parent==W/'section_capsules','Unexpected capsule')
 capsule=capsule_path.read_bytes();need(sha(capsule)==d['capsule_sha256'],'Capsule drift')
 review_path=Path(d['review_path']);need(review_path.parent==W/'adversarial_memory_review','Unexpected review')
 review_raw=review_path.read_bytes();need(sha(review_raw)==d['review_sha256'],'Review drift')
 review=json.loads(review_raw);need(review['status']=='APPROVED_DOCUMENTARY_FIDELITY_ONLY' and review['capsule_sha256']==sha(capsule),'Approval mismatch')
 p=Path(d['provenance_path']);need(p.parent==W/'section_capsules','Unexpected provenance')
 prov_raw=p.read_bytes();need(sha(prov_raw)==d['provenance_sha256'],'Provenance drift');prov=json.loads(prov_raw)
 need(review['source_sha256']==prov['source_result_sha256'],'Review source mismatch')
 text=raw.decode();marker='\n## Exposição canônica integral: fórmulas e derivações'
 start=text.index(marker)+len(marker);expo=text[start:start+d['new_exposition_chars']]
 need(sha(expo.encode())==d['new_exposition_sha256'],'Exposition drift')
 need(expo.count(capsule.decode())==1,'Reviewed capsule absent')
 refcounts={'literal':0,'summary':0}
 def walk(v):
  if isinstance(v,list):
   for x in v:walk(x)
  elif isinstance(v,dict):
   if '@EXPOSITION' in v or '@SUMMARY' in v:
    a,n=v['span'];need(0<=a<a+n<=len(expo),'Bad span');fragment=expo[a:a+n]
    if '@SUMMARY' in v:
     need(fragment.startswith('**Estatutos ['+v['@SUMMARY']+']**'),'Wrong summary target')
     need('\n**Estatutos [' not in fragment,'Summary crosses block')
     need(v['source_pointer'].startswith('/core/'),'Missing source field');refcounts['summary']+=1
    else:need(fragment.startswith(v['starts_with']),'Wrong literal target');refcounts['literal']+=1
   else:
    for x in v.values():walk(x)
 for m in re.finditer(r'(?m)^### [^\n]+\nFonte: resultado_publicado_integral [^\n]+\n([^\n]+)',text):
  try:node=json.loads(m[1])
  except json.JSONDecodeError:continue
  walk(node)
 need(refcounts=={'literal':d['literal_refs'],'summary':d['summary_refs']},'Reference counts differ')
 # Undo reference edits, header and section; exact equality guards ALL other content.
 for r in d['replacements']:
  need(text.count(r['after'])==1,'Ambiguous JSON change')
  text=text.replace(r['after'],r['before'],1)
 h=d['header_change'];need(text.count(h['after'])==1,'Header change missing');text=text.replace(h['after'],h['before'],1)
 text=text.replace(capsule.decode(),prov['original_section_text'],1)
 need(text.encode()==parent_raw,'Undeclared change outside approved section and references')
 need(path.read_bytes()==raw and parent.read_bytes()==parent_raw,'Concurrent change')
 return {'status':'SECTION_INTEGRATION_VERIFIED_NOT_DEPLOYED','draft_sha256':sha(raw),
 'parent_sha256':sha(parent_raw),'all_other_parent_bytes_preserved':True,'references':refcounts,
 'scope':'Byte preservation and internal reference integrity; documentary review only, not proof or API fit.'}
