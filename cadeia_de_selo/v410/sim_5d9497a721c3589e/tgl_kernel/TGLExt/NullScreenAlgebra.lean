-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_012 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ScreenAreaCalculus

set_option autoImplicit false
set_option maxHeartbeats 3600000
namespace ChatgptAudit
open Matrix
noncomputable section

def screenIndex (i : Fin 2) : Fin 4 := if i=0 then 2 else 3
def screenBlock (A : Tensor4) : ScreenMatrix := A.submatrix screenIndex screenIndex
def screenColumns (F : Tensor4) : ScreenVectors := F.submatrix id screenIndex
def nullScreenGram (h : ScreenMatrix) : Tensor4 :=
  !![0,-1,0,0; -1,0,0,0; 0,0,h 0 0,h 0 1; 0,0,h 1 0,h 1 1]
def inNullFrame (D B F : Tensor4) : Tensor4 := D*B*F

theorem null_gram_screen_block (h : ScreenMatrix) :
    screenBlock (nullScreenGram h)=h := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem screen_gram_in_frame (g F : Tensor4) :
    screenGram g (screenColumns F)=screenBlock (Fᵀ*g*F) := by
  rfl

theorem null_screen_variation_block (h : ScreenMatrix) (b : Tensor4) :
    screenBlock (bᵀ*nullScreenGram h+nullScreenGram h*b)=
      (screenBlock b)ᵀ*h+h*screenBlock b := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [screenBlock,screenIndex,nullScreenGram,Matrix.mul_apply,Fin.sum_univ_succ] <;>
    simp [Matrix.vecMul,dotProduct,Fin.sum_univ_succ]

theorem null_frame_trace (D B F : Tensor4) (hFD : F*D=1) :
    Matrix.trace (inNullFrame D B F)=Matrix.trace B := by
  unfold inNullFrame
  rw [Matrix.trace_mul_comm,← Matrix.mul_assoc,hFD,one_mul]

theorem null_frame_first_diagonal (D B F : Tensor4)
    (hk : ∀ a, (B*F) a 0=0) : inNullFrame D B F 0 0=0 := by
  unfold inNullFrame
  rw [Matrix.mul_assoc,Matrix.mul_apply]
  simp only [hk,mul_zero,Finset.sum_const_zero]

theorem null_frame_metric_product (g D B F : Tensor4) (hFD : F*D=1) :
    (Fᵀ*g*F)*inNullFrame D B F=Fᵀ*g*B*F := by
  unfold inNullFrame
  calc
    _=(Fᵀ*g)*(F*D)*(B*F) := by noncomm_ring
    _=_ := by rw [hFD,mul_one]; simp only [Matrix.mul_assoc]

theorem null_frame_second_diagonal (g D B F : Tensor4) (h : ScreenMatrix)
    (hFD : F*D=1) (hgram : Fᵀ*g*F=nullScreenGram h)
    (hn : (Fᵀ*g*B*F) 0 1=0) : inNullFrame D B F 1 1=0 := by
  have he : (nullScreenGram h*inNullFrame D B F) 0 1=0 := by
    rw [← hgram,null_frame_metric_product g D B F hFD]
    exact hn
  simpa [nullScreenGram,Matrix.mul_apply,Fin.sum_univ_succ] using he

theorem ambient_expansion_is_screen_trace (g D B F : Tensor4) (h : ScreenMatrix)
    (hFD : F*D=1) (hgram : Fᵀ*g*F=nullScreenGram h)
    (hk : ∀ a, (B*F) a 0=0) (hn : (Fᵀ*g*B*F) 0 1=0) :
    Matrix.trace B=Matrix.trace (screenBlock (inNullFrame D B F)) := by
  have hz0 := null_frame_first_diagonal D B F hk
  have hz1 := null_frame_second_diagonal g D B F h hFD hgram hn
  have ht : Matrix.trace (inNullFrame D B F)=Matrix.trace (screenBlock (inNullFrame D B F)) := by
    simp [Matrix.trace,Matrix.diag,screenBlock,screenIndex,Fin.sum_univ_succ,hz0,hz1]
  exact (null_frame_trace D B F hFD).symm.trans ht

theorem frame_metric_variation (g D B F : Tensor4) (hFD : F*D=1) :
    Fᵀ*(Bᵀ*g+g*B)*F=
      (inNullFrame D B F)ᵀ*(Fᵀ*g*F)+(Fᵀ*g*F)*inNullFrame D B F := by
  have hTF : Dᵀ*Fᵀ=1 := by rw [← Matrix.transpose_mul,hFD,Matrix.transpose_one]
  symm
  unfold inNullFrame
  calc
    _=(Fᵀ*Bᵀ)*(Dᵀ*Fᵀ)*g*F+(Fᵀ*g)*(F*D)*(B*F) := by
      simp only [Matrix.transpose_mul]
      noncomm_ring
    _=_ := by rw [hTF,hFD]; noncomm_ring

theorem screen_metric_variation (g D B F : Tensor4) (h : ScreenMatrix)
    (hFD : F*D=1) (hgram : Fᵀ*g*F=nullScreenGram h) :
    (screenColumns F)ᵀ*(Bᵀ*g+g*B)*screenColumns F=
      (screenBlock (inNullFrame D B F))ᵀ*h+h*screenBlock (inNullFrame D B F) := by
  change screenGram (Bᵀ*g+g*B) (screenColumns F)=_
  rw [screen_gram_in_frame,frame_metric_variation g D B F hFD,hgram]
  exact null_screen_variation_block h (inNullFrame D B F)

#print axioms null_gram_screen_block
#print axioms screen_gram_in_frame
#print axioms null_screen_variation_block
#print axioms null_frame_trace
#print axioms null_frame_first_diagonal
#print axioms null_frame_metric_product
#print axioms null_frame_second_diagonal
#print axioms ambient_expansion_is_screen_trace
#print axioms frame_metric_variation
#print axioms screen_metric_variation
end
end ChatgptAudit
