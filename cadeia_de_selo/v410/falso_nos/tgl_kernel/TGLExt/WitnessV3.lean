import TGLExt.NoNormalTrace

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 89 — WitnessV3: o tipo endurecido — o fator DENTRO da testemunha
  [TGLExt — v132, Bloco B do PLANO_ULTIMA_FLAG, pedra 2 de 3]

A lição v103 (11× aplicada): o nome reservado só é cunhado quando o TIPO
captura o espírito inteiro. O espírito nomeado pós-v123 era UM: o fator
III₁ DENTRO da FullWitnessData fundida. Esta pedra ENDURECE o tipo:

* `vnRatio`/`vnRealizedLog` — a razão modular realizada num (M, Ω)
  ABSTRATO (a generalização do objRatio da pedra 87);
* ★★★ `FullWitnessDataV3 extends FullWitnessData` — o contrato endurecido:
  TUDO da testemunha fundida (Poincaré fiel nas regiões e nas fibras,
  Dirac genuinamente ilimitado, frame curvo, fluxo, covariância) MAIS o
  pacote do fator: `factor : VonNeumannAlgebra FH` + Ω unitário cíclico +
  ω = ⟨Ω,·Ω⟩ WOT-sequencialmente NORMAL (a noção não é vácua) + ω
  NÃO-tracial + S-invariante realizada LOG-DENSA + **o assassinato:
  NENHUM funcional tracial normalizado sobre o fator é WOT-sequencialmente
  contínuo** — a definição operacional de III₁ que o programa selou
  ("o único traço é zero" + a marca densa + o objeto), como CAMPOS;
* ★★ `finiteDim_normal_trace_exists` — O MOTOR DO DENTE: em dimensão
  finita o traço ortonormal normalizado É aditivo, homogêneo, unital,
  tracial E WOT-sequencialmente contínuo;
* ★★★ `finiteDim_cannot_feed_witnessV3` — O DENTE (lição v103): NENHUMA
  bancada finito-dimensional pode habitar o tipo — o campo do assassinato
  colide com o traço que a dimensão finita sempre tem;
* ★★★ `theWitnessV3` — O HABITANTE (nome NÃO-reservado): a testemunha
  fundida do v123 casada com o fator da marca (⅓,¼) das pedras 86–88;
* ★ `witnessV3_infinite` — o habitante é forçosamente ∞-dimensional.

O gate NÃO se move por esta pedra (o nome reservado segue reservado até a
pedra 90). β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix UniformSpace Filter Topology
open scoped ComplexConjugate

noncomputable section

/-! ## A — a razão modular realizada num (M, Ω) abstrato -/

section Abstract

variable {FH : Type} [NormedAddCommGroup FH] [InnerProductSpace ℂ FH]
  [CompleteSpace FH]

/-- a razão modular r realizada em (M, Ω): A, B ∈ M com
    ⟨Ω,(AB)Ω⟩ = r·⟨Ω,(BA)Ω⟩ e ⟨Ω,(BA)Ω⟩ ≠ 0. -/
def vnRatio (M : VonNeumannAlgebra FH) (Om : FH) (r : ℝ) : Prop :=
  ∃ A B : FH →L[ℂ] FH, A ∈ M ∧ B ∈ M
    ∧ (inner ℂ Om ((A * B) Om) : ℂ)
        = ((r : ℝ) : ℂ) * inner ℂ Om ((B * A) Om)
    ∧ (inner ℂ Om ((B * A) Om) : ℂ) ≠ 0

/-- os log-ratios realizados em (M, Ω). -/
def vnRealizedLog (M : VonNeumannAlgebra FH) (Om : FH) : Set ℝ :=
  {t : ℝ | ∃ r : ℝ, 0 < r ∧ vnRatio M Om r ∧ t = Real.log r}

/-! ## B — O MOTOR DO DENTE: dimensão finita sempre tem traço normal -/

/-- [KERNEL] ★★ em dimensão finita (não-trivial) o traço ortonormal
    normalizado τ(T) = n⁻¹·Σᵢ⟨eᵢ, T eᵢ⟩ é aditivo, homogêneo, unital,
    TRACIAL em toda B(FH) e WOT-sequencialmente contínuo — a dimensão
    finita NUNCA mata o peso. -/
