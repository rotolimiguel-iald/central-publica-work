"""Measure full R3-bundle coverage before freezing the candidate expectation."""
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
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
DEST = BUNDLE/'full_audit_r3'
TRIO = {'propext','Classical.choice','Quot.sound'}


def prepare():
    assert not DEST.exists()
    earlier_path = BUNDLE/'full_audit_r2/PREPARED.json'
    earlier = json.loads(earlier_path.read_bytes())
    plan_path = BUNDLE/'PLAN_R3.json'
    plan = json.loads(plan_path.read_bytes())
    baseline = OUT/'candidate_r3/um.py'
    assert pin(baseline) == earlier['baseline']
    tree = ast.parse(baseline.read_text(encoding='utf-8'))
    embedded = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
                    and isinstance(n.targets[0],ast.Name) and n.targets[0].id == '_EMBEDDED_KERNEL_FILES')
    for row in earlier['copies']:
        assert pin(row['source']['path']) == row['source']
        assert pin(row['copy']['path']) == row['copy']
    glue = 'import '+plan['audit_module']+'\n'
    sources = {'TGLExt':embedded['TGLExt.lean']+'\n'+glue,
               'TGL/Audit':glue+'\n'+embedded['TGL/Audit.lean']}
    DEST.mkdir()
    for name, body in sources.items():
        new(DEST/'src'/(name+'.lean'),body)
    new(DEST/'PREPARED.json',dict(baseline=pin(baseline),plan=pin(plan_path),script=pin(__file__),
        earlier_cache=pin(earlier_path),copies=earlier['copies'],
        sources={name:pin(DEST/'src'/(name+'.lean')) for name in sources},
        scope='Same proof bodies; three generated names corrected from the actual imported environment.'))
    print(json.dumps(dict(prepared=True,receipt=pin(DEST/'PREPARED.json')),ensure_ascii=False))


def build():
    prep = json.loads((DEST/'PREPARED.json').read_bytes())
    compiled_path = BUNDLE/'COMPILED_R3.json'
    compiled = json.loads(compiled_path.read_bytes())
    assert compiled['passed'] and compiled['plan'] == prep['plan']
    assert not (DEST/'MEASURED_COVERAGE_R1.json').exists()
    for row in prep['copies']:
        assert pin(row['source']['path']) == row['source']
        assert pin(row['copy']['path']) == row['copy']
    paths = [BUNDLE/'lib']+sorted(KERNEL.glob('.lake/packages/*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
    env = dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
    results=[]
    for name, source_pin in prep['sources'].items():
        source = Path(source_pin['path'])
        assert pin(source) == source_pin
        binary = BUNDLE/'lib'/(name+'.olean')
        assert not binary.exists(), ('Unreceipted output; preserve and recover',str(binary))
        binary.parent.mkdir(parents=True,exist_ok=True)
        command=[str(LEAN),'-R',str(DEST/'src'),'-o',str(binary),str(source)]
        print('FULL_BUILD_START '+name,flush=True)
        start=dt.datetime.now(dt.timezone.utc).isoformat()
        t0=time.perf_counter()
        proc=subprocess.run(command,cwd=DEST/'src',env=env,capture_output=True)
        seconds=time.perf_counter()-t0
        end=dt.datetime.now(dt.timezone.utc).isoformat()
        stdout,stderr=proc.stdout.decode('utf-8'),proc.stderr.decode('utf-8')
        stem=name.replace('/','_')
        new(DEST/(stem+'_STDOUT.log'),stdout)
        new(DEST/(stem+'_STDERR.log'),stderr)
        axioms={}
        for declaration,values in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",stdout,re.S):
            axioms[declaration]=[v.strip() for v in values.split(',') if v.strip()]
        for declaration in re.findall(r"'([^']+)' does not depend on any axioms",stdout):
            axioms[declaration]=[]
        result=dict(module=name,source=pin(source),command=command,LEAN_PATH=env['LEAN_PATH'],
            toolchain=subprocess.check_output([str(LEAN),'--version'],text=True).strip(),
            start_utc=start,end_utc=end,seconds=seconds,exit_code=proc.returncode,
            stdout=pin(DEST/(stem+'_STDOUT.log')),stderr=pin(DEST/(stem+'_STDERR.log')),
            passed=proc.returncode == 0 and 'sorryAx' not in stdout and all(set(v)<=TRIO for v in axioms.values()),
            axiom_report=axioms,compiled_bundle=pin(compiled_path),prepared=pin(DEST/'PREPARED.json'))
        if proc.returncode == 0:
            result['object']=pin(binary)
        new(DEST/(stem+'_BUILD_RECEIPT.json'),result)
        print(json.dumps(dict(module=name,exit=proc.returncode,seconds=seconds)),flush=True)
        assert result['passed']
        results.append(result)
    raw=Path(results[-1]['stdout']['path']).read_text(encoding='utf-8')
    totals=re.findall(r'TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)',raw)
    assert len(totals)==1 and int(totals[0][2])==0
    record=dict(passed=True,prepared=pin(DEST/'PREPARED.json'),compiled_bundle=pin(compiled_path),
        total_declarations=int(totals[0][0]),total_theorems=int(totals[0][1]),outside_trio=int(totals[0][2]),
        axiom_report_count=len(results[-1]['axiom_report']),
        coverage_line='TGL_AXIOM_COVERAGE_TOTAL decl=%s thm=%s fora_do_trio=%s'%totals[0],
        sources=prep['sources'],builds=[pin(DEST/(r['module'].replace('/','_')+'_BUILD_RECEIPT.json')) for r in results],
        scope='Pre-measured whole import closure; broad parser. Runtime parser coverage must be derived separately from this pinned log.')
    assert set(json.loads((BUNDLE/'PLAN_R3.json').read_bytes())['theorems']) <= set(results[-1]['axiom_report'])
    new(DEST/'MEASURED_COVERAGE_R1.json',record)
    print(json.dumps(record,ensure_ascii=False),flush=True)


if __name__=='__main__':
    {'prepare':prepare,'build':build}[sys.argv[1]]()
