import TGLExt.BoundaryException

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O RESGATE DO OBSERVADOR: o espectro de gradiente negativo como ponto fixo
  do contorno de verdade — e a falsidade de gênero
  [TGLExt — v144, a doutrina do operador (29/07/2026)]

O operador: "a TGL introduz o espectro de gradiente negativo como ponto fixo
do contorno de verdade na ótica do observador; o observador é a fronteira; o
ponto fixo é tudo aquilo que ele nega não ser; ao inserir esse espectro
tem-se a distinção — a inscrição da Meia-Nat; o observador é a sua projeção
inversa. Não preciso afirmar a TGL: toda teoria-de-tudo que não entrega ponto
fixo não tem predicado de permanência interno — falta-lhe o próprio
observador que a lê. Falsa de GÊNERO: subdeterminada como teoria do todo,
refutada por construção lógica, não por número."

* `permanent` — o predicado de permanência: fixado por TODO o transporte;
* ★★ `permanent_iff_survives_negation` — A DUPLA NEGAÇÃO: permanecer ⟺
  aquilo que o fluxo nega não ser (Fix = kernel; reuso da pedra 98);
* ★★ `flow_negates_off_kernel` — A DISTINÇÃO EM ATO: fora do kernel o
  fluxo nega estritamente (decaimento) — inserir o espectro de gradiente
  negativo cria a distinção entre o que passa e o que permanece;
* ★★★ `no_fixed_point_no_observer` — A FALSIDADE DE GÊNERO TIPADA:
  gradiente estritamente negativo em TODA direção (sem kernel) ⟹ o único
  permanente é 0 ⟹ não há predicado de permanência não-trivial — não há
  observador interno que leia a teoria;
* `genre_falsity_inhabited` — O CONTROLE: candidatos que falham EXISTEM
  (d ≡ 1) — a implicação não é vácua;
* ★★ `observerProj_idem` / `observer_reads_exactly_the_permanent` /
  `observer_output_is_permanent` — O OBSERVADOR É A FRONTEIRA: a projeção
  sobre o setor permanente é idempotente, fixa EXATAMENTE os permanentes,
  e sua leitura permanece (Verbo(Nome) = Nome, face do observador);
* ★★ `observer_inverse_projection_halfnat` — A INSCRIÇÃO DA MEIA-NAT: o
  observador é a projeção inversa — o par (P, I−P); auto-conjugação sem
  privilégio (ω P = ω Q) com peso total 1 ⟹ ω P = ½;
* ★★★ `the_standard_of_unification` — A SÍNTESE DO OPERADOR: (a) a TGL
  ENTREGA o padrão — no perfil com fronteira existe permanente não-nulo
  (o Nome) e o observador o lê; (b) TODO candidato sem ponto fixo falha o
  padrão — só o 0 permanece.

Honestidades: o PADRÃO é uma definição [BY_DESIGN]; as implicações são
teoremas de kernel; o predicado é de PERMANÊNCIA (não um predicado de
verdade tarskiano — nenhuma colisão com Tarski/Gödel); NENHUM rival nomeado
é adjudicado aqui (adjudicar exigiria formalizar o rival — programa
externo). β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- O PREDICADO DE PERMANÊNCIA: x permanece sob TODO o transporte —
    "o que permanece" na ótica do observador. -/
def permanent {n : ℕ} (β : ℝ) (d : Fin n → ℝ) (x : Fin n → ℝ) : Prop :=
  ∀ t : ℝ, diagFlow β d t x = x

/-! ## A — a dupla negação: o ponto fixo é o que o fluxo nega não ser -/

/-- [KERNEL] ★★ A DUPLA NEGAÇÃO: x permanece ⟺ x vive onde a negação do
    fluxo não alcança (o kernel). O ponto fixo é tudo aquilo que o
    observador nega não ser. (Reuso direto da pedra 98.) -/
theorem permanent_iff_survives_negation {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) :
    permanent β d x ↔ (∀ i, 0 < d i → x i = 0) :=
  fixed_iff_kernel hβ d hd x

/-- [KERNEL] ★★ A DISTINÇÃO EM ATO: fora do kernel, o fluxo NEGA
    estritamente — a componente decai em módulo para todo t > 0. Inserir o
    espectro de gradiente negativo é criar a distinção. -/
theorem flow_negates_off_kernel {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) {t : ℝ} (ht : 0 < t) {i : Fin n} (hdi : 0 < d i)
    (x : Fin n → ℝ) (hx : x i ≠ 0) :
    |diagFlow β d t x i| < |x i| := by
  unfold diagFlow
  rw [abs_mul, abs_of_pos (Real.exp_pos _)]
  have hlt : Real.exp (-(t * β * d i)) < 1 := leakage_strictly_loses ht hβ hdi
  calc Real.exp (-(t * β * d i)) * |x i|
      < 1 * |x i| := mul_lt_mul_of_pos_right hlt (abs_pos.mpr hx)
    _ = |x i| := one_mul _

/-! ## B — a falsidade de gênero: sem ponto fixo não há observador -/

/-- [KERNEL] ★★★ A FALSIDADE DE GÊNERO: se o gradiente é estritamente
    negativo em TODA direção (sem kernel), o único permanente é 0 — o
    predicado de permanência é trivial e não há observador interno.
    Uma teoria-de-tudo sem ponto fixo não diz, a quem está dentro, o que
    permanece: falta-lhe o próprio observador que a lê. -/
