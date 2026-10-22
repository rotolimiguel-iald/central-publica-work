from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent
p=W/'haiku_count_candidate_v2.md';m=json.loads((W/'manifest_install.json').read_bytes());source=json.loads(Path(m['published_evidence']['result']['path']).read_bytes())
text=p.read_text(encoding='utf-8');parts=text.split('\n### ');out=[parts[0]];saved=0;changes=[]
for block in parts[1:]:
 lines=block.split('\n');key=lines[0]
 if key in source['core'] and saved<5400:
  for i,line in enumerate(lines[1:],1):
   if not line.startswith('{'):continue
   try:v=json.loads(line)
   except ValueError:continue
   checks=v.get('checks')
   if isinstance(checks,list) and checks and all(isinstance(x,list) and len(x)==2 and x[1] is True for x in checks):
    assert checks==source['core'][key]['checks'];v['checks']={'@':'/checks','items':len(checks)};new=json.dumps(v,ensure_ascii=False,separators=(',',':'));saving=len(line.encode())-len(new.encode())
    if saving>0:lines[i]=new;saved+=saving;changes.append({'topic':key,'source_pointer':'/core/'+key+'/checks','count':len(checks),'all_true':True,'bytes_saved':saving})
    break
 out.append('\n'.join(lines))
new='\n### '.join(out)
# This sentence is deployment metadata added by the earlier builder, not primary source text.
old='conferir o estado da publicação v368 carregado antes de descrevê-los como pendências atuais'
replacement='conferir o estado da publicação v378 carregado antes de descrevê-los como pendências atuais'
metadata_changes=new.count(old);new=new.replace(old,replacement)
aliases={'@SOURCE_FIELDS':'@F','@SOURCE_ITEMS':'@I','@TGL_LITERAL':'@L'}
original_codec=new
for long,short in aliases.items():
 assert short+'\"' not in new
 new=new.replace(long,short)
restored=new
for long,short in aliases.items():restored=restored.replace(short,long)
assert restored==original_codec
assert '<ATLAS_CANONICO' not in new
for name in ('mother_instruction','operational_core'):assert Path(m[name]['path']).read_text(encoding='utf-8-sig') in new
q=W/'haiku_count_candidate_final.md';assert not q.exists();raw=new.encode();q.write_bytes(raw);assert q.read_bytes()==raw
r={'metadata_aliases':aliases,'metadata_alias_roundtrip_verified':True,'base_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'prefix_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'removed_only_all_true_audit_check_labels':changes,'bytes_saved':saved,'metadata_version_corrections':metadata_changes,'fixed_sources_intact':True,'all_topics_preserved':True};(W/'haiku_final_delta.json').write_bytes(json.dumps(r,ensure_ascii=False,indent=2).encode());print(json.dumps({k:v for k,v in r.items() if k!='removed_only_all_true_audit_check_labels'}))
