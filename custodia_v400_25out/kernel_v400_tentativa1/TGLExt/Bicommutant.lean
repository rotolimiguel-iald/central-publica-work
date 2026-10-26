import TGLExt.MarkovTower

set_option autoImplicit false

/-!
# O bicomutante geral finito   [TGLExt — Degrau 1 (fecho)]

O TEOREMA DO BICOMUTANTE para subálgebras-* arbitrárias de `Mₙ(ℂ)` agindo
em `H = Mₙ(ℂ)` por multiplicação à esquerda — a peça que faltava do
Degrau 1 (LeftRight.lean fez o caso `A = Mₙ` pleno):

* (B1) RECONSTRUÇÃO: todo superoperador `Φ ∈ End(H)` é
  `Σ_{k,l} L_{C^{kl}} R_{E_{kl}}` com `C^{kl} := Cmat Φ k l` — `End(H)`
  é gerado por multiplicações à esquerda e à direita;
* (B2) EXTRAÇÃO: os coeficientes `C^{kl}` são únicos (lidos de volta);
* (B3) ESTRUTURA DO COMUTANTE: se `Φ` comuta com `L(A)`, cada `C^{kl}`
  comuta com `A` em `Mₙ` — `L(A)′ ⊆ span{L_x R_y : x ∈ A′}`;
* (B4) COMPLEMENTO DE FROBENIUS: `W ⊕ W^⊥ = H` para todo submódulo,
  SEM instância de produto interno (contagem de posto + definitude
  do traço `Tr(xᴴx)`);
* (B5) REDUÇÃO: para `A` fechada por produto e estrela, o projetor de
  Frobenius sobre `span A` comuta com `L(A)`;
* (B6) O TEOREMA: `1 ∈ A`, `A·A ⊆ A`, `Aᴴ = A` ⟹
  `L(A)′′ = L(span_ℂ A)` — em dimensão finita o fecho de von Neumann
  é o fecho LINEAR (a topologia é grátis).

β NÃO entra: infraestrutura pura. Sem sorry, sem axiom.
Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## B1 — a matriz de coeficientes e a reconstrução -/

omit [Fintype n] in
/-- A matriz de coeficientes `C^{kl}` de um superoperador `Φ ∈ End(Mₙ(ℂ))`:
    `(Cmat Φ k l) i j = (Φ E_{jk}) i l`. -/
def Cmat (Φ : Module.End ℂ (Matrix n n ℂ)) (k l : n) : Matrix n n ℂ :=
  Matrix.of fun i j => (Φ (Matrix.single j k 1)) i l

omit [Fintype n] in
@[simp] theorem Cmat_apply (Φ : Module.End ℂ (Matrix n n ℂ)) (k l i j : n) :
    Cmat Φ k l i j = (Φ (Matrix.single j k 1)) i l := rfl

/-- [KERNEL] RECONSTRUÇÃO DE SUPEROPERADORES: todo `Φ ∈ End(H)`,
    `H = Mₙ(ℂ)`, é soma `Σ_{k,l} L_{C^{kl}} R_{E_{kl}}` — o palco inteiro
    é gerado pelas multiplicações à esquerda e à direita. -/
theorem end_reconstruction (Φ : Module.End ℂ (Matrix n n ℂ)) :
    Φ = ∑ p : n × n, Lmul (Cmat Φ p.1 p.2) * Rmul (Matrix.single p.1 p.2 1) := by
  refine (Matrix.stdBasis ℂ n n).ext fun pq => ?_
  obtain ⟨p, q⟩ := pq
  rw [Matrix.stdBasis_eq_single, LinearMap.sum_apply]
  ext i j
  rw [Matrix.sum_apply, Fintype.sum_eq_single ((q, j) : n × n)]
  · simp only [Module.End.mul_apply, Lmul_apply, Rmul_apply,
      Matrix.single_mul_single_same, Matrix.mul_single_apply_same,
      mul_one, Cmat_apply]
  · rintro ⟨k, l⟩ hkl
    simp only [Module.End.mul_apply, Lmul_apply, Rmul_apply]
    by_cases hk : q = k
    · subst hk
      have hl : j ≠ l := fun h => hkl (by rw [h])
      rw [Matrix.single_mul_single_same, one_mul,
        Matrix.mul_single_apply_of_ne (hbj := hl)]
    · rw [Matrix.single_mul_single_of_ne (h := hk), mul_zero, Matrix.zero_apply]

