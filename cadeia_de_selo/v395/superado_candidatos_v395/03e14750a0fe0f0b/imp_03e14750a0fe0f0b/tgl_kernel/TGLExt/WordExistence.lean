import TGLExt.ExactWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A EXISTÊNCIA DA PALAVRA: a face finita fecha
  [TGLExt — v89, o incremento 10 do programa SemifiniteAnalysis]

O v88 identificou o Nome DADA a palavra aniquiladora real. Esta pedra
prova que, NA FACE FINITA, a palavra EXISTE — e com ela a testemunha
espectral deixa de ser hipótese: é TEOREMA. Princípio-guia (leitura do
operador, §168): a geometria da palavra é o β-espectro — no operador
concreto dos Three Locks, a primeira raiz não-nula mede 4β EXATOS
(0,048125 no runtime); cunhar o Nome custa dividir pela palavra no zero.

O QUE ESTA PEDRA PROVA [KERNEL] (dim finita):

* ★ `star_aeval_eq_map_conj` — star(p(T)) = (p conjugado)(T) para T = T†
  (a estrela atravessa a palavra trocando os coeficientes);
* ★★ `minpoly_selfadjoint_real` — O POLINÔMIO MÍNIMO DO AUTO-ADJUNTO É
  REAL: conj(coeff n) = coeff n (o mínimo divide o conjugado; monicidade
  e grau igual forçam igualdade);
* ★★★ `minpoly_zero_not_double_root` — O SLIVER ESPECTRAL: 0 tem
  multiplicidade ≤ 1 no mínimo (¬ X² ∣ minpoly) — por argumento de NORMA
  (‖T r(T) x‖² = ⟪r(T)x, T² r(T)x⟫ = 0), puro espaço de Hilbert, sem
  diagonalizar;
* ★★★ `annihilating_word_exists` — A PALAVRA EXISTE: ker T ≠ ⊥ ⟹
  minpoly = X·q com q(0) ≠ 0 e q REAL (o zero entra com multiplicidade
  exatamente 1; os coeficientes herdam a realidade do mínimo);
* ★★★ `finite_face_witness_unconditional` — A TESTEMUNHA INCONDICIONAL:
  na face finita, SpectralApproximationWitness T VALE para todo T = T†
  com kernel não-trivial — a fronteira do v85 é TEOREMA aqui;
* ★★★ `finite_face_corner_in_algebra` — O CANTO NA ÁLGEBRA, SEM
  HIPÓTESE EXTRA: P_{ker T} ∈ {T}″ ∧ P_{ker T} ∈ {T}′ na face finita —
  o canto pertence à álgebra de von Neumann (algébrica) do operador.

O QUE RESTA (o último elo, nomeado): a palavra em ∞-dim — cálculo
funcional contínuo com 0 isolado no espectro [KNOWN] — e a passagem do
canto finito ao ConcreteBreuerCorner ∞-dim incondicional. β jamais
literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Polynomial

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

section CompleteFace

variable [CompleteSpace H]

/-- [KERNEL] ★ a estrela atravessa a palavra trocando os coeficientes:
    star(p(T)) = (p̄)(T) para T = T†. -/
