"""Create and claim the explicitly requested formal proof unit."""
import json, subprocess
from diary_r1 import ROOT,PY,CLI,WHO,new

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA.P1'
BOOT=ROOT/'work/cunhagem_regra_20261014/CADASTRO_PROVA.json'

def call(args):
    cp=subprocess.run([PY,'-B','-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8',check=True)
    return json.loads(cp.stdout)

parent=call([CLI,'ver','F1.REGRA'])
new(BOOT,[{'id':'F1.REGRA.P1','frente':parent['frente'],
    'titulo':'Prova do contrato da regra, satisfação e figura da verdade',
    'status':'PROPOSTA','dono':WHO,
    'criterio':'Enunciado tipado que distingue definição e teoremas; exemplo não vazio e controles negativos; Lean4.31 sandbox exit0, axiomas só trio e zero sorry; revisão independente; fontes e verbatim por hash.',
    'fonte':'Pedido humano direto nesta conversa: Exatamente isso, agora faça a prova (14/10/2026).',
    'dependencias':['F1.REGRA']}])
created=call([CLI,'nova','--json',BOOT,'--quem',WHO])
claimed=call([CLI,'reivindicar','F1.REGRA.P1','--quem',WHO,'--nota','Prova autorizada pelo operador, sandbox apenas. Memorias ao entregar: DIARIO_CONSTRUCAO_QG.md, TGL_ATLAS.md, TGL_INDICE_VIVO.md, AVISO_GERENCIA.md e ACOM propria; backup e append. Sem kernel canonico, Bancada, um.py ou gate.'])
OUT.mkdir()
new(OUT/'CLAIM_RECEIPT.json',{'creation':created,'claim':claimed})
for label,args in [('NOS_VIVO',[r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.REGRA.P1']),('MAPA',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','conceitual.regra.negatividade_juridica'])]:
    cp=subprocess.run([PY,'-B','-X','utf8',*args],capture_output=True,text=True,encoding='utf-8')
    new(OUT/(label+'.json'),{'command':args,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
print(json.dumps({'created':created,'claim':claimed,'out':str(OUT)},ensure_ascii=False))
