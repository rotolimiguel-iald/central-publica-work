import TGLExt.WordExistence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

/-!
# A PALAVRA EM ∞-DIM: o cálculo funcional com 0 isolado
  [TGLExt — v94, o incremento 11 do programa SemifiniteAnalysis]

O v89 fechou a face finita (a palavra existe SEM diagonalização). Esta
pedra fecha a face INFINITA: para T = T† com 0 ISOLADO no espectro de
S = T·T (a situação de gap dos Three Locks), o cálculo funcional
contínuo cunha a projeção espectral, e Weierstrass no intervalo
[−‖S‖, ‖S‖] fornece as palavras polinomiais que convergem a ela EM
NORMA — logo pontualmente: a SpectralApproximationWitness do v85 VALE
em ∞-dim. Composta com o frame algébrico v80×82×83×84, ela produz o
CANTO DE BREUER CONCRETO com hipóteses puramente ESTRUTURAIS
(auto-adjunção + gap espectral + kernel finito não-trivial).

A ENGENHARIA DA PROVA (as escolhas que a tornam formalizável):
* trabalhar com S = T·T (espectro ⊆ {0} ∪ [g², ∞); ker S = ker T):
  as funções  f(y) = max(0, 1 − (2/g²)y)  e  k(y) = (max(g²/2, y))⁻¹
  são CONTÍNUAS EM TODO ℝ — nenhum indicador descontínuo;
* as identidades valem NO ESPECTRO via `cfc_congr` (id·f = 0 e
  1 − f = k·id em σ(S)) — o homomorfismo cfc faz o resto;
* a UNICIDADE do v88 identifica cfc f S = starProjection(ker T) por
  três cláusulas pontuais (simetria, pouso, fixação) — a idempotência
  vem DE GRAÇA pela identificação;
* Weierstrass em Icc(−‖S‖, ‖S‖) ⊇ σ(S) + `norm_cfc_le` (o cfc é
  isométrico) dão a sequência de palavras; a palavra em T é a palavra
  em S composta com X² e levada a ℂ[X].

O QUE ESTA PEDRA PROVA [KERNEL]:
* ★ `ker_mul_self_eq_ker` — ker(T·T) = ker T para T = T†;
* ★ `cfc_polynomial_eval` — o dicionário palavra↔função: cfc do
  avaliador polinomial = aeval;
* ★★★ `iso_zero_cfc_eq_starProjection` — A PROJEÇÃO ESPECTRAL É O
  NOME: 0 isolado ⟹ cfc da função-chapéu = P_{ker T};
* ★★★ `spectral_witness_of_isolated_zero` — A PALAVRA EM ∞-DIM:
  0 isolado ⟹ SpectralApproximationWitness T;
* ★★★★ `concrete_breuer_corner_infinite` — O CANTO DE BREUER CONCRETO
  EM ∞-DIM: T = T†, gap, kernel finito ≠ ⊥ ⟹ P ∈ {T}″ ∩ {T}′ com
  0 < τ(ker) < ∞ e τ(kerᗮ) = ⊤ — a testemunha deixou de ser hipótese.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Polynomial

noncomputable section

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★ ker(T·T) = ker T para T = T†: o quadrado não esconde
    kernel (‖Tx‖² = ⟪T(Tx), x⟫ via o adjunto). -/
theorem ker_mul_self_eq_ker (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) :
    (T * T).ker = T.ker := by
  ext x
  constructor
  · intro hx
    have hx0 : (T * T) x = 0 := LinearMap.mem_ker.mp hx
    have hswap := ContinuousLinearMap.adjoint_inner_left T (T x) x
    rw [hsa] at hswap
    have hnorm : inner ℂ (T x) (T x) = (0 : ℂ) := by
      rw [hswap]
      calc inner ℂ x (T (T x)) = inner ℂ x ((T * T) x) := rfl
        _ = inner ℂ x (0 : H) := by rw [hx0]
        _ = 0 := inner_zero_right x
    exact LinearMap.mem_ker.mpr (inner_self_eq_zero.mp hnorm)
  · intro hx
    have hx0 : T x = 0 := LinearMap.mem_ker.mp hx
    refine LinearMap.mem_ker.mpr ?_
    calc (T * T) x = T (T x) := rfl
      _ = T 0 := by rw [hx0]
      _ = 0 := map_zero T

