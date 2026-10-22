"""Pre-audit exact roots and sources before the next main invocation.

Every output is new. Existing source and cache bytes are verified and copied;
neither canonical sources nor another attempt's objects are replaced.
"""
import ast
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r7'
DEST = BUNDLE/'whole_preaudit_r1'
CANDIDATE = OUT/'candidate_r7/um_v394_integrated.py'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}


def read(meta):
    path = Path(meta['path'])
    assert pin(path) == meta, ('pin mismatch', str(path))
    return path.read_bytes()


def embedded(raw):
    tree = ast.parse(raw)
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
        and isinstance(n.targets[0], ast.Name) and n.targets[0].id == '_EMBEDDED_KERNEL_FILES')


def validate_bundle(compiled):
    assert compiled['passed'] is True
    plan = json.loads(read(compiled['plan']))
    expected = {r['module']: r['transposed_source'] for r in plan['modules']}
    expected[plan['audit_module']] = plan['audit']
    rows = {r['module']: r for r in compiled['modules']}
    assert len(rows) == len(compiled['modules']) and set(rows) == set(expected)
    for name, row in rows.items():
        assert row['passed'] is True and row['source'] == expected[name]
        read(row['source']); read(row['object'])
        actual = row
        if row.get('reused') is True:
            actual = json.loads(read(row['prior_receipt']))
            assert read(actual['source']) == read(row['source'])
            assert read(actual['object']) == read(row['object'])
            assert row['axiom_report'] == actual['axiom_report']
        assert actual['passed'] is True and type(actual['exit_code']) is int and actual['exit_code'] == 0
        read(actual['stdout']); read(actual['stderr'])
        assert all(set(v) <= TRIO for v in actual['axiom_report'].values())
        assert all(read(m) is not None for m in actual['dependencies'])
    return plan


def prepare():
    assert not DEST.exists(), 'A previous attempt exists; inspect it, do not overwrite'
    compiled_path = BUNDLE/'COMPILED_R1.json'
    compiled = json.loads(compiled_path.read_bytes())
    plan = validate_bundle(compiled)
    integration_path = OUT/'INTEGRATION_NETWORK_R7.json'
    integration = json.loads(integration_path.read_bytes())
    assert read(integration['candidate']) == CANDIDATE.read_bytes()
    assert integration['compiled_bundle'] == pin(compiled_path)
    bodies = embedded(CANDIDATE.read_bytes())
    for rel, body in bodies.items():
        assert (CANDIDATE.parent/'tgl_kernel'/rel).read_bytes() == body.encode('utf-8')
    stage_path = BUNDLE/'CACHE_STAGE_RECEIPT_R2.json'
    stage = json.loads(stage_path.read_bytes())
    for row in stage['copies']:
        assert read(row['copy']) == read(row['source'])
    available = {Path(r['copy']['path']).resolve(): r['copy'] for r in stage['copies']}
    available.update({Path(r['object']['path']).resolve(): r['object'] for r in compiled['modules']})
    # Prior root objects are excluded; these two roots must be built anew.
    copies = []
    for source in sorted((BUNDLE/'lib').rglob('*.olean')):
        rel = source.relative_to(BUNDLE/'lib')
        if rel.as_posix() in {'TGLExt.olean', 'TGL/Audit.olean'}:
            continue
        assert source.resolve() in available, ('unreceipted cache object', str(source))
        raw = read(available[source.resolve()])
        target = DEST/'lib'/rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
        assert target.read_bytes() == raw
        copies.append(dict(source=pin(source), copy=pin(target)))
    sources = {}
    for module in ('TGLExt', 'TGL/Audit'):
        source = DEST/'src'/(module+'.lean')
        new(source, bodies[module+'.lean'])
        sources[module] = pin(source)
    record = dict(candidate=pin(CANDIDATE), integration=pin(integration_path),
        baseline=plan['baseline'], plan=compiled['plan'], compiled_bundle=pin(compiled_path),
        cache_stage=pin(stage_path), copies=copies, sources=sources,
        formal_files_sha256={rel:__import__('hashlib').sha256(body.encode('utf-8')).hexdigest()
            for rel, body in bodies.items()}, script=pin(__file__), production_modified=False)
    new(DEST/'PREPARED.json', record)
    print(json.dumps(dict(prepared=pin(DEST/'PREPARED.json'), copies=len(copies)), ensure_ascii=False))


