"""Add new verified roots beside a pinned bundle, preserving its original plan."""
import datetime as dt
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
REDE = OUT.parent/'F1.REDE'
BUNDLE = OUT/'network_bundle_r4'
PREFIX = 'TGLExt.F1Fecho394.'
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}


def imports(body):
    return re.findall(r'^import[ \t]+([\w.]+)[ \t]*$', body, re.M)


def main():
    revision, *roots = sys.argv[1:]
    assert re.fullmatch(r'R[2-9][0-9]*', revision) and roots
    plan_path = BUNDLE/('PLAN_'+revision+'.json')
    assert not plan_path.exists()
    base = json.loads((BUNDLE/'PLAN.json').read_bytes())
    old = {m['name']: m for m in base['modules']}
    chosen, visiting, ordered = {}, set(), []

    def resolve(name):
        if name.startswith(('TGLExt.', 'Mathlib.', 'Lean.', 'Std.', 'Batteries.')) or name in old or name in chosen:
            return
        assert name not in visiting, ('cycle', name)
        visiting.add(name)
        paths = [p for root in (REDE, OUT) for p in root.glob('*/'+name+'.lean')
                 if 'review' not in p.parent.name]
        assert len(paths) == 1, (name, paths)
        source = paths[0]
        choices = []
        for rec in (source.parent/'attempts').glob('*/RECEIPT.json'):
            data = json.loads(rec.read_bytes())
            if data.get('exit_code') != 0:
                continue
            snap = rec.parent/source.name
            obj = snap.with_suffix('.olean')
            if snap.exists() and obj.exists() and pin(snap)['sha256'] == pin(source)['sha256']:
                choices.append((rec, data, obj))
        assert choices, ('no accepted build', name)
        rec, data, obj = sorted(choices)[-1]
        log = rec.parent/'AXIOMS.txt'
        if not log.exists():
            log = rec.parent/'STDOUT.log'
        raw = log.read_text(encoding='utf-8')
        assert 'sorryAx' not in raw
        reports = {}
        for decl, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", raw, re.S):
            reports[decl] = [v.strip() for v in values.split(',') if v.strip()]
        for decl in re.findall(r"'([^']+)' does not depend on any axioms", raw):
            reports[decl] = []
        assert reports and all(set(v) <= TRIO for v in reports.values())
        body = source.read_text(encoding='utf-8')
        assert not re.search(r'(?m)^\s*(?:axiom|sorry)\b', body)
        for dep in imports(body):
            resolve(dep)
        chosen[name] = dict(name=name, source=pin(source), receipt=pin(rec),
                            object=pin(obj), axiom_report=reports, body=body)
        visiting.remove(name)
        ordered.append(name)

    for root in roots:
        resolve(root)
    assert ordered, 'No new component; do not duplicate a revision'
    added = []
    for name in ordered:
        row = chosen[name]
        body = row.pop('body')
        def replace(match):
            dep = match.group(1)
            return 'import '+(PREFIX+dep if dep in old or dep in chosen else dep)
        transposed = re.sub(r'^import[ \t]+([\w.]+)[ \t]*$', replace, body, flags=re.M)
        restored = re.sub(r'^import '+re.escape(PREFIX)+r'([\w.]+)[ \t]*$', r'import \1', transposed, flags=re.M)
        normalized = re.sub(r'^import[ \t]+([\w.]+)[ \t]*$', r'import \1', body, flags=re.M)
        assert restored == normalized
        rel = (PREFIX+name).replace('.', '/')+'.lean'
        path = BUNDLE/'src'/rel
        new(path, transposed)
        row.update(relative=rel, module=PREFIX+name, transposed_source=pin(path))
        added.append(row)
    names = set(base['theorems'])
    for row in added:
        names.update(n for n in row['axiom_report'] if not n.startswith('_private.'))
    all_roots = list(dict.fromkeys(base['roots']+roots))
    audit_name = 'NetworkProofAudit'+revision
    audit = ''.join('import '+PREFIX+n+'\n' for n in all_roots)
    audit += '\n'+'\n'.join('#print axioms '+n for n in sorted(names))+'\n'
    audit_path = BUNDLE/'src/TGLExt/F1Fecho394'/(audit_name+'.lean')
    new(audit_path, audit)
    plan = dict(base, created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                original_plan=pin(BUNDLE/'PLAN.json'), script=pin(__file__),
                roots=all_roots, modules=base['modules']+added,
                audit=pin(audit_path), audit_module=PREFIX+audit_name,
                audit_relative='TGLExt/F1Fecho394/'+audit_name+'.lean',
                theorems=sorted(names), revision=revision)
    new(plan_path, plan)
    print(json.dumps(dict(added=len(added), declarations=len(names), plan=pin(plan_path)), ensure_ascii=False))


if __name__ == '__main__':
    main()
