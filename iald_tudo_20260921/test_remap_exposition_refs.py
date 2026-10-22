import unittest
from remap_exposition_refs import remap

class RemapTests(unittest.TestCase):
 def test_literal_moved_stays_literal(self):
  old='abc exact words xyz';node={'v':{'@EXPOSITION':'old','starts_with':'exact','span':[4,11]}}
  result,changes=remap(node,old,'PREFIX '+old,[],0,'/core/a')
  self.assertEqual(result['v']['span'],[11,11]);self.assertNotIn('@SUMMARY',result['v']);self.assertEqual(len(changes),1)
 def test_paraphrase_is_explicit_and_source_path_preserved(self):
  old='original words';new='**Estatutos [a]**\n\nA semantic summary.'
  blocks=[{'id':'a','original_section_coordinates':{'unicode_start':0,'unicode_end_exclusive':len(old)}}]
  node={'@':'/statuses','fields':{'/test':{'@EXPOSITION':'old','starts_with':'original','span':[0,len(old)]}}}
  result,_=remap(node,old,new,blocks,0,'/core/a')
  ref=result['fields']['/test'];self.assertEqual(ref['@SUMMARY'],'a');self.assertEqual(ref['source_pointer'],'/core/a/statuses/test');self.assertNotIn('starts_with',ref)
 def test_missing_block_fails(self):
  with self.assertRaises(ValueError):remap({'@EXPOSITION':'old','starts_with':'hello','span':[0,5]},'hello','goodbye',[],0)
 def test_stale_original_span_fails(self):
  with self.assertRaises(ValueError):remap({'@EXPOSITION':'old','starts_with':'wrong','span':[0,5]},'hello','hello',[],0)
 def test_last_block_span_does_not_include_next(self):
  old='old';new='**Estatutos [a]**\nnew\n**Estatutos [b]**\nnext'
  blocks=[{'id':'a','original_section_coordinates':{'unicode_start':0,'unicode_end_exclusive':3}}]
  out,_=remap({'@EXPOSITION':'old','starts_with':'old','span':[0,3]},old,new,blocks,0,'/core/a/statuses/x')
  start,n=out['span'];self.assertNotIn('Estatutos [b]',new[start:start+n])
if __name__=='__main__':unittest.main()
