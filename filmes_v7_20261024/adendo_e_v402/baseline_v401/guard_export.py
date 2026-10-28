from pathlib import Path
import sys,os,runpy,json,hashlib
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;os.chdir(W);os.environ['MPLCONFIGDIR']=str(W/'source/mpl_config')
seal=json.loads((W/'source/um_absoluto_selo.json').read_bytes())
for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json']:
 assert hashlib.sha256((W/'source'/name).read_bytes()).hexdigest()==seal['sha256'][name],name
def inside(v):
 if isinstance(v,int):return
 if not Path(os.fsdecode(v)).resolve().is_relative_to(W):raise PermissionError('Write outside isolated film tree')
def audit(event,args):
 if event=='open':
  path,mode,flags=args
  if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):inside(path)
 elif event in ('os.remove','os.rmdir','os.mkdir','os.chmod','os.utime'):inside(args[0])
 elif event in ('os.rename','os.replace'):inside(args[0]);inside(args[1])
 elif event in ('subprocess.Popen','os.system','socket.connect','socket.bind'):raise PermissionError('Processes/network forbidden during extraction')
sys.addaudithook(audit)
runpy.run_path(str(W/'export_data.py'),run_name='__main__')
