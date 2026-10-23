-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_046 (06-07/09/2026), transposta em 07/09/2026
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
import TGLExt.AperiodicCentralizerExpectation
import TGLExt.TheLiftFiresOnThePeriodicTower
import TGLExt.TheModularFlowIsAHorizon

set_option autoImplicit false

namespace ChatgptAudit.Aperiodic046

open TGLExt

noncomputable section

/-- The lift now has a constructed expectation for every admissible profile. -/
theorem the_lift_fires_on_the_aperiodic_tower (P : SiteProfile) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h ((aperiodicExpectationInput P).E A) =
        (aperiodicExpectationInput P).E (adT h A) :=
  the_lift_on_the_tower (aperiodicExpectationInput P) h

/-- Every other inhabitant agrees on the factor and has the same covariance. -/
theorem every_expectation_on_the_general_tower_is_covariant (P : SiteProfile)
    (I : ExpectationInput P) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      I.E A = (aperiodicExpectationInput P).E A ∧
        adT h (I.E A) = I.E (adT h A) :=
  fun A hA => ⟨the_expectation_is_unique I (aperiodicExpectationInput P) A hA,
    the_lift_on_the_tower I h A hA⟩

theorem aperiodic_expectation_agrees_periodic (P : SiteProfile)
    (T : ℝ) (hT : 0 < T) (hp : LocalPhasePeriod P T)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E A = (periodicExpectationInput P T hT hp).E A :=
  the_expectation_is_unique (aperiodicExpectationInput P)
    (periodicExpectationInput P T hT hp) A hA

theorem aperiodic_expectation_agrees_tracial (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E A = (tracialExpectationInput P hp).E A :=
  the_expectation_is_unique (aperiodicExpectationInput P) (tracialExpectationInput P hp) A hA

theorem aperiodic_expectation_commutes_with_modular_flow (P : SiteProfile) (t : ℝ) :
    ∀ A ∈ theFactorObject P,
      modularConjugation P t ((aperiodicExpectationInput P).E A) =
        (aperiodicExpectationInput P).E (modularConjugation P t A) :=
  every_expectation_commutes_with_modular_flow (aperiodicExpectationInput P) t

/-- The response composition remains conditional on a factor-preserving covariant source. -/
theorem response_covariant_on_the_general_tower (P : SiteProfile) (h : TowerHorizon P)
    (K : (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hKmem : ∀ A ∈ theFactorObject P, K A ∈ theFactorObject P)
    (hKcov : ∀ A ∈ theFactorObject P, adT h (K A) = K (adT h A)) :
    ∀ A ∈ theFactorObject P,
      adT h ((aperiodicExpectationInput P).E (K A)) =
        (aperiodicExpectationInput P).E (K (adT h A)) := by
  intro A hA
  rw [the_lift_on_the_tower (aperiodicExpectationInput P) h (K A) (hKmem A hA),
    hKcov A hA]

#print axioms the_lift_fires_on_the_aperiodic_tower
#print axioms every_expectation_on_the_general_tower_is_covariant
#print axioms aperiodic_expectation_agrees_periodic
#print axioms aperiodic_expectation_agrees_tracial
#print axioms aperiodic_expectation_commutes_with_modular_flow
#print axioms response_covariant_on_the_general_tower

end

end ChatgptAudit.Aperiodic046