def parsers():
    path = OUT/'full_rite/qualified_index_v394_r2.py'
    spec = importlib.util.spec_from_file_location('exact_lean_parsers', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, pin(path)


def build():
    prepared_path = DEST/'PREPARED.json'
    prepared = json.loads(prepared_path.read_bytes())
    read(prepared['candidate']); read(prepared['compiled_bundle'])
    assert not (DEST/'MEASURED_COVERAGE_R1.json').exists()
    for row in prepared['copies']:
        assert read(row['source']) == read(row['copy'])
    paths = [DEST/'lib']+sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    version = subprocess.check_output([str(LEAN), '--version'], text=True).strip()
    assert '4.31.0' in version
    parser, parser_pin = parsers()
    results = []
    for module, meta in prepared['sources'].items():
        source = Path(meta['path']); read(meta)
        obj = DEST/'lib'/(module+'.olean')
        assert not obj.exists(), ('Output already exists; inspect previous attempt', str(obj))
        obj.parent.mkdir(parents=True, exist_ok=True)
        command = [str(LEAN), '-j', '8', '-R', str(DEST/'src'), '-o', str(obj), str(source)]
        print('WHOLE_PREAUDIT_START '+module, flush=True)
        start = dt.datetime.now(dt.timezone.utc).isoformat(); t0 = time.perf_counter()
        p = subprocess.run(command, cwd=DEST/'src', env=env, capture_output=True)
        seconds = time.perf_counter()-t0; end = dt.datetime.now(dt.timezone.utc).isoformat()
        stem = module.replace('/', '_')
        stdout, stderr = p.stdout.decode('utf-8'), p.stderr.decode('utf-8')
        new(DEST/(stem+'_STDOUT.log'), stdout); new(DEST/(stem+'_STDERR.log'), stderr)
        parsed = parser.parse_lean_axioms_v394(stdout)
        report = parsed['axioms']
        safe = not any(set(v)-TRIO for v in report.values())
        passed = p.returncode == 0 and pin(source) == meta and safe and 'sorryAx' not in stdout
        if module == 'TGL/Audit':
            provenance = parser.parse_lean_provenance_v394(stdout)
            totals = re.findall(r'(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=([0-9]+) thm=([0-9]+) fora_do_trio=([0-9]+)\s*$', stdout)
            passed = passed and parsed['ok'] and provenance['ok'] and set(provenance['sources']) == set(report)
            passed = passed and len(totals) == 1 and int(totals[0][0]) == len(report) and int(totals[0][2]) == 0
        result = dict(module=module, source=meta, command=command, cwd=str(DEST/'src'),
            LEAN_PATH=env['LEAN_PATH'], toolchain=version, start_utc=start, end_utc=end,
            seconds=seconds, exit_code=p.returncode, passed=passed, axiom_report=report,
            stdout=pin(DEST/(stem+'_STDOUT.log')), stderr=pin(DEST/(stem+'_STDERR.log')),
            prepared=pin(prepared_path), parser=parser_pin, script=pin(__file__))
        if p.returncode == 0:
            result['object'] = pin(obj)
        receipt = DEST/(stem+'_BUILD_RECEIPT.json'); new(receipt, result)
        print(json.dumps(dict(module=module, exit=p.returncode, passed=passed, seconds=seconds)), flush=True)
        assert passed, ('Build failed; original attempt preserved', str(receipt))
        results.append(pin(receipt))
    for row in prepared['copies']:
        read(row['source']); read(row['copy'])
    read(prepared['candidate'])
    new(DEST/'DECLARATION_SOURCES.json', provenance['sources'])
    record = dict(passed=True, prepared=pin(prepared_path), candidate=prepared['candidate'],
        compiled_bundle=prepared['compiled_bundle'], sources=prepared['sources'], builds=results,
        total_declarations=int(totals[0][0]), total_theorems=int(totals[0][1]), outside_trio=0,
        axiom_report_count=len(report), unread_names=0, provenance=pin(DEST/'DECLARATION_SOURCES.json'),
        parser=parser_pin, formal_files_sha256=prepared['formal_files_sha256'],
        scope='Whole compiler closure, exact qualified names and source hashes; measured before a future main, no runtime or seal claimed.')
    new(DEST/'MEASURED_COVERAGE_R1.json', record)
    print(json.dumps(dict(measured=pin(DEST/'MEASURED_COVERAGE_R1.json'), declarations=len(report)), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    {'prepare':prepare, 'build':build}[sys.argv[1]]()
