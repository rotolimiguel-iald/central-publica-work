from pathlib import Path
import ast, datetime, hashlib, json, os

root = Path(__file__).resolve().parent
source = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
b = source.read_bytes()
text = b.decode('utf8')
tree = ast.parse(text)
names = {'_QG_FRONTIER_FLAGS', '_GRAVITY_PRICE_FLAGS', '_V350_MODULAR_CONTRACTS',
         'verify_v350_modular_provenance', 'finalize_v350_modular_frontier',
         'v350_frontier_flag_has_proof', 'v350_gravity_flags_have_proof',
         'evaluate_v350_kernel_frontier'}
found = {}
for node in tree.body:
    name = node.name if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else None
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
    if name in names:
        assert name not in found
        found[name] = {'start_line': node.lineno, 'end_line': node.end_lineno,
                       'source': ast.get_source_segment(text, node)}
assert set(found) == names
lines = text.splitlines()
ranges = [(134535,134602),(160134,160154),(160188,160208),(160988,161016)]
excerpts = '\n\n'.join('\n'.join(f'{i}: {lines[i-1]}' for i in range(a,z+1)) for a,z in ranges)
assert source.read_bytes() == b, 'canonical source changed during reading'
def put(name, payload):
    p = root/name
    assert not p.exists()
    t = p.with_name(p.name+'.tmp'); t.write_bytes(payload); assert t.read_bytes() == payload; os.replace(t,p)
    return {'path':str(p),'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}
snapshot = '\n\n'.join(row['source'] for row in found.values())+'\n'
outputs = [put('CANONICAL_READERS_SNAPSHOT.py', snapshot.encode('utf8')),
           put('CANONICAL_CONSUMERS_BOUNDED.txt', excerpts.encode('utf8'))]
data = {'timestamp':datetime.datetime.now().astimezone().isoformat(),
        'canonical_source':{'path':str(source),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},
        'mode':'read-only AST extraction; canonical program never imported or executed',
        'nodes':found,'outputs':outputs}
put('CANONICAL_READERS_PROVENANCE.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps({'nodes':list(found),'outputs':outputs},ensure_ascii=False))
