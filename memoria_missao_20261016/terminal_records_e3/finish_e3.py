"""Register independently accepted E3, preserving every scientific requirement."""
from support_e3 import *

def main():
    p=project('FINAL_E3_PROJECT',100000)
    task=next(t for t in p['projection']['settled'] if t['id']==TASK)
    assert task['status']=='satisfied' and task['reviewed_by']!=ACTOR['id']
    claim=command([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT],'FINAL_E3_BOARD')['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    expected={}
    for path in [BASE.parent/'DEPLOYMENT.json',BASE.parent/'handoff_capacity_e1/DEPLOYMENT_E1.json',
        BASE.parent/'terminal_projection_e2/DEPLOYMENT_E2.json',BASE/'DEPLOYMENT_E3.json']:
        expected.update({r['target']:r['new_sha256'] for r in json.loads(path.read_bytes())['files']})
    installed=[pin(path) for path in expected]
    assert all(row['sha256']==expected[row['path']] for row in installed)
    live=json.loads((BASE/'LIVE_VERIFICATION_E3.json').read_bytes())
    assert live['ok'] and live['installed']==pin(CORE/'lib/iald_memory/mission.py')
    files=['FINDING.json','mission_candidate_r2.py','SOURCE_BASELINE_E3_R2.json',
        'TEST_RESULTS_E3_R2.json','TRACKER_TEST_RESULTS_E3_R2.json','REVIEW_E3_R2.json',
        'DOC_PLAN_E3_R2.json','PROTOCOL_ADDITION_E3_R2.txt','INSTRUCTIONS_ADDITION_E3.txt',
        'install_e3_r2.py','DEPLOYMENT_E3.json','verify_live_e3_r2.py','LIVE_VERIFICATION_E3.json',
        'REVIEW_INSTALLED_E3.json','ACCEPT_E3_RECEIPT.json']
    delivery=new('DELIVERY_E3.json',dict(ok=True,unit=UNIT,author=ACTOR['id'],claim=claim,
        at=dt.datetime.now(dt.timezone.utc).isoformat(),reference=pin(REF),requirement=TASK,
        accepted_task=task,mission_revision=p['receipt']['revision'],status='INSTALLED_INDEPENDENTLY_ACCEPTED',
        measurements=live,evidence=[pin(BASE/f) for f in files],installed_current=installed,
        tracker=pin(OUT/'mission_resume_20261016/track_build_r45.py'),
        scientific_custody=pin(OUT/'PROGRESS_R44_SCIENCE_CUSTODY.json'),
        limits=['Only exactly recognized legacy mechanical build notices are indexed.',
          'Full q/p and journal are retained; source mismatch stays visible.',
          'Finite required context can still overflow explicitly; measured characters are not billed tokens.',
          'Clients must synchronize; this does not modify model weights or execute Lindblad in them.',
          'Scientific mission remains incomplete; no gate, provider or production-science changes.']))
    marker='mission_terminal_records_e3_20261016'
    text=f'''

## 16/10/2026 — Memória da missão: avisos mecânicos no índice, conclusões preservadas
<!-- {marker} -->
[REAL — em nome de codex-gerente-tgl, reivindicação917 de {UNIT}] O uso prolongado voltou a produzir overflow:100318caracteres na revisão172, pois avisos mecânicos do tracker repetiam o fluxo. A recusa foi explícita. A camada E3 foi construída e corrigida após ataques independentes, preservando candidatas e recibos falhos. Somente avisos de build de esquema/texto exatos, tarefa/handle coerentes e recibos JSON pinados e verificados são indexados. Ordens, ciência, erratas, ambiguidades e execuções incertas permanecem integrais; get e diário conservam todos os registros.

[REAL] Código e três adendos (protocolo, AGENTS e CLAUDE) instalados com backup de bytes, plano e pares path/SHA revisados. M3_TERMINAL_RECORDS aceito por revisor distinto. O trackerR45 escreve deltas de fluxo, sem duplicar cada início/fim como fato; seus9testes locais passam. A verificação real viaMCP em processo novo mediu {live['full_projection_chars_same_snapshot']}→{live['compact_projection_chars']} caracteres no mesmo estado ({100*live['reduction_fraction']:.2f}% de redução adicional), com {live['indexed_mechanical_records']} avisos indexados e {live['visible_records']} registros integrais. Sync=handoff, preflight, poll e igualdade do get antes/depois conferidos. Oito destinos da cadeiaM0+E1+E2+E3 conferidos por hash.

[OPEN — limite] O crescimento de fatos obrigatórios ainda pode causar overflow visível. Caracteres não equivalem a tokens faturados. Sessões devem aplicar o protocolo; não há garantia universal de memória nem alteração de pesos/GKLS. A memória é controle operacional discreto com inscrição preservada, revisão e PODA. Nenhum trabalho científico foi iniciado durante a correção prioritária; compilações já em voo foram apenas custodiadas.

[REAL/OPEN — continuidade] R44 conserva5declarações novas do momento real nulo, só no trio e revistas como componente. O fator Fourier(2π)^3 foi localizado; adaptador e derivada forte ainda não estão aceitos, e a sonda de especializaçãoHilbert daR7 falhou com limites finitos. R3/R4/R5/R7/R8/R10 permanecem abertos no alcance original. Os IDs de provedores anteriores não foram repetidos. O próximo passo é recuperar a missão atual e os erros registrados, com trackerR45 e preflight, sem reconstruirM0–M3.

Evidência: `{delivery}`; SHA256 `{pin(delivery)['sha256']}`.
'''
    new('MEMORY_ADDITION_E3.txt',text.encode('utf-8'))
    sys.path.insert(0,str(CENTRAL/'work/rede_quantica_20261013'))
    from diary_r1 import append_bytes
    surfaces=[CENTRAL/'memory/DIARIO_CONSTRUCAO_QG.md',CENTRAL/'memory/TGL_ATLAS.md',
        CENTRAL/'memory/TGL_INDICE_VIVO.md',OUT.parent/'AVISO_GERENCIA.md']
    assert all(path.name in claim['nota'] for path in surfaces)
    rows=[]
    for i,path in enumerate(surfaces,1):
        row=append_bytes(path,text,marker);rows.append(row);new('MEMORY_APPEND_E3_'+str(i)+'.json',row)
    memory=new('MEMORY_E3.json',dict(unit=UNIT,claim=claim,surfaces=rows,append_only=True))
    entry=new('MAP_ENTRY_E3.json',dict(tipo='ANOTACAO',rota_id='infra.memoria_missao.ancoragem_e_poda_20261016',
        dominio='INFRAESTRUTURA',titulo='E3: avisos mecanicos indexados e tracker sem duplicacao de fatos',
        resultado=f"M3 aceito independentemente; {live['full_projection_chars_same_snapshot']} para {live['compact_projection_chars']} caracteres no mesmo estado. MCP e recuperacao integral conferidos.",
        estatuto='REAL',status='EXAMINADA',veredito='INSTALLED_INDEPENDENTLY_ACCEPTED',
        defeito='Contexto finito; overflow ainda possivel para fatos obrigatorios. Clientes devem sincronizar.',
        proximo_passo='Retomar somente ciencia aberta com trackerR45, referencia propria e preflight.',
        onde=str(CORE/'MISSION_PROTOCOL.md'),artefatos=[str(delivery),str(memory)],olhou_dados=False))
    command([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',ACTOR['id']],'MAP_RECEIPT_E3')
    command([r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE',
        '--evidencia',delivery,memory,BASE/'ACCEPT_E3_RECEIPT.json',BASE/'MAP_RECEIPT_E3.json',
        '--nota','E3 instalado e aceito independentemente; trackerR45 evita duplicacao mecanica; ciencia integral aberta.'],'BOARD_DELIVERY_E3')
    science_entry=new('MAP_ENTRY_R44.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='R44: momento real Maxwell e diagnosticos preservados durante reparo de memoria',
        resultado='Cinco listas no trio, revisao independente componente. Fator Fourier explicito. Tres builds posteriores EXIT1, nenhuma promocao de criterio. MemoriaE3 prioritaria entregue.',
        estatuto='REAL — componente; OPEN — criterios integrais',status='EM_CURSO',veredito='COMPONENT_ONLY',
        defeito='R7 especializacao Hilbert; R8 derivada forte, normalizacao e carga completas ainda abertas.',
        proximo_passo='Usar erros terminais e estado atual, sem repetir tentativas encerradas.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R44_SCIENCE_CUSTODY.json'),str(delivery)],olhou_dados=False))
    command([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',science_entry,'--quem',ACTOR['id']],'MAP_RECEIPT_R44')
    command([r'C:\IALD\PROGRAMA_IALD\iald.py','avancar','F1.FECHO_20261015','--quem',ACTOR['id'],
        '--status','EM_CURSO','--evidencia',OUT/'PROGRESS_R44_SCIENCE_CUSTODY.json',
        '--nota','R44: custodia de5axiomas revisados e3builds falhos; sem criterio integral aceito. E3 de memoria corrigida primeiro.'],'BOARD_PROGRESS_R44')
    snapshot=call('session_memory.py',dict(operation='get',reference=str(REF)),'FINAL_FLOW_GET')
    record=dict(id='memory-e3-delivered',kind='fact',statute='REAL',
        text='E3 entregue e aceito independentemente. Avisos mecanicos legados terminais indexados com pins, originais no get. TrackerR45 usa somente flow. Protocolo/AGENTS/CLAUDE instalados; oito alvos conferidos. R44 cientifico e limitacoes nos recibos; criterios integrais continuam abertos.',
        sources=[dict(kind='artifact',ref=str(delivery),sha256=pin(delivery)['sha256']),
            dict(kind='artifact',ref=str(OUT/'PROGRESS_R44_SCIENCE_CUSTODY.json'),sha256=pin(OUT/'PROGRESS_R44_SCIENCE_CUSTODY.json')['sha256'])])
    call('session_memory.py',dict(operation='transition',reference=str(REF),actor=ACTOR,
        expected_revision=snapshot['revision'],event_id='memory-e3-delivered',changes=dict(records=[record],
        flow=dict(handles=snapshot['p']['handles'],phase='memory_e3_delivered_science_open',
            next_action='M0/M1/M2/M3 satisfeitos: nao reconstruir. Usar trackerR45. R7 investigar especializacao generica; R8 corrigir diagnosticos de derivada forte e adaptadorFourierR2 ainda nao compilado. R4/R5 fisicos e R3/R10 integrais abertos.'))),'FINAL_FLOW_E3')
    verify=call('session_memory.py',dict(operation='verify',reference=str(REF)),'FINAL_VERIFY_E3')
    assert verify['ok']
    command([r'C:\IALD\PROGRAMA_IALD\iald.py','liberar',UNIT,'--quem',ACTOR['id'],
        '--nota','E3 entregue; memoria aditiva coberta pela reivindicacao917.'],'BOARD_RELEASE_E3')
    final=new('FINAL_E3.json',dict(ok=True,unit=UNIT,delivery=pin(delivery),memory=pin(memory),
        acceptance=pin(BASE/'ACCEPT_E3_RECEIPT.json'),map=pin(BASE/'MAP_RECEIPT_E3.json'),
        board=pin(BASE/'BOARD_DELIVERY_E3.json'),verify=pin(BASE/'FINAL_VERIFY_E3.json'),claim_released=True))
    print(json.dumps(dict(ok=True,delivery=str(delivery),revision=verify['receipt']['revision'],final=str(final))))

if __name__=='__main__':main()
