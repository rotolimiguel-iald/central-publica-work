import TGLExt.PoincareWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A REPRESENTAÇÃO FIEL: Poincaré inteiro age unitariamente em L²(ℝ⁴)
  [TGLExt — v118, o incremento 39 do programa SemifiniteAnalysis]

O v116 nomeou o resíduo da testemunha: "rep unitária FIEL do setor
conexo (∞-dim; não existe f.d.) + III₁". Esta pedra CONSTRÓI a metade
construtível — a representação regular:

* `SpacetimeL2` = L²(ℝ⁴, ℂ) com a medida de Lebesgue — ∞-dim;
* ★★ `measurePreserving_pAct` — TODA transformação de Poincaré preserva
  a medida de Lebesgue (|det Λ| = 1 pela relação definidora + translação
  invariante): a unitariedade nasce da relação ΛᵀηΛ = η;
* ★★ `regularRep` — U(g)F = F ∘ φ(g⁻¹): isometria linear de L², com
  ★ `regularRep_one` (U(1) = id) e ★★ `regularRep_mul`
  (U(g)U(h) = U(gh) — a lei de grupo);
* ★★★ `regularRep_faithful` — A FIDELIDADE: para TODO g ≠ 1 existe
  F ∈ L² com U(g)F ≠ F (o indicador de uma bola pequena em torno de um
  ponto movido — o deslocamento é visto por um conjunto de medida
  positiva). NENHUMA direção é cega: translações, rotações, PARIDADE e
  BOOSTS movem vetores de L²;
* ★★ `regularRep_moves_boost` — o corolário nomeado: o BOOST (χ ≠ 0),
  que a fibra do v116 não via (setor próprio cego), MOVE vetores da
  representação regular.

O QUE ISTO FECHA: a metade "rep unitária fiel em ∞-dim" do resíduo da
witness EXISTE em kernel. O QUE SEGUE ABERTO (nomeado, sem véu): acoplar
esta representação às FIBRAS da rede covariante e o fator III₁ (teoria
modular de von Neumann, ausente da mathlib) — o `qgClosureCertificateV2`
segue RESERVADO (lição v103, oitava aplicação).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open MeasureTheory Metric

noncomputable section

/-- L²(ℝ⁴, ℂ): a morada da representação regular. -/
abbrev SpacetimeL2 : Type := Lp ℂ 2 (volume : Measure (Fin 4 → ℝ))

/-! ## A — Poincaré preserva Lebesgue -/

theorem lorentz_det_ne_zero (Λ : LorentzGrp) : Λ.1.det ≠ 0 := by
  intro h
  have h2 := lorentz_det_sq Λ
  rw [h] at h2
  norm_num at h2

theorem lorentz_abs_det_inv_one (Λ : LorentzGrp) : |(Λ.1.det)⁻¹| = 1 := by
  have h2 := lorentz_det_sq Λ
  have habs : |Λ.1.det| = 1 := by
    nlinarith [abs_nonneg Λ.1.det, sq_abs Λ.1.det,
      sq_nonneg (|Λ.1.det| - 1), sq_nonneg (|Λ.1.det| + 1)]
  rw [abs_inv, habs]
  norm_num

