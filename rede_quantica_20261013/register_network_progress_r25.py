"""Register R25 once; each receipt is exclusive and immutable."""
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg
out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST = out
mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', out/'MAP_ENTRY_PROGRESS_R25.json',
    '--quem', WHO+' / F1.FECHO_20261015'], 'MAP_RECEIPT_PROGRESS_R25.json')
board = reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
    '--evidencia', out/'PROGRESS_R25.json', '--nota',
    'Densidade física Maxwell e pontes da ação direita do Tomita:14 módulos44 prints; duas revisões independentes de fontes. Tracialidade e carga ainda consumidoras. Base v393, candidata v394. Memórias sob reivindicação845; R1-R10 preservados.'], 'BOARD_PROGRESS_R25.json')
acom = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_PROGRESS_RECEIPT_R25.json',
    json.loads((out/'ACOM_PROGRESS_REQUEST_R25.json').read_bytes()))
print(json.dumps({'map': mapped, 'board': board, 'acom_ok': acom.get('ok')}, ensure_ascii=False))
