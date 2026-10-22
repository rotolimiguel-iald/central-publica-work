# Nota047 — propriedades da expectativa construída

[INPUT] Estudo solicitado pelo root, somente leitura de fontes locais e criação exclusiva desta nota. Não houve código047, compilação, alteração046, edição de memória ou modificação de originais. Esta nota não integra o selo046. Os fontes046 foram lidos enquanto o root ainda validava o lote: o texto abaixo não aprova seus hashes finais nem antecipa a compilação final.

[DERIVED — conclusão de trabalho] A prioridade útil é provar propriedades do mapa restrito ao fator usando o contrato já construído. Linearidade, unidade, preservação de ω, estrela e bimodularidade podem ser obtidas por ortogonalidade e separância, sem uma nova hipótese de existência. A positividade admite uma prova direta pelas médias de conjugação. CP exige quantificar todas as amplificações finitas. Normalidade exige uma ponte adicional de ordem/topologia; não deve ser inferida simplesmente porque cada média é normal e existe um limite forte.

Escrevemos H = TowerHilbert P, M = theFactorObject P, N = omegaCentralizer P, Ω = hOmega P e E = aperiodicExpectation P.

**Domínio que precisa permanecer explícito.** E é definido como zero fora de M. A soma com um operador externo mostra por que não se deve empacotá-lo como mapa linear B(H) → B(H): se A ∉ M, também 1+A ∉ M, mas E(1)=1 e E(A)=E(1+A)=0. O alvo correto é M →ₗ[ℂ] M, ou M →ₗ[ℂ] B(H) com imagem em N. Todas as identidades abaixo quantificam A,B ∈ M. Não é preciso equipar N com toda a estrutura de álgebra de von Neumann antes de provar essas identidades.

1. **APIs locais efetivamente encontradas — evitar refazer046.**

[REAL — leitura das declarações; nenhuma nova prova compilada nesta investigação]

- `AperiodicCentralizerExpectation.lean`, namespace `ChatgptAudit.Aperiodic046`: `aperiodic_expectation_spec P A hA` dá E(A) ∈ M, ‖E(A)‖ ≤ ‖A‖ e convergência forte das médias `periodAverage P ((n:ℝ)+1) ... A` em todo vetor. `aperiodic_expectation_prefix P N A hA` identifica cada prefixo com `towerPi P (specExpect (towerW P N) (expectationMatrix P N A))`. Já existem `aperiodic_expectation_into`, `aperiodic_expectation_fixes`, `aperiodic_expectation_ortho`, `aperiodicExpectationInput`, `aperiodic_expectation_contractive` e `aperiodic_expectation_idempotent`.
- `AperiodicVectorAverage.lean`, mesmo namespace: `modular_vector_average_add` NÃO é nome encontrado; os nomes corretos são `modular_average_vector_add`, `modular_average_vector_smul`, `modular_average_vector_bound`. Eles tratam do vetor v, não da variável operador A. `aperiodic_average_operator P A hA` já constrói o operador limite no fator. Não repetir a construção.
- `BoundedOmegaLimit.lean`: `bounded_omega_limit_lift P C bound hbound hmem hnorm z hz` constrói B ∈ M, ‖B‖ ≤ bound, BΩ=z e convergência forte. Seu índice atual é ℕ; uma aplicação a nets exige generalização demonstrada, não mudança silenciosa de quantificador. `omega_lift_unique` identifica operadores do fator que têm o mesmo valor em Ω.
- `fontes/tgl_kernel/TGLExt/TheOathOnTheTower.lean`, namespace `TGLExt`, linhas344–348: `ExpectationInput P` tem somente E, into, fixes e ortho. `omega_definite {A} (hA : A ∈ M) (h0 : omegaState P (star A * A)=0) : A=0` é o lema de definitude. `the_expectation_is_unique (I₁ I₂ : ExpectationInput P) : ∀ A ∈ M, I₁.E A=I₂.E A` já existe. `omegaState_sub X Y` também.
- `CentralizerDensity.lean`, namespace `ChatgptAudit.Density033`: `omega_state_add P A B`, `omega_state_smul P c A`; `omega_centralizer_zero P`, `omega_centralizer_one P`; `omega_centralizer_add P hA hC`, `omega_centralizer_smul P c hA`, `omega_centralizer_mul P hA hC`; `omegaCentralizerAlgebra P : Subalgebra ℂ (H →L[ℂ] H)`. Não localizei um lema de fechamento por estrela nesse módulo. O original033 contém instâncias anônimas históricas; o import em futura bancada limpa deve selecionar o override035 com nomes, cuja transposição já está pinada, e não recompilar o original033 por conveniência.
- `fontes/tgl_kernel/TGLExt/TheImportedExpectation.lean`, linha202: `the_reading_preserves_omega {P} (I : TakesakiInput P) : ∀ A ∈ M, omegaState P (theReading I A)=omegaState P A`. A prova usa apenas ortho com B=1. Podemos reutilizar a identidade por um adaptador corretamente habitado, ou transportar essas poucas linhas para um lema sobre qualquer `ExpectationInput`, evitando introduzir `TakesakiInput` como antecedente adicional.
- `TracialCentralizerExpectation.lean`: `omega_product_inner (x y : H →L[ℂ] H) : omegaState P (x*y)=inner ℂ (star x Ω) (y Ω)`.
- `ModularFlowAlgebra.lean`: `modularConjugation P t` já é um `≃⋆ₐ[ℂ]`, portanto sua linearidade, multiplicatividade e compatibilidade com estrela são as APIs genéricas `map_add`, `map_smul`, `map_mul`, `map_star`.
- `ModularPower.lean`: `modularConjugation_preserves_state (t:ℝ) (a:H →L[ℂ] H) : omegaState P (modularConjugation P t a)=omegaState P a`.
- `PeriodAverageOperator.lean`: `period_average_operator (T:ℝ) (hT:0<T) (A:H →L[ℂ] H)` devolve a fórmula vetorial da integral e ‖periodAverage ... A‖≤‖A‖. `average_vector_add` e `average_vector_smul` também são lineares no vetor, não constituem ainda os lemas sobre A.
- `TowerExpectation.lean`: `factor_eq_of_omega` e `expectation_preserves_state` existem. `ExpectationBimodule.lean.expectation_bimodular` e `ExpectationPositive.lean.expectation_positive` dizem respeito ao corte `towerExpectation P N`, não diretamente à projeção global E. Não trocar esses objetos por homonímia.

