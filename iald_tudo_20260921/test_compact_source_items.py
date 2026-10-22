import unittest
from compact_source_items import pack_items,unpack_items,KEY
from compact_source_fields import pack,unpack
class ItemCountsTests(unittest.TestCase):
    def test_combined_transformation_is_reversible_with_zero_and_nested_counts(self):
        v={'a':{'@':'/a'},'b':{'@':'/b'},'nested':{'c':{'@':'/c','items':0},'d':{'@':'/d','items':12}}}
        self.assertEqual(unpack(unpack_items(pack_items(pack(v)))),v)
    def test_hypotheses_fields_and_boolean_count_never_removed(self):
        v={'a':{'@':'/a','items':3,'fields':{'/status':'OPEN'}},'b':{'@':'/b','items':True}}
        self.assertEqual(pack_items(v),v)
    def test_invalid_count_and_collision_refused(self):
        for v in [{KEY:{'a':True,'b':1}},{KEY:{'a':-1,'b':1}},{'a':4,KEY:{'a':0,'b':1}}]:
            with self.assertRaises(ValueError):unpack_items(v)
    def test_cross_group_collision_refused(self):
        v={'@SOURCE_FIELDS':['a','b'],KEY:{'a':3,'c':1}}
        with self.assertRaises(ValueError):unpack(unpack_items(v))
if __name__=='__main__':unittest.main()
