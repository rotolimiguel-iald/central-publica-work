import TGLExt.RetaDeLuzBorchers
import Mathlib.Algebra.Order.Interval.Set.Group
import Mathlib.Algebra.Order.ToIntervalMod
import Mathlib.MeasureTheory.Group.LIntegral

/-!
# A RETA DE LUZ, elo 2: o boost da reta NAO tem autovetor (espectro sem pontos)
  [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\forma_inscrita_da_luz\habitante_v3\lean\RetaDeLuzEspectro.lean` (sha16 ee7e55e5924bff52): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: nenhum.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]

  [DERIVED] se D(s) f = c(s) f com |c(s)| = 1 para TODO s (a forma de `NoEigenOutsideVacuum` do contrato,
  com a fase livre), entao f = 0. Argumento: |f|^2 fica 1-periodica q.t.p.; a integral sobre R e a soma,
  sobre Z, de copias IGUAIS da integral em [0, 1); finita so se cada copia e zero.
  Leitura: no espaco de UMA particula nao ha vacuo; logo «sem autovetor fora da reta do vacuo» vira
  «sem autovetor nenhum». Com Delta^{it} := D(2 pi t) (definicao do elo 1), o candidato modular tambem nao
  tem autovetor (corolario). ⚠ Que D(2 pi t) seja o grupo modular de um subespaco padrao segue [OPEN].
-/

set_option autoImplicit false

noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal

namespace TGLExt.RetaDeLuz

/-- [DERIVED] ★ a dilatacao da reta de luz nao tem autovetor em L^2. -/
theorem D_no_eigen (f : L2R) (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ D s f = c • f) : f = 0 := by
  set g : ℝ → ℝ≥0∞ := fun ξ => ‖f ξ‖ₑ ^ ((2 : ℝ≥0∞).toReal) with hg
  have hfin : ∫⁻ ξ, g ξ < ∞ :=
    lintegral_rpow_enorm_lt_top_of_eLpNorm_lt_top (p := 2) two_ne_zero ENNReal.ofNat_ne_top
      (Lp.eLpNorm_lt_top f)
  -- |f|^2 e invariante por translacao inteira, q.t.p.
  have hper : ∀ n : ℤ, (fun ξ => g (ξ + n)) =ᵐ[volume] g := by
    intro n
    obtain ⟨c, hc, hD⟩ := h (-(n : ℝ))
    have h1 := D_ae (-(n : ℝ)) f
    rw [hD] at h1
    have h2 := Lp.coeFn_smul c f
    have hce : ‖c‖ₑ = 1 := by rw [← ofReal_norm, hc, ENNReal.ofReal_one]
    filter_upwards [h1, h2] with ξ e1 e2
    simp only [hg]
    rw [neg_neg] at e1
    rw [← e1, e2, Pi.smul_apply, smul_eq_mul, enorm_mul, hce, one_mul]
  -- cada ladrilho [n, n+1) pesa o mesmo que [0, 1)
  have hpiece : ∀ n : ℤ, ∫⁻ ξ in Ico (n : ℝ) (n + 1), g ξ = ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ := by
    intro n
    rw [← lintegral_indicator measurableSet_Ico, ← lintegral_indicator measurableSet_Ico]
    calc ∫⁻ ξ, (Ico (n : ℝ) (n + 1)).indicator g ξ
        = ∫⁻ ξ, (Ico (n : ℝ) (n + 1)).indicator g (ξ + n) :=
          (lintegral_add_right_eq_self _ (n : ℝ)).symm
      _ = ∫⁻ ξ, (Ico (0 : ℝ) 1).indicator g ξ := by
          apply lintegral_congr_ae
          filter_upwards [hper n] with ξ hξ
          by_cases hm : ξ ∈ Ico (0 : ℝ) 1
          · have hm' : ξ + n ∈ Ico (n : ℝ) (n + 1) := ⟨by linarith [hm.1], by linarith [hm.2]⟩
            rw [indicator_of_mem hm', indicator_of_mem hm, hξ]
          · have hm' : ξ + n ∉ Ico (n : ℝ) (n + 1) := fun h' =>
              hm ⟨by linarith [h'.1], by linarith [h'.2]⟩
            rw [indicator_of_notMem hm', indicator_of_notMem hm]
  -- a integral total e a soma dos ladrilhos
  have htot : ∫⁻ ξ, g ξ = ∑' _n : ℤ, ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ := by
    rw [← setLIntegral_univ, ← iUnion_Ico_intCast (α := ℝ),
      lintegral_iUnion (fun n => measurableSet_Ico) (pairwise_disjoint_Ico_intCast (α := ℝ)) g]
    exact tsum_congr hpiece
  have hC : ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ = 0 := by
    by_contra hne
    have htop := ENNReal.tsum_const_eq_top_of_ne_zero (α := ℤ) hne
    rw [htot, htop] at hfin
    exact lt_irrefl _ hfin
  have hzero : ∫⁻ ξ, g ξ = 0 := by rw [htot, hC, tsum_zero]
  have hgm : AEMeasurable g volume :=
    ((Lp.aestronglyMeasurable f).enorm).pow_const _
  have hgae : g =ᵐ[volume] 0 := (lintegral_eq_zero_iff' hgm).mp hzero
  apply Lp.ext
  filter_upwards [hgae, Lp.coeFn_zero ℂ 2 (volume : Measure ℝ)] with ξ hξ hz
  rw [hz]
  simp only [hg, Pi.zero_apply] at hξ
  have hpos : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  rw [ENNReal.rpow_eq_zero_iff] at hξ
  rcases hξ with ⟨h0, _⟩ | ⟨_, hneg⟩
  · simpa using h0
  · exact absurd hneg (not_lt.mpr hpos.le)

/-- [DERIVED] corolario: o candidato modular Delta^{it} := D(2 pi t) nao tem autovetor. -/
theorem modularCandidate_no_eigen (f : L2R)
    (h : ∀ t : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ modularCandidate t f = c • f) : f = 0 := by
  apply D_no_eigen f
  intro s
  obtain ⟨c, hc, hD⟩ := h (s / (2 * Real.pi))
  refine ⟨c, hc, ?_⟩
  have e : 2 * Real.pi * (s / (2 * Real.pi)) = s := by
    field_simp
  simpa [modularCandidate, e] using hD

#print axioms D_no_eigen
#print axioms modularCandidate_no_eigen

end TGLExt.RetaDeLuz
