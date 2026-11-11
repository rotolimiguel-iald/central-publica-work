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
import TGLExt.PastContinuousExtension
import TGLExt.EquilibriumAreaExpansion

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

variable {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (P : EquilibriumScreenData U g Gamma p v) (T : TensorField4) (rate : ℝ)

def screenHeatFlux (t : ℝ) : ℝ :=
  -rate*t*tensorQuad (T (P.curve t)) (P.velocity (P.curve t))*
    inducedArea g P.curve P.screen.vectors t

theorem screen_heat_flux_zero : screenHeatFlux P T rate 0=0 := by
  simp [screenHeatFlux]

theorem screen_heat_flux_continuous_zero (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    ContinuousAt (screenHeatFlux P T rate) 0 := by
  have hm := screen_matter_continuous_zero U hU g T Gamma hT p v P
  have hA := screen_area_continuous_zero U hU g Gamma hg p v P
  exact ((continuousAt_const.mul continuousAt_id).mul hm).mul hA

theorem screen_heat_flux_continuous_past (hU : IsOpen U)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    ∀ᶠ t in 𝓝[<] (0:ℝ), ContinuousAt (screenHeatFlux P T rate) t := by
  filter_upwards [screen_matter_continuous_past U hU g T Gamma hT p v P,P.area_rate] with t hm hA
  exact ((continuousAt_const.mul continuousAt_id).mul hm).mul hA.continuousAt

def screenHeatExtension (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    PastContinuousExtension (screenHeatFlux P T rate) :=
  pastContinuousExtension (screenHeatFlux P T rate)
    (screen_heat_flux_continuous_zero P T rate hU hg hT)
    (screen_heat_flux_continuous_past P T rate hU hT)

def constructedHeat (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) : ℝ → ℝ :=
  pastIntegral (screenHeatExtension P T rate hU hg hT)

theorem constructed_heat_continuous (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    Continuous (constructedHeat P T rate hU hg hT) :=
  past_integral_continuous _

theorem constructed_heat_zero (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    constructedHeat P T rate hU hg hT 0=0 :=
  past_integral_zero _

theorem constructed_heat_rate (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    ∀ᶠ t in 𝓝[<] (0:ℝ),
      HasDerivAt (constructedHeat P T rate hU hg hT) (screenHeatFlux P T rate t) t :=
  past_integral_matches_flux _

theorem screen_heat_flux_linear_limit (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    Tendsto (fun t => screenHeatFlux P T rate t/t) (𝓝[<] 0)
      (𝓝 (-rate*tensorQuad (T p) v)) := by
  have hm : Tendsto (fun t => tensorQuad (T (P.curve t)) (P.velocity (P.curve t)))
      (𝓝[<] (0:ℝ)) (𝓝 (tensorQuad (T (P.curve 0)) (P.velocity (P.curve 0)))) :=
    (screen_matter_continuous_zero U hU g T Gamma hT p v P).tendsto.mono_left nhdsWithin_le_nhds
  have hA : Tendsto (inducedArea g P.curve P.screen.vectors) (𝓝[<] (0:ℝ))
      (𝓝 (inducedArea g P.curve P.screen.vectors 0)) :=
    (screen_area_continuous_zero U hU g Gamma hg p v P).tendsto.mono_left nhdsWithin_le_nhds
  have hl : Tendsto
      (fun t => -rate*tensorQuad (T (P.curve t)) (P.velocity (P.curve t))*
        inducedArea g P.curve P.screen.vectors t)
      (𝓝[<] (0:ℝ)) (𝓝 (-rate*tensorQuad (T p) v)) := by
    simpa only [P.curve_zero,P.velocity_at_point,
      equilibrium_screen_area_initial U g Gamma p v P,mul_one] using
      (tendsto_const_nhds.mul hm).mul hA
  have he : (fun t => screenHeatFlux P T rate t/t) =ᶠ[𝓝[<] (0:ℝ)]
      (fun t => -rate*tensorQuad (T (P.curve t)) (P.velocity (P.curve t))*
        inducedArea g P.curve P.screen.vectors t) := by
    filter_upwards [self_mem_nhdsWithin] with t ht
    have hn : t≠0 := ne_of_lt ht
    unfold screenHeatFlux
    field_simp [hn]
  exact hl.congr' he.symm

theorem screen_heat_quadratic_limit (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (E : PastContinuousExtension (screenHeatFlux P T rate)) :
    Tendsto (fun t => pastIntegral E t/t^2) (𝓝[<] 0)
      (𝓝 (-rate*tensorQuad (T p) v/2)) :=
  primitive_quadratic_limit (screenHeatFlux P T rate) (pastIntegral E) _
    (past_integral_matches_flux E) (past_integral_continuous E).continuousAt (past_integral_zero E)
    (screen_heat_flux_linear_limit P T rate hU hg hT)

theorem constructed_heat_quadratic_limit (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U) :
    Tendsto (fun t => constructedHeat P T rate hU hg hT t/t^2) (𝓝[<] 0)
      (𝓝 (-rate*tensorQuad (T p) v/2)) :=
  screen_heat_quadratic_limit P T rate hU hg hT _

theorem heat_extension_difference_quadratic_zero (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (E F : PastContinuousExtension (screenHeatFlux P T rate)) :
    Tendsto (fun t => (pastIntegral E t-pastIntegral F t)/t^2) (𝓝[<] 0) (𝓝 0) := by
  have he := (screen_heat_quadratic_limit P T rate hU hg hT E).sub
    (screen_heat_quadratic_limit P T rate hU hg hT F)
  simpa only [sub_div,sub_self] using he

#print axioms screen_heat_flux_zero
#print axioms screen_heat_flux_continuous_zero
#print axioms screen_heat_flux_continuous_past
#print axioms screenHeatExtension
#print axioms constructedHeat
#print axioms constructed_heat_continuous
#print axioms constructed_heat_zero
#print axioms constructed_heat_rate
#print axioms screen_heat_flux_linear_limit
#print axioms screen_heat_quadratic_limit
#print axioms constructed_heat_quadratic_limit
#print axioms heat_extension_difference_quadratic_zero
end
end ChatgptAudit.Flow020
