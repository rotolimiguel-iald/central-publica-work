"""Read canonical inputs; write byte copies only in this isolated order root."""
from pathlib import Path
import ast, datetime, hashlib, json, os, shutil, subprocess

ROOT = Path(__file__).resolve().parent
CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
KERNEL = CANON / 'tgl_kernel'
EXPECTED = 'c1c761809efcde52ea8c6c4f7f0e7598c1d8e636e6858f1780dd622ef62a1d40'

def digest(b): return hashlib.sha256(b).hexdigest()
def put(p, b):
    assert p.is_relative_to(ROOT) and not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    q = p.with_name(p.name + '.tmp')
    q.write_bytes(b)
    assert q.read_bytes() == b and len(b) > 0
    os.replace(q, p)

raw = (CANON / 'um.py').read_bytes()
assert digest(raw) == EXPECTED, 'Canonical changed: do not copy another version silently.'
put(ROOT / 'um.py', raw)
tree = ast.parse(raw.decode('utf-8-sig'))
embedded = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in node.targets):
        embedded = ast.literal_eval(node.value)
assert isinstance(embedded, dict)
records = []
for name, text in embedded.items():
    rel = Path(name)
    assert not rel.is_absolute() and '..' not in rel.parts
    p = KERNEL / rel
    b = p.read_bytes()
    # The materialized files are the build inputs; comparison is explicitly textual
    # because the monolith string stores LF while a materializer may retain CRLF.
    assert b.decode('utf-8-sig').replace('\r\n', '\n') == text.replace('\r\n', '\n'), name
    put(ROOT / 'kernel' / rel, b)
    records.append(dict(path=str(p),relative=name,sha256=digest(b),bytes=len(b)))
for name in ['lake-manifest.json']:
    if not (ROOT/'kernel'/name).exists(): put(ROOT/'kernel'/name,(KERNEL/name).read_bytes())
for name in ['um_absoluto_selo.json','tgl_kernel_proof_manifest.json','A_PROVA_DA_QG_TGL_arvore.md']:
    put(ROOT/'inputs'/name,(CANON/name).read_bytes())
record = dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    original=str(CANON/'um.py'),sha256=digest(raw),bytes=len(raw),
    crlf=raw.count(b'\r\n'),lf_only=raw.count(b'\n')-raw.count(b'\r\n'),
    original_executed=False,embedded_count=len(records),files=records,
    canonical_project_objects_copied=False)
put(ROOT/'CUSTODIA_V353_FONTES.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(source_copy=True,embedded_count=len(records),pin=digest(raw))),flush=True)
# Local, independent package tree; no link into the canonical tree and no inherited
# TGL/TGLExt project objects. Lake will rebuild the project dependency closure.
src=KERNEL/'.lake/packages'; dst=ROOT/'kernel/.lake/packages'
assert not dst.exists()
shutil.copytree(src,dst)
print('Package byte copy completed',flush=True)
packages=[]
for p in sorted(dst.iterdir()):
    if not p.is_dir(): continue
    command=['git','-C',str(p),'rev-parse','HEAD']
    run=subprocess.run(command,capture_output=True)
    packages.append(dict(name=p.name,command=command,returncode=run.returncode,
                         head=run.stdout.decode().strip(),stderr=run.stderr.decode(errors='replace')))
put(ROOT/'DEPENDENCIAS_LAKE_V353.json',json.dumps(packages,indent=2).encode())
assert digest((CANON/'um.py').read_bytes()) == EXPECTED
print('Canonical unchanged; local lake tree ready',flush=True)