2. **Primeiro alvo: unicidade pontual e consequências algébricas.**

[DERIVED — propostas de enunciados, ainda não nomes de lemas existentes]

Criar um único auxiliar com este conteúdo: dados I : ExpectationInput P, A∈M e C∈N, se ∀ B∈N, ω(B* (A−C))=0, então I.E A=C. A prova é literalmente a prova local de `the_expectation_is_unique`: D=I.E A−C pertence a N; subtrair as duas ortogonalidades testadas em D dá ω(D*D)=0; `omega_definite` encerra. Não construir um novo record cuja conclusão desejada seja um campo.

Esse auxiliar paga:

- E(0)=0, E(A+B)=E(A)+E(B), E(cA)=cE(A). As imagens candidatas pertencem a N pelos lemas033; suas ortogonalidades vêm de `omegaState_sub`, add e smul. Isso vale para QUALQUER `ExpectationInput P`, não apenas para o escolhido em046.
- E(1)=1 vem diretamente de `I.fixes 1 (omega_centralizer_one P)`.
- ω(E(A))=ω(A) vem de `I.ortho A hA 1 (omega_centralizer_one P)`, seguido de `rw [star_one, one_mul, omegaState_sub]`; `sub_eq_zero.mp` e simetria dão a orientação desejada.
- Provar primeiro ω(A*)=conj(ω(A)) por adjunto/`inner_conj_symm`, e N fechado por estrela usando essa igualdade e a definição de N. Não presumir que o `Subalgebra`033 já é uma `StarSubalgebra`.
- Para a estrela de E, testar o candidato E(A)*. A identidade
  ω(B* (A*−E(A)*)) = conj(ω((A−E(A))B)) = conj(ω(B(A−E(A))))
  usa B∈N; o último termo zera pela ortogonalidade de A testada em B*. Assim E(A*)=E(A)*.
- Para C∈N, o candidato C E(A) satisfaz ortogonalidade de CA por testar a ortogonalidade de A em C*B: (C*B)*=B*C. Logo E(CA)=C E(A).
- Para D∈N, o candidato E(A)D satisfaz ortogonalidade de AD porque ω(B*(A−E(A))D)=ω(DB*(A−E(A))) e (BD*)*=DB*. Logo E(AD)=E(A)D. Compor as duas identidades dá E(CAD)=C E(A)D. A rotação pela direita usa a definição de centralizador, não comutatividade entre D e A.

Depois empacotar o mapa linear restrito a M. A cota046 fornece `LinearMap.mkContinuous 1` e ‖E‖≤1, sem tentar integrar funções B(H) em norma. O codomínio pode continuar M/B(H); empacotar N como álgebra estrelada é um alvo posterior de API.

3. **Positividade e CP: caminho direto que não acrescenta um postulado.**

