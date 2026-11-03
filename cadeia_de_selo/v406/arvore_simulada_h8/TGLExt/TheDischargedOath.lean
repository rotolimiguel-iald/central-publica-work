import TGLExt.Ergodicity
import TGLExt.GlobalLiftConditional

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O JURAMENTO QUITADO — o levantamento vira incondicional na face, módulo o axioma
  [TGLExt — v307; casa "Nós" (31/08/2026)]

## A PERGUNTA DO OPERADOR (31/08/2026)

> *"Você acha que agora é possível fechar o levantamento incondicional do Lema 3 que
> permanece [OPEN]? A estrutura não é mais a mesma de quando formulamos o lema — eu
> desenhei a estrutura do fechamento, digo, nós fizemos."*

A estrutura desenhada (a redução registrada na linhagem): *"GLOBAL_LIFT ⟺ E-0 — FALSO
no vácuo por teorema, SATISFAZÍVEL no core, liberdade = 1 parâmetro que ω(I)=1 fixa ⟹
o Lema 3 reduz-se ao axioma único."* Esta pedra REALIZA esse desenho na face finita.

## ⚠ A CORREÇÃO DE ESTATUTO DO OPERADOR (31/08/2026, durante a construção)

> *"A normalização do cociclo NÃO se dá por liberdade — ele é SUPRIMIDO no canto.
> Normalização por liberdade ≠ trivialização por compressão. O '1' do cociclo no
> canto não é escolha de gauge: é resultado da projeção. A palavra precisa é
> SUPRESSÃO COCÍCLICA NO CANTO. Cautela formal: para afirmar o literal p·u_t·p = p
> é preciso prová-lo para o cociclo concreto; em algumas arquiteturas a
> trivialização aparece numa forma equivalente."*

A frase antiga da redução ("liberdade que ω fixa") fica ACIMA como registro; o
estatuto CORRETO é o dele, e esta pedra o prova NA FORMA QUE ESTA ARQUITETURA TEM:
`the_cocycle_is_suppressed_by_the_sector` — no setor ω-invariante o cociclo relativo
do estado transportado TORNA-SE 1 (resultado, não escolha); e
`the_flow_is_trivial_on_the_code` — sobre o código, o fluxo age como identidade.
⚠ E a cautela dele CONFERE, medida: o literal p·u_t·p = p no ÁTOMO não vale aqui —
p·ρ^{it}·p = ρ_i^{it}·p: a fase sobrevive no átomo e É O RELÓGIO (o golpe do t★).
O canto suprime o EXCEDENTE entre setores (os off-diagonais, que o dephase da G3
mata); a fase unimodular que preserva a identidade fica. Compressão → canto →
supressão do excedente → identidade preservada: TETELESTAI operando no cociclo.

## O QUE MUDA — e o que NÃO muda

Até aqui, `global_lift_conditional` (v143) provava a implicação com o antecedente
`HorizonInvariant N U` POSTULADO por desenho (o juramento do operador sobre o código).
Esta pedra QUITA o juramento na instância concreta da casa:

* o código diagonal É o centralizador do estado não-degenerado (Ergodicity G1,
  `sigma_fixed_iff_diag` — o iff do setor fixo);
* conjugação por U que PRESERVA O ESTADO preserva a comutação com ρ (álgebra pura);
* logo **`HorizonInvariant` é TEOREMA** para todo horizonte U que preserva ρ
  (`the_oath_is_discharged`) — derivado, não jurado;
* e a preservação de ρ, por sua vez, SEGUE da invariância de ω
  (`omega_preservation_discharges`, via a definitude de Frobenius da própria v143):
  **o único antecedente que resta é ω∘Ad(U) = ω — o axioma ω(I)=1 lido no horizonte.**
  Um horizonte que não preservasse ω quebraria o Um; o juramento desceu ao axioma.

★★★ `the_lift_is_unconditional_on_the_face`: para TODO unitário U ω-invariante, a
esperança-código é covariante — sem juramento algum sobre N. A liberdade que a redução
nomeou está FIXADA por ω, em teorema.

