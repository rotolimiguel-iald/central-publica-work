from pathlib import Path
import json,hashlib,os,re
from datetime import datetime
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
K=R/'k'; O=R/'consulta_A2_CONTRATO';O.mkdir(exist_ok=True)
ORDER=R.parents[1]/'TUNEL/PARA_CHATGPT/ORDEM_011_fecho_matematico_da_realizacao_concreta.md'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(n,b):
 p=O/n;assert not p.exists(),p;t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def ref(rel,needle,endneedle=None,count=15):
 p=K/rel;s=p.read_text(encoding='utf-8-sig');ls=s.splitlines();indexes=[i for i,x in enumerate(ls) if needle in x and not x.lstrip().startswith(('*','--'))];assert indexes,(rel,needle);i=indexes[0]
 end=i+count
 if endneedle:
  end=next(j for j in range(i+1,len(ls)) if endneedle in ls[j])
 return dict(source=pin(p),line=i+1,locator=needle,excerpt='\n'.join(ls[i:end]))
refs=[
 ref('TGL/ModularRealization.lean','structure ContinuousCoreData','attribute [instance]'),
 ref('TGL/ModularRealization.lean','structure ThreeLocksCoreData','/-- A realizacao modular'),
 ref('TGL/CoreSupport.lean','noncomputable def threeLocksFromSupport',count=31),
 ref('TGL/CoreSupport.lean','theorem support_maximal',count=3),
 ref('TGL/VerbInhabitant.lean','theorem dual_calibration_exists',count=17),
 ref('TGLExt/SusyRelativeGap.lean','structure SubadditiveTraceData',count=18),
 ref('TGLExt/SusyRelativeGap.lean','theorem susy_relative_gives_breuer',count=4),
 ref('TGLExt/SusyRelativeGap.lean','def modelSusy',count=14),
 ref('TGLExt/SpectralReduction.lean','def SpectralApproximationWitness',count=4),
 ref('TGLExt/SpectralReduction.lean','theorem concrete_breuer_corner_conditional',count=12),
 ref('TGLExt/SemifiniteSeed.lean','theorem matrix_trace_is_faithful_weight',count=6),
 ref('TGLExt/TheNonMinimalCoupling.lean','theorem split_forbids_minimality',count=9),
 ref('TGLExt/TheNonMinimalCoupling.lean','theorem the_split_is_inhabited',count=7),
 ref('TGLExt/V351RegularCoreTraceContract.lean','structure RegularCoreTraceData',count=24),
 ref('TGLExt/V351RegularCoreTraceConstruction.lean','def scalarInverseLimitTraceData',count=12),
 ref('TGLExt/V351InverseLimitFiniteMinorants.lean','theorem scalarInverseLimitWeight_finite_contractions',count=5),
 ref('TGLExt/V351InverseLimitFiniteMinorants.lean','theorem scalarInverseLimitWeight_finite_minorants',count=8),
 ref('TGLExt/V351InverseLimitScaling.lean','theorem scalarInverseLimitWeight_dual',count=4),
 ref('TGLExt/V351InverseLimitFaithful.lean','theorem scalarInverseLimitWeight_faithful',count=3),
 ref('TGLExt/V350UnitIntervalProjection.lean','theorem unitIntervalProjection_idempotent',count=2)
]
# Pin the counterexample source and relevant lines, without interpreting a generic zero model as the new trace.
cp=K/'TGLExt/V350CoreContractCounterexample.lean';cs=cp.read_text(encoding='utf-8-sig').splitlines()
refs.append(dict(source=pin(cp),line=12,locator='legacy zero model; incompatibility with positive ThreeLocks',excerpt='\n'.join(cs[11:43])))
prev=R/'revisao_tracialidade_quadratica/compilation.json';comp=json.loads(prev.read_bytes());objmap={x['module']:x for x in comp['objects']}
for row in refs:
 mod=str(Path(row['source']['path']).relative_to(K).with_suffix('')).replace('\\','.').replace('/','.')
 if mod in objmap:
  x=objmap[mod];assert pin(Path(x['source']['path']))['sha256']==row['source']['sha256'];assert pin(Path(x['own']['path']))==x['own'];assert pin(Path(x['trace']['path']))==x['trace']
  row['previous_own_compilation']=dict(object=x['own'],trace=x['trace'],used_as_A2_acceptance=False)
 else:row['previous_own_compilation']=dict(located_in_previous_compilation=False,used_as_A2_acceptance=False)
