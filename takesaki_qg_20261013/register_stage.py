"""Register the already measured stage through official board/map/ACOM CLIs."""
from pathlib import Path
import hashlib, json, subprocess, sys

ROOT = Path(r'C:\IALD\Central de Patentes')
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TAKESAKI'
WORK = ROOT / 'work/takesaki_qg_20261013'
PY = r'C:\Python314\python.exe'

def pin(p):
    return {'kind': 'artifact', 'ref': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def save(name, value):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

def run(name, args, payload=None):
    # Preflight prevents accidental repeated mutation when this wrapper is rerun.
    if (OUT / name).exists():
        raise FileExistsError(OUT / name)
    cp = subprocess.run([PY, '-B', '-X', 'utf8', *args], input=None if payload is None else json.dumps(payload, ensure_ascii=False), text=True, encoding='utf-8', capture_output=True)
    receipt = {'command': [PY, '-B', '-X', 'utf8', *args], 'exit_code': cp.returncode, 'stdout': cp.stdout, 'stderr': cp.stderr}
    save(name, receipt)
    if cp.returncode:
        print(json.dumps(receipt, ensure_ascii=False))
        sys.exit(cp.returncode)
    print(json.dumps({'receipt': name, 'exit_code': cp.returncode, 'stdout': cp.stdout[:1400]}, ensure_ascii=False))
    return cp

save('NOTA_TRANSCRICAO_REVISAO_R1.json', {
    'author': 'codex-gerente-tgl',
    'clarifies': str(OUT / 'REVISAO_LOCAL_INDEPENDENTE_R1.json'),
    'text': 'O campo report_verbatim da R1 contém uma síntese fiel das mensagens, não uma reprodução literal integral. Leia-o como paráfrase da revisão. A R1 já identifica o caráter compacto e a ausência de aprovação c1. O resultado técnico da revisão não muda.'
})
run('MAP_REGISTER_ETAPA_R1.json', [r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', str(OUT / 'MAP_ENTRY_ETAPA_R1.json'), '--quem', 'codex-gerente-tgl / F1.TAKESAKI'])
run('BOARD_REGISTER_ETAPA_R1.json', [r'C:\IALD\PROGRAMA_IALD\iald.py', 'avancar', 'F1.TAKESAKI', '--quem', 'codex-gerente-tgl', '--status', 'EM_CURSO', '--evidencia', str(OUT / 'RESULTADO_ETAPA_R1.json'), str(OUT / 'NOTA_TRANSCRICAO_REVISAO_R1.json'), '--nota', 'Primeira etapa: contrato completado, cinco lemas Lean/trio/zero sorry, derivacao local revista; integracao do suplemento na fila em curso, sem envio ao Kimi comprovado neste recibo.'])

request = {
    'operation': 'transition', 'reference': str(WORK / 'ACOM_REFERENCE.json'), 'expected_revision': 0,
    'event_id': 'f1-takesaki-etapa-r1-20261013', 'actor': {'id': 'codex-gerente-tgl', 'kind': 'agent'},
    'changes': {
        'records': [
            {'id': 'local-build-r1', 'kind': 'fact', 'statute': 'REAL', 'text': 'Cinco teoremas locais compilados: EXIT0, apenas trio, zero sorry; os14pinos do recibo foram conferidos. O alcance é algébrico condicional, sem construção geral de produto cruzado.', 'sources': [pin(OUT / 'VERIFICACAO_PINS_LOCAL_R1.json'), pin(OUT / 'local_lemmas/RESULTADO_LOCAL_R1.json')]},
            {'id': 'derivation-r1', 'kind': 'candidate', 'statute': 'DECLARADO', 'text': 'Derivação textual de Takesaki por peso dual, densidade e regularizadores; revisão independente de leitura sem defeito material. Candidata local sobre resultado KNOWN, não aprovação c1 nem teorema geral Lean.', 'sources': [pin(OUT / 'DERIVACAO_LOCAL_R1.md'), pin(OUT / 'REVISAO_LOCAL_INDEPENDENTE_R1.json'), pin(OUT / 'NOTA_TRANSCRICAO_REVISAO_R1.json')]},
            {'id': 'queue-pending-r1', 'kind': 'pending', 'statute': 'OPEN', 'text': 'Mesmo request/job conservados. Contrato suplementar completo, preview Kimi aprovado; API precisa integrar suplemento/outbox/consumidores preservando âncora. Coordenação instruída a concluir; nenhuma resposta de provedor comprovada nesta etapa.', 'sources': [pin(OUT / 'QUEUE_STATUS_ETAPA_R1.json'), pin(OUT / 'CONTRATO_TAKESAKI_R1.json')]},
            {'id': 'index-incident-r1', 'kind': 'fact', 'statute': 'REAL', 'text': 'construir.py --help regenerou inesperadamente o índice. Banco com backup do construtor; resumo derivado sem backup prévio demonstrado. Segundo acionamento foi relatado pela coordenação; sem atribuir horários sem evidência.', 'sources': [pin(OUT / 'RECIBO_PROCESSO_INDICE_R1.json')]},
            {'id': 'stack-proposal-r1', 'kind': 'candidate', 'statute': 'DECLARADO', 'text': 'Prioridades propostas: proveniência por afirmação/versão, projeção com repetições removidas preservando originais/ocorrências, medição de recuperação, retenção e custo. ACOMv2 já implantada, não refazer reparo.', 'sources': [pin(OUT / 'RELATORIO_ETAPA_R1.md')]}
        ],
        'flow': {'phase': 'local_stage_recorded_queue_integration_in_progress', 'next_action': 'Acompanhar integração coordenada do suplemento; despachar uma única chamada pelo mesmo job e conferir candidato retornado. Não declarar conclusão geral de Takesaki.', 'handles': [{'id': 'takesaki-job', 'request_id': '9fec8d26-d3b7-4262-b4e6-e3a5aa450760', 'job_id': 'ff9a08c5-5b3a-4b17-b0ea-319d59a978a2', 'coordination_thread_id': '01a0ce2b-8c2f-71b0-a9a8-91b17715a569', 'unit': 'F1.TAKESAKI'}]}
    }
}
save('ACOM_TRANSITION_REQUEST_R1.json', request)
run('ACOM_TRANSITION_RECEIPT_R1.json', [r'C:\IALD\MEMORIA_IALD\session_memory.py'], request)
run('ACOM_VERIFY_R1.json', [r'C:\IALD\MEMORIA_IALD\session_memory.py'], {'operation': 'verify', 'reference': str(WORK / 'ACOM_REFERENCE.json')})
