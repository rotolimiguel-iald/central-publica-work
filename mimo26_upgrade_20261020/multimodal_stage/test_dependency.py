import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import iald_mimo_multimodal as media

class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='dependency_test_',dir=Path(__file__).resolve().parent)
        self.root=Path(self.temp.name)
        self.swap=patch.object(media,'VENDOR',self.root); self.swap.start()
    def tearDown(self): self.swap.stop();self.temp.cleanup()
    def prepare(self):
        data=b'synthetic executable test bytes; never executed'
        (self.root/'ffprobe.exe').write_bytes(data)
        (self.root/'manifest.json').write_text(json.dumps({'files':{'ffprobe.exe':hashlib.sha256(data).hexdigest()},'source':'https://example.invalid/test-only'}))
        return data
    def test_missing_pin_wav_only(self):
        caps=media.media_capabilities()
        self.assertTrue(caps['audio']);self.assertFalse(caps['video'])
        self.assertEqual(caps['audio_formats'],['wav'])
    def test_verified_available(self):
        self.prepare();caps=media.media_capabilities()
        self.assertTrue(caps['video']);self.assertIn('mp3',caps['audio_formats'])
        self.assertNotIn('ffprobe',json.dumps(caps));self.assertNotIn(str(self.root),json.dumps(caps))
    def test_executable_swapped(self):
        self.prepare();(self.root/'ffprobe.exe').write_bytes(b'swapped')
        self.assertFalse(media.media_capabilities()['video'])
    def test_manifest_invalid(self):
        self.prepare();(self.root/'manifest.json').write_text('{"files":{"ffprobe.exe":"wrong"}}')
        self.assertFalse(media.media_capabilities()['video'])
    def test_no_path_bypass(self):
        with patch('shutil.which',return_value='untrusted.exe') as lookup:
            self.assertFalse(media.media_capabilities()['video']);lookup.assert_not_called()
    def test_execution_snapshot(self):
        data=self.prepare();destination=self.root/'snapshot.exe'
        media._copy_verified_decoder(destination)
        (self.root/'ffprobe.exe').write_bytes(b'changed after copy')
        self.assertEqual(destination.read_bytes(),data)
    def test_corrupt_snapshot_not_accepted(self):
        self.prepare();(self.root/'ffprobe.exe').write_bytes(b'swapped')
        with self.assertRaises(ValueError):media._copy_verified_decoder(self.root/'rejected.exe')
    def test_missing_file(self):
        self.prepare();(self.root/'ffprobe.exe').unlink()
        self.assertFalse(media.media_capabilities()['video'])
    def test_manifest_object_required(self):
        (self.root/'manifest.json').write_text('[]')
        self.assertFalse(media.media_capabilities()['video'])

if __name__=='__main__':unittest.main(verbosity=2)
