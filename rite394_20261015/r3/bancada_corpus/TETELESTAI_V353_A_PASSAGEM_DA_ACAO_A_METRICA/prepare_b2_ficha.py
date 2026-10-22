from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/FLRWGeometry.lean').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
 assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b)
 assert q.read_bytes()==b and len(b)>0;os.replace(q,p)
providers={
 'Solder4D':['eta4','solder4_lorentzian'],
 'EmergenceTriad':['LorentzByCongruence'],
 'CovariantScalarConservation':['Coordinate4','TensorField4','coordinatePartial','tensorFieldJet','tensorFieldDivergence','tensorFieldJet_congr_on'],
 'MetricCompatibleJet':['leviCivitaJet'],
 'MetricFieldConnection':['leviCivitaField','levi_civita_field_metric_compatible'],
 'CoordinateCurvature':['coordinateCurvature'],
 'MetricCurvatureSymmetries':['coordinateRicci','geometricEinsteinTensor'],
 'GeneralMetricEinstein':['metricInverse','metric_inverse_unique','constructed_metric_inverse_left','constructed_metric_inverse_right','metric_only_einstein_equation'],
 'GeneralMetricClausius':['metric_einstein_from_screen_clausius'],
 'TriadMaster':['einstein_coefficient_from_clausius'],
 'AnsatzEinstein':['ansatzRicci00','ansatzG00_zero']}
rows=[]
for stem,names in providers.items():
 p=R/'kernel/TGLExt'/f'{stem}.lean';s=p.read_text(encoding='utf8')
 for name in names:
  m=re.search(r'^(?:def|abbrev|theorem) '+name+r'\b',s,re.M);assert m,name
  end=s.find(':=',m.start());assert end!=-1
  rows.append(dict(name=name,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='NÃO USAR como FLRW: outro ansatz, Ricci definido à mão' if stem=='AnsatzEinstein' else 'REUSAR maquinaria geral, instanciando a família FLRW; não reconstruir Einstein/Clausius.'))
text=(R/'um.py').read_text(encoding='utf8').splitlines()
anchors=['"ext_v338_generalmetric_metric_only_einstein_equation_kernel_proved":','"ext_v338_generalclausius_metric_einstein_from_screen_clausius_kernel_proved":','"ext_tm_einstein_coefficient_kernel_proved":','"ext_rp_hubble_form_kernel_proved":']
consumers=[dict(path=str(R/'um.py'),line=i+1,text=l.strip(),sha256=sha(R/'um.py')) for i,l in enumerate(text) if any(a in l for a in anchors)]
target='''a : Real -> Real; U : Set Coordinate4 open; for each x in U, ContDiffAt Real infinity a (x 0) and 0<a(x 0).
flrwMetric a x = diag(1,-a(x0)^2,-a(x0)^2,-a(x0)^2).
Use metricInverse(flrwMetric a), leviCivitaField of that same metric/inverse, coordinateRicci and geometricEinsteinTensor.
G00=3*(a'/a)^2; Gii=-(2*a*a''+(a')^2) for spatial i; off-diagonal G=0.
For null k, Ric(k,k)=2*((a'/a)^2-a''/a)*(k0)^2.
For T=diag(rho,p*a^2,p*a^2,p*a^2), scalar rho,p depend on x0 and are differentiable locally.
Instantiate metric_only_einstein_equation with connected U, null balance and divergence zero:
exists Lambda, G+Lambda*g=(2*pi/eta)*T, then H^2=(2*pi/(3*eta))*rho-Lambda/3
and H'=-(pi/eta)*(rho+p), equivalently a''/a=-(pi/(3*eta))*(rho+3*p)-Lambda/3.
Same divergence zero implies rho'+3*(a'/a)*(rho+p)=0.
With eta=1/(4*G_Newton) and G_Newton>0, coefficient 2*pi/(3*eta)=8*pi*G_Newton/3.
The formal Lambda sign follows G+Lambda*g=kappa*T in the existing layer; no identification with a physically named Lambda is assumed.'''
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO_B2',
 current_B1='B1 source written first, author Lake build and independent reproduction still in progress; only B2 searches and fiche prepared here.',
 target=target,decision='NOVO: avaliação FLRW da maquinaria geral. REUSAR: reconstrução de Einstein, inversa, conexão, curvatura e divergência. A busca não achou fornecedor FLRW; o ansatz univariado antigo é outra métrica e não será renomeado.',
 providers=rows,consumers=consumers,proposed_consumers=['ext_flrw_einstein_00_kernel_proved','ext_flrw_friedmann_first_kernel_proved','ext_flrw_friedmann_second_kernel_proved','ext_flrw_continuity_kernel_proved'],
 downstream='B3 tgl_friedmann_from_sector_closure consome equação 00; B4 compara a equação derivada de Clausius. Implementação do mapa pertence à gerência.',
 searches=json.loads((R/'BUSCAS_B2.json').read_text(encoding='utf8')),
 constraints=['A geometria é computada por definições gerais; componentes Ricci/Einstein não serão campos pressupostos.','a é suave localmente sobre U, sem impor suavidade ou positividade fora da carta.','A assinatura é eta4=(+---), conferida na inversa/congruência.','Não escolher entre rotas cosmológicas, modificar D1 ou reabrir A1.','B2 não introduz beta, nem parâmetro empírico. eta/G continuam INPUT.','Módulos pretendidos: FLRWGeometry para componentes; FLRWFieldEquations para consumidor geral, Friedmann e conservação. Lemas auxiliares só se consumidos.', 'Buscar.py não retornou ocorrências dos nomes/tipos consultados; é limitação do índice, não prova de ausência de toda a literatura.'])
put(R/'REAPROVEITAMENTO_B2.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior ao código B2]\n\n# B2 — FLRW na carta e nas definições geométricas da casa\n\n'+data['decision']+'\n\n## Tipo exigido\n```text\n'+target+'\n```\n\n## Consumidores\n'+json.dumps(consumers,ensure_ascii=False,indent=2)+'\n\n'+data['downstream']+'\n\n## Fornecedores e tipos lidos\n'
for row in rows:md+=f"\n### {row['name']}\n{row['path']}:{row['line']} · SHA256 `{row['sha256']}`\n```lean\n{row['statement']}\n```\n{row['decision']}\n"
md+='\n## Buscas\n'+json.dumps(data['searches'],ensure_ascii=False,indent=2)+'\n\n## Restrições e alcance\n'+'\n'.join('- '+c for c in data['constraints'])+'\n\n'+data['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B2.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(rows),consumers=len(consumers),ficha=sha(R/'REAPROVEITAMENTO_B2.json'))))
