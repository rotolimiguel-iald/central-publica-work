"""Read-only exact numeric/structural recheck against preserved v399 baseline."""
import argparse,hashlib,json,pathlib,math
HERE=pathlib.Path(__file__).resolve().parent
DEFAULT_ROOT=pathlib.Path(r'C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7')
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):return sum([diff(a[k],b[k],path+'/'+k) if k in a and k in b else [path+'/'+k] for k in sorted(a.keys()|b.keys())],[])
 if isinstance(a,list):return [path+'/LENGTH'] if len(a)!=len(b) else sum([diff(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[])
 return [] if a==b else [path]
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,default=DEFAULT_ROOT);p.add_argument('--baseline',type=pathlib.Path,default=HERE/'baseline_v399');a=p.parse_args()
 allowed={'hud.json':{'/items/33/text','/items/33/value','/result_hash16','/seal_pin','/seal_timestamp','/seal_version','/selo_timestamp','/stdout_sha256'},'frames.json':set(),'scene.json':{'/source_sha256'},'PROVENANCE_PUBLIC.json':{'/generated_at','/seal_version','/selo/result_hash','/selo/timestamp','/um_sha16','/sources/rodada_v399_stdout.txt','/sources/rodada_v400_stdout.txt','/sources/tgl_kernel_proof_manifest.json/sha256','/sources/um.py/bytes','/sources/um.py/sha256','/sources/um_absoluto.json/bytes','/sources/um_absoluto.json/sha256','/sources/um_absoluto_selo.json/bytes','/sources/um_absoluto_selo.json/sha256'},'STDOUT_LINES.json':{'/source','/source_sha256'}}
 seal=json.loads((a.root/'source/um_absoluto_selo.json').read_bytes());oldseal=json.loads((a.baseline/'source/um_absoluto_selo.json').read_bytes());assert seal['um_version']=='v400' and oldseal['um_version']=='v399'
 for root,s in [(a.root,seal),(a.baseline,oldseal)]:
  for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json']:assert hashlib.sha256((root/'source'/name).read_bytes()).hexdigest()==s['sha256'][name]
  hud=json.loads((root/'data/hud.json').read_bytes());assert hud['items'][33]['value']==hud['items'][33]['text']==s['sha256']['um.py'][:16]
 counts={};unexpected=[]
 for name,permit in allowed.items():
  x=json.loads((a.baseline/'data'/name).read_bytes());y=json.loads((a.root/'data'/name).read_bytes());ds=diff(x,y);counts[name]=len(ds);unexpected.extend(name+':'+q for q in ds if q not in permit)
 x=json.loads((a.baseline/'source/tgl_kernel_proof_manifest.json').read_bytes());y=json.loads((a.root/'source/tgl_kernel_proof_manifest.json').read_bytes());assert set(diff(x,y))<={'/timestamp','/build_stdout_sha256'}
 prov=json.loads((a.root/'data/PROVENANCE_PUBLIC.json').read_bytes());assert len(prov['anchors'])>=64 and prov['anchors_all_ok'];assert all(q['ok'] and math.isfinite(q['residual']) and abs(q['json_value']-q['live_value'])<=q['tol'] for q in prov['anchors'])
 print(json.dumps({'status':'STOP' if unexpected else 'PASS','source':seal['um_version'],'source_sha256':seal['sha256']['um.py'],'metadata_difference_counts':counts,'scientific_or_unclassified_differences':unexpected}))
 raise SystemExit(bool(unexpected))
if __name__=='__main__':main()
