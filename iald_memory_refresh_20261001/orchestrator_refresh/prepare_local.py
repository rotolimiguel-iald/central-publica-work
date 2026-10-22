"""Prepare a sealed local candidate only. Never activate, dispatch or edit sources."""
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import socket
import sqlite3
import sys
from unittest.mock import patch

WORK = Path(__file__).resolve().parent
PARENT = WORK.parent
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
ROOTS = (Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'),
         Path(r'C:\IALD\Artigo\the_boundary'))
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as memory
from iald_orchestrator.safe_files import save_json


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_write_guard(event, args):
    if event in ('subprocess.Popen', 'os.system', 'socket.connect', 'socket.getaddrinfo'):
        raise RuntimeError('External execution/network forbidden')
    if event == 'open':
        path, mode, flags = args
        writable = (isinstance(mode, str) and any(x in mode for x in 'wax+')) or (
            isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)))
        if writable and not isinstance(path, int) and not Path(path).resolve().is_relative_to(WORK.resolve()):
            raise RuntimeError('Write outside refresh staging forbidden')
    if event in ('os.rename', 'os.remove', 'os.rmdir', 'os.mkdir'):
        for value in args[:2] if event == 'os.rename' else args[:1]:
            if isinstance(value, (str, bytes)) and not Path(os.fsdecode(value)).resolve().is_relative_to(WORK.resolve()):
                raise RuntimeError('Filesystem mutation outside refresh staging forbidden')


def queue_metadata():
    path = BASE / 'state/tasks.sqlite3'
    with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as db:
        db.execute('PRAGMA query_only=ON')
        data = {}
        for table, field, terminal in (
            ('tasks', 'status', ('result_ready', 'completed', 'failed', 'cancelled', 'interrupted')),
            ('coordination_jobs', 'stage', ('completed', 'failed', 'cancelled')),
        ):
            marks = ','.join('?' for _ in terminal)
            data[table] = {'counts': db.execute(f'SELECT {field},COUNT(*) FROM {table} GROUP BY {field}').fetchall(),
                'nonterminal': db.execute(f"SELECT id,{field},json_extract(execution_constraints,'$.memory_generation') "
                    f'FROM {table} WHERE {field} NOT IN ({marks})', terminal).fetchall()}
        data['running_attempts'] = db.execute(
            "SELECT COUNT(*) FROM attempts WHERE status='running' AND finished_at IS NULL").fetchone()[0]
        return data


