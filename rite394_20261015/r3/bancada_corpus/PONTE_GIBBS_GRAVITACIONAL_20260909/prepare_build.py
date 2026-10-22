from pathlib import Path
import os, json, hashlib, datetime
root=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out=Path(__file__).resolve().parent
assert out.is_relative_to(root)
def new(p,b):
    assert p.resolve().is_relative_to(root) and not p.exists()
    temp=p.with_name(p.name+'.tmp')
    with temp.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes()==b
    os.replace(temp,p)
    assert p.read_bytes()==b
def pin(p):
    b=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
specs={
 'ProbeResponseRecord':root/'RESPOSTA_MICROSCOPICA_FONTE_20260909',
 'TransverseGibbsResponse':root/'RESPOSTA_GIBBS_TRANSVERSAL_20260909_180432_151368',
 'MixedQuadraticGibbsResponse':root/'RESPOSTA_GIBBS_MISTA_QUADRATICA_20260909_181702_377524'
}
cached={}
for module,folder in specs.items():
    source=folder/(module+'.lean')
    good=[]
    for receipt in sorted(folder.glob('BUILD_*/BUILD_RESULT.json')):
        data=json.loads(receipt.read_bytes())
        if data['status']=='PASS_COMPILED_SCOPE' and any(
            s['sha256']==pin(source)['sha256'] for s in data['sources']):
            assert (receipt.parent/(module+'.lean')).read_bytes()==source.read_bytes()
            good.append(receipt)
    assert good, 'No current PASS for '+module
    cached[module]={'source':source.as_posix(),'build':good[-1].parent.as_posix()}
builder=root/'RESPOSTA_MICROSCOPICA_FONTE_20260909'/'build_source.py'
new(out/'build_source.py',builder.read_bytes())
config={'approved_library':(root/'INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582'/'BUILD_SUCCESSOR_20260909_174751_385895').as_posix(),'cached':cached}
new(out/'CONFIG_BUILD.json',(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode())
new(out/'BUILDER_PROVENANCE.json',(json.dumps({'builder_source':pin(builder),'copy':pin(out/'build_source.py'),'transformations':[]},indent=2)+'\n').encode())
print(json.dumps(config,ensure_ascii=False,indent=2))
