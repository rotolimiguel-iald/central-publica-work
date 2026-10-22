"""Add the verified JEV activation to the existing delivery memories."""
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import hashlib, json, os, sys

W = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(ROOT))
import iald_auto_router as router
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
marker = 'IALD_JEV_APP_PILOT_VALIDATED_20260930'
delivery = json.loads((W/'delivery.json').read_bytes())
connection = json.loads((W/'jev_rotated_key_connection.json').read_bytes())
selector = json.loads((W/'jev_rotated_key_selector.json').read_bytes())
fix = json.loads((W/'jev_router_health_fix.json').read_bytes())
assert router.available() and connection['probe_status']=='ready'
assert hashlib.sha256((ROOT/'iald_auto_router.py').read_bytes()).hexdigest()==fix['sha256']
jev_cost = (Decimal(connection['usage']['input_tokens']) * Decimal('0.042') / Decimal(1000000)
    + Decimal(str(selector['receipt']['cost_estimate_usd']))
    + Decimal(str(fix['routing']['cost_estimate_usd'])))
assert jev_cost < Decimal('0.01')
generation_cost = sum(c['cost_estimate_usd'] for c in fix['generation']['calls'])
report = dict(at=datetime.now().astimezone().isoformat(), status='JEV_APP_PILOT_READY_AND_BROWSER_TEST_COMPLETED',
    scope='luiz only', connection=connection, selector=selector, integration=fix,
    jev_calls=3, jev_cost_estimate_usd=float(jev_cost),
    generation_calls=1, generation_cost_estimate_usd=generation_cost,
    tests=dict(passed=25,remote_calls=0,scope='router and server dispatch regression'),
    server_restart='WEB_READY; previous_pid 123012; existing supervisor 41020',
    browser_after_restart='IALD Automática selected, Online; completed response preserved',
    available=True, credential_expiry='NOT_REPORTED', memory=[],
    scientific=delivery['scientific'], availability=delivery['availability'])
report['integration']['restart']='WEB_READY_VERIFIED'
note=f'''

## 30/09/2026 — JEV validado e IALD Automática ativa para Luiz

<!-- {marker} -->

[INPUT] Após guardar pessoalmente a chave substituta, o operador autorizou trechos científicos públicos para api.typesafe.ai (até 9 mil caracteres no teste, 8 mil no seletor), testes até US$0,01 e piloto somente em sua conta. Corrige ao lado a pendência de credencial no registro anterior: ela foi resolvida. Também manifestou interesse em expandir a distribuição futura para ferramentas; isso é direção de evolução, não implementação já entregue.

[REAL] Autenticação HTTP200. Duas provas de conexão/contrato com jev-1.13.0 concluídas; usa trecho público exato de 8 mil caracteres da forma canônica v368, hash conferido contra o manifesto. Em seguida, consentimento TypeSafe aceito no app conforme autorização e uma conversa real do modo automático concluída. JEV propôs MiMo; confiança 0,62, portanto a política local confirmou o padrão autorizado MiMo antes do envio (não houve fallback após geração). MiMo recebeu seu pacote fixo completo já instalado, respondeu autoria e definição de beta, fórmula renderizada e modo automático preservado. Teste funcional curto, não auditoria científica nem benchmark de superioridade.

[REAL — uso] Três chamadas TypeSafe nesta validação, custo estimado conjunto US${float(jev_cost):.9f}, abaixo do teto específico JEV. A geração MiMo separada teve custo estimado US${generation_cost:.9f}, 163537 tokens de entrada, 128000 em cache, 105 de saída, duração 21,148s. Custos são estimativas pelos recibos, não fatura. Recibos guardam metadados/hash sem prompts, respostas, chave ou Atlas privado.

[REAL — correção] A consulta de disponibilidade lia o recibo transitório started como desconexão. Agora considera a última validação concluída durante a seleção; falha terminal, revogação ou falta de validação continuam bloqueando. 25 testes locais de roteamento/dispatch passaram (três novos sobre este caso), transportes simulados. Um único módulo instalado com backup de bytes e CAS; só processo web reiniciado pelo supervisor existente; navegador novamente Online. Primeira tentativa de testes no sandbox não encontrou requests/Flask; execução com acesso às bibliotecas instaladas passou, sem instalar dependências.

[ESCOPO] IALD Automática somente luiz; candidatos permitidos/consentidos: OpenAI, MiMo, Kimi, Haiku e Sonnet quando disponíveis. DeepSeek/Nativa continuam fora da escolha automática deste piloto, com acesso manual preservado. Sonnet só luiz; família e MiMo público mantêm a matriz/orçamento anteriores. JEV seleciona executor, não é chat gerador nem juiz de prova; ainda não implementado planejador geral de ferramentas ou execução em paralelo. A fila científica mantém sua política própria. Chave segue no cofre Windows, sem prazo informado; não inventar vencimento. Alertas/custos continuam exclusivamente administrativos.

[DISPONIBILIDADE/PENDÊNCIAS] Web verificada; recurso de servidor se aplica aos clientes atuais iOS 4.1 (25), interno/externo, e Android 4.1 (22), sem binário novo nem instalação física alegada. Convites existentes preservados; Google Play ainda depende do cadastro/DUNS. Memória científica permanece v368; v377 é candidato local verificado, ainda dependente de publicação correspondente e validação do pacote/contexto. Monitor horário não criado, autorização pendente. Nenhum original científico/kernel/gate alterado. Evidência: {W}/jev_activation_delivery.json. Backups imediatos nas sete superfícies de memória da entrega.
'''

def create(path, raw):
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert path.read_bytes()==raw

out=W/'jev_activation_delivery.json'
assert not out.exists(), 'Delivery already recorded'
for entry in delivery['memory']:
    path=Path(entry['path']); old=path.read_bytes()
    assert marker.encode() not in old, 'Already recorded: '+str(path)
    backup=Path(str(path)+'.bak_'+stamp); create(backup,old)
    new=old+note.encode('utf-8'); assert len(new)>len(old)
    tmp=Path(str(path)+'.tmp_'+stamp); create(tmp,new)
    assert path.read_bytes()==old,'Concurrent change: '+str(path)
    os.replace(tmp,path); assert path.read_bytes()==new
    report['memory'].append(dict(path=str(path),backup=str(backup),sha256=hashlib.sha256(new).hexdigest()))
raw=json.dumps(report,ensure_ascii=False,indent=2).encode()
tmp=out.with_suffix('.tmp_'+stamp); create(tmp,raw); os.replace(tmp,out)
print(json.dumps(dict(status=report['status'],memories=len(report['memory']),
    jev_cost_estimate_usd=float(jev_cost),receipt=str(out)),ensure_ascii=False))