/-! ## B2 — unicidade/extração dos coeficientes -/

/-- [KERNEL] EXTRAÇÃO: os coeficientes de `Σ L_{D^{kl}} R_{E_{kl}}` são
    exatamente os `D^{kl}` — a decomposição de B1 é única. -/
theorem Cmat_of_sum (D : n → n → Matrix n n ℂ) (k₀ l₀ : n) :
    Cmat (∑ p : n × n, Lmul (D p.1 p.2) * Rmul (Matrix.single p.1 p.2 1)) k₀ l₀
      = D k₀ l₀ := by
  ext i j
  rw [Cmat_apply, LinearMap.sum_apply, Matrix.sum_apply,
    Fintype.sum_eq_single ((k₀, l₀) : n × n)]
  · simp only [Module.End.mul_apply, Lmul_apply, Rmul_apply,
      Matrix.single_mul_single_same, Matrix.mul_single_apply_same, mul_one]
  · rintro ⟨k, l⟩ hkl
    simp only [Module.End.mul_apply, Lmul_apply, Rmul_apply]
    by_cases hk : k₀ = k
    · subst hk
      have hl : l₀ ≠ l := fun h => hkl (by rw [h])
      rw [Matrix.single_mul_single_same, one_mul,
        Matrix.mul_single_apply_of_ne (hbj := hl)]
    · rw [Matrix.single_mul_single_of_ne (h := hk), mul_zero, Matrix.zero_apply]

/-! ## B3 — a estrutura do comutante -/

/-- `a·E_{jk} = Σ_m (a m j) • E_{mk}`: multiplicar a matriz-unidade pela
    esquerda põe a coluna `j` de `a` na coluna `k`. -/
theorem mul_single_one_eq_sum (a : Matrix n n ℂ) (j k : n) :
    a * Matrix.single j k 1 = ∑ m, a m j • Matrix.single m k (1 : ℂ) := by
  ext s t
  rw [Matrix.sum_apply]
  by_cases ht : t = k
  · subst ht
    rw [Matrix.mul_single_apply_same, mul_one,
      Fintype.sum_eq_single s (fun m hm => by
        rw [Matrix.smul_apply, Matrix.single_apply_of_row_ne hm, smul_zero]),
      Matrix.smul_apply, Matrix.single_apply_same, smul_eq_mul, mul_one]
  · rw [Matrix.mul_single_apply_of_ne (hbj := ht)]
    refine (Finset.sum_eq_zero fun m _ => ?_).symm
    rw [Matrix.smul_apply, Matrix.single_apply_of_col_ne _ _ (Ne.symm ht), smul_zero]

/-- Os coeficientes de `L_a ∘ Φ`: multiplicação à esquerda em cada `C^{kl}`. -/
theorem Cmat_Lmul_left (a : Matrix n n ℂ) (Φ : Module.End ℂ (Matrix n n ℂ)) (k l : n) :
    Cmat (Lmul a * Φ) k l = a * Cmat Φ k l := by
  ext i j
  simp only [Cmat_apply, Module.End.mul_apply, Lmul_apply, Matrix.mul_apply]

/-- Os coeficientes de `Φ ∘ L_a`: multiplicação à direita em cada `C^{kl}`. -/
theorem Cmat_Lmul_right (a : Matrix n n ℂ) (Φ : Module.End ℂ (Matrix n n ℂ)) (k l : n) :
    Cmat (Φ * Lmul a) k l = Cmat Φ k l * a := by
  ext i j
  rw [Cmat_apply, Module.End.mul_apply, Lmul_apply, mul_single_one_eq_sum a j k,
    map_sum, Matrix.sum_apply, Matrix.mul_apply]
  refine Finset.sum_congr rfl fun m _ => ?_
  rw [map_smul, Matrix.smul_apply, smul_eq_mul, Cmat_apply, mul_comm]

/-- [KERNEL] ESTRUTURA DO COMUTANTE: se `Φ` comuta com `L(A)`, cada
    coeficiente `C^{kl}` comuta com `A` dentro de `Mₙ(ℂ)`. -/