[DERIVED] Para A≥0 e v∈H, cada conjugação satisfaz
  ⟨v, σ_t(A)v⟩ = ⟨U_(−t)v, A U_(−t)v⟩ ≥0.
A média em [0,T], T>0, preserva esse sinal. Passar a n→∞ com a convergência forte046 dá ⟨v,E(A)v⟩≥0. Junto de E(A)*=E(A), já pago acima para A*=A, isso prova positividade. Não é preciso afirmar continuidade em norma t↦σ_t(A), que não foi dada.

[REAL — APIs Mathlib lidas, relativas a `.../tgl_kernel/.lake/packages/mathlib/Mathlib/`]

- `Analysis/InnerProductSpace/Positive.lean`: `ContinuousLinearMap.isPositive_iff' [CompleteSpace H] (T:H →L[ℂ] H) : T.IsPositive ↔ IsSelfAdjoint T ∧ ∀ x, 0 ≤ inner ℂ (T x) x`; `ContinuousLinearMap.nonneg_iff_isPositive T`; `ContinuousLinearMap.IsPositive.inner_nonneg_right`; `ContinuousLinearMap.IsPositive.adjoint_conj` e `.conj_adjoint`.
- `MeasureTheory/Integral/IntervalIntegral/Basic.lean`, linha870: `ContinuousLinearMap.intervalIntegral_comp_comm (L:E →L[𝕜] F) (hf:IntervalIntegrable f μ a b) : (∫x in a..b, L(f x) ∂μ)=L(∫x in a..b,f x ∂μ)`. Aplicar a um funcional vetorial `innerSL` e, para o sinal, à parte real. Na linha1383, `intervalIntegral.integral_nonneg_of_forall (hab:a≤b) (hf:∀u,0≤f u)` é o lema escalar real. Usar `modular_orbit_continuous` para integrabilidade e `le_of_tendsto` no limite escalar.
- `Algebra/Order/Module/PositiveLinearMap.lean`: `PositiveLinearMap R E₁ E₂` estende um mapa linear e um `OrderHom`. Positividade de E e linearidade permitem provar monotonicidade por E(B−A)≥0 e então empacotar `M →ₚ[ℂ] M` quando as instâncias do subtipo estiverem disponíveis.
- `Analysis/CStarAlgebra/CompletelyPositiveMap.lean`: `CompletelyPositiveMap A₁ A₂` estende `A₁ →ₗ[ℂ] A₂` com campo
  `map_cstarMatrix_nonneg' (k:ℕ) (M:CStarMatrix (Fin k) (Fin k) A₁) (hM:0≤M) : 0≤M.map toLinearMap`.
  O arquivo já fornece `NonUnitalStarAlgHomClass.instCompletelyPositiveMapClass` e `CompletelyPositiveMap.map_cstarMatrix_nonneg {n} [Fintype n] (φ:A₁ →CP A₂) (M:CStarMatrix n n A₁) (hM:0≤M) : 0≤M.map φ`. Não refazer a CP de cada automorfismo modular.

[OPEN — trabalho concreto de CP] Uma prova de positividade simples não é uma prova de CP. Repetir o argumento das médias para cada k e todos v₁,…,v_k, aplicando o mesmo U_(−t) a cada componente:
  Σᵢⱼ ⟨vᵢ, E(Aᵢⱼ)vⱼ⟩ = lim média_t Σᵢⱼ ⟨U_(−t)vᵢ, Aᵢⱼ U_(−t)vⱼ⟩ ≥0.
A linearidade da integral e as somas são finitas. A passagem escalar ao limite é a mesma046 para cada entrada. Para produzir o record Mathlib de CP, ainda é necessário construir/usar a representação de `CStarMatrix k k M` em H^k com norma ℓ² e provar a equivalência entre positividade nessa representação e a ordem C*-algébrica. Não localizei nessa investigação uma ponte pronta com assinatura verificável para esse caso de operadores; não inventar um nome. É legítimo entregar antes um teorema explícito para todos k e formas quadráticas positivas de blocos, distinguindo-o do empacotamento completo.

4. **Continuidade e normalidade: etapa adicional com quantificadores certos.**

[DERIVED] O contrato já permite uma estimativa mais forte na norma GNS:
  ‖E(A)Ω‖ ≤ ‖AΩ‖.
Basta usar ortho com B=E(A): ‖E(A)Ω‖²=⟨E(A)Ω,AΩ⟩ e Cauchy–Schwarz, tratando separadamente o caso de norma zero. Com linearidade, resulta
  ‖(E(A)−E(B))Ω‖ ≤ ‖(A−B)Ω‖.
Esse é um alvo047 útil e pequeno. Ele decorre da construção; não é uma hipótese de continuidade acrescentada ao contrato.

