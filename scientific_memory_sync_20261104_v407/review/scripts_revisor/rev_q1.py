"""Revisor independente F0.3 v407 - Q1 e Q2 (somente leitura). Saida: review\\REV_Q1_Q2.json"""
import sys, os, json, hashlib, re
sys.dont_write_bytecode = True
from pathlib import Path

BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as cm

W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
REV = W / 'review'
EPOCH = 'v407_4323b401f15cc971'
REL = cm.RELEASES / EPOCH
SNAP = REL / 'snapshots' / EPOCH


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {'EPOCH': EPOCH, 'files': [], 'problems': []}
prep = json.loads((W / ('PREPARATION_' + EPOCH + '.json')).read_bytes())
manifest = json.loads((REL / 'manifest.json').read_bytes())
catalog = json.loads(cm.CATALOG.read_bytes())
entries = [e for e in catalog['files'] if Path(e['source']).suffix.lower() != '.pdf']
out['catalog_n_entries_total'] = len(catalog['files'])
out['catalog_n_text_entries'] = len(entries)
out['catalog_names_equal_SNAPSHOT_NAMES'] = {Path(e['source']).name for e in entries} == set(cm.SNAPSHOT_NAMES)
out['catalog_pin_now'] = {'bytes': len(cm.CATALOG.read_bytes()), 'sha256': sha(cm.CATALOG.read_bytes())}
out['catalog_pin_in_PREPARATION'] = prep['catalog_pin']
out['catalog_pin_equal'] = (out['catalog_pin_now']['sha256'] == prep['catalog_pin']['sha256'] and out['catalog_pin_now']['bytes'] == prep['catalog_pin']['bytes'])

prep_src = {Path(p['path']).name: p for p in prep['sources']}
man_docs = {d['name']: d for d in manifest['documents']}
live = {}
for e in entries:
    p = Path(e['source'])
    name = p.name
    live_b = p.read_bytes()
    live_st = p.stat()
    snap_p = SNAP / name
    snap_b = snap_p.read_bytes()
    snap_st = snap_p.stat()
    row = {
        'name': name,
        'live_path': str(p),
        'live_is_symlink': p.is_symlink(),
        'live_bytes': len(live_b), 'live_sha256': sha(live_b), 'live_mtime_ns': live_st.st_mtime_ns,
        'snap_bytes': len(snap_b), 'snap_sha256': sha(snap_b), 'snap_mtime_ns': snap_st.st_mtime_ns,
        'byte_for_byte_live_eq_snapshot': live_b == snap_b,
        'prep_sha256': prep_src[name]['sha256'], 'prep_bytes': prep_src[name]['bytes'], 'prep_mtime_ns': prep_src[name]['mtime_ns'],
        'prep_path_equal_catalog_source': prep_src[name]['path'] == str(p),
        'manifest_sha256': man_docs[name]['sha256'], 'manifest_bytes': man_docs[name]['bytes'],
        'manifest_matches_fisica_snapshot': man_docs[name].get('matches_fisica_snapshot'),
        'manifest_path': man_docs[name]['path'],
    }
    row['live_sha_eq_snap_sha'] = row['live_sha256'] == row['snap_sha256']
    row['live_sha_eq_prep'] = row['live_sha256'] == row['prep_sha256']
    row['snap_sha_eq_prep'] = row['snap_sha256'] == row['prep_sha256']
    row['manifest_sha_eq_all'] = row['manifest_sha256'] == row['live_sha256'] == row['snap_sha256'] == row['prep_sha256']
    row['bytes_all_equal'] = len({row['live_bytes'], row['snap_bytes'], row['prep_bytes'], row['manifest_bytes']}) == 1
    row['live_mtime_eq_prep_mtime'] = row['live_mtime_ns'] == row['prep_mtime_ns']
    row['snap_mtime_eq_prep_mtime'] = row['snap_mtime_ns'] == row['prep_mtime_ns']
    row['manifest_path_is_snapshot_copy'] = (man_docs[name]['path'] == str(snap_p))
    out['files'].append(row)
    live[name] = live_b
    if not (row['byte_for_byte_live_eq_snapshot'] and row['manifest_sha_eq_all'] and row['bytes_all_equal']):
        out['problems'].append('Q1 divergence: ' + name)
    if not row['live_mtime_eq_prep_mtime']:
        out['problems'].append('Q1 live mtime changed since preparation: ' + name)

