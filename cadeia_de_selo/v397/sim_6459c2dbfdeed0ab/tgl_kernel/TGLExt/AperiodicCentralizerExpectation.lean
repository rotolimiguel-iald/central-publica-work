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
import TGLExt.AperiodicVectorAverage
import TGLExt.AperiodicAveragePrefix
import TGLExt.TracialCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Filter
open scoped Topology

noncomputable section

/-- Choose the constructed strong limit on the factor; the contract ignores values outside it. -/
def aperiodicExpectation (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P := by
  classical
  exact if hA : A ∈ theFactorObject P then
    Classical.choose (aperiodic_average_operator P A hA)
  else 0

/-- Membership, norm bound, and strong convergence are proved by the operator construction. -/
theorem aperiodic_expectation_spec (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    aperiodicExpectation P A ∈ theFactorObject P ∧
      ‖aperiodicExpectation P A‖ ≤ ‖A‖ ∧
      ∀ v, Tendsto
        (fun n : ℕ => periodAverage P ((n : ℝ) + 1) (by positivity) A v)
        atTop (𝓝 (aperiodicExpectation P A v)) := by
  simpa only [aperiodicExpectation, dif_pos hA] using
    Classical.choose_spec (aperiodic_average_operator P A hA)

/-- The selected limit has the local pinching as every finite prefix. -/
theorem aperiodic_expectation_prefix (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    towerExpectation P N (aperiodicExpectation P A) =
      towerPi P (specExpect (towerW P N) (expectationMatrix P N A)) :=
  aperiodic_average_prefix_of_limit P N A (aperiodicExpectation P A)
    ((aperiodic_expectation_spec P A hA).2.2 (hOmega P))

/-- The limit lies in the global centralizer, without a common local phase period. -/
theorem aperiodic_expectation_into (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    aperiodicExpectation P A ∈ omegaCentralizer P := by
  apply centralizer_from_expectations _ (aperiodic_expectation_spec P A hA).1
  intro N
  rw [aperiodic_expectation_prefix P N A hA]
  exact pinching_into_global_centralizer _ _

/-- Every element of the centralizer is fixed by the constructed map. -/
theorem aperiodic_expectation_fixes (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ omegaCentralizer P) :
    aperiodicExpectation P A = A := by
  have he (N : ℕ) :
      towerExpectation P N (aperiodicExpectation P A) = towerExpectation P N A := by
    rw [aperiodic_expectation_prefix P N A hA.1,
      pinching_fixes_global_local N _
        (expectation_of_centralizer_is_centralizer N A hA)]
    rfl
  apply factor_eq_of_omega (aperiodic_expectation_spec P A hA.1).1 hA.1
  have ht := expectation_omega_limit (aperiodicExpectation P A)
  simp only [he] at ht
  exact tendsto_nhds_unique ht (expectation_omega_limit A)

/-- The finite pinching orthogonalities pass to the GNS limit. -/
theorem aperiodic_expectation_ortho (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ omegaCentralizer P) :
    omegaState P (star B * (A - aperiodicExpectation P A)) = 0 := by
  have hn (N : ℕ) : inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P)) = 0 := by
    have h := pinching_global_ortho N (expectationMatrix P N A)
      (towerExpectation P N B) (expectation_of_centralizer_is_centralizer N B hB)
    rw [omega_product_inner, star_star] at h
    rw [aperiodic_expectation_prefix P N A hA]
    exact h
  have ht : Tendsto (fun N => inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P)))
      atTop (𝓝 (inner ℂ (B (hOmega P))
        (A (hOmega P) - aperiodicExpectation P A (hOmega P)))) :=
    (expectation_omega_limit B).inner
      ((expectation_omega_limit A).sub
        (expectation_omega_limit (aperiodicExpectation P A)))
  have he : (fun N => inner ℂ (towerExpectation P N B (hOmega P))
      (towerExpectation P N A (hOmega P) -
        towerExpectation P N (aperiodicExpectation P A) (hOmega P))) =
      (fun _ : ℕ => (0 : ℂ)) := funext hn
  rw [he] at ht
  have hz := tendsto_nhds_unique ht tendsto_const_nhds
  rw [omega_product_inner, star_star]
  exact hz

/-- A constructed inhabitant for every admissible profile, including aperiodic ones. -/
def aperiodicExpectationInput (P : SiteProfile) : ExpectationInput P where
  E := aperiodicExpectation P
  into := aperiodic_expectation_into P
  fixes := aperiodic_expectation_fixes P
  ortho := fun A hA B hB => aperiodic_expectation_ortho P A B hA hB

theorem aperiodic_contract_inhabited (P : SiteProfile) : Nonempty (ExpectationInput P) :=
  ⟨aperiodicExpectationInput P⟩

theorem aperiodic_expectation_contractive (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖(aperiodicExpectationInput P).E A‖ ≤ ‖A‖ :=
  (aperiodic_expectation_spec P A hA).2.1

theorem aperiodic_expectation_idempotent (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    (aperiodicExpectationInput P).E ((aperiodicExpectationInput P).E A) =
      (aperiodicExpectationInput P).E A :=
  (aperiodicExpectationInput P).fixes _ ((aperiodicExpectationInput P).into A hA)

#print axioms aperiodicExpectation
#print axioms aperiodic_expectation_spec
#print axioms aperiodic_expectation_prefix
#print axioms aperiodic_expectation_into
#print axioms aperiodic_expectation_fixes
#print axioms aperiodic_expectation_ortho
#print axioms aperiodicExpectationInput
#print axioms aperiodic_contract_inhabited
#print axioms aperiodic_expectation_contractive
#print axioms aperiodic_expectation_idempotent

end

end ChatgptAudit.Aperiodic046
