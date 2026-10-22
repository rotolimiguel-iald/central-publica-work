"""Resume after the map's lexical refusal; do not repeat memory appends."""
from setup import ROOT, UNIT, ACTOR,save,command,memory
from record_trajectory_r2 import pin,checkpins
import json,sys

if __name__=='__main__':
    failure=json.loads((ROOT/'MAP_REGISTER_R11.json').read_text(encoding='utf-8'))
    assert failure['exit_code']!=0 and json.loads(failure['stdout'])['ok'] is False
    for row in json.loads((ROOT/'MEMORY_APPLIED_R11.json').read_text(encoding='utf-8')):
        checkpins(row['backup']); checkpins(row['after'])
        assert row['backup']['sha256']==row['before']['sha256']
    ref=str(ROOT/'SESSION_REFERENCE.json')
    state=memory({'operation':'get','reference':ref},'GET_RECOVER_R11');assert state['revision']==12
    entry=json.loads((ROOT/'MAP_ENTRY_R11.json').read_text(encoding='utf-8'))
    entry['resultado']='Auditoria registra resultados condicionais e zero do ramo proporcional; previsao fisica completa/calibracao independente ainda incompletas.'
    save('MAP_ENTRY_R11_1.json',entry)
    command('MAP_REGISTER_R11_1',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R11_1.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R11',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R11.json'),'--nota','Impasse fisicoR11: meta5sigma incompleta;precisa relacao fisica/calibracao independente. Unidade naoFECHADA,sem dado observado.'])
    txt=(ROOT/'MEMORY_APPEND_R11.txt').read_text(encoding='utf-8')
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':12,'event_id':'lensing-goal-audit-r11',
      'changes':{'records':[{'id':'lensing-goal-audit-r11','kind':'fact','statute':'OPEN','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R11.json'),'sha256':pin(ROOT/'DELIVERY_R11.json')['sha256']}],'text':txt}],
       'flow':{'phase':'physical_input_impasse_audited_r11',
        'next_action':'Resume with concrete full-action source/physical relation determining non-proportional lens response, or documented independent mass calibration. Existing branches reviewed; fullgoal notcomplete; sameblockerR9-R11. No arbitrary parameter choices or repeated forecasts.',
        'handles':state['p']['handles']}}},'TRANSITION_R11')
    save('REGISTRATION_R11.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R11.json'),'acom':out,
      'memory':pin(ROOT/'MEMORY_APPLIED_R11.json'),'map':pin(ROOT/'MAP_REGISTER_R11_1.json'),'board':pin(ROOT/'BOARD_UPDATE_R11.json'),
      'lexical_refusal':pin(ROOT/'MAP_REGISTER_R11.json'),'corrected_map_entry':pin(ROOT/'MAP_ENTRY_R11_1.json'),
      'recovery_script':pin(__file__),'memory_appends_repeated':False})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
