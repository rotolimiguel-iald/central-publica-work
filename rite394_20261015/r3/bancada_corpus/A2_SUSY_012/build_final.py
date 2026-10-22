from support import *
import subprocess,sys
rows=[]
for module in ['TGLExt.V354CoreProjectionLattice','TGLExt.V354ProjectionTraceSubadditivity','TGLExt.V354RegularSusy']:
 p=subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'run_lean.py'),module],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 row=dict(module=module,returncode=p.returncode)
 rows.append(row)
 atomic(ROOT/'final_build_logs'/(module+'.txt'),p.stdout)
 print(p.stdout.decode('utf8'),flush=True)
 if p.returncode!=0: break
record(ROOT/('FINAL_BUILD.json' if all(x['returncode']==0 for x in rows) and len(rows)==3 else 'FINAL_BUILD_FAILED.json'),dict(timestamp=stamp(),rows=rows))
sys.exit(p.returncode)
