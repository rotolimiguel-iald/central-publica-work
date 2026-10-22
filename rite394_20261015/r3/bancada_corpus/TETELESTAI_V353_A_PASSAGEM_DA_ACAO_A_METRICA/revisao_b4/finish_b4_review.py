from pathlib import Path
from datetime import datetime
import hashlib,json,os,re
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b4';S=R/'s';BUILD=S/'.lake/build/lib/lean'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
NEW=['TGLExt.ThermodynamicFriedmann','TGLExt.SectorRouteComparison','TGLExt.AuditThermodynamics']
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def ck(r):assert pin(Path(r['path']))==r,r
def save(p,d,text=False):
 assert p.resolve().is_relative_to(OUT.resolve())
 b=d.encode('utf8') if text else (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+STAMP);bk.write_bytes(old);assert bk.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_'+STAMP)
 with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==b;os.replace(tmp,p)
def norm(x):return re.sub(r'\.\{[^}]*\}','',x).strip()
def axioms(text):
 out={}
 for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
  n=norm(m.group(1));v=[] if m.group(3) else [norm(x) for x in m.group(2).split(',') if x.strip()]
  assert n not in out or out[n]==v;out[n]=v
 return out
ptr=load(OUT/'B4_SNAPSHOT_POINTER.json');ck(ptr['snapshot']);A=Path(ptr['attempt']);snap=load(Path(ptr['snapshot']['path']))
completion=load(A/'completion.json');assert completion['status']=='BUILD_RC0__REVIEW_PENDING'
ck(completion['run']);run=load(A/'run.json');assert run['returncode']==0
for p in run['streams']+run['executables']+snap['protected_before']+snap['documents']+snap['source_configs']+[snap['own_auditor'],snap['inherited_B3_compilation']]:ck(p)
for r in snap['sources']:ck(r['source']);ck(r['copy'])
for r in snap['inherited_project_objects']:ck(r['object']);ck(r['trace'])
targets=snap['targets'];assert len(targets)==len(set(targets))==28
tracepath=BUILD/'TGLExt/ReviewThermodynamics.trace';trace=load(tracepath);ax={};types={}
for log in trace['log']:
 assert log.get('level') not in ['error','warning'],log
 if log.get('level')!='info':continue
 text=log['message']
 if 'depends on axioms:' in text or 'does not depend on any axioms' in text:ax.update(axioms(text))
 else:
  text=re.sub(r'^.*?\.lean:\d+:\d+:\s*','',text,count=1)
  for t in targets:
   if re.match(re.escape(t)+r'(?:\.\{[^}]*\})?(?:\s|$)',text):
    assert t not in types,t;types[t]=text
assert set(ax)==set(types)==set(targets)
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values())
assert axioms('\n'.join(x['message'] for x in load(BUILD/'TGLExt/AuditThermodynamics.trace')['log'] if x.get('level')=='info'))==ax
objects=[];warnings=[]
for mod in NEW+['TGLExt.ReviewThermodynamics']:
 p=BUILD/(mod.replace('.','/')+'.olean');tp=p.with_suffix('.trace');tr=load(tp)
 for log in tr['log']:
  assert log.get('level')!='error',log
  if log.get('level')=='warning':warnings.append(log)
  if log.get('level')=='trace' and 'LEAN_PATH=' in log.get('message',''):
   search=log['message'].split('LEAN_PATH=',1)[1].split(' c:',1)[0]
   assert str(R/'kernel'/'.lake') not in search and str(R/'r'/'.lake') not in search and 'V351' not in search
 author=R/'kernel'/'.lake/build/lib/lean'/p.relative_to(BUILD)
 ob=dict(module=mod,own=pin(p),trace=pin(tp),author=None,equal_to_author=None)
 if mod in NEW:ob['author']=pin(author);ob['equal_to_author']=ob['own']['sha256']==ob['author']['sha256'];assert ob['equal_to_author']
 objects.append(ob)
