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
import TGLExt.MetricCompatibleJet

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix
noncomputable section

abbrev ConnectionMatrix4 := Fin 4 → Matrix (Fin 4) (Fin 4) ℝ
abbrev ConnectionDerivative4 := Fin 4 → ConnectionMatrix4
abbrev ConnectionSecondDerivative4 := Fin 4 → ConnectionDerivative4

def connectionCurvatureJet (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (i j : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  dGamma i j-dGamma j i+Gamma i*Gamma j-Gamma j*Gamma i

def curvatureDerivativeJet (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (ddGamma : ConnectionSecondDerivative4) (k i j : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  ddGamma k i j-ddGamma k j i+dGamma k i*Gamma j+Gamma i*dGamma k j-
    dGamma k j*Gamma i-Gamma j*dGamma k i

def exteriorCurvatureDerivativeJet (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (ddGamma : ConnectionSecondDerivative4) (k i j : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  curvatureDerivativeJet Gamma dGamma ddGamma k i j+
    Gamma k*connectionCurvatureJet Gamma dGamma i j-
    connectionCurvatureJet Gamma dGamma i j*Gamma k

theorem curvature_jet_antisymmetric (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (i j : Fin 4) : connectionCurvatureJet Gamma dGamma i j = -connectionCurvatureJet Gamma dGamma j i := by
  unfold connectionCurvatureJet
  abel

theorem exterior_bianchi_jet (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (ddGamma : ConnectionSecondDerivative4) (hs : ∀ i j k, ddGamma i j k=ddGamma j i k)
    (i j k : Fin 4) :
    exteriorCurvatureDerivativeJet Gamma dGamma ddGamma i j k+
    exteriorCurvatureDerivativeJet Gamma dGamma ddGamma j k i+
    exteriorCurvatureDerivativeJet Gamma dGamma ddGamma k i j=0 := by
  simp only [exteriorCurvatureDerivativeJet,curvatureDerivativeJet,connectionCurvatureJet]
  rw [hs i j k,hs i k j,hs j k i]
  noncomm_ring

theorem first_bianchi_jet (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (ht : ∀ i j l, Gamma i l j=Gamma j l i)
    (hdt : ∀ k i j l, dGamma k i l j=dGamma k j l i) (i j k a : Fin 4) :
    connectionCurvatureJet Gamma dGamma i j a k+
    connectionCurvatureJet Gamma dGamma j k a i+
    connectionCurvatureJet Gamma dGamma k i a j=0 := by
  have hd : dGamma i j a k-dGamma j i a k+dGamma j k a i-dGamma k j a i+
      dGamma k i a j-dGamma i k a j=0 := by
    rw [hdt i j k a,hdt j i k a,hdt k j i a]
    abel
  have hp (l : Fin 4) : Gamma i a l*Gamma j l k-Gamma j a l*Gamma i l k+
      Gamma j a l*Gamma k l i-Gamma k a l*Gamma j l i+
      Gamma k a l*Gamma i l j-Gamma i a l*Gamma k l j=0 := by
    rw [ht j k l,ht i k l,ht j i l]
    ring
  have hs : (∑ l : Fin 4, (Gamma i a l*Gamma j l k-Gamma j a l*Gamma i l k+
      Gamma j a l*Gamma k l i-Gamma k a l*Gamma j l i+
      Gamma k a l*Gamma i l j-Gamma i a l*Gamma k l j))=0 := by
    simp only [hp,Finset.sum_const_zero]
  simp only [Finset.sum_add_distrib,Finset.sum_sub_distrib] at hs
  simp only [connectionCurvatureJet,Matrix.sub_apply,Matrix.add_apply,Matrix.mul_apply]
  linarith

theorem curvature_jet_metric_skew
    (g : Matrix (Fin 4) (Fin 4) ℝ) (dg : ConnectionMatrix4)
    (ddg : ConnectionDerivative4) (Gamma : ConnectionMatrix4) (dGamma : ConnectionDerivative4)
    (hm : ∀ i, dg i=(Gamma i)ᵀ*g+g*Gamma i)
    (hdm : ∀ k i, ddg k i=(dGamma k i)ᵀ*g+(Gamma i)ᵀ*dg k+dg k*Gamma i+g*dGamma k i)
    (hdd : ∀ i j, ddg i j=ddg j i) (i j : Fin 4) :
    (connectionCurvatureJet Gamma dGamma i j)ᵀ*g+g*connectionCurvatureJet Gamma dGamma i j=0 := by
  have he := (hdm i j).symm.trans ((hdd i j).trans (hdm j i))
  rw [hm i,hm j] at he
  calc
    (connectionCurvatureJet Gamma dGamma i j)ᵀ*g+g*connectionCurvatureJet Gamma dGamma i j =
      ((dGamma i j)ᵀ*g+(Gamma j)ᵀ*((Gamma i)ᵀ*g+g*Gamma i)+
        ((Gamma i)ᵀ*g+g*Gamma i)*Gamma j+g*dGamma i j)-
      ((dGamma j i)ᵀ*g+(Gamma i)ᵀ*((Gamma j)ᵀ*g+g*Gamma j)+
        ((Gamma j)ᵀ*g+g*Gamma j)*Gamma i+g*dGamma j i) := by
          simp only [connectionCurvatureJet,Matrix.transpose_sub,Matrix.transpose_add,Matrix.transpose_mul]
          noncomm_ring
    _ = 0 := sub_eq_zero.mpr he

theorem curvature_pair_symmetry_from_identities (R : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (hfirst : ∀ a b c d, R a b c d= -R b a c d)
    (hlast : ∀ a b c d, R a b c d= -R a b d c)
    (hcyclic : ∀ a b c d, R a b c d+R a c d b+R a d b c=0)
    (a b c d : Fin 4) : R a b c d=R c d a b := by
  linarith only [hcyclic a b c d,hcyclic b a c d,hcyclic c d a b,hcyclic d c a b,
    hfirst b a c d,hfirst c a b d,hfirst c b d a,hfirst d c a b,hfirst d a b c,hfirst d b c a,
    hlast a c d b,hlast b c d a,hlast b d c a]

#print axioms curvature_jet_antisymmetric
#print axioms exterior_bianchi_jet
#print axioms first_bianchi_jet
#print axioms curvature_jet_metric_skew
#print axioms curvature_pair_symmetry_from_identities
end
end ChatgptAudit
