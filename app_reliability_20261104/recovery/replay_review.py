"""Author replay of independent probes. Not a new independent acceptance.

Parse only deltas() and Independent from the reviewer's source. Do not execute
its top-level snapshot/writes; all replay artifacts stay in recovery.
"""
import ast
import hashlib
import io
import json
from pathlib import Path
import unittest
import test_recovery as t
import iald_auto_recovery as recovery

ROOT=Path(__file__).resolve().parent
source=ROOT.parent/'review'/'run_review.py'
raw=source.read_bytes()
tree=ast.parse(raw.decode())
nodes=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))
       and node.name in {'deltas','Independent'}]
env={'t':t,'recovery':recovery,'unittest':unittest,'json':json,'observations':[]}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<independent probes replayed by author>','exec'),env)
log=io.StringIO()
result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(env['Independent']))
(ROOT/'REVIEW_PROBES_R2_LOG.txt').write_text(log.getvalue(),encoding='utf-8')
receipt={'status':'PASS' if result.wasSuccessful() else 'FAIL','role':'AUTHOR_REPLAY_NOT_INDEPENDENT_ACCEPTANCE',
    'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),
    'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
    'observations':env['observations'], 'network':'socket connect forbidden',
    'runtime_written':False,'review_written':False}
(ROOT/'REVIEW_PROBES_R2.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
if not result.wasSuccessful():print(log.getvalue())
raise SystemExit(not result.wasSuccessful())
