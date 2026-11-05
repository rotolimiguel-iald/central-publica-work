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
import TGLExt.Screen013Constructed

set_option autoImplicit false
set_option maxHeartbeats 3000000
namespace ChatgptAudit.Screen013
open Matrix TGLExt
noncomputable section

theorem zero_direction_has_no_null_screen (g B : Tensor4) (S : ScreenVectors) :
    ¬ Nonempty (NullScreenAt g B 0 S) := by
  rintro ⟨F⟩
  have hDF : F.inverse*F.frame=1 := mul_eq_one_comm.mp F.right_inverse
  have he := congrArg (fun A : Tensor4 => A 0 0) hDF
  simp only [Matrix.mul_apply,F.first_column,Pi.zero_apply,mul_zero,Finset.sum_const_zero,
    Matrix.one_apply,ite_true] at he
  norm_num at he

def offAxisNullVector : Coordinate4 := ![5,3,4,0]

theorem off_axis_vector_nonzero : offAxisNullVector≠0 := by
  intro h
  have he := congrArg (fun v : Coordinate4 => v 0) h
  norm_num [offAxisNullVector] at he

theorem off_axis_vector_null : tensorQuad eta4 offAxisNullVector=0 := by
  rw [minkowski_quad_coordinates]
  norm_num [offAxisNullVector,Matrix.cons_val_two,Matrix.cons_val_three]

def offAxisNullFrame : NormalizedNullFrame eta4 offAxisNullVector :=
  flatNullFrame offAxisNullVector off_axis_vector_nonzero off_axis_vector_null

theorem off_axis_frame_verified :
    offAxisNullFrame.frame*offAxisNullFrame.inverse=1 ∧
    offAxisNullFrame.frameᵀ*eta4*offAxisNullFrame.frame=nullScreenGram (-1) ∧
    (∀ a, offAxisNullFrame.frame a 0=offAxisNullVector a) :=
  ⟨offAxisNullFrame.right_inverse,offAxisNullFrame.gram,offAxisNullFrame.first_column⟩

theorem normalized_family_area_constant (g : ℝ → Tensor4) (S : ℝ → ScreenVectors)
    (hn : ∀ t, screenGram (g t) (S t)=-1) :
    (fun t => screenArea (screenGram (g t) (S t)))=(fun _ => (1:ℝ)) := by
  funext t
  rw [hn t,negative_identity_screen_area]

theorem normalized_family_expansion_obstruction (g : ℝ → Tensor4)
    (S : ℝ → ScreenVectors) (theta t : ℝ)
    (hn : ∀ s, screenGram (g s) (S s)=-1)
    (hr : HasDerivAt (fun s => screenArea (screenGram (g s) (S s)))
      (theta*screenArea (screenGram (g t) (S t))) t) : theta=0 := by
  rw [hn t,negative_identity_screen_area,mul_one] at hr
  rw [normalized_family_area_constant g S hn] at hr
  exact hr.unique (hasDerivAt_const t (1:ℝ))

#print axioms zero_direction_has_no_null_screen
#print axioms off_axis_vector_nonzero
#print axioms off_axis_vector_null
#print axioms offAxisNullFrame
#print axioms off_axis_frame_verified
#print axioms normalized_family_area_constant
#print axioms normalized_family_expansion_obstruction
end
end ChatgptAudit.Screen013
