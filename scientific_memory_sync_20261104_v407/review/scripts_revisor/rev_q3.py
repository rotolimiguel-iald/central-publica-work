"""Revisor independente F0.3 v407 - Q3 integridade do release (somente leitura). Saida: review\\REV_Q3.json"""
import sys, os, json, hashlib, re, sqlite3
sys.dont_write_bytecode = True
from pathlib import Path
from contextlib import closing

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


out = {'problems': []}
prep = json.loads((W / ('PREPARATION_' + EPOCH + '.json')).read_bytes())
mraw = (REL / 'manifest.json').read_bytes()
manifest = json.loads(mraw)
out['manifest_file'] = {'bytes': len(mraw), 'sha256': sha(mraw), 'prep_pin': prep['manifest'],
                        'eq_prep_pin': (len(mraw) == prep['manifest']['bytes'] and sha(mraw) == prep['manifest']['sha256'])}
out['manifest_top_keys'] = {k: (v if k != 'documents' else '<13 docs>') for k, v in manifest.items()}
if not out['manifest_file']['eq_prep_pin']:
    out['problems'].append('manifest pin differs from PREPARATION')

# the .bak manifest (first save, inside build) vs final
baks = sorted(p for p in REL.glob('manifest.json.bak_*'))
out['manifest_bak_files'] = [p.name for p in baks]
for b in baks:
    first = json.loads(b.read_bytes())
    stripped = {k: v for k, v in manifest.items() if k not in cm.SNAPSHOT_FIELDS}
    out['manifest_bak_vs_final'] = {
        'bak_bytes': b.stat().st_size,
        'final_minus_SNAPSHOT_FIELDS_equals_bak': stripped == first,
        'keys_only_in_final': sorted(set(manifest) - set(first)),
        'keys_only_in_bak': sorted(set(first) - set(manifest)),
    }
    if not out['manifest_bak_vs_final']['final_minus_SNAPSHOT_FIELDS_equals_bak']:
        out['problems'].append('manifest.json.bak differs from final beyond SNAPSHOT_FIELDS')

# SEALED_SNAPSHOT.json
sraw = (SNAP / 'SEALED_SNAPSHOT.json').read_bytes()
binding = json.loads(sraw)
seal = json.loads((SNAP / 'um_absoluto_selo.json').read_bytes())
proof = json.loads((SNAP / 'tgl_kernel_proof_manifest.json').read_bytes())
out['sealed_snapshot'] = {
    'bytes': len(sraw), 'sha256': sha(sraw),
    'manifest_snapshot_manifest_sha256': manifest['snapshot_manifest_sha256'],
    'sha_eq_manifest_field': sha(sraw) == manifest['snapshot_manifest_sha256'],
    'keys': sorted(binding),
    'schema': binding['schema'],
    'source_mode': binding['source_mode'], 'manifest_source_mode': manifest['source_mode'],
    'release': binding['release'],
    'generation_eq_manifest': binding['generation'] == manifest['generation'],
    'index_sha256_eq_manifest': binding['index_sha256'] == manifest['index_sha256'],
    'documents_eq_manifest_name_sha_bytes': binding['documents'] == [{k: d[k] for k in ('name', 'sha256', 'bytes')} for d in manifest['documents']],
    'formal_source_hash': binding['formal_source_hash'],
    'formal_source_hash_eq_seal_in_snapshot': binding['formal_source_hash'] == seal['formal_source_hash'],
    'formal_source_hash_eq_proof_in_snapshot': binding['formal_source_hash'] == proof['formal_source_hash'],
    'snapshot_root_in_manifest': manifest['snapshot_root'],
    'snapshot_root_eq_actual': Path(manifest['snapshot_root']) == SNAP,
    'n_documents': len(binding['documents']),
    'names_eq_SNAPSHOT_NAMES': {d['name'] for d in binding['documents']} == set(cm.SNAPSHOT_NAMES),
}
for k, v in out['sealed_snapshot'].items():
    if isinstance(v, bool) and not v:
        out['problems'].append('sealed_snapshot check false: ' + k)

# the snapshot directory has exactly the 13 + SEALED_SNAPSHOT.json (no extras, no symlinks)
files_in_snap = sorted(p.name for p in SNAP.iterdir())
out['snapshot_dir_listing'] = files_in_snap
out['snapshot_dir_extras'] = sorted(set(files_in_snap) - set(cm.SNAPSHOT_NAMES) - {'SEALED_SNAPSHOT.json'})
out['snapshot_dir_symlinks'] = [p.name for p in SNAP.iterdir() if p.is_symlink()]
# release dir listing (all files, recursive)
out['release_tree'] = sorted(str(p.relative_to(REL)) for p in REL.rglob('*') if p.is_file())
out['release_tree_dirs'] = sorted(str(p.relative_to(REL)) for p in REL.rglob('*') if p.is_dir())
out['leftover_tmp_or_journal'] = [str(p.relative_to(REL)) for p in REL.rglob('*') if re.search(r'(\.tmp_|-journal$|-wal$|-shm$|^tmp)', p.name)]

# --- index
ipath = REL / 'index.sqlite3'
ib = ipath.read_bytes()
out['index'] = {'bytes': len(ib), 'sha256': sha(ib), 'manifest_index_sha256': manifest['index_sha256'],
                'sha_eq_manifest': sha(ib) == manifest['index_sha256'],
                'header_magic': ib[:16], 'file_format_write_version': ib[18], 'file_format_read_version': ib[19],
                'journal_mode_is_rollback_legacy': (ib[18] == 1 and ib[19] == 1)}
out['index']['header_magic'] = out['index']['header_magic'].decode('latin1')
if not out['index']['sha_eq_manifest']:
    out['problems'].append('index sha != manifest')

