"""Web startup hook; path constants must be pinned in reviewed deployment.

No imports or commands obtained from HTTP/user/corpus content.
"""
import json
import os
from pathlib import Path
import subprocess


def ensure_worker(python, runner, config, log):
    # The child acquires the global mutex; duplicate startup children exit without
    # opening state or launching any preparation/deployment subprocess.
    paths = [Path(value).resolve(strict=True) for value in (python, runner, config)]
    if os.name != 'nt':
        raise RuntimeError('Windows deployment required')
    target = Path(log)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('ab') as output:
        proc = subprocess.Popen([str(paths[0]), '-B', '-X', 'utf8', str(paths[1]),
                                 '--config', str(paths[2])], stdin=subprocess.DEVNULL,
                                stdout=output, stderr=subprocess.STDOUT,
                                creationflags=subprocess.CREATE_NO_WINDOW,
                                close_fds=True)
    return {'spawned_pid': proc.pid, 'verified_running': False}


def admin_status(path):
    """Call ONLY after existing is_admin check. Deliberately no paths or content."""
    try:
        p = Path(path)
        if p.stat().st_size > 65536:
            raise ValueError('Status exceeds contract')
        state = json.loads(p.read_bytes())
        observation=p.with_name('observation.json')
        if observation.exists() and observation.stat().st_size>65536:
            raise ValueError('Observation exceeds contract')
        if observation.exists() and json.loads(observation.read_bytes()).get('readable') is False:
            return {'phase':'BLOCKED','reason':'Latest updater observation failed',
                    'previous_phase':state.get('phase'),'uncertain':state.get('uncertain',False)}
        return {k: state.get(k) for k in ('phase', 'candidate_key', 'package_sha256',
                                         'reason', 'uncertain') if k in state}
    except FileNotFoundError:
        return {'phase': 'BLOCKED', 'reason': 'Worker status not available'}
    except Exception:
        return {'phase': 'BLOCKED', 'reason': 'Worker status unreadable'}


def acquire_mutex():
    """Caller retains handle until process exit; never writes state on contention."""
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    handle = kernel.CreateMutexW(None, True, 'Global\\IALD_AppScienceUpdater_8082')
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    if ctypes.get_last_error() == 183:
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle(handle)
        return None
    return handle
