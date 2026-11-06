"""Verify the actual restart and replay public, synthetic fixtures on installed bytes."""
import hashlib
import http.client
import json
from pathlib import Path
import re
import runpy
import sys
import time

from transaction import ROOT, WORK

def main():
    restart = json.loads((WORK/'restart.json').read_bytes())
    identity = json.loads((WORK/'INSTALLED_VERIFICATION.json').read_bytes())['identity']
    import maintenance
    listeners = maintenance._listeners()
    assert len(listeners)==1 and listeners[0].pid == restart['new_web_pid']
    import psutil
    child = psutil.Process(listeners[0].pid)
    assert child.ppid()==restart['supervisor_pid'] and maintenance._has_script(child,ROOT/'iald_web_server.py')
    needle = re.compile(rb'release=(v\d+) source_sha256=([a-f0-9]{16,64}) lean_files=(\d+)')
    found = []
    for f in sorted((ROOT/'logs').glob('web-server_*.log'),key=lambda f:f.stat().st_mtime,reverse=True)[:3]:
        if f.stat().st_mtime < child.create_time()-2:
            continue
        with f.open('rb') as log:
            for line in log:
                for match in needle.finditer(line):
                    rel,pin,n = (v.decode('ascii') for v in match.groups())
                    if rel==identity['release'] and identity['source_sha256'].startswith(pin):
                        found.append(dict(log=f.name,release=rel,source_pin=pin,lean_files=int(n)))
    assert found,'Startup release not observed in the new process log yet'
    connection = http.client.HTTPConnection('127.0.0.1',8082,timeout=5)
    try:
        connection.request('GET','/login')
        response=connection.getresponse()
        assert response.status==200 and response.read(8192)
    finally:
        connection.close()
    evidence=json.loads((WORK/'integration_review/STAGED_TESTS_R2.json').read_bytes())
    fixture=Path(evidence['stream_fixture']['path'])
    assert hashlib.sha256(fixture.read_bytes()).hexdigest()==evidence['stream_fixture']['sha256']
    counts=runpy.run_path(str(fixture))['run'](ROOT/'iald_app_memory.py')
    assert counts==evidence['observer_cases']
    result=dict(status='PASS',pid=child.pid,supervisor=child.ppid(),startup=found,
                login_http=response.status,stream_cases_on_installed_source=sum(counts.values()),
                paid_generation_requests=0,scope='Local web entrypoint and installed synthetic stream fixture.')
    with (WORK/'LIVE_BACKEND.json').open('x',encoding='utf8') as file:
        json.dump(result,file,indent=2)
    print(json.dumps(result))

if __name__=='__main__':
    main()
