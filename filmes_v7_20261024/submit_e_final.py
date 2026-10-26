"""Submit the immutable E candidate under its existing actor and lease."""
import hashlib, json, pathlib, runpy
W=pathlib.Path(__file__).resolve().parent
R=pathlib.Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
M=runpy.run_path(str(W/'mission.py'))
pr=M['project']()
task=next(t for t in pr['projection']['active'] if t['id']=='E')
assert task['status']=='working' and task['lease']['owner']=='codex-video-web'
identity={'actor':{'id':'codex-video-web','kind':'agent'},'expected_revision':pr['receipt']['revision'],
          'projection_sha256':pr['projection_sha256'],'task_id':'E','lease_id':task['lease']['id']}
assert M['call']({'operation':'check',**identity})['ready']
files=[R/'audit/DELIVERY_E.json',R/'PUBLIC_DELIVERY_V7.json',R.parent/'PUBLIC_DELIVERY_V7.json',
       R/'RENDER_MANIFEST.json',R/'render/MEDIA_VALIDATION.json',R/'audit/WEB_BUILD.json']
evidence=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
payload={'operation':'submit',**identity,'event_id':'ordem022-E-v399-final-media-web-submit-20261024',
         'evidence':evidence,'note':'132 public files checked; 16 media and 25 images PASS; current 43-pin jobs; final web and parent UI receipts. Independent review remains pending.'}
request=W/'SUBMIT_E_FINAL_REQUEST.json'
with request.open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,indent=2)
result=M['call'](payload)
out=W/'SUBMIT_E_FINAL_RESULT.json'
with out.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
after=M['project']()
current=next(t for t in after['projection']['active'] if t['id']=='E')
assert current['status']=='review_pending' and current['submitted_by']=='codex-video-web'
print(json.dumps({'status':current['status'],'submitted_by':current['submitted_by'],
                 'revision':after['receipt']['revision'],'result_file':str(out),
                 'result_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
