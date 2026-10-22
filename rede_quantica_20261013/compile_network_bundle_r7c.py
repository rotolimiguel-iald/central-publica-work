"""Compile the dependency DAG in an isolated cache, with immutable receipts.

Six independent Lean processes at most; each uses four worker threads. Reuse
requires exact source/object custody from the already compiled prior bundle.
No production write, network, provider call, or silent retry is performed.
"""
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import subprocess
import time
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r7'
PRIOR = OUT/'network_bundle_r4'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
PREFIX = 'TGLExt.F1Fecho394.'


def parse_axioms(raw):
    reports = {}
    for name, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", raw, re.S):
        reports[name] = [v.strip() for v in values.split(',') if v.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms", raw):
        reports[name] = []
    for line in raw.splitlines():
        cols = line.split('\t')
        if len(cols) >= 3 and cols[0] in ('LOCAL_DECL', 'BENCH_DECL', 'BUNDLE_DECL'):
            reports[cols[1]] = [v for v in cols[-1].split(',') if v]
    return reports


def main():
    plan_path = BUNDLE/'PLAN.json'
    plan = json.loads(plan_path.read_bytes())
    cache_stage = BUNDLE/'CACHE_STAGE_RECEIPT_R2.json'
    cache_pins = json.loads(cache_stage.read_bytes())['copies']
    assert all(pin(x['copy']['path']) == x['copy'] for x in cache_pins)
    final = BUNDLE/'COMPILED_R1.json'
    assert not final.exists(), 'Already completed; inspect receipt instead'
    roots = [BUNDLE/'lib', PRIOR/'lib', KERNEL/'.lake/build/lib/lean']
    roots += sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))
    roots += [LEAN.parent.parent/'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, roots)))
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert '4.31.0' in version
    rows = list(plan['modules']) + [dict(module=plan['audit_module'],
        transposed_source=plan['audit'], relative=plan['audit_relative'])]
    bymod = {r['module']: r for r in rows}
    dependencies = {}
    for row in rows:
        src = Path(row['transposed_source']['path'])
        assert pin(src) == row['transposed_source']
        imports = re.findall(r'^import\s+([\w.]+)\s*$', src.read_text(encoding='utf-8'), re.M)
        deps = [n for n in imports if n.startswith(PREFIX)]
        assert all(d in bymod for d in deps), (row['module'], deps)
        dependencies[row['module']] = deps
    results, pending, failures = {}, set(bymod), []

    # Every reused binary has its actual prior successful build receipt checked.
    for row in rows:
        if 'reuse_prior_object' not in row:
            continue
        old_receipt = PRIOR/'builds'/(Path(row['relative']).stem+'.json')
        old = json.loads(old_receipt.read_bytes())
        assert old['passed'] and old['exit_code'] == 0
        assert pin(Path(old['object']['path'])) == row['reuse_prior_object'] == old['object']
        assert pin(Path(old['source']['path'])) == row['reuse_prior_source'] == old['source']
        assert Path(old['source']['path']).read_bytes() == Path(row['transposed_source']['path']).read_bytes()
        assert all(pin(Path(x['path'])) == x for x in old['dependencies'])
        copy = (BUNDLE/'lib'/row['relative']).with_suffix('.olean')
        assert pin(copy)['sha256'] == row['reuse_prior_object']['sha256']
        results[row['module']] = dict(module=row['module'], reused=True, passed=True,
            source=row['transposed_source'], object=pin(copy), prior_object=row['reuse_prior_object'],
            prior_receipt=pin(old_receipt), axiom_report=old['axiom_report'])
        pending.remove(row['module'])
    for n in results:
        assert all(d in results for d in dependencies[n]), ('reused module needs new dependency', n)

    def build(module, dep_pins):
        row = bymod[module]
        src = Path(row['transposed_source']['path'])
        rel = Path(row['relative'])
        binary = (BUNDLE/'lib'/rel).with_suffix('.olean')
        receipt = BUNDLE/'builds'/(rel.stem+'.json')
        if receipt.exists():
            done = json.loads(receipt.read_bytes())
            assert done['passed'] and done['source'] == pin(src)
            assert done['object'] == pin(binary)
            assert done['dependencies'] == dep_pins
            assert all(pin(Path(p['path'])) == p for p in dep_pins)
            print('REUSED '+module, flush=True)
            return done
        assert not binary.exists(), ('unreceipted object; investigate', str(binary))
        d = BUNDLE/'builds'/(rel.stem+'_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
        d.mkdir(parents=True, exist_ok=False)
        binary.parent.mkdir(parents=True, exist_ok=True)
        command = [str(LEAN), '-j', '4', '-R', str(BUNDLE/'src'), '-o', str(binary), str(src)]
        for p in dep_pins:
            assert pin(Path(p['path'])) == p
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        t0 = time.perf_counter()
        print('BUILD_START '+module, flush=True)
        p = subprocess.run(command, cwd=BUNDLE/'src', env=env, capture_output=True)
        elapsed = time.perf_counter()-t0
        end = dt.datetime.now(dt.timezone.utc).isoformat()
        stdout, stderr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')
        reports = parse_axioms(stdout)
        new(d/'STDOUT.log', stdout)
        new(d/'STDERR.log', stderr)
        stable = pin(src) == row['transposed_source'] and all(pin(Path(x['path'])) == x for x in dep_pins)
        passed = p.returncode == 0 and stable and 'sorryAx' not in stdout and all(set(v) <= TRIO for v in reports.values())
        if module == plan['audit_module']:
            count = [int(line.split('\t')[1]) for line in stdout.splitlines() if line.startswith('BUNDLE_COUNT\t')]
            passed = passed and len(count) == 1 and count[0] == len(reports) and count[0] > 0
        result = dict(module=module, source=pin(src), command=command, cwd=str(BUNDLE/'src'),
            LEAN_PATH=env['LEAN_PATH'], toolchain=version, start_utc=start, end_utc=end,
            seconds=elapsed, exit_code=p.returncode, passed=passed, axiom_report=reports,
            stdout=pin(d/'STDOUT.log'), stderr=pin(d/'STDERR.log'), dependencies=dep_pins,
            inputs_unchanged=stable, production_modified=False, script=pin(__file__))
        if p.returncode == 0:
            result['object'] = pin(binary)
        new(d/'BUILD_RECEIPT.json', result)
        print(json.dumps(dict(module=module, exit=p.returncode, passed=passed,
            seconds=elapsed, receipt=str(d/'BUILD_RECEIPT.json')), ensure_ascii=False), flush=True)
        if passed:
            new(receipt, result)
        return result

    start = dt.datetime.now(dt.timezone.utc).isoformat()
    with cf.ThreadPoolExecutor(max_workers=6) as pool:
        running = {}
        while pending or running:
            ready = sorted(n for n in pending if all(d in results and results[d]['passed'] for d in dependencies[n]))
            while ready and len(running) < 6 and not failures:
                n = ready.pop(0)
                pins = [results[d]['object'] for d in dependencies[n]]
                running[pool.submit(build, n, pins)] = n
                pending.remove(n)
            if not running:
                if pending and not failures:
                    raise RuntimeError(('unresolved dependencies', sorted(pending)))
                break
            done, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for future in done:
                name = running.pop(future)
                try:
                    result = future.result()
                    results[name] = result
                    if not result['passed']:
                        failures.append(dict(module=name, result=result))
                except Exception as exc:
                    failures.append(dict(module=name, exception=repr(exc)))
    if failures:
        failure = BUNDLE/('FAILURE_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'.json')
        new(failure, dict(plan=pin(plan_path), failures=failures, pending=sorted(pending),
            passed=[n for n,r in results.items() if r['passed']], start_utc=start,
            end_utc=dt.datetime.now(dt.timezone.utc).isoformat()))
        raise RuntimeError(str(failure))
    assert len(results) == len(rows)
    audit = results[plan['audit_module']]['axiom_report']
    assert all(pin(x['copy']['path']) == x['copy'] for x in cache_pins)
    new(final, dict(cache_stage=pin(cache_stage), passed=True, plan=pin(plan_path), modules=[results[r['module']] for r in rows],
        all_local_declarations=len(audit), start_utc=start, end_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        script=pin(__file__), scope=plan['scope'], independent_review_pending=True))
    print(json.dumps(dict(passed=True, modules=len(rows), reused=sum('reused' in r for r in results.values()),
        axioms=len(audit), receipt=pin(final)), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