orderlines=ORDER.read_text(encoding='utf-8-sig').splitlines();a2=next(i for i,x in enumerate(orderlines) if x.startswith('### A2'))
consolidation=[pin(R/('CONSOLIDACAO_A1B_20260915'+ext)) for ext in ['.md','.json']]
stamp=datetime.now().astimezone().isoformat()
findings=[
 dict(id='A2-TYPE',status='REAL_READ__BRIDGE_OPEN',claim='A1 value has domain PositiveCoreInput P; ContinuousCoreData.canonicalTrace has domain the whole Ring Core and requires cyclicity on arbitrary xy/yx. No literal coercion or generic adapter was found in the scoped sources.'),
 dict(id='A2-SQUARE-EXTENSION',status='DERIVED_COUNTEREXAMPLE_NOT_LEAN',claim='x->tau(x*x) and x->tau(abs x) fail arbitrary-product cyclicity: in M2, p=e11 and n=e12 give pn=n,np=0; the first value at n is tau(e22)>0 and the second likewise. This refutes those adapters, not existence of every possible extension.'),
 dict(id='A2-LEGACY-CONSISTENCY',status='REAL_READ__NO_GLOBAL_IMPOSSIBILITY_CLAIM',claim='The legacy contract does not require additivity/complex linearity on the whole core. Its zero model exists, but cannot supply positive ThreeLocks. One cannot infer an inconsistency of the bare contract merely from codomain ENNReal.'),
 dict(id='A2-SUPPORT',status='REAL_SUPPLIER__PROJECTION_INSTANCE_OPEN',claim='finite_contractions returns a sequence of contractions with finite tau(E*E) and strong limit1, not idempotents. Finite minorants return positive inputs. No nonzero finite-trace projection in the actual regular core was identified in the consulted suppliers.'),
 dict(id='A2-SPLIT',status='INPUT_IN_CONSTRUCTOR__CONCRETE_INSTANCE_OPEN',claim='threeLocksFromSupport requires q,qp,qm, trace(q)=1, orthogonality and equal face trace. Matrix examples and lattice idTraceSub are not instances for the A1 core/trace.'),
 dict(id='A2-GAP',status='GENERIC_CONDITIONAL__CONCRETE_OPERATOR_OPEN',claim='SusyRelativeData assumes finite free-gap and difference, inclusion and nonzero kernel. SpectralReduction additionally receives a polynomial witness and uses semifiniteDimTrace on submodules, not scalarInverseLimitWeight.'),
 dict(id='A2-CALIBRATION',status='DERIVED_REUSE_TARGET',claim='dual_calibration_exists already receives ThreeLocksCoreData; using it to produce the support needed for that same constructor would be circular. Reuse the exp/log calculation directly with A1 dual_scaling once a finite nonzero projection is supplied.'),
 dict(id='A2-MINIMAL-REPRESENTATIVE',status='REAL_GENERIC__IDENTIFICATION_OPEN',claim='Hmin=1-q has algebraic kernel maximality by CoreSupport. Identifying it as a spectral zero projection and relating any specified effective continuous operators/domains still requires actual concrete data. Defining1-q alone does not establish an independently prescribed SUSY-relative gap.')
]
md=f'''{stamp}

# Consulta A2 — contrato legado, traço positivo e suporte

**[CONSULTA READ-ONLY — A2 NÃO ACEITO]** ORDEM012/B1–B6 e A1(b) estão entregues segundo a consolidação lida. Esta nota prepara A2 da ORDEM011. Não há Lean novo, build, execução de writer/monólito, alteração de memória ou artefato anterior. Busca limitada às fontes locais indicadas e ocorrências relacionadas em K; não é inventário exaustivo do acervo ou da bancada TOE.

**Conclusão:** A1 não preenche literalmente ContinuousCoreData. Existe uma obrigação de compatibilidade de domínios e ciclicidade do campo legado, além das entradas concretas de suporte/split/gap de A2. As construções consultadas não fornecem essas entradas já instanciadas no mesmo core. A parede demonstrável abaixo refuta adaptações naturais específicas; NÃO demonstra impossibilidade de todo o contrato nem exige sua alteração.

## 1. O pedido exato

ORDEM011:{a2+1}:

> {chr(10).join(orderlines[a2:a2+4])}

TGL/ModularRealization.lean:68–83 exige `Core : Type` com `Ring`, `StarRing`, `Algebra ℂ`, embedding injetivo da cunha, ação dual e:

```text
canonicalTrace : Core -> ENNReal
trace_zero : canonicalTrace 0 = 0
trace_tracial : forall x y, canonicalTrace(x*y)=canonicalTrace(y*x)
trace_star : forall x, canonicalTrace(star x)=canonicalTrace x
trace_dual_scaling : canonicalTrace(theta_s x)=ofReal(exp(-s))*canonicalTrace x
```

A1 fornece `scalarInverseLimitTraceData.{{u}} P : RegularCoreTraceData.{{u}} P`, cujo value é literalmente `scalarInverseLimitWeight P : PositiveCoreInput P -> ENNReal`. Seu campo tracial é igualdade entre `positiveSquare a` e `positiveSquare (star a)`. O cone positivo não é um anel: não pode ser escolhido como `Core` mantendo as operações exigidas. Não há coerção que converta a igualdade quadrática na igualdade de valores em produtos arbitrários, que podem não ser positivos.

A ponte necessária, sem reformular contrato, seria uma função total F:N->ENNReal acompanhada dos quatro campos legados e de uma igualdade explícita F(X)=tau(X) para todo X positivo do MESMO core; W,D e o embedding requerido continuam precisando casar por tipo. Esse é um alvo de adaptação, não uma hipótese a inserir para declarar A2 construído. Mesmo a igualdade em todos positivos é uma condição de identificação do traço A1, não um campo novo que esta consulta acrescenta ao contrato antigo.

## 2. Parede exata dos atalhos — e seu limite

[DERIVED — cálculo matemático, não novo teorema Lean] Em M2, tome p=e11 e n=e12. Temos pn=n, np=0, n* n=e22 e |n|=e22. Para qualquer traço positivo fiel tau, tau(e22)>0 (finitude nem é necessária). Logo F(x)=tau(x*x) satisfaz F(pn)>0=F(np); F(x)=tau(|x|) falha igualmente. Ambas coincidem com tau nas projeções, mas isso não basta para `trace_tracial`. Assim não usar o mapa quadrático de A1 como `canonicalTrace` para quitar o campo legado.

A extensão linear usual de um traço positivo é complexa no ideal integrável; ela não é automaticamente uma função ENNReal em TODO o anel. Também não se pode declarar valor infinito fora do ideal e esperar ciclicidade: produtos com um fator projetor podem dar n e zero no exemplo acima, inclusive quando n não é integrável numa amplificação infinita.

**Não concluo que o contrato legado seja impossível.** Ele não exige aditividade/linearidade em todo Core. Por exemplo, no caso matricial finito, x->|Tr(x)| é uma função ENNReal (via ofReal) cíclica, invariante por estrela e coincide com o traço nos positivos, embora não linear. Isso é ilustração de compatibilidade desses campos, não fornecedor da ação dual do core atual. O exemplo zero já está em V350CoreContractCounterexample, e o próprio arquivo prova que ele não fornece ThreeLocks com traço positivo. Portanto a lacuna é um adaptador legítimo ainda não localizado, não uma contradição deduzida do codomínio isoladamente.

## 3. Projeção finita e faces

[REAL — enunciados lidos] `scalarInverseLimitWeight_finite_contractions` devolve E_n em N, norm<=1, tau(E_n*E_n)<infinito e E_n->1 fortemente. Não devolve E_n^2=E_n. `scalarInverseLimitWeight_finite_minorants` entrega minorantes positivos finitos e agora recebe a tracialidade34 efetivamente paga. Não devolve automaticamente uma projeção espectral. `unitIntervalProjection_idempotent` é uma projeção no Hilbert regular; o resultado lido não inclui pertinência ao core nem traço A1 finito.

[DERIVED/OPEN — menor entrada útil] Extrair de um positivo finito não nulo uma projeção espectral de limiar q, com 0<q e c*q<=X para algum c>0, pagaria tau(q)<=tau(X)/c<infinito. A1 já paga a parte de ordem/fidelidade; falta um fornecedor concreto para essa extração no mesmo N, com pertinência e idempotência. Não reabrir a construção do peso. Semifinitude/fidelidade não tornam uma projeção arbitrária escolhida divisível em faces iguais; em particular uma projeção minimal não serve ao split exigido.

Uma possível economia, ainda DERIVED/OPEN: escolher a projeção finita e sob e11 de um sistema matricial já representado e usar uma parcial isometria v com v*v=e11 e vv*=e22. Então e e v e v* são ortogonais e têm o mesmo traço pela igualdade quadrática A1; q=e+v e v* tem traço positivo finito. **Não localizei nesta consulta a escolha dessa e com domínio/pertinência/traço já provados**, nem declaro preenchidos os dados matriciais correspondentes. Essa rota evita exigir um teorema global de divisibilidade de toda projeção, mas permanece candidato de aplicação, não fornecedor pronto.

A calibração para tau(q)=1 pode usar theta_(log tau(q).toReal), preservando as projeções e o split. O lema antigo `dual_calibration_exists` recebe um ThreeLocksCoreData pronto; chamá-lo para produzir o q necessário ao mesmo construtor seria circular. Reusar sua conta exp/log diretamente com `scalarInverseLimitWeight_dual` depois de obter q é a dependência correta.

[DERIVED — parede de escolha] Qualquer projeção não nula que seja FIXA pela ação dual não pode ter traço A1 positivo finito: tau(q)=exp(-1)*tau(q) força tau(q) em {{0,infinito}}; fidelidade exclui zero. Portanto usar uma projeção de uma subálgebra fixa só por ser matricial não paga PF. A aplicação a uma projeção concreta requer exibir que ela é fixa; não presumi isso de um nome.

## 4. Gap e projeção do zero: o que as assinaturas realmente dizem

`threeLocksFromSupport` recebe todo o suporte e split, incluindo tau(q)=1. Atribui H3Lt=1-q e prova aniquilação/maximalidade por álgebra. Isso é reutilizável depois de fornecer os dados, mas não produz o suporte. `ThreeLocksCoreData` não tem campo numérico de gap nem domínio de operador ilimitado; codifica transformada limitada e maximalidade. A2, além desse termo, exige identificação com os operadores contínuos efetivos e sua projeção espectral. Não substituir essa identificação pela escolha de um homônimo.

Para Hmin=1-q atuando no Hilbert, a decomposição por uma projeção ortogonal fornece ker(Hmin)=range(q) e Hmin é identidade no complemento: a estimativa de gap é elementar para ESSE representante. Ligá-lo a um operador Three Locks previamente especificado é uma obrigação separada; a consulta não inventa esse operador nem afirma que ele já coincide.

`SusyRelativeData` é reticular e recebe `free_gap_finite`, `gap_relative`, `diff_finite`, `ker_le_gap`, `ker_ne_bot`. `susy_relative_gives_breuer` é a implicação depois desses dados. O modelo `modelSusy` mora em ENNReal com peso identidade; não é uma instanciação no core de A1. A camada `SubadditiveTraceData` ainda pede subaditividade sobre sup reticular; aditividade de tau em positivos não constitui sozinha esse adaptador de projeções.

`concrete_breuer_corner_conditional` recebe auto-adjunção, `SpectralApproximationWitness`, kernel não trivial e inclusão do kernel em subespaço FINITO-DIMENSIONAL. A conclusão usa `semifiniteDimTrace` em submódulos, não tau=scalarInverseLimitWeight. Uma projeção tau-finita pode ter dimensão Hilbert infinita. Não transportar essa conclusão por homonímia nem cobrar dimensão finita desnecessariamente do core.

`SemifiniteSeed.matrix_trace_is_faithful_weight` trata matrizes reais finitas; `TheNonMinimalCoupling.the_split_is_inhabited` trata M2. São provas genéricas/concretas em outros tipos. Nenhuma é o consumidor A2 instanciado no mesmo N/traço. O resultado `split_forbids_minimality` explica por que um candidato de posto um sozinho não paga faces não nulas iguais.

## 5. Próximo passo mínimo e estatutos

1. **OPEN — fronteira de tipos:** nomear o adaptador de traço total exigido pelo legado e sua identificação com A1 nos positivos; não preencher com quadrados, módulo ou zero sem provar ciclicidade. Não propor alteração silenciosa do contrato.
2. **OPEN — dados consumíveis:** fornecedor de projeção não nula tau-finita no mesmo core, split ortogonal de traço igual e calibração; reusar A1 para ordem/fidelidade/tracialidade/escala.
3. **REAL genérico / OPEN concreto:** aplicar CoreSupport depois desses dados e provar a identificação espectral/domínios para o representante admitido por A2. Reusar os resultados genéricos de gap somente quando seus tipos forem realmente instanciados com tau e os operadores efetivos.

Nenhum aceite A2 nesta consulta. A consolidação mantém A2–A7 separados. ORDEM012 já entregue não é reaberta. Ausência no recorte lido não é ausência universal do acervo. As primeiras tentativas de localização CoreSupport/ModularRealization em TGLExt falharam e foram corrigidas para TGL; um padrão de glob Windows passado como caminho literal foi recusado e não foi contado como busca negativa de provas.

## Fontes, tipos e pins relidos
'''
for i,row in enumerate(refs,1):
 p=row['source'];md+=f"\n### {i}. {row['locator']}\n\n[{Path(p['path']).name}:{row['line']}](<{p['path']}:{row['line']}>) — {p['bytes']} bytes; SHA256 `{p['sha256']}`.\n\n```lean\n{row['excerpt']}\n```\n"
