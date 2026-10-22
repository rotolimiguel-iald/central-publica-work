from pathlib import Path
from datetime import datetime
import hashlib, json, re, os, subprocess, time

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
OUT = ROOT / 'revisao'
STAGES = [
    ('V351ResolventPhaseFunctions', '20260914_095907_662952', 9),
    ('V351ResolventPhaseCalculus', '20260914_100402_294282', 10),
    ('V351ResolventImaginaryPowers', '20260914_100649_329613', 9),
    ('V351ResolventImaginaryContinuity', '20260914_101045_813310', 3),
    ('V351ScalarTomitaImaginaryPowers', '20260914_101128_096848', 8),
]
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def write(p, b):
    assert p.is_relative_to(OUT)
    p.parent.mkdir(parents=True, exist_ok=True)
    assert not p.exists(), str(p)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_bytes(b)
    assert tmp.read_bytes() == b
    os.replace(tmp, p)

def dump(p, obj):
    write(p, (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))

def parse_axioms(s):
    result = {}
    for m in re.finditer(r"(?m)^'(.+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", s):
        assert m[1] not in result
        result[m[1]] = [a.strip() for a in (m[2] or '').split(',') if a.strip()]
    return result

def main():
    now = datetime.now().astimezone()
    area = OUT / ('resolvent_phase39_independent_' + now.strftime('%Y%m%d_%H%M%S_%f'))
    area.mkdir()
    print('AREA ' + str(area), flush=True)
    manifest = ROOT / 'DEPENDENCIAS_A1_FASE_RESOLVENTE.json'
    deps = json.loads(manifest.read_text(encoding='utf-8-sig'))
    inherited = []
    old_dirs = sorted([p for p in OUT.iterdir() if p.is_dir() and p != area], reverse=True)
    for d in deps:
        rel = Path(*d['module'].split('.'))
        src = Path(d['source'])
        obj = Path(d['object'])
        assert pin(src)['sha256'] == d['source_sha256']
        assert pin(obj)['sha256'] == d['object_sha256']
        selected = obj
        provenance = 'author_pinned_inherited_object_not_recompiled_here'
        for old in old_dirs:
            candidate = old / 'build' / rel.with_suffix('.olean')
            if candidate.is_file() and pin(candidate)['sha256'] == d['object_sha256']:
                selected = candidate
                provenance = 'prior_review_snapshot_byte_equal_to_manifest_no_new_recompilation'
                break
        dsts = area / 'kernel' / rel.with_suffix('.lean')
        dsto = area / 'build' / rel.with_suffix('.olean')
        write(dsts, src.read_bytes())
        write(dsto, selected.read_bytes())
        inherited.append({'module': d['module'], 'source_origin': pin(src), 'author_object': pin(obj),
                          'selected_object': pin(selected), 'frozen_source': pin(dsts), 'frozen_object': pin(dsto),
                          'provenance': provenance})
    write(area / 'inputs' / manifest.name, manifest.read_bytes())
    for name in ['REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md','REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json']:
        write(area / 'inputs' / name, (ROOT/name).read_bytes())
    modules = []
    all_targets = []
    for stem, attempt, count in STAGES:
        folder = ROOT / 'attempts' / attempt
        run = json.loads((folder/'run.json').read_text(encoding='utf-8-sig'))
        source = ROOT/'kernel/TGLExt'/(stem+'.lean')
        obj = ROOT/'build/TGLExt'/(stem+'.olean')
        b = source.read_bytes()
        assert pin(source)['sha256'] == run['source_sha256']
        assert b == (folder/(stem+'.lean')).read_bytes()
        text = b.decode('utf-8-sig')
        targets = ['TGLV350.Regular.'+x for x in re.findall(r'(?m)^#print axioms\s+(\S+)', text)]
        assert len(targets) == count
        src = area/'kernel/TGLExt'/(stem+'.lean')
        assert not src.exists(), 'New target unexpectedly included in dependency manifest'
        write(src, b)
        clean = re.sub(r'/\-[\s\S]*?\-/|--[^\n]*', '', text)
        assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler)\b', clean)
        capture = area/'author_final'/stem
        for filename in [stem+'.lean','run.json','stdout.txt','stderr.txt']:
            write(capture/filename, (folder/filename).read_bytes())
        auth_text = (folder/'stdout.txt').read_text(encoding='utf-8-sig')
        auth_axioms = parse_axioms(auth_text)
        assert run['returncode'] == 0 and set(auth_axioms) == set(targets)
        assert all(set(a) <= TRIO for a in auth_axioms.values())
        assert not (folder/'stderr.txt').read_text(encoding='utf-8-sig').strip()
        assert not re.search(r'(?i)\b(?:warning|error):', auth_text)
        history = []
        for hist_src in sorted((ROOT/'attempts').glob('*/'+stem+'.lean')):
            hist_run = hist_src.parent/'run.json'
            if hist_src.parent.name == attempt or not hist_run.is_file():
                continue
            r = json.loads(hist_run.read_text(encoding='utf-8-sig'))
            history.append({'attempt': hist_src.parent.name, 'run': pin(hist_run),
                            'source': pin(hist_src), 'returncode': r.get('returncode'), 'accepted': False})
        modules.append({'stem': stem, 'source_original': pin(source), 'object_author': pin(obj),
                        'source_snapshot': pin(src), 'author_run': pin(folder/'run.json'),
                        'author_stdout': pin(folder/'stdout.txt'), 'author_stderr': pin(folder/'stderr.txt'),
                        'author_metadata': run, 'targets': targets, 'author_axioms': auth_axioms,
                        'history_excluded': history})
        all_targets.extend(targets)
    assert len(all_targets) == len(set(all_targets)) == 39
    # Only independent project snapshot and read-only dependency package directories.
    original_paths = modules[0]['author_metadata']['lean_path']
    packages = [p for p in original_paths if '\\.lake\\packages\\' in p]
    assert packages
    lean_paths = [str(area/'build')] + packages
    env = os.environ.copy()
    env['LEAN_PATH'] = ';'.join(lean_paths)
    env['TMP'] = env['TEMP'] = str(area/'tmp')
    (area/'tmp').mkdir()
    exe = Path(modules[0]['author_metadata']['command'][0])
    for m in modules:
        assert Path(m['author_metadata']['command'][0]) == exe
        assert m['author_metadata']['lean_version'] == modules[0]['author_metadata']['lean_version']
    preflight = {'time': now.isoformat(), 'area': str(area), 'dependency_manifest': pin(manifest),
                 'dependencies_count': len(inherited), 'lean_path': lean_paths, 'toolchain': pin(exe),
                 'project_author_build_in_lean_path': False, 'modules': modules,
                 'independent_scope': 'five_new_modules_plus_auditor39_only'}
    dump(area/'dependencies.json', inherited)
    dump(area/'preflight.json', preflight)
    print('PREPARED ' + str(len(inherited)) + ' pinned dependencies; starting own Lean', flush=True)

    def compile_one(stem, targets, author=None):
        rel = Path('TGLExt')/stem if author else Path(stem)
        src = area/'kernel'/rel.with_suffix('.lean')
        obj = area/'build'/rel.with_suffix('.olean')
        obj.parent.mkdir(parents=True, exist_ok=True)
        command = [str(exe), '--root='+str(area/'kernel'), '-o', str(obj), str(src)]
        stdout_path, stderr_path = area/(stem+'.stdout.txt'), area/(stem+'.stderr.txt')
        start = time.monotonic()
        with stdout_path.open('xb') as out, stderr_path.open('xb') as err:
            proc = subprocess.run(command, cwd=area/'kernel', env=env, stdout=out, stderr=err)
        outtext = stdout_path.read_text(encoding='utf-8-sig')
        errtext = stderr_path.read_text(encoding='utf-8-sig')
        amap = parse_axioms(outtext)
        item = {'command': command, 'returncode': proc.returncode, 'seconds': time.monotonic()-start,
                'source': pin(src), 'object': pin(obj) if obj.exists() else None,
                'stdout': pin(stdout_path), 'stderr': pin(stderr_path), 'axioms': amap,
                'exact_targets': set(amap) == set(targets), 'trio_only': all(set(a)<=TRIO for a in amap.values()),
                'no_warnings_or_errors': not re.search(r'(?i)\b(?:warning|error):',outtext+errtext),
                'stderr_empty': not errtext.strip()}
        if author:
            item['binary_byte_equal_to_author'] = obj.exists() and obj.read_bytes() == Path(author['object_author']['path']).read_bytes()
        dump(area/(stem+'.run.json'), item)
        print(stem+' rc='+str(proc.returncode)+' targets='+str(len(amap))+' equal='+str(item.get('binary_byte_equal_to_author')), flush=True)
        assert proc.returncode == 0 and item['exact_targets'] and item['trio_only'] and item['no_warnings_or_errors'] and item['stderr_empty'], item
        if author:
            assert item['binary_byte_equal_to_author'], 'Independent binary differs'
        return item

    results = []
    for mod in modules:
        results.append(compile_one(mod['stem'], mod['targets'], mod))
    audit = '\n'.join('import TGLExt.'+m['stem'] for m in modules) + '\n\nset_option pp.universes true\nset_option pp.proofs false\n'
    for target in all_targets:
        audit += '\n#check @'+target+'\n#print axioms '+target+'\n'
    write(area/'kernel/AuditResolventPhase39.lean', audit.encode('utf-8'))
    auditor = compile_one('AuditResolventPhase39', all_targets)
    preserved = all(pin(Path(d['source_origin']['path']))['sha256'] == d['source_origin']['sha256'] and
                    pin(Path(d['author_object']['path']))['sha256'] == d['author_object']['sha256'] and
                    pin(Path(d['frozen_source']['path']))['sha256'] == d['frozen_source']['sha256'] and
                    pin(Path(d['frozen_object']['path']))['sha256'] == d['frozen_object']['sha256'] for d in inherited)
    preserved = preserved and all(pin(Path(m['source_original']['path']))['sha256'] == m['source_original']['sha256'] and
                                 pin(Path(m['object_author']['path']))['sha256'] == m['object_author']['sha256'] for m in modules)
    result = {'time': datetime.now().astimezone().isoformat(), 'all_exit_zero': True,
              'independent_module_compilations': 5, 'independent_auditors': 1, 'exact_targets': 39,
              'trio_only': True, 'all_binary_byte_equal_to_author': True, 'pins_preserved': preserved,
              'modules': results, 'auditor': auditor, 'preflight': pin(area/'preflight.json'),
              'dependencies': pin(area/'dependencies.json'), 'lean_path': lean_paths,
              'new_project_builds_inherited': False,
              'inherited_dependencies_not_recompiled': len(inherited),
              'author_monolith_or_helpers_executed': False}
    dump(area/'compilation.json', result)
    assert preserved
    print('COMPLETE '+str(area/'compilation.json'), flush=True)

if __name__ == '__main__':
    main()
