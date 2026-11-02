-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_049 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import Mathlib.MeasureTheory.Function.Holder
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! Concrete bounded multipliers on Lebesgue L².
No identification with a spacetime action or a functional-calculus modular phase is assumed. -/

set_option autoImplicit false

noncomputable section
open MeasureTheory Filter
open scoped ENNReal ComplexConjugate

namespace ChatgptAudit.Continuous049

abbrev SpectralHilbert := Lp ℂ 2 (volume : Measure ℝ)

/-- The positive bounded graph coordinate. -/
def spectralWeightA (c x : ℝ) : ℝ :=
  Real.exp (c * x / 2) / Real.sqrt (Real.exp (c * x) + Real.exp (-c * x))

/-- The second bounded graph coordinate. -/
def spectralWeightB (c x : ℝ) : ℝ :=
  Real.exp (-c * x / 2) / Real.sqrt (Real.exp (c * x) + Real.exp (-c * x))

theorem spectral_weight_den_pos (c x : ℝ) :
    0 < Real.sqrt (Real.exp (c * x) + Real.exp (-c * x)) :=
  Real.sqrt_pos.2 (add_pos (Real.exp_pos _) (Real.exp_pos _))

theorem spectral_weightA_pos (c x : ℝ) : 0 < spectralWeightA c x :=
  div_pos (Real.exp_pos _) (spectral_weight_den_pos c x)

theorem spectral_weightB_pos (c x : ℝ) : 0 < spectralWeightB c x :=
  div_pos (Real.exp_pos _) (spectral_weight_den_pos c x)

theorem spectral_weight_square_sum (c x : ℝ) :
    spectralWeightA c x ^ 2 + spectralWeightB c x ^ 2 = 1 := by
  have ha : Real.exp (c * x / 2) ^ 2 = Real.exp (c * x) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hb : Real.exp (-c * x / 2) ^ 2 = Real.exp (-c * x) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hd := Real.sq_sqrt (le_of_lt (add_pos (Real.exp_pos (c * x))
    (Real.exp_pos (-c * x))))
  unfold spectralWeightA spectralWeightB
  rw [div_pow, div_pow, ← add_div, ha, hb, hd]
  exact div_self (ne_of_gt (add_pos (Real.exp_pos _) (Real.exp_pos _)))

theorem spectral_weightA_le_one (c x : ℝ) : spectralWeightA c x ≤ 1 := by
  have := spectral_weight_square_sum c x
  have := spectral_weightA_pos c x
  nlinarith [sq_nonneg (spectralWeightB c x)]

theorem spectral_weightB_le_one (c x : ℝ) : spectralWeightB c x ≤ 1 := by
  have := spectral_weight_square_sum c x
  have := spectral_weightB_pos c x
  nlinarith [sq_nonneg (spectralWeightA c x)]

theorem spectral_weightA_norm_le_one (c x : ℝ) : ‖spectralWeightA c x‖ ≤ 1 := by
  simpa only [Real.norm_eq_abs, abs_of_pos (spectral_weightA_pos c x)] using
    spectral_weightA_le_one c x

theorem spectral_weightB_norm_le_one (c x : ℝ) : ‖spectralWeightB c x‖ ≤ 1 := by
  simpa only [Real.norm_eq_abs, abs_of_pos (spectral_weightB_pos c x)] using
    spectral_weightB_le_one c x

theorem spectral_weightA_continuous (c : ℝ) : Continuous (spectralWeightA c) := by
  unfold spectralWeightA
  apply Continuous.div
  · fun_prop
  · fun_prop
  · intro x
    exact ne_of_gt (spectral_weight_den_pos c x)

theorem spectral_weightB_continuous (c : ℝ) : Continuous (spectralWeightB c) := by
  unfold spectralWeightB
  apply Continuous.div
  · fun_prop
  · fun_prop
  · intro x
    exact ne_of_gt (spectral_weight_den_pos c x)

theorem spectral_weight_reflection (c x : ℝ) :
    spectralWeightA c (-x) = spectralWeightB c x := by
  simp only [spectralWeightA, spectralWeightB, mul_neg, neg_mul, neg_neg, add_comm]

theorem spectral_weightB_reflection (c x : ℝ) :
    spectralWeightB c (-x) = spectralWeightA c x := by
  simpa only [neg_neg] using (spectral_weight_reflection c (-x)).symm

theorem spectral_weight_ratio (c x : ℝ) :
    spectralWeightB c x = Real.exp (-c * x) * spectralWeightA c x := by
  unfold spectralWeightA spectralWeightB
  rw [← mul_div_assoc, ← Real.exp_add]
  congr 2
  ring

