import importlib.util,json,hashlib,tempfile,unittest
from pathlib import Path
A=Path(r'C:\IALD\Central de Patentes\work\iald_v410_20261111')
spec=importlib.util.spec_from_file_location('guard_r4',A/'preservation_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def h(b):return hashlib.sha256(b).hexdigest()
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.root=Path(__file__).resolve().parent / ("guard_fixture_"+__import__("uuid").uuid4().hex);self.root.mkdir();g.ROOT=self.root/'runtime';g.WORK=self.root/'work';g.ROOT.mkdir();g.WORK.mkdir();(g.WORK/'validation').mkdir()
  self.p=g.ROOT/'server.py';self.p.write_bytes(b'old');self.source=g.WORK/'new.py';self.source.write_bytes(b'new')
  self.other=g.ROOT/'private.py';self.other.write_bytes(b'unchanged')
  (g.WORK/'PRESERVATION_BASELINE.json').write_text(json.dumps({'files':[{'path':str(p),'sha256':h(p.read_bytes())} for p in (self.p,self.other)]}))
  self.rows=[dict(source=str(self.source),destination=str(self.p),sha256=h(b'new'),baseline=h(b'old'))];self.pin()
 def pin(self):
  raw=json.dumps({'files':self.rows}).encode();(g.WORK/'RUNTIME_DELTA_R4.json').write_bytes(raw);(g.WORK/'validation/review_final.json').write_text(json.dumps({'status':'PASS','runtime_delta_sha256':h(raw)}))
 def test_before_after(self):
  self.assertTrue(all(g.verify().values()));self.p.write_bytes(b'new');self.assertTrue(all(g.verify(installed=True).values()))
  with self.assertRaises(RuntimeError):g.verify()
 def test_protected_change(self):
  self.other.write_bytes(b'changed')
  with self.assertRaises(RuntimeError):g.verify()
 def test_stage_tamper(self):
  self.source.write_bytes(b'tampered')
  with self.assertRaises(RuntimeError):g.verify()
 def test_unreviewed_delta(self):
  (g.WORK/'RUNTIME_DELTA_R4.json').write_bytes(b'{}')
  with self.assertRaises(RuntimeError):g.verify()
 def test_wrong_baseline(self):
  self.rows[0]['baseline']=h(b'other');self.pin()
  with self.assertRaises(RuntimeError):g.verify()
 def test_new_module(self):
  new=g.ROOT/'snapshot.py';self.rows.append(dict(source=str(self.source),destination=str(new),sha256=h(b'new'),baseline=None));self.pin();g.verify();new.write_bytes(b'new');self.p.write_bytes(b'new');g.verify(installed=True)
 def test_outside_runtime(self):
  self.rows[0]['destination']=str(g.WORK/'bad.py');self.pin()
  with self.assertRaises(RuntimeError):g.verify()
 def test_duplicate(self):
  self.rows.append(self.rows[0]);self.pin()
  with self.assertRaises(RuntimeError):g.verify()
if __name__=='__main__':unittest.main()

