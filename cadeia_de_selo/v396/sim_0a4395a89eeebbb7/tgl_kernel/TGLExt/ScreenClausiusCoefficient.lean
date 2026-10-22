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
import TGLExt.ConstructedHeatPrimitive

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def clausiusCoefficient (rate eta ricci matter : ℝ) : ℝ :=
  rate/2*(eta*ricci/(2*Real.pi)-matter)

theorem residual_quadratic_coefficient (rate eta ricci matter : ℝ) (area heat : ℝ → ℝ)
    (hA : Tendsto (fun t => (area t-area 0)/t^2) (𝓝[<] 0) (𝓝 (-ricci/2)))
    (hQ : Tendsto (fun t => heat t/t^2) (𝓝[<] 0) (𝓝 (-rate*matter/2))) :
    Tendsto (fun t => horizonBalancePrimitive rate eta area heat t/t^2) (𝓝[<] 0)
      (𝓝 (clausiusCoefficient rate eta ricci matter)) := by
  have hk : Tendsto (fun _ : ℝ => (rate/(2*Real.pi))*eta) (𝓝[<] 0)
      (𝓝 ((rate/(2*Real.pi))*eta)) := tendsto_const_nhds
  have hh := hQ.sub (hk.mul hA)
  have hf : (fun t => horizonBalancePrimitive rate eta area heat t/t^2)=
      (fun t => heat t/t^2-((rate/(2*Real.pi))*eta)*((area t-area 0)/t^2)) := by
    funext t
    unfold horizonBalancePrimitive
    ring
  have hc : -rate*matter/2-((rate/(2*Real.pi))*eta)*(-ricci/2)=
      clausiusCoefficient rate eta ricci matter := by
    unfold clausiusCoefficient
    ring
  rwa [←hf,hc] at hh

theorem clausius_coefficient_zero_iff (rate eta ricci matter : ℝ)
    (hrate : rate≠0) (heta : eta≠0) :
    clausiusCoefficient rate eta ricci matter=0 ↔ ricci=(2*Real.pi/eta)*matter := by
  constructor
  · intro h
    have hh : rate/2≠0 := div_ne_zero hrate (by norm_num)
    have hz : eta*ricci/(2*Real.pi)-matter=0 :=
      (mul_eq_zero.mp h).resolve_left hh
    have he : eta*ricci=matter*(2*Real.pi) :=
      (div_eq_iff (mul_ne_zero (by norm_num) Real.pi_ne_zero)).mp (sub_eq_zero.mp hz)
    rw [div_mul_eq_mul_div]
    apply (eq_div_iff heta).mpr
    nlinarith only [he]
  · intro h
    unfold clausiusCoefficient
    rw [h]
    field_simp [heta,Real.pi_ne_zero]
    ring

theorem past_zero_limit_iff (f : ℝ → ℝ) (c : ℝ)
    (hf : Tendsto f (𝓝[<] 0) (𝓝 c)) :
    Tendsto f (𝓝[<] 0) (𝓝 0) ↔ c=0 := by
  constructor
  · intro hz
    exact tendsto_nhds_unique hf hz
  · intro hz
    simpa only [hz] using hf

variable {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (P : EquilibriumScreenData U g Gamma p v) (T : TensorField4) (rate eta : ℝ)

theorem screen_clausius_coefficient (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i)
    (E : PastContinuousExtension (screenHeatFlux P T rate)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta
        (inducedArea g P.curve P.screen.vectors) (pastIntegral E) t/t^2)
      (𝓝[<] 0)
      (𝓝 (clausiusCoefficient rate eta (tensorQuad (coordinateRicci Gamma p) v) (tensorQuad (T p) v))) := by
  apply residual_quadratic_coefficient
  · simpa only [equilibrium_screen_area_initial U g Gamma p v P] using
      screen_area_quadratic_limit U hU g Gamma hg hG p v P ht
  · exact screen_heat_quadratic_limit P T rate hU hg hT E

theorem screen_clausius_iff_null_balance (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i)
    (hrate : rate≠0) (heta : eta≠0)
    (E : PastContinuousExtension (screenHeatFlux P T rate)) :
    Tendsto (fun t => horizonBalancePrimitive rate eta
        (inducedArea g P.curve P.screen.vectors) (pastIntegral E) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      tensorQuad (coordinateRicci Gamma p) v=(2*Real.pi/eta)*tensorQuad (T p) v := by
  exact (past_zero_limit_iff _ _
    (screen_clausius_coefficient P T rate eta hU hg hG hT ht E)).trans
    (clausius_coefficient_zero_iff rate eta _ _ hrate heta)

theorem constructed_clausius_iff_null_balance (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i)
    (hrate : rate≠0) (heta : eta≠0) :
    Tendsto (fun t => horizonBalancePrimitive rate eta
        (inducedArea g P.curve P.screen.vectors) (constructedHeat P T rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) ↔
      tensorQuad (coordinateRicci Gamma p) v=(2*Real.pi/eta)*tensorQuad (T p) v :=
  screen_clausius_iff_null_balance P T rate eta hU hg hG hT ht hrate heta _

#print axioms residual_quadratic_coefficient
#print axioms clausius_coefficient_zero_iff
#print axioms past_zero_limit_iff
#print axioms screen_clausius_coefficient
#print axioms screen_clausius_iff_null_balance
#print axioms constructed_clausius_iff_null_balance
end
end ChatgptAudit.Flow020
