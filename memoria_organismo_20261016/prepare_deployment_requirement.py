"""Track preparatory deployment work separately from production activation."""
import json
from mission_io import WORK, REFERENCE, ACTOR, call, pin, project, save
from advance import action


def main():
    current, _ = project()
    if not any(t['id'] == 'P' for t in current['projection']['active'] + current['projection']['settled']):
        request = {
            'operation': 'extend', 'reference': str(REFERENCE), 'actor': ACTOR,
            'expected_revision': current['receipt']['revision'],
            'projection_sha256': current['projection_sha256'],
            'event_id': 'organism-deployment-preparation-requirement-r1',
            'requirements': [{'id': 'P', 'depends_on': ['C'], 'criterion':
                'Preparar instalador em staging com allowlist, pinos, baselines, backups de bytes, '
                'CAS de destinos, reversao e verificacao de carregamento; testar falha e troca '
                'em copia, sem ativacao. Revisao independente do plano antes de D.'}],
            'reason': 'Decomposicao operacional da instalacao ja autorizada: preparar e testar '
                      'o instalador enquanto A/N/Q constroem adaptadores, preservando D apos V.',
            'sources': [pin(WORK / 'OPERADOR_VERBATIM.txt'), pin(WORK / 'CONTRATO_INTEGRACAO_R1.txt')],
        }
        call('mission_cli.py', request, 'extend_P')
    current, _ = project()
    task = next(t for t in current['projection']['active'] + current['projection']['settled'] if t['id'] == 'P')
    if task['status'] == 'open':
        action('claim', 'P', {'lease_seconds': 43200})
    current, receipt = project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'P')
    checked, path = call('mission_cli.py', {
        'operation': 'check', 'reference': str(REFERENCE), 'actor': ACTOR,
        'task_id': 'P', 'lease_id': task['lease']['id'],
        'expected_revision': current['receipt']['revision'],
        'projection_sha256': current['projection_sha256']}, 'check_P')
    print(json.dumps({'revision': current['receipt']['revision'], 'lease': task['lease'],
                      'check_receipt': str(path)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
