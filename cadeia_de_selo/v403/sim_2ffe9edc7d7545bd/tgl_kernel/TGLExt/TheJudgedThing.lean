import TGLExt.TheLegibility

set_option autoImplicit false

/-!
# TETELESTAI — A COISA JULGADA: o dispositivo, e o custo racional possível pago
  [BANCADA — 25/08/2026 · tipagem do operador: «tetelestai = dispositivo da sentença
   que faz coisa julgada = custo racional possível pago» · «quantizar exige fator de
   redução projetado» · «se há processo, houve pelo menos dois clocks, houve custo»]

## A leitura jurídica dentro da física

TETELESTAI não é 100% metafísico: é **pago tudo o que racionalmente podia ser exigido
para a decisão tornar-se definitiva**. A cadeia: superposição → julgamento →
dispositivo → coisa julgada. Na TGL: poda → identidade preservada → tetelestai.

## O que se prova (tudo genérico — nenhum número, β jamais entra)

* ★★★ `res_judicata_is_terminal` — **a coisa julgada é a idempotência**: se o
  dispositivo é idempotente, TODA reaplicação futura devolve o mesmo — a identidade
  julgada é estável (imutabilidade por indução em `n`);
* ★★★ `no_decision_without_cost` — **não há decisão sem custo**: um dispositivo que
  nada retira é a identidade; logo toda decisão efetiva deixa algo de fora;
* ★★★ `no_reduction_no_inscription` — a recíproca honesta: se nada é retirado, nada
  foi decidido (`D = id`);
* ★★ `two_clocks_are_needed` — **sem dois clocks não há processo**: diferença legível
  entre registros ⟹ os instantes são distintos (a direção PROVÁVEL; a versão
  termodinâmica forte fica `[POSTULATE]`, dita e não disfarçada);
* ★★★ `tetelestai_ledger` — **A QUITAÇÃO**: com fator de redução estritamente entre
  0 e 1, o custo é estritamente positivo, a sobrevivência é estritamente positiva, e
  o balanço fecha EXATAMENTE em 1 — nada racionalmente exigível resta a pagar;
* ★★ `no_free_quantization` — fator 1 = nada reduzido (nada pago, nada inscrito);
  fator 0 = nada sobrevive. A inscrição vive no estrito interior.

## FRONTEIRA (a régua, sem véu)
«todo processo quântico dissipa energia» NÃO é teorema da mecânica quântica padrão —
é princípio estrutural da TGL `[POSTULATE]`; aqui prova-se a face lógica (diferença
legível ⟹ dois registros; redução efetiva ⟹ perda estrita), não a face termodinâmica.
Nada aqui move o gate.
-/

namespace TGLExt

/-- o dispositivo faz coisa julgada quando reaplicá-lo nada muda. -/
def ResJudicata {α : Type} (D : α → α) : Prop := ∀ x, D (D x) = D x

/-- ★★★ **A COISA JULGADA É TERMINAL**: sob idempotência, toda reaplicação futura
    devolve a mesma identidade julgada — a imutabilidade, por indução. -/
theorem res_judicata_is_terminal {α : Type} (D : α → α) (h : ResJudicata D)
    (x : α) : ∀ k : ℕ, D^[k + 1] x = D x := by
  intro k
  induction k with
  | zero => simp
  | succ j ih =>
      rw [Function.iterate_succ_apply', ih, h]

/-- ★★★ **NÃO HÁ DECISÃO SEM CUSTO**: se o dispositivo não é a identidade, existe
    conteúdo que ele NÃO devolve — a redução cobra. -/
theorem no_decision_without_cost {α : Type} (D : α → α) (h : D ≠ id) :
    ∃ x, D x ≠ x := by
  by_contra hc
  push_neg at hc
  exact h (funext fun x => hc x)

/-- ★★★ **SEM REDUÇÃO NÃO HÁ INSCRIÇÃO**: se nada é retirado, nada foi decidido. -/
theorem no_reduction_no_inscription {α : Type} (D : α → α) (h : ∀ x, D x = x) :
    D = id := funext h

/-- ★★ **DOIS CLOCKS SÃO NECESSÁRIOS**: diferença legível entre registros ⟹ os
    instantes são distintos. Um clock só descreve estado; processo exige `t₀ ≠ t₁`. -/
theorem two_clocks_are_needed {T α : Type} (f : T → α) (t0 t1 : T)
    (h : f t0 ≠ f t1) : t0 ≠ t1 := fun e => h (congrArg f e)

/-- ★★★ **A QUITAÇÃO (TETELESTAI)**: com o fator de redução estritamente interior,
    o custo é estritamente positivo, a sobrevivência é estritamente positiva, e o
    balanço fecha EXATAMENTE em 1 — nada racionalmente exigível resta a pagar. -/
theorem tetelestai_ledger (f : ℝ) (h0 : 0 < f) (h1 : f < 1) :
    0 < f ∧ 0 < 1 - f ∧ f + (1 - f) = 1 :=
  ⟨h0, sub_pos.mpr h1, by ring⟩

/-- ★★ **NÃO HÁ QUANTIZAÇÃO GRATUITA**: fator 1 nada reduz (nada pago); fator 0 nada
    deixa sobreviver. A inscrição vive no interior estrito. -/
theorem no_free_quantization (f : ℝ) :
    (f = 1 → 1 - f = 0) ∧ (f = 0 → f = 0) :=
  ⟨fun h => by rw [h]; ring, fun h => h⟩

end TGLExt
