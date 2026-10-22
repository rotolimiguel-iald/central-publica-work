from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,json,unittest
from claude_memory_package import load_package
from claude_profiles import HAIKU,context_budget

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.prefix='fixture-only'
        (self.root/'prefix.md').write_text(self.prefix,encoding='utf-8')
        self.data={'schema':'iald.claude.memory.v1','model':HAIKU.model,'prefix_file':'prefix.md',
         'prefix_sha256':hashlib.sha256(self.prefix.encode()).hexdigest(),'tools_sha256':'a'*64,
         'budget':context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=183000,
                                 request_input_tokens=184500,reserved_output_tokens=4096)}
        self.save()
    def save(self):
        (self.root/'manifest.json').write_text(json.dumps(self.data),encoding='utf-8')
    def test_load_measured_package(self):
        self.assertEqual(load_package(self.root).prefix,self.prefix)
    def test_changed_prefix_fails(self):
        (self.root/'prefix.md').write_text('changed',encoding='utf-8')
        with self.assertRaises(ValueError):load_package(self.root)
    def test_path_injection_fails(self):
        self.data['prefix_file']='../private.md';self.save()
        with self.assertRaises(ValueError):load_package(self.root)
    def test_wrong_model_fails(self):
        self.data['model']='other';self.save()
        with self.assertRaises(ValueError):load_package(self.root)
    def test_forged_budget_fails(self):
        self.data['budget']['remaining_tokens']=99999;self.save()
        with self.assertRaises(ValueError):load_package(self.root)
    def test_insufficient_dynamic_reserve_fails(self):
        self.data['budget']=context_budget(HAIKU.model,counted_model=HAIKU.model,
            permanent_tokens=190000,request_input_tokens=191500,reserved_output_tokens=4096)
        self.save()
        with self.assertRaises(ValueError):load_package(self.root)
    def test_reduced_reserve_cannot_qualify_package(self):
        self.data['budget']=context_budget(HAIKU.model,counted_model=HAIKU.model,
            permanent_tokens=188000,request_input_tokens=189000,reserved_output_tokens=1,margin_tokens=0)
        self.save()
        with self.assertRaises(ValueError):load_package(self.root)

if __name__=='__main__':unittest.main()