/-- [KERNEL] ★ o dicionário palavra↔função: o cfc do avaliador
    polinomial é o aeval (indução em monômios; o homomorfismo faz o
    resto). -/
theorem cfc_polynomial_eval (S : H →L[ℂ] H) (hS : IsSelfAdjoint S)
    (p : Polynomial ℝ) :
    cfc (fun x : ℝ => p.eval x) S = Polynomial.aeval S p := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
    have h1 : (fun x : ℝ => (p + q).eval x)
        = fun x : ℝ => p.eval x + q.eval x := by
      funext x
      rw [Polynomial.eval_add]
    rw [h1, cfc_add S (fun x : ℝ => p.eval x) (fun x : ℝ => q.eval x)
          p.continuous.continuousOn q.continuous.continuousOn,
        hp, hq, map_add]
  | monomial n c =>
    have h1 : (fun x : ℝ => (Polynomial.monomial n c).eval x)
        = fun x : ℝ => c • (id x : ℝ) ^ n := by
      funext x
      rw [Polynomial.eval_monomial, smul_eq_mul, id_eq]
    rw [h1, cfc_smul c (fun x : ℝ => (id x : ℝ) ^ n) S
          (Continuous.continuousOn (continuous_id.pow n)),
        cfc_pow (id : ℝ → ℝ) n S (Continuous.continuousOn continuous_id),
        cfc_id ℝ S hS, Polynomial.aeval_monomial, ← Algebra.smul_def]

section IsolatedZero

variable (T : H →L[ℂ] H)

/-- a função-chapéu: 1 no zero, 0 a partir de g2 — contínua em todo ℝ. -/
private def fhat (g2 : ℝ) : ℝ → ℝ := fun y => max 0 (1 - (2 / g2) * y)

/-- o inverso amansado: (max(g2/2, y))⁻¹ — contínuo e nunca singular. -/
private def kinv (g2 : ℝ) : ℝ → ℝ := fun y => (max (g2 / 2) y)⁻¹

private lemma fhat_continuous (g2 : ℝ) : Continuous (fhat g2) := by
  unfold fhat
  exact continuous_const.max
    (continuous_const.sub (continuous_const.mul continuous_id))

private lemma kinv_continuous {g2 : ℝ} (hg : 0 < g2) : Continuous (kinv g2) := by
  unfold kinv
  refine Continuous.inv₀ (continuous_const.max continuous_id) fun y => ?_
  have hpos : 0 < max (g2 / 2) y :=
    lt_of_lt_of_le (by linarith) (le_max_left _ _)
  exact ne_of_gt hpos

private lemma fhat_at_zero (g2 : ℝ) : fhat g2 0 = 1 := by
  unfold fhat
  norm_num

private lemma fhat_at_ge {g2 : ℝ} (hg : 0 < g2) {y : ℝ} (hy : g2 ≤ y) :
    fhat g2 y = 0 := by
  unfold fhat
  have h1 : (2 : ℝ) ≤ 2 / g2 * y := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hg]
    nlinarith
  exact max_eq_left (by linarith)

/-- [KERNEL] ★★★ A PROJEÇÃO ESPECTRAL É O NOME: com 0 isolado no
    espectro de S = T·T, o cfc da função-chapéu é EXATAMENTE a projeção
    ortogonal sobre ker T — simétrica (cfc_predicate), pousa no kernel
    (S∘P = 0 via id·f =σ 0), fixa o kernel (1−P = K∘S via
    1−f =σ k·id); a unicidade do v88 fecha a identificação. -/
