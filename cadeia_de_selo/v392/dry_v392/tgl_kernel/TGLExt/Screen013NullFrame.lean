-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026 (COPIA MECANICA de 013 sob namespace Screen013: a versao que COEXISTE com 012 no ROOT — colisao flatNullFrame; CONTADA; o original de 013 fica na bancada)
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
import TGLExt.CovariantNullPreservation
import TGLExt.SpatialScreenConstruction

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Screen013
open Matrix TGLExt
noncomputable section

def spacetimeLift (t : ℝ) (u : SpatialVector) : Coordinate4 := ![t,u 0,u 1,u 2]

theorem minkowski_pair_lift (t s : ℝ) (u w : SpatialVector) :
    tensorPair eta4 (spacetimeLift t u) (spacetimeLift s w)=t*s-inner ℝ u w := by
  rw [spatial_inner_components]
  simp [tensorPair,spacetimeLift,eta4,Matrix.mulVec,dotProduct,Fin.sum_univ_four]
  ring

def nullFrameMatrix (t : ℝ) (u : SpatialVector) (S : SpatialScreenBasis u) : Tensor4 :=
  fun a => ![(spacetimeLift t (t • u)) a,
    (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u)) a,
    (spacetimeLift 0 S.first) a,(spacetimeLift 0 S.second) a]

theorem null_frame_matrix_gram (t : ℝ) (ht : t≠0) (u : SpatialVector)
    (hu : inner ℝ u u=1) (S : SpatialScreenBasis u) :
    (nullFrameMatrix t u S)ᵀ*eta4*nullFrameMatrix t u S=nullScreenGram (-1) := by
  have hfu : inner ℝ S.first u=0 := by rw [real_inner_comm,S.axis_first_zero]
  have hsu : inner ℝ S.second u=0 := by rw [real_inner_comm,S.axis_second_zero]
  have hsf : inner ℝ S.second S.first=0 := by rw [real_inner_comm,S.cross_zero]
  ext i j
  rw [frame_pair_entry]
  fin_cases i <;> fin_cases j
  all_goals first
    | change tensorPair eta4 (spacetimeLift t (t • u)) (spacetimeLift t (t • u))=_
    | change tensorPair eta4 (spacetimeLift t (t • u)) (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u))=_
    | change tensorPair eta4 (spacetimeLift t (t • u)) (spacetimeLift 0 S.first)=_
    | change tensorPair eta4 (spacetimeLift t (t • u)) (spacetimeLift 0 S.second)=_
    | change tensorPair eta4 (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u)) (spacetimeLift t (t • u))=_
    | change tensorPair eta4 (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u)) (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u))=_
    | change tensorPair eta4 (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u)) (spacetimeLift 0 S.first)=_
    | change tensorPair eta4 (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u)) (spacetimeLift 0 S.second)=_
    | change tensorPair eta4 (spacetimeLift 0 S.first) (spacetimeLift t (t • u))=_
    | change tensorPair eta4 (spacetimeLift 0 S.first) (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u))=_
    | change tensorPair eta4 (spacetimeLift 0 S.first) (spacetimeLift 0 S.first)=_
    | change tensorPair eta4 (spacetimeLift 0 S.first) (spacetimeLift 0 S.second)=_
    | change tensorPair eta4 (spacetimeLift 0 S.second) (spacetimeLift t (t • u))=_
    | change tensorPair eta4 (spacetimeLift 0 S.second) (spacetimeLift (-(2*t)⁻¹) ((2*t)⁻¹ • u))=_
    | change tensorPair eta4 (spacetimeLift 0 S.second) (spacetimeLift 0 S.first)=_
    | change tensorPair eta4 (spacetimeLift 0 S.second) (spacetimeLift 0 S.second)=_
  all_goals rw [minkowski_pair_lift]
  all_goals simp only [real_inner_smul_left,real_inner_smul_right,hu,S.unit_first,
    S.unit_second,S.cross_zero,S.axis_first_zero,S.axis_second_zero,hfu,hsu,hsf]
  all_goals norm_num [nullScreenGram,Matrix.cons_val_two,Matrix.cons_val_three]
  all_goals try field_simp
  all_goals ring

