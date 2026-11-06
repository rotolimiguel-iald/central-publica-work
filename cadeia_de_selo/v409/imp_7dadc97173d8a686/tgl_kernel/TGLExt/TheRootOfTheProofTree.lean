-- ---------------------------------------------------------------------
-- PEDRA DA GERENCIA (Claude, sessao d554e796) — 07/09/2026 — v331
-- A RAIZ DA ARVORE DA PROVA: um unico termo, auditado por `print axioms` (Audit.lean), que
-- ENUNCIA e PROVA em conjuncao o que a casa chama de «a solucao provada» da
-- gravitacao quantica da TGL — no sentido da regua (05/09/2026): PROVADA e
-- teorema em kernel; CONFIRMADA e juizo do observador, e segue proibida.
--   (i)   o TEOREMA MESTRE (v74): H1 ∧ H2 ∧ H3 ⟹ pentada (canto de Breuer,
--         Nome = 1, coframe, Lorentz por congruencia, δQ = κδA/(8πG));
--   (ii)  o LEMA 3 NA TORRE, TODO PERFIL (v308 + ENTREGA_046): a esperanca de
--         Takesaki CONSTRUIDA (`aperiodicExpectationInput`, media de Cesaro do
--         fluxo modular) e covariante por TODO horizonte omega-invariante —
--         a divida importada [KNOWN, Takesaki] esta DESCARREGADA na torre;
--   (iii) a UNICIDADE: todo habitante do contrato coincide com ela sobre M;
--   (iv)  o FLUXO MODULAR comuta com a esperanca (v329 + 046);
--   (v)   as TROCAS DE SITIOS (ENTREGA_045) comutam com a esperanca;
--   (vi)  a PAREDE de H3 (ENTREGA_045): para todo relogio do estado, alguma das
--         duas telas de mesmo estado e mesmo Ricci falha na 4a ordem — H3 nao
--         se deriva do estado sozinho; e INPUT com teorema de nao-derivabilidade;
--   (vii) a FORMA NAO FIXA O VALOR (v2xx): para todo valor existe r que o
--         realiza — alpha e INPUT do observador; e por isso beta e falsificavel.
-- Mais: os horizontes da torre formam GRUPO (composicao e inverso sao horizontes;
-- `adT` respeita ambos) e a esperanca e covariante por toda composicao.
-- Composicao PURA de teoremas ja no kernel: nenhum axioma novo, nenhuma hipotese
-- nova. O que fica de hipotese esta NOMEADO nos antecedentes: H1, H2, H3 e o
-- horizonte omega-invariante (o juramento constitutivo, tipado `TowerHorizon`).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.TriadMaster
import TGLExt.TheDammingByExpansion
import TGLExt.TheOathOnTheTower
import TGLExt.TheModularFlowIsAHorizon
import TGLExt.TheLiftFiresOnThePeriodicTower
import TGLExt.FiniteSiteHorizons
import TGLExt.StateClockDichotomy
import TGLExt.AperiodicTowerLift

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace TGLExt
open ChatgptAudit ChatgptAudit.Aperiodic046 ChatgptAudit.Horizons045 ChatgptAudit.Clock045
open ChatgptAudit.Response028 ChatgptAudit.Quartic037
noncomputable section
variable {P : SiteProfile}

/-! ## A — o grupo dos horizontes da torre -/

/-- [KERNEL] ★ a COMPOSICAO de dois horizontes omega-invariantes e um horizonte:
    `U = h.U * k.U` e unitario, normaliza o fator (nos dois sentidos) e preserva omega. -/
