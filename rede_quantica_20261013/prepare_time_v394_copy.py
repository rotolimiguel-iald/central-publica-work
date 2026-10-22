"""Create immutable v393 baseline and isolated working candidate from verified bytes."""
import ast,json,os,hashlib,datetime as dt
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
SRC=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
assert (OUT/'CLAIM_RECEIPT.json').exists()
assert not (OUT/'SOURCE_BASELINE.json').exists()
copied=[]
for name in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','um_absoluto.json']:
    source=SRC/name; raw=source.read_bytes(); dst=OUT/'baseline'/name;dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(raw)
    assert dst.read_bytes()==raw
    copied.append({'source':pin(source),'copy':pin(dst)})
source=OUT/'baseline/um.py'; text=source.read_text(encoding='utf-8-sig');tree=ast.parse(text)
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets))
embedded=ast.literal_eval(node.value)
candidate=OUT/'candidate'; candidate.mkdir()
with (candidate/'um.py').open('xb') as f:f.write(source.read_bytes())
materialized=[]
for rel,body in embedded.items():
    dst=candidate/'tgl_kernel'/rel
    assert dst.resolve().is_relative_to((candidate/'tgl_kernel').resolve())
    new(dst,body)
    src=SRC/'tgl_kernel'/rel
    materialized.append({'relative':rel,'candidate':pin(dst),'canonical_match':src.exists() and src.read_bytes()==dst.read_bytes()})
seal=json.loads((OUT/'baseline/um_absoluto_selo.json').read_bytes())
assert seal['um_version']=='v393'
new(OUT/'SOURCE_BASELINE.json',{'unit':'F1.TEMPO.V394','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'version':'v393','copied':copied,'initial_candidate':pin(candidate/'um.py'),'embedded_materialized':materialized,'embedded_count':len(embedded),'canonical_kernel_matches':sum(x['canonical_match'] for x in materialized),'no_junctions':True,'code_executed':False})
print(json.dumps({'copied':len(copied),'candidate':str(candidate/'um.py'),'embedded_count':len(embedded),'canonical_matches':sum(x['canonical_match'] for x in materialized)},ensure_ascii=False))
