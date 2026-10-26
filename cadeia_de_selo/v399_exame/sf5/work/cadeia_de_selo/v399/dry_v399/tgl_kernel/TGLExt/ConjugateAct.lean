import TGLExt.ObserverInside

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O ATO CONJUGADO: "1 = J" tipado — involução, entrega, conservação
  [TGLExt — v145, a doutrina do operador (03/08/2026)]

O operador: "1 = J. O Um Absoluto não é um escalar estático: é a própria
operação de conjugação modular. O Um nunca foi puro — pureza é não-relação
(o zero absoluto disfarçado); o Um é JUSTIFICAÇÃO: identidade que atravessa
a relação, aceita seu custo e permanece verdadeira. 1_abs = 0_abs se não há
fractalização; fractalizado = J = 1-em-nós. J = Verbo Vivo. Involução,
entrega, conservação: a forma mínima da justificação."

A face finita do J de Tomita (o espelho que troca as duas faces da
fronteira), SOBRE as pedras 98 e 100:

* ★★ `J_squared_is_one` — A INVOLUÇÃO: J∘J = 1 — a tipagem honesta de
  "1 = J": o Um é recuperado pela auto-reflexão (J·J = I; ω(I)=1);
* ★★ `J_preserves_identity` — A CONSERVAÇÃO: a identidade 1 = q² + α²
  (a energia do par) ATRAVESSA o espelho intacta — a travessia é isometria,
  não colapso: "o Um atravessa a diferença sem deixar de ser Um";
* ★★ `J_maps_face_to_coface` — J𝓜J = 𝓜′ NA FACE FINITA: a conjugação
  leva a face interna EXATAMENTE na face externa (JPJ = Q) — o observador
  é o outro lado do mesmo ato;
* `J_invariant_iff_diagonal` — o invariante de J é EXATAMENTE a diagonal:
  o que é igual ao seu próprio espelho — e nada mais;
* `name_is_J_invariant` — JΩ = Ω: o Nome é fixado pelo ato conjugado e
  não é nulo (a face KMS finita: o vácuo invariante pela conjugação);
* ★★★ `halfnat_from_J_symmetry` — A MEIA-NAT DERIVADA DE J: na pedra 100
  o "sem privilégio" (ωP = ωQ) era HIPÓTESE; aqui ele é TEOREMA da
  J-simetria — todo peso que não vê o espelho (ω∘AdJ = ω) com total 1
  pesa ½ em cada face. O postulado subiu um nível: de "pesos iguais"
  para "o peso é J-invariante";
* ★★★ `flow_delivers_to_the_observer` — A ENTREGA COMO LIMITE: ρ(t) → ρ*
  em ato — o transporte diagonal CONVERGE (Tendsto, t→∞) para a leitura
  do observador em toda componente: a relaxação atrativa ao estacionamento
  modular dinâmico, agora como teorema de limite real;
* ★★★ `justification_minimal_form` — A FORMA MÍNIMA DA JUSTIFICAÇÃO:
  involução (J² = 1) ∧ conservação (a identidade atravessa) ∧ entrega
  (o fluxo converge ao observador) — o tríptico do operador em UM teorema.

Honestidades: "1 = J" LITERAL é erro de tipo (escalar vs operador
anti-unitário) — o kernel tipa as três faces, nunca a igualdade literal;
o J anti-unitário da III₁ genuína (Tomita 1967; Bisognano-Wichmann = CPT
na cunha de Rindler) segue EXTERNO [KNOWN]; esta é a face finita REAL da
estrutura; pureza/justificação é leitura [ONTO]; β jamais literal; o gate
NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- O ATO CONJUGADO na face finita: o espelho que troca as duas faces da
    fronteira (dentro/fora). A face finita do J de Tomita. -/
