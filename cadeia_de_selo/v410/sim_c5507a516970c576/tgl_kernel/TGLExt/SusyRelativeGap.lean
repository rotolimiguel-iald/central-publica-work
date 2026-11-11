import TGLExt.LocalBreuerGap

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O NÍVEL 4 DA CAMADA: SUSY-relativo ⟹ gap local de Breuer
  [TGLExt — v65, completando a arquitetura da Resposta 8]

A Resposta 8 desenhou QUATRO níveis de dados (Q8.3). O v64 tipou os
níveis 1 e 3 e compôs o (B3). Esta pedra fecha o NÍVEL 4:
`SusyRelativeData` — o certificado de que o operador LIVRE tem gap
τ-finito (fisicamente VAZIO: spec(D₀) ⊂ [¼,∞), ε < ½), a perturbação é
relativamente τ-compacta (tipado: o gap do perturbado está sob o do
livre ⊔ um suporte τ-finito — a face reticular do teorema de Weyl
relativo), e o kernel habita o gap. TEOREMA: nível 4 ⟹ nível 3 ⟹ (B3).
É a forma tipada do `susy_relative_compact_gives_breuer_gap` que o
especialista pediu. E duas faces novas que cedem terreno solo:

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★ `susy_relative_gap_finite` — do certificado SUSY-relativo segue a
  finitude do gap do PERTURBADO: τ(P_ε(D)) ≤ τ(P_ε(D₀)) + τ(diff) < ∞
  (monotonia + SUBADITIVIDADE do traço sobre o sup — o mecanismo de
  Weyl relativo em forma reticular);
* ★ `susy_relative_gives_breuer` — **NÍVEL 4 ⟹ (B3)**: a composição
  completa SusyRelativeData → BreuerGapData → 0 < τ(ker) < ∞;
* ★ `susy_relative_package_consistent` — o nível 4 é HABITADO;
* ★ `perturbation_injective_on_kernel` / `kernel_dim_le_rank_of_perturbation`
  — **a face DISCRETA de Birman–Schwinger**: se H₀ é positivo-definido
  (o livre tem gap) então V é INJETIVA sobre ker(H₀ − V), logo
  **dim ker(H₀ − V) ≤ posto(V)** — o número de modos zero é limitado
  pelo POSTO DA INSCRIÇÃO. O modo zero do TGL é único porque a
  inscrição −½sech² é de posto um no sentido do limite;
* ★ `discrete_parallel_solder_preserves_metric` — **o germe da
  solda-campo**: a face algébrica discreta de ∇e = 0 — se o transporte
  Λ é isométrico (Λᵀ η Λ = η) e e′ = Λ e, então e′ᵀ η e′ = eᵀ η e:
  a solda transportada inscreve a MESMA métrica. O que falta para o
  campo contínuo é exatamente o core (a parede única).

VOCABULÁRIO: a subaditividade τ(p ⊔ q) ≤ τ(p) + τ(q) é verdadeira para
traços genuínos (Kaplansky: p∨q − q ∼ p − p∧q) e entra como DADO da
camada, não como fabricação; a instanciação no double core GENUÍNO
segue ABERTA e nomeada. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal
open Matrix

noncomputable section

/- ═══════ 1. A camada subaditiva e o certificado nível 4 ═══════ -/

/-- [DATA] camada tracial semifinita SUBADITIVA: o peso respeita
    τ(p ⊔ q) ≤ τ(p) + τ(q) (verdadeiro para traços: Kaplansky). -/
structure SubadditiveTraceData (L : Type) [Lattice L] [BoundedOrder L]
    extends SemifiniteTraceData L where
  subadd : ∀ p q : L, tau (p ⊔ q) ≤ tau p + tau q

/-- [DATA — Q8.3, nível 4] o certificado SUSY-relativo: gap do livre
    τ-finito (fisicamente ⊥); gap do perturbado sob livre ⊔ diferença
    (Weyl relativo, face reticular); diferença τ-finita; kernel no gap. -/
structure SusyRelativeData (L : Type) [Lattice L] [BoundedOrder L]
    (T : SubadditiveTraceData L) where
  ker : L
  gapD : L
  gapD0 : L
  diff : L
  free_gap_finite : T.tau gapD0 < ⊤
  gap_relative : gapD ≤ gapD0 ⊔ diff
  diff_finite : T.tau diff < ⊤
  ker_le_gap : ker ≤ gapD
  ker_ne_bot : ker ≠ ⊥

variable {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}

/- ═══════ 2. Nível 4 ⟹ nível 3 ⟹ (B3) ═══════ -/

/-- [KERNEL] ★ O GAP DO PERTURBADO É FINITO: monotonia sob o Weyl
    relativo + subaditividade — τ(P_ε(D)) ≤ τ(P_ε(D₀)) + τ(diff) < ∞. -/
theorem susy_relative_gap_finite (S : SusyRelativeData L T) :
    T.tau S.gapD < ⊤ :=
  lt_of_le_of_lt (T.mono S.gap_relative)
    (lt_of_le_of_lt (T.subadd S.gapD0 S.diff)
      (ENNReal.add_lt_top.mpr ⟨S.free_gap_finite, S.diff_finite⟩))

/-- [KERNEL] o empacotamento: nível 4 constrói o nível 3. -/
def SusyRelativeData.toBreuerGapData (S : SusyRelativeData L T) :
    BreuerGapData L T.toSemifiniteTraceData where
  ker := S.ker
  gap := S.gapD
  ker_le_gap := S.ker_le_gap
  gap_finite := susy_relative_gap_finite S
  ker_ne_bot := S.ker_ne_bot

