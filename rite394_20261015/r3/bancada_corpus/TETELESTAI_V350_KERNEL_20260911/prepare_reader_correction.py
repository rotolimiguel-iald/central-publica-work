"""Correct two existing result readers; add no theorem, gate input, or layer."""
from pathlib import Path
from datetime import datetime
import ast
import copy
import hashlib
import json
import math
import os

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'reader_correction_v2'
OUT.mkdir(exist_ok=True)
source_raw = (ROOT/'um.py').read_bytes()
source = source_raw.decode('utf-8')
tree = ast.parse(source)
lines = source.splitlines(keepends=True)
names = ['prove_the_assembly_and_the_single_debt', 'prove_the_atlas_and_the_index']
nodes = {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names}
blocks = {name:''.join(lines[node.lineno-1:node.end_lineno]) for name,node in nodes.items()}
eol = '\r\n' if b'\r\n' in source_raw else '\n'

def replace_one(text, old, new):
    old, new = old.replace('\n',eol), new.replace('\n',eol)
    assert text.count(old) == 1, old[:100]
    return text.replace(old,new,1)

assembly = blocks[names[0]]
assembly = replace_one(assembly,
    '    # a bandeira do razonete: continua ESCURA (ausencia do nome reservado)\n',
    '    # Read the constructed certificate flag; its former absence is historical.\n')
assembly = replace_one(assembly,
    '    total = len(clausulas)\n',
    '    total = len(clausulas)\n'
    '    expected_clause_flags = ["red_" + key for key in _REDUCTION_FLAGS\n'
    '                             if key.startswith("clause_")]\n'
    '    clause_readings_present = all(type(kf.get(key)) is bool for key in expected_clause_flags)\n')
assembly = replace_one(assembly,
    '        ("[MEDIDA] A MONTAGEM: %d de %d clausulas do certificado PROVADAS nesta arvore" % (provadas, total), bool(provadas == 7)),\n'
    '        ("[MEDIDA] a oitava depende de UM enunciado nomeado: o teorema de comutacao", bool(provadas == total - 1)),\n',
    '        ("[MEDIDA] A MONTAGEM: %d de %d clausulas lidas; as sete clausulas anteriores permanecem provadas" % (provadas, total),\n'
    '         bool(clause_readings_present and all(ok for _, ok in clausulas[:-1]))),\n'
    '        ("[FAIL-CLOSED] a bandeira construida exige todas as clausulas verificadas",\n'
    '         bool((not bandeira or provadas == total)\n'
    '              and v350_frontier_flag_has_proof(kf, "red_clause_JMJ_contains")\n'
    '              and v350_frontier_flag_has_proof(kf, "gpf_tower_act_III_inhabitant_constructed"))),\n')
assembly = replace_one(assembly,
    '            "a_montagem": "7/8 clausulas provadas; a 8a condicionada ao teorema de comutacao. A divida do item = UM enunciado",\n'
    '            "o_que_nao_fecha": "a BANDEIRA. Instancia condicionada NAO habita; o nome reservado segue ESCURO. Montar nao e pagar",\n',
    '            "a_montagem": ("%d/%d clausulas verificadas nesta rodada; a oitava e lida pelo fornecedor Lean do teorema de comutacao" % (provadas, total)),\n'
    '            "o_que_nao_fecha": ("A bandeira do Ato III esta construida nesta realizacao; isso nao amplia o escopo dos teoremas nem altera o gate principal"\n'
    '                                 if bandeira and provadas == total else\n'
    '                                 "A bandeira do Ato III nao esta construida nesta rodada; uma montagem condicionada nao substitui seu fornecedor"),\n')
