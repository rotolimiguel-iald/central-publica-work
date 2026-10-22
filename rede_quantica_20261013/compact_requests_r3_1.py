"""Replace never-submitted drafts after a local preview size refusal."""
import datetime as dt
import json
import sqlite3
import uuid
from prepare_requests_r3 import DEST,BASE,F,ML,bundle
from diary_r1 import ROOT,OUT,WORK,claim,new,pin

claim()
common=[
 ('BosonicTwoParticle.lean',F/'BosonicTwoParticle.lean',1,38),
 ('BosonicSectors.lean',F/'BosonicSectors.lean',1,55),
 ('BosonicSectors.lean',F/'BosonicSectors.lean',91,119),
 ('BosonicSectors.lean',F/'BosonicSectors.lean',154,166),
 ('BosonicSectors.lean',F/'BosonicSectors.lean',188,213),
 ('SectorDirectSum.lean',F/'SectorDirectSum.lean',1,77),
 ('BosonicFock.lean',F/'BosonicFock.lean',1,55),
 ('TheImportedSecondQuantization.lean',ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt/TheImportedSecondQuantization.lean',86,100),
]
db=sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)
rows=[]
for provider in ('mimo','deepseek'):
 oldpath=DEST/f'REQUEST_{provider.upper()}_R3.json';old=json.loads(oldpath.read_text(encoding='utf-8'))
 for table in ('coordination_jobs','tasks'):
  assert not db.execute(f'SELECT id FROM {table} WHERE request_id=?',(old['request_id'],)).fetchone()
 spec=common.copy()
 if provider=='mimo':
  spec += [('Mathlib/Analysis/InnerProductSpace/TensorProduct.lean',ML/'Analysis/InnerProductSpace/TensorProduct.lean',48,83),('Mathlib/Analysis/InnerProductSpace/TensorProduct.lean',ML/'Analysis/InnerProductSpace/TensorProduct.lean',137,151)]
 else:
  spec += [('CanonicalWedge.lean',OUT/'modular_wedge/CanonicalWedge.lean',29,44),('Mathlib/LinearAlgebra/TensorProduct/Basic.lean',ML/'LinearAlgebra/TensorProduct/Basic.lean',84,139),('Mathlib/Analysis/Normed/Operator/Extend.lean',ML/'Analysis/Normed/Operator/Extend.lean',311,344)]
 pins,body=bundle(spec)
 prompt=old['prompt'].split('PINNED SCIENTIFIC SOURCE EXCERPTS')[0]+'The excerpts below deliberately include the definitions and necessary APIs, not every proof from R2. Omitted R2 proofs were independently compiled; their statements are dependencies, not new axioms. Full source files remain pinned locally. Do not treat an incomplete excerpt as a complete file.\n\nPINNED SCIENTIFIC SOURCE EXCERPTS:\n'+body
 assert len(prompt)<=24000,(provider,len(prompt))
 rid=str(uuid.uuid4());payload={**old,'prompt':prompt,'request_id':rid}
 path=DEST/f'REQUEST_{provider.upper()}_R3_1.json';new(path,payload)
 sp=DEST/f'SOURCES_{provider.upper()}_R3_1.json';new(sp,{'request_id':rid,'sources':pins})
 new(BASE/'state/session_requests'/f'{rid}.json',{'protocol':'iald-session-request/v1','request_id':rid,'house':'Central de Patentes / IALD','session_id':'01a11878-6e36-7d10-83c4-cd72e757fdd0','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'payload':pin(path),'execution_constraints':payload['execution_constraints'],'state':'prepared_not_submitted','supersedes_unsubmitted_draft':old['request_id']})
 rows.append({'provider':provider,'request_id':rid,'superseded_unsubmitted_request_id':old['request_id'],'payload':pin(path),'sources':pin(sp),'prompt_chars':len(prompt),'state':'PREPARED_NOT_SUBMITTED'})
db.close()
new(DEST/'DRAFT_SUPERSESSION_R3_1.json',{'reason':'MiMo local preview refused input >24000 chars before any queue registration or provider call. DeepSeek original was not previewed or submitted. Both complete drafts retained, compact scientific excerpts prepared for admission. Old IDs checked absent in tasks and coordination_jobs; never submit them.','repeats_execution':False,'units':rows})
print(json.dumps({'prepared':[{'provider':x['provider'],'request_id':x['request_id'],'prompt_chars':x['prompt_chars']} for x in rows]}))
