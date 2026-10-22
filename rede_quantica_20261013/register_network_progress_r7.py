"""Register R7 once; immutable receipts identify each successful mutation."""
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=out
mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',out/'MAP_ENTRY_PROGRESS_R7.json','--quem',WHO+' / F1.FECHO_20261015'],'MAP_RECEIPT_PROGRESS_R7.json')
board=reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',out/'PROGRESS_R7.json','--nota','Parte polar, fluxo modular concreto, BW em H1, cunha nao abeliana, peso finito e Gamma_positive revistos; 24campos restantes explicitos. Main final em andamento; memoria4superficies sob845 e R1-R10 preservado.'],'BOARD_PROGRESS_R7.json')
acom=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_PROGRESS_RECEIPT_R7.json',json.loads((out/'ACOM_PROGRESS_REQUEST_R7.json').read_bytes()))
print(json.dumps({'map':mapped,'board':board,'acom_ok':acom.get('ok')},ensure_ascii=False))
