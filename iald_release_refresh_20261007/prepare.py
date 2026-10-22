"""Prepare a pinned scientific refresh without changing production or running um.py."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse, quote
from concurrent.futures import ThreadPoolExecutor
import ast
import hashlib
import json
import shutil
import subprocess
import urllib.request

W = Path(__file__).resolve().parent
OLD = W.parent / 'iald_release_refresh_20261006'
R = Path(r'C:\IALD\projetos_pyhton\IALD')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
VAULT = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v390')
VERSION = 'v390'


def sha(raw): return hashlib.sha256(raw).hexdigest()
def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == raw: return
        backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(path.read_bytes())
        if backup.read_bytes() != path.read_bytes(): raise ValueError('Backup mismatch')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream: stream.write(raw)
    if temp.read_bytes() != raw or not raw: raise ValueError('Temporary mismatch')
    temp.replace(path)


def write(path, value): save(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode())
def git(*args):
    return subprocess.check_output(['git', '-c', 'safe.directory='+REPO.as_posix(), '-C', str(REPO), *args])


def capture():
    head = git('rev-parse', 'HEAD').decode().strip()
    remote = subprocess.check_output(['git', 'ls-remote', 'https://github.com/rotolimiguel-iald/the_boundary.git', 'refs/heads/main']).decode().split()[0]
    if remote != head: raise ValueError('Public head differs; select a verified immutable revision')
    tracked = set(git('ls-tree', '-r', '--name-only', '-z', head).decode().split('\0'))
    manifest = json.loads((R/'iald_nucleo_fixo.json').read_bytes())
    paths = {}
    for key in ('program','seal','result','proof_manifest'):
        rel = unquote('/'.join(urlparse(manifest['published_evidence'][key]['url']).path.split('/')[4:]))
        if rel not in tracked: raise ValueError('Published source absent')
        paths[key] = rel
    seal = json.loads(git('show', head+':'+paths['seal']))
    if seal['um_version'] != VERSION or seal['fail_closed_selftest'] != 'FAIL_CLOSED_SELFTEST_PASSED':
        raise ValueError('Unexpected scientific release')
    custody_bytes = (VAULT/'CUSTODY_MANIFEST.json').read_bytes()
    custody = json.loads(custody_bytes)
    if custody['version'] != VERSION or custody['mismatches'] != 0: raise ValueError('Custody invalid')
    verified, mismatches = [], []
    for row in custody['artifacts']:
        path = (VAULT/row['file']).resolve()
        if not path.is_relative_to(VAULT.resolve()) or path.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):
            raise ValueError('Unexpected custody path')
        raw = path.read_bytes()
        if sha(raw) != row['sha256']: mismatches.append(row['file'])
        verified.append({'file':row['file'],'sha256':sha(raw),'bytes':len(raw)})
    if mismatches: raise ValueError('Custody byte mismatches')
    files = {}
    for key, rel in paths.items():
        raw = git('show', head+':'+rel)
        name = Path(rel).name
        if raw != (VAULT/name).read_bytes(): raise ValueError('Public/custody divergence: '+name)
        if key != 'seal' and sha(raw) != seal['sha256'][name]: raise ValueError('Seal pin differs')
        files[name] = {'sha256':sha(raw),'bytes':len(raw),'git_path':rel}
    write(W/'v390_verified_handoff.json', {'status':'VERIFIED_LOCAL_V390_HANDOFF','version':VERSION,
          'checked_at_utc':datetime.now(timezone.utc).isoformat(),'source_executed_or_imported':False,
          'mirror':{'root':str(REPO),'head':head,'remote_main':remote},'vault_root':str(VAULT),
          'custody_manifest':{'path':str(VAULT/'CUSTODY_MANIFEST.json'),'sha256':sha(custody_bytes)},
          'custody_artifacts_verified':len(verified),'custody_mismatches':[], 'custody_artifacts':verified,
          'files':files,'seal':{k:seal[k] for k in ('timestamp','result_hash','formal_source_hash') if k in seal}})
    def download(item):
        name, record = item
        url = 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+head+'/'+quote(record['git_path'],safe='/')
        with urllib.request.urlopen(url, timeout=60) as response:
            digest = hashlib.sha256(); size = 0
            while chunk := response.read(1024*1024): digest.update(chunk); size += len(chunk)
            if response.status != 200: raise ValueError('Public source HTTP failure')
        match = digest.hexdigest() == record['sha256'] and size == record['bytes']
        if not match: raise ValueError('Public raw source differs')
        return {'name':name,'url':url,'status':200,'bytes':size,'expected_sha256':record['sha256'],
                'actual_sha256':digest.hexdigest(),'matches_vault':match}
    with ThreadPoolExecutor(max_workers=4) as pool: results = list(pool.map(download, files.items()))
    write(W/'public_v390_verification.json', {'status':'PASS','requested_commit':head,
          'all_four_hashes_match_vault':True,'artifacts':results})
    return head


def scaffold():
    code_names = ['iald_web_server.py','iald_auto_router.py','iald_jev_control.py','iald_task_bridge.py',
                  'iald_app_providers.py','iald_operator_bench.py','iald_research_routes.py',
                  'iald_bench_catalog.py','iald_public_fetch.py','iald_release_binding.py',
                  'iald_memoria_canonica.py','iald_kernel.py','claude_memory_package.py','claude_profiles.py',
                  'claude_profiles.json','iald_nucleo_fixo.json','IALD_Kernel_v5.txt']
    records = []
    for name in code_names:
        path=R/name
        if not path.is_file():
            if name == 'claude_profiles.json': continue
            raise ValueError('Missing live source '+name)
        raw=path.read_bytes(); save(W/'baseline'/name,raw)
        records.append({'name':name,'sha256':sha(raw),'bytes':len(raw)})
    write(W/'baseline.json',{'files':records,'client_files_changed':False})


if __name__ == '__main__':
    commit = capture()
    scaffold()
    print(json.dumps({'release':VERSION,'commit':commit,'status':'PUBLIC_AND_CUSTODY_VERIFIED_SCAFFOLDED'}))
