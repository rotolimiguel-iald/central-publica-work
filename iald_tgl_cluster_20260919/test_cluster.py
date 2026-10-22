import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from iald_cluster import active_cluster

class ClusterTests(unittest.TestCase):
    def test_tamper_and_version_mismatch_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); cluster=root/'cluster.md'; manifest=root/'manifest.json'
            raw=b'# Test\n### topic\ncontent'
            cluster.write_bytes(raw)
            cfg={'path':str(cluster),'sha256':hashlib.sha256(raw).hexdigest(),
                 'release':'v368','commit':'a'*40,'release_source_sha256':'b'*64,'core_sections':1}
            manifest.write_text(json.dumps({'active_cluster':cfg}))
            self.assertTrue(active_cluster(manifest,'b'*64)[1]['cluster_always_present'])
            with self.assertRaises(ValueError):active_cluster(manifest,'c'*64)
            cluster.write_bytes(raw+b'new')
            with self.assertRaises(ValueError):active_cluster(manifest,'b'*64)

    def test_missing_cluster_preserves_legacy_config(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'manifest.json';path.write_text('{}')
            self.assertEqual(active_cluster(path,'a'*64),('',{}))

if __name__=='__main__':unittest.main()
