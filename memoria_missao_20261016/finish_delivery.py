"""Publish a new additive delivery and append the authorized memory surfaces."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os, subprocess, sys, uuid
from activate import ROOT, CORE, CENTRAL, OUT, REF, ACTOR, call, pin, source, save, new_bytes

UNIT='F9.MEMORIA_MISSAO_20261016'
TUNNEL=CENTRAL/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT

def current():
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(CORE/'mission_cli.py')],
        input=json.dumps({'operation':'project','reference':str(REF),'max_chars':48000}),
        capture_output=True,text=True,encoding='utf-8')
    v=json.loads(r.stdout)
    if r.returncode or not v.get('ok'):raise RuntimeError(v)
    return v['result']

def restore_deliveries():
    project=current()
    assert any(t['id']=='M0_MEMORIA' and t['status']=='satisfied' for t in project['projection']['settled'])
    inventory=json.loads((ROOT/'CURRENT_REQUIREMENTS_INVENTORY.json').read_bytes())
    for task in ['R1','R2','R9']:
        p=current();t=next(x for x in p['projection']['active'] if x['id']==task)
        if t['status']=='review_pending':continue
        assert t['status']=='open'
        claim=call('mission_cli.py',{'operation':'claim','reference':str(REF),'actor':ACTOR,'task_id':task,
            'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
            'event_id':'restore-existing-'+task+'-claim','lease_seconds':600},task+'_RESTORE_CLAIM')
        p=current()
        call('mission_cli.py',{'operation':'submit','reference':str(REF),'actor':ACTOR,'task_id':task,
            'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
            'event_id':'restore-existing-'+task+'-submit','lease_id':claim['task']['lease']['id'],
            'evidence':inventory['requirements'][task]['evidence'],
            'note':'Entrega existente recuperada para revisão; nenhum novo trabalho científico ou aceite inferido.'},task+'_RESTORE_SUBMIT')
    p=current();save('MISSION_CURRENT_RECEIPT.json',p)
    assert not p['projection']['tetelestai']
    return p

def append_memory(path,raw,stamp):
    old=path.read_bytes();backup=path.with_name(path.name+'.bak_'+stamp+'_mission_sync')
    new_bytes(backup,old)
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    combined=old+raw
    with tmp.open('xb') as f:
        f.write(combined);f.flush();os.fsync(f.fileno())
    assert tmp.stat().st_size==len(combined)
    if path.read_bytes()!=old:raise RuntimeError('Memory changed concurrently: '+str(path))
    os.replace(tmp,path)
    assert path.read_bytes()==combined and backup.read_bytes()==old
    return {'target':str(path),'backup':str(backup),'before_sha256':hashlib.sha256(old).hexdigest(),
            'after_sha256':pin(path)['sha256'],'added_bytes':len(raw),'prefix_unchanged':True}

def main():
    if (ROOT/'DELIVERY.json').exists():raise RuntimeError('Delivery already exists: do not overwrite.')
    p=restore_deliveries()
    review=ROOT/'ACTIVATION_INDEPENDENT_REVIEW.json'
    assert review.exists()
    m0=next(x for x in p['projection']['settled'] if x['id']=='M0_MEMORIA')
    assert m0['reviewed_by']!=m0['submitted_by']
    tasks={x['id']:x['status'] for x in p['projection']['active']+p['projection']['settled']}
    sources=['OPERADOR_VERBATIM.txt','SOURCE_BYTES_CHECK.json','NOVA_UNIDADE.json','DEPLOYMENT.json',
      'VALIDATION_FINAL.json','REVIEW_CORE_R2.json','SUPPLEMENT_FINAL_PIN.json','INSTALLED_MCP_VERIFICATION.json',
      'ACTIVATION_INDEPENDENT_REVIEW.json','ACOM_REFERENCE.json','FECHO_MISSION_REFERENCE.json',
      'LEGACY_CHECKPOINT.json','LEGACY_CONTINUITY_RECEIPT.json','FECHO_MIGRATE_RECEIPT.json',
      'MISSION_REQUIREMENTS.json','CURRENT_REQUIREMENTS_INVENTORY.json','CURRENT_BASIS.json','QUEUE_READ_ONLY.json',
      'EXISTING_BUILD_PROCESSES.json','EXISTING_BUILDS_CUSTODY.json','MISSION_CURRENT_RECEIPT.json',
      'mission.py','mission_cli.py','mission_bridge.py','MISSION_PROTOCOL.md','test_mission.py','test_mcp.py',
      'test_mission.py.FINAL.log','test_mcp.py.FINAL.log','activate.py','checkpoint.py',
      'verify_installed.py','capture_existing_builds.py','finish_delivery.py']
    result={'unit':UNIT,'at':datetime.now(timezone.utc).isoformat(),'author':'codex-gerente-tgl',
      'technical_status':'INSTALLED_AND_INDEPENDENTLY_REVIEWED_WITH_SCOPE','board_status_requested':'ENTREGUE',
      'reuse':{'existing':'ACOM MemoryStore v2, same SQLite delta ledger, CAS, q/p, session CLI, existing MCP server.',
              'nos_vivo':'Consulta da unidade nova recusou: unidade não está no grafo. Não interpretado como ausência do código; README/fontes/quadro e mapa foram lidos diretamente.',
              'routes':['infra.memoria_acom.core_20261010','infra.memoria_acom.integracao_20261010']},
      'diagnosis':'O histórico acumulava progresso, mas os dez requisitos originais continuavam sem estado atualizado. Agentes e retomadas podiam trabalhar com critérios/pendências antigos.',
      'implemented':['Identidade e inscrição imutáveis no mesmo ACOM','DAG de requisitos, critérios, evidências e posse temporária',
         'CAS e preflight recusam revisão antiga ou dependência rompida','Candidato e aceite por revisor distinto separados',
         'PODA tira satisfeitos da fila ativa e conserva a história','Invalidação propaga para dependentes',
         'Parada exige todos os requisitos satisfeitos e ausência de execução pendente/incerta',
         'CLI, quatro ferramentas no MCP existente e instruções persistentes Codex/Claude',
         'Poll local de até 30s sem modelo e handoff com referência/revisão/critério/lease'],
      'operational_mapping':{'inscription':'objetivo e restrições preservados','q':'registros com fonte/estatuto e requisitos atuais',
         'p':'fase, próxima ação e identidades externas','dissipation':'poda de trabalho já aceito e recusa de incoerência operacional',
         'tetelestai':'conjunção de critérios satisfeitos, evidências válidas e ausência de trabalho incerto',
         'scope':'Adaptação discreta auditável. Não é demonstração de equação GKLS/Lindblad nos pesos do modelo.'},
      'validation':{'unit_tests':28,'isolated_stdio_assertions':8,'independent_final_focal_tests':2,
         'independent_handle_controls':9,'installed_files':8,'new_mcp_tools':4,'actual_installed_stdio':'PASS',
         'independent_activation':'PASS_WITH_SCOPE','M0_state':m0['status'],'reviewer':m0['reviewed_by']},
      'current_mission':{'reference':str(REF),'revision':p['receipt']['revision'],'projection_chars':p['actual_chars'],
         'tasks':tasks,'handles':len(p['projection']['flow']['handles']),
         'unresolved_handles':[h['id'] for h in p['projection']['unresolved_handles']],
         'tetelestai':p['projection']['tetelestai'],'science_basis':'v393; v394 candidate in sandbox'},
      'limits':['Clientes precisam cumprir o protocolo. Processos MCP já abertos não foram recarregados; o CLI funciona imediatamente.',
         'Ator distinto é uma fronteira de confiança local, não autenticação criptográfica de outra pessoa.',
         'Preflight e execução externa não são uma transação atômica; retorno é reconciliado por CAS.',
         'Projeta estado obrigatório sem corte silencioso; overflow recusa. Não promete memória infalível ou redução percentual de tokens não medida.',
         'Hooks/trust e pesos não foram alterados. Não houve nova chamada de provedor, build científico ou alteração de gate nesta correção.'],
      'migration_notes':'Duas tentativas de preparação recusaram uma suposição errada sobre newline antes de criar o novo contexto. Conferência de bytes resolveu: fonte igual à inscrição; nenhum original foi corrigido.',
      'artifacts':[pin(ROOT/f) for f in sources]}
    save('DELIVERY.json',result)
    TUNNEL.mkdir(exist_ok=True)
    copy_names=['DELIVERY.json','MISSION_PROTOCOL.md','mission.py','mission_cli.py','mission_bridge.py',
        'MISSION_REQUIREMENTS.json','CURRENT_REQUIREMENTS_INVENTORY.json','MISSION_CURRENT_RECEIPT.json',
        'VALIDATION_FINAL.json','INSTALLED_MCP_VERIFICATION.json','ACTIVATION_INDEPENDENT_REVIEW.json']
    for name in copy_names:new_bytes(TUNNEL/name,(ROOT/name).read_bytes())
    save('TUNNEL_CUSTODY.json',{'files':[pin(TUNNEL/n) for n in copy_names],
        'note':'Cópias de evidência. A referência executável continua no caminho original, não se bifurcou o banco.'})
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    text=('\r\n\r\n## 16/10/2026 — Missão ancorada e PODA operacional\r\n'
       '<!-- IALD_MISSION_DELIVERY_20261016 -->\r\n'
       '[INPUT] Ordem do operador: corrigir a memória e a sincronização dos agentes antes de avançar a ciência. '
       '[AUTORIA] codex-gerente-tgl; unidade '+UNIT+', reivindicação 891 (superfícies nomeadas).\r\n\r\n'
       '[REAL] Instalados controlador e CLI no mesmo ACOM, quatro ferramentas no MCP existente, protocolo no README e instruções globais Codex/Claude. '
       'Oito destinos por hash, backups imediatos de bytes; 28 testes do núcleo, oito verificações stdio em cópia e teste do servidor instalado em processo novo. '
       'Revisão independente do código e da ativação; M0 aceito tecnicamente pelo revisor distinto. O quadro recebe ENTREGUE, não se presume ratificação da c1.\r\n\r\n'
       '[REAL] A missão corrente usa `'+str(REF)+'`, revisão '+str(p['receipt']['revision'])+'. '
       'Dez critérios originais e oito decisões INPUT preservados, com M0 memória acrescentado. R1/R2/R9 recuperados como entregas aguardando revisão; demais resíduos permanecem explícitos. '
       'Três jobs externos e oito builds previamente iniciados estão em handles; nenhum foi repetido. Snapshot do build ainda em execução é datado, não afirma estado futuro.\r\n\r\n'
       '[REGRA] Sincronizar na retomada, antes de ação material e antes de integrar devolução. Referência exata, requisito, lease, revisão e pinos viajam juntos. '
       'Revisão velha ou evidência rompida recusa; candidato não é aceite; satisfeitos saem da fila ativa; parada exige ausência de pendências/incerteza.\r\n\r\n'
       '[ESCOPO] Adaptação operacional da preservação da inscrição e PODA/Tetelestai, sem alegar Lindblad físico nos pesos. '
       'Consumidores legados precisam aderir; processos antigos não foram reiniciados. CLI disponível em processo novo. '
       'A ciência continua incompleta; v393 é a base conferida e V351 nomeia módulos reaproveitados. Nenhum um.py, kernel, Bancada, dado ou gate alterado.\r\n\r\n'
       '[EVIDÊNCIA] `'+str(TUNNEL/'DELIVERY.json')+'`, SHA256 `'+pin(ROOT/'DELIVERY.json')['sha256']+'`. '
       'Protocolo: `'+str(CORE/'MISSION_PROTOCOL.md')+'`.\r\n')
    raw=text.encode('utf-8')
    paths=[CENTRAL/'memory/DIARIO_CONSTRUCAO_QG.md',CENTRAL/'memory/TGL_ATLAS.md',CENTRAL/'memory/TGL_INDICE_VIVO.md',
           CENTRAL/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    receipts=[]
    for i,path in enumerate(paths):
        row=append_memory(path,raw,stamp);save('MEMORY_APPEND_'+str(i+1)+'.json',row);receipts.append(row)
    save('MEMORY_DELIVERY.json',{'author':'codex-gerente-tgl','unit':UNIT,'claim_event':891,'surfaces':receipts})
    print(json.dumps({'delivery':str(TUNNEL/'DELIVERY.json'),'revision':p['receipt']['revision'],'chars':p['actual_chars'],'tasks':tasks,'memory_surfaces':len(receipts)}))

if __name__=='__main__':main()