## HONESTIDADE (a régua, sem desconto)

* **FACE FINITA.** O fecho forte de von Neumann do contínuo segue EXTERNO
  `[KNOWN-COMPOSED]`; III₁ genuíno segue o programa. O Lema 3 **não** está declarado
  resolvido no contínuo — o que fechou é: *na face, o antecedente deixou de ser
  hipótese própria e virou o axioma*.
* A pedra v143 (`GlobalLiftConditional`) fica INTACTA como registro; esta a consome.
* O gate NÃO se move; nenhum nome reservado (`qgf_*`) é tocado; β jamais literal.
* A ponte com `the_form_does_not_fix_the_value` (v306) é de FORMA, não de objeto —
  dita aqui para ninguém encadear homônimos: lá a liberdade era da identidade de α em
  ℝ; aqui é a escolha do levantamento, fixada por ω. Mesma disciplina, objetos
  distintos, cada um com o seu teorema.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- O CÓDIGO DIAGONAL da casa — o mesmo N de `diagExpect_isFrobProjection`. -/
abbrev diagCode : Submodule ℂ (Matrix n n ℂ) :=
  Submodule.span ℂ {m : Matrix n n ℂ | ∃ d, m = Matrix.diagonal d}

/-- [KERNEL] pertencer ao código diagonal É ser fixo de `diagExpect`. -/
theorem mem_diagCode_iff {x : Matrix n n ℂ} :
    x ∈ diagCode (n := n) ↔ x = diagExpect x := by
  constructor
  · intro hx
    induction hx using Submodule.span_induction with
    | mem m hm =>
        obtain ⟨d, rfl⟩ := hm
        simp [diagExpect]
    | zero => simp [diagExpect]
    | add a b _ _ ha hb =>
        show a + b = diagExpect (a + b)
        conv_lhs => rw [ha, hb]
        simp [diagExpect]
    | smul c a _ ha =>
        show c • a = diagExpect (c • a)
        conv_lhs => rw [ha]
        simp [diagExpect]
  · intro hx
    exact Submodule.subset_span ⟨x.diag, hx⟩

/-- [KERNEL] conjugação por U que preserva ρ preserva a comutação com ρ. -/
theorem commute_conj_of_state_preserving {U ρ x : Matrix n n ℂ}
    (hUU : U * Uᴴ = 1) (hρ : U * ρ * Uᴴ = ρ) (h : Commute ρ x) :
    Commute ρ (adU U x) := by
  have hU : Uᴴ * U = 1 := mul_eq_one_comm.mp hUU
  have hρU : ρ * U = U * ρ := by
    calc ρ * U = (U * ρ * Uᴴ) * U := by rw [hρ]
      _ = U * ρ * (Uᴴ * U) := by rw [mul_assoc]
      _ = U * ρ := by rw [hU, mul_one]
  have hUHρ : Uᴴ * ρ = ρ * Uᴴ := by
    calc Uᴴ * ρ = Uᴴ * (U * ρ * Uᴴ) := by rw [hρ]
      _ = ((Uᴴ * U) * ρ) * Uᴴ := by rw [← mul_assoc, ← mul_assoc]
      _ = ρ * Uᴴ := by rw [hU, one_mul]
  have cU : Commute ρ U := hρU
  have cUH : Commute ρ Uᴴ := hUHρ.symm
  unfold adU
  exact (cU.mul_right h).mul_right cUH

/-- [KERNEL] ★★★ **O JURAMENTO QUITADO**: para o código diagonal com pesos positivos
    e DISTINTOS, `HorizonInvariant` é TEOREMA para todo U unitário que preserva o
    estado — derivado, não postulado. -/
