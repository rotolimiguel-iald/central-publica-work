"""Register a new partial layer, with byte backups and current CAS/lease.

Does not accept scientific requirements or manufacture operator acts. All
outputs are exclusive. If a stage fails, recover only the unfinished stage.
"""
from setup_mission import ROOT,UNIT,ACTOR,REF,pin,save,shell,call
from pathlib import Path
import json,sys,datetime,os

def main():
    for name in ['REGISTRATION_R2.json','MEMORY_APPLIED_R2.json','MAP_ENTRY_R2.json']:
        if (ROOT/name).exists():raise FileExistsError(name)
    progress=json.loads((ROOT/'PROGRESS_R2.json').read_text(encoding='utf-8'))
    for row in progress['evidence']:
        if pin(row['path'])['sha256']!=row['sha256']:raise ValueError('EVIDENCE_CHANGED: '+row['path'])
    board=shell('BOARD_PREFLIGHT_REGISTER_R2.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT])
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    current=call('PROJECT_REGISTER_R2.json',{'operation':'project','reference':REF,'max_chars':50000})
    task=next(t for t in current['projection']['active'] if t['id']=='R1')
    call('CHECK_REGISTER_R2.json',{'operation':'check','reference':REF,'actor':ACTOR,
        'expected_revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],
        'task_id':'R1','lease_id':task['lease']['id']})
    state=call('GET_REGISTER_R2.json',{'operation':'get','reference':REF},False)
    note=(ROOT/'MEMORY_APPEND_R2.txt').read_text(encoding='utf-8')
    extra=note.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        target=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=target.read_bytes();before=pin(target)
        assert b'IALD_FASE9_INTEGRACAO_20261019_R2' not in raw
        backup=target.with_name(target.name+'.bak_'+stamp)
        with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        temp=target.with_name(target.name+'.tmp_f9integration_r2_'+stamp)
        with temp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and target.read_bytes()==raw
        os.replace(temp,target);assert target.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(backup),'after':pin(target),'pure_append':True})
    save('MEMORY_APPLIED_R2.json',rows)
    entry={'tipo':'ROTA','rota_id':'d1.fase9.integracao_20261019','dominio':'D1_FUNDO_COSMOLOGICO',
        'titulo':'Fase9: envelope completo, pivô e execução física sintética',
        'pergunta':'O que falta para uma discriminação5sigma sem ajustar parâmetros?',
        'dados':['Fontes documentais L1b/L6 e cenários sintéticos; nenhum composto observadoV2'],
        'metodo':'Reuso de contratos; envelope PSD analítico; pivô Gaussiano; integração física em cópia com recibos e recusa numérica',
        'resultado':progress['summary'],
        'veredito':'PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA','estatuto':'DERIVED',
        'status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
        'defeito':'Mapas físicos/erros totais/calibração real e atos ainda abertos; resultado sintético não é observação.',
        'nao_refazer':'Reutilizar os pontos CAMB custodiados e os controles já qualificados; não repetir chamadas/IDs encerrados.',
        'proximo_passo':progress['next_action'],
        'onde':str(ROOT/'RELATORIO_PROGRESSO_R2.txt'),
        'artefatos':[str(ROOT/'PROGRESS_R2.json'),str(ROOT/'RELATORIO_PROGRESSO_R2.txt')],
        'refs':['d1.fase9.auditoria_suficiencia_20261019'],
        'nota':'Documentos públicos foram lidos; nenhum centro local composto. Sem produção, congelamento, abertura ou gate.'}
    save('MAP_ENTRY_R2.json',entry)
    mapped=shell('MAP_REGISTER_R2.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R2.json'),'--quem',ACTOR['id']])
    boarded=shell('BOARD_PROGRESS_R2.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'PROGRESS_R2.json'),'--nota',progress['summary']])
    # E3: mechanical terminal states belong in p.handles, not separate q facts.
    handles=list(state['p']['handles'])
    for hid,rel,status in [('f9-full-prior-r1','r2_full_integration/COMMAND_RESULT_R1.json','failed'),
                           ('f9-full-prior-recovery-r2','r2_full_integration/recovery_r2/COMMAND_RESULT_R2.json','completed')]:
        assert all(h['id']!=hid for h in handles)
        terminal=json.loads((ROOT/rel).read_text(encoding='utf-8'))
        assert (terminal['exit_code']==0)==(status=='completed')
        handles.append({'id':hid,'kind':'synthetic_physical_integration','task_id':'R2',
            'status':status,'no_repeat':True,'receipt':pin(ROOT/rel),
            'interpretation':'Execution status only; numerical/scientific qualification in PROGRESS_R2'})
    trans=call('TRANSITION_R2.json',{'operation':'transition','reference':REF,'actor':ACTOR,
        'expected_revision':state['revision'],'event_id':'fase9-integration-components-r2',
        'changes':{'records':[{'id':'fase9-components-r2','kind':'fact','statute':'REAL','text':note,
          'sources':[{'kind':'artifact','ref':str(ROOT/'PROGRESS_R2.json'),'sha256':pin(ROOT/'PROGRESS_R2.json')['sha256']}]}],
        'flow':{'phase':'components_r2_scientific_inference_open','next_action':progress['next_action'],'handles':handles}}},False)
    after=call('PROJECT_AFTER_REGISTER_R2.json',{'operation':'project','reference':REF,'max_chars':50000})
    task=next(t for t in after['projection']['active'] if t['id']=='R1')
    call('HANDOFF_VALID_R2.json',{'operation':'handoff','reference':REF,'actor':ACTOR,
        'expected_revision':after['receipt']['revision'],'projection_sha256':after['projection_sha256'],
        'task_id':'R1','lease_id':task['lease']['id'],'max_chars':50000})
    save('REGISTRATION_R2.json',{'status':'PARTIAL_PROGRESS_REGISTERED','unit':UNIT,
        'progress':pin(ROOT/'PROGRESS_R2.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R2.json'),
        'map':pin(ROOT/'MAP_REGISTER_R2.json'),'board':pin(ROOT/'BOARD_PROGRESS_R2.json'),
        'acom':trans,'handoff':pin(ROOT/'HANDOFF_VALID_R2.json'),'script':pin(Path(__file__))})
    print(json.dumps({'status':'REGISTERED','map':mapped,'board':boarded,'revision':trans['revision']},ensure_ascii=False))
if __name__=='__main__':main()
