-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_009 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.SmoothMatrixCalculus
import TGLExt.CurvatureJetAlgebra

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

abbrev ConnectionField4 := Coordinate4 → ConnectionMatrix4

def SmoothConnectionOn (U : Set Coordinate4) (Gamma : ConnectionField4) : Prop :=
  ∀ i, SmoothMatrixOn U (fun x => Gamma x i)

def connectionFirstJet (Gamma : ConnectionField4) (x : Coordinate4) : ConnectionDerivative4 :=
  fun i j => tensorFieldJet (fun y => Gamma y j) x i

def connectionSecondJet (Gamma : ConnectionField4) (x : Coordinate4) : ConnectionSecondDerivative4 :=
  fun k i j => tensorFieldJet (fun y => connectionFirstJet Gamma y i j) x k

def coordinateCurvature (Gamma : ConnectionField4) (x : Coordinate4) (i j : Fin 4) :
    Matrix (Fin 4) (Fin 4) ℝ := connectionCurvatureJet (Gamma x) (connectionFirstJet Gamma x) i j

def exteriorCovariantCurvatureDerivative (Gamma : ConnectionField4) (x : Coordinate4)
    (k i j : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  tensorFieldJet (fun y => coordinateCurvature Gamma y i j) x k+
    Gamma x k*coordinateCurvature Gamma x i j-coordinateCurvature Gamma x i j*Gamma x k

theorem coordinate_curvature_antisymmetric (Gamma : ConnectionField4) (x : Coordinate4) (i j : Fin 4) :
    coordinateCurvature Gamma x i j= -coordinateCurvature Gamma x j i :=
  curvature_jet_antisymmetric (Gamma x) (connectionFirstJet Gamma x) i j

theorem connection_first_jet_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma) (i j : Fin 4) :
    SmoothMatrixOn U (fun x => connectionFirstJet Gamma x i j) :=
  tensorFieldJet_smooth U hU (fun x => Gamma x j) (hG j) i

theorem coordinate_curvature_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma) (i j : Fin 4) :
    SmoothMatrixOn U (fun x => coordinateCurvature Gamma x i j) := by
  exact SmoothMatrixOn.sub U _ _
    (SmoothMatrixOn.add U _ _
      (SmoothMatrixOn.sub U _ _ (connection_first_jet_smooth U hU Gamma hG i j)
        (connection_first_jet_smooth U hU Gamma hG j i))
      (SmoothMatrixOn.mul U _ _ (hG i) (hG j)))
    (SmoothMatrixOn.mul U _ _ (hG j) (hG i))

theorem coordinate_curvature_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x : Coordinate4) (hx : x∈U) (k i j : Fin 4) :
    tensorFieldJet (fun y => coordinateCurvature Gamma y i j) x k =
      curvatureDerivativeJet (Gamma x) (connectionFirstJet Gamma x) (connectionSecondJet Gamma x) k i j := by
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :
      ∀ a b, DifferentiableAt ℝ (fun y => A y a b) x :=
    smooth_matrix_differentiableAt U hU A hA x hx
  have hGi := hdiff _ (hG i)
  have hGj := hdiff _ (hG j)
  have hA := connection_first_jet_smooth U hU Gamma hG i j
  have hB := connection_first_jet_smooth U hU Gamma hG j i
  have hAB := SmoothMatrixOn.sub U _ _ hA hB
  have hC := SmoothMatrixOn.mul U _ _ (hG i) (hG j)
  have hD := SmoothMatrixOn.mul U _ _ (hG j) (hG i)
  have hABC := SmoothMatrixOn.add U _ _ hAB hC
  change tensorFieldJet (fun y =>
    connectionFirstJet Gamma y i j-connectionFirstJet Gamma y j i+
      Gamma y i*Gamma y j-Gamma y j*Gamma y i) x k = _
  rw [tensorFieldJet_sub _ _ x (hdiff _ hABC) (hdiff _ hD),
    tensorFieldJet_add _ _ x (hdiff _ hAB) (hdiff _ hC),
    tensorFieldJet_sub _ _ x (hdiff _ hA) (hdiff _ hB)]
  simp only [Pi.sub_apply,Pi.add_apply,tensorFieldJet_mul _ _ x hGi hGj,
    tensorFieldJet_mul _ _ x hGj hGi,curvatureDerivativeJet,connectionFirstJet,connectionSecondJet]
  abel

theorem coordinate_exterior_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x : Coordinate4) (hx : x∈U) (i j k : Fin 4) :
    exteriorCovariantCurvatureDerivative Gamma x i j k+
    exteriorCovariantCurvatureDerivative Gamma x j k i+
    exteriorCovariantCurvatureDerivative Gamma x k i j=0 := by
  have he (a b c : Fin 4) : exteriorCovariantCurvatureDerivative Gamma x a b c =
      exteriorCurvatureDerivativeJet (Gamma x) (connectionFirstJet Gamma x)
        (connectionSecondJet Gamma x) a b c := by
    rw [exteriorCovariantCurvatureDerivative,coordinate_curvature_derivative U hU Gamma hG x hx]
    rfl
  rw [he,he,he]
  apply exterior_bianchi_jet
  intro a b c
  exact tensorFieldJet_commute U hU (fun y => Gamma y c) (hG c) x hx a b

theorem torsion_free_first_jet (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (k i j l : Fin 4) :
    connectionFirstJet Gamma x k i l j=connectionFirstJet Gamma x k j l i := by
  have he : (fun y => Gamma y i l j) =ᶠ[𝓝 x] (fun y => Gamma y j l i) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact ht y hy i j l
  exact congrArg (fun L : Coordinate4 →L[ℝ] ℝ => L (Pi.single k 1)) he.fderiv_eq

theorem coordinate_first_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (i j k a : Fin 4) :
    coordinateCurvature Gamma x i j a k+
    coordinateCurvature Gamma x j k a i+
    coordinateCurvature Gamma x k i a j=0 :=
  first_bianchi_jet (Gamma x) (connectionFirstJet Gamma x) (ht x hx)
    (torsion_free_first_jet U hU Gamma ht x hx) i j k a

#print axioms coordinate_curvature_antisymmetric
#print axioms connection_first_jet_smooth
#print axioms coordinate_curvature_smooth
#print axioms coordinate_curvature_derivative
#print axioms coordinate_exterior_bianchi
#print axioms torsion_free_first_jet
#print axioms coordinate_first_bianchi
end
end ChatgptAudit
