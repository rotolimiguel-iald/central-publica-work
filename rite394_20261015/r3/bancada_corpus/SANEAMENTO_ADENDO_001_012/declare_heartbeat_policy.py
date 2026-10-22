from support import *
D=ROOT/'heartbeat';rows=json.loads((D/'POR_MODULO_INTERPRETADO.json').read_text(encoding='utf-8'))
policy=[]
for r in rows:
 current=[dict(option=c['kind'],value=c['value'],line=c['line'],scope=c['scope']) for c in r['caps']]
 reason='DECISÃO ATUAL: manter exatamente a configuração do fonte recebido para preservar o escopo deste saneamento; otimização de elaboração não é objetivo desta rodada, conforme esclarecimento do operador. É política atual, não medição de necessidade nem recuperação de motivação passada.'
 history='NÃO RECUPERADO: motivo histórico específico da escolha de todos os valores numéricos. Os diagnósticos e relatos já citados permanecem OBSERVADO/DECLARADO, sem conversão dessa lacuna em medição.' if current else 'Não há elevação de maxHeartbeats neste fonte a justificar; permanece o padrão da toolchain. Não se inventa motivo histórico adicional.'
 policy.append(dict(module=r['module'],source=r['source'],current_settings=current or [dict(option='maxHeartbeats',value=200000,scope='default, no override')],current_reason=reason,historical_reason_status=history,observed_general_timeouts=r['general_timeout_events'],observed_typeclass_timeouts=r['typeclass_timeout_events'],nature_of_entry='DECISÃO ATUAL / DOCUMENTAL; não novo resultado de build'))
record(D/'POLITICA_ATUAL_POR_MODULO.json',dict(created_utc=stamp(),literal_scope='Declarar motivo por módulo; não minimizar empiricamente todos os limites.',status='PAGO — declaração documental autoral, histórico NÃO RECUPERADO onde não localizado',modules=policy,builds_added_for_this_policy=0))
lines=['','## Esclarecimento do operador e decisão atual por módulo','',
'[INPUT — orientação do operador nesta sessão] A cláusula pede declarar o motivo por módulo; não exige minimizar empiricamente todos os limites. A decisão atual deve ficar separada da história não recuperada.',
'', '[DECISÃO ATUAL — declaração autoral, não medição] Manter a configuração recebida em cada módulo abaixo para preservar o escopo do saneamento. Otimização de elaboração fica fora desta rodada. Os testes verdes existentes não serão repetidos para fabricar necessidade mínima. Zero builds novos por esta política.',
'', '[OPEN — histórico] O motivo histórico exato não localizado permanece **NÃO RECUPERADO**. Um timeout observado informa aquela falha; uma decisão atual não transforma o passado desconhecido em medido. As evidências anteriores e seus pins permanecem válidos e delimitados.',
'', '| Módulo | Configuração que se decide manter | Motivo ATUAL | História |','|---|---|---|---|']
for p in policy:
 conf='; '.join(c['option']+'='+str(c['value'])+(' @L'+str(c['line']) if 'line' in c else ' padrão') for c in p['current_settings'])
 hist='NÃO RECUPERADO quanto à escolha numérica; ver evidências acima' if next(r for r in rows if r['module']==p['module'])['caps'] else 'Sem elevação no fonte'
 lines.append(f'| `{p["module"]}` | {conf} | Preservar configuração e escopo; não otimizar elaboração nesta rodada | {hist} |')
lines+=['',f'JSON por módulo: [{(D/"POLITICA_ATUAL_POR_MODULO.json").name}](<{D/"POLITICA_ATUAL_POR_MODULO.json"}>), SHA256 `{digest(D/"POLITICA_ATUAL_POR_MODULO.json")}`.', '', 'O item h fica PAGO no alcance literal de declaração documental autoral, sem promover a lacuna histórica nem alegar otimização/necessidade mínima.']
p=D/'RECIBO_H.md';atomic(p,p.read_bytes()+'\n'.join(lines).encode('utf-8')+b'\n')
p=ROOT/'FALHAS_E_LIMITES.md';atomic(p,p.read_bytes()+'''\n## Esclarecimento final de h\n\nA cláusula literal exige declarar motivo por módulo, não benchmark mínimo. Foi registrada política ATUAL por módulo de preservar a configuração recebida no escopo desta rodada. O item documental é PAGO; a motivação histórica exata continua NÃO RECUPERADA onde faltar evidência. Nenhum build adicional foi executado para essa política.\n'''.encode('utf-8'))
p=ROOT/'finalize.py';s=p.read_text(encoding='utf-8')
s=s.replace("'h':dict(status='NÃO PAGO',qualification='Justificativa integral dos orçamentos ainda aberta; levantamento documental entregue'", "'h':dict(status='PAGO',qualification='Declaração por módulo; decisão atual separada da história NÃO RECUPERADA'")
s=s.replace("impediment='Não foi localizada justificativa histórica específica para a escolha exata de todos os limites. Os logs de falha não demonstram o mínimo necessário nem a motivação do autor; não preencher essa lacuna com história inferida.'", "impediment='Não se recuperou a motivação histórica exata de todos os valores. A cláusula documental está atendida pela declaração ATUAL por módulo, sem fazer passar essa decisão por história medida; não se pede mínimo empírico.'")
s=s.replace("# Avoid a numerical-uniqueness claim not present in the theorem.", "records['h']['current_policy_report']=pin(ROOT/'heartbeat/POLITICA_ATUAL_POR_MODULO.json')\n# Avoid a numerical-uniqueness claim not present in the theorem.")
s='\n'.join("'', 'Em h, cada módulo recebeu a decisão ATUAL de manter sua configuração para preservar o escopo desta rodada, sem otimização empírica. A motivação histórica não localizada permanece NÃO RECUPERADA; a política atual não a converte em medição. O item fica PAGO no alcance literal documental, sem novos builds.'," if 'Mantém-se NÃO PAGO' in l else l for l in s.splitlines())+'\n'
compile(s,str(p),'exec');atomic(p,s)
