"""Run only the two requested suites, with all network/process dispatch denied."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
tempfile.tempdir=str(HERE)

def write(name,raw):
    p=HERE/name; stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():p.with_name(p.name+'.bak_'+stamp).write_bytes(p.read_bytes())
    t=p.with_name(p.name+'.tmp_'+stamp);t.write_bytes(raw)
    assert t.read_bytes()==raw;os.replace(t,p)

if __name__=='__main__':
    log=io.StringIO()
    def blocked(*a,**k):raise AssertionError('Real network/process dispatch forbidden')
    with patch('socket.create_connection',blocked), patch('socket.getaddrinfo',blocked), \
         patch.object(socket.socket,'connect',blocked), patch.object(socket.socket,'connect_ex',blocked), \
         patch.object(subprocess,'Popen',blocked):
        suite=unittest.defaultTestLoader.loadTestsFromNames(['test_app_integration','test_actual_app_integration'])
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    text=log.getvalue();print(text)
    write('integration_output.txt',text.encode('utf-8'))
    pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')}
    report=dict(created_at=datetime.now(timezone.utc).isoformat(),tests_run=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
        success=result.wasSuccessful(),pins=pins,modules={name:str(getattr(module,'__file__','')) for name,module in sys.modules.items() if name.startswith('iald_')},
        failures_detail=[{'test':str(test),'traceback':trace} for test,trace in result.failures+result.errors],
        real_network=False,real_provider=False,real_bench_dispatch=False)
    write('integration_results.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    raise SystemExit(not result.wasSuccessful())
