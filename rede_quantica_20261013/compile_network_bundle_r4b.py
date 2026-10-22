"""Compile the transposed network graph without writing any canonical cache.

Each attempt is exclusive. Resume consumes only a successful matching receipt,
including current dependency hashes; failure or an incomplete attempt is visible.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r4'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}


def main():
    revision = sys.argv[1] if len(sys.argv)>1 else 'R1'
    assert re.fullmatch(r'R[1-9][0-9]*', revision)
    plan_path = BUNDLE/('PLAN.json' if revision == 'R1' else 'PLAN_'+revision+'.json')
    plan = json.loads(plan_path.read_bytes())
    roots = [BUNDLE/'lib', KERNEL/'.lake/build/lib/lean']
    roots += sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))
    roots += [LEAN.parent.parent/'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots)))
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    modules = plan['modules']+[dict(module=plan['audit_module'],
        transposed_source=plan['audit'], relative=plan.get('audit_relative','TGLExt/F1Fecho394/NetworkProofAudit.lean'))]
    outputs = []
    for row in modules:
        src = Path(row['transposed_source']['path'])
        assert pin(src) == row['transposed_source']
        rel = Path(row['relative'])
        binary = (BUNDLE/'lib'/rel).with_suffix('.olean')
        receipt = BUNDLE/'builds'/(rel.stem+'.json')
        if receipt.exists():
            done = json.loads(receipt.read_bytes())
            assert done['passed'] and done['source'] == pin(src)
            assert done['object'] == pin(binary)
            assert all(pin(Path(p['path'])) == p for p in done['dependencies'])
            outputs.append(done)
            print('REUSED '+row['module'], flush=True)
            continue
        if binary.exists():
            raise FileExistsError(('unreceipted output; preserve and investigate', str(binary)))
        d = BUNDLE/'builds'/(rel.stem+'_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
        d.mkdir(parents=True, exist_ok=False)
        binary.parent.mkdir(parents=True, exist_ok=True)
        command = [str(LEAN), '-R', str(BUNDLE/'src'), '-o', str(binary), str(src)]
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        t0 = time.perf_counter()
        print('BUILD_START '+row['module'], flush=True)
        p = subprocess.run(command, cwd=BUNDLE/'src', env=env, capture_output=True)
        elapsed = time.perf_counter()-t0
        end = dt.datetime.now(dt.timezone.utc).isoformat()
        stdout = p.stdout.decode('utf-8', errors='strict')
        stderr = p.stderr.decode('utf-8', errors='strict')
        reports = {}
        for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", stdout, re.S):
            reports[name] = [v.strip() for v in values.split(',') if v.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", stdout):
            reports[name] = []
        for line in stdout.splitlines():
            cols = line.split('\t')
            if len(cols) >= 3 and cols[0] in ('LOCAL_DECL', 'BENCH_DECL'):
                reports[cols[1]] = [v for v in cols[-1].split(',') if v]
        new(d/'STDOUT.log', stdout)
        new(d/'STDERR.log', stderr)
        passed = p.returncode == 0 and 'sorryAx' not in stdout and all(set(v) <= TRIO for v in reports.values())
        result = dict(module=row['module'], source=pin(src), command=command,
            cwd=str(BUNDLE/'src'), LEAN_PATH=env['LEAN_PATH'], toolchain=version,
            start_utc=start, end_utc=end, seconds=elapsed, exit_code=p.returncode,
            passed=passed, axiom_report=reports, stdout=pin(d/'STDOUT.log'),
            stderr=pin(d/'STDERR.log'), dependencies=[r['object'] for r in outputs],
            production_modified=False, script=pin(__file__))
        if p.returncode == 0:
            result['object'] = pin(binary)
        new(d/'BUILD_RECEIPT.json', result)
        print(json.dumps({'module':row['module'], 'exit':p.returncode,
                          'seconds':elapsed, 'receipt':str(d/'BUILD_RECEIPT.json')}, ensure_ascii=False), flush=True)
        if not passed:
            raise RuntimeError(('compile failed; original attempt retained', str(d)))
        new(receipt, result)
        outputs.append(result)
    audit = outputs[-1]['axiom_report']
    assert set(plan['theorems']) <= set(audit)
    new(BUNDLE/('COMPILED_'+revision+'.json'), dict(passed=True, plan=pin(plan_path),
        modules=outputs, explicit_axioms=len(audit), expected_theorems=len(plan['theorems']),
        script=pin(__file__), scope=plan['scope'], independent_review_pending=True))
    print(json.dumps({'passed':True, 'modules':len(outputs), 'axioms':len(audit),
                     'receipt':pin(BUNDLE/('COMPILED_'+revision+'.json'))}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
