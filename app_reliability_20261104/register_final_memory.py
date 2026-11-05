"""Append the final operational outcome to this mission and manager inbox."""
import hashlib,json
from datetime import datetime,timezone
from task import W,REF,OWNER,call,new,project

def pin(name):
    p=W/name
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

final=pin('FINAL_DELIVERY.json')
p=project()
if not p['projection']['tetelestai']:
    raise RuntimeError('Independent delivery acceptance is still pending')
source={'kind':'artifact','ref':final['path'],'sha256':final['sha256']}
records=[
 {'id':'reliability-final-live-verified','kind':'fact','statute':'REAL','supersedes':'reliability-backend-installed','sources':[source],
  'text':'Complemento ao progresso: nova credencial OpenAI ativa, validade Nunca observada, ACL restrita e HTTP200 em teste mínimo. Backend recarregado. Dois turnos web autenticados, ChatGPT manual e AUTO/MiMo, responderam autoria e v407; recarga preservou respostas e envio ficou habilitado. Recuperação de recusa inicial OpenAI foi testada offline, não induzida live. Cinco arquivos instalados, 1782 pinos científicos preservados. Nenhuma build nova necessária para esta correção de servidor; aparelhos/lojas não reinspecionados. v408 final não observada. Registro interno de prazo atualizado. Limite da observação AX documentado sem valor de credencial no recibo.'},
 {'id':'operator-key-duration-fulfilled','kind':'fact','statute':'REAL','supersedes':'operator-key-duration','sources':[source],
  'text':'Preferência de duração máxima cumprida: provedor mostrou Active / Nunca; criação e entrada feitas pelo operador e teste de API passou. Sem promessa contra revogação, falta de crédito ou indisponibilidade externa.'}]
r=call({'operation':'transition','reference':str(REF),'expected_revision':p['receipt']['revision'],
        'actor':{'id':OWNER,'kind':'agent'},'event_id':'app-reliability-final-live-memory',
        'changes':{'records':records,'flow':{'phase':'delivered','next_action':'No pending execution. Reuse final receipts; future v408 activation requires verified final release.'}}},False)
new('FINAL_MEMORY_RECEIPT.json',r)
sources=[pin(x) for x in ['FINAL_DELIVERY.json','LIVE_VALIDATION.json','review/FINAL_DELIVERY_REVIEW.json','FINAL_DELIVERY_ACCEPT.json','FINAL_MEMORY_RECEIPT.json']]
text='''---
quem: codex-app-01a094df
casa: IALD Nativa
tipo: project
estatuto: REAL
alvo_sugerido: novo:app-reliability-20261104
fontes:
'''+''.join('  - '+x['path']+'  sha256:'+x['sha256']+'\n' for x in sources)+'''---
# App: autenticação recuperada e continuidade verificada

Complemento ao depósito 20261104_app_reliability_pending_credential.md, preservado. A pendência de chave e teste live foi resolvida. OpenAI: Active / Nunca, apenas Chat completions, armazenamento dedicado protegido para usuário e SYSTEM. Teste mínimo HTTP200, 14 tokens; não é o custo total do chat. Registro de prazo atualizado somente na administração interna. A observação AX de campo oculto foi documentada sem reproduzir o valor; não afirmar ausência universal de exposição.

Cinco arquivos backend revisados instalados, somente filho web reiniciado sob supervisor existente, HTTP200. No AUTO textual público, uma recusa inicial inequívoca OpenAI pode provocar uma nova escolha JEV entre executores elegíveis, conservando contexto, direitos, consentimentos, tarefa e carteira. Não repetir após envio incerto, timeout ou saída parcial. Não é fallback geral de todos os provedores ou do ramo privado. Falha operacional não vira conteúdo de resposta da IA no fluxo AUTO.

Dois turnos reais pela web autenticada: ChatGPT manual respondeu autoria/v407 e AUTO escolheu MiMo para continuidade. Recarga preservou respostas; envio habilitado ao digitar. Recuperação após recusa foi verificada offline, não provocada em produção. Não é benchmark nem certificação de exatidão geral.

Ciência v407 preservada: 1782/1782 arquivos; v408 final selada/publicada não observada nas fontes conferidas. Nenhum um.py/Lean executado ou gate alterado. Cliente não mudou: backend compartilhado web/iOS/Android ativo, sem necessidade de nova build. Lojas, instalação física e Google Play não verificados nesta entrega. Revisão independente dos quatro requisitos concluída; promoção de memória e auditoria do quadro continuam atos da gerência.

Referência própria: C:/IALD/Central de Patentes/work/app_reliability_20261104/SESSION_REFERENCE.json.
'''
new('MEMORY_FINAL_DEPOSIT.md',text.encode('utf-8'))
route={'tipo':'ROTA','rota_id':'infra.app.reliability_20261104','dominio':'INFRA_APP_IALD',
       'titulo':'Autenticação OpenAI renovada e recuperação AUTO delimitada',
       'pergunta':'Como recuperar a recusa inicial de credencial sem perder contexto nem repetir execução incerta?',
       'dados':['Recibos HTTP e testes sintéticos de software; sem dados físicos'],
       'metodo':'Diagnóstico e revisão independente; testes offline e dois turnos públicos autenticados',
       'resultado':'Cinco destinos instalados; 1782 arquivos científicos preservados; HTTP200 e dois turnos recebidos após renovação',
       'veredito':'INSTALLED_AUTHENTICATED_CHAT_VERIFIED','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
       'defeito':'Recuperação de recusa testada offline; sem falha induzida live ou inspeção física de aparelho',
       'nao_refazer':'Não repetir chamadas concluídas nem renovar novamente a credencial ativa sem fato novo',
       'proximo_passo':'v408 depende da custódia final; monitorar por fluxo existente, sem novo job nesta entrega',
       'onde':'Backend compartilhado IALD','artefatos':[final['path']], 'refs':[],
       'nota':'Registro retrospectivo; não é pré-registro de ciência. Quadro e missão próprios.'}
new('ROUTE_FINAL.json',route)
print(json.dumps({'memory_revision':r['revision'],'deposit':pin('MEMORY_FINAL_DEPOSIT.md')},ensure_ascii=False))
