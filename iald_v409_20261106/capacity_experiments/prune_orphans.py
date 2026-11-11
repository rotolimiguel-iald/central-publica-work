"""Remove only unreachable in-prompt dictionary entries; isolated candidate."""
import hashlib,json,sys
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parent;A=W/'app'
sys.dont_write_bytecode=True;sys.path[:0]=[str(A),str(W)]
import verify_d53 as v
import preservation_guard
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def save(p,x):
    if not isinstance(x,bytes):x=json.dumps(x,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(x)
pins=json.loads((E/'BASELINE_PINS.json').read_bytes())
assert all(sha(Path(p).read_bytes())==h for p,h in pins.items())
raw=(E/'BASELINE_COPY.md').read_bytes();text=raw.decode();lines=text.splitlines(keepends=True)
di=next(i+1 for i,s in enumerate(lines) if s.strip()=='DICIONÁRIO DE LITERAIS')
dictionary=json.loads(lines[di]); roots=[]; direct=set()
def refs(x):
    if isinstance(x,list):
        for y in x:yield from refs(y)
    elif isinstance(x,dict):
        for k,y in x.items():
            if k in ('@L','@TGL_LITERAL'):
                assert isinstance(y,str);yield y
            else:yield from refs(y)
for i,line in enumerate(lines):
    if i==di:continue
    try:node=json.loads(line)
    except ValueError:continue
    roots.append((i,node));direct.update(refs(node))
reachable=set();todo=list(direct)
while todo:
    key=todo.pop();assert key in dictionary,key
    if key in reachable:continue
    reachable.add(key);todo.extend(refs(dictionary[key]))
kept={k:x for k,x in dictionary.items() if k in reachable}
orphan={k:x for k,x in dictionary.items() if k not in reachable}
# Independent decoder: no original result and no fetch resolver are available here.
expo=text.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
def decode(x,d,stack=()):
    if isinstance(x,list):return [decode(y,d,stack) for y in x]
    if not isinstance(x,dict):return x
    if len(x)==1:
        k,y=next(iter(x.items()))
        if k in ('@L','@TGL_LITERAL'):
            assert y not in stack;return decode(d[y],d,stack+(y,))
        if k=='@concat':return ''.join(decode(z,d,stack) for z in y)
        if k=='@enum':return y.upper().replace(' ','_')
        if k=='@upper':return y.upper()
        if k in ('@X','@EXPOSITION'):
            a,n=y;assert a>=0 and n>0 and a+n<=len(expo);return expo[a:a+n]
    return {k:decode(y,d,stack) for k,y in x.items()}
for i,node in roots:assert decode(node,dictionary)==decode(node,kept),i
end='\r\n' if lines[di].endswith('\r\n') else '\n'
output=list(lines);output[di]=dump(kept)+end;candidate=''.join(output)
assert all(x==y for i,(x,y) in enumerate(zip(lines,output)) if i!=di)
assert candidate.split('<EXPOSICAO_CANONICA>\n',1)[1]==text.split('<EXPOSICAO_CANONICA>\n',1)[1]
manifest=json.loads((A/'science/memory_stage/manifest_staged.json').read_bytes())
document=Path(manifest['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig')
history=json.loads((A/'D53_HISTORY.json').read_bytes());core=json.loads(document)['core']
sem=v.verify(candidate,core,document,history,json.loads((A/'KERNEL_HIGHLIGHTS.json').read_bytes()))
def actual_kimi(prefix):
    prompt=json.dumps({'instructions':prefix,'conversation':[{'role':'user','content':'Explique o alcance documentado da v409.'}]},ensure_ascii=False)
    n=len(prompt.encode());reserve=v.providers.MODELS['kimi']['output']
    return dict(prompt_utf8_bytes=n,output_reserve=reserve,margin=4096,slack=v.providers.WINDOW-reserve-4096-n,
        scope='Exact instructions/conversation single JSON envelope for synthetic projected system + user. Real ACOM/history/owner notice require separate final admission.')
save(E/'shared_orphans_pruned.md',candidate.encode())
save(E/'ORPHANS_REMOVED.json',orphan)
result=dict(status='ISOLATED_LOSSLESS_PRUNING_CANDIDATE_NOT_REBUILT',baseline_bytes=len(raw),candidate_bytes=len(candidate.encode()),
    bytes_saved=len(raw)-len(candidate.encode()),dictionary_before=len(dictionary),dictionary_after=len(kept),orphans=len(orphan),
    direct_references=len(direct),transitively_reachable=len(reachable),all_json_roots_roundtripped=len(roots),
    semantic_checks=sem,exposition_identical=True,all_non_dictionary_lines_identical=True,
    bounds_declared_policy=v.bounds(candidate),kimi_effective_envelope_before=actual_kimi(text),kimi_effective_envelope_after=actual_kimi(candidate),
    candidate_sha256=sha(candidate.encode()),baseline_sha256=sha(raw),submitted_artifacts_unchanged=True,
    provider_calls=0,ceilings_changed=False,reserve_changed=False,new_runtime_contract=False,
    contract='Same @L/@TGL_LITERAL, transitive @concat and existing metadata; no new tags, external pointers, source changes or index compaction.',
    review='Builder independent decoder is a separate implementation, not independent-agent review. Await parent decision before any rebuild.')
assert all(sha(Path(p).read_bytes())==h for p,h in pins.items());preservation_guard.verify()
save(E/'PRUNING_REPORT.json',result)
print(json.dumps(result,ensure_ascii=False))
