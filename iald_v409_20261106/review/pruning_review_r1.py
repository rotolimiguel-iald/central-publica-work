"""Independent dictionary reachability and semantic conservation review."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent.parent
E=W/'capacity_experiments'
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(Path(p).read_bytes())
pin=lambda p:{'path':str(p),'sha256':sha(Path(p).read_bytes())}
report=read(E/'PRUNING_REPORT.json')
old=(E/'BASELINE_COPY.md').read_bytes();new=(E/'shared_orphans_pruned.md').read_bytes()
assert sha(old)==report['baseline_sha256'] and sha(new)==report['candidate_sha256']
assert old==(W/'app/packages/shared/prefix.md').read_bytes()
p2=read(W/'review/P2_R1.json')
assert p2['status']=='PASS_P2_ONLY_APP_NOT_ACCEPTED'
assert next(e['sha256'] for e in p2['evidence'] if e['path'].endswith('prefix.md'))==sha(old)
for p,h in read(E/'BASELINE_PINS.json').items():assert sha(Path(p).read_bytes())==h
ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True)
assert len(ol)==len(nl)
changed=[i for i,(x,y) in enumerate(zip(ol,nl)) if x!=y]
assert len(changed)==1
idx=changed[0]
assert ol[idx-1].decode().strip()=='DICIONÁRIO DE LITERAIS'
before=json.loads(ol[idx]);after=json.loads(nl[idx])
assert all(k in before and v==before[k] for k,v in after.items())
roots=[]
for i,line in enumerate(ol):
    if i==idx:continue
    try: roots.append(json.loads(line))
    except ValueError:pass

def references(node):
    todo=[node];found=set()
    while todo:
        v=todo.pop()
        if isinstance(v,list):todo.extend(v)
        elif isinstance(v,dict):
            for k,x in v.items():
                if k in ('@L','@TGL_LITERAL'):
                    assert isinstance(x,str);found.add(x)
                else:todo.append(x)
    return found

def closure(initial,dictionary):
    reached=set(initial)
    while True:
        expanded=set(reached)
        for k in reached:
            assert k in dictionary,('missing literal',k)
            expanded.update(references(dictionary[k]))
        if expanded==reached:return reached
        reached=expanded

direct=set().union(*(references(r) for r in roots))
reachable=closure(direct,before)
assert set(after)==reachable
removed={k:v for k,v in before.items() if k not in reachable}
assert removed==read(E/'ORPHANS_REMOVED.json')
assert closure({'A'},{'A':{'@concat':[{'@L':'B'},'!']},'B':{'@TGL_LITERAL':'C'},'C':'retained','D':'orphan'})=={'A','B','C'}
assert closure({'A'},{'A':{'@L':'B'},'B':{'@L':'A'}})=={'A','B'}
try:closure({'missing'},{})
except AssertionError:pass
else:raise AssertionError('Missing dependency was accepted')

def decode(value,dictionary,stack=()):
    if isinstance(value,list):return [decode(v,dictionary,stack) for v in value]
    if not isinstance(value,dict):return value
    if len(value)==1:
        key,arg=next(iter(value.items()))
        if key in ('@L','@TGL_LITERAL'):
            assert arg not in stack,'cyclic literal'
            return decode(dictionary[arg],dictionary,stack+(arg,))
        if key=='@concat':return ''.join(decode(v,dictionary,stack) for v in arg)
        if key=='@upper':return arg.upper()
        if key=='@enum':return arg.upper().replace(' ','_')
    return {k:decode(v,dictionary,stack) for k,v in value.items()}
for root in roots:assert decode(root,before)==decode(root,after)
# Exposition coordinates and metadata are unchanged, so preserving their tags
# also preserves the interpretation validated independently in P2_R1.
assert old.split(b'<EXPOSICAO_CANONICA>\n',1)[1]==new.split(b'<EXPOSICAO_CANONICA>\n',1)[1]
assert len(roots)==490 and len(removed)==174 and len(after)==186
assert (len(old),len(new),len(old)-len(new))==(890840,847129,43711)
for model,measure in report['bounds_declared_policy'].items():
    assert measure['slack']==1048576-148656-4096-measure['input_bound']
assert min(m['slack'] for m in report['bounds_declared_policy'].values())==5044
k=report['kimi_effective_envelope_after']
assert k['slack']==1048576-k['output_reserve']-k['margin']-k['prompt_utf8_bytes']==26041
for row in read(W/'PRESERVATION_BASELINE.json')['files']:
    assert sha(Path(row['path']).read_bytes())==row['sha256']
out={'status':'PASS_STAGING_REBUILD_ONLY','reviewer':'codex-app-v409-review',
 'dictionary_before':len(before),'dictionary_after':len(after),'removed_unreachable':len(removed),
 'json_roots_equal':len(roots),'all_non_dictionary_bytes_equal':True,'exposition_equal':True,
 'transitive_graph_controls':3,'resident_complete_from_bound_P2':7,'history_exact_from_bound_P2':177,
 'index_uncompacted':True,'old_bytes':len(old),'new_bytes':len(new),'bytes_saved':len(old)-len(new),
 'bounds_scope':'Existing builder measurements and arithmetic checked only; not a repeated count, runtime admission or guarantee for real history/ACOM.',
 'declared_reserve_min_slack':5044,'kimi_131072_synthetic_slack':26041,
 'findings':[], 'rebuild_allowed':True,'finalize_condition':'Rebuild staging with this exact removal-only rule; independently remeasure final package admission under unchanged ceilings/reserves, preserve P2 v409+v408/index/history/scope, and bind final byte hashes before finalize. No automatic app acceptance.',
 'app_accepted':False,'deploy_allowed':False,'runtime_modified':False,'provider_calls':0,
 'evidence':[pin(E/'prune_orphans.py'),pin(E/'PRUNING_REPORT.json'),pin(E/'shared_orphans_pruned.md'),pin(E/'BASELINE_COPY.md'),pin(E/'ORPHANS_REMOVED.json'),pin(W/'review/P2_R1.json')]}
with (W/'review/PRUNING_R1.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({k:out[k] for k in ('status','removed_unreachable','json_roots_equal','bytes_saved','deploy_allowed')}))
