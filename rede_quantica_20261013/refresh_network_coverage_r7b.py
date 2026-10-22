"""Refresh exact coverage in a NEW candidate from an independent prior audit.

The old contract, source metadata and specification remain as explicit history.
No count is taken from the main invocation that will later check this contract.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
from diary_r1 import new, pin
import preaudit_network_r7b as audit

OUT = audit.OUT
DEST = OUT/'coverage_candidate_r7'
CONTRACT = OUT/'full_rite/KH_N1_V394_NETWORK_R7_PREAUDIT.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def assignments(tree):
    return {n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign)
        and isinstance(n.targets[0],ast.Name)}


def measured_contract():
    measured_path = audit.DEST/'MEASURED_COVERAGE_R1.json'
    m = json.loads(measured_path.read_bytes())
    assert m['passed'] is True
    prep = json.loads(audit.read(m['prepared']))
    candidate_raw = audit.read(m['candidate'])
    assert m['candidate'] == prep['candidate'] == pin(audit.CANDIDATE)
    compiled = json.loads(audit.read(m['compiled_bundle']))
    assert m['compiled_bundle'] == prep['compiled_bundle']
    plan = audit.validate_bundle(compiled)
    bodies = audit.embedded(candidate_raw)
    reconstructed = audit.embedded(audit.read(plan['baseline']))
    for row in plan['modules']:
        content = audit.read(row['transposed_source']).decode('utf-8')
        if row['relative'] in reconstructed:
            assert reconstructed[row['relative']] == content
        reconstructed[row['relative']] = content
    reconstructed[plan['audit_relative']] = audit.read(plan['audit']).decode('utf-8')
    glue = 'import '+plan['audit_module']+'\n'
    reconstructed['TGLExt.lean'] += '\n'+glue
    reconstructed['TGL/Audit.lean'] = glue+'\n'+reconstructed['TGL/Audit.lean']
    assert reconstructed == bodies, 'Source set must equal the audited baseline plus the declared additions'
    hashes = {rel:sha(body.encode('utf-8')) for rel,body in bodies.items()}
    assert hashes == prep['formal_files_sha256'] == m['formal_files_sha256']
    builds = [json.loads(audit.read(meta)) for meta in m['builds']]
    assert len(builds) == 2 and {b['module'] for b in builds} == {'TGLExt','TGL/Audit'}
    for b in builds:
        assert b['passed'] is True and type(b['exit_code']) is int and b['exit_code'] == 0
        source = audit.read(b['source'])
        assert source == bodies[b['module']+'.lean'].encode('utf-8')
        assert b['prepared'] == m['prepared']
        assert Path(b['command'][-1]).resolve() == Path(b['source']['path']).resolve()
        audit.read(b['stdout']); audit.read(b['stderr']); audit.read(b['object'])
    actual = next(b for b in builds if b['module'] == 'TGL/Audit')
    parser, parser_pin = audit.parsers()
    assert parser_pin == m['parser'] == actual['parser']
    log = audit.read(actual['stdout']).decode('utf-8')
    ax = parser.parse_lean_axioms_v394(log)
    provenance = parser.parse_lean_provenance_v394(log)
    totals = re.findall(r'(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=([0-9]+) thm=([0-9]+) fora_do_trio=([0-9]+)\s*$',log)
    assert len(totals) == 1 and ax['ok'] and provenance['ok']
    decl, thm, outside = map(int,totals[0])
    assert decl >= thm > 0 and outside == 0
    assert ax['axioms'] == actual['axiom_report'] and set(ax['axioms']) == set(provenance['sources'])
    assert provenance['sources'] == json.loads(audit.read(m['provenance']))
    assert all(p in bodies for p in provenance['sources'].values())
    assert all(set(a) <= audit.TRIO for a in ax['axioms'].values())
    assert len(ax['axioms']) == decl
    for key,value in [('total_declarations',decl),('total_theorems',thm),('outside_trio',0),('axiom_report_count',decl),('unread_names',0)]:
        assert type(m[key]) is int and m[key] == value
    for row in prep['copies']:
        audit.read(row['source']); audit.read(row['copy'])
    return dict(schema='tgl-v394-whole-kernel-coverage/v2', version='v394', revision='network_r7',
        whole_closure_audit=True, audit_exit_code=0, decl=decl, thm=thm,
        fora_do_trio=0, nao_lidas_pelo_regex=0, axiom_report_entries=decl,
        sorryAx_no_log_do_audit=0, formal_files_sha256=hashes,
        measured_coverage_receipt=pin(measured_path), audit_log=actual['stdout'],
        audit_receipt=next(meta for meta,b in zip(m['builds'],builds) if b['module']=='TGL/Audit'),
        candidate_before_patch=m['candidate'], provenance=m['provenance'], parser=parser_pin,
        additional_formal_sources={},
        scope='Exact compiler counts before main; prior nonembedded _check_damming.lean is historical and is not part of this new isolated source tree.')


def compose(raw, contract, contract_meta):
    tree = ast.parse(raw); nodes = assignments(tree)
    bodies = ast.literal_eval(nodes['_EMBEDDED_KERNEL_FILES'].value)
    assert contract['formal_files_sha256'] == {k:sha(v.encode('utf-8')) for k,v in bodies.items()}
    for key in ('decl','thm','axiom_report_entries','nao_lidas_pelo_regex','fora_do_trio'):
        assert type(contract[key]) is int and contract[key] >= 0
    assert contract['decl'] == contract['axiom_report_entries'] >= contract['thm'] > 0
    assert contract['nao_lidas_pelo_regex'] == contract['fora_do_trio'] == 0
    specs = ast.literal_eval(nodes['_V393_SPECS'].value)
    sources = ast.literal_eval(nodes['_V393_FONTES'].value)
    matches = [i for i,s in enumerate(specs) if s['nome']=='kh_n1_cobertura_v394']
    assert len(matches) == 1
    i = matches[0]; old = copy.deepcopy(specs[i]); current = copy.deepcopy(old)
    prior_source = copy.deepcopy(sources['kh_n1_v394'])
    replacements = {'h_decl':contract['decl'], 'h_thm':contract['thm'],
        'h_fora_do_trio':0, 'h_nao_lidas_pelo_regex':0,
        'h_report_exact':contract['axiom_report_entries'], 'h_sources_exact':contract['formal_files_sha256']}
    assert set(replacements) <= {c['id'] for c in current['checks']}
    for check in current['checks']:
        if check['id'] in replacements:
            check['valor'] = replacements[check['id']]
            check['descricao'] = 'Comparacao exata com a pre-auditoria integral do bundle R7, pinada antes do rito'
    current['extras'] = dict(preaudit_contract_sha256=contract_meta['sha256'], signature='codex-gerente-tgl, claim845',
        previous_spec_preserved=old, previous_source_preserved=prior_source)
    current['erratas'].append(dict(ao_lado_de='contrato historico v394 anterior ao bundle R7',
        agora='A copia nova cobra seu fecho exato com o parser completo. O contrato anterior e seus bytes ficam preservados como historia; a rodada nova nao revalida sua contagem antiga.',
        estatuto='[DERIVED] expectativa medida previamente',assinatura='codex-gerente-tgl, F1.FECHO_20261015'))
    specs[i] = current
    sources['kh_n1_v394'] = dict(arquivo=contract_meta['path'], bytes=contract_meta['bytes'], sha256=contract_meta['sha256'],
        papel='Pre-auditoria imutavel da copia v394 network R7; anterior ao rito')
    lines = raw.decode('utf-8').splitlines(keepends=True)
    for name,value in sorted([('_V393_SPECS',specs),('_V393_FONTES',sources)],key=lambda row:nodes[row[0]].lineno,reverse=True):
        node = nodes[name]
        lines[node.lineno-1:node.end_lineno] = [name+' = '+repr(value)+'\n']
    result = ''.join(lines).encode('utf-8')
    updated = ast.parse(result)
    assert {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)} == {
        n.name:ast.dump(n,include_attributes=False) for n in updated.body if isinstance(n,ast.FunctionDef)}
    assert audit.embedded(result) == bodies
    return result


def main():
    assert not DEST.exists() and not CONTRACT.exists()
    contract = measured_contract()
    contract_meta = new(CONTRACT,contract)
    source = audit.read(contract['candidate_before_patch'])
    raw = compose(source,contract,contract_meta)
    path = DEST/'um_v394_prechecked.py'
    new(path,raw.decode('utf-8'))
    new(DEST/'RECEIPT.json',dict(candidate=pin(path), source=contract['candidate_before_patch'],
        contract=contract_meta, script=pin(__file__), embedded_sources_unchanged=True,
        runtime_functions_unchanged=True, status='CONSTRUCTED_PENDING_REVIEW_AND_MAIN', production_modified=False))
    print(json.dumps(dict(candidate=pin(path),contract=contract_meta),ensure_ascii=False))


if __name__ == '__main__':
    main()
