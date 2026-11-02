-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026
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
set_option maxHeartbeats 7000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Screen014
open Matrix
noncomputable section

def rawScreenGram (a b c : ℝ) (h : ScreenMatrix) : Tensor4 :=
  !![0,-1,0,0; -1,a,b,c; 0,b,h 0 0,h 0 1; 0,c,h 1 0,h 1 1]

def completionQ0 (b c : ℝ) (h : ScreenMatrix) : ℝ := (h 1 1*b-h 0 1*c)/h.det
def completionQ1 (b c : ℝ) (h : ScreenMatrix) : ℝ := (h 0 0*c-h 1 0*b)/h.det
def nullCompletion (a b c : ℝ) (h : ScreenMatrix) : Tensor4 :=
  !![1,(a-b*completionQ0 b c h-c*completionQ1 b c h)/2,0,0;
     0,1,0,0; 0,-completionQ0 b c h,1,0; 0,-completionQ1 b c h,0,1]

theorem raw_gram_shape (G : Tensor4) (hs : Gᵀ=G)
    (h00 : G 0 0=0) (h01 : G 0 1= -1) (h02 : G 0 2=0) (h03 : G 0 3=0) :
    G=rawScreenGram (G 1 1) (G 1 2) (G 1 3) (screenBlock G) := by
  have hs' (i j : Fin 4) : G j i=G i j := congrArg (fun M : Tensor4 => M i j) hs
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rawScreenGram,screenBlock,screenIndex,Matrix.cons_val_two,Matrix.cons_val_three,
      hs' 0 1,hs' 0 2,hs' 0 3,hs' 1 2,hs' 1 3,h00,h01,h02,h03]

def coefficientCompletion (a b c p q : ℝ) : Tensor4 :=
  !![1,(a-b*p-c*q)/2,0,0; 0,1,0,0; 0,-p,1,0; 0,-q,0,1]

theorem completion_coefficients_solve (b c : ℝ) (h : ScreenMatrix) (hd : h.det≠0) :
    h 0 0*completionQ0 b c h+h 0 1*completionQ1 b c h=b ∧
    h 1 0*completionQ0 b c h+h 1 1*completionQ1 b c h=c := by
  constructor
  · calc
      _=(h.det*b)/h.det := by
        simp only [completionQ0,completionQ1,Matrix.det_fin_two]
        ring
      _=b := by field_simp
  · calc
      _=(h.det*c)/h.det := by
        simp only [completionQ0,completionQ1,Matrix.det_fin_two]
        ring
      _=c := by field_simp

theorem completed_gram_coefficients (a b c p q : ℝ) (h : ScreenMatrix)
    (hs : hᵀ=h) (hp : h 0 0*p+h 0 1*q=b) (hq : h 1 0*p+h 1 1*q=c) :
    (coefficientCompletion a b c p q)ᵀ*rawScreenGram a b c h*
      coefficientCompletion a b c p q=nullScreenGram h := by
  have h10 : h 1 0=h 0 1 := congrArg (fun M : ScreenMatrix => M 0 1) hs
  rw [← hp,← hq]
  ext i j
  rw [frame_pair_entry]
  fin_cases i <;> fin_cases j <;>
    simp [tensorPair,Matrix.mulVec,dotProduct,coefficientCompletion,rawScreenGram,
      nullScreenGram,Fin.sum_univ_four,h10,Matrix.cons_val_two,Matrix.cons_val_three] <;> ring

theorem completed_gram (a b c : ℝ) (h : ScreenMatrix) (hs : hᵀ=h) (hd : h.det≠0) :
    (nullCompletion a b c h)ᵀ*rawScreenGram a b c h*nullCompletion a b c h=nullScreenGram h := by
  have hc := completion_coefficients_solve b c h hd
  exact completed_gram_coefficients a b c (completionQ0 b c h) (completionQ1 b c h) h hs hc.1 hc.2