/-- A bounded measurable weight regarded as an L∞ vector. -/
def boundedSpectralWeight (w : ℝ → ℝ) (hw : Continuous w) (hb : ∀ x, ‖w x‖ ≤ 1) :
    Lp ℂ ∞ (volume : Measure ℝ) :=
  (memLp_top_of_bound (Complex.continuous_ofReal.comp hw).aestronglyMeasurable 1
    (Eventually.of_forall fun x => by simpa only [Function.comp_apply, Complex.norm_real] using hb x)).toLp _

theorem bounded_spectral_weight_ae (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) :
    boundedSpectralWeight w hw hb =ᵐ[volume] fun x => (w x : ℂ) :=
  MemLp.coeFn_toLp _

/-- Multiplication is constructed through the L∞ × L² Hölder map. -/
def boundedSpectralMultiplier (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  (ContinuousLinearMap.lsmul ℂ ℂ).holderL volume ∞ 2 2
    (boundedSpectralWeight w hw hb)

theorem bounded_spectral_multiplier_ae (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (f : SpectralHilbert) :
    boundedSpectralMultiplier w hw hb f =ᵐ[volume] fun x => (w x : ℂ) * f x := by
  have h := (ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder
    (r := 2) (boundedSpectralWeight w hw hb) f
  filter_upwards [h, bounded_spectral_weight_ae w hw hb] with x hx hwx
  simpa only [boundedSpectralMultiplier, ContinuousLinearMap.holderL_apply_apply,
    ContinuousLinearMap.lsmul_apply, smul_eq_mul, hwx] using hx

theorem bounded_spectral_multiplier_norm (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (f : SpectralHilbert) :
    ‖boundedSpectralMultiplier w hw hb f‖ ≤ ‖f‖ := by
  apply Lp.norm_le_norm_of_ae_le
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f] with x hx
  rw [hx, norm_mul, Complex.norm_real]
  exact (mul_le_mul_of_nonneg_right (hb x) (norm_nonneg (f x))).trans_eq (one_mul _)

theorem bounded_spectral_multiplier_selfadjoint (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) : IsSelfAdjoint (boundedSpectralMultiplier w hw hb) := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.2
  intro f g
  simp only [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f,
    bounded_spectral_multiplier_ae w hw hb g] with x hf hg
  change inner ℂ ((boundedSpectralMultiplier w hw hb f) x) (g x) =
    inner ℂ (f x) ((boundedSpectralMultiplier w hw hb g) x)
  rw [hf, hg]
  simp [RCLike.inner_apply]
  ring

def spectralA (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  boundedSpectralMultiplier (spectralWeightA c) (spectral_weightA_continuous c)
    (spectral_weightA_norm_le_one c)

def spectralB (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  boundedSpectralMultiplier (spectralWeightB c) (spectral_weightB_continuous c)
    (spectral_weightB_norm_le_one c)

theorem spectralA_ae (c : ℝ) (f : SpectralHilbert) :
    spectralA c f =ᵐ[volume] fun x => (spectralWeightA c x : ℂ) * f x :=
  bounded_spectral_multiplier_ae _ _ _ f

theorem spectralB_ae (c : ℝ) (f : SpectralHilbert) :
    spectralB c f =ᵐ[volume] fun x => (spectralWeightB c x : ℂ) * f x :=
  bounded_spectral_multiplier_ae _ _ _ f

theorem spectralA_norm_le (c : ℝ) (f : SpectralHilbert) : ‖spectralA c f‖ ≤ ‖f‖ :=
  bounded_spectral_multiplier_norm _ _ _ f

theorem spectralB_norm_le (c : ℝ) (f : SpectralHilbert) : ‖spectralB c f‖ ≤ ‖f‖ :=
  bounded_spectral_multiplier_norm _ _ _ f

theorem spectralA_selfadjoint (c : ℝ) : IsSelfAdjoint (spectralA c) :=
  bounded_spectral_multiplier_selfadjoint _ _ _

theorem spectralB_selfadjoint (c : ℝ) : IsSelfAdjoint (spectralB c) :=
  bounded_spectral_multiplier_selfadjoint _ _ _

theorem spectralAB_commute (c : ℝ) : spectralA c * spectralB c = spectralB c * spectralA c := by
  apply ContinuousLinearMap.ext
  intro f
  apply Lp.ext
  filter_upwards [spectralA_ae c (spectralB c f), spectralB_ae c (spectralA c f),
    spectralA_ae c f, spectralB_ae c f] with x hab hba ha hb
  change (spectralA c (spectralB c f)) x = (spectralB c (spectralA c f)) x
  rw [hab, hba, ha, hb]
  ring

theorem spectralAB_square_sum (c : ℝ) :
    spectralA c * spectralA c + spectralB c * spectralB c = 1 := by
  apply ContinuousLinearMap.ext
  intro f
  apply Lp.ext
  filter_upwards [spectralA_ae c (spectralA c f), spectralB_ae c (spectralB c f),
    spectralA_ae c f, spectralB_ae c f,
    Lp.coeFn_add (spectralA c (spectralA c f)) (spectralB c (spectralB c f))]
      with x haa hbb ha hb hadd
  change (spectralA c (spectralA c f) + spectralB c (spectralB c f)) x = f x
  rw [hadd]
  change (spectralA c (spectralA c f)) x + (spectralB c (spectralB c f)) x = f x
  rw [haa, hbb, ha, hb]
  have hs : (spectralWeightA c x : ℂ) ^ 2 + (spectralWeightB c x : ℂ) ^ 2 = 1 := by
    exact_mod_cast spectral_weight_square_sum c x
  calc
    _ = ((spectralWeightA c x : ℂ) ^ 2 + (spectralWeightB c x : ℂ) ^ 2) * f x := by ring
    _ = f x := by rw [hs, one_mul]

theorem spectralA_injective (c : ℝ) : Function.Injective (spectralA c) := by
  intro f g hfg
  apply Lp.ext
  filter_upwards [spectralA_ae c f, spectralA_ae c g] with x hf hg
  have he := congrArg (fun u : SpectralHilbert => u x) hfg
  rw [hf, hg] at he
  have hn : (spectralWeightA c x : ℂ) ≠ 0 := by
    exact_mod_cast ne_of_gt (spectral_weightA_pos c x)
  exact mul_left_cancel₀ hn he

theorem spectralAB_quadratic_nonneg (c : ℝ) (h : SpectralHilbert) :
    0 ≤ (inner ℂ (spectralA c h) (spectralB c h)).re := by
  rw [L2.inner_def]
  change 0 ≤ RCLike.re (∫ x : ℝ, inner ℂ ((spectralA c h) x) ((spectralB c h) x))
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (spectralA c h) (spectralB c h))]
  apply integral_nonneg_of_ae
  filter_upwards [spectralA_ae c h, spectralB_ae c h] with x ha hb
  rw [ha, hb]
  change 0 ≤ (inner ℂ ((spectralWeightA c x : ℂ) * h x)
    ((spectralWeightB c x : ℂ) * h x)).re
  have he : (inner ℂ ((spectralWeightA c x : ℂ) * h x)
      ((spectralWeightB c x : ℂ) * h x)).re =
      spectralWeightA c x * spectralWeightB c x * ‖h x‖ ^ 2 := by
    simp [RCLike.inner_apply, Complex.mul_re, Complex.normSq_apply,
      Complex.sq_norm, mul_add]
    ring
  rw [he]
  exact mul_nonneg (mul_nonneg (le_of_lt (spectral_weightA_pos c x))
    (le_of_lt (spectral_weightB_pos c x))) (sq_nonneg ‖h x‖)

/-- Scalar conjugation as a continuous semilinear map. -/
def spectralScalarConjugation : ℂ →SL[starRingEnd ℂ] ℂ where
  toFun := star
  map_add' := star_add
  map_smul' a z := by simp [smul_eq_mul]
  cont := continuous_star

/-- Reflection on the real spectral variable preserves Lebesgue measure. -/
def spectralReflection : SpectralHilbert →ₗᵢ[ℂ] SpectralHilbert :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => -x) (Measure.measurePreserving_neg volume)

/-- Conjugation followed by reflection, before bundling its inverse. -/
def spectralJMap : SpectralHilbert →SL[starRingEnd ℂ] SpectralHilbert :=
  (spectralScalarConjugation.compLpL 2 volume).comp spectralReflection.toContinuousLinearMap

theorem spectralJMap_ae (f : SpectralHilbert) :
    spectralJMap f =ᵐ[volume] fun x => star (f (-x)) := by
  have hc := spectralScalarConjugation.coeFn_compLpL (spectralReflection f)
  have hr := Lp.coeFn_compMeasurePreserving f (Measure.measurePreserving_neg volume)
  filter_upwards [hc, hr] with x hx hrx
  change (spectralScalarConjugation.compLpL 2 volume (spectralReflection f)) x =
    star (f (-x))
  rw [hx]
  change star ((spectralReflection f) x) = _
  change (spectralReflection f) x = f (-x) at hrx
  rw [hrx]

theorem spectralJMap_involutive : Function.Involutive spectralJMap := by
  intro f
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (spectralJMap_ae f)
  filter_upwards [spectralJMap_ae (spectralJMap f), hr] with x hx hy
  rw [hx, hy, neg_neg, star_star]

theorem spectralJMap_norm (f : SpectralHilbert) : ‖spectralJMap f‖ = ‖f‖ := by
  have hbound : ∀ g : SpectralHilbert, ‖spectralJMap g‖ ≤ ‖g‖ := by
    intro g
    calc
      ‖spectralJMap g‖ ≤ ‖spectralReflection g‖ := by
        apply Lp.norm_le_norm_of_ae_le
        filter_upwards [spectralScalarConjugation.coeFn_compLpL (spectralReflection g)]
          with x hx
        change ‖(spectralScalarConjugation.compLpL 2 volume (spectralReflection g)) x‖ ≤ _
        rw [hx]
        change ‖star ((spectralReflection g) x)‖ ≤ _
        simp
      _ = ‖g‖ := spectralReflection.norm_map g
  exact le_antisymm (hbound f) (by simpa only [spectralJMap_involutive f] using hbound (spectralJMap f))

/-- The concrete antiunitary Jf(ξ)=conj(f(-ξ)). -/
def spectralJ : SpectralHilbert ≃ₛₗᵢ[starRingEnd ℂ] SpectralHilbert where
  toLinearEquiv :=
    { spectralJMap.toLinearMap with
      invFun := spectralJMap
      left_inv := spectralJMap_involutive
      right_inv := spectralJMap_involutive }
  norm_map' := spectralJMap_norm

theorem spectralJ_ae (f : SpectralHilbert) :
    spectralJ f =ᵐ[volume] fun x => star (f (-x)) :=
  spectralJMap_ae f

theorem spectralJ_involutive : Function.Involutive spectralJ :=
  spectralJMap_involutive

theorem spectralJA_eq_BJ (c : ℝ) (f : SpectralHilbert) :
    spectralJ (spectralA c f) = spectralB c (spectralJ f) := by
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (spectralA_ae c f)
  filter_upwards [spectralJ_ae (spectralA c f), spectralB_ae c (spectralJ f),
    spectralJ_ae f, hr] with x hj hb hf ha
  rw [hj, hb, hf, ha, spectral_weight_reflection]
  simp

theorem spectralJB_eq_AJ (c : ℝ) (f : SpectralHilbert) :
    spectralJ (spectralB c f) = spectralA c (spectralJ f) := by
  have h := spectralJA_eq_BJ c (spectralJ f)
  apply spectralJ.injective
  simpa only [spectralJ_involutive f, spectralJ_involutive (spectralB c f)] using h.symm

#print axioms SpectralHilbert
#print axioms spectralWeightA
#print axioms spectralWeightB
#print axioms spectral_weight_den_pos
#print axioms spectral_weightA_pos
#print axioms spectral_weightB_pos
#print axioms spectral_weight_square_sum
#print axioms spectral_weightA_le_one
#print axioms spectral_weightB_le_one
#print axioms spectral_weightA_norm_le_one
#print axioms spectral_weightB_norm_le_one
#print axioms spectral_weightA_continuous
#print axioms spectral_weightB_continuous
#print axioms spectral_weight_reflection
#print axioms spectral_weightB_reflection
#print axioms spectral_weight_ratio
#print axioms boundedSpectralWeight
#print axioms bounded_spectral_weight_ae
#print axioms boundedSpectralMultiplier
#print axioms bounded_spectral_multiplier_ae
#print axioms bounded_spectral_multiplier_norm
#print axioms bounded_spectral_multiplier_selfadjoint
#print axioms spectralA
#print axioms spectralB
#print axioms spectralA_ae
#print axioms spectralB_ae
#print axioms spectralA_norm_le
#print axioms spectralB_norm_le
#print axioms spectralA_selfadjoint
#print axioms spectralB_selfadjoint
#print axioms spectralAB_commute
#print axioms spectralAB_square_sum
#print axioms spectralA_injective
#print axioms spectralAB_quadratic_nonneg
#print axioms spectralScalarConjugation
#print axioms spectralReflection
#print axioms spectralJMap
#print axioms spectralJMap_ae
#print axioms spectralJMap_involutive
#print axioms spectralJMap_norm
#print axioms spectralJ
#print axioms spectralJ_ae
#print axioms spectralJ_involutive
#print axioms spectralJA_eq_BJ
#print axioms spectralJB_eq_AJ

end ChatgptAudit.Continuous049
