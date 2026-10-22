"""User-bound DPAPI storage for the TypeSafe API key."""

from .profiles import BASE
from .safe_files import replace_bytes
from .secret_store import _crypt

KEY_FILE = BASE / 'state/secrets/jev.dpapi'


def store_key(value):
    if (not isinstance(value, str) or not 20 <= len(value.strip()) <= 1024
            or not all(33 <= ord(char) <= 126 for char in value.strip())):
        raise ValueError('Formato de chave inválido.')
    replace_bytes(KEY_FILE, _crypt(value.strip().encode('utf-8')))


def load_key():
    if not KEY_FILE.is_file():
        raise RuntimeError('Chave Jev ainda não cadastrada no cofre local.')
    return _crypt(KEY_FILE.read_bytes(), decrypt=True).decode('utf-8')


def key_metadata():
    if not KEY_FILE.is_file():
        return {'stored': False}
    info = KEY_FILE.stat()
    return {'stored': True, 'mtime_ns': info.st_mtime_ns, 'size': info.st_size,
            'storage': 'WINDOWS_DPAPI_CURRENT_USER', 'expires_at': None,
            'expiry_status': 'NOT_REPORTED_BY_PROVIDER'}
