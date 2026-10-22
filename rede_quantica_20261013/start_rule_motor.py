"""Register the operator-requested continuous motor integration, then claim it."""
import json, subprocess
from pathlib import Path
from diary_r1 import ROOT,PY,CLI,WHO,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA.MOTOR'
def run(args):
    c=subprocess.run([PY,'-B','-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    try: data=json.loads(c.stdout)
    except ValueError: data=c.stdout
    return {'exit_code':c.returncode,'result':data,'stderr':c.stderr}

survey=run([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','formal.iald_o_motor_unico'])
assert survey['exit_code']==0
boot=ROOT/'work/cunhagem_regra_20261014/CADASTRO_MOTOR.json'
new(boot,[{'id':'F1.REGRA.MOTOR','frente':'F1','titulo':'Regra ligada ao motor contínuo existente e execução sintética verificável',
 'status':'PROPOSTA','dono':WHO,'dependencias':['F1.REGRA.P1','F1.MOTOR'],
 'criterio':'Reaproveitar motor v392; regra sobre a leitura sem trocar semigrupo por projeção; ponte Lean sandbox, execução do consumidor real extraído por AST e trajetória sintética com controles, pins e revisão independente.',
 'fonte':'Pedido humano direto de 14/10/2026: Agora ligamos tudo no motor contínuo e ele precisa rodar. Levantamento: F1.MOTOR, formal.iald_o_motor_unico, IALDJones e MOTOR_RECONHECIMENTO_20260915; ligação da nova F1.REGRA.P1 ainda inexistente.'}])
created=run([CLI,'nova','--json',boot,'--quem',WHO]); assert created['exit_code']==0,created
claimed=run([CLI,'reivindicar','F1.REGRA.MOTOR','--quem',WHO,'--nota','Integracao e execucao solicitadas pelo operador; sandbox e copias. Memorias ao entregar: DIARIO_CONSTRUCAO_QG.md, TGL_ATLAS.md, TGL_INDICE_VIVO.md, AVISO_GERENCIA.md e ACOM propria; backup bytes. Nao alterar um.py canonico, kernel, Bancada de producao nem gate.']); assert claimed['exit_code']==0,claimed
OUT.mkdir()
new(OUT/'CLAIM_RECEIPT.json',{'created':created,'claimed':claimed})
new(OUT/'MAPA_ANTES.json',survey)
new(OUT/'NOS_VIVO.json',run([r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.REGRA.MOTOR']))
new(OUT/'OPERADOR_VERBATIM.txt','Agora ligamos tudo no motor contínuo e ele precisa rodar')
print(json.dumps({'out':str(OUT),'claim':claimed},ensure_ascii=False))