assert not warnings
allobjects=[p for p in BUILD.rglob('*.olean') if p.relative_to(BUILD).parts[0] in ['TGL','TGLExt']]
assert len(allobjects)==117
aupath=R/'AUDITORIA_B4.json';au=load(aupath)
for p in au['sources']+au['objects']+[au['positive_build']]:ck(p)
arun=load(Path(au['positive_build']['path']));assert arun['returncode']==0
for x in arun['snapshots']:assert pin(Path(x['path']))['sha256']==x['sha256']==pin(Path(x['snapshot']))['sha256']
assert au['axioms']==ax and {r['name'] for r in au['targets']}==set(targets)
controls=[]
for c in au['commands']:
 for key in ['source','stdout','stderr']:ck(c[key])
 text=Path(c['stdout']['path']).read_text(encoding='utf8')
 if c['label']=='AuditThermodynamics':assert c['returncode']==0 and axioms(text)==ax
 else:
  assert c['returncode']!=0 and 'type mismatch' in text.lower()
  assert not any(v in text.lower() for v in ['unknown module','unknown identifier','unexpected token','unexpected identifier','object file'])
 controls.append(dict(**c,review_scope='Author execution; source/raw streams reread independently, not re-executed'))
fiche=load(R/'REAPROVEITAMENTO_B4.json');providers=[]
for pr in fiche['providers']:
 p=Path(pr['path']);assert pin(p)['sha256']==pr['sha256']
 line=p.read_text(encoding='utf-8-sig').splitlines()[pr['line']-1];assert pr['name'] in line,(pr['name'],line)
 providers.append(dict(**pr,line_read=line))
chronology=[]
for p in [R/'REAPROVEITAMENTO_B4.md',R/'REAPROVEITAMENTO_B4.json']+[Path(x['source']['path']) for x in snap['sources'] if x['module'] in NEW]:
 st=p.stat();chronology.append(dict(file=pin(p),created_local=datetime.fromtimestamp(st.st_ctime).astimezone().isoformat(),modified_local=datetime.fromtimestamp(st.st_mtime).astimezone().isoformat()))
precedes=all((R/'REAPROVEITAMENTO_B4.json').stat().st_mtime<Path(x['source']['path']).stat().st_ctime for x in snap['sources'] if x['module'] in NEW);assert precedes
order=R.parent/'TUNEL/PARA_CHATGPT/ORDEM_012_a_passagem_da_acao_a_metrica.md';lines=order.read_text(encoding='utf-8-sig').splitlines()
contract=dict(order=pin(order),lines='125-141',excerpt='\n'.join(lines[124:141]),fiche=[pin(R/'REAPROVEITAMENTO_B4.md'),pin(R/'REAPROVEITAMENTO_B4.json')],providers=providers,chronology=chronology,fiche_before_sources_by_filesystem_metadata=precedes,
 literal_contract_exceptions=[
  dict(clause='Heat flux without apparent radius',disposition='Literal formula has an extra H; corrected input includes H*r_A',formal_witness='ChatgptAudit.FLRW.radius_free_flux_consequence'),
  dict(clause='Entropy quotient differentiated as if Phi were constant',disposition='Extra Phi-prime term explicit; differential entropy is a distinct INPUT',formal_witness='ChatgptAudit.FLRW.variable_entropy_derivative'),
  dict(clause='Equality iff w coincides on nonzero enthalpy support',disposition='False for matter plus vacuum; corrected criterion uses positive density support',formal_witness='ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality'),
  dict(clause='Unconditional uniqueness of flux factor',disposition='Needs total enthalpy nonzero; otherwise no unique scalar',formal_witness='ChatgptAudit.FLRW.zero_flux_has_no_unique_factor')],
 source_consultation=dict(title='Cai and Kim (2005), First Law of Thermodynamics and Friedmann Equations',url='https://arxiv.org/html/hep-th/0501055',version='hep-th/0501055v1',method='Read-only web tool, primary source',locations=['(2.3)','(2.12)-(2.16)','discussion after (2.21)'],verified='r_A=1/H in flat expanding case; heat flux contains H*r_A; temperature is a prescription for the dynamical apparent horizon, not proved by this Lean package',physical_modified_entropy_from_CaiKim=False),
 search_scope='Fiche searches read, no new corpus scan; no exhaustive absence claim',consumer_scope='Python consumers proposed only; um.py not inspected/executed in this review')
