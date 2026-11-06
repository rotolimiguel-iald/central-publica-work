-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_020 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ConstructedHorizonPencil

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

variable (U : Set Coordinate4) (hU : IsOpen U) (A B : TensorField4)
  (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
  (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
  (T : TensorField4) (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
  (rate eta : ℝ)

def ConstructedClausiusAt (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) : Prop :=
  let P := localEquilibriumScreen U hU A B hAB hBA hA hB p v hp hv hn
  let hg := frame_metric_smooth U A hA
  Tendsto (fun t => horizonBalancePrimitive rate eta
    (inducedArea (frameMetricField A) P.curve P.screen.vectors)
    (constructedHeat P T rate hU hg hT) t/t^2) (𝓝[<] 0) (𝓝 0)

theorem constructed_clausius_at_iff (hrate : rate≠0) (heta : eta≠0)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    ConstructedClausiusAt U hU A B hAB hBA hA hB T hT rate eta p v hp hv hn ↔
      tensorQuad (coordinateRicci (frameLeviCivita A B) p) v=
        (2*Real.pi/eta)*tensorQuad (T p) v := by
  let P := localEquilibriumScreen U hU A B hAB hBA hA hB p v hp hv hn
  have hg := frame_metric_smooth U A hA
  have hG : SmoothConnectionOn U (frameLeviCivita A B) :=
    levi_civita_field_smooth U hU (frameMetricField A) (inverseFrameMetricField B)
      hg (inverse_frame_metric_smooth U B hB)
  have ht := levi_civita_field_torsion_free U hU (frameMetricField A) (inverseFrameMetricField B)
    (fun x _ => frame_metric_symmetric A x)
  exact constructed_clausius_iff_null_balance P T rate eta hU hg hG hT (ht p hp) hrate heta

theorem einstein_from_constructed_clausius (hconn : IsPreconnected U)
    (hrate : rate≠0) (heta : eta≠0)
    (hsT : ∀ x∈U, (T x)ᵀ=T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (inverseFrameMetricField B)
      (frameLeviCivita A B) T x j=0)
    (hbalance : ∀ p (hp : p∈U) v (hv : v≠0) (hn : tensorQuad (frameMetricField A p) v=0),
      ConstructedClausiusAt U hU A B hAB hBA hA hB T hT rate eta p v hp hv hn) :
    ∃ cosmological : ℝ, ∀ x∈U,
      frameEinsteinTensor A B x+cosmological • frameMetricField A x=(2*Real.pi/eta) • T x := by
  apply geometric_area_einstein_reconstruction U hU hconn A B T eta heta
    hAB hBA hA hB hT hsT hdT
  intro p hp v hv hn
  let P := localEquilibriumScreen U hU A B hAB hBA hA hB p v hp hv hn
  exact ⟨horizonPencilFromScreen P T rate eta hU (frame_metric_smooth U A hA) hT hrate
    (hbalance p hp v hv hn)⟩

#print axioms ConstructedClausiusAt
#print axioms constructed_clausius_at_iff
#print axioms einstein_from_constructed_clausius
end
end ChatgptAudit.Flow020
