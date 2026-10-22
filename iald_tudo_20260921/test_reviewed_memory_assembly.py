"""Check drift rejection and the boundary that protects unreviewed topics."""
import unittest
from assemble_reviewed_memory import verify_capsule, replace_topic, sha

class ReviewGate(unittest.TestCase):
    def setUp(self):
        self.capsule, self.source = b'reviewed prose', b'published evidence'
        self.measure = {'capsule_sha256': sha(self.capsule), 'source_sha256': sha(self.source)}
        self.report = ('APROVADA quanto à fidelidade ' + sha(self.capsule)).encode()

    def test_exact_approved_artifacts_accepted(self):
        verify_capsule(self.capsule, self.source, self.measure, self.report)

    def test_modified_capsule_and_source_rejected(self):
        for capsule, source in [(self.capsule+b'x', self.source), (self.capsule, self.source+b'x')]:
            with self.subTest(capsule=capsule):
                with self.assertRaises(ValueError):
                    verify_capsule(capsule, source, self.measure, self.report)

    def test_negative_review_rejected(self):
        with self.assertRaises(ValueError):
            verify_capsule(self.capsule, self.source, self.measure, b'Revision required')

    def test_replacement_preserves_neighbors_and_exposition(self):
        original = 'kernel\n### example\nFonte: resultado_publicado_integral /core/example\n{"a":1}\n\n### neighbor\nbody\n## exposition\nformula'
        out, old = replace_topic(original, 'example', '### example — reviewed\ncontent\n')
        self.assertEqual(out, original.replace(old, '### example — reviewed\ncontent'))
        with self.assertRaises(ValueError):
            replace_topic(out, 'example', 'again')
        with self.assertRaises(ValueError):
            replace_topic(original+'\n'+original, 'example', 'duplicate')

if __name__ == '__main__':
    unittest.main()
