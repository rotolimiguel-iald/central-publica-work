"""Synthetic checks only. Never runs a benchmark or shadow provider."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from analysis_v2 import analyze,render_header,validate_advisory

class ContractTests(unittest.TestCase):
    def pairs(self,better=False):
        a=dict(supported=1,unsupported=0,contradicted=0,covered=1,input_tokens=10000)
        b=dict(supported=1,unsupported=0,contradicted=0,covered=1,input_tokens=100)
        if better:a.update(supported=0,unsupported=1,covered=0)
        return [dict(id=str(i),targets=1,A=dict(a),B=dict(b),citation_valid_B=True,critical_error_B=False) for i in range(36)]
    def evaluate(self,rows,**kw):
        return analyze(rows,[str(i) for i in range(36)],kw.pop('controls',[True]*6),independent_pairs=kw.pop('independent',True),complete=kw.pop('complete',True))
    def test_equal_perfect_small_sample_is_inconclusive(self):
        r=self.evaluate(self.pairs());self.assertEqual(r['status'],'INCONCLUSIVE');self.assertLess(r['h1_lower'],-.05)
    def test_favorable_fixture_never_authorizes_deployment(self):
        r=self.evaluate(self.pairs(True));self.assertEqual(r['status'],'MEASURED_PASS_WITH_SCOPE');self.assertFalse(r['deployment_authorized'])
    def test_missing_duplicate_pairs_are_not_dropped(self):
        rows=self.pairs();rows[-1]=copy.deepcopy(rows[0])
        with self.assertRaises(ValueError):self.evaluate(rows)
    def test_empty_factual_is_not_perfect_fidelity(self):
        rows=self.pairs()
        for r in rows:r['B'].update(supported=0,covered=0)
        r=self.evaluate(rows);self.assertEqual(r['status'],'NOT_ADOPT');self.assertEqual(r['h1_mean'],-1)
    def test_density_cannot_hide_missing_coverage(self):
        rows=self.pairs(True)
        for r in rows:r.update(targets=2)
        self.assertEqual(self.evaluate(rows)['status'],'NOT_ADOPT')
    def test_zero_tokens_refused(self):
        rows=self.pairs();rows[0]['A']['input_tokens']=0
        with self.assertRaises(ValueError):self.evaluate(rows)
    def test_critical_or_failed_control_blocks(self):
        rows=self.pairs(True);rows[0]['critical_error_B']=True
        self.assertEqual(self.evaluate(rows)['status'],'NOT_ADOPT')
        self.assertEqual(self.evaluate(self.pairs(True),controls=[False]+[True]*5)['status'],'NOT_ADOPT')
    def test_incomplete_and_dependent_runs_do_not_pass(self):
        self.assertEqual(self.evaluate(self.pairs(True),complete=False)['status'],'INCOMPLETE')
        r=self.evaluate(self.pairs(True),independent=False)
        self.assertEqual(r['status'],'INCONCLUSIVE');self.assertIsNone(r['h1_lower'])
    def test_header_hash_is_integrity_and_slice_exact(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            p=Path(d)/'source.txt';p.write_bytes(b'one\r\ntwo\r\n')
            e=dict(source_id='s1',path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),first_line=2,last_line=2,source_statute='DECLARADO')
            h=render_header([e]);self.assertIn(hashlib.sha256(b'two').hexdigest(),h);self.assertIn('"truth_verified": false',h)
            p.write_bytes(b'changed')
            with self.assertRaises(ValueError):render_header([e])
    def test_header_short_pin_refused(self):
        e=dict(source_id='s',path='not_read',sha256='f'*16,first_line=1,last_line=1,source_statute='REAL')
        with self.assertRaises(ValueError):render_header([e])
    def advisory(self):return dict(schema='iald.voice.advisory.v2',statute='DECLARADO',action='suggest',answer='Proposta',suggested_executor='mimo',reason='Catálogo fornecido',evidence=[],uncertainties=[],dispatch_authorized=False)
    def test_advisory_eligibility_and_dispatch_guard(self):
        a=self.advisory();self.assertTrue(validate_advisory(a,['mimo'])['semantic_review_required'])
        with self.assertRaises(ValueError):validate_advisory(a,[])
        a['dispatch_authorized']=True
        with self.assertRaises(ValueError):validate_advisory(a,['mimo'])
    def test_advisory_extra_field_refused(self):
        a=self.advisory();a['tool_call']='execute'
        with self.assertRaises(ValueError):validate_advisory(a,['mimo'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    r=unittest.TextTestRunner(verbosity=2).run(suite)
    result=dict(status='PASS' if r.wasSuccessful() else 'FAIL',tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),scope='Synthetic statistical, integrity and advisory contract only; no model/benchmark/shadow run',provider_calls=0)
    with Path(__file__).with_name('TEST_RESULTS.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    raise SystemExit(0 if r.wasSuccessful() else 1)
