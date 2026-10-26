from pathlib import Path
R=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um')
V=R/'delivery_v7'
old=(R/'Chatgpt/cinema_origin_20260914_071728/export_frames_v5_origin.py').read_text(encoding='utf-8')
old=old.replace("NOS = os.path.dirname(os.path.abspath(__file__))", "NOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')")
old=old.replace('rodada_v350_stdout.txt','rodada_v398_stdout.txt')
old=old.replace("theorems_clean, theorems_total = int(m.group(1)), int(m.group(2))", "proof = C['estatuto_da_prova_v391']['prova_1_kernel']\ntheorems_clean, theorems_total = proof['n_theorems_clean'], proof['n_theorems_expected']\nassert (theorems_clean,theorems_total)==(int(m.group(1)),int(m.group(2)))")
old=old.replace('um.SEALED_CODATA_ALPHA * ONE','um.ALPHA_FINE_CODATA_2018 * ONE')
old=old.replace("'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')", "'generated_at': selo['timestamp']")
old=old.replace("'path': p, 'bytes':", "'path': n, 'bytes':")
old=old.replace('NOT_FALSIFIED != CONFIRMED','NOT_FALSIFIED; nature decides')
old=old.replace('PROVED = theorem in kernel; CONFIRMED = judgement, forbidden; NOT_FALSIFIED is never CONFIRMED;', 'PROVED = theorem in kernel; nature decides;')
old=old.replace("write('hud.json', hud); write('frames.json', F, compact=True); write('MANIFEST.json', manifest)", "exec(compile(open(os.path.join(VID,'extend_export.py'),encoding='utf-8').read(), 'extend_export.py', 'exec'))\nwrite('hud.json', hud); write('frames.json', F, compact=True); write('MANIFEST.json', manifest)")
old=old.replace("for a in anchors:\n    print(","for a in []:\n    print(")
(V/'export_data.py').write_bytes(old.encode('utf-8'))
guard='''from pathlib import Path
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
'''
(V/'guard_export.py').write_bytes(guard.encode())
print(V/'export_data.py')
