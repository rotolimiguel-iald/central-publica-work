from pathlib import Path
import ast, collections, hashlib, json, re, os, subprocess, datetime
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
 assert not p.exists(); q=p.with_name(p.name+'.tmp'); q.write_bytes(b)
 assert q.read_bytes()==b and len(b)>0;os.replace(q,p)
tree=ast.parse((R/'um.py').read_text(encoding='utf8'))
node=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets))
keys=[ast.literal_eval(k) for k in node.keys]
seen=set(); dependencies=[]
def visit(m):
 if m in seen or not m.startswith(('TGL.','TGLExt.')):return
 seen.add(m);p=R/'kernel'/Path(*m.split('.')).with_suffix('.lean')
 s=p.read_text(encoding='utf8')
 for dep in re.findall(r'^import\s+(\S+)',s,re.M):visit(dep)
 dependencies.append(dict(module=m,path=str(p),sha256=sha(p)))
visit('TGLExt.TheSameBetaReadsThreeFaces')
cmd=['rg','-n','(β|beta|α|alpha).*(Real.exp \\(1 / 2\\)|Real.sqrt \\(Real.exp 1\\))',str(R/'kernel'),'-g','*.lean','-g','!TheSameBetaReadsThreeFaces.lean','-g','!AuditSameBeta.lean']
run=subprocess.run(cmd,capture_output=True)
put(R/'searches/07_cost_type.stdout.txt',run.stdout or b'[no matches]\n')
put(R/'searches/07_cost_type.stderr.txt',run.stderr or b'[empty stderr]\n')
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
 embedded_literal_entries=len(keys),embedded_unique_entries=len(set(keys)),
 duplicated_keys={k:n for k,n in collections.Counter(keys).items() if n>1},
 copied_formal_files=len(json.loads((R/'CUSTODIA_V353_FONTES.json').read_text())['files']),
 lake_manifest_extra=True,dependencies=dependencies,
 supplementary_type_search=dict(command=cmd,returncode=run.returncode,
 timing='After the initial B1 source, before sealing: additional check, not falsely represented as pre-code.',
 result='No matching pre-existing bridge if output empty; matches require reading and decision.'),
 scope='B1 standalone project dependency closure only, not the whole default target TGL.Audit. All copied project sources available for B2-B6.')
put(R/'PROVENIENCIA_B1.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps({k:v for k,v in data.items() if k not in ['dependencies','supplementary_type_search']},ensure_ascii=False));print('project_dependency_count',len(dependencies));print(run.stdout.decode('utf8'))
