from pathlib import Path
import json,os
R=Path(__file__).resolve().parent
def put(p,s):
 assert p.is_relative_to(R) and not p.exists();b=s.encode('utf8')
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(R/'deliver_reviewed_delta_v2.py').read_text(encoding='utf8')
s=s.replace("assert v['status']==q['status'],v['status']", "assert v['status']==q['status'],v['status']\nfull_trace=q.get('full_trace_constructed',False)\nassert full_trace == a.get('full_trace_constructed',False) == v.get('full_trace_constructed',False)\ntrace_label='contrato do traço concreto construído' if full_trace else 'traço concreto ainda OPEN'\ntrace_table='PAGO: mesmo peso, todas as leis do contrato.' if full_trace else 'NÃO PAGO por esta entrega.'")
s=s.replace('new_trace_inhabitant=False','new_trace_inhabitant=full_trace')
s=s.replace('A1(b): traço concreto ainda OPEN.]','A1(b): {trace_label}.]')
s=s.replace('| Habitante do contrato do traço | NÃO PAGO por esta entrega. |','| Habitante do contrato do traço | {trace_table} |')
assert s != (R/'deliver_reviewed_delta_v2.py').read_text(encoding='utf8')
put(R/'deliver_reviewed_delta_v3.py',s)
q=dict(audit='AUDITORIA_TRACIALIDADE_QUADRATICA_A1B',review='revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL',
 status='A1_QUADRATIC_TRACE_REVIEW_ACCEPTED__REGULAR_TRACE_CONSTRUCTED',name='tracialidade_e_contrato_do_traco_regular',
 title='Tracialidade e contrato do traço no core original',theorems=1,definitions=1,full_trace_constructed=True,
 docs=['REAPROVEITAMENTO_A1B_COMPATIBILIDADE_QUADRATICA','ADENDO_PRE_EMBALAGEM_CONTRATO_TRACO','ADENDO_EMBALAGEM_CONSUMIDORA_DO_TRACO'],
 description='Um teorema público, seis auxiliares privados e uma definição consumidora. O balanço33 é transportado pelo grafo original da raiz de Tomita a formas limitadas. Os cortes de domínio são retirados um por vez por convergência forte, comparando supremos ENNReal inclusive infinitos. A fórmula existente do peso perturbado e a relação S Lambda(a)=Lambda(a*) fornecem a igualdade no núcleo finito. O fornecedor27 a estende a todo o core. A definição RegularCoreTraceData usa literalmente scalarInverseLimitWeight e os fornecedores anteriores para zero, aditividade, homogeneidade, monotonicidade, fidelidade, normalidade, minorantes finitos e escala dual. Não há nova medida, estado, GNS ou gerador.',
 limit='O alcance é o contrato matemático RegularCoreTraceData na realização concreta. A construção não identifica h com Delta_nu, não confirma uma interpretação física, não calcula significância experimental e não incorpora automaticamente a prova ao monólito. As etapas restantes da ORDEM011 continuam sujeitas aos próprios tipos e verificações. Gate e originais permanecem intocados.')
put(R/'delivery_configs/quadratic_trace.json',json.dumps(q,ensure_ascii=False,indent=2))
text='[OPEN — esclarecimento da embalagem, anterior à validação] O adendo prévio propunha preencher o contrato no mesmo arquivo. A implementação usa um módulo consumidor separado, V351RegularCoreTraceConstruction, com uma única definição e nenhum novo teorema: ele importa V351QuadraticTrace e liga diretamente as leis já provadas ao contrato existente. Isso permite conferir separadamente a prova e o preenchimento dos campos, sem recompilar a prova a cada ajuste de tipagem da estrutura. Não há segunda definição do peso. Ambos integram a mesma entrega34 e a mesma validação/auditoria. O arquivo preparado não é contado como contrato construído antes de compilar e passar revisão independente. O writer v3 é cópia do v2 e corrige os rótulos historicamente fixos OPEN/new_trace_inhabitant=False somente quando auditoria e revisão concordarem full_trace_constructed=True. O writer v2 preservado continua ancorando todas as entregas anteriores. Nenhum writer34 foi executado nesta preparação.'
put(R/'ADENDO_EMBALAGEM_CONSUMIDORA_DO_TRACO.md',text+'\n')
put(R/'ADENDO_EMBALAGEM_CONSUMIDORA_DO_TRACO.json',json.dumps(dict(status='OPEN__PRE_VALIDATION_CONSUMER_MODULE',text=text,full_trace_constructed=False,writer_executed=False,gate_changed=False),ensure_ascii=False,indent=2))
print('Prepared writer v3, config and scope addendum. No delivery executed.')
