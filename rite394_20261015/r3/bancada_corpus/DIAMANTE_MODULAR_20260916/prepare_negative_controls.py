from pathlib import Path
import json, os
ROOT=Path(__file__).resolve().parent
plans=[
    ('ModularCornerCounterexample.lean','FalseCompressedFlow.lean',
     'theorem compressed_flow_half_turn : p*flow (Real.pi/2)*p=0 := by',
     'theorem compressed_flow_half_turn : p*flow (Real.pi/2)*p=p := by'),
    ('ModularRemainderDensity.lean','FalseEntropySign.lean',
     'relativeEntropy rho vacuum + (entropy rho-entropy vacuum) -',
     'relativeEntropy rho vacuum - (entropy rho-entropy vacuum) -')]
directory=ROOT/'negative';directory.mkdir(exist_ok=True)
for source,name,old,new in plans:
    text=(ROOT/source).read_text(encoding='utf8')
    assert text.count(old)==1
    target=directory/name
    assert not target.exists()
    tmp=target.with_suffix('.tmp');data=text.replace(old,new).encode('utf8')
    tmp.write_bytes(data);assert tmp.read_bytes()==data;os.replace(tmp,target)
print(json.dumps([name for _,name,_,_ in plans]))