uri = ipath.resolve().as_uri() + '?mode=ro'
out['index']['uri_used'] = uri
with closing(sqlite3.connect(uri, uri=True)) as db:
    out['sqlite_version'] = sqlite3.sqlite_version
    out['index']['integrity_check'] = [r[0] for r in db.execute('PRAGMA integrity_check').fetchall()]
    out['index']['count_passages'] = db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]
    out['index']['manifest_chunks'] = manifest['chunks']
    out['index']['count_eq_manifest_chunks'] = out['index']['count_passages'] == manifest['chunks']
    out['index']['sqlite_master'] = [(t, n) for t, n, s in db.execute('SELECT type,name,sql FROM sqlite_master')]
    out['index']['fts_schema_sql'] = db.execute("SELECT sql FROM sqlite_master WHERE name='passages'").fetchone()[0]
    out['index']['journal_mode_reported'] = db.execute('PRAGMA journal_mode').fetchone()[0]
    out['index']['documents_in_index'] = [(d, n) for d, n in db.execute('SELECT document, COUNT(*) FROM passages GROUP BY document ORDER BY MIN(rowid)')]
    out['index']['rowid_range'] = db.execute('SELECT MIN(rowid), MAX(rowid) FROM passages').fetchone()
    if out['index']['integrity_check'] != ['ok']:
        out['problems'].append('integrity_check != ok')
    if not out['index']['count_eq_manifest_chunks']:
        out['problems'].append('count != manifest chunks')

    # chunk comparison for ALL 13 documents, against the LIVE originals (independent of the snapshot copies) and against the snapshot copies
    per_doc = []
    for d in manifest['documents']:
        name = d['name']
        live_path = [e['source'] for e in json.loads(cm.CATALOG.read_bytes())['files'] if Path(e['source']).name == name][0]
        live_text = Path(live_path).read_bytes().decode('utf-8-sig')
        snap_text = (SNAP / name).read_bytes().decode('utf-8-sig')
        expected_live = list(cm.chunks(live_text))
        expected_snap = list(cm.chunks(snap_text))
        actual = [(int(a), int(b), t) for a, b, t in db.execute('SELECT first_line,last_line,body FROM passages WHERE document=? ORDER BY rowid', (name,))]
        bodies = ''.join(t for _, _, t in actual)
        # contiguity of line numbers
        contiguous = True
        prev_last = 0
        for a, b, t in actual:
            if not (a == prev_last + 1 or a == prev_last):
                contiguous = False
            prev_last = b
        lines_total = len(live_text.splitlines(keepends=True))
        row = {'name': name, 'passages': len(actual),
               'eq_cm_chunks_of_LIVE_text': actual == expected_live,
               'eq_cm_chunks_of_SNAPSHOT_text': actual == expected_snap,
               'concat_bodies_eq_full_text': bodies == live_text,
               'line_numbers_contiguous': contiguous,
               'first_line_of_first': actual[0][0] if actual else None,
               'last_line_of_last': actual[-1][1] if actual else None,
               'splitlines_count_of_text': lines_total,
               'last_line_eq_splitlines_count': (actual[-1][1] == lines_total) if actual else None,
               'text_chars': len(live_text), 'text_has_CRLF': ('\r\n' in live_text), 'text_has_BOM_in_raw': Path(live_path).read_bytes()[:3] == b'\xef\xbb\xbf'}
        per_doc.append(row)
        if not (row['eq_cm_chunks_of_LIVE_text'] and row['eq_cm_chunks_of_SNAPSHOT_text'] and row['concat_bodies_eq_full_text']):
            out['problems'].append('passages differ for ' + name)
    out['per_document'] = per_doc
    out['sum_passages_per_doc'] = sum(r['passages'] for r in per_doc)
    out['sum_eq_manifest_chunks'] = out['sum_passages_per_doc'] == manifest['chunks']

    # statute names: FTS and literal
    est = json.loads((W / ('ESTATUTOS_' + EPOCH + '.json')).read_bytes())
    stat = {}
    for rn in est['records']:
        fts = [(d, n) for d, n in db.execute('SELECT document, COUNT(*) FROM passages WHERE passages MATCH ? GROUP BY document', ('"' + rn + '"',))]
        # literal substring (python side) over all bodies
        lit = {}
        for rid, doc, body in db.execute('SELECT rowid, document, body FROM passages'):
            if rn in body:
                lit[doc] = lit.get(doc, 0) + 1
        stat[rn] = {'fts_hits_by_document': fts, 'literal_substring_hits_by_document': lit,
                    'indexed_in_um_absoluto_json_fts': any(d == 'um_absoluto.json' for d, _ in fts),
                    'indexed_in_um_absoluto_json_literal': 'um_absoluto.json' in lit}
        if not fts:
            out['problems'].append('statute not FTS-indexed: ' + rn)
    out['statutes_indexed'] = stat

(REV / 'REV_Q3.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('problems:', out['problems'])
print(json.dumps({k: out[k] for k in ('manifest_file', 'manifest_top_keys', 'manifest_bak_files', 'manifest_bak_vs_final', 'sealed_snapshot', 'snapshot_dir_extras', 'snapshot_dir_symlinks', 'leftover_tmp_or_journal', 'release_tree', 'release_tree_dirs')}, ensure_ascii=False, indent=1))
ix = dict(out['index'])
print(json.dumps(ix, ensure_ascii=False, indent=1))
for r in out['per_document']:
    print(r)
print('sum passages', out['sum_passages_per_doc'], 'eq manifest', out['sum_eq_manifest_chunks'])
print(json.dumps(out['statutes_indexed'], ensure_ascii=False, indent=1))
