"""Integrate a recompiled network bundle into a new standalone candidate only."""
import ast
import hashlib
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r4'


def main():
    revision = sys.argv[1]
    plan_path = BUNDLE/('PLAN.json' if revision == 'R1' else 'PLAN_'+revision+'.json')
    plan = json.loads(plan_path.read_bytes())
    compiled_path = BUNDLE/('COMPILED_'+revision+'.json')
    compiled = json.loads(compiled_path.read_bytes())
    assert compiled['passed'] and compiled['plan'] == pin(plan_path)
    expected_modules = {row['module']:row['transposed_source'] for row in plan['modules']}
    assert len(expected_modules) == len(plan['modules']) and expected_modules
    assert plan['audit_module'] not in expected_modules
    expected_modules[plan['audit_module']] = plan['audit']
    compiled_modules = compiled['modules']
    assert isinstance(compiled_modules,list) and len(compiled_modules) == len(expected_modules)
    actual_modules = {row['module']:row for row in compiled_modules}
    assert len(actual_modules) == len(compiled_modules) and set(actual_modules) == set(expected_modules)
    for name, source_pin in expected_modules.items():
        assert actual_modules[name]['source'] == source_pin
    audit_report = actual_modules[plan['audit_module']]['axiom_report']
    assert set(audit_report) == set(plan['theorems']) and audit_report
    assert all(set(v) <= {'propext','Classical.choice','Quot.sound'} for v in audit_report.values())
    dest = OUT/'candidate_r4'
    assert not dest.exists() and not (OUT/'INTEGRATION_NETWORK_R4.json').exists()
    baseline = OUT/'candidate_r3/um.py'
    raw = baseline.read_bytes()
    tree = ast.parse(raw.decode('utf-8'))
    offsets, total = [], 0
    for line in raw.splitlines(keepends=True):
        offsets.append(total)
        total += len(line)
    assignments = {n.targets[0].id:n for n in tree.body
                   if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    functions = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
    edits = []

    def span(node):
        return offsets[node.lineno-1]+node.col_offset, offsets[node.end_lineno-1]+node.end_col_offset

    def replace(node, value):
        a, b = span(node)
        edits.append((a, b, value.encode('utf-8')))

    def append_dict(node, values):
        a, b = span(node)
        assert raw[b-1:b] == b'}'
        comma = ',\n' if node.keys and raw[a:b-1].rstrip()[-1:] != b',' else '\n'
        edits.append((b-1, b-1, (comma+''.join('    '+repr(k)+': '+repr(v)+',\n' for k,v in values.items())).encode('utf-8')))

    embedded_node = assignments['_EMBEDDED_KERNEL_FILES'].value
    embedded = ast.literal_eval(embedded_node)
    added = {}
    sources = {}
    for row in plan['modules']:
        path = Path(row['transposed_source']['path'])
        assert pin(path) == row['transposed_source']
        assert row['relative'] not in embedded
        added[row['relative']] = path.read_text(encoding='utf-8')
        sources[row['relative']] = pin(path)['sha256']
    audit_path = Path(plan['audit']['path'])
    assert pin(audit_path) == plan['audit']
    audit_rel = plan.get('audit_relative', 'TGLExt/F1Fecho394/NetworkProofAudit.lean')
    added[audit_rel] = audit_path.read_text(encoding='utf-8')
    sources[audit_rel] = pin(audit_path)['sha256']
    for result in compiled['modules']:
        assert result['passed'] and result['exit_code'] == 0
        assert pin(result['source']['path']) == result['source']
        assert pin(result['object']['path']) == result['object']
        assert all(set(v) <= {'propext','Classical.choice','Quot.sound'} for v in result['axiom_report'].values())
    glue = 'import '+plan['audit_module']+'\n'
    replacements = {'TGLExt.lean':embedded['TGLExt.lean']+'\n'+glue,
                    'TGL/Audit.lean':glue+'\n'+embedded['TGL/Audit.lean']}
    for key, value in zip(embedded_node.keys, embedded_node.values):
        if isinstance(key, ast.Constant) and key.value in replacements:
            replace(value, repr(replacements[key.value]))
    append_dict(embedded_node, added)
    old_theorem_flags = ast.literal_eval(assignments['_LEAN_THEOREM_FLAGS'].value)
    declarations = sorted(set(plan['theorems'])-set(old_theorem_flags.values()))
    assert declarations
    flags = {f'ext_net394_{i:04d}':name for i,name in enumerate(declarations, 1)}
    assert not set(flags) & set(old_theorem_flags)
    append_dict(assignments['_LEAN_THEOREM_FLAGS'].value, flags)
    ladder = next(n.value for n in functions['prove_external_ladder'].body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'ext_flags' for t in n.targets))
    old_flags = ast.literal_eval(ladder)
    assert len(old_flags) == len(set(old_flags)) == 7171
    a, b = span(ladder)
    edits.append((b-1, b-1, ''.join('        '+repr(k)+',\n' for k in flags).encode('utf-8')))
    expected = len(old_flags)+len(flags)
    for name in ('_V394_FORMAL_CONTRACT', '_V394_QUADRATIC_CONTRACT'):
        value = ast.literal_eval(assignments[name].value)
        assert value['expected_ladder'] == 7171
        value['expected_ladder'] = expected
        replace(assignments[name].value, repr(value))
    contract = dict(declarations=declarations, source_sha256=sources, expected_ladder=expected,
        baseline_candidate=pin(baseline), bundle_plan=pin(plan_path),
        constructed_components=['existing one-particle wedge and partial Fourier',
            'same bosonic Fock, exponential vectors and totality',
            'regular Weyl operators, CCR, locality and boost covariance',
            'cyclic and separating vacuum of the standard wedge algebra',
            'closed dense involutive Tomita operator of the actual algebra-vacuum pair',
            'Gamma(J) intertwining and closed dense positive exponential lift',
            'closed dense involutive exponential Tomita candidate, pair identification still open',
            'actual Fock wedge covariant core, faithful embedding and dual action'],
        open_joint_contract=['global localization and joint physical device realization',
            'identification of the pair polar factors with second quantization and KMS',
            'modular weight and scaled trace on the actual Fock crossed product',
            'joint nontrivial Maxwell/stress realization and all-directions H3'])
    runtime = OUT/'network_runtime_r1.py'
    chunk = '\n_V394_NETWORK_CONTRACT = '+repr(contract)+'\n\n'+runtime.read_text(encoding='utf-8')+'\n\n'
    pos = offsets[functions['main'].lineno-1]
    edits.append((pos, pos, chunk.encode('utf-8')))
    hook = b'    _figs = emit_figures(core)'
    assert raw.count(hook) == 1
    pos = raw.index(hook)
    edits.append((pos, pos, b'    _network_result = rede_fock_v394(core)\n    print("   [v394] rede Fock: %s" % _network_result["verdict"])\n'))
    seal = b'            "regra_quadratica_v394": '
    assert raw.count(seal) == 1
    pos = raw.index(b'\n', raw.index(seal))+1
    edits.append((pos, pos, b'            "rede_fock_v394": {k_: (core.get("rede_fock_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "exact_ladder", "constructed_components", "open_joint_contract", "whole_certificate_inhabited", "scope", "does_not_gate_core")},\n'))
    article = functions['_v394_article_tex']
    marker = next(n for n in article.body if isinstance(n, ast.Assert))
    pos = offsets[marker.lineno-1]
    paragraph = '''    network = core.get('rede_fock_v394') or {}
    block += ('Rede Fock nesta rodada: ' if pt else 'Fock network in this run: ') + esc(network.get('verdict', 'NOT_RUN')) + '.\\n'
    block += ('A mesma realizacao Fock fornece Weyl/CCR, algebra R(K), vacuo ciclico e separante e Tomita fechado do par. A identificacao polar, KMS e o contrato fisico conjunto continuam explicitos; este resultado certifica componentes.\\n' if pt else 'The same Fock realization supplies Weyl/CCR, R(K), a cyclic and separating vacuum, and the closed pair Tomita operator. Polar identification, KMS and the joint physical contract remain explicit; this result certifies components.\\n')
'''
    edits.append((pos, pos, paragraph.encode('utf-8')))
    # Integrate the independently reviewed offline MiKTeX correction exactly.
    pdf_receipt = OUT/'full_rite/pdf_patch_r2/PDF_PATCH_RECEIPT_R2.json'
    pdf = json.loads(pdf_receipt.read_bytes())
    assert pdf['baseline_source'] == pin(baseline)
    ast_hash = hashlib.sha256(ast.dump(functions['compile_pdf'], include_attributes=False).encode()).hexdigest()
    assert ast_hash == pdf['baseline_function_ast_sha256']
    pdf_source = Path(pdf['replacement']['path'])
    assert pin(pdf_source) == pdf['replacement']
    review_path = OUT/'full_rite/pdf_patch_review/REVISAO_PDF_R2_R1.json'
    review = json.loads(review_path.read_bytes())
    assert review['verdict'] == 'PASSA_COM_ESCOPO_MIKTEX_LOCAL' and not review['material_findings']
    replace(functions['compile_pdf'], pdf_source.read_text(encoding='utf-8').rstrip())
    # The execution file may have an additive filename. Its logical seal key
    # remains um.py while the measured bytes are always the executed file.
    identity_targets = []
    for node in ast.walk(functions['main']):
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'f':
            try:
                values = ast.literal_eval(node.iter)
            except (ValueError, TypeError):
                continue
            if isinstance(values, (tuple, list)) and 'um.py' in values:
                for child in ast.walk(node):
                    if isinstance(child, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'p' for t in child.targets):
                        if ast.unparse(child.value) == 'os.path.join(OUT, f)':
                            identity_targets.append(child.value)
    assert len(identity_targets) == 1, 'Unexpected self-identity loop; inspect rather than patch broadly'
    replace(identity_targets[0], "os.path.abspath(__file__) if f == 'um.py' else os.path.join(OUT, f)")
    previous = len(raw)+1
    for a,b,value in sorted(edits, reverse=True):
        assert b <= previous, ('overlapping edit', a,b,previous)
        raw = raw[:a]+value+raw[b:]
        previous = a
    updated = ast.parse(raw.decode('utf-8'))
    old_functions = {n.name:ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)}
    new_functions = {n.name:ast.dump(n, include_attributes=False) for n in updated.body if isinstance(n, ast.FunctionDef)}
    changed = sorted(k for k,v in old_functions.items() if new_functions.get(k) != v)
    assert changed == ['_v394_article_tex', 'compile_pdf', 'main', 'prove_external_ladder']
    assert pin(baseline) == contract['baseline_candidate']
    dest.mkdir()
    new(dest/'um.py', raw.decode('utf-8'))
    all_sources = {**embedded, **replacements, **added}
    for rel, body in all_sources.items():
        target = dest/'tgl_kernel'/rel
        assert target.resolve().is_relative_to((dest/'tgl_kernel').resolve())
        new(target, body)
    receipt = dict(unit='F1.FECHO_20261015', claim_event=845,
        candidate=pin(dest/'um.py'), baseline=pin(baseline), script=pin(__file__),
        runtime=pin(runtime), bundle_plan=pin(plan_path), compiled_bundle=pin(compiled_path),
        pdf_patch=pin(pdf_receipt), pdf_review=pin(review_path),
        self_identity_review=pin(OUT/'full_rite/SELF_IDENTITY_EXPANDED_BASELINE_R3.json'),
        new_flags=flags, expected_ladder=expected, embedded_source_count=len(all_sources),
        changed_existing_functions=changed,
        status='CONSTRUCTED_PENDING_INDEPENDENT_REVIEW_AND_FULL_RITE',
        whole_certificate_inhabited=False, canonical_unchanged=True)
    new(OUT/'INTEGRATION_NETWORK_R4.json', receipt)
    print(json.dumps({k:receipt[k] for k in ('candidate','expected_ladder','embedded_source_count','changed_existing_functions')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
