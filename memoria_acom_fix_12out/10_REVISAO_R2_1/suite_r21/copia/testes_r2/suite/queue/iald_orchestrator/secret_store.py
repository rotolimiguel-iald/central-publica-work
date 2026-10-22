"""User-bound Windows DPAPI storage. No credential ever leaves this module in status."""
import ctypes
from ctypes import wintypes
import os
from .profiles import BASE
from .safe_files import replace_bytes

KEY_FILE = BASE/'state/secrets/mimo.dpapi'


class Blob(ctypes.Structure):
    _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_ubyte))]


def _crypt(data, *, decrypt=False):
    if os.name != 'nt':
        raise RuntimeError('Este cofre exige Windows DPAPI.')
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    result = Blob()
    library = ctypes.WinDLL('crypt32', use_last_error=True)
    function = library.CryptUnprotectData if decrypt else library.CryptProtectData
    function.restype = wintypes.BOOL
    function.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    # CRYPTPROTECT_UI_FORBIDDEN; default scope is current Windows user, not machine.
    if not function(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(result)):
        raise RuntimeError('Falha ao acessar o cofre Windows DPAPI.')
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    try:
        return ctypes.string_at(result.data, result.size)
    finally:
        ctypes.memset(result.data, 0, result.size)
        kernel.LocalFree(result.data)
        ctypes.memset(buffer, 0, len(buffer))


def store_mimo(value):
    if not isinstance(value, str) or not 20 <= len(value.strip()) <= 1024:
        raise ValueError('Formato de chave inválido.')
    value = value.strip()
    if not all(33 <= ord(char) <= 126 for char in value):
        raise ValueError('Formato de chave inválido.')
    replace_bytes(KEY_FILE, _crypt(value.encode('utf-8')))


def load_mimo():
    if not KEY_FILE.is_file():
        raise RuntimeError('Chave MiMo ainda não cadastrada no cofre local.')
    return _crypt(KEY_FILE.read_bytes(), decrypt=True).decode('utf-8')


def key_metadata():
    if not KEY_FILE.is_file():
        return {'stored': False}
    info = KEY_FILE.stat()
    return {'stored': True, 'mtime_ns': info.st_mtime_ns, 'size': info.st_size,
            'storage': 'WINDOWS_DPAPI_CURRENT_USER', 'expires_at': None,
            'expiry_status': 'NOT_REPORTED_BY_PROVIDER'}
