"""Register R8 once; immutable receipts identify each successful mutation."""
import json
from diary_r1 import ROOT,CLI,WHO
import register_rule_tetelestai as reg
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=out
mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',out/'MAP_ENTRY_PROGRESS_R8.json','--quem',WHO+' / F1.FECHO_20261015'],'MAP_RECEIPT_PROGRESS_R8.json')
board=reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',out/'PROGRESS_R8.json','--nota','KMS concreta auditada85decl; Gamma_no_fixed122; BW setorespositivos e GNS real revistos. Main EXIT0,27/28controles,recusa DESY3offline e deltas para conciliar. Memoria4superficies sob845; R1-R10 preservado.'],'BOARD_PROGRESS_R8.json')
acom=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_PROGRESS_RECEIPT_R8.json',json.loads((out/'ACOM_PROGRESS_REQUEST_R8.json').read_bytes()))
print(json.dumps({'map':mapped,'board':board,'acom_ok':acom.get('ok')},ensure_ascii=False))
