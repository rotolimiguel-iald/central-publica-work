"""Prepare explicit, pinned staged files. Never install, build or run Git."""
from pathlib import Path
import argparse, ast, hashlib, json, re, sys

W = Path(__file__).resolve().parent
PARENT = W.parent
ROOT = Path('C:/IALD/projetos_pyhton/IALD')
MOBILE = ROOT / 'iald-app'
SURFACES = (ROOT/'app', MOBILE/'www', MOBILE/'ios/App/App/public', MOBILE/'android/app/src/main/assets/public')
NATIVES = ('ios/App/App.xcodeproj/project.pbxproj', 'android/app/build.gradle')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_bytes())

def save(p, value):
    from transaction import atomic
    p = Path(p)
    if p.exists():
        raise ValueError('Existing output: preserve it and reconcile explicitly')
    raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, indent=2).encode()
    atomic(p, raw)

def safe(path):
    p = Path(path).resolve()
    if any(x.startswith('.') or x.lower() in {'iald_stack_v7.py','iald_psion_state.json','keystore.properties','local.properties'} for x in p.parts):
        raise ValueError('Private or hidden path refused')
    if p.suffix.lower() in {'.key','.pem','.p8','.p12','.jks','.keystore'}:
        raise ValueError('Credential path refused')
    return p

def row(source, destination, expected, baseline):
    source, destination = safe(source), safe(destination)
    if not source.is_relative_to(PARENT) or not destination.is_relative_to(ROOT):
        raise ValueError('Source/destination outside task scope')
    if not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('Explicit staged hash required')
    if sha(source) != expected or (sha(destination) if destination.exists() else None) != baseline:
        raise ValueError('Stage or baseline changed')
    raw = source.read_bytes()
    if destination.suffix == '.py':
        ast.parse(raw)
    # Freeze selected bytes within release, not a mutable agent directory.
    frozen = W/'stage'/destination.relative_to(ROOT)
    save(frozen, raw)
    return dict(source=str(frozen), destination=str(destination), sha256=expected, baseline=baseline)

def assemble(manifest_path):
    spec = load(manifest_path)
    if (W/'install_plan.json').exists():
        raise ValueError('Plan already exists')
    science = load(W/'SCIENCE_BASELINE.json')
    protected = {Path(f['path']).resolve() for f in science['files']}
    for f in science['files']:
        if sha(f['path']) != f['sha256']:
            raise ValueError('Science baseline changed')
    pending, assets = [], []
    for asset in spec['assets']:
        name = asset['name']
        if Path(name).name != name or name in assets:
            raise ValueError('Asset must be a unique flat filename')
        assets.append(name)
        for surface in SURFACES:
            target = surface/name
            baseline = asset['baselines'][str(target)]
            pending.append((asset['source'], target, asset['sha256'], baseline))
    if not assets:
        raise ValueError('Explicit nonempty asset list required')
    for f in spec.get('runtime', []):
        target = safe(f['destination'])
        if target.parent != ROOT or target.suffix != '.py':
            raise ValueError('Runtime scope is top-level Python only')
        pending.append((f['source'], target, f['sha256'], f['baseline']))
    targets = [safe(x[1]) for x in pending]
    if len(targets) != len(set(targets)) or protected.intersection(targets):
        raise ValueError('Conflicting staged diffs or scientific destination')
    rows = [row(*x) for x in pending]
    native = []
    for rel, old, new, count in [(NATIVES[0], b'CURRENT_PROJECT_VERSION = 37;', b'CURRENT_PROJECT_VERSION = 38;', 2),
                                 (NATIVES[1], b'versionCode 32', b'versionCode 33', 1)]:
        target = MOBILE/rel
        raw = target.read_bytes()
        if raw.count(old) != count:
            raise ValueError('Native baseline version changed')
        source = W/'native'/target.name
        save(source, raw.replace(old,new))
        native.append(row(source,target,sha(source),hashlib.sha256(raw).hexdigest()))
    rows.extend(native)
    save(W/'NATIVE_PLAN.json', dict(ios='4.1(38)', android='4.1(33)', files=native))
    tracked = [f for f in rows if Path(f['destination']).is_relative_to(MOBILE/'www')
               or Path(f['destination']).is_relative_to(MOBILE/'ios')
               or Path(f['destination']) == MOBILE/NATIVES[1]]
    save(W/'PRIVATE_GIT_PLAN.json', dict(status='CANDIDATE_NOT_EXECUTED',
         repository='https://github.com/rotolimiguel-iald/iald-app.git',
         branch='codex/mobile-release', ios='4.1(38)', android='4.1(33)',
         files=[dict(path=str(Path(f['destination']).relative_to(MOBILE)).replace('\\','/'),
                     sha256=f['sha256']) for f in tracked],
         instructions='Parent must verify current branch, clean index, HEAD baseline and exact diff before any Git write. Explicit mobile_release.py commit/push phases only after final review. Push may start Xcode Cloud.'))
    save(W/'install_plan.json', dict(status='PREPARED_NOT_INSTALLED', files=rows, assets=assets,
         science_baseline=str(W/'SCIENCE_BASELINE.json'), science_sha256=sha(W/'SCIENCE_BASELINE.json'),
         input_manifest_sha256=sha(manifest_path), accounts_modified=False, wallet_modified=False))
    save(W/'INPUT_MANIFEST.json', spec)
    print(json.dumps(dict(status='PREPARED_NOT_REVIEWED', files=len(rows), assets=assets)))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    assemble(parser.parse_args().manifest)
