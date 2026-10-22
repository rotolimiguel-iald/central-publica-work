"""Fixture evaluation of repair predicates, not execution of a modified um.py."""
import ast
import copy
import json
from pathlib import Path

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
OUT=ROOT/'revisao/runtime_seals_preliminary_20260913_100700_656494'
current=json.loads((OUT/'final_current.json').read_bytes())['core']['kernel_formalization']
ins=json.loads((OUT/'final_inspection.json').read_bytes())
tree=ast.parse((ROOT/'um.py').read_text(encoding='utf-8'))
owned=[]
for n in tree.body:
    if isinstance(n,ast.FunctionDef) and n.name=='prove_the_atlas_and_the_index':
        for a in n.body:
            if isinstance(a,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['_atlas','_indice'] for t in a.targets):
                owned.extend(ast.literal_eval(a.value))
contracts={}
for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_V350_MODULAR_CONTRACTS' for t in n.targets):
        contracts=ast.literal_eval(n.value)
clauses=list(ins['proposed_guard_evaluation']['clause_providers'])
allowed={'propext','Classical.choice','Quot.sound'}
def proof(k,f):
    return (k.get('lake_build_ok') is True and k.get('all_verified') is True and k.get('audit_returncode')==0
        and f in contracts and all(isinstance(k.get('axiom_report',{}).get(n),list)
            and set(k['axiom_report'][n])<=allowed for n in contracts[f]))
def assembly(k):
    return (all(type(k.get(f)) is bool for f in clauses)
        and all(k[f] for f in clauses[:7])
        and type(k.get('gpf_tower_act_III_inhabitant_constructed')) is bool
        and (not k['gpf_tower_act_III_inhabitant_constructed'] or all(k[f] for f in clauses))
        and all(not k.get(f) or proof(k,f) for f in ['red_clause_JMJ_contains','gpf_tower_act_III_inhabitant_constructed']))
def atlas(k): return all(k.get(f) is True for f in owned)
cases={}
for name in ['current_8_of_8','historical_7_of_8','eight_flag_off','false_converse_with_flag_on','missing_boolean',
             'true_without_bridges','true_with_sorry','missing_atlas_name','unrelated_flags_changed']:
    k=copy.deepcopy(current)
    if name=='historical_7_of_8':k['red_clause_JMJ_contains']=False;k['gpf_tower_act_III_inhabitant_constructed']=False
    elif name=='eight_flag_off':k['gpf_tower_act_III_inhabitant_constructed']=False
    elif name=='false_converse_with_flag_on':k['red_clause_JMJ_contains']=False
    elif name=='missing_boolean':k.pop(clauses[0])
    elif name=='true_without_bridges':
        for v in contracts.values():k['axiom_report'].pop(v[1],None)
    elif name=='true_with_sorry':
        for v in contracts.values():k['axiom_report'][v[1]]=['sorryAx']
    elif name=='missing_atlas_name':k[owned[0]]=False
    elif name=='unrelated_flags_changed':
        for f in list(k):
            if f.startswith(('qgf_','gpf_')):k[f]=not k[f]
    before=copy.deepcopy(k)
    cases[name]={'assembly':assembly(k),'atlas_own_terms':atlas(k),'fixture_unchanged':k==before}
result={'scope':'DESIGN_VALIDATION_ONLY__NO_AUTHOR_FUNCTION_EXECUTED_OR_CHANGED',
    'atlas_owned_names':owned,'clauses':clauses,
    'final_design':'Assembly preserves 7/8 and 8/8 states plus existing proof guard on lit converse/ActIII; Atlas owns only its 6+6 names, other flags diagnostic.',
    'clarification':'final_inspection proposed_atlas checked global provenance; this final design deliberately removes that global dependency from Atlas. Provenance remains enforced by kernel/frontier and assembly.',
    'cases':cases}
dest=OUT/'consumer_repair_design.json';assert not dest.exists()
dest.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(result,ensure_ascii=False,indent=2))
