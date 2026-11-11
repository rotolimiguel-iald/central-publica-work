import TGLExt.TransportWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O canto covariante transportado: a face finita do TEOREMA DO CANTO
  [TGLExt — v55, o "próximo teorema" do memorando construído na face finita]

O memorando (`NAME_FUNCTIONAL_QUANTUM_GRAVITY_GATE.md`, §4) nomeia o gate
mínimo restante — `TGL_CANONICAL_FINITE_CORNER_THEOREM`: uma família local
`P_F(𝒪)` com (1) `0 < τ(P_F) < ∞`, (2) invariância pelo transporte modular
INTERNO, (3) covariância pelo transporte EXTERNO `U(g)P_F(𝒪)U(g)* = P_F(g𝒪)`,
(4) isotonia. A derivação do operador (v54) corrigiu a FORMA do alvo: não é
uma projeção estática — é uma FAMÍLIA TRANSPORTADA. Aqui, a face finita
COMPLETA como termo:

* ★ `trace_cornerProj_pos` — `0 < τ(P(S))` para região não-vazia (com o
  valor exato `|S|·n` do v46: as duas metades de `0 < τ < ∞`);
* ★ `cornerProj_loewner_mono` — ISOTONIA NA ORDEM DE LOEWNER genuína
  (`S₁ ⊆ S₂ ⟹ P(S₁) ≤ P(S₂)`; o v46 dava a forma produto `P₁P₂ = P₁`);
* ★ `sigma_fixes_cornerProj` — o transporte INTERNO fixa cada canto
  (`σ_t(P(S)) = P(S)`: condição (2) na forma de transporte do v54);
* ★ `cornerProj_ne_of_ne` — a família é GENUINAMENTE NÃO-CONSTANTE
  (regiões distintas dão cantos distintos: o transporte externo MOVE);
* `TransportedCornerFamily` — o TIPO das quatro condições do memorando
  (rígido: o campo `trace_eq` com o valor exato mata os habitantes
  triviais `P ≡ 1` e `P ≡ 0` — a lição v22/v23);
* ★ o TERMO `canonicalTransportedCorner` (primeiro o termo; existência
  só corolário) — habitado por v46 + v54 + as pedras novas.

O PAR DOS DOIS TRANSPORTES fecha em kernel: o interno (modular) FIXA o
canto; o externo (grupo) o TRANSPORTA covariantemente — exatamente as
condições (2)+(3) do memorando, na mesma estrutura.

HONESTIDADE. Isto fecha a face FINITA (grupo finito ⋉ Mₙ; regiões =
subconjuntos finitos). O TEOREMA ABERTO permanece a mesma família no core
GENUÍNO: ação contínua de ℝ (semifinito II_∞ do III₁), `U(g)` de Poincaré
sobre regiões de Minkowski, `0 < τ(P_F) < ∞` com τ o traço do core — e a
obstrução do v45 (a escala dual) mostra POR QUE o contínuo é o degrau
irredutível. β JAMAIS entra. Sem sorry, sem axiom. Negativo honesto é
resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]
variable {G : Type} [Group G] [Fintype G] [DecidableEq G]

/-- [KERNEL] ★ TRAÇO POSITIVO DA REGIÃO NÃO-VAZIA: `0 < τ(P(S))` — com o
    valor exato `|S|·n` (v46), as duas metades de `0 < τ(P_F) < ∞` do
    memorando ficam em kernel na face finita. -/
theorem trace_cornerProj_pos [Nonempty n] {S : Finset G} (hS : S.Nonempty) :
    (0 : ℂ) < (cornerProj (n := n) S).trace := by
  rw [trace_cornerProj]
  have hpos : 0 < S.card * Fintype.card n :=
    Nat.mul_pos (Finset.card_pos.mpr hS) Fintype.card_pos
  have : (0 : ℝ) < ((S.card * Fintype.card n : ℕ) : ℝ) := by exact_mod_cast hpos
  exact_mod_cast Complex.zero_lt_real.mpr this

/-- [KERNEL] ★ ISOTONIA NA ORDEM DE LOEWNER: `S₁ ⊆ S₂ ⟹ P(S₁) ≤ P(S₂)` —
    a condição (4) do memorando na ordem genuína dos operadores (a diferença
    é a diagonal indicadora de `S₂ ∖ S₁`, positiva-semidefinida). -/
theorem cornerProj_loewner_mono {S₁ S₂ : Finset G} (hS : S₁ ⊆ S₂) :
    cornerProj (n := n) S₁ ≤ cornerProj S₂ := by
  rw [Matrix.le_iff]
  unfold cornerProj
  rw [Matrix.diagonal_sub]
  rw [Matrix.posSemidef_diagonal_iff]
  intro p
  by_cases h1 : p.1 ∈ S₁
  · simp [h1, hS h1]
  · by_cases h2 : p.1 ∈ S₂ <;> simp [h1, h2]

/-- [KERNEL] ★ O TRANSPORTE INTERNO FIXA O CANTO: `σ_t(P(S)) = P(S)` — a
    condição (2) do memorando (`Ad λ_φ(s)`-invariância) na forma de
    transporte do v54, composta da invariância modular do v46. -/