theorem normalized_null_gram_squared :
    nullScreenGram (-1)*nullScreenGram (-1)=(1:Tensor4) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [nullScreenGram,Matrix.mul_apply,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

structure NormalizedNullFrame (g : Tensor4) (v : Coordinate4) where
  frame : Tensor4
  inverse : Tensor4
  right_inverse : frame*inverse=1
  gram : frameᵀ*g*frame=nullScreenGram (-1)
  first_column : ∀ a, frame a 0=v a

def flatNullFrame (v : Coordinate4) (hv : v≠0) (hn : tensorQuad eta4 v=0) :
    NormalizedNullFrame eta4 v := by
  let u := unitNullSpatial v
  have hu : ‖u‖=1 := unit_null_spatial_norm v hv hn
  let S := reflectedSpatialScreen u hu
  let F := nullFrameMatrix (v 0) u S
  let D := nullScreenGram (-1)*Fᵀ*eta4
  have ht := nonzero_null_time v hv hn
  have huu : inner ℝ u u=1 := by rw [real_inner_self_eq_norm_sq,hu]; norm_num
  have hgram : Fᵀ*eta4*F=nullScreenGram (-1) := null_frame_matrix_gram _ ht u huu S
  have hDF : D*F=1 := by
    change (nullScreenGram (-1)*Fᵀ*eta4)*F=1
    calc
      _=nullScreenGram (-1)*(Fᵀ*eta4*F) := by simp only [Matrix.mul_assoc]
      _=1 := by rw [hgram]; exact normalized_null_gram_squared
  refine {
    frame := F
    inverse := D
    right_inverse := mul_eq_one_comm.mp hDF
    gram := hgram
    first_column := ?_ }
  intro a
  fin_cases a
  · rfl
  · change v 0*(v 1/v 0)=v 1
    field_simp
  · change v 0*(v 2/v 0)=v 2
    field_simp
  · change v 0*(v 3/v 0)=v 3
    field_simp

theorem invertible_solder_nonzero (E D : Tensor4) (hDE : D*E=1)
    (v : Coordinate4) (hv : v≠0) : E.mulVec v≠0 := by
  intro h
  apply hv
  have he := congrArg (fun w : Coordinate4 => D.mulVec w) h
  rw [Matrix.mulVec_mulVec,hDE,Matrix.one_mulVec,Matrix.mulVec_zero] at he
  exact he

def solderedNullFrame (E D : Tensor4) (hED : E*D=1) (hDE : D*E=1)
    (v : Coordinate4) (hv : v≠0) (hn : tensorQuad (Eᵀ*eta4*E) v=0) :
    NormalizedNullFrame (Eᵀ*eta4*E) v := by
  have hn' : tensorQuad eta4 (E.mulVec v)=0 := by
    rw [← tensorQuad_congruence]
    exact hn
  let F := flatNullFrame (E.mulVec v) (invertible_solder_nonzero E D hDE v hv) hn'
  refine {
    frame := D*F.frame
    inverse := F.inverse*E
    right_inverse := ?_
    gram := ?_
    first_column := ?_ }
  · calc
      (D*F.frame)*(F.inverse*E)=D*(F.frame*F.inverse)*E := by simp only [Matrix.mul_assoc]
      _=1 := by rw [F.right_inverse,Matrix.mul_one,hDE]
  · calc
      (D*F.frame)ᵀ*(Eᵀ*eta4*E)*(D*F.frame)=
        F.frameᵀ*(E*D)ᵀ*eta4*(E*D)*F.frame := by
          simp only [Matrix.transpose_mul,Matrix.mul_assoc]
      _=nullScreenGram (-1) := by simp only [hED,Matrix.transpose_one,Matrix.mul_one,F.gram]
  · intro a
    change ∑ j, D a j*F.frame j 0=v a
    simp only [F.first_column]
    have he : D.mulVec (E.mulVec v)=v := by
      rw [Matrix.mulVec_mulVec,hDE,Matrix.one_mulVec]
    exact congrArg (fun w : Coordinate4 => w a) he

#print axioms minkowski_pair_lift
#print axioms null_frame_matrix_gram
#print axioms normalized_null_gram_squared
#print axioms flatNullFrame
#print axioms invertible_solder_nonzero
#print axioms solderedNullFrame
end
end ChatgptAudit.Screen013
