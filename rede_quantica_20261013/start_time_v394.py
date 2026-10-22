"""Create and claim the operator-authorized isolated v394 construction."""
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin
import register_rule_tetelestai as reg

UNIT='F1.TEMPO.V394'
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT
ORDER='Realize tudo que vc falou que ainda falta, para construir a versão394 e não mexer na existente faça uma cópia'
reg.DEST=OUT
boot=WORK/'CADASTRO_TEMPO_V394.json'
new(boot,[{'id':UNIT,'frente':'F1','titulo':'Candidata v394 isolada: tempo, frequencia, objeto gravitacional e regra','dono':WHO,'status':'PROPOSTA','dependencias':['F1.TEMPO.LEITURA_20261015','F1.REGRA.MOTOR'],'criterio':'Formalizar composicao R9 em Lean sandbox (exit0, trio, zero sorry), ligar os parametros pelos contratos fisicos existentes com verificacao dimensional, integrar e executar copia isolada v394 com controles e revisao independente. Conservar originais byte a byte; sem publicacao, instalacao ou gate. Nao reduzir o objetivo a um novo handoff documental.','fonte':ORDER+' Levantamento de 15/10: mapa1122 traz entrega documental R1-R9; nenhuma candidata v394 ou composicao Lean conjunta encontrada no quadro/Nos Vivo.'}])
created=reg.call([CLI,'nova','--json',boot,'--quem',WHO])
claimed=reg.call([CLI,'reivindicar',UNIT,'--quem',WHO,'--nota','Ordem direta para construir e testar copia v394. Somente sandbox novo no tunel; memoria DIARIO_CONSTRUCAO_QG.md, TGL_ATLAS.md, TGL_INDICE_VIVO.md, AVISO_GERENCIA.md e ACOM propria com backups de bytes. Originais um.py/kernel/selos, Bancada de producao e gate preservados.'])
new(OUT/'CLAIM_RECEIPT.json',{'created':created,'claimed':claimed})
new(OUT/'OPERADOR_VERBATIM.txt',ORDER)
reg.call(['C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_VIVO.json')
reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','v394'],'MAPA_ANTES.json')
reg.call([CLI,'anotar','--quem',WHO,'--tipo','AVISO_CLAUDE','--unidade',UNIT,'--dados',json.dumps({'destinatario':'claude-c1','ordem':ORDER,'escopo':'Copia isolada da v393 para candidata v394, por nova ordem humana direta; nenhuma alteracao do original. Formalizacao R9, contratos fisicos, integracao e testes em andamento.','pasta':str(OUT)},ensure_ascii=False)],'NOTICE_START.json')
print(json.dumps({'unit':UNIT,'out':str(OUT),'claim':claimed},ensure_ascii=False))