theorem completion_first_column (F : Tensor4) (a b c : ℝ) (h : ScreenMatrix) :
    ∀ i, (F*nullCompletion a b c h) i 0=F i 0 := by
  intro i
  simp [nullCompletion,Matrix.mul_apply,Fin.sum_univ_four,
    Matrix.cons_val_two,Matrix.cons_val_three]

theorem completion_keeps_screen (F : Tensor4) (a b c : ℝ) (h : ScreenMatrix) :
    screenColumns (F*nullCompletion a b c h)=screenColumns F := by
  ext i j
  fin_cases j <;>
    simp [screenColumns,screenIndex,nullCompletion,Matrix.mul_apply,Fin.sum_univ_four,
      Matrix.cons_val_two,Matrix.cons_val_three]

theorem null_screen_gram_determinant (h : ScreenMatrix) :
    (nullScreenGram h).det= -h.det := by
  have hminor : (nullScreenGram h).submatrix Fin.succ (1:Fin 4).succAbove=
      !![-1,0,0;0,h 0 0,h 0 1;0,h 1 0,h 1 1] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  rw [Matrix.det_succ_row_zero]
  simp only [Fin.sum_univ_four]
  rw [hminor]
  norm_num [nullScreenGram,Matrix.cons_val_two,Matrix.cons_val_three,
    Matrix.det_fin_three,Matrix.det_fin_two]
  ring

theorem frame_det_nonzero_from_null_gram (g F : Tensor4) (h : ScreenMatrix)
    (hgram : Fᵀ*g*F=nullScreenGram h) (hd : h.det≠0) : F.det≠0 := by
  intro hz
  have he := congrArg Matrix.det hgram
  rw [Matrix.det_mul,Matrix.det_mul,Matrix.det_transpose,hz,
    null_screen_gram_determinant] at he
  apply hd
  linarith

def completedNullScreen (g B : Tensor4) (v : Coordinate4) (F : Tensor4)
    (a b c : ℝ) (h : ScreenMatrix)
    (hs : hᵀ=h) (hgram : Fᵀ*g*F=rawScreenGram a b c h)
    (hf : ∀ i, F i 0=v i) (hnegative : h 0 0 < 0) (hd : 0 < h.det)
    (hpair : ∀ w, tensorPair g v (B.mulVec w)=0) :
    NullScreenAt g B v (screenColumns F) := by
  let C := nullCompletion a b c h
  let Fc := F*C
  have hg : Fcᵀ*g*Fc=nullScreenGram h := by
    calc
      Fcᵀ*g*Fc=Cᵀ*(Fᵀ*g*F)*C := by
        simp only [Fc,Matrix.transpose_mul,Matrix.mul_assoc]
      _=nullScreenGram h := by rw [hgram]; exact completed_gram a b c h hs (ne_of_gt hd)
  have hcol : ∀ i, Fc i 0=v i := by
    intro i
    change (F*nullCompletion a b c h) i 0=v i
    rw [completion_first_column,hf]
  refine {
    frame := Fc
    inverse := Fc⁻¹
    metric := h
    right_inverse := Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.2
      (frame_det_nonzero_from_null_gram g Fc h hg (ne_of_gt hd)))
    gram := hg
    first_column := hcol
    columns := (completion_keeps_screen F a b c h).symm
    first_screen_negative := hnegative
    determinant_positive := hd
    preserves_null_pairing := ?_ }
  rw [mixed_frame_pair_entry]
  have he : (fun i => Fc i 0)=v := funext hcol
  rw [he]
  exact hpair _

#print axioms raw_gram_shape
#print axioms completion_coefficients_solve
#print axioms completed_gram_coefficients
#print axioms completed_gram
#print axioms completion_first_column
#print axioms completion_keeps_screen
#print axioms null_screen_gram_determinant
#print axioms frame_det_nonzero_from_null_gram
#print axioms completedNullScreen
end
end ChatgptAudit.Screen014
