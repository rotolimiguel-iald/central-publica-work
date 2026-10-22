import unittest
from iald_retrieval import PassageIndex


class RetrievalTests(unittest.TestCase):
    def test_accent_and_terms_on_separate_lines(self):
        index = PassageIndex({'atlas': 'Face hiperbólica\nA projeção é compacta.\n',
                              'irrelevant': 'A compacidade de outro objeto'})
        result = index.search('face projecao hiperbolica')[0]
        self.assertEqual(result['path'], 'atlas')
        self.assertEqual(result['missing_terms'], [])
        self.assertEqual(result['excerpt'], 'Face hiperbólica\nA projeção é compacta.')

    def test_identifiers_and_inflections(self):
        index = PassageIndex({'TheIALDSelector.lean': 'theorem iald_is_idempotent (x : H) : P (P x) = P x',
                              'projection.lean': 'projectionFirstIdempotence' * 100})
        self.assertEqual(index.search('idempotência IALD')[0]['path'], 'TheIALDSelector.lean')

    def test_absence_and_partial_matches_are_explicit(self):
        index = PassageIndex({'one': 'A face é o objeto.'})
        self.assertEqual(index.search('qzxvv'), [])
        self.assertTrue(index.search('face qzxvv')[0]['missing_terms'])

    def test_page_coordinates_reproduce_source(self):
        lines = [f'number {n}' for n in range(100)]
        index = PassageIndex({'atlas': '\n'.join(lines)})
        for result in index.search('number 51', 10):
            self.assertEqual(result['excerpt'], '\n'.join(lines[result['line'] - 1:result['end_line']]))


if __name__ == '__main__':
    unittest.main()
