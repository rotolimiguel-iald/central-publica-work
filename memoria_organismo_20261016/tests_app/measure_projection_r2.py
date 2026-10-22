import sys,json,time,uuid
from pathlib import Path
w=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(w/'staging/app'),str(w/'staging/core/lib')]
import iald_app_memory as m
folder=w/'tests_app/runs'/('growth_'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
m._SHARED_ROOT=Path('\\\\?\\'+str(folder/'store'))
results=[];start=time.monotonic()
for i in range(1,101):
 b=m.begin(folder,'growth-fixture','growth',[{'role':'user','content':'Continue a atividade '+str(i)}],'turn_'+str(i))
 m.finish_result(b,{'answer':'Resposta candidata '+str(i)})
 if i in (1,3,5,10,25,50,100):
  p=b.projection(); row={'turns':i,'required_chars':p['required_chars'],'actual_chars':p['actual_chars'],'revision':p['receipt']['revision'],'elapsed_seconds':round(time.monotonic()-start,3),'review_pending':len(p['activity']['active']),'escaped_memory_bytes_lower_bound':len(json.dumps({'common_memory':p['text']},ensure_ascii=False).encode('utf8'))};results.append(row);print(json.dumps(row),flush=True)
  target=w/'tests_app/MULTITURN_MEASUREMENT_R2.json';tmp=target.with_suffix('.tmp');tmp.write_text(json.dumps({'fixture':'scalar command + candidate answer, no tools, all pending review','rows':results,'complete':i==100,'provider_calls':0},indent=2),encoding='utf8');tmp.replace(target)
