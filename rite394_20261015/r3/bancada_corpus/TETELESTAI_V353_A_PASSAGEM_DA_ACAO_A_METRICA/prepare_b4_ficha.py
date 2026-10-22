from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/ThermodynamicFriedmann.lean').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
providers={
 'TriadMaster':['HorizonEquilibriumData','einstein_coefficient_from_clausius','horizon_clausius_composition'],
 'TheImportedEquilibrium':['EquilibriumInput','discharge_by_import','the_trio_is_a_pair'],
 'SectorFluidClosure':['enthalpy_eq','corrected_closure','effective_enthalpy','multiplicative_closure'],
 'SectorFriedmann':['tgl_friedmann_from_sector_closure'],
 'LocalHorizonBalance':['local_clausius_forces_ricci']}
rows=[]
for stem,names in providers.items():
    p=R/'kernel/TGLExt'/f'{stem}.lean';s=p.read_text(encoding='utf8')
    for name in names:
        m=re.search(r'^(?:structure|theorem) '+name+r'\b',s,re.M);assert m,name
        end=s.find('where' if s[m.start():].startswith('structure') else ':=',m.start())
        rows.append(dict(name=name,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='ADAPTAR dados explícitos; lei de área modificada não cabe no tipo de área original' if name=='HorizonEquilibriumData' else 'NÃO CASAR por nome: tela nula local, não horizonte FLRW' if name=='local_clausius_forces_ricci' else 'REUSAR tipos/implicações pertinentes; importação fica explícita'))
p=R/'kernel/.lake/packages/mathlib/Mathlib/Analysis/Calculus/MeanValue.lean';s=p.read_text(encoding='utf8');n='IsOpen.exists_is_const_of_deriv_eq_zero';m=re.search(r'^theorem _root_\.'+re.escape(n),s,re.M);end=s.find(':=',m.start())
rows.append(dict(name=n,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='REUSAR para integrar a diferença com derivada nula em intervalo aberto conexo'))
text=(R/'um.py').read_text(encoding='utf8').splitlines()
anchors=['EXTERNAL_KNOWN_THEOREMS =','def prove_d1_camb_protocol(', '"ext_rp_hubble_form_kernel_proved":','"ext_tm_einstein_coefficient_kernel_proved":']
consumers=[dict(path=str(R/'um.py'),line=i+1,text=l.strip(),sha256=sha(R/'um.py')) for i,l in enumerate(text) if any(a in l for a in anchors)]
target='''Natural units c=hbar=k_B=1; cpl:TGLCoupling; G>0, Phi>0, H>0.
Imported horizon data: radius=1/H, area=4*pi/H^2, temperature=H/(2*pi),
 qdot=area*(rho+p)*H*radius, sdot=Adot/(4*G*Phi), qdot=temperature*sdot.
Adot is the HasDerivAt derivative of 4*pi/(H(t)^2), not an assumed Einstein equation.
Then Hdot=-4*pi*G*Phi*(rho+p). Use the existing coefficient composition.
Literal errata flux without radius instead implies Hdot=-4*pi*G*Phi*H*(rho+p).
For constant w, Phi=1+cpl.beta*abs(1+w) is constant; continuity plus the derived
second equation yields HasDerivAt (H^2-(8*pi*G/3)*Phi*rho) 0 and an existential constant C
on an open connected time interval. H^2=(8*pi*G/3)*Phi*rho+C.
For variable Phi, use a primitive P(t) with P'=Phi*rho', yielding H^2=(8*pi*G/3)*P+C.
Derivative of H^2-(8*pi*G/3)*Phi*rho contains -(8*pi*G/3)*Phi'*rho;
derivative of S_BH/Phi contains -S_BH*Phi'/Phi^2 in addition to A'/(4G*Phi).
For finite sectors of B3 at t in I, R=sum rho_i>0, E=sum(1+w_i)*rho_i>=0,
 M2=sum(1+w_i)^2*rho_i, sectorEnthalpy=sum(1+beta*(1+w_i))*(rho_i+p_i):
 sectorEnthalpy-(1+beta*abs(1+wEff))*E=beta*(M2-E^2/R)>=0.
 M2-E^2/R=sum rho_i*((1+w_i)-E/R)^2;
 equality iff exists common w, forall i with rho_i>0, w_i=common w.
The criterion omitting vacuum sectors is false: positive matter plus vacuum is a typed counterexample.
Phi_flux=1+beta*M2/E is the unique scalar matching enthalpy-weighted closure if E!=0.
At E=0 uniqueness is not asserted; non-phantom sectors then have zero flux, allowing every factor.
For common w and E!=0, Phi_flux=1+beta*(1+w); equals 1+beta*abs(1+w) if 1+w>=0.
No route is selected and no empirical datum chooses an equation.'''
corrections=[
 'Fluxo: eq. (2.12) de Cai–Kim tem o fator raio aparente. A errata/ordem omitem esse raio e não produzem a segunda equação declarada. Serão provadas a consequência literal e a correção com raio.',
 'Entropia variável: S=A/(4G*Phi) não implica dS=dA/(4G*Phi) quando Phi varia. Tipar a lei diferencial como INPUT distinto, provar o termo ausente e o caso constante.',
 'Igualdade da variância: o suporte correto é rho_i>0, incluindo vácuo; o suporte rho_i+p_i!=0 pedido na ordem falha para matéria+vácuo. Provar contraexemplo e critério corrigido.',
 'Unicidade Phi_flux exige entalpia total diferente de zero. Sem isso a divisão não pode selecionar o fator.',
 'Constante cosmológica/integral permanece explícita, como em B2/B3. A primeira fórmula multiplicativa é a integração da rota setorial; não da rota total variável em geral.']