theorem sigma_fixes_cornerProj (u : G →* Matrix.unitaryGroup n ℂ)
    {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (S : Finset G) (t : ℝ) :
    sigma (piRep u ρ) t (cornerProj (n := n) S) = cornerProj S := by
  unfold sigma
  rw [← cornerProj_comm_modPow u hρ S t, mul_assoc, modPow_mul_neg, mul_one]

/-- [KERNEL] ★ A FAMÍLIA É GENUINAMENTE NÃO-CONSTANTE: regiões distintas
    dão cantos distintos — o transporte EXTERNO (condição (3), v46:
    `λ_g P(S) λ_gᴴ = P(gS)`) move a família de verdade; nada aqui é a
    família constante degenerada. -/
theorem cornerProj_ne_of_ne [Nonempty n] {S₁ S₂ : Finset G} (h : S₁ ≠ S₂) :
    cornerProj (n := n) S₁ ≠ cornerProj S₂ := by
  obtain ⟨g, hg⟩ : ∃ g, ¬(g ∈ S₁ ↔ g ∈ S₂) := by
    by_contra hall
    push Not at hall
    exact h (Finset.ext_iff.mpr fun a => hall a)
  intro heq
  have hentry : cornerProj (n := n) S₁ (g, Classical.arbitrary n)
      (g, Classical.arbitrary n)
      = cornerProj S₂ (g, Classical.arbitrary n) (g, Classical.arbitrary n) := by
    rw [heq]
  by_cases h1 : g ∈ S₁ <;> by_cases h2 : g ∈ S₂ <;>
    simp [cornerProj_apply, h1, h2] at hentry hg

/-- O TIPO DO TEOREMA DO CANTO (face finita): as quatro condições do
    memorando §4, mais projeção genuína e normalização total. RÍGIDO: o
    campo `trace_eq` (valor exato `|S|·n`) mata os habitantes triviais
    `P ≡ 1` (traço errado em `S ≠ G`) e `P ≡ 0` (traço errado em `S ≠ ∅`,
    e `total` falha) — a família constante não habita este tipo. -/
structure TransportedCornerFamily (u : G →* Matrix.unitaryGroup n ℂ)
    (ρ : Matrix n n ℂ) where
  /-- a família local `𝒪 ↦ P_F(𝒪)` (regiões = subconjuntos finitos). -/
  P : Finset G → Matrix (G × n) (G × n) ℂ
  /-- projeção: idempotente. -/
  idem : ∀ S, P S * P S = P S
  /-- projeção: autoadjunta. -/
  selfadj : ∀ S, (P S)ᴴ = P S
  /-- (4) ISOTONIA na ordem de Loewner. -/
  isotone : ∀ S₁ S₂, S₁ ⊆ S₂ → P S₁ ≤ P S₂
  /-- (3) COVARIÂNCIA pelo transporte externo: `U(g) P(S) U(g)* = P(gS)`. -/
  covariant : ∀ (g : G) (S : Finset G),
    lam (n := n) g * P S * (lam g)ᴴ = P (S.image fun a => g * a)
  /-- (2) INVARIÂNCIA pelo transporte modular interno: `σ_t(P(S)) = P(S)`. -/
  internal_invariant : ∀ (S : Finset G) (t : ℝ),
    sigma (piRep u ρ) t (P S) = P S
  /-- (1) o TRAÇO da região, exato: `τ(P(S)) = |S|·n` (donde `0 < τ < ∞`
      para regiões não-vazias — traço positivo e finito). -/
  trace_eq : ∀ S, (P S).trace = ((S.card * Fintype.card n : ℕ) : ℂ)
  /-- normalização: a região total é a identidade (`ω(I) = 1` tracial). -/
  total : P Finset.univ = 1

/-- ★ O TERMO: o canto covariante transportado CONSTRUÍDO — a face finita
    do `TGL_CANONICAL_FINITE_CORNER_THEOREM` habitada (v46 dá projeção,
    covariância, traço e total; v55 dá Loewner e o transporte interno). -/
noncomputable def canonicalTransportedCorner (u : G →* Matrix.unitaryGroup n ℂ)
    {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) : TransportedCornerFamily (n := n) u ρ where
  P := cornerProj (n := n)
  idem := cornerProj_idem
  selfadj := cornerProj_conjTranspose
  isotone := fun _ _ hS => cornerProj_loewner_mono hS
  covariant := fun g S => lam_conj_cornerProj g S
  internal_invariant := fun S t => sigma_fixes_cornerProj u hρ S t
  trace_eq := trace_cornerProj
  total := cornerProj_univ

/-- [KERNEL] ★ EXISTÊNCIA (corolário do termo): o teorema do canto tem
    testemunha na face finita, para todo grupo finito, toda representação
    unitária e todo estado fiel. O ABERTO é o mesmo enunciado no core
    genuíno (ℝ contínuo, Poincaré, II_∞). -/
theorem canonicalTransportedCorner_exists (u : G →* Matrix.unitaryGroup n ℂ)
    {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) :
    Nonempty (TransportedCornerFamily (n := n) u ρ) :=
  ⟨canonicalTransportedCorner u hρ⟩

end

end TGLExt
