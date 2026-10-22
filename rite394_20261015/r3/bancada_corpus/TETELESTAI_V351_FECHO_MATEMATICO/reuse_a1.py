from pathlib import Path
import re, json, hashlib
ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'TETELESTAI_V350_KERNEL_20260911'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(path, text):
 b=text.encode('utf-8')
 if path.exists(): raise RuntimeError(f'Refusing overwrite {path}')
 temp=path.with_suffix(path.suffix+'.tmp'); temp.write_bytes(b)
 assert temp.stat().st_size==len(b)
 temp.replace(path)
def save(name,data): write(ROOT/name,json.dumps(data,ensure_ascii=False,indent=2))

specs=[
 ('TGL/ModularRealization.lean','structure ContinuousCoreData','ADAPTAR','O contrato legado recebe Core→ENNReal sem cone positivo, fidelidade, normalidade ou semifinitude. O novo tipo restringirá o peso a PositiveCoreInput P; não se afirmará conversão automática ao legado.'),
 ('TGL/ModularRealization.lean','structure ThreeLocksCoreData','CONSUMIDOR','Consumidor posterior A2: PF_trace_pos e PF_trace_finite precisam do mesmo traço.'),
 ('TGLExt/V350CoreContractCounterexample.lean','def zeroTraceLegacyCore','REUSAR','Sonda negativa: refutar a restrição zero no novo contrato. A prova antiga só refuta ThreeLocks, não fortalece o core.'),
 ('TGLExt/V350RegularGeneratedAlgebra.lean','def regularCoreAlgebra','REUSAR','Mesma álgebra concreta; não reconstruir produto gerado.'),
 ('TGLExt/V350RegularDualAction.lean','def regularDualAction','REUSAR','Mesma ação dual concreta; a operação no cone usa regularDualAction_apply e dualAmbient_nonneg.'),
 ('TGLExt/V350RegularNormality.lean','theorem regularCoreEmbedding_preserves_positive_directed_isLUB','REUSAR','Normalidade da inclusão já paga; não é a normalidade do traço.'),
 ('TGLExt/V350DualFixedWeightLaws.lean','abbrev PositiveCoreInput','REUSAR','Cone positivo exato, adição e escala já definidos neste arquivo.'),
 ('TGLExt/V350ScalarDualWeight.lean','def scalarDualWeight','REUSAR','Peso ν concreto de partida. Não casa com traço: invariância dual não é escala e^-s.'),
 ('TGLExt/V350ScalarDualWeight.lean','theorem scalarDualWeight_normal','REUSAR','Normalidade por IsLUB interno já provada para ν; preservação na perturbação ainda exigida.'),
 ('TGLExt/V350ScalarDualWeight.lean','theorem scalarDualWeight_faithful','REUSAR','Fidelidade já provada para ν.'),
 ('TGLExt/V350ScalarDualWeight.lean','theorem scalarDualWeight_square_finite_strong_density','REUSAR','Ideal finito fortemente denso de ν. Não identificar isso por rfl com semifinitude por minorantes positivos de τ.'),
 ('TGLExt/V350RegularScalarWeightCertificate.lean','theorem regularScalarWeightCertificate','REUSAR','Agrega leis já provadas. Explicitamente não fornece KMS nem traço.'),
 ('TGLExt/V350DualWeightForm.lean','theorem dualQuadraticIntegral_dual_invariant','REUSAR','Ponte para demonstrar que renomear ν como τ falha na escala dual.'),
 ('TGLExt/V350RegularFiniteWeight.lean','theorem regularAverage_dualQuadraticIntegral','REUSAR','Valor finito explícito sobre quadrado de média: testemunha contra troca de ν por τ.'),
 ('TGLExt/SemifiniteSeed.lean','theorem matrix_trace_is_faithful_weight','NAO_CASA','Matrizes reais finitas; não fornece N(P)+→ENNReal nem escala dual.'),
 ('TGLExt/DimensionTrace.lean','def dimTraceData','NAO_CASA','Reticulado de subespaços reais finitos; tipo distinto do cone positivo de N(P).'),
 ('TGLExt/BreuerTrace.lean','theorem opWeight_star_mul_self_comm','NAO_CASA','Traço padrão de B(ellTwo), não o traço semifinito de N(P) com ação dual prescrita.'),
 ('TGLExt/LocalBreuerGap.lean','structure SemifiniteTraceData','NAO_CASA','Peso fiel/monótono em reticulado: nome não fornece normalidade e semifinitude no core.')]

records=[]
for rel,decl,decision,reason in specs:
 p=ROOT/'kernel'/rel; raw=p.read_bytes(); lines=raw.decode('utf-8').splitlines()
 starts=[i for i,l in enumerate(lines) if re.match(re.escape(decl)+r'(?:\s|\(|\{|:|$)', l)]
 assert len(starts)==1,(rel,decl,starts)
 i=starts[0]; block=[]
 for l in lines[i:]:
  block.append(l)
  if ':=' in l or l.rstrip().endswith('where'): break
 records.append(dict(file=str(p),line=i+1,sha256=sha(raw),declaration=decl,statement='\n'.join(block),decision=decision,reason=reason))

