-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_018 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ConstructedNullCongruence

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem constructed_congruence_transported_screen (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    ∃ N : Set Coordinate4, IsOpen N ∧ N⊆U ∧ p∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V p=v ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad (frameMetricField A x) (V x)=0) ∧
        EqOn (vectorAcceleration (frameLeviCivita A B) V) (fun _ => 0) N ∧
        ∃ curve : ℝ → Coordinate4, curve 0=p ∧ HasDerivAt curve v 0 ∧
          ∃ S : GeometricScreenAlong (frameMetricField A) (frameLeviCivita A B) V curve,
            screenGram (frameMetricField A p) (S.vectors 0)=-1 ∧
            ∀ᶠ t in 𝓝[<] (0:ℝ), HasDerivAt (inducedArea (frameMetricField A) curve S.vectors)
              (vectorExpansion (frameLeviCivita A B) V (curve t)*
                inducedArea (frameMetricField A) curve S.vectors t) t := by
  obtain ⟨N,hN,hNU,hpN,V,hV,hVp,hvN,hnN,hgeo⟩ :=
    local_levi_civita_null_congruence U hU A B hAB hBA hA hB p v hp hv hn
  refine ⟨N,hN,hNU,hpN,V,hV,hVp,hvN,hnN,hgeo,?_⟩
  obtain ⟨curve,hcp,hcv,S,hGram,hArea⟩ :=
    local_levi_civita_transported_screen N hN A B V
      (fun x hx => hAB x (hNU hx)) (fun x hx => hBA x (hNU hx))
      (fun a b => (hA a b).mono hNU) (fun a b => (hB a b).mono hNU)
      hV hnN hgeo p hpN (hvN p hpN)
  exact ⟨curve,hcp,by simpa only [hVp] using hcv,S,hGram,hArea⟩

#print axioms constructed_congruence_transported_screen
end
end ChatgptAudit.Flow018
