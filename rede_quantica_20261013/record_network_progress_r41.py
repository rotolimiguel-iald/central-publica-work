"""Custody recovery and terminal builds without repeating accepted memory work."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MEM = ROOT / 'work/memoria_missao_20261016'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'mission_recovery_terminal_handles_20261016_r41'


def main():
    target = OUT / 'PROGRESS_R41.json'
    if target.exists():
        raise RuntimeError('Immutable receipt already exists; recover instead of repeating')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT / 'memory/DIARIO_CONSTRUCAO_QG.md', ROOT / 'memory/TGL_ATLAS.md',
                ROOT / 'memory/TGL_INDICE_VIVO.md', OUT.parent / 'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, project_receipt = live.project()
    settled = [t['id'] for t in current['projection']['settled']]
    assert {'M0_MEMORIA', 'M1_HANDOFF_CAPACITY'} <= set(settled)
    for task_id in ['R7', 'R8']:
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=task_id, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R41_REGISTER_'+task_id)
    expected = {x['target']: x['new_sha256'] for x in json.loads((MEM/'DEPLOYMENT.json').read_bytes())['files']}
    expected.update({x['target']: x['new_sha256'] for x in json.loads((MEM/'handoff_capacity_e1/DEPLOYMENT_E1.json').read_bytes())['files']})
    installed = [pin(p) for p in expected]
    assert all(p['sha256'] == expected[p['path']] for p in installed)
    attempts = {}
    for stamp, status in [('20261016T150503_386413Z', 'terminated'), ('20261016T150836_845057Z', 'failed')]:
        receipt = OUT/'orbital_rotation/attempts'/stamp/'RECEIPT.json'
        result = json.loads(receipt.read_bytes())
        assert result['exit_code'] != 0
        handle = next(h for h in current['projection']['flow']['handles'] if h['id'] == 'build-'+stamp)
        assert handle['status'] == status
        attempts[stamp] = dict(status=status, exit_code=result['exit_code'], receipt=pin(receipt))
    evidence = [MEM/'VALIDATION_FINAL.json', MEM/'REVIEW_CORE_R2.json', MEM/'FINAL_RECEIPT.json',
        MEM/'handoff_capacity_e1/FINAL_E1.json', project_receipt,
        OUT/'mission_resume_20261016/BALANCE_R3_TERMINATION_R41.json',
        OUT/'gns_coefficient_tomita/CanonicalFockActualModularBalanceR4.lean',
        OUT/'mission_review_20261016/R7_BALANCE_R4_CONJUGATION_CANDIDATE.json',
        OUT/'maxwell_global/MaxwellNullSchwartzConsumerR1.lean',
        OUT/'maxwell_global/MAXWELL_NULL_SCHWARTZ_CONSUMER_CANDIDATE_R1.json']
    evidence.extend(Path(p) for p in sys.argv[1:])
    claims = {
        'memory': ('REAL', 'A implantação e o complemento de capacidade existentes foram recuperados, sem reconstrução: oito alvos conferem por SHA256. A validação registrada tem 28 testes locais e ensaio MCP; revisão independente PASS_WITH_SCOPE. M0_MEMORIA e M1_HANDOFF_CAPACITY permanecem satisfeitos.'),
        'anchor': ('REAL', 'A mesma referência recuperou a missão na revisão89; transições90/91 corrigiram os dois handles de compilação para estados terminais por recibo. Os seis requisitos satisfeitos e os seis abertos continuam distintos; R1-R10 conservam o alcance.'),
        'r7': ('REAL', 'BalanceR3 encerrou após642,498s, EXIT4294967295, sem avanço além do marcador conjugate_right. NormR6 terminou EXIT1 em140,975s, com timeout whnf nas linhas82/165. Os diagnósticos são resultados negativos; nenhum teorema novo foi aceito.'),
        'candidate': ('DECLARADO', 'BalanceR4 recebida como candidata de agente, ainda sem build, com transporte tipado por congrArg. Receber a devolução não fecha R7 e não dispara execução automática.'),
        'r8_candidate': ('DECLARADO', 'MaxwellNullSchwartzConsumerR1 recebida na revisão91, sem build. Propõe Parseval ponderado e derivada pontual do mesmo representante sob regularidade Schwartz explícita; existência/densidade, derivada forte, carga real e energia Fock não nula continuam abertas. R8 não foi aceito.'),
        'limits': ('REAL', 'O código impõe revisão, posse, pinos e parada aos consumidores que usam o protocolo. Sessões antigas precisam aderir ao CLI ou recarregar o MCP; não houve recarga nesta etapa. Não há garantia de infalibilidade, implementação de Lindblad nos pesos ou economia global de tokens já medida.'),
        'remaining': ('OPEN', 'R3/R4/R5/R7/R8/R10 permanecem: rito integral, identificação física/relógio, dispositivo/rede, Takesaki/traço, Maxwell completo e revisão conjunta. Dois jobs awaiting_dispatch não foram repetidos. Base v393, v394 candidata; nenhum original científico, Bancada, dado observado ou gate alterado.')}
    progress = dict(unit='F1.FECHO_20261015', author=WHO, at=dt.datetime.now(dt.timezone.utc).isoformat(),
        reference=str(live.REFERENCE), revision=current['receipt']['revision'], claim=claim,
        claims={k:dict(statute=s,text=t) for k,(s,t) in claims.items()}, installed=installed,
        settled=settled, active=[{k:t[k] for k in ['id','criterion','status']} for t in current['projection']['active']],
        attempts=attempts, evidence=[pin(p) for p in evidence], tests_repeated=False, providers_called=False)
    new(target, progress)
    text = '\n\n## 16/10/2026 — Ancoragem recuperada e execuções reconciliadas\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, pela reivindicação vigente F1.FECHO_20261015.\n'
    for name,(statute,body) in claims.items():
        text += f'\n[{statute} — {name}] {body}\n'
    text += f'\nEvidência: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R41.txt', text)
    new(OUT/'MEMORY_PROGRESS_R41.json', dict(claim=claim, surfaces=[append_bytes(p,text,MARKER) for p in surfaces], evidence=pin(target)))
    new(OUT/'MAP_ENTRY_PROGRESS_R41.json', dict(tipo='ANOTACAO', rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL', titulo='Ancoragem recuperada; duas compilações terminais sem repetição',
        resultado=' '.join(t for _,t in claims.values()), estatuto='REAL — custódia; OPEN — critérios científicos',
        status='EM_CURSO', veredito='MEMORY_DEPLOYMENT_VERIFIED_BUILD_HANDLES_RECONCILED',
        defeito=claims['remaining'][1], proximo_passo='Preservar diagnósticos e retomar somente requisitos abertos com revisão atual.',
        onde=str(OUT), artefatos=[str(target),str(OUT/'MEMORY_PROGRESS_R41.json')], olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_PROGRESS_R41.json','--quem',WHO], 'MAP_RECEIPT_PROGRESS_R41.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',target,
        OUT/'MEMORY_PROGRESS_R41.json','--nota','R41: memória recuperada; tentativas terminais custodiadas; nenhuma nova construção científica aceita.'], 'BOARD_PROGRESS_R41.json')
    current,_ = live.project()
    flow = dict(current['projection']['flow'])
    flow.update(phase='mission_synchronized_r7_diagnostics_preserved',
        next_action='M0/M1 aceitos: não reconstruir memória. Antes de integrar candidato, recuperar referência e revisão atuais; R7 aguarda correção de conversão, R8 a ponte carga/energia, R4/R5/R3/R10 mantêm critérios integrais.')
    result, receipt = live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=current['receipt']['revision'], event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',text='Memória instalada conferida; dois builds terminais e candidata R4 preservados. Sem nova prova aceita; alcance integral em PROGRESS_R41.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],flow=flow)), 'R41_TRANSITION')
    print(json.dumps(dict(progress=pin(target), revision=result['revision'], receipt=str(receipt)),ensure_ascii=False))


if __name__ == '__main__':
    main()
