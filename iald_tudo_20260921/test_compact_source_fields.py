import unittest
from compact_source_fields import pack,unpack,KEY
class SourceFieldsTests(unittest.TestCase):
    def test_lossless_nested_reference_grouping(self):
        n={'items':[{'a':{'@':'/a'},'b':{'@':'/b'},'text':'formula unchanged'}]}
        self.assertEqual(unpack(pack(n)),n)
        self.assertEqual(pack(n)['items'][0][KEY],['a','b'])
    def test_protected_fields_and_evidence_not_dropped(self):
        n={'a':{'@':'/a','fields':{'/status':'OPEN'}},'b':{'@':'/b','items':2},
           'c':{'@EXPOSITION':'literal','span':[0,3],'starts_with':'abc'}}
        self.assertEqual(pack(n),n)
    def test_ambiguous_pointer_names_not_grouped(self):
        n={'a/b':{'@':'/a/b'},'c~d':{'@':'/c~d'},'a':{'@':'/different'}}
        self.assertEqual(pack(n),n)
    def test_decoder_refuses_overwrite_and_duplicates(self):
        for n in [{KEY:['a','a']},{'a':4,KEY:['a','b']},{KEY:'ab'}]:
            with self.assertRaises(ValueError):unpack(n)
    def test_reserved_key_collision_is_visible(self):
        with self.assertRaises(ValueError):pack({KEY:['a','b']})
if __name__=='__main__':unittest.main()
