from pathlib import Path
import json,os
R=Path(r'C:\IALD\Central de Patentes');W=R/'work/rede_quantica_20261013';O=R/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
def new(p,b):
 if p.exists():raise FileExistsError(p)
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.rename(t,p)
code=(W/'register_delivery_r1a.py').read_text(encoding='utf-8')
code=code.replace("str(OUT/'MEMORY_DELIVERY_R1.json'),'--nota'", "str(OUT/'MEMORY_DELIVERY_R1.json'),str(OUT/'MEMORY_CORRECTION_R1.json'),str(OUT/'NOTA_REGISTRO_R1.json'),'--nota'")
code=code.replace("source(OUT/'MEMORY_DELIVERY_R1.json'),source(OUT/'RESULTADO_ENTREGA_R1.json')", "source(OUT/'MEMORY_DELIVERY_R1.json'),source(OUT/'MEMORY_CORRECTION_R1.json'),source(OUT/'RESULTADO_ENTREGA_R1.json')")
new(W/'register_delivery_r1b.py',code.encode())
new(O/'NOTIFICATION_REJECTED_R1.json',(json.dumps({'action':'send_message_to_thread','destination_thread':'01a0ce2b-8c2f-71b0-a9a8-91b17715a569','status':'REJECTED_NOT_SENT','reason':'A mensagem divulga detalhes internos da entrega a outra thread, mas a autorização visível para atualizar memória não autoriza claramente enviar esse relatório específico ao destino.','handling':'No workaround or retry. User informed. Existing authorized board/map/memory delivery proceeds independently.'},ensure_ascii=False,indent=2)+'\n').encode())
print('Prepared final registration wrapper; previous files preserved.')
