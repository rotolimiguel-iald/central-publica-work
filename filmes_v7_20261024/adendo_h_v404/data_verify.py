"""Data-only reproduction and guard controls; no remote requests."""
import sys,json,ast,subprocess
import context as c
import data_manage as manager
from data_compare import run as compare

def main():
 manager.check();first=c.read(c.H/'NUMERIC_COMPARISON.json');assert first['status']=='PASS_NUMERIC_PENDING_DISTINCT_REVIEW'
 c.save(c.H/'DATA_FIRST_COMPARISON.json',first)
 paths=[c.S/'data'/n for n in manager.FILES]+[c.S/'PROVENANCE_PUBLIC.json']
 paths += [c.S/'replay'/n for n in ['replay-manifest.json','um_nucleo_filme.py','um_scalar_excerpt.py','anchors.json','replay_runner.py','replay-trust.mjs']]
 before={str(p.relative_to(c.S)):c.pin(p) for p in paths}
 manager.run('export');manager.run('replay')
 after={str(p.relative_to(c.S)):c.pin(p) for p in paths}
 equal=before==after;c.save(c.H/'DATA_REPRODUCIBILITY.json',{'status':'PASS' if equal else 'STOP','before':before,'after':after,'exact_byte_equality':equal})
 assert equal,'STOP_NONREPRODUCIBLE'
 # Audit callbacks taken verbatim from installed isolated guard. Controls use sys.audit only,
 # therefore no out-of-scope file is created and no actual network/process is attempted.
 raw=(c.S/'guard_export.py').read_text(encoding='utf-8');tree=ast.parse(raw)
 definitions='\n'.join(ast.get_source_segment(raw,n) for n in tree.body if isinstance(n,ast.FunctionDef))
 controls=[('open', [str(c.H/'DATA_FORBIDDEN_SENTINEL'),'w',0]),('os.remove',[str(c.H/'DATA_FORBIDDEN_SENTINEL')]),('os.rename',[str(c.S/'data/x'),str(c.H/'DATA_FORBIDDEN_SENTINEL')]),('subprocess.Popen',[]),('os.system',[]),('socket.connect',[]),('socket.bind',[])]
 code='import sys,os\nfrom pathlib import Path\nW=Path('+repr(str(c.S))+')\n'+definitions+'\nsys.addaudithook(audit)\nresults=[]\n'
 code+='for event,args in '+repr(controls)+':\n try:sys.audit(event,*args)\n except PermissionError:results.append((event,True))\n else:results.append((event,False))\nprint(repr(results))\nassert all(ok for _,ok in results)\n'
 proc=subprocess.run([sys.executable,'-B','-X','utf8','-c',code],capture_output=True,text=True,encoding='utf-8')
 c.save(c.H/'DATA_GUARD_CONTROLS.json',{'status':'PASS' if proc.returncode==0 else 'FAIL','returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'guard':c.pin(c.S/'guard_export.py'),'method':'Emit audited forbidden events; no actual outside mutation, process or socket attempted'})
 assert proc.returncode==0
 compare();c.stable_seal()
 print('REPRODUCIBILITY_AND_GUARD_PASS')
if __name__=='__main__':main()