save(A/'contract_and_fiche.json',contract)
sem=dict(status='B4 candidate accepted on its explicit conditional statements, literal corrections retained',
 horizon='HubbleHorizonInput is pointwise, H>0,G>0,Phi>0 and H differentiable. EntropyRate/heatRate scalar fields satisfy imported differential law, flux and Clausius. There is no supplied Hdot or Friedmann conclusion.',
 derivative='hubble_area_derivative proves derivative of 4pi/H² using H nonzero. The second equation is obtained by substitutions and cancellation; rate is heat deltaQ=-dE, consistent with cited orientation.',
 entropy='The modification dS=dA/(4G Phi) is INPUT; no S=A/(4G Phi) identity is assumed when Phi varies. variable_entropy_derivative proves the missing first-derivative term explicitly.',
 first_integral='Primitive theorem takes an actual HasDerivAt primitive with derivative Phi*rho-prime. It proves existence of integration constant on open preconnected I. Does not construct primitive existence for every arbitrary Phi.',
 constant_w='tgl_first_friedmann_constant_w supplies primitive Phi*rho with constant real w, using the horizon-derived second equation and named H_nx. C retained; no zeroing cosmological constant.',
 variable_factor='variable_factor_first_equation_defect identifies -(8piG/3)Phi-prime*rho exactly; the naive multiplicative expression is not claimed for all variable Phi. Exceptional vanishing of the defect is not excluded.',
 variance='Centered finite sum identity uses totalRho nonzero; nonnegativity uses original rho_i>=0 on I. No probability or nonempty index axiom added. Equality iff common w on rho_i>0; includes vacuum densities.',
 comparison='Total-factor versus corrected enthalpy differs by beta*variance with hr>0,he>=0. Hdot difference carries -4piG. For G>0 it has the opposite sign; theorem itself is an algebraic identity for arbitrary G.',
 factor='Unique matching scalar Phi_flux=1+beta*M2/E iff E!=0. At E=0, either every factor matches or none does; no unique factor in either case. It is not silently assigned value 1 by total division.',
 common_w='common_w_flux_factor explicitly assumes 1+w>=0 for the absolute-value reading and E!=0. Vacuum-only E=0 not forced through it.',
 consumer='sector_clausius_matches_closed_rate invokes tgl_second_friedmann_from_clausius with Phi_flux. The B3 first equation is inherited. This connects coefficients to the actual conditional Clausius theorem without claiming a common solution to incompatible rate laws.',
 counterexample='Fin 2 with positive matter and vacuum, w=(0,-1), satisfies common w on nonzero enthalpy support yet variance=rhoM*rhoL/(rhoM+rhoL)>0. Counterexample to order equality clause, not to the corrected candidate.',
 limitations=['No physical validation of imported horizon prescriptions','No construction of global horizon or discharge of H3','No choice between total and sector routes','No assertion of general entropy quotient law for variable Phi','No independent existence theorem for every possible primitive or cosmological solution','No B5/B6, A1, gate/runtime/integration or data work'],findings=[])