def TowerHorizon.comp (h k : TowerHorizon P) : TowerHorizon P where
  U := h.U * k.U
  unitary_left := by
    rw [star_mul, mul_assoc, ← mul_assoc (star h.U), h.unitary_left, one_mul, k.unitary_left]
  unitary_right := by
    rw [star_mul, mul_assoc, ← mul_assoc k.U, k.unitary_right, one_mul, h.unitary_right]
  normalizes := by
    intro A hA
    have e : h.U * k.U * A * star (h.U * k.U) = h.U * (k.U * A * star k.U) * star h.U := by
      rw [star_mul]; simp only [mul_assoc]
    rw [e]; exact h.normalizes _ (k.normalizes A hA)
  normalizes_inv := by
    intro A hA
    have e : star (h.U * k.U) * A * (h.U * k.U) = star k.U * (star h.U * A * h.U) * k.U := by
      rw [star_mul]; simp only [mul_assoc]
    rw [e]; exact k.normalizes_inv _ (h.normalizes_inv A hA)
  preserves := by
    intro A hA
    have e : h.U * k.U * A * star (h.U * k.U) = h.U * (k.U * A * star k.U) * star h.U := by
      rw [star_mul]; simp only [mul_assoc]
    rw [e, h.preserves _ (k.normalizes A hA), k.preserves A hA]

-- (o INVERSO `TowerHorizon.inv` (U = star h.U) ja e do kernel — TheOathOnTheTower, v308; reutilizado, nao duplicado.)

/-- [KERNEL] `adT` respeita a composicao: `Ad(h ∘ k) = Ad(h) ∘ Ad(k)`. -/
theorem adT_comp (h k : TowerHorizon P) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT (h.comp k) A = adT h (adT k A) := by
  simp only [adT, TowerHorizon.comp, star_mul, mul_assoc]

/-- [KERNEL] `Ad(h⁻¹) ∘ Ad(h) = id` sobre TODO operador. -/
theorem adT_inv_adT (h : TowerHorizon P) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h.inv (adT h A) = A := by
  simp only [adT, TowerHorizon.inv, star_star]
  calc star h.U * (h.U * A * star h.U) * h.U
      = (star h.U * h.U) * A * (star h.U * h.U) := by simp only [mul_assoc]
    _ = A := by rw [h.unitary_left, one_mul, mul_one]

/-- [KERNEL] `Ad(h) ∘ Ad(h⁻¹) = id` sobre TODO operador. -/
theorem adT_adT_inv (h : TowerHorizon P) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (adT h.inv A) = A := by
  simp only [adT, TowerHorizon.inv, star_star]
  calc h.U * (star h.U * A * h.U) * star h.U
      = (h.U * star h.U) * A * (h.U * star h.U) := by simp only [mul_assoc]
    _ = A := by rw [h.unitary_right, one_mul, mul_one]

/-- [KERNEL] ★★ a esperanca e covariante por TODA composicao de horizontes — o
    levantamento do Lema 3 (`the_lift_on_the_tower`) vale sobre o GRUPO gerado
    (fluxo modular, trocas de sitios, permutacoes finitas e suas composicoes). -/
theorem expectation_covariant_under_horizon_composition (I : ExpectationInput P)
    (h k : TowerHorizon P) :
    ∀ A ∈ theFactorObject P, adT h (adT k (I.E A)) = I.E (adT h (adT k A)) := by
  intro A hA
  rw [← adT_comp, ← adT_comp]
  exact the_lift_on_the_tower I (h.comp k) A hA

