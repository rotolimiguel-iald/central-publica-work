"""Read the current board once and preserve a bounded, non-authorizing snapshot."""
from pathlib import Path
import datetime, hashlib, json

ROOT=Path(__file__).resolve().parent
def main():
    source=Path(r'C:\IALD\PROGRAMA_IALD\PROGRAMA.json')
    raw=source.read_bytes()
    board=json.loads(raw)
    ids={'F3.1','F3.2','F3.3','F3.4','F3.5','F3.INTEGRACAO_20261019'}
    units=[{k:u.get(k) for k in ('id','titulo','status','gate','criterio_de_fechado')}
           for u in board['unidades'] if u['id'] in ids]
    if {u['id'] for u in units}!=ids:raise ValueError('MISSING_EXPECTED_BOARD_UNIT')
    pending=[p for p in board['pendencias_externas'] if p.get('id')=='X13']
    result={
        'schema':'iald.fase9.current-acts-audit/v1',
        'read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source':{'path':str(source),'sha256':hashlib.sha256(raw).hexdigest()},
        'units':units,'x13_entries':pending,
        'scope':'Current PROGRAMA.json only; not an exhaustive search of every operator act.',
        'interpretation':{
            'F3.4':'Read the resolved two-witness decision; do not ask again.',
            'X13':'This snapshot does not supply an authenticated ratification of executor deviations.',
            'D-H':'Documentary byte verification is not operator admission; no actual D-H act is supplied to this candidate.',
            'd72':'Keep the F3.5 operator gate and workload identity; no execution in this audit.',
            'opening':'Keep F3.3 separate from source admission and synthetic numerical qualification.'},
        'may_freeze':False,'may_open_observed_data':False,
        'scientific_statistic_generated':False,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=ROOT/'ACTS_SNAPSHOT_R3.json'
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'output':str(out),'unit_statuses':{u['id']:u['status'] for u in units},'x13_entries':len(pending)},ensure_ascii=False))

if __name__=='__main__':main()
