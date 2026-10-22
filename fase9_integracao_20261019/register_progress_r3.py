"""Register reviewed partial progress additively, with byte backups and CAS."""
from setup_mission import ROOT,UNIT,ACTOR,REF,pin,save,shell,call
from pathlib import Path
import json,sys,datetime,os
def main():
    for name in ['REGISTRATION_R3.json','MEMORY_APPLIED_R3.json','MAP_ENTRY_R3.json']:
        if (ROOT/name).exists():raise FileExistsError(name)
    progress=json.loads((ROOT/'PROGRESS_R3.json').read_text(encoding='utf-8'))
    for row in progress['evidence']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('EVIDENCE_CHANGED: '+row['path'])
    board=shell('BOARD_PREFLIGHT_REGISTER_R3.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT])
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id'] and datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    current=call('PROJECT_REGISTER_R3.json',{'operation':'project','reference':REF,'max_chars':60000})
    task=next(t for t in current['projection']['active'] if t['id']=='R1')
    call('CHECK_REGISTER_R3.json',{'operation':'check','reference':REF,'actor':ACTOR,
       'expected_revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],
       'task_id':'R1','lease_id':task['lease']['id']})
    state=call('GET_REGISTER_R3.json',{'operation':'get','reference':REF},False)
    assert next(h for h in state['p']['handles'] if h['id']=='f9-full-prior-refinement-r3')['status']=='completed'
    note=(ROOT/'MEMORY_APPEND_R3.txt').read_text(encoding='utf-8');extra=note.encode('utf-8')
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        target=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=target.read_bytes();before=pin(target)
        assert b'IALD_FASE9_INTEGRACAO_20261019_R3' not in raw
        backup=target.with_name(target.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        temp=target.with_name(target.name+'.tmp_f9integration_r3_'+stamp)
        with temp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and target.read_bytes()==raw
        os.replace(temp,target);assert target.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(backup),'after':pin(target),'pure_append':True})
    save('MEMORY_APPLIED_R3.json',rows)
    entry={'tipo':'RESULTADO','rota_id':'d1.fase9.integracao_20261019','dominio':'D1_FUNDO_COSMOLOGICO',
       'titulo':'Fase9 R3: mapas, viés e refinamento físico sintético',
       'pergunta':'O que falta para discriminação5sigma sem ajuste aos dados?',
       'dados':['Fontes existentes e cenário sintético; nenhum composto observadoV2'],
       'metodo':'Derivação de mapas por leitura; envelopePSDe viés; refinamento pré-pinando e reutilizando cache físico',
       'resultado':progress['summary'],'veredito':'PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA',
       'estatuto':'DERIVED','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
       'defeito':'Convergência global .01 não atingida; mapas instrumentais/erros/caudas e atos permanecem abertos.',
       'nao_refazer':'Reutilizar729pontos físicos e revisões; não repetirsolver.',
       'proximo_passo':progress['next_action'],'onde':str(ROOT/'RELATORIO_PROGRESSO_R3.txt'),
       'artefatos':[str(ROOT/'PROGRESS_R3.json'),str(ROOT/'RELATORIO_PROGRESSO_R3.txt')],
       'refs':['d1.fase9.auditoria_suficiencia_20261019'],
       'nota':'Revisão de componentes; não aceitec1 integral, não observado/congelamento/gate.'}
    save('MAP_ENTRY_R3.json',entry)
    mapped=shell('MAP_REGISTER_R3.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R3.json'),'--quem',ACTOR['id']])
    boarded=shell('BOARD_PROGRESS_R3.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'PROGRESS_R3.json'),'--nota',progress['summary']])
    trans=call('TRANSITION_R3.json',{'operation':'transition','reference':REF,'actor':ACTOR,
       'expected_revision':state['revision'],'event_id':'fase9-integration-components-r3',
       'changes':{'records':[{'id':'fase9-components-r3','kind':'fact','statute':'REAL','text':note,
          'sources':[{'kind':'artifact','ref':str(ROOT/'PROGRESS_R3.json'),'sha256':pin(ROOT/'PROGRESS_R3.json')['sha256']}]}],
          'flow':{'phase':'components_r3_scientific_inference_open','next_action':progress['next_action'],'handles':state['p']['handles']}}},False)
    after=call('PROJECT_AFTER_REGISTER_R3.json',{'operation':'project','reference':REF,'max_chars':60000})
    task=next(t for t in after['projection']['active'] if t['id']=='R1')
    call('HANDOFF_VALID_R3.json',{'operation':'handoff','reference':REF,'actor':ACTOR,
       'expected_revision':after['receipt']['revision'],'projection_sha256':after['projection_sha256'],
       'task_id':'R1','lease_id':task['lease']['id'],'max_chars':60000})
    save('REGISTRATION_R3.json',{'status':'PARTIAL_PROGRESS_REGISTERED','unit':UNIT,
       'progress':pin(ROOT/'PROGRESS_R3.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R3.json'),
       'map':pin(ROOT/'MAP_REGISTER_R3.json'),'board':pin(ROOT/'BOARD_PROGRESS_R3.json'),
       'acom':trans,'handoff':pin(ROOT/'HANDOFF_VALID_R3.json'),'script':pin(Path(__file__))})
    print(json.dumps({'status':'REGISTERED','map':mapped,'board':boarded,'revision':trans['revision']},ensure_ascii=False))
if __name__=='__main__':main()
