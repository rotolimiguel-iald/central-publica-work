"""Resume after the map's lexical title refusal; preserve the failed receipt."""
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=out
mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',out/'MAP_ENTRY_PROGRESS_R1A.json','--quem',WHO+' / F1.FECHO_20261015'],'MAP_RECEIPT_PROGRESS_R1A.json')
board=reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',out/'PROGRESS_R1.json','--nota','Progresso parcial verificado; escopo R1-R10 permanece.16fontes reutilizadas e18declaracoes quadráticas; memória4superfícies com backup sob845.'],'BOARD_PROGRESS_R1.json')
acom=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_PROGRESS_RECEIPT_R1.json',json.loads((out/'ACOM_PROGRESS_REQUEST_R1.json').read_bytes()))
print(json.dumps({'map':mapped,'board':board,'acom_ok':acom.get('ok')},ensure_ascii=False))
