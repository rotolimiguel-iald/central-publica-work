from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'revisao'
RUN = ROOT / 'attempts/20260914_081118_098129/run.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, data):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    assert not p.exists(), str(p)
    if not isinstance(data, bytes): data = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_bytes(data); assert tmp.stat().st_size == len(data)
    tmp.replace(p)
run = json.loads(RUN.read_text(encoding='utf-8'))
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
OUT = REVIEW / ('a1_independent_' + stamp)
OUT.mkdir()
save(OUT / 'author_run.json', RUN.read_bytes())
source = ROOT / 'kernel/TGLExt/V351RegularCoreTraceContract.lean'
accepted_source = RUN.parent / source.name
assert sha(source) == sha(accepted_source) == run['source_sha256']
source_copy = OUT / 'kernel/TGLExt/V351RegularCoreTraceContract.lean'
save(source_copy, source.read_bytes())
names = re.findall(r'^#print axioms (\S+)\s*$', source.read_text(encoding='utf-8'), re.M)
names = ['TGLV351.' + n for n in names]
assert len(names) == len(set(names)) == 11
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
def parse(out):
    hits = re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$", out, re.M)
    data = {n: [a.strip() for a in ax.split(',') if a.strip()] for n, ax in hits}
    assert len(hits) == len(data) == 11, hits
    assert set(data) == set(names)
    assert all(set(a) <= allowed for a in data.values())
    return data
parse((RUN.parent / 'stdout.txt').read_text(encoding='utf-8'))
deps = json.loads((ROOT / 'DEPENDENCIAS_A1.json').read_text(encoding='utf-8'))
assert len(deps) == 375
dep_manifest = []
for d in deps:
    rel = Path(*d['module'].split('.'))
    obj = ROOT / 'build' / rel.with_suffix('.olean')
    src = ROOT / 'kernel' / rel.with_suffix('.lean')
    assert sha(obj) == d['object_sha256'], str(obj)
    assert sha(src) == d['source_sha256'], str(src)
    assert sha(d['object_origin']) == d['object_sha256'], d['object_origin']
    dest = OUT / 'build' / rel.with_suffix('.olean')
    save(dest, obj.read_bytes())
    save(OUT / 'dependency_sources' / rel.with_suffix('.lean'), src.read_bytes())
    dep_manifest.append(dict(d, source=str(src), copied_object=str(dest)))
save(OUT / 'dependencies.json', dep_manifest)
# Only the frozen copy of the 375 project dependencies is on the project path.
# Library packages are inherited read-only, not independently rebuilt.
packages = [p for p in run['lean_path'] if '/.lake/packages/' in p.replace('\\', '/')]
assert len(packages) == 9, packages
build = OUT / 'build'; build.mkdir(exist_ok=True)
lean_path = [str(build)] + packages
env = os.environ.copy(); env['LEAN_PATH'] = os.pathsep.join(lean_path)
compiler = Path(run['command'][0])
compiler_pin = sha(compiler)
package_directory_status = {p: Path(p).is_dir() for p in packages}
pins = {}
for rel in ['REAPROVEITAMENTO_A1.md', 'REAPROVEITAMENTO_A1.json', 'LACUNAS_A1.md',
            'AUDITORIA_A1.json', 'audit_a1.py', 'DEPENDENCIAS_A1.json', 'BASE_E_FONTES.json', 'um.py']:
    p = ROOT / rel
    if p.exists():
        pins[rel] = sha(p)
        if p.name != 'um.py': save(OUT / 'inputs' / rel, p.read_bytes())
save(OUT / 'preflight.json', dict(time=datetime.datetime.now().astimezone().isoformat(),
    source_sha256=sha(source), author_object_sha256=sha(run['command'][2]), compiler=str(compiler),
    compiler_sha256=compiler_pin, lean_path=lean_path, project_dependencies=375,
    provenance='375 dependency binaries inherited from author build with source/object/origin hashes checked; packages read-only from accepted run; no library rebuild',
    package_directory_status=package_directory_status, names=names, pins=pins))
print('SNAPSHOT_READY ' + str(OUT), flush=True)
def compile_one(label, src, obj):
    obj.parent.mkdir(parents=True, exist_ok=True)
    command = [str(compiler), '-o', str(obj), str(src)]
    start = time.monotonic()
    with (OUT / (label + '.stdout.txt')).open('wb') as out, (OUT / (label + '.stderr.txt')).open('wb') as err:
        result = subprocess.run(command, cwd=OUT / 'kernel', env=env, stdout=out, stderr=err)
    stdout = (OUT / (label + '.stdout.txt')).read_text(encoding='utf-8')
    stderr = (OUT / (label + '.stderr.txt')).read_text(encoding='utf-8')
    data = dict(command=command, returncode=result.returncode, seconds=time.monotonic()-start,
        source_sha256=sha(src), stdout_sha256=sha(OUT / (label+'.stdout.txt')),
        stderr_sha256=sha(OUT / (label+'.stderr.txt')), object_sha256=sha(obj) if obj.exists() else None)
    if result.returncode == 0 and 'error:' not in stdout and 'warning:' not in stdout and not stderr:
        data['axioms'] = parse(stdout)
    save(OUT / (label + '.json'), data)
    print(label.upper() + ' ' + json.dumps(data, ensure_ascii=False), flush=True)
    return data
module = compile_one('module', source_copy, build / 'TGLExt/V351RegularCoreTraceContract.olean')
if module['returncode'] != 0:
    save(OUT / 'compilation.json', dict(all_exit_zero=False, module=module)); sys.exit(1)
audit_source = OUT / 'kernel/ReviewA1Audit.lean'
audit_text = 'import TGLExt.V351RegularCoreTraceContract\nset_option pp.universes true\nset_option pp.explicit true\n'
for n in names: audit_text += '#check ' + n + '\n#print axioms ' + n + '\n'
audit_text += '#print TGLV351.RegularCoreTraceData\n'
save(audit_source, audit_text.encode('utf-8'))
auditor = compile_one('auditor', audit_source, build / 'ReviewA1Audit.olean')
post = all(sha(d['source']) == d['source_sha256'] and sha(d['object_origin']) == d['object_sha256'] and sha(d['copied_object']) == d['object_sha256'] for d in dep_manifest)
post = post and sha(source) == run['source_sha256'] and all(sha(ROOT / k) == v for k,v in pins.items())
summary = dict(all_exit_zero=module['returncode']==0 and auditor['returncode']==0,
    exact_targets_and_allowed_axioms='axioms' in module and 'axioms' in auditor,
    module_binary_equals_author=module['object_sha256']==sha(run['command'][2]),
    author_source_dependencies_inputs_preserved=post, module=module, auditor=auditor,
    review_dir=str(OUT), completed=datetime.datetime.now().astimezone().isoformat())
save(OUT / 'compilation.json', summary)
print('COMPILATION_FINAL ' + json.dumps({k:v for k,v in summary.items() if k not in ['module','auditor']}, ensure_ascii=False))
