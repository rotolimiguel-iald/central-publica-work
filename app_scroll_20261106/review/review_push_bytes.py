from pathlib import Path
import ast,hashlib,json,subprocess,os,types,sys
sys.dont_write_bytecode=True
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106');M=W/'mobile';R=W/'review';script=M/'push_reviewed_bytes.py'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
sys.path.insert(0,str(M))
import publication_guards as pg
plan,audit,auth=pg.checked('push') # read-only guard path, no intent/push
repo=pg.REPO;c=pg.read(pg.D/'COMMIT.json');tip=c['commit'];base=plan['baseline']['base_commit']
def git(*args):
 env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
 p=subprocess.run(['git','-C',str(repo),*args],capture_output=True,env=env)
 require(p.returncode==0,'Read-only git query failed')
 return p.stdout
def names(*args):return set(git(*args,'-z').decode().strip('\0').split('\0'))-{''}
require(git('rev-parse','HEAD').decode().strip()==tip,'HEAD mismatch')
require(git('rev-parse',tip+'^').decode().strip()==base,'Parent mismatch')
require(git('symbolic-ref','HEAD').decode().strip()=='refs/heads/codex/mobile-release','Branch mismatch')
require(not names('diff','--cached','--name-only'),'Staged edits')
require(names('diff','HEAD','--name-only')=={'android/app/build.gradle'},'Unexpected dirty files')
require(not names('diff','--ignore-space-at-eol','HEAD','--name-only'),'Non-EOL diff')
require(names('diff','--name-only',base,tip)==pg.FILES,'Delta outside six files')
for name,h in c['pins'].items():require(sha((repo/name).read_bytes())==h==sha(git('show',tip+':'+name)),'Raw bytes differ')
require(not (pg.D/'PUSH_INTENT.json').exists(),'Push intent already exists')
attrs=git('check-attr','text','eol','--','android/app/build.gradle').decode().strip()
# Exercise the actual helper function, with every external effect replaced by inert doubles.
tree=ast.parse(script.read_text());body=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
code=compile(body,'reviewed-push-helper','exec');tests=[]
for mode in ['pass','review_drift','branch','index','other_dirty','semantic_diff','working_pins','commit_blob','remote_changed','existing_intent','post_push_uncertain']:
 effects=[];remote_calls=[0]
 values={'a':sha(b'a'),'b':sha(b'b')};receipt={'status':'COMMITTED_VERIFIED','base':'base','commit':'tip','pins':values}
 def read(p):
  if p.name=='PUSH_BYTES_REVIEW.json':return {'status':'PASS','script_sha256':'bad' if mode=='review_drift' else sha(script.read_bytes())}
  return receipt
 def branch():require(mode!='branch','branch')
 def gn(*args):
  if args==('diff','--cached','--name-only'):return {'extra'} if mode=='index' else set()
  if args==('diff','HEAD','--name-only'):return {'other'} if mode=='other_dirty' else {'android/app/build.gradle'}
  if '--ignore-space-at-eol' in args:return {'android/app/build.gradle'} if mode=='semantic_diff' else set()
  return set(values)
 def gg(*args):
  if args[0]=='rev-parse':return b'base'
  if args[0]=='show':return b'bad' if mode=='commit_blob' else args[1].split(':')[1].encode()
  if args[0]=='push':effects.append('push');return b''
  raise AssertionError(args)
 def remote():
  remote_calls[0]+=1
  return 'other' if mode=='remote_changed' or (mode=='post_push_uncertain' and remote_calls[0]>1) else ('base' if remote_calls[0]==1 else 'tip')
 def intent(*args):require(mode!='existing_intent','existing');effects.append('intent')
 g=types.SimpleNamespace(branch=branch,head=lambda:'tip',names=gn,git=gg,pins=lambda plan:{} if mode=='working_pins' else values,remote=remote,BRANCH='refs/heads/codex/mobile-release')
 ns={'g':g,'HERE':M,'D':pg.D,'FILES':set(values),'checked':lambda phase:({'baseline':{'base_commit':'base'}},None,None),'intent':intent,'pin':lambda p:{'path':str(p)},'read':read,'report':lambda *a:effects.append('report'),'require':require,'sha':sha}
 exec(code,ns);error=None
 try:ns['push']()
 except RuntimeError as e:error=str(e)
 if mode=='pass':require(error is None and effects==['intent','push','report'],'Positive fixture')
 elif mode=='post_push_uncertain':require(error is not None and effects==['intent','push'],'Uncertain result must retain intent and omit success')
 else:require(error is not None and not effects,'Negative must precede push/intent')
 tests.append({'name':mode,'status':'PASS','simulated_effects':effects})
report={'status':'PASS','reviewer':'codex-scroll-independent-reviewer','script_sha256':sha(script.read_bytes()),'tests':tests,'observed':{'commit':tip,'base':base,'six_raw_working_plan_commit_pins_verified':True,'index_empty':True,'dirty_only':'android/app/build.gradle','ignore_space_at_eol_diff_empty':True,'attributes':attrs,'push_intent_absent_at_review':True,'checked_push_guard':'PASS, read-only','remote_not_queried_by_reviewer':True},'pins':[pin(script),pin(M/'git_release42.py'),pin(M/'publication_guards.py'),pin(M/'PLAN.json'),pin(pg.D/'COMMIT.json'),pin(M/'PARENT_PUBLICATION_READY.json')],'findings':[],'scope':'Small helper review only; no real push/intent/commit/build/installation or remote mutation. Actual helper tested with inert doubles. Existing checked/branch/raw pins/six-file allowlist/remote preflight/exclusive intent and non-force push retained. Remote state must still pass at execution. No mobile completion acceptance.'}
with (R/'PUSH_BYTES_REVIEW.json').open('xb') as f:f.write((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':'PASS','tests':len(tests),'script_sha256':report['script_sha256'],'commit':tip,'report':str(R/'PUSH_BYTES_REVIEW.json')}))
