from pathlib import Path
import json,re,hashlib,sys
W=Path(__file__).resolve().parent.parent;V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy')
cores={n:json.loads((V/('um_unificado_v'+str(n))/'um_absoluto.json').read_bytes())['core'] for n in (408,409,410)}
source=(V/'um_unificado_v410/um_absoluto.json').read_bytes().decode('utf-8-sig');core=cores[410]
prefix=(W/'app/packages/shared/prefix.md').read_text(encoding='utf8');history=json.loads((W/'app/D53_HISTORY.json').read_bytes());residents=set(history['resident'])
# The canonical exposition/mother/kernel remain outside this transform; topic provenance only.
allowed=[]
for name,value in core.items():
 if re.search(r'_v\d+$',name) or name in residents or not isinstance(value,dict):continue
 if all(name in cores[n] and cores[n][name]==value for n in (408,409)):allowed.append(name)
heads=[m for m in re.finditer(r'(?m)^### ([^\n]+)\n',prefix) if m[1] in core];end=prefix.index('\n<EXPOSICAO_CANONICA>')
# Preserve marker and everything after last topic by finding original section marker.
sys.path[:0]=[str(W/'app/build')];import haiku_codec as codec
end=prefix.index('\n'+codec.MARKER)
rows=[prefix[:heads[0].start()]];details=[];decoder=json.JSONDecoder()
core_start=re.search(r'(?m)^  "core": ',source).end();core_value,core_end=decoder.raw_decode(source,core_start);assert core_value==core
for i,m in enumerate(heads):
 stop=heads[i+1].start() if i+1<len(heads) else end;block=prefix[m.start():stop];name=m[1]
 if name in allowed:
  hit=[m for m in re.finditer(r'(?m)^    "'+re.escape(name)+r'": ',source) if core_start<m.start()<core_end];assert len(hit)==1,(name,len(hit))
  offset=hit[0].end();value,size=decoder.raw_decode(source,offset);length=size-offset;assert value==core[name]
  node={'@H':[offset,length]}
  for k in ('estatuto','status','verdict','all_verified','does_not_gate_core','limites','diz','nao_diz'):
   if k in value:node[k]=value[k]
  updated=m.group()+json.dumps(node,ensure_ascii=False,separators=(',',':'))+'\n\n'
  details.append({'topic':name,'versions_equal':[408,409,410],'canonical_json_sha256':hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'before_bytes':len(block.encode()),'after_bytes':len(updated.encode()),'span':[offset,length],'qualifiers_inline':[k for k in node if k!='@H']})
  block=updated
 rows.append(block)
rows.append(prefix[end:]);out=''.join(rows)
(W/'experiments/candidate_provenance.txt').write_text(out,encoding='utf8')
report={'status':'EXPERIMENT_NOT_INTEGRATED','before':len(prefix.encode()),'after':len(out.encode()),'entries':len(details),'details':details,'policy':'Historical equality across v408/v409/v410; same @H; qualifiers including limites/diz/nao_diz remain inline; unchanged sections outside core topics.'}
(W/'experiments/PROVENANCE_EXPERIMENT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:report[k] for k in ('status','before','after','entries')}))
