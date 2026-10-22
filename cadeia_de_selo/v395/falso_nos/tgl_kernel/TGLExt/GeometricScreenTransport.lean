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
import TGLExt.NullScreenAlgebra

set_option autoImplicit false
set_option maxHeartbeats 3600000
namespace ChatgptAudit
open Matrix Filter Topology
noncomputable section

def connectionAlong (Gamma : ConnectionField4) (x v : Coordinate4) : Tensor4 :=
  ∑ i, v i • Gamma x i

theorem connection_metric_sum (Gamma : ConnectionField4) (x v : Coordinate4) (g : Tensor4) :
    (∑ i, v i • ((Gamma x i)ᵀ*g+g*Gamma x i))=
      (connectionAlong Gamma x v)ᵀ*g+g*connectionAlong Gamma x v := by
  have ht : (∑ i, v i • Gamma x i)ᵀ=∑ i, v i • (Gamma x i)ᵀ := by
    ext a b
    simp only [Matrix.transpose_apply,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul]
  simp [connectionAlong,ht,Finset.sum_add_distrib,Matrix.sum_mul,Matrix.mul_sum]

theorem metric_along_curve_derivative (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (hm : MetricCompatibleOn U g Gamma)
    (x v : Coordinate4) (hx : x∈U)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (curve : ℝ → Coordinate4) (t : ℝ) (hc : HasDerivAt curve v t) (hec : curve t=x) :
    HasMatrixDerivAt (fun s => g (curve s))
      ((connectionAlong Gamma x v)ᵀ*g x+g x*connectionAlong Gamma x v) t := by
  intro a b
  have hga : DifferentiableAt ℝ (fun y => g y a b) (curve t) := by
    rw [hec]
    exact hg a b
  have hd := hga.hasFDerivAt.comp_hasDerivAt t hc
  have he : fderiv ℝ (fun y => g y a b) (curve t) v=
      ((connectionAlong Gamma x v)ᵀ*g x+g x*connectionAlong Gamma x v) a b := by
    rw [hec,← scalarAlong_eq_fderiv (fun _ => v) (fun y => g y a b) x]
    have hm' : (∑ i, v i • tensorFieldJet g x i)=
        (connectionAlong Gamma x v)ᵀ*g x+g x*connectionAlong Gamma x v := by
      simp only [metric_compatibility_formula U g Gamma hm x hx]
      exact connection_metric_sum Gamma x v (g x)
    simpa only [scalarAlong,tensorFieldJet,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul] using
      congrArg (fun A : Tensor4 => A a b) hm'
  rw [he] at hd
  exact hd

theorem lie_screen_gram_derivative (g : ℝ → Tensor4) (S : ℝ → ScreenVectors)
    (L B : Tensor4) (t : ℝ)
    (hg : HasMatrixDerivAt g (Lᵀ*g t+g t*L) t)
    (hS : HasMatrixDerivAt S ((B-L)*S t) t) :
    HasMatrixDerivAt (fun s => screenGram (g s) (S s))
      ((S t)ᵀ*(Bᵀ*g t+g t*B)*S t) t := by
  have hd := screen_gram_derivative g S _ _ t hg hS
  have he :
      (((B-L)*S t)ᵀ*g t+(S t)ᵀ*(Lᵀ*g t+g t*L))*S t+
        ((S t)ᵀ*g t)*((B-L)*S t)=
      (S t)ᵀ*(Bᵀ*g t+g t*B)*S t := by
    simp only [Matrix.transpose_mul,Matrix.transpose_sub,Matrix.sub_mul,Matrix.mul_sub,
      Matrix.add_mul,Matrix.mul_add,Matrix.mul_assoc]
    abel
  rw [he] at hd
  exact hd

theorem geometric_screen_area_derivative (g : ℝ → Tensor4) (S : ℝ → ScreenVectors)
    (D B F L : Tensor4) (h : ScreenMatrix) (t : ℝ)
    (hFD : F*D=1) (hgram : Fᵀ*g t*F=nullScreenGram h)
    (hcols : S t=screenColumns F) (hp : 0<h.det)
    (hk : ∀ a, (B*F) a 0=0) (hn : (Fᵀ*g t*B*F) 0 1=0)
    (hg : HasMatrixDerivAt g (Lᵀ*g t+g t*L) t)
    (hS : HasMatrixDerivAt S ((B-L)*S t) t) :
    HasDerivAt (fun s => screenArea (screenGram (g s) (S s)))
      (Matrix.trace B*screenArea (screenGram (g t) (S t))) t := by
  have hvalue : screenGram (g t) (S t)=h := by
    rw [hcols,screen_gram_in_frame,hgram,null_gram_screen_block]
  have hd := lie_screen_gram_derivative g S L B t hg hS
  rw [hcols,screen_metric_variation (g t) D B F h hFD hgram] at hd
  have hh : HasMatrixDerivAt (fun s => screenGram (g s) (S s))
      ((screenBlock (inNullFrame D B F))ᵀ*screenGram (g t) (S t)+
        screenGram (g t) (S t)*screenBlock (inNullFrame D B F)) t := by
    rw [hvalue]
    exact hd
  have ha := screen_area_derivative (fun s => screenGram (g s) (S s))
    (screenBlock (inNullFrame D B F)) t (by rw [hvalue]; exact hp) hh
  rw [← ambient_expansion_is_screen_trace (g t) D B F h hFD hgram hk hn] at ha
  exact ha

theorem coordinate_screen_area_derivative (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (curve : ℝ → Coordinate4) (t : ℝ) (hc : HasDerivAt curve (V x) t) (hec : curve t=x)
    (S : ℝ → ScreenVectors) (D F : Tensor4) (h : ScreenMatrix)
    (hFD : F*D=1) (hgram : Fᵀ*g x*F=nullScreenGram h)
    (hcols : S t=screenColumns F) (hp : 0<h.det)
    (hk : ∀ a, (covariantVectorGradient Gamma V x*F) a 0=0)
    (hn : (Fᵀ*g x*covariantVectorGradient Gamma V x*F) 0 1=0)
    (hS : HasMatrixDerivAt S
      ((covariantVectorGradient Gamma V x-connectionAlong Gamma x (V x))*S t) t) :
    HasDerivAt (fun s => screenArea (screenGram (g (curve s)) (S s)))
      (vectorExpansion Gamma V x*screenArea (screenGram (g x) (S t))) t := by
  have hd := geometric_screen_area_derivative (fun s => g (curve s)) S D
    (covariantVectorGradient Gamma V x) F (connectionAlong Gamma x (V x)) h t
    hFD (by rw [hec]; exact hgram) hcols hp hk (by rw [hec]; exact hn)
    (by simpa only [hec] using metric_along_curve_derivative U g Gamma hm x (V x) hx hg curve t hc hec) hS
  simpa only [hec,vectorExpansion] using hd

#print axioms connection_metric_sum
#print axioms metric_along_curve_derivative
#print axioms lie_screen_gram_derivative
#print axioms geometric_screen_area_derivative
#print axioms coordinate_screen_area_derivative
end
end ChatgptAudit
