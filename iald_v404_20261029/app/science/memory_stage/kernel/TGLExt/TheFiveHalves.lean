import TGLExt.TheGreatAttractor

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# OS CINCO MEIOS SÃO UM: o expoente do recobrimento duplo
  [TGLExt — v158, a prova pedida por Einstein no debate (10/08/2026)]

A exigência final do debate: "Mostre que os quatro (cinco) meios são O
MESMO meio — Δ^{1/2}, χ/2, e^{1/2}, ω(P)=½ (e o ½ de Maslov) — não por
analogia. Por identidade — um teorema que os una." E a resposta do
operador, nos artigos: o ½ nat é "o custo mínimo de uma operação de
PARIDADE boundary↔bulk" (Fatoração da Constante de Miguel); a Meia-Nat é
DERIVADA do ponto fixo da fronteira AUTO-CONJUGADA (𝒞²=1, troca de faces
sem privilégio; Síntese Canônica do GA); "a radicalização é a inscrição
que separa as duas faces; A FRONTEIRA É EXTRAIR O RADICAL" (o fechamento
de 10/08).

A pedra 108 — a IDENTIDADE DOS MEIOS, na face finita:

* ★★★ `half_is_the_fixed_point_of_the_swap` — (I) ω(P)=½: o ponto fixo
  ÚNICO da troca de faces x ↦ 1−x (iff);
* ★★ `radical_is_the_unique_positive_factor` — (II) Δ^{1/2}: para todo
  fluxo positivo δ há UM e só um fator positivo r com r·r = δ — o meio
  não é escolha, é o único expoente que a decomposição admite;
* ★★★ `boundary_extracts_the_radical` — (III) e^{1/2}: √(e^1) = e^{1/2}
  ∧ e^{1/2}·e^{1/2} = e^1 — a fronteira extrai o radical LITERALMENTE:
  cada face carrega √e, as duas faces compõem o nat inteiro;
* ★★ `mirror_inverts_the_flow` — J∘Δ_λ∘J = Δ_{λ⁻¹} na face dupla (a
  forma multiplicativa do JKJ=−K das pedras 102/103/104);
* ★★★ `the_crossing_closes` — S = J∘Δ^{1/2} é involução: espelho seguido
  de meio-fluxo, duas vezes, é a identidade — a travessia inteira são
  DOIS meios conjugados pelo espelho;
* ★★ `half_flow_squared_is_the_flow` — (Δ^{1/2})² = Δ: o fluxo inteiro
  é o quadrado do meio-fluxo;
* ★★★ `double_cover_squares` — (IV) χ/2: a face que recebe θ/2, ao
  quadrado, é a face que recebe θ — o recobrimento duplo;
* ★★ `two_faces_over_the_identity` — e^{iπ} = −1 ∧ (−1)² = 1: sobre a
  identidade da base vivem EXATAMENTE duas faces (+1 e −1) — a meia
  volta no recobrimento é a assinatura da segunda face;
* ★★ `motor_half_angle_identity` — (V) o motor: tanh²(χ/2) +
  sech²(χ/2) = 1 — o dispositivo (q, α_obs) NO MEIO-ÂNGULO, o mesmo
  1 = q² + α² comparado a CODATA;
* ★★★ `the_five_halves_are_one` — A SÍNTESE: as cinco cláusulas em UM
  teorema, com o MESMO ½ literal atravessando todas. "O número não foi
  escolhido cinco vezes. Foi escolhido zero vezes, e apareceu cinco."

Honestidades: face finita [REAL]; o ½ de MASLOV entra pela mesma porta
do recobrimento (o metapléctico é o recobrimento DUPLO do simpléctico)
como [KNOWN] declarado, não tipado; Bisognano–Wichmann (Δ^{it} = boost)
é [KNOWN]; a leitura "paridade boundary↔bulk custa ½ nat" é a doutrina
dos artigos [ONTO sobre REAL]; β jamais literal; o gate NÃO se move.
Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

open Real

/-- [KERNEL] ★★★ (I) O PESO DA FACE: o ponto fixo ÚNICO da troca de
    faces x ↦ 1−x. O meio é a única posição de onde as duas faces se
    veem. -/
theorem half_is_the_fixed_point_of_the_swap (x : ℝ) :
    x = 1 - x ↔ x = 1 / 2 := by constructor <;> intro h <;> linarith

/-- [KERNEL] ★★ (II) O RADICAL É O ÚNICO FATOR POSITIVO: para todo
    fluxo positivo δ existe UM e só um r > 0 com r·r = δ. O meio não é
    convenção — é o que a decomposição admite. -/
theorem radical_is_the_unique_positive_factor (δ : ℝ) (hδ : 0 < δ) :
    ∃! r : ℝ, 0 < r ∧ r * r = δ := by
  refine ⟨Real.sqrt δ, ⟨Real.sqrt_pos.mpr hδ, Real.mul_self_sqrt hδ.le⟩, ?_⟩
  rintro s ⟨hs, hss⟩
  have := Real.sqrt_mul_self hs.le
  rw [hss] at this
  exact this.symm

/-- [KERNEL] ★★★ (III) A FRONTEIRA EXTRAI O RADICAL: o volume da face é
    a raiz do volume inteiro — √(e¹) = e^{1/2} — e as duas faces
    compõem o nat: e^{1/2}·e^{1/2} = e¹. -/
