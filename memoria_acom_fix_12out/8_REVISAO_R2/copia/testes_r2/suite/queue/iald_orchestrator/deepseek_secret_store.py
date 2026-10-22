"""Dedicated user-bound DPAPI credential for the official DeepSeek API."""
from .profiles import BASE
from .safe_files import replace_bytes
from .secret_store import _crypt

KEY_FILE = BASE / 'state/secrets/deepseek.dpapi'


def store_key(value):
    if (not isinstance(value, str) or not value.startswith('sk-')
            or not 20 <= len(value) <= 1024
            or not all(33 <= ord(char) <= 126 for char in value)):
        raise ValueError('Formato de chave inválido.')
    replace_bytes(KEY_FILE, _crypt(value.encode('utf-8')))


def load_key():
    if not KEY_FILE.is_file():
        raise RuntimeError('Chave DeepSeek ainda não cadastrada no cofre local.')
    return _crypt(KEY_FILE.read_bytes(), decrypt=True).decode('utf-8')


def key_metadata():
    if not KEY_FILE.is_file():
        return {'stored': False}
    info = KEY_FILE.stat()
    return {'stored': True, 'mtime_ns': info.st_mtime_ns, 'size': info.st_size,
            'storage': 'WINDOWS_DPAPI_CURRENT_USER', 'expires_at': None,
            'expiry_status': 'NOT_REPORTED_BY_PROVIDER'}
