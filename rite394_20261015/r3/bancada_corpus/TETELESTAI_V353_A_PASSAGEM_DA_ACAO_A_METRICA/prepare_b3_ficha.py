from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/SectorFluidClosure.lean').exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    assert not p.exists(); q=p.with_name(p.name+'.tmp'); q.write_bytes(b)
    assert q.read_bytes()==b and b; os.replace(q,p)
groups={}
for line in (R/'searches_B3/03_workbenches.stdout.txt').read_text(encoding='utf8').splitlines():
    p=Path(line); key=sha(p); group=groups.setdefault(key,dict(sha256=key,paths=[],matches=[]))
    group['paths'].append(str(p))
    if not group['matches']:
        group['matches']=[dict(line=i+1,text=s) for i,s in enumerate(p.read_text(encoding='utf8').splitlines()) if re.search(r'SectorFluid|sector.*(conserv|closure)|non.?interact|non.?exchang|H_nx|w_eff|wEff|closure_identity',s)]
put(R/'BUSCAS_B3_GRUPOS.json',json.dumps(list(groups.values()),ensure_ascii=False,indent=2).encode('utf8'))
providers={
 'RhoPlusPClosure':['lambda_drops_out','closure_identity','hubble_form'],
 'TheSameBetaReadsThreeFaces':['TGLCoupling','the_same_beta_reads_three_faces'],
 'FLRWFieldEquations':['flrwStress','flrw_stress_divergence','flrw_friedmann_first','flrw_friedmann_from_general_metric','flrw_newton_coefficient'],
 'FiniteCoherentSources':['finite_covector_stress_conserved'],
 'GeneralSourceEinsteinBridge':['general_source_heat_matching']}
rows=[]
for stem,names in providers.items():
    p=R/'kernel/TGLExt'/f'{stem}.lean'; s=p.read_text(encoding='utf8')
    for name in names:
        m=re.search(r'^(?:def|structure|theorem) '+name+r'\b',s,re.M); assert m,name
        end=s.find('where' if name=='TGLCoupling' else ':=',m.start()); assert end>=0
        rows.append(dict(name=name,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='TIPO DIFERENTE: fonte covetorial/fluxo total, não a lei escalar com w constante' if stem in ['FiniteCoherentSources','GeneralSourceEinsteinBridge'] else 'REUSAR diretamente'))
for stem,name in [('Add','HasDerivAt.fun_sum'),('Mul','HasDerivAt.const_mul')]:
    p=R/f'kernel/.lake/packages/mathlib/Mathlib/Analysis/Calculus/Deriv/{stem}.lean';s=p.read_text(encoding='utf8')
    m=re.search(r'^theorem '+re.escape(name)+r'\b',s,re.M);end=s.find(':=',m.start())
    rows.append(dict(name=name,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='REUSAR, especializando escalares reais e soma finita'))
