"""Record completion only after actual documentary acceptance."""
import hashlib,json
import task
p=task.project()
assert p['projection']['tetelestai'] is True
assert not p['projection']['active']
assert not p['projection']['unresolved_handles']
task.new('MISSION_COMPLETED_PROJECTION_R1.json',p)
artifacts=[task.W/x for x in ['OPERATOR_DOCUMENTAL_ACCEPT_R1.json','review/VERIFY_FINAL_REVIEW_R1.json','FINAL_DELIVERY_R1.json','LIVE_VALIDATION_R1.json','MISSION_COMPLETED_PROJECTION_R1.json']]
s=task.call({'operation':'project','reference':str(task.REF),'max_chars':100000},False)
r=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':s['receipt']['revision'],'event_id':'v395-final-documental-completion','changes':{'records':[{'id':'v395-final-documental-completion','kind':'fact','statute':'REAL','text':'Entrega operacional v395 concluída após teste autenticado, revisão independente e aceite documental explicitamente autorizado pelo operador. Todos os requisitos satisfeitos; sem handles pendentes. O teste de login anteriormente pendente foi concluído. Quadro ENTREGUE evento1109; aceite gerencial do quadro é distinto. Nenhuma alteração de ciência, kernel ou gate.','sources':[{'kind':'artifact','ref':str(a),'sha256':hashlib.sha256(a.read_bytes()).hexdigest()} for a in artifacts]}],'flow':{'phase':'completed','next_action':'Entrega operacional concluída. Não repetir instalação, testes ou chamadas encerradas.'}}},False)
task.new('ACOM_FINAL_RECEIPT_R1.json',r)
final=task.project()
assert final['projection']['tetelestai'] is True
print(json.dumps({'status':'COMPLETED','revision':final['receipt']['revision'],'tetelestai':True}))