theorem commutant_Cmat_comm {A : Set (Matrix n n ℂ)}
    {Φ : Module.End ℂ (Matrix n n ℂ)} (hΦ : Φ ∈ commutantSet (Lmul '' A))
    {a : Matrix n n ℂ} (ha : a ∈ A) (k l : n) :
    a * Cmat Φ k l = Cmat Φ k l * a := by
  have h : Lmul a * Φ = Φ * Lmul a := hΦ (Lmul a) ⟨a, ha, rfl⟩
  calc a * Cmat Φ k l = Cmat (Lmul a * Φ) k l := (Cmat_Lmul_left a Φ k l).symm
    _ = Cmat (Φ * Lmul a) k l := by rw [h]
    _ = Cmat Φ k l * a := Cmat_Lmul_right a Φ k l

/-- [KERNEL] `L(A)′ ⊆ span{L_x R_y : x ∈ A′}`: todo elemento do comutante
    de `L(A)` é combinação linear de `L_x R_y` com `x` no comutante de `A`
    em `Mₙ(ℂ)` — B1 + B3 em forma de span. -/
theorem exists_span_form {A : Set (Matrix n n ℂ)}
    {Φ : Module.End ℂ (Matrix n n ℂ)} (hΦ : Φ ∈ commutantSet (Lmul '' A)) :
    Φ ∈ Submodule.span ℂ {f : Module.End ℂ (Matrix n n ℂ) |
      ∃ x y : Matrix n n ℂ, (∀ a ∈ A, a * x = x * a) ∧ f = Lmul x * Rmul y} := by
  rw [end_reconstruction Φ]
  exact sum_mem fun p _ => Submodule.subset_span
    ⟨Cmat Φ p.1 p.2, Matrix.single p.1 p.2 1,
      fun a ha => commutant_Cmat_comm hΦ ha p.1 p.2, rfl⟩

/-! ## B4 — o complemento de Frobenius (sem instância de produto interno) -/

omit [DecidableEq n] in
theorem frob_zero_left (x : Matrix n n ℂ) : frob 0 x = 0 := by
  simp [frob]

omit [DecidableEq n] in
theorem frob_zero_right (w : Matrix n n ℂ) : frob w 0 = 0 := by
  simp [frob]

omit [DecidableEq n] in
theorem frob_add_left (x y w : Matrix n n ℂ) :
    frob (x + y) w = frob x w + frob y w := by
  simp [frob, conjTranspose_add, add_mul]

omit [DecidableEq n] in
theorem frob_add_right (w x y : Matrix n n ℂ) :
    frob w (x + y) = frob w x + frob w y := by
  simp [frob, mul_add]

omit [DecidableEq n] in
/-- `frob` é ANTIlinear na primeira variável. -/
theorem frob_smul_left (c : ℂ) (x w : Matrix n n ℂ) :
    frob (c • x) w = star c * frob x w := by
  simp [frob, conjTranspose_smul, Matrix.smul_mul, smul_eq_mul]

omit [DecidableEq n] in
/-- `frob` é linear na segunda variável. -/
theorem frob_smul_right (c : ℂ) (w x : Matrix n n ℂ) :
    frob w (c • x) = c * frob w x := by
  simp [frob, Matrix.mul_smul, smul_eq_mul]

omit [DecidableEq n] in
/-- [KERNEL] A forma de Frobenius é DEFINIDA: `⟨x,x⟩ = 0 ↔ x = 0`
    (via `Tr(xᴴx)` em anel star-ordenado — sem análise). -/
theorem frob_self_eq_zero_iff (x : Matrix n n ℂ) : frob x x = 0 ↔ x = 0 :=
  Matrix.trace_conjTranspose_mul_self_eq_zero_iff

/-- O complemento de Frobenius de um submódulo:
    `W^⊥ = {x | ∀ w ∈ W, ⟨w,x⟩ = 0}`. -/
def frobOrtho (W : Submodule ℂ (Matrix n n ℂ)) : Submodule ℂ (Matrix n n ℂ) where
  carrier := {x | ∀ w ∈ W, frob w x = 0}
  add_mem' := fun {x y} hx hy w hw => by
    rw [frob_add_right, hx w hw, hy w hw, add_zero]
  zero_mem' := fun w _ => frob_zero_right w
  smul_mem' := fun c x hx w hw => by rw [frob_smul_right, hx w hw, mul_zero]

omit [DecidableEq n] in
theorem mem_frobOrtho {W : Submodule ℂ (Matrix n n ℂ)} {x : Matrix n n ℂ} :
    x ∈ frobOrtho W ↔ ∀ w ∈ W, frob w x = 0 := Iff.rfl

