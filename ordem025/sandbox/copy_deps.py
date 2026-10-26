from pathlib import Path
import hashlib,json,re,shutil,sys
ROOT=Path(__file__).resolve().parent
KERNEL=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
seen=set();records=json.loads((ROOT/'DEPENDENCY_COPIES.json').read_text()) if (ROOT/'DEPENDENCY_COPIES.json').exists() else []
def visit(module):
    if module in seen or not module.startswith('TGLExt.'):return
    seen.add(module)
    src=KERNEL/(module.replace('.','/')+'.lean')
    if not src.exists():raise RuntimeError(str(src))
    for imp in re.findall(r'^import\s+([^\r\n]+)',src.read_text(encoding='utf-8'),re.M):
        for m in imp.split():visit(m)
    cached=KERNEL/'.lake/build/lib/lean'/module.replace('.','/')
    for f in cached.parent.glob(cached.name+'.*'):
        target=ROOT/f.relative_to(KERNEL/'.lake/build/lib/lean')
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(f.read_bytes()).digest():continue
        shutil.copyfile(f,target)
        records.append({'source':str(f),'target':str(target),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
for m in sys.argv[1:] or ['TGLExt.Fundacao','TGLExt.NoFullWitness','TGLExt.TheGreatAttractor','TGLExt.BisognanoWichmann','TGLExt.Solder4D','TGLExt.O16.BoostRepresentationBridges']:visit(m)
(ROOT/'DEPENDENCY_COPIES.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print({'modules':len(seen),'files':len(records),'bytes':sum(r['bytes'] for r in records)})
