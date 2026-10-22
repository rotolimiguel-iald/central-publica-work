"""Custody and local registration of the authenticated follow-up."""
import datetime as dt
import json
import subprocess
import sys
import support_live as s

def run_once(label,args):
    if (s.ROOT/(label+'_INTENT.json')).exists():
        raise RuntimeError('Existing attempt: recover, do not repeat '+label)
    s.new(label+'_INTENT.json',{'command':args,'time_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf-8')
    out=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    assert cp.returncode==0,str(out)
    print(cp.stdout[:1800])
    return out

def main():
    s.check('L3_MEMORY_FOLLOWUP')
    evidence=[s.pin(s.ROOT/n) for n in ['APP_LIVE_RESULT_R1.json','IOS_DISTRIBUTION_RESULT_R1.json',
        'review/FINAL_REVIEW_R1.json','MEMORY_APPLIED_R1.json','review/MEMORY_PLAN_REVIEW_R1.json']]
    delivery=s.new('DELIVERY_LIVE_R1.json',{'status':'SUPPLEMENT_DELIVERED_WITH_LIMITS',
      'author':s.ACTOR['id'],'unit':'F9.MEMORIA_ORGANISMO_20261016','claim':940,'scope_event':941,
      'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reference':s.pin(s.REFERENCE),
      'evidence':evidence,'real_chat_messages':2,'memory_surfaces_appended':11,
      'availability':{'web':'authenticated synthetic test passed; reload continuity observed',
        'iOS_internal':'4.1(33) Em testes; operator is member',
        'iOS_external':'4.1(33) Em testes; Piloto6testers',
        'physical_installation':'not verified; Apple reports operator on32',
        'Android':'4.1(28) signed APK/AAB local; no new distribution',
        'Bancada':'prior unavailable18777 not retested or restarted',
        'native':'prior isolated validation; no live inference here'},
      'limitations':['No causal ACOM benchmark','Reviewer checked files, not independent browser access',
        'Pending app results remain unaccepted by the human','No scientific kernel/gate change']})
    entry=s.new('MAP_ENTRY_LIVE_R1.json',{'tipo':'RESULTADO','rota_id':'infra.memoria_organismo.atividade_20261016',
      'dominio':'INFRAESTRUTURA','titulo':'Teste autenticado e distribuição iOS33 da memória de atividade',
      'metodo':'Duas mensagens sintéticas via UI, recarga, inspeção de atividade e commit Apple; revisão documental independente.',
      'resultado':'MiMo recuperou referência e pendência; iOS4.1(33) Em testes em Equipe e Piloto; onze apêndices com backups de bytes.',
      'veredito':'VERIFIED_WITH_SCOPE','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,
      'defeito':'Instalação física33 não verificada; Android28 local; Bancada18777 e nativa mantêm limites anteriores. Teste não isola causalidade ACOM.',
      'nao_refazer':'Reutilizar dois jobs do teste e build33; não reenviar nem reconstruir versão.',
      'proximo_passo':'Gerência audita; operador atualiza aparelho quando conveniente. Melhorar legibilidade do painel em unidade própria.',
      'artefatos':[str(delivery),*[x['path'] for x in evidence]],'onde':str(s.ROOT)})
    map_result=run_once('MAP_REGISTER_LIVE_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    board_result=run_once('BOARD_REGISTER_LIVE_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F9.MEMORIA_ORGANISMO_20261016','--quem',s.ACTOR['id'],'--status','ENTREGUE','--evidencia',str(delivery),'--nota','Complemento: web autenticada e iOS33 em ambos os grupos; onze superfícies com backups. Limites remanescentes explícitos.'])
    registration=s.new('REGISTRATION_LIVE_R1.json',{'delivery':s.pin(delivery),'map':s.pin(map_result),'board':s.pin(board_result)})
    state,_=s.call('session_memory.py',{'operation':'get','reference':str(s.REFERENCE)},'GET_FINAL')
    sources=[{'kind':'artifact','ref':str(p),'sha256':s.pin(p)['sha256']} for p in [delivery,registration]]
    s.call('session_memory.py',{'operation':'transition','reference':str(s.REFERENCE),'actor':s.ACTOR,
      'expected_revision':state['revision'],'event_id':'organism-live-material-20261017',
      'changes':{'records':[{'id':'live-app-ios33-20261017','kind':'fact','statute':'REAL','sources':sources,
          'text':'Duas mensagens sintéticas no app/MiMo com continuidade pós recarga e pendência recuperada. iOS33 do commit483641a Em testes nos dois grupos; operador ainda32 segundo Apple. Onze apêndices e backups; nenhuma instalação física alegada. Bancada/nativa/Android mantêm limites anteriores.'}],
          'flow':{'phase':'live_followup_delivered','next_action':'Revisor confere memória e registro L3; gerência audita complemento. Não repetir jobs/builds. Física segue referência FECHO distinta.'}}},'TRANSITION_FINAL')
    p=s.project();t=next(t for t in p['projection']['active'] if t['id']=='L3_MEMORY_FOLLOWUP')
    r,out=s.action('submit','submit-live-memory-20261017',task_id=t['id'],lease_id=t['lease']['id'],
          evidence=[s.pin(delivery),s.pin(registration),s.pin(s.ROOT/'MEMORY_APPLIED_R1.json')])
    print(out)

if __name__=='__main__':
    main()
