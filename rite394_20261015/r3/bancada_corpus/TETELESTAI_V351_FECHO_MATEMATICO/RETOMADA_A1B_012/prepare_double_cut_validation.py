from pathlib import Path
import os
R=Path(__file__).resolve().parent
def put(p,b):
    assert p.is_relative_to(R) and not p.exists()
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
changes={
 'modular_implementation':'modular_cut_balance',
 'ModularImplementation':'ModularCutBalance',
 'MODULAR_IMPLEMENTATION':'MODULAR_CUT_BALANCE',
 'AUDITORIA_IMPLEMENTADOR_MODULAR_A1B':'AUDITORIA_BALANCO_DOS_CORTES_A1B',
 'AUDITORIA_VETORES_FIXOS_MODULARES_A1B':'AUDITORIA_IMPLEMENTADOR_MODULAR_A1B',
 'BadModularCutBalanceRightSignChanged':'BadModularCutBalanceComplementChanged',
 'private_theorems=0':'private_theorems=9',
 'modular_cut_balance_constructed=True, implementator_equality_proved=True, fixed_tomita_vectors_constructed=True':'double_cut_balance_constructed=True, cut_commutation_constructed=True',
}
for stem in ['run_modular_implementation_replay','audit_modular_implementation','validate_modular_implementation']:
    s=(R/(stem+'.py')).read_text(encoding='utf8')
    # Replace the prerequisite first to avoid subsequently replacing its replacement.
    s=s.replace('AUDITORIA_VETORES_FIXOS_MODULARES_A1B','__PREREQUISITE__')
    for old,new in changes.items(): s=s.replace(old,new)
    s=s.replace('__PREREQUISITE__','AUDITORIA_IMPLEMENTADOR_MODULAR_A1B')
    if stem.startswith('audit_'):
        needle="assert len(targets)==1 and sum(t['kind']=='theorem' for t in targets)==1"
        assert needle in s
        s=s.replace(needle,needle+"\nassert len(re.findall(r'^private theorem ',s,re.M)) == 9\nassert not re.search(r'^private def ',s,re.M)")
    p=R/(stem.replace('modular_implementation','modular_cut_balance')+'.py')
    put(p,s.encode('utf8'));print(p)
