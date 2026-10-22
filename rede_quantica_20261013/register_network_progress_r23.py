"""Register R23 once; each receipt is exclusive and immutable."""
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg
out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST = out
mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', out/'MAP_ENTRY_PROGRESS_R23.json',
    '--quem', WHO+' / F1.FECHO_20261015'], 'MAP_RECEIPT_PROGRESS_R23.json')
board = reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
    '--evidencia', out/'PROGRESS_R23.json', '--nota',
    'Boost longitudinal Maxwell e aproximação finita:79 locais e20 prints no trio, revisões de fontes e custódia. Densidade e tracialidade concreta ainda abertas. Base v393. Quatro memórias sob reivindicação845; R1-R10 preservados.'], 'BOARD_PROGRESS_R23.json')
acom = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_PROGRESS_RECEIPT_R23.json',
    json.loads((out/'ACOM_PROGRESS_REQUEST_R23.json').read_bytes()))
print(json.dumps({'map': mapped, 'board': board, 'acom_ok': acom.get('ok')}, ensure_ascii=False))
