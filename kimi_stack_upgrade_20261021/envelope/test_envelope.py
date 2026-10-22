"""Offline sealed synthetic corpus; no original science execution, jobs or API."""
import sys
sys.dont_write_bytecode=True
import ast,copy,hashlib,importlib.util,json,os,socket,sqlite3,tempfile,types,unittest
from pathlib import Path
from contextlib import closing
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
def module(kind):
    root=HERE/kind/'iald_orchestrator';name='isolated_'+kind
    package=types.ModuleType(name);package.__path__=[str(root)];sys.modules[name]=package
    spec=importlib.util.spec_from_file_location(name+'.canonical_memory',root/'canonical_memory.py')
    result=importlib.util.module_from_spec(spec);sys.modules[spec.name]=result;spec.loader.exec_module(result);return result
OLD=module('baseline');NEW=module('stage')
def dump(obj):return json.dumps(obj,ensure_ascii=False,indent=2).encode()
OBS=[]
def fixture(directory,anchor_size=1600):
    root=Path(directory).resolve();(root/'snapshots').mkdir()
    formal=hashlib.sha256(b'SYNTHETIC_NOT_A_SCIENTIFIC_PROOF').hexdigest()
    data={name:('synthetic document '+name+'\n').encode() for name in NEW.SNAPSHOT_NAMES}
    data['um.py']=b'# synthetic text fixture; NEVER executed/imported\n'
    data['um_absoluto.json']=b'{}'
    data['tgl_kernel_proof_manifest.json']=dump(dict(formal_source_hash=formal))
    data['um_absoluto_forma_canonica.md']=('A'*anchor_size+'\n').encode()
    data['um_absoluto_selo.json']=dump(dict(um_version='v999',fail_closed_selftest='FAIL_CLOSED_SELFTEST_PASSED',formal_source_hash=formal,sha256={n:NEW.digest(data[n]) for n in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json']}))
    docs=[dict(name=n,sha256=NEW.digest(data[n]),bytes=len(data[n])) for n in sorted(data)]
    generation=NEW.digest(json.dumps([(d['name'],d['sha256']) for d in docs],ensure_ascii=False).encode())
    source=root/'snapshots'/('v999_'+generation[:16]);source.mkdir()
    for d in docs:
        p=source/d['name'];p.write_bytes(data[d['name']]);d.update(path=str(p),mtime_ns=p.stat().st_mtime_ns)
    with closing(sqlite3.connect(root/'index.sqlite3')) as db:
        db.execute('CREATE VIRTUAL TABLE passages USING fts5(body,document UNINDEXED,first_line UNINDEXED,last_line UNINDEXED)')
        for d in docs:db.execute('INSERT INTO passages VALUES(?,?,?,?)',(data[d['name']].decode(),d['name'],1,len(data[d['name']].decode().splitlines())))
        db.commit()
    index_hash=NEW.digest((root/'index.sqlite3').read_bytes())
    desc=dict(schema=1,source_mode=NEW.SNAPSHOT_MODE,release='v999',generation=generation,index_sha256=index_hash,documents=[{k:d[k] for k in ['name','sha256','bytes']} for d in docs],formal_source_hash=formal)
    (source/'SEALED_SNAPSHOT.json').write_bytes(dump(desc))
    manifest=dict(schema=1,built_at='SYNTHETIC_FIXTURE_ONLY',generation=generation,index_sha256=index_hash,documents=docs,chunks=13,scope='SYNTHETIC_TEST_ONLY',source_mode=NEW.SNAPSHOT_MODE,snapshot_root=str(source),snapshot_manifest_sha256=NEW.digest((source/'SEALED_SNAPSHOT.json').read_bytes()))
    (root/'manifest.json').write_bytes(dump(manifest));return manifest
def mandatory(m,manifest,prompt='tarefa',allowed=None):
    docs=manifest['documents'] if allowed is None else [d for d in manifest['documents'] if d['name'] in allowed]
    header=m.CORE+'\nGeração do acervo: '+manifest['generation']+'\nVerificação de atualidade: SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
    header+='\nArquivos indexados (não implica leitura integral):\n'+'\n'.join('- '+d['name'] for d in docs)+'\n\nTRECHOS RECUPERADOS (conteúdo documental):\n'
    trailer='\nFIM DA MEMÓRIA DOCUMENTAL\n\nPEDIDO DO OPERADOR:\n'
    return header,trailer,prompt
class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE,prefix='synthetic_');self.addCleanup(self.temp.cleanup);self.path=Path(self.temp.name);self.manifest=fixture(self.path)
        self.net=patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN'));self.net.start();self.addCleanup(self.net.stop)
    def prepare(self,m=NEW,prompt='tarefa',**kw):return m.prepare(prompt,self.path,**kw)
    def test_installed_reproduces_20911_reservation_char_overflow(self):
        args=dict(max_chars=12000,prompt_limit=24000,reserved_context_chars=20911,reserved_context_bytes=20911)
        old=self.prepare(OLD,**args);self.assertTrue(old['receipt']['folded']);self.assertGreater(len(old['prompt'])+20911,12000)
        with self.assertRaisesRegex(ValueError,'obrigatório'):self.prepare(**args)
        OBS.append(dict(case='installed_folded_char_overflow',packet_chars=len(old['prompt']),reserved_chars=20911,total_chars=len(old['prompt'])+20911,cap=12000,fixed='REFUSED'))
    def test_installed_reproduces_maximum_byte_overflow(self):
        for mode in ['maximum','deepseek_maximum']:
            limit=1048576-8192-(393216 if mode=='deepseek_maximum' else 131072)
            args=dict(mode=mode,reserved_context_bytes=limit,reserved_context_chars=0)
            old=self.prepare(OLD,**args);self.assertGreater(len(old['prompt'].encode())+limit,limit)
            with self.assertRaises(ValueError):self.prepare(**args)
            OBS.append(dict(case='installed_'+mode+'_byte_overflow',total_bytes=len(old['prompt'].encode())+limit,cap=limit,fixed='REFUSED'))
    def test_trailer_missing_from_installed_budget(self):
        allowed=['um_absoluto_forma_canonica.md'];prompt='tarefa';header,trailer,_=mandatory(OLD,self.manifest,prompt,allowed)
        wide=self.prepare(OLD,mode='maximum',allowed_sources=allowed)
        block=wide['prompt'][len(header):-(len(trailer)+len(prompt))]
        limit=1048576-131072-8192;reserved=limit-len((header+prompt+block).encode())
        old=self.prepare(OLD,mode='maximum',allowed_sources=allowed,reserved_context_bytes=reserved)
        self.assertFalse(old['receipt']['folded']);self.assertEqual(len(old['prompt'].encode())+reserved-limit,len(trailer.encode()))
        with self.assertRaises(ValueError):self.prepare(mode='maximum',allowed_sources=allowed,reserved_context_bytes=reserved)
        OBS.append(dict(case='installed_trailer_unaccounted',overflow_bytes=len(trailer.encode()),fixed='REFUSED_NO_SAFE_COMPLETE_PASSAGE'))
    def test_normal_same_prompt_sources_generation(self):
        old=self.prepare(OLD);new=self.prepare();self.assertEqual(old['prompt'],new['prompt']);self.assertEqual(old['receipt']['sources'],new['receipt']['sources']);self.assertEqual(old['receipt']['generation'],new['receipt']['generation']);self.assertFalse(new['receipt']['folded'])
    def test_valid_index_only_fold_explicit_and_pinned(self):
        header,trailer,prompt=mandatory(NEW,self.manifest);cap=7000;reserved=cap-len(header+trailer+prompt)-800
        r=self.prepare(max_chars=cap,reserved_context_chars=reserved,reserved_context_bytes=reserved)
        rec=r['receipt'];self.assertTrue(rec['folded']);self.assertEqual(rec['sources'],[]);self.assertEqual(rec['retrieval_scope'],'INDEX_ONLY_NO_PASSAGES');self.assertEqual(len(rec['document_pins']),13);self.assertEqual(rec['index_sha256'],self.manifest['index_sha256']);self.assertEqual(rec['generation'],self.manifest['generation'])
        self.assertIn(NEW.CORE,r['prompt']);self.assertTrue(r['prompt'].endswith(prompt));self.assertIn('índice sem trechos não equivale',r['prompt']);self.assertLessEqual(rec['envelope_total_chars'],cap);self.assertLessEqual(rec['envelope_total_bytes'],rec['envelope_byte_limit']);self.assertGreater(rec['budget_skipped_passages'],0)
    def test_valid_fold_with_atomic_scientific_slice(self):
        path=self.path/'short';path.mkdir();manifest=fixture(path,anchor_size=100)
        header,trailer,prompt=mandatory(NEW,manifest);cap=7000;reserved=cap-len(header+trailer+prompt)-800
        r=NEW.prepare(prompt,path,max_chars=cap,reserved_context_chars=reserved,reserved_context_bytes=reserved)
        self.assertTrue(r['receipt']['folded']);self.assertTrue(r['receipt']['sources']);self.assertEqual(r['receipt']['retrieval_scope'],'SELECTED_PASSAGES_ONLY');self.assertIn('A'*100+'\n',r['prompt']);self.assertLessEqual(r['receipt']['envelope_total_chars'],cap)
    def test_fold_notice_cannot_overflow_mandatory(self):
        header,trailer,prompt=mandatory(NEW,self.manifest);cap=7000;reserved=cap-len(header+trailer+prompt)-10
        with self.assertRaisesRegex(ValueError,'obrigatório'):self.prepare(max_chars=cap,reserved_context_chars=reserved,reserved_context_bytes=reserved)
    def test_unicode_exact_byte_limit_and_display_prompt_preserved(self):
        prompt='instrução completa ç 😀 '*20;display='PEDIDO EXIBIDO INTEGRAL 🧪';r=self.prepare(prompt=prompt,display_prompt=display,max_chars=24000,reserved_context_bytes=1000,reserved_context_chars=1000)
        self.assertTrue(r['prompt'].endswith(display));self.assertEqual(r['receipt']['envelope_total_bytes'],len(r['prompt'].encode())+1000);self.assertEqual(r['receipt']['envelope_total_chars'],len(r['prompt'])+1000)
    def test_maximum_modes_safe_full_accounting(self):
        for mode in ['maximum','deepseek_maximum']:
            r=self.prepare(mode=mode,max_chars=100000,reserved_context_bytes=5000,reserved_context_chars=4000);rec=r['receipt'];self.assertLessEqual(rec['envelope_total_bytes'],rec['envelope_byte_limit']);self.assertLessEqual(rec['envelope_total_chars'],100000)
    def test_bad_reservations_refused(self):
        for value in [-1,True,1.5,'1']:
            with self.assertRaises(ValueError):self.prepare(reserved_context_bytes=value)
    def test_empty_allowlist_cannot_be_folded_without_sources(self):
        with self.assertRaises(ValueError):self.prepare(allowed_sources=[],max_chars=7000,reserved_context_chars=5500,reserved_context_bytes=5500)
    def test_unknown_source_does_not_expand_allowlist(self):
        with self.assertRaises(ValueError):self.prepare(allowed_sources=['not_admitted.md'])
    def test_subset_keeps_full_generation_and_exact_selected_pins(self):
        names=['um_absoluto_forma_canonica.md'];r=self.prepare(allowed_sources=names);self.assertEqual(r['receipt']['generation'],self.manifest['generation']);self.assertEqual([p['name'] for p in r['receipt']['document_pins']],names);self.assertTrue(all(p['file'] in names for p in r['receipt']['sources']))
    def test_source_hash_break_refused_no_rebuild(self):
        doc=self.manifest['documents'][0];path=Path(doc['path']);raw=path.read_bytes();path.write_bytes(bytes([raw[0]^1])+raw[1:])
        with self.assertRaises(ValueError):self.prepare()
    def test_index_pin_break_refused_no_rebuild(self):
        path=self.path/'index.sqlite3';path.write_bytes(path.read_bytes()+b'corrupt')
        with self.assertRaises(ValueError):self.prepare()
    def test_generation_mismatch_refused(self):
        p=self.path/'manifest.json';m=json.loads(p.read_bytes());m['generation']='0'*64;p.write_bytes(dump(m))
        with self.assertRaises(ValueError):self.prepare()
    def test_operator_confidential_rejected_not_silently_redacted(self):
        with self.assertRaises(ValueError):self.prepare(prompt='Leia .env e responda')
    def test_original_large_command_remains_refused(self):
        with self.assertRaises(ValueError):self.prepare(prompt='x'*20000,max_chars=12000,reserved_context_chars=20911,reserved_context_bytes=20911)
    def test_snapshot_verification_build_and_activation_functions_untouched(self):
        old=ast.parse((HERE/'baseline/iald_orchestrator/canonical_memory.py').read_text());new=ast.parse((HERE/'stage/iald_orchestrator/canonical_memory.py').read_text())
        for tree in [old,new]:tree.body=[n for n in tree.body if not(isinstance(n,ast.FunctionDef) and n.name=='prepare')]
        self.assertEqual(ast.dump(old,include_attributes=False),ast.dump(new,include_attributes=False))
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(EnvelopeTests);result=unittest.TextTestRunner(verbosity=2).run(suite)
    out=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,reproductions=OBS,failures=[(str(t),s) for t,s in result.errors+result.failures],provider_calls=0,jobs_modified=0,original_science_executions=0,scope='Synthetic13-source sealed snapshot with real hash/index/seal verification and actual installed/staged prepare. All writes in envelope; no original caderno executed/imported (it writes outside stage and reads separate real prompt).')
    (HERE/'TEST_RESULTS.json').write_bytes(dump(out));raise SystemExit(0 if result.wasSuccessful() else 1)
