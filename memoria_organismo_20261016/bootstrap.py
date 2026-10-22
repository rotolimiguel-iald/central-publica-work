"""Register the new instruction; no adoption of another mission or production change."""
import json
import uuid
from mission_io import WORK, REFERENCE, ACTOR, pin, save, call, project

def main():
    if REFERENCE.exists():
        raise RuntimeError('Already initialized: recover the exact reference')
    source = WORK / 'OPERADOR_VERBATIM.txt'
    call('session_memory.py', {'operation': 'init', 'objective_file': str(source),
        'objective_sha256': pin(source)['sha256'], 'request_id': str(uuid.uuid4()),
        'scope': {'house': 'IALD', 'principal': 'luiz-antonio-rotoli-miguel'},
        'actor': ACTOR, 'write_reference': str(REFERENCE),
        'constraints': {'unit': 'F9.MEMORIA_ORGANISMO_20261016',
            'preserve_existing_data_and_capabilities': True, 'same_acom_core': True,
            'no_science_gate_credentials_trust_or_user_permission_changes': True,
            'independent_review_before_production_installation': True}}, 'init')
    raw, _ = call('session_memory.py', {'operation': 'project', 'reference': str(REFERENCE),
                                     'max_chars': 32000}, 'session_project')
    requirements = [
        {'id': 'I', 'criterion': 'Inventario dos consumidores reais e lacunas: app/JEV/chat/stream/workers, nativa, holografica, fila/provedores, sessoes/CLI/MCP e Bancada. Fontes/linhas/hashes e contrato comum preservando usuarios, casas, ciencia e legado.', 'depends_on': []},
        {'id': 'C', 'criterion': 'Ponte comum de atividade reutiliza MemoryStore/MissionController: identidade/revisao, requisitos, progresso, candidatos, delegacoes, retomada, parada e invalidacao; sem autoaprovacao de modelo nem segundo banco. Testes de concorrencia/falha/isolacao e baixo custo medido.', 'depends_on': ['I']},
        {'id': 'A', 'criterion': 'App/JEV/conversa/stream/ferramentas/workers usam a ponte em pontos reais de inicio, contexto, delegacao, retorno e conclusao; backend compartilhado web/iOS/Android preservado. Nao basta import ou documentacao. Testes dos caminhos reais em copia.', 'depends_on': ['C']},
        {'id': 'N', 'criterion': 'IALD nativa e memoria holografica integram a mesma memoria evolutiva, preservando mecanismos existentes, privacidade e dominios. Projecao/candidatos nao apagam originais; reinicio e retomada cruzada demonstrados.', 'depends_on': ['C']},
        {'id': 'Q', 'criterion': 'Fila cientifica/executores, CLI/MCP e consumidores da Bancada recebem/reconciliam a mesma identidade de atividade e estado atual nos pontos aplicaveis. IDs remotos incertos nao repetidos. Sem alterar calculo cientifico/gate; limites de processos antigos explicitos.', 'depends_on': ['C']},
        {'id': 'V', 'criterion': 'Revisao independente conjunta com testes de estado obsoleto, mudanca de meta, concorrencia, particao de usuario, retomada entre consumidores e PODA/Tetelestai; matriz completa de cobertura, sem promover artefato de modelo a verdade.', 'depends_on': ['A', 'N', 'Q']},
        {'id': 'D', 'criterion': 'Instalacao segura dos componentes proprios por hash e backup, sem perder conversas/trabalhos/estado; conferir processo efetivo, rollback e teste real apropriado. Matriz de disponibilidade app/nativa/holografica/fila/MCP/Bancada com limitacoes verificadas.', 'depends_on': ['V']},
        {'id': 'M', 'criterion': 'Protocolo/instrucoes/Atlas/diario/indice/mapa/quadro atualizados aditivamente sob reivindicacao; recibo final de todos os requisitos e desempenho; explicar decisao do dispositivo separadamente, sem impedir memoria.', 'depends_on': ['D']},
    ]
    save(WORK/'REQUIREMENTS_R1.json', requirements)
    call('mission_cli.py', {'operation': 'configure', 'reference': str(REFERENCE),
        'actor': ACTOR, 'expected_revision': raw['receipt']['revision'],
        'event_id': 'organism-memory-configure-r1', 'requirements': requirements,
        'sources': [pin(source), pin(WORK/'REQUIREMENTS_R1.json')]}, 'configure')
    current, _ = project()
    call('mission_cli.py', {'operation': 'claim', 'reference': str(REFERENCE), 'actor': ACTOR,
        'task_id': 'I', 'expected_revision': current['receipt']['revision'],
        'projection_sha256': current['projection_sha256'], 'event_id': 'organism-inventory-claim-r1',
        'lease_seconds': 14400}, 'claim_inventory')
    current, receipt = project()
    task = next(x for x in current['projection']['active'] if x['id'] == 'I')
    _, handoff = call('mission_cli.py', {'operation': 'handoff', 'reference': str(REFERENCE),
        'actor': ACTOR, 'task_id': 'I', 'lease_id': task['lease']['id'],
        'expected_revision': current['receipt']['revision'],
        'projection_sha256': current['projection_sha256'], 'max_chars': 125000}, 'inventory_handoff')
    save(WORK/'START.json', {'reference': pin(REFERENCE), 'project': pin(receipt),
        'handoff': pin(handoff), 'revision': current['receipt']['revision']})
    print(json.dumps({'reference': str(REFERENCE), 'handoff': str(handoff),
                      'revision': current['receipt']['revision']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
