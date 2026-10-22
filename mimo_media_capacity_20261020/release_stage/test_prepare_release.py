"""Synthetic fixtures under release_stage only; no actual runtime writes."""
import copy
import json
from pathlib import Path
import unittest
import uuid
import prepare_release as release


class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(__file__).parent/'synthetic_fixtures'/uuid.uuid4().hex
        self.work=self.root/'work';self.runtime=self.root/'fake_runtime_R'
        self.work.mkdir(parents=True);self.runtime.mkdir(parents=True)
        self.config={'groups':{}}
        for group,targets in release.TARGETS.items():
            folder=self.work/release.GROUP_DIRS[group];folder.mkdir()
            entry=dict(final_for_packaging=True,receipt=release.GROUP_DIRS[group]+'/FINAL.json',
                       receipt_status='FINAL_STAGING_READY',files=[])
            receipt=dict(status='FINAL_STAGING_READY',files=[])
            for relative in targets:
                source=folder/relative;source.parent.mkdir(parents=True,exist_ok=True)
                raw=('candidate '+relative).encode();source.write_bytes(raw)
                target=self.runtime/relative
                # Mix existing and new module targets.
                baseline=None
                if not relative.startswith(('private_media','new_private','iald_media')):
                    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(('baseline '+relative).encode())
                    baseline=release.digest(target.read_bytes())
                row=dict(source=str(source.relative_to(self.work)),target=relative,
                         sourcehash=release.digest(raw),baseline=baseline)
                entry['files'].append(row);receipt['files'].append(dict(source=str(source),sha256=row['sourcehash']))
            path=folder/'FINAL.json';path.write_text(json.dumps(receipt),encoding='utf-8')
            entry['receipt_sha256']=release.digest(path.read_bytes());self.config['groups'][group]=entry
        science=self.runtime/'canonical'/'core.txt';science.parent.mkdir();science.write_bytes(b'immutable synthetic science')
        self.science=science
        (self.work/'SCIENCE_BASELINE.json').write_text(json.dumps(dict(release='synthetic',preserve_all=True,
            files=[dict(role='test_core',path=str(science),sha256=release.digest(science.read_bytes()),bytes=science.stat().st_size)])),encoding='utf-8')
        self.before={str(f):release.digest(f.read_bytes()) for f in self.runtime.rglob('*') if f.is_file()}

    def prepare(self,freeze=True):return release.prepare(self.config,self.work,self.runtime,freeze=freeze)

    def test_final_receipts_freeze_exact_18_only_staging(self):
        result=self.prepare();self.assertEqual(result['files'],18)
        plan=json.loads((self.work/'release_stage/INSTALL_PLAN.json').read_bytes())
        self.assertEqual(len(plan['files']),18)
        self.assertEqual({str(f):release.digest(f.read_bytes()) for f in self.runtime.rglob('*') if f.is_file()},self.before)
        for row in plan['files']:
            self.assertEqual(release.digest(Path(row['source']).read_bytes()),row['sourcehash'])
            self.assertEqual(row['destination'],row['target']);self.assertEqual(row['sha256'],row['sourcehash'])
        pin=json.loads((self.work/'release_stage/INSTALL_PLAN_PIN.json').read_bytes())
        self.assertEqual(pin['sha256'],release.digest((self.work/'release_stage/install_plan.json').read_bytes()))

    def test_wait_no_plan_or_tree(self):
        self.config['groups']['client']['final_for_packaging']=False
        result=self.prepare();self.assertEqual(result['status'],'WAITING_FINAL_RECEIPTS')
        self.assertFalse((self.work/'release_stage').exists())

    def test_check_does_not_freeze(self):
        self.assertEqual(self.prepare(False)['status'],'READY_FOR_STAGING_FREEZE')
        self.assertFalse((self.work/'release_stage').exists())

    def test_runtime_cas_rejects_change(self):
        (self.runtime/'iald_app_providers.py').write_bytes(b'changed R')
        with self.assertRaises(release.Refusal):self.prepare()

    def test_source_pin_rejects_change(self):
        (self.work/'backend_stage/iald_app_providers.py').write_bytes(b'changed source')
        with self.assertRaises(release.Refusal):self.prepare()

    def test_receipt_pin_rejects_change(self):
        (self.work/'backend_stage/FINAL.json').write_bytes(b'{}')
        with self.assertRaises(release.Refusal):self.prepare()

    def test_science_change_rejects(self):
        self.science.write_bytes(b'changed science')
        with self.assertRaises(release.Refusal):self.prepare()

    def test_unlisted_or_duplicate_target_rejects(self):
        for target in ['.env','node_modules/pkg/file.js','iald_stack_v7.py','../escape.py','iald_mimo_multimodal.py']:
            config=copy.deepcopy(self.config)
            config['groups']['backend']['files'][0]['target']=target
            with self.subTest(target=target),self.assertRaises(release.Refusal):
                release.prepare(config,self.work,self.runtime,freeze=True)

    def test_no_overwrite_existing_release(self):
        self.prepare()
        with self.assertRaises(release.Refusal):self.prepare()

    def test_source_outside_group_refuses(self):
        self.config['groups']['backend']['files'][0]['source']='../outside/iald_app_providers.py'
        with self.assertRaises(release.Refusal):self.prepare()

    def test_new_target_unexpectedly_created_refuses(self):
        (self.runtime/'private_media_store.py').write_bytes(b'new competitor')
        with self.assertRaises(release.Refusal):self.prepare()

    def test_native_hash_map_receipt(self):
        entry=self.config['groups']['backend'];path=self.work/entry['receipt'];data=json.loads(path.read_bytes())
        data['files']={Path(row['source']).name:row['sha256'] for row in data['files']}
        path.write_text(json.dumps(data),encoding='utf-8');entry['receipt_sha256']=release.digest(path.read_bytes())
        self.assertEqual(self.prepare(False)['status'],'READY_FOR_STAGING_FREEZE')

    def test_primary_pinned_nested_source_manifest(self):
        entry=self.config['groups']['backend'];primary=self.work/entry['receipt'];data=json.loads(primary.read_bytes())
        manifest=primary.with_name('SOURCE_PLAN.json');manifest.write_text(json.dumps(data),encoding='utf-8')
        pin=release.digest(manifest.read_bytes());primary.write_text(json.dumps(dict(status='FINAL_STAGING_READY',plan=dict(sha256=pin))),encoding='utf-8')
        entry['receipt_sha256']=release.digest(primary.read_bytes())
        entry['supplemental_receipts']=[dict(path='backend_stage/SOURCE_PLAN.json',sha256=pin,source_manifest_bound_by_primary_field='plan.sha256',covers_sources=True)]
        self.assertEqual(self.prepare(False)['status'],'READY_FOR_STAGING_FREEZE')
        primary.write_text(json.dumps(dict(status='FINAL_STAGING_READY',plan=dict(sha256='0'*64))),encoding='utf-8')
        entry['receipt_sha256']=release.digest(primary.read_bytes())
        with self.assertRaises(release.Refusal):self.prepare(False)


if __name__=='__main__':unittest.main(verbosity=2)
