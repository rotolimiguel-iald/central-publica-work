import importlib.util,json,tempfile,time,uuid,sys
from pathlib import Path
W=Path(__file__).resolve().parent
sys.path.insert(0,r'C:\IALD\projetos_pyhton\IALD')
spec=importlib.util.spec_from_file_location('stage_jobs',W/'stage_main/iald_chat_jobs.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Cipher:
 def seal(self,b):return b
 def open(self,b):return b
results=[]
for name,frames,expected in [
 ('complete',['{"choices":[{"delta":{"content":"ok"}}]}','[DONE]'],'completed'),
 ('warning_after_answer',['{"choices":[{"delta":{"content":"partial"}}]}','{"iald_aviso":{"tipo":"falha_motor"}}','[DONE]'],'failed'),
 ('error',['{"error":"failure"}','[DONE]'],'failed'),
 ('missing_terminal',['{"choices":[{"delta":{"content":"partial"}}]}'],'failed')]:
 with tempfile.TemporaryDirectory(dir=W) as tmp:
  j=m.ChatJobs(tmp,cipher=Cipher());payload={'request_id':str(uuid.uuid4()),'iald_conv':'isolated','stream':True,'messages':[{'role':'user','content':'synthetic'}]};calls=[]
  def produce(body,stop):
   calls.append(1)
   for f in frames:yield 'data: '+f+'\n\n'
  out=j.submit('synthetic',payload,produce)
  for _ in range(100):
   out=j.get('synthetic',payload['request_id'])
   if out['status'] in m.TERMINAL:break
   time.sleep(.01)
  assert out['status']==expected,(name,out)
  j.submit('synthetic',payload,produce)
  assert len(calls)==1
  results.append({'test':name,'status':out['status'],'dispatches':len(calls)})
(W/'jobs_tests.json').write_text(json.dumps({'passed':True,'tests':results,'provider_calls':0},indent=2),encoding='utf-8')
print(json.dumps(results))