assembly = replace_one(assembly,
    '        "verdict": ("ENTANGLEMENT_IS_NOT_CONJUNCTION_AND_THE_FALSE_ROUTE_IS_CLOSED_BY_THEOREM__SEVEN_OF_EIGHT_CLAUSES_PROVED__THE_CERTIFICATE_IS_ASSEMBLED_CONDITIONED_ON_ONE_NAMED_STATEMENT__THE_FLAG_STAYS_DARK_BECAUSE_ASSEMBLING_IS_NOT_PAYING" if all_v\n'
    '                    else "ASSEMBLY_NOT_SEALED_THIS_RUN"),\n',
    '        "verdict": ("ASSEMBLY_NOT_SEALED_THIS_RUN" if not all_v else\n'
    '                    "EIGHT_CLAUSES_VERIFIED__ACT_III_CERTIFICATE_CONSTRUCTED_ON_THE_PRODUCT_TOWER__PRINCIPAL_GATE_UNCHANGED" if bandeira else\n'
    '                    "EIGHT_CLAUSES_VERIFIED__ACT_III_CERTIFICATE_FLAG_NOT_CONSTRUCTED" if provadas == total else\n'
    '                    "ENTANGLEMENT_IS_NOT_CONJUNCTION_AND_THE_FALSE_ROUTE_IS_CLOSED_BY_THEOREM__SEVEN_OF_EIGHT_CLAUSES_PROVED__THE_CERTIFICATE_IS_ASSEMBLED_CONDITIONED_ON_ONE_NAMED_STATEMENT__THE_FLAG_STAYS_DARK_BECAUSE_ASSEMBLING_IS_NOT_PAYING"),\n')
assembly = replace_one(assembly,
    '    """v251 (LOTE) -- A MONTAGEM FEITA E A DIVIDA REDUZIDA A UM ENUNCIADO [ADITIVO].\n',
    '    """v251 historical derivation; current clause/flag readings are reported below.\n'
    '    Integration correction: constructing clause eight must not fail a seven-only check.\n')
assembly = replace_one(assembly,
    '    # LIDA da rodada, pelo nome Lean que a prova; a oitava nao tem nome porque nao\n'
    '    # existe, e a ausencia do nome a mantem nao-provada, por construcao.\n',
    '    # Read each clause from its Lean provider, including the eighth when present.\n'
    '    # Missing readings remain visible; the historical count is not a requirement.\n')

atlas = blocks[names[1]]
atlas = replace_one(atlas,
    '        ("[FAIL-CLOSED] ***a tipagem e\' NOMINAL e nao pagou preco nenhum: %d bandeira(s) "\n'
    '         "qgf_/gpf_ acesa(s) -- as %d acesas de red_/gpi_ sao o regime normal (kernel "\n'
    '         "provado e importacao com ponte) e nao sao acrescimo desta versao. CUNHAR NOME "\n'
    '         "NAO PAGA PRECO" % (len(_preco), len(_kernel_import)), bool(not _preco)),\n',
    '        # Other constructions may already be proved; naming does not create or erase them.\n')
atlas = replace_one(atlas,
    '        "n_atlas": len(_a), "n_indice": len(_i),\n',
    '        "n_atlas": len(_a), "n_indice": len(_i),\n'
    '        "preexisting_construction_flags": sorted(_preco),\n'
    '        "preexisting_kernel_import_count": len(_kernel_import),\n')

updated = {names[0]: assembly, names[1]: atlas}
candidate = source
for name in names:
    assert candidate.count(blocks[name]) == 1
    candidate = candidate.replace(blocks[name],updated[name],1)
roundtrip = candidate
for name in names:
    roundtrip = roundtrip.replace(updated[name],blocks[name],1)
assert roundtrip.encode('utf-8') == source_raw
ast.parse(candidate)

# Exercise only the existing readers and their existing dictionary, without importing um.py.
reduction = next(node for node in tree.body if isinstance(node,ast.Assign)
                 and any(isinstance(target,ast.Name) and target.id=='_REDUCTION_FLAGS' for target in node.targets))
env = {'math':math,'_REDUCTION_FLAGS':ast.literal_eval(reduction.value)}
proof_contracts = next(node for node in tree.body if isinstance(node,ast.Assign)
                      and any(isinstance(target,ast.Name) and target.id=='_V350_MODULAR_CONTRACTS'
                              for target in node.targets))
env['_V350_MODULAR_CONTRACTS'] = ast.literal_eval(proof_contracts.value)
proof_readers = [node for node in tree.body if isinstance(node,ast.FunctionDef)
                 and node.name in ['verify_v350_modular_provenance','v350_frontier_flag_has_proof']]
assert len(proof_readers) == 2
exec(compile(ast.Module(body=proof_readers,type_ignores=[]),'<unchanged-existing-proof-readers>','exec'),env)
new_tree = ast.parse(candidate)
reader_nodes = [node for node in new_tree.body if isinstance(node,ast.FunctionDef) and node.name in names]
exec(compile(ast.Module(body=reader_nodes,type_ignores=[]),'<existing-readers-only>','exec'),env)
fresh = json.loads((ROOT/'r/completed_attempt_02/um_absoluto.json').read_bytes())['core']
old = json.loads((ROOT/'fontes/um_absoluto.json').read_bytes())['core']
tests = []
def check(label, predicate):
    assert predicate,label
    tests.append(label)