omit [DecidableEq n] in
/-- [KERNEL] `W ⊓ W^⊥ = ⊥`: a definitude mata a interseção. -/
theorem disjoint_frobOrtho (W : Submodule ℂ (Matrix n n ℂ)) :
    Disjoint W (frobOrtho W) := by
  rw [Submodule.disjoint_def]
  intro x hxW hxO
  exact (frob_self_eq_zero_iff x).mp (mem_frobOrtho.mp hxO x hxW)

/-- O mapa de teste de Frobenius contra uma família finita de vetores. -/
def frobTest {d : ℕ} (v : Fin d → Matrix n n ℂ) :
    Matrix n n ℂ →ₗ[ℂ] (Fin d → ℂ) where
  toFun x i := frob (v i) x
  map_add' x y := funext fun i => frob_add_right (v i) x y
  map_smul' c x := funext fun i => frob_smul_right c (v i) x

omit [DecidableEq n] in
/-- Quem aniquila cada gerador aniquila todo o gerado (a antilinearidade
    na primeira variável atravessa o `span`). -/
theorem frob_eq_zero_of_span {d : ℕ} (v : Fin d → Matrix n n ℂ)
    {x : Matrix n n ℂ} (hx : ∀ i, frob (v i) x = 0) {w : Matrix n n ℂ}
    (hw : w ∈ Submodule.span ℂ (Set.range v)) : frob w x = 0 := by
  induction hw using Submodule.span_induction with
  | mem u hu => obtain ⟨i, rfl⟩ := hu; exact hx i
  | zero => exact frob_zero_left x
  | add u v _ _ ihu ihv => rw [frob_add_left, ihu, ihv, add_zero]
  | smul c u _ ih => rw [frob_smul_left, ih, mul_zero]

omit [DecidableEq n] in
/-- CONTAGEM DE POSTO: `dim H ≤ dim W + dim W^⊥` — rank-nullity aplicado
    ao mapa de teste contra uma base de `W`. -/
theorem finrank_le_add_frobOrtho (W : Submodule ℂ (Matrix n n ℂ)) :
    Module.finrank ℂ (Matrix n n ℂ)
      ≤ Module.finrank ℂ W + Module.finrank ℂ (frobOrtho W) := by
  obtain ⟨s, hs⟩ : ∃ s : Fin (Module.finrank ℂ W) → Matrix n n ℂ,
      Submodule.span ℂ (Set.range s) = W := by
    refine ⟨fun i => ((Module.finBasis ℂ W i : W) : Matrix n n ℂ), ?_⟩
    have hcomp : (fun i => ((Module.finBasis ℂ W i : W) : Matrix n n ℂ))
        = W.subtype ∘ (Module.finBasis ℂ W) := rfl
    rw [hcomp, Set.range_comp, Submodule.span_image, Module.Basis.span_eq,
      Submodule.map_top, Submodule.range_subtype]
  have hker : LinearMap.ker (frobTest s) ≤ frobOrtho W := fun x hx =>
    mem_frobOrtho.mpr fun w hw =>
      frob_eq_zero_of_span s (fun i => congr_fun (LinearMap.mem_ker.mp hx) i)
        (by rw [hs]; exact hw)
  have hrn := LinearMap.finrank_range_add_finrank_ker (frobTest s)
  have h1 := Submodule.finrank_le (LinearMap.range (frobTest s))
  rw [Module.finrank_pi, Fintype.card_fin] at h1
  have h2 := Submodule.finrank_mono hker
  omega

omit [DecidableEq n] in
/-- [KERNEL] O COMPLEMENTO DE FROBENIUS É COMPLEMENTO: `W ⊕ W^⊥ = H`,
    sem instância de produto interno (disjunção + contagem de posto). -/
theorem isCompl_frobOrtho (W : Submodule ℂ (Matrix n n ℂ)) :
    IsCompl W (frobOrtho W) :=
  (Submodule.isCompl_iff_disjoint W (frobOrtho W)
    (finrank_le_add_frobOrtho W)).mpr (disjoint_frobOrtho W)

/-- O projetor de Frobenius sobre `W` (ao longo de `W^⊥`), como
    endomorfismo de `H`. -/
def frobProj (W : Submodule ℂ (Matrix n n ℂ)) : Module.End ℂ (Matrix n n ℂ) :=
  W.projection (frobOrtho W) (isCompl_frobOrtho W)

omit [DecidableEq n] in
theorem frobProj_apply_of_mem_left {W : Submodule ℂ (Matrix n n ℂ)}
    {x : Matrix n n ℂ} (hx : x ∈ W) : frobProj W x = x :=
  Submodule.projection_apply_of_mem_left _ hx