theorem the_oath_is_discharged {d : n → ℝ} (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) {U : Matrix n n ℂ}
    (hU : Uᴴ * U = 1) (hρ : U * rhoD d * Uᴴ = rhoD d) :
    HorizonInvariant (diagCode (n := n)) U := by
  have hUU : U * Uᴴ = 1 := mul_eq_one_comm.mp hU
  have hρ' : Uᴴ * rhoD d * U = rhoD d := by
    calc Uᴴ * rhoD d * U = Uᴴ * (U * rhoD d * Uᴴ) * U := by rw [hρ]
      _ = ((Uᴴ * U) * rhoD d) * (Uᴴ * U) := by
            rw [← mul_assoc, ← mul_assoc, mul_assoc (Uᴴ * U * rhoD d) Uᴴ U]
      _ = rhoD d := by rw [hU, one_mul, mul_one]
  have passo : ∀ (V : Matrix n n ℂ), V * Vᴴ = 1 → V * rhoD d * Vᴴ = rhoD d →
      ∀ y ∈ diagCode (n := n), adU V y ∈ diagCode (n := n) := by
    intro V hVV hVρ y hy
    have hyd : y = diagExpect y := mem_diagCode_iff.mp hy
    have hcy : Commute (rhoD d) y := by
      rw [hyd]
      exact commute_diagonal _ _
    have hc : Commute (rhoD d) (adU V y) :=
      commute_conj_of_state_preserving hVV hVρ hcy
    have hfix : ∀ t, sigma (rhoD d) t (adU V y) = adU V y :=
      fun t => sigma_fixed_of_commute _ _ hc t
    exact mem_diagCode_iff.mpr ((sigma_fixed_iff_diag d hd hinj _).mp hfix)
  refine ⟨passo U hUU hρ, ?_⟩
  have h1 : Uᴴ * Uᴴᴴ = 1 := by rw [conjTranspose_conjTranspose]; exact hU
  have h2 : Uᴴ * rhoD d * Uᴴᴴ = rhoD d := by
    rw [conjTranspose_conjTranspose]; exact hρ'
  exact passo Uᴴ h1 h2

/-- [KERNEL] ★★ **ω QUITA O ESTADO**: se ω(Ad(U)·) = ω(·) para ω = ⟨ρ, ·⟩ de traço,
    então U preserva ρ — pela definitude de Frobenius (a mesma da v143). O único
    antecedente que resta ao levantamento é a invariância de ω: o axioma, lido no
    horizonte. -/
theorem transported_state_eq {ρ U : Matrix n n ℂ}
    (hUU : U * Uᴴ = 1)
    (hω : ∀ y, (ρ * adU U y).trace = (ρ * y).trace) :
    Uᴴ * ρ * U = ρ := by
  have hU : Uᴴ * U = 1 := mul_eq_one_comm.mp hUU
  have hMy : ∀ y, ((Uᴴ * ρ * U - ρ) * y).trace = 0 := by
    intro y
    have h1 : (ρ * adU U y).trace = (Uᴴ * ρ * U * y).trace := by
      unfold adU
      calc (ρ * (U * y * Uᴴ)).trace = ((ρ * U * y) * Uᴴ).trace := by
              rw [← mul_assoc, ← mul_assoc]
        _ = (Uᴴ * (ρ * U * y)).trace := by rw [Matrix.trace_mul_comm]
        _ = (Uᴴ * ρ * U * y).trace := by rw [← mul_assoc, ← mul_assoc]
    rw [Matrix.sub_mul, Matrix.trace_sub, ← h1, hω, sub_self]
  have h0 : ((Uᴴ * ρ * U - ρ) * (Uᴴ * ρ * U - ρ)ᴴ).trace = 0 := hMy _
  have hM0 : (Uᴴ * ρ * U - ρ)ᴴ = 0 := by
    apply frob_self_definite
    unfold frob
    rw [conjTranspose_conjTranspose]
    exact h0
  have hM : Uᴴ * ρ * U - ρ = 0 := by
    have := congrArg conjTranspose hM0
    rwa [conjTranspose_conjTranspose, conjTranspose_zero] at this
  exact sub_eq_zero.mp hM