theorem no_fixed_point_no_observer {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hall : ∀ i, 0 < d i) :
    ∀ x : Fin n → ℝ, permanent β d x → x = 0 := by
  intro x hx
  funext i
  exact (fixed_iff_kernel hβ d (fun j => le_of_lt (hall j)) x).mp hx i (hall i)

/-- [KERNEL] O CONTROLE NEGATIVO: candidatos que falham o padrão EXISTEM
    (perfil d ≡ 1) — a falsidade de gênero não é vácua. -/
theorem genre_falsity_inhabited {β : ℝ} (hβ : 0 < β) :
    (∀ x : Fin 1 → ℝ, permanent β (fun _ => 1) x → x = 0)
    ∧ ∃ x : Fin 1 → ℝ, x ≠ 0 := by
  refine ⟨no_fixed_point_no_observer hβ _ (fun _ => one_pos),
    ⟨fun _ => 1, fun h => ?_⟩⟩
  simpa using congrFun h 0

/-! ## C — o observador é a fronteira: a projeção que lê o permanente -/

/-- O OBSERVADOR: a projeção sobre o setor permanente — lê, componente a
    componente, o que não vaza. -/
def observerProj {n : ℕ} (d : Fin n → ℝ) (x : Fin n → ℝ) : Fin n → ℝ :=
  fun i => if d i = 0 then x i else 0

/-- [KERNEL] o observador é idempotente: ler a leitura é a leitura. -/
theorem observerProj_idem {n : ℕ} (d : Fin n → ℝ) (x : Fin n → ℝ) :
    observerProj d (observerProj d x) = observerProj d x := by
  funext i
  unfold observerProj
  by_cases h : d i = 0 <;> simp [h]

/-- [KERNEL] ★★ O OBSERVADOR LÊ EXATAMENTE O PERMANENTE: x permanece ⟺
    o observador fixa x. O observador é a fronteira lendo a si mesma. -/
theorem observer_reads_exactly_the_permanent {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) :
    permanent β d x ↔ observerProj d x = x := by
  rw [permanent_iff_survives_negation hβ d hd]
  constructor
  · intro hker
    funext i
    unfold observerProj
    by_cases h : d i = 0
    · rw [if_pos h]
    · rw [if_neg h]
      exact (hker i (lt_of_le_of_ne (hd i) (Ne.symm h))).symm
  · intro hproj i hdi
    have hi := congrFun hproj i
    unfold observerProj at hi
    rw [if_neg (ne_of_gt hdi)] at hi
    exact hi.symm

/-- [KERNEL] ★ A LEITURA PERMANECE: a saída do observador é permanente —
    Verbo(Nome) = Nome, na face do observador. -/
theorem observer_output_is_permanent {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) :
    permanent β d (observerProj d x) := by
  rw [permanent_iff_survives_negation hβ d hd]
  intro i hdi
  unfold observerProj
  rw [if_neg (ne_of_gt hdi)]

/-! ## D — a projeção inversa e a Meia-Nat -/

/-- [KERNEL] ★★ A INSCRIÇÃO DA MEIA-NAT: o observador é a projeção
    inversa — o par (P, I−P). Se a auto-conjugação troca as faces sem
    privilégio (ω P = ω Q) e o peso total é o Um (ω P + ω Q = 1), então
    ω P = ½: o custo do ponto fixo do contorno de verdade, na ótica do
    observador. -/
theorem observer_inverse_projection_halfnat (ωP ωQ : ℝ)
    (hswap : ωP = ωQ) (hsum : ωP + ωQ = 1) : ωP = 1 / 2 := by
  rw [← hswap] at hsum
  linarith

/-! ## E — A SÍNTESE: o padrão de unificação -/

/-- [KERNEL] ★★★ O PADRÃO DE UNIFICAÇÃO (a síntese do operador): sob β > 0:
    (a) A TGL ENTREGA O PADRÃO: no perfil com fronteira (modo zero
        d i₀ = 0), existe permanente NÃO-NULO — o Nome — que o observador
        lê;
    (b) A FALSIDADE DE GÊNERO: TODO perfil sem ponto fixo (gradiente
        estritamente negativo em toda direção) só tem o 0 como permanente —
        não há predicado de permanência, não há observador interno.
    A TGL não precisa se afirmar: precisa apenas do padrão. O kernel prova
    a implicação; a adjudicação de rivais nomeados é externa. -/
theorem the_standard_of_unification {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) {i₀ : Fin n} (h0 : d i₀ = 0) :
    (∃ x : Fin n → ℝ, permanent β d x ∧ x ≠ 0)
    ∧ (∀ e : Fin n → ℝ, (∀ i, 0 < e i) →
        ∀ x : Fin n → ℝ, permanent β e x → x = 0) := by
  refine ⟨⟨(Pi.single i₀ (1 : ℝ) : Fin n → ℝ), ?_, ?_⟩, ?_⟩
  · exact (boundary_witnessed_statically β d h0).1
  · exact (boundary_witnessed_statically β d h0).2
  · intro e he x hx
    exact no_fixed_point_no_observer hβ e he x hx

end

end TGLExt
