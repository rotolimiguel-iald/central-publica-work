import json,sys
from task import W,REF,OWNER,pin,save,call
g=call({'operation':'get','reference':str(REF)},False)
handles=list(g['p'].get('handles',[]))
source=W/'INSTALLED.json'
changes={'records':[{'id':'scroll_static_installed','kind':'fact','statute':'REAL','text':'Shared client scroll repair installed in ten reviewed targets without restart; 1797 scientific/runtime pins preserved. Browser synthetic public/private regressions passed. Native distribution pending.','sources':[{'kind':'artifact','ref':str(source),'sha256':pin(source)['sha256']}]}], 'flow':{'phase':'mobile_build','next_action':'Verify Android build, publish approved artifacts, inspect same iOS Cloud run and both groups after Apple login.','handles':handles+[{'id':'android42_build','status':'running','source':str(W/'mobile/release/build42/gradle.started.json'),'session_id':'11659'}]}}
save('STATIC_PROGRESS_CHANGES.json',changes)
r=call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':g['revision'],'event_id':'scroll-static-progress','changes_file':str(W/'STATIC_PROGRESS_CHANGES.json'),'changes_sha256':pin(W/'STATIC_PROGRESS_CHANGES.json')['sha256']},False)
save('STATIC_PROGRESS_RECEIPT.json',r)
print(r['receipt']['revision'])
