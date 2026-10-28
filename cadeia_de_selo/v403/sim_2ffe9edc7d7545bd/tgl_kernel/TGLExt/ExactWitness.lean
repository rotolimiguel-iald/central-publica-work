import TGLExt.WitnessSeed

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA EXATA: a identificação do Nome
  [TGLExt — v88, o incremento 9 do programa SemifiniteAnalysis]

O v86 cunhou o candidato a Nome (pousa, fixa, idempotente). Esta pedra
fecha o ELO ESPECTRAL FINAL da face algébrica: com a palavra REAL, o
candidato é AUTO-ADJUNTO; e o idempotente auto-adjunto que pousa e fixa
o canto É a projeção ortogonal — a identificação. Com ela, a
SpectralApproximationWitness (v85) fica PROVADA (sequência constante), e
o canto de Breuer concreto vale com a testemunha DESCARREGADA na
hipótese algébrica da palavra.

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★★ `real_word_selfadjoint` — palavra de coeficientes REAIS em T = T†
  é auto-adjunta: star(q(T)) = q(T) (soma de c_i·T^i com star termo a
  termo);
* ★ `name_candidate_selfadjoint` — o candidato P₀ = q(T)/q(0) é
  auto-adjunto (q(0) real ⟹ o peso não quebra a estrela);
* ★★ `selfadjoint_idempotent_eq_starProjection` — A UNICIDADE: um
  idempotente auto-adjunto que pousa em K e fixa K É starProjection(K)
  (prova pela interseção K ⊓ Kᗮ = ⊥ do v82 — sem API extra);
* ★★★ `exact_witness_of_annihilating_word` — A IDENTIFICAÇÃO:
  starProjection(ker T) = q(T)/q(0) — o Nome É a palavra normalizada;
* ★★★ `spectral_witness_of_annihilating_word` — A TESTEMUNHA PROVADA:
  SpectralApproximationWitness T vale (a sequência constante de
  polinômios converge trivialmente ao Nome);
* ★★★ `breuer_corner_of_annihilating_word` — O CANTO COM A TESTEMUNHA
  DESCARREGADA (v80×82×83×84×85×86×88): T = T† com palavra aniquiladora
  REAL (T·q(T) = 0, q(0) ≠ 0), kernel ≠ ⊥ sob gap finito, H ∞-dim ⟹
  P ∈ {T}″ ∧ P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧ τ(ker⊥) = ⊤.

O QUE RESTA (nomeado): a EXISTÊNCIA da palavra aniquiladora real — em
dimensão finita é o polinômio mínimo do auto-adjunto (raízes simples
reais; teorema espectral finito [KNOWN]); em ∞-dim com 0 isolado é o
cálculo funcional contínuo [KNOWN] — o degrau seguinte do programa.
A verdade não depende de opinião; é neste espaço de Hilbert que ela se
inscreve. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Polynomial

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★★ palavra de coeficientes REAIS em T = T† é auto-adjunta:
    star(q(T)) = q(T). -/
