import unittest
from remap_reviewed_interval import remap_interval


class IntervalTests(unittest.TestCase):
    def setUp(self):
        self.before='prefix\n';self.old='old passage in reviewed section\n'
        self.after='**Estatutos [previous]** unchanged summary\n'
        self.replacement='**Estatutos [new]** shorter summary\n'
        self.args=dict(old_exposition=self.before+self.old+self.after,
            new_exposition=self.before+self.replacement+self.after,
            start=len(self.before),old_length=len(self.old),replacement=self.replacement,
            summary_id='new',summary_span=[len(self.before),len(self.replacement)],
            source_pointer='/core/topic')

    def test_old_summary_shifts_but_keeps_exact_content(self):
        node={'@SUMMARY':'previous','source_pointer':'/core/older/value',
              'span':[len(self.before+self.old),len(self.after)]}
        result,_=remap_interval(node,**self.args)
        self.assertEqual(result['span'],[len(self.before+self.replacement),len(self.after)])
        self.assertEqual(result['source_pointer'],node['source_pointer'])

    def test_removed_literal_becomes_explicit_summary_with_primary_path(self):
        node={'@':'/nested','fields':{'/value':{'@EXPOSITION':'literal',
              'starts_with':'old passage','span':[len(self.before),len(self.old)]}}}
        result,_=remap_interval(node,**self.args)
        ref=result['fields']['/value']
        self.assertEqual(ref['@SUMMARY'],'new')
        self.assertEqual(ref['source_pointer'],'/core/topic/nested/value')
        self.assertNotIn('starts_with',ref)

    def test_before_replacement_remains_identical(self):
        node={'@EXPOSITION':'literal','starts_with':'prefix','span':[0,len(self.before)]}
        result,changes=remap_interval(node,**self.args)
        self.assertEqual(result,node);self.assertEqual(changes,[])

    def test_boundary_crossing_is_not_silently_remapped(self):
        node={'@EXPOSITION':'literal','starts_with':'prefix','span':[0,len(self.before)+3]}
        with self.assertRaisesRegex(ValueError,'crosses'):
            remap_interval(node,**self.args)

    def test_unrelated_exposition_change_is_rejected(self):
        args=dict(self.args);args['new_exposition']+='unexpected'
        with self.assertRaisesRegex(ValueError,'outside replacement'):
            remap_interval({},**args)


if __name__=='__main__':unittest.main()
