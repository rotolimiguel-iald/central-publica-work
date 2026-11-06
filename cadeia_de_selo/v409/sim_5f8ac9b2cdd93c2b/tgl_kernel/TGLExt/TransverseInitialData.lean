-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_018 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.SmoothFlowControls

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Flow017 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def transverseProjection (v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ) :
    Coordinate4 →L[ℝ] Coordinate4 :=
  ContinuousLinearMap.id ℝ Coordinate4-ell.smulRight v

def initialPosition (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ) (z : Coordinate4) :
    Coordinate4 := p+transverseProjection v ell z

theorem exists_normalized_covector (v : Coordinate4) (hv : v≠0) :
    ∃ ell : Coordinate4 →L[ℝ] ℝ, ell v=1 := by
  have hex : ∃ j : Fin 4, v j≠0 := by
    by_contra h
    push Not at h
    exact hv (funext h)
  obtain ⟨j,hj⟩ := hex
  refine ⟨(v j)⁻¹ • (ContinuousLinearMap.proj j : Coordinate4 →L[ℝ] ℝ),?_⟩
  simp [hj]

theorem transverse_projection_decomposition (v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (z : Coordinate4) : transverseProjection v ell z+ell z • v=z := by
  simp [transverseProjection]

theorem transverse_projection_velocity (v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (hell : ell v=1) : transverseProjection v ell v=0 := by
  simp [transverseProjection,hell]

theorem initial_position_in_section (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (hell : ell v=1) (z : Coordinate4) : ell (initialPosition p v ell z-p)=0 := by
  simp [initialPosition,transverseProjection,map_sub,hell]

theorem initial_position_shift (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (hell : ell v=1) (z : Coordinate4) (s : ℝ) :
    initialPosition p v ell (z+s • v)=initialPosition p v ell z := by
  simp only [initialPosition,map_add,map_smul,transverse_projection_velocity v ell hell,smul_zero,add_zero]

theorem initial_time_shift (v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ)
    (hell : ell v=1) (z : Coordinate4) (s : ℝ) : ell (z+s • v)=ell z+s := by
  simp [map_add,map_smul,hell]

theorem initial_position_smooth (p v : Coordinate4) (ell : Coordinate4 →L[ℝ] ℝ) :
    ContDiff ℝ ∞ (initialPosition p v ell) :=
  contDiff_const.add (transverseProjection v ell).contDiff

def transportedNullSeed (A B : TensorField4) (p v : Coordinate4) (x : Coordinate4) : Coordinate4 :=
  (B x).mulVec ((A p).mulVec v)

theorem transported_seed_initial (A B : TensorField4) (p v : Coordinate4)
    (hBA : B p*A p=1) : transportedNullSeed A B p v p=v := by
  simp only [transportedNullSeed,Matrix.mulVec_mulVec,hBA,Matrix.one_mulVec]

theorem transported_seed_null (A B : TensorField4) (p v x : Coordinate4)
    (hAB : A x*B x=1) (hn : tensorQuad (frameMetricField A p) v=0) :
    tensorQuad (frameMetricField A x) (transportedNullSeed A B p v x)=0 := by
  rw [frameMetricField,tensorQuad_congruence,transportedNullSeed,Matrix.mulVec_mulVec,hAB,Matrix.one_mulVec]
  simpa only [frameMetricField,tensorQuad_congruence] using hn

theorem transported_seed_nonzero (A B : TensorField4) (p v x : Coordinate4)
    (hBA : B p*A p=1) (hAB : A x*B x=1) (hv : v≠0) :
    transportedNullSeed A B p v x≠0 := by
  intro hz
  have hh := congrArg (fun w : Coordinate4 => (A x).mulVec w) hz
  rw [transportedNullSeed,Matrix.mulVec_mulVec,hAB,Matrix.one_mulVec,Matrix.mulVec_zero] at hh
  have hv0 := congrArg (fun w : Coordinate4 => (B p).mulVec w) hh
  rw [Matrix.mulVec_mulVec,hBA,Matrix.one_mulVec,Matrix.mulVec_zero] at hv0
  exact hv hv0

theorem transported_seed_smooth (U : Set Coordinate4) (A B : TensorField4)
    (hB : SmoothMatrixOn U B) (p v : Coordinate4) :
    ContDiffOn ℝ ∞ (transportedNullSeed A B p v) U := by
  apply contDiffOn_pi.2
  exact matrix_mulVec_smooth U B (fun _ => (A p).mulVec v) hB (fun _ => contDiffOn_const)

#print axioms exists_normalized_covector
#print axioms transverse_projection_decomposition
#print axioms transverse_projection_velocity
#print axioms initial_position_in_section
#print axioms initial_position_shift
#print axioms initial_time_shift
#print axioms initial_position_smooth
#print axioms transported_seed_initial
#print axioms transported_seed_null
#print axioms transported_seed_nonzero
#print axioms transported_seed_smooth
end
end ChatgptAudit.Flow018
