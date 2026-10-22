import TGLExt.FiniteCrossedProduct
import TGLExt.GlobalLiftLadder

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A FAMÍLIA DO CANTO: localização, isotonia, covariância, traço finito e
  invariância modular — construída   [TGLExt — v46]

O teorema-alvo do gate do operador ("construir P_F local covariante com
0 < τ(P_F) < ∞ e [P_F, λ(s)] = 0"), na sua face KERNELIZÁVEL HOJE — com a
adjudicação da casa (FECHAMENTO_MATRIZ_S_CORE_II.md, 05/07/2026): a
EXISTÊNCIA de P com τ(P)=1 em II∞ é [REAL clássico]; a CANONICIDADE de
P_ℱ = s(ker H₃L) é classe unitária [REAL]; τ(P_ℱ)=1 é ω(I)=1 em forma
tracial [POSTULATE por design]. O que este arquivo PROVA [KERNEL]:

* ★ `corner_fixed_by_flow`: TODO canto espectral `cfc f H` de um `H` que
  comuta com o estado é FIXO pelo fluxo modular — `[P_F, λ(s)] = 0` sai
  DE GRAÇA da construção funcional (P_F = 1_{0}(H₃L) com H₃L função do
  gerador modular ⟹ invariância modular AUTOMÁTICA);
* ★ `DualScalingData.finite_trace_not_fixed`: τ(m) ≠ 0 ⟹ θ_{s₀}(m) ≠ m —
  o requisito `θ_s(P_F) ≠ P_F` do gate não precisa ser IMPOSTO: é
  TEOREMA (contrapositiva da obstrução v45; o no-go como bússola);
* ★ a FAMÍLIA DO CANTO CONSTRUÍDA no produto cruzado finito (v44):
  `cornerProj S` para regiões `S ⊆ G`, com TODOS os axiomas de rede:
  - projeção ortogonal (`cornerProj_idem`, `cornerProj_conjTranspose`);
  - LOCALIZAÇÃO/ISOTONIA: `S₁ ⊆ S₂ ⟹ P(S₁)·P(S₂) = P(S₁)` (P(S₁) ≼ P(S₂));
  - COVARIÂNCIA: `λ_g·P(S)·λ_gᴴ = P(g·S)` — o grupo move a região;
  - TRAÇO FINITO: `Tr P(S) = |S|·n` (positivo ⟺ região não-vazia);
  - INVARIÂNCIA MODULAR: `P(S)` comuta com π(A) e com o fluxo dual
    `(πρ)^{it}` — o canto atravessa a dinâmica modular sem deformar.

**HONESTIDADE.** Face finita + tipada. O que NÃO está aqui e segue com
seu estatuto: a não-trivialidade de `ker H₃L` no core GENUÍNO (III⋊ℝ)
[CONDITIONAL — falha nomeada `no_zero_lock_kernel`]; a rede AQFT
contínua de regiões de Minkowski (a testemunha plena); τ(P_ℱ)=1 como
escolha do Um [POSTULATE]. β JAMAIS entra: ρ, H, f, S genéricos.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — invariância modular de graça: o canto espectral é fixo pelo fluxo -/

/-- [KERNEL] ★ O CANTO ESPECTRAL É FIXO PELO FLUXO: se `H` comuta com o
    estado `ρ`, então TODA função espectral `cfc f H` (em particular a
    projeção-janela `P_F = 1_{[0,ε]}(H)`) é fixa pelo fluxo modular:
    `σ_t(cfc f H) = cfc f H`. A exigência `[P_F, λ(s)] = 0` do gate é
    AUTOMÁTICA para cantos construídos funcionalmente de um `H`
    compatível com o gerador modular. -/
theorem corner_fixed_by_flow (ρ H : Matrix n n ℂ) (h : Commute ρ H)
    (f : ℝ → ℝ) (t : ℝ) :
    sigma ρ t (cfc f H) = cfc f H :=
  sigma_fixed_of_commute ρ (cfc f H) ((h.symm.cfc_real f).symm) t

/-! ## B — o no-go como teorema positivo: traço finito ⟹ não θ-fixo -/

/-- [KERNEL] ★ TRAÇO NÃO-NULO PROÍBE A FIXAÇÃO DUAL: com a lei de escala
    de Takesaki, `τ(m) ≠ 0 ⟹ θ_{s₀}(m) ≠ m` para todo `s₀ > 0` — a
    contrapositiva da obstrução v45. O requisito `θ_s(P_F) ≠ P_F` do
    gate NÃO precisa ser imposto: qualquer canto de traço finito
    positivo o satisfaz POR TEOREMA (o no-go da casa virou bússola e
    agora virou lei). -/
theorem DualScalingData.finite_trace_not_fixed {M : Type} (D : DualScalingData M)
    {s₀ : ℝ} (hs : 0 < s₀) {m : M} (htau : D.tau m ≠ 0) :
    D.theta s₀ m ≠ m :=
  fun hfix => htau (D.fixed_tau_zero hs hfix)

/-! ## C — a família do canto no produto cruzado finito (v44) -/

variable {G : Type} [Group G] [Fintype G] [DecidableEq G]

/-- A FAMÍLIA DO CANTO: para cada região finita `S ⊆ G`, o projetor
    bloco-diagonal `P(S) = diag(1_{p.1 ∈ S})` no produto cruzado
    `M_{G×n}` — a sombra finita da rede local `𝒪 ↦ P_F(𝒪)`. -/
def cornerProj (S : Finset G) : Matrix (G × n) (G × n) ℂ :=
  Matrix.diagonal fun p => if p.1 ∈ S then 1 else 0

@[simp] theorem cornerProj_apply (S : Finset G) (p q : G × n) :
    cornerProj (n := n) S p q
      = if p = q then (if p.1 ∈ S then (1 : ℂ) else 0) else 0 := by
  by_cases h : p = q
  · subst h
    simp [cornerProj]
  · simp [cornerProj, h]

/-- [KERNEL] `P(S)` é IDEMPOTENTE. -/
theorem cornerProj_idem (S : Finset G) :
    cornerProj (n := n) S * cornerProj S = cornerProj S := by
  unfold cornerProj
  rw [diagonal_mul_diagonal]
  congr 1
  funext p
  by_cases h : p.1 ∈ S <;> simp [h]

/-- [KERNEL] `P(S)` é AUTOADJUNTO: projeção ortogonal genuína. -/
theorem cornerProj_conjTranspose (S : Finset G) :
    (cornerProj (n := n) S)ᴴ = cornerProj S := by
  unfold cornerProj
  rw [diagonal_conjTranspose]
  congr 1
  funext p
  by_cases h : p.1 ∈ S <;> simp [h]

/-- [KERNEL] ★ LOCALIZAÇÃO/ISOTONIA: `S₁ ⊆ S₂ ⟹ P(S₁)·P(S₂) = P(S₁)` —
    a região menor vive DENTRO da maior (`P(S₁) ≼ P(S₂)` como projeções;
    o axioma de isotonia da rede local, na sombra finita). -/
theorem cornerProj_mono {S₁ S₂ : Finset G} (hS : S₁ ⊆ S₂) :
    cornerProj (n := n) S₁ * cornerProj S₂ = cornerProj S₁ := by
  unfold cornerProj
  rw [diagonal_mul_diagonal]
  congr 1
  funext p
  by_cases h1 : p.1 ∈ S₁
  · simp [h1, hS h1]
  · simp [h1]

/-- [KERNEL] ★ COVARIÂNCIA: `λ_g·P(S)·λ_gᴴ = P(g·S)` — o unitário do
    grupo TRANSPORTA a região (`U(g)P_F(𝒪)U(g)* = P_F(g𝒪)`, o axioma de
    covariância da rede, na sombra finita; a MESMA λ_g do peso dual). -/
theorem lam_conj_cornerProj (g : G) (S : Finset G) :
    lam (n := n) g * cornerProj S * (lam g)ᴴ
      = cornerProj (S.image fun a => g * a) := by
  rw [lam_conjTranspose]
  ext p q
  rw [mul_lam_apply, lam_mul_apply]
  rcases eq_or_ne p q with h | h
  · subst h
    simp only [cornerProj_apply]
    have hmem : (g⁻¹ * p.1 ∈ S) ↔ (p.1 ∈ S.image fun a => g * a) := by
      constructor
      · intro hin
        exact Finset.mem_image.mpr ⟨g⁻¹ * p.1, hin, by rw [mul_inv_cancel_left]⟩
      · intro hin
        rcases Finset.mem_image.mp hin with ⟨a, ha, hga⟩
        rwa [← hga, inv_mul_cancel_left]
    by_cases hin : g⁻¹ * p.1 ∈ S
    · rw [if_pos hin, if_pos (hmem.mp hin)]
    · rw [if_neg hin, if_neg (fun hc => hin (hmem.mpr hc))]
  · have hne : (g⁻¹ * p.1, p.2) ≠ (g⁻¹ * q.1, q.2) := by
      intro hc
      apply h
      injection hc with h1 h2
      exact Prod.ext (mul_left_cancel h1) h2
    simp only [cornerProj_apply, if_neg hne, if_neg h]

/-- [KERNEL] ★ TRAÇO FINITO DA REGIÃO: `Tr P(S) = |S|·n` — positivo
    exatamente quando a região é não-vazia; a contabilidade honesta do
    canto (no core genuíno, `0 < τ(P_F) < ∞` com a escala inscrita pelo
    Um [POSTULATE ω(I)=1]). -/
theorem trace_cornerProj (S : Finset G) :
    (cornerProj (n := n) S).trace = ((S.card * Fintype.card n : ℕ) : ℂ) := by
  unfold cornerProj
  rw [Matrix.trace_diagonal, Fintype.sum_prod_type]
  have h : ∀ g : G, (∑ _i : n, (if g ∈ S then (1 : ℂ) else 0))
      = if g ∈ S then (Fintype.card n : ℂ) else 0 := by
    intro g
    by_cases hg : g ∈ S <;> simp [hg, Finset.card_univ]
  rw [Finset.sum_congr rfl fun g _ => h g, Finset.sum_ite_mem,
    Finset.univ_inter, Finset.sum_const, nsmul_eq_mul]
  push_cast
  ring

/-- [KERNEL] O CANTO COMUTA COM A BASE: `P(S)·π(a) = π(a)·P(S)` — o
    projetor da região é bloco-escalar (o mesmo mecanismo da ação dual). -/
theorem cornerProj_comm_piRep (u : G →* Matrix.unitaryGroup n ℂ)
    (S : Finset G) (a : Matrix n n ℂ) :
    cornerProj (n := n) S * piRep u a = piRep u a * cornerProj S := by
  ext p q
  simp only [cornerProj, Matrix.diagonal_mul, Matrix.mul_diagonal, piRep_apply]
  rcases eq_or_ne p.1 q.1 with h | h
  · rw [h]
    exact mul_comm _ _
  · simp only [if_neg h, mul_zero, zero_mul]

/-- [KERNEL] ★ INVARIÂNCIA MODULAR DO CANTO: `P(S)` comuta com o fluxo
    modular do peso dual `(πρ)^{it}` — `[P_F, λ_φ(s)] = 0` do gate, na
    sombra finita: o canto atravessa a dinâmica sem deformar. -/
theorem cornerProj_comm_modPow (u : G →* Matrix.unitaryGroup n ℂ)
    {ρ : Matrix n n ℂ} (hρ : ρ.PosDef) (S : Finset G) (t : ℝ) :
    cornerProj (n := n) S * modPow (piRep u ρ) t
      = modPow (piRep u ρ) t * cornerProj S := by
  rw [modPow_piRep u hρ]
  exact cornerProj_comm_piRep u S (modPow ρ t)

/-- [KERNEL] O canto da região TOTAL é a identidade: `P(G) = 1` — a
    família esgota o palco (τ-normalização do todo = ω(I)=1 em forma
    finita). -/
theorem cornerProj_univ : cornerProj (n := n) (Finset.univ : Finset G) = 1 := by
  unfold cornerProj
  rw [← Matrix.diagonal_one]
  congr 1
  funext p
  simp

end

end TGLExt
