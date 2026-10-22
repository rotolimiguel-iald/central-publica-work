"""Independent provenance checks for the manually reviewed 65-block proposal.

The reviewer has compared every original block and capsule in the tool transcript.
This script checks anchoring; it does not infer semantic approval from hashes.
"""
from pathlib import Path
from datetime import datetime
import hashlib,json,re,sys
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def resolve(obj,pointer):
 for part in pointer.split('/')[1:]:
  key=part.replace('~1','/').replace('~0','~')
  obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 return obj

v2='--v2' in sys.argv
d=json.loads((WORK/('section_capsules/provenance_v2.json' if v2 else 'section_capsules/provenance.json')).read_bytes())
capsule=(WORK/('section_capsules/form_canonica_viva_v2.md' if v2 else 'section_capsules/form_canonica_viva.md')).read_bytes()
require(sha(capsule)==d['capsule_sha256'],'Capsule drift')
original=d['original_section_text']
require(sha(original.encode())==d['original_section_sha256'],'Original drift')
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
entry=next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
source_raw=Path(entry['path']).read_bytes()
require(sha(source_raw)==entry['public_sha256']==d['source_result_sha256'],'Source drift')
source=json.loads(source_raw);text=capsule.decode();field_count=0
require(len(d['blocks'])==65,'Expected 65 reviewed blocks')
require(len({b['id'] for b in d['blocks']})==65,'Duplicate block')
for b in d['blocks']:
 a=b['original_section_coordinates'];c=b['new_capsule_coordinates']
 old=original[a['unicode_start']:a['unicode_end_exclusive']]
 new=text[c['unicode_start']:c['unicode_end_exclusive']]
 require(sha(old.encode())==b['original_block_sha256'],'Old block drift')
 require(sha(new.encode())==b['new_block_sha256'],'New block drift')
 require(new.startswith('**Estatutos ['+b['id']+']**'),'Wrong target block')
 node=resolve(source,b['source_pointer'])
 require(node['verdict']==b['source_verdict_literal'],'Verdict provenance changed')
 keys=[]
 for f in b['source_fields']:
  value=resolve(source,f['source_pointer'])
  require(isinstance(value,str),'Non-string source field')
  require(sha(value.encode())==f['original_literal_sha256'],'Field provenance changed')
  require('`'+f['key']+'`: '+value in old,'Field absent in full original')
  keys.append(f['key']);field_count+=1
 require(set(keys)==set(node['statuses']),'Source statuses missing from mapping')
require(field_count==256,'Expected all 256 fields')
if v2:
 # Only the manually inspected changes may distinguish V2 from reviewed V1.
 previous=(WORK/'section_capsules/form_canonica_viva.md').read_text(encoding='utf8')
 for c in d['corrections']:
  require(previous.count(c['old_literal'])==1,'Ambiguous V2 correction')
  previous=previous.replace(c['old_literal'],c['new_literal'],1)
  for anchor in c['source_evidence']:
   require(resolve(source,anchor['pointer'])==anchor['literal'],'Additional primary anchor mismatch')
 require(previous==text,'Unreviewed V2 modification')
result={'status':'CHANGES_REQUIRED_AFTER_MANUAL_REVIEW',
 'capsule_sha256':sha(capsule),'source_sha256':sha(source_raw),'original_sha256':sha(original.encode()),
 'reviewed_blocks':65,'source_fields_verified':field_count,
 'scope':'Documentary condensation fidelity only. No Lean compilation, scientific proof or full corpus validation.',
 'findings':[
 {'id':'R1','block':'continuous_modular_zero','required':'Restore resistance_beta interpretation: pair(1_abs,0_mod) pays beta_TGL not to fall to absolute zero, with original DER/NUM and ONTO scope.'},
 {'id':'R2','block':'certificate_II','required':'Restore certificate IV pre-registration in the referenced round, not just protocol.'},
 {'id':'R3','block':'semifinite_weight/fused_witness','required':'Attribute historical phrase no semifinite weight to source; avoid promoting it as a classification without resolving trace/weight types.'},
 {'id':'R4','block':'the_wedge_net','required':'Anchor extra TGLSpecificAQFTWitness/M_TGL names to primary source fields or remove unsupported additions.'}],
 'integration_requirements':['Remap all 61 affected @EXPOSITION references; paraphrase is not literal equivalence.','Preserve full kernel/core and 325-topic coverage.','Recount Haiku native wire including tools/output before deployment.']}
if v2:
 result['status']='APPROVED_DOCUMENTARY_FIDELITY_ONLY'
 result['findings_resolved']=result.pop('findings')
 result['limits']=['No global corpus approval or proof certification.','Historical weight classification precision remains explicitly pending.','No operational retrieval or native API fit certified.']
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
p=WORK/'adversarial_memory_review'/('canonical_section_'+('v2' if v2 else 'v1')+'_review_'+stamp+'.json')
with p.open('xb')as out:out.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':result['status'],'blocks':65,'fields':field_count,'receipt':str(p)}))
