"""Adversarial compiler probes kept OUTSIDE the embedded production kernel."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / 'environment.json').read_bytes())
environment = os.environ.copy()
environment['LEAN_PATH'] = os.pathsep.join(config['lean_path'])
folder = ROOT / 'tests' / 'probes'
folder.mkdir(parents=True, exist_ok=True)
probes = {
    'WrongType': '''import TGLExt.FrontierCertificate
namespace V350ProbeWrongType
def named : True := True.intro
def forced : TGLExt.ModularRealizationCertificate := named
end V350ProbeWrongType
''',
    'UnprovedPremise': '''import TGLExt.FrontierCertificate
namespace V350ProbeUnprovedPremise
def conditional (h : False) : TGLExt.ModularRealizationCertificate := False.elim h
def forced : TGLExt.ModularRealizationCertificate := conditional
end V350ProbeUnprovedPremise
''',
    'ForeignAxiom': '''import TGLExt.FrontierCertificate
namespace V350ProbeForeignAxiom
axiom hiddenPremise : TGLExt.ModularRealizationCertificate
noncomputable def named : TGLExt.ModularRealizationCertificate := hiddenPremise
#print axioms named
end V350ProbeForeignAxiom
''',
    'SorryTerm': '''import TGLExt.FrontierCertificate
namespace V350ProbeSorryTerm
def named : TGLExt.ModularRealizationCertificate := by sorry
#print axioms named
end V350ProbeSorryTerm
''',
}


def run(name):
    raw = probes[name].encode('utf-8')
    source = folder / (name + '.lean')
    source.write_bytes(raw)
    result = subprocess.run([config['lean'], str(source)], cwd=folder,
                            env=environment, capture_output=True)
    (folder / (name + '.stdout.txt')).write_bytes(result.stdout)
    (folder / (name + '.stderr.txt')).write_bytes(result.stderr)
    output = result.stdout.decode('utf-8', errors='replace')
    if name in ('WrongType', 'UnprovedPremise'):
        passed = result.returncode != 0 and 'type mismatch' in output.lower()
        decision = 'REJECTED_BY_EXACT_TYPE'
    else:
        found = re.findall(r"depends on axioms: \[([^\]]*)\]", output, re.S)
        axioms = [a.strip() for group in found for a in group.replace('\n', ' ').split(',') if a.strip()]
        passed = result.returncode == 0 and bool(set(axioms) - {'propext', 'Classical.choice', 'Quot.sound'})
        decision = 'REJECTED_BY_AXIOM_WHITELIST'
    record = {'probe': name, 'returncode': result.returncode, 'passed': passed,
              'decision': decision, 'source_sha256': hashlib.sha256(raw).hexdigest(),
              'stdout_sha256': hashlib.sha256(result.stdout).hexdigest()}
    print(json.dumps(record), flush=True)
    if not passed:
        print(output, flush=True)
    return record


with ThreadPoolExecutor(max_workers=2) as pool:
    records = list(pool.map(run, probes))
report = {'probes': records, 'all_passed': all(r['passed'] for r in records),
          'production_kernel_unchanged': True}
target = ROOT / 'lean_contract_tests.json'
temporary = target.with_suffix('.json.tmp')
temporary.write_text(json.dumps(report, indent=2), encoding='utf-8')
temporary.replace(target)
assert report['all_passed']
