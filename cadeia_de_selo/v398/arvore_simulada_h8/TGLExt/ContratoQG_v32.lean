import TGLExt.ContratoQG_v31_Teoremas
import TGLExt.O16.ContentContractProposal
import TGLExt.TheGravitonIsTheConjugatedPhase

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false

/-!
# CONTRATO DE TIPO v3.2 DE H2 / H3 / IMPORT-H3 — A LUZ   [TGLExt — v372, pedra da gerência (26/09/2026)]

Ratificação: as decisões do operador de 26/09/2026 (Q1 «o campo é a luz; o gráviton é a forma conjugada»,
Q2 «nome sem peso é mentira» ⟹ `peso_do_nome`, Q3 N₀/T₀, Q4 «o mesmo nome … pelo conteúdo», Q5 «autorizo a
máquina a reconhecer a prova»), verbatim no Atlas §X. Tipagem: a proposta `ORDEM016.ContractV32Proposal`
da bancada (`FECHAMENTO_PARCIAL_016`, P3), REESCRITA sobre os TIPOS CANÔNICOS — o retipo `m_pos → peso_do_nome`
foi feito NO canônico (`TGL/SpecificAQFTWitness.lean`, v372), de modo que a família paralela `Photon.*` da
bancada deixa de ser necessária para o contrato. Nomes com sufixo `v32` para não repetir declaração do kernel.

O que muda da v3.1: (i) o habitante tem massa nula e helicidade ±1 (a LUZ, não spin-2 propagante: o gráviton é
a forma conjugada da luz — `TheGravitonIsTheConjugatedPhase`, 28/08); (ii) o par exibe a realização analítica
de Tomita (D-6); (iii) o tensor tem as cláusulas locais (simetria, conservação fraca, covariância pelo boost);
(iv) `same_horizon` deixa de ser `rfl` (tautologia, dita pelo operador) e passa a RECONHECIMENTO PELO CONTEÚDO
(`ORDEM016.D6.ReconhecimentoPeloConteudo`: um unitário que leva o vetor ao vetor e a álgebra à álgebra).

Só tipos. Nenhum nome reservado é cunhado; nada move o gate. PROVADA ≠ CONFIRMADA.
-/

noncomputable section
namespace TGLExt.ContratoQGv32
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 MeasureTheory Matrix

/-- **ContratoH2v32** — o H2 v3.1 sobre a LUZ: massa nula, helicidade ±1, e a realização de Tomita do par. -/
structure ContratoH2v32 (W0 : TGLSpecificAQFTWitness) (R0 : TGLModularRealization W0)
    (N0 : KillingNormalization) extends TGLExt.ContratoQGv31.ContratoH2 W0 R0 N0 where
  photon_mass : W0.m = 0
  photon_helicity : W0.helicity = 1 ∨ W0.helicity = -1
  pair_realization : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (W0.net rightWedge).toStarSubalgebra W0.vac R0.modular.modularConjugation Δit

/-- a assinatura (+,−,−,−) componente a componente. -/
def metricSignV32 (μ : Fin 4) : ℝ := if μ = 0 then 1 else -1

/-- a derivada parcial de um teste. -/
def testDerivativeV32 (f : (Fin 4 → ℝ) → ℝ) (μ : Fin 4) (x : Fin 4 → ℝ) : ℝ :=
  fderiv ℝ f x (Pi.single μ 1)

/-- **StressTensorDataLocalV32** — o tensor do par com as cláusulas locais (A-1.c da bancada). -/
structure StressTensorDataLocalV32 (W0 : TGLSpecificAQFTWitness) (B : WedgeBoostRep W0)
    extends StressTensorData W0 where
  symmetric : ∀ ψ x, (T ψ x).transpose = T ψ x
  test_integrable : ∀ (ψ : W0.H) (ν μ : Fin 4) (f : (Fin 4 → ℝ) → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    Integrable (fun x => metricSignV32 μ * T ψ x μ ν * testDerivativeV32 f μ x)
  conserved : ∀ (ψ : W0.H) (ν : Fin 4) (f : (Fin 4 → ℝ) → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    (∑ μ : Fin 4, ∫ x : Fin 4 → ℝ, metricSignV32 μ * T ψ x μ ν * testDerivativeV32 f μ x) = 0
  boost_covariant : ∀ (s : ℝ) (ψ : W0.H) (x : Fin 4 → ℝ),
    T (B.V s ψ) x = (TGLExt.boostMat (-s)).transpose * T ψ (wedgeBoostMap (-s) x) * TGLExt.boostMat (-s)

/-- **ContratoH3v32** — o H3 v3.1 sobre o MESMO horizonte da luz e o MESMO boost do tensor. -/
structure ContratoH3v32 (W0 : TGLSpecificAQFTWitness) (R0 : TGLModularRealization W0)
    (N0 : KillingNormalization) (B : WedgeBoostRep W0) (T0 : StressTensorDataLocalV32 W0 B)
    extends TGLExt.ContratoQGv31.ContratoH3 W0 R0 N0 T0.toStressTensorData where
  light_horizon : ContratoH2v32 W0 R0 N0
  same_stress_boost : light_horizon.boost = B
  same_local_horizon : H2 = light_horizon.toContratoH2

/-- **ContratoImportH3v32** — o import com o índice h2 EFETIVAMENTE usado e o mesmo horizonte por CONTEÚDO. -/
structure ContratoImportH3v32 (W0 : TGLSpecificAQFTWitness) (R0 : TGLModularRealization W0)
    (N0 : KillingNormalization) (B : WedgeBoostRep W0) (T0 : StressTensorDataLocalV32 W0 B)
    (h2 : ContratoH2v32 W0 R0 N0) where
  produce : ContratoH3v32 W0 R0 N0 B T0
  same_horizon : ORDEM016.D6.ReconhecimentoPeloConteudo
    (W0.net rightWedge).toStarSubalgebra (W0.net rightWedge).toStarSubalgebra W0.vac W0.vac
  source_realization : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (W0.net rightWedge).toStarSubalgebra W0.vac R0.modular.modularConjugation h2.Δit
  source_is_the_light : produce.light_horizon = h2

end TGLExt.ContratoQGv32