paths=(ROOT/'search_other_workshops.txt').read_text(encoding='utf-8-sig').splitlines()
distinct={}
for s in paths:
 p=Path(s); raw=p.read_bytes(); h=sha(raw)
 distinct.setdefault(h,dict(file=str(p),sha256=h,other_paths=0))['other_paths']+=1
save('OUTRAS_BANCADAS_HASHES.json',list(distinct.values()))

lines=(ROOT/'um.py').read_text(encoding='utf-8-sig').splitlines()
consumers=[]
for name in ['qgf_continuous_modular_realization_constructed','evaluate_v350_kernel_frontier','canonicalFullTGLWitness']:
 hits=[dict(line=i+1,text=l) for i,l in enumerate(lines) if name in l]
 consumers.append(dict(name=name,file=str(ROOT/'um.py'),occurrences=hits))

data=dict(status='FICHA_ANTES_DO_CODIGO_FORMAL',target='A1',sources=records,consumers=consumers,
 required_type='Para todo P:SiteProfile, τ:PositiveCoreInput P→ENNReal com zero, adição, homogeneidade NNReal, monotonia, fidelidade, normalidade IsLUB, semifinitude por supremo de minorantes positivos finitos, τ(a*a)=τ(aa*) e τ(regularDualAction P s A)=ofReal(exp(-s))*τ(A). Canonicalidade exige adicionalmente τ=(ν)_(h^-1), h^(it)=regularUnitary P t, não apenas escolher uma normalização arbitrária.',
 decision='NOVO: contrato forte e suas recusas; REUSAR: cone, álgebra, ação, normalidade/ideal/peso existentes. ADAPTAR: ponte modular/perturbação do peso para τ. Não construir nova teoria genérica sem necessidade.',
 external_workshops=dict(matching_paths=len(paths),distinct_byte_hashes=len(distinct),limitation='Busca rg retornou acessos negados em diretórios de dependências Python; nenhum desses diretórios é fornecedor Lean. Não afirmar inexistência global.'),
 literature=dict(url='https://arxiv.org/pdf/2004.02383',sections=['9.4','9.9','10.13','10.15'],status='KNOWN: consultado; não é termo Lean'),
 limits=['A busca inicial do acervo foi truncada em 50 ocorrências históricas; exige refinamento Pedersen-Takesaki, não prova ausência.', 'Bancada TOE: único arquivo por padrão foi FrontierCertificate.lean, contrato não construtor de traço.', 'Mathlib Analysis: busca dos nomes dá subespaços padrão e homônimos; não identifica implementação do teorema de perturbação.', 'DEV não reativado: nenhum módulo suspenso fornece τ no cone positivo com escala dual.'],
 stopping_rule='Contrato compilado não é habitante. Falha de provedor não é impossibilidade matemática. Registrar precisamente o lema faltante e manter b NÃO PAGO se não houver construção nem parede contra sua existência.')
save('REAPROVEITAMENTO_A1.json',data)
md=['[REAL — ficha de reaproveitamento por leitura; nenhuma nova prova declarada]\n','# A1 — traço no core regular da mesma torre\n',data['required_type']+'\n',data['decision']+'\n','## Fornecedores e tipos\n']
for r in records:
 md += [f"### {r['declaration']} — {r['decision']}\n",f"[{Path(r['file']).name}](<{r['file']}:{r['line']}>) · SHA256 `{r['sha256']}`\n",r['reason']+'\n','```lean\n'+r['statement']+'\n```\n']
md += ['## Consumidor e alcance\n','A1 fornece o traço para A2, que fornece o core/ThreeLocks compatíveis a A5. A bandeira qgf_continuous_modular_realization_constructed não vira True por esta ficha. Localizadores exatos de todas as ocorrências estão no JSON. O gate principal pago permanece intacto.\n','## Busca e limites\n',f"922 arquivos embutidos (918 Lean), buscas registradas em BUSCAS_A1.json; {len(paths)} caminhos correspondentes em outras bancadas, {len(distinct)} hashes distintos.\n"]
md += ['- '+x+'\n' for x in data['limits']]
md += ['\n'+data['stopping_rule']+'\n','\nConvenção: Λ_t=h^(it), L=log h desloca L−s; K=−log h desloca K+s. O traço é a perturbação ν_(h^-1); não trocar sinais nem inferir normalização da lei de escala.\n']
write(ROOT/'REAPROVEITAMENTO_A1.md','\n'.join(md))
print(json.dumps(dict(providers=len(records),other_paths=len(paths),other_distinct=len(distinct),sheet_sha256=sha((ROOT/'REAPROVEITAMENTO_A1.md').read_bytes())),indent=2))