# --- selo / programa / prova
seal = json.loads(live['um_absoluto_selo.json'])
proof = json.loads(live['tgl_kernel_proof_manifest.json'])
prog = live['um.py'].decode('utf-8-sig')
selo = {}
selo['um_version'] = seal.get('um_version')
selo['um_version_is_v407'] = seal.get('um_version') == 'v407'
selo['fail_closed_selftest'] = seal.get('fail_closed_selftest')
selo['fail_closed_ok'] = seal.get('fail_closed_selftest') == 'FAIL_CLOSED_SELFTEST_PASSED'
selo['formal_source_hash_seal'] = seal.get('formal_source_hash')
selo['formal_source_hash_proof_manifest'] = proof.get('formal_source_hash')
selo['formal_source_hash_equal'] = seal.get('formal_source_hash') == proof.get('formal_source_hash')
selo['seal_sha256_listed_names'] = sorted(seal['sha256'])
checks = {}
for name, h in seal['sha256'].items():
    if name in live:
        checks[name] = (sha(live[name]) == h)
selo['seal_sha256_vs_live_for_files_among_the_13'] = checks
selo['seal_sha256_names_not_among_13'] = sorted(n for n in seal['sha256'] if n not in live)
selo['seal_sha256_all_among_13_match'] = all(checks.values()) and len(checks) > 0
selo['mandatory_three_in_seal_and_match'] = {n: (seal['sha256'].get(n) == sha(live[n])) for n in ('um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json')}
selo['files_among_13_not_listed_in_seal'] = sorted(n for n in live if n not in seal['sha256'])
# every seal key related to verdict (informational only)
selo['keys_with_verdict'] = {k: (v if isinstance(v, (str, bool, int)) else '<%s>' % type(v).__name__) for k, v in seal.items() if 'verdict' in k.lower()}
out['selo'] = selo
rx = re.findall(r'(?m)^UM_VERSION\s*=\s*["\'](v[0-9]+)["\']', prog)
out['um_py'] = {
    'regex_helper_findall': rx,
    'regex_equals_[v407]': rx == ['v407'],
    'substring_count_UM_VERSION_space_eq_dq_v407': prog.count('UM_VERSION = "v407"'),
    'substring_count_UM_VERSION_any': prog.count('UM_VERSION'),
}
ctx = []
for m in re.finditer(r'UM_VERSION', prog):
    s = max(0, m.start() - 30)
    ctx.append(prog[s:m.end() + 40].replace('\n', '\\n'))
    if len(ctx) >= 12:
        break
out['um_py']['first_UM_VERSION_contexts'] = ctx

# --- estatutos no core
core = json.loads(live['um_absoluto.json'])['core']
st_all = [k for k in core if k.startswith('estatuto_')]
st_dict = {k: v for k, v in core.items() if k.startswith('estatuto_') and isinstance(v, dict)}
out['estatutos_core'] = {
    'all_estatuto_keys_in_core': st_all,
    'dict_estatuto_keys': list(st_dict),
    'all_verified_True': {k: v.get('all_verified') is True for k, v in st_dict.items()},
    'does_not_gate_core_True': {k: v.get('does_not_gate_core') is True for k, v in st_dict.items()},
    'cert_um_py_sha256_lido_de_si': {k: (v.get('certificacao', {}).get('um_py_sha256_lido_de_si') if isinstance(v.get('certificacao'), dict) else None) for k, v in st_dict.items()},
    'um_py_sha256_live': sha(live['um.py']),
}
est_file = json.loads((W / ('ESTATUTOS_' + EPOCH + '.json')).read_bytes())
out['estatutos_file'] = {
    'record_names': list(est_file['records']),
    'records_equal_core_dict_records_now': est_file['records'] == st_dict,
    'source_pin': est_file['source'],
    'source_pin_sha_eq_live_um_absoluto': est_file['source']['sha256'] == sha(live['um_absoluto.json']),
    'source_pin_bytes_eq_live': est_file['source']['bytes'] == len(live['um_absoluto.json']),
    'source_path_is_snapshot_copy': est_file['source']['path'] == str(SNAP / 'um_absoluto.json'),
    'all_verified': {k: v.get('all_verified') is True for k, v in est_file['records'].items()},
    'does_not_gate_core': {k: v.get('does_not_gate_core') is True for k, v in est_file['records'].items()},
    'prep_statute_record_names': prep['statute_record_names'],
    'names_equal_prep': list(est_file['records']) == prep['statute_record_names'],
}

