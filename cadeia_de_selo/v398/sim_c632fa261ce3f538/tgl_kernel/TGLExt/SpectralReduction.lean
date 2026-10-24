import TGLExt.BicommutantSkeleton

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A REDUÇÃO ESPECTRAL: a metade topológica de von Neumann e o resíduo
  reduzido a UMA testemunha
  [TGLExt — v85, o incremento 7 do programa SemifiniteAnalysis]

O v84 deixou o resíduo com um nome: P_{ker T} ∈ {T}″ pede o bicomutante
CONTÍNUO. Esta pedra prova a metade topológica que faltava e reduz o
resíduo inteiro a UMA hipótese nomeada:

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★★ `commutant_pointwise_limit_closed` — A METADE TOPOLÓGICA DE VON
  NEUMANN: o comutante de QUALQUER conjunto é fechado sob limites
  pontuais (SOT) de sequências — comutar sobrevive ao limite (a mesma
  causalidade da régua, agora na álgebra);
* ★ `commutant_add_smul_closed` — o comutante é subespaço (fechado sob
  + e •): com o monoide do v84, A′ é uma SUBÁLGEBRA SOT-fechada — a
  definição inteira de álgebra de von Neumann, verificada peça a peça;
* ★ `generator_in_bicommutant` / ★★ `powers_in_bicommutant` /
  ★★ `polynomials_in_bicommutant` — T, T^n e TODO polinômio p(T) vivem
  em {T}″: a álgebra gerada algebricamente por T está sob o bicomutante;
* ★★★ `limit_of_polynomials_in_bicommutant` — A REDUÇÃO: todo limite
  pontual de polinômios em T pertence a {T}″ — o bicomutante algébrico
  já contém o fecho forte da álgebra gerada;
* ★★ `corner_in_algebra_of_approximation` — se P_{ker T} admite
  aproximantes polinomiais (a TESTEMUNHA ESPECTRAL, definição
  `SpectralApproximationWitness`), então P ∈ {T}″;
* ★★★ `concrete_breuer_corner_conditional` — O CANTO DE BREUER CONCRETO,
  CONDICIONAL A UMA TESTEMUNHA (v80×82×83×84×85): T auto-adjunto com
  kernel não-trivial sob gap finito em H ∞-dim + testemunha espectral ⟹
  P_{ker T} ∈ {T}″ ∧ P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧ τ(ker⊥) = ⊤ —
  **uma projeção FINITA DA ÁLGEBRA, comutando com ela, dentro de um
  complemento infinito**: a forma exata do ConcreteBreuerCorner.

HONESTIDADE: a testemunha espectral (P = lim pontual de p_n(T)) é
exatamente o que o cálculo espectral fornece para T auto-adjunto com 0
isolado no espectro — a nossa situação de gap — [KNOWN] na literatura;
construí-la em kernel (teorema espectral) é o programa. NÃO se declara
gravitação quântica incondicional: a implicação está fechada; a
testemunha é a fronteira. Nada é III₁; nenhuma flag do fecho se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★★ A METADE TOPOLÓGICA DE VON NEUMANN: o comutante de
    qualquer conjunto é fechado sob limites PONTUAIS (SOT) de
    sequências — comutar sobrevive ao limite. -/
theorem commutant_pointwise_limit_closed (A : Set (H →L[ℂ] H))
    (a : ℕ → H →L[ℂ] H) (b : H →L[ℂ] H)
    (hmem : ∀ n, a n ∈ A.centralizer)
    (hlim : ∀ x, Filter.Tendsto (fun n => a n x) Filter.atTop (nhds (b x))) :
    b ∈ A.centralizer := by
  rw [Set.mem_centralizer_iff]
  intro s hs
  ext x
  show s (b x) = b (s x)
  have h2 : ∀ n, s (a n x) = a n (s x) := by
    intro n
    have hn := hmem n
    rw [Set.mem_centralizer_iff] at hn
    have h3 := hn s hs
    calc s (a n x) = (s * a n) x := rfl
      _ = (a n * s) x := by rw [h3]
      _ = a n (s x) := rfl
  have h1 : Filter.Tendsto (fun n => s (a n x)) Filter.atTop (nhds (s (b x))) :=
    (s.continuous.tendsto (b x)).comp (hlim x)
  have h1' : Filter.Tendsto (fun n => a n (s x)) Filter.atTop (nhds (s (b x))) := by
    simpa only [h2] using h1
  exact tendsto_nhds_unique h1' (hlim (s x))

/-- [KERNEL] ★ o comutante é subespaço: fechado sob soma e escalar —
    com o monoide do v84, A′ é uma subálgebra SOT-fechada (a definição
    de álgebra de von Neumann, peça a peça). -/
