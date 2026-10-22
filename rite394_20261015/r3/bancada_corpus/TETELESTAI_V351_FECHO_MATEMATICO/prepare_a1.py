"""Read-only inventory; materialize only the authorized copy, never execute um.py."""
from pathlib import Path
import ast, hashlib, json, os, re, subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'TETELESTAI_V350_KERNEL_20260911'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(path, data):
    b = data.encode('utf-8') if isinstance(data, str) else data
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == b: return
        raise RuntimeError(f'Refusing overwrite: {path}')
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(b)
    assert tmp.stat().st_size == len(b)
    tmp.replace(path)
def save(name, data): write(ROOT / name, json.dumps(data, ensure_ascii=False, indent=2))

raw=(ROOT/'um.py').read_bytes()
tree=ast.parse(raw.decode('utf-8-sig'))
nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
assert len(nodes)==1
files=ast.literal_eval(nodes[0].value)
inventory=[]
for rel, text in files.items():
    path=ROOT/'kernel'/rel
    assert path.resolve().is_relative_to((ROOT/'kernel').resolve())
    write(path,text)
    inventory.append(dict(path=str(path),relative=rel,bytes=path.stat().st_size,sha256=sha(path.read_bytes())))
save('BASE_E_FONTES.json',dict(time_utc=datetime.now(timezone.utc).isoformat(),program_sha256=sha(raw),bytes=len(raw),crlf=raw.count(b'\r\n'),lf_only=raw.count(b'\n')-raw.count(b'\r\n'),embedded_count=len(files),sources=inventory))

pattern=r'canonicalTrace|ContinuousCoreData|scalarDualWeight|faithful.*trace|semifinite|Semifinite|perturb|KMS|[Tt]akesaki'
groups={
 'embedded': [ROOT/'kernel/TGL',ROOT/'kernel/TGLExt'],
 'notes': [p for p in OLD.glob('*.md') if p.name.startswith(('ROTA','RELATORIO','TRACO','CONVENCOES','RESPOSTA_GATE','AUDITORIA_DAS'))],
 'deliveries': [ROOT.parent/'TUNEL/DO_CHATGPT'],
}
results=[]
for name, paths in groups.items():
    cmd=['rg','-n','--max-columns','600','--max-columns-preview','-g','*.lean','-g','*.md',pattern,*map(str,paths)]
    run=subprocess.run(cmd,capture_output=True)
    out=run.stdout.decode('utf-8',errors='replace')
    write(ROOT/f'search_{name}.txt',out)
    results.append(dict(group=name,command=cmd,returncode=run.returncode,hits=len(out.splitlines()),stderr=run.stderr.decode('utf-8',errors='replace')))
save('BUSCAS_A1.json',results)
print(json.dumps(dict(embedded=len(files),lean=sum(p.endswith('.lean') for p in files),sha256=sha(raw),searches=results),ensure_ascii=False,indent=2))