omit [DecidableEq n] in
theorem frobProj_apply_of_mem_ortho {W : Submodule ℂ (Matrix n n ℂ)}
    {x : Matrix n n ℂ} (hx : x ∈ frobOrtho W) : frobProj W x = 0 :=
  Submodule.projection_apply_of_mem_right _ hx

omit [DecidableEq n] in
theorem frobProj_apply_mem (W : Submodule ℂ (Matrix n n ℂ)) (x : Matrix n n ℂ) :
    frobProj W x ∈ W :=
  Submodule.projection_apply_mem _ x

omit [DecidableEq n] in
theorem sub_frobProj_mem (W : Submodule ℂ (Matrix n n ℂ)) (x : Matrix n n ℂ) :
    x - frobProj W x ∈ frobOrtho W := by
  have h := Submodule.projection_eq_self_sub_projection (isCompl_frobOrtho W) x
  have h2 := Submodule.projection_apply_mem (isCompl_frobOrtho W).symm x
  rw [h] at h2
  exact h2

/-! ## B5 — a redução: o projetor comuta com a álgebra -/

omit [DecidableEq n] in
/-- `span A` é estável por multiplicação à esquerda por `A` (quando
    `A·A ⊆ A`). -/
theorem span_mul_mem {A : Set (Matrix n n ℂ)}
    (hmul : ∀ a ∈ A, ∀ b ∈ A, a * b ∈ A) {a : Matrix n n ℂ} (ha : a ∈ A)
    {w : Matrix n n ℂ} (hw : w ∈ Submodule.span ℂ A) :
    a * w ∈ Submodule.span ℂ A := by
  induction hw using Submodule.span_induction with
  | mem b hb => exact Submodule.subset_span (hmul a ha b hb)
  | zero => rw [mul_zero]; exact Submodule.zero_mem _
  | add u v _ _ ihu ihv => rw [mul_add]; exact Submodule.add_mem _ ihu ihv
  | smul c u _ ih => rw [Matrix.mul_smul]; exact Submodule.smul_mem _ c ih

omit [DecidableEq n] in
/-- `(span A)^⊥` é estável por multiplicação à esquerda por `A` (quando
    `A` é fechada por estrela): `⟨s, a·t⟩ = ⟨aᴴ·s, t⟩ = 0`. -/
theorem frobOrtho_mul_mem {A : Set (Matrix n n ℂ)}
    (hmul : ∀ a ∈ A, ∀ b ∈ A, a * b ∈ A) (hstar : ∀ a ∈ A, aᴴ ∈ A)
    {a : Matrix n n ℂ} (ha : a ∈ A) {t : Matrix n n ℂ}
    (ht : t ∈ frobOrtho (Submodule.span ℂ A)) :
    a * t ∈ frobOrtho (Submodule.span ℂ A) := by
  refine mem_frobOrtho.mpr fun s hs => ?_
  have key : frob s (a * t) = frob (aᴴ * s) t := by
    simp only [frob, conjTranspose_mul, conjTranspose_conjTranspose, mul_assoc]
  rw [key]
  exact mem_frobOrtho.mp ht (aᴴ * s) (span_mul_mem hmul (hstar a ha) hs)

/-- [KERNEL] REDUÇÃO: para `A` fechada por produto e estrela, o projetor
    de Frobenius sobre `span A` comuta com toda `L_a`, `a ∈ A` —
    decomposição `x = w + t`, `a·w ∈ W`, `a·t ∈ W^⊥`. -/
theorem frobProj_comm_Lmul {A : Set (Matrix n n ℂ)}
    (hmul : ∀ a ∈ A, ∀ b ∈ A, a * b ∈ A) (hstar : ∀ a ∈ A, aᴴ ∈ A)
    {a : Matrix n n ℂ} (ha : a ∈ A) :
    Lmul a * frobProj (Submodule.span ℂ A)
      = frobProj (Submodule.span ℂ A) * Lmul a := by
  refine LinearMap.ext fun x => ?_
  simp only [Module.End.mul_apply, Lmul_apply]
  have hsplit : a * x
      = a * frobProj (Submodule.span ℂ A) x
        + a * (x - frobProj (Submodule.span ℂ A) x) := by
    rw [← mul_add]
    congr 1
    abel
  rw [hsplit, map_add,
    frobProj_apply_of_mem_left (span_mul_mem hmul ha (frobProj_apply_mem _ x)),
    frobProj_apply_of_mem_ortho (frobOrtho_mul_mem hmul hstar ha (sub_frobProj_mem _ x)),
    add_zero]

