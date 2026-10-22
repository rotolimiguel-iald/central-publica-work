# Revisão matemática adversarial — rota ShiftRelated / leitura total

**[DERIVED — demonstração matemática abaixo, não compilação Lean] A compatibilidade positiva proposta é verdadeira para operadores limitados no mesmo von Neumann algebra, com tracialidade quadrática no cone. O supremo não infla o valor de nenhum positivo. [OPEN] A ponte analítica ainda requer construção e revisão formal; este parecer não conclui A2.**

Carver, agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`, revisor independente convocado pela principal; identidade recebida [INPUT]. Autoria da rota e implementação permanecem com a principal/Poincare. Escrita exclusiva desta revisão em `C:\IALD\Central de Patentes\Chatgpt\REVISAO_A2_012\TRACE_COMPLETION_012`. Nenhum dos 33 lemas pagos foi reaberto, alterado ou recompilado. Nenhum wrapper ou fonte Lean foi criado.

Considere um Hilbert complexo H, um von Neumann algebra unital M ⊆ B(H), p,q ∈ M positivos e r,s ∈ M. Suponha n ∈ ℕ, n ≥ 1, e

\[
pr=rq,\qquad sp=qs,\qquad p^n=rs,\qquad q^n=sr.
\]

Seja τ:M₊→[0,∞] uma leitura que satisfaz τ(a* a)=τ(a a*) para todo a ∈ M. Para esta proposição não são necessárias normalidade, semifinitude, fidelidade, finitude de τ(p), dimensão finita, suporte finito, inversibilidade nem imagem fechada de r. A pertença de r,s ao mesmo M é necessária para a conclusão sobre um traço definido somente em M.

**Demonstração própria da compatibilidade.** Denote por supp(t) a projeção sobre o fecho da imagem de um positivo t, isto é, sobre (ker t)⊥. Use o polar canônico r=u d, d=(r* r)¹ᐟ², com u ∈ M, e=u* u a projeção sobre (ker r)⊥ e f=u u* a projeção sobre o fecho de ran(r). A existência desse polar e sua pertença a M são fornecedores clássicos; ver Jones, *Von Neumann Algebras*, §2.3 e §3.4, EP8, páginas impressas 9 e 22 (índices PDF 8 e 21). A remissão fornece o polar, não uma formalização da proposição ShiftRelated. [Fonte primária consultada](https://math.berkeley.edu/~vfr/VonNeumann2009.pdf).

1. Como q é positivo e n ≥ 1, ker(qⁿ)=ker(q). De qⁿ=sr, obtemos ker(r) ⊆ ker(q). Logo supp(q) ≤ e, portanto eq=qe=q. Analogamente, para p positivo, closure(ran(pⁿ))=closure(ran(p)). De pⁿ=rs segue closure(ran(p)) ⊆ closure(ran(r)), portanto supp(p) ≤ f e fp=pf=p. A igualdade de kernels das potências vale já para auto-adjuntos; pode ser deduzida de ker(t²)=ker(t), usando ‖tξ‖²=⟨ξ,t²ξ⟩, e uma potência de dois maior que n.

2. Tomando adjuntos em pr=rq, temos r* p=q r*. Assim

\[
(r^*r)q=r^*pr=q(r^*r).
\]

O cálculo funcional contínuo dá dq=qd. Não é preciso supor que p,q ou r comutem entre si além das relações exibidas.

3. Substituindo r=u d no entrelaçamento:

\[
(pu-uq)d=0.
\]

O operador limitado D=pu−uq é zero em ran(d), portanto em seu fecho eH. Em ker(d)=ker(r), temos uξ=0 e qξ=0, de modo que Dξ=0 também. Pela decomposição H=eH⊕ker(d), concluímos pu=uq em todo H. Este é o passo de densidade que não pode ser substituído por cancelamento de d ou por d⁻¹.

4. Multiplicando à direita por u* e usando pf=p:

\[
p=pf=puu^*=uqu^*.
\]

Também u* p u=e q=q. Portanto os endpoints são equivalentes por esse transporte parcial, mesmo com kernels não triviais.

5. Ponha a=u√q ∈ M. Como e domina supp(q), e√q=√q. Então

\[
a^*a=\sqrt q\,e\sqrt q=q,\qquad
aa^*=uqu^*=p.
\]

Aplicando a tracialidade quadrática existente, τ(q)=τ(a* a)=τ(a a*)=τ(p). A conta usa somente valores no cone positivo e igualdade em ENNReal; não usa um traço cíclico total, subtração de infinitos ou um testemunho hipotético de ContinuousCoreData. Não há circularidade com a extensão que se deseja construir.

A equação sp=qs não foi necessária nesta demonstração analítica; permanece parte natural da relação simétrica/composta proposta. Não se propõe podar a relação nem adicionar consumidores artificiais por isso.

**Cuidado com os suportes do polar.** Em geral não se pode afirmar u* u=supp(q) e u u*=supp(p) para o polar de r. Contraexemplo exato: em M₂(ℂ), p=q=diag(1,0), r=I, s=p, n=1 satisfazem todas as equações, mas o polar é u=I. As duas inclusões demonstradas são suficientes. Se for necessário um polar entre os suportes exatos, restrinja v=u supp(q); então v* v=supp(q) e v v*=supp(p). A revisão não presume nem exige que u seja unitário.

**Efeito sobre o supremo.** Escreva R para ShiftRelated e F(x)=sup{τ(t):t∈M₊, R(t,x)}. Para x∈M₊, a reflexividade dá F(x)≥τ(x), enquanto a compatibilidade demonstrada dá τ(t)=τ(x) para cada termo do supremo. Portanto F(x)=τ(x), também se τ(x)=∞. Mais geralmente, se uma classe contém um positivo p, todos os seus representantes positivos têm o mesmo valor: R(t,x) e R(p,x) implicam R(t,p) por simetria/transitividade. Assim o conjunto de valores da classe é um singleton; quando não existe positivo, o supremo vazio é 0. Não há aproximação capaz de acumular valores maiores dentro de uma classe positiva.

As leis algébricas de F têm os fornecedores certos: R(xy,yx) dá ciclicidade; star transporta cada positivo para ele mesmo e dá F(x*)=F(x); a ação dual é um *-automorfismo que bijeta as classes positivas e escala τ por c=exp(−s)∈(0,∞), logo escala o supremo. Só a existência de um homomorfismo em uma direção não bastaria para a última igualdade; o transporte inverso é necessário. F(0)=τ(0)=0 segue da compatibilidade. A leitura dos fontes candidatos nesta rodada é semântica; os rc autorais não foram reapresentados como compilação independente.

**Duas adulterações que realmente quebram a compatibilidade.** Elas delimitam a hipótese usada, sem contradizer a proposição demonstrada.

- Testemunhas no ambiente errado: tome M igual à álgebra diagonal em M₂(ℂ), com τ(diag(a,b))=a+2b nos positivos. Esse é um traço fiel e finito em M. Para p=e₁₁, q=e₂₂, r=e₁₂, s=e₂₁, n=1, todas as equações valem no ambiente M₂(ℂ), mas τ(p)=1 e τ(q)=2. As testemunhas r,s não pertencem a M. A definição candidata usa o subtipo do próprio core e evita esse erro.
- Peso não tracial: no próprio M₂(ℂ), use φ(A)=A₁₁+2A₂₂ nos positivos. Agora as mesmas quatro matrizes pertencem todas à álgebra e satisfazem R(p,q), mas φ(p)=1 e φ(q)=2. O supremo construído com φ teria Fφ(p)≥2>φ(p). Normalidade, positividade e fidelidade de um peso não substituem a tracialidade quadrática. A1 fornece precisamente a lei necessária.

**Alcance da palavra “traço”.** F é uma leitura total cíclica com a restrição positiva correta; isso não a torna um funcional linear no anel inteiro. Já em M=ℂ, a relação tem classes unitárias (singletons): r≠0 força a=b, e r=0 força a=b=0 pelas potências. Assim F(z)=z quando z é real não negativo, e F(z)=0 nos demais casos. Temos F(1)=1, F(−1)=0, F(0)=0; logo a aditividade global falha. Mais amplamente, uma função aditiva de um grupo aditivo para ENNReal que leve 0 em 0 tem de ser identicamente zero, pois F(x)+F(−x)=0. O contrato legado lido em ModularRealization pede trace_zero, trace_tracial, trace_star e trace_dual_scaling, sem aditividade global. A rota é compatível com essas quatro exigências; a terminologia da entrega precisa conservar esse alcance. No cone, aditividade, normalidade e demais leis de A1 são preservadas pela igualdade F|M₊=τ.

**Fornecedores localizados e obrigação formal restante.** A1 já expõe `scalarInverseLimitWeight_tracial` em `TGLExt/V351QuadraticTrace.lean`, com a assinatura sobre TODO a no mesmo core, e `scalarInverseLimitTraceData.tracial` o reutiliza em `TGLExt/V351RegularCoreTraceConstruction.lean`. O argumento acima consome esse campo uma vez, no a=u√q construído.

Na Mathlib local foram localizados `Commute.cfcₙ_nnreal`/`Commute.cfc_nnreal` em `Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean`, as identidades de `CFC.sqrt` em `Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean`, e `LinearEquiv.extendOfIsometry` em `Analysis/Normed/Operator/Extend.lean`. São componentes, não um polar pronto. A busca textual completa na árvore Mathlib pelos padrões `polar.?decomp|partial.?isometr|polarDecomp` não encontrou ocorrências; isso registra o resultado dessa busca, não prova ausência sob qualquer nome. As buscas iniciais com caminho inexistente/erro de grafia foram corrigidas e não contam como evidência negativa. A referência alternativa de Harvard retornou falha de abertura; o fornecedor bibliográfico efetivamente lido foi Jones.

Para um polar genérico compartilhado, a obrigação útil é entregar r=u|r| com u no mesmo M, u* u=proj(ker r)⊥, u u*=proj closure(ran r), e as identidades correspondentes de núcleo/imagem. Uma construção possível estende a isometria |r|ξ↦rξ dos respectivos fechos de imagem e define zero no kernel. A pertença a M deve ser provada: por comutante/unicidade, ou por limite forte dos elementos r(|r|+εI)⁻¹∈M quando ε↓0. Esses são planos de implementação, não lemas Lean auditados nesta rodada. O polar específico de Tomita não pode ser usado para um r arbitrário apenas pela coincidência do nome.

Não localizei contraexemplo sob as hipóteses completas; a demonstração resolve a dúvida matemática. Não há P0 matemático identificado. A obrigação prioritária de formalização é construir o polar interno e fechar a compatibilidade sem assumi-la. Continua [OPEN] o aceite de código dessa ponte e de sua ligação efetiva aos demais campos de ContinuousCoreData; não há aceite de ThreeLocksCoreData, FullWitness, SUSY no mesmo core ou do adendo inteiro. A2 não foi declarado concluído.

**Adendo da mesma revisão:** [ADENDO_APROXIMACAO_SEM_POLAR.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/ADENDO_APROXIMACAO_SEM_POLAR.md>) confere a variante t=r+s* e demonstra uma alternativa por regularizações, com convergência em norma e uso direto de `scalarInverseLimitWeight_square_le_of_strong`. Portanto construir o polar interno é uma opção, não obrigação exclusiva para fechar esta compatibilidade. A obrigação formal passa a ser implementar e revisar uma das duas provas, sem assumir seu resultado. O adendo também registra zero e fidelidade positiva da versão congelada do leitor, sem promover a cota inferior a igualdade com A1.

Metadados dos arquivos efetivamente consultados, distinção entre leitura integral e de faixas, hashes/bytes e cópias da ficha/fontes candidatos constam de `LEITURAS_E_PARECER.json`; o selo desta revisão é apenas documental.
