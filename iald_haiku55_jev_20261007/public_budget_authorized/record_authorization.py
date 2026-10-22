"""Append the operator's cost authorization and verified public budget activation."""
from pathlib import Path
import json,sys
w=Path(__file__).resolve().parent;sys.path.insert(0,str(w))
from transaction import backup,atomic,write_evidence
assert json.loads((w/'restart.json').read_bytes())['status']=='PASS'
assert json.loads((w/'budget_validation.json').read_bytes())['status']=='PASS'
c=Path(r'C:\IALD\Central de Patentes');r=Path(r'C:\IALD\projetos_pyhton\IALD')
paths=[Path(r'C:\Users\rotol\.codex\AGENTS.md'),r/'CLAUDE.md',c/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',r/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',c/'memory/TGL_ATLAS.md',c/'memory/TGL_INDICE_VIVO.md',Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md'),Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\app-iald-mobile.md')]
marker='<!-- IALD_UPDATE_COSTS_AUTHORIZED_20261007 -->'
body='''

## 07/10/2026 — Custos necessários às atualizações da IALD autorizados

<!-- IALD_UPDATE_COSTS_AUTHORIZED_20261007 -->

[INPUT — ordem permanente do operador] “Pode fazer tudo sempre que eu mandar atualizar e isso for necessário pode fazer, é o custo”. Contexto: parametrização JEV/Haiku 5.5 e orçamento público anteriormente pendente. Ao receber pedido de atualização da IALD, executar as etapas necessárias, incluindo uso/testes pagos e ativação de configurações de custo já acordadas, sem pedir novamente confirmação rotineira desse custo. Manter uso proporcional à tarefa, rastreabilidade, sigilo, permissões dos usuários e limites financeiros vigentes; não interpretar como ordem de gasto ilimitado nem como contratação não solicitada. Mudança de escopo/destino sensível, exigência própria de contrato ou revisão automática concreta continua sendo tratada pelo requisito aplicável, sem inventar novas exigências.

[REAL — pendência anterior resolvida] Ativados IALD_HAIKU_PUBLICO_USD_DIA=1.00 e IALD_HAIKU_GRUPO_USD_DIA=5.00. A política atual aplica US$1 por conta/dia em cada grupo, US$5/dia ao grupo Haiku e US$5/dia ao grupo compartilhado MiMo/DeepSeek: até US$10/dia somando esses dois grupos, dentro dos controles gerais existentes. OpenAI/Kimi mantêm suas políticas atuais. O teto geral do provedor Claude lido nesta entrega é US$15/dia e ficou inalterado. luiz mantém a política anterior; a entrega não introduziu limite individual nele. Saldos e limites contratuais dos provedores continuam externos.

[REAL — verificação] Apenas duas variáveis numéricas acrescentadas ao .env; demais bytes preservados, backup byte a byte e ACL restrita. RouteBridge real com pacote Haiku 5.5 validou (1.0,5.0), Haiku elegível para contas públicas aprovadas e Sonnet restrito. Processo web reiniciado por supervisor existente após conferir fila ociosa; HTTP de entrada verificado. Nenhuma nova chamada paga, mensagem de teste ou alteração de conta/credencial. Elegibilidade não garante saldo ou disponibilidade futura de fornecedor.

[DISPONIBILIDADE] Configuração no backend compartilhado por web/iOS/Android; sem alteração de cliente ou nova compilação. Não se alegou instalação física nem inspeção dos grupos das lojas. Este adendo resolve somente a pendência de orçamento público registrada na entrega Haiku/JEV; não anuncia geração de imagens/vídeos integrada nem bancada em RAM.

[EVIDÊNCIA] C:\\IALD\\Central de Patentes\\work\\iald_haiku55_jev_20261007\\public_budget_authorized: public_budget_configuration.json, budget_validation.json, restart.json e memory_delivery.json. Backup imediato e append atômico nas oito superfícies de memória, incluindo AGENTS global.
'''
rows=[]
for p in paths:
    old=p.read_bytes()
    if marker.encode() in old:rows.append({'path':str(p),'status':'ALREADY_RECORDED'});continue
    nl='\r\n' if b'\r\n' in old else '\n';new=old+body.replace('\n',nl).encode('utf-8')
    bk=backup(p)
    assert p.read_bytes()==old,'Concurrent edit'
    atomic(p,new);assert p.read_bytes().startswith(old) and len(new)>len(old)
    rows.append({'path':str(p),'status':'APPENDED','backup':bk,'before':len(old),'after':len(new)})
write_evidence(w/'memory_delivery.json',{'status':'PASS','surfaces':rows})
print(json.dumps({'status':'PASS','memory_surfaces':len(rows)}))
