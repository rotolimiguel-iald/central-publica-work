"""Transpose verified local Lean modules into a new, immutable kernel bundle.

Only import paths change. Original bodies/receipts are pinned, old attempts
remain intact, and the transposed graph must compile before program integration.
No original program, kernel, board, memory or provider is touched.
"""
import ast
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
REDE = OUT.parent/'F1.REDE'
DEST = OUT/'network_bundle_r4'
PREFIX = 'TGLExt.F1Fecho394.'
ROOT_MODULES = ['CanonicalWeylAssemblyR5', 'CanonicalWedgeFlowR2',
                'WedgePairTomitaR2', 'WeylAntiunitaryR4', 'OneParticleSymplecticR2',
                'ExponentialLiftR2', 'MaxwellBoostChargeAssemblyR1']
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}


def imports(body):
    return re.findall(r'^import\s+([\w.]+)\s*$', body, re.M)


def main():
    if DEST.exists():
        raise FileExistsError('Bundle already attempted: recover, never overwrite')
    chosen, active, ordered = {}, set(), []

    def resolve(name):
        if name.startswith(('TGLExt.', 'Mathlib.', 'Lean.', 'Std.', 'Batteries.')):
            return
        if name in chosen:
            return
        if name in active:
            raise ValueError(('import cycle', name))
        active.add(name)
        sources = [p for root in (REDE, OUT) for p in root.glob('*/'+name+'.lean')
                   if 'review' not in p.parent.name]
        if len(sources) != 1:
            raise ValueError(('source ambiguity', name, [str(p) for p in sources]))
        source = sources[0]
        source_pin = pin(source)
        choices = []
        for rec in (source.parent/'attempts').glob('*/RECEIPT.json'):
            data = json.loads(rec.read_bytes())
            if data.get('exit_code') != 0:
                continue
            if data.get('source', {}).get('sha256', data.get('source_sha256')) == source_pin['sha256']:
                choices.append((rec, data))
        if not choices:
            raise RuntimeError(('no accepted source compilation', name))
        rec, data = sorted(choices)[-1]
        snap = rec.parent/(name+'.lean')
        binary = rec.parent/(name+'.olean')
        if pin(snap)['sha256'] != source_pin['sha256'] or not binary.exists():
            raise ValueError(('source/object custody failed', name))
        raw = (rec.parent/'AXIOMS.txt').read_text(encoding='utf-8')
        if 'sorryAx' in raw or re.search(r'(?m)^\s*(?:sorry|axiom)\b', source.read_text(encoding='utf-8')):
            raise ValueError(('unaccepted axioms', name))
        reports = {}
        for theorem, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", raw, re.S):
            reports[theorem] = [v.strip() for v in values.split(',') if v.strip()]
        for theorem in re.findall(r"'([^']+)' does not depend on any axioms", raw):
            reports[theorem] = []
        for line in raw.splitlines():
            cols = line.split('\t')
            if len(cols) >= 3 and cols[0] in ('LOCAL_DECL', 'BENCH_DECL'):
                reports[cols[1]] = [v for v in cols[-1].split(',') if v]
        if not all(set(v) <= TRIO for v in reports.values()):
            raise ValueError(('axiom report outside trio', name))
        body = source.read_text(encoding='utf-8')
        for dep in imports(body):
            resolve(dep)
        chosen[name] = dict(name=name, source=source_pin, receipt=pin(rec),
                            object=pin(binary), axiom_report=reports, original_body=body)
        active.remove(name)
        ordered.append(name)

    for root in ROOT_MODULES:
        resolve(root)
    baseline = OUT/'candidate_r3/um.py'
    tree = ast.parse(baseline.read_text(encoding='utf-8'))
    assignments = {n.targets[0].id: n.value for n in tree.body
                   if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    embedded = ast.literal_eval(assignments['_EMBEDDED_KERNEL_FILES'])
    old_names = set(ast.literal_eval(assignments['_LEAN_THEOREM_FLAGS']).values())
    modules, theorem_names = [], set()
    for name in ordered:
        data = chosen[name]
        body = data.pop('original_body')
        def replace_import(match):
            dep = match.group(1)
            return 'import '+(PREFIX+dep if dep in chosen else dep)
        transposed = re.sub(r'^import\s+([\w.]+)\s*$', replace_import, body, flags=re.M)
        # Exact reconstruction guards against any body edit beyond module imports.
        restored = re.sub(r'^import '+re.escape(PREFIX)+r'([\w.]+)\s*$',
                          r'import \1', transposed, flags=re.M)
        normalized = re.sub(r'^import\s+([\w.]+)\s*$', r'import \1', body, flags=re.M)
        if restored != normalized:
            raise AssertionError(('body changed', name))
        rel = (PREFIX+name).replace('.', '/')+'.lean'
        if rel in embedded:
            raise ValueError(('module collision', rel))
        path = DEST/'src'/rel
        new(path, transposed)
        data.update(relative=rel, module=PREFIX+name, transposed_source=pin(path))
        modules.append(data)
        theorem_names.update(n for n in data['axiom_report']
                             if not n.startswith('_private.') and n not in old_names)
    if not theorem_names:
        raise ValueError('No explicit proof obligations in bundle')
    # Audit all named exposed declarations after transposition, without assuming
    # the old object files remain valid under a different module identity.
    audit_body = ''.join('import '+PREFIX+n+'\n' for n in ROOT_MODULES)
    audit_body += '\n'+'\n'.join('#print axioms '+n for n in sorted(theorem_names))+'\n'
    audit_path = DEST/'src/TGLExt/F1Fecho394/NetworkProofAudit.lean'
    new(audit_path, audit_body)
    new(DEST/'PLAN.json', dict(unit='F1.FECHO_20261015', claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), baseline=pin(baseline),
        script=pin(__file__), roots=ROOT_MODULES, modules=modules, audit=pin(audit_path),
        audit_module='TGLExt.F1Fecho394.NetworkProofAudit', theorems=sorted(theorem_names),
        status='TRANSPOSED_PENDING_COMPILATION_AND_INDEPENDENT_REVIEW',
        scope='Existing Fock, actual Weyl algebra, wedge standard vacuum and closed pair Tomita; polar identification remains separate.',
        production_modified=False))
    print(json.dumps({'modules':len(modules), 'theorems':len(theorem_names),
                      'plan':pin(DEST/'PLAN.json')},ensure_ascii=False))


if __name__ == '__main__':
    main()
