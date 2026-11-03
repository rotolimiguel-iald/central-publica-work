"""Reviewer Q9b: install_plan.json -- sha of every origin, destinations only in R, no runtime .py, unique, active manifest last, baselines match R NOW, plan vs the accepted v404 plan (normalised),
manifest_install.json internal consistency (every path under the target dir is in the plan; hashes match the staged bytes), staged tree vs plan coverage. Read-only."""
import hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
W4 = Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sh = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: json.loads(Path(p).read_bytes())
plan = rd(W / 'install_plan.json')
p4 = rd(W4 / 'install_plan.json')
files = plan['files']
out = {'plan_sha256': sh((W / 'install_plan.json').read_bytes()), 'n_files': len(files), 'top_keys': {k: (v if not isinstance(v, (list, dict)) else type(v).__name__) for k, v in plan.items()}}
bad_src, bad_dst, bad_base, missing_src = [], [], [], []
now_baseline_none = 0
for r in files:
    s, d = Path(r['source']), Path(r['destination'])
    if not s.is_file():
        missing_src.append(str(s))
        continue
    if not (s.resolve().is_relative_to(W) and sh(s.read_bytes()) == r['sha256']):
        bad_src.append(str(s))
    if not d.resolve().is_relative_to(R):
        bad_dst.append(str(d))
    cur = sh(d.read_bytes()) if d.exists() else None
    if cur != r['baseline']:
        bad_base.append((str(d), r['baseline'], cur))
    if cur is None:
        now_baseline_none += 1
out['sources_missing'] = missing_src[:5]
out['sources_hash_mismatch_or_outside_W'] = bad_src[:5]
out['destinations_outside_R'] = bad_dst[:5]
out['baseline_mismatch_now'] = bad_base[:5]
out['new_destinations(no baseline)'] = now_baseline_none
out['destinations_existing_overwritten'] = [str(Path(r['destination']).relative_to(R)) for r in files if r['baseline'] is not None]
out['unique_destinations'] = len({r['destination'] for r in files}) == len(files)
out['active_manifest_last'] = Path(files[-1]['destination']) == R / 'iald_nucleo_fixo.json' and Path(files[-1]['source']).name == 'manifest_install.json'
out['py_destinations'] = [str(Path(r['destination']).relative_to(R)) for r in files if Path(r['destination']).suffix == '.py']
out['py_at_R_root'] = [r for r in out['py_destinations'] if '\\' not in r and '/' not in r]
out['runtime_python_changes_declared'] = plan.get('runtime_python_changes')
# destination groups
import collections
c = collections.Counter()
for r in files:
    rel = Path(r['destination']).relative_to(R)
    c['/'.join(rel.parts[:2]) if rel.parts[0] == '.iald_runtime' else (rel.parts[0] if len(rel.parts) > 1 else rel.parts[0])] += 1
out['destination_groups'] = dict(c)
# vs the accepted v404 plan (normalised)


def norm(plan_, ver, commit12):
    o = {}
    for r in plan_['files']:
        d = str(Path(r['destination']).relative_to(R))
        d = d.replace('v%s_%s' % (ver, commit12), 'vXXX_commit').replace('v%s' % ver, 'vXXX')
        o[d] = r
    return o


n5 = norm(plan, '405', '6a2138d73c1a')
n4 = norm(p4, '404', '1d3c4cbe3f3c')
out['plan_v404_files'] = len(p4['files'])
out['only_in_v405'] = sorted(set(n5) - set(n4))
out['only_in_v404'] = sorted(set(n4) - set(n5))
# staged tree coverage
st = W / 'app/science/memory_stage'
staged = {str(p.relative_to(W)) for p in st.rglob('*') if p.is_file()}
excluded = {'manifest_staged.json', 'manifest_full.json', 'manifest_install.json', 'iald_nucleo_fixo.json'}
plan_src = {str(Path(r['source']).relative_to(W)) for r in files}
expect = {s for s in staged if Path(s).name not in excluded or s.endswith('manifest_install.json')}
out['staged_files_not_in_plan'] = sorted(s for s in staged if s not in plan_src and Path(s).name not in ('manifest_staged.json', 'manifest_full.json', 'iald_nucleo_fixo.json'))[:10]
out['plan_sources_outside_stage_and_packages'] = sorted(s for s in plan_src if not s.startswith('app\\science\\memory_stage') and not s.startswith('app\\packages'))
out['package_sources'] = sorted(s for s in plan_src if s.startswith('app\\packages'))
# manifest_install consistency
mi = rd(st / 'manifest_install.json')
target = R / 'canonical_releases' / ('v405_' + rd(W / 'app/RELEASE.json')['espelho_commit'][:12])
paths = []
for row in mi['entries'] + [mi['published_evidence'][k] for k in ('program', 'seal', 'result', 'proof_manifest')]:
    paths.append(row['path'])
