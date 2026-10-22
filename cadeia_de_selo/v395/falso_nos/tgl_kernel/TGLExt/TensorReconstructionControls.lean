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
import TGLExt.LorentzMetricField

set_option autoImplicit false
namespace ChatgptAudit
open Matrix TGLExt
noncomputable section

def linearTraceField (x : Coordinate4) : Tensor4 := x 0 • eta4

theorem linear_trace_annihilates_null_cone (x : Coordinate4) (v : SpacetimeVector)
    (hv : tensorQuad eta4 v=0) : tensorQuad (linearTraceField x) v=0 := by
  have he : tensorQuad (linearTraceField x) v=x 0*tensorQuad eta4 v := by
    simp only [linearTraceField,tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  rw [he,hv,mul_zero]

theorem linear_trace_has_no_constant_coefficient :
    ¬ ∃ c : ℝ, ∀ x : Coordinate4, linearTraceField x=c • eta4 := by
  rintro ⟨c,hc⟩
  have h0 := congrArg (fun A : Tensor4 => A 0 0) (hc 0)
  have h1 := congrArg (fun A : Tensor4 => A 0 0) (hc (Pi.single 0 1))
  norm_num [linearTraceField,eta4,Pi.single_apply] at h0 h1
  linarith

theorem linear_trace_divergence (x : Coordinate4) (j : Fin 4) :
    tensorFieldDivergence (fun _ => eta4) (fun _ _ => 0) linearTraceField x j =
      (Pi.single j (1:ℝ) : Coordinate4) 0 := by
  have hf : DifferentiableAt ℝ (fun y : Coordinate4 => y 0) x :=
    (hasFDerivAt_apply 0 x).differentiableAt
  have hg : ∀ i k : Fin 4, DifferentiableAt ℝ (fun _ : Coordinate4 => eta4 i k) x :=
    fun i k => differentiableAt_const _
  have hm : ∀ i, covariantTensorJet eta4 (tensorFieldJet (fun _ => eta4) x) (fun _ => 0) i=0 := by
    intro i
    ext k l
    simp [covariantTensorJet,tensorFieldJet,coordinatePartial]
  change tensorFieldDivergence (fun _ => eta4) (fun _ _ => 0)
    (fun y => y 0 • eta4) x j = _
  rw [pure_trace_field_divergence (fun _ => eta4) (fun _ => eta4) (fun _ _ => 0)
    (fun y => y 0) x hf hg eta4_mul_self hm j,coordinatePartial,
    (hasFDerivAt_apply 0 x).fderiv]
  rfl

#print axioms linear_trace_annihilates_null_cone
#print axioms linear_trace_has_no_constant_coefficient
#print axioms linear_trace_divergence
end
end ChatgptAudit