/-- [KERNEL] ★★ NÍVEL 4 ⟹ (B3): a composição completa da arquitetura
    da Resposta 8 — do certificado SUSY-relativo segue
    0 < τ(1_{{0}}(𝔻)) < ∞ (o `susy_relative_compact_gives_breuer_gap`
    pedido, na camada tipada). -/
theorem susy_relative_gives_breuer (S : SusyRelativeData L T) :
    0 < T.tau S.ker ∧ T.tau S.ker < ⊤ :=
  breuer_kernel_weight S.toBreuerGapData

/-- [MODEL] a camada subaditiva é habitada (peso identidade em ℝ≥0∞:
    p ⊔ q = max ≤ p + q). -/
def idTraceSub : SubadditiveTraceData ℝ≥0∞ where
  toSemifiniteTraceData := idTrace
  subadd := fun p q => sup_le le_self_add le_add_self

/-- [MODEL] o certificado nível 4 é habitado (livre com gap VAZIO ⊥;
    diferença de peso 1; kernel = gap = 1). -/
def modelSusy : SusyRelativeData ℝ≥0∞ idTraceSub where
  ker := 1
  gapD := 1
  gapD0 := ⊥
  diff := 1
  free_gap_finite := bot_lt_top
  gap_relative := le_sup_right
  diff_finite := ENNReal.one_lt_top
  ker_le_gap := le_rfl
  ker_ne_bot := one_ne_zero

/-- [KERNEL] ★ CONSISTÊNCIA do nível 4: o certificado não é vazio. -/
theorem susy_relative_package_consistent :
    Nonempty (SusyRelativeData ℝ≥0∞ idTraceSub) := ⟨modelSusy⟩

/- ═══════ 3. A face discreta de Birman–Schwinger ═══════ -/

/-- [KERNEL] ★ V É INJETIVA SOBRE O KERNEL DO PERTURBADO: se H₀ é
    positivo-definido (o livre tem gap) e (H₀ − V) x = 0 com V x = 0,
    então H₀ x = 0 e a positividade força x = 0. -/
theorem perturbation_injective_on_kernel {n : Type} [Fintype n]
    (H0 V : Matrix n n ℝ)
    (hpd : ∀ x : n → ℝ, x ≠ 0 → 0 < x ⬝ᵥ (H0 *ᵥ x))
    (x : n → ℝ) (hker : (H0 - V) *ᵥ x = 0) (hVx : V *ᵥ x = 0) : x = 0 := by
  have hH0x : H0 *ᵥ x = 0 := by
    have h := hker
    rw [Matrix.sub_mulVec, hVx, sub_zero] at h
    exact h
  by_contra hx0
  have hpos := hpd x hx0
  rw [hH0x] at hpos
  simp at hpos

/-- [KERNEL] ★★ A FACE DISCRETA DE BIRMAN--SCHWINGER: dim ker(H₀ − V) ≤
    posto(V) — **o número de modos zero é limitado pelo POSTO DA
    INSCRIÇÃO**. O modo zero do TGL é único porque a inscrição
    −½sech²(κ/2) é de posto um (um único estado ligado). -/
theorem kernel_dim_le_rank_of_perturbation {n : Type} [Fintype n]
    [DecidableEq n]
    (H0 V : Matrix n n ℝ)
    (hpd : ∀ x : n → ℝ, x ≠ 0 → 0 < x ⬝ᵥ (H0 *ᵥ x)) :
    Module.finrank ℝ (LinearMap.ker (H0 - V).mulVecLin) ≤
      Module.finrank ℝ (LinearMap.range V.mulVecLin) := by
  set K := LinearMap.ker (H0 - V).mulVecLin
  set f := V.mulVecLin.domRestrict K
  have hinj : Function.Injective f := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro a ha
    have hxK : (H0 - V) *ᵥ (a : n → ℝ) = 0 := by
      have := a.2
      rwa [LinearMap.mem_ker, Matrix.mulVecLin_apply] at this
    have hVx : V *ᵥ (a : n → ℝ) = 0 := by
      simpa [f, LinearMap.domRestrict_apply, Matrix.mulVecLin_apply] using ha
    have hx0 : (a : n → ℝ) = 0 :=
      perturbation_injective_on_kernel H0 V hpd _ hxK hVx
    exact Subtype.ext hx0
  have hle : LinearMap.range f ≤ LinearMap.range V.mulVecLin := by
    rintro y ⟨a, rfl⟩
    exact ⟨(a : n → ℝ), by simp [f, LinearMap.domRestrict_apply]⟩
  calc Module.finrank ℝ K
      = Module.finrank ℝ (LinearMap.range f) :=
        (LinearMap.finrank_range_of_inj hinj).symm
    _ ≤ Module.finrank ℝ (LinearMap.range V.mulVecLin) :=
        Submodule.finrank_mono hle

/- ═══════ 4. O germe da solda-campo ═══════ -/

/-- [KERNEL] ★ A SOLDA TRANSPORTADA INSCREVE A MESMA MÉTRICA — a face
    algébrica discreta de ∇e = 0 (o germe da solda-campo): se o
    transporte Λ é isométrico (Λᵀ η Λ = η) e e′ = Λ e, então
    e′ᵀ η e′ = eᵀ η e. O que falta para o campo CONTÍNUO é exatamente
    o core — a parede única. -/
theorem discrete_parallel_solder_preserves_metric {n : Type} [Fintype n]
    (eta Lam e : Matrix n n ℝ) (hiso : Lamᵀ * eta * Lam = eta) :
    (Lam * e)ᵀ * eta * (Lam * e) = eᵀ * eta * e := by
  rw [Matrix.transpose_mul]
  have h : eᵀ * Lamᵀ * eta * (Lam * e) = eᵀ * (Lamᵀ * eta * Lam) * e := by
    noncomm_ring
  rw [h, hiso]

end

end TGLExt
