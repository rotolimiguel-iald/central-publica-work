"""Resume only missing registration after the map requested a ROTA entry."""
from setup import ROOT,ACTOR,UNIT,save,command,memory
from pathlib import Path
import json,hashlib,sys
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
extra=(ROOT/'MEMORY_APPEND_R1.txt').read_bytes()
rows=json.loads((ROOT/'MEMORY_APPLIED_R1.json').read_text(encoding='utf-8'))
for row in rows:
    assert pin(row['after']['path'])==row['after']
    assert pin(row['backup']['path'])==row['backup']
    assert Path(row['after']['path']).read_bytes()==Path(row['backup']['path']).read_bytes()+extra
entry=json.loads((ROOT/'MAP_ENTRY_R1.json').read_text(encoding='utf-8'));entry['tipo']='ROTA'
save('MAP_ENTRY_R1_ROTA.json',entry)
command('MAP_REGISTER_R1_RECOVERED',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R1_ROTA.json'),'--quem',ACTOR['id']])
command('BOARD_UPDATE_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R1.json'),'--nota','Levantamento revisado entregue; mapa fisico por trajetoria e poder apos nuisance pendentes. Sem veredito observado.'])
ref=str(ROOT/'SESSION_REFERENCE.json');state=memory({'operation':'get','reference':ref},'GET_FINAL_R1')
out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':state['revision'],'event_id':'lensing-survey-r1-delivered','changes':{'records':[{'id':'lensing-survey-r1','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R1.json'),'sha256':pin(ROOT/'DELIVERY_R1.json')['sha256']}],'text':extra.decode('utf-8')}],'flow':{'phase':'lensing_survey_and_conditional_precision','next_action':'Recover/derive the physical lens trajectory response; test identifiability against mass/distance nuisance before observed verdict. Reuse R-G, keep formal H3 mission separate.','handles':[]}}},'TRANSITION_R1')
for e in json.loads((ROOT/'DELIVERY_R1.json').read_text(encoding='utf-8'))['evidence']:assert pin(e['path'])==e
save('VERIFIED_DELIVERY_R1.json',{'status':'PASS','memory_surfaces':3,'pure_appends':True,'scientific_reruns':0,'registration_recovery':'First map call refused nonexistent route; new ROTA registration only. No memory append repeated.','delivery':pin(ROOT/'DELIVERY_R1.json'),'map':pin(ROOT/'MAP_REGISTER_R1_RECOVERED.json'),'board':pin(ROOT/'BOARD_UPDATE_R1.json'),'acom':out})
print(json.dumps({'status':'PASS','acom':out,'delivery':pin(ROOT/'DELIVERY_R1.json')},ensure_ascii=False))
