"""Prepare the immutable R51 stage and close returned branch handles by CAS."""
import copy
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live


def main():
    target = OUT / 'PROGRESS_R51_CONFIG.json'
    if target.exists():
        raise RuntimeError('Immutable configuration already exists')
    review = OUT / 'mission_review_20261016/R51_SMEARING_REVIEW_R1.json'
    reviewed = json.loads(review.read_bytes())
    assert reviewed['verdict'].startswith('PASS')
    assert reviewed['requirement_satisfied'] is False
    split = OUT / 'takesaki_fock/CANONICAL_FOCK_NORMALIZED_SPLIT_CANDIDATE_R4.json'
    assert split.is_file()
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R51_BRANCHES_GET')
    handles = copy.deepcopy(state['p']['handles'])
    branch_sources = {
        'r51-fock-finite-projection': split,
        'r51-wick-local-identification': review,
    }
    for handle in handles:
        if handle['id'] in branch_sources:
            handle.update(status='returned', receipt=pin(branch_sources[handle['id']]),
                          full_requirement_accepted=False)
    next_action = (
        'R7: compilar a candidata CanonicalFockNormalizedSplitR4.lean (ainda DECLARADO), '
        'que corrige os timeouts da R3 por lemas genericos; nao repetir a tentativa encerrada '
        '20261016T204808_750590Z. Depois de EXIT0/trio e revisao, combinar o split com '
        'CanonicalFockCyclicTraceCompletionR3 para preencher RemainingModularCoreInput no mesmo '
        'core Fock. R8: consumir esse A com AxisCompactMaxwellCertificateR4 e a identificacao '
        'Wick/Bochner agora demonstrada; verificar alcance integral antes de aceite. '
        'R4/R5 continuam com relogio/espectro fisico e dispositivo; R3/R10 com rito integral '
        'e revisao. M0-M3 estao aceitos: reutilizar o protocolo, nao redesenhar a memoria.'
    )
    result, flow_receipt = live.call('session_memory.py', dict(
        operation='transition', reference=str(live.REFERENCE), actor=live.ACTOR,
        expected_revision=state['revision'], event_id='r51-branches-returned',
        changes=dict(flow=dict(handles=handles, next_action=next_action))), 'R51_BRANCHES_RETURNED')
    current, project_receipt = live.project()
    assert not current['projection']['unresolved_handles']
    config = dict(
        components=[
            ['20261016T203505_683079Z', 8, 'takesaki_fock', 'R51_CYCLIC_REVIEW_R1.json'],
            ['20261016T204544_576190Z', 5, 'takesaki_fock', 'R51_FINITE_MATRIX_REVIEW_R2.json'],
            ['20261016T204338_618085Z', 5, 'takesaki_fock', 'R51_FINITE_MATRIX_REVIEW_R2.json'],
            ['20261016T203933_770584Z', 15, 'maxwell_global', 'R51_POINT_WICK_REVIEW_R1.json'],
            ['20261016T204422_618535Z', 8, 'maxwell_global', 'R51_POINT_WICK_REVIEW_R2.json'],
            ['20261016T205038_032609Z', 11, 'maxwell_global', 'R51_SMEARING_REVIEW_R1.json'],
        ],
        failed_attempts=[
            '20261016T201910_284165Z', '20261016T203505_746532Z',
            '20261016T203613_985553Z', '20261016T203748_174706Z',
            '20261016T204127_892966Z', '20261016T204208_723695Z',
            '20261016T204650_618420Z', '20261016T204808_750590Z',
        ],
        claims=[
            dict(statute='REAL', text='Extensao ciclica ENNReal do value positivo existente ao mesmo core Fock: invariancia ciclica/star, escala dual e concordancia exata no cone positivo. Nao se afirma linearidade complexa fora desse cone.'),
            dict(statute='REAL', text='Projecao finita nao nula e normalizada construida pela semifinitude/fidelidade; nilpotente nao nulo e canto ortogonal derivados do par Weyl e transportados pela fibre injetiva, sem premissa final de tipo II ou de canto.'),
            dict(statute='REAL', text='No dominio coerente regular do mesmo Fock, aniquilacao pontual integra por Bochner para a aniquilacao fisica normalizada. A forma Wick de quatro termos e sua contracao local igualam o tensor calibrado, mantendo A:RemainingModularCoreInput explicito. Nenhum campo pontual limitado global foi afirmado.'),
            dict(statute='OPEN', text='O split de tracos iguais nao esta provado nesta entrega: a R3 falhou por elaboracao; a R4 e candidata nao compilada. Falta ligar esse split, a extensao ciclica e o consumidor completo. R7/R8 integrais e R3/R4/R5/R10 permanecem abertos.'),
            dict(statute='REAL', text='Errata ao lado do fluxo da revisao357: a segunda falha da CyclicR2 era ENNReal.mul_iSup na linha107, nao positive_dual_cancel. A R3 verde resolveu as duas conversoes; tentativa antiga preservada.'),
            dict(statute='REAL', text='Memoria de missao M0-M3 permanece aceita. Os oito alvos instalados foram reconferidos; protocolos CLI/MCP/AGENTS preservados. Fluxos terminais foram retirados da fila ativa sem apagar os recibos. Economia historica medida em caracteres, nao tokens faturados; clientes precisam sincronizar.'),
        ],
        remaining='R7 split/PF e montagem do consumidor; R8 fornecedor conjunto sob A; R4/R5 relogio/espectro fisico e dispositivo; R3/R10 rito e revisao. Nenhum criterio integral reduzido.',
        next_action=next_action,
        extra_evidence=[str(split), str(OUT / 'takesaki_fock/CanonicalFockNormalizedSplitR4.lean'),
                        str(flow_receipt), str(project_receipt)],
    )
    new(target, config)
    print(json.dumps(dict(config=pin(target), revision=result['revision'],
                          unresolved_handles=0, components=6, expected_axiom_reports=52), ensure_ascii=False))


if __name__ == '__main__':
    main()
