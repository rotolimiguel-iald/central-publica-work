"""Register independently accepted E2, with additive memory and full custody."""
from support_e2 import *

def main():
    p=project('FINAL_E2_PROJECT',100000)
    t=next(t for t in p['projection']['settled'] if t['id']==TASK)
    assert t['status']=='satisfied' and t['reviewed_by']!=ACTOR['id']
    claim=command([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT],'FINAL_E2_BOARD')['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    expected={}
    for f in [BASE.parent/'DEPLOYMENT.json',BASE.parent/'handoff_capacity_e1/DEPLOYMENT_E1.json',BASE/'DEPLOYMENT_E2.json']:
        expected.update({r['target']:r['new_sha256'] for r in json.loads(f.read_bytes())['files']})
    installed=[pin(x) for x in expected]
    assert all(x['sha256']==expected[x['path']] for x in installed)
    live=json.loads((BASE/'LIVE_VERIFICATION_E2.json').read_bytes())
    assert live['ok'] and live['installed']==pin(CORE/'lib/iald_memory/mission.py')
    files=['FINDING.json','SOURCE_BASELINE.json','mission_candidate.py','TEST_RESULTS_E2.json',
           'REVIEW_E2.json','DOC_PLAN_E2.json','PROTOCOL_ADDITION_E2.txt','INSTRUCTIONS_ADDITION_E2.txt',
           'install_e2.py','DEPLOYMENT_E2.json','verify_live_e2.py','LIVE_VERIFICATION_E2.json',
           'REVIEW_INSTALLED_E2.json','ACCEPT_E2_RECEIPT.json']
    evidence=[pin(BASE/f) for f in files]
    delivery=new('DELIVERY_E2.json',dict(ok=True,unit=UNIT,author=ACTOR['id'],claim=claim,
        at=dt.datetime.now(dt.timezone.utc).isoformat(),reference=pin(REF),requirement=TASK,
        accepted_task=t,mission_revision=p['receipt']['revision'],status='INSTALLED_INDEPENDENTLY_ACCEPTED',
        measurements=live,evidence=evidence,installed_current=installed,
        limits=['Terminal details are indexed in projection, not deleted from state.',
                'Orders/facts/errata remain required; sufficient growth can still cause explicit overflow.',
                'Characters are measured, not billed token savings.',
                'Clients must use synchronization protocol; no universal memory guarantee or weights change.',
                'Science remains incomplete and gate unchanged.']))
    marker='mission_terminal_projection_e2_20261016'
    text=f'''

## 16/10/2026 — PODA aplicada ao fluxo encerrado, com recuperação integral
<!-- {marker} -->
[REAL — codex-gerente-tgl, reivindicação912 de {UNIT}] A projeção da revisão109 recusou102632caracteres diante do orçamento100000. A causa medida incluiu52handles terminais completos. O controlador agora mantém pendências/estados desconhecidos integrais e um índice compacto dos encerrados, com recuperação pelo get da referência exata. O estado q/p persistido, original, diário, critérios, fatos e erratas não foram apagados nem resumidos.

[REAL] Código e três adendos (protocolo, AGENTS e CLAUDE) instalados com backups de bytes após revisão independente; M2_TERMINAL_PROJECTION aceito por revisor distinto. Testes sintéticos:1000terminais e3pendentes; detalhes integrais continuam no get. A verificação da missão real pelo MCP em processo novo mediu {live['full_projection_chars_same_snapshot']}→{live['compact_projection_chars']} caracteres no mesmo estado ({100*live['reduction_fraction']:.2f}% de redução), com {live['terminal_handles']} encerrados e {live['active_handles']} pendentes. Sync=handoff, preflight e poll conferidos; estado/journal sem mutação por leitura. Oito destinos instalados conferidos pela cadeia M0+E1+E2.

[ESCOPO] Contagem de caracteres não equivale a tokens faturados. Fatos obrigatórios ainda podem exceder capacidade e provocar recusa explícita. O índice terminal não autoriza repetir execuções. Get devolve estado atual: conferir revisão/hash antes de integrar; histórico anterior no diário. Clientes devem aderir ao protocolo. Nenhum provedor, Lean, um.py, kernel, Bancada, dado ou gate alterado nesta correção; os seis critérios científicos restantes conservam o alcance.

Evidência: `{delivery}`; SHA256 `{pin(delivery)['sha256']}`.
'''
    new('MEMORY_ADDITION_E2.txt',text.encode('utf-8'))
    sys.path.insert(0,str(CENTRAL/'work/rede_quantica_20261013'))
    from diary_r1 import append_bytes
    surfaces=[CENTRAL/'memory/DIARIO_CONSTRUCAO_QG.md',CENTRAL/'memory/TGL_ATLAS.md',
        CENTRAL/'memory/TGL_INDICE_VIVO.md',OUT.parent/'AVISO_GERENCIA.md']
    assert all(x.name in claim['nota'] for x in surfaces)
    rows=[]
    for i,s in enumerate(surfaces,1):
        row=append_bytes(s,text,marker);rows.append(row);new('MEMORY_APPEND_E2_'+str(i)+'.json',row)
    memory=new('MEMORY_E2.json',dict(unit=UNIT,claim=claim,surfaces=rows,append_only=True))
    entry=new('MAP_ENTRY_E2.json',dict(tipo='ANOTACAO',rota_id='infra.memoria_missao.ancoragem_e_poda_20261016',
        dominio='INFRAESTRUTURA',titulo='PODA dos detalhes encerrados na projecao; recuperacao integral',
        resultado=f"Projecao real {live['full_projection_chars_same_snapshot']} para {live['compact_projection_chars']} caracteres. Estado integral preservado; MCP novo conferido; M2 aceito independentemente.",
        estatuto='REAL',status='EXAMINADA',veredito='INSTALLED_INDEPENDENTLY_ACCEPTED',
        defeito='Fatos obrigatorios continuam crescendo; overflow explicito. Caracteres nao sao tokens faturados. Clientes precisam aderir.',
        proximo_passo='Retomar somente criterios cientificos abertos, com referencia e revisao atuais; incluir E2 nas verificacoes de implantacao.',
        onde=str(CORE/'MISSION_PROTOCOL.md'),artefatos=[str(delivery),str(memory),str(BASE/'ACCEPT_E2_RECEIPT.json')],olhou_dados=False))
    command([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',ACTOR['id']],'MAP_RECEIPT_E2')
    command([r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE',
        '--evidencia',delivery,memory,BASE/'ACCEPT_E2_RECEIPT.json',BASE/'MAP_RECEIPT_E2.json',
        '--nota','E2: projecao terminal compacta instalada e revisada; oito destinos conferidos, memoria aditiva; ciencia e gate inalterados.'],'BOARD_DELIVERY_E2')
    p=project('BEFORE_E2_FINAL_FLOW',100000)
    record=dict(id='memory-e2-delivered',kind='fact',statute='REAL',
        text='E2 entregue: detalhes dos handles terminais saem apenas da projecao ativa, indice recuperavel; estado e fatos preservados. M2 aceito independentemente. Codigo, protocolo, AGENTS/CLAUDE instalados; oito alvos conferidos incluindo M0+E1+E2. Limites e medidas em DELIVERY_E2.',
        sources=[dict(kind='artifact',ref=str(delivery),sha256=pin(delivery)['sha256']),
                 dict(kind='artifact',ref=str(memory),sha256=pin(memory)['sha256'])])
    call('session_memory.py',dict(operation='transition',reference=str(REF),actor=ACTOR,
        expected_revision=p['receipt']['revision'],event_id='memory-e2-delivered',changes=dict(records=[record],
        flow=dict(phase='memory_e2_delivered_science_open',next_action='M0/M1/M2 satisfeitos: nao reconstruir. R42 guarda23listas revisadas e duas candidatas falhas; corrigir Star de pi (R7) e APIs ContDiff/PiLp (R8). R4/R5 dispositivo e R3/R10 integrais. Project+preflight; toda verificacao de instalacao inclui DEPLOYMENT_E2.'))),'FINAL_FLOW_E2')
    verify=call('session_memory.py',dict(operation='verify',reference=str(REF)),'FINAL_VERIFY_E2')
    assert verify['ok']
    command([r'C:\IALD\PROGRAMA_IALD\iald.py','liberar',UNIT,'--quem',ACTOR['id'],
        '--nota','E2 entregue com memoria sob reivindicacao912; revisao independente e recibos preservados.'],'BOARD_RELEASE_E2')
    result=dict(ok=True,unit=UNIT,delivery=pin(delivery),memory=pin(memory),
        acceptance=pin(BASE/'ACCEPT_E2_RECEIPT.json'),map=pin(BASE/'MAP_RECEIPT_E2.json'),
        board=pin(BASE/'BOARD_DELIVERY_E2.json'),verify=pin(BASE/'FINAL_VERIFY_E2.json'),claim_released=True)
    new('FINAL_E2.json',result)
    print(json.dumps({'ok':True,'delivery':str(delivery),'revision':verify['receipt']['revision']}))

if __name__=='__main__':main()
