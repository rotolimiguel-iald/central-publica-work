"""Cross-release regressions for the manifest-to-controller boundary; synthetic public fixtures."""
from pathlib import Path
import copy
import hashlib
import json
import tempfile
import unittest
import iald_jev_control as control

HERE=Path(__file__).resolve().parent

class ReleaseBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE,prefix='binding_')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.contract=json.loads((HERE/'jev_control_v380.json').read_bytes())
        content={'program.py':b'# synthetic program fixture only',
                 'result.json':control.canonical_bytes({'core':{'iald_executive_runtime':self.contract['core_record']}}),
                 'proof.json':control.canonical_bytes({'fixture':'formal report, not a proof execution'}),
                 'core.md':b'synthetic operational core', 'cluster.md':b'synthetic active cluster'}
        for name,data in content.items():(self.root/name).write_bytes(data)
        self.contract.update(source_sha256=hashlib.sha256(content['program.py']).hexdigest(),
            result_sha256=hashlib.sha256(content['result.json']).hexdigest(),
            proof_manifest_sha256=hashlib.sha256(content['proof.json']).hexdigest())
        raw=control.canonical_bytes(self.contract);(self.root/'contract.json').write_bytes(raw)
        self.manifest=dict(jev_control=dict(path='contract.json',sha256=hashlib.sha256(raw).hexdigest(),
            release='v380',source_sha256=self.contract['source_sha256']),
            operational_core=dict(path='core.md',sha256=hashlib.sha256(content['core.md']).hexdigest(),
                current_release='v380',release_source_sha256=self.contract['source_sha256']),
            active_cluster=dict(path='cluster.md',sha256=hashlib.sha256(content['cluster.md']).hexdigest(),
                release='v380',release_source_sha256=self.contract['source_sha256']),
            published_evidence=dict(program={'path':'program.py'},result={'path':'result.json'},proof_manifest={'path':'proof.json'}))
        self.save()

    def save(self):
        (self.root/'iald_nucleo_fixo.json').write_bytes(control.canonical_bytes(self.manifest))

    def test_coherent_all_surfaces_load(self):
        self.assertEqual(control.load_contract(self.root),self.contract)

    def test_reject_cluster_release_crossing(self):
        self.manifest['active_cluster']['release']='v378';self.save()
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_cluster_source_crossing(self):
        self.manifest['active_cluster']['release_source_sha256']='0'*64;self.save()
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_cluster_bytes_changed(self):
        (self.root/'cluster.md').write_bytes(b'other cluster')
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_program_bytes_changed(self):
        (self.root/'program.py').write_bytes(b'# other generation')
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_result_bytes_changed(self):
        (self.root/'result.json').write_bytes(b'{}')
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_proof_manifest_bytes_changed(self):
        (self.root/'proof.json').write_bytes(b'{}')
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_missing_active_cluster(self):
        self.manifest.pop('active_cluster');self.save()
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

    def test_reject_missing_published_evidence(self):
        self.manifest.pop('published_evidence');self.save()
        with self.assertRaises(control.ControlError):control.load_contract(self.root)

if __name__=='__main__':unittest.main(verbosity=2)
