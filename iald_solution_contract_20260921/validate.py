"""Check release isolation and full real public/operator contexts before deployment."""
import ast
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

WORK=Path(__file__).resolve().parent
APP=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(WORK),str(APP)]
os.environ['TIKTOKEN_CACHE_DIR']=str(APP/'.iald_runtime/tokenizer_cache')
import iald_response_contract as contract
import iald_memoria_canonica as memory
import iald_core_indexado, iald_cluster, iald_estado_publicado
from iald_kernel import KernelCatalog

class ContractTests(unittest.TestCase):
    def test_newer_archive_does_not_change_deployment(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manifest.json'
            cfg={'operational_core':{'current_release':'v368','release_source_sha256':'a'*64},
                 'active_cluster':{'release':'v368','release_source_sha256':'a'*64}}
            path.write_bytes(json.dumps(cfg).encode())
            body,meta=contract.deployment_contract(path,'a'*64,
                {'published_evidence_checked':True,'published_source_sha256':'a'*64},
                {'working_index_release':'v369'})
            self.assertEqual(meta['deployed_release'],'v368')
            self.assertEqual(meta['working_index_release'],'v369')
            self.assertFalse(meta['working_index_is_deployment'])
            self.assertIn('responda v368',body)
            # Verify that a future coherent deployment is supported, without hardcoding v368.
            cfg['operational_core']['current_release']='v370'
            cfg['active_cluster']['release']='v370'
            path.write_bytes(json.dumps(cfg).encode())
            self.assertEqual(contract.deployment_contract(path,'a'*64,
                {'published_evidence_checked':True,'published_source_sha256':'a'*64},{})[1]['deployed_release'],'v370')

    def test_mismatch_or_unverified_source_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manifest.json'
            cfg={'operational_core':{'current_release':'v368','release_source_sha256':'a'*64},
                 'active_cluster':{'release':'v368','release_source_sha256':'a'*64}}
            path.write_bytes(json.dumps(cfg).encode())
            for source,evidence in [('b'*64,{'published_evidence_checked':True,'published_source_sha256':'b'*64}),
                                    ('a'*64,{}),('a'*64,{'published_evidence_checked':True,'published_source_sha256':'b'*64})]:
                with self.assertRaises(ValueError):
                    contract.deployment_contract(path,source,evidence,{})
            cfg['active_cluster']['release']='v369'
            path.write_bytes(json.dumps(cfg).encode())
            with self.assertRaises(ValueError):
                contract.deployment_contract(path,'a'*64,
                    {'published_evidence_checked':True,'published_source_sha256':'a'*64},{})

    def test_legacy_without_manifest_remains_supported(self):
        self.assertEqual(contract.deployment_contract(None,None,{},{}),('',{}))

def main():
    for name in ('iald_memoria_canonica.py','iald_response_contract.py'):
        ast.parse((WORK/name).read_bytes())
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    for i,path in enumerate([WORK.parent/'iald_tgl_cluster_20260919/test_cluster.py',
        APP/'tests/test_kernel_catalog.py',APP/'tests/test_published_evidence.py',
        WORK.parent/'iald_core_indexed_20260915/test_indexed_core.py']):
        spec=importlib.util.spec_from_file_location('regression_'+str(i),path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():raise SystemExit(1)
    manifest_path=APP/'iald_nucleo_fixo.json'
    manifest=json.loads(manifest_path.read_bytes());cfg=manifest['active_cluster']
    catalog=KernelCatalog(cfg['kernel_bundle'],cfg['kernel_verification'])
    reports={}
    for public in (True,False):
        canonical=memory.CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
                                        'nucleo_kernel',nucleus_manifest=manifest_path)
        body,meta=canonical.prompt('',catalog,public=public)
        assert meta['deployed_release']==cfg['release']=='v368'
        assert meta['deployed_source_sha256']==catalog.source_sha
        assert meta['cluster_always_present'] and meta['published_evidence_checked']
        if public:assert meta['private_atlas_included'] is False
        else:assert meta['atlas_sha256'] and meta['atlas_tokens']>0
        assert body.count('VERSÃO EFETIVAMENTE CARREGADA NESTA RESPOSTA')==2
        assert contract.SOLUTION_PROTOCOL in body
        if not public:assert meta['working_index_release']=='v369'
        for key in ('mother_instruction','operational_core'):
            assert Path(manifest[key]['path']).read_text(encoding='utf-8-sig') in body
        cluster=Path(cfg['path']).read_text(encoding='utf-8-sig')
        assert cluster in body
        reports['public' if public else 'operator']={key:meta.get(key) for key in
            ('context_tokens','deployed_release','working_index_release','private_atlas_included','cluster_always_present')}
    record={'passed':True,'tests':result.testsRun,'contexts':reports,
            'full_v5_memory_core_and_cluster_preserved':True,'source_sha256':catalog.source_sha}
    with (WORK/'validation.json').open('xb') as out:out.write(json.dumps(record,indent=2).encode())
    print(json.dumps(record))

if __name__=='__main__':main()