Se A_i∈M são uniformemente limitados e convergem fortemente a A∈M, a estimativa dá E(A_i)Ω→E(A)Ω. Os operadores direitos locais comutam com M e seus vetores C'Ω são densos, como usados em `BoundedOmegaLimit.lean`. A cota ‖E(A_i)‖≤‖A_i‖ estende a convergência a todo H. O enunciado deve quantificar um filtro/net arbitrário ou declarar explicitamente que prova somente a versão sequencial. A prova ε/3 de046 pode ser generalizada sem nova suposição analítica.

Alternativa para a versão WOT limitada: K=fecho(NΩ) e p_K sua projeção ortogonal. Ortogonalidade implica E(A)Ω=p_K(AΩ). A API exata em `Analysis/InnerProductSpace/Projection/Basic.lean`, linha173, é
  `Submodule.eq_starProjection_of_mem_of_inner_eq_zero {u v:E} (hvm:v∈K) (hvo:∀w∈K,inner 𝕜 (u−v) w=0) : K.starProjection u=v`.
Requer `[K.HasOrthogonalProjection]`; K fechado no Hilbert completo fornece a instância apropriada. É preciso estender a ortogonalidade de NΩ ao seu fecho e usar a simetria conjugada para a orientação do produto interno. A norma da projeção é ≤1; a API evita reconstruí-la por escolha de limites.

A fórmula de p_K dá continuidade fraca de E(A_i)Ω quando A_i→A em WOT. Para C',D' direitos locais,
  ⟨C'Ω,E(A)D'Ω⟩ = ⟨D'^*C'Ω,E(A)Ω⟩ = ⟨p_K(D'^*C'Ω),AΩ⟩.
É um funcional vetorial de A. A densidade dos vetores direitos e a cota uniforme estendem a convergência a todos os testes WOT. O primeiro produto é na ordem D'^*C'; essa ordem importa.

[REAL — limite das APIs encontradas] `ContinuousLinearMapWOT.tendsto_iff_forall_inner_apply_tendsto`, em `Analysis/InnerProductSpace/WeakOperatorTopology.lean`, linha48, tem assinatura
  `Tendsto f l (𝓝 A) ↔ ∀ x y, Tendsto (fun a => inner 𝕜 y (f a x)) l (𝓝 (inner 𝕜 y (A x)))`.
Já `TGLExt.omegaState_seqWOT P`, em `NoNormalTrace.lean`, prova somente o contrato `SeqWOTContinuous` (sequências uniformemente limitadas). A própria origem distingue isso de normalidade σ-fraca plena. Nas buscas em `Analysis/VonNeumannAlgebra` (somente Basic.lean nesta versão), `Analysis/CStarAlgebra`, `Analysis/InnerProductSpace` e `Analysis/LocallyConvex`, não encontrei um teorema pronto de Tomiyama ou um pacote de mapas normais que dispense construir a ponte. Isso é resultado desta busca delimitada, não afirmação de inexistência universal.

[DERIVED — rota de normalidade por ordem, ainda não formalizada] Depois de positividade e preservaçãoω, considere uma rede crescente positiva A_i com sup A em M; seja B=sup E(A_i) no centralizador. Como B≤E(A), a normalidade do estado vetorial daria
  ω(B)=sup_i ω(E(A_i))=sup_i ω(A_i)=ω(A)=ω(E(A)).
A fidelidade de ω sobre positivos força B=E(A). Essa prova exige construir/ligar os supremos limitados e a continuidade normal do estado vetorial; `omega_definite` trata ω(X*X)=0, e seu uso para um positivo geral exige a raiz positiva em M ou um lema equivalente demonstrado. Não esconder essas obrigações em novos campos assumidos. Outra rota é formalizar a continuidade em WOT nas bolas e então a equivalência apropriada com normalidade σ-fraca. A palavra normal só deve entrar com a ponte efetivamente demonstrada ou com estatuto de especialização matemática externa explicitado.

5. **Entrega mínima recomendada para047.**

Primeiro: auxiliar de unicidade pontual; zero/add/smul/one; preservaçãoω; estrela; bimodularidade; mapa linear contínuo restrito a M; contração GNS. Tudo tem argumentos concretos e usa o contrato046 sem elevar hipóteses. Segundo: positividade pelas integrais e amplificações finitas CP com a ponte de representação indicada. Terceiro: continuidade em famílias limitadas com quantificação explícita e, quando a infraestrutura de ordem/σ-fraca estiver paga, normalidade. Nenhum desses passos identifica área física, calor microscópico, H3 ou geometria do espaço-tempo. H3/QG permanecem OPEN, sem mudança de gate.
