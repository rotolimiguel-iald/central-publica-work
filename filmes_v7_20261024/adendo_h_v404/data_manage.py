"""Scoped v404 data staging; no TTS/render or production mutation."""
from pathlib import Path
import sys, json, subprocess, time
import context as c
ACTOR={'id':'codex-video-v404-data','kind':'agent'}
FILES=['hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','STDOUT_LINES.json','MANIFEST.json']
def check():return c.check('V404_DATA',ACTOR)
def prepare():
 check();c.stable_seal()
 # Resume byte-identical copies after visible preparation failure.
 assert c.read(c.V/'source/um_absoluto_selo.json')['um_version']=='v402'
 paths=[]
 for part in ['source','data','replay','web/vendor/pyodide']:
  paths += [p for p in (c.V/part).iterdir() if p.is_file() and '.bak_' not in p.name and '__pycache__' not in p.parts and p.suffix!='.tmp' and not p.name.startswith(('audio_', 'AUDIO_'))]
 paths += [c.V/x for x in ['export_data.py','extend_export.py','guard_export.py','PROVENANCE_PUBLIC.json','web/replay-demo.html']]
 records=[]
 for p in sorted(set(paths)):
  dest=c.B/p.relative_to(c.V);c.atomic(dest,p.read_bytes());records.append({'original':c.pin(p),'copy':c.pin(dest)})
 c.save(c.H/'DATA_BASELINE_MANIFEST.json',{'version':'v402','files':records})
 # Only data-owned paths, never web runtime files owned by the parent.
 stage=['export_data.py','extend_export.py','guard_export.py','web/replay-demo.html']
 stage += [p.relative_to(c.V).as_posix() for part in ['replay','web/vendor/pyodide'] for p in (c.V/part).iterdir() if p.is_file() and '.bak_' not in p.name and '__pycache__' not in p.parts and p.suffix not in ('.tmp','.png') and not p.name.startswith(('TEST_','REVIEW_','DELIVERY_','REPRODUCIBILITY'))]
 for rel in stage:c.atomic(c.S/rel,(c.V/rel).read_bytes())
 intake=c.read(c.H/'SOURCE_INTAKE.json');records=[]
 for name,expected in intake['files'].items():
  p=c.N/name;assert c.pin(p)==expected
  dest=c.S/'source'/name;c.atomic(dest,p.read_bytes());records.append({'canonical':expected,'isolated':c.pin(dest)})
 c.save(c.H/'SOURCE_CAPTURE.json',{'source':'v404','source_sha256':intake['files']['um.py']['sha256'],'canonical_seal':intake['files']['um_absoluto_selo.json'],'files':records,'order':c.pin(c.ORDER),'preflight':check()})
 p=c.S/'extend_export.py';text=p.read_text(encoding='utf-8')
 old="live_gate=um.prove_qg_closure_gate(ONE,kf,independent_rite=C['void_floor_v11'])"
 new="live_gate=um.prove_qg_closure_gate(ONE,kf,independent_rite=C['void_floor_v11'],blind_null=C['void_stacking_blind'])"
 assert text.count(old)==1;text=text.replace(old,new)
 # Explicitly retain the distinction between measured flags and verdict inputs.
 needle="F['gate']['computed_count']=len(flags)-len(literal_flags)"
 added="""
gate_record=C['bandeiras_do_gate_v403']
assert gate_record['all_verified'] and gate_record['values']['n_calculated']==F['gate']['computed_count']
assert gate_record['values']['n_literal']==F['gate']['literal_count']
assert gate_record['values']['n_flags']==len(flags)
assert live_gate['gate']==C['qg_closure']['gate']
F['gate']['informative_flags']=gate_record['values']['informative']
F['gate']['n_read_by_the_verdict']=gate_record['values']['n_read_by_the_verdict']
F['gate']['flag_scope_source']='core.bandeiras_do_gate_v403.values'
"""
 assert text.count(needle)==1;c.atomic(p,text.replace(needle,needle+added).encode())
 # Builder reads existing parent-owned worker, but emits trust only under replay/.
 p=c.S/'replay/build_replay.py';text=p.read_text(encoding='utf-8')
 text=text.replace("(ROOT/'web/replay-worker.js').read_bytes()", "(pathlib.Path("+repr(str(c.V/'web/replay-worker.js'))+")).read_bytes()")
 text=text.replace("write(ROOT/'web/replay-trust.mjs',trust.encode())", "write(ROOT/'replay/replay-trust.mjs',trust.encode())")
 text=text.replace("def write(p,b):\n p.parent", "def write(p,b):\n if p.exists() and p.read_bytes()!=b:\n  import time\n  old=p.read_bytes(); backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(old);assert backup.read_bytes()==old\n p.parent")
 c.atomic(p,text.encode());c.stable_seal()
 print('PREPARED',len(records),len(paths))
def run(stage):
 check();c.stable_seal()
 args={'export':['guard_export.py'],'replay':['replay/build_replay.py','--source',str(c.S/'source/um.py'),'--hud',str(c.S/'data/hud.json')],'test':['replay/test_replay.py']}[stage]
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(c.S/args[0]),*args[1:]],cwd=c.S,capture_output=True)
 c.save(c.H/('DATA_RUN_'+stage+'.json'),{'returncode':r.returncode,'stdout':r.stdout.decode('utf-8','replace'),'stderr':r.stderr.decode('utf-8','replace')})
 print(stage,r.returncode,r.stdout.decode('utf-8','replace')[-1000:],r.stderr.decode('utf-8','replace')[-1500:])
 if r.returncode:raise SystemExit(r.returncode)
 if stage=='export':c.atomic(c.S/'PROVENANCE_PUBLIC.json',(c.S/'data/PROVENANCE_PUBLIC.json').read_bytes())
 c.stable_seal()
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 else:run(sys.argv[1])
