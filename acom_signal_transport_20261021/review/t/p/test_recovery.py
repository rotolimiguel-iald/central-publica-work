"""Offline crash recovery regressions in a new directory, no provider adapter."""
from pathlib import Path
from unittest.mock import patch
import json
import acom_signal_codec as p

ROOT=Path(__file__).resolve().parent/'recovery_R2'
ROOT.mkdir(exist_ok=False)
checks={}
ctx=p.Context('alice','g1','c1')
raw=b'local recovery exact bytes'*100
frames=list(p.encode(ctx,'same-request','query',p.slices(raw)))
s=p.Store(ROOT/'store')
rename=p.os.rename
def crash(src,dst):
    if str(src).endswith('.tmp'):
        raise InterruptedError('injected after fsync before rename')
    return rename(src,dst)
try:
    with patch.object(p.os,'rename',crash):s.receive(ctx,iter(frames))
except InterruptedError:pass
else:raise AssertionError('injection did not fire')
tmp=s._path(ctx,'blocks',p.sha(raw)).with_name(p.sha(raw)+'.tmp')
assert tmp.read_bytes()==raw
assert s.db.execute('SELECT count(*) FROM requests').fetchone()[0]==0
s.close();s=p.Store(ROOT/'store')
r=s.receive(ctx,iter(frames))
assert Path(r['path']).read_bytes()==raw and not tmp.exists()
checks['crash_fsync_rename_reopen_same_frames_id']=True
r=s.receive(ctx,iter(frames))
assert r['replayed'] and not r['dispatch_allowed']
checks['second_replay_no_dispatch']=True
path=s._path(ctx,'blocks',p.sha(raw))
tmp.write_bytes(raw);s._put(ctx,path,raw)
assert not tmp.exists() and path.read_bytes()==raw
checks['valid_destination_and_orphan_idempotent']=True
def refuse(name,fn):
    try:fn()
    except p.Refusal:checks[name]=True
    else:raise AssertionError(name)
for label,bad in [('wrong_size',b'x'),('wrong_hash',b'x'*len(raw))]:
    path.unlink();tmp.write_bytes(bad)
    refuse('orphan_'+label,lambda:s._put(ctx,path,raw))
    assert tmp.read_bytes()==bad and not path.exists()
    tmp.unlink();s._put(ctx,path,raw)
tmp.write_bytes(b'x'*len(raw))
refuse('valid_destination_conflicting_tmp',lambda:s._put(ctx,path,raw))
assert path.read_bytes()==raw and tmp.exists();tmp.unlink()
path.write_bytes(b'x'*len(raw));tmp.write_bytes(raw)
refuse('conflicting_destination_preserved',lambda:s._put(ctx,path,raw))
assert path.read_bytes()==b'x'*len(raw) and tmp.read_bytes()==raw
other=p.Context('bob','g1','c1')
refuse('foreign_scope_path',lambda:s._put(other,path,raw))
refuse('outside_store_path',lambda:s._put(ctx,ROOT/p.sha(raw),raw))
refuse('unauthenticated_recovery',lambda:s._put(p.Context('alice','g1','c1',False),path,raw))
s.close()
(ROOT/'RESULT.json').write_text(json.dumps({'status':'PASS','checks':checks,'provider_calls':0,'network_calls':0},indent=2),encoding='utf-8')
print(json.dumps({'recovery':'PASS','checks':len(checks)}))
