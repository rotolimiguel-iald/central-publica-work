"""Parent-only executor of prepared three-surface append; disabled without --apply."""
import argparse,json,hashlib
from pathlib import Path
from atomic_append import append_reviewed,exclusive
from prepare_memory_R2 import validate,TARGETS
HERE=Path(__file__).resolve().parent
PLAN=HERE/'FINAL_R1/PLAN.json'
PLAN_SHA='6ef802b3f34dfc717e9773733fe86a4e0aa7d8ddd7cb5232a8057c1c19abc5c4'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,message):
 if not ok:raise RuntimeError(message)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true',required=True);parser.parse_args()
 require(sha(PLAN.read_bytes())==PLAN_SHA,'Plan changed')
 plan=json.loads(PLAN.read_bytes());require(plan['status']=='PREPARED_VERIFIED_NOT_APPLIED','Invalid plan')
 require([Path(i['path']).resolve() for i in plan['surfaces']]==[p.resolve() for p in TARGETS],'Unexpected surfaces')
 pins,*_=validate();require(pins==plan['evidence'],'Final evidence changed')
 chunk=Path(plan['append']['path']).read_bytes();require(sha(chunk)==plan['append']['sha256'],'Append changed')
 require(sha(Path(plan['helper']['path']).read_bytes())==plan['helper']['sha256'],'Atomic helper changed')
 for item in plan['surfaces']:
  raw=Path(item['path']).read_bytes()
  require(sha(raw)==item['before_sha256'] and len(raw)==item['before_bytes'],'Memory baseline changed')
  require(sha(raw+chunk)==item['after_sha256'] and len(raw+chunk)==item['after_bytes'],'Append output mismatch')
 intent=HERE/'FINAL_R1/APPLICATION_INTENT.json';receipt=HERE/'FINAL_R1/APPLIED.json'
 require(not intent.exists() and not receipt.exists(),'Existing intent: reconcile, do not replay')
 exclusive(intent,json.dumps({'plan_sha256':PLAN_SHA,'surfaces':[i['path'] for i in plan['surfaces']],'multi_file_atomic':False},indent=2).encode())
 outcomes=[]
 for item in plan['surfaces']:
  result=append_reviewed(item['path'],chunk,item['before_sha256'],item['after_sha256'],apply=True);outcomes.append(result)
  exclusive(HERE/('FINAL_R1/APPLIED_SURFACE_'+str(len(outcomes))+'.json'),json.dumps(result,indent=2).encode())
 exclusive(receipt,json.dumps({'status':'APPLIED_THREE_OPERATIONAL_SURFACES','plan_sha256':PLAN_SHA,'outcomes':outcomes},indent=2).encode())
 print(str(receipt))
if __name__=='__main__':main()
