-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_049 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.BoundedGraphOperator
import TGLExt.ClosedAntilinearStandardSubspace

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Continuous049
open Complex ClosedSubmodule
noncomputable section
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The anti-linear operator JT on the exact domain of the graph operator T. -/
def boundedGraphTomita (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (boundedGraphOperator A B hAi).domain →ₛₗ[starRingEnd ℂ] H :=
  J.toLinearEquiv.toLinearMap.comp (boundedGraphOperator A B hAi).toFun

theorem bounded_graph_tomita_apply (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J x = J (B (boundedGraphParameter A hAi x)) := rfl

theorem bounded_graph_tomita_lift (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJB : ∀ h, J (B h) = A (J h)) (h : H) :
    boundedGraphTomita A B hAi J (boundedGraphLift A B hAi h) = A (J h) := by
  rw [bounded_graph_tomita_apply, bounded_graph_parameter_lift, hJB]

theorem bounded_graph_tomita_maps_domain (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJB : ∀ h, J (B h) = A (J h))
    (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J x ∈ (boundedGraphOperator A B hAi).domain := by
  refine ⟨J (boundedGraphParameter A hAi x), ?_⟩
  rw [bounded_graph_tomita_apply, hJB]
  rfl

theorem bounded_graph_tomita_involutive (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (hJB : ∀ h, J (B h) = A (J h)) (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J
      ⟨boundedGraphTomita A B hAi J x, bounded_graph_tomita_maps_domain A B hAi J hJB x⟩
        = (x : H) := by
  have hy : (⟨boundedGraphTomita A B hAi J x,
      bounded_graph_tomita_maps_domain A B hAi J hJB x⟩ :
      (boundedGraphOperator A B hAi).domain) =
      boundedGraphLift A B hAi (J (boundedGraphParameter A hAi x)) := by
    apply Subtype.ext
    exact hJB (boundedGraphParameter A hAi x)
  rw [hy, bounded_graph_tomita_lift A B hAi J hJB, hJ, bounded_graph_parameter_apply]

theorem bounded_graph_tomita_closed (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) :
    IsClosed (Set.range (fun x : (boundedGraphOperator A B hAi).domain =>
      ((x : H), boundedGraphTomita A B hAi J x))) := by
  have heq : Set.range (fun x : (boundedGraphOperator A B hAi).domain =>
      ((x : H), boundedGraphTomita A B hAi J x)) =
      (fun p : H × H => (p.1, J p.2)) ⁻¹'
        ((boundedGraphOperator A B hAi).graph : Set (H × H)) := by
    ext p
    constructor
    · rintro ⟨x, rfl⟩
      change ((x : H), J (J (boundedGraphOperator A B hAi x))) ∈
        (boundedGraphOperator A B hAi).graph
      rw [hJ]
      exact (boundedGraphOperator A B hAi).mem_graph x
    · intro hp
      change (p.1, J p.2) ∈ (boundedGraphOperator A B hAi).graph at hp
      rw [LinearPMap.mem_graph_iff] at hp
      obtain ⟨x, hx, hy⟩ := hp
      refine ⟨x, Prod.ext hx ?_⟩
      change J (boundedGraphOperator A B hAi x) = p.2
      rw [hy, hJ]
  rw [heq]
  exact (bounded_graph_closed A B hAi hcomm hsum).preimage
    (continuous_fst.prodMk (J.continuous.comp continuous_snd))

theorem bounded_graph_J_tomita (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : (boundedGraphOperator A B hAi).domain) :
    J (boundedGraphTomita A B hAi J x) = boundedGraphOperator A B hAi x :=
  hJ (boundedGraphOperator A B hAi x)

/-- A concrete standard subspace obtained from the bounded graph data. -/
def boundedGraphStandardSubspace [CompleteSpace H]
    (A B : H →L[ℂ] H) (hAi : Function.Injective A) (hA : IsSelfAdjoint A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (hJB : ∀ h, J (B h) = A (J h)) : StandardSubspace H :=
  closedAntilinearStandardSubspace
    (boundedGraphOperator A B hAi).domain (boundedGraphTomita A B hAi J)
    (bounded_graph_tomita_closed A B hAi hcomm hsum J hJ)
    (bounded_graph_tomita_maps_domain A B hAi J hJB)
    (bounded_graph_tomita_involutive A B hAi J hJ hJB)
    (bounded_graph_domain_dense A B hAi hA)

#print axioms boundedGraphTomita
#print axioms bounded_graph_tomita_apply
#print axioms bounded_graph_tomita_lift
#print axioms bounded_graph_tomita_maps_domain
#print axioms bounded_graph_tomita_involutive
#print axioms bounded_graph_tomita_closed
#print axioms bounded_graph_J_tomita
#print axioms boundedGraphStandardSubspace

end
end ChatgptAudit.Continuous049
