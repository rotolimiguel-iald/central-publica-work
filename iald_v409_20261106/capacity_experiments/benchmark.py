"""Isolated lossless literal benchmark. No runtime edits or provider calls."""
import hashlib,json,re,sys
from collections import Counter
from pathlib import Path

E=Path(__file__).resolve().parent; W=E.parent; A=W/'app'
sys.dont_write_bytecode=True
sys.path[:0]=[str(A),str(A/'build'),str(W)]
import haiku_codec as c
import fit_transport as ft
import verify_d53 as verify
import preservation_guard

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def write(p,b):
    if not isinstance(b,bytes):b=json.dumps(b,ensure_ascii=False,indent=2).encode()
    if p.exists():
        assert p.read_bytes()==b,str(p)
        return
    with p.open('xb') as f:f.write(b)

original=A/'packages/shared/prefix.md'; raw=original.read_bytes()
protected={str(p):sha(p.read_bytes()) for p in A.rglob('*') if p.is_file()}
write(E/'BASELINE_COPY.md',raw)
write(E/'BASELINE_PINS.json',protected)
text=raw.decode()
for long,short in ft.ALIASES.items():text=text.replace(short,long)
lines=text.splitlines(keepends=True)
dm='DICIONÁRIO DE LITERAIS'
di=next(i+1 for i,l in enumerate(lines) if l.strip()==dm)
old_dictionary=json.loads(lines[di])
expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
history=json.loads((A/'D53_HISTORY.json').read_bytes())
manifest=json.loads((A/'science/memory_stage/manifest_staged.json').read_bytes())
document=Path(manifest['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig')
core=json.loads(document)['core']
nodes={}; names={}; active=None
for i,line in enumerate(lines):
    if line.startswith(c.MARKER):break
    if line.startswith('### '):active=line.strip()[4:]
    if active in core and line.startswith('{'):
        nodes[i]=json.loads(line);names[i]=active

# Decode using an independent implementation, never resolving a source/fetch pointer.
def decode(v,d):
    if isinstance(v,list):return [decode(x,d) for x in v]
    if not isinstance(v,dict):return v
    if set(v)=={'@TGL_LITERAL'}:return decode(d[v['@TGL_LITERAL']],d)
    if set(v)=={'@EXPOSITION'}:
        start,size=v['@EXPOSITION'];assert 0<=start and size>0 and start+size<=len(expo)
        return expo[start:start+size]
    if set(v)=={'@concat'}:return ''.join(decode(x,d) for x in v['@concat'])
    if set(v)=={'@upper'}:return v['@upper'].upper()
    if set(v)=={'@enum'}:return v['@enum'].upper().replace(' ','_')
    return {k:decode(x,d) for k,x in v.items()}

original_decoded={i:decode(v,old_dictionary) for i,v in nodes.items()}
counts=Counter()
def scan(v):
    if isinstance(v,str):counts[v]+=1
    elif isinstance(v,list):
        for x in v:scan(x)
    elif isinstance(v,dict):
        for k,x in v.items():
            if not k.startswith('@'):scan(x)
for v in nodes.values():scan(v)
results=[]
for threshold in (80,64,48,32,24):
    dictionary=dict(old_dictionary); lookup={}; choices=[]; serial=0
    for value,count in sorted(counts.items(),key=lambda x:(-x[1],x[0])):
        if len(value)<threshold:continue
        literal_bytes=len(dump(value).encode())
        candidates=[]
        if count>1:
            ident='N'+str(serial)
            assert ident not in dictionary
            node={'@TGL_LITERAL':ident}
            ref_bytes=len(dump({'@L':ident}).encode())
            entry_bytes=len((dump(ident)+':'+dump(value)+',').encode())
            gain=count*(literal_bytes-ref_bytes)-entry_bytes
            if gain>0:candidates.append((gain,'literal',node,ident))
        offset=expo.find(value)
        if offset>=0:
            node={'@EXPOSITION':[offset,len(value)]}
            gain=count*(literal_bytes-len(dump({'@X':[offset,len(value)]}).encode()))
            if gain>0:candidates.append((gain,'exposition',node,None))
        if not candidates:continue
        gain,kind,node,ident=max(candidates,key=lambda x:x[0])
        if ident is not None:dictionary[ident]=value;serial+=1
        lookup[value]=node
        choices.append(dict(value_sha256=sha(value.encode()),characters=len(value),occurrences=count,kind=kind,net_json_bytes_saved=gain))
    def encode(v):
        if isinstance(v,str):return lookup.get(v,v)
        if isinstance(v,list):return [encode(x) for x in v]
        if isinstance(v,dict):return {k:(x if k.startswith('@') else encode(x)) for k,x in v.items()}
        return v
    output=list(lines)
    for i,v in nodes.items():
        enc=encode(v)
        assert decode(enc,dictionary)==original_decoded[i],names[i]
        assert c.decode_literals(enc,dictionary,expo)==c.decode_literals(v,old_dictionary,expo),names[i]
        output[i]=dump(enc)+'\n'
    output[di]=dump(dictionary)+'\n'
    candidate=''.join(output)
    for long,short in ft.ALIASES.items():candidate=candidate.replace(long,short)
    semantic=verify.verify(candidate,core,document,history,json.loads((A/'KERNEL_HIGHLIGHTS.json').read_bytes()))
    encoded=candidate.encode();bounds=verify.bounds(candidate)
    name=f'shared_threshold_{threshold}.md';write(E/name,encoded)
    result=dict(threshold=threshold,path=str(E/name),sha256=sha(encoded),bytes=len(encoded),
        saved_bytes=len(raw)-len(encoded),net_json_sum=sum(x['net_json_bytes_saved'] for x in choices),
        new_dictionary_entries=serial,exposition_substrings=sum(x['kind']=='exposition' for x in choices),
        all_topic_json_nodes_equal=len(nodes),resident_full_prompt_only=semantic['complete_resident'],
        semantic_checks=semantic,bounds=bounds,choices=choices)
    write(E/f'RESULT_{threshold}.json',result)
    results.append({k:v for k,v in result.items() if k!='choices'})
assert all(sha(Path(p).read_bytes())==v for p,v in protected.items())
preservation_guard.verify()
best=min(results,key=lambda r:r['bytes'])
report=dict(status='ISOLATED_BENCHMARK_COMPLETE_NOT_REBUILT',baseline_bytes=len(raw),baseline_sha256=sha(raw),
    variants=results,best_threshold=best['threshold'],best_saved_bytes=best['saved_bytes'],
    submitted_artifacts_unchanged=True,provider_calls=0,ceilings_changed=False,reserve_changed=False,
    same_contract='@L aliases @TGL_LITERAL, @X aliases @EXPOSITION; existing in-prompt dictionary and Unicode spans; no new runtime tag or external pointer.',
    scope='Post-build exact incremental interning of literal values on the submitted shared prefix; not an end-to-end prepare rebuild. Keys and protocol coordinates unchanged. Every selection has positive net JSON savings including dictionary entry.',
    independent_decoder='Separate recursion implementation checked every topic JSON node; resident complete equality checked without restore/fetch by existing verifier. Not an independent reviewer.')
write(E/'REPORT.json',report)
print(json.dumps({k:report[k] for k in ('status','baseline_bytes','best_threshold','best_saved_bytes')}))
for r in results:print(json.dumps({k:r[k] for k in ('threshold','bytes','saved_bytes','new_dictionary_entries','exposition_substrings','bounds')}))
