from pathlib import Path
import hashlib,json
from bootstrap import cli,save,REF,ACTOR
W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
review=V/'replay/REVIEW_FROZEN_PREVIEW_CAPTIONS.json'
evidence={'status':'CORRECTED_REVIEWED_RECAPTURING','patch':json.loads((W/'CLOSING_FINITE_PATCH.json').read_bytes()),'capture_yield':json.loads((W/'CAPTURE_YIELD_PATCH.json').read_bytes()),'review':{'file':str(review),'sha256':hashlib.sha256(review.read_bytes()).hexdigest()},'coverage_preview':{'film1_samples':224,'film2_samples':360,'minimum_width_fraction':0.8291666666666667,'failures':0,'method':'UI audit; opaque object mask, one sample per second. Final jobs pending.'},'prior_limit':'Previous return occupied56s and incorrectly excluded it from minimum-width check; old renders retained as intermediate.'}
save('CLOSING_PROGRESS.json',evidence)
state=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'get','reference':str(REF)})['result']
handles=state['p']['handles']
for h in handles:
 if h['id'] in ['21be2e3bef15424aa5ab7c5aaf8a2a4d','1d02d0cad4294527843ce6aa3660991c']:
  h['status']='completed';h['scope']='Intermediate prior framing; retained but superseded for final delivery'
for identity in ['c44cc1f04e6b458f81cfe20ee06d0bf0','88907500dba54d2fbf6246ebafd67325']:
 if not any(h['id']==identity for h in handles):handles.append({'id':identity,'kind':'local_render','status':'completed','task_id':'B','scope':'Intermediate or preview; retained'})
handles.append({'id':'5a6d79d3bbde4d7e9452aca8dcee16c9','kind':'local_render','status':'running','task_id':'B','version':'v399','scope':'Corrected closing; final recapture'})
p=W/'CLOSING_PROGRESS.json'
result=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':'v7-closing-corrected-recapture','changes':{'records':[{'id':'v7_closing_corrected','kind':'fact','statute':'REAL','text':'Revisão encontrou fechamento pequeno por56s indevidamente excluído como transição. Corrigido: geometria ampla até últimos3s. Auditoria UI1fps224+360amostras, mínimo82,9167% fora transições. Revisão focada PASS; nova captura em andamento, anteriores preservadas. Make recusa LUFS NaN/infinito.','sources':[{'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}],'flow':{'phase':'v399_corrected_final_capture','next_action':'Concluir captura, codificações, validação e entrega para revisão da gerência; reutilizar áudio completo.','handles':handles}}})
save('TRANSITION_CLOSING_PROGRESS.json',result)
print(json.dumps(result,ensure_ascii=False))