theorem iso_zero_cfc_eq_starProjection
    (hsa : ContinuousLinearMap.adjoint T = T)
    {g2 : ℝ} (hg : 0 < g2)
    (hiso : ∀ y ∈ spectrum ℝ (T * T), y = 0 ∨ g2 ≤ y) :
    cfc (fhat g2) (T * T) = (T.ker).starProjection := by
  have hS : IsSelfAdjoint (T * T) := by
    have h : star (T * T) = T * T := by
      rw [star_mul, ContinuousLinearMap.star_eq_adjoint, hsa]
    exact h
  have hker : (T * T).ker = T.ker := ker_mul_self_eq_ker T hsa
  have hcf : ContinuousOn (fhat g2) (spectrum ℝ (T * T)) :=
    (fhat_continuous g2).continuousOn
  have hck : ContinuousOn (kinv g2) (spectrum ℝ (T * T)) :=
    (kinv_continuous hg).continuousOn
  -- pousa: S * P0 = 0 (id·f = 0 no espectro)
  have hSP : (T * T) * cfc (fhat g2) (T * T) = 0 := by
    have h1 : (T * T) * cfc (fhat g2) (T * T)
        = cfc (fun y : ℝ => id y * fhat g2 y) (T * T) := by
      conv_lhs => lhs; rw [← cfc_id ℝ (T * T) hS]
      rw [← cfc_mul (id : ℝ → ℝ) (fhat g2) (T * T)
            (Continuous.continuousOn continuous_id) hcf]
    have h2 : cfc (fun y : ℝ => id y * fhat g2 y) (T * T)
        = cfc (fun _ : ℝ => (0 : ℝ)) (T * T) := by
      refine cfc_congr fun y hy => ?_
      show id y * fhat g2 y = 0
      rw [id_eq]
      rcases hiso y hy with h0 | hge
      · subst h0
        simp
      · rw [fhat_at_ge hg hge, mul_zero]
    rw [h1, h2, cfc_const 0 (T * T) hS, map_zero]
  -- fixa: 1 − P0 = K * S (1−f = k·id no espectro)
  have hfix_op : 1 - cfc (fhat g2) (T * T)
      = cfc (kinv g2) (T * T) * (T * T) := by
    have h1 : (1 : H →L[ℂ] H) - cfc (fhat g2) (T * T)
        = cfc (fun y : ℝ => 1 - fhat g2 y) (T * T) := by
      rw [cfc_sub (fun _ : ℝ => (1 : ℝ)) (fhat g2) (T * T)
            (Continuous.continuousOn continuous_const) hcf,
          cfc_const 1 (T * T) hS, map_one]
    have h2 : cfc (fun y : ℝ => 1 - fhat g2 y) (T * T)
        = cfc (fun y : ℝ => kinv g2 y * id y) (T * T) := by
      refine cfc_congr fun y hy => ?_
      show 1 - fhat g2 y = kinv g2 y * id y
      rw [id_eq]
      rcases hiso y hy with h0 | hge
      · subst h0
        rw [fhat_at_zero]
        simp
      · rw [fhat_at_ge hg hge, sub_zero]
        have hy2 : g2 / 2 ≤ y := by linarith
        have hyne : y ≠ 0 := ne_of_gt (by linarith)
        unfold kinv
        rw [max_eq_right hy2, inv_mul_cancel₀ hyne]
    have h3 : cfc (fun y : ℝ => kinv g2 y * id y) (T * T)
        = cfc (kinv g2) (T * T) * (T * T) := by
      conv_rhs => rhs; rw [← cfc_id ℝ (T * T) hS]
      rw [← cfc_mul (kinv g2) (id : ℝ → ℝ) (T * T) hck
            (Continuous.continuousOn continuous_id)]
    rw [h1, h2, h3]
  -- simétrica: o cfc real preserva a auto-adjunção
  have hsaP : IsSelfAdjoint (cfc (fhat g2) (T * T)) :=
    cfc_predicate (fhat g2) (T * T)
  have hadj : ContinuousLinearMap.adjoint (cfc (fhat g2) (T * T))
      = cfc (fhat g2) (T * T) := by
    rw [← ContinuousLinearMap.star_eq_adjoint]
    exact hsaP
  have hP : ∀ u v : H, inner ℂ (cfc (fhat g2) (T * T) u) v
      = inner ℂ u (cfc (fhat g2) (T * T) v) := by
    intro u v
    have h := ContinuousLinearMap.adjoint_inner_left
      (cfc (fhat g2) (T * T)) v u
    rwa [hadj] at h
  -- as duas cláusulas pontuais
  have hland : ∀ x : H, cfc (fhat g2) (T * T) x ∈ T.ker := by
    intro x
    rw [← hker]
    refine LinearMap.mem_ker.mpr ?_
    calc (T * T) (cfc (fhat g2) (T * T) x)
        = ((T * T) * cfc (fhat g2) (T * T)) x := rfl
      _ = (0 : H →L[ℂ] H) x := by rw [hSP]
      _ = 0 := rfl
  have hfix : ∀ x ∈ T.ker, cfc (fhat g2) (T * T) x = x := by
    intro x hx
    have hSx : (T * T) x = 0 := LinearMap.mem_ker.mp (hker ▸ hx)
    have h1 : ((1 : H →L[ℂ] H) - cfc (fhat g2) (T * T)) x = 0 := by
      rw [hfix_op]
      calc (cfc (kinv g2) (T * T) * (T * T)) x
          = (cfc (kinv g2) (T * T)) ((T * T) x) := rfl
        _ = (cfc (kinv g2) (T * T)) 0 := by rw [hSx]
        _ = 0 := map_zero _
    have h2 : x - cfc (fhat g2) (T * T) x = 0 := by
      calc x - cfc (fhat g2) (T * T) x
          = ((1 : H →L[ℂ] H) - cfc (fhat g2) (T * T)) x := by
            rw [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply]
        _ = 0 := h1
    exact (sub_eq_zero.mp h2).symm
  -- a unicidade do v88 fecha
  exact selfadjoint_idempotent_eq_starProjection T.ker
    (cfc (fhat g2) (T * T)) hP hland hfix

