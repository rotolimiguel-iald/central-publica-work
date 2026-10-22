from pathlib import Path
import hashlib, json, re, shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
seen=set(); records=[]
def visit(module):
 if not module.startswith(('TGL.','TGLExt.')) or module in seen:return
 seen.add(module)
 rel=Path(*module.split('.'))
 src=ROOT/'kernel'/rel.with_suffix('.lean')
 before=OLD/rel.with_suffix('.lean')
 assert src.read_bytes()==before.read_bytes(),str(src)
 for dep in re.findall(r'^import\s+(\S+)',src.read_text(encoding='utf-8'),re.M):visit(dep)
 obj=OLD/'.lake/build/lib/lean'/rel.with_suffix('.olean')
 b=obj.read_bytes(); dst=ROOT/'build'/rel.with_suffix('.olean')
 dst.parent.mkdir(parents=True,exist_ok=True)
 if dst.exists():assert dst.read_bytes()==b
 else:dst.write_bytes(b)
 records.append(dict(module=module,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),object_sha256=hashlib.sha256(b).hexdigest(),object_origin=str(obj)))
for m in ['TGLExt.V350ScalarDualWeight','TGLExt.V350CoreContractCounterexample']:visit(m)
p=ROOT/'DEPENDENCIAS_A1.json'
assert not p.exists()
p.write_text(json.dumps(records,indent=2),encoding='utf-8')
print(f'{len(records)} imported source/object pairs checked and copied')
