"""Independent reviewer script (sonnet-app-v405-revisor): group 1 -- RELEASE.json, ls-remote, blobs at the pinned commit and at the previous pin.
Adapted from the v404 reviewer's r1. No network here: the ls-remote stdout literal is passed as argv[1] (one call made before by the reviewer)."""
import json, hashlib, subprocess, sys, re
from pathlib import Path

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v405')
NOS = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
sh = lambda b: hashlib.sha256(b).hexdigest()


def git(*a):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + REPO.as_posix(), '-c', 'core.quotepath=false', '-C', str(REPO), *a])


out = []
ok = True


def chk(n, v, achado=None):
    global ok
    out.append({'n': len(out) + 1, 'name': n, 'ok': bool(v), 'achado': achado})
    ok &= bool(v)


ls = sys.argv[1].split()
rel = json.loads((W / 'app/RELEASE.json').read_bytes())
chk('RELEASE.json exact keys', set(rel) == {'release', 'espelho_commit', 'um_py_sha256'}, sorted(rel))
chk('release == v405', rel['release'] == 'v405')
chk('espelho_commit == ls-remote origin refs/heads/main (literal from the single network call)', ls[0] == rel['espelho_commit'] and ls[1] == 'refs/heads/main', ls)
chk('espelho_commit is 40 hex', bool(re.fullmatch(r'[0-9a-f]{40}', rel['espelho_commit'])))
seal_v = json.loads((V / 'um_absoluto_selo.json').read_bytes())
seal_n = json.loads((NOS / 'um_absoluto_selo.json').read_bytes())
chk('selo cofre um_version == v405', seal_v['um_version'] == 'v405')
chk('selo Nos um_version == v405', seal_n['um_version'] == 'v405', seal_n['um_version'])
chk('selo cofre sha256.um.py == RELEASE.um_py_sha256', seal_v['sha256']['um.py'] == rel['um_py_sha256'], seal_v['sha256']['um.py'])
chk('selo Nos sha256.um.py == RELEASE.um_py_sha256', seal_n['sha256']['um.py'] == rel['um_py_sha256'])
chk('selo cofre == selo Nos (bytes)', (V / 'um_absoluto_selo.json').read_bytes() == (NOS / 'um_absoluto_selo.json').read_bytes())
chk('bytes of cofre um.py hash == pin', sh((V / 'um.py').read_bytes()) == rel['um_py_sha256'])
chk('bytes of Nos um.py hash == pin', sh((NOS / 'um.py').read_bytes()) == rel['um_py_sha256'])
chk('selo fail_closed_selftest PASSED', seal_v.get('fail_closed_selftest') == 'FAIL_CLOSED_SELFTEST_PASSED', seal_v.get('fail_closed_selftest'))
C1 = rel['espelho_commit']
C0 = '1d3c4cbe'  # previous pin (v404 app release); resolved to the full object below
C0full = git('rev-parse', C0 + '^{commit}').decode().strip()
chk('previous pin (1d3c4cbe) is an ancestor of the pinned commit', subprocess.call(['git', '-C', str(REPO), '-c', 'safe.directory=' + REPO.as_posix(), 'merge-base', '--is-ancestor', C0full, C1]) == 0, C0full)
chk('pinned commit is local HEAD and origin/main', git('rev-parse', 'HEAD').decode().strip() == C1 == git('rev-parse', 'origin/main').decode().strip())
tr = git('ls-tree', '-r', '--name-only', '-z', C1).decode().split('\0')
ump = [p for p in tr if Path(p).name == 'um.py']
chk('exactly one um.py tracked at pinned commit', len(ump) == 1, ump)
b1 = git('show', C1 + ':' + ump[0])
chk('um.py blob at pinned commit sha256 == RELEASE pin == cofre selo == Nos selo', sh(b1) == rel['um_py_sha256'] == seal_v['sha256']['um.py'] == seal_n['sha256']['um.py'], sh(b1))
# every file prepare reads
bind = json.loads((W / 'app/PUBLIC_GIT_BINDING.json').read_bytes())
chk('PUBLIC_GIT_BINDING.commit == RELEASE.espelho_commit', bind['commit'] == C1)
chk('PUBLIC_GIT_BINDING.local_head_at_build == pinned', bind['local_head_at_build'] == C1)
diff = []
for relp, row in bind['sources'].items():
    x1 = git('show', C1 + ':' + relp)
    chk('binding sha == blob at pinned commit: ' + relp, sh(x1) == row['sha256'] and len(x1) == row['bytes'])
    chk('binding url is pinned raw url for ' + relp, row['url'].startswith('https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + C1 + '/'), row['url'][:110])
    try:
        x0 = git('show', C0full + ':' + relp)
        if x0 != x1:
            diff.append(relp)
    except subprocess.CalledProcessError:
        diff.append(relp + ' (absent at previous pin)')
chk('files prepare reads that differ between previous pin and pinned: listed', True, sorted(diff))
# selo, core, proof manifest and canonical form: bytes at pinned == vault
for nm, loc in [('um_absoluto_selo.json', 'um_absoluto_selo.json'), ('um_absoluto.json', 'um_absoluto.json'), ('um_absoluto_forma_canonica.md', 'um_absoluto_forma_canonica.md'), ('Lean/tgl_kernel_proof_manifest.json', 'tgl_kernel_proof_manifest.json'), ('um_absoluto_pt.txt', 'um_absoluto_pt.txt')]:
    rp = [p for p in tr if p.endswith(nm) and 'Grande Atrator' in p and 'fontes_pinadas' not in p]
    chk('exactly one ' + nm + ' under Grande Atrator', len(rp) == 1, rp)
    if len(rp) == 1:
        blob = git('show', C1 + ':' + rp[0])
        chk(nm + ' at pinned commit == cofre bytes', blob == (V / loc).read_bytes())
        if nm in seal_v['sha256'] or loc in seal_v['sha256']:
            chk(nm + ' sha == selo.sha256[...]', sh(blob) == seal_v['sha256'][loc.split('/')[-1]])
print(json.dumps({'ok': ok, 'n': len(out), 'passed': sum(o['ok'] for o in out), 'checks': out}, ensure_ascii=False, indent=1))