theorem finiteDim_normal_trace_exists
    (hfd : FiniteDimensional ℂ FH) (hpos : 0 < Module.finrank ℂ FH)
    (M : VonNeumannAlgebra FH) :
    ∃ τ : (FH →L[ℂ] FH) → ℂ,
      (∀ A B, τ (A + B) = τ A + τ B) ∧
      (∀ (c : ℂ) A, τ (c • A) = c * τ A) ∧
      τ 1 = 1 ∧
      (∀ A B, τ (A * B) = τ (B * A)) ∧
      SeqWOTContinuous M τ := by
  haveI := hfd
  have hne : Module.finrank ℂ FH ≠ 0 := hpos.ne'
  have hn0 : ((Module.finrank ℂ FH : ℕ) : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr hne
  set n : ℕ := Module.finrank ℂ FH with hn
  let b : OrthonormalBasis (Fin n) ℂ FH := stdOrthonormalBasis ℂ FH
  refine ⟨fun T => ((n : ℂ))⁻¹ * ∑ i, (inner ℂ (b i) (T (b i)) : ℂ),
    ?_, ?_, ?_, ?_, ?_⟩
  · intro A B
    simp only [ContinuousLinearMap.add_apply, inner_add_right,
      Finset.sum_add_distrib, mul_add]
  · intro c A
    simp only [ContinuousLinearMap.smul_apply, inner_smul_right,
      ← Finset.mul_sum]
    ring
  · dsimp only
    have h1 : ∀ i : Fin n,
        (inner ℂ (b i) ((1 : FH →L[ℂ] FH) (b i)) : ℂ) = 1 := by
      intro i
      have hid : (1 : FH →L[ℂ] FH) (b i) = b i := rfl
      rw [hid, inner_self_eq_norm_sq_to_K, b.orthonormal.1 i]
      norm_num
    rw [Finset.sum_congr rfl (fun i _ => h1 i), Finset.sum_const,
      Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one,
      inv_mul_cancel₀ hn0]
  · intro A B
    dsimp only
    have key : ∀ S T : FH →L[ℂ] FH,
        (∑ i, (inner ℂ (b i) ((S * T) (b i)) : ℂ))
          = ∑ i, ∑ j, (inner ℂ (b j) (T (b i)) : ℂ)
              * (inner ℂ (b i) (S (b j)) : ℂ) := by
      intro S T
      refine Finset.sum_congr rfl fun i _ => ?_
      have hexp : (S * T) (b i) = S (T (b i)) := rfl
      rw [hexp]
      conv_lhs => rw [show T (b i)
        = ∑ j, (inner ℂ (b j) (T (b i)) : ℂ) • b j
        from (b.sum_repr' (T (b i))).symm]
      rw [map_sum, inner_sum]
      refine Finset.sum_congr rfl fun j _ => ?_
      rw [map_smul, inner_smul_right]
    congr 1
    rw [key A B, key B A]
    conv_rhs => rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    ring
  · intro T Tinf C hmem hminf hC hwot
    dsimp only
    have hterm : ∀ i : Fin n,
        Tendsto (fun k => (inner ℂ (b i) (T k (b i)) : ℂ)) atTop
          (nhds (inner ℂ (b i) (Tinf (b i)))) := fun i => hwot (b i) (b i)
    have hsum : Tendsto (fun k => ∑ i, (inner ℂ (b i) (T k (b i)) : ℂ))
        atTop (nhds (∑ i, (inner ℂ (b i) (Tinf (b i)) : ℂ))) :=
      tendsto_finsetSum _ (fun i _ => hterm i)
    exact hsum.const_mul _

end Abstract

/-! ## C — O TIPO ENDURECIDO -/

/-- [DATA — O CONTRATO ENDURECIDO DA TESTEMUNHA, v132] a testemunha
    completa COM O FATOR DENTRO: a FullWitnessData fundida (Poincaré,
    Dirac ilimitado, frame, fluxo, covariância) + o objeto de von Neumann
    com Ω cíclico, estado normal não-tracial, S-invariante log-densa e o
    ASSASSINATO do traço normal — a metade antes não-tipável (III₁ na
    definição operacional do programa), agora TIPADA como campos. -/
structure FullWitnessDataV3 extends FullWitnessData where
  FH : Type
  [instNACG : NormedAddCommGroup FH]
  [instIPS : InnerProductSpace ℂ FH]
  [instCS : CompleteSpace FH]
  factor : VonNeumannAlgebra FH
  Om : FH
  om_unit : ‖Om‖ = 1
  om_cyclic : Dense ((fun T : FH →L[ℂ] FH => T Om) ''
    (factor : Set (FH →L[ℂ] FH)))
  om_normal : SeqWOTContinuous factor
    (fun T : FH →L[ℂ] FH => (inner ℂ Om (T Om) : ℂ))
  state_not_tracial : ∃ A B : FH →L[ℂ] FH, A ∈ factor ∧ B ∈ factor
    ∧ (inner ℂ Om ((A * B) Om) : ℂ) ≠ inner ℂ Om ((B * A) Om)
  ratio_log_dense : Dense
    ((AddSubgroup.closure (vnRealizedLog factor Om) : AddSubgroup ℝ) : Set ℝ)
  no_normal_tracial : ∀ τ : (FH →L[ℂ] FH) → ℂ,
    (∀ A B, τ (A + B) = τ A + τ B) →
    (∀ (c : ℂ) A, τ (c • A) = c * τ A) →
    τ 1 = 1 →
    (∀ A B, A ∈ factor → B ∈ factor → τ (A * B) = τ (B * A)) →
    SeqWOTContinuous factor τ → False

attribute [instance] FullWitnessDataV3.instNACG FullWitnessDataV3.instIPS
  FullWitnessDataV3.instCS

/-- [KERNEL] ★ a ponte de tipos: toda testemunha V3 reduz à completa —
    o V3 CONTÉM o V2 que contém o v1 endurecido. -/
def fullFromWitnessV3 (w : FullWitnessDataV3) : FullWitnessData :=
  w.toFullWitnessData

/-! ## D — O DENTE (lição v103) -/

/-- [KERNEL] ★★★ O DENTE: NENHUMA bancada finito-dimensional habita o
    tipo endurecido — em dimensão finita o traço ortonormal normalizado
    satisfaz TODAS as hipóteses do campo do assassinato, e o campo o
    proíbe. A testemunha V3 é forçosamente ∞-dimensional. -/
theorem finiteDim_cannot_feed_witnessV3 (w : FullWitnessDataV3) :
    ¬ FiniteDimensional ℂ w.FH := by
  intro hfd
  have hOm : w.Om ≠ 0 := by
    intro h0
    have hu := w.om_unit
    rw [h0, norm_zero] at hu
    norm_num at hu
  haveI : Nontrivial w.FH := ⟨w.Om, 0, hOm⟩
  haveI := hfd
  have hpos : 0 < Module.finrank ℂ w.FH := Module.finrank_pos
  obtain ⟨τ, hadd, hsmul, hone, htr, hnormal⟩ :=
    finiteDim_normal_trace_exists hfd hpos w.factor
  exact w.no_normal_tracial τ hadd hsmul hone
    (fun A B _ _ => htr A B) hnormal

/-! ## E — O HABITANTE (nome não-reservado) -/

/-- [KERNEL] ★★★ A TESTEMUNHA V3 HABITADA (nome NÃO-reservado): a
    testemunha fundida do v123 (Poincaré fiel nas regiões E nas fibras)
    casada com o fator da marca (⅓,¼) — o objeto M_TGL, Ω cíclico
    unitário, ω normal não-tracial, S-invariante log-densa e o
    assassinato do peso, TODOS como campos habitados por teorema. -/
def theWitnessV3 : FullWitnessDataV3 where
  toFullWitnessData := theFusedWitness
  FH := TowerHilbert mixProfile
  factor := theFactorObject mixProfile
  Om := hOmega mixProfile
  om_unit := hOmega_norm
  om_cyclic := factor_omega_cyclic
  om_normal := omegaState_seqWOT mixProfile
  state_not_tracial := by
    obtain ⟨A, B, hA, hB, hne⟩ := omega_not_tracial mixProfile (by
      rw [show mixProfile.w 0 = 1 / 3 from rfl]
      norm_num)
    exact ⟨A, B, hA, hB, hne⟩
  ratio_log_dense := by
    have hsub : realizedLog
        ⊆ vnRealizedLog (theFactorObject mixProfile) (hOmega mixProfile) := by
      rintro t ⟨r, hr, ⟨N, A, B, heq, hne⟩, rfl⟩
      exact ⟨r, hr, ⟨towerPi mixProfile A, towerPi mixProfile B,
        towerPi_mem_factor _, towerPi_mem_factor _, heq, hne⟩, rfl⟩
    have hmono := AddSubgroup.closure_mono hsub
    apply Dense.mono _ signature_log_dense
    exact_mod_cast hmono
  no_normal_tracial := fun τ hadd hsmul hone htr hnormal =>
    no_normal_tracial_state_mix τ hadd hsmul hone htr hnormal

/-- [KERNEL] ★ o habitante é forçosamente ∞-dimensional: o dente morde
    a própria casa — H_φ(⅓,¼) não é finito-dimensional, POR TEOREMA. -/
theorem witnessV3_infinite : ¬ FiniteDimensional ℂ (theWitnessV3.FH) :=
  finiteDim_cannot_feed_witnessV3 theWitnessV3

/-- [KERNEL] ★★ A SÍNTESE DA PEDRA 89: o tipo endurecido existe, o dente
    proíbe a bancada, o habitante vive — com o fator da marca (⅓,¼), o
    vetor do Nome e o assassinato DENTRO da testemunha. -/
theorem witnessV3_synthesis :
    (¬ FiniteDimensional ℂ (theWitnessV3.FH))
    ∧ theWitnessV3.factor = theFactorObject mixProfile
    ∧ theWitnessV3.Om = hOmega mixProfile :=
  ⟨witnessV3_infinite, rfl, rfl⟩

end

end TGLExt
