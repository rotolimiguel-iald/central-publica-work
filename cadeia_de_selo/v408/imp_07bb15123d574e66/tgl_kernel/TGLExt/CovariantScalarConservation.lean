-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_008 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.MetricCompatibleJet
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix Filter Topology
noncomputable section

abbrev Coordinate4 := Fin 4 → ℝ
abbrev TensorField4 := Coordinate4 → Matrix (Fin 4) (Fin 4) ℝ

def coordinatePartial (f : Coordinate4 → ℝ) (x : Coordinate4) (i : Fin 4) : ℝ :=
  fderiv ℝ f x (Pi.single i 1)

def tensorFieldJet (A : TensorField4) (x : Coordinate4) (i : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun j k => coordinatePartial (fun y => A y j k) x i

def tensorFieldDivergence (gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (A : TensorField4) (x : Coordinate4) (j : Fin 4) : ℝ :=
  tensorJetDivergence (gInv x) (A x) (tensorFieldJet A x) (Gamma x) j

theorem coordinatePartial_mul (f g : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 4) :
    coordinatePartial (fun y => f y*g y) x i = coordinatePartial f x i*g x+f x*coordinatePartial g x i := by
  simp only [coordinatePartial,fderiv_fun_mul hf hg,_root_.add_apply,_root_.smul_apply,smul_eq_mul]
  ring

theorem tensorFieldJet_smul (f : Coordinate4 → ℝ) (g : TensorField4) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (hg : ∀ j k, DifferentiableAt ℝ (fun y => g y j k) x) :
    tensorFieldJet (fun y => f y • g y) x =
      fun i => coordinatePartial f x i • g x+f x • tensorFieldJet g x i := by
  funext i
  ext j k
  exact coordinatePartial_mul f (fun y => g y j k) x hf (hg j k) i

theorem tensorFieldJet_congr_on (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : Set.EqOn A B U) (x : Coordinate4) (hx : x∈U) :
    tensorFieldJet A x=tensorFieldJet B x := by
  funext i
  ext j k
  have he : (fun y => A y j k) =ᶠ[𝓝 x] (fun y => B y j k) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    rw [hAB hy]
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single i 1)) he.fderiv_eq

theorem tensorFieldDivergence_congr_on (U : Set Coordinate4) (hU : IsOpen U)
    (gInv : TensorField4) (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (A B : TensorField4) (hAB : Set.EqOn A B U) (x : Coordinate4) (hx : x∈U) :
    tensorFieldDivergence gInv Gamma A x=tensorFieldDivergence gInv Gamma B x := by
  funext j
  rw [tensorFieldDivergence,tensorFieldDivergence,hAB hx,tensorFieldJet_congr_on U hU A B hAB x hx]

theorem tensorFieldJet_symmetric_on (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : ∀ x∈U, (g x)ᵀ=g x) (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    (tensorFieldJet g x i)ᵀ=tensorFieldJet g x i := by
  ext j k
  have he : (fun y => g y k j) =ᶠ[𝓝 x] (fun y => g y j k) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A j k) (hg y hy)
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single i 1)) he.fderiv_eq

theorem partials_zero_implies_fderiv_zero (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hz : ∀ i, coordinatePartial f x i=0) : fderiv ℝ f x=0 := by
  ext v
  have hv : v=∑ i : Fin 4, v i • Pi.single i (1:ℝ) := by
    ext j
    simp [Pi.single_apply]
  rw [hv,map_sum]
  simp only [map_smul,show ∀ i, fderiv ℝ f x (Pi.single i 1)=0 from hz,smul_zero,Finset.sum_const_zero]
  rfl

theorem pure_trace_field_divergence (g gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (hg : ∀ j k, DifferentiableAt ℝ (fun y => g y j k) x)
    (hInv : gInv x*g x=1)
    (hmetric : ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (fun y => f y • g y) x j=coordinatePartial f x j := by
  rw [tensorFieldDivergence,tensorFieldJet_smul f g x hf hg]
  exact divergence_pure_trace_jet (g x) (gInv x) hInv (tensorFieldJet g x) (Gamma x) hmetric
    (f x) (coordinatePartial f x) j

theorem conserved_pure_trace_is_constant (U : Set Coordinate4) (hU : IsOpen U)
    (hconn : IsPreconnected U) (g gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (f : Coordinate4 → ℝ) (hf : DifferentiableOn ℝ f U)
    (hg : ∀ j k, DifferentiableOn ℝ (fun y => g y j k) U)
    (hInv : ∀ x∈U, gInv x*g x=1)
    (hmetric : ∀ x∈U, ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0)
    (hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence gInv Gamma (fun y => f y • g y) x j=0) :
    ∃ c : ℝ, ∀ x∈U, f x=c := by
  apply hU.exists_is_const_of_fderiv_eq_zero hconn hf
  intro x hx
  apply partials_zero_implies_fderiv_zero
  intro j
  rw [← pure_trace_field_divergence g gInv Gamma f x (hf.differentiableAt (hU.mem_nhds hx))
    (fun i k => (hg i k).differentiableAt (hU.mem_nhds hx)) (hInv x hx) (hmetric x hx) j]
  exact hdiv x hx j

#print axioms coordinatePartial_mul
#print axioms tensorFieldJet_smul
#print axioms tensorFieldJet_congr_on
#print axioms tensorFieldDivergence_congr_on
#print axioms tensorFieldJet_symmetric_on
#print axioms partials_zero_implies_fderiv_zero
#print axioms pure_trace_field_divergence
#print axioms conserved_pure_trace_is_constant
end
end ChatgptAudit
