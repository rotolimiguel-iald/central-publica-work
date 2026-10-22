"""Stage only app runtime sources; never edit scientific originals or accounts."""
from pathlib import Path
import hashlib, json, os, sys

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
STAGE = W / 'stage'
FILES = '''claude_profiles.py claude_memory_package.py claude_profile_pipeline.py
claude_request_guard.py claude_native_account.py claude_route_bridge.py
claude_context_snapshot.py claude_server_selection.py claude_account_policy.py
iald_web_server.py iald_task_bridge.py iald_task_sandbox.py iald_motor_claude.py
iald_auto_router.py iald_task_policy.py iald_jev_control.py'''.split()

def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), str(path)
    path.write_bytes(raw)
    assert path.read_bytes() == raw

def main():
    state = {}
    for name in FILES:
        raw = (R / name).read_bytes()
        save(W / 'original' / name, raw)
        save(STAGE / name, raw)
        state[name] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    save(W / 'baseline.json', json.dumps(state, indent=2).encode())
    sys.path[:0] = [str(R), 'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
    os.environ['TIKTOKEN_CACHE_DIR'] = str(R / '.iald_runtime/tokenizer_cache')
    from iald_release_binding import load_release
    from iald_kernel import KernelCatalog
    from iald_memoria_canonica import CanonicalMemory
    release = load_release(R / 'iald_nucleo_fixo.json')
    assert release.identity['release'] == 'v390'
    catalog = KernelCatalog(Path(release.config['active_cluster']['kernel_bundle']))
    prefix, metadata = CanonicalMemory(
        Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
        nucleus_manifest=release.path).prompt('', catalog, public=True)
    assert metadata['private_atlas_included'] is False
    for key in ('mother_instruction', 'operational_core'):
        source = release.config[key]
        raw = Path(source['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
        assert raw.decode('utf-8-sig') in prefix
    release.check_manifest()
    save(W / 'package/prefix.md', prefix.encode())
    save(W / 'public_memory_provenance.json', json.dumps({
        'deployment': release.identity, 'metadata': metadata,
        'manifest_sha256': hashlib.sha256(release.raw).hexdigest(),
        'prefix_sha256': hashlib.sha256(prefix.encode()).hexdigest(),
        'bytes': len(prefix.encode()), 'scope': 'PUBLIC_FIXED_SOURCES',
        'private_atlas_included': False, 'generation_requests': 0,
    }, ensure_ascii=False, indent=2).encode())
    print(json.dumps({'staged_files': len(state), 'prefix_bytes': len(prefix.encode()),
                      'deployment': release.identity, 'private_atlas_included': False}))

if __name__ == '__main__':
    main()
