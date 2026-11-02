import TGLExt.AnsatzEinstein

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A LUZ QUE CAIU: sem queda, sem geometria
  [TGLExt — v110, o incremento 30 do programa SemifiniteAnalysis]

Derivação do operador (18/07/2026): ESPAÇO-TEMPO = q = LUZ QUE CAIU.
O q do ansatz (g₀₀ = q², o perfil do RELÓGIO) tem a mesma FUNÇÃO
ontológica do q da identidade 1 = q² + α² (a cota REFLETIDA — a luz
que não atravessa) e do fator de campo fraco q = 1 + Φ/c² [KNOWN].
A luz que caiu é a que ficou marcando o tempo. Esta pedra dá o eco
em kernel:

* ★★ `constant_profile_flat` — SEM QUEDA, SEM GEOMETRIA: q constante
  (nenhuma luz caiu de forma desigual) ⟹ R¹₀₀₁ ≡ 0 — o membro
  Minkowski da família;
* ★★ `curvature_implies_fall` — a contrapositiva: CURVATURA ⟹ A LUZ
  CAIU (R¹₀₀₁(s) ≠ 0 ⟹ q NÃO é constante);
* ★ `fall_demands_source_v108` — a queda EXIGE fonte no exemplar:
  G₂₂ = 2/q > 0 (eco do v109 — a luz que caiu É a fonte).

A igualdade numérica q_identidade = q_métrico é REFUTADA POR TIPO
(constante < 1 vs campo ≥ 1): a igualdade é de FUNÇÃO ontológica
(v100). β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] ★★ SEM QUEDA, SEM GEOMETRIA: perfil constante (nenhuma
    queda desigual da luz) ⟹ curvatura nula — o membro Minkowski da
    família do ansatz. -/
theorem constant_profile_flat (c : ℝ) (s : ℝ) :
    ansatzRiemann1001 (fun _ => c) s = 0 := by
  unfold ansatzRiemann1001 ansatzGamma100 ansatzGamma001
  simp

/-- [KERNEL] ★★ A CONTRAPOSITIVA: CURVATURA ⟹ A LUZ CAIU — se
    R¹₀₀₁(s) ≠ 0 então o perfil NÃO é constante (existe queda). -/
theorem curvature_implies_fall (q : ℝ → ℝ) (s : ℝ)
    (hR : ansatzRiemann1001 q s ≠ 0) :
    ¬ ∃ c : ℝ, q = fun _ => c := by
  rintro ⟨c, rfl⟩
  exact hR (constant_profile_flat c s)

/-- [KERNEL] ★ A QUEDA EXIGE FONTE no exemplar do v108: G₂₂ = 2/q > 0
    — a luz que caiu É a fonte (eco do v109). -/
theorem fall_demands_source_v108 (s : ℝ) :
    0 < ansatzG22 qfun s :=
  (static_not_vacuum s).2

/-- [KERNEL] ★★★ A GEOMETRIA É A SEGUNDA VARIAÇÃO INSCRITA NO SETOR
    (o refinamento do operador, 18/07/2026): para q ≠ 0,
    R¹₀₀₁(s) ≠ 0 ⟺ q″(s) ≠ 0 — o setor q não tem geometria em si
    (o VALOR não curva); a geometria é a VARIAÇÃO segunda inscrita
    nele. q é o módulo-portador; a inscrição é a curvatura. -/
theorem geometry_iff_second_variation (q : ℝ → ℝ)
    (hq1 : Differentiable ℝ q) (hq2 : Differentiable ℝ (deriv q))
    (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzRiemann1001 q s ≠ 0 ↔ deriv (deriv q) s ≠ 0 := by
  rw [ansatzRiemann_closed q hq1 hq2 hqne s]
  constructor
  · intro hR hdd
    exact hR (by rw [hdd]; ring)
  · intro hdd hR
    have h : q s * deriv (deriv q) s = 0 := by linarith [neg_eq_zero.mp hR]
    rcases mul_eq_zero.mp h with h1 | h2
    · exact hqne s h1
    · exact hdd h2

/-- [KERNEL — o desenho do tipo, nomeado] ★ TUDO QUE TEM GEOMETRIA É
    PROJETADO: para TODO habitante do contrato da solda, a métrica é
    FORÇADA a ser projeção do frame (g = EᵀηE) — g nunca é campo
    livre; o terceiro movimento do operador (18/07/2026) já era o
    desenho do tipo. -/
theorem geometry_is_projection (S : SolderFieldData) (x : Fin 4 → ℝ) :
    S.g x = solderMetric4 (S.frame.E x) :=
  S.solder_eq x

end

end TGLExt
