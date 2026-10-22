"""Copy the existing verified Lean cache into isolation; never link to production."""
import hashlib
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
SOURCE=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\build\lib\lean')
DEST=OUT/'formal_verified/lib'

def main():
    assert not (OUT/'formal_verified/CACHE_RECEIPT.json').exists()
    entries=[]
    for src in sorted(SOURCE.rglob('*.olean')):
        rel=src.relative_to(SOURCE);dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        before=src.read_bytes()
        with dst.open('xb') as f:f.write(before)
        assert dst.read_bytes()==before
        assert src.read_bytes()==before
        entries.append({'relative':str(rel),'bytes':len(before),'sha256':hashlib.sha256(before).hexdigest()})
    new(OUT/'formal_verified/CACHE_RECEIPT.json',{'source':str(SOURCE),'destination':str(DEST),'entries':entries,'count':len(entries),'bytes':sum(x['bytes'] for x in entries),'mechanism':'ordinary independent byte copies, no links or junctions','compiled_here':False})
    print({'count':len(entries),'bytes':sum(x['bytes'] for x in entries)})

if __name__=='__main__':main()
