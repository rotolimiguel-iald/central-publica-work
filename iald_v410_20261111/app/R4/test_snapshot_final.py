"""Engineering checks only: identity, recovery and capacity; no provider calls."""
from pathlib import Path
import ast,hashlib,json,sys,time
R=Path(__file__).resolve().parent
sys.path.insert(0,r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(R/'runtime'))
from iald_science_snapshot import ScienceSnapshot
results=[]
def check(name, fn):
    fn();results.append({'name':name,'passed':True})
def require(value):
    if not value:raise AssertionError('Check failed')
def rejected(fn):
    try:fn()
    except (ValueError,KeyError):return
    raise AssertionError('Expected visible refusal')
start=time.monotonic();snap=ScienceSnapshot.capture(R/'release_final/release.json')
check('whole_core_bounded',lambda:require(0<len(snap.prefix.encode())<150000))
check('jev_same_version',lambda:require(snap.routing_memory()[1]['release']==snap.identity['release']))
check('kernel_same_version',lambda:require(snap.catalog.source_sha==snap.identity['source_sha256']))
check('no_match_not_absence',lambda:require(snap.search('xyzzyunknown999')['zero_matches_proves_absence'] is False))
check('unregistered_source_refused',lambda:rejected(lambda:snap.fetch('../../secret')))
check('invalid_page_refused',lambda:rejected(lambda:snap.fetch('resultado_publicado_integral',-1)))
check('legacy_private_atlas_not_read',lambda:require(snap.execute_tool('iald_atlas_read',{'start_line':1})['status']=='UNAVAILABLE_USE_VERSIONED_SEARCH_TGL'))
# All original documents round-trip, including UTF8 and exact newline text.
for ident,doc in snap._documents.items():
    chunks=[];offset=0
    while True:
        page=snap.fetch(ident,offset,50000);chunks.append(page['text'])
        if page['next_offset'] is None:break
        offset=page['next_offset']
    require(hashlib.sha256(''.join(chunks).encode()).hexdigest()==doc['sha256'])
results.append({'name':'all_documents_paginate_exact_raw_utf8','passed':True,'documents':len(snap._documents)})
queries=[]
for query in ('Explique a identidade da IALD','Qual o estatuto de H3?','Articule a solução matemática da gravidade quântica'):
    retrieved=snap.pre_retrieve([{'role':'user','content':query}])
    require(len(retrieved['prompt'].encode())<=120000)
    require(all(u['whole_unit'] for u in retrieved['receipt']['units']))
    queries.append({'query':query,'bytes':len(retrieved['prompt'].encode()),'ids':retrieved['receipt']['source_ids'],
                    'excluded':retrieved['receipt']['budget_excluded_unit_ids']})
results.append({'name':'whole_optional_units_with_explicit_budget_exclusions','passed':True})
check('mandatory_overflow_refused',lambda:rejected(lambda:snap.pre_retrieve([{'role':'user','content':'fetch_tgl resultado_publicado_integral 0'}],max_bytes=100)))
continued=snap.pre_retrieve([{'role':'user','content':'fetch_tgl resultado_publicado_integral 12000'}])
check('kimi_explicit_continuation',lambda:require(continued['receipt']['units'][-1]['offset']==12000))
# Swap only a fixture active pointer. Existing snapshot cannot consult the replacement.
active=R/'fixture_active_final.json';raw=json.dumps({'science_snapshot':{'path':str(snap.manifest_path),'sha256':snap.manifest_sha256}}).encode()
if active.exists():raise ValueError('Fixture already exists; preserve test run')
active.write_bytes(raw)
pinned=ScienceSnapshot.capture(active);active.write_bytes(b'{"schema":"invalid-new-active"}')
check('concurrent_active_switch_old_call_pinned',lambda:require(pinned.fetch('um_selo_publicado_integral')['identity']==snap.check()))
check('new_call_corrupt_active_refused',lambda:rejected(lambda:ScienceSnapshot.capture(active)))
for p in (R/'runtime').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
results.append({'name':'runtime_syntax','passed':True})
out={'status':'PASS_ENGINEERING_ONLY','identity':snap.check(),'checks':results,'queries':queries,
     'elapsed_seconds':time.monotonic()-start,'new_provider_calls':0,
     'limitations':['Lexical selection is not proof of semantic completeness or answer quality.',
                    'Cross-source hypotheses and errata require explicit retrieval; no scientific validation.',
                    'These tests do not validate server integration or deployment.']}
path=R/'SNAPSHOT_TESTS_FINAL.json'
with path.open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(json.dumps({'status':out['status'],'checks':len(results),'queries':queries},ensure_ascii=False))
