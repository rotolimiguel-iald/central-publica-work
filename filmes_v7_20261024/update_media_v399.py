from pathlib import Path
import ast, runpy

root = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
path = root / 'cinema/media_v7.py'
module = runpy.run_path(str(path))
source = path.read_text(encoding='utf-8')
old = "  while len(done)<3:\n"
new = """  while len(done)<3:
   # A previous authorized preparation may still be finishing after a reanchor.
   # Preserve its inputs until its stage lock is released; never overlap jobs.
   existing_locks=list((out/'.pipeline').glob('*.lock'))
   if existing_locks:
    require(time.monotonic()-started<args.watch_timeout,'Waiting for previous media stage timed out')
    state('WAITING_EXISTING_STAGE',stage_locks=[str(p) for p in existing_locks]);time.sleep(max(2,args.poll_seconds));continue
"""
assert source.count(old) == 1
source = source.replace(old, new)
old = "  d=load(p);state=d.get('state',{});all_entries.append((p,d,state))"
new = "  d=load(p);state=d.get('state',{})\n  if p.stat().st_mtime_ns < (root/'data/hud.json').stat().st_mtime_ns:continue\n  all_entries.append((p,d,state))"
assert source.count(old) == 1
source = source.replace(old, new)
old = "pipe.stage('asset_'+name,[tp,*inputs],"
new = "pipe.stage('asset_'+name,[tp,root/'data/hud.json',root/'data/PROVENANCE_PUBLIC.json',*inputs],"
assert source.count(old) == 1
source = source.replace(old, new)
ast.parse(source)
module['atomic'](path, source.encode('utf-8'))
print(module['pin'](path))
