from pathlib import Path
import os,json
base=Path(r'C:\IALD\Central de Patentes\Chatgpt')
out=Path(__file__).resolve().parent
source=base/'COLAGEM_SUAVE_REAL_20260909_164537_702751'/'build_smooth_gluing.py'
old=source.read_bytes()
text=old.decode('utf-8')
changes={
 'len(receipt["runs"])==21':'len(receipt["runs"])==12',
 'len(receipt["cached_modules"])==45':'len(receipt["cached_modules"])==63',
 'len(approved_plan["sources"])==63':'len(approved_plan["sources"])==72',
 'transposed63':'transposed72',
 'Approved63':'Approved72',
 '(?:noncomputable\\s+)?(abbrev|def|theorem|structure)':'(?:local\\s+)?(?:noncomputable\\s+)?(abbrev|def|theorem|structure|instance)'}
for a,b in changes.items():
    assert text.count(a)==1,(a,text.count(a))
    text=text.replace(a,b)
def new(p,data):
    assert not p.exists()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==data
    os.rename(tmp,p)
    assert p.read_bytes()==data
new(out/'build_selector_bridge.py',text.encode('utf-8'))
config={'approved_library':(base/'INTEGRADOR_LOCAL_GERAL_20260909_170426_647362'/'BUILD_SUCCESSOR_20260909_171052_146967').as_posix()}
new(out/'CONFIG_BUILD.json',(json.dumps(config,indent=2)+'\n').encode())
assert source.read_bytes()==old
print('Created fresh builder for approved72 library; source preserved.')
