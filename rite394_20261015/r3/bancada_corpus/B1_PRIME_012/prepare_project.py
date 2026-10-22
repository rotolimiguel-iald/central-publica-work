from support import *
import concurrent.futures, shutil, time
SOURCE=ROOT.parent/"TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA"/"kernel"
STAGE=ROOT/"kernel.copying"
assert not STAGE.exists() and not (ROOT/"kernel").exists()
STAGE.mkdir()
paths=[]
for p in SOURCE.rglob("*"):
    r=p.relative_to(SOURCE)
    if r.parts[0]==".lake" and (len(r.parts)<2 or r.parts[1]!="packages"): continue
    if p.is_symlink() or p.is_junction(): raise RuntimeError(f"External-link risk: {p}")
    if p.is_file(): paths.append((p,r))
print(f"COPY {len(paths)} files, real bytes, no source build objects",flush=True)
started=stamp()
def copy_one(item):
    p,r=item; target=STAGE/r; target.parent.mkdir(parents=True,exist_ok=True)
    tmp=target.with_name(target.name+".copying")
    before=p.stat(); h=digest(p)
    shutil.copyfile(p,tmp)
    assert tmp.stat().st_size==before.st_size and digest(tmp)==h
    assert p.stat().st_mtime_ns==before.st_mtime_ns
    os.replace(tmp,target)
    return dict(path=r.as_posix(),bytes=before.st_size,sha256=h)
entries=[]; last=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for row in pool.map(copy_one,paths):
        entries.append(row)
        if time.monotonic()-last>20:
            print(f"COPIED {len(entries)}/{len(paths)}",flush=True);last=time.monotonic()
os.replace(STAGE,ROOT/"kernel")
record(ROOT/"PROVENIENCIA_COPIA.json",dict(source=str(SOURCE),destination=str(ROOT/"kernel"),started_utc=started,finished_utc=stamp(),mode="byte copies; sha256 source/destination; no links",base_build_copied=False,packages_rebuilt=False,files=entries))
print(f"READY {len(entries)} files {sum(e['bytes'] for e in entries)} bytes",flush=True)
