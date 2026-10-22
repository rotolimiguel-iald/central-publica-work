"""Verify all core subtree ranges against the real checked corpus reader, offline."""
from pathlib import Path
import hashlib,json,os,sys,math
E=Path(__file__).resolve().parent;A=E.parent.parent;W=A.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
assert task.check('all_engines_admission',actor='codex-v394-app-builder')['ready']
sys.path[:0]=[str(A/'compat/staging'),str(R),str(A)]
from prepare_science import save,write,sha
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Offline recovery only')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Private source refused')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(E):raise RuntimeError('Write outside R2')
sys.addaudithook(guard)
from iald_core_indexado import DocumentCorpus
fixture=E/'fixtures/iald_nucleo_fixo.json';corpus=DocumentCorpus(fixture)
docs=corpus._load();manifest=json.loads((E/'manifest_pending_publication.json').read_bytes())
baseline=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
assert set(docs)=={x['id'] for x in baseline['entries']}
assert 'tgl_cluster_integral' not in docs
try:corpus.fetch('tgl_cluster_integral')
except ValueError:pass
else:raise AssertionError('Derived cluster exposed by DocumentCorpus')
doc=docs['resultado_publicado_integral'];text=doc['text'];decoder=json.JSONDecoder()
original=json.loads(text);records={}
def skip(i):
    while i<len(text) and text[i].isspace():i+=1
    return i
i=skip(0);assert text[i]=='{';i+=1
while True:
    i=skip(i);key,i=decoder.raw_decode(text,i);i=skip(i);assert text[i]==':';i=skip(i+1)
    if key=='core':
        assert text[i]=='{';i+=1
        while True:
            i=skip(i)
            if text[i]=='}':break
            name,i=decoder.raw_decode(text,i);i=skip(i);assert text[i]==':';start=skip(i+1)
            value,end=decoder.raw_decode(text,start)
            assert value==original['core'][name]
            assert json.loads(text[start:end])==original['core'][name]
            canonical=json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
            ptr='/core/'+name.replace('~','~0').replace('/','~1')
            records[name]={'source_id':'resultado_publicado_integral','json_pointer':ptr,
                'source_sha256':doc['sha256'],'offset_unicode_chars':start,'end_unicode_chars':end,
                'whole_subtree_chars':end-start,'canonical_value_sha256':sha(canonical),
                'minimum_pages_at_4500_chars':math.ceil((end-start)/4500),'all_descendant_fields_recovered_equal':True}
            i=skip(end)
            if text[i]==',':i+=1
            else:assert text[i]=='}';break
        break
    _,i=decoder.raw_decode(text,i);i=skip(i)
    assert text[i]==',';i+=1
assert set(records)==set(original['core']) and len(records)==422
projection_map=json.loads((E/'PROJECTION_MAP_R2.json').read_bytes())
for capsule in projection_map['capsules']:
    assert records[capsule['topic']]['canonical_value_sha256']==capsule['source_value_sha256']
sample_names=list(records)[::max(1,len(records)//3)]+[n for n in records if n.endswith('_v394')]
sample_pages=[]
for name in dict.fromkeys(sample_names):
    row=records[name]
    for offset in dict.fromkeys((row['offset_unicode_chars'],max(row['offset_unicode_chars'],row['end_unicode_chars']-4500))):
        page=corpus.fetch('resultado_publicado_integral',offset=offset,max_chars=4500)
        assert page['sha256']==doc['sha256'] and page['text']==text[offset:offset+4500]
        sample_pages.append({'topic':name,'offset':offset,'returned_chars':len(page['text']),'sha256':page['sha256']})
def pin(path):
    path=Path(path);raw=path.read_bytes();return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}
gaps={'scientific_core_fields_missing_from_result':[],
    'all_422_core_subtrees_and_descendants_recoverable':True,
    'representation_limits':[{
        'item':'Exact full derived-cluster Markdown serialization (headers, grouping, literal dictionary/codec layout)',
        'is_scientific_core_field':False,'recoverable_from_core_json_alone':False,
        'recovery':'Full derived Markdown remains byte-pinned locally; not a DocumentCorpus source; no URL or extra publication requested.'},{
        'item':'Canonical exposition embedded in the full-cluster Markdown',
        'is_scientific_core_field':False,'recoverable_from_core_json_alone':False,
        'recovery_source_id':'um_forma_canonica_integral','source_already_in_public_corpus':True,
        'recovery':'Use the existing canonical exposition entry; verify final v394 publication separately.'}],
    'public_v394_status':'NOT_VERIFIED_IN_THIS_OFFLINE_STAGE'}
assert 'um_forma_canonica_integral' in docs
write(E/'RECOVERY_MAP_R2.json',{'status':'ALL_422_CORE_SUBTREES_VERIFIED_COMPLETE',
    'source':{k:doc[k] for k in ('id','sha256','bytes')},'offset_units':'Unicode characters of DocumentCorpus UTF-8-sig decoded text',
    'pagination':'fetch_tgl(id=resultado_publicado_integral,offset=<offset_unicode_chars>,max_chars=4500); concatenate unchanged pages until end_unicode_chars.',
    'topics':records,'actual_fetch_sample_pages':sample_pages,'gaps':gaps,
    'fixture_urls_are_syntax_only_not_v394_publication':True,'network_calls':0})
testpath=E/'TEST_RESULTS_R2.json';tests=json.loads(testpath.read_bytes())
tests['tests'] += [{'name':n,'status':'PASS'} for n in (
    'DocumentCorpus_contains_only_original_public_source_ids',
    'derived_cluster_not_fetchable_or_required_as_public_entry',
    'all_422_original_core_subtrees_and_descendant_fields_exactly_recovered',
    'all_projection_pointers_match_original_core_subtree_hashes',
    'runtime_fetch_sample_pages_preserve_exact_text_offsets_and_source_hash',
    'non_JSON_markdown_representation_limits_declared_without_hiding_scientific_gap')]
tests['test_count']=len(tests['tests']);tests['recovery_map']=pin(E/'RECOVERY_MAP_R2.json');write(testpath,tests)
delivery_path=E/'DELIVERY_PREPARED_R2.json';delivery=json.loads(delivery_path.read_bytes())
delivery.update(status='PREPARED_R2_NO_DERIVED_PUBLICATION_DEPENDENCY',revision_label='R2',
    correction='Removed derived full-cluster DocumentCorpus entry; original public sources only. Full cluster local pinned; complete original core fields recovered through existing result JSON.',
    recovery_map=pin(E/'RECOVERY_MAP_R2.json'),recovery_verifier=pin(__file__),
    public_corpus_source_ids=sorted(docs),no_new_derived_publication_required=True,
    gaps=gaps,tests_passed=tests['test_count'],test_results=pin(testpath),
    r1_receipt_preserved=pin(E.parent/'DELIVERY_PREPARED_R1.json'))
write(delivery_path,delivery)
print(json.dumps({'status':delivery['status'],'core_topics_recovered':len(records),'scientific_core_gaps':0,
    'actual_fetch_pages_checked':len(sample_pages),'tests_passed':tests['test_count'],'public_entries':len(docs)}))