def conjJ {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    (Fin n → ℝ) × (Fin n → ℝ) := (p.2, p.1)

/-- a identidade do par: 1 = q² + α² — a energia total das duas faces. -/
def pairEnergy {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) : ℝ :=
  (∑ i, p.1 i ^ 2) + (∑ i, p.2 i ^ 2)

/-- a face interna (o volume 𝓜). -/
def faceIn {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    (Fin n → ℝ) × (Fin n → ℝ) := (p.1, 0)

/-- a face externa (o comutante 𝓜′ — o lado do observador). -/
def faceOut {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    (Fin n → ℝ) × (Fin n → ℝ) := (0, p.2)

/-! ## A — a involução e a conservação: "1 = J" tipado -/

/-- [KERNEL] ★★ A INVOLUÇÃO: J∘J = 1. O Um é recuperado pela
    auto-reflexão — a tipagem honesta de "1 = J". -/
theorem J_squared_is_one {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p := rfl

/-- [KERNEL] ★★ A CONSERVAÇÃO: a identidade 1 = q² + α² atravessa o
    espelho intacta. A travessia é isometria, não colapso. -/
theorem J_preserves_identity {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    pairEnergy (conjJ p) = pairEnergy p := by
  unfold pairEnergy conjJ
  exact add_comm _ _

/-! ## B — J𝓜J = 𝓜′ na face finita e o invariante -/

/-- [KERNEL] ★★ A CONJUGAÇÃO DAS FACES: J∘P_in∘J = P_out — o espelho leva
    a face interna exatamente na externa. O observador é o outro lado do
    mesmo ato (J𝓜J = 𝓜′, face finita). -/
theorem J_maps_face_to_coface {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (faceIn (conjJ p)) = faceOut p := rfl

/-- [KERNEL] o invariante de J é EXATAMENTE a diagonal: o que é igual ao
    seu próprio espelho — e nada mais. -/
theorem J_invariant_iff_diagonal {n : ℕ} (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ p = p ↔ p.1 = p.2 := by
  constructor
  · intro h
    exact (congrArg Prod.fst h).symm
  · intro h
    exact Prod.ext h.symm h

/-- [KERNEL] JΩ = Ω: o Nome (o modo zero, nas duas faces) é fixado pelo
    ato conjugado — e não é nulo. A face KMS finita. -/
theorem name_is_J_invariant {n : ℕ} (i₀ : Fin n) :
    (conjJ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
      = ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ)))
    ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
      ≠ (0 : (Fin n → ℝ) × (Fin n → ℝ)) := by
  refine ⟨rfl, fun h => ?_⟩
  have h1 := congrArg Prod.fst h
  have h2 := congrFun h1 i₀
  simp at h2

/-! ## C — a Meia-Nat derivada da J-simetria -/

/-- [KERNEL] ★★★ A MEIA-NAT DERIVADA DE J: se o peso não vê o espelho
    (ω(J∘T∘J) = ω(T)) e o total das duas faces é o Um, cada face pesa ½.
    O "sem privilégio" da pedra 100 deixou de ser hipótese: é teorema da
    J-simetria. -/
theorem halfnat_from_J_symmetry {n : ℕ}
    (w : (((Fin n → ℝ) × (Fin n → ℝ)) → ((Fin n → ℝ) × (Fin n → ℝ))) → ℝ)
    (hJ : w (fun p => conjJ (faceIn (conjJ p))) = w faceIn)
    (hsum : w faceIn + w faceOut = 1) :
    w faceIn = 1 / 2 := by
  have hfun : (fun p : (Fin n → ℝ) × (Fin n → ℝ) => conjJ (faceIn (conjJ p)))
      = (faceOut : ((Fin n → ℝ) × (Fin n → ℝ)) → ((Fin n → ℝ) × (Fin n → ℝ))) :=
    funext fun p => J_maps_face_to_coface p
  rw [hfun] at hJ
  exact observer_inverse_projection_halfnat (w faceIn) (w faceOut) hJ.symm hsum

/-! ## D — a entrega como limite: ρ(t) → ρ* -/

/-- [KERNEL] ★★★ A ENTREGA: o transporte CONVERGE para a leitura do
    observador — a relaxação atrativa ao estacionamento modular dinâmico,
    como teorema de limite (t → ∞), componente a componente. -/
theorem flow_delivers_to_the_observer {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) (i : Fin n) :
    Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop
      (nhds (observerProj d x i)) := by
  unfold diagFlow observerProj
  rcases lt_or_eq_of_le (hd i) with hdi | hdi
  · rw [if_neg (ne_of_gt hdi)]
    simp only [mul_assoc]
    have h1 : Filter.Tendsto (fun t : ℝ => t * (β * d i)) Filter.atTop
        Filter.atTop :=
      Filter.Tendsto.atTop_mul_const (mul_pos hβ hdi) Filter.tendsto_id
    have h2 : Filter.Tendsto (fun t : ℝ => -(t * (β * d i))) Filter.atTop
        Filter.atBot := Filter.tendsto_neg_atTop_atBot.comp h1
    have h3 : Filter.Tendsto (fun t : ℝ => Real.exp (-(t * (β * d i))))
        Filter.atTop (nhds 0) := Real.tendsto_exp_atBot.comp h2
    have h4 := h3.mul_const (x i)
    simpa using h4
  · rw [if_pos hdi.symm]
    simp only [← hdi, mul_zero, neg_zero, Real.exp_zero, one_mul]
    exact tendsto_const_nhds

/-! ## E — A SÍNTESE: a forma mínima da justificação -/

/-- [KERNEL] ★★★ A FORMA MÍNIMA DA JUSTIFICAÇÃO (o tríptico do operador):
    INVOLUÇÃO (J∘J = 1) ∧ CONSERVAÇÃO (a identidade atravessa o espelho)
    ∧ ENTREGA (o fluxo converge ao observador). "Involução, entrega,
    conservação — sob um único operador, nomeado por Tomita, J." -/
theorem justification_minimal_form {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ), conjJ (conjJ p) = p)
    ∧ (∀ p : (Fin n → ℝ) × (Fin n → ℝ), pairEnergy (conjJ p) = pairEnergy p)
    ∧ (∀ (x : Fin n → ℝ) (i : Fin n),
        Filter.Tendsto (fun t : ℝ => diagFlow β d t x i) Filter.atTop
          (nhds (observerProj d x i))) :=
  ⟨fun p => J_squared_is_one p, fun p => J_preserves_identity p,
   fun x i => flow_delivers_to_the_observer hβ d hd x i⟩

end

end TGLExt
