"""Record this unit's completed material stage in its own ACOM context."""
from pathlib import Path
import json,hashlib,subprocess,os
ROOT=Path(r'C:\IALD\Central de Patentes')
W=ROOT/'work/rede_quantica_20261013'
O=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
PY=r'C:\Python314\python.exe'
def pin(p): return {'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,x):
    b=json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8');p=O/n;t=p.with_name(p.name+'.tmp')
    if p.exists():raise FileExistsError(p)
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.rename(t,p)
ref=str(W/'ACOM_REFERENCE.json')
q={'operation':'transition','reference':ref,'expected_revision':0,'event_id':'f1-rede-stage1-20261013','actor':{'id':'codex-gerente-tgl','kind':'agent'},'changes':{'records':[
 {'id':'sources-contract-r1','kind':'candidate','statute':'DECLARADO','text':'Contrato científico conectado com dez blocos N0–N9 a partir dos artigos e dispositivos do operador. Revisão independente exige V unitário e entrelaçamento Poincare completo/localização; T modular positivo. R2 incorporará essas obrigações; R1 preservada.', 'sources':[pin(O/'CONTRATO_REDE_R1.json'),pin(O/'review_contract/REVIEW_CONTRACT_R1.json')]},
 {'id':'light-ray-real-r1','kind':'fact','statute':'REAL','text':'Rede concreta de semirretas K_a=U(a)K_0 construída, isotonia, covariâncias por translação/dilatação e não vacuidade. Build e recompilação independente EXIT0, só trio. Não é rede4D.', 'sources':[pin(O/'light_ray/RESULTADO_LIGHT_RAY_R1.json'),pin(O/'review_light_ray/REVIEW_LIGHT_RAY_R1.json')]},
 {'id':'fubini-real-r1','kind':'fact','statute':'REAL','text':'Ponte FubiniL2 vetorial construída e especializada ao H1 original; norma, linearidade, sobrejetividade, seções AE, Fourier parcial e entrelaçamento B0 provados. Build e revisão independente EXIT0, trio. Símbolo sigma=4*pi^2*xi; ainda não é o modular de K(W) construído.', 'sources':[pin(O/'fubini/DELIVERY_R1.json'),pin(O/'review_fubini/20261013T213537_597067Z/REVIEW_RESULT.json')]},
 {'id':'device-real-r1','kind':'fact','statute':'REAL','text':'Modelo 2x2x2 de H/salto do Supercondutor pré-registrado: 142 verificações aprovadas e reproduzidas. Geometria27sítios apenas documental; parâmetros de engenharia INPUT. Nenhum dado observado, hardware, 5sigma ou rede4D medido.', 'sources':[pin(O/'finite_device/RESULTADO_DEVICE_R1.json'),pin(O/'review_device_r2/REVIEW_DEVICE_R1.json')]},
 {'id':'deepseek-return-r1','kind':'candidate','statute':'DECLARADO','text':'Chamada única especificamente autorizada retornou; 43961caracteres, revisão científica local em curso. Receber resposta não equivale a prova. Coordenadora concluiu transporte no mesmo job.', 'sources':[pin(O/'provider/SOURCE_CUSTODY_R1.json'),pin(ROOT/'work/rede_transport_20261013/DELIVERY_R1.json')]},
 {'id':'modular-wedge-open-r1','kind':'pending','statute':'OPEN','text':'Construção de J, T positivo, S=JT, Delta=S†S e K(W_R) em andamento no sandbox; representação completa4D, ponte do refinamento do dispositivo, Fock/Maxwell e H3 não fechados por estas peças.', 'sources':[pin(O/'CONTRATO_REDE_R1.json')]}
], 'flow':{'phase':'positive_modular_wedge_construction','next_action':'Concluir e revisar J/T/S no espaço canônico; incorporar revisão remota e local numa R2 aditiva; entregar por quadro/mapa com alcance explícito.', 'handles':[{'unit':'F1.REDE','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat'}]}}}
save('ACOM_STAGE_1_REQUEST.json',q)
for n,payload in [('ACOM_STAGE_1_RECEIPT.json',q),('ACOM_STAGE_1_VERIFY.json',{'operation':'verify','reference':ref})]:
    if (O/n).exists(): raise FileExistsError(n)
    cp=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
    save(n,{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(cp.stdout+cp.stderr)
    x=json.loads(cp.stdout)
    print(json.dumps({'receipt':n,'ok':x.get('ok'),'revision':x.get('receipt',x.get('result',{})).get('revision')},ensure_ascii=False))