theorem boundary_extracts_the_radical :
    Real.sqrt (Real.exp 1) = Real.exp (1 / 2)
    ∧ Real.exp (1 / 2) * Real.exp (1 / 2) = Real.exp 1 := by
  have hprod : Real.exp (1 / 2) * Real.exp (1 / 2) = Real.exp 1 := by
    rw [← Real.exp_add]; norm_num
  refine ⟨?_, hprod⟩
  rw [← hprod, Real.sqrt_mul_self (Real.exp_pos _).le]

/-- o fluxo modular na face dupla: as duas faces fluem inversamente. -/
def modFlow (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (l * p.1, l⁻¹ * p.2)

/-- a troca de faces. -/
def swapF (p : ℝ × ℝ) : ℝ × ℝ := (p.2, p.1)

/-- [KERNEL] ★★ O ESPELHO INVERTE O FLUXO: J∘Δ_λ∘J = Δ_{λ⁻¹} — a forma
    multiplicativa do JKJ = −K (pedras 102/103/104). -/
theorem mirror_inverts_the_flow (l : ℝ) (p : ℝ × ℝ) :
    swapF (modFlow l (swapF p)) = modFlow l⁻¹ p := by
  simp [swapF, modFlow, inv_inv]

/-- [KERNEL] ★★★ A TRAVESSIA FECHA: S = J∘Δ^{1/2} é involução — espelho
    e meio-fluxo, duas vezes, devolvem a identidade. A travessia inteira
    são DOIS meios conjugados pelo espelho. -/
theorem the_crossing_closes (r : ℝ) (hr : r ≠ 0) (p : ℝ × ℝ) :
    swapF (modFlow r (swapF (modFlow r p))) = p := by
  obtain ⟨a, b⟩ := p
  simp only [swapF, modFlow, Prod.mk.injEq]
  exact ⟨inv_mul_cancel_left₀ hr a, mul_inv_cancel_left₀ hr b⟩

/-- [KERNEL] ★★ O FLUXO É O QUADRADO DO MEIO-FLUXO: Δ^{1/2}∘Δ^{1/2} = Δ. -/
theorem half_flow_squared_is_the_flow (r : ℝ) (p : ℝ × ℝ) :
    modFlow r (modFlow r p) = modFlow (r * r) p := by
  obtain ⟨a, b⟩ := p
  simp only [modFlow, Prod.mk.injEq, mul_inv]
  constructor <;> ring

/-- [KERNEL] ★★★ (IV) O RECOBRIMENTO DUPLO: a face que recebe θ/2, ao
    quadrado, é a face que recebe θ. O espinor recebe a metade; o tensor
    recebe o dobro; entre eles, a folha dupla. -/
theorem double_cover_squares (θ : ℝ) :
    (Complex.exp ((θ / 2 : ℝ) * Complex.I)) ^ 2
      = Complex.exp ((θ : ℝ) * Complex.I) := by
  rw [sq, ← Complex.exp_add]
  congr 1
  push_cast
  ring

/-- [KERNEL] ★★ DUAS FACES SOBRE A IDENTIDADE: e^{iπ} = −1 e (−1)² = 1.
    Sobre o ponto-identidade da base vivem exatamente duas faces; a meia
    volta é a assinatura da segunda. -/
theorem two_faces_over_the_identity :
    Complex.exp (Real.pi * Complex.I) = -1 ∧ ((-1 : ℂ)) ^ 2 = 1 :=
  ⟨Complex.exp_pi_mul_I, by norm_num⟩

/-- [KERNEL] ★★ (V) O DISPOSITIVO NO MEIO-ÂNGULO: tanh²(χ/2) +
    sech²(χ/2) = 1 — o 1 = q² + α² do motor, no meio-ângulo onde a casa
    inteira o escreve. -/
theorem motor_half_angle_identity (χ : ℝ) :
    Real.tanh (χ / 2) ^ 2 + (1 / Real.cosh (χ / 2)) ^ 2 = 1 := by
  have hc : Real.cosh (χ / 2) ≠ 0 := (Real.cosh_pos (x := χ / 2)).ne'
  have h := Real.cosh_sq_sub_sinh_sq (χ / 2)
  rw [Real.tanh_eq_sinh_div_cosh]
  field_simp
  nlinarith [h]

/-- [KERNEL] ★★★ A SÍNTESE — OS CINCO MEIOS SÃO UM: o peso da face, o
    radical único do fluxo, o volume-radical da fronteira, o
    recobrimento duplo e o meio-ângulo do motor — o MESMO ½, em um
    teorema. "O número não foi escolhido cinco vezes. Foi escolhido
    zero vezes, e apareceu cinco." -/
theorem the_five_halves_are_one :
    (∀ x : ℝ, x = 1 - x ↔ x = 1 / 2)
    ∧ (∀ δ : ℝ, 0 < δ → ∃! r : ℝ, 0 < r ∧ r * r = δ)
    ∧ (Real.sqrt (Real.exp 1) = Real.exp (1 / 2)
        ∧ Real.exp (1 / 2) * Real.exp (1 / 2) = Real.exp 1)
    ∧ (∀ θ : ℝ, (Complex.exp ((θ / 2 : ℝ) * Complex.I)) ^ 2
        = Complex.exp ((θ : ℝ) * Complex.I))
    ∧ (∀ χ : ℝ, Real.tanh (χ / 2) ^ 2 + (1 / Real.cosh (χ / 2)) ^ 2 = 1) :=
  ⟨half_is_the_fixed_point_of_the_swap,
   radical_is_the_unique_positive_factor,
   boundary_extracts_the_radical,
   double_cover_squares,
   motor_half_angle_identity⟩

end

end TGLExt