/-- [KERNEL] ★★★ A PALAVRA EM ∞-DIM: 0 isolado no espectro de T·T ⟹
    a testemunha espectral do v85 EXISTE — Weierstrass em
    Icc(−‖S‖, ‖S‖) ⊇ σ(S) dá palavras reais p_n com
    ‖p_n(S) − P_{ker T}‖ ≤ 1/(n+1) (o cfc é isométrico), e a palavra
    complexa q_n := (p_n ∘ X²) levada a ℂ[X] converge PONTUALMENTE. -/
theorem spectral_witness_of_isolated_zero [Nontrivial H]
    (hsa : ContinuousLinearMap.adjoint T = T)
    {g2 : ℝ} (hg : 0 < g2)
    (hiso : ∀ y ∈ spectrum ℝ (T * T), y = 0 ∨ g2 ≤ y) :
    SpectralApproximationWitness T := by
  have hS : IsSelfAdjoint (T * T) := by
    have h : star (T * T) = T * T := by
      rw [star_mul, ContinuousLinearMap.star_eq_adjoint, hsa]
    exact h
  have hproj : cfc (fhat g2) (T * T) = (T.ker).starProjection :=
    iso_zero_cfc_eq_starProjection T hsa hg hiso
  -- o espectro mora no intervalo de Weierstrass
  have hicc : ∀ y ∈ spectrum ℝ (T * T), y ∈ Set.Icc (-‖T * T‖) ‖T * T‖ := by
    intro y hy
    have hb : ‖y‖ ≤ ‖T * T‖ := spectrum.norm_le_norm_of_mem hy
    rw [Real.norm_eq_abs] at hb
    exact Set.mem_Icc.mpr (abs_le.mp hb)
  -- Weierstrass: as palavras reais no intervalo
  have hWeier : ∀ n : ℕ, ∃ p : Polynomial ℝ,
      ∀ y ∈ Set.Icc (-‖T * T‖) ‖T * T‖,
        |p.eval y - fhat g2 y| < 1 / ((n : ℝ) + 1) := fun n =>
    exists_polynomial_near_of_continuousOn (-‖T * T‖) ‖T * T‖ (fhat g2)
      ((fhat_continuous g2).continuousOn) (1 / ((n : ℝ) + 1)) (by positivity)
  choose ps hps using hWeier
  -- a palavra real avaliada em S aproxima a projeção EM NORMA
  have hnorm : ∀ n : ℕ,
      ‖Polynomial.aeval (T * T) (ps n) - (T.ker).starProjection‖
        ≤ 1 / ((n : ℝ) + 1) := by
    intro n
    rw [← hproj, ← cfc_polynomial_eval (T * T) hS (ps n),
        ← cfc_sub (fun y : ℝ => (ps n).eval y) (fhat g2) (T * T)
          ((ps n).continuous.continuousOn)
          ((fhat_continuous g2).continuousOn)]
    refine norm_cfc_le (by positivity) fun y hy => ?_
    show ‖(ps n).eval y - fhat g2 y‖ ≤ 1 / ((n : ℝ) + 1)
    rw [Real.norm_eq_abs]
    exact le_of_lt (hps n y (hicc y hy))
  -- a palavra complexa em T: q_n(T) = p_n(T·T)
  have hword : ∀ n : ℕ,
      Polynomial.aeval T (((ps n).comp (Polynomial.X ^ 2)).map (algebraMap ℝ ℂ))
        = Polynomial.aeval (T * T) (ps n) := by
    intro n
    have hX2 : Polynomial.aeval T ((Polynomial.X : Polynomial ℝ) ^ 2)
        = T * T := by
      rw [map_pow, Polynomial.aeval_X, sq]
    rw [Polynomial.aeval_map_algebraMap, Polynomial.aeval_comp, hX2]
  refine ⟨fun n => ((ps n).comp (Polynomial.X ^ 2)).map (algebraMap ℝ ℂ),
    fun x => ?_⟩
  rw [tendsto_iff_norm_sub_tendsto_zero]
  have hb : ∀ n : ℕ,
      ‖(Polynomial.aeval T
            (((ps n).comp (Polynomial.X ^ 2)).map (algebraMap ℝ ℂ))) x
          - (T.ker).starProjection x‖
        ≤ (1 / ((n : ℝ) + 1)) * ‖x‖ := by
    intro n
    have h1 : (Polynomial.aeval T
            (((ps n).comp (Polynomial.X ^ 2)).map (algebraMap ℝ ℂ))) x
          - (T.ker).starProjection x
        = (Polynomial.aeval (T * T) (ps n) - (T.ker).starProjection) x := by
      rw [ContinuousLinearMap.sub_apply, hword n]
    rw [h1]
    calc ‖(Polynomial.aeval (T * T) (ps n) - (T.ker).starProjection) x‖
        ≤ ‖Polynomial.aeval (T * T) (ps n) - (T.ker).starProjection‖ * ‖x‖ :=
          ContinuousLinearMap.le_opNorm _ x
      _ ≤ (1 / ((n : ℝ) + 1)) * ‖x‖ :=
          mul_le_mul_of_nonneg_right (hnorm n) (norm_nonneg x)
  have hlim : Filter.Tendsto (fun n : ℕ => (1 / ((n : ℝ) + 1)) * ‖x‖)
      Filter.atTop (nhds (0 * ‖x‖)) :=
    Filter.Tendsto.mul_const ‖x‖ tendsto_one_div_add_atTop_nhds_zero_nat
  rw [zero_mul] at hlim
  exact squeeze_zero (fun n => norm_nonneg _) hb hlim