theorem star_aeval_eq_map_conj (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (p : Polynomial ℂ) :
    star (aeval T p) = aeval T (p.map (starRingEnd ℂ)) := by
  have hstarT : star T = T := by
    rw [ContinuousLinearMap.star_eq_adjoint]
    exact hsa
  have hR : aeval T (p.map (starRingEnd ℂ))
      = ∑ i ∈ Finset.range (p.natDegree + 1),
          (starRingEnd ℂ (p.coeff i)) • T ^ i := by
    rw [Polynomial.aeval_eq_sum_range'
      (Nat.lt_succ_of_le (Polynomial.natDegree_map_le))]
    exact Finset.sum_congr rfl fun i _ => by rw [Polynomial.coeff_map]
  have hL : star (aeval T p)
      = ∑ i ∈ Finset.range (p.natDegree + 1),
          (starRingEnd ℂ (p.coeff i)) • T ^ i := by
    rw [Polynomial.aeval_eq_sum_range, star_sum]
    exact Finset.sum_congr rfl fun i _ => by
      rw [star_smul, star_pow, hstarT, ← starRingEnd_apply]
  rw [hL, hR]

end CompleteFace

variable [FiniteDimensional ℂ H]

/-- [KERNEL] ★★ O POLINÔMIO MÍNIMO DO AUTO-ADJUNTO É REAL:
    conj(coeff n) = coeff n para todo n. -/
theorem minpoly_selfadjoint_real (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) :
    ∀ n, starRingEnd ℂ ((minpoly ℂ T).coeff n) = (minpoly ℂ T).coeff n := by
  have hint : IsIntegral ℂ T := Algebra.IsIntegral.isIntegral T
  have h0 : aeval T ((minpoly ℂ T).map (starRingEnd ℂ)) = 0 := by
    rw [← star_aeval_eq_map_conj T hsa, minpoly.aeval, star_zero]
  have hdvd : minpoly ℂ T ∣ (minpoly ℂ T).map (starRingEnd ℂ) :=
    minpoly.dvd ℂ T h0
  have hmm : (minpoly ℂ T).Monic := minpoly.monic hint
  have hmm2 : ((minpoly ℂ T).map (starRingEnd ℂ)).Monic := hmm.map _
  obtain ⟨c, hc⟩ := hdvd
  have hmne : minpoly ℂ T ≠ 0 := minpoly.ne_zero hint
  have hcne : c ≠ 0 := by
    intro h
    rw [h, mul_zero] at hc
    exact hmm2.ne_zero hc
  have hdeg : ((minpoly ℂ T).map (starRingEnd ℂ)).natDegree
      = (minpoly ℂ T).natDegree := Polynomial.natDegree_map (starRingEnd ℂ)
  have hdegc : c.natDegree = 0 := by
    have hmul := Polynomial.natDegree_mul hmne hcne
    rw [← hc, hdeg] at hmul
    omega
  have hcl : c.leadingCoeff = 1 := by
    have hlm := hmm2.leadingCoeff
    rw [hc, Polynomial.leadingCoeff_mul, hmm.leadingCoeff, one_mul] at hlm
    exact hlm
  have hc1 : c = 1 := by
    have h1 : c = Polynomial.C (c.coeff 0) :=
      Polynomial.eq_C_of_natDegree_eq_zero hdegc
    rw [h1, Polynomial.leadingCoeff_C] at hcl
    rw [h1, hcl, Polynomial.C_1]
  have hmapeq : (minpoly ℂ T).map (starRingEnd ℂ) = minpoly ℂ T := by
    rw [hc, hc1, mul_one]
  intro n
  have hcoeff := congrArg (fun p => Polynomial.coeff p n) hmapeq
  simpa [Polynomial.coeff_map] using hcoeff

/-- [KERNEL] ★★★ O SLIVER ESPECTRAL (por norma, sem diagonalizar): o
    zero entra no mínimo com multiplicidade ≤ 1 — ¬ X² ∣ minpoly.
    ‖T r(T)x‖² = ⟪r(T)x, T² r(T)x⟫ = 0 força T·r(T) = 0, grau menor que
    o mínimo: contradição. -/
theorem minpoly_zero_not_double_root (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) :
    ¬ (Polynomial.X ^ 2 ∣ minpoly ℂ T) := by
  have hint : IsIntegral ℂ T := Algebra.IsIntegral.isIntegral T
  intro hdvd
  obtain ⟨r, hr⟩ := hdvd
  have hrne : r ≠ 0 := by
    intro h
    rw [h, mul_zero] at hr
    exact minpoly.ne_zero hint hr
  have hop : aeval T (Polynomial.X ^ 2 * r) = 0 := by
    rw [← hr]
    exact minpoly.aeval ℂ T
  have hzero : aeval T (Polynomial.X * r) = 0 := by
    ext x
    have h2 : T (T ((aeval T r) x)) = 0 := by
      calc T (T ((aeval T r) x))
          = (T * (T * aeval T r)) x := rfl
        _ = (aeval T (Polynomial.X ^ 2 * r)) x := by
            congr 1
            rw [map_mul, map_pow, Polynomial.aeval_X, sq, mul_assoc]
        _ = (0 : H →L[ℂ] H) x := by rw [hop]
        _ = 0 := rfl
    have hswap := ContinuousLinearMap.adjoint_inner_left T
      (T ((aeval T r) x)) ((aeval T r) x)
    rw [hsa] at hswap
    have hnorm : inner ℂ (T ((aeval T r) x)) (T ((aeval T r) x)) = (0 : ℂ) := by
      rw [hswap, h2, inner_zero_right]
    have hTz : T ((aeval T r) x) = 0 := inner_self_eq_zero.mp hnorm
    show (aeval T (Polynomial.X * r)) x = (0 : H →L[ℂ] H) x
    rw [map_mul, Polynomial.aeval_X]
    exact hTz
  have hdvd2 : minpoly ℂ T ∣ Polynomial.X * r := minpoly.dvd ℂ T hzero
  have hXr : Polynomial.X * r ≠ 0 := mul_ne_zero Polynomial.X_ne_zero hrne
  have hlt : (Polynomial.X * r).natDegree < (minpoly ℂ T).natDegree := by
    rw [hr, Polynomial.natDegree_mul (pow_ne_zero 2 Polynomial.X_ne_zero) hrne,
        Polynomial.natDegree_mul Polynomial.X_ne_zero hrne,
        Polynomial.natDegree_pow, Polynomial.natDegree_X]
    omega
  exact hXr (Polynomial.eq_zero_of_dvd_of_natDegree_lt hdvd2 hlt)

/-- [KERNEL] ★★★ A PALAVRA EXISTE: para T = T† com kernel não-trivial,
    o mínimo fatora como X·q com q(0) ≠ 0 e q REAL — a palavra
    aniquiladora do v88, construída. -/
theorem annihilating_word_exists (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (hker : T.ker ≠ ⊥) :
    ∃ q : Polynomial ℂ, aeval T (Polynomial.X * q) = 0 ∧ q.coeff 0 ≠ 0 ∧
      ∀ n, starRingEnd ℂ (q.coeff n) = q.coeff n := by
  obtain ⟨x, hxk, hx0⟩ := (Submodule.ne_bot_iff _).mp hker
  have hTx : T x = 0 := LinearMap.mem_ker.mp hxk
  have hc0 : (minpoly ℂ T).coeff 0 = 0 := by
    by_contra hne
    have hcomm : T * aeval T (minpoly ℂ T).divX
        = aeval T (minpoly ℂ T).divX * T := by
      have ha : aeval T (Polynomial.X * (minpoly ℂ T).divX)
          = aeval T ((minpoly ℂ T).divX * Polynomial.X) := by rw [mul_comm]
      rw [map_mul, map_mul, Polynomial.aeval_X] at ha
      exact ha
    have happ : (aeval T (minpoly ℂ T)) x = ((minpoly ℂ T).coeff 0) • x := by
      have hdec : aeval T (minpoly ℂ T)
          = aeval T (Polynomial.X * (minpoly ℂ T).divX)
            + aeval T (Polynomial.C ((minpoly ℂ T).coeff 0)) := by
        rw [← map_add, Polynomial.X_mul_divX_add]
      have h1 : (aeval T (Polynomial.X * (minpoly ℂ T).divX)) x = 0 := by
        rw [map_mul, Polynomial.aeval_X, hcomm]
        show (aeval T (minpoly ℂ T).divX) (T x) = 0
        rw [hTx, map_zero]
      rw [hdec, ContinuousLinearMap.add_apply, h1, zero_add,
          Polynomial.aeval_C, Algebra.algebraMap_eq_smul_one]
      simp
    rw [minpoly.aeval] at happ
    have : ((minpoly ℂ T).coeff 0) • x = 0 := by
      rw [← happ]
      rfl
    rcases smul_eq_zero.mp this with h | h
    · exact hne h
    · exact hx0 h
  have hXdvd : Polynomial.X ∣ minpoly ℂ T := Polynomial.X_dvd_iff.mpr hc0
  obtain ⟨q, hq⟩ := hXdvd
  refine ⟨q, ?_, ?_, ?_⟩
  · rw [← hq]
    exact minpoly.aeval ℂ T
  · intro h0
    have hX2 : Polynomial.X ^ 2 ∣ minpoly ℂ T := by
      obtain ⟨s, hs⟩ := Polynomial.X_dvd_iff.mpr h0
      exact ⟨s, by rw [hq, hs]; ring⟩
    exact minpoly_zero_not_double_root T hsa hX2
  · intro n
    have hco : (minpoly ℂ T).coeff (n + 1) = q.coeff n := by
      rw [hq, Polynomial.coeff_X_mul]
    rw [← hco]
    exact minpoly_selfadjoint_real T hsa (n + 1)

/-- [KERNEL] ★★★ A TESTEMUNHA INCONDICIONAL DA FACE FINITA: para todo
    T = T† com kernel não-trivial, SpectralApproximationWitness T VALE —
    a fronteira do v85 é TEOREMA aqui. -/
theorem finite_face_witness_unconditional (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (hker : T.ker ≠ ⊥) :
    SpectralApproximationWitness T := by
  obtain ⟨q, hann, hc, hq⟩ := annihilating_word_exists T hsa hker
  exact spectral_witness_of_annihilating_word T hsa q hann hc hq

/-- [KERNEL] ★★★ O CANTO NA ÁLGEBRA, SEM HIPÓTESE EXTRA (face finita):
    P_{ker T} ∈ {T}″ ∧ P_{ker T} ∈ {T}′ para todo T = T† com kernel
    não-trivial — o canto pertence à álgebra (algébrica) de von Neumann
    do operador. -/
theorem finite_face_corner_in_algebra (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) (hker : T.ker ≠ ⊥) :
    (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer ∧
      (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer :=
  ⟨corner_in_algebra_of_approximation T
      (finite_face_witness_unconditional T hsa hker),
   corner_projection_in_commutant_set T hsa⟩

end

end TGLExt
