from review_helpers import *
def main():
 a=Path(load(OUT/'SNAPSHOT_POINTER.json')['attempt']);assert load(a/'run.json')['returncode']==0
 d=OUT/('negative_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));d.mkdir()
 src=R/'probes/BadModularImplementationRightSignChanged.lean';dst=V/'ReviewControls'/src.name
 fresh(dst,src.read_bytes());fresh(d/src.name,src.read_bytes())
 env=os.environ.copy()
 for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
 env['PATH']=str(BIN)+os.pathsep+env.get('PATH','');env['GIT_OPTIONAL_LOCKS']='0'
 pkgs=load(V/'lake-manifest.json')['packages'];n=int(env.get('GIT_CONFIG_COUNT','0'))
 for i,pkg in enumerate(pkgs,n):
  env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str((V/'.lake/packages'/pkg['name']).resolve()).replace(chr(92),'/')
 env['GIT_CONFIG_COUNT']=str(n+len(pkgs))
 cmd=[str(BIN/'lake.exe'),'env','lean',str(dst)];start=time.time()
 with (d/'stdout.txt').open('xb') as out,(d/'stderr.txt').open('xb') as err:
  p=subprocess.Popen(cmd,cwd=V,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
  save(d/'process.json',dict(pid=p.pid,command=cmd,cwd=str(V),started=now()));print('NEGATIVE_STARTED',p.pid,flush=True);rc=p.wait()
 j=dict(returncode=rc,elapsed_seconds=time.time()-start,finished=now(),command=cmd,cwd=str(V),source=pin(src),own_source=pin(dst),snapshot=pin(d/src.name),stdout=pin(d/'stdout.txt'),stderr=pin(d/'stderr.txt'),own_execution=True,dev_objects_used=False)
 save(d/'run.json',j);j['run']=pin(d/'run.json');save(OUT/'negative_control_own.json',j)
 text=(d/'stdout.txt').read_text(encoding='utf8');assert rc==1 and 'type mismatch' in text.lower()
 assert not any(w in text.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
 print('NEGATIVE_EXIT',rc,'TYPE_MISMATCH',flush=True)
if __name__=='__main__':main()
