"""Register R33 once; each receipt is exclusive and immutable."""
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg
out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST = out
mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', out/'MAP_ENTRY_PROGRESS_R33.json',
    '--quem', WHO+' / F1.FECHO_20261015'], 'MAP_RECEIPT_PROGRESS_R33.json')
board = reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
    '--evidencia', out/'PROGRESS_R33.json', '--nota',
    'Decomposição polar S=J raiz no mesmo Fock GNS, igualdade dos domínios, raiz auto-adjunta injetiva de imagem densa e extensão aos fechos reais.2 módulos,10 prints,619 pinos. Revisão própria; sem auditoria independente. Base v393/candidata v394; reivindicação881; R1-R10 preservados.'], 'BOARD_PROGRESS_R33.json')
acom = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_PROGRESS_RECEIPT_R33.json',
    json.loads((out/'ACOM_PROGRESS_REQUEST_R33.json').read_bytes()))
print(json.dumps({'map': mapped, 'board': board, 'acom_ok': acom.get('ok')}, ensure_ascii=False))
