"""Link the explicit successor and submit the installed infrastructure for review."""
import json
from activate import ROOT, CORE, REF, OLD, ACTOR, call, pin, source, save

def main():
    old=json.loads((ROOT/'LEGACY_CHECKPOINT.json').read_bytes())
    link={'id':'mission-controller-successor-20261016','kind':'fact','statute':'REAL',
        'text':'A missão de conclusão foi reconciliada no mesmo ACOM. Continuar pelo caminho EXATO '+str(REF)+
        '. Os dez critérios originais e oito decisões INPUT foram transportados; este contexto preserva toda a linhagem anterior. Prioridade atual é memória, antes da construção científica. A referência nova não é uma missão de outra sessão.',
        'sources':[source(REF),source(ROOT/'CURRENT_REQUIREMENTS_INVENTORY.json'),source(ROOT/'INSTALLED_MCP_VERIFICATION.json')]}
    call('session_memory.py',{'operation':'transition','reference':str(OLD),'expected_revision':old['revision'],
        'event_id':'mission-controller-successor-20261016','actor':ACTOR,'changes':{'records':[link],
        'flow':{'phase':'mission_migrated_memory_priority','next_action':'Use mission_cli.py project com '+str(REF)+
        '; concluir memória M0 antes de retomar ciência. Não repetir jobs ou builds incertos.'}}},'LEGACY_CONTINUITY')
    own={'id':'installed-mission-controller-20261016','kind':'fact','statute':'REAL',
        'text':'Controlador/CLI/MCP e instruções instalados em oito destinos, backups preservados. Testes locais e revisão independente registrados. MCP real em processo novo recuperou a missão de 11 requisitos; dez científicos originais e M0 memória. Aceite técnico e registros finais em andamento; nenhuma conclusão científica promovida.',
        'sources':[source(ROOT/f) for f in ['DEPLOYMENT.json','VALIDATION_FINAL.json','SUPPLEMENT_FINAL_PIN.json','INSTALLED_MCP_VERIFICATION.json',
                   'FECHO_MISSION_REFERENCE.json','CURRENT_REQUIREMENTS_INVENTORY.json']]}
    call('session_memory.py',{'operation':'transition','reference':str(ROOT/'ACOM_REFERENCE.json'),
        'expected_revision':0,'event_id':'installed-mission-controller-20261016','actor':ACTOR,
        'changes':{'records':[own],'flow':{'phase':'installed_review_and_registration','next_action':'Revisão do M0 real; depois registrar entrega/memórias e concluir correção operacional.'}}},'OWN_INSTALLED')
    project=call('mission_cli.py',{'operation':'project','reference':str(REF)},'M0_BEFORE_CLAIM')
    claim=call('mission_cli.py',{'operation':'claim','reference':str(REF),'task_id':'M0_MEMORIA',
        'expected_revision':project['receipt']['revision'],'projection_sha256':project['projection_sha256'],
        'event_id':'memory-infrastructure-claim-v1','actor':ACTOR,'lease_seconds':7200},'M0_CLAIM')
    project=call('mission_cli.py',{'operation':'project','reference':str(REF)},'M0_CURRENT')
    call('mission_cli.py',{'operation':'check','reference':str(REF),'task_id':'M0_MEMORIA','actor':ACTOR,
        'lease_id':claim['task']['lease']['id'],'expected_revision':project['receipt']['revision'],
        'projection_sha256':project['projection_sha256']},'M0_PREFLIGHT')
    files=['DEPLOYMENT.json','VALIDATION_FINAL.json','REVIEW_CORE_R2.json','SUPPLEMENT_FINAL_PIN.json',
      'INSTALLED_MCP_VERIFICATION.json','MISSION_REQUIREMENTS.json','CURRENT_REQUIREMENTS_INVENTORY.json',
      'FECHO_MIGRATE_RECEIPT.json','LEGACY_CONTINUITY_RECEIPT.json','activate.py','checkpoint.py']
    submit=call('mission_cli.py',{'operation':'submit','reference':str(REF),'task_id':'M0_MEMORIA',
        'actor':ACTOR,'event_id':'memory-infrastructure-submit-v1','lease_id':claim['task']['lease']['id'],
        'expected_revision':project['receipt']['revision'],'projection_sha256':project['projection_sha256'],
        'evidence':[pin(ROOT/f) for f in files],
        'note':'Aceite técnico pela revisão independente; gerência conserva ratificação do quadro. Projeção e migração não recompilam nem aceitam ciência.'},'M0_SUBMIT')
    print(json.dumps({'status':submit['task']['status'],'reference':str(REF),'revision':submit['receipt']['revision']}))

if __name__=='__main__':main()
