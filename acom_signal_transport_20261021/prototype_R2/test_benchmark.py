"""Offline synthetic benchmark/adversaries. Outputs only measurements, no source data."""
import sys,os,io,json,ast,struct,zlib,gzip,hashlib,random,time,statistics,tempfile,base64,tracemalloc,copy
from pathlib import Path
from dataclasses import dataclass
S=Path(__file__).resolve().parent;W=S.parent/'control_run_R2';W.mkdir(exist_ok=False)
sys.dont_write_bytecode=True
def audit(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_DENIED')
    if event=='open':
        p,mode,flags=args
        if isinstance(p,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if not Path(p).resolve().is_relative_to(W):raise RuntimeError('WRITE_OUTSIDE_MISSION_DENIED')
sys.addaudithook(audit)
import acom_signal_codec as p

def save(name,value):
    raw=json.dumps(value,ensure_ascii=False,indent=2).encode()
    with (W/name).open('xb') as f:f.write(raw)
    assert (W/name).read_bytes()==raw
def same_file(path,raw):
    with Path(path).open('rb') as f:
        for i in range(0,len(raw),p.BLOCK):
            if f.read(p.BLOCK)!=raw[i:i+p.BLOCK]:return False
        return f.read(1)==b''
def decode(ctx,store,frames,**kw):return store.receive(ctx,iter(frames),**kw)
def frames(ctx,id,raw,**kw):return list(p.encode(ctx,id,'query',p.slices(raw),**kw))
def headers(frames):
    out=[]
    for frame in frames:
        n=struct.unpack('!I',frame[:4])[0];out.append((json.loads(frame[4:4+n]),frame[4+n:]))
    return out
def altered(frames,index,**changes):
    pairs=headers(frames);h,body=pairs[index];h.update(changes);pairs[index]=(h,body)
    return [p.pack(h,body) for h,body in pairs]
checks={};errors={}
def check(name,condition):
    checks[name]=bool(condition)
    if not condition:raise AssertionError(name)
def denied(name,fn,classes=(p.Refusal,)):
    try:fn()
    except classes as exc:checks[name]=True;errors[name]=str(exc)
    else:raise AssertionError('NOT REFUSED: '+name)

root=Path(tempfile.mkdtemp(prefix='s',dir=W));store=p.Store(root/'store')
a=p.Context('alice','g1','c1');bob=p.Context('bob','g1','c1');revoked=p.Context('alice','g2','c1');other=p.Context('alice','g1','c2')
raw=('Comando íntegro: ação, revisão e decisão.\r\n'*2000).encode()+bytes(range(256))
wire=frames(a,'first',raw,declared_sha=p.sha(raw),declared_bytes=len(raw));receipt=decode(a,store,wire)
check('cold_byte_equality',same_file(receipt['path'],raw))
offer=store.offer(a,receipt['root']);warm=frames(a,'warm',raw,known=offer)
wr=decode(a,store,warm);check('warm_byte_equality',same_file(wr['path'],raw))
check('warm_all_references',all(h['codec']=='ref' for h,b in headers(warm)[1:-1]))
check('warm_smaller_than_cold',sum(map(len,warm))<sum(map(len,wire)))
again=decode(a,store,warm,on_block=lambda *args:(_ for _ in ()).throw(AssertionError('Replay emitted twice')))
check('exact_replay_no_dispatch',again['replayed'] and not again['dispatch_allowed'])
store.close();store=p.Store(root/'store')
check('replay_ledger_survives_reopen',decode(a,store,warm)['replayed'])
denied('changed_request_identity',lambda:decode(a,store,frames(a,'first',raw,declared_sha=None)))
denied('changed_request_payload',lambda:decode(a,store,frames(a,'warm',raw+b'x')),classes=(p.Conflict,))
for name,ctx in [('cross_account',bob),('revoked_generation',revoked),('cross_conversation',other)]:
    denied(name,lambda ctx=ctx:decode(ctx,store,wire))
    denied(name+'_base_offer',lambda ctx=ctx:store.offer(ctx,receipt['root']),classes=(p.MissingBase,))
denied('unauthenticated',lambda:decode(p.Context('alice','g1','c1',False),store,wire))
denied('csrf_missing',lambda:decode(p.Context('alice','g1','c1',True,False),store,wire))
check('cross_scope_no_objects',store.db.execute('SELECT count(*) FROM objects WHERE scope=?',(bob.key,)).fetchone()[0]==0)
denied('unknown_base',lambda:decode(a,store,altered(warm,0,base='f'*64)),classes=(p.MissingBase,))
denied('reference_without_negotiation',lambda:decode(a,store,altered(warm,0,base=None)))
denied('bad_scope_in_header',lambda:decode(a,store,altered(wire,0,scope=bob.key)))
denied('bad_hash',lambda:decode(a,store,altered(wire,1,sha='0'*64)))
denied('bad_offset',lambda:decode(a,store,altered(wire,1,offset=1)))
denied('bad_sequence',lambda:decode(a,store,altered(wire,1,n=9)))
denied('bad_block_raw_length',lambda:decode(a,store,altered(wire,1,bytes=p.BLOCK+1)))
denied('bad_wire_length',lambda:decode(a,store,altered(wire,1,wire=p.BLOCK+129)))
denied('unknown_codec',lambda:decode(a,store,altered(wire,1,codec='q8amp')))
denied('bad_object_hash',lambda:decode(a,store,altered(wire,-1,sha='0'*64)))
denied('bad_manifest_root',lambda:decode(a,store,altered(wire,-1,root='0'*64)))
denied('bad_total_bytes',lambda:decode(a,store,altered(wire,-1,bytes=len(raw)+1)))
denied('duplicate_data_frame',lambda:decode(a,store,wire[:2]+wire[1:]))
denied('truncated_payload',lambda:decode(a,store,[wire[0],wire[1][:-1]]))
denied('missing_end',lambda:decode(a,store,wire[:-1]))
denied('trailing_body',lambda:decode(a,store,wire+[b'x']))
denied('oversized_header',lambda:decode(a,store,[struct.pack('!I',p.MAX_HEADER+1)]))
denied('huge_network_chunk',lambda:decode(a,store,[b'x'*(p.BLOCK+4097)]))
denied('duplicate_json_key',lambda:decode(a,store,[struct.pack('!I',len(b'{"t":"begin","t":"end"}'))+b'{"t":"begin","t":"end"}']))
denied('decompression_bomb_length_before_inflate',lambda:p.unacom1(p.MAGIC+struct.pack('<QI',p.BLOCK+1,0)+b'0'*32+zlib.compress(b'x'*(p.BLOCK+1))))
small=p.acom1(b'abc')
denied('trailing_zlib_member',lambda:p.unacom1(small+zlib.compress(b'abc')))
denied('truncated_zlib',lambda:p.unacom1(small[:-1]))
denied('corrupt_acom_crc',lambda:p.unacom1(small[:14]+b'xxxx'+small[18:]))
denied('corrupt_acom_payload',lambda:p.unacom1(small[:-2]+b'xx'))
denied('declared_over_limit_before_body',lambda:decode(a,store,altered(wire,0,bytes=p.MAX_OBJECT+1)))
before=store.db.execute('SELECT count(*) FROM requests').fetchone()[0]
denied('bad_end_no_commit',lambda:decode(a,store,altered(frames(a,'no-commit',raw),-1,sha='f'*64)))
check('bad_end_no_new_request',store.db.execute('SELECT count(*) FROM requests').fetchone()[0]==before)
check('failed_transfer_temp_cleaned',not list((root/'store'/a.key/'pending').iterdir()))
# A negotiated manifest can outlive an evicted block. Explicit cold repair only.
block_hash=offer['blocks'][0];cache=store._path(a,'blocks',block_hash);original=cache.read_bytes();cache.unlink()
denied('warm_missing_block',lambda:decode(a,store,frames(a,'repair',raw,known=offer)),classes=(p.MissingBase,))
repair=decode(a,store,frames(a,'repair',raw));check('explicit_cold_after_refusal',same_file(repair['path'],raw))
backup=cache.with_suffix('.bak_corrupt_test');backup.write_bytes(original);cache.write_bytes(b'bad')
denied('cached_block_corrupt',lambda:decode(a,store,frames(a,'corrupt-cache',raw,known=offer)))
cache.write_bytes(original)
# Arbitrary network fragmentation, not just complete frame iteration.
chunked=(part[i:i+7] for part in frames(a,'fragmented',raw) for i in range(0,len(part),7))
check('fragmented_network_roundtrip',same_file(decode(a,store,chunked)['path'],raw))
# A response transfer completes on a validated end frame, without waiting for EOF.
stream_frames=frames(a,'streaming',raw);seen=[]
def stream_source():
    yield from stream_frames
    raise AssertionError('Decoder waited for EOF after terminal frame')
streamed=store.receive(a,stream_source(),on_block=lambda data,index:seen.append((index,len(data))),require_eof=False)
check('stream_end_without_eof',same_file(streamed['path'],raw) and len(seen)>1)
check('bounded_reader',streamed['reader_peak']<=2*(p.BLOCK+4096))
# Pure ACOM1 functions selected by AST: no NumPy/Torch or module side effects.
codec_source=Path(r'C:\IALD\projetos_pyhton\IALD\iald_web\app\patents\acom_codec.py')
tree=ast.parse(codec_source.read_bytes());names={'AcomIntegrityError','AcomResult','compress','decompress'}
nodes=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
ns=dict(dataclass=dataclass,hashlib=hashlib,struct=struct,time=time,zlib=zlib,MAGIC=p.MAGIC,_CRC=zlib.crc32)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(codec_source),'exec'),ns)
for name,data in [('text',b'abc'*10000),('random',random.Random(12).randbytes(p.BLOCK))]:
    check('acom1_new_decoder_old_encoder_'+name,p.unacom1(ns['compress'](data).container)==data)
    check('acom1_old_decoder_new_encoder_'+name,ns['decompress'](p.acom1(data))==data)
