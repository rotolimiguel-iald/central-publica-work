import difflib
import unittest
from pathlib import Path
from merge_client import merge, sha, Refusal


def patch(a, b, context=0):
    return ''.join(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                                      fromfile='base', tofile='candidate', n=context)).encode()


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.text = 'one\ntwo\nthree\nfour\nfive\n'
        self.raw = self.text.replace('\n', '\r\n').encode()
        self.a = patch(self.text, self.text.replace('two', 'TWO'))
        self.b = patch(self.text, self.text.replace('five', 'FIVE'))

    def runmerge(self, patches, raw=None):
        raw = self.raw if raw is None else raw
        return merge(raw, sha(raw), patches)[0]

    def test_order_independent_crlf(self):
        a = [('waiting', self.a), ('repair', self.b)]
        result = self.runmerge(a)
        self.assertEqual(result, self.runmerge(a[::-1]))
        self.assertEqual(result, b'one\r\nTWO\r\nthree\r\nfour\r\nFIVE\r\n')

    def test_overlap(self):
        with self.assertRaisesRegex(Refusal, 'collisions'):
            self.runmerge([('a', self.a), ('b', self.a)])

    def test_context_overlap(self):
        with self.assertRaisesRegex(Refusal, 'collisions'):
            self.runmerge([('a', patch(self.text, self.text.replace('two', 'TWO'), 3)),
                           ('b', patch(self.text, self.text.replace('five', 'FIVE'), 3))])

    def test_wrong_baseline(self):
        with self.assertRaises(Refusal):
            merge(self.raw, '0'*64, [('a', self.a)])
        with self.assertRaises(Refusal):
            self.runmerge([('a', self.a.replace(b'-two', b'-wrong'))])

    def test_insert_collision(self):
        p = patch(self.text, self.text.replace('two\n', 'two\ninsert\n'))
        with self.assertRaisesRegex(Refusal, 'collisions'):
            self.runmerge([('a', p), ('b', p)])

    def test_mixed_newline(self):
        with self.assertRaises(Refusal):
            self.runmerge([('a', self.a)], b'one\r\ntwo\n')

    def test_bom(self):
        self.assertTrue(self.runmerge([('a', self.a)], b'\xef\xbb\xbf'+self.raw).startswith(b'\xef\xbb\xbf'))

    def test_actual_frozen_waiting_diffs(self):
        w = Path(__file__).resolve().parent.parent/'waiting'
        for name in ['iald.js', 'iald.css']:
            raw = (w/(name+'.baseline')).read_bytes()
            output = merge(raw, sha(raw), [(name, (w/(name+'.diff')).read_bytes())])[0]
            self.assertEqual(output.decode().replace('\r\n', '\n'),
                             (w/name).read_text(encoding='utf-8'))
            self.assertEqual(output.count(b'\n'), output.count(b'\r\n'))


if __name__ == '__main__':
    unittest.main()
