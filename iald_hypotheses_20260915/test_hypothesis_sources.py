import hashlib
import unittest
from types import SimpleNamespace
from iald_hipoteses import hypothesis_sources


class HypothesisSourcesTests(unittest.TestCase):
    def setUp(self):
        self.source = 'namespace Example\ntheorem established : True := True.intro\nend Example\n'
        digest = hashlib.sha256(self.source.encode()).hexdigest()
        self.catalog = SimpleNamespace(records={'Proof.lean': {'sha256': digest}},
                                       _read_checked=lambda name: self.source)
        self.proof = {'formal_files_sha256': {'Proof.lean': digest},
                      'axiom_report': {'Example.established': []}}
        self.entries = [{'id': 'fixture', 'catalog_path': 'Proof.lean', 'terms': ['Example.established'],
                         'url': 'https://example.test/Proof.lean', 'reading': 'A constructed witness.'}]

    def test_full_source_and_report_provenance_are_preserved(self):
        body, rows = hypothesis_sources(self.entries, self.catalog, self.proof)
        self.assertIn(self.source, body)
        self.assertEqual(rows[0]['terms'][0]['line'], 2)
        self.assertEqual(rows[0]['terms'][0]['axioms_reported'], [])
        self.assertIn('COMPILER_NOT_RERUN', rows[0]['status'])

    def test_missing_reported_term_is_not_promoted(self):
        self.proof['axiom_report'].clear()
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_comment_is_not_a_declaration(self):
        self.source = '-- theorem established : True := True.intro\n'
        digest = hashlib.sha256(self.source.encode()).hexdigest()
        self.catalog.records['Proof.lean']['sha256'] = digest
        self.proof['formal_files_sha256']['Proof.lean'] = digest
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_changed_bytes_are_rejected(self):
        self.source += '-- changed after publication\n'
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_other_release_report_is_rejected(self):
        self.proof['formal_files_sha256']['Proof.lean'] = 'other-release'
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_unchecked_axiom_is_rejected(self):
        self.proof['axiom_report']['Example.established'] = ['sorryAx']
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_invalid_lists_and_duplicate_sources_are_rejected(self):
        for entries in [[], {}, self.entries * 2]:
            with self.subTest(entries=entries):
                with self.assertRaises(ValueError): hypothesis_sources(entries, self.catalog, self.proof)

    def test_optional_absence_claims_nothing(self):
        self.assertEqual(hypothesis_sources(None, self.catalog, self.proof), ('', []))

    def test_unknown_source_is_rejected(self):
        self.entries[0]['catalog_path'] = '../Other.lean'
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)

    def test_oversized_document_fails_without_truncation(self):
        self.source += '-- ' + 'x' * 120000
        digest = hashlib.sha256(self.source.encode()).hexdigest()
        self.catalog.records['Proof.lean']['sha256'] = digest
        self.proof['formal_files_sha256']['Proof.lean'] = digest
        with self.assertRaises(ValueError): hypothesis_sources(self.entries, self.catalog, self.proof)


if __name__ == '__main__':
    unittest.main(verbosity=2)
