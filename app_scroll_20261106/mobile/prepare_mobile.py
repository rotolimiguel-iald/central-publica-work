"""Read-only inventory or explicitly released frontend staging; never install."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
W = HERE.parent
REPO = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
PREVIOUS = W.parent / 'iald_owner_notice_20261105/mobile'
NATIVE = ('ios/App/App.xcodeproj/project.pbxproj', 'android/app/build.gradle')
ASSETS = ('iald.js', 'owner_office.js')
SURFACES = ('www', 'ios/App/App/public', 'android/app/src/main/assets/public')

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return json.loads(Path(path).read_bytes())

def put(path, data):
    path = Path(path)
    require(path.resolve().is_relative_to(HERE), 'Output outside mobile')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.read_bytes() == data, 'Existing evidence differs; preserve and reconcile')
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temp = Path(stream.name)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        require(temp.read_bytes() == data and os.name == 'nt', 'Write verification failed')
        temp.rename(path)
    finally:
        temp.unlink(missing_ok=True)

def report(path, value):
    put(path, (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode())

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], stderr=subprocess.DEVNULL)

def inventory():
    head = git('rev-parse', 'HEAD').decode().strip()
    branch = git('branch', '--show-current').decode().strip()
    require(branch == 'codex/mobile-release', 'Unexpected branch')
    native = {n: (REPO/n).read_bytes() for n in NATIVE}
    require(all(data == git('show', head+':'+n) for n, data in native.items()), 'Native baseline differs from HEAD')
    ios = re.findall(rb'CURRENT_PROJECT_VERSION = (\d+);', native[NATIVE[0]])
    android = re.findall(rb'(?m)^\s*versionCode (\d+)\s*$', native[NATIVE[1]])
    iv = re.findall(rb'MARKETING_VERSION = ([\d.]+);', native[NATIVE[0]])
    av = re.findall(rb'versionName "([\d.]+)"', native[NATIVE[1]])
    require(len(ios)==2 and len(set(ios))==1 and len(android)==1, 'Ambiguous build numbers')
    require(len(iv)==2 and len(set(iv))==1 and av == iv[:1], 'Marketing version mismatch')
    pins = {s+'/'+a: sha((REPO/s/a).read_bytes()) for s in SURFACES for a in ASSETS}
    require(all(len({pins[s+'/'+a] for s in SURFACES})==1 for a in ASSETS), 'Mobile assets differ')
    require(all(sha(git('show', head+':'+s+'/'+a)) == pins[s+'/'+a]
                for s in SURFACES[:2] for a in ASSETS), 'Tracked assets differ from HEAD')
    previous_push = read(PREVIOUS/'release/PUSH.json')
    require(previous_push['commit'] == head, 'Previous release HEAD changed; reconcile')
    return dict(status='PREPARED_NOT_EXECUTED', checkout=str(REPO), branch=branch, base_commit=head,
                version=av[0].decode(), current_ios=int(ios[0]), current_android=int(android[0]),
                next_ios=int(ios[0])+1, next_android=int(android[0])+1,
                native_pins={n:sha(b) for n,b in native.items()}, asset_pins=pins)

def prepare(manifest_path):
    state = inventory()
    require(state == read(HERE/'BASELINE.json'), 'Baseline drift')
    manifest_path = Path(manifest_path).resolve(strict=True)
    require(manifest_path.is_relative_to(W/'stage'), 'Parent manifest must be in W/stage')
    ready = read(manifest_path)
    require(ready.get('status') == 'READY_FOR_MOBILE' and ready.get('parent') == 'codex-app-scroll-01a094df', 'Parent release missing')
    require(ready.get('base_commit') == state['base_commit'], 'Parent baseline mismatch')
    assets = ready['assets']
    require(assets and set(assets).issubset(ASSETS), 'Unexpected asset allowlist')
    rows = []
    for name, item in assets.items():
        source = Path(item['path']).resolve(strict=True)
        require(source.is_relative_to((W/'stage').resolve()), 'Candidate outside stage')
        raw = source.read_bytes()
        require(raw.strip() and sha(raw)==item['sha256'], 'Candidate hash mismatch')
        raw.decode('utf-8')
        for surface in SURFACES:
            target = surface+'/'+name
            staged = HERE/'prepared'/target
            put(staged, raw)
            rows.append(dict(source=str(staged), target=str(REPO/target), old=state['asset_pins'][target], new=sha(raw)))
    for n in NATIVE:
        raw = (REPO/n).read_bytes()
        if n.endswith('.pbxproj'):
            before = ('CURRENT_PROJECT_VERSION = %d;'%state['current_ios']).encode()
            after = ('CURRENT_PROJECT_VERSION = %d;'%state['next_ios']).encode()
            count = 2
        else:
            before = ('versionCode %d'%state['current_android']).encode()
            after = ('versionCode %d'%state['next_android']).encode()
            count = 1
        require(raw.count(before)==count, 'Version substitution mismatch')
        data = raw.replace(before, after)
        put(HERE/'prepared'/n, data)
        rows.append(dict(source=str(HERE/'prepared'/n), target=str(REPO/n), old=sha(raw), new=sha(data)))
    report(HERE/'PLAN.json', dict(status='REQUIRES_INDEPENDENT_REVIEW_AND_PARENT_INSTALL', baseline=state,
           parent_manifest=dict(path=str(manifest_path),sha256=sha(manifest_path.read_bytes())), rows=rows,
           tracked_files=[s+'/'+a for s in SURFACES[:2] for a in assets]+list(NATIVE)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent-ready')
    args = parser.parse_args()
    if args.parent_ready:
        prepare(args.parent_ready)
    else:
        report(HERE/'BASELINE.json', inventory())
