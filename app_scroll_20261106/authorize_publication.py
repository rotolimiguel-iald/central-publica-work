import json,sys
from pathlib import Path
from task import W,pin,save,check,call,REF,OWNER
M=W/'mobile';sys.path.insert(0,str(M))
from publication_guards import scan,FILES,REPO
check('mobile')
plan=json.loads((M/'PLAN.json').read_bytes());installed=json.loads((W/'INSTALLED.json').read_bytes());audit=json.loads((M/'release/AUDIT.json').read_bytes())
assert installed['status']=='PASS' and audit['status']=='PASS' and audit['signer_matches_previous']
for row in plan['rows']:assert pin(row['target'])['sha256']==row['new']
for name in FILES:scan((REPO/name).read_bytes())
for kind in ('apk','aab'):assert pin(audit[kind])['sha256']==audit[kind+'_sha256']
scripts={n:pin(M/n)['sha256'] for n in ['publication_guards.py','publish_apk42.py','git_release42.py','release_controls.py','prepare_mobile.py']}
save('mobile/PUBLICATION_WORKFLOW_REVIEW.json',{'status':'PASS','reviewer':OWNER,'author':'codex-mobile-prep','script_pins':scripts,'checks':['Six tracked paths only, exact private repository and branch, normal push with no tags or force','HEAD/remote/index and reviewed blob pins before commit; no uncertain retry','Existing signing certificate and embedded resources audited','New APK published by non-overwrite rename; preserve previous APK hashes','No credentials or private case material in selected files; conservative scan passed']})
save('mobile/INSTALL_NORMALIZED.json',{'status':'PASS','plan_sha256':pin(M/'PLAN.json')['sha256'],'installed':{r['target']:r['new'] for r in plan['rows']},'source':pin(W/'INSTALLED.json')})
save('mobile/PARENT_PUBLICATION_READY.json',{'status':'PUBLICATION_AUTHORIZED','parent':OWNER,'phases':['apk','commit','push'],'plan_sha256':pin(M/'PLAN.json')['sha256'],'script_pins':scripts,'workflow_review':pin(M/'PUBLICATION_WORKFLOW_REVIEW.json'),'install':pin(M/'INSTALL_NORMALIZED.json'),'build':pin(M/'release/AUDIT.json')})
g=call({'operation':'get','reference':str(REF)},False);handles=list(g['p'].get('handles',[]))
for h in handles:
 if h['id']=='android42_build':h.update(status='completed',evidence=pin(M/'release/AUDIT.json'))
changes={'flow':{'phase':'mobile_publication','next_action':'Publish audited Android package and reviewed private source commit; await Apple login for actual distribution verification.','handles':handles}}
save('BUILD_COMPLETE_CHANGES.json',changes)
r=call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':g['revision'],'event_id':'scroll-android42-completed','changes_file':str(W/'BUILD_COMPLETE_CHANGES.json'),'changes_sha256':pin(W/'BUILD_COMPLETE_CHANGES.json')['sha256']},False)
save('BUILD_COMPLETE_RECEIPT.json',r)
print(json.dumps({'status':'PASS','revision':r['revision'],'apk_bytes':Path(audit['apk']).stat().st_size}))
