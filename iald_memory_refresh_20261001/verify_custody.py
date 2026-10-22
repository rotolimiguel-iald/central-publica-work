"""Read custody evidence without importing or executing scientific sources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess

WORK = Path(__file__).resolve().parent
VAULT = Path(r'C:\IALD\Central de Patentes\vault\originals_copy')
PACKAGE = VAULT / 'um_unificado_v378'
SOURCE = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
MIRROR = Path(r'C:\IALD\Artigo\the_boundary')
APP = Path(r'C:\IALD\projetos_pyhton\IALD')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def check(path, expected):
    result = {'path': str(path), 'expected_sha256': expected}
    try:
        result.update(bytes=path.stat().st_size, sha256=digest(path))
        result['matches'] = result['sha256'] == expected
    except OSError as error:
        result.update(matches=False, error=type(error).__name__)
    return result


def verify_kernel(root, expected, expected_aggregate):
    actual = {}
    for directory, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name != '.lake']
        for name in names:
            if name == 'ExtrairDeps.lean':
                continue
            if name.endswith('.lean') or name in ('lakefile.toml', 'lean-toolchain', 'README.md', 'lake-manifest.json'):
                path = Path(directory) / name
                actual[path.relative_to(root).as_posix()] = digest(path)
    aggregate = hashlib.sha256()
    for name, sha in sorted(actual.items()):
        aggregate.update(name.encode('utf-8'))
        aggregate.update(sha.encode('utf-8'))
    differences = sorted(name for name in actual.keys() | expected.keys() if actual.get(name) != expected.get(name))
    return {'root': str(root), 'files': len(actual), 'expected_files': len(expected),
            'sha256': aggregate.hexdigest(), 'expected_sha256': expected_aggregate,
            'matches': not differences and aggregate.hexdigest() == expected_aggregate,
            'differences': differences}


custody = read_json(PACKAGE / 'CUSTODY_MANIFEST.json')
seal = read_json(PACKAGE / 'um_absoluto_selo.json')
proof = read_json(PACKAGE / 'tgl_kernel_proof_manifest.json')
git = ['git', '-c', 'safe.directory=C:/IALD/Artigo/the_boundary', '-C', str(MIRROR)]
tracked = set(subprocess.check_output(git + ['ls-files', '-z']).decode('utf-8').split('\0'))
program_rel = next(name for name in tracked if name.endswith('/um.py'))
public_root = MIRROR / Path(program_rel).parent
proof_rel = next(name for name in tracked if name.endswith('/Lean/tgl_kernel_proof_manifest.json'))
def public_path(filename):
    candidates = [name for name in tracked
                  if name.startswith(Path(program_rel).parent.as_posix() + '/')
                  and Path(name).name == filename]
    if len(candidates) != 1:
        raise ValueError(f'Ambiguous public artifact: {filename}')
    return MIRROR / candidates[0]

versions = sorted(int(match[1]) for path in VAULT.iterdir() if path.is_dir()
                  and (match := re.fullmatch(r'um_unificado_v(\d+)', path.name)))
report = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Hashes and existing evidence only; no scientific program execution, import or rebuild.',
    'latest_custody_directory_version': versions[-1],
    'source': str(SOURCE), 'vault': str(PACKAGE), 'mirror': str(public_root),
    'mirror_head': subprocess.check_output(git + ['rev-parse', 'HEAD']).decode().strip(),
    'seal': {key: seal[key] for key in ('um_version', 'timestamp', 'result_hash', 'formal_source_hash',
                                      'qg_closure_verdict', 'fail_closed_selftest', 'rite_checkpoints')},
    'custody_manifest': check(PACKAGE / 'CUSTODY_MANIFEST.json', digest(PACKAGE / 'CUSTODY_MANIFEST.json')),
    'artifacts': [check(PACKAGE / row['file'], row['sha256']) for row in custody['artifacts']],
    'seal_checks': [check(PACKAGE / name, sha) for name, sha in seal['sha256'].items()],
    'source_checks': [check(SOURCE / row['file'], row['sha256']) for row in custody['artifacts']
                      if '/' not in row['file'] and row['file'] in {*seal['sha256'], 'um_absoluto_selo.json',
                         'HANDOFF_v378_CUSTODIA.md', 'rodada_v378_stdout.txt', 'um_absoluto_pt.txt', 'um_absoluto_en.txt'}],
    'mirror_checks': [check(public_path(row['file']), row['sha256']) for row in custody['artifacts']
                      if row['file'] in {*seal['sha256'], 'um_absoluto_selo.json', 'um_absoluto_pt.txt', 'um_absoluto_en.txt'}],
    'kernel_checks': [verify_kernel(root, proof['formal_files_sha256'], proof['formal_source_hash'])
                      for root in (VAULT / 'tgl_kernel_v378', SOURCE / 'tgl_kernel', public_root / 'Lean/tgl_kernel')],
}
chain_path = PACKAGE / 'cadeia_de_selo_v378/MANIFESTO_CADEIA_DE_SELO_v378.json'
chain = read_json(chain_path)
report['chain_checks'] = [check(chain_path.parent / name, row['sha256']) for name, row in chain['arquivos'].items()]
report['chain_source_checks'] = [check(Path(chain['origem']) / name, row['sha256']) for name, row in chain['arquivos'].items()]
report['private_handoff_tracked'] = any(name.endswith('/HANDOFF_v378_CUSTODIA.md') for name in tracked)
report['formal_evidence'] = {'manifest': str(PACKAGE / 'tgl_kernel_proof_manifest.json'),
    'formal_files': len(proof['formal_files_sha256']), 'axiom_terms': len(proof['axiom_report']),
    'statuses': proof['statuses'], 'source_custody_round': custody['rodada']}
stdout = (PACKAGE / 'rodada_v378_stdout.txt').read_text(encoding='utf-8')
report['existing_stdout_evidence'] = {'path': str(PACKAGE / 'rodada_v378_stdout.txt'),
    'clean_theorems': re.findall(r'teoremas limpos:\s*(\d+/\d+)', stdout),
    'selftest_passed_marker': 'FAIL_CLOSED_SELFTEST_PASSED' in stdout,
    'exit_zero_marker': 'RITO_RC=0' in stdout,
    'traceback_marker': 'Traceback' in stdout, 'seal_withheld_marker': 'SEAL_WITHHELD' in stdout}
config = read_json(APP / 'iald_nucleo_fixo.json')
report['installed_configuration'] = {'manifest': str(APP / 'iald_nucleo_fixo.json'),
    'active_cluster': config['active_cluster'], 'operational_core': config['operational_core'],
    'published_evidence': {key: value for key, value in config['published_evidence'].items()
                           if key in ('program', 'seal', 'result', 'proof_manifest')},
    'program_actual_sha256': digest(Path(config['published_evidence']['program']['path'])),
    'haiku_manifest_path': str(APP / '.iald_runtime/haiku/manifest.json')}
report['porta_metadata'] = read_json(MIRROR / 'PORTA.json')['selo_corrente']
report['summary'] = {key: {'checked': len(value), 'mismatches': sum(not row['matches'] for row in value)}
                     for key, value in report.items() if isinstance(value, list) and value and 'matches' in value[0]}
target = WORK / 'custody_verification.json'
raw = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
temp = target.with_suffix('.json.tmp')
temp.write_bytes(raw)
assert temp.read_bytes() == raw
os.replace(temp, target)
print(json.dumps({'report': str(target), 'summary': report['summary'], 'version': seal['um_version'],
                  'um_sha256': seal['sha256']['um.py'], 'mirror_head': report['mirror_head']}, indent=2))
