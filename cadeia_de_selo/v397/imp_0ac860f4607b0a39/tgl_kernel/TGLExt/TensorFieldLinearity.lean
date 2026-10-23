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
import TGLExt.CovariantScalarConservation

set_option autoImplicit false
namespace ChatgptAudit
open Matrix
noncomputable section

theorem tensorFieldJet_sub (A B : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x)
    (hB : ∀ j k, DifferentiableAt ℝ (fun y => B y j k) x) :
    tensorFieldJet (fun y => A y-B y) x = tensorFieldJet A x-tensorFieldJet B x := by
  funext i
  ext j k
  change (fderiv ℝ (fun y => A y j k-B y j k) x) (Pi.single i 1) = _
  rw [fderiv_fun_sub (hA j k) (hB j k)]
  rfl

theorem tensorFieldJet_const_smul (c : ℝ) (A : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x) :
    tensorFieldJet (fun y => c • A y) x=c • tensorFieldJet A x := by
  rw [tensorFieldJet_smul (fun _ => c) A x (differentiableAt_const c) hA]
  funext i
  simp [coordinatePartial]

theorem tensorFieldDivergence_sub (gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (A B : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x)
    (hB : ∀ j k, DifferentiableAt ℝ (fun y => B y j k) x) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (fun y => A y-B y) x j =
      tensorFieldDivergence gInv Gamma A x j-tensorFieldDivergence gInv Gamma B x j := by
  have hc (i : Fin 4) :
      covariantTensorJet (A x-B x) (tensorFieldJet A x-tensorFieldJet B x) (Gamma x) i =
        covariantTensorJet (A x) (tensorFieldJet A x) (Gamma x) i-
          covariantTensorJet (B x) (tensorFieldJet B x) (Gamma x) i := by
    simp only [covariantTensorJet,Pi.sub_apply,Matrix.mul_sub,Matrix.sub_mul]
    abel
  simp only [tensorFieldDivergence,tensorFieldJet_sub A B x hA hB,tensorJetDivergence,hc,
    Matrix.sub_apply,mul_sub,Finset.sum_sub_distrib]

theorem tensorFieldDivergence_const_smul (gInv : TensorField4)
    (Gamma : Coordinate4 → Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (c : ℝ) (A : TensorField4) (x : Coordinate4)
    (hA : ∀ j k, DifferentiableAt ℝ (fun y => A y j k) x) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (fun y => c • A y) x j =
      c*tensorFieldDivergence gInv Gamma A x j := by
  have hc (i : Fin 4) :
      covariantTensorJet (c • A x) (c • tensorFieldJet A x) (Gamma x) i =
        c • covariantTensorJet (A x) (tensorFieldJet A x) (Gamma x) i := by
    simp only [covariantTensorJet,Pi.smul_apply,Matrix.mul_smul,Matrix.smul_mul,smul_sub]
  simp only [tensorFieldDivergence,tensorFieldJet_const_smul c A x hA,tensorJetDivergence,hc,
    Matrix.smul_apply,smul_eq_mul,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro k hk
  ring

#print axioms tensorFieldJet_sub
#print axioms tensorFieldJet_const_smul
#print axioms tensorFieldDivergence_sub
#print axioms tensorFieldDivergence_const_smul
end
end ChatgptAudit
