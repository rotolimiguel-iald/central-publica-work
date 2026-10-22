from pathlib import Path
from datetime import datetime
import hashlib,json,os,re
O=Path(__file__).resolve().parent;R=O.parent;V=R/'v';M=V/'.lake/packages/mathlib/Mathlib'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.parent==O and not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
specs=[
 (V/'TGLExt/V351ScalarGNSClosedness.lean',['scalarGNSCutMap_weight_embedding','scalarWeightGNSEmbedding_of_cut_actions']),
 (V/'TGLExt/V351ScalarRightActionLimits.lean',['scalarRightAction_regular','scalarRightAction_closed_of_bounded_strongStar']),
 (V/'TGLExt/V350AntiunitaryPositiveConjugation.lean',['antiunitaryConjugate_apply','antiunitaryConjugate_mul']),
 (V/'TGLExt/V350ScalarGNSAction.lean',['scalarGNSAmbientAction_norm_le']),
 (V/'TGLExt/V350ScalarGNSRepresentation.lean',['scalarGNSRepresentation']),
 (V/'TGLExt/V350StrongOperatorField.lean',['operatorFieldLift_norm_le']),
 (V/'TGLExt/V350DualWeightCuts.lean',['dualIntegralFamily']),
 (V/'TGLExt/V350L2CharacterMultiplier.lean',['characterPhase','characterMultiplier_ae']),
 (V/'TGLExt/V351RegularPositiveGraph.lean',['regularSpectralCoordinates','regularSpectralResolvent']),
 (V/'TGLExt/V351RegularImaginaryPowers.lean',['regularSpectralCoordinates_character']),
 (V/'TGLExt/V351ScalarMultiplierCalculus.lean',['compactScalarRepresentation','realScalarMultiplier_cfc_ae']),
 (V/'TGLExt/V351InverseGeneratorCutoff.lean',['regularInverseGeneratorCutoff_graph_iff']),
 (M/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Range.lean',['cfc_mem']),
 (M/'Analysis/VonNeumannAlgebra/Basic.lean',['centralizer_centralizer']),
 (M/'Topology/Algebra/Group/Basic.lean',['Set.isClosed_centralizer']),
 (M/'Topology/Constructions.lean',['IsClosed.isClosedEmbedding_subtypeVal','IsClosed.isClosedMap_subtype_val']),
 (M/'Analysis/SpecialFunctions/Trigonometric/Deriv.lean',['hasDerivAt_sin']),
 (M/'Analysis/SpecialFunctions/Sigmoid.lean',['continuous_sigmoid'])]
providers=[]
for p,names in specs:
 text=p.read_text(encoding='utf8');lines=text.splitlines();locs=[]
 for name in names:
  hits=[dict(line=i+1,header=l) for i,l in enumerate(lines) if re.search(r'\b(?:def|theorem|lemma)\s+'+re.escape(name)+r'(?=[\s({:])',l)]
  assert hits,(p,name);locs.append(dict(name=name,locations=hits))
 providers.append(dict(source=pin(p),declarations=locs))
date=datetime.now().astimezone().isoformat()
body=r'''# Consulta — ação direita fechada, CFC e aproximantes por seno

[DERIVED — análise matemática e interfaces locais; nenhuma implementação ou compilação desta rota.]

A proposta é válida com as duas propriedades, de b e b*, e com o sinal abaixo. Ela oferece uma rota mais curta para o consumidor R do que a construção adicional por grafos/projeções: mantém diretamente o J original e fornece aproximantes explícitos. O fechamento GNS3 e os dois lemas de limites já foram reproduzidos em pareceres separados. Esta nota não aprova a fonte de álgebra ainda em DEV, nem acrescenta novos alvos aos aceites anteriores.

1. **A propriedade e a ordem do produto.** Escreva N=regularCoreAlgebra P, π=scalarGNSRepresentation P, J=scalarTomitaPolarFactor P e ρ(b)=Jπ(b*)J⁻¹. A função ρ é complexa-linear em b porque as duas conjugações escalares se cancelam; é antirrepresentação: ρ(bc)=ρ(c)ρ(b), e ρ(b*)=ρ(b)*. Isso não exige comutatividade de N nem igualdade global de comutantes. Seja P(b) a identidade, para TODO a∈nν, de pertença ab∈nν e Λν(ab)=ρ(b)Λν(a). Para produto, primeiro use P(b) em a e depois P(c) em ab: Λν((ab)c)=ρ(c)ρ(b)Λν(a). O resultado tem exatamente a ordem de ρ(bc). Soma/escala/unidade usam a linearidade da inscrição e do ideal já existentes. NÃO se deve deduzir P(b*) de P(b) sem prova. Definir E={b∈N | P(b)∧P(b*)} torna legítima a estrela; no produto, a componente estrelada usa c*b* nessa ordem.

2. **Fechamento em norma sem novos vetores escolhidos.** Os dois teoremas dos cortes dão a equivalência exata

   P(b) ↔ ∀ a∈nν, ∀ n∈ℕ, C_n(ρ(b)Λν(a)) = D(ab)Ω_n,

   onde C_n=scalarGNSCutMap P n, D=dualOrbitRepresentation e Ω_n=scalarCutVacuum P n. O sentido direto é scalarGNSCutMap_weight_embedding; o reverso usa scalarWeightGNSEmbedding_of_cut_actions para o vetor já definido ρ(b)Λν(a). Assim não há tentativa de provar fechado um conjunto definido por uma escolha existencial descontínua. Para cada a,n ambos os lados são contínuos na NORMA de b. As cotas de operatorFieldLift/dualIntegralFamily dão ||D(b)||≤||b||; a restrição que define π preserva essa cota, e J é isométrico. A norma da estrela é contínua. A interseção de conjuntos isClosed_eq é fechada, mesmo sobre todos a; isso é interseção topológica, não interseção a.e. não enumerável. P e P∘star fechados dão E fechado em N.

3. **Levar E ao ambiente corretamente.** N é fechado na norma do CLM porque N=(N′)′ e Set.isClosed_centralizer vale para qualquer conjunto no ambiente Hausdorff com multiplicação separadamente contínua. A inclusão de N é uma closed embedding, por IsClosed.isClosedEmbedding_subtypeVal; sua imagem de E fechado é fechada, por IsClosed.isClosedMap_subtype_val. Não se está usando a afirmação falsa de que toda imagem contínua de fechado é fechada. E.map N.subtype é uma StarSubalgebra ℂ de B(H_regular) fechada. cfc_mem, em Range.lean, recebe exatamente esse IsClosed local e o elemento pertencente: não pede CompleteSpace N nem WStarAlgebra N. O CFC é feito no B(H_regular) completo já disponível. O transporte de volta ao subtipo é uma igualdade/injetividade da inclusão, não uma nova equivalência de álgebras de von Neumann.

4. **Sinal e aproximação concretos.** Use m=n+1>0 e U_t=regularUnitary P t. A fonte characterPhase é exp(−i s ξ), e regularSpectralCoordinates_character fornece V⁻¹U_t V=M_exp(−i 2πtξ). Logo a escolha

   A_m = (m/(2i))·(U_(−1/m) − U_(1/m))

   tem símbolo +m sin(2πξ/m), e é auto-adjunta. Inverter a ordem produz o sinal oposto. Se k significar log h, seu símbolo é −2πξ: nesse vocabulário R=sigmoid(−k), não sigmoid(k). Evite introduzir um novo operador log apenas para nomear a aproximação. A convenção acima já fixa o símbolo positivo desejado para R.

   Para reutilizar SEM GENERALIZAR o fornecedor realScalarMultiplier_cfc_ae, ponha

   X_m=(I+A_m/m)/2,  g_m(ξ)=(1+sin(2πξ/m))/2,
   f_m(z)=ofReal(sigmoid(m·(2 Re z−1))),  R_m=cfc f_m X_m.

   X_m∈E, tem símbolo g_m∈[0,1] e 0≤X_m≤I. O fornecedor existente exige precisamente um g contínuo entre 0 e 1; aplicá-lo diretamente a m sin seria erro de hipótese. Aplicá-lo a g_m, usando a naturalidade do CFC pela mesma V, dá o símbolo

   q_m(ξ)=sigmoid(m sin(2πξ/m)).

   A função f_m é globalmente contínua em ℂ, compatível com a hipótese explícita do fornecedor. cfc_mem dá R_m∈E; positividade e cota R_m≤I também seguem de 0≤q_m≤1 e do multiplicador positivo já existente. A pertença dos U_± a E vem do novo scalarRightAction_regular, aplicado também a −t e à identidade de estrela do grupo. Nenhuma geração forte abstrata foi assumida.

5. **Limite forte-* realmente suficiente.** Para cada ξ fixo, m sin(2πξ/m)→2πξ, pela derivada de sin em zero, portanto q_m(ξ)→sigmoid(2πξ). Para cada u∈L² vetorial, ||(q_m(ξ)−q(ξ))u(ξ)||²≤||u(ξ)||². DCT em norma² dá a convergência forte dos multiplicadores; conjugação pela MESMA V dá R_m→regularSpectralResolvent P. Como R_m e R são auto-adjuntos, os adjuntos convergem fortemente sem invocar continuidade forte geral da estrela. A cota uniforme é 1. O teorema scalarRightAction_closed_of_bounded_strongStar agora produz P(R), e a auto-adjunção dá R∈E. Não se afirma convergência na norma de operadores, monotonia dos R_m ou cota uniforme dos A_m. As oscilações do seno no infinito impedem inferir essas propriedades da convergência pontual; nenhuma delas é necessária.

6. **O consumidor sqrt(Bε) não pode ser só homônimo.** Para ε>0, o cálculo esperado no MESMO R é

   Bε = cfc (x ↦ x/(1+(ε−1)x)) R,
   sqrt(Bε) = cfc (x ↦ sqrt(x/(1+(ε−1)x))) R.

   No espectro [0,1], 1+(ε−1)x≥min(1,ε)>0. Resta provar a primeira igualdade com regularInverseGeneratorCutoff já definido, não criar outro corte com o mesmo nome. Uma ponte curta usa Dε=I+(ε−1)R, sua inversibilidade pela cota, o par (R y,(I−R)y) do grafo h e regularInverseGeneratorCutoff_graph_iff: em y=Dε⁻¹x, a soma da segunda componente com ε vezes a primeira é x, logo Bε x=R Dε⁻¹x. CFC identifica essa expressão racional. A segunda igualdade usa unicidade da raiz positiva ou composição CFC. A função racional tem apenas continuidade garantida no espectro; se o adaptador escolhido exigir continuidade global, deve-se estendê-la explicitamente, sem tratar o denominador como não nulo em toda ℝ. Por exemplo substituir o denominador por max(min(1,ε),1+(ε−1)x) fornece extensão contínua que coincide em [0,1]. A raiz real continua globalmente contínua. Depois cfc_mem e R∈E dão a ação direita desse sqrt(Bε), com o J original.

**Próximas obrigações concretas [OPEN].** (i) equivalência pelos cortes, leis e fechamento de E/map — fonte autoral em DEV, não examinada como final; (ii) identidade espectral do X_m, CFC do símbolo e DCT forte-* do R_m; (iii) consumo do lema de limites para R; (iv) igualdade do corte racional com o Bε existente e sua raiz. Nenhuma exige Schwartz, Fourier-L¹, Kaplansky, novo GNS, novo J ou novos domínios máximos. Em comparação, a rota por grafos/projeções exigiria adaptadores de representação diagonal e geração adicionais; não é necessária para este consumidor se a construção acima for implementada. Tracialidade, ordem das avaliações perturbadas e conclusão de A1(b) permanecem separadas; esta nota não as paga e não move gate.

Fornecedores e localizadores abaixo são lidos nesta consulta; seus hashes completos estão no JSON acompanhante. A lista é delimitada, não uma busca exaustiva. Nenhuma fonte autoral, memória ou parecer anterior foi alterado.
'''
table='\n| Fonte | Declaração e linha lidas |\n|---|---|\n'
for p in providers:
 for d in p['declarations']:
  for h in d['locations']:
   table+='| ['+Path(p['source']['path']).name+'](<'+p['source']['path']+':'+str(h['line'])+'>) | `'+d['name']+'` — '+str(h['line'])+' |\n'
md=body.replace('\n\n', '\n\n',1)+'\nData: '+date+'\n'+table
mp=O/'CONSULTA_CFC_SENO_ACAO_DIREITA.md';fresh(mp,md.encode('utf8'))
data=dict(timestamp=date,status='DERIVED__READ_ONLY_CONSULTATION__NOT_LEAN_ACCEPTANCE',new_lean_targets=0,new_builds_for_consultation=0,providers=providers,note=pin(mp),review_already_completed=pin(R/'revisao_limites_direita/REVIEW_A1_RIGHT_ACTION_LIMITS_FINAL.md'),open_items=['Closed star subalgebra and ambient CFC adapter','Normalized sine symbols and dominated strong-star convergence','Right-action limit at the original R','Rational identity with existing inverse cutoff and square root','Weight perturbation and trace'],source_unchanged=True,memories_modified=False)
jp=O/'CONSULTA_CFC_SENO_ACAO_DIREITA.json';fresh(jp,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
for rec in providers:assert pin(Path(rec['source']['path']))==rec['source']
print(json.dumps(dict(md=pin(mp),json=pin(jp)),ensure_ascii=False))