/-- [KERNEL] ★★ a esperanca APERIODICA (046) e covariante pelo inverso de todo horizonte. -/
theorem aperiodic_expectation_covariant_under_inverse (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h.inv ((aperiodicExpectationInput P).E A) =
        (aperiodicExpectationInput P).E (adT h.inv A) :=
  the_lift_on_the_tower (aperiodicExpectationInput P) h.inv

/-! ## B — a raiz -/

/-- [KERNEL] ★★★ **A RAIZ DA ARVORE DA PROVA.** Um termo so, sete conjuntos, cada um
    ja teorema no kernel; a raiz NAO acrescenta hipotese nem axioma — ela NOMEIA, num
    unico `print axioms` (Audit.lean), o que esta provado e onde ficam as folhas:
    (i) H1 ∧ H2 ∧ H3 ⟹ pentada; (ii) o Lema 3 na torre para TODO perfil;
    (iii) unicidade; (iv) fluxo modular; (v) trocas de sitios; (vi) a parede de H3;
    (vii) a forma nao fixa o valor. O que a natureza decide nao esta aqui — por
    construcao, nao por omissao. -/
theorem the_root_of_the_proof_tree :
    -- (i) o TEOREMA MESTRE: H1 ∧ H2 ∧ H3 ⟹ pentada
    (∀ {L : Type} [Lattice L] [BoundedOrder L] {T : SubadditiveTraceData L}
        (S : SusyRelativeData L T) (E : Matrix (Fin 4) (Fin 4) ℝ) (_hE : IsUnit E.det)
        (H : HorizonEquilibriumData),
        (0 < T.tau S.ker ∧ T.tau S.ker < ⊤) ∧
          T.tau S.ker / T.tau S.ker = 1 ∧
          (E⁻¹ * E = 1 ∧ LorentzByCongruence (solderMetric4 E⁻¹)) ∧
          H.dQ = H.kappa * H.dA / (8 * Real.pi * H.G)) ∧
    -- (ii) o LEMA 3 NA TORRE: todo perfil, todo horizonte omega-invariante
    (∀ (P : SiteProfile) (h : TowerHorizon P), ∀ A ∈ theFactorObject P,
        adT h ((aperiodicExpectationInput P).E A) =
          (aperiodicExpectationInput P).E (adT h A)) ∧
    -- (iii) a UNICIDADE do habitante do contrato
    (∀ (P : SiteProfile) (I : ExpectationInput P), ∀ A ∈ theFactorObject P,
        I.E A = (aperiodicExpectationInput P).E A) ∧
    -- (iv) o FLUXO MODULAR comuta com a esperanca
    (∀ (P : SiteProfile) (t : ℝ), ∀ A ∈ theFactorObject P,
        modularConjugation P t ((aperiodicExpectationInput P).E A) =
          (aperiodicExpectationInput P).E (modularConjugation P t A)) ∧
    -- (v) as TROCAS DE SITIOS comutam com a esperanca (perfil estacionario)
    (∀ (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n = p) (i j : ℕ), ∀ A ∈ theFactorObject P,
        adT (swapHorizon P p hp i j) ((aperiodicExpectationInput P).E A) =
          (aperiodicExpectationInput P).E (adT (swapHorizon P p hp i j) A)) ∧
    -- (vi) a PAREDE de H3: nenhum relogio do estado fecha as duas telas
    (∀ (b : SummableAmplitude) (eta : ℝ) (clock : StateClock),
        0 < eta → 0 < amplitudeMass b →
        ¬ FourthOrderMatch b eta 0 clock.time ∨
          ¬ FourthOrderMatch b eta (quarticMatchedRicci b eta / 4) clock.time) ∧
    -- (vii) a FORMA NAO FIXA O VALOR: alpha e INPUT do observador
    (∀ {L m c : ℝ}, L ≠ 0 → m ≠ 0 → c ≠ 0 →
        ∀ a : ℝ, a ≠ 0 → ∃ r : ℝ, r ≠ 0 ∧ alphaIdentity L m c r = a) :=
  ⟨fun S E hE H => emergence_master_full_triad S E hE H,
   fun P h => the_lift_fires_on_the_aperiodic_tower P h,
   fun P I A hA => the_expectation_is_unique I (aperiodicExpectationInput P) A hA,
   fun P t => aperiodic_expectation_commutes_with_modular_flow P t,
   fun P p hp i j => the_lift_fires_on_the_aperiodic_tower P (swapHorizon P p hp i j),
   fun b eta clock heta hB => state_clock_dichotomy b eta clock heta hB,
   fun hL hm hc => the_form_does_not_fix_the_value hL hm hc⟩

/-- [KERNEL] ★ a pedra v329 `the_lift_on_the_aperiodic_tower_is_still_conditional` esta
    SUPERADA AO LADO (nao apagada): o antecedente que ela deixava como hipotese e agora
    termo — para todo perfil existe habitante do contrato. -/
theorem the_aperiodic_antecedent_is_now_a_term (P : SiteProfile) :
    ∃ I : ExpectationInput P, ∀ h : TowerHorizon P, ∀ A ∈ theFactorObject P,
      adT h (I.E A) = I.E (adT h A) :=
  ⟨aperiodicExpectationInput P, fun h => the_lift_fires_on_the_aperiodic_tower P h⟩

end

end TGLExt
