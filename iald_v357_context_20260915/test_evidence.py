import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from iald_estado_publicado import published_evidence, PublishedEvidenceError


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        self.paths={key:root/name for key,name in [('program','um.py'),('seal','seal.json'),('result','result.json'),('proof_manifest','proof.json')]}
        self.paths['program'].write_bytes(b'# fixture, never executed\n')
        self.catalog=SimpleNamespace(source_sha=hashlib.sha256(self.paths['program'].read_bytes()).hexdigest(),
            records={'TGL.lean':{'sha256':'fixture-source-hash'}})
        self.result={'core':{
            'qg_closure':{'gate':{'kernel_frontier':{'scope':'minimal','remaining':['H2','H3']}},'formal_flags':{'built':True},'physics_flags':{},'experiment_flags':{}},
            'joint_coincidence_result':dict(protocol_hash='fixture',threshold=1e-30,n_inventory=35,n_admissible=3,
                primary={'p_joint':.5458727599916506,'boolean':False},with_H0_ladder={},generous={},naive_product_INVALID={'why_invalid':'identity residual'},outcome='NOT_EXCLUDED',verdict='False'),
            'the_price_of_the_gravity_proof':{'itens':[{'item':'H1','pago':True,'estado_hoje':'obsolete: open'}],'pagos':1,'abertos':2},
            'the_imported_expectation':{'theorem':'existing imported theorem','statuses':{'mode':'KNOWN'},'citations':[],'verdict':'IMPORTED'}}}
        self.proof={'formal_source_hash':'formal-fixture','formal_files_sha256':{'TGL.lean':'fixture-source-hash'},
            'axiom_report':{'theorem':['propext']},'formal_checker':'fixture','lean_version':[],'timestamp':'fixture'}
        self.seal={'timestamp':'fixture','fail_closed_selftest':'fixture','formal_source_hash':'formal-fixture',
            'collapse_definition':{key:False for key in ('statement_pt','external_reflection_status','physical_collapse_proven','cost_payment_status','qg_gate_moved')}}
        self.config={key:{'path':str(path),'url':'https://example.test/fixture'} for key,path in self.paths.items()}
        self.write()

    def write(self):
        for key,value in [('result',self.result),('proof_manifest',self.proof)]: self.paths[key].write_text(json.dumps(value),encoding='utf-8')
        self.seal['sha256']={self.paths[key].name:hashlib.sha256(self.paths[key].read_bytes()).hexdigest() for key in ('program','result','proof_manifest')}
        self.paths['seal'].write_text(json.dumps(self.seal),encoding='utf-8')

    def test_current_flags_and_negative_statistics_are_preserved(self):
        body,meta=published_evidence(self.config,self.catalog)
        self.assertTrue(meta['published_evidence_checked'])
        self.assertIn('0.5458727599916506',body)
        self.assertIn('"boolean": false',body)
        self.assertIn('"discharged_in_kernel": true',body)
        self.assertNotIn('obsolete: open',body)
        self.assertIn('COMPILER_NOT_RERUN',body)

    def test_changed_artifact_fails_closed(self):
        self.paths['result'].write_bytes(b'{}')
        with self.assertRaises(PublishedEvidenceError): published_evidence(self.config,self.catalog)

    def test_catalog_from_another_release_fails_closed(self):
        self.catalog.source_sha='other-version'
        with self.assertRaises(PublishedEvidenceError): published_evidence(self.config,self.catalog)

    def test_axiom_outside_policy_fails_closed(self):
        self.proof['axiom_report']['theorem'].append('sorryAx')
        self.write()
        with self.assertRaises(PublishedEvidenceError): published_evidence(self.config,self.catalog)

    def test_changed_formal_source_fails_closed(self):
        self.catalog.records['TGL.lean']['sha256']='different'
        with self.assertRaises(PublishedEvidenceError): published_evidence(self.config,self.catalog)

    def test_missing_config_does_not_claim_verified_evidence(self):
        self.assertEqual(published_evidence(None,self.catalog),('',{}))
        with self.assertRaises(PublishedEvidenceError): published_evidence({'seal':self.config['seal']},self.catalog)

if __name__=='__main__': unittest.main(verbosity=2)
