"""Integrate one explicitly reviewed section into a NEW, undeployed draft."""
from pathlib import Path
from datetime import datetime
import json,re,hashlib
from verify_reviewed_draft import verify
from remap_exposition_refs import remap
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
parent=W/'haiku_reviewed_compact_evidence_20260922_122038_339588.md'
verify(parent)
raw=parent.read_bytes();text=raw.decode()
provenance=W/'section_capsules/provenance_v2.json';d=json.loads(provenance.read_bytes())
capsule_path=W/'section_capsules/form_canonica_viva_v2.md';capsule_raw=capsule_path.read_bytes();capsule=capsule_raw.decode()
review_path=W/'adversarial_memory_review/canonical_section_v2_review_20260922_130651.json';review_raw=review_path.read_bytes();review=json.loads(review_raw)
assert review['status']=='APPROVED_DOCUMENTARY_FIDELITY_ONLY'
assert sha(capsule_raw)==d['capsule_sha256']==review['capsule_sha256']
base=json.loads((W/'haiku_candidate.json').read_bytes())
marker='\n## Exposição canônica integral: fórmulas e derivações'
expo_start=text.index(marker)+len(marker)
old_expo=text[expo_start:expo_start+base['exposition_chars']]
old_section=d['original_section_text']
assert old_expo.count(old_section)==1
section_start=old_expo.index(old_section)
new_expo=old_expo.replace(old_section,capsule,1)
replacements=[];references=[]
pattern=r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)'
for m in list(re.finditer(pattern,text)):
 try:node=json.loads(m[3])
 except json.JSONDecodeError:continue # separately reviewed prose capsules
 value,changes=remap(node,old_expo,new_expo,d['blocks'],section_start,m[2])
 if not changes:continue
 before=m[0];after=before[:-len(m[3])]+json.dumps(value,ensure_ascii=False,separators=(',',':'))
 replacements.append({'before':before,'after':after})
 references.extend(changes)
assert text.count(old_expo)==1
text=text.replace(old_expo,new_expo,1)
for r in replacements:
 assert text.count(r['before'])==1
 text=text.replace(r['before'],r['after'],1)
old_header='É referência interna a conteúdo carregado, não consulta externa nem omissão.\n'
new_header=old_header+'@SUMMARY indica síntese semântica do bloco Estatutos [id] carregado; não é citação literal. span aponta ao bloco sintetizado na exposição; source_pointer identifica o campo integral em resultado_publicado_integral para consulta. A revisão documental não certifica prova matemática nem execução.\n'
assert text.count(old_header)==1
text=text.replace(old_header,new_header,1)
payload=text.encode()
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');out=W/('haiku_reviewed_section_'+stamp+'.md')
receipt={'status':'REVIEWED_SECTION_DRAFT_NOT_DEPLOYED','sha256':sha(payload),'path':str(out),
 'parent_path':str(parent),'parent_sha256':sha(raw),'section_compaction':True,
 'capsule_path':str(capsule_path),'capsule_sha256':sha(capsule_raw),
 'provenance_path':str(provenance),'provenance_sha256':sha(provenance.read_bytes()),
 'review_path':str(review_path),'review_sha256':sha(review_raw),
 'old_exposition_sha256':sha(old_expo.encode()),'new_exposition_sha256':sha(new_expo.encode()),
 'old_exposition_chars':len(old_expo),'new_exposition_chars':len(new_expo),
 'replacements':replacements,'header_change':{'before':old_header,'after':new_header},
 'literal_refs':sum('@EXPOSITION' in x['after'] for x in references),
 'summary_refs':sum('@SUMMARY' in x['after'] for x in references),
 'anthropic_tokens':None,'scope':'Only declared section and reference changes; not full corpus approval.'}
with out.open('xb')as f:f.write(payload)
with out.with_suffix('.json').open('xb')as f:f.write((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
assert parent.read_bytes()==raw
print(json.dumps({k:receipt[k] for k in ['status','path','sha256','literal_refs','summary_refs']}))
