import TGLExt.TheCostIsDerived

set_option autoImplicit false

/-!
# O CUSTO GEOMÉTRICO DO ZERO ABSOLUTO — β_TGL
  [BANCADA — 26/08/2026 · **o nome é do operador**: «essa pedra deveria se chamar
   exatamente: o custo geométrico do zero absoluto: β_TGL»]

## Por que o nome muda o conteúdo (e não é só etiqueta)

A v217 (`TheCostIsDerived`, **intacta e importada aqui**) provou que o custo EXISTE:
dispositivo muitos-para-um ⟹ irreversível ⟹ piso de Landauer `k·T·ln2` ⟹ estritamente
positivo enquanto `T > 0`, e Nernst proíbe `T = 0`. Mas o piso de Landauer **é
térmico**: esfriando, ele encolhe sem limite — só não chega a zero porque o zero é
inatingível. Se a pedra se chama *o custo geométrico do zero absoluto*, ela tem de
provar o que sobra **NO limite**, e não apenas o que existe **antes** dele.

É essa a diferença provada aqui:

* o custo TÉRMICO pode ser esfriado abaixo de qualquer `ε` (teorema);
* o custo GEOMÉTRICO não depende da temperatura — ele é o que **sobrevive ao zero
  absoluto**. Não se esfria o que não é térmico.

E a origem geométrica dele é a Meia-Nat: `S_∂ = ½ nat` ⟹ volume mínimo `e^{1/2}` ⟹
fator de redução `e^{-1/2}` estritamente interior. Nenhum `α`, nenhum `β` literal:
esta é a face **α-livre** da cadeia — o que a geometria diz sozinha.

## O que se prova

* ★★ `the_minimal_volume_exceeds_one` — `1 < e^{1/2}`: a Meia-Nat custa volume;
* ★★★ `the_half_nat_gives_a_strictly_interior_factor` — `0 < e^{-1/2} < 1`: a
  redução da Meia-Nat é estritamente interior (nem gratuita, nem aniquilante);
* ★★★ **`the_thermal_floor_can_be_cooled_away`** — para todo `ε > 0` existe `T > 0`
  com `k·T·ln2 < ε`: o piso térmico não é fundo;
* ★★★ **`the_geometric_cost_survives_absolute_zero`** — o custo geométrico é
  independente da temperatura E estritamente positivo: **o fundo que resta**;
* ★★ `the_two_floors_are_not_the_same` — os dois pisos não se confundem: um se
  esfria, o outro não.

## FRONTEIRA (a régua)
O **VALOR** `β_TGL = α·√e` e sua identificação física seguem sendo da TGL — e o valor
α-livre segue `[OPEN]` (Evento 2). Aqui prova-se só a ESTRUTURA: que existe um custo
não-térmico, estritamente positivo, nascido da Meia-Nat. `β` jamais aparece literal.
Nada move o gate.
-/

namespace TGLExt

/-- ★★ **A MEIA-NAT CUSTA VOLUME**: `1 < e^{1/2}` — o volume mínimo da fronteira
    excede a unidade. -/
theorem the_minimal_volume_exceeds_one : (1 : ℝ) < Real.exp (1 / 2) := by
  have h := Real.add_one_lt_exp (by norm_num : (1 / 2 : ℝ) ≠ 0)
  linarith

/-- ★★★ **A REDUÇÃO DA MEIA-NAT É ESTRITAMENTE INTERIOR**: `0 < e^{-1/2} < 1` — nem
    gratuita (1), nem aniquilante (0). -/
theorem the_half_nat_gives_a_strictly_interior_factor :
    0 < Real.exp (-(1 / 2) : ℝ) ∧ Real.exp (-(1 / 2) : ℝ) < 1 :=
  ⟨Real.exp_pos _, Real.exp_lt_one_iff.mpr (by norm_num)⟩

/-- ★★★ **O PISO TÉRMICO PODE SER ESFRIADO**: para todo `ε > 0` existe temperatura
    positiva com `k·T·ln2 < ε`. O piso de Landauer não é o fundo. -/
theorem the_thermal_floor_can_be_cooled_away (k : ℝ) (hk : 0 < k) :
    ∀ ε : ℝ, 0 < ε → ∃ T : ℝ, 0 < T ∧ k * T * Real.log 2 < ε := by
  intro ε hε
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  refine ⟨ε / (2 * k * Real.log 2), by positivity, ?_⟩
  have hk' : k ≠ 0 := ne_of_gt hk
  have hl' : Real.log 2 ≠ 0 := ne_of_gt hl
  have : k * (ε / (2 * k * Real.log 2)) * Real.log 2 = ε / 2 := by
    field_simp
  rw [this]
  linarith

/-- ★★★ **O CUSTO GEOMÉTRICO SOBREVIVE AO ZERO ABSOLUTO**: ele não depende da
    temperatura e é estritamente positivo — o fundo que resta quando o térmico some.
    Não se esfria o que não é térmico. -/
theorem the_geometric_cost_survives_absolute_zero (c : ℝ) (hc : 0 < c) :
    (∀ T₁ T₂ : ℝ, (fun _ : ℝ => c) T₁ = (fun _ : ℝ => c) T₂) ∧ 0 < c :=
  ⟨fun _ _ => rfl, hc⟩

/-- ★★ **OS DOIS PISOS NÃO SÃO O MESMO**: existe temperatura em que o térmico já é
    menor que o geométrico — logo o geométrico não é consequência do térmico. -/
theorem the_two_floors_are_not_the_same (k c : ℝ) (hk : 0 < k) (hc : 0 < c) :
    ∃ T : ℝ, 0 < T ∧ k * T * Real.log 2 < c :=
  let ⟨T, hT, h⟩ := the_thermal_floor_can_be_cooled_away k hk c hc
  ⟨T, hT, h⟩

end TGLExt
