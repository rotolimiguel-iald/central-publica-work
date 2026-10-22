"""Prepare and audit the complete candidate import closure in an isolated cache.

The expected declaration totals are measured here before candidate generation,
never inferred from the subsequent runtime that must satisfy the contract.
"""
import ast
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
R2 = ROOT/'work/rite394_20261015/r2/tgl_kernel'
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
DEST = BUNDLE/'full_audit_r2'
TRIO = {'propext','Classical.choice','Quot.sound'}


def prepare():
    assert not DEST.exists()
    plan = json.loads((BUNDLE/'PLAN_R2.json').read_bytes())
    baseline = OUT/'candidate_r3/um.py'
    tree = ast.parse(baseline.read_text(encoding='utf-8'))
    embedded = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
                    and isinstance(n.targets[0],ast.Name) and n.targets[0].id == '_EMBEDDED_KERNEL_FILES')
    copies = []

    def copy(source, target):
        assert not target.exists(), ('cache destination exists', str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = source.read_bytes()
        with target.open('xb') as f:
            f.write(raw)
        assert source.read_bytes() == target.read_bytes()
        copies.append(dict(source=pin(source), copy=pin(target)))

    lib = KERNEL/'.lake/build/lib/lean'
    for source in sorted((lib/'TGL').rglob('*')):
        if source.is_file() and not source.name.startswith('Audit.'):
            copy(source, BUNDLE/'lib'/source.relative_to(lib))
    for source in sorted(lib.glob('TGL.*')):
        if source.is_file():
            copy(source, BUNDLE/'lib'/source.name)
    for name in ('TimeGravitonScalar','TimeGravitonMatrix','TimeGravitonFlow','TimeGravitonKraus','RuleQuadraticResidual'):
        source = R2/'TGLExt'/(name+'.lean')
        assert source.read_bytes() == embedded['TGLExt/'+name+'.lean'].encode('utf-8')
        cache = R2/'.lake/build/lib/lean/TGLExt'
        files = sorted(cache.glob(name+'.*'))
        assert any(p.suffix == '.olean' for p in files)
        for p in files:
            copy(p, BUNDLE/'lib/TGLExt'/p.name)
    glue = 'import '+plan['audit_module']+'\n'
    sources = dict(TGLExt=embedded['TGLExt.lean']+'\n'+glue,
                   **{'TGL/Audit':glue+'\n'+embedded['TGL/Audit.lean']})
    DEST.mkdir()
    for name, body in sources.items():
        new(BUNDLE/'src'/(name+'.lean'), body)
    new(DEST/'PREPARED.json', dict(baseline=pin(baseline), plan=pin(BUNDLE/'PLAN_R2.json'),
        script=pin(__file__), copies=copies,
        sources={name:pin(BUNDLE/'src'/(name+'.lean')) for name in sources},
        purpose='Fresh root and total audit over copied dependencies; no original cache writes.'))
    print(json.dumps(dict(prepared=True, copied_files=len(copies), receipt=pin(DEST/'PREPARED.json')), ensure_ascii=False), flush=True)


def build():
    prep = json.loads((DEST/'PREPARED.json').read_bytes())
    compiled = json.loads((BUNDLE/'COMPILED_R2.json').read_bytes())
    assert compiled['passed'] and compiled['plan'] == prep['plan']
    assert not (DEST/'MEASURED_COVERAGE_R1.json').exists()
    for row in prep['copies']:
        assert pin(row['source']['path']) == row['source']
        assert pin(row['copy']['path']) == row['copy']
    paths = [BUNDLE/'lib']+sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    results = []
    for name, source_pin in prep['sources'].items():
        source = Path(source_pin['path'])
        assert pin(source) == source_pin
        binary = BUNDLE/'lib'/(name+'.olean')
        if binary.exists():
            raise FileExistsError(('new root output exists; recover without overwriting', str(binary)))
        binary.parent.mkdir(parents=True,exist_ok=True)
        command = [str(LEAN),'-R',str(BUNDLE/'src'),'-o',str(binary),str(source)]
        print('FULL_BUILD_START '+name,flush=True)
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        t0 = time.perf_counter()
        proc = subprocess.run(command,cwd=BUNDLE/'src',env=env,capture_output=True)
        seconds = time.perf_counter()-t0
        end = dt.datetime.now(dt.timezone.utc).isoformat()
        stdout, stderr = proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8')
        stem = name.replace('/','_')
        new(DEST/(stem+'_STDOUT.log'),stdout)
        new(DEST/(stem+'_STDERR.log'),stderr)
        axioms = {}
        for declaration, values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",stdout,re.S):
            axioms[declaration] = [v.strip() for v in values.split(',') if v.strip()]
        for declaration in re.findall(r"'([^']+)' does not depend on any axioms",stdout):
            axioms[declaration] = []
        result = dict(module=name, source=pin(source), command=command, LEAN_PATH=env['LEAN_PATH'],
            toolchain=subprocess.check_output([str(LEAN),'--version'],text=True).strip(),
            start_utc=start,end_utc=end,seconds=seconds,exit_code=proc.returncode,
            stdout=pin(DEST/(stem+'_STDOUT.log')),stderr=pin(DEST/(stem+'_STDERR.log')),
            passed=proc.returncode == 0 and 'sorryAx' not in stdout and all(set(v)<=TRIO for v in axioms.values()),
            axiom_report=axioms)
        if proc.returncode == 0:
            result['object'] = pin(binary)
        new(DEST/(stem+'_BUILD_RECEIPT.json'),result)
        print(json.dumps(dict(module=name,exit=proc.returncode,seconds=seconds)),flush=True)
        assert result['passed']
        results.append(result)
    raw = Path(results[-1]['stdout']['path']).read_text(encoding='utf-8')
    totals = re.findall(r'TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)',raw)
    assert len(totals) == 1 and int(totals[0][2]) == 0
    record = dict(passed=True, prepared=pin(DEST/'PREPARED.json'), compiled_bundle=pin(BUNDLE/'COMPILED_R2.json'),
        total_declarations=int(totals[0][0]),total_theorems=int(totals[0][1]),outside_trio=int(totals[0][2]),
        axiom_report_count=len(results[-1]['axiom_report']),coverage_line='TGL_AXIOM_COVERAGE_TOTAL decl=%s thm=%s fora_do_trio=%s'%totals[0],
        sources=prep['sources'], builds=[pin(DEST/(r['module'].replace('/','_')+'_BUILD_RECEIPT.json')) for r in results],
        scope='Pre-measured exact mathematical coverage for this candidate import closure; not a full runtime or seal.')
    assert set(json.loads((BUNDLE/'PLAN_R2.json').read_bytes())['theorems']) <= set(results[-1]['axiom_report'])
    new(DEST/'MEASURED_COVERAGE_R1.json',record)
    print(json.dumps(record,ensure_ascii=False),flush=True)


if __name__ == '__main__':
    {'prepare':prepare,'build':build}[sys.argv[1]]()
