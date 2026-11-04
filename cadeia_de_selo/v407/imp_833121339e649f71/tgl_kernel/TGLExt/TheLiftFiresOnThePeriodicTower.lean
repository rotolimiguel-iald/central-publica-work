-- ---------------------------------------------------------------------
-- PEDRA DA GERENCIA (Claude, sessao d554e796) — 06/09/2026 — v329
-- O LEVANTAMENTO DISPARA NA TORRE PERIODICA: a implicacao do Lema 3 no continuo
-- (`the_lift_on_the_tower`, v308: contrato da esperanca + horizonte omega-invariante
-- ⟹ esperanca COVARIANTE sobre M) ganha ANTECEDENTE CONSTRUIDO — o habitante
-- `periodicExpectationInput` da bancada (ENTREGA_007, v317) para todo perfil com
-- periodo comum, e `stationaryExpectationInput` para perfil constante nao tracial;
-- e o habitante tracial `tracialExpectationInput` (ENTREGA_006, v316) em w = 1/2.
-- Composicao PURA de teoremas ja no kernel: nenhum axioma novo, nenhuma hipotese
-- nova. O que fica de hipotese e SO o horizonte omega-invariante (o juramento
-- constitutivo do operador, 20/07/2026, tipado como `TowerHorizon`) e a
-- periodicidade do perfil (a esperanca APERIODICA segue [OPEN]).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.PeriodicCentralizerExpectation
import TGLExt.TracialCentralizerExpectation
import TGLExt.TheOathOnTheTower

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace TGLExt
open ChatgptAudit
noncomputable section
variable {P : SiteProfile}

/-- [KERNEL] ★★★ **O LEVANTAMENTO DISPARA na torre PERIODICA**: para todo perfil com
    periodo comum `T` das fases locais e todo horizonte omega-invariante `h`, a esperanca
    de Takesaki CONSTRUIDA (`periodicExpectationInput`) e covariante sobre o fator:
    `Ad(h) ∘ E = E ∘ Ad(h)`. Antes desta pedra o antecedente `I : ExpectationInput P` de
    `the_lift_on_the_tower` era hipotese; agora e termo. -/
theorem the_lift_fires_on_the_periodic_tower (T : ℝ) (hT : 0 < T)
    (hp : LocalPhasePeriod P T) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h ((periodicExpectationInput P T hT hp).E A)
        = (periodicExpectationInput P T hT hp).E (adT h A) :=
  the_lift_on_the_tower (periodicExpectationInput P T hT hp) h

/-- [KERNEL] ★★ o caso ESTACIONARIO nao tracial (`w(n) = p`, `p ≠ 1/2`): o periodo e
    `2π/|log p − log(1−p)|` (o invariante T do fator de Powers, agora sem importacao). -/
theorem the_lift_fires_on_the_stationary_tower (p : ℝ) (hp : ∀ n, P.w n = p)
    (hne : p ≠ 1/2) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h ((stationaryExpectationInput P p hp hne).E A)
        = (stationaryExpectationInput P p hp hne).E (adT h A) :=
  the_lift_on_the_tower (stationaryExpectationInput P p hp hne) h

/-- [KERNEL] ★ o caso TRACIAL (`w = 1/2`): `E = id`, a covariancia e imediata — registrada
    para que os TRES habitantes construidos estejam sob o mesmo enunciado. -/
theorem the_lift_fires_on_the_tracial_tower (hp : ∀ n, P.w n = 1/2) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      adT h ((tracialExpectationInput P hp).E A)
        = (tracialExpectationInput P hp).E (adT h A) :=
  the_lift_on_the_tower (tracialExpectationInput P hp) h

/-- [KERNEL] ★★ **unicidade + covariancia**: QUALQUER habitante do contrato coincide com o
    periodico sobre M (`the_expectation_is_unique`) e, portanto, e covariante por todo
    horizonte — nao ha esperanca «alternativa» que escape ao levantamento. -/
theorem every_expectation_on_the_periodic_tower_is_covariant (T : ℝ) (hT : 0 < T)
    (hp : LocalPhasePeriod P T) (I : ExpectationInput P) (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P,
      I.E A = (periodicExpectationInput P T hT hp).E A ∧
        adT h (I.E A) = I.E (adT h A) :=
  fun A hA => ⟨the_expectation_is_unique I (periodicExpectationInput P T hT hp) A hA,
    the_lift_on_the_tower I h A hA⟩

/-- [KERNEL] ★ o que NAO se prova aqui, dito como enunciado condicional: para um perfil
    SEM periodo comum o antecedente segue hipotese — a implicacao permanece a mesma. -/
theorem the_lift_on_the_aperiodic_tower_is_still_conditional (I : ExpectationInput P)
    (h : TowerHorizon P) :
    ∀ A ∈ theFactorObject P, adT h (I.E A) = I.E (adT h A) :=
  the_lift_on_the_tower I h

/-- [KERNEL] ★★ **o funcional de resposta transporta covariante na torre** (a forma do G_μν global
    condicional, agora com a esperanca CONSTRUIDA): se a fonte `K` preserva M e transporta covariante
    por `h`, entao `E ∘ K` transporta covariante — o corolario `response_covariant` da face finita
    (v143) sobe a torre para todo horizonte omega-invariante e todo perfil periodico. -/
theorem response_covariant_on_the_periodic_tower (T : ℝ) (hT : 0 < T)
    (hp : LocalPhasePeriod P T) (h : TowerHorizon P)
    (K : (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hKmem : ∀ A ∈ theFactorObject P, K A ∈ theFactorObject P)
    (hKcov : ∀ A ∈ theFactorObject P, adT h (K A) = K (adT h A)) :
    ∀ A ∈ theFactorObject P,
      adT h ((periodicExpectationInput P T hT hp).E (K A))
        = (periodicExpectationInput P T hT hp).E (K (adT h A)) := by
  intro A hA
  rw [the_lift_on_the_tower (periodicExpectationInput P T hT hp) h (K A) (hKmem A hA), hKcov A hA]

#print axioms response_covariant_on_the_periodic_tower
#print axioms the_lift_fires_on_the_periodic_tower
#print axioms the_lift_fires_on_the_stationary_tower
#print axioms the_lift_fires_on_the_tracial_tower
#print axioms every_expectation_on_the_periodic_tower_is_covariant
#print axioms the_lift_on_the_aperiodic_tower_is_still_conditional
end
end TGLExt
