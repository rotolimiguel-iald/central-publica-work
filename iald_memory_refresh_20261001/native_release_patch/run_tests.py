"""Run staged regressions offline; never import the web server or providers."""
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

STAGE = Path(__file__).resolve().parent
PRODUCTION = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(STAGE), str(PRODUCTION)]
temporary_root = STAGE / 'test_tmp'
temporary_root.mkdir(exist_ok=True)
tempfile.tempdir = str(temporary_root)

with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
    suite = unittest.defaultTestLoader.discover(str(STAGE / 'tests'), pattern='test_*.py')
    # The legacy test selects a cache relative to its original checkout. Reuse
    # the existing, read-only tokenizer data; a cache miss cannot access network.
    os.environ['TIKTOKEN_CACHE_DIR'] = str(PRODUCTION / '.iald_runtime/tokenizer_cache')
    result = unittest.TextTestRunner(verbosity=2).run(suite)

record = {'tests_run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skipped': len(result.skipped),
          'successful': result.wasSuccessful(), 'network_blocked': True,
          'real_server_imported': 'iald_web_server' in sys.modules,
          'production_edited': False}
target = STAGE / 'test_results.json'
if target.exists():
    target.with_name('test_results.previous.json').write_bytes(target.read_bytes())
raw = (json.dumps(record, indent=2) + '\n').encode('utf-8')
temporary = target.with_suffix('.json.tmp')
temporary.write_bytes(raw)
assert temporary.stat().st_size == len(raw)
os.replace(temporary, target)
raise SystemExit(0 if result.wasSuccessful() else 1)