web=[dict(title='Cai & Kim (2005), JHEP 02 050',url='https://arxiv.org/html/hep-th/0501055',equations=['2.3','2.12','2.13','2.14','2.16','2.17'],role='Raio aparente, fluxo com H*r_A, prescrição de temperatura e primeira lei; especialização plana r_A=1/H. Temperatura em horizonte dinâmico é prescrição da derivação, discutida após 2.21.',imported_into_witness=False),dict(title='Jacobson (1995), PRL 75 1260',url='https://arxiv.org/abs/gr-qc/9504004',role='Termodinâmica local como motivação/importação; hipóteses locais adicionais não são provadas por um dado escalar FLRW.',imported_into_witness=False)]
groups={}
for line in (R/'searches_B4/03_workbenches.stdout.txt').read_text(encoding='utf8').splitlines():
    p=Path(line); key=sha(p);g=groups.setdefault(key,dict(sha256=key,paths=[]));g['paths'].append(str(p))
put(R/'BUSCAS_B4_GRUPOS.json',json.dumps(list(groups.values()),ensure_ascii=False,indent=2).encode('utf8'))
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO_B4',target=target,providers=rows,consumers=consumers,
 decision='ADAPTAR dados termodinâmicos explícitos; NOVO o cálculo cosmológico e o teorema da diferença. As correções são teoremas de parede, não escolha de rota. Nenhuma nova camada Einstein.',
 proposed_consumers=['ext_tgl_second_friedmann_from_clausius_kernel_proved','ext_tgl_first_friedmann_constant_w_kernel_proved','ext_the_two_routes_differ_kernel_proved','ext_the_entropy_factor_that_reproduces_the_sector_closure_kernel_proved','EXTERNAL_KNOWN_THEOREMS (entradas B6)'],
 corrections=corrections,external_sources=web,searches=[json.loads((R/p).read_text(encoding='utf8')) for p in ['BUSCAS_B4.json','BUSCAS_B4_RETRY.json']],
 search_limits='Pesquisa por nomes/tipos e leituras dos fornecedores pertinentes, não prova de ausência exaustiva. Regex variance também localiza invariance; esses homônimos não são fornecedores estatísticos.',
 groups=dict(path=str(R/'BUSCAS_B4_GRUPOS.json'),sha256=sha(R/'BUSCAS_B4_GRUPOS.json'),groups=len(groups),files=sum(len(x['paths']) for x in groups.values())))
put(R/'REAPROVEITAMENTO_B4.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior ao código B4]\n\n# B4 — termodinâmica explícita e diferença entre rotas\n\n'+data['decision']+'\n\n## Tipo exato\n```text\n'+target+'\n```\n\n## Correções necessárias\n'+'\n'.join('- '+x for x in corrections)+'\n\n## Consumidores\n```json\n'+json.dumps(consumers,ensure_ascii=False,indent=2)+'\n```\n\n## Fornecedores\n'
for row in rows:md+=f"\n### {row['name']}\n{row['path']}:{row['line']} · SHA256 `{row['sha256']}`\n```lean\n{row['statement']}\n```\n{row['decision']}\n"
md+='\n## Fontes externas e alcance\n'+'\n'.join(f"- [{x['title']}]({x['url']}): {x['role']} `imported_into_witness:false`." for x in web)+'\n\n## Buscas\n```json\n'+json.dumps(data['searches'],ensure_ascii=False,indent=2)+'\n```\n\n'+data['search_limits']+'\n\nGrupos: '+json.dumps(data['groups'],ensure_ascii=False)+'\n\n'+data['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B4.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(rows),consumers=len(consumers),groups=data['groups'])))
