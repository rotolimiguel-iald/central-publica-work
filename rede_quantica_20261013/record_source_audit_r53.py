"""Custody of reviewed source findings and synchronized residuals, not science acceptance."""
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r53 as live
reg.DEST = OUT
MARKER = 'mission_source_progress_r53_20261016'


def evidence(path):
    return {k: v for k, v in pin(path).items() if k in ['path', 'sha256']}


def main():
    target = OUT / 'PROGRESS_R53.json'
    if target.exists():
        raise RuntimeError('Recover the existing immutable delivery; never overwrite')
    review = Path(sys.argv[1]).resolve()
    if not review.is_relative_to(OUT / 'mission_review_20261016'):
        raise RuntimeError('Review must be in the assigned independent-review directory')
    review_doc = json.loads(review.read_bytes())
    if 'PASS' not in str(review_doc.get('verdict', '')):
        raise RuntimeError('A passing independent source review is required')
    r4 = OUT / 'physical_clock_reuse/R53/R53_PHYSICAL_CLOCK_SOURCE_AUDIT_R1.json'
    r5 = OUT / 'global_net_inventory/R53/DEVICE_CONTINUUM_SOURCE_AUDIT_R1.json'
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, project_receipt = live.project()
    expected_settled = {'M0_MEMORIA', 'M1_HANDOFF_CAPACITY', 'M2_TERMINAL_PROJECTION',
                        'M3_TERMINAL_RECORDS', 'R1', 'R2', 'R6', 'R7', 'R8', 'R9'}
    assert {x['id'] for x in current['projection']['settled']} == expected_settled
    for requirement in ['R4', 'R5']:
        task = next(x for x in current['projection']['active'] if x['id'] == requirement)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=requirement, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R53_DELIVERY_CHECK_' + requirement)
    memory_delivery = ROOT/'work/memoria_missao_20261016/terminal_records_e3/DELIVERY_E3.json'
    installed = json.loads(memory_delivery.read_bytes())['installed_current']
    assert all(pin(x['path'])['sha256'] == x['sha256'] for x in installed)
    generic = OUT/'mission_resume_20261016/LIVE_R53_RAW_SESSION_RECOVERY_20261016T213544_851696Z_944861e3_RECEIPT.json'
    specific = OUT/'mission_resume_20261016/LIVE_R53_PROJECT_20261016T213445_206047Z_a3c4e6f2_RECEIPT.json'
    raw = json.loads(generic.read_bytes())['result']
    compact = json.loads(specific.read_bytes())['result']
    assert raw['receipt']['state_sha256'] == compact['receipt']['state_sha256']
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R53_RETURN_GET')
    handles = copy.deepcopy(state['p']['handles'])
    returns = {'r53-physical-clock-source': r4, 'r53-device-continuum-source': r5,
               'r53-joint-source-review': review}
    for identity, path in returns.items():
        handle = next(x for x in handles if x['id'] == identity)
        assert handle['status'] in ['running', 'returned']
        handle.update(status='returned', receipt=evidence(path), requirement_satisfied=False)
    next_action = ('Aguardar a identificacao humana do aparelho/setor mecanico: MQC, Supercondutor ou Psi-NET. '
        'Nao escolher por conveniencia nem reconstruir a rede aceita. Com a resposta, usar os contratos residuais R53 '
        'para ligar estado, referencial, energia, relogio, dominio e transporte do mesmo sistema. '
        'R4/R5 permanecem abertos; R3 rito integral e R10 revisao conjunta dependem deles. '
        'M0-M3 ja aceitos: continuar com referencia exata, sincronizacao/preflight/handoff/CAS e PODA. '
        'Nenhuma nova auditoria desta camada sem achado material.')
    live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id='r53-source-audits-and-review-returned',
        changes=dict(flow=dict(handles=handles))), 'R53_RETURNS_FLOW')
    current, project_receipt = live.project()
    assert not current['projection']['unresolved_handles']
    claims = [
        ('REAL', 'As duas auditorias documentais R53 e a revisao independente retornaram. A rede continua, Fock, Takesaki e Maxwell ja aceitos permanecem preservados; nenhum requisito de construcao R4/R5 foi promovido a satisfeito por uma leitura de fontes.'),
        ('REAL', 'Ha estados e relogios nomeados nas fontes Custo/F1.TEMPO, Supercondutor e MQC. A lacuna e a identificacao dos objetos, dominios e normalizacoes do mesmo aparelho, nao a ausencia de todo estado ou relogio. O teste finito 2x2x2 nao constitui a familia de refinamentos e o entrelacamento exigidos pelo contrato da rede.'),
        ('DERIVED', 'No gerador MQC auditado, H_eff=0 e afirmado no referencial girante. Para taxas positivas e 0<beta<1, o estado estacionario tem suporte de posto 2 em C^3; uma construcao modular precisa declarar esse suporte ou justificar uma realizacao fiel, sem apagar o terceiro nivel. Isso e diagnostico algebrico documental, sem novo build ou medida.'),
        ('REAL', 'O PDF MQC associa 9 cm a 1,667 MHz; sua regra f=c/(2L) fornece aproximadamente 1,667 GHz. Divergencia de unidade preservada ao lado; nenhum original corrigido silenciosamente. A referencia de fase OH do Supercondutor e outro objeto.'),
        ('DERIVED', 'B0_no_eigen obstrui entrelacamento injetivo de uma reta propria comum de boosts com H1. O diagnostico nao se aplica automaticamente ao vacuo de Fock nem a modos bosonicos sem truncamento; a ausencia de ponte foi examinada apenas no recorte de fontes descrito pelos relatorios.'),
        ('REAL', 'Memoria M0-M3 reconferida em oito arquivos instalados. Na mesma revisao 419, projecao generica tem 302989 caracteres e a projecao propria da missao 100030; sao representacoes distintas do mesmo estado. A generica recusou 250000 e foi recuperada com 330000; a propria usa capacidade explicita 125000. Sem truncamento, repeticao de reivindicacao ou alegacao de economia de tokens faturados.'),
        ('OPEN', 'A identidade do dispositivo/setor continua pendente da resposta humana ja solicitada. R4/R5, R3 e R10 continuam abertos com os criterios originais. Nenhum novo experimento, build, provedor, producao cientifica ou gate foi executado/alterado nesta etapa.'),
    ]
    new(target, dict(unit='F1.FECHO_20261015', author=WHO, at=dt.datetime.now(dt.timezone.utc).isoformat(),
        claim=claim, reference=pin(live.REFERENCE), revision=current['receipt']['revision'],
        evidence=[pin(p) for p in [r4, r5, review, project_receipt, generic, specific,
                                   memory_delivery, OUT/'R53_SOURCE_REVIEW_START.json', Path(__file__)]],
        original_criteria_preserved=True, settled_ids=sorted(expected_settled),
        active_requirements=current['projection']['active'], unresolved_handles=[],
        claims=[dict(statute=s, text=t) for s, t in claims], next_action=next_action,
        new_builds=0, provider_calls=0, new_experiments=0, production_changes=False, gate_moved=False,
        full_mission_complete=False))
    text = '\n\n## 16/10/2026 — R53: fontes do dispositivo e retomada sincronizada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicacao F1.FECHO_20261015.\n'
    text += ''.join(f'\n[{s}] {t}\n' for s, t in claims)
    text += f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R53.txt', text)
    mem = OUT/'MEMORY_PROGRESS_R53.json'
    new(mem, dict(claim=claim, evidence=pin(target), surfaces=[append_bytes(p, text, MARKER) for p in surfaces]))
    entry = OUT/'MAP_ENTRY_PROGRESS_R53.json'
    new(entry, dict(tipo='ANOTACAO', rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='R53: diagnostico das fontes do dispositivo e memoria sincronizada',
        resultado=' '.join(t for _, t in claims), estatuto='REAL — custodia; DERIVED — diagnosticos; OPEN — ponte fisica',
        status='EM_CURSO', veredito='SOURCE_AUDIT_REVIEWED_DEVICE_IDENTITY_PENDING',
        proximo_passo=next_action, onde=str(OUT), artefatos=[str(target), str(mem)], olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', entry, '--quem', WHO], 'MAP_RECEIPT_PROGRESS_R53.json')
    reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
        '--evidencia', target, mem, '--nota', 'R53: fontes/revisao conferidas; pendente identidade do dispositivo; criterios preservados.'], 'BOARD_PROGRESS_R53.json')
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R53_MATERIAL_GET')
    result, receipt = live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id=MARKER,
        changes=dict(records=[dict(id=MARKER, kind='fact', statute='REAL',
            text='R53: duas auditorias de fontes e revisao independente concluidas. Relatorio pina os diagnosticos e seus limites. Aparelho/setor ainda requer identificacao humana; R4/R5/R3/R10 continuam abertos. M0-M3 instalados e recuperados sem truncamento; nenhum trabalho aceito reaberto.',
            sources=[dict(kind='artifact', ref=str(target), sha256=pin(target)['sha256'])])],
            flow=dict(handles=state['p']['handles'], phase='device_identity_pending_source_audit_complete', next_action=next_action))), 'R53_MATERIAL_TRANSITION')
    verified, vr = live.call('session_memory.py', dict(operation='verify', reference=str(live.REFERENCE)), 'R53_FINAL_VERIFY')
    print(json.dumps(dict(progress=pin(target), revision=result['revision'], receipt=str(receipt),
        verify_receipt=str(vr), verify_ok=verified.get('ok')), ensure_ascii=False))


if __name__ == '__main__':
    main()
