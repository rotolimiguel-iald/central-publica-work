"""Register the measured routing admission repair, preserving accepted layers."""
from mission_io import WORK,REFERENCE,ACTOR,call,pin,project
from advance import action
p,_=project()
source=pin(WORK/'tests_app/JEV_REAL_C2_MEASUREMENT_R1.json')
known=p['projection']['active']+p['projection']['settled']
if not any(t['id']=='J' for t in known):
    call('mission_cli.py',{'operation':'extend','reference':str(REFERENCE),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'event_id':'organism-jev-admission-J-r1',
        'requirements':[{'id':'J','depends_on':['A'],'criterion':
            'Corrigir admissão JEV medida com contrato real: distinguir guarda local por bytes dos limites documentados de tokens; contexto ampliado oficial somente quando necessário, antes de qualquer envio, sem cortar ordens/critérios/pendências. Preservar modelo1.13, autenticação, carteira, decisões, recusa visível e execução única. Pinar fontes oficiais, testar1/10/100turnos, fronteiras/overflow/Unicode, payload efetivamente enviado e header. Nenhum fallback ou retry após envio incerto; nenhuma alteração da ciência. Entregar camada nova para revisão independente antes da implantação.'}],
        'reason':'Pacote real com10turnos excede guarda local34.681>30.000bytes; API oficial tem contexto documentado em tokens e modo ampliado. Admissão correta é necessária à continuidade autorizada.',
        'sources':[source,pin(WORK/'OPERADOR_VERBATIM.txt')]},'extend_J')
p,_=project();v=next(t for t in p['projection']['active'] if t['id']=='V')
if 'J satisfeita' not in v['criterion']:
    action('amend','V',{'criterion':v['criterion']+' Exigir J satisfeita e pacote JEV real validado com a memória final, incluindo100turnos sintéticos sem perda de ordens.',
        'reason':'Medida real corrigiu a expectativa do pacote sintético; integrar a admissão antes de produção.',
        'sources':[source]})
print('J registrada e V vinculada ao reparo de admissão.')
