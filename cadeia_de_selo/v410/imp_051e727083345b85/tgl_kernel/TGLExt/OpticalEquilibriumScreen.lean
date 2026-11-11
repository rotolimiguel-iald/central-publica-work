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
import TGLExt.OpticalNullCongruence

set_option autoImplicit false
set_option maxHeartbeats 12000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Optical043
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Optical036
  ChatgptAudit.Wave029 ChatgptAudit.Screen014 ChatgptAudit.Flow019
open scoped Topology ContDiff Matrix.Norms.Elementwise
noncomputable section

/-- Columns are the central null direction, its negatively paired null partner,
and the two actual Jacobi screen fields. -/
def opticalJacobiFrame (a c t : ℝ) : Tensor4 :=
  !![1/2,-1,0,0;
     0,0,jacobiOscillator a t,0;
     0,0,0,jacobiOscillator c t;
     1/2,1,0,0]

/-- An inverse on the domain where the two Jacobi factors do not vanish. -/
def opticalJacobiFrameInverse (a c t : ℝ) : Tensor4 :=
  !![1,0,0,1;
     -1/2,0,0,1/2;
     0,1/jacobiOscillator a t,0,0;
     0,0,1/jacobiOscillator c t,0]

theorem optical_frame_first_column (a c t : ℝ) :
    ∀ r, opticalJacobiFrame a c t r 0=centralNullDirection r := by
  intro r
  fin_cases r <;> rfl

theorem optical_frame_columns (a c t : ℝ) :
    screenColumns (opticalJacobiFrame a c t)=geometricJacobiColumns a c t := by
  ext r i
  fin_cases r <;> fin_cases i <;>
    norm_num [screenColumns,screenIndex,opticalJacobiFrame,geometricJacobiColumns,
      geometricJacobiField,transverseScreenVector,Matrix.cons_val_two,Matrix.cons_val_three]

theorem optical_frame_right_inverse (a c t : ℝ)
    (ha : jacobiOscillator a t≠0) (hc : jacobiOscillator c t≠0) :
    opticalJacobiFrame a c t*opticalJacobiFrameInverse a c t=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [opticalJacobiFrame,opticalJacobiFrameInverse,Matrix.mul_apply,
      Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three,ha,hc]

