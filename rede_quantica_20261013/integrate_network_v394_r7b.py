"""Integrate only a completed, checked isolated bundle into a NEW candidate.

The previous main and immutable candidates remain untouched. This operation
does not execute the program, install production, or claim a joint inhabitant.
"""
import ast
import hashlib
import json
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r7'
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}


def main():
    plan_path, compiled_path = BUNDLE/'PLAN.json', BUNDLE/'COMPILED_R1.json'
    plan, compiled = json.loads(plan_path.read_bytes()), json.loads(compiled_path.read_bytes())
    assert compiled['passed'] is True and compiled['plan'] == pin(plan_path)
    expected = {r['module']: r['transposed_source'] for r in plan['modules']}
    expected[plan['audit_module']] = plan['audit']
    rows = {r['module']: r for r in compiled['modules']}
    assert len(rows) == len(compiled['modules']) and set(rows) == set(expected)
    for name, source in expected.items():
        r = rows[name]
        assert r['passed'] is True and r['source'] == source == pin(source['path'])
        assert pin(r['object']['path']) == r['object']
        assert r.get('reused') is True or (type(r['exit_code']) is int and r['exit_code'] == 0)
        assert all(set(v) <= TRIO for v in r['axiom_report'].values())
    audit_row = rows[plan['audit_module']]
    report = audit_row['axiom_report']
    assert report and len(report) == compiled['all_local_declarations']
    log = Path(audit_row['stdout']['path'])
    assert pin(log) == audit_row['stdout']
    current_sources, logged_axioms = {}, {}
    for line in log.read_text(encoding='utf-8').splitlines():
        cols = line.split('\t')
        if len(cols) == 4 and cols[0] == 'BUNDLE_DECL':
            assert cols[1] not in current_sources
            current_sources[cols[1]] = cols[2].replace('.', '/')+'.lean'
            logged_axioms[cols[1]] = [v for v in cols[3].split(',') if v]
            assert set(logged_axioms[cols[1]]) <= TRIO, ('audit log outside trio', cols[1])
    assert set(current_sources) == set(report)
    assert logged_axioms == report, 'Audit transcript and receipt disagree'
    baseline = OUT/'full_rite/reconciliation_candidate_r3/um_v394_reconciled.py'
    assert pin(baseline) == plan['baseline']
    destination = OUT/'candidate_r7'
    assert not destination.exists() and not (OUT/'INTEGRATION_NETWORK_R7.json').exists()
    raw = baseline.read_bytes()
    tree = ast.parse(raw)
    offsets, total = [], 0
    for line in raw.splitlines(keepends=True):
        offsets.append(total)
        total += len(line)
    assignments = {n.targets[0].id: n for n in tree.body
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    edits = []

    def replace(node, text):
        a = offsets[node.lineno-1]+node.col_offset
        b = offsets[node.end_lineno-1]+node.end_col_offset
        edits.append((a, b, text.encode('utf-8')))

    def set_assignment(name, value):
        replace(assignments[name].value, repr(value))

    embedded = ast.literal_eval(assignments['_EMBEDDED_KERNEL_FILES'].value)
    original_embedded = dict(embedded)
    source_rows = list(plan['modules'])+[dict(relative=plan['audit_relative'], transposed_source=plan['audit'])]
    added = []
    for row in source_rows:
        path = Path(row['transposed_source']['path'])
        body = path.read_bytes().decode('utf-8')
        rel = row['relative']
        if rel in embedded:
            assert embedded[rel] == body, ('existing source changed', rel)
        else:
            embedded[rel] = body
            added.append(rel)
    glue = 'import '+plan['audit_module']+'\n'
    assert glue not in embedded['TGLExt.lean'] and glue not in embedded['TGL/Audit.lean']
    embedded['TGLExt.lean'] += '\n'+glue
    embedded['TGL/Audit.lean'] = glue+'\n'+embedded['TGL/Audit.lean']
    set_assignment('_EMBEDDED_KERNEL_FILES', embedded)
    old_flags = ast.literal_eval(assignments['_LEAN_THEOREM_FLAGS'].value)
    public = {n for n in report if not n.startswith('_private.')}
    new_names = sorted(public-set(old_flags.values()))
    assert new_names
    new_flags = {f'ext_net394r7_{i:05d}': name for i, name in enumerate(new_names, 1)}
    assert not set(new_flags) & set(old_flags)
    set_assignment('_LEAN_THEOREM_FLAGS', {**old_flags, **new_flags})
    ladder = next(n.value for n in functions['prove_external_ladder'].body if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == 'ext_flags' for t in n.targets))
    old_ladder = ast.literal_eval(ladder)
    assert len(old_ladder) == len(set(old_ladder)) == 8107
    replace(ladder, repr(old_ladder+list(new_flags)))
    expected_ladder = len(old_ladder)+len(new_flags)
    for name in ('_V394_FORMAL_CONTRACT', '_V394_QUADRATIC_CONTRACT'):
        v = ast.literal_eval(assignments[name].value)
        assert v['expected_ladder'] == len(old_ladder)
        v['expected_ladder'] = expected_ladder
        set_assignment(name, v)
    stones = ast.literal_eval(assignments['_ESQUELETO_STONES'].value)
    present = {x[2] for x in stones}
    for path in sorted(added):
        if path not in present:
            stones.append(('v394', Path(path).stem, path, None, None))
    set_assignment('_ESQUELETO_STONES', stones)
    old_contract = ast.literal_eval(assignments['_V394_NETWORK_CONTRACT'].value)
    source_inventory = OUT/'full_rite/declaration_sources_r3/DECLARATION_SOURCES.json'
    previous_sources = json.loads(source_inventory.read_bytes())
    declarations = sorted(set(old_contract['declarations']) | public)
    declarations_to_sources = {n: current_sources.get(n, previous_sources.get(n)) for n in declarations}
    assert all(isinstance(p, str) and p in embedded for p in declarations_to_sources.values())
    source_paths = set(old_contract['source_sha256']) | set(added) | set(declarations_to_sources.values())
    source_hashes = {p: hashlib.sha256(embedded[p].encode()).hexdigest() for p in sorted(source_paths)}
    contract = dict(declarations=declarations, declaration_sources=declarations_to_sources,
        source_sha256=source_hashes, expected_ladder=expected_ladder,
        baseline_candidate=pin(baseline), bundle_plan=pin(plan_path), compiled_bundle=pin(compiled_path),
        historical_source_inventory=pin(source_inventory),
        constructed_components=[
            'Original H1, partial Fourier, standard geometric wedge and bosonic Fock',
            'Exponential vectors, totality, regular Weyl/CCR and the concrete wedge algebra',
            'Cyclic/separating vacuum and actual closed pair Tomita equal to the exponential closure',
            'Actual positive self-adjoint half-modular factor and Delta=S-dagger-S on its genuine domain',
            'CFC modular flow equals Gamma(B0(-2*pi*t)) on the entire same Fock, including vacuum',
            'Concrete full-wedge KMS for physical Gamma(B0(2*pi*t)), and no-fixed/positive-energy terms',
            'Faithful regular crossed-product embedding, dual action, semifinite faithful invariant dual weight',
            'Actual weight GNS representation and closed uniform adjunction core; directed-positive normality',
            'Strongly continuous scalar spatial orthogonal action on original H1, covariant with U1',
            'Concrete annihilation on dense invariant exponential domain, with a nonzero-action witness'],
        open_joint_contract=[
            'Full Lorentz/helicity representation, global localization, and physical device/clock identification',
            'Full finite-weight adjunction graph, its modular identification, distinct scaled trace and PF split',
            'Joint nontrivial Maxwell field/stress source and all-directions H3 scope',
            'A joint inhabitant of CanonicalNetInput and the remaining twenty-one trace/PF interface fields'])
    set_assignment('_V394_NETWORK_CONTRACT', contract)
    runtime = OUT/'network_runtime_r2.py'
    rt = ast.parse(runtime.read_text(encoding='utf-8'))
    fn = next(n for n in rt.body if isinstance(n, ast.FunctionDef) and n.name == 'rede_fock_v394')
    replace(functions['rede_fock_v394'], ast.get_source_segment(runtime.read_text(encoding='utf-8'), fn))
    article = ast.get_source_segment(raw.decode('utf-8'), functions['_v394_article_tex'])
    lines = article.splitlines()
    targets = [i for i,line in enumerate(lines) if "block += ('A mesma realizacao Fock" in line]
    assert len(targets) == 1
    lines[targets[0]] = "    block += ('Na mesma Fock, o Tomita real, seu quadrado e o fluxo modular foram ligados a Gamma(B0(-2 pi t)); KMS da cunha e fornecido por termo. Rede global de helicidade, traco escalado e fonte Maxwell conjuntos continuam abertos. Resultados de versoes anteriores preservam seus alcances historicos.\\n' if pt else 'On the same Fock, the actual Tomita, its square and modular flow are identified with Gamma(B0(-2 pi t)); wedge KMS is a theorem. The joint global helicity net, scaled trace and Maxwell source remain open. Earlier-version results retain their historical scope.\\n')"
    replace(functions['_v394_article_tex'], '\n'.join(lines))
    previous = len(raw)+1
    for a,b,value in sorted(edits, reverse=True):
        assert b <= previous
        raw = raw[:a]+value+raw[b:]
        previous = a
    updated = ast.parse(raw)
    old_functions = {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, ast.FunctionDef)}
    new_functions = {n.name: ast.dump(n, include_attributes=False) for n in updated.body if isinstance(n, ast.FunctionDef)}
    changed = sorted(k for k,v in old_functions.items() if new_functions.get(k) != v)
    assert changed == ['_v394_article_tex', 'prove_external_ladder', 'rede_fock_v394']
    assert all(embedded[k] == v for k,v in original_embedded.items() if k not in {'TGLExt.lean','TGL/Audit.lean'})
    assert pin(baseline) == plan['baseline']
    new(destination/'um_v394_integrated.py', raw.decode('utf-8'))
    for rel, body in embedded.items():
        target = destination/'tgl_kernel'/rel
        assert target.resolve().is_relative_to((destination/'tgl_kernel').resolve())
        new(target, body)
    result = dict(unit='F1.FECHO_20261015', claim_event=845, candidate=pin(destination/'um_v394_integrated.py'),
        baseline=pin(baseline), compiled_bundle=pin(compiled_path), bundle_plan=pin(plan_path),
        script=pin(__file__), runtime=pin(runtime), new_flags=new_flags,
        expected_ladder=expected_ladder, source_count=len(embedded), added_sources=added,
        changed_existing_functions=changed, original_scientific_bodies_unchanged=True,
        status='CONSTRUCTED_PENDING_INDEPENDENT_REVIEW_AND_FULL_RITE',
        whole_certificate_inhabited=False, production_modified=False)
    new(OUT/'INTEGRATION_NETWORK_R7.json', result)
    print(json.dumps({k:result[k] for k in ('candidate','expected_ladder','source_count','changed_existing_functions')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