save('prototype_tests_R2.json',{'status':'PASS','checks':checks,'count':len(checks),'refusals':errors,'provider_calls':0,'network_calls':0,'scope_note':'Context flags are synthetic trusted-server adapter decisions; no real authentication/CSRF implementation claimed.','acom1_source':{'path':str(codec_source),'sha256':p.sha(codec_source.read_bytes())}})

# Synthetic fixtures: valid byte PNG/PDF plus messages/text/random; not user files.
rng=random.Random(4729)
def png():
    width,height=384,256
    def chunk(kind,data):return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
    scan=b''.join(b'\0'+rng.randbytes(width*3) for _ in range(height))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(scan))+chunk(b'IEND',b'')
def pdf():
    content=zlib.compress((b'BT /F1 12 Tf 30 700 Td (Synthetic transport benchmark) Tj ET\n')*4000)
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',b'<< /Length '+str(len(content)).encode()+b' /Filter /FlateDecode >>\nstream\n'+content+b'\nendstream']
    raw=b'%PDF-1.4\n';offsets=[0]
    for i,obj in enumerate(objects,1):offsets.append(len(raw));raw+=str(i).encode()+b' 0 obj\n'+obj+b'\nendobj\n'
    xref=len(raw);raw+=b'xref\n0 6\n0000000000 65535 f \n'+b''.join(f'{n:010d} 00000 n \n'.encode() for n in offsets[1:]);return raw+b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n'+str(xref).encode()+b'\n%%EOF\n'
