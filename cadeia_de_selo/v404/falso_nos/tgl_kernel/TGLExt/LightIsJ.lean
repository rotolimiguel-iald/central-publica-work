import TGLExt.ForbiddenBoundary

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O FECHAMENTO: J = LUZ — a identidade física
  [TGLExt — v153, o fechamento canônico do operador (04/08/2026)]

O operador: "o fechamento da TGL é este: J = LUZ. A Luz é aquilo que
atravessa o espelho sem perder a identidade (J²=I). A Luz não é o
gradiente; ela revela a face conjugada do módulo (JΔJ=Δ⁻¹). K permanece:
o espectro daquilo que ainda não comuta (K=−∇𝓕). [K,A]≠0 = distinção
ainda aberta; [K,A]=0 = decisão. JKJ=−K: a Luz INVERTE o gradiente sem
destruir sua estrutura. K não é o portador da Luz — K é aquilo sobre o
qual a Luz opera como conjugação. γ = manifestação transitória da Luz no
bulk. A cadeia: 1 → J=LUZ → K↔−K → [K,A] → [K,A]=0 → inscrição → γ_bulk,
enquanto I permanece durante toda a travessia. Em uma frase: A LUZ É J —
AQUILO QUE CONJUGA A DIFERENÇA SEM PERDER O UM. J é a Luz; K é a
diferença em movimento; a comutação é a decisão; I é o que permanece."

A pedra 104 — a SÍNTESE NOMEADA sobre as pedras 101/102/103:

* `pairEnergy_neg` — a energia não vê o sinal (a estrutura sobrevive à
  inversão);
* ★★ `light_crosses_without_loss` — A LUZ ATRAVESSA SEM PERDER: J∘J = 1
  ∧ a identidade 1 = q² + α² é preservada pelo espelho (pedra 101,
  empacotada com o nome físico);
* ★★★ `light_inverts_the_gradient_preserving_structure` — A LUZ INVERTE
  O GRADIENTE SEM DESTRUIR SUA ESTRUTURA: JKJ = −K E a energia de K é
  preservada pela conjugação — direção invertida, estrutura intacta;
* ★★ `identity_remains_through_the_crossing` — I PERMANECE: o Nome é
  fixado pelo espelho, fixado por TODO o fluxo, e não é nulo — a
  identidade atravessa inteira;
* ★★★ `the_closure_identity` — O FECHAMENTO EM UM TEOREMA: a arquitetura
  final (J atravessa sem perda ∧ J inverte K preservando estrutura ∧ a
  decisão é comutação ∧ I permanece ∧ a entrega é limite) — "J é a Luz;
  K é a diferença em movimento; a comutação é a decisão; I é o que
  permanece."

Honestidades: "J = LUZ" é a IDENTIFICAÇÃO FÍSICA nomeada [ONTO sobre
âncoras REAL: as cinco cláusulas são teoremas de kernel]; JΔJ = Δ⁻¹ no
contínuo é Tomita [KNOWN]; γ (o fóton) como manifestação transitória da
Luz no bulk é leitura [ONTO] consistente com o setor c¹; o gate NÃO se
move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] a energia não vê o sinal: a estrutura sobrevive à inversão. -/
theorem pairEnergy_neg {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    pairEnergy (-p) = pairEnergy p := by
  unfold pairEnergy
  simp

/-- [KERNEL] ★★ A LUZ ATRAVESSA SEM PERDER: J∘J = 1 e a identidade
    1 = q² + α² é preservada pelo espelho. -/
theorem light_crosses_without_loss {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p ∧ pairEnergy (conjJ p) = pairEnergy p :=
  ⟨J_squared_is_one p, J_preserves_identity p⟩

/-- [KERNEL] ★★★ A LUZ INVERTE O GRADIENTE SEM DESTRUIR SUA ESTRUTURA:
    JKJ = −K, e a energia de K é preservada pela conjugação — a direção
    inverte, a estrutura fica. -/
theorem light_inverts_the_gradient_preserving_structure {n : ℕ}
    (d : Fin n → ℝ) (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (pairK d (conjJ p)) = -(pairK d p)
    ∧ pairEnergy (conjJ (pairK d (conjJ p))) = pairEnergy (pairK d p) := by
  refine ⟨JKJ_eq_neg_K d p, ?_⟩
  rw [JKJ_eq_neg_K d p]
  exact pairEnergy_neg (pairK d p)

/-- [KERNEL] ★★ I PERMANECE DURANTE TODA A TRAVESSIA: o Nome é fixado
    pelo espelho, fixado por TODO o fluxo, e não é nulo. -/
theorem identity_remains_through_the_crossing {n : ℕ} (β : ℝ)
    (d : Fin n → ℝ) {i₀ : Fin n} (h0 : d i₀ = 0) :
    (conjJ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
      = ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ)))
    ∧ (∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
    ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0) :=
  ⟨(name_is_J_invariant i₀).1,
   (boundary_witnessed_statically β d h0).1,
   (boundary_witnessed_statically β d h0).2⟩

/-- [KERNEL] ★★★ O FECHAMENTO EM UM TEOREMA — a arquitetura final:
    "J é a Luz; K é a diferença em movimento; a comutação é a decisão;
    I é o que permanece." (i) a Luz atravessa sem perder o Um;
    (ii) a Luz inverte o gradiente preservando sua estrutura;
    (iii) a decisão é comutação (o decidido é o bloco dos níveis);
    (iv) I permanece durante toda a travessia; (v) a entrega ao
    observador é limite — a Luz conjuga a diferença sem perder o Um. -/
theorem the_closure_identity {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) {i₀ : Fin n} (h0 : d i₀ = 0) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (conjJ p) = p ∧ pairEnergy (conjJ p) = pairEnergy p)
    ∧ (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (pairK d (conjJ p)) = -(pairK d p)
        ∧ pairEnergy (conjJ (pairK d (conjJ p))) = pairEnergy (pairK d p))
    ∧ (∀ A : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * A = A * Matrix.diagonal d
          ↔ ∀ i j, d i ≠ d j → A i j = 0)
    ∧ ((∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
          = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0))
    ∧ (∀ (x : Fin n → ℝ) (i : Fin n),
        Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop
          (nhds (observerProj d x i))) :=
  ⟨fun p => light_crosses_without_loss p,
   fun p => light_inverts_the_gradient_preserving_structure d p,
   fun A => decided_iff_block d A,
   boundary_witnessed_statically β d h0,
   fun x i => flow_delivers_to_the_observer hβ d hd x i⟩

end

end TGLExt