/-- [KERNEL] ★★★★ O CANTO DE BREUER CONCRETO EM ∞-DIM: hipóteses
    puramente ESTRUTURAIS — T = T†, 0 isolado no espectro de T·T,
    kernel não-trivial sob gaiola finita, H ∞-dim — e o canto INTEIRO
    conclui: P_{ker T} ∈ {T}″ ∧ P ∈ {T}′ ∧ 0 < τ(ker) < ∞ ∧
    τ(kerᗮ) = ⊤. A testemunha do v85 DEIXOU DE SER HIPÓTESE: ela é
    TEOREMA (Weierstrass + cfc). A palavra está fechada. -/
theorem concrete_breuer_corner_infinite (hH : ¬FiniteDimensional ℂ H)
    (hsa : ContinuousLinearMap.adjoint T = T)
    {g2 : ℝ} (hg : 0 < g2)
    (hiso : ∀ y ∈ spectrum ℝ (T * T), y = 0 ∨ g2 ≤ y)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥)
    (hle : T.ker ≤ gp) (hgp : FiniteDimensional ℂ gp) :
    ((T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer ∧
      (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau T.ker ∧
          (semifiniteDimTrace ℂ H).tau T.ker < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) := by
  haveI : Nontrivial H := by
    obtain ⟨x, -, hx0⟩ := (Submodule.ne_bot_iff _).mp hker
    exact ⟨⟨x, 0, hx0⟩⟩
  exact concrete_breuer_corner_conditional hH T hsa
    (spectral_witness_of_isolated_zero T hsa hg hiso) gp hker hle hgp

end IsolatedZero

end

end TGLExt
