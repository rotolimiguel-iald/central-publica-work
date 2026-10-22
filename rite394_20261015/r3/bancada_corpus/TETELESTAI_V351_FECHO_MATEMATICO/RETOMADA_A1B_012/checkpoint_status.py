from pathlib import Path
import datetime, hashlib, json, os, sys
R=Path(__file__).resolve().parent
inp=(R/sys.argv[1]).resolve();assert inp.is_relative_to(R)
data=json.loads(inp.read_text(encoding='utf8'))
stamp=datetime.datetime.now().astimezone().isoformat()
suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b,memory=False):
    assert p.is_relative_to(R) and b
    if p.exists():
        assert memory
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+suffix)
        bak.write_bytes(old);assert bak.read_bytes()==old and len(b)>=len(old)
    t=p.with_name(p.name+'.tmp_'+suffix);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
record=dict(timestamp=stamp,input=pin(inp),status=data,
    receipts=[pin(p) for p in sorted(R.glob('RECIBO_DELTA_*.json'))],
    artifacts=[pin((R/p).resolve()) for p in data['artifacts']],
    full_trace_constructed=False,gate_changed=False)
p=R/('CHECKPOINT_STATUS_'+suffix+'.json');put(p,json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
text='\n\n## Adendo '+stamp+' — '+data['title']+'\n\n'+data['text']+'\n\nSnapshot: '+p.name+'. Este adendo corrige estados transitórios anteriores, preservados. Não repetir escritores de retratos históricos.\n'
md=R/'MEMORIA_RETOMADA_A1B_012.md';put(md,md.read_bytes()+text.encode('utf8'),True)
jp=R/'MEMORIA_RETOMADA_A1B_012.json';d=json.loads(jp.read_text(encoding='utf8'))
d.setdefault('append_only_checkpoints',[]).append(pin(p));put(jp,json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'),True)
print(json.dumps(dict(checkpoint=pin(p),memory=pin(md)),ensure_ascii=False))
