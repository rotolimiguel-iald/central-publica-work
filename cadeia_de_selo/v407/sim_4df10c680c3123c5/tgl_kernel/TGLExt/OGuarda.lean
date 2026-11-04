import TGLExt.TheFlowLawContrast
set_option autoImplicit false

/-!
Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `73466598d3419fb0`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; compilada no sandbox da v407 (k407c/final), so no trio.

Fala do operador (02/11/2026): K como leitura que confessa o pagamento, verificacao, guarda da travessia.
Aqui so o que um guarda precisa cumprir, escrito de modo que possa falhar:
ler so as bordas; recibo fiel; so carimbar quem atravessa; quem desce paga; o que falta tende a 1 e nao
chega a 1 antes do limite.

K aqui e o fator de Hubble, homonimo do K modular. Nada disto diz que a natureza realiza K: `E` e dado.
K sozinho nao confere nada: e numero para toda `E` positiva. A recusa esta na comparacao, ver `AChaveDaGuarda`.

DOIS LIMITES, que nao se confundem. (a) Se `E` tende a `L > 0` (a fronteira silencia): a cobranca PARA, parcial;
`o_que_falta_tende_a_um`. `w -> -1` sozinho nao basta: a hipotese e `E -> L > 0`. Este NAO e o Tetelestai do kernel.
(b) Se `E` cresce sem limite (rumo a origem): `1 - 1/K` tende a 1 e fica abaixo de 1 em todo ponto finito;
`a_cobranca_tende_a_um`, `a_cobranca_nunca_completa`. Esta e a forma de `the_payment_completes_only_in_the_limit`,
sem ligacao de termo entre as duas pedras. Ler (b) como o Tetelestai e leitura [ONTO].
-/

namespace TGLExt.OGuarda

open Filter Topology

noncomputable section

/-- o fator da lei, entre a entrada `a` e a saida `b`. -/
def K (β : ℝ) (E : ℝ → ℝ) (a b : ℝ) : ℝ := (E b / E a) ^ ((2 / 3 : ℝ) * β)

/-- o que falta pagar de `a` ate o limite `L`. -/
def falta (β : ℝ) (E : ℝ → ℝ) (L a : ℝ) : ℝ := (E a / L) ^ ((2 / 3 : ℝ) * β)

variable {β L : ℝ} {E : ℝ → ℝ} {a b c : ℝ}

/-- o recibo so depende das bordas: nada da estrada entra. -/
theorem o_recibo_le_so_as_bordas (ha : 0 < E a) (hb : 0 < E b) :
    Real.log (K β E a b) = (2 / 3 : ℝ) * β * (Real.log (E b) - Real.log (E a)) := by
  unfold K
  rw [Real.log_rpow (div_pos hb ha), Real.log_div hb.ne' ha.ne']

/-- recibo fiel: com a mesma entrada, recibos iguais so para saidas iguais. -/
theorem o_recibo_e_fiel (hβ : β ≠ 0) (ha : 0 < E a) (hb : 0 < E b) (hc : 0 < E c) :
    K β E a b = K β E a c ↔ E b = E c := by
  have hr : (2 / 3 : ℝ) * β ≠ 0 := mul_ne_zero (by norm_num) hβ
  unfold K
  rw [Real.rpow_left_inj (div_pos hb ha).le (div_pos hc ha).le hr]
  constructor
  · intro h
    exact (div_left_inj' ha.ne').mp h
  · intro h
    rw [h]

/-- so carimba quem atravessa: K = 1 exatamente quando entrada e saida coincidem. -/
theorem so_carimba_quem_atravessa (hβ : β ≠ 0) (ha : 0 < E a) (hb : 0 < E b) :
    K β E a b = 1 ↔ E a = E b := by
  have hr : (2 / 3 : ℝ) * β ≠ 0 := mul_ne_zero (by norm_num) hβ
  unfold K
  constructor
  · intro h
    have h1 : (E b / E a) ^ ((2 / 3 : ℝ) * β) = (1 : ℝ) ^ ((2 / 3 : ℝ) * β) := by
      rw [h, Real.one_rpow]
    have h2 := (Real.rpow_left_inj (div_pos hb ha).le zero_le_one hr).mp h1
    exact ((div_eq_one_iff_eq ha.ne').mp h2).symm
  · intro h
    rw [h, div_self hb.ne', Real.one_rpow]

/-- quem desce paga: com custo positivo e `E` maior na saida, K passa de 1. -/
theorem quem_desce_paga (hβ : 0 < β) (ha : 0 < E a) (hab : E a < E b) : 1 < K β E a b := by
  unfold K
  apply Real.one_lt_rpow
  · rw [one_lt_div ha]
    exact hab
  · positivity

/-- a conta fecha: do limite ate `b` e o pago de `a` a `b` vezes o que faltava de `a` ate o limite. -/
theorem a_conta_fecha (hL : 0 < L) (ha : 0 < E a) (hb : 0 < E b) :
    (E b / L) ^ ((2 / 3 : ℝ) * β) = K β E a b * falta β E L a := by
  unfold K falta
  rw [← Real.mul_rpow (div_pos hb ha).le (div_pos ha hL).le]
  congr 1
  field_simp

/-- se `E` tende a `L`, o que falta pagar tende a 1. -/
theorem o_que_falta_tende_a_um {ι : Type*} {l : Filter ι} {u : ι → ℝ} (hL : 0 < L)
    (h : Tendsto (fun i => E (u i)) l (𝓝 L)) :
    Tendsto (fun i => falta β E L (u i)) l (𝓝 1) := by
  unfold falta
  have h1 : Tendsto (fun i => E (u i) / L) l (𝓝 (L / L)) := h.div_const L
  rw [div_self hL.ne'] at h1
  have h2 := h1.rpow_const (p := (2 / 3 : ℝ) * β) (Or.inl one_ne_zero)
  simpa using h2

/-- antes do limite, sempre falta: com `E a` acima de `L`, o resto passa de 1. -/
theorem antes_do_limite_sempre_falta (hβ : 0 < β) (hL : 0 < L) (hE : L < E a) :
    1 < falta β E L a := by
  unfold falta
  apply Real.one_lt_rpow
  · rw [one_lt_div hL]
    exact hE
  · positivity

/-- rumo a origem a cobranca tende a 1: `E` sem limite leva `1 - 1/K` a 1. -/
theorem a_cobranca_tende_a_um {ι : Type*} {l : Filter ι} {u : ι → ℝ} (hβ : 0 < β) (ha : 0 < E a)
    (h : Tendsto (fun i => E (u i)) l atTop) :
    Tendsto (fun i => 1 - (K β E a (u i))⁻¹) l (𝓝 1) := by
  have hr : 0 < (2 / 3 : ℝ) * β := by positivity
  have h1 : Tendsto (fun i => E (u i) / E a) l atTop := h.atTop_div_const ha
  have h2 : Tendsto (fun i => K β E a (u i)) l atTop := (tendsto_rpow_atTop hr).comp h1
  have h3 : Tendsto (fun i => (K β E a (u i))⁻¹) l (𝓝 0) := h2.inv_tendsto_atTop
  simpa using tendsto_const_nhds.sub h3

/-- em ponto finito a cobranca nao se completa: `1 - 1/K` fica abaixo de 1. -/
theorem a_cobranca_nunca_completa (ha : 0 < E a) (hb : 0 < E b) : 1 - (K β E a b)⁻¹ < 1 := by
  have hk : 0 < K β E a b := Real.rpow_pos_of_pos (div_pos hb ha) _
  have := inv_pos.mpr hk
  linarith

end

end TGLExt.OGuarda
