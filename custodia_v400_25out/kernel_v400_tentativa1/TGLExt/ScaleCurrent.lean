import TGLExt.MixedLadder

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A CORRENTE J EM TODA ESCALA: a corrente está fechada; o fator é o muro
  [TGLExt — v131, a síntese do operador "fechamos toda a corrente"]

O operador (20/07/2026): "a corrente J — a corrente modular — é o módulo que
falta ao completamento fraco-*. Fechamos toda a corrente."

Esta pedra REÚNE, num único enunciado, a corrente J em TODA escala — o que já
estava provado desde a v124/v125, agora explícito como "toda a corrente":

* `current_at_every_scale` — a corrente (`chainUp N`/`chainDown N`, as palavras
  ascendente/descendente) carrega a razão modular `λ^(N+1)` em TODO andar N
  (`powers_ladder`); 0 está no fecho do espectro de razões (a marca de III);
  e nenhum piso tracial sobrevive à escada;
* `current_iii1_mark` — a marca de III₁ HABITADA: o par incomensurável
  (1/2, 1/3) gera espectro de razões log-DENSO (`the_mixing_mark`), com a
  corrente carregando a razão em toda escala. A corrente J está FECHADA:
  as duas faces conjugadas em cada andar, a razão em toda escala, o espectro
  denso — todas as assinaturas de III₁.

O MURO, NOMEADO SEM VÉU (o que o código já dizia em v124 e v125): o FATOR —
o limite indutivo FRACO-* da escada com o estado-produto (ITPFI; o III₁ de
Araki–Woods como OBJETO de von Neumann). Isso exige teoria de álgebras de von
Neumann (fecho fraco-*, bicomutante no sentido de operadores, Tomita–Takesaki
de vN, unicidade de Connes do fator hiperfinito III₁) — AUSENTE da mathlib de
hoje. A corrente está fechada; o objeto-limite é o muro. O gate segue
fail-closed em `qgClosureCertificateV2` (reservado): a assinatura NÃO é o
objeto, e a régua não cunha o objeto sobre a assinatura.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix

noncomputable section

/-! ## A — a corrente J em toda escala (a razão modular em todo andar) -/

/-- [KERNEL] ★★★ A CORRENTE J EM TODA ESCALA: para `λ ∈ (0,1)`, a corrente
    (`chainUp N`/`chainDown N`) carrega a razão modular `λ^(N+1)` em TODO
    andar; 0 está no fecho do espectro de razões (marca de III); nenhum piso
    tracial sobrevive. A corrente está fechada em toda escala. -/
theorem current_at_every_scale (l : ℝ) (hl0 : 0 < l) (hl1 : l < 1) :
    (∀ N : ℕ, RatioWitness (chainDensity l N) (chainUp N) (chainDown N)
        (l ^ (N + 1)))
    ∧ ((0 : ℝ) ∈ closure (Set.range fun N : ℕ => l ^ N))
    ∧ (∀ c : ℝ, 0 < c → ∃ N : ℕ, l ^ N < c) :=
  ⟨powers_ladder l hl0,
   zero_mem_closure_ratio_spectrum l (le_of_lt hl0) hl1,
   fun c hc => no_trace_floor l hl1 c hc⟩

/-! ## B — a marca de III₁ habitada com a corrente (o par 1/2, 1/3) -/

/-- [KERNEL] ★★★ A MARCA DE III₁ COM A CORRENTE: o par incomensurável
    (1/2, 1/3) gera espectro de razões log-DENSO (a S-invariante toca todo
    ponto — III₁, não III_λ), com a corrente carregando a razão em toda
    escala. A assinatura de III₁ está completa; falta o fator (o muro). -/
theorem current_iii1_mark :
    Dense ((AddSubgroup.closure
      {Real.log ((1 : ℝ) / 2), Real.log ((1 : ℝ) / 3)}
      : AddSubgroup ℝ) : Set ℝ)
    ∧ (∀ N : ℕ, RatioWitness (chainDensity (1 / 2) N) (chainUp N) (chainDown N)
        ((1 / 2) ^ (N + 1))) :=
  ⟨the_mixing_mark, powers_ladder (1 / 2) (by norm_num)⟩

end

end TGLExt
