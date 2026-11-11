import TGLExt.QGSolutionComplete
import TGLExt.O16.OrbitalBoostTransport
import TGLExt.O16.OrbitalMeasureSupport_v2
import TGLExt.ClosedAntilinearStandardSubspace
import TGLExt.GenericAntilinearAdjoint
import TGLExt.V351FourierTranslation

/-!
Auditoria c1 do complemento F1.3 v3.1 (sandbox; copia; nada aqui e pedra; nada entra no kernel;
so leitura sobre o build do kernel do Nos).

Pergunta: a saida do D1a.3 TIPA HOJE como enunciado Lean, com Delta_K := S_K^dagger S_K no padrao de
`ContinuousModularReconstruction.lean:87-112` e calculo multiplicativo depois do Fourier, tendo as pecas
ainda abertas do D1a.1-D1a.2 (ponte de Fubini L2 vetorial, J_W, Delta_W^{1/2}, simbolo) como CAMPOS?
O complemento v3.1 diz que a segunda camada «so pode ser tipada apos construir». Esta sonda testa isso.
Nada aqui constroi o D1a: so tipa o enunciado; nenhum habitante e dado.
-/

set_option autoImplicit false

noncomputable section
namespace AuditF13v31
open MeasureTheory
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 TGLExt.ImportedSQ TGLExt.QGSolution
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.Continuous050

/-- a fibra transversal (como na sonda c1 v3). -/
abbrev TransverseFiber : Type := Lp Fib 2 (volume : Measure Transverse)

/-- L2(R_rapidez; L2(Transverse; Fib)). -/
abbrev RapidityHilbert : Type := TGLV350.Regular.RegularHilbert TransverseFiber

/-- D1a.0 (pago, O16): a carta de rapidez. -/
def toRapidity : H1 ≃ₗᵢ[ℂ] Lp Fib 2 momentumMeasure := orbitalL2Equivalence (E := Fib) 0

/-- D1a.1: Fourier parcial na rapidez, a partir da ponte de Fubini L2 vetorial `Fub` (FALTA no pin). -/
def partialFourier (Fub : Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert) :
    H1 ≃ₗᵢ[ℂ] RapidityHilbert :=
  (toRapidity.trans Fub).trans (Lp.fourierTransformₗᵢ ℝ TransverseFiber)

