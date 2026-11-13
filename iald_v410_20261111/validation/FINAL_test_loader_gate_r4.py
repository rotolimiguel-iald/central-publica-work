import importlib.util,json,tempfile,types,sys,unittest
from pathlib import Path
from unittest.mock import patch
SOURCE=Path(r'C:\IALD\Central de Patentes\work\iald_v410_20261111\transaction.py')
spec=importlib.util.spec_from_file_location('transaction_fixture',SOURCE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class LoaderRollback(unittest.TestCase):
 def run_fixture(self,ok):
  with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as td:
   base=Path(td);work=base/'work';root=base/'runtime';work.mkdir();root.mkdir();(work/'validation').mkdir()
   dest=root/'catalog.json';dest.write_bytes(b'old');src=work/'new.json';src.write_bytes(b'new')
   plan={'files':[{'source':str(src),'destination':str(dest),'sha256':m.digest(b'new'),'baseline':m.digest(b'old')}]}
   pp=work/'install_plan.json';pp.write_text(json.dumps(plan));pin=m.digest(pp.read_bytes())
   (work/'validation/final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':pin}));(work/'validation/review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':pin}))
   result=types.SimpleNamespace(returncode=0 if ok else 1,stdout='{"status":"PASS"}',stderr='synthetic loader failure')
   scope={'accounts_modified':False,'bench_restarted':False,'client_files_changed':False,'scope_measurement':{}}
   with patch.object(m,'WORK',work),patch.object(m,'ROOT',root),patch.object(m,'quiet'),patch.object(m,'check_science_destinations'),patch.object(m,'scope_snapshot',return_value={'plan_overlap':[]}),patch.object(m,'scope_compare',return_value=scope),patch.object(m.subprocess,'run',return_value=result) as call,patch.dict(sys.modules,{'maintenance':types.SimpleNamespace(assert_quiesced=lambda:None)}):
    if ok:m.apply_plan(pp)
    else:
     with self.assertRaisesRegex(RuntimeError,'rolling back'):m.apply_plan(pp)
    self.assertEqual(dest.read_bytes(),b'new' if ok else b'old');self.assertEqual(call.call_count,1)
    self.assertTrue(list(root.glob('catalog.json.bak_*')))
    self.assertEqual((work/'deployment.json').exists(),ok)
 def test_loader_failure_rolls_back(self):self.run_fixture(False)
 def test_loader_pass_installs(self):self.run_fixture(True)
if __name__=='__main__':unittest.main()
