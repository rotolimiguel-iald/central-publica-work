import sys,json,hashlib
from pathlib import Path
from unittest.mock import patch
A=Path(r'C:\IALD\Central de Patentes\work\iald_v410_20261111')
W=Path(__file__).parent
R=A/'app/R4/runtime';U=A/'app/R4/continuous_update'
sys.path[:0]=[str(R),r'C:\IALD\projetos_pyhton\IALD',str(U)]
from iald_science_snapshot import ScienceSnapshot
manifest=A/'app/R4/release_final/release.json'
s=ScienceSnapshot.capture(manifest)
checks=[]
def ok(name,value):
 assert value,name
 checks.append(name)
ok('unit_ids_unique',len({u['id'] for u in s._units})==len(s._units))
for ident,doc in s._documents.items():
 text=doc['text']; parts=[];off=0
 while True:
  page=s.fetch(ident,off,49999);parts.append(page['text'])
  if page['next_offset'] is None:break
  off=page['next_offset']
 ok('full_document_'+ident,hashlib.sha256(''.join(parts).encode()).hexdigest()==doc['sha256'])
 sections=sorted([u for u in s._units if u['document_id']==ident and 'start_char' in u],key=lambda u:u['start_char'])
 if sections:ok('sections_'+ident,sections[0]['start_char']==0 and sections[-1]['end_char']==len(text) and all(a['end_char']==b['start_char'] for a,b in zip(sections,sections[1:])) and ''.join(u['text'] for u in sections)==text)
topics=[u for u in s._units if 'json_pointer' in u]
original=json.loads(s._documents[topics[0]['document_id']]['text'])['core']
ok('all_topics',len(topics)==len(original))
for u in topics:
 key=u['json_pointer'].removeprefix('/core/').replace('~1','/').replace('~0','~')
 assert json.loads(u['text'])=={'core':{key:original[key]}}
ok('all_topics_exact',True)
with patch.object(Path,'read_bytes',side_effect=AssertionError('Snapshot read disk after capture')):
 s.routing_memory();s.search('H3');s.catalog.verification()
 d=next(iter(s._documents))
 for text in ('H3',f'fetch_tgl {d} 0'):
  receipt=s.pre_retrieve([{'role':'user','content':text}])['receipt']
  ok('global_statutes_'+text,receipt['units'][0]['id']=='result_global_statutes' and receipt['units'][0]['whole_unit'])
 s.pre_retrieve([{'role':'user','content':'H3'}],max_bytes=20000)
 ok('no_fs_after_capture',True)
 try:s.pre_retrieve([{'role':'user','content':'H3'}],max_bytes=1)
 except ValueError:ok('mandatory_overflow_refused',True)
 else:raise AssertionError('mandatory truncation')
result={'status':'PASS_NARROW_OFFLINE_NOT_FINAL_ACCEPT','checks':checks,'documents':len(s._documents),'units':len(s._units),'topics':len(topics),'identity':s.check(),'prefix_bytes':len(s.prefix.encode()),'native_prefix_bytes':len(s.native_prefix.encode()),'snapshot_sha256':hashlib.sha256((R/'iald_science_snapshot.py').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
output=W/'reviewer_snapshot_final_r4.json'
assert not output.exists()
output.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode())
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
