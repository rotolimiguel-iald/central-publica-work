"""Add measured projection-growth repair without rewriting the accepted core."""
from mission_io import WORK,REFERENCE,ACTOR,call,pin,project
from advance import action

p,_=project()
known=p['projection']['active']+p['projection']['settled']
source=pin(WORK/'tests_app/APP_PROJECTION_GROWTH_FINDING_R1.json')
if not any(t['id']=='C2' for t in known):
    call('mission_cli.py',{
        'operation':'extend','reference':str(REFERENCE),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'event_id':'organism-core-projection-growth-C2-r1',
        'requirements':[{'id':'C2','depends_on':['C'],'criterion':
            'Corrigir o crescimento medido da projeção em versão nova do core: indexar apenas registros mecânicos verificáveis de execução terminal, sem perder ordens, critérios, decisões, ciência, erratas, pendências/incertezas. Originais e recuperação completos preservados. Medir 1/10/100 turnos, pendentes versus revisados; manter recusa visível de overflow obrigatório, API/CAS e revisão/hash. Testar mutação de pinos, escopo, revisão, estado desconhecido e recuperação exata; sem autoaceite.'}],
        'reason':'A integração real mediu 60126 caracteres obrigatórios em 10 turnos; duplicação de metadados impediria continuidade no JEV30k. Correção necessária ao pedido de memória progressiva do operador.',
        'sources':[source,pin(WORK/'OPERADOR_VERBATIM.txt')]},'extend_C2')
p,_=project()
v=next(t for t in p['projection']['active'] if t['id']=='V')
if 'C2' not in v['criterion']:
    action('amend','V',{'criterion':v['criterion']+' Inclui C2 satisfeita e testes cruzados de todos os consumidores no core final; nenhum plano de produção antes dessa evidência.',
        'reason':'Incluir o achado material de crescimento da projeção antes da revisão conjunta e implantação.',
        'sources':[source]})
print('C2 registrada; V inclui a correção medida.')
