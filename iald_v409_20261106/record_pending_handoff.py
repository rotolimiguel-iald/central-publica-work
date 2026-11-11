"""Publish a partial, local handoff with no claim of activation."""
import hashlib
import json
from pathlib import Path
import task

W = Path(__file__).resolve().parent
report = W / 'PREPARATION_REVIEWED_R1.json'
data = json.loads(report.read_bytes())
assert data['status'] == 'PREPARED_REVIEWED_AWAITING_V409_OPERATOR_GATE'
assert not (W / 'deployment.json').exists()
result = {
    'ordem': 'ORDEM_009', 'estado': 'parcial', 'autor': task.OWNER,
    'resumo': 'App/JEV e snapshot F0.3 v409 preparados e revisados; v408 permanece instalada. Nenhuma ativacao ou reinicio executados.',
    'arquivos': [{'path': str(report), 'sha256': hashlib.sha256(report.read_bytes()).hexdigest()}, *data['evidence']],
    'o_que_falta': ['Aceite humano especifico v409: reinicio apenas do filho web 8082 e escrita/ativacao na pasta protegida F0.3; pergunta pendente no chat.',
                    'Conferir snapshot nos caminhos finais antes de CAS, implantar em janela ociosa e revisar/aceitar deploy antes de verify.',
                    'Verificacao instalada, Torre e recibo final. UI nao validada: Computer Use interrompido por URL nao identificavel neste turno.'],
    'referencia': str(task.REF), 'unidade': task.UNIT,
    'cientifico': 'Fontes read-only; nenhuma execucao de um.py/Lean ou alteracao de gate.'
}
target = Path(r'C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\009_RESULTADO.json')
raw = json.dumps(result, ensure_ascii=False, indent=2).encode()
with target.open('xb') as stream:
    stream.write(raw)
assert target.read_bytes() == raw
route = {
    'tipo': 'ROTA', 'rota_id': 'app.release.v409', 'dominio': 'APP',
    'titulo': 'Release v409 preparada e revisada; ativacao pendente do operador',
    'pergunta': 'Integrar v409 preservando a memoria e as correcoes atuais do app?',
    'dados': ['Fontes v409 custodiadas e publicadas verificadas; baseline atual v408'],
    'metodo': 'Construtor e revisor distintos; P2 v408/v409; poda exata de literais inacessiveis no dicionario; seis COUNTs publicos; revisao integral da fila.',
    'resultado': '1788 destinos de dados, 483 topicos; 174 literais orfaos eliminados sem mudar a reconstrucao. 13 pinos operacionais preservados. Runtime continua v408.',
    'veredito': 'PREPARED_REVIEWED_AWAITING_OPERATOR', 'estatuto': 'REAL',
    'status': 'EXAMINADA', 'olhou_dados': False,
    'defeito': 'Ativacao ainda nao executada. Sem ensaio de chat ou aparelho nesta preparacao.',
    'nao_refazer': 'Nao repetir contagens nem construir novamente. Usar os planos revisados e a referencia desta missao.',
    'proximo_passo': result['o_que_falta'][0], 'onde': str(W),
    'artefatos': [str(report), str(W / 'validation/review_final.json'), str(target)],
    'refs': ['app.release.v408'], 'nota': 'Registro parcial, nao equivale a entrega instalada.'
}
task.new('ROUTE_PREPARED_R1.json', route)
task.new('TUNNEL_PARTIAL_RECEIPT_R1.json', {'path': str(target), 'sha256': hashlib.sha256(raw).hexdigest()})
print(json.dumps({'status': 'PARTIAL_RECORDED', 'path': str(target)}))
