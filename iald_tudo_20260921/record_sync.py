"""Record sanitized synchronization evidence and append its lineage with byte backups."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def main():
    observed=json.loads((WORK/'sync_observation.json').read_bytes())
    assert observed['elapsed_since_child_start_s']>=120
    assert observed['sync_started'] and observed['sync_other_lines']==0
    assert observed['stderr_bytes']==0 and observed['unsigned_json_post']==401
    assert observed['local_health']==observed['public_health']==200
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    receipt={**observed,'status':'TECHNICALLY_ACTIVE_OPERATOR_UI_PENDING',
        'before_unsigned_post':503,'render_deploy':'dep-daos37p42hec73fvcs6g',
        'render_status_observed':'Deploy succeeded | Live',
        'remote_sync_http_200_seen':True,'exact_cycle_count':None,
        'runtime_admin_status_available':False,'old_web_pid':66068,'new_web_pid':57020,
        'supervisor_pid':41020,'personal_central_key_accessed':False,
        'clipboard_cleared_by_helper':True,'clipboard_history_cleared':'user_reported',
        'secret_value_in_receipt':False,'operator_ui_confirmation':'pending'}
    helper.create(WORK/'sync_central.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    note='''[INPUT] O operador autorizou expressamente a sincronização com segredo separado após esclarecer que sua chave pessoal da Central não seria utilizada: “sendo assim, se não expõe a minha central não vejo problema, pode fazer”. Depois confirmou a colagem no Render.

[REAL] Segredo exclusivo gerado pelo helper fornecido, salvo no .env local e cadastrado como CENTRAL_IALD_SYNC_SEGREDO no serviço central-de-patentes. Nenhum valor de segredo registrado. Chave pessoal da Central não acessada. A primeira execução recusou antes de alterar .env porque PowerShell 5 herdou PSModulePath incompatível do PowerShell 7; a segunda removeu essa variável apenas no ambiente do processo do helper, sem mudar código nem configuração global. Backup íntegro .env.bak_20260921_204217 preservado; backup vazio da tentativa recusada também preservado. Helper confirmou limpeza do clipboard; limpeza do histórico foi solicitada e reportada pelo operador.

[REAL] Render: implantação dep-daos37p42hec73fvcs6g “Deploy succeeded | Live”. Requisição JSON não assinada passou de indisponível (503 inicial) a 401. Uma verificação sem Content-Type recebeu 415 após ativação: não era teste válido de assinatura; refeita com JSON vazio, 401. Após ausência de reservas de geração ativas e marcadores de conversa em curso, somente filho web 66068 encerrado; supervisor 41020 criou filho 57020 às 20:51:42. Log r5 confirmou sincronização LIGADA, sem outros marcadores de sincronização nem stderr durante pelo menos 120 s; saúde local e pública 200. UI de logs do Render mostrou POST /api/iald-sync/puxar com 200. Nenhuma sessão admin local utilizada, portanto não há contagem exata de ciclos nem ultima_sincronizacao do endpoint admin neste recibo.

[OPEN] Operador confere pessoalmente patente IALD → Usuários do app → sincronização recente; agente não entra na Central. T2 depende de login pessoal no roteador e eventual exceção mínima para files.pythonhosted.org; T3 chave/crédito Anthropic; T4 contagem/cache; T5 builds18/17 e testes físicos. Não declarar Claude ativo nem builds novas distribuídas. Recibo: work/iald_tudo_20260921/sync_central.json. Meta integral continua ativa.
'''
    rows=[]
    marker='IALD_CENTRAL_SYNC_ACTIVATED_20260921'
    for path in helper.TARGETS:
        before=path.read_bytes();assert marker.encode() not in before
        backup=path.with_name(path.name+'.bak_'+stamp);helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n## '+now.strftime('%d/%m/%Y %H:%M')+' — Codex: sincronização Central/IALD ativada\n\n<!-- '+marker+' -->\n\n'+note
        after=before+addition.replace('\n',newline).encode()
        tmp=path.with_name(path.name+'.tmp_'+stamp);helper.create(tmp,after)
        assert path.read_bytes()==before
        tmp.replace(path);assert path.read_bytes()==after and len(after)>len(before)
        rows.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    helper.create(WORK/'sync_memory_record.json',json.dumps({'at':now.isoformat(),'memories':rows,'goal_complete':False},ensure_ascii=False,indent=2).encode())
    print(json.dumps({'sync_receipt_recorded':True,'memories_updated':len(rows),'goal_complete':False}))

if __name__=='__main__':main()
