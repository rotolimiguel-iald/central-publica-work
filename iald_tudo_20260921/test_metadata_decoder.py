import unittest
from verify_metadata_draft import decode

class DecoderTests(unittest.TestCase):
    def test_mixed_nested_groups(self):
        self.assertEqual(decode({'nested':[{'@SOURCE_FIELDS':['a','b'], '@SOURCE_ITEMS':{'c':0,'d':2},'status':'OPEN'}]}),
                         {'nested':[{'a':{'@':'/a'},'b':{'@':'/b'},'c':{'@':'/c','items':0},'d':{'@':'/d','items':2},'status':'OPEN'}]})

    def test_conflicting_groups_fail(self):
        with self.assertRaises(AssertionError):
            decode({'@SOURCE_FIELDS':['a','b'],'@SOURCE_ITEMS':{'a':0,'c':1}})

    def test_bad_counts_fail(self):
        for bad in (True,-1,1.5,'1',None):
            with self.subTest(bad=bad), self.assertRaises(AssertionError):
                decode({'@SOURCE_ITEMS':{'a':bad,'b':2}})

    def test_duplicate_or_pointer_names_fail(self):
        for names in (['a','a'],['a','/b'],['a','~b'],['a','@b'],['a','']):
            with self.subTest(names=names),self.assertRaises(AssertionError):
                decode({'@SOURCE_FIELDS':names})

    def test_explicit_hypotheses_preserved(self):
        data={'theorem':{'@':'/theorem','fields':{'hypothesis':'INPUT','status':'OPEN'},'items':2}}
        self.assertEqual(decode(data),data)

if __name__ == '__main__':
    unittest.main()