image=png();messages=json.dumps({'messages':[{'role':'user' if i%2==0 else 'assistant','content':f'Mensagem íntegra {i}: ação e revisão. '+('Conservar todos os caracteres, números e decisões. '*60)} for i in range(160)]},ensure_ascii=False).encode()
fixtures={'messages_json':messages,'text_utf8':('ação; texto completo; requisito; revisão.\r\n'*20000).encode(),'png_raw':image,'pdf_raw':pdf(),'random_raw':rng.randbytes(1024*1024),'messages_png_base64':json.dumps({'messages':[{'role':'user','content':[{'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(image).decode()}}]}]},separators=(',',':')).encode()}
rows=[]
def envelope_size(packet):
    return len(p.canonical({'iald_transport':{'protocol':p.PROTOCOL,'encoding':'base64-frames','data':base64.b64encode(packet).decode()}}))
for name,body in fixtures.items():
    # Base is a real prior transfer of the exact prefix, not free pre-shared data.
    prefix=body[:(len(body)//p.BLOCK)*p.BLOCK] or body
    sr=p.Store(root/('b'+str(len(rows))));base_id='base_'+name
    base_packet=b''.join(p.encode(a,base_id,'attachment',p.slices(prefix),declared_sha=p.sha(prefix),declared_bytes=len(prefix)))
    seed=sr.receive(a,p.slices(base_packet));known=sr.offer(a,seed['root'])
    samples=[];measure={}
    for mode in ('cold','warm'):
        times=[];encode_times=[];decode_times=[];peaks=[]
        for k in range(3):
            request=f'{name}_{mode}_{k}';t0=time.perf_counter()
            measured_frames=list(p.encode(a,request,'attachment',p.slices(body),known=known if mode=='warm' else None,declared_sha=p.sha(body),declared_bytes=len(body)))
            packet=b''.join(measured_frames)
            t1=time.perf_counter();tracemalloc.start()
            receipt=sr.receive(a,p.slices(packet));_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();t2=time.perf_counter()
            assert same_file(receipt['path'],body)
            encode_times.append((t1-t0)*1000);decode_times.append((t2-t1)*1000);times.append((t2-t0)*1000);peaks.append(peak)
        hs=headers(measured_frames)
        metadata=sum(len(frame)-len(data) for frame,(h,data) in zip(measured_frames,hs))
        assert metadata+sum(len(data) for h,data in hs)==len(packet)
        capabilities=p.canonical({'transport':p.PROTOCOL,'scope':a.key,'bases':[known['root']] if mode=='warm' else []})
        # Conservative negotiation includes full offered block list; optimized
        # session root-only advert is reported separately and never hidden.
        offer_bytes=len(p.canonical(known)) if mode=='warm' else 0
        measure[mode]={'binary_packet_bytes':len(packet),'json_packet_bytes':envelope_size(packet),'manifest_framing_bytes':metadata,'payload_bytes':sum(len(data) for h,data in hs),'capabilities_bytes':len(capabilities),'full_offer_manifest_bytes':offer_bytes,'total_binary_plus_full_offer_bytes':len(packet)+len(capabilities)+offer_bytes,'total_json_plus_full_offer_bytes':envelope_size(packet)+len(capabilities)+offer_bytes,'encode_ms_median':statistics.median(encode_times),'decode_spool_sqlite_ms_median':statistics.median(decode_times),'total_cpu_io_ms_median':statistics.median(times),'decoder_peak_python_bytes':max(peaks),'reference_blocks':sum(h.get('codec')=='ref' for h,data in hs),'data_blocks':sum(h.get('t')=='block' and h.get('codec')!='ref' for h,data in hs)}
    gzip_times=[];zlib_times=[]
    for k in range(3):
        t0=time.perf_counter();gz=gzip.compress(body,compresslevel=6,mtime=0);gzip.decompress(gz);gzip_times.append((time.perf_counter()-t0)*1000)
        t0=time.perf_counter();zz=zlib.compress(body,6);zlib.decompress(zz);zlib_times.append((time.perf_counter()-t0)*1000)
    zenv=p.canonical({'iald_transport':{'protocol':'iald-byte-envelope/1','encoding':'zlib','raw_bytes':len(body),'sha256':p.sha(body),'data':base64.b64encode(zz).decode()}})
    # Minimum savings after EVERYTHING on that hop: conservative 5% AND 1024 B.
    candidates={'identity':len(body),'gzip_http':len(gz),'zlib_json':len(zenv),'blocks_json_cold':measure['cold']['total_json_plus_full_offer_bytes'],'blocks_json_warm':measure['warm']['total_json_plus_full_offer_bytes']}
    eligible={k:v for k,v in candidates.items() if k=='identity' or len(body)-v>=max(1024,int(len(body)*.05))}
    selection=min(eligible,key=eligible.get)
    setup_bytes=len(base_packet)+len(p.canonical(known))
    # DERIVED link serialization only; no network timing or provider latency measured.
    transfer={str(mbps):{k:round(v*8/(mbps*1_000_000)*1000,3) for k,v in candidates.items()} for mbps in (2,10,50)}
    rows.append({'fixture':name,'raw_bytes':len(body),'raw_sha256':p.sha(body),'gzip_bytes':len(gz),'zlib_bytes':len(zz),'zlib_json_envelope_bytes':len(zenv),'gzip_roundtrip_ms_median':statistics.median(gzip_times),'zlib_roundtrip_ms_median':statistics.median(zlib_times),'protocol':measure,'base_setup_wire_bytes':setup_bytes,'warm_total_including_base_setup':setup_bytes+measure['warm']['total_json_plus_full_offer_bytes'],'warm_amortized_total_bytes_per_request':{str(n):round(setup_bytes/n+measure['warm']['total_json_plus_full_offer_bytes'],1) for n in (1,2,10)},'worst_case_evicted_base_plus_manual_full_bytes':measure['warm']['total_json_plus_full_offer_bytes']+measure['cold']['total_json_plus_full_offer_bytes'],'selection_5percent_1024B':selection,'candidates_bytes':candidates,'derived_serialization_ms_at_Mbps':transfer})
    sr.close()
save('benchmark_R2.json',{'status':'MEASURED_SYNTHETIC_LOCAL_NOT_NETWORK','rows':rows,'runs_per_case':3,'include_costs':['all frame headers/manifests/end/root','binary and JSON-base64 packet','capability advert','conservative full base offer','real prior cold base setup','amortization','missing-base wasted transfer plus explicit cold resend'],'timing_limits':['gzip/zlib CPU only versus protocol encode + local spool/SQLite: reported separately, not equal endpoints.','Packet bytes include protocol metadata; HTTP/TLS framing and auth headers not measured.','Buffers holding fixture and complete packet are benchmark instrumentation; receiver decoder uses bounded Reader + disk spool.','Derived 2/10/50Mbps are link serialization estimates, not measured latency, CPU savings, TTFB or model speed.'],'network_calls':0,'provider_calls':0})
store.close()
print(json.dumps({'tests':'PASS','checks':len(checks),'fixtures':len(rows),'summary':[{'fixture':v['fixture'],'raw':v['raw_bytes'],'gzip':v['gzip_bytes'],'cold_json':v['protocol']['cold']['total_json_plus_full_offer_bytes'],'warm_json':v['protocol']['warm']['total_json_plus_full_offer_bytes'],'selected':v['selection_5percent_1024B']} for v in rows]}))
