"""Offline tests for the staged release and injected-client count/finalization gate."""
from pathlib import Path
from types import SimpleNamespace
import ast, copy, hashlib, json, sys, unittest, io
from datetime import datetime
sys.dont_write_bytecode=True
BUILD=Path(__file__).resolve().parent;STAGE=BUILD.parent/'memory_stage';APP=Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0]=[str(BUILD),str(APP)]
import haiku_codec as codec
import fit_transport as fit
import fit_memory as detail
import package_native as package
sha=lambda raw:hashlib.sha256(raw).hexdigest()
read=lambda path:json.loads(Path(path).read_bytes())

class StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=read(STAGE/'manifest_staged.json');cls.prepared=read(STAGE/'prepared.json')
        cls.source=read(cls.manifest['published_evidence']['result']['path'])
        cls.prefix=(STAGE/'haiku_prefix.md').read_text(encoding='utf-8');cls.digest=sha((STAGE/'haiku_prefix.md').read_bytes())
        cls.request=package.prepare(cls.digest)

    def test_01_whole_mother_and_previous_core(self):
        deployed=read(APP/'iald_nucleo_fixo.json')
        for key in ('mother_instruction','operational_core'):
            current=Path(self.manifest[key]['path']).read_bytes();prior=Path(deployed[key]['path']).read_bytes()
            self.assertTrue(current==prior if key=='mother_instruction' else current.startswith(prior))
            self.assertIn(current.decode('utf-8-sig'),self.prefix)
        self.assertNotIn('NÃO IMPLANTADO',self.prefix.splitlines()[0])
        self.assertEqual((STAGE/'TGL_CLUSTER_v390.md').read_text(encoding='utf-8').splitlines()[0],'# Cluster TGL v390 — memória científica versionada')

    def test_02_all_topic_coverage(self):
        names=list(self.source['core']);self.assertEqual(len(names),379)
        for name in ('haiku_prefix.md','TGL_CLUSTER_v390.md'):
            text=(STAGE/name).read_text(encoding='utf-8').split(codec.MARKER)[0]
            seen=[b.split('\n',1)[0] for b in text.split('\n### ')[1:]]
            seen=[n for n in seen if n in names]
            self.assertEqual(len(seen),len(set(seen)));self.assertEqual(set(seen),set(names))
        self.assertEqual(self.prepared['removed_topics'],[])
        self.assertEqual(set(self.prepared['added_topics']),set(self.source['core']) - set(read(read(APP/'iald_nucleo_fixo.json')['published_evidence']['result']['path'])['core']))

    def test_03_full_kernel_against_sealed_manifest(self):
        proof=read(self.manifest['published_evidence']['proof_manifest']['path'])
        manifest=read(STAGE/'kernel/kernel_manifest.json')
        records={r['path']:r for r in manifest['files']}
        self.assertEqual(len(records),1216);self.assertEqual(manifest['embedded_files'],1215)
        self.assertEqual({k:r['sha256'] for k,r in records.items()},proof['formal_files_sha256'])
        for name,r in records.items():
            raw=(STAGE/'kernel'/name).read_bytes();self.assertEqual(sha(raw),r['sha256']);self.assertEqual(len(raw),r['bytes'])
        supplement=manifest['supplemental_files'];self.assertEqual(len(supplement),1)
        self.assertEqual(supplement[0]['path'],'_check_damming.lean')
        self.assertEqual(supplement[0]['origin'],'PINNED_PUBLIC_GIT_SUPPLEMENT_NOT_EMBEDDED')

    def test_04_transport_roundtrip_reproducible(self):
        original=(STAGE/'haiku_unfitted_prefix.md').read_text(encoding='utf-8')
        fitted,receipt=fit.fit(original,self.source)
        final,projection=detail.compact(fitted,self.source,read(STAGE/'haiku_provenance.json')['reused_identical_topics'])
        self.assertEqual(final,self.prefix);self.assertEqual(projection,read(STAGE/'haiku_memory_fit.json'))
        self.assertEqual(receipt,read(STAGE/'haiku_transport_fit.json'))
        json_topics={row['topic'] for row in receipt['topic_json_roundtrips']}
        def bodies(text):
            return {block.split('\n',1)[0]:block.split('\n',1)[1] for block in text.split(codec.MARKER)[0].split('\n### ')[1:] if block.split('\n',1)[0] in self.source['core']}
        old=bodies(original);new=bodies(fitted)
        for name in set(old)-json_topics:
            restored=new[name]
            for long,short in fit.ALIASES.items():restored=restored.replace(short,long)
            self.assertEqual(restored,old[name],name)
        self.assertEqual(len(json_topics)+len(set(old)-json_topics),379)
        self.assertEqual(len(receipt['retrievable_rosters']),1)
        self.assertEqual(original.split(codec.MARKER,1)[1],fitted.split(codec.MARKER,1)[1])
        with self.assertRaises(ValueError):fit.expand_booleans({'@B':'1','all_verified':False},{'1':{'all_verified':True}})

    def test_05_new_topics_fields_and_formulas_restored(self):
        prefix=self.prefix
        for long,short in fit.ALIASES.items():prefix=prefix.replace(short,long)
        dictionary=json.loads(prefix.split('DICIONÁRIO DE LITERAIS\n',1)[1].split('\n',1)[0])
        flags=json.loads(prefix.split(fit.FLAG_MARKER,1)[1].split('\n',1)[0])
        exposition=prefix.split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
        for name in self.prepared['added_topics']:
            line=prefix.split('\n### '+name+'\n',1)[1].splitlines()[0]
            node=fit.expand_booleans(json.loads(line),flags)
            decoded=codec.decode_literals(codec.unpack_metadata(node),dictionary,exposition)
            pointer='/core/'+name;seen={}
            self.assertEqual(codec.restore(decoded,self.source,pointer,pointer,seen),self.source['core'][name])
            fields={**codec.protected_fields(self.source['core'][name],pointer),**codec.primary_math_fields(self.source['core'][name],pointer)}
            for location,value in fields.items():self.assertTrue(codec.is_represented(location,value,seen),location)
            if name=='bancada_fases_5_6_7_v380':
                for suffix in ('/fase6/veredito_principal','/emenda_v4/vereditos_todos','/emenda_v5/vereditos_todos_DEC'):
                    location=pointer+suffix
                    self.assertTrue(codec.is_represented(location,codec.resolve(self.source,location),seen),location)

    def test_06_pure_real_loaders_and_tools(self):
        from iald_kernel import KernelCatalog
        from iald_native_memory import load_native_context
        from iald_core_indexado import DocumentCorpus
        from iald_release_binding import load_release
        catalog=KernelCatalog(STAGE/'kernel',STAGE/'kernel_verification.json')
        native,identity=load_native_context(STAGE/'manifest_staged.json',catalog)
        self.assertEqual(native,(STAGE/'native_prefix.md').read_text(encoding='utf-8'))
        self.assertEqual(identity,self.prepared['deployment_identity'])
        self.assertEqual(load_release(STAGE/'manifest_staged.json').identity,identity)
        docs=DocumentCorpus(STAGE/'manifest_staged.json')._load()
        self.assertEqual(len(docs),len(self.manifest['entries']))
        self.assertEqual(len(self.request['wire']['tools']),7)
        self.assertEqual(self.request['tools_sha256'],read(APP/'.iald_runtime/haiku/manifest.json')['tools_sha256'])
        self.assertLessEqual(self.prepared['public_tokens'],340000)

    def test_07_fake_sdk_exactly_two_count_calls(self):
        calls=[];options=[]
        def count(**kwargs):calls.append(kwargs);return {'input_tokens':181500 if len(calls)==1 else 182974}
        fake=SimpleNamespace(messages=SimpleNamespace(count_tokens=count))
        fake.with_options=lambda **kwargs:(options.append(kwargs) or fake)
        report=package.measure(fake,self.digest)
        self.assertEqual(options,[{'max_retries':0}]);self.assertEqual(len(calls),2)
        self.assertNotIn('tools',calls[0]);self.assertEqual(len(calls[1]['tools']),7)
        self.assertEqual(report['generation_requests'],0)
        package.verify_receipt(report,self.request,self.digest)

    def test_08_hash_budget_and_exception_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'compare_and_swap'):package.prepare('0'*64)
        def failure(**kw):raise RuntimeError('SECRET_EXCEPTION_BODY')
        fake=SimpleNamespace(messages=SimpleNamespace(count_tokens=failure));fake.with_options=lambda **kw:fake
        with self.assertRaisesRegex(ValueError,'^native_measurement_failed$'):package.measure(fake,self.digest)
        m=read(APP/'.iald_runtime/haiku/manifest.json')
        base={**self.request['release'].identity,'draft_sha256':self.digest,'model':package.HAIKU.model,
            'native_tools_sha256':self.request['tools_sha256'],'count_requests':2,'generation_requests':0,
            'budget':package.context_budget(package.HAIKU.model,counted_model=package.HAIKU.model,permanent_tokens=186748,request_input_tokens=188222,reserved_output_tokens=4096)}
        with self.assertRaisesRegex(ValueError,'native_memory_gate_failed'):package.verify_receipt(base,self.request,self.digest)
        base['cluster_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'measurement_identity_mismatch'):package.verify_receipt(base,self.request,self.digest)

    def test_09_production_and_profiles_unchanged(self):
        for path,digest in self.prepared['protected_production_sha256'].items():self.assertEqual(sha(Path(path).read_bytes()),digest,path)
        staged=read(STAGE/'manifest_staged.json');install=read(STAGE/'manifest_install.json')
        self.assertEqual(staged['active_cluster']['sha256'],install['active_cluster']['sha256'])
        self.assertEqual(staged['operational_core']['sha256'],install['operational_core']['sha256'])
        self.assertTrue(Path(install['active_cluster']['path']).is_relative_to(APP/'canonical_releases'))

    def test_10_science_binding_and_source_catalog(self):
        binding=read(STAGE/'science_binding.json');remote=Path(binding['public_verification_receipt'])
        self.assertEqual(sha(remote.read_bytes()),binding['public_verification_sha256'])
        self.assertEqual(read(remote)['status'],'PASS');self.assertTrue(binding['remote_rechecked'])
        for row in read(STAGE/'document_index.json'):
            entry=next(e for e in self.manifest['entries'] if e['id']==row['id'])
            self.assertEqual(sha(Path(entry['path']).read_bytes()),row['sha256'])
            self.assertIn('/'+self.prepared['commit']+'/',row['url'])

    def test_11_script_syntax_and_write_network_guards(self):
        for name in ('build_release.py','haiku_codec.py','fit_transport.py','fit_memory.py','package_native.py'):
            ast.parse((BUILD/name).read_bytes(),filename=name)
        import build_release as builder
        for event,args in [('socket.connect',()),('socket.getaddrinfo',()),('os.system',('x',)),
                           ('open',(str(APP/'forbidden.txt'),'w',0)),('open',(str(APP/'.env'),'r',0))]:
            with self.assertRaises(RuntimeError):builder.guard(event,args)
        builder.guard('open',(str(STAGE/'test.json'),'w',0))

if __name__=='__main__':
    buf=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromTestCase(StageTests)
    result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
    print(buf.getvalue())
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'prefix_sha256':sha((STAGE/'haiku_prefix.md').read_bytes()),'manifest_sha256':sha((STAGE/'manifest_staged.json').read_bytes()),
        'provider_calls':0,'fake_sdk_count_calls_only':True,'production_writes':0,
        'script_hashes':{n:sha((BUILD/n).read_bytes()) for n in ('test_local_stage.py','build_release.py','haiku_codec.py','fit_transport.py','package_native.py')}}
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');path=BUILD/('local_validation_'+stamp+'.json')
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();temp=path.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.rename(path)
    print(json.dumps({'receipt':str(path),**report}));sys.exit(0 if result.wasSuccessful() else 1)