# --- Q2 generation / epoch
pairs = [(Path(e['source']).name, sha(live[Path(e['source']).name])) for e in entries]
gen_live = hashlib.sha256(json.dumps(pairs, ensure_ascii=False).encode()).hexdigest()
pairs_snap = [(Path(e['source']).name, sha((SNAP / Path(e['source']).name).read_bytes())) for e in entries]
gen_snap = hashlib.sha256(json.dumps(pairs_snap, ensure_ascii=False).encode()).hexdigest()
pairs_man = [(d['name'], d['sha256']) for d in manifest['documents']]
gen_man = hashlib.sha256(json.dumps(pairs_man, ensure_ascii=False).encode()).hexdigest()
out['Q2'] = {
    'generation_recomputed_from_LIVE_in_catalog_order': gen_live,
    'generation_recomputed_from_SNAPSHOT_in_catalog_order': gen_snap,
    'generation_recomputed_from_manifest_docs_order': gen_man,
    'manifest_generation': manifest['generation'],
    'prep_generation': prep['generation'],
    'catalog_order_names': [n for n, _ in pairs],
    'manifest_order_names': [n for n, _ in pairs_man],
    'orders_equal': [n for n, _ in pairs] == [n for n, _ in pairs_man],
    'epoch_expected': 'v407_' + gen_live[:16],
    'epoch_in_manifest_snapshot_root': Path(manifest['snapshot_root']).name,
    'release_dir_name': REL.name,
    'epoch_equal_everywhere': ('v407_' + gen_live[:16]) == REL.name == Path(manifest['snapshot_root']).name == prep['epoch'],
    'generation_all_equal': len({gen_live, gen_snap, gen_man, manifest['generation'], prep['generation']}) == 1,
    'CHECK_ANTES_sealed_generation': json.loads((W / 'CHECK_ANTES_v407.json').read_bytes())['sealed_generation'],
}
out['Q2']['check_antes_eq_recomputed'] = out['Q2']['CHECK_ANTES_sealed_generation'] == gen_live

# 16 hex digits requested
out['pins16'] = {
    'um.py': sha(live['um.py'])[:16],
    'um_absoluto.json': sha(live['um_absoluto.json'])[:16],
    'um_absoluto_selo.json': sha(live['um_absoluto_selo.json'])[:16],
    'tgl_kernel_proof_manifest.json': sha(live['tgl_kernel_proof_manifest.json'])[:16],
}
(REV / 'REV_Q1_Q2.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
# brief console summary
print('problems:', out['problems'])
for r in out['files']:
    print('%-62s live==snap bytes:%s sha_all_eq:%s live_mtime==prep:%s snap_mtime==prep:%s manifest_matches_fisica:%s' % (r['name'], r['byte_for_byte_live_eq_snapshot'], r['manifest_sha_eq_all'], r['live_mtime_eq_prep_mtime'], r['snap_mtime_eq_prep_mtime'], r['manifest_matches_fisica_snapshot']))
print(json.dumps({k: out[k] for k in ('selo', 'um_py', 'estatutos_core', 'estatutos_file', 'Q2', 'pins16')}, ensure_ascii=False, indent=1))