for label, core in [('seven_clause_baseline',old),('eight_clause_runtime',fresh)]:
    before = copy.deepcopy(core['kernel_formalization'])
    for name in names:
        check(label+':'+name,env[name](core)['all_verified'] is True)
    check(label+':readers_preserve_flags',before==core['kernel_formalization'])
partial = copy.deepcopy(fresh)
partial['kernel_formalization']['gpf_tower_act_III_inhabitant_constructed'] = False
check('eight_clauses_without_certificate_is_reported', env[names[0]](partial)['all_verified'] is True
      and 'FLAG_NOT_CONSTRUCTED' in env[names[0]](partial)['verdict'])
for key in ['red_'+key for key in env['_REDUCTION_FLAGS'] if key.startswith('clause_')]:
    missing = copy.deepcopy(fresh)
    missing['kernel_formalization'].pop(key)
    check('missing_clause_reading:'+key,env[names[0]](missing)['all_verified'] is False)
incoherent = copy.deepcopy(fresh)
incoherent['kernel_formalization']['red_clause_JMJ_contains'] = False
check('lit_certificate_missing_eighth_rejected',env[names[0]](incoherent)['all_verified'] is False)
for flag in ['red_clause_JMJ_contains','gpf_tower_act_III_inhabitant_constructed']:
    for term in env['_V350_MODULAR_CONTRACTS'][flag]:
        missing = copy.deepcopy(fresh)
        missing['kernel_formalization']['axiom_report'].pop(term)
        check('missing_provider_or_bridge:'+term,env[names[0]](missing)['all_verified'] is False)
        untrusted = copy.deepcopy(fresh)
        untrusted['kernel_formalization']['axiom_report'][term] = ['sorryAx']
        check('forbidden_axiom:'+term,env[names[0]](untrusted)['all_verified'] is False)
for key in ['ext_ai_atlas_separation_kernel_proved','ext_ai_atlas_coverage_kernel_proved',
            'ext_ai_atlas_covariance_kernel_proved','ext_ai_atlas_chain_rule_kernel_proved',
            'ext_ai_atlas_self_kernel_proved','ext_ai_atlas_inverse_kernel_proved',
            'ext_iald_selector_constructed','ext_iald_selects_kernel_proved',
            'ext_iald_idempotent_kernel_proved','ext_iald_selfadjoint_kernel_proved',
            'ext_iald_rank_one_kernel_proved','ext_iald_gate_and_record_kernel_proved']:
    missing = copy.deepcopy(fresh)
    missing['kernel_formalization'][key] = False
    check('missing_atlas_or_index_proof:'+key,env[names[1]](missing)['all_verified'] is False)
unrelated = copy.deepcopy(fresh)
unrelated['kernel_formalization']['qgf_unrelated_test_flag'] = True
check('unrelated_construction_is_not_a_reader_requirement',env[names[1]](unrelated)['all_verified'] is True)

def write_new(path,raw):
    assert not path.exists()
    temporary = path.with_name(path.name+'.tmp')
    with temporary.open('xb') as stream:stream.write(raw)
    assert temporary.read_bytes()==raw
    os.replace(temporary,path)

raw=candidate.encode('utf-8')
write_new(OUT/'um.py',raw)
report=dict(timestamp=datetime.now().astimezone().isoformat(),
            source_sha256=hashlib.sha256(source_raw).hexdigest(),candidate_sha256=hashlib.sha256(raw).hexdigest(),
            modified_existing_functions=names,added_functions=[],embedded_lean_changed=False,
            principal_gate_changed=False,only_named_functions_changed=True,
            tests_passed=tests,regression_tests=len(tests),
            current_assembly=env[names[0]](fresh),current_atlas=env[names[1]](fresh),
            status='CANDIDATE_TESTED_NOT_INSTALLED_NOT_FULL_RUNTIME', runtime_result_not_rewritten=True)
write_new(OUT/'verification.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({key:report[key] for key in ['candidate_sha256','modified_existing_functions','added_functions','regression_tests','status']}))
