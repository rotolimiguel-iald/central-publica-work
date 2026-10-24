"""Synthetic sealed canonical-memory snapshot builder (own implementation, written from the
verification rules in canonical_memory._verify_snapshot / resolve_directory). No production data."""
import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

SNAPSHOT_MODE = 'SEALED_IMMUTABLE_SNAPSHOT'
NAMES = ['um.py', 'um_absoluto.json', 'um_absoluto_selo.json', 'tgl_kernel_proof_manifest.json',
         'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md', 'A_PROVA_DA_QG_TGL_arvore.md',
         'DESENHO_DO_FECHAMENTO_QG.md', 'MEMORIA_DA_LINHAGEM.md', 'DA_IRMA.md',
         'A Ponte Einstein Cartan Miguel.tex', 'paper_PT.tex',
         'ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md']


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dump(o):
    return json.dumps(o, ensure_ascii=False, indent=2).encode()


def build_release(releases_root, anchor_size=1600, body_lines=40):
    """Creates <releases_root>/<epoch>/{manifest.json,index.sqlite3,snapshots/<epoch>/...}. Returns (release_dir, manifest)."""
    formal = sha(b'SYNTHETIC_NOT_A_SCIENTIFIC_PROOF')
    data = {}
    for n in NAMES:
        # several lines so that FTS returns more than one passage per document
        data[n] = ('synthetic document ' + n + '\n' + ''.join('linha %d de %s com termos tgl identidade fronteira\n' % (i, n) for i in range(body_lines))).encode()
    data['um.py'] = b'# synthetic text fixture; NEVER executed/imported\n'
    data['um_absoluto.json'] = b'{}'
    data['tgl_kernel_proof_manifest.json'] = dump(dict(formal_source_hash=formal))
    data['um_absoluto_forma_canonica.md'] = ('A' * anchor_size + '\n').encode()
    data['um_absoluto_selo.json'] = dump(dict(
        um_version='v999', fail_closed_selftest='FAIL_CLOSED_SELFTEST_PASSED', formal_source_hash=formal,
        sha256={n: sha(data[n]) for n in ['um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json']}))
    docs = [dict(name=n, sha256=sha(data[n]), bytes=len(data[n])) for n in sorted(data)]
    generation = sha(json.dumps([(d['name'], d['sha256']) for d in docs], ensure_ascii=False).encode())
    epoch = 'v999_' + generation[:16]
    release = Path(releases_root) / epoch
    snap_root = release / 'snapshots' / epoch
    snap_root.mkdir(parents=True)
    for d in docs:
        p = snap_root / d['name']
        p.write_bytes(data[d['name']])
        d.update(path=str(p), mtime_ns=p.stat().st_mtime_ns)
    with closing(sqlite3.connect(release / 'index.sqlite3')) as db:
        db.execute('CREATE VIRTUAL TABLE passages USING fts5(body,document UNINDEXED,first_line UNINDEXED,last_line UNINDEXED)')
        for d in docs:
            text = data[d['name']].decode()
            lines = text.splitlines()
            # chunk into passages of ~10 lines so retrieval is non-trivial
            step = 10
            for i in range(0, len(lines), step):
                chunk = '\n'.join(lines[i:i + step])
                db.execute('INSERT INTO passages VALUES(?,?,?,?)', (chunk, d['name'], i + 1, min(i + step, len(lines))))
        db.commit()
    index_hash = sha((release / 'index.sqlite3').read_bytes())
    desc = dict(schema=1, source_mode=SNAPSHOT_MODE, release='v999', generation=generation, index_sha256=index_hash,
                documents=[{k: d[k] for k in ['name', 'sha256', 'bytes']} for d in docs], formal_source_hash=formal)
    (snap_root / 'SEALED_SNAPSHOT.json').write_bytes(dump(desc))
    manifest = dict(schema=1, built_at='SYNTHETIC_FIXTURE_ONLY', generation=generation, index_sha256=index_hash,
                    documents=docs, chunks=-1, scope='SYNTHETIC_TEST_ONLY', source_mode=SNAPSHOT_MODE,
                    snapshot_root=str(snap_root), snapshot_manifest_sha256=sha((snap_root / 'SEALED_SNAPSHOT.json').read_bytes()))
    (release / 'manifest.json').write_bytes(dump(manifest))
    return release, manifest


def make_active(copy_root):
    """Creates the synthetic ACTIVE pointer + release under <copy_root>/state/canonical_memory."""
    base = Path(copy_root) / 'state' / 'canonical_memory'
    releases = base / 'releases'
    releases.mkdir(parents=True, exist_ok=True)
    release, manifest = build_release(releases)
    active = dict(schema=1, release='v999', epoch=release.name, generation=manifest['generation'],
                  manifest_sha256=sha((release / 'manifest.json').read_bytes()))
    (base / 'ACTIVE.json').write_bytes(dump(active))
    return release, manifest
