from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;CHAT=R.parent.parent
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def check(e):
 p=Path(e['path']);assert pin(p)=={k:e[k] for k in ['path','bytes','sha256']};return p
def put(p,s):
 assert p.is_relative_to(R) and not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
audit=load(R/'AUDITORIA_TRACIALIDADE_QUADRATICA_A1B.json')
review=load(R/'revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL.json')
assert audit['full_trace_constructed'] and review['full_trace_constructed']
assert all(not review[k] for k in ['P0','P1','P2']) and review['mathematical_review_passed']
assert (R/'RECIBO_DELTA_QUADRATIC_TRACE.json').exists()
rows=[]
for p in sorted(R.glob('RECIBO_DELTA_*.json')):
 d=load(p);delivery=check(d['delivery']);check(d['manifest']);check(d['acceptance'])
 rows.append(dict(receipt=pin(p),timestamp=d['timestamp'],delivery=d['delivery'],manifest=d['manifest'],acceptance=d['acceptance']))
rows.sort(key=lambda x:x['timestamp'])
B=CHAT/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA';prior=[]
for n in range(1,7):
 p=B/f'RECIBO_B{n}.json';d=load(p);check(d['delivery']);check(d['manifest'])
 prior.append(dict(target=f'B{n}',receipt=pin(p),delivery=d['delivery'],manifest=d['manifest']))
stamp=datetime.datetime.now().astimezone().isoformat()
scope='[REAL] A1(b) entrega um habitante RegularCoreTraceData para todo SiteProfile na realização regular construída. O valor é literalmente scalarInverseLimitWeight, obtido do peso dual pelos cortes inversos do mesmo gerador; fiel, normal, semifinito, aditivo, homogêneo, monótono, tracial e com escala dual exp(-s). O contrato fortalecido anterior já recusava o traço zero. B1–B6 já entregues; recibos e manifestos correspondem aos bytes atuais. A matemática verificada aqui não identifica h com Delta_nu nem confirma uma realização física.'
pending='[OPEN] A2 permanece distinto: realizar os Three Locks e sua projeção espectral de zero no mesmo core, com traço positivo finito e split, descarregando as entradas de threeLocksFromSupport. A3–A7 e a incorporação no monólito não são consequências automáticas de A1. Em particular qgf_continuous_modular_realization_constructed exige A1 com A2 pela ORDEM011; esta entrega não autoriza ligá-lo apenas pela existência do traço. Nenhuma significância experimental, rito da natureza ou gate foi recalculado.'
text=stamp+'\n\n'+scope+'\n\n'+pending+'\n\n'
text+='O marco final fornece `TGLV350.Regular.scalarInverseLimitWeight_tracial` e `TGLV350.Regular.scalarInverseLimitTraceData.{u}`. Reutilizar esses termos e seus fornecedores: não reconstruir as etapas anteriores nem criar um segundo peso. A incorporação é da gerência; os originais foram preservados.\n\n'
text+='Encadeamento consumido: peso/GNS/Tomita originais → ação modular no core → gerador regular e afiliação → cortes inversos e ação direita → peso limite e suas leis → extensão tracial e minorantes → igualdade dos implementadores → balanço dos cortes → formas quadráticas → tracialidade → contrato completo. As hipóteses e os tipos exatos permanecem nas entregas abaixo.\n\n'
text+='## Entregas da retomada, por data\n\n'
for row in rows:text+=f"- [{Path(row['delivery']['path']).name}](<{row['delivery']['path']}>)\n"
text+='\n## B1–B6 anteriores\n\n'
for row in prior:text+=f"- [{row['target']}](<{row['delivery']['path']}>)\n"
d=dict(timestamp=stamp,scope=scope,pending=pending,full_trace_constructed=True,gate_changed=False,
 deltas=rows,prior_B=prior,author_audit=pin(R/'AUDITORIA_TRACIALIDADE_QUADRATICA_A1B.json'),
 independent_review=pin(R/'revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL.json'))
put(R/'CONSOLIDACAO_A1B_20260915.md',text)
put(R/'CONSOLIDACAO_A1B_20260915.json',json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(dict(summary=pin(R/'CONSOLIDACAO_A1B_20260915.md'),deltas=len(rows),B_verified=len(prior)),ensure_ascii=False))