/-- [KERNEL] ★★ ω QUITA O ESTADO (corolário do lema acima). -/
theorem omega_preservation_discharges {ρ U : Matrix n n ℂ}
    (hUU : U * Uᴴ = 1)
    (hω : ∀ y, (ρ * adU U y).trace = (ρ * y).trace) :
    U * ρ * Uᴴ = ρ := by
  have h2 : Uᴴ * ρ * U = ρ := transported_state_eq hUU hω
  calc U * ρ * Uᴴ = U * (Uᴴ * ρ * U) * Uᴴ := by rw [h2]
    _ = ((U * Uᴴ) * ρ) * (U * Uᴴ) := by
          rw [← mul_assoc, ← mul_assoc, mul_assoc (U * Uᴴ * ρ) U Uᴴ]
    _ = ρ := by rw [hUU, one_mul, mul_one]

/-- [KERNEL] ★★ **A FACE DO CANTO**: sobre o código, o fluxo modular age como
    IDENTIDADE — no setor selecionado o grau cocíclico não age. -/
theorem the_flow_is_trivial_on_the_code {d : n → ℝ} {y : Matrix n n ℂ}
    (hy : y ∈ diagCode (n := n)) (t : ℝ) :
    sigma (rhoD d) t y = y := by
  have hyd : y = diagExpect y := mem_diagCode_iff.mp hy
  rw [hyd]
  exact sigma_fixed_of_commute _ _ (commute_diagonal _ _) t

/-- [KERNEL] ★★★ **A SUPRESSÃO COCÍCLICA NO SETOR** (a correção de estatuto do
    operador, 31/08): no setor ω-invariante, o cociclo relativo do estado
    transportado TORNA-SE 1 — resultado da seleção do setor, não escolha de
    representante. É a forma equivalente que ESTA arquitetura tem (a cautela
    formal dele, honrada: não afirmamos o literal p·u_t·p = p, que no átomo
    falha — a fase é o relógio). -/
theorem the_cocycle_is_suppressed_by_the_sector {ρ U : Matrix n n ℂ}
    (hUU : U * Uᴴ = 1)
    (hω : ∀ y, (ρ * adU U y).trace = (ρ * y).trace) (t : ℝ) :
    modPow (Uᴴ * ρ * U) t * modPow ρ (-t) = 1 := by
  rw [transported_state_eq hUU hω]
  exact modPow_mul_neg ρ t

/-- [KERNEL] ★★★★★ **O LEVANTAMENTO INCONDICIONAL NA FACE**: para todo unitário U
    cujo horizonte preserva ω (o axioma, lido no horizonte), a esperança-código é
    covariante — SEM juramento sobre N. A estrutura desenhada pelo operador,
    com o estatuto que ele corrigiu em 31/08: o cociclo não foi escolhido
    trivial — TORNOU-SE trivial no setor selecionado (supressão, não gauge). -/
theorem the_lift_is_unconditional_on_the_face {d : n → ℝ} (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) {U : Matrix n n ℂ}
    (hU : Uᴴ * U = 1)
    (hω : ∀ y, (rhoD d * adU U y).trace = (rhoD d * y).trace) :
    ∀ x, adU U (diagExpect x) = diagExpect (adU U x) := by
  have hUU : U * Uᴴ = 1 := mul_eq_one_comm.mp hU
  have hρ : U * rhoD d * Uᴴ = rhoD d := omega_preservation_discharges hUU hω
  exact global_lift_conditional hU (the_oath_is_discharged hd hinj hU hρ)
    diagExpect_isFrobProjection

/-- [KERNEL] ★★ o corolário da física, agora incondicional na face: a resposta E∘K
    transporta covariante para todo horizonte ω-invariante. -/
theorem the_response_is_unconditional_on_the_face {d : n → ℝ} (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) {U : Matrix n n ℂ} {Kf : Matrix n n ℂ → Matrix n n ℂ}
    (hU : Uᴴ * U = 1)
    (hω : ∀ y, (rhoD d * adU U y).trace = (rhoD d * y).trace)
    (hK : ∀ x, Kf (adU U x) = adU U (Kf x)) :
    ∀ x, diagExpect (Kf (adU U x)) = adU U (diagExpect (Kf x)) := by
  intro x
  rw [hK x, ← the_lift_is_unconditional_on_the_face hd hinj hU hω (Kf x)]

end

end TGLExt
