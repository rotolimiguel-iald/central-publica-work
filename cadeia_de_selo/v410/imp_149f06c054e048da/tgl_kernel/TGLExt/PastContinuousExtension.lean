-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_020 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.EquilibriumCongruenceControls
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def pastClamp (a t : ℝ) : ℝ := max a (min t 0)

theorem past_clamp_continuous (a : ℝ) : Continuous (pastClamp a) := by
  unfold pastClamp
  fun_prop

theorem past_clamp_mem (a : ℝ) (ha : a≤0) (t : ℝ) : pastClamp a t∈Icc a 0 :=
  ⟨le_max_left _ _,max_le ha (min_le_right _ _)⟩

theorem past_clamp_fixes (a t : ℝ) (ht : t∈Icc a 0) : pastClamp a t=t := by
  simp only [pastClamp,min_eq_left ht.2,max_eq_right ht.1]

structure PastContinuousExtension (f : ℝ → ℝ) where
  value : ℝ → ℝ
  continuous : Continuous value
  at_zero : value 0=f 0
  matches_past : value =ᶠ[𝓝[<] 0] f

def pastContinuousExtension (f : ℝ → ℝ) (hf0 : ContinuousAt f 0)
    (hf : ∀ᶠ t in 𝓝[<] (0:ℝ), ContinuousAt f t) : PastContinuousExtension f :=
  Classical.choice (by
    obtain ⟨l,hl,hsub⟩ := mem_nhdsLT_iff_exists_Ioo_subset.mp hf
    change l<0 at hl
    let a := l/2
    have ha : a<0 := by dsimp only [a]; linarith
    have hla : l<a := by dsimp only [a]; linarith
    have hI : ContinuousOn f (Icc a 0) := by
      intro t ht
      by_cases hzero : t=0
      · subst t
        exact hf0.continuousWithinAt
      · have ht0 : t<0 := lt_of_le_of_ne ht.2 hzero
        exact (hsub ⟨lt_of_lt_of_le hla ht.1,ht0⟩).continuousWithinAt
    refine ⟨{
      value := f ∘ pastClamp a
      continuous := hI.comp_continuous (past_clamp_continuous a) (past_clamp_mem a ha.le)
      at_zero := ?_
      matches_past := ?_ }⟩
    · simp only [Function.comp_apply,past_clamp_fixes a 0 ⟨ha.le,le_rfl⟩]
    · filter_upwards [Ioo_mem_nhdsLT ha] with t ht
      exact congrArg f (past_clamp_fixes a t ⟨ht.1.le,ht.2.le⟩))

def pastIntegral {f : ℝ → ℝ} (E : PastContinuousExtension f) (t : ℝ) : ℝ :=
  ∫ s in (0:ℝ)..t, E.value s

theorem past_integral_derivative {f : ℝ → ℝ} (E : PastContinuousExtension f) (t : ℝ) :
    HasDerivAt (pastIntegral E) (E.value t) t :=
  (E.continuous.integral_hasStrictDerivAt 0 t).hasDerivAt

theorem past_integral_continuous {f : ℝ → ℝ} (E : PastContinuousExtension f) :
    Continuous (pastIntegral E) :=
  continuous_iff_continuousAt.2 (fun t => (past_integral_derivative E t).continuousAt)

theorem past_integral_zero {f : ℝ → ℝ} (E : PastContinuousExtension f) :
    pastIntegral E 0=0 := by
  simp [pastIntegral]

theorem past_integral_initial_derivative {f : ℝ → ℝ} (E : PastContinuousExtension f) :
    HasDerivAt (pastIntegral E) (f 0) 0 := by
  rw [←E.at_zero]
  exact past_integral_derivative E 0

theorem past_integral_matches_flux {f : ℝ → ℝ} (E : PastContinuousExtension f) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (pastIntegral E) (f t) t := by
  filter_upwards [E.matches_past] with t ht
  rw [←ht]
  exact past_integral_derivative E t

#print axioms past_clamp_continuous
#print axioms past_clamp_mem
#print axioms past_clamp_fixes
#print axioms pastContinuousExtension
#print axioms past_integral_derivative
#print axioms past_integral_continuous
#print axioms past_integral_zero
#print axioms past_integral_initial_derivative
#print axioms past_integral_matches_flux
end
end ChatgptAudit.Flow020