for key in ('mother_instruction', 'operational_core', 'jev_control'):
    paths.append(mi[key]['path'])
for key in ('path', 'kernel_bundle', 'kernel_verification'):
    paths.append(mi['active_cluster'][key])
plan_dst = {r['destination']: r for r in files}
in_plan = []
for p in paths:
    P = Path(p)
    if P.is_dir() or str(P).endswith('kernel') or str(P).endswith('\\kernel'):
        in_plan.append((p, 'dir', any(d.startswith(p + '\\') for d in plan_dst)))
    else:
        in_plan.append((p, 'file', p in plan_dst))
out['manifest_install_paths_under_target'] = all(Path(p).resolve().is_relative_to(target) for p in paths)
out['manifest_install_paths_all_in_plan'] = all(x[2] for x in in_plan)
out['manifest_install_paths_not_in_plan'] = [x for x in in_plan if not x[2]][:5]
# the hashes recorded in manifest_install vs the staged bytes
hash_checks = []
for row in mi['entries']:
    src_row = plan_dst[row['path']]
    hash_checks.append(('entry:' + row['id'], row.get('public_sha256') == src_row['sha256']))
ev = mi['published_evidence']
hash_checks.append(('active_cluster.sha256', mi['active_cluster']['sha256'] == plan_dst[mi['active_cluster']['path']]['sha256']))
hash_checks.append(('operational_core.sha256', mi['operational_core']['sha256'] == plan_dst[mi['operational_core']['path']]['sha256']))
hash_checks.append(('jev_control.sha256', mi['jev_control']['sha256'] == plan_dst[mi['jev_control']['path']]['sha256']))
hash_checks.append(('mother.sha256', mi['mother_instruction']['sha256'] == plan_dst[mi['mother_instruction']['path']]['sha256']))
hash_checks.append(('release/commit/source', mi['active_cluster']['release'] == 'v405' and mi['active_cluster']['commit'] == rd(W / 'app/RELEASE.json')['espelho_commit'] and mi['active_cluster']['release_source_sha256'] == rd(W / 'app/RELEASE.json')['um_py_sha256']))
for k in ('program', 'seal', 'result', 'proof_manifest'):
    pth = ev[k]['path']
    hash_checks.append(('evidence:' + k + ' in plan', pth in plan_dst))
out['manifest_install_hash_checks_failed'] = [n for n, ok in hash_checks if not ok]
out['manifest_install_hash_checks_total'] = len(hash_checks)
# the installed manifests of the two packages
for pkg, dst in (('haiku_expanded', '.iald_runtime\\haiku55\\manifest.json'), ('shared', '.iald_runtime\\haiku\\manifest.json')):
    row = next(r for r in files if str(Path(r['destination']).relative_to(R)) == dst)
    mj = rd(row['source'])
    pre = next(r for r in files if str(Path(r['destination']).relative_to(R)) == dst.replace('manifest.json', 'prefix.md'))
    nc = next(r for r in files if str(Path(r['destination']).relative_to(R)) == dst.replace('manifest.json', 'native_count.json'))
    out['package_' + pkg] = {'manifest_prefix_sha_equals_plan_prefix_sha': mj['prefix_sha256'] == pre['sha256'], 'native_count_prefix_sha_equals': rd(nc['source'])['prefix_sha256'] == pre['sha256'], 'deployment': mj['deployment']}
print(json.dumps(out, ensure_ascii=False, indent=1))
