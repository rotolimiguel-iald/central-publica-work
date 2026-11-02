"""Brief, exclusive deployment window for the existing web child/supervisor.

No process is stopped until its identity and an idle, frozen ledger are verified.
The supervisor remains alive and is resumed in finally; other services untouched.
"""
from pathlib import Path
from contextlib import contextmanager
import time
import psutil

ROOT=Path('C:/IALD/projetos_pyhton/IALD')
_active=None

def _has_script(process,path):
    expected=str(path.resolve()).casefold()
    return any(str(Path(arg).resolve()).casefold()==expected for arg in process.cmdline()[1:] if arg and not arg.startswith('-'))

def _web_processes():
    result=[]
    for proc in psutil.process_iter(['name']):
        if (proc.info.get('name') or '').casefold()!='python.exe':continue
        try:
            if _has_script(proc,ROOT/'iald_web_server.py'):result.append(proc)
        except psutil.NoSuchProcess:continue
    return result

def _listeners():
    return [c for c in psutil.net_connections(kind='tcp') if c.status==psutil.CONN_LISTEN and c.laddr.port==8082]

def assert_quiesced():
    """The actual runtime process state, not a caller boolean, gates writes."""
    if _active is None:raise RuntimeError('No controlled maintenance window')
    parent=_active['supervisor']
    if parent.create_time()!=_active['supervisor_created'] or parent.status()!=psutil.STATUS_STOPPED:
        raise RuntimeError('Supervisor is not the suspended deployment owner')
    if not _has_script(parent,ROOT/'start_iald_web.ps1') or _web_processes() or _listeners():
        raise RuntimeError('Web admissions are not stopped')

@contextmanager
def stopped_web(quiet):
    global _active
    if _active is not None:raise RuntimeError('Nested maintenance refused')
    web=_web_processes()
    if len(web)!=1:raise RuntimeError('Expected one web child')
    child=web[0];parent=child.parent()
    if parent is None or not _has_script(parent,ROOT/'start_iald_web.ps1'):
        raise RuntimeError('Unexpected supervisor')
    if any(a.casefold()=='-nosupervise' for a in parent.cmdline()):
        raise RuntimeError('Supervisor will not restart child')
    listeners=_listeners()
    if len(listeners)!=1 or listeners[0].pid!=child.pid:raise RuntimeError('Listener mismatch')
    identity={'old_web_pid':child.pid,'supervisor_pid':parent.pid,'supervisor_created':parent.create_time()}
    parent_suspended=child_suspended=terminated=False
    try:
        parent.suspend();parent_suspended=True
        child.suspend();child_suspended=True
        if parent.status()!=psutil.STATUS_STOPPED or child.status()!=psutil.STATUS_STOPPED:
            raise RuntimeError('Process suspension could not be verified')
        quiet()  # No web thread can admit work after this point.
        child.terminate();child.wait(timeout=5);terminated=True
        _active={'supervisor':parent,**identity}
        assert_quiesced()
        yield identity
    finally:
        _active=None
        try:
            if child_suspended and not terminated:
                try:child.resume()
                except psutil.NoSuchProcess:pass
        finally:
            if parent_suspended:parent.resume()

def await_restart(identity, timeout=90):
    import http.client
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        web=_web_processes()
        if len(web)==1 and web[0].pid!=identity['old_web_pid'] and web[0].ppid()==identity['supervisor_pid']:
            parent=web[0].parent()
            if parent.create_time()!=identity['supervisor_created']:raise RuntimeError('Supervisor identity changed')
            connection=http.client.HTTPConnection('127.0.0.1',8082,timeout=2)
            try:
                connection.request('GET','/login');response=connection.getresponse();response.read()
                if response.status==200:
                    listeners=_listeners()
                    if len(listeners)==1 and listeners[0].pid==web[0].pid:
                        return {**identity,'status':'PASS','new_web_pid':web[0].pid,'http_status':200,
                                'restart_scope':'Existing web child only; same supervisor resumed; bench/llama untouched'}
            except (OSError,http.client.HTTPException):pass
            finally:connection.close()
        time.sleep(1)
    raise RuntimeError('Web restart not verified within deadline')
