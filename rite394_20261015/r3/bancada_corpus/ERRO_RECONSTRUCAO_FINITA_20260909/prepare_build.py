from pathlib import Path
import hashlib, json, os, datetime
folder=Path(__file__).resolve().parent
root=folder.parent
source=root/'PONTE_GIBBS_GRAVITACIONAL_20260909'/'build_source.py'
raw=source.read_bytes()
text=raw.decode('utf8')
changes=[('len(receipt["runs"])==8','len(receipt["runs"])==9'),
         ('len(receipt["cached_modules"])==72','len(receipt["cached_modules"])==77'),
         ('len(approved_plan["sources"])==77','len(approved_plan["sources"])==83'),
         ('transposed77 library','transposed83 library'),('Approved77 module','Approved83 module')]
for a,b in changes:
    assert text.count(a)==1,a
    text=text.replace(a,b)
def new(path,data):
    assert not path.exists() and path.resolve().is_relative_to(root.resolve())
    temp=path.with_suffix(path.suffix+'.tmp_'+datetime.datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==data
    temp.rename(path)
    assert path.read_bytes()==data
new(folder/'build_source.py',text.encode('utf8'))
cfg={'approved_library':str(root/'INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394'/'BUILD_SUCCESSOR_20260909_192313_320129'),'cached':{}}
new(folder/'CONFIG_BUILD.json',(json.dumps(cfg,indent=2)+'\n').encode())
new(folder/'BUILDER_PROVENANCE.json',(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'changes':changes,'result_sha256':hashlib.sha256(text.encode('utf8')).hexdigest()},indent=2)+'\n').encode())
print('Prepared leaf builder against approved83; no source executed.')