theorem commutant_add_smul_closed (A : Set (H →L[ℂ] H)) :
    (∀ a b : H →L[ℂ] H, a ∈ A.centralizer → b ∈ A.centralizer →
        a + b ∈ A.centralizer) ∧
      (∀ (c : ℂ) (a : H →L[ℂ] H), a ∈ A.centralizer →
        c • a ∈ A.centralizer) := by
  constructor
  · intro a b ha hb
    rw [Set.mem_centralizer_iff] at ha hb ⊢
    intro s hs
    rw [mul_add, add_mul, ha s hs, hb s hs]
  · intro c a ha
    rw [Set.mem_centralizer_iff] at ha ⊢
    intro s hs
    rw [mul_smul_comm, smul_mul_assoc, ha s hs]

/-- [KERNEL] ★ o gerador habita o próprio bicomutante: T ∈ {T}″. -/
theorem generator_in_bicommutant (T : H →L[ℂ] H) :
    T ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer :=
  operator_algebra_in_double_commutant _ (Set.mem_singleton T)

/-- [KERNEL] ★★ as potências habitam o bicomutante: T^n ∈ {T}″. -/
theorem powers_in_bicommutant (T : H →L[ℂ] H) (n : ℕ) :
    T ^ n ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer := by
  induction n with
  | zero =>
    rw [pow_zero]
    exact (operator_commutant_unital_multiplicative _).1
  | succ k ih =>
    rw [pow_succ]
    exact (operator_commutant_unital_multiplicative _).2 _ _ ih
      (generator_in_bicommutant T)

/-- [KERNEL] ★★ todo polinômio em T habita o bicomutante:
    p(T) ∈ {T}″ — a álgebra gerada algebricamente por T está sob {T}″. -/
theorem polynomials_in_bicommutant (T : H →L[ℂ] H) (p : Polynomial ℂ) :
    Polynomial.aeval T p ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
    rw [map_add]
    exact (commutant_add_smul_closed _).1 _ _ hp hq
  | monomial n c =>
    rw [Polynomial.aeval_monomial]
    have h1 : (algebraMap ℂ (H →L[ℂ] H)) c * T ^ n = c • T ^ n := by
      rw [Algebra.smul_def]
    rw [h1]
    exact (commutant_add_smul_closed _).2 c _ (powers_in_bicommutant T n)

/-- [KERNEL] ★★★ A REDUÇÃO: todo limite PONTUAL de polinômios em T
    pertence a {T}″ — o bicomutante algébrico já contém o fecho forte
    da álgebra gerada por T. -/
theorem limit_of_polynomials_in_bicommutant (T b : H →L[ℂ] H)
    (p : ℕ → Polynomial ℂ)
    (hlim : ∀ x, Filter.Tendsto (fun n => (Polynomial.aeval T (p n)) x)
      Filter.atTop (nhds (b x))) :
    b ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer :=
  commutant_pointwise_limit_closed _ (fun n => Polynomial.aeval T (p n)) b
    (fun n => polynomials_in_bicommutant T (p n)) hlim

/-- [DEF — A TESTEMUNHA ESPECTRAL] P_{ker T} admite aproximantes
    polinomiais pontuais. Para T auto-adjunto com 0 isolado no espectro
    (a situação de gap), o cálculo espectral fornece exatamente isto
    [KNOWN]; construí-la em kernel é o programa. -/
def SpectralApproximationWitness (T : H →L[ℂ] H) : Prop :=
  ∃ p : ℕ → Polynomial ℂ, ∀ x,
    Filter.Tendsto (fun n => (Polynomial.aeval T (p n)) x)
      Filter.atTop (nhds ((T.ker).starProjection x))

/-- [KERNEL] ★★ com a testemunha espectral, o canto pertence à ÁLGEBRA:
    P_{ker T} ∈ {T}″. -/
theorem corner_in_algebra_of_approximation (T : H →L[ℂ] H)
    (hW : SpectralApproximationWitness T) :
    (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer := by
  obtain ⟨p, hlim⟩ := hW
  exact limit_of_polynomials_in_bicommutant T _ p hlim

/-- [KERNEL] ★★★ O CANTO DE BREUER CONCRETO, CONDICIONAL A UMA
    TESTEMUNHA (v80×82×83×84×85): T auto-adjunto, kernel não-trivial sob
    gap finito, H ∞-dim, testemunha espectral ⟹ P_{ker T} ∈ {T}″ ∧
    P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧ τ(ker⊥) = ⊤ — uma projeção FINITA DA
    ÁLGEBRA, comutando com ela, dentro de um complemento INFINITO. A
    implicação está FECHADA; a testemunha é a fronteira. -/
theorem concrete_breuer_corner_conditional (hH : ¬FiniteDimensional ℂ H)
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T)
    (hW : SpectralApproximationWitness T)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥)
    (hle : T.ker ≤ gp) (hgp : FiniteDimensional ℂ gp) :
    ((T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer ∧
      (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau T.ker ∧
          (semifiniteDimTrace ℂ H).tau T.ker < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) := by
  have hframe := breuer_corner_full_algebraic_frame hH T hsa gp hker hle hgp
  exact ⟨⟨corner_in_algebra_of_approximation T hW, hframe.1.1⟩, hframe.2⟩

end

end TGLExt
