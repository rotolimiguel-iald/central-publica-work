"""Offline cross-runtime fixtures only. Does not import application code."""
import sys
sys.dont_write_bytecode=True
import base64,copy,hashlib,json,random,subprocess,time,zlib
from pathlib import Path
import chat_wire_codec as c
ROOT=Path(__file__).resolve().parent
FIX=ROOT/'fixtures';FIX.mkdir(exist_ok=True)
scope='synthetic_account_generation_17'
binding={'kind':'request','request_id':'synthetic_17','conversation':'conv17'}
page={'kind':'page','job_id':'job17','after':0}
results=[];bench=[]
def write(name,raw):
    (FIX/name).write_bytes(raw);return name
def record(name,fn):
    try:fn();results.append(dict(name=name,pass_=True))
    except Exception as e:results.append(dict(name=name,pass_=False,error=repr(e)))
def assert_(value):
    if not value:raise AssertionError()
def refuses(fn):
    try:fn()
    except c.WireError:return
    raise AssertionError('not refused')
request=c.dump(dict(account=scope,request_id='synthetic_17',iald_conv='conv17',stream=True,messages=[{'role':'user','content':'ação 😀 e\u0000 literal '+('texto íntegro\n'*3000)}]))
# Preserve exact whitespace, not just parsed JSON equality.
request=b' \n'+request+b'\t\r\n'
small=c.dump(dict(account=scope,request_id='synthetic_17',iald_conv='conv17',stream=True,messages=[]))
noise=random.Random(1729).randbytes(3*1024*1024)
attachments=c.dump(dict(account=scope,request_id='synthetic_17',iald_conv='conv17',stream=True,messages=[{'role':'user','content':[{'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(noise).decode()}},{'type':'document','data':base64.b64encode(b'%PDF synthetic\x00\xff'+noise[:1024]).decode()}]}]))
overhead=len(c.dump({'x':''}));at_limit=c.dump({'x':'a'*(c.REQUEST_LIMIT-overhead)})
page_large=c.dump({'x':'p'*(c.REQUEST_LIMIT+100)})
good=[]
for name,raw,b,limit in [('unicode',request,binding,c.REQUEST_LIMIT),('incompressible_multimegabyte',attachments,binding,c.REQUEST_LIMIT),('exact20MiB',at_limit,binding,c.REQUEST_LIMIT),('page_above20MiB',page_large,page,c.PAGE_LIMIT)]:
    t=time.perf_counter();env=c.encode_envelope(raw,scope,b,limit);packet=c.dump(env)
    bench.append(dict(case=name,operation='encode',ms=(time.perf_counter()-t)*1000,raw_bytes=len(raw),packet_bytes=len(packet)))
    good.append(dict(name=name,raw=write(name+'.raw',raw),packet=write('python_'+name+'.json',packet),binding=b,limit=limit))
    def check(raw=raw,env=env,b=b,limit=limit,name=name):
        t=time.perf_counter();out=c.decode_envelope(env,scope,b,limit);assert_(out==raw)
        bench.append(dict(case=name,operation='decode',ms=(time.perf_counter()-t)*1000,raw_bytes=len(raw)))
    record('python_roundtrip_'+name,check)
base=c.encode_envelope(request,scope,binding,c.REQUEST_LIMIT);bad=[]
def mutant(name,**updates):
    env=copy.deepcopy(base);env.update(updates);bad.append(dict(name=name,packet=write('bad_'+name+'.json',c.dump(env))))
mutant('wronghash',sha256='0'*64)
mutant('negative',raw_bytes=-1);mutant('bool_length',raw_bytes=True)
mutant('overbound',raw_bytes=c.REQUEST_LIMIT+1)
mutant('bomb',raw_bytes=2,data=base64.b64encode(zlib.compress(b'a'*2000000)).decode())
compressed=base64.b64decode(base['data'])
mutant('trailing',data=base64.b64encode(compressed+b'x').decode())
mutant('concatenated',data=base64.b64encode(compressed+compressed).decode())
mutant('truncated',data=base64.b64encode(compressed[:-1]).decode())
mutant('base64_whitespace',data=base['data']+'\n')
mutant('cross_scope',scope='other_generation')
mutant('replay_different_request',binding={**binding,'request_id':'different'})
mutant('wrong_binding_kind',binding=page)
mutant('unknown_field',extra=True)
mutant('wrong_codec',codec='gzip')
mutant('invalid_base64_padding',data='A===')
mutant('noncanonical_base64',data='Zh==')
for name,raw in [('inflated_duplicate',b'{"x":1,"x":2}'),('inflated_utf8',b'\xff')]:
    mutant(name,raw_bytes=len(raw),sha256=c.digest(raw),data=base64.b64encode(zlib.compress(raw)).decode())
for item in bad:
    env=json.loads((FIX/item['packet']).read_bytes())
    record('python_reject_'+item['name'],lambda env=env:refuses(lambda:c.decode_envelope(env,scope,binding,c.REQUEST_LIMIT)))
for name,raw in [('duplicate',b'{"x":1,"x":2}'),('utf8',b'\xff'),('nonfinite',b'1e999'),('trailingjson',b'{}x'),('deep',b'['*130+b'0'+b']'*130)]:
    record('python_json_'+name,lambda raw=raw:refuses(lambda:c.strict_json(raw,c.REQUEST_LIMIT)))
record('python_over_20MiB',lambda:refuses(lambda:c.strict_json(at_limit+b' ',c.REQUEST_LIMIT)))
record('python_nonobject_request',lambda:refuses(lambda:c.request_candidate(b'[]',scope)))
record('python_no_gain_identity',lambda:assert_(c.request_candidate(small,scope)==small))
record('python_incompressible_identity',lambda:assert_(c.request_candidate(attachments,scope)==attachments))
record('python_request_exact',lambda:assert_(c.decode_request(c.request_candidate(request,scope),scope)[0]==request))
pe=copy.deepcopy(c.encode_envelope(request,scope,page,c.PAGE_LIMIT));pe['binding']['after']=True
record('python_bool_cursor_rejected',lambda:refuses(lambda:c.decode_envelope(pe,scope,{'kind':'page','job_id':'job17','after':1},c.PAGE_LIMIT)))
spec=dict(scope=scope,binding=binding,good=good,bad=bad,request_raw=write('request.raw',request),small_raw=write('small.raw',small),incompressible_request='incompressible_multimegabyte.raw')
write('cases.json',c.dump(spec))
node=subprocess.run([r'C:\Program Files\nodejs\node.exe',str(ROOT/'node_tests.mjs'),str(FIX)],capture_output=True,text=True,timeout=180)
node_report=json.loads((FIX/'node_results.json').read_bytes()) if (FIX/'node_results.json').exists() else {'results':[],'bench':[]}
for item in good:
    def check(item=item):
        env=json.loads((FIX/('node_'+item['name']+'.json')).read_bytes());raw=(FIX/item['raw']).read_bytes()
        t=time.perf_counter();assert_(c.decode_envelope(env,scope,item['binding'],item['limit'])==raw)
        bench.append(dict(case=item['name'],operation='decode_node_packet',ms=(time.perf_counter()-t)*1000,raw_bytes=len(raw)))
    record('Node_to_Python_'+item['name'],check)
all_ok=all(r['pass_'] for r in results) and all(r['pass'] for r in node_report['results']) and node.returncode==0
receipt=dict(status='PASS' if all_ok else 'FAIL',python=sys.version,node=node_report.get('node'),python_tests=results,node_tests=node_report['results'],node_exit=node.returncode,node_stderr=node.stderr,network_calls=0,application_imports=0,byte_equality_cross_runtime=True if all_ok else None)
(ROOT/'TEST_RESULTS.json').write_bytes(c.dump(receipt))
(ROOT/'CPU_BENCHMARK.json').write_bytes(c.dump(dict(status='REAL_LOCAL_SINGLE_RUN',python=bench,node=node_report['bench'],notes=['Wall clock includes JSON validation, hashing, base64 and compression/decompression. Not a network or browser-device benchmark.','Complete envelope byte counts include JSON manifest and base64; no cache/base/delta.','Same-binding replay remains the existing ChatJobs canonical idempotency responsibility. Cross-binding replay rejected here.'])))
print(json.dumps(dict(status=receipt['status'],python_tests=len(results),node_tests=len(node_report['results']),failures=[r for r in results if not r['pass_']]+[r for r in node_report['results'] if not r['pass']],node_stderr=node.stderr)))
sys.exit(0 if all_ok else 1)
