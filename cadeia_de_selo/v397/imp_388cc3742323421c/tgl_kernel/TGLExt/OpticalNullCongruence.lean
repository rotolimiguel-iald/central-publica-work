-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_043 (06/09/2026), transposta em 06/09/2026
-- Lote 042..043 (complementos a ORDEM_009; ORDEM_008 cumprida: zero instancias anonimas, lote compilado
--   junto em diretorio limpo). 042: COMPLETAMENTO CONSERVADO DA RESPOSTA NULA — criterio completo, na
--   familia e fundo plano fixados, para a resposta nula admitir fonte conservada: toda fonte suave simetrica
--   com T(d,d) = c[w(d)]^2 nos nulos e S + f g com S = c(w x w - g^{-1}(w,w) g/2); conservacao <=> df = -c(div w) w;
--   criterio = existencia de potencial suave; controle phi = t^2/2 admite; CONTRAEXEMPLO phi = t^2 x exclui toda
--   fonte conservada (inclusive traco variavel) num aberto. 043: TELA EFETIVA DE JACOBI e calor construido —
--   habitante explicito de EquilibriumScreenData so com (a,c) da metrica (perfis de Riccati; campo nulo,
--   geodesico, gradiente diag(0,q_a,q_c,0)); opticalScreenHeat = constructedHeat, igual a opticalHeat041 como
--   germe em t -> 0-; sem casamento: lim D/t^2 = kappa[eta(a+c) - 2 pi m]/(4 pi); com casamento: lim D/t^4 =
--   kappa eta (a^2+c^2)/(24 pi) > 0 — a igualdade finita exata FALHA, o balanco infinitesimal fica.
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia especificada; L, area fisica, retorno estabilizador,
--   materia/geometria/normalizacao e reconstrucao geral OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 10/10; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.JacobiRiccatiProfile

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Optical043
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Wave029 ChatgptAudit.Optical036
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

/-- The Jacobi rate pulled back to the existing affine null coordinate. -/
def opticalRate (a : ℝ) (x : Coordinate4) : ℝ :=
  jacobiLogDerivative a (opticalPhaseCoordinate x)

/-- The longitudinal correction required by the full plane-wave null equation. -/
def opticalLongitudinalCorrection (a c : ℝ) (x : Coordinate4) : ℝ :=
  ((opticalRate a x ^ 2 - a) * (x 1)^2 +
    (opticalRate c x ^ 2 - c) * (x 2)^2) / 2

/-- A congruence field in the original coordinates, not just a tangent on one ray. -/
def opticalNullVelocity (a c : ℝ) (x : Coordinate4) : Coordinate4 :=
  ![1/2 + opticalLongitudinalCorrection a c x,
    opticalRate a x * x 1, opticalRate c x * x 2,
    1/2 - opticalLongitudinalCorrection a c x]

def opticalCubicProfile (a c : ℝ) (x : Coordinate4) : ℝ :=
  opticalRate a x ^ 3 * (x 1)^2 + opticalRate c x ^ 3 * (x 2)^2

/-- The complete covariant derivative, including its longitudinal entries. -/
def opticalNullGradientMatrix (a c : ℝ) (x : Coordinate4) : Tensor4 :=
  !![-opticalCubicProfile a c x, opticalRate a x ^ 2 * x 1,
      opticalRate c x ^ 2 * x 2, -opticalCubicProfile a c x;
    -(opticalRate a x ^ 2 * x 1), opticalRate a x, 0, -(opticalRate a x ^ 2 * x 1);
    -(opticalRate c x ^ 2 * x 2), 0, opticalRate c x, -(opticalRate c x ^ 2 * x 2);
    opticalCubicProfile a c x, -(opticalRate a x ^ 2 * x 1),
      -(opticalRate c x ^ 2 * x 2), opticalCubicProfile a c x]

theorem optical_rate_central (a t : ℝ) :
    opticalRate a (centralNullCurve t) = jacobiLogDerivative a t := by
  unfold opticalRate
  rw [optical_phase_coordinate_central]

