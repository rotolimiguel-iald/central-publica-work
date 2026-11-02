"""Immutable browser supplement: retain prior evidence and submit without acceptance."""
import json,datetime
from pathlib import Path
import context as c
A={'id':'codex-video-v404-data','kind':'agent'}
def main():
 preflight=c.check('V404_DATA_BROWSER',A);c.stable_seal()
 original=c.read(c.H/'DATA_DELIVERY.json');comparison=c.read(c.H/'NUMERIC_COMPARISON.json')
 assert comparison['status']=='PASS_NUMERIC_PENDING_DISTINCT_REVIEW'
 # Existing submission remains byte-identical, including all effective data files.
 previous=c.read(c.H/'DATA_SUBMIT_VERIFIED.json')['task']['evidence']
 for e in previous:assert c.sha(Path(e['path']))==e['sha256']
 for e in original['files']:assert c.pin(Path(e['path']))==e
 r=c.read(c.S/'replay/TEST_BROWSER_V404.json');m=c.read(c.S/'replay/replay-manifest.json')
 assert r['status']=='PASS' and r['source']==m['source']['version']=='v404'
 assert r['source_sha256']==m['source']['sha256']==c.sha(c.S/'source/um.py')
 assert r['manifest_sha256']==r['manifest_before_sha256']==c.sha(c.S/'replay/replay-manifest.json')
 assert not r['external_requests'] and all(x['ok'] for x in r['checks'])
 assert len(r['result']['rows'])==61 and all(x['ok'] for x in r['result']['rows'])
 trust_text=(c.S/'web/replay-trust.mjs').read_text(encoding='utf-8')
 trust=json.loads(trust_text.removeprefix('export const replayTrust = ').strip().removesuffix(';'))
 assert trust=={'manifestURL':'../replay/replay-manifest.json','sha256':r['manifest_sha256']}
 assert r['trust_sha256']==c.sha(c.S/'web/replay-trust.mjs')
 served=[]
 for url,relative in [('/replay/replay-manifest.json','replay/replay-manifest.json'),('/data/hud.json','data/hud.json'),('/web/replay-trust.mjs','web/replay-trust.mjs')]:
  rows=[x for x in r['served'] if x['url']==url];assert rows
  assert all(Path(x['path'])==c.S/relative and x['sha256']==c.sha(c.S/relative) for x in rows)
  served.append({'url':url,'candidate':c.pin(c.S/relative),'requests':len(rows)})
 for e in r['read_only_runtime']:assert c.sha(Path(e['path']))==e['sha256']
 assert next(x for x in r['read_only_runtime'] if x['url']=='/web/replay-worker.js')['sha256']==m['worker_sha256']
 effective=[c.S/'web/replay-trust.mjs',c.S/'replay/test_browser_v404.cjs',c.S/'replay/TEST_BROWSER_V404.json',c.S/'replay/BROWSER_V404_OK.png',c.S/'replay/BROWSER_V404_TAMPER.png']
 out={'status':'PASS_BROWSER_CANDIDATE_PENDING_DISTINCT_REVIEW','reference':str(c.REF),'task_id':'V404_DATA_BROWSER','original_delivery':c.pin(c.H/'DATA_DELIVERY.json'),'numeric_comparison':c.pin(c.H/'NUMERIC_COMPARISON.json'),'original_status_preserved':comparison['status'],'original_effective_files_still_pinned':True,'files':[c.pin(x) for x in effective],'source':m['source'],'manifest':c.pin(c.S/'replay/replay-manifest.json'),'request_source_binding':served,'browser_numeric_checks':len(r['result']['rows']),'browser_control_groups':len(r['checks']),'external_requests':r['external_requests'],'borrowed_read_only_runtime':r['read_only_runtime'],'failures_preserved':[c.pin(c.H/n) for n in ['DATA_BROWSER_LAUNCH_FAILURE_R1.json','DATA_BROWSER_LOOPBACK_FAILURE_R2.json']],'preflight':preflight,'render_released':False,'semantic_acceptance':False,'limits':['Local browser replay only; loopback HTTP allowed and external replay requests blocked.','Production web panel/worker/comparator read only, pinned; parent must integrate and independently verify the candidate.','No TTS/render, production change, Lean execution or nature confirmation.','Original DATA_DELIVERY and NUMERIC_COMPARISON remain immutable; this supplement updates browser availability only.','Producer readiness PASS must come from distinct verification, not this candidate status.'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 target=c.H/'DATA_DELIVERY_BROWSER_R2.json';assert not target.exists();c.save(target,out)
 p=c.project();t=next(x for x in p['projection']['active'] if x['id']=='V404_DATA_BROWSER')
 result=c.mission.call({'operation':'submit','actor':A,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':t['id'],'lease_id':t['lease']['id'],'event_id':'v404-data-browser-submit','evidence':[{'path':str(x),'sha256':c.sha(x)} for x in [target,c.H/'DATA_DELIVERY.json',c.H/'NUMERIC_COMPARISON.json']],'note':'Complemento browser 61/61 e controles negativos PASS; originais imutáveis; sem aceite próprio ou liberação de render.'})
 c.save(c.H/'DATA_BROWSER_SUBMIT.json',result)
 p=c.project();t=next(x for x in p['projection']['active'] if x['id']=='V404_DATA_BROWSER')
 c.save(c.H/'DATA_BROWSER_SUBMIT_VERIFIED.json',{'receipt':p['receipt'],'task':t})
 print(json.dumps({'status':out['status'],'mission_status':t['status'],'rows':out['browser_numeric_checks'],'checks':out['browser_control_groups'],'delivery':str(target),'original_unchanged':True}))
if __name__=='__main__':main()
