"""Independent source-to-candidate checks for the adversarially identified gaps."""
import hashlib
import json
from pathlib import Path
import unittest

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def child(path, key):
    return path + '/' + str(key).replace('~', '~0').replace('/', '~1')


def resolve(document, path):
    for part in path.split('/')[1:]:
        key = part.replace('~1', '/').replace('~0', '~')
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def leaves(value, path):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, child(path, key))
    elif isinstance(value, list):
        for key, item in enumerate(value):
            yield from leaves(item, child(path, key))
    else:
        yield path, value


class SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
        entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
        raw = Path(entry['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == entry['public_sha256']
        cls.source = json.loads(raw)
        receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
        raw = (WORK / 'haiku_candidate.md').read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
        text = raw.decode('utf-8')
        glossary = json.loads(text.split('a referência preserva o valor, não acrescenta estatuto.\n', 1)[1].split('\n', 1)[0])
        exposition = text.split('\n## Exposição canônica integral: fórmulas e derivações', 1)[1][:receipt['exposition_chars']]
        assert hashlib.sha256(exposition.encode('utf-8')).hexdigest() == receipt['exposition_sha256']
        cls.represented = {}
        cls.topics = {}

        def expand(value, path, topic_path):
            if isinstance(value, dict):
                if set(value) == {'@TGL_LITERAL'}:
                    expand(glossary[value['@TGL_LITERAL']], path, topic_path)
                elif set(value) == {'@EXPOSITION', 'starts_with', 'span'}:
                    expected = resolve(cls.source, path)
                    assert isinstance(expected, str) and expected.startswith(value['starts_with'])
                    start, length = value['span']
                    assert type(start) is int and type(length) is int
                    assert start >= 0 and length > 0 and start + length <= len(exposition)
                    actual = exposition[start:start + length]
                    assert actual == expected
                    cls.represented[path] = actual
                elif '@' in value:
                    base = topic_path + value['@']
                    for suffix, item in value.get('fields', {}).items():
                        expand(item, base + suffix, topic_path)
                else:
                    for key, item in value.items():
                        expand(item, child(path, key), topic_path)
            elif isinstance(value, list):
                for key, item in enumerate(value):
                    expand(item, child(path, key), topic_path)
            else:
                cls.represented[path] = value

        for topic in receipt['topics']:
            marker = '\n### ' + topic['id'] + '\nFonte: resultado_publicado_integral ' + topic['pointer'] + '\n'
            assert text.count(marker) == 1
            body = json.loads(text.split(marker, 1)[1].split('\n', 1)[0])
            cls.topics[topic['id']] = body
            expand(body, topic['pointer'], topic['pointer'])

    def assert_source_subtree(self, pointer):
        items = list(leaves(resolve(self.source, pointer), pointer))
        self.assertTrue(items)
        for path, expected in items:
            with self.subTest(path=path):
                self.assertIn(path, self.represented)
                self.assertEqual(self.represented[path], expected)

    def test_entire_echo_hypothesis_survives_with_generic_child_names(self):
        self.assert_source_subtree('/core/gw_echo_kms_rite/record/hypothesis')

    def test_independently_identified_statements_survive(self):
        gaps = json.loads((WORK / 'adversarial_memory_review/missing_source_strings.json').read_bytes())
        paths = [row['pointer'] for row in gaps if row['pointer'].endswith('/statement')]
        self.assertEqual(len(paths), 5)
        for path in paths:
            self.assert_source_subtree(path)

    def test_interface_construction_layers_and_light_chain_survive(self):
        self.assert_source_subtree('/core/interface_is_light/witness_layers')
        self.assert_source_subtree('/core/interface_is_light/light_chain')

    def test_only_boolean_audit_rows_are_externalized(self):
        source = self.source['core']['external_ladder']['per_theorem']
        self.assertTrue(source)
        self.assertTrue(all(type(value) is bool for value in source.values()))
        entry = self.topics['external_ladder']['per_theorem']
        self.assertEqual(entry['@'], '/per_theorem')
        self.assertEqual(entry['true_fields'], sum(source.values()))
        self.assertEqual(entry['false_fields'], len(source) - sum(source.values()))


if __name__ == '__main__':
    unittest.main()