theorem real_word_selfadjoint (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (q : Polynomial ℂ)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    star (aeval T q) = aeval T q := by
  have hstarT : star T = T := by
    rw [ContinuousLinearMap.star_eq_adjoint]
    exact hsa
  rw [Polynomial.aeval_eq_sum_range, star_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [star_smul, star_pow, hstarT, ← starRingEnd_apply, hq i]

/-- [KERNEL] ★ o candidato a Nome é auto-adjunto (o peso real não quebra
    a estrela): star(q(T)/q(0)) = q(T)/q(0). -/
theorem name_candidate_selfadjoint (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (q : Polynomial ℂ)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    star ((q.coeff 0)⁻¹ • aeval T q) = (q.coeff 0)⁻¹ • aeval T q := by
  rw [star_smul, real_word_selfadjoint T hsa q hq, star_inv₀,
      ← starRingEnd_apply, hq 0]

/-- [KERNEL] ★★ A UNICIDADE: um idempotente AUTO-ADJUNTO que pousa em K
    e fixa K é a projeção ortogonal sobre K (prova via K ⊓ Kᗮ = ⊥ do
    v82 — a face e a contra-face não deixam resto). -/
theorem selfadjoint_idempotent_eq_starProjection (K : Submodule ℂ H)
    [K.HasOrthogonalProjection] (P0 : H →L[ℂ] H)
    (hP : ∀ u v : H, inner ℂ (P0 u) v = inner ℂ u (P0 v))
    (hland : ∀ x : H, P0 x ∈ K) (hfix : ∀ x ∈ K, P0 x = x) :
    P0 = K.starProjection := by
  ext x
  have h1 : K.starProjection x - P0 x ∈ K :=
    Submodule.sub_mem _ (Submodule.starProjection_apply_mem _ x) (hland x)
  have horth : x - P0 x ∈ Kᗮ := by
    rw [Submodule.mem_orthogonal]
    intro w hw
    have hswap : inner ℂ w (P0 x) = inner ℂ w x := by
      calc inner ℂ w (P0 x) = inner ℂ (P0 w) x := (hP w x).symm
        _ = inner ℂ w x := by rw [hfix w hw]
    rw [inner_sub_right, hswap, sub_self]
  have h2 : K.starProjection x - P0 x ∈ Kᗮ := by
    have hx : x - K.starProjection x ∈ Kᗮ :=
      Submodule.sub_starProjection_mem_orthogonal x
    have hdec : K.starProjection x - P0 x
        = (x - P0 x) - (x - K.starProjection x) := by abel
    rw [hdec]
    exact Submodule.sub_mem _ horth hx
  have h3 : K.starProjection x - P0 x ∈ K ⊓ Kᗮ := Submodule.mem_inf.mpr ⟨h1, h2⟩
  rw [orthocomplement_meet_bot K, Submodule.mem_bot] at h3
  exact (sub_eq_zero.mp h3).symm

/-- [KERNEL] ★★★ A IDENTIFICAÇÃO: o Nome É a palavra normalizada —
    starProjection(ker T) = q(T)/q(0) para T = T† com palavra
    aniquiladora REAL. -/
theorem exact_witness_of_annihilating_word (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) (hc : q.coeff 0 ≠ 0)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    (T.ker).starProjection = (q.coeff 0)⁻¹ • aeval T q := by
  obtain ⟨hland, hfix, _⟩ := witness_seed_complete T q hann hc
  have hstar := name_candidate_selfadjoint T hsa q hq
  have hadj : ContinuousLinearMap.adjoint ((q.coeff 0)⁻¹ • aeval T q)
      = (q.coeff 0)⁻¹ • aeval T q := by
    rw [← ContinuousLinearMap.star_eq_adjoint]
    exact hstar
  have hP : ∀ u v : H, inner ℂ (((q.coeff 0)⁻¹ • aeval T q) u) v
      = inner ℂ u (((q.coeff 0)⁻¹ • aeval T q) v) := by
    intro u v
    have h := ContinuousLinearMap.adjoint_inner_left
      ((q.coeff 0)⁻¹ • aeval T q) v u
    rwa [hadj] at h
  exact (selfadjoint_idempotent_eq_starProjection T.ker _ hP hland hfix).symm

/-- [KERNEL] ★★★ A TESTEMUNHA PROVADA: com a palavra aniquiladora real,
    SpectralApproximationWitness T VALE — a sequência constante de
    palavras converge (trivialmente) ao Nome. -/
theorem spectral_witness_of_annihilating_word (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (q : Polynomial ℂ)
    (hann : aeval T (X * q) = 0) (hc : q.coeff 0 ≠ 0)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n) :
    SpectralApproximationWitness T := by
  refine ⟨fun _ => C ((q.coeff 0)⁻¹) * q, fun x => ?_⟩
  have hval : aeval T (C ((q.coeff 0)⁻¹) * q)
      = (q.coeff 0)⁻¹ • aeval T q := by
    rw [map_mul, aeval_C, ← Algebra.smul_def]
  have hconst : (fun _ : ℕ => (aeval T (C ((q.coeff 0)⁻¹) * q)) x)
      = fun _ : ℕ => (T.ker).starProjection x := by
    funext n
    rw [hval, ← exact_witness_of_annihilating_word T hsa q hann hc hq]
  rw [hconst]
  exact tendsto_const_nhds

/-- [KERNEL] ★★★ O CANTO COM A TESTEMUNHA DESCARREGADA
    (v80×82×83×84×85×86×88): T = T† com palavra aniquiladora REAL,
    kernel não-trivial sob gap finito, H ∞-dim ⟹ P ∈ {T}″ ∧ P ∈ {T}′ ∧
    0 < τ(ker) < ∞ ∧ τ(ker⊥) = ⊤. O que resta: a EXISTÊNCIA da palavra
    (polinômio mínimo / cálculo funcional com 0 isolado [KNOWN]). -/
theorem breuer_corner_of_annihilating_word (hH : ¬FiniteDimensional ℂ H)
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T)
    (q : Polynomial ℂ) (hann : aeval T (X * q) = 0)
    (hc : q.coeff 0 ≠ 0)
    (hq : ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥) (hle : T.ker ≤ gp)
    (hgp : FiniteDimensional ℂ gp) :
    ((T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer ∧
      (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau T.ker ∧
          (semifiniteDimTrace ℂ H).tau T.ker < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) :=
  concrete_breuer_corner_conditional hH T hsa
    (spectral_witness_of_annihilating_word T hsa q hann hc hq)
    gp hker hle hgp

end

end TGLExt