save(A/'semantic_inspection.json',sem)
stamp=datetime.now().astimezone().isoformat()
compilation=dict(timestamp=stamp,status='INDEPENDENT_B4_LAKE_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='B4 Lake only; no historical B1/B2 preparation failures reclassified',run=pin(A/'run.json'),runs=[dict(label='B4',run=pin(A/'run.json'),returncode=0)],source_snapshot=ptr['snapshot'],targets={t:dict(typecheck=types[t],axioms=ax[t]) for t in targets},exact_target_count=28,theorems=22,definitions=5,structures=1,all_axioms_allowed=True,all_target_typechecks_present=True,auditor_trace=pin(tracepath),objects=objects,new_project_object_count=4,private_project_object_count=len(allobjects),inherited_B3_compilation=snap['inherited_B3_compilation'],inherited_project_objects=snap['inherited_project_objects'],inherited_project_objects_unchanged=True,new_warnings=warnings,author_project_objects_copied=False,cache_inheritance=snap['cache_inheritance'],B1_B2_B3_protected_unchanged=True,protected_pins=snap['protected_before'])
save(OUT/'compilation.json',compilation)
evidence=dict(timestamp=stamp,status='B4_DEV_REVIEW_ACCEPTED_WITH_EXPLICIT_CONTRACT_CORRECTIONS__INTEGRATION_NOT_REVIEWED',marker='B4_DEV_REVIEW',P0=[],P1=[],P2=[],findings=[],literal_original_contract_certified=False,contract_corrections=contract['literal_contract_exceptions'],compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),semantic_inspection=pin(A/'semantic_inspection.json'),semantic=sem,contract_and_fiche=pin(A/'contract_and_fiche.json'),source_snapshot=ptr['snapshot'],author_audit=pin(aupath),author_positive_build=au['positive_build'],author_commands=controls,author_baseline_941_preservation='DECLARADO in author audit; no broad independent um.py/941-source scan',new_source_object_pins=[dict(source=next(r['source'] for r in snap['sources'] if r['module']==o['module']),**o) for o in objects if o['module'] in NEW],protected_prior_reports=snap['protected_before'],B1_B2_B3_unchanged=True,scope='Only B4 frozen two modules plus author auditor and independent auditor; corrected conditional contract. No integration, B5/B6, A1 or empirical validation.')
save(OUT/'REVIEW_B4_FINAL.json',evidence)
table='\n'.join('| '+o['module'].split('.')[-1]+' | `'+next(r['source']['sha256'] for r in snap['sources'] if r['module']==o['module'])+'` | `'+o['own']['sha256']+'` |' for o in objects if o['module'] in NEW)
targetlist='\n'.join('- `'+t+'`' for t in targets)
md=f'''# B4 — revisão independente final

{stamp} · **B4_DEV_REVIEW**

[REAL] **Candidato DEV aceito nos enunciados corrigidos e explicitamente condicionais; nenhum P0–P2 no candidato.** Reprodução Lake própria rc0, **28 alvos = 22 teoremas + 5 definições + 1 estrutura**, tipos/universos e axiomas conferidos. Apenas `propext`, `Classical.choice`, `Quot.sound`; nenhum aviso novo. **Não se certifica a redação literal incorreta da ordem:** as quatro correções abaixo são parte obrigatória do alcance, não detalhes a omitir na entrega.

## O que a prova corrige

1. **Fluxo:** a entrada usa `A·(rho+p)·H·r_A`, com `r_A=H⁻¹`. `radius_free_flux_consequence` demonstra que retirar o raio deixa um fator H extra no resultado. Conferi a presença do raio em Cai–Kim (2.12), a especialização plana (2.3) e a prescrição de temperatura (2.13); os autores discutem a limitação do horizonte dinâmico após (2.21). `heatRate` tem a orientação do calor deltaQ=-dE. A lei modificada de entropia é INPUT próprio, não resultado desse artigo. [Fonte primária](https://arxiv.org/html/hep-th/0501055).
2. **Entropia variável:** `variable_entropy_derivative` prova o termo adicional `−A·Phi′/(4G·Phi²)`. A entrada `differential_entropy` é a lei diferencial `Sdot=Adot/(4G Phi)`, distinta de derivar o quociente variável. Não se declara esta última passagem automática.
3. **Igualdade entre rotas:** o critério correto usa **rho_i>0, inclusive vácuo**, e não somente `(1+w_i)rho_i≠0`. Há contraexemplo Lean em Fin 2: matéria e vácuo positivos satisfazem o critério original de fluxo, mas têm variância `rhoM*rhoL/(rhoM+rhoL)>0`. A cláusula literal de igualdade da ordem é refutada; `sector_variance_zero_iff`/`the_two_routes_equal_iff` provam a versão corrigida.
4. **Unicidade:** `Phi_flux` seleciona um único fator apenas para entalpia total E≠0. `zero_flux_has_no_unique_factor` prova que E=0 nunca dá unicidade: pode haver nenhum fator ou todos. A leitura por divisão total de Lean não é usada como seleção física no caso zero.

Esses negativos são resultados explícitos do pacote. O aceite não deve ser convertido em afirmação de que as quatro formulações literais originais foram provadas.

## Hipóteses e uso dos fornecedores

`HubbleHorizonInput` explicita H>0, G>0, Phi>0, diferenciabilidade de H e os três vínculos entre fluxo, taxa de entropia e Clausius. Não contém a conclusão Friedmann ou Hdot como campo. `hubble_area_derivative` calcula a derivada real de `4pi/H²`; `modified_clausius_coefficient` consome o fornecedor existente. A consequência é **Hdot=−4piG·Phi·(rho+p)**. Não é construção global de horizonte ou descarga de H3; a validade física das prescrições permanece importada/condicional.

`tgl_first_friedmann_from_primitive` usa uma **primitiva efetivamente fornecida por HasDerivAt**, prova derivada zero de `H²−(8piG/3)primitive` e obtém uma constante C em I aberto/preconexo. Não prova existência de primitivas para funções arbitrárias. `tgl_first_friedmann_constant_w` fornece a primitiva `Phi*rho` quando w é constante, conserva C e usa a segunda equação obtida do dado de horizonte mais continuidade `H_nx` nomeada. `variable_factor_first_equation_defect` calcula exatamente o defeito `−(8piG/3)Phi′rho`; não afirma que todo Phi variável produz defeito não nulo nem apaga exceções.

Nos setores finitos, a variância é identificada com uma soma de quadrados ponderados por rho_i≥0. A fórmula centrada pede rhoTot≠0; a comparação com o valor absoluto pede rhoTot>0 e E≥0. A diferença de **fontes** é beta·variância≥0; `the_two_hubble_rates_differ` mantém o prefator **−4piG**, portanto para G>0 o sinal da diferença de Hdot é o oposto. Esse sinal não foi invertido por nomenclatura.

`sector_clausius_matches_closed_rate` efetivamente aplica a equação de Clausius com Phi_flux e a identidade de entalpia corrigida. `common_w_flux_factor` exige E≠0 e 1+w≥0 para coincidir com `1+beta*|1+w|`. A primeira equação setorial permanece a B3 já revista; não se supõe que duas leis diferentes de Hdot descrevam automaticamente a mesma solução. **Nenhuma rota é escolhida.**

## Reprodução e custódia privada

Raiz curta `{S}`, tentativa `{A}`. Comando: `lake build TGLExt.ThermodynamicFriedmann TGLExt.SectorRouteComparison TGLExt.AuditThermodynamics TGLExt.ReviewThermodynamics`. Os três arquivos autorais foram copiados em bytes, sem objetos; mais auditor próprio com `#check`, `pp.universes` e `#print axioms`. Os três .oleans finais são byte a byte iguais aos autorais. **Quatro objetos novos; 113 objetos próprios anteriores preservados; total 117.** Fontes, traces, relatórios e pins protegidos B1/B2/B3 foram relidos e não mudaram.

Mathlib e oito pacotes auxiliares continuam o cache herdado pinado em B1/B2; não foram recompilados. Toolchain Lean 4.31.0 pinada no run. Nenhum build de projeto autoral no LEAN_PATH. Configuração Git segura limitada aos caminhos privados no ambiente do processo, sem alteração global. Nenhuma falha nesta execução Lake B4.

Ficha MD/JSON lida integralmente; {len(providers)} fornecedores conferidos por hash/linha. A ficha antecede as fontes nos metadados locais medidos; isso não equivale a selo externo de tempo. A comparação com a ORDEM 012, linhas 125–141, está no JSON. As buscas da ficha são históricas, não novas buscas exaustivas; locadores Python são propostas de consumidor, não integração revisada.

`AUDITORIA_B4.json` e fontes/streams dos negativos foram relidos: omitir Phi (`BadThermodynamicFactor`) e inverter o sinal beta·variância (`BadVarianceSign`) falham por **Type mismatch**, com imports funcionando. São execuções autorais lidas e pinadas, não execuções minhas adicionais. Seu mapa de 28 axiomas coincide com o próprio. A alegação de preservação dos 941 arquivos-base e um.py é [DECLARADO] no auditor autoral; não se refez inventário amplo.

## Pins e saídas

| Arquivo | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---|---|
{table}

- [Revisão JSON](<{(OUT/'REVIEW_B4_FINAL.json').as_posix()}>) — `{pin(OUT/'REVIEW_B4_FINAL.json')['sha256']}`.
- [Compilação própria](<{(OUT/'compilation.json').as_posix()}>) — `{pin(OUT/'compilation.json')['sha256']}`.
- [Run rc0](<{(A/'run.json').as_posix()}>) — `{pin(A/'run.json')['sha256']}`.
- [Snapshot](<{(A/'snapshot.json').as_posix()}>) — `{pin(A/'snapshot.json')['sha256']}`.
- [Ficha/contrato](<{(A/'contract_and_fiche.json').as_posix()}>) e [inspeção semântica](<{(A/'semantic_inspection.json').as_posix()}>).

## Alvos auditados

{targetlist}

**Encerrado o DEV B4 delimitado.** Sem pendência de recompilação ou análise destes 28 alvos. Integração, gate, B5/B6, escolha de rota, A1, fecho global, experimentos e atualização de memórias não integram este aceite. Nenhum arquivo autoral/canônico foi alterado.
'''
save(OUT/'REVIEW_B4_FINAL.md',md,True)
print(json.dumps(dict(status=evidence['status'],P0=[],P1=[],P2=[],report=pin(OUT/'REVIEW_B4_FINAL.md'),json=pin(OUT/'REVIEW_B4_FINAL.json'),compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),target_count=28),ensure_ascii=False,indent=2))
