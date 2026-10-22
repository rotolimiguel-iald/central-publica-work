"""Read-only comparison of the canonical source and pinned A1 baseline."""
from pathlib import Path
import ast, datetime, hashlib, json, os
ROOT=Path(__file__).absolute().parent
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
def sha(b):return hashlib.sha256(b).hexdigest()
def extract(raw):
    tree=ast.parse(raw.decode('utf-8-sig'))
    nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
    assert len(nodes)==1
    return ast.literal_eval(nodes[0].value)
local=(ROOT/'um.py').read_bytes();canonical=CAN.read_bytes()
a,b=extract(local),extract(canonical)
changed=[k for k in sorted(a.keys()&b.keys()) if a[k]!=b[k]]
rec=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='CANONICAL_DRIFT_DETECTED__LOCAL_BASELINE_PRESERVED',
 canonical=dict(path=str(CAN),sha256=sha(canonical),bytes=len(canonical),lf_only=canonical.count(b'\n')-canonical.count(b'\r\n'),mtime_ns=CAN.stat().st_mtime_ns),
 local=dict(path=str(ROOT/'um.py'),sha256=sha(local),bytes=len(local),lf_only=local.count(b'\n')-local.count(b'\r\n')),
 embedded=dict(local_count=len(a),canonical_count=len(b),added=sorted(b.keys()-a.keys()),removed=sorted(a.keys()-b.keys()),changed=changed,
  all_identical=(a==b),per_file=[dict(name=k,sha256=sha(a[k].encode('utf-8'))) for k in sorted(a) if k in b and a[k]==b[k]]),
 program_executed=False,canonical_written=False,scope='Somente custodia e comparacao AST dos fontes embutidos; sem ler/avaliar resultados de natureza.',
 integration='Entrega contra copia v351; gerencia integra sobre sua versao corrente. Nenhuma igualdade byte a byte entre monolitos deve ser afirmada.')
assert sha(local)==json.loads((ROOT/'MANIFESTO_A1.json').read_bytes())['program_sha256']
assert CAN.read_bytes()==canonical,'Canonical source changed again during comparison'
p=ROOT/'CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json';assert not p.exists()
raw=(json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode('utf-8');tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw
os.replace(tmp,p)
print(json.dumps({k:v for k,v in rec.items() if k!='embedded'}|{'embedded':{k:v for k,v in rec['embedded'].items() if k!='per_file'}},ensure_ascii=False,indent=2))
