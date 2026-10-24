-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_007 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ExpectationProjection
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt MeasureTheory
noncomputable section
variable {P : SiteProfile}

theorem modularFlow_continuous_apply (f : ℝ → TowerHilbert P) (hf : Continuous f) :
    Continuous (fun t => modularFlow P t (f t)) := by
  apply continuous_iff_continuousAt.mpr
  intro s
  rw [Metric.continuousAt_iff]
  intro ε hε
  obtain ⟨d,hd,hf'⟩ := Metric.continuousAt_iff.mp hf.continuousAt (ε/2) (half_pos hε)
  obtain ⟨e,he,hg⟩ := Metric.continuousAt_iff.mp
    (modularFlow_strongly_continuous (f s)).continuousAt (ε/2) (half_pos hε)
  refine ⟨min d e,lt_min hd he,fun t ht => ?_⟩
  have h1 := hf' (lt_of_lt_of_le ht (min_le_left _ _))
  have h2 := hg (lt_of_lt_of_le ht (min_le_right _ _))
  have h3 := dist_triangle (modularFlow P t (f t)) (modularFlow P t (f s))
    (modularFlow P s (f s))
  have heq : dist (modularFlow P t (f t)) (modularFlow P t (f s)) = dist (f t) (f s) :=
    (modularFlowIsometry P t).isometry.dist_eq _ _
  rw [heq] at h3
  linarith

theorem modular_orbit_continuous (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (v : TowerHilbert P) : Continuous (fun t : ℝ => modularConjugation P t x v) := by
  change Continuous (fun t => modularFlow P t (x (modularFlow P (-t) v)))
  exact modularFlow_continuous_apply _
    (x.continuous.comp ((modularFlow_strongly_continuous v).comp continuous_neg))

theorem modular_orbit_bound (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (v : TowerHilbert P) (t : ℝ) : ‖modularConjugation P t x v‖ ≤ ‖x‖*‖v‖ := by
  change ‖modularFlow P t (x (modularFlow P (-t) v))‖ ≤ _
  rw [modularFlow_norm]
  simpa only [modularFlow_norm] using x.le_opNorm (modularFlow P (-t) v)

def periodAverageVector (P : SiteProfile) (T : ℝ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P) : TowerHilbert P :=
  T⁻¹ • ∫ t in (0:ℝ)..T, modularConjugation P t x v

theorem average_vector_add (T : ℝ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (v w : TowerHilbert P) :
    periodAverageVector P T x (v+w) = periodAverageVector P T x v + periodAverageVector P T x w := by
  simp only [periodAverageVector,map_add]
  rw [intervalIntegral.integral_add
    ((modular_orbit_continuous x v).intervalIntegrable 0 T)
    ((modular_orbit_continuous x w).intervalIntegrable 0 T),smul_add]

theorem average_vector_smul (T : ℝ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (c : ℂ) (v : TowerHilbert P) :
    periodAverageVector P T x (c•v) = c•periodAverageVector P T x v := by
  simp only [periodAverageVector,map_smul,intervalIntegral.integral_smul]
  exact smul_comm _ _ _

theorem average_vector_bound (T : ℝ) (hT : 0<T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P) :
    ‖periodAverageVector P T x v‖ ≤ ‖x‖*‖v‖ := by
  have hb := intervalIntegral.norm_integral_le_of_norm_le_const
    (a := (0:ℝ)) (b := T) (fun t _ => modular_orbit_bound x v t)
  simp only [sub_zero,abs_of_pos hT] at hb
  calc
    ‖periodAverageVector P T x v‖ = T⁻¹ * ‖∫ t in (0:ℝ)..T, modularConjugation P t x v‖ := by
      rw [periodAverageVector,norm_smul,Real.norm_eq_abs,abs_of_pos (inv_pos.mpr hT)]
    _ ≤ T⁻¹ * (‖x‖*‖v‖*T) := mul_le_mul_of_nonneg_left hb (le_of_lt (inv_pos.mpr hT))
    _ = ‖x‖*‖v‖ := by field_simp

def periodAverage (P : SiteProfile) (T : ℝ) (hT : 0<T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  ({ toFun := periodAverageVector P T x
     map_add' := average_vector_add T x
     map_smul' := fun c v => average_vector_smul T x c v } :
    TowerHilbert P →ₗ[ℂ] TowerHilbert P).mkContinuous ‖x‖ (average_vector_bound T hT x)

theorem period_average_operator (T : ℝ) (hT : 0<T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    (∀ v, periodAverage P T hT x v = T⁻¹ • ∫ t in (0:ℝ)..T, modularConjugation P t x v) ∧
      ‖periodAverage P T hT x‖ ≤ ‖x‖ := by
  refine ⟨fun _ => rfl,?_⟩
  exact ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) (average_vector_bound T hT x)

theorem period_average_commutes (T : ℝ) (hT : 0<T)
    (x y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hc : ∀ t, y * modularConjugation P t x = modularConjugation P t x * y) :
    y * periodAverage P T hT x = periodAverage P T hT x * y := by
  ext v
  change y (T⁻¹ • ∫ t in (0:ℝ)..T, modularConjugation P t x v) =
    T⁻¹ • ∫ t in (0:ℝ)..T, modularConjugation P t x (y v)
  rw [y.map_smul_of_tower,← y.intervalIntegral_comp_comm
    ((modular_orbit_continuous x v).intervalIntegrable 0 T)]
  congr 1
  apply intervalIntegral.integral_congr
  intro t ht
  exact congrArg (fun a : TowerHilbert P →L[ℂ] TowerHilbert P => a v) (hc t)

theorem period_average_mem_factor (T : ℝ) (hT : 0<T)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) :
    periodAverage P T hT x ∈ theFactorObject P := by
  change periodAverage P T hT x ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro y hy
  have hsig (t : ℝ) := (modularConjugation_preserves_factor P t x).mp hx
  have hc (t : ℝ) : y * modularConjugation P t x = modularConjugation P t x * y ∧
      star y * modularConjugation P t x = modularConjugation P t x * star y := by
    have hh := hsig t
    change modularConjugation P t x ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hh
    rw [StarSubalgebra.mem_centralizer_iff] at hh
    exact hh y hy
  exact ⟨period_average_commutes T hT x y (fun t => (hc t).1),
    period_average_commutes T hT x (star y) (fun t => (hc t).2)⟩

#print axioms modularFlow_continuous_apply
#print axioms modular_orbit_continuous
#print axioms modular_orbit_bound
#print axioms periodAverageVector
#print axioms average_vector_add
#print axioms average_vector_smul
#print axioms average_vector_bound
#print axioms periodAverage
#print axioms period_average_operator
#print axioms period_average_commutes
#print axioms period_average_mem_factor
end
end ChatgptAudit
