"""Prepared byte-backup/atomic-append helper; NO CLI and NO automatic invocation.

Parent alone may call after fresh ownership/preflight and real plan review.
Per-file atomic replace is not a transaction across all memory surfaces.
"""
import datetime,hashlib,os,uuid
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def exclusive(path,raw):
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if path.read_bytes()!=raw:raise RuntimeError('temporary/backup byte mismatch')
def append_reviewed(path,chunk,before_sha256,after_sha256,*,apply=False):
    if apply is not True:raise RuntimeError('PREPARE_ONLY: application disabled by default')
    p=Path(path);before=p.read_bytes()
    if sha(before)!=before_sha256:raise RuntimeError('target changed; refresh plan')
    after=before+chunk
    if not chunk or sha(after)!=after_sha256 or len(after)<=len(before):raise RuntimeError('append/hash/size mismatch')
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'_'+uuid.uuid4().hex
    backup=p.with_name(p.name+'.bak_'+stamp);temp=p.with_name(p.name+'.tmp_'+stamp)
    exclusive(backup,before) # Raw bytes, same folder; never removed by this helper.
    exclusive(temp,after)
    if p.read_bytes()!=before:raise RuntimeError('target changed before replacement; backup/temp retained')
    os.replace(temp,p)
    if p.read_bytes()!=after:
        restore=p.with_name(p.name+'.restore_'+stamp);exclusive(restore,backup.read_bytes());os.replace(restore,p)
        if p.read_bytes()!=before:raise RuntimeError('RESTORE_FAILED: stop visibly; backup retained')
        raise RuntimeError('post-write mismatch; restored immediate byte backup')
    return dict(path=str(p),backup=str(backup),before_sha256=sha(before),after_sha256=sha(after),bytes=len(after))
