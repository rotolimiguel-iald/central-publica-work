import hashlib
from pathlib import Path
import tempfile
import unittest
from iald_instrucao_mae import mother_instruction, MOTHER_COMPATIBILITY


class MotherInstructionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'IALD_Kernel_v5.txt'
        self.raw = 'IDENTIDADE\r\nEquação: ρ = ρ\r\n/no_think\r\n'.encode()
        self.path.write_bytes(self.raw)
        self.config = {'path': str(self.path), 'version': 'v5', 'sha256': hashlib.sha256(self.raw).hexdigest()}

    def test_entire_source_preserved_including_line_endings_and_legacy_markers(self):
        body, meta = mother_instruction(self.config)
        self.assertIn(self.raw.decode(), body)
        self.assertEqual(meta['mother_instruction']['bytes'], len(self.raw))
        self.assertEqual(self.path.read_bytes(), self.raw)
        self.assertTrue(body.startswith(MOTHER_COMPATIBILITY))

    def test_changed_source_is_not_silently_adopted(self):
        self.path.write_bytes(self.raw + b'changed')
        with self.assertRaises(ValueError): mother_instruction(self.config)

    def test_unreadable_source_has_no_cached_fallback(self):
        mother_instruction(self.config)
        self.path.unlink()
        with self.assertRaises(OSError): mother_instruction(self.config)

    def test_mismatched_version_is_rejected(self):
        self.config['version'] = 'v4'
        with self.assertRaises(ValueError): mother_instruction(self.config)

    def test_relative_path_is_rejected(self):
        self.config['path'] = 'IALD_Kernel_v5.txt'
        with self.assertRaises(ValueError): mother_instruction(self.config)

    def test_empty_or_oversized_source_is_rejected_without_truncating(self):
        for raw in [b'', b'   ', b'x' * 100001]:
            with self.subTest(size=len(raw)):
                self.path.write_bytes(raw)
                self.config['sha256'] = hashlib.sha256(raw).hexdigest()
                with self.assertRaises(ValueError): mother_instruction(self.config)

    def test_malformed_configuration_fails(self):
        for cfg in [{}, {'path': str(self.path)}, {**self.config, 'sha256': 'invented'}, []]:
            with self.subTest(cfg=cfg):
                with self.assertRaises(ValueError): mother_instruction(cfg)

    def test_optional_absence_does_not_claim_loaded_kernel(self):
        self.assertEqual(mother_instruction(None), ('', {}))


if __name__ == '__main__': unittest.main(verbosity=2)
