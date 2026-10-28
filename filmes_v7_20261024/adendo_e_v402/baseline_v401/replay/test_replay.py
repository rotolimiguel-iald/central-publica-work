"""Offline source and numerical conformance tests. Does not import um.py."""
import ast, copy, hashlib, importlib.util, json, math, pathlib, time, unittest
import build_replay as build
from replay_runner import calculate
R=pathlib.Path(__file__).resolve().parent.parent
class ReplayTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((R/'replay/replay-manifest.json').read_bytes());cls.anchors=json.loads((R/'replay/anchors.json').read_bytes())
  cls.source=(R/'source/um.py').read_bytes();cls.excerpt=(R/'replay/um_nucleo_filme.py').read_bytes();cls.scalar=(R/'replay/um_scalar_excerpt.py').read_bytes()
  t=time.perf_counter();cls.result=calculate(cls.excerpt.decode(),cls.scalar.decode());cls.seconds=time.perf_counter()-t
 def test_source_pin_and_seal(self):
  seal=json.loads((R/'source/um_absoluto_selo.json').read_bytes())
  self.assertEqual(build.digest(self.source),seal['sha256']['um.py']);self.assertEqual(build.digest(self.source),self.m['source']['sha256'])
 def test_ranges_are_exact_source_bytes(self):
  lines=self.source.splitlines(keepends=True)
  for a in self.m['excerpt_ranges']:
   origin=b''.join(lines[a['source_start_line']-1:a['source_end_line']]);cut=self.excerpt[a['excerpt_byte_start']:a['excerpt_byte_end']]
   self.assertEqual(origin,cut);self.assertEqual(build.digest(cut),a['sha256'])
 def test_scalar_is_exact(self):
  a=self.m['scalar_range'];self.assertEqual(self.scalar,b''.join(self.source.splitlines(keepends=True)[a['source_start_line']-1:a['source_end_line']]))
 def test_no_original_import_or_top_level_effects(self):
  tree=ast.parse(self.excerpt)
  for n in tree.body:self.assertIsInstance(n,(ast.FunctionDef,ast.Assign,ast.Import))
  self.assertEqual({a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names},{'math','numpy'})
  forbidden={'open','eval','exec','compile','__import__'}
  self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in forbidden for n in ast.walk(tree)))
 def test_all_numerical_anchors(self):
  self.assertGreaterEqual(len(self.anchors),20)
  for a in self.anchors:self.assertLessEqual(abs(self.result['values'][a['key']]-a['value']),a['atol'],a['key'])
 def test_hud_anchors_independent(self):
  hud=json.loads((R/'data/hud.json').read_bytes());table={a['key']:a for a in self.anchors}
  for match in self.m['hud_compared']:
   item=next(i for i in hud['items'] if i['id']==match['id']);a=table[match['key']]
   self.assertLessEqual(abs(self.result['values'][item['key']]-item['value']),a['atol'])
 def test_no_anchor_values_in_runner_input(self):
  import inspect
  self.assertEqual(list(inspect.signature(calculate).parameters),['excerpt','scalar','progress'])
 def test_tampered_source_detected(self):
  bad=self.excerpt.replace(b'SEALED_CODATA_ALPHA = ',b'SEALED_CODATA_ALPHA = 2 * ',1)
  self.assertNotEqual(build.digest(bad),self.m['assets']['um_nucleo_filme.py']['sha256'])
  changed=calculate(bad.decode(),self.scalar.decode())
  a=next(a for a in self.anchors if a['key']=='core.graviton_polarization.values.beta_runtime')
  self.assertGreater(abs(changed['values'][a['key']]-a['value']),a['atol'])
 def test_chain_zero_cannot_pass(self):
  a=next(a for a in self.anchors if a['key']=='core.powers_ladder.values.ratio_chain_N8');self.assertGreater(abs(a['value']),a['atol'])
 def test_vendor_budget_and_pins(self):
  v=self.m['vendor'];self.assertLessEqual(v['total_bytes'],25000000)
  for f in v['files']:
   b=(R/'web/vendor/pyodide'/f['name']).read_bytes();self.assertEqual(build.digest(b),f['sha256']);self.assertEqual(len(b),f['bytes'])
 def test_all_assets_pinned(self):
  for a in self.m['assets'].values():self.assertEqual(build.digest((R/'replay'/a['url']).read_bytes()),a['sha256'])
 def test_hud_source_identity_rejected(self):
  from unittest.mock import patch
  hud_path=R/'data/hud.json';original=pathlib.Path.read_bytes
  def read(path):
   data=original(path)
   if path==hud_path:
    value=json.loads(data);value['seal_pin']='0'*64;return build.encoded(value)
   return data
  with patch.object(pathlib.Path,'read_bytes',read):
   with self.assertRaisesRegex(ValueError,'HUD source identity'):
    build.build(R/'source/um.py',hud_path,R/'replay/invalid_hud_test')
 def test_uncomputed_fields_explicit(self):
  self.assertIn('einstein',self.m['hud_documentary_only']);self.assertIn('z_disc',self.m['hud_documentary_only'])
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReplayTests);out=unittest.TextTestRunner(verbosity=1).run(suite)
 report={'status':'PASS' if out.wasSuccessful() else 'FAIL','tests':out.testsRun,'failures':len(out.failures),'errors':len(out.errors),'engine':'CPython','source':ReplayTests.m['source']['version'],'numpy_version':ReplayTests.result['numpy_version'],'calculation_seconds':ReplayTests.seconds,'anchors':len(ReplayTests.anchors),'source_sha256':ReplayTests.m['source']['sha256'],'excerpt_sha256':build.digest(ReplayTests.excerpt),'manifest_sha256':build.digest((R/'replay/replay-manifest.json').read_bytes()),'rows':[dict(a,actual=ReplayTests.result['values'][a['key']],residual=abs(ReplayTests.result['values'][a['key']]-a['value'])) for a in ReplayTests.anchors]}
 build.write(R/'replay/TEST_OFFLINE.json',build.encoded(report));raise SystemExit(not out.wasSuccessful())
