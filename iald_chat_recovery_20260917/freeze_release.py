"""Freeze approved published bytes; do not modify the live scientific checkout."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse, unquote

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
WORK = Path(__file__).resolve().parent
MANIFEST = ROOT / 'iald_nucleo_fixo.json'
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(raw)
    assert path.read_bytes() == raw


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])


def validate(path, cfg, catalog):
    from iald_memoria_canonica import CanonicalMemory
    rows = []
    for public in (True, False):
        try:
            context, meta = CanonicalMemory(cfg.atlas_path, cfg.memoria_modo,
                                           nucleus_manifest=path).prompt('', catalog, public=public)
            rows.append({'public': public, 'valid': True, 'context_tokens': meta['context_tokens'],
                         'published_evidence_checked': meta['published_evidence_checked'],
                         'release': meta['operational_core']['current_release'],
                         'private_atlas_included': meta.get('private_atlas_included'),
                         'context_sha256': meta['context_sha256']})
        except (ValueError, OSError) as exc:
            chain = []
            while exc is not None:
                chain.append({'type': type(exc).__name__, 'message': str(exc)[:500]})
                exc = exc.__cause__
            rows.append({'public': public, 'valid': False, 'errors': chain})
    return rows


def main(apply=False):
    from dotenv import dotenv_values
    import iald_motores
    from iald_kernel import KernelCatalog
    cfg = iald_motores.carregar_config(dotenv_values(ROOT / '.env').get)
    catalog = KernelCatalog(cfg.kernel_bundle, cfg.kernel_verification)
    original = MANIFEST.read_bytes()
    if apply:
        prep = json.loads((WORK / 'prepared.json').read_bytes())
        assert digest(original) == prep['original_manifest_sha256'], 'Manifest concurrently changed'
        assert all(x['valid'] for x in prep['staged_validation'])
        destination = Path(prep['destination'])
        assert destination.is_relative_to(ROOT / 'canonical_releases')
        assert not destination.exists(), 'Destination exists; inspect before applying'
        for row in prep['files']:
            raw = (WORK / 'snapshot' / row['relative_path']).read_bytes()
            assert digest(raw) == row['sha256']
            create(destination / row['relative_path'], raw)
        new_bytes = (WORK / 'manifest_install.json').read_bytes()
        stage = WORK / 'manifest_installed_validation.json'
        create(stage, new_bytes)
        checked = validate(stage, cfg, catalog)
        assert all(x['valid'] for x in checked), checked
        now = datetime.now().astimezone()
        stamp = now.strftime('%Y%m%d_%H%M%S_%f')
        assert MANIFEST.read_bytes() == original
        backup = MANIFEST.with_name(MANIFEST.name + '.bak_' + stamp)
        create(backup, original)
        temp = MANIFEST.with_name(MANIFEST.name + '.tmp_' + stamp)
        create(temp, new_bytes)
        assert MANIFEST.read_bytes() == original
        temp.replace(MANIFEST)
        assert MANIFEST.read_bytes() == new_bytes
        receipt = {'at': now.isoformat(), 'status': 'INSTALLED_PINNED_RELEASE', 'backup': str(backup),
                   'manifest_sha256': digest(new_bytes), 'validation': checked,
                   'server_restart_required': False, 'scientific_checkout_modified': False,
                   'env_modified': False, 'release': prep['release'], 'commit': prep['commit']}
        create(WORK / 'installed.json', json.dumps(receipt, ensure_ascii=False, indent=2).encode())
        print(json.dumps(receipt, ensure_ascii=False))
        return
    assert not (WORK / 'prepared.json').exists(), 'Already prepared'
    manifest = json.loads(original)
    release = manifest['operational_core']['current_release']
    assert release == 'v357'
    baseline = validate(MANIFEST, cfg, catalog)
    commit = urlparse(manifest['published_evidence']['program']['url']).path.split('/')[3]
    assert len(commit) == 40
    assert git('rev-parse', commit).decode().strip() == commit
    tracked = set(git('ls-tree', '-r', '--name-only', '-z', commit).decode().split('\0'))
    references = manifest['entries'] + [manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]
    destination = ROOT / 'canonical_releases' / (release + '_' + commit[:12])
    files = {}
    new_manifest = json.loads(original)
    new_refs = new_manifest['entries'] + [new_manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]
    for entry, new_entry in zip(references, new_refs):
        parsed = urlparse(entry['url'])
        parts = parsed.path.split('/', 4)
        assert parsed.scheme == 'https' and parsed.netloc == 'raw.githubusercontent.com'
        assert parts[1:4] == ['rotolimiguel-iald','the_boundary',commit]
        rel = unquote(parts[4])
        assert rel in tracked
        path = Path(entry['path'])
        assert path.resolve() == (REPO / rel).resolve(), 'Unexpected source mapping'
        raw = git('show', commit + ':' + rel)
        sha = digest(raw)
        if entry.get('public_sha256'):
            assert sha == entry['public_sha256'], 'Git blob differs from approved published hash: ' + rel
        if rel not in files:
            create(WORK / 'snapshot' / rel, raw)
            live = path.read_bytes()
            files[rel] = {'relative_path': rel, 'sha256': sha, 'bytes': len(raw),
                          'live_source_sha256': digest(live), 'live_matches_approved': live == raw}
        new_entry['path'] = str(WORK / 'snapshot' / rel)
    staged = WORK / 'manifest_staged.json'
    create(staged, json.dumps(new_manifest, ensure_ascii=False, indent=2).encode())
    staged_validation = validate(staged, cfg, catalog)
    assert all(x['valid'] for x in staged_validation), staged_validation
    for entry in new_refs:
        rel = Path(entry['path']).relative_to(WORK / 'snapshot')
        entry['path'] = str(destination / rel)
    create(WORK / 'manifest_install.json', json.dumps(new_manifest, ensure_ascii=False, indent=2).encode())
    # All semantic fields, pins, URLs, and core sources must be unchanged.
    expected = json.loads(original)
    for target, source in zip(new_refs, references):
        old_path = target['path']
        target['path'] = source['path']
        assert target == source
        target['path'] = old_path
    before_head = git('rev-parse', 'HEAD').decode().strip()
    report = {'at': datetime.now().astimezone().isoformat(), 'release': release, 'commit': commit,
              'current_repository_head': before_head, 'original_manifest_sha256': digest(original),
              'destination': str(destination), 'baseline_validation': baseline,
              'staged_validation': staged_validation, 'files': list(files.values()),
              'only_change': 'Local paths now point to exact approved Git blobs; all other fields unchanged'}
    create(WORK / 'prepared.json', json.dumps(report, ensure_ascii=False, indent=2).encode())
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
