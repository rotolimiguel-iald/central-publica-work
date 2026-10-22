"""Copy existing inputs into an isolated runtime; never execute source originals."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import ast
import hashlib
import json
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um')
RUN = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'RODADA_INTEGRAL_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
assert RUN.resolve().is_relative_to(ROOT) and RUN.name.startswith('RODADA_INTEGRAL_')

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def write_json(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data)
    assert tmp.stat().st_size == len(data)
    os.replace(tmp, path)

def enumerate_files(source, target, role):
    result = []
    for base, dirs, files in os.walk(source, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            if path.is_symlink() or path.is_junction():
                raise RuntimeError(f'Unexpected link: {path}')
        for name in files:
            path = Path(base) / name
            result.append((path, target / path.relative_to(source), role))
    if not result:
        raise RuntimeError(f'No readable inputs: {source}')
    return result

def copy_checked(item):
    source, target, role = item
    assert target.is_relative_to(RUN)
    before = source.stat()
    long_source = Path('\\\\?\\' + str(source.resolve()))
    long_target = Path('\\\\?\\' + str(target.absolute()))
    source_hash = digest(long_source)
    if not long_target.exists() or digest(long_target) != source_hash:
        try:
            long_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(long_source, long_target)
        except OSError as error:
            raise RuntimeError(f'Copy failed: {source} -> {target}: {error}') from error
    target_hash = digest(long_target)
    after = source.stat()
    if source_hash != target_hash or (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f'Input changed or copy differs: {source}')
    return {'source': str(source), 'target': str(target.relative_to(RUN)), 'role': role,
            'bytes': after.st_size, 'source_mtime_ns': after.st_mtime_ns, 'sha256': source_hash}

def main():
    contract = json.loads((ROOT / 'CONTRATO_ATIVO_GATE_V350.json').read_text(encoding='utf-8'))
    assert digest(ROOT / 'um.py') == contract['working_sha256']
    assert contract['principal_gate_missing_proof_inputs'] == []
    RUN.mkdir(exist_ok=len(sys.argv) > 1)
    write_json(RUN / 'preparation_status.json', {'status': 'COPYING', 'run': str(RUN)})
    items = [(ROOT / 'um.py', RUN / 'um.py', 'working_program')]
    items += enumerate_files(SOURCE / 'cache', RUN / 'cache', 'data_cache')
    items += enumerate_files(SOURCE / 'tgl_kernel/.lake/packages', RUN / 'tgl_kernel/.lake/packages', 'dependency_copy')
    items += enumerate_files(SOURCE / 'Nós/tgl_kernel/.lake/build', RUN / 'tgl_kernel/.lake/build', 'build_cache_seed')
    for name in ['12_nivel2_frozen.json', '13_nivel2_resultado.json']:
        items.append((SOURCE / 'Nós/nivel2_mcmc' / name, RUN / 'nivel2_mcmc' / name, 'mcmc_result_input'))
    records = []
    last = time.monotonic()
    print(json.dumps({'run': str(RUN), 'copy_files': len(items)}, ensure_ascii=False), flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(copy_checked, item) for item in items]
        for future in as_completed(futures):
            records.append(future.result())
            if time.monotonic() - last > 15:
                print(f'Copied and hash-verified {len(records)}/{len(items)} files', flush=True)
                last = time.monotonic()
    # Materialize exactly the embedded corpus, including current Audit. No DEV files.
    tree = ast.parse((RUN / 'um.py').read_text(encoding='utf-8-sig'))
    assignments = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)]
    embedded = ast.literal_eval(assignments[0].value)
    for name, content in embedded.items():
        target = (RUN / 'tgl_kernel' / name).resolve()
        assert target.is_relative_to(RUN / 'tgl_kernel')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    original = SOURCE / 'Nós/um.py'
    assert digest(original) == digest(ROOT / 'fontes/um_v350_original.py')
    manifest = {'status': 'PREPARED_NOT_EXECUTED', 'run': str(RUN),
                'working_sha256': digest(RUN / 'um.py'), 'canonical_sha256': digest(original),
                'embedded_files': len(embedded), 'copied_files': len(records),
                'copied_bytes': sum(x['bytes'] for x in records), 'copied_entries': records,
                'build_cache_is_seed_not_new_validation': True, 'original_paths_written': [],
                'scope': 'Full execution of the existing program; no new theorem or gate condition.'}
    write_json(RUN / 'input_manifest.json', manifest)
    write_json(RUN / 'preparation_status.json', {k: v for k, v in manifest.items() if k != 'copied_entries'})
    print(json.dumps({k: v for k, v in manifest.items() if k != 'copied_entries'}, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
