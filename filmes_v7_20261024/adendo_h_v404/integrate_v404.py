"""Install verified candidate bytes locally; never render, finalize or publish."""
from context import *
import os,time,hashlib

def verify(row):
 p=Path(row.get('path',row.get('file','')));assert p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],str(p)

def checked_bytes(row):
 raw=Path(row.get('path',row.get('file',''))).read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'Pinned bytes changed'
 return raw

def create_new(path,value):
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.new_'+str(time.time_ns()))
 with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==raw;os.link(tmp,path);tmp.unlink();assert path.read_bytes()==raw

def baseline():
 result={}
 for file,first,second in [('DATA_BASELINE_MANIFEST.json','original','copy'),('MEDIA_V402_BACKUP.json','original','backup'),('baseline_audio_v402/BASELINE.json','source','backup')]:
  for row in read(H/file)['files']:
   p=Path(str(row[first]['path']).removeprefix('\\\\?\\'))
   if not p.is_relative_to(V):continue
   rel=p.relative_to(V).as_posix();old=result.get(rel)
   assert old is None or old['sha256']==row[first]['sha256']
   result[rel]=row[first]
 old_audio_pointer=read(E/'AUDIO_READY.json')['receipt'];verify(old_audio_pointer)
 audio=read(Path(old_audio_pointer['path']))
 for row in [audio['build'],*audio['media'],*audio['subtitles'],*audio['timelines']]:
  verify(row);p=Path(row['path']);rel=p.relative_to(V).as_posix()
  assert rel not in result or result[rel]['sha256']==row['sha256']
  result[rel]=row
 return result

def prepare():
 pf=check();stable_seal();b=baseline()
 assert not (H/'INTEGRATION.json').exists(),'Already integrated'
 if (H/'INTEGRATION_PLAN.json').exists():assert sha(H/'INTEGRATION_PLAN.json')==sha(H/'INTEGRATION_PLAN_R1.json'),'Recover changed plan'
 cmp=read(H/'NUMERIC_COMPARISON.json');assert not cmp['unexpected_differences']
 assert read(H/'PARENT_DATA_REVIEW.json')['status']=='PASS_WITH_SCOPE'
 assert read(S/'replay/TEST_BROWSER.json')['status']=='PASS'
 ar=read(H/'AUDIO_READY.json');assert ar['status']=='AUDIO_READY';verify(ar['receipt'])
 d=read(Path(ar['receipt']['path']));assert d['status']=='PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'
 for row in d['media_subtitles']:verify(row)
 source=[Path(x['isolated']['path']).relative_to(S).as_posix() for x in read(H/'SOURCE_CAPTURE.json')['files']]
 data=['data/'+x['file'] for x in cmp['files']]
 public=read(V/'replay/DELIVERY_C.json')['public_files']
 rels=source+data+public+['PROVENANCE_PUBLIC.json','extend_export.py','web/replay-trust.mjs']
 rels+=['replay/'+n for n in ['TEST_OFFLINE.json','TEST_BROWSER.json','BROWSER_OK.png','BROWSER_TAMPER.png']]
 rels+=['audio/'+n for n in ['build_narration.py','script_templates.json','NARRATION_PLAN_v404.json','NARRATION_BUILD.json']]
 rels += [p.relative_to(S).as_posix() for p in (S/'subs').rglob('*.vtt')]
 for film in ['film1','film2']:
  rels.append('data/'+film+'_narration_timeline.json')
  for lang in ['en','pt-BR']:
   for ext in ['wav','m4a']:rels.append(f'audio/{film}/{lang}.{ext}')
 # Cache is append-only. Copy only newly returned transport artifacts, never old keys.
 newkeys=[u['key'] for u in read(H/'AUDIO_PLAN.json')['new_units']]
 for key in newkeys:
  rels += [p.relative_to(S).as_posix() for p in (S/'audio/cache').glob(key+'*') if p.is_file()]
 rows=[]
 for rel in dict.fromkeys(rels):
  src=S/rel;dst=V/rel;assert src.is_file(),rel
  before=pin(dst) if dst.exists() else None
  if before:
   assert rel in b and before['sha256']==b[rel]['sha256'] and before['bytes']==b[rel]['bytes'],'Baseline CAS: '+rel
  rows.append({'relative':rel,'candidate':pin(src),'before':before,'changed':before is None or before['sha256']!=sha(src)})
 deps={n:pin(H/n) for n in ['AUDIO_READY.json','AUDIO_PLAN.json','NUMERIC_COMPARISON.json','PARENT_DATA_REVIEW.json','DATA_READY.json','SOURCE_CAPTURE.json','AUDIO_RESULT_REVIEW.json']}
 deps['candidate_audio_receipt']=ar['receipt']
 derived=[{'relative':n,'before':pin(V/n) if (V/n).exists() else None} for n in ['audit/DELIVERY_D_V404.json','replay/DELIVERY_ADENDO_H_V404.json','replay/DELIVERY_C.json']]
 assert derived[0]['before'] is None and derived[1]['before'] is None
 save(H/'INTEGRATION_PLAN.json',{'status':'PREPARED_ONLY','revision':'R2','source':'v404','source_sha256':sha(S/'source/um.py'),'preflight':pf,'files':rows,'derived_destinations':derived,'dependencies':deps,'source_rels':source,'data_rels':data,'replay_public':public,'candidate_audio':pin(H/'AUDIO_READY.json'),'candidate_audio_receipt':ar['receipt'],'scope':'Local data/replay/audio replacement; renderer, exported videos/images and final public manifest untouched.'})
 print(json.dumps({'status':'PREPARED_ONLY','files':len(rows),'changed':sum(x['changed'] for x in rows)}))

