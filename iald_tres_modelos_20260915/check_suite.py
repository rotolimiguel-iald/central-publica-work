import hashlib
import json
from pathlib import Path
import re
from datetime import datetime
WORK=Path(__file__).resolve().parent
def read(name):
    data=(WORK/name).read_bytes()
    text=data.decode('utf-16') if data[:2] in (b'\xff\xfe',b'\xfe\xff') else data.decode('utf-8-sig')
    rows={}
    for match in re.finditer(r'^\s*(XX)?\s*(test_[a-z_]+\.(?:py|mjs))\s+(.+)$',text,re.M):
        fail,name,result=match.groups()
        rows[name]={'failed':bool(fail),'result':result.strip()}
    return rows,text,hashlib.sha256(data).hexdigest()
before,_,before_hash=read('suite_before.log')
after,text,after_hash=read('suite_final.log')
expected={'test_acervo.py','test_rotas.py','test_memoria.py','test_psinet_ciclo.py','test_janela_status.py',
          'test_lembrar.py','test_memoria_ui.py','test_streaming_agente.py','test_http_real.py'}
assert '9 SUITE(S) COM FALHA' in text,'Suite incomplete or new failure'
assert len(after)==33 and set(before)==set(after)
assert {n for n,r in after.items() if r['failed']}==expected
for name,old in before.items():
    if name=='test_seguranca_rotas.py':
        assert after[name]['result']=='RESULTADO: 60 OK, 0 falhas'
    else:
        assert after[name]==old,'Changed result: '+name
report={'at':datetime.now().astimezone().isoformat(),'passed':True,'total_suites':33,'green_suites':24,
        'known_red_suites':sorted(expected),'new_failures':0,'old_red_results_unchanged':True,
        'baseline_extra_stale_csp_test_fixed':True,'before_sha256':before_hash,'final_sha256':after_hash,
        'write_and_network_guard':'sync2/sitecustomize.py, same bytes as existing guard',
        'results':after}
with (WORK/'suite_gate.json').open('xb') as f:f.write(json.dumps(report,indent=2).encode())
print(json.dumps({k:v for k,v in report.items() if k!='results'}))