theorem optical_rate_hasFDerivAt (a : ℝ) (ha : 0 ≤ a) (x : Coordinate4)
    (hx : jacobiOscillator a (opticalPhaseCoordinate x) ≠ 0) :
    HasFDerivAt (opticalRate a)
      ((-a - opticalRate a x ^ 2) •
        ((ContinuousLinearMap.proj (0 : Fin 4) : Coordinate4 →L[ℝ] ℝ) +
          (ContinuousLinearMap.proj (3 : Fin 4) : Coordinate4 →L[ℝ] ℝ))) x := by
  exact (jacobi_log_derivative_hasDerivAt a ha (opticalPhaseCoordinate x) hx).comp_hasFDerivAt
    x (optical_phase_coordinate_hasFDerivAt x)

theorem optical_rate_partial (a : ℝ) (ha : 0 ≤ a) (x : Coordinate4)
    (hx : jacobiOscillator a (opticalPhaseCoordinate x) ≠ 0) (i : Fin 4) :
    coordinatePartial (opticalRate a) x i =
      (-a - opticalRate a x ^ 2) *
        ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) := by
  unfold coordinatePartial
  rw [(optical_rate_hasFDerivAt a ha x hx).fderiv]
  simp [mul_add]

theorem optical_longitudinal_smooth (a c : ℝ) :
    ContDiffOn ℝ ∞ (opticalLongitudinalCorrection a c) (opticalCongruenceDomain a c) := by
  have hA : ContDiffOn ℝ ∞ (opticalRate a) (opticalCongruenceDomain a c) :=
    jacobi_log_profile_smooth a _ (fun _ hx => hx.1)
  have hC : ContDiffOn ℝ ∞ (opticalRate c) (opticalCongruenceDomain a c) :=
    jacobi_log_profile_smooth c _ (fun _ hx => hx.2)
  unfold opticalLongitudinalCorrection
  fun_prop

theorem optical_null_velocity_smooth (a c : ℝ) :
    SmoothVectorOn (opticalCongruenceDomain a c) (opticalNullVelocity a c) := by
  have hA : ContDiffOn ℝ ∞ (opticalRate a) (opticalCongruenceDomain a c) :=
    jacobi_log_profile_smooth a _ (fun _ hx => hx.1)
  have hC : ContDiffOn ℝ ∞ (opticalRate c) (opticalCongruenceDomain a c) :=
    jacobi_log_profile_smooth c _ (fun _ hx => hx.2)
  have hB := optical_longitudinal_smooth a c
  intro i
  fin_cases i <;> dsimp [opticalNullVelocity] <;> fun_prop

theorem optical_null_velocity_frequency (a c : ℝ) (x : Coordinate4) :
    opticalNullVelocity a c x 0 + opticalNullVelocity a c x 3 = 1 := by
  change (1/2 + opticalLongitudinalCorrection a c x) +
    (1/2 - opticalLongitudinalCorrection a c x) = 1
  ring

theorem optical_null_velocity_nonzero (a c : ℝ) (x : Coordinate4) :
    opticalNullVelocity a c x ≠ 0 := by
  intro hz
  have h := optical_null_velocity_frequency a c x
  rw [hz] at h
  norm_num at h

/-- Nullity is algebraic. Differential conclusions below are restricted to the domain. -/
theorem optical_null_velocity_null (a c : ℝ) (x : Coordinate4) :
    tensorQuad (frameMetricField (waveSolder a c) x) (opticalNullVelocity a c x) = 0 := by
  have hw : Coherent023.covectorRead waveCovector (opticalNullVelocity a c x) = 1 := by
    simpa [Coherent023.covectorRead, waveCovector, dotProduct, Fin.sum_univ_four] using
      optical_null_velocity_frequency a c x
  rw [wave_metric_formula]
  have he : eta4 + waveProfile a c x • Matrix.vecMulVec waveCovector waveCovector =
      eta4 - (-waveProfile a c x) • Matrix.vecMulVec waveCovector waveCovector := by
    simp
  rw [he, tensorQuad_sub_smul, Coherent023.outer_tensor_quad, hw]
  change tensorQuad eta4
    ![1/2 + opticalLongitudinalCorrection a c x,
      opticalRate a x * x 1, opticalRate c x * x 2,
      1/2 - opticalLongitudinalCorrection a c x] - (-waveProfile a c x) * 1^2 = 0
  rw [tensorQuad_eta]
  dsimp [opticalLongitudinalCorrection, waveProfile]
  ring

