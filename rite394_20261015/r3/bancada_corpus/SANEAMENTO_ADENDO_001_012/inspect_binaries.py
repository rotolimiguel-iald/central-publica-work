from support import *
import re
B=ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
D=ROOT/'binary';D.mkdir(exist_ok=True)
def pin(p):return dict(path=str(p),bytes=p.stat().st_size,sha256=digest(p))
def normalize(x,root):
 if isinstance(x,str):return x.replace(str(root),'<ROOT>').replace(str(root).replace('\\','/'),'<ROOT>')
 if isinstance(x,list):return [normalize(z,root) for z in x]
 if isinstance(x,dict):return {k:normalize(v,root) for k,v in x.items()}
 return x
def diff(x,y,path=''):
 if type(x)!=type(y):return [dict(key=path,left=x,right=y)]
 if isinstance(x,dict):
  out=[]
  for k in sorted(x.keys()|y.keys()):out+=diff(x.get(k),y.get(k),path+'/'+k)
  return out
 if isinstance(x,list):
  if len(x)!=len(y):return [dict(key=path+'/length',left=len(x),right=len(y))]
  return sum([diff(a,b,path+'/'+str(n)) for n,(a,b) in enumerate(zip(x,y))],[])
 return [] if x==y else [dict(key=path,left=x,right=y)]
rows=[]
for mod in ['TGLExt/MixedLadder','TGLExt/SecondCone','TGL/AreaScale']:
 row={'module':mod,'roots':[]};raws=[]
 for root in [B/'kernel',B/'s']:
  files={'source':root/(mod+'.lean'),'olean':root/'.lake/build/lib/lean'/(mod+'.olean'),'trace':root/'.lake/build/lib/lean'/(mod+'.trace'),'setup':root/'.lake/build/ir'/(mod+'.setup.json')}
  r={'root':str(root),'files':{k:pin(p) if p.exists() else dict(path=str(p),exists=False) for k,p in files.items()}}
  raw={k:p.read_bytes() for k,p in files.items() if p.exists()}
  for k,b in raw.items():atomic(D/'originals'/root.name/(mod+'.'+k),b)
  r['trace_normalized']=normalize(json.loads(raw['trace']),root)
  r['setup_normalized']=normalize(json.loads(raw['setup']),root) if 'setup' in raw else None
  row['roots'].append(r);raws.append(raw)
 x,y=raws
 row['same_source']=x['source']==y['source'];row['same_olean']=x['olean']==y['olean']
 off=[i for i,(a,b) in enumerate(zip(x['olean'],y['olean'])) if a!=b]
 row['binary_difference']=dict(first_offset=off[0] if off else None,differing_positions_in_overlap=len(off),length_delta=len(y['olean'])-len(x['olean']),sample_offsets=off[:32])
 row['trace_differences']=diff(*[z['trace_normalized'] for z in row['roots']])
 row['setup_differences']=diff(*[z['setup_normalized'] for z in row['roots']])
 row['trace_inputs_equal_after_root_normalization']=row['roots'][0]['trace_normalized']['inputs']==row['roots'][1]['trace_normalized']['inputs']
 rows.append(row)
 print(mod,'source_equal',row['same_source'],'inputs_equal',row['trace_inputs_equal_after_root_normalization'],'trace_diff',row['trace_differences'],'setup_diff_count',len(row['setup_differences']))
record(D/'MEDICAO_ORIGINAIS.json',rows)
# Preserve and read the prior reviewer account, not its assertion as current proof.
references=[]
for p in [B/'AUDITORIA_B6.json',B/'revisao_b6/REVIEW_B6_FINAL.json',B/'revisao_b6/independent_20260914_172114_917733/binary_reproducibility_limit.json',B/'revisao_b6/independent_20260914_172114_917733/run.json']:
 b=p.read_bytes();json.loads(b);references.append(pin(p));atomic(D/'references'/p.name,b)
record(D/'REFERENCIAS_LIDAS.json',references)