anchors=['def prove_rho_plus_p_closure(', '"ext_rp_hubble_form_kernel_proved":', 'def prove_d1_camb_protocol(', '"background": "H^2 = (8 pi G/3)']
consumers=[dict(path=str(R/'um.py'),line=i+1,text=l.strip(),sha256=sha(R/'um.py')) for i,l in enumerate((R/'um.py').read_text(encoding='utf8').splitlines()) if any(a in l for a in anchors)]
target='''SectorFluid (iota : Type) [Fintype iota] (I : Set Real) (H : Real -> Real):
 rho : iota -> Real -> Real; w : iota -> Real (constant in time);
 rho_nonneg : forall i t in I, 0 <= rho i t;
 H_nx : forall i t in I, HasDerivAt (rho i) (-3*H t*(1+w i)*rho i t) t.
c : TGLExt.TGLCoupling from B1, with the same c.beta in every factor.
rhoT_i=(1+c.beta*(1+w_i))*rho_i; pT_i=w_i*rhoT_i.
The rescaled HasDerivAt equation follows from H_nx by constant multiplication.
rhoTot=sum rho_i; pTot=sum w_i*rho_i; enthalpy=sum(rho_i+w_i*rho_i).
rhoTtot=rhoTot+c.beta*enthalpy, and corrected total continuity holds.
wEff(t)=pTot(t)/rhoTot(t).
For rhoTot(t)>0 and enthalpy(t)>=0: rhoTot(t)*abs(1+wEff(t))=enthalpy(t).
Apply B2 to the actual FLRW stress of rhoTtot,pTtot on open preconnected U,
with smooth positive a, time coordinates in I, H=flrwHubble a and explicit H_null.
Conservation is proved from H_nx, not assumed separately.
At eta=1/(4*G), G>0, B2 yields exists Lambda and
 H^2=(8*pi*G/3)*rhoTot*(1+c.beta*abs(1+wEff))-Lambda/3.
The zero-constant specialization must have a named H_zero_cosmological:
 general Einstein equation with its Lambda and explicit Lambda=0.
No step silently discards the integration constant; no hypothesis is the desired Friedmann equation.
Three-sector corollary applies the existing closure_identity and hubble_form.'''
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO_B3',target=target,
decision='NOVO: tipagem SectorFluid e ponte entre conservação escalar setorial e FLRW já provado em B2. REUSAR soma/derivada Mathlib, TGLCoupling B1, toda geometria B2 e identidades de RhoPlusPClosure. Não refazer a camada Einstein.',
providers=rows,consumers=consumers,proposed_consumers=['ext_tgl_friedmann_from_sector_closure_kernel_proved','ext_sector_rescaling_preserves_continuity_kernel_proved','ext_sector_effective_equation_of_state_kernel_proved'],
searches=[json.loads((R/p).read_text(encoding='utf8')) for p in ['BUSCAS_B3.json','BUSCAS_B3_RETRY.json']],
workbench_groups=dict(path=str(R/'BUSCAS_B3_GRUPOS.json'),sha256=sha(R/'BUSCAS_B3_GRUPOS.json'),distinct_bytes=len(groups),files=sum(len(g['paths']) for g in groups.values())),
search_limits=['As duas leituras inicialmente negadas foram refeitas com acesso autorizado; erro de acesso não foi contado como ausência.','A busca no índice do acervo retornou 25 recortes históricos e corte explícito. Não prova ausência exaustiva; resultados empíricos ali mencionados não foram revalidados nem utilizados.','Fornecedores covetoriais tratam outro tipo de fonte e não satisfazem H_nx por homonímia.'],
constraints=['B2 está compilado e auditado pelo autor; revisão independente em curso. Sua fonte permanece congelada.','Λ existencial não é zero por definição; o enunciado geral a conserva e o corolário zero exige hipótese nomeada.','ρ>0 e entalpia>=0 entram exatamente no uso de w_eff/valor absoluto; nenhuma divisão por zero é ocultada.','Não supor que a rescalagem seja não negativa sem hipótese adicional sobre o fator.','Não-troca setorial e w_i constante são hipóteses [INPUT]; TGL-S/TGL-L e Lema 3 continuam abertos.','As entradas propostas e a V3/D1 são consumidor da gerência; este trabalho não edita runtime nem gate.'])
put(R/'REAPROVEITAMENTO_B3.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior ao código B3]\n\n# B3 — conservação setorial e a equação 00\n\n'+data['decision']+'\n\n## Tipo exato e hipóteses\n```text\n'+target+'\n```\n\n## Consumidores existentes\n```json\n'+json.dumps(consumers,ensure_ascii=False,indent=2)+'\n```\n\nPropostos: '+', '.join(data['proposed_consumers'])+'\n\n## Fornecedores\n'
for row in rows: md+=f"\n### {row['name']}\n{row['path']}:{row['line']} · SHA256 `{row['sha256']}`\n```lean\n{row['statement']}\n```\n{row['decision']}\n"
md+='\n## Seis buscas e repetição das leituras negadas\n```json\n'+json.dumps(data['searches'],ensure_ascii=False,indent=2)+'\n```\n\nGrupos por bytes: '+json.dumps(data['workbench_groups'],ensure_ascii=False)+'\n\n'+ '\n'.join('- '+x for x in data['search_limits']+data['constraints'])+'\n\n'+data['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B3.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(rows),consumers=len(consumers),groups=[dict(sha=g['sha256'],files=len(g['paths']),first=g['paths'][0],matches=g['matches'][:6]) for g in groups.values()]),ensure_ascii=False))