md+='\nA proveniência de objetos anteriores, quando encontrada, está no JSON; ela não é aceite A2. Nenhum build foi executado nesta consulta.\n'
checks=dict(timestamp=stamp,status='A2_CONTRACT_REUSE_CONSULTATION__NO_A2_ACCEPTANCE',order=pin(ORDER),order_A2_line=a2+1,consolidation=consolidation,previous_A1_review_compilation=pin(prev),scope=dict(no_lean_written=True,no_build=True,no_writer=True,no_memory_changes=True,A2_accepted=False,exhaustive_search=False,gate_changed=False),findings=findings,sources=refs,search_scope=['Explicit files requested under R/k','Scoped rg in R/k/TGL and R/k/TGLExt for ThreeLocks constructors, PF trace and projection providers','Previously accepted A1 compilation pins, read-only'],not_searched_exhaustively=['TOE','entire archive','all deliveries','Mathlib'],risks_not_claimed=['No global impossibility theorem for ContinuousCoreData','No instantiated finite projection/split/gap in A1 core','No actual Lean counterexample newly proved'])
fresh('CONSULTA_A2_CONTRATO.md',md.encode('utf-8'))
checks['report']=pin(O/'CONSULTA_A2_CONTRATO.md')
fresh('CONSULTA_A2_CONTRATO.json',(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(report=pin(O/'CONSULTA_A2_CONTRATO.md'),json=pin(O/'CONSULTA_A2_CONTRATO.json'),sources=len(refs),A2_accepted=False),ensure_ascii=False))