def main():
    target = WORK / 'candidate'
    if target.exists():
        raise RuntimeError('Candidate already exists; preserve it, do not overwrite')
    catalog = json.loads(memory.CATALOG.read_bytes())
    active = json.loads((memory.MEMORY / 'manifest.json').read_bytes())
    before = {str(path): sha(path) for path in (
        memory.CATALOG, memory.MEMORY / 'manifest.json', memory.MEMORY / 'index.sqlite3',
        BASE / 'state/tasks.sqlite3', BASE / 'iald_orchestrator/canonical_memory.py')}
    queues = queue_metadata()
    custody = json.loads((PARENT / 'custody_verification.json').read_bytes())
    release = json.loads((PARENT / 'release_inputs.json').read_bytes())
    assert release['release'] == custody['seal']['um_version'] == 'v378'
    expected = {Path(row['path']).name: row['sha256'] for row in custody['artifacts'] if row.get('matches')}
    program = next(row for row in release['artifacts'] if row['name'] == 'um.py')
    assert program['sha256'] == release['source_sha256'] == expected['um.py']
    files, checks, changes = [], [], []
    for item in catalog['files']:
        original = Path(item['source'])
        if original.suffix.lower() == '.pdf':
            continue
        if not any(original.resolve().is_relative_to(root.resolve()) for root in ROOTS):
            raise ValueError('Registered source outside scientific roots')
        wanted = expected.get(original.name, item['sha256'])
        original_hash = sha(original)
        selected = original
        if original.name == 'um.py' and original_hash != wanted:
            # PROPOSAL ONLY: use the already verified public v378 program.
            # Never replace the live Physics program or the registered catalog.
            selected = Path(program['source_path'])
            changes.append({'name': original.name, 'registered_source': str(original),
                'observed_registered_sha256': original_hash, 'proposed_source': str(selected),
                'required_sha256': wanted,
                'reason': 'Live Physics program has diverged from the sealed v378 result/seal'})
        if not any(selected.resolve().is_relative_to(root.resolve()) for root in ROOTS):
            raise ValueError('Proposed source outside scientific roots')
        if memory.FORBIDDEN.search(str(selected)):
            raise ValueError('Forbidden source')
        measured = sha(selected)
        if measured != wanted:
            raise ValueError('Source differs from verified v378 custody or unchanged snapshot: ' + original.name)
        files.append({'name': original.name, 'source': str(selected), 'sha256': measured})
        checks.append({'name': original.name, 'registered_source': str(original),
            'selected_source': str(selected), 'registered_sha256': original_hash,
            'selected_sha256': measured, 'matches_prior_fisica_snapshot': measured == item['sha256']})
    if len(files) != 13:
        raise ValueError('Unexpected source allowlist size')
    proposal = {'schema': 1, 'scope': 'STAGED_INDEX_CATALOG_ONLY__NOT_A_FISICA_SNAPSHOT_OR_INSTALLATION',
        'target_release': release['release'], 'source_catalog': str(memory.CATALOG),
        'source_catalog_sha256': before[str(memory.CATALOG)], 'source_changes_proposed': changes,
        'files': files}
    proposed_path = WORK / 'MANIFESTO_LOCAL.index_v378.proposed.json'
    save_json(proposed_path, proposal)
    save_json(WORK / 'preflight.json', {'protected_before': before, 'queue_metadata': queues,
        'active_generation': active['generation'], 'source_checks': checks,
        'registered_catalog_modified': False, 'proposal_installed': False})

    # Existing builder and its byte-exact backups/atomic replace; destination W only.
    result = memory.build(directory=target, catalog=proposed_path)
    assert result['generation'] == memory.digest(json.dumps(
        [(d['name'], d['sha256']) for d in result['documents']], ensure_ascii=False).encode())
    assert sha(target / 'index.sqlite3') == result['index_sha256']
    loaded, freshness = memory.load(target, refresh=False)
    assert loaded['generation'] == result['generation']
    with closing(sqlite3.connect((target / 'index.sqlite3').resolve().as_uri() + '?mode=ro', uri=True)) as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        assert db.execute('SELECT COUNT(*) FROM passages').fetchone()[0] == result['chunks']
    # This is an offline retrieval probe, not a job, provider request or dispatch.
    packet = memory.prepare('the_dissipation_law_with_contrast_v378', directory=target,
                            allowed_sources=['um.py'])
    assert packet['receipt']['generation'] == result['generation']
    assert all(row['sha256'] == release['source_sha256'] for row in packet['receipt']['sources'])
    assert 'v378' in packet['prompt']
    for row in result['documents']:
        assert sha(row['path']) == row['sha256'], 'Source changed after preparation'
    protected_after = {path: sha(path) for path in before}
    if before != protected_after:
        raise ValueError('Protected state changed during preparation; external activity requires review')
    record = {'state': 'PREPARED_NOT_ACTIVATED', 'target_release': release['release'],
        'source_sha256': release['source_sha256'], 'candidate_generation': result['generation'],
        'candidate_index_sha256': result['index_sha256'], 'documents': len(result['documents']),
        'chunks': result['chunks'], 'built_at': result['built_at'], 'freshness': freshness,
        'active_generation_preserved': active['generation'], 'protected_hashes_unchanged': True,
        'queue_metadata': queues, 'proposal': str(proposed_path),
        'source_changes_proposed': changes, 'retrieval_receipt': packet['receipt'],
        'inference_calls': 0, 'network_calls': 0, 'job_mutations': 0,
        'blockers': ['The registered live program no longer matches the sealed v378 SHA.',
            'One existing nonterminal coordination has a fixed generation different from the current cache.',
            'Existing publish/read path has no atomic pair selection across processes; see offline reproducer.']}
    save_json(WORK / 'refresh_receipt.json', record)
    print(json.dumps({key: record[key] for key in ('state', 'target_release', 'source_sha256',
        'candidate_generation', 'candidate_index_sha256', 'documents', 'chunks', 'protected_hashes_unchanged')}))


if __name__ == '__main__':
    sys.addaudithook(local_write_guard)
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
        main()