theorem optical_null_velocity_central (a c t : ℝ) :
    opticalNullVelocity a c (centralNullCurve t) = centralNullDirection := by
  ext i
  fin_cases i <;>
    simp [opticalNullVelocity, opticalLongitudinalCorrection,
      centralNullCurve, centralNullDirection, Matrix.cons_val_two, Matrix.cons_val_three]

theorem optical_null_velocity_origin (a c : ℝ) :
    opticalNullVelocity a c 0 = centralNullDirection := by
  simpa only [centralNullCurve, zero_smul] using optical_null_velocity_central a c 0

theorem optical_longitudinal_partial (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (x : Coordinate4) (hx : x ∈ opticalCongruenceDomain a c) (i : Fin 4) :
    coordinatePartial (opticalLongitudinalCorrection a c) x i =
      (opticalRate a x * (-a - opticalRate a x ^ 2) * (x 1)^2 +
        opticalRate c x * (-c - opticalRate c x ^ 2) * (x 2)^2) *
          ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) +
      (opticalRate a x ^ 2 - a) * x 1 * (Pi.single i (1 : ℝ) : Coordinate4) 1 +
      (opticalRate c x ^ 2 - c) * x 2 * (Pi.single i (1 : ℝ) : Coordinate4) 2 := by
  have hA := ((optical_rate_hasFDerivAt a ha x hx.1).pow 2).sub_const a
  have hC := ((optical_rate_hasFDerivAt c hc x hx.2).pow 2).sub_const c
  have hB := ((hA.mul ((hasFDerivAt_apply (𝕜 := ℝ) 1 x).pow 2)).add
    (hC.mul ((hasFDerivAt_apply (𝕜 := ℝ) 2 x).pow 2))).mul_const ((2 : ℝ)⁻¹)
  change HasFDerivAt (fun y : Coordinate4 =>
    ((opticalRate a y ^ 2 - a) * (y 1)^2 +
      (opticalRate c y ^ 2 - c) * (y 2)^2) * (2 : ℝ)⁻¹) _ x at hB
  have he : (fun y : Coordinate4 =>
      ((opticalRate a y ^ 2 - a) * (y 1)^2 +
        (opticalRate c y ^ 2 - c) * (y 2)^2) * (2 : ℝ)⁻¹) =
      opticalLongitudinalCorrection a c := by
    funext y
    simp only [opticalLongitudinalCorrection, div_eq_mul_inv]
  rw [he] at hB
  unfold coordinatePartial
  rw [hB.fderiv]
  fin_cases i <;>
    norm_num [ContinuousLinearMap.proj_apply, Pi.single_apply, Fin.ext_iff] <;> ring

