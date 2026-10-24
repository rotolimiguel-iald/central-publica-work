-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_013 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.GeometricAreaHorizon
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection

set_option autoImplicit false
set_option maxHeartbeats 3000000
namespace ChatgptAudit
open Matrix TGLExt
open scoped RealInnerProductSpace
noncomputable section

abbrev SpatialVector := EuclideanSpace ℝ (Fin 3)

def spatialAxis (i : Fin 3) : SpatialVector := EuclideanSpace.single i (1:ℝ)

structure SpatialScreenBasis (u : SpatialVector) where
  first : SpatialVector
  second : SpatialVector
  unit_first : inner ℝ first first=1
  unit_second : inner ℝ second second=1
  cross_zero : inner ℝ first second=0
  axis_first_zero : inner ℝ u first=0
  axis_second_zero : inner ℝ u second=0

def reflectedSpatialScreen (u : SpatialVector) (hu : ‖u‖=1) : SpatialScreenBasis u := by
  let R : SpatialVector ≃ₗᵢ[ℝ] SpatialVector :=
    Submodule.reflection (ℝ ∙ (spatialAxis 0-u))ᗮ
  have hR : R (spatialAxis 0)=u := by
    apply Submodule.reflection_sub
    simp [spatialAxis,hu]
  refine {
    first := R (spatialAxis 1)
    second := R (spatialAxis 2)
    unit_first := ?_
    unit_second := ?_
    cross_zero := ?_
    axis_first_zero := ?_
    axis_second_zero := ?_ }
  · rw [R.inner_map_map]
    simp [spatialAxis]
  · rw [R.inner_map_map]
    simp [spatialAxis]
  · rw [R.inner_map_map]
    simp [spatialAxis,EuclideanSpace.inner_single_left]
  · rw [← hR,R.inner_map_map]
    simp [spatialAxis,EuclideanSpace.inner_single_left]
  · rw [← hR,R.inner_map_map]
    simp [spatialAxis,EuclideanSpace.inner_single_left]

theorem spatial_inner_components (u v : SpatialVector) :
    inner ℝ u v=u 0*v 0+u 1*v 1+u 2*v 2 := by
  simp only [PiLp.inner_apply,Fin.sum_univ_three,RCLike.inner_apply,conj_trivial]
  ring

theorem minkowski_quad_coordinates (v : Coordinate4) :
    tensorQuad eta4 v=(v 0)^2-(v 1)^2-(v 2)^2-(v 3)^2 := by
  have he : ![v 0,v 1,v 2,v 3]=v := by
    funext i
    fin_cases i <;> rfl
  rw [← he]
  exact tensorQuad_eta _ _ _ _

theorem nonzero_null_time (v : Coordinate4) (hv : v≠0) (hn : tensorQuad eta4 v=0) :
    v 0≠0 := by
  intro ht
  rw [minkowski_quad_coordinates,ht] at hn
  have h1 : v 1=0 := by nlinarith [sq_nonneg (v 2),sq_nonneg (v 3)]
  have h2 : v 2=0 := by nlinarith [sq_nonneg (v 1),sq_nonneg (v 3)]
  have h3 : v 3=0 := by nlinarith [sq_nonneg (v 1),sq_nonneg (v 2)]
  apply hv
  funext i
  fin_cases i
  · exact ht
  · exact h1
  · exact h2
  · exact h3

def unitNullSpatial (v : Coordinate4) : SpatialVector :=
  WithLp.toLp 2 (fun i : Fin 3 => v i.succ/v 0)

theorem unit_null_spatial_norm (v : Coordinate4) (hv : v≠0)
    (hn : tensorQuad eta4 v=0) : ‖unitNullSpatial v‖=1 := by
  have ht := nonzero_null_time v hv hn
  have hq := minkowski_quad_coordinates v
  have hs : ‖unitNullSpatial v‖^2=1 := by
    rw [EuclideanSpace.real_norm_sq_eq]
    simp only [Fin.sum_univ_three]
    change (v 1/v 0)^2+(v 2/v 0)^2+(v 3/v 0)^2=1
    field_simp
    nlinarith [hn]
  nlinarith [norm_nonneg (unitNullSpatial v)]

#print axioms reflectedSpatialScreen
#print axioms spatial_inner_components
#print axioms minkowski_quad_coordinates
#print axioms nonzero_null_time
#print axioms unit_null_spatial_norm
end
end ChatgptAudit
