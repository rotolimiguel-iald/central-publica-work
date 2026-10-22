# Revisor B: adversarial path tests against the candidate guard (sandbox only, synthetic files).
import os, sys, json, ctypes, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
COPIA = os.path.join(os.path.dirname(HERE), 'copia', 'MEMORIA_IALD')
sys.path.insert(0, os.path.join(COPIA, 'lib')); sys.path.insert(0, COPIA)
from iald_memory import guard
import session_memory as sm
BS = chr(92)
SB = os.path.join(HERE, 'sb_paths')
if os.path.exists(SB):
    subprocess.run(['cmd', '/c', 'rmdir', '/s', '/q', SB])
os.makedirs(SB)
CANARY = b'FAKE_SYNTHETIC_CANARY_NOT_A_SECRET\n'
def mk(name, data=CANARY):
    p = os.path.join(SB, name)
    with open(p, 'wb') as f: f.write(data)
    return p
files = {}
for n in ['IALD_PSION_STATE_32B.JSON', 'iald_psion_state_32B.json.bak_20261010_092000', 'iald_psion_state_32B.json.BAK_X',
          '.env', '.ENV.local', 'server.KEY', 'cert.pem.bak_1', 'ｉａｌｄ_psion_state.json',
          'iald_psion_ѕtate.json', 'iald‐psion‐state.json', 'iald_stack_v7.py', 'iald_stack_v7.py.bak_2',
          'secret.pem', 'copia_iald_psion_state_32B.json', 'iald_psion_state_32B.json~', 'iald_psion_state_32B (2).json',
          '.env~', 'server.key~', 'env.bak_iald']:
    files[n] = mk(n)
os.makedirs(os.path.join(SB, 'Escritorio')); mk(os.path.join('Escritorio', 'peca.txt'))
os.makedirs(os.path.join(SB, 'outra')); mk(os.path.join('outra', 'nada.txt'))
os.link(files['.env'], os.path.join(SB, 'innocent_hl.txt'))
sl_ok = True
try:
    os.symlink(files['.env'], os.path.join(SB, 'innocent_sl.txt'))
except OSError as e:
    sl_ok = repr(e)
subprocess.run(['cmd', '/c', 'mklink', '/J', os.path.join(SB, 'jx'), os.path.join(SB, 'Escritorio')], capture_output=True)
subprocess.run(['cmd', '/c', 'mklink', '/J', os.path.join(SB, 'jy'), os.path.join(SB, 'outra')], capture_output=True)
def short(p):
    buf = ctypes.create_unicode_buffer(1024)
    n = ctypes.windll.kernel32.GetShortPathNameW(p, buf, 1024)
    return buf.value if n else None
cases = {}
def add(label, p): cases[label] = p
for n, p in files.items(): add('name:' + n, p)
add('hardlink innocent_hl.txt -> .env', os.path.join(SB, 'innocent_hl.txt'))
add('symlink innocent_sl.txt -> .env', os.path.join(SB, 'innocent_sl.txt'))
add('junction jx/peca.txt -> Escritorio', os.path.join(SB, 'jx', 'peca.txt'))
add('junction jx dir', os.path.join(SB, 'jx'))
add('short name of .env', short(files['.env']))
add('short name of IALD_PSION_STATE_32B.JSON', short(files['IALD_PSION_STATE_32B.JSON']))
add('short name of server.KEY', short(files['server.KEY']))
sd = short(os.path.join(SB, 'Escritorio'))
add('short name dir Escritorio/peca.txt', (sd + BS + 'peca.txt') if sd else None)
add('trailing space .env_', files['.env'] + ' ')
add('trailing dot .env.', files['.env'] + '.')
add('trailing dots+spaces server.KEY. .', files['server.KEY'] + '. .')
add('ADS .env::$DATA', files['.env'] + '::$DATA')
add('ADS server.KEY::$DATA', files['server.KEY'] + '::$DATA')
add('ADS secret.pem::$DATA', files['secret.pem'] + '::$DATA')
add('prefix //?/ .env', BS + BS + '?' + BS + files['.env'])
add('prefix //?/ hardlink', BS + BS + '?' + BS + os.path.join(SB, 'innocent_hl.txt'))
drive, rest = os.path.splitdrive(files['.env'])
add('UNC localhost C$ .env', BS + BS + 'localhost' + BS + drive[0] + '$' + rest)
add('UNC localhost C$ .env::$DATA', BS + BS + 'localhost' + BS + drive[0] + '$' + rest + '::$DATA')
add('//?/UNC/localhost .env::$DATA', BS + BS + '?' + BS + 'UNC' + BS + 'localhost' + BS + drive[0] + '$' + rest + '::$DATA')
add('//./ device .env::$DATA', BS + BS + '.' + BS + files['.env'] + '::$DATA')
add('dotdot jy/../.env', os.path.join(SB, 'jy', '..', '.env'))
add('forward slashes upper .env', files['.env'].replace(BS, '/').upper())
add('escritorio NFD component', os.path.join(SB, 'Escritório_x', 'a.txt'))
add('escritorio cyrillic i (nonexistent)', os.path.join(SB, 'Escrіtorio', 'a.txt'))
out = {'symlink_created': sl_ok, 'cases': []}
for label, p in cases.items():
    if p is None:
        out['cases'].append({'case': label, 'path_reason': 'SHORT_NAME_UNAVAILABLE'}); continue
    try:
        r_sb = guard.path_reason(p, roots=[SB])
    except Exception as e:
        r_sb = 'EXC:' + type(e).__name__
    try:
        r_prod = guard.path_reason(p)  # default identity roots (stat only, never read)
    except Exception as e:
        r_prod = 'EXC:' + type(e).__name__
    try:
        _, data = sm.read_allowed_file(p)
        read = 'READ_OK canary=%s bytes=%d' % (data == CANARY, len(data))
    except Exception as e:
        read = 'refused:%s:%s' % (type(e).__name__, str(e)[:70])
    out['cases'].append({'case': label, 'path': p, 'reason_roots_sandbox': r_sb, 'reason_default_roots': r_prod,
                         'read_allowed_file_default_roots': read})
with open(os.path.join(HERE, 't1_paths_result.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for c in out['cases']:
    print(c['case'], '|', c.get('reason_roots_sandbox'), '|', c.get('reason_default_roots'), '|', c.get('read_allowed_file_default_roots', c.get('path_reason')))
print('symlink', sl_ok)
