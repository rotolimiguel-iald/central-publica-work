import importlib.util
import json
from pathlib import Path
import sys
import unittest
APP=Path(r'C:\IALD\projetos_pyhton\IALD');WORK=Path(__file__).resolve().parent
sys.path[:0]=[str(WORK),str(APP)]
import iald_cluster,iald_core_indexado,iald_memoria_canonica,iald_estado_publicado
suite=unittest.TestSuite()
for i,path in enumerate([WORK/'test_cluster.py', APP/'tests/test_kernel_catalog.py',APP/'tests/test_published_evidence.py',
                        WORK.parent/'iald_core_indexed_20260915/test_indexed_core.py']):
    spec=importlib.util.spec_from_file_location('test_cluster_suite_'+str(i),path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
result=unittest.TextTestRunner(verbosity=1).run(suite)
(WORK/'test_results.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful()}))
sys.exit(not result.wasSuccessful())