theorem optical_frame_gram (a c t : ℝ) :
    (opticalJacobiFrame a c t)ᵀ*
      frameMetricField (waveSolder a c) (centralNullCurve t)*opticalJacobiFrame a c t=
      nullScreenGram (screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
        (geometricJacobiColumns a c t)) := by
  rw [geometric_jacobi_gram,central_curve_metric]
  ext i j
  simp only [Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
  fin_cases i <;> fin_cases j <;>
    norm_num [opticalJacobiFrame,nullScreenGram,eta4,Matrix.diagonal_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.ext_iff]
  all_goals ring

theorem optical_frame_preserves_null_pairing (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (t : ℝ) (ht : centralNullCurve t∈opticalCongruenceDomain a c) :
    ((opticalJacobiFrame a c t)ᵀ*
      frameMetricField (waveSolder a c) (centralNullCurve t)*
      covariantVectorGradient
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
        (opticalNullVelocity a c) (centralNullCurve t)*
      opticalJacobiFrame a c t) 0 1=0 := by
  rw [central_curve_metric,optical_null_gradient_central_levi_civita a c ha hc t ht]
  norm_num [opticalJacobiFrame,eta4,Matrix.mul_apply,Matrix.transpose_apply,
    Fin.sum_univ_four,Matrix.diagonal_apply,Matrix.cons_val_two,Matrix.cons_val_three]

/-- This is a certificate for the specified columns, not an abstract choice of screen. -/
def opticalScreenCertificate (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (t : ℝ) (ht : centralNullCurve t∈opticalCongruenceDomain a c) :
    NullScreenAt (frameMetricField (waveSolder a c) (centralNullCurve t))
      (covariantVectorGradient
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
        (opticalNullVelocity a c) (centralNullCurve t))
      (opticalNullVelocity a c (centralNullCurve t)) (geometricJacobiColumns a c t) := by
  have hn := (optical_congruence_domain_central_iff a c t).mp ht
  exact {
    frame := opticalJacobiFrame a c t
    inverse := opticalJacobiFrameInverse a c t
    metric := screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
      (geometricJacobiColumns a c t)
    right_inverse := optical_frame_right_inverse a c t hn.1 hn.2
    gram := optical_frame_gram a c t
    first_column := by
      rw [optical_null_velocity_central]
      exact optical_frame_first_column a c t
    columns := (optical_frame_columns a c t).symm
    first_screen_negative := by
      rw [geometric_jacobi_gram]
      change -(jacobiOscillator a t)^2<0
      exact neg_neg_of_pos (sq_pos_of_ne_zero hn.1)
    determinant_positive := by
      rw [geometric_jacobi_gram_det]
      exact sq_pos_of_ne_zero (mul_ne_zero hn.1 hn.2)
    preserves_null_pairing := optical_frame_preserves_null_pairing a c ha hc t ht }

/-- The first-order screen transport is established for the actual Jacobi fields,
using the covariant gradient of the neighborhood congruence. -/
theorem optical_screen_transport (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (t : ℝ) (ht : centralNullCurve t∈opticalCongruenceDomain a c) :
    HasMatrixDerivAt (geometricJacobiColumns a c)
      ((covariantVectorGradient
          (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
          (opticalNullVelocity a c) (centralNullCurve t)-
        connectionAlong (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
          (centralNullCurve t) (opticalNullVelocity a c (centralNullCurve t)))*
        geometricJacobiColumns a c t) t := by
  have hn := (optical_congruence_domain_central_iff a c t).mp ht
  have hqa := jacobi_log_derivative_mul a t hn.1
  have hqc := jacobi_log_derivative_mul c t hn.2
  have hconn : connectionAlong
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (centralNullCurve t) (opticalNullVelocity a c (centralNullCurve t))=0 := by
    simp [connectionAlong,central_curve_connection_zero]
  rw [optical_null_gradient_central_levi_civita a c ha hc t ht,hconn,sub_zero]
  intro r i
  have hd := hasDerivAt_pi.mp (geometric_jacobi_field_derivative a c i t) r
  apply hd.congr_deriv
  fin_cases r <;> fin_cases i <;>
    norm_num [geometricJacobiVelocity,geometricJacobiColumns,geometricJacobiField,
      transverseScreenVector,Matrix.mul_apply,Fin.sum_univ_four,Matrix.diagonal_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,hqa,hqc]

/-- The curve and screen columns are the functions already constructed in stage036. -/
def opticalGeometricScreen (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    GeometricScreenAlong (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (opticalNullVelocity a c) centralNullCurve where
  vectors := geometricJacobiColumns a c
  continuous_zero := fun r i =>
    (hasDerivAt_pi.mp (geometric_jacobi_field_derivative a c i 0) r).continuousAt
  curve_tangent := Filter.Eventually.of_forall (fun t => by
    rw [optical_null_velocity_central]
    exact central_curve_derivative t)
  frames := by
    filter_upwards [(optical_congruence_domain_eventually a c).filter_mono
      (nhdsWithin_le_nhds (s := Iio (0:ℝ)))] with t ht
    exact ⟨opticalScreenCertificate a c ha hc t ht⟩
  transport := by
    filter_upwards [(optical_congruence_domain_eventually a c).filter_mono
      (nhdsWithin_le_nhds (s := Iio (0:ℝ)))] with t ht
    exact optical_screen_transport a c ha hc t ht

theorem optical_geometric_screen_initial_gram (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    screenGram (frameMetricField (waveSolder a c) 0)
      ((opticalGeometricScreen a c ha hc).vectors 0)= -1 := by
  change screenGram (frameMetricField (waveSolder a c) 0) (geometricJacobiColumns a c 0)= -1
  have h := geometric_jacobi_gram a c 0
  have he : screenGram (frameMetricField (waveSolder a c) 0)
      (geometricJacobiColumns a c 0)=!![-1,0;0,-1] := by
    simpa [centralNullCurve,jacobiOscillator] using h
  rw [he]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

/-- The area rate follows from the existing geometric transport theorem.
No heat, entropy, matter coupling, or Clausius condition is used. -/
theorem optical_geometric_area_rate (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    ∀ᶠ t in 𝓝[<] (0:ℝ),
      HasDerivAt
        (inducedArea (frameMetricField (waveSolder a c)) centralNullCurve
          (geometricJacobiColumns a c))
        (vectorExpansion
          (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
          (opticalNullVelocity a c) (centralNullCurve t)*
          inducedArea (frameMetricField (waveSolder a c)) centralNullCurve
            (geometricJacobiColumns a c) t) t := by
  have hg : SmoothMatrixOn (opticalCongruenceDomain a c)
      (frameMetricField (waveSolder a c)) := by
    intro i j
    exact (frame_metric_smooth univ (waveSolder a c) (wave_solder_smooth a c) i j).mono
      (subset_univ (opticalCongruenceDomain a c))
  have hm : MetricCompatibleOn (opticalCongruenceDomain a c)
      (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) :=
    levi_civita_field_metric_compatible (opticalCongruenceDomain a c)
      (optical_congruence_domain_open a c)
      (frameMetricField (waveSolder a c)) (inverseFrameMetricField (waveInverseSolder a c))
      (fun x _ => frame_metric_symmetric (waveSolder a c) x)
      (fun x _ => inverse_frame_metric_left (waveSolder a c) (waveInverseSolder a c) x
        (wave_solder_inverse a c x) (wave_inverse_solder a c x))
      (fun x _ => inverse_frame_metric_right (waveSolder a c) (waveInverseSolder a c) x
        (wave_solder_inverse a c x) (wave_inverse_solder a c x))
  exact geometric_screen_area_rate (opticalCongruenceDomain a c)
    (optical_congruence_domain_open a c)
    (frameMetricField (waveSolder a c))
    (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
    (opticalNullVelocity a c) hg hm
    (optical_null_velocity_geodesic_levi_civita a c ha hc)
    centralNullCurve (opticalGeometricScreen a c ha hc)
    ((optical_congruence_domain_eventually a c).filter_mono
      (nhdsWithin_le_nhds (s := Iio (0:ℝ))))

/-- An actual equilibrium screen for the specified plane-wave geometry.
The constructor has no state, matter, entropy, heat, or matching parameter. -/
def opticalEquilibriumScreen (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    EquilibriumScreenData univ (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      0 centralNullDirection where
  neighborhood := opticalCongruenceDomain a c
  neighborhood_open := optical_congruence_domain_open a c
  neighborhood_subset := subset_univ _
  point_mem := optical_congruence_domain_origin a c
  velocity := opticalNullVelocity a c
  velocity_smooth := optical_null_velocity_smooth a c
  velocity_at_point := by
    simpa only [centralNullCurve,zero_smul] using optical_null_velocity_central a c 0
  velocity_nonzero := fun x _ => optical_null_velocity_nonzero a c x
  velocity_null := fun x _ => optical_null_velocity_null a c x
  geodesic := optical_null_velocity_geodesic_levi_civita a c ha hc
  equilibrium_gradient := optical_null_gradient_origin_levi_civita a c ha hc
  curve := centralNullCurve
  curve_zero := by simp [centralNullCurve]
  curve_tangent := central_curve_derivative 0
  screen := opticalGeometricScreen a c ha hc
  screen_gram_zero := optical_geometric_screen_initial_gram a c ha hc
  area_rate := optical_geometric_area_rate a c ha hc

theorem optical_equilibrium_curve (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    (opticalEquilibriumScreen a c ha hc).curve=centralNullCurve := rfl

theorem optical_equilibrium_columns (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    (opticalEquilibriumScreen a c ha hc).screen.vectors=geometricJacobiColumns a c := rfl

theorem optical_equilibrium_velocity_central (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (t : ℝ) :
    (opticalEquilibriumScreen a c ha hc).velocity
      ((opticalEquilibriumScreen a c ha hc).curve t)=centralNullDirection :=
  optical_null_velocity_central a c t

theorem optical_equilibrium_area (a c : ℝ) (ha : 0≤a) (hc : 0≤c) (t : ℝ) :
    inducedArea (frameMetricField (waveSolder a c))
      (opticalEquilibriumScreen a c ha hc).curve
      (opticalEquilibriumScreen a c ha hc).screen.vectors t=geometricJacobiArea a c t := rfl

#print axioms opticalJacobiFrame
#print axioms opticalJacobiFrameInverse
#print axioms optical_frame_first_column
#print axioms optical_frame_columns
#print axioms optical_frame_right_inverse
#print axioms optical_frame_gram
#print axioms optical_frame_preserves_null_pairing
#print axioms opticalScreenCertificate
#print axioms optical_screen_transport
#print axioms opticalGeometricScreen
#print axioms optical_geometric_screen_initial_gram
#print axioms optical_geometric_area_rate
#print axioms opticalEquilibriumScreen
#print axioms optical_equilibrium_curve
#print axioms optical_equilibrium_columns
#print axioms optical_equilibrium_velocity_central
#print axioms optical_equilibrium_area
end
end ChatgptAudit.Optical043
