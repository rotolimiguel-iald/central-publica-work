"""Prepare append-only memory payload/plan from pinned final receipts. NEVER applies.

Only CLI writes are new artifacts inside this directory. Original finish_memory.py
is read as provenance, never imported (it applies changes at module top level).
"""
import argparse,datetime,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
W=HERE.parent
MARKER='IALD_SIGNAL_TRANSPORT_20261021_FINAL'
ROLES=('deployment','live','mobile')
MOBILE_FIELDS=('web','ios_internal','ios_external','android','google_play')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def load(path):return json.loads(Path(path).read_bytes().decode('utf-8'))
def scalar(value,label):
    require(type(value) in (str,int,float,bool),label+': scalar required')
    value=str(value)
    require(0<len(value)<=500 and not any(ord(c)<32 for c in value),label+': invalid scalar')
    return json.dumps(value,ensure_ascii=False) # quoted receipt content, no prose injection
def pinned(pin):
    require(isinstance(pin,dict) and isinstance(pin.get('path'),str),'receipt path required')
    require(re.fullmatch('[a-f0-9]{64}',pin.get('sha256','')) is not None,'measured receipt sha256 required')
    p=Path(pin['path']).resolve();require(p.is_file(),'missing final receipt: '+str(p))
    raw=p.read_bytes();require(sha(raw)==pin['sha256'],'receipt pin mismatch: '+str(p))
    require(0<len(raw)<=16*1024*1024,'receipt size bound')
    obj=json.loads(raw.decode('utf-8'));require(isinstance(obj,dict),'receipt object required')
    return obj,dict(path=str(p),sha256=sha(raw),bytes=len(raw))
def validate(inputs):
    require(inputs.get('final_snapshot') is True,'parent must identify the FINAL deployment/live/mobile snapshots; no inference from latest filename')
    receipts={};pins=[]
    for role in ROLES:
        require(role in inputs.get('receipts',{}),'missing final receipt role: '+role)
        obj,pin=pinned(inputs['receipts'][role]);require('status' in obj,role+': status required')
        scalar(obj['status'],role+'.status');receipts[role]=obj;pins.append(dict(role=role,**pin))
    mobile=receipts['mobile'];matrix=mobile.get('availability',mobile)
    require(isinstance(matrix,dict),'mobile availability object required')
    for k in MOBILE_FIELDS:
        require(k in matrix,'missing explicit availability '+k);scalar(matrix[k],k)
    require(type(matrix.get('physical_installation_verified')) is bool,'physical installation must be explicit boolean')
    return receipts,pins,matrix
def render(receipts,pins,matrix):
    date=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    rows=['','',f'## {date} — Transporte do app e disponibilidade observada',f'<!-- {MARKER} -->',
      '[INPUT] Unidade F9.ACOM_SIGNAL_TRANSPORT_20261021. Registro operacional; não altera ciência, kernel, selo ou gate.',
      '[REAL — engenharia / escopo] A camada do app implementa transporte UTF-8/deflate sem perdas, hash e negociação; não é o controle de átomo luminídico. Esse controle continua experimental e não se declara implantado por este registro. Não se infere redução de tokens do modelo nem ganho de latência a partir da compressão.',
      '[DECLARADO — recibos finais pinados] Implantação: '+scalar(receipts['deployment']['status'],'deployment.status')+'; validação live: '+scalar(receipts['live']['status'],'live.status')+'; entrega mobile: '+scalar(receipts['mobile']['status'],'mobile.status')+'. Os estados abaixo não equivalem a todos os canais atualizados ou instalação física.',
      '| Superfície | Estado literal do recibo |','|---|---|']
    for k in MOBILE_FIELDS:rows.append('| '+k+' | '+scalar(matrix[k],k).replace('|','\\|')+' |')
    rows.append('[DECLARADO] Instalação física: '+('verificada no recibo.' if matrix['physical_installation_verified'] else 'não verificada; build/publicação/distribuição não comprovam instalação no aparelho.'))
    for key in ('pending','limitations','pendencias'):
        if key in receipts['mobile']:
            v=receipts['mobile'][key];require(isinstance(v,list) and len(v)<=30,'pending/limitations list required')
            for item in v:rows.append('[OPEN — recibo mobile] '+scalar(item,key))
    rows.append('[EVIDÊNCIAS] '+'; '.join(p['role']+': '+p['path']+' SHA256 '+p['sha256'] for p in pins)+'. Referência: '+str(W/'SESSION_REFERENCE.json')+'.')
    rows+=['<!-- END_'+MARKER+' -->','']
    return '\n'.join(rows).encode('utf-8')
def new(path,raw):
    p=Path(path).resolve();require(p.is_relative_to(HERE.resolve()),'output must stay in memory_prepare')
    with p.open('xb') as f:f.write(raw)
    require(p.read_bytes()==raw,'output mismatch')
def prepare(inputs,outname):
    receipts,pins,matrix=validate(inputs) # Missing receipt => NO output plan/text.
    surfaces=load(HERE/'SURFACES.json')['surfaces']
    out=(HERE/outname).resolve();require(out.parent==HERE and not out.exists(),'fresh direct child output directory required')
    chunk=render(receipts,pins,matrix);items=[]
    for row in surfaces:
        p=Path(row['path']);require(p.name.upper()!='MEMORY.MD','MEMORY index must not receive diary')
        before=p.read_bytes();require(MARKER.encode() not in before,'already present: '+str(p))
        items.append(dict(path=str(p),role=row['role'],before_sha256=sha(before),before_bytes=len(before),expected_after_sha256=sha(before+chunk),expected_after_bytes=len(before)+len(chunk),operation='APPEND_ONLY_NOT_APPLIED',backup_plan='Raw bytes in SAME directory: <name>.bak_<UTCmicroseconds>_<unique>; verify before any replacement; keep backup.',application_guard='Parent fresh unit/mission preflight + independent review and recheck ALL source/receipt/target pins; helper never invoked by preparer. Each replacement atomic, whole set is not one transaction.'))
    out.mkdir();new(out/'APPEND.txt',chunk)
    plan=dict(status='PREPARED_NOT_APPLIED_REQUIRES_FRESH_PARENT_REVIEW',marker=MARKER,reference=str(W/'SESSION_REFERENCE.json'),receipts=pins,append=dict(path=str(out/'APPEND.txt'),sha256=sha(chunk),bytes=len(chunk)),surfaces=items,board_route_included=False)
    new(out/'PLAN.json',(json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode())
    delivery=dict(status='FINAL_RECEIPT_SUMMARY_NOT_MEMORY_APPLIED',reference=str(W/'SESSION_REFERENCE.json'),sources=pins,observed_receipt_statuses={r:receipts[r]['status'] for r in ROLES},availability=matrix,transport='UTF8/deflate lossless; no token/latency gain inferred',luminidic_control='experimental only; no deployment inferred',memory_applied=False,board_updated=False,route_updated=False)
    new(out/'DELIVERY_FROM_RECEIPTS.json',(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n').encode())
    return plan
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--inputs',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args()
    try:
        plan=prepare(load(args.inputs),args.out);print(json.dumps(dict(status=plan['status'],surfaces=len(plan['surfaces']))))
    except Exception as e:
        print(json.dumps(dict(status='REFUSED_NOT_APPLIED',error=str(e)),ensure_ascii=False));sys.exit(2)