/-- [KERNEL] ★ a parte de Lorentz preserva Lebesgue (|det| = 1). -/
theorem measurePreserving_mulVec (Λ : LorentzGrp) :
    MeasurePreserving (fun x : Fin 4 → ℝ => Λ.1.mulVec x) volume volume := by
  have hfun : (fun x : Fin 4 → ℝ => Λ.1.mulVec x) = Matrix.toLin' Λ.1 := by
    funext x
    rw [Matrix.toLin'_apply]
  rw [hfun]
  refine ⟨(LinearMap.continuous_on_pi _).measurable, ?_⟩
  rw [Real.map_matrix_volume_pi_eq_smul_volume_pi (lorentz_det_ne_zero Λ),
    lorentz_abs_det_inv_one, ENNReal.ofReal_one, one_smul]

/-- [KERNEL] ★ a translação preserva Lebesgue (invariância de Haar). -/
theorem measurePreserving_translate (a : Fin 4 → ℝ) :
    MeasurePreserving (fun x : Fin 4 → ℝ => x + a) volume volume :=
  ⟨measurable_add_const a, map_add_right_eq_self volume a⟩

/-- [KERNEL] ★★ TODA transformação de Poincaré preserva a medida de
    Lebesgue: a unitariedade nasce de ΛᵀηΛ = η (|det Λ| = 1). -/
theorem measurePreserving_pAct (g : PoincareGroup) :
    MeasurePreserving (pAct g) volume volume := by
  have hfun : pAct g
      = (fun x : Fin 4 → ℝ => x + g.tr)
        ∘ (fun x : Fin 4 → ℝ => g.lor.1.mulVec x) := by
    funext x
    rfl
  rw [hfun]
  exact (measurePreserving_translate g.tr).comp (measurePreserving_mulVec g.lor)

/-! ## B — a representação regular -/

/-- A REPRESENTAÇÃO REGULAR: U(g)F = F ∘ φ(g⁻¹). -/
def regularRep (g : PoincareGroup) : SpacetimeL2 →ₗᵢ[ℂ] SpacetimeL2 :=
  Lp.compMeasurePreservingₗᵢ ℂ (pAct g⁻¹) (measurePreserving_pAct g⁻¹)

theorem regularRep_apply (g : PoincareGroup) (F : SpacetimeL2) :
    regularRep g F
      = Lp.compMeasurePreserving (pAct g⁻¹) (measurePreserving_pAct g⁻¹) F := rfl

/-- a congruência da composição (a prova é irrelevante, a função manda). -/
theorem comp_congr_fun {f₁ f₂ : (Fin 4 → ℝ) → (Fin 4 → ℝ)} (h : f₁ = f₂)
    (hf₁ : MeasurePreserving f₁ (volume : Measure (Fin 4 → ℝ)) volume)
    (F : SpacetimeL2) :
    Lp.compMeasurePreserving f₁ hf₁ F
      = Lp.compMeasurePreserving f₂ (h ▸ hf₁) F := by
  subst h
  rfl

/-- [KERNEL] ★ U(1) = id. -/
theorem regularRep_one (F : SpacetimeL2) : regularRep 1 F = F := by
  rw [regularRep_apply]
  have h1 : pAct (1 : PoincareGroup)⁻¹ = id := by
    funext x
    rw [inv_one, pAct_one]
    rfl
  rw [comp_congr_fun h1 (measurePreserving_pAct 1⁻¹) F]
  exact Lp.compMeasurePreserving_id_apply F

/-- [KERNEL] ★★ A LEI DE GRUPO: U(gh) = U(g) ∘ U(h). -/
theorem regularRep_mul (g h : PoincareGroup) (F : SpacetimeL2) :
    regularRep (g * h) F = regularRep g (regularRep h F) := by
  rw [regularRep_apply, regularRep_apply, regularRep_apply]
  have hfun : pAct ((g * h)⁻¹) = pAct h⁻¹ ∘ pAct g⁻¹ := by
    funext x
    rw [mul_inv_rev]
    exact pAct_mul h⁻¹ g⁻¹ x
  rw [comp_congr_fun hfun (measurePreserving_pAct (g * h)⁻¹) F]
  exact Lp.compMeasurePreserving_comp_apply F
    (measurePreserving_pAct h⁻¹) (measurePreserving_pAct g⁻¹)

/-! ## C — A FIDELIDADE: nenhuma direção é cega em L² -/

/-- o indicador de uma bola como elemento de L². -/
def ballIndicator (x₀ : Fin 4 → ℝ) (r : ℝ) : SpacetimeL2 :=
  indicatorConstLp 2
    (measurableSet_ball : MeasurableSet (Metric.ball x₀ r))
    (ne_of_lt (measure_ball_lt_top : volume (Metric.ball x₀ r) < ⊤)) (1 : ℂ)

theorem ballIndicator_coe (x₀ : Fin 4 → ℝ) (r : ℝ) :
    ballIndicator x₀ r
      =ᵐ[volume] (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) := by
  unfold ballIndicator
  exact indicatorConstLp_coeFn

/-- [KERNEL] ★★★ A FIDELIDADE DA REPRESENTAÇÃO REGULAR: todo g ≠ 1 move
    algum vetor de L² — o indicador de uma bola pequena em torno de um
    ponto que g⁻¹ desloca. Translações, rotações, paridade E BOOSTS:
    nenhuma das dez direções é cega na representação regular. -/
theorem regularRep_faithful (g : PoincareGroup) (hg : g ≠ 1) :
    ∃ F : SpacetimeL2, regularRep g F ≠ F := by
  -- (1) um ponto movido por φ := pAct g⁻¹
  have hginv : g⁻¹ ≠ 1 := fun h => hg (by
    have := congrArg (·⁻¹) h
    simpa using this)
  have hmoved : ∃ x₀, pAct g⁻¹ x₀ ≠ x₀ := by
    by_contra hall
    push Not at hall
    exact hginv (poincare_faithful g⁻¹ hall)
  obtain ⟨x₀, hx₀⟩ := hmoved
  set φ := pAct g⁻¹ with hφdef
  set y₀ := φ x₀ with hy₀
  have hd : 0 < dist y₀ x₀ := dist_pos.mpr hx₀
  set r := dist y₀ x₀ / 3 with hr
  have hrpos : 0 < r := by positivity
  -- (2) a constante de Lipschitz da parte linear
  set L := LinearMap.toContinuousLinearMap (Matrix.toLin' (g⁻¹).lor.1) with hL
  have hlip : ∀ x, dist (φ x) y₀ ≤ ‖L‖ * dist x x₀ := by
    intro x
    have hsub : φ x - y₀ = L (x - x₀) := by
      show pAct g⁻¹ x - pAct g⁻¹ x₀ = L (x - x₀)
      unfold pAct
      have : L (x - x₀) = (g⁻¹).lor.1.mulVec (x - x₀) := by
        show Matrix.toLin' (g⁻¹).lor.1 (x - x₀) = _
        rw [Matrix.toLin'_apply]
      rw [this, Matrix.mulVec_sub]
      abel
    rw [dist_eq_norm, hsub]
    calc ‖L (x - x₀)‖ ≤ ‖L‖ * ‖x - x₀‖ := L.le_opNorm _
      _ = ‖L‖ * dist x x₀ := by rw [dist_eq_norm]
  -- (3) o raio pequeno: dentro de B(x₀, δ) o φ manda tudo perto de y₀
  set δ := min r (r / (‖L‖ + 1)) with hδ
  have hδpos : 0 < δ := by
    apply lt_min hrpos
    positivity
  have hδr : δ ≤ r := min_le_left _ _
  have hnorm_pos : (0 : ℝ) < ‖L‖ + 1 := by positivity
  have himage : ∀ x ∈ Metric.ball x₀ δ, dist (φ x) y₀ < r := by
    intro x hx
    have hdx : dist x x₀ < δ := mem_ball.mp hx
    calc dist (φ x) y₀ ≤ ‖L‖ * dist x x₀ := hlip x
      _ ≤ ‖L‖ * δ := by
          apply mul_le_mul_of_nonneg_left (le_of_lt hdx) (norm_nonneg _)
      _ ≤ ‖L‖ * (r / (‖L‖ + 1)) := by
          apply mul_le_mul_of_nonneg_left (min_le_right _ _) (norm_nonneg _)
      _ < r := by
          rw [div_eq_mul_inv]
          rw [← mul_assoc]
          have h1 : ‖L‖ * r < (‖L‖ + 1) * r := by nlinarith [hrpos]
          calc ‖L‖ * r * (‖L‖ + 1)⁻¹ < (‖L‖ + 1) * r * (‖L‖ + 1)⁻¹ := by
                apply mul_lt_mul_of_pos_right h1
                positivity
            _ = r := by field_simp
  -- (4) dentro de B(x₀, δ): o indicador vale 1 e o transportado vale 0
  set F := ballIndicator x₀ r with hF
  refine ⟨F, fun heq => ?_⟩
  -- as duas classes têm representantes explícitos
  have hUF : regularRep g F =ᵐ[volume] fun x => (F : (Fin 4 → ℝ) → ℂ) (φ x) := by
    rw [regularRep_apply]
    exact Lp.coeFn_compMeasurePreserving F (measurePreserving_pAct g⁻¹)
  have hcoe : (F : (Fin 4 → ℝ) → ℂ)
      =ᵐ[volume] (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) :=
    ballIndicator_coe x₀ r
  have hmap : (volume : Measure (Fin 4 → ℝ)).map φ = volume :=
    (measurePreserving_pAct g⁻¹).map_eq
  have hcomp : (fun x => (F : (Fin 4 → ℝ) → ℂ) (φ x))
      =ᵐ[volume] fun x => (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x) := by
    have h1 : ((F : (Fin 4 → ℝ) → ℂ) ∘ φ)
        =ᵐ[volume] ((Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) ∘ φ) := by
      apply ae_eq_comp ((measurePreserving_pAct g⁻¹).measurable.aemeasurable)
      rw [hmap]
      exact hcoe
    exact h1
  -- a igualdade em Lp forçaria indicator∘φ =ᵃᵉ indicator
  have hae : (fun x => (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x))
      =ᵐ[volume] (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) := by
    calc (fun x => (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x))
        =ᵐ[volume] (fun x => (F : (Fin 4 → ℝ) → ℂ) (φ x)) := hcomp.symm
      _ =ᵐ[volume] regularRep g F := hUF.symm
      _ =ᵐ[volume] (F : (Fin 4 → ℝ) → ℂ) := by rw [heq]
      _ =ᵐ[volume] (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) := hcoe
  -- mas as duas funções diferem em TODA a bola B(x₀, δ), de medida positiva
  have hdiff : Metric.ball x₀ δ
      ⊆ {x | (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x)
             ≠ (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) x} := by
    intro x hx
    have hin : x ∈ Metric.ball x₀ r :=
      mem_ball.mpr (lt_of_lt_of_le (mem_ball.mp hx) hδr)
    have hout : φ x ∉ Metric.ball x₀ r := by
      intro hmem
      have h1 : dist (φ x) y₀ < r := himage x hx
      have h2 : dist (φ x) x₀ < r := mem_ball.mp hmem
      have h3 : dist y₀ x₀ ≤ dist y₀ (φ x) + dist (φ x) x₀ := dist_triangle _ _ _
      rw [dist_comm y₀ (φ x)] at h3
      have : dist y₀ x₀ < 2 * r := by linarith
      rw [hr] at this
      linarith [hd]
    show (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x)
        ≠ (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) x
    rw [Set.indicator_of_notMem hout, Set.indicator_of_mem hin]
    norm_num
  have hnull : volume {x | (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) (φ x)
      ≠ (Metric.ball x₀ r).indicator (fun _ => (1 : ℂ)) x} = 0 := by
    exact hae
  have hpos : (0 : ENNReal) < volume (Metric.ball x₀ δ) :=
    measure_ball_pos volume x₀ hδpos
  have : volume (Metric.ball x₀ δ) = 0 :=
    le_antisymm (hnull ▸ measure_mono hdiff) zero_le
  rw [this] at hpos
  exact lt_irrefl 0 hpos

/-- o boost puro como elemento de Poincaré. -/
def boostElement (χ : ℝ) : PoincareGroup := ⟨0, theBoost χ⟩

theorem boostElement_ne_one (χ : ℝ) (hχ : χ ≠ 0) : boostElement χ ≠ 1 := by
  intro h
  have hlor := congrArg PoincareGroup.lor h
  exact boost_ne_one χ hχ (by
    show theBoost χ = 1
    exact hlor)

/-- [KERNEL] ★★ O SETOR QUE ERA CEGO AGORA É VISTO: o boost (χ ≠ 0)
    MOVE vetores de L² — a direção que a fibra do v116 não via
    (`proper_sector_fibers_blind`) age NÃO-trivialmente na
    representação regular. -/
theorem regularRep_moves_boost (χ : ℝ) (hχ : χ ≠ 0) :
    ∃ F : SpacetimeL2, regularRep (boostElement χ) F ≠ F :=
  regularRep_faithful (boostElement χ) (boostElement_ne_one χ hχ)

/-- [KERNEL] ★ a morada é genuinamente ∞-dimensional (herda o padrão do
    programa: L² sobre um espaço sem átomos não é finito-dim; aqui basta
    o não-trivial: a bola unitária tem indicador não-nulo). -/
theorem spacetimeL2_nontrivial : ∃ F : SpacetimeL2, F ≠ 0 := by
  refine ⟨ballIndicator 0 1, fun h => ?_⟩
  have hcoe := ballIndicator_coe (0 : Fin 4 → ℝ) 1
  rw [h] at hcoe
  have hzero : ((0 : SpacetimeL2) : (Fin 4 → ℝ) → ℂ) =ᵐ[volume] 0 :=
    Lp.coeFn_zero ℂ 2 volume
  have hae : (Metric.ball (0 : Fin 4 → ℝ) 1).indicator (fun _ => (1 : ℂ))
      =ᵐ[volume] 0 := (hcoe.symm.trans hzero)
  have hdiff : Metric.ball (0 : Fin 4 → ℝ) 1
      ⊆ {x | (Metric.ball (0 : Fin 4 → ℝ) 1).indicator (fun _ => (1 : ℂ)) x
             ≠ (0 : (Fin 4 → ℝ) → ℂ) x} := by
    intro x hx
    show (Metric.ball (0 : Fin 4 → ℝ) 1).indicator (fun _ => (1 : ℂ)) x ≠ 0
    rw [Set.indicator_of_mem hx]
    norm_num
  have hnull : volume {x | (Metric.ball (0 : Fin 4 → ℝ) 1).indicator
      (fun _ => (1 : ℂ)) x ≠ (0 : (Fin 4 → ℝ) → ℂ) x} = 0 := hae
  have hpos : (0 : ENNReal) < volume (Metric.ball (0 : Fin 4 → ℝ) 1) :=
    measure_ball_pos volume 0 one_pos
  have : volume (Metric.ball (0 : Fin 4 → ℝ) 1) = 0 :=
    le_antisymm (hnull ▸ measure_mono hdiff) zero_le
  rw [this] at hpos
  exact lt_irrefl 0 hpos

end

end TGLExt
