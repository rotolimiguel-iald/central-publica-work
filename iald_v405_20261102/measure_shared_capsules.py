"""Independent measurement (builder, read-only): every compact capsule of the shared prefix keeps ALL status/statute/verdict/
hypothesis/scope fields of its source topic, with values equal to the source; 0 topics lost. Writes nothing but stdout."""
import json,re,sys
from pathlib import Path
A=(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent)/'app';sys.dont_write_bytecode=True;sys.path.insert(0,str(A/'build'))
import haiku_codec as c,fit_memory as fm
res=json.loads(Path(next((A/'science/memory_stage/release').glob('Um*/um_absoluto.json'))).read_bytes())
text=(A/'packages/shared/prefix.md').read_text(encoding='utf-8')
for long,short in __import__('fit_transport').ALIASES.items():text=text.replace(short,long)
dm='DICIONÁRIO DE LITERAIS\n';dictionary=json.loads(text.split(dm,1)[1].split('\n',1)[0])
expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
head=text.split(c.MARKER)[0]
hs=[h for h in re.finditer(r'(?m)^### ([^\n]+)\n',head) if h[1] in res['core']]
bodies={}
for i,h in enumerate(hs):
    stop=hs[i+1].start() if i+1<len(hs) else len(head);bodies[h[1]]=head[h.end():stop].strip()
core=res['core'];missing=[n for n in core if n not in bodies]
compact=[];checked=0;bad=[];status_fields=0
for n,b in bodies.items():
    line=b.splitlines()[0] if b else ''
    try:v=json.loads(line)
    except ValueError:continue
    if not (isinstance(v,dict) and '@' in v):continue
    compact.append(n);p='/core/'+n
    d=c.decode_literals(c.unpack_metadata(v),dictionary,expo) if False else v
    # fields are plain JSON; literal refs resolved with the prefix dictionary (ids carry the Hn_ prefix of the capsule)
    def dec(x):
        if isinstance(x,dict) and set(x)=={'@TGL_LITERAL'}:
            k=x['@TGL_LITERAL'];assert k in dictionary,k;return dictionary[k]
        if isinstance(x,dict):return {k2:dec(y) for k2,y in x.items()}
        if isinstance(x,list):return [dec(y) for y in x]
        return x
    cap=c.decode_literals(c.unpack_metadata(v),dictionary,expo)
    try:
        got=c.restore(cap,res,p,p,{})
        assert got==core[n]
        need=fm.fields(core[n]);have=cap.get('fields',{})
        for path,val in need.items():
            if re.search(r'status|statute|estatuto|verdict|veredit',path,re.I):status_fields+=1
            if path not in have or have[path]!=val:bad.append((n,path))
        checked+=1
    except Exception as e:bad.append((n,'EXC '+type(e).__name__+': '+str(e)[:120]))
print(json.dumps({'core_topics':len(core),'topics_with_a_block_in_shared':len(bodies),'topics_lost':missing,'compact_capsules':len(compact),'capsules_restored_equal_source':checked,'status_like_fields_checked':status_fields,'statute_or_field_mismatches':bad[:10],'n_mismatches':len(bad)},ensure_ascii=False))
