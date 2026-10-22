"""New synthetic tests only; no real admission, data composite or old test run."""
from pathlib import Path
import hashlib,json,tempfile,unittest,math,ast
from admission import read_admission,AdmissionError
from preflight_bridge import prepare_with_admission
from numerical_qualification import assess_evidence,threshold_stable,NumericalQualificationError

HERE=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()

class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='fixture_',dir=HERE)
        self.root=Path(self.temp.name).resolve()
        assert self.root.parent==HERE.resolve()
        self.addCleanup(self.temp.cleanup)
        self.source=self.root/'fixture.txt'
        self.source.write_bytes(b'fabricated source; no scientific observation')
        self.digest=sha(self.source.read_bytes());self.spec=sha(b'fabricated spec')
        self.verified={'a':{'status':'REAL_DOCUMENTARY_HASH_ONLY','source_sha256':self.digest},
                       'b':{'status':'DECLARADO_UNVERIFIED','source_sha256':None}}
        self.doc={'schema':'iald.fase9.source-admission/v1','act':'D-H','witness':'scalar',
                  'spec_sha256':self.spec,'decision':'ADMIT','authority_evidence':'SYNTHETIC TEST ONLY',
                  'readers':[{'reader_id':x,'sources':[{'path':str(self.source),'sha256':self.digest}]} for x in ['a','b']]}
        self.path=self.root/'admission.json'
        self.gate={'spec_sha256':self.spec,'v2_frozen':False,'verified_readers':self.verified,
                   'binding_sha256':sha(b'fixture binding'),'spec_snapshot':{'leitores':{'a':{},'b':{}}}}
    def run_receipt(self,**updates):
        self.path.write_text(json.dumps(self.doc),encoding='utf-8')
        args=dict(trusted_receipt_sha256=sha(self.path.read_bytes()),spec_sha256=self.spec,
                  verified_readers=self.verified,known_source_hashes={'a':[self.digest]},source_root=self.root)
        args.update(updates);return read_admission(self.path,**args)
    def test_full_receipt_does_not_open(self):
        r=self.run_receipt();self.assertTrue(r['required_sources_admitted']);self.assertEqual(r['n_alvos_declarados'],0)
        self.assertFalse(r['may_open_data']);self.assertFalse(r['authority_verified_by_this_module'])
    def test_partial_admission_preserves_inventory_rule(self):
        self.doc['readers']=self.doc['readers'][1:]
        r=self.run_receipt();self.assertEqual(r['n_alvos_declarados'],0);self.assertFalse(r['required_sources_admitted'])
    def test_absent_act_preserves_pending(self):
        r=prepare_with_admission(self.gate,expected_spec_sha256=self.spec,source_root=self.root)
        self.assertEqual(r['declared_unverified_reader_ids'],['b']);self.assertFalse(r['required_sources_admitted'])
    def test_bridge_consumes_exact_act(self):
        self.run_receipt()
        r=prepare_with_admission(self.gate,expected_spec_sha256=self.spec,source_root=self.root,
            admission_path=self.path,trusted_admission_sha256=sha(self.path.read_bytes()))
        self.assertTrue(r['required_sources_admitted']);self.assertFalse(r['v2_frozen'])
    def test_no_trusted_pin_refused(self):
        with self.assertRaisesRegex(AdmissionError,'AUTHENTICATED_ACT_PIN_MISSING'):self.run_receipt(trusted_receipt_sha256=None)
    def test_scope_mismatch(self):
        self.doc['witness']='joint'
        with self.assertRaisesRegex(AdmissionError,'SCOPE'):self.run_receipt()
    def test_changed_source(self):
        self.source.write_bytes(b'mutated')
        with self.assertRaisesRegex(AdmissionError,'BYTES_CHANGED'):self.run_receipt()
    def test_missing_key_is_typed(self):
        del self.doc['decision']
        with self.assertRaises(AdmissionError):self.run_receipt()
    def test_duplicate_and_unknown_refused(self):
        self.doc['readers'].append(self.doc['readers'][0])
        with self.assertRaisesRegex(AdmissionError,'DUPLICATE'):self.run_receipt()
    def test_root_escape(self):
        with self.assertRaisesRegex(AdmissionError,'OUTSIDE'):self.run_receipt(source_root=self.root/'narrower')
    def test_incomplete_source_scope(self):
        with self.assertRaisesRegex(AdmissionError,'COVER'):self.run_receipt(known_source_hashes={'a':[sha(b'other')]})

class NumericalTests(unittest.TestCase):
    def setUp(self):self.policy=json.loads((HERE/'POLICY_R1.json').read_text(encoding='utf-8'))
    def test_unstable_refused(self):
        with self.assertRaisesRegex(NumericalQualificationError,'NOT_CONVERGED'):
            assess_evidence({'x':{'100':1.,'200':1.2,'400':1.201}},self.policy)
    def test_nan_bool_refused(self):
        for value in [float('nan'),float('inf'),True]:
            with self.subTest(value=value),self.assertRaises(NumericalQualificationError):
                assess_evidence({'x':{'100':0,'200':0,'400':value}},self.policy)
    def test_missing_level_refused(self):
        with self.assertRaises(NumericalQualificationError):assess_evidence({'x':{'100':0,'200':0}},self.policy)
    def test_refinement_is_not_certified(self):
        r=assess_evidence({'x':{'100':0,'200':0,'400':0}},self.policy)
        self.assertIsNone(r['rigorous_integral_error_bound']);self.assertFalse(r['qualified_observed_verdict'])
        with self.assertRaisesRegex(NumericalQualificationError,'MISSING'):threshold_stable(6,None,5)
    def test_threshold_interval(self):
        self.assertEqual(threshold_stable(6,.01,5),'ABOVE')
        self.assertEqual(threshold_stable(4,.01,5),'BELOW')
        with self.assertRaisesRegex(NumericalQualificationError,'WITHIN'):threshold_stable(5.0001,.001,5)
    def test_reused_actual_quadrature_against_analytic_integral(self):
        # Extract only two reviewed pure functions; never execute source module/main.
        origin=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2\f9_runner_v1x_staged_e1_bytes.py')
        raw=origin.read_bytes()
        audit=json.loads((HERE.parent.parent/'fase9_auditoria_20261019'/'STATISTICAL_SCOPE_R1.json').read_text(encoding='utf-8'))
        expected=next(x['sha256'] for x in audit['evidence'] if Path(x['path'])==origin)
        self.assertEqual(sha(raw),expected)
        tree=ast.parse(raw);wanted={'_legendre_nodes_weights','_ln_evidence_uniform'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
        self.assertEqual(len(nodes),2)
        space={'math':math,'ReaderGateError':NumericalQualificationError}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(origin),'exec'),space)
        a=.7; exact=math.log(math.sqrt(math.pi)*math.erf(a)/(2*a))
        levels={str(n):space['_ln_evidence_uniform'](lambda x:-x*x,-a,a,n) for n in self.policy['levels']}
        r=assess_evidence({'analytic_gaussian':levels},self.policy)
        self.assertLess(abs(r['models']['analytic_gaussian']['log_evidence']-exact),1e-12)

if __name__=='__main__':unittest.main()