def apply():
 pf=check();stable_seal();plan=read(H/'INTEGRATION_PLAN.json');assert not (H/'INTEGRATION.json').exists(),'Already integrated'
 review=read(H/'INTEGRATION_REVIEW.json');assert review['status']=='PASS_WITH_SCOPE' and review['actor']!='codex-video-v7'
 assert review['plan_sha256']==sha(H/'INTEGRATION_PLAN.json') and review['installer_sha256']==sha(Path(__file__))
 dep={k:json.loads(checked_bytes(v)) for k,v in plan['dependencies'].items()}
 assert dep['AUDIO_RESULT_REVIEW.json']['status']=='PASS_WITH_SCOPE'
 raw_candidates={row['relative']:checked_bytes(row['candidate']) for row in plan['files']}
 for row in plan['files']:
  verify(row['candidate']);dst=V/row['relative'];assert (pin(dst) if dst.exists() else None)==row['before'],'Concurrent change'
 for row in plan['derived_destinations']:
  dst=V/row['relative'];assert (pin(dst) if dst.exists() else None)==row['before'],'Derived destination changed'
 stamp=str(time.time_ns());out=[]
 # Preserve all touched bytes before replacing any file.
 for row in plan['files']+plan['derived_destinations']:
  if row.get('changed',True) and row['before']:
   p=V/row['relative'];backup=p.with_name(p.name+'.bak_v402_'+stamp);raw=p.read_bytes();backup.write_bytes(raw);assert backup.read_bytes()==raw;row['backup']=pin(backup)
 stable_seal()
 for row in plan['files']:
  p=V/row['relative'];assert (pin(p) if p.exists() else None)==row['before']
  if row['changed']:
   p.parent.mkdir(parents=True,exist_ok=True);raw=raw_candidates[row['relative']];assert len(raw)==row['candidate']['bytes'] and hashlib.sha256(raw).hexdigest()==row['candidate']['sha256'];tmp=p.with_name(p.name+'.tmp_v404_'+stamp);tmp.write_bytes(raw);assert tmp.read_bytes()==raw and raw;os.replace(tmp,p)
  installed=pin(p);assert installed['sha256']==row['candidate']['sha256'] and installed['bytes']==row['candidate']['bytes'];out.append({**row,'installed':installed})
 stable_seal();create(H/'INTEGRATION.json',{'status':'PASS','source':'v404','source_sha256':plan['source_sha256'],'files':out,'derived_destinations':plan['derived_destinations'],'plan':pin(H/'INTEGRATION_PLAN.json'),'review':pin(H/'INTEGRATION_REVIEW.json'),'preflight':pf})
 cmp=dep['NUMERIC_COMPARISON.json'];approved={**cmp,'status':'PASS','builder_status':cmp['status'],'original_report':plan['dependencies']['NUMERIC_COMPARISON.json'],'distinct_review':plan['dependencies']['PARENT_DATA_REVIEW.json'],'scope':'Parent-accepted exact comparison; original builder report preserved.'};create(H/'NUMERIC_APPROVED.json',approved)
 ready={'status':'DATA_READY','source':'v404','source_sha256':plan['source_sha256'],'seal':pin(V/'source/um_absoluto_selo.json'),'comparison':pin(H/'NUMERIC_APPROVED.json'),'integration':pin(H/'INTEGRATION.json'),'unexpected_scientific_differences':0,'anchors':{'total':64,'all_ok':True},'source_files':[pin(V/n) for n in plan['source_rels']],'data_files':[pin(V/n) for n in plan['data_rels']],'root_provenance':pin(V/'PROVENANCE_PUBLIC.json')}
 assert len(read(V/'data/PROVENANCE_PUBLIC.json')['anchors'])==ready['anchors']['total']
 create(H/'MEDIA_DATA_READY.json',ready)
 parent={**dep['PARENT_DATA_REVIEW.json'],'data_ready_sha256':sha(H/'MEDIA_DATA_READY.json'),'files':[{'file':Path(n).name,'current_sha256':sha(V/n)} for n in plan['data_rels']]};create(H/'PARENT_NUMERIC_REVIEW.json',parent)
 # Project the builder's candidate receipt to the identical installed media, with attribution.
 d=dep['candidate_audio_receipt'];media=[];subtitles=[]
 for row in out:
  rel=row['relative']
  if rel.startswith('audio/film') and rel.endswith(('.wav','.m4a')):media.append(row['installed'])
  if rel.startswith('subs/') and rel.endswith('.vtt'):subtitles.append(row['installed'])
 assert len(media)==8 and len(subtitles)==26
 installed_d={**d,'candidate_receipt':plan['candidate_audio_receipt'],'parent_projection_actor':'codex-video-v7','integration':pin(H/'INTEGRATION.json'),'media':media,'subtitles':subtitles,'scope':'Byte-identical installed candidate; builder status retained, independent execution/plan review separately pinned.'}
 for row in plan['derived_destinations']:
  dst=V/row['relative'];assert (pin(dst) if dst.exists() else None)==row['before'],'Derived CAS before projection'
 create_new(V/'audit/DELIVERY_D_V404.json',installed_d)
 audio={**dep['AUDIO_READY.json'],'receipt':pin(V/'audit/DELIVERY_D_V404.json'),'integration':'INSTALLED_WITH_BYTE_VERIFICATION','production_modified':True};create(H/'MEDIA_AUDIO_READY.json',audio)
 publicpins=[{'path':n,'sha256':sha(V/n),'bytes':(V/n).stat().st_size} for n in plan['replay_public']]
 full=V/'replay/DELIVERY_ADENDO_H_V404.json';create_new(full,{'status':'PASS_WITH_SCOPE','source':'v404','source_sha256':plan['source_sha256'],'public_files':plan['replay_public'],'public_file_pins':publicpins,'data_review':plan['dependencies']['PARENT_DATA_REVIEW.json'],'browser':pin(V/'replay/TEST_BROWSER.json'),'offline':pin(V/'replay/TEST_OFFLINE.json'),'integration':pin(H/'INTEGRATION.json'),'scope':'Numerical replay only; no new Lean proof or nature test.'})
 fixed=V/'replay/DELIVERY_C.json';old=pin(fixed);assert old==next(x['before'] for x in plan['derived_destinations'] if x['relative']=='replay/DELIVERY_C.json'),'Pointer CAS before replace'
 save(fixed,{'schema':'tgl.replay-current-pointer.v1','status':'CURRENT_V404_POINTER','source':'v404','source_sha256':plan['source_sha256'],'full_receipt':{'path':full.relative_to(V).as_posix(),'sha256':sha(full),'bytes':full.stat().st_size},'public_files':plan['replay_public'],'public_file_pins':publicpins,'_private_history':{'previous_fixed_receipt':old,'previous_source':'v402'}})
 stable_seal();print(json.dumps({'status':'INSTALLED_LOCALLY','files':len(out),'changed':sum(x['changed'] for x in out),'media':len(media),'subtitles':len(subtitles)}))

if __name__=='__main__':
 import sys
 {'prepare':prepare,'apply':apply}[sys.argv[1]]()