theorem optical_null_velocity_partial (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (x : Coordinate4) (hx : x ∈ opticalCongruenceDomain a c) (i r : Fin 4) :
    coordinatePartial (fun y => opticalNullVelocity a c y r) x i =
      ![coordinatePartial (opticalLongitudinalCorrection a c) x i,
        (-a - opticalRate a x ^ 2) *
          ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) *
            x 1 + opticalRate a x * (Pi.single i (1 : ℝ) : Coordinate4) 1,
        (-c - opticalRate c x ^ 2) *
          ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) *
            x 2 + opticalRate c x * (Pi.single i (1 : ℝ) : Coordinate4) 2,
        -coordinatePartial (opticalLongitudinalCorrection a c) x i] r := by
  have hB : DifferentiableAt ℝ (opticalLongitudinalCorrection a c) x :=
    ((optical_longitudinal_smooth a c).differentiableOn (by simp)).differentiableAt
      ((optical_congruence_domain_open a c).mem_nhds hx)
  fin_cases r
  · change coordinatePartial (fun y => (1/2 : ℝ) + opticalLongitudinalCorrection a c y) x i =
      coordinatePartial (opticalLongitudinalCorrection a c) x i
    rw [coordinatePartial_add _ _ x (differentiableAt_const _) hB i]
    simp [coordinatePartial]
  · have h := (optical_rate_hasFDerivAt a ha x hx.1).mul
      (hasFDerivAt_apply (𝕜 := ℝ) 1 x)
    change HasFDerivAt (fun y : Coordinate4 => opticalRate a y * y 1) _ x at h
    change fderiv ℝ (fun y : Coordinate4 => opticalRate a y * y 1) x (Pi.single i 1) =
      (-a - opticalRate a x ^ 2) *
        ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) *
          x 1 + opticalRate a x * (Pi.single i (1 : ℝ) : Coordinate4) 1
    rw [h.fderiv]
    fin_cases i <;>
      norm_num [ContinuousLinearMap.proj_apply, Pi.single_apply, Fin.ext_iff] <;> ring
  · have h := (optical_rate_hasFDerivAt c hc x hx.2).mul
      (hasFDerivAt_apply (𝕜 := ℝ) 2 x)
    change HasFDerivAt (fun y : Coordinate4 => opticalRate c y * y 2) _ x at h
    change fderiv ℝ (fun y : Coordinate4 => opticalRate c y * y 2) x (Pi.single i 1) =
      (-c - opticalRate c x ^ 2) *
        ((Pi.single i (1 : ℝ) : Coordinate4) 0 + (Pi.single i (1 : ℝ) : Coordinate4) 3) *
          x 2 + opticalRate c x * (Pi.single i (1 : ℝ) : Coordinate4) 2
    rw [h.fderiv]
    fin_cases i <;>
      norm_num [ContinuousLinearMap.proj_apply, Pi.single_apply, Fin.ext_iff] <;> ring
  · change coordinatePartial (fun y => (1/2 : ℝ) - opticalLongitudinalCorrection a c y) x i =
      -coordinatePartial (opticalLongitudinalCorrection a c) x i
    rw [coordinatePartial_sub _ _ x (differentiableAt_const _) hB i]
    simp [coordinatePartial]