/-! ## B6 — o teorema do bicomutante geral finito -/

omit [Fintype n] [DecidableEq n] in
/-- O comutante é fechado por escalar (complemento aos lemas da semente
    de Commutant.lean, aqui na álgebra `End(H)`). -/
theorem smul_mem_commutant {S : Set (Module.End ℂ (Matrix n n ℂ))}
    {T : Module.End ℂ (Matrix n n ℂ)} (c : ℂ) (hT : T ∈ commutantSet S) :
    c • T ∈ commutantSet S :=
  fun s hs => by rw [mul_smul_comm, smul_mul_assoc, hT s hs]

theorem Lmul_zero : Lmul (0 : Matrix n n ℂ) = 0 :=
  LinearMap.ext fun x => by simp

theorem Lmul_add (a b : Matrix n n ℂ) : Lmul (a + b) = Lmul a + Lmul b :=
  LinearMap.ext fun x => by simp [add_mul]

theorem Lmul_smul (c : ℂ) (a : Matrix n n ℂ) : Lmul (c • a) = c • Lmul a :=
  LinearMap.ext fun x => by simp

/-- [KERNEL] O TEOREMA DO BICOMUTANTE GERAL FINITO: para `A ⊆ Mₙ(ℂ)` com
    `1 ∈ A`, `A·A ⊆ A` e `Aᴴ = A`, o bicomutante da representação padrão
    é o fecho LINEAR: `L(A)′′ = L(span_ℂ A)`. Em dimensão finita o fecho
    de von Neumann é grátis — a topologia não acrescenta nada. A prova:
    `T ∈ L(A)′′` comuta com todo `R_b ∈ L(A)′`, logo `T = L_x` (LeftRight);
    o projetor de Frobenius `p` sobre `span A` está em `L(A)′` (B4+B5),
    logo `T` comuta com `p`; avaliando em `1`: `x = p x ∈ span A`. -/
theorem finite_bicommutant {A : Set (Matrix n n ℂ)}
    (hone : (1 : Matrix n n ℂ) ∈ A)
    (hmul : ∀ a ∈ A, ∀ b ∈ A, a * b ∈ A)
    (hstar : ∀ a ∈ A, aᴴ ∈ A) :
    commutantSet (commutantSet (Lmul '' A))
      = Lmul '' (Submodule.span ℂ A : Set (Matrix n n ℂ)) := by
  apply Set.Subset.antisymm
  · intro T hT
    have hsub : Set.range (Rmul (n := n)) ⊆ commutantSet (Lmul '' A) := by
      rintro _ ⟨b, rfl⟩ _ ⟨a, -, rfl⟩
      exact lmul_mul_rmul_comm a b
    have hR : T ∈ commutantSet (Set.range (Rmul (n := n))) :=
      commutant_antitone hsub hT
    rw [commutant_range_Rmul] at hR
    obtain ⟨x, rfl⟩ := hR
    have h1W : (1 : Matrix n n ℂ) ∈ Submodule.span ℂ A := Submodule.subset_span hone
    have hP : frobProj (Submodule.span ℂ A) ∈ commutantSet (Lmul '' A) := by
      rintro _ ⟨a, ha, rfl⟩
      exact frobProj_comm_Lmul hmul hstar ha
    have hx := LinearMap.congr_fun (hT (frobProj (Submodule.span ℂ A)) hP) 1
    simp only [Module.End.mul_apply, Lmul_apply, mul_one,
      frobProj_apply_of_mem_left h1W] at hx
    exact ⟨x, hx ▸ frobProj_apply_mem (Submodule.span ℂ A) x, rfl⟩
  · rintro _ ⟨x, hx, rfl⟩
    rw [SetLike.mem_coe] at hx
    induction hx using Submodule.span_induction with
    | mem a ha => exact subset_bicommutant _ ⟨a, ha, rfl⟩
    | zero => rw [Lmul_zero]; exact zero_mem_commutant _
    | add u v _ _ ihu ihv => rw [Lmul_add]; exact add_mem_commutant ihu ihv
    | smul c u _ ih => rw [Lmul_smul]; exact smul_mem_commutant c ih

end

end TGLExt