/-- Delta := S^dagger S para S = genericTomita T J, no padrao de ContinuousModularReconstruction.lean:91-112
(caracterizacao completa do grafo). -/
def IsTomitaSquare (T : H1 →ₗ.[ℂ] H1) (J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (Δ : H1 →ₗ.[ℂ] H1) : Prop :=
  ∀ f g : H1, (f, g) ∈ Δ.graph ↔
    ∃ hf : f ∈ T.domain,
      ∃ hSf : genericTomita T J ⟨f, hf⟩ ∈ (genericTomitaAdjoint T J).domain,
        genericTomitaAdjoint T J ⟨genericTomita T J ⟨f, hf⟩, hSf⟩ = g

/-- calculo multiplicativo depois do Fourier: Delta e a multiplicacao MAXIMAL por e^{sigma(xi)} apos Phi. -/
def IsMultiplierAfter (Φ : H1 ≃ₗᵢ[ℂ] RapidityHilbert) (σ : ℝ → ℝ) (Δ : H1 →ₗ.[ℂ] H1) : Prop :=
  ∀ f g : H1, (f, g) ∈ Δ.graph ↔
    (⇑(Φ g) : ℝ → TransverseFiber) =ᵐ[volume]
      fun ξ => (Real.exp (σ ξ) : ℂ) • (⇑(Φ f) : ℝ → TransverseFiber) ξ

/-- Delta^{it} pelo mesmo calculo multiplicativo e B0(-2 pi t): apos Phi, o boost age como e^{i t sigma}. -/
def ModularGroupIsBoost (Φ : H1 ≃ₗᵢ[ℂ] RapidityHilbert) (σ : ℝ → ℝ) : Prop :=
  ∀ (t : ℝ) (f : H1),
    (⇑(Φ (B0 (-(2 * Real.pi * t)) f)) : ℝ → TransverseFiber) =ᵐ[volume]
      fun ξ => Complex.exp (((t * σ ξ : ℝ) : ℂ) * Complex.I) • (⇑(Φ f) : ℝ → TransverseFiber) ξ

/-- A SAIDA DO D1a.3 como enunciado: `Fub`, `J`, `T`, `σ` sao as entregas abertas do D1a.1-D1a.2;
nao ha campo «Delta livre» (Delta fica preso a S^dagger S e ao multiplicador) e nao ha «exists xi != 0». -/
structure D1a3Output where
  Fub : Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert
  J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1
  J_involutive : Function.Involutive J
  T : H1 →ₗ.[ℂ] H1
  T_selfadjoint : IsSelfAdjoint T
  σ : ℝ → ℝ
  KWR : StandardSubspace H1
  K_is_fix : ∀ x : H1, x ∈ KWR.toClosedSubmodule ↔
    ∃ hx : x ∈ T.domain, genericTomita T J ⟨x, hx⟩ = x
  Δ : H1 →ₗ.[ℂ] H1
  delta_is_SdagS : IsTomitaSquare T J Δ
  delta_multiplier : IsMultiplierAfter (partialFourier Fub) σ Δ
  modular_is_boost : ModularGroupIsBoost (partialFourier Fub) σ

/-- o Delta do enunciado nao e campo livre: S^dagger S o determina (unicidade pelo grafo). -/
theorem tomitaSquare_unique (T : H1 →ₗ.[ℂ] H1) (J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (Δ₁ Δ₂ : H1 →ₗ.[ℂ] H1) (h₁ : IsTomitaSquare T J Δ₁) (h₂ : IsTomitaSquare T J Δ₂) :
    Δ₁ = Δ₂ := by
  apply LinearPMap.eq_of_eq_graph
  ext ⟨f, g⟩
  rw [h₁ f g, h₂ f g]

/-- R4: as pecas genericas servem a H1 diretamente (H1 e completo). -/
example : CompleteSpace H1 := inferInstance

theorem generic_pairing_on_H1 (T : H1 →ₗ.[ℂ] H1) (hT : IsSelfAdjoint T)
    (J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hJ : Function.Involutive J)
    (x : T.domain) (y : genericAdjointDomain T J) :
    inner ℂ (genericTomita T J x) (y : H1) = inner ℂ (genericTomitaAdjoint T J y) (x : H1) :=
  generic_adjoint_pairing T hT J hJ x y

/-- num Hilbert nao trivial, nenhum subespaco padrao e nulo (copia da sonda c1 v3). -/
theorem standard_ne_bot {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [Nontrivial H]
    (S : StandardSubspace H) : S.toClosedSubmodule ≠ ⊥ := by
  intro h
  have hc := S.IsCyclic
  rw [h, ClosedSubmodule.mulI, ClosedSubmodule.mapEquiv_bot_eq_bot, sup_idem] at hc
  obtain ⟨x, hx⟩ := exists_ne (0 : H)
  have hx' : x ∈ (⊤ : ClosedSubmodule ℝ H) := ClosedSubmodule.mem_top
  rw [← hc, ClosedSubmodule.mem_bot] at hx'
  exact hx hx'

/-- H1 nao trivial (copia da sonda c1 v3b). -/
theorem H1_nontrivial : Nontrivial H1 := by
  haveI : SigmaFinite (orbitalMeasure 0) := orbitalMeasure_sigmaFinite 0
  haveI : (orbitalMeasure 0).IsOpenPosMeasure := orbitalMeasure_openPos 0
  have huniv : (orbitalMeasure 0) Set.univ ≠ 0 :=
    (isOpen_univ.measure_pos (orbitalMeasure 0) Set.univ_nonempty).ne'
  obtain ⟨n, hn⟩ : ∃ n, (orbitalMeasure 0) (spanningSets (orbitalMeasure 0) n) ≠ 0 := by
    by_contra hcon
    push_neg at hcon
    apply huniv
    rw [← iUnion_spanningSets (orbitalMeasure 0)]
    exact measure_iUnion_null hcon
  have hs : MeasurableSet (spanningSets (orbitalMeasure 0) n) := measurableSet_spanningSets _ n
  have hfin : (orbitalMeasure 0) (spanningSets (orbitalMeasure 0) n) ≠ ⊤ :=
    (measure_spanningSets_lt_top _ n).ne
  obtain ⟨v, hv⟩ := exists_ne (0 : Fib)
  refine ⟨⟨indicatorConstLp 2 hs hfin v, 0, ?_⟩⟩
  intro h0
  have hnorm := congrArg norm h0
  rw [norm_indicatorConstLp (by norm_num) (by norm_num), norm_zero] at hnorm
  change ‖v‖ * ((orbitalMeasure 0) (spanningSets (orbitalMeasure 0) n)).toReal ^ (1 / (2 : ENNReal).toReal) = 0
    at hnorm
  have hv' : 0 < ‖v‖ := norm_pos_iff.mpr hv
  have hreal : 0 < ((orbitalMeasure 0) (spanningSets (orbitalMeasure 0) n)).toReal :=
    ENNReal.toReal_pos hn hfin
  have hpow : 0 < ((orbitalMeasure 0) (spanningSets (orbitalMeasure 0) n)).toReal ^ (1 / (2 : ENNReal).toReal) :=
    Real.rpow_pos_of_pos hreal _
  have := mul_pos hv' hpow
  linarith

/-- o «exists xi != 0» da v3 e CONSEQUENCIA da saida (sem hipotese extra): pode sair do enunciado. -/
theorem exists_nonzero_of_output (O : D1a3Output) :
    ∃ ξ : H1, ξ ∈ O.KWR.toClosedSubmodule ∧ ξ ≠ 0 := by
  haveI := H1_nontrivial
  by_contra h
  apply standard_ne_bot O.KWR
  apply SetLike.ext
  intro x
  constructor
  · intro hx
    rw [ClosedSubmodule.mem_bot]
    by_contra hne
    exact h ⟨x, hx, hne⟩
  · intro hx
    rw [ClosedSubmodule.mem_bot] at hx
    subst hx
    exact zero_mem _

/-- a proposta R3 com o certificado modular TIPADO pela saida acima (forma para a fila do operador). -/
structure LightNetStandardWedgeData extends LightNetData where
  out : D1a3Output
  wedge_glue : toLightNetData.K rightWedge = out.KWR.toClosedSubmodule.toSubmodule

/-- a forma do complemento v3.1 (so os dois campos que ele tipa; o terceiro fica em prosa). -/
structure LightNetStandardWedgeData_v31 extends LightNetData where
  KWR : StandardSubspace H1
  wedge_glue : toLightNetData.K rightWedge = KWR.toClosedSubmodule.toSubmodule


/-! ## versao BGL: K(W_R) CONSTRUIDO por closedAntilinearStandardSubspace (rota D1a.3 da propria v3) -/

/-- S_W := genericTomita T J (= J_W Delta_W^{1/2}) como mapa semilinear do dominio (o `toFun` de GenericAntilinearAdjoint.lean:76). -/
abbrev SW (T : H1 →ₗ.[ℂ] H1) (J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) : T.domain →ₛₗ[starRingEnd ℂ] H1 :=
  (genericTomita T J).toFun

/-- A SAIDA DO D1a.3 (forma BGL): S_W involucao fechada densa, K(W_R) := Fix S_W construido,
Delta_K := S_W^dagger S_W pelo grafo, Delta_K^{it} multiplicativo = B0(-2 pi t). -/
structure D1a3OutputBGL where
  Fub : Lp Fib 2 momentumMeasure ≃ₗᵢ[ℂ] RapidityHilbert
  J : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1
  J_involutive : Function.Involutive J
  T : H1 →ₗ.[ℂ] H1
  T_selfadjoint : IsSelfAdjoint T
  σ : ℝ → ℝ
  hclosed : IsClosed (Set.range (fun x : T.domain => ((x : H1), SW T J x)))
  hmaps : ∀ x : T.domain, SW T J x ∈ T.domain
  hinv : ∀ x : T.domain, SW T J ⟨SW T J x, hmaps x⟩ = (x : H1)
  hdense : Dense (T.domain : Set H1)
  Δ : H1 →ₗ.[ℂ] H1
  delta_is_SdagS : IsTomitaSquare T J Δ
  delta_multiplier : IsMultiplierAfter (partialFourier Fub) σ Δ
  modular_is_boost : ModularGroupIsBoost (partialFourier Fub) σ

/-- K(W_R) e CONSTRUIDO (ClosedAntilinearStandardSubspace.lean:213-221), nao e campo livre. -/
def D1a3OutputBGL.KWR (O : D1a3OutputBGL) : StandardSubspace H1 :=
  ChatgptAudit.Continuous049.closedAntilinearStandardSubspace O.T.domain (SW O.T O.J)
    O.hclosed O.hmaps O.hinv O.hdense

theorem D1a3OutputBGL.mem_KWR (O : D1a3OutputBGL) (x : H1) :
    x ∈ O.KWR.toClosedSubmodule ↔ ∃ hx : x ∈ O.T.domain, SW O.T O.J ⟨x, hx⟩ = x := Iff.rfl

/-- S_W e o operador de Tomita de K(W_R): h + i k |-> h - i k (Continuous049.fixed_sum_tomita). -/
theorem D1a3OutputBGL.S_is_tomita_of_K (O : D1a3OutputBGL) (h k : H1)
    (hh : h ∈ O.KWR.toClosedSubmodule) (hk : k ∈ O.KWR.toClosedSubmodule) :
    ∃ hd : h + Complex.I • k ∈ O.T.domain, SW O.T O.J ⟨h + Complex.I • k, hd⟩ = h - Complex.I • k :=
  ⟨_, ChatgptAudit.Continuous049.fixed_sum_tomita O.T.domain (SW O.T O.J) h k hh hk⟩

/-- o «exists xi != 0» tambem e consequencia na forma BGL. -/
theorem D1a3OutputBGL.exists_nonzero (O : D1a3OutputBGL) :
    ∃ ξ : H1, ξ ∈ O.KWR.toClosedSubmodule ∧ ξ ≠ 0 := by
  haveI := H1_nontrivial
  by_contra h
  apply standard_ne_bot O.KWR
  apply SetLike.ext
  intro x
  constructor
  · intro hx
    rw [ClosedSubmodule.mem_bot]
    by_contra hne
    exact h ⟨x, hx, hne⟩
  · intro hx
    rw [ClosedSubmodule.mem_bot] at hx
    subst hx
    exact zero_mem _

/-- a interface R3 sobre a forma BGL: colagem com o K CONSTRUIDO. -/
structure LightNetStandardWedgeDataBGL extends LightNetData where
  out : D1a3OutputBGL
  wedge_glue : toLightNetData.K rightWedge = out.KWR.toClosedSubmodule.toSubmodule

end AuditF13v31

#print axioms AuditF13v31.toRapidity
#print axioms AuditF13v31.partialFourier
#print axioms AuditF13v31.IsTomitaSquare
#print axioms AuditF13v31.IsMultiplierAfter
#print axioms AuditF13v31.ModularGroupIsBoost
#print axioms AuditF13v31.D1a3Output
#print axioms AuditF13v31.tomitaSquare_unique
#print axioms AuditF13v31.generic_pairing_on_H1
#print axioms AuditF13v31.standard_ne_bot
#print axioms AuditF13v31.H1_nontrivial
#print axioms AuditF13v31.exists_nonzero_of_output
#print axioms AuditF13v31.LightNetStandardWedgeData
#print axioms AuditF13v31.LightNetStandardWedgeData_v31
#print axioms AuditF13v31.D1a3OutputBGL
#print axioms AuditF13v31.D1a3OutputBGL.KWR
#print axioms AuditF13v31.D1a3OutputBGL.mem_KWR
#print axioms AuditF13v31.D1a3OutputBGL.S_is_tomita_of_K
#print axioms AuditF13v31.D1a3OutputBGL.exists_nonzero
#print axioms AuditF13v31.LightNetStandardWedgeDataBGL
