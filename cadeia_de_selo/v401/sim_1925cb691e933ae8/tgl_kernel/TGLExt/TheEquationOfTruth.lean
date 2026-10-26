/- [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\equacao_da_verdade\cetico\lean\TheEquationOfTruth.lean` (sha16 35b91f86b88b8e6c): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: flow → truthFlow.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA] -/
/-
  TheEquationOfTruth.lean — pre-resolucao Lean da gerencia (23/09/2026), frente V3.
  [INPUT] a «equacao da verdade» colada pelo operador (texto do canal ChatGPT, [DECLARADO]).
  Este arquivo tipa, em kernel, as implicacoes MATEMATICAS do texto. Nao move gate nenhum.
  Homonimos: a anulacao da leitura (d/ds P(T_s x) = 0), o zero modular (K Ω = 0) e a anulacao
  do perfil (a'(0) = 0) sao TRES objetos distintos; nenhum lema aqui os identifica.
  O `Q H` (direcoes atenuadas) deste arquivo NAO e «o fundo» da TGL.
-/
import Mathlib
import TGLExt.TheNameIsTheInstrument

open scoped InnerProductSpace Nat
open Filter Topology

namespace TGLExt.EquationOfTruth

/-! ## (1) O bit da verdade: V(b, b̂) = 1 − (b − b̂)² -/

/-- A valoracao da atribuicao binaria. -/
def truthValue (b bh : ℤ) : ℤ := 1 - (b - bh) ^ 2

theorem truthValue_table :
    truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 0 ∧ truthValue 0 1 = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [truthValue]

theorem truthBit_eq_one_iff (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 1 ↔ b = bh := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

theorem truthBit_eq_zero_iff (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 0 ↔ b ≠ bh := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

/-- Nos bits, V so assume 0 ou 1 (e bivalente). -/
theorem truthBit_bivalent (b bh : ℤ) (hb : b = 0 ∨ b = 1) (hbh : bh = 0 ∨ bh = 1) :
    truthValue b bh = 0 ∨ truthValue b bh = 1 := by
  rcases hb with rfl | rfl <;> rcases hbh with rfl | rfl <;> norm_num [truthValue]

/-! ## (2) Os tres vinculos: ker (Σ D_j† D_j) = ⋂ ker D_j -/

section Penalty

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- A penalidade dos vinculos: H = Σ_j D_j† D_j. -/
noncomputable def penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) : E →L[𝕜] E :=
  ∑ j, ContinuousLinearMap.adjoint (D j) * D j

theorem re_inner_adjoint_mul_self (A : E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, (ContinuousLinearMap.adjoint A * A) x⟫_𝕜 = ‖A x‖ ^ 2 := by
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.adjoint_inner_right,
    inner_self_eq_norm_sq]

/-- A forma quadratica da penalidade e a soma dos quadrados dos defeitos. -/
theorem re_inner_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, penalty D x⟫_𝕜 = ∑ j, ‖D j x‖ ^ 2 := by
  simp only [penalty, ContinuousLinearMap.sum_apply, inner_sum, map_sum]
  exact Finset.sum_congr rfl fun j _ => re_inner_adjoint_mul_self (D j) x

/-- A familia e a exclusao conjunta: ker H = ⋂_j ker D_j (uma violacao nao compensa outra). -/
theorem ker_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) :
    (penalty D).ker = ⨅ j, (D j).ker := by
  ext x
  simp only [Submodule.mem_iInf, LinearMap.mem_ker]
  constructor
  · intro h j
    have h0 : ∑ j, ‖D j x‖ ^ 2 = 0 := by
      have h' : (penalty D) x = 0 := h
      rw [← re_inner_penalty, h', inner_zero_right, map_zero]
    have hj := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg ‖D j x‖)).1 h0 j
      (Finset.mem_univ _)
    exact norm_eq_zero.1 (pow_eq_zero_iff two_ne_zero |>.1 hj)
  · intro h
    simp [penalty, h]

/-- A forma com tres operadores, literal: ker (D₁†D₁ + D₂†D₂ + D₃†D₃) = ker D₁ ⊓ ker D₂ ⊓ ker D₃. -/
theorem ker_threeLocks (D₁ D₂ D₃ : E →L[𝕜] E) :
    (ContinuousLinearMap.adjoint D₁ * D₁ + ContinuousLinearMap.adjoint D₂ * D₂
        + ContinuousLinearMap.adjoint D₃ * D₃).ker
      = D₁.ker ⊓ D₂.ker ⊓ D₃.ker := by
  have h := ker_penalty (𝕜 := 𝕜) ![D₁, D₂, D₃]
  simp only [penalty, Fin.sum_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons] at h
  rw [h]
  ext x
  simp only [Submodule.mem_iInf, Submodule.mem_inf, Fin.forall_fin_succ, IsEmpty.forall_iff,
    Matrix.cons_val_zero, Matrix.cons_val_succ, and_true, and_assoc]

/-- A penalidade e auto-adjunta. -/
theorem isSelfAdjoint_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) :
    IsSelfAdjoint (penalty D) := by
  unfold penalty
  refine isSelfAdjoint_sum _ fun j _ => ?_
  rw [← ContinuousLinearMap.star_eq_adjoint]
  exact IsSelfAdjoint.star_mul_self (D j)

/-- A seletora apofatica A_C = −H e nao-positiva: Re⟪x, A_C x⟫ ≤ 0. -/
theorem selector_nonpos {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E) (x : E) :
    RCLike.re ⟪x, (-penalty D) x⟫_𝕜 ≤ 0 := by
  rw [ContinuousLinearMap.neg_apply, inner_neg_right, map_neg, re_inner_penalty, neg_nonpos]
  exact Finset.sum_nonneg fun j _ => sq_nonneg _

end Penalty

/-! ## (3) P H = 0 e H P = 0 para P = projecao ortogonal sobre ker H, H auto-adjunto -/

section Projection

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

theorem H_mul_proj (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection] :
    H * H.ker.starProjection = 0 := by
  ext x
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.zero_apply]
  exact LinearMap.mem_ker.1 (H.ker.starProjection_apply_mem x)

theorem proj_mul_H (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection] :
    H.ker.starProjection * H = 0 := by
  ext x
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.zero_apply,
    Submodule.starProjection_apply_eq_zero_iff, Submodule.mem_orthogonal]
  intro u hu
  have e : ⟪H u, x⟫_𝕜 = ⟪u, H x⟫_𝕜 := hH.isSymmetric u x
  have hu0 : H u = 0 := LinearMap.mem_ker.1 hu
  rw [← e, hu0, inner_zero_left]

end Projection

/-! ## (4) P · exp(−sH) = P e a conservacao da leitura I(T_s x) = I(x) -/

section Exponential

variable {𝔸 : Type*} [NormedRing 𝔸] [CompleteSpace 𝔸]

/-- Algebra pura: se P A = 0 entao P · exp A = P (pela serie). -/
theorem mul_exp_eq_of_mul_eq_zero (𝕂 : Type*) [RCLike 𝕂] [NormedAlgebra 𝕂 𝔸] (P A : 𝔸) (h : P * A = 0) :
    P * NormedSpace.exp A = P := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕂) A).mul_left P
  have h1 : HasSum (fun n : ℕ => P * ((n !⁻¹ : 𝕂) • A ^ n)) P := by
    have hf : (fun n : ℕ => P * ((n !⁻¹ : 𝕂) • A ^ n)) = fun n => if n = 0 then P else 0 := by
      funext n
      cases n with
      | zero => simp
      | succ n => simp [pow_succ', ← mul_assoc, h]
    rw [hf]
    exact hasSum_ite_eq 0 P
  exact hs.unique h1

/-- Simetrica: se A P = 0 entao exp A · P = P. -/
theorem exp_mul_eq_of_mul_eq_zero (𝕂 : Type*) [RCLike 𝕂] [NormedAlgebra 𝕂 𝔸] (P A : 𝔸) (h : A * P = 0) :
    NormedSpace.exp A * P = P := by
  have hs := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕂) A).mul_right P
  have h1 : HasSum (fun n : ℕ => ((n !⁻¹ : 𝕂) • A ^ n) * P) P := by
    have hf : (fun n : ℕ => ((n !⁻¹ : 𝕂) • A ^ n) * P) = fun n => if n = 0 then P else 0 := by
      funext n
      cases n with
      | zero => simp
      | succ n => simp [pow_succ, mul_assoc, h]
    rw [hf]
    exact hasSum_ite_eq 0 P
  exact hs.unique h1

end Exponential

section Flow

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- O fluxo da seletora, com parametro em 𝕜: truthFlow H u = exp(−u H). -/
noncomputable def truthFlow (H : E →L[𝕜] E) (u : 𝕜) : E →L[𝕜] E := NormedSpace.exp ((-u) • H)

/-- O semigrupo real: T_s = exp(−s H), s ∈ ℝ lido em 𝕜. -/
noncomputable def T (H : E →L[𝕜] E) (s : ℝ) : E →L[𝕜] E := truthFlow H (s : 𝕜)

variable (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]

/-- A leitura: I(x) = P x. -/
noncomputable abbrev reading : E →L[𝕜] E := H.ker.starProjection

include hH in
theorem proj_mul_flow (u : 𝕜) : reading H * truthFlow H u = reading H := by
  refine mul_exp_eq_of_mul_eq_zero 𝕜 _ _ ?_
  rw [mul_smul_comm, proj_mul_H H hH, smul_zero]

theorem flow_mul_proj (u : 𝕜) : truthFlow H u * reading H = reading H := by
  refine exp_mul_eq_of_mul_eq_zero 𝕜 _ _ ?_
  rw [smul_mul_assoc, H_mul_proj H, smul_zero]

include hH in
/-- P T_s = P. -/
theorem proj_mul_T (s : ℝ) : reading H * T H s = reading H := proj_mul_flow H hH _

include hH in
/-- A conservacao da leitura: I(T_s x) = I(x). -/
theorem reading_T (s : ℝ) (x : E) : reading H (T H s x) = reading H x := by
  rw [← ContinuousLinearMap.mul_apply, proj_mul_T H hH]

/-- O setor da familia fica parado: z ∈ F ⟹ T_s z = z. -/
theorem T_fix_of_mem_ker (s : ℝ) {z : E} (hz : z ∈ H.ker) : T H s z = z := by
  have hPz : reading H z = z := Submodule.starProjection_eq_self_iff.2 hz
  have := congrArg (fun A : E →L[𝕜] E => A z) (flow_mul_proj H (s : 𝕜))
  simp only [ContinuousLinearMap.mul_apply, hPz] at this
  exact this

/-- A decomposicao T_s x = P x + T_s (x − P x): a componente da familia permanece. -/
theorem T_decomp (s : ℝ) (x : E) :
    T H s x = reading H x + T H s (x - reading H x) := by
  have hP : T H s (reading H x) = reading H x :=
    T_fix_of_mem_ker H s (H.ker.starProjection_apply_mem x)
  rw [map_sub, hP, add_sub_cancel]

end Flow

/-! ## (4b) O veredito: V_x(T_s x) = 1, e a ponte com `NameInstrument.Verifies` (v336) -/

section Verdict

open Classical in
/-- V_r(y) = 1 se I(y) = I(r), 0 caso contrario (o criterio da secao 1 do texto). -/
noncomputable def verdict {X Y : Type*} (I : X → Y) (r y : X) : ℤ := if I y = I r then 1 else 0

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- V_x(T_s x) = 1: a transformacao efetiva e verificada pela leitura da familia. -/
theorem verdict_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]
    (s : ℝ) (x : E) : verdict (fun y => reading H y) x (T H s x) = 1 := by
  simp [verdict, reading_T H hH s x]

/-- O veredito binario e o bit da verdade: verdict ∈ {0,1} e vale 1 sse as leituras coincidem. -/
theorem verdict_eq_one_iff {X Y : Type*} (I : X → Y) (r y : X) :
    verdict I r y = 1 ↔ I y = I r := by
  unfold verdict; split_ifs with h <;> simp [h]

end Verdict

section NameBridge

variable {𝕜 : Type*} {E : Type} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- Ponte com a folha v336 da arvore (`TGLExt.NameInstrument.Verifies`, read (f x) = read x):
    a leitura P e um Nome que VERIFICA cada T_s, e (pela folha) toda iterada de T_s. -/
theorem name_verifies_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]
    (s : ℝ) :
    (⟨fun x => reading H x⟩ : TGLExt.NameInstrument E E).Verifies (fun x => T H s x) :=
  fun x => reading_T H hH s x

theorem name_verifies_T_iterate (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection] (s : ℝ) (n : ℕ) :
    (⟨fun x => reading H x⟩ : TGLExt.NameInstrument E E).Verifies ((fun x => T H s x)^[n]) :=
  TGLExt.name_verifies_iterate _ (name_verifies_T H hH s) n

end NameBridge

/-! ## (5) Memoria estavel: Im P = Fix P, P^n = P, Px = Py ↔ x − y ∈ ker P -/

section Idempotent

variable {R M : Type*} [Semiring R] [AddCommGroup M] [Module R M]

theorem mem_range_iff_fixed (P : M →ₗ[R] M) (hP : IsIdempotentElem P) (z : M) :
    z ∈ LinearMap.range P ↔ P z = z := by
  constructor
  · rintro ⟨x, rfl⟩
    rw [← Module.End.mul_apply, hP.eq]
  · intro h
    exact ⟨z, h⟩

theorem pow_eq_self (P : M →ₗ[R] M) (hP : IsIdempotentElem P) {n : ℕ} (hn : n ≠ 0) :
    P ^ n = P := hP.pow_eq hn

theorem apply_eq_apply_iff (P : M →ₗ[R] M) (x y : M) :
    P x = P y ↔ x - y ∈ LinearMap.ker P := by
  rw [LinearMap.mem_ker, map_sub, sub_eq_zero]

/-- Instanciado na leitura: Im P = Fix P para a projecao ortogonal. -/
theorem starProjection_range_iff_fixed {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
    [InnerProductSpace 𝕜 E] (K : Submodule 𝕜 E) [K.HasOrthogonalProjection] (z : E) :
    z ∈ LinearMap.range (K.starProjection : E →ₗ[𝕜] E) ↔ K.starProjection z = z :=
  by
  have hid : IsIdempotentElem (K.starProjection : E →ₗ[𝕜] E) := by
    show (K.starProjection : E →ₗ[𝕜] E) * (K.starProjection : E →ₗ[𝕜] E) = K.starProjection
    ext x
    exact congrArg (fun A : E →L[𝕜] E => A x) K.isIdempotentElem_starProjection
  exact mem_range_iff_fixed _ hid z

end Idempotent

/-! ## (6) A reciproca: leitura continua conservada ⟺ l = l ∘ P (com o limite NOMEADO) -/

section Converse

/-- Hipotese NOMEADA: o semigrupo converge (ponto a ponto) para a projecao da familia. -/
def FlowTendsToFamily {X : Type*} [TopologicalSpace X] (Tf : ℝ → X → X) (P : X → X) : Prop :=
  ∀ x, Tendsto (fun s => Tf s x) atTop (𝓝 (P x))

/-- Abstrata: com P ∘ T_s = P (s ≥ 0) e o limite nomeado, uma leitura continua e conservada
    ao longo do semigrupo sse fatora pela familia: l = l ∘ P. -/
theorem conserved_iff_factors {X Y : Type*} [TopologicalSpace X] [TopologicalSpace Y]
    [T2Space Y] (Tf : ℝ → X → X) (P : X → X) (hPT : ∀ s, 0 ≤ s → ∀ x, P (Tf s x) = P x)
    (hlim : FlowTendsToFamily Tf P) (l : X → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (Tf s x) = l x) ↔ ∀ x, l x = l (P x) := by
  constructor
  · intro hc x
    have h1 : Tendsto (fun s => l (Tf s x)) atTop (𝓝 (l (P x))) :=
      (hl.tendsto _).comp (hlim x)
    have h2 : Tendsto (fun s => l (Tf s x)) atTop (𝓝 (l x)) := by
      refine tendsto_const_nhds.congr' ?_
      filter_upwards [eventually_ge_atTop (0 : ℝ)] with s hs
      exact (hc s hs x).symm
    exact tendsto_nhds_unique h2 h1
  · intro hf s hs x
    rw [hf (Tf s x), hPT s hs x, ← hf x]

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]

/-- Instanciada no semigrupo da seletora. -/
theorem conserved_iff_factors_T (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    [H.ker.HasOrthogonalProjection]
    (hlim : FlowTendsToFamily (fun s x => T H s x) (fun x => reading H x))
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (T H s x) = l x) ↔ ∀ x, l x = l (reading H x) :=
  conserved_iff_factors (fun s x => T H s x) (fun x => reading H x)
    (fun s _ x => reading_T H hH s x) hlim l hl

end Converse

/-! ## (7) A derivada da leitura se anula; a da dinamica, nao necessariamente -/

section Derivative

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [CompleteSpace E]
variable (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) [H.ker.HasOrthogonalProjection]

include hH in
/-- d/du P(truthFlow u x) = 0 (parametro em 𝕜; para 𝕜 = ℝ e literalmente d/ds). -/
theorem hasDerivAt_reading_flow (x : E) (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => reading H (truthFlow H v x)) 0 u := by
  have : (fun v : 𝕜 => reading H (truthFlow H v x)) = fun _ => reading H x := by
    funext v
    rw [← ContinuousLinearMap.mul_apply, proj_mul_flow H hH]
  rw [this]
  exact hasDerivAt_const _ _

include hH in
/-- A forma literal em s ∈ ℝ: d/ds P(T_s x) = 0 (qualquer estrutura real em E serve: a funcao
    e constante por `reading_T`). -/
theorem hasDerivAt_reading_T [NormedSpace ℝ E] (x : E) (s : ℝ) :
    HasDerivAt (fun r : ℝ => reading H (T H r x)) 0 s := by
  have : (fun r : ℝ => reading H (T H r x)) = fun _ => reading H x :=
    funext fun r => reading_T H hH r x
  rw [this]
  exact hasDerivAt_const _ _

/-- A dinamica inteira: d/du truthFlow u = (−H) · truthFlow u. -/
theorem hasDerivAt_flow (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => truthFlow H v) ((-H) * truthFlow H u) u := by
  have h := hasDerivAt_exp_smul_const' (𝕂 := 𝕜) (-H) u
  have e : ∀ v : 𝕜, (-v) • H = v • (-H) := fun v => by rw [neg_smul, smul_neg]
  simp only [truthFlow, e]
  exact h

/-- Aplicada a x: d/du truthFlow u x = −H (truthFlow u x). -/
theorem hasDerivAt_flow_apply (x : E) (u : 𝕜) :
    HasDerivAt (fun v : 𝕜 => truthFlow H v x) (-(H (truthFlow H u x))) u := by
  have h := (hasDerivAt_flow H u).clm_apply (hasDerivAt_const u x)
  simpa using h

/-- Dinamica nao nula: fora da familia, a derivada em u = 0 e −H x ≠ 0,
    enquanto a derivada da leitura e 0. -/
theorem flow_derivative_ne_zero_at_zero (x : E) (hx : x ∉ H.ker) :
    HasDerivAt (fun v : 𝕜 => truthFlow H v x) (-(H x)) 0 ∧ -(H x) ≠ 0 := by
  refine ⟨?_, ?_⟩
  · have h := hasDerivAt_flow_apply H x 0
    simpa [truthFlow, NormedSpace.exp_zero] using h
  · intro h0
    exact hx (LinearMap.mem_ker.2 (neg_eq_zero.1 h0))

end Derivative

/-! ## (8) O limite espectral em dimensao finita: exp(−sH) x → P x (s → ∞)
  Descarrega a hipotese nomeada `FlowTendsToFamily` quando E e de dimensao finita e H ≥ 0. -/

section Limit

/- `[CompleteSpace E]` e redundante sob `[FiniteDimensional 𝕜 E]` (`FiniteDimensional.complete`);
   fica explicito so para as instancias. -/
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [FiniteDimensional 𝕜 E] [CompleteSpace E]

/-- exp age num autovetor como a exponencial escalar do autovalor. -/
theorem exp_apply_of_eigen (A : E →L[𝕜] E) (μ : 𝕜) (v : E) (hv : A v = μ • v) :
    NormedSpace.exp A v = NormedSpace.exp μ • v := by
  have hpow : ∀ n : ℕ, (A ^ n) v = μ ^ n • v := by
    intro n
    induction n with
    | zero => simp
    | succ n ih =>
      rw [pow_succ', ContinuousLinearMap.mul_apply, ih, map_smul, hv, smul_smul, ← pow_succ]
  have h1 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕜) A).mapL
    (ContinuousLinearMap.apply 𝕜 E v)
  have h2 := (NormedSpace.exp_series_hasSum_exp' (𝕂 := 𝕜) μ).smul_const v
  refine h1.unique ?_
  convert h2 using 1
  funext n
  simp [hpow, smul_smul]

/-- No autovetor de autovalor real ev: T_s v = e^{−s·ev} v. -/
theorem T_apply_eigen (H : E →L[𝕜] E) (ev : ℝ) (v : E) (hv : H v = (ev : 𝕜) • v) (s : ℝ) :
    T H s v = ((Real.exp (-(s * ev)) : ℝ) : 𝕜) • v := by
  have hA : ((-(s : 𝕜)) • H) v = ((-(s : 𝕜)) * (ev : 𝕜)) • v := by
    rw [ContinuousLinearMap.smul_apply, hv, smul_smul]
  rw [T, truthFlow, exp_apply_of_eigen _ _ _ hA]
  congr 1
  have e1 : (-(s : 𝕜)) * (ev : 𝕜) = algebraMap ℝ 𝕜 (-(s * ev)) := by
    rw [RCLike.algebraMap_eq_ofReal]; push_cast; ring
  rw [e1, ← NormedSpace.algebraMap_exp_comm, RCLike.algebraMap_eq_ofReal, Real.exp_eq_exp_ℝ]

/-- ★ O limite espectral: para H auto-adjunto com forma nao-negativa, em dimensao finita,
    T_s x → P x quando s → ∞ (os modos zero ficam; os demais decaem como e^{−s·ev}). -/
theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x, H x⟫_𝕜) :
    FlowTendsToFamily (fun s x => T H s x) (fun x => reading H x) := by
  intro x
  have hsym : (H : E →ₗ[𝕜] E).IsSymmetric := hH.isSymmetric
  have hn : Module.finrank 𝕜 E = Module.finrank 𝕜 E := rfl
  set b := hsym.eigenvectorBasis hn with hb
  have hi : ∀ i, Tendsto (fun s => T H s (b i)) atTop (𝓝 (reading H (b i))) := by
    intro i
    set ev := hsym.eigenvalues hn i with hev
    have hv : H (b i) = (ev : 𝕜) • b i := hsym.apply_eigenvectorBasis hn i
    by_cases h0 : ev = 0
    · have hk : b i ∈ H.ker := by
        rw [LinearMap.mem_ker]
        have : H (b i) = 0 := by rw [hv, h0]; simp
        exact this
      have hP : reading H (b i) = b i := Submodule.starProjection_eq_self_iff.2 hk
      rw [hP]
      have hc : (fun s => T H s (b i)) = fun _ => b i := funext fun s => T_fix_of_mem_ker H s hk
      rw [hc]
      exact tendsto_const_nhds
    · have hpos_i : 0 < ev := by
        have h1 := hpos (b i)
        rw [hv, inner_smul_right, RCLike.re_ofReal_mul, inner_self_eq_norm_sq,
          b.orthonormal.1 i] at h1
        norm_num at h1
        exact lt_of_le_of_ne h1 (Ne.symm h0)
      have hP : reading H (b i) = 0 := by
        have h2 : reading H (H (b i)) = 0 := by
          have := congrArg (fun A : E →L[𝕜] E => A (b i)) (proj_mul_H H hH)
          simpa using this
        rw [hv, map_smul] at h2
        exact (smul_eq_zero.1 h2).resolve_left (by exact_mod_cast h0)
      rw [hP]
      have hc : (fun s => T H s (b i)) = fun s => ((Real.exp (-(s * ev)) : ℝ) : 𝕜) • b i :=
        funext fun s => T_apply_eigen H ev (b i) hv s
      rw [hc]
      have hexp : Tendsto (fun s : ℝ => Real.exp (-(s * ev))) atTop (𝓝 0) :=
        Real.tendsto_exp_neg_atTop_nhds_zero.comp (tendsto_id.atTop_mul_const hpos_i)
      have h3 := (((RCLike.continuous_ofReal (K := 𝕜)).tendsto 0).comp hexp).smul_const (b i)
      simpa using h3
  have hT : ∀ s, T H s x = ∑ i, b.repr x i • T H s (b i) := by
    intro s
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul]
  have hPx : reading H x = ∑ i, b.repr x i • reading H (b i) := by
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul]
  have hfun : (fun s => T H s x) = fun s => ∑ i, b.repr x i • T H s (b i) := funext hT
  show Tendsto (fun s => T H s x) atTop (𝓝 (reading H x))
  rw [hfun, hPx]
  exact tendsto_finsetSum _ fun i _ => (hi i).const_smul _

/-- ★ A reciproca INCONDICIONAL em dimensao finita, para a penalidade dos vinculos:
    uma leitura continua e conservada ao longo de T_s = exp(−s H_3L) sse l = l ∘ P. -/
theorem conserved_iff_factors_penalty {ι : Type*} [Fintype ι] (D : ι → E →L[𝕜] E)
    {Y : Type*} [TopologicalSpace Y] [T2Space Y] (l : E → Y) (hl : Continuous l) :
    (∀ s, 0 ≤ s → ∀ x, l (T (penalty D) s x) = l x) ↔
      ∀ x, l x = l (reading (penalty D) x) := by
  refine conserved_iff_factors_T (penalty D) (isSelfAdjoint_penalty D)
    (flowTendsToFamily_of_finiteDimensional (penalty D) (isSelfAdjoint_penalty D) ?_) l hl
  intro x
  rw [re_inner_penalty]
  exact Finset.sum_nonneg fun j _ => sq_nonneg _

end Limit

/-! ## (9) O perfil hiperbolico a = sech(χ/2), q = tanh(χ/2)
  HOMONIMO: esta anulacao a'(0) = 0 e do perfil em χ; NAO e o zero modular K Ω = 0,
  nem a anulacao da leitura em (7). Nenhum lema aqui os liga. -/

section Profile

open Real

noncomputable def profA (χ : ℝ) : ℝ := (cosh (χ / 2))⁻¹
noncomputable def profQ (χ : ℝ) : ℝ := tanh (χ / 2)

theorem hasDerivAt_profA (χ : ℝ) :
    HasDerivAt profA (-(1 / 2) * profA χ * profQ χ) χ := by
  have hc : HasDerivAt (fun y => cosh (y / 2)) (sinh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).cosh
  have hne : cosh (χ / 2) ≠ 0 := (cosh_pos _).ne'
  have h : HasDerivAt (fun y => (cosh (y / 2))⁻¹) (-(sinh (χ / 2) * (1 / 2)) / cosh (χ / 2) ^ 2) χ :=
    hc.inv hne
  have e : -(1 / 2) * profA χ * profQ χ = -(sinh (χ / 2) * (1 / 2)) / cosh (χ / 2) ^ 2 := by
    simp only [profA, profQ, tanh_eq_sinh_div_cosh]
    field_simp
  rw [e]
  exact h

theorem hasDerivAt_profQ (χ : ℝ) :
    HasDerivAt profQ ((1 / 2) * profA χ ^ 2) χ := by
  have hc : HasDerivAt (fun y => cosh (y / 2)) (sinh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).cosh
  have hs : HasDerivAt (fun y => sinh (y / 2)) (cosh (χ / 2) * (1 / 2)) χ :=
    ((hasDerivAt_id' χ).div_const 2).sinh
  have hne : cosh (χ / 2) ≠ 0 := (cosh_pos _).ne'
  have h := hs.div hc hne
  have hfun : profQ = fun y => sinh (y / 2) / cosh (y / 2) := by
    funext y
    simp only [profQ, tanh_eq_sinh_div_cosh]
  have key : cosh (χ / 2) * (1 / 2) * cosh (χ / 2) - sinh (χ / 2) * (sinh (χ / 2) * (1 / 2))
      = 1 / 2 := by
    linear_combination (1 / 2 : ℝ) * cosh_sq_sub_sinh_sq (χ / 2)
  have e : (1 / 2) * profA χ ^ 2 = (cosh (χ / 2) * (1 / 2) * cosh (χ / 2)
      - sinh (χ / 2) * (sinh (χ / 2) * (1 / 2))) / cosh (χ / 2) ^ 2 := by
    rw [key]
    simp only [profA]
    field_simp
  rw [hfun, e]
  exact h

theorem profA_zero : profA 0 = 1 := by simp [profA]
theorem profQ_zero : profQ 0 = 0 := by simp [profQ]

/-- a'(0) = 0. -/
theorem profA_deriv_zero : deriv profA 0 = 0 := by
  rw [(hasDerivAt_profA 0).deriv, profQ_zero, mul_zero]

/-- q'(0) = 1/2. -/
theorem profQ_deriv_zero : deriv profQ 0 = 1 / 2 := by
  rw [(hasDerivAt_profQ 0).deriv, profA_zero]; norm_num

/-- a''(0) = −1/4. -/
theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 4) := by
  have hd : deriv profA = fun χ => -(1 / 2) * profA χ * profQ χ := by
    funext χ; exact (hasDerivAt_profA χ).deriv
  rw [hd]
  have h := (((hasDerivAt_profA 0).const_mul (-(1 / 2) : ℝ)).mul (hasDerivAt_profQ 0))
  have h' : HasDerivAt (fun χ => -(1 / 2) * profA χ * profQ χ)
      (-(1 / 2) * (-(1 / 2) * profA 0 * profQ 0) * profQ 0
        + -(1 / 2) * profA 0 * (1 / 2 * profA 0 ^ 2)) 0 := h
  rw [h'.deriv, profA_zero, profQ_zero]
  norm_num

end Profile

end TGLExt.EquationOfTruth

-- Auditoria de axiomas
#print axioms TGLExt.EquationOfTruth.truthValue_table
#print axioms TGLExt.EquationOfTruth.truthBit_eq_one_iff
#print axioms TGLExt.EquationOfTruth.truthBit_eq_zero_iff
#print axioms TGLExt.EquationOfTruth.truthBit_bivalent
#print axioms TGLExt.EquationOfTruth.re_inner_penalty
#print axioms TGLExt.EquationOfTruth.ker_penalty
#print axioms TGLExt.EquationOfTruth.ker_threeLocks
#print axioms TGLExt.EquationOfTruth.isSelfAdjoint_penalty
#print axioms TGLExt.EquationOfTruth.selector_nonpos
#print axioms TGLExt.EquationOfTruth.H_mul_proj
#print axioms TGLExt.EquationOfTruth.proj_mul_H
#print axioms TGLExt.EquationOfTruth.mul_exp_eq_of_mul_eq_zero
#print axioms TGLExt.EquationOfTruth.exp_mul_eq_of_mul_eq_zero
#print axioms TGLExt.EquationOfTruth.proj_mul_flow
#print axioms TGLExt.EquationOfTruth.proj_mul_T
#print axioms TGLExt.EquationOfTruth.reading_T
#print axioms TGLExt.EquationOfTruth.T_fix_of_mem_ker
#print axioms TGLExt.EquationOfTruth.T_decomp
#print axioms TGLExt.EquationOfTruth.verdict_T
#print axioms TGLExt.EquationOfTruth.verdict_eq_one_iff
#print axioms TGLExt.EquationOfTruth.name_verifies_T
#print axioms TGLExt.EquationOfTruth.name_verifies_T_iterate
#print axioms TGLExt.EquationOfTruth.mem_range_iff_fixed
#print axioms TGLExt.EquationOfTruth.pow_eq_self
#print axioms TGLExt.EquationOfTruth.apply_eq_apply_iff
#print axioms TGLExt.EquationOfTruth.starProjection_range_iff_fixed
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors_T
#print axioms TGLExt.EquationOfTruth.hasDerivAt_reading_flow
#print axioms TGLExt.EquationOfTruth.hasDerivAt_reading_T
#print axioms TGLExt.EquationOfTruth.hasDerivAt_flow
#print axioms TGLExt.EquationOfTruth.hasDerivAt_flow_apply
#print axioms TGLExt.EquationOfTruth.flow_derivative_ne_zero_at_zero
#print axioms TGLExt.EquationOfTruth.exp_apply_of_eigen
#print axioms TGLExt.EquationOfTruth.T_apply_eigen
#print axioms TGLExt.EquationOfTruth.flowTendsToFamily_of_finiteDimensional
#print axioms TGLExt.EquationOfTruth.conserved_iff_factors_penalty
#print axioms TGLExt.EquationOfTruth.hasDerivAt_profA
#print axioms TGLExt.EquationOfTruth.hasDerivAt_profQ
#print axioms TGLExt.EquationOfTruth.profA_deriv_zero
#print axioms TGLExt.EquationOfTruth.profQ_deriv_zero
#print axioms TGLExt.EquationOfTruth.profA_second_deriv_zero
#print axioms TGLExt.EquationOfTruth.re_inner_adjoint_mul_self
#print axioms TGLExt.EquationOfTruth.flow_mul_proj
#print axioms TGLExt.EquationOfTruth.profA_zero
#print axioms TGLExt.EquationOfTruth.profQ_zero
