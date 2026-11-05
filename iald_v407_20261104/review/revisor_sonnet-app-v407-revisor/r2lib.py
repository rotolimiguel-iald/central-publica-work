"""Revisor sonnet-app-v407-revisor -- rodada 2 (INSTALACAO): biblioteca comum. Somente leitura.
Gancho de auditoria que CONTA e BLOQUEIA: socket.connect/getaddrinfo fora do unico GET permitido (127.0.0.1:8082), subprocess, os.system, abertura de .env*/segredos,
escrita fora da pasta do revisor. Os contadores vao para o JSON de cada script (D9, parte do meu proprio rastro)."""
import hashlib, json, os, sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
REL = R / 'canonical_releases' / 'v407_bf9017157406'
BS = chr(92)

EVENTS = {'socket_connect_allowed': [], 'socket_connect_blocked': [], 'getaddrinfo_allowed': [], 'getaddrinfo_blocked': [], 'subprocess_blocked': 0, 'os_system_blocked': 0, 'env_open_blocked': 0, 'secret_open_blocked': 0, 'write_outside_blocked': 0, 'opens_read': 0}
ALLOWED_HOSTPORT = ('127.0.0.1', 8082)


def _guard(event, args):
    if event == 'socket.connect':
        addr = args[1]
        if isinstance(addr, tuple) and tuple(addr[:2]) == ALLOWED_HOSTPORT:
            EVENTS['socket_connect_allowed'].append(list(addr[:2]))
            return
        EVENTS['socket_connect_blocked'].append(repr(addr)[:80])
        raise RuntimeError('blocked socket.connect ' + repr(addr)[:80])
    if event == 'socket.getaddrinfo':
        host, port = args[0], args[1]
        if host in ('127.0.0.1', 'localhost') and int(port or 0) == 8082:
            EVENTS['getaddrinfo_allowed'].append([host, port])
            return
        EVENTS['getaddrinfo_blocked'].append(repr((host, port))[:80])
        raise RuntimeError('blocked getaddrinfo ' + repr((host, port))[:80])
    if event == 'subprocess.Popen':
        EVENTS['subprocess_blocked'] += 1
        raise RuntimeError('blocked subprocess')
    if event == 'os.system':
        EVENTS['os_system_blocked'] += 1
        raise RuntimeError('blocked os.system')
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        name = os.path.basename(os.fsdecode(path))
        if name.startswith('.env'):
            EVENTS['env_open_blocked'] += 1
            raise RuntimeError('.env forbidden')
        if name in ('iald_stack_v7.py', 'iald_psion_state.json', '.iald_secret_key'):
            EVENTS['secret_open_blocked'] += 1
            raise RuntimeError('private input forbidden')
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing:
            p = Path(os.fsdecode(path)).resolve()
            if not p.is_relative_to(HERE):
                EVENTS['write_outside_blocked'] += 1
                raise RuntimeError('write outside reviewer folder: ' + str(p))
        else:
            EVENTS['opens_read'] += 1


def install_guard():
    sys.addaudithook(_guard)


sha_bytes = lambda b: hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def norm(p):
    return os.path.normcase(os.path.normpath(str(p)))


rd = lambda p: json.loads(Path(p).read_bytes())
