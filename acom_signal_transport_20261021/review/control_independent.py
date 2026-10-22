from pathlib import Path
import hashlib, importlib.util, json, os, struct, sys, tempfile
W=Path(__file__).resolve().parents[1];R=W/'review/r1'
def audit(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'): raise RuntimeError('OFFLINE_ONLY')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
            if not Path(path).resolve().is_relative_to(R):raise RuntimeError('REVIEW_WRITES_ONLY')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('independent_signal',W/'prototype/acom_signal_codec.py');p=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p;spec.loader.exec_module(p)
results=[]
def record(name,passed,**details):results.append(dict(name=name,passed=bool(passed),**details))
ctx=p.Context('review','g1','conversation');root=Path(tempfile.mkdtemp(prefix='i_',dir=R));store=p.Store(root/'s')
def wire(id,raw):return list(p.encode(ctx,id,'query',p.slices(raw),declared_sha=p.sha(raw),declared_bytes=len(raw)))
for name,raw in [('empty',b''),('one_byte',b'\0'),('unicode_exact','é\r\ne\u0301\n\ufeff'.encode()),('all_bytes',bytes(range(256))),('max8MiB',b'\xff'*p.MAX_OBJECT)]:
    r=store.receive(ctx,wire(name,raw));record(name,Path(r['path']).read_bytes()==raw)
too_big=b'\0'*(p.MAX_OBJECT+1)
try: wire('over',too_big)
except p.Refusal as exc:record('over8MiB',True,error=str(exc))
else:record('over8MiB',False)
# Narrow fault injection at the documented durability boundary; no external calls.
payload=b'fault-injection-unique-block'*100;frames=wire('crash',payload)
rename=p.os.rename
class SimulatedCrash(Exception):pass
def stop_before_block_publish(src,dest):
    if Path(dest).parent.name=='blocks':raise SimulatedCrash('after fsync before rename')
    return rename(src,dest)
p.os.rename=stop_before_block_publish
try:store.receive(ctx,frames)
except SimulatedCrash:pass
finally:p.os.rename=rename
store.close();store=p.Store(root/'s')
try:
    r=store.receive(ctx,frames)
    record('recover_interrupted_block_publish',Path(r['path']).read_bytes()==payload)
except Exception as exc:
    record('recover_interrupted_block_publish',False,error_type=type(exc).__name__,error=str(exc),pending_block_files=len(list((root/'s'/ctx.key/'blocks').glob('*.tmp'))),request_committed=bool(store.db.execute('SELECT 1 FROM requests WHERE id=?',('crash',)).fetchone()))
store.close()
# Recount the measured packets with the measured request IDs, rather than 'counts'.
bench=json.loads((W/'benchmark_R3.json').read_bytes());repro=json.loads((R/'benchmark_R2.json').read_bytes())
stable=['fixture','raw_bytes','raw_sha256','gzip_bytes','zlib_bytes','zlib_json_envelope_bytes','candidates_bytes']
record('six_fixture_byte_counts_reproduced',all(all(a[k]==b[k] for k in stable) for a,b in zip(bench['rows'],repro['rows'])))
accounting=[]
for row in bench['rows']:
    for mode in ('cold','warm'):
        m=row['protocol'][mode]
        accounting.append(dict(fixture=row['fixture'],mode=mode,packet=m['binary_packet_bytes'],components=m['manifest_framing_bytes']+m['payload_bytes'],delta=m['binary_packet_bytes']-m['manifest_framing_bytes']-m['payload_bytes']))
record('packet_components_sum',all(x['delta']==0 for x in accounting),details=accounting)
out=R/'independent_checks.json';out.write_text(json.dumps({'checks':results,'network_calls':0,'provider_calls':0,'runtime_modified':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':len(results),'failed':[x for x in results if not x['passed']],'receipt':str(out)},ensure_ascii=False))
