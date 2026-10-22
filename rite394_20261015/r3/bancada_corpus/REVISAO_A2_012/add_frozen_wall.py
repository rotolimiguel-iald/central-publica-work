from review_a2 import *

m='TGLExt.V354TraceReaderWall'
p=AUTHOR/'src'/modpath(m); q=SRC/modpath(m)
assert not q.exists() and not OUT.exists()
write(q,p.read_bytes())
data=json.loads((ROOT/'INPUTS.json').read_text(encoding='utf-8'))
data['snapshots'].append(dict(module=m,source=info(p),copy=info(q)))
assert imports(q)==['TGLExt.V354PositiveTraceReader']
data['new_graph'][m]=imports(q)
code=code_only(q.read_text(encoding='utf-8'))
ns=re.findall(r'^namespace\s+(\S+)',code,re.M)[0]
names=[ns+'.'+n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+(\w+)',code,re.M)]
data['expected_public_names']+=names
data['excluded_unfrozen']=[]
data['freeze_note']='All eight V354 files frozen by the author in the user message; subsequent source changes invalidate this review snapshot'
record(ROOT/'INPUTS.json',data)
scan=json.loads((ROOT/'SOURCE_SCAN.json').read_text(encoding='utf-8'))
scan['files'].append(dict(source=info(q),public_names=names,forbidden=re.findall(
    r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',code,re.M),
    classical_occurrences=[],dimensional_occurrences=[],heartbeats=[]))
scan['all_clean']=all(not x['forbidden'] for x in scan['files'])
record(ROOT/'SOURCE_SCAN.json',scan)
audit='import TGLExt.V354TraceReaderWall\nset_option pp.universes true\n'
audit+='\n'.join('#check '+n+'\n#print axioms '+n for n in data['expected_public_names'])+'\n'
audit+='\n#print TGLV350.Regular.regularNormalizedFaces\n#print TGLV350.Regular.regularContinuousCorner\n'
write(SRC/'AuditAllPublic.lean',audit)
print('Frozen modules:',len(data['new_graph']),'Public names:',len(data['expected_public_names']))
