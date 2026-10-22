from support import *
import concurrent.futures,shutil,time
A=ROOT.parent/"TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k"
B=ROOT.parent/"TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/kernel"
S=ROOT/"kernel.copying_v2";assert not S.exists() and not (ROOT/"kernel").exists();S.mkdir()
common=[]
for fam in ["TGL","TGLExt"]:
    for p in (B/fam).glob("*.lean"):
        q=A/fam/p.name
        if q.exists() and digest(p)!=digest(q):common.append(dict(a=str(q),b=str(p),sha_a=digest(q),sha_b=digest(p)))
record(ROOT/"COMPARACAO_BASES.json",dict(common_source_differences=common))
assert all(Path(x["a"]).relative_to(A).as_posix()=="TGL/Audit.lean" for x in common),"Unexpected source difference"
# TGL/Audit from A1 is kept. Task-specific audits do not depend on its historical list.
files=[]
for p in A.rglob("*"):
    rel=p.relative_to(A)
    if len(rel.parts)>1 and rel.parts[:2]==(".lake","config"):continue
    if p.is_symlink() or p.is_junction():raise RuntimeError(str(p))
    if p.is_dir():(S/rel).mkdir(parents=True,exist_ok=True)
    elif p.is_file():files.append((p,rel))
print(f"COPY {len(files)} files including local caches and empty directories",flush=True)
def cp(entry):
    p,rel=entry;q=S/rel;q.parent.mkdir(parents=True,exist_ok=True);t=q.with_name(q.name+".copying")
    st=p.stat();h=digest(p);shutil.copyfile(p,t)
    assert digest(t)==h and p.stat().st_mtime_ns==st.st_mtime_ns
    os.replace(t,q);return dict(path=rel.as_posix(),source=str(p),bytes=st.st_size,sha256=h)
rows=[];last=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for row in pool.map(cp,files):
        rows.append(row)
        if time.monotonic()-last>25:print(f"COPIED {len(rows)}/{len(files)}",flush=True);last=time.monotonic()
for fam in ["TGL","TGLExt"]:
    for p in (B/fam).glob("*.lean"):
        rel=Path(fam)/p.name
        if not (S/rel).exists():rows.append(cp((p,rel)))
os.replace(S,ROOT/"kernel")
record(ROOT/"PROVENIENCIA_COPIA.json",dict(time_utc=stamp(),source_a=str(A),source_b=str(B),destination=str(ROOT/"kernel"),mode="byte copies with source/destination sha256; no external links; package and unaffected project cache inherited",files=rows))
print("COPY READY",len(rows),flush=True)
