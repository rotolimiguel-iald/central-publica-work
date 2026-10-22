from pathlib import Path
import datetime, hashlib, json, os, re

root = Path(__file__).resolve().parent
def pin(path):
    b = path.read_bytes()
    return {'path':str(path), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
def latest(module, success=True):
    source = root/'src/TGLExt'/f'{module}.lean'
    matches=[]
    for record in (root/'attempts').glob('*/RESULT.json'):
        d=json.loads(record.read_bytes())
        if d['source']['sha256']==pin(source)['sha256'] and d['source_unchanged']:
            if (d['returncode']==0)==success:
                matches.append((record,d))
    assert matches, (module, success)
    return sorted(matches,key=lambda x:str(x[0]))[-1]

modules=['V354TraceShiftEquivalence','V354CyclicTraceCompletion','AuditTraceCompletion012',
         'GoodTraceCompletion012']
builds={name:latest(name) for name in modules}
audit_result=builds['AuditTraceCompletion012'][1]
output=Path(audit_result['stdout']['path']).read_text(encoding='utf8')
expected=re.findall(r'^#print axioms (\S+)$',
    (root/'src/TGLExt/AuditTraceCompletion012.lean').read_text(encoding='utf8'),re.M)
allowed={'propext','Classical.choice','Quot.sound'}
rows=[]
for name in expected:
    pattern=r"'"+re.escape(name)+r"' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))"
    found=re.findall(pattern, output, re.S)
    assert len(found)==1,(name,found)
    deps={re.sub(r'\.\{[^}]*\}', '',x.strip()) for x in found[0][0].split(',') if x.strip()}
    rows.append({'name':name,'axioms':sorted(deps),'allowed':deps<=allowed})
controls=[]
for name in ['BadTraceCommute012','BadTraceZero012']:
    record,d=latest(name,False)
    content=Path(d['stdout']['path']).read_text(encoding='utf8')
    semantic=bool(re.search(r'(Type mismatch|type mismatch|Application type mismatch)',content))
    infrastructure=bool(re.search(r'(does not exist|unknownIdentifier|unexpected token|timeout)',content))
    controls.append({'name':name,'result':pin(record),'returncode':d['returncode'],
                     'semantic_rejection':semantic and not infrastructure,
                     'scope':'Interface misuse rejected; not a universal analytic no-go theorem.'})
math_sources=[root/'src/TGLExt'/f'{n}.lean' for n in modules[:2]]
for p in math_sources:
    content=p.read_text(encoding='utf8')
    assert not re.search(r'\b(axiom|sorry|native_decide|trustCompiler)\b',content),p
data={
 'timestamp':datetime.datetime.now().astimezone().isoformat(),
 'status':'AUTHOR_PARTIAL_CYCLIC_COMPLETION_POSITIVE_COMPATIBILITY_OPEN',
 'sources':[pin(p) for p in math_sources],
 'builds':{n:{'record':pin(path),'returncode':d['returncode']} for n,(path,d) in builds.items()},
 'axiom_checks':rows,'all_axioms_allowed':all(row['allowed'] for row in rows),
 'controls':controls,'all_controls_semantic':all(c['semantic_rejection'] for c in controls),
 'proven_scope':['Shift relation is reflexive, symmetric, transitive; cyclic pairs, star and homomorphisms preserve it.',
                'Actual-core candidate is cyclic, star invariant, dual homogeneous, zero preserving and faithful on positive inputs.',
                'The positive A1 trace is a lower bound on the candidate.',
                'Agreement with A1 follows IF positive shift compatibility is supplied. This premise has not been proved here.'],
 'open':['Positive shift compatibility with the A1 trace.','Consequently the finite value of this candidate at PF and its agreement with A1 on all positives.','Legacy ContinuousCoreData plus actual ThreeLocks/SUSY integration.'],
 'full_trace_A1_previously_constructed':True,
 'full_A2_constructed':False,'gate_changed':False,
 'review':'Independent review requested from Carver; not asserted completed by this author audit.',
 'reused_after_search':{'SemiconjBy.pow_right':'Replaced the initial two local power inductions; no new power-transport theorem retained.'},
 'limits':['No physical confirmation or EOM realization.',
           'No numerical sigma or empirical claim.',
           'No canonical program edit.']}
assert data['all_axioms_allowed'] and data['all_controls_semantic']
path=root/'AUDITORIA_AUTORAL_COMPLETION_012.json'
assert not path.exists()
payload=json.dumps(data,ensure_ascii=False,indent=2).encode('utf8')
temp=path.with_name(path.name+'.tmp');temp.write_bytes(payload);assert temp.read_bytes()==payload;os.replace(temp,path)
print(json.dumps({'path':str(path),'names':len(rows),'controls':len(controls),'status':data['status']}))
