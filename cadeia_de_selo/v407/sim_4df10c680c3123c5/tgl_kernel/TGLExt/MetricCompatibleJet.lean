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
import TGLExt.EmergenceTriad

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace ChatgptAudit
open Matrix TGLExt
noncomputable section

def covariantTensorJet (A : Matrix (Fin 4) (Fin 4) ℝ)
    (dA Gamma : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (i : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  dA i - (Gamma i)ᵀ*A - A*Gamma i

def tensorJetDivergence (gInv A : Matrix (Fin 4) (Fin 4) ℝ)
    (dA Gamma : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (j : Fin 4) : ℝ :=
  ∑ i, ∑ k, gInv i k * covariantTensorJet A dA Gamma i k j

def lowerChristoffelJet (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (i : Fin 4) :
    Matrix (Fin 4) (Fin 4) ℝ := fun j k => (dg i j k + dg k i j - dg j i k)/2

def leviCivitaJet (gInv : Matrix (Fin 4) (Fin 4) ℝ)
    (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (i : Fin 4) : Matrix (Fin 4) (Fin 4) ℝ :=
  gInv * lowerChristoffelJet dg i

theorem lower_christoffel_metric_identity (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (hs : ∀ i, (dg i)ᵀ=dg i) (i : Fin 4) :
    (lowerChristoffelJet dg i)ᵀ + lowerChristoffelJet dg i = dg i := by
  ext j k
  have he : dg i k j=dg i j k := congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A j k) (hs i)
  simp only [lowerChristoffelJet,Matrix.transpose_apply,Matrix.add_apply]
  linarith

theorem levi_civita_jet_metric_compatible
    (g gInv : Matrix (Fin 4) (Fin 4) ℝ) (hgInv : gInvᵀ=gInv)
    (hleft : gInv*g=1) (hright : g*gInv=1)
    (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (hs : ∀ i, (dg i)ᵀ=dg i) :
    ∀ i, covariantTensorJet g dg (leviCivitaJet gInv dg) i=0 := by
  intro i
  have h1 : (leviCivitaJet gInv dg i)ᵀ*g=(lowerChristoffelJet dg i)ᵀ := by
    rw [leviCivitaJet,Matrix.transpose_mul,hgInv,Matrix.mul_assoc,hleft,mul_one]
  have h2 : g*leviCivitaJet gInv dg i=lowerChristoffelJet dg i := by
    rw [leviCivitaJet,← Matrix.mul_assoc,hright,one_mul]
  rw [covariantTensorJet,h1,h2,← lower_christoffel_metric_identity dg hs i]
  abel

theorem levi_civita_jet_torsion_free (gInv : Matrix (Fin 4) (Fin 4) ℝ)
    (dg : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) (hs : ∀ i, (dg i)ᵀ=dg i)
    (i j l : Fin 4) : leviCivitaJet gInv dg i l j=leviCivitaJet gInv dg j l i := by
  simp only [leviCivitaJet,Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro k hk
  have he (a b c : Fin 4) : dg a c b=dg a b c :=
    congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A b c) (hs a)
  unfold lowerChristoffelJet
  rw [he i j k,he j i k,he k i j]
  ring

theorem covariant_pure_trace_jet
    (g : Matrix (Fin 4) (Fin 4) ℝ) (dg Gamma : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (hc : ∀ i, covariantTensorJet g dg Gamma i=0) (c : ℝ) (dc : Fin 4 → ℝ) (i : Fin 4) :
    covariantTensorJet (c • g) (fun i => dc i • g+c • dg i) Gamma i=dc i • g := by
  have he : covariantTensorJet (c • g) (fun i => dc i • g+c • dg i) Gamma i =
      dc i • g + c • covariantTensorJet g dg Gamma i := by
    simp only [covariantTensorJet,Matrix.mul_smul,Matrix.smul_mul,smul_sub]
    abel
  rw [he,hc,smul_zero,add_zero]

theorem divergence_pure_trace_jet
    (g gInv : Matrix (Fin 4) (Fin 4) ℝ) (hInv : gInv*g=1)
    (dg Gamma : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ)
    (hc : ∀ i, covariantTensorJet g dg Gamma i=0) (c : ℝ) (dc : Fin 4 → ℝ) (j : Fin 4) :
    tensorJetDivergence gInv (c • g) (fun i => dc i • g+c • dg i) Gamma j=dc j := by
  simp only [tensorJetDivergence,covariant_pure_trace_jet g dg Gamma hc,
    Matrix.smul_apply,smul_eq_mul]
  calc
    (∑ i, ∑ k, gInv i k*(dc i*g k j)) = ∑ i, dc i*(gInv*g) i j := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Matrix.mul_apply,Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro k hk
      ring
    _ = dc j := by simp [hInv,Matrix.one_apply]

#print axioms lower_christoffel_metric_identity
#print axioms levi_civita_jet_metric_compatible
#print axioms levi_civita_jet_torsion_free
#print axioms covariant_pure_trace_jet
#print axioms divergence_pure_trace_jet
end
end ChatgptAudit