/-- All sixteen entries are derived from the Riccati equations and the actual connection. -/
theorem optical_null_gradient_formula (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (x : Coordinate4) (hx : x ∈ opticalCongruenceDomain a c) :
    covariantVectorGradient (waveConnection a c) (opticalNullVelocity a c) x =
      opticalNullGradientMatrix a c x := by
  ext r i
  change coordinatePartial (fun y => opticalNullVelocity a c y r) x i +
    ((waveConnection a c x i).mulVec (opticalNullVelocity a c x)) r = _
  rw [optical_null_velocity_partial a c ha hc x hx i r,
    optical_longitudinal_partial a c ha hc x hx i]
  fin_cases r <;> fin_cases i <;>
    norm_num [opticalNullGradientMatrix, opticalCubicProfile, opticalNullVelocity,
      opticalLongitudinalCorrection, waveConnection, waveTransverse, waveRaised,
      waveCovector, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
      Pi.single_apply, Matrix.cons_val_two, Matrix.cons_val_three, Fin.ext_iff] <;> ring

theorem optical_null_velocity_geodesic (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    EqOn (vectorAcceleration (waveConnection a c) (opticalNullVelocity a c))
      (fun _ => 0) (opticalCongruenceDomain a c) := by
  intro x hx
  unfold vectorAcceleration
  rw [optical_null_gradient_formula a c ha hc x hx]
  ext i
  fin_cases i <;>
    norm_num [opticalNullGradientMatrix, opticalCubicProfile, opticalNullVelocity,
      opticalLongitudinalCorrection, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
      Matrix.cons_val_two, Matrix.cons_val_three, Fin.ext_iff] <;> ring

theorem optical_null_gradient_central (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (t : ℝ) (ht : centralNullCurve t ∈ opticalCongruenceDomain a c) :
    covariantVectorGradient (waveConnection a c) (opticalNullVelocity a c)
      (centralNullCurve t) =
        Matrix.diagonal ![0, jacobiLogDerivative a t, jacobiLogDerivative c t, 0] := by
  rw [optical_null_gradient_formula a c ha hc (centralNullCurve t) ht]
  simp only [opticalNullGradientMatrix, opticalCubicProfile, optical_rate_central]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [centralNullCurve, centralNullDirection, Matrix.diagonal_apply,
      Matrix.cons_val_two, Matrix.cons_val_three, Fin.ext_iff]

theorem optical_null_gradient_origin (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    covariantVectorGradient (waveConnection a c) (opticalNullVelocity a c) 0 = 0 := by
  have ht : centralNullCurve 0 ∈ opticalCongruenceDomain a c := by
    simpa only [centralNullCurve, zero_smul] using optical_congruence_domain_origin a c
  have h := optical_null_gradient_central a c ha hc 0 ht
  rw [centralNullCurve, zero_smul] at h
  rw [h]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [jacobi_log_derivative_zero, Fin.ext_iff]

theorem optical_null_velocity_expansion (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (x : Coordinate4) (hx : x ∈ opticalCongruenceDomain a c) :
    vectorExpansion (waveConnection a c) (opticalNullVelocity a c) x =
      opticalRate a x + opticalRate c x := by
  unfold vectorExpansion
  rw [optical_null_gradient_formula a c ha hc x hx]
  norm_num [opticalNullGradientMatrix, Matrix.trace, Matrix.diag, Fin.sum_univ_four,
    Matrix.cons_val_two, Matrix.cons_val_three, Fin.ext_iff]
  ring

theorem optical_null_gradient_formula_levi_civita (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (x : Coordinate4) (hx : x ∈ opticalCongruenceDomain a c) :
    covariantVectorGradient
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (opticalNullVelocity a c) x = opticalNullGradientMatrix a c x := by
  rw [wave_levi_civita]
  exact optical_null_gradient_formula a c ha hc x hx

theorem optical_null_gradient_central_levi_civita (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c)
    (t : ℝ) (ht : centralNullCurve t ∈ opticalCongruenceDomain a c) :
    covariantVectorGradient
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (opticalNullVelocity a c) (centralNullCurve t) =
        Matrix.diagonal ![0, jacobiLogDerivative a t, jacobiLogDerivative c t, 0] := by
  rw [wave_levi_civita]
  exact optical_null_gradient_central a c ha hc t ht

theorem optical_null_gradient_origin_levi_civita (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    covariantVectorGradient
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (opticalNullVelocity a c) 0 = 0 := by
  rw [wave_levi_civita]
  exact optical_null_gradient_origin a c ha hc

theorem optical_null_velocity_geodesic_levi_civita (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    EqOn (vectorAcceleration
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) (opticalNullVelocity a c))
      (fun _ => 0) (opticalCongruenceDomain a c) := by
  rw [wave_levi_civita]
  exact optical_null_velocity_geodesic a c ha hc

#print axioms opticalRate
#print axioms opticalLongitudinalCorrection
#print axioms opticalNullVelocity
#print axioms opticalCubicProfile
#print axioms opticalNullGradientMatrix
#print axioms optical_rate_central
#print axioms optical_rate_hasFDerivAt
#print axioms optical_rate_partial
#print axioms optical_longitudinal_smooth
#print axioms optical_null_velocity_smooth
#print axioms optical_null_velocity_frequency
#print axioms optical_null_velocity_nonzero
#print axioms optical_null_velocity_null
#print axioms optical_null_velocity_central
#print axioms optical_null_velocity_origin
#print axioms optical_longitudinal_partial
#print axioms optical_null_velocity_partial
#print axioms optical_null_gradient_formula
#print axioms optical_null_velocity_geodesic
#print axioms optical_null_gradient_central
#print axioms optical_null_gradient_origin
#print axioms optical_null_velocity_expansion
#print axioms optical_null_gradient_formula_levi_civita
#print axioms optical_null_gradient_central_levi_civita
#print axioms optical_null_gradient_origin_levi_civita
#print axioms optical_null_velocity_geodesic_levi_civita

end
end ChatgptAudit.Optical043
