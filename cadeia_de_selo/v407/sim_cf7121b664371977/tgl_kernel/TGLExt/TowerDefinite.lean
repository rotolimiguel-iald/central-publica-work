import TGLExt.TowerModular
import TGLExt.ScaleCurrent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 83 — TowerDefinite: o colimite da torre é pré-Hilbert DEFINIDO
  [TGLExt — v131, Bloco A do PLANO_ULTIMA_FLAG, pedra 1 de 5]

O plano registrado (PLANO_ULTIMA_FLAG_O_FATOR_COMO_OBJETO.md) pede: o produto
interno DEFINIDO no colimite da torre. Esta pedra o entrega, com um refinamento
que o barateia por teorema: os pesos da torre são ESTRITAMENTE positivos
(`towerW_pos`), logo a densidade é definida-positiva e o radical GNS é ZERO —
o quociente da pedra 78 é trivial AQUI, e o colimite JÁ é o pré-Hilbert:

* `SiteProfile` — o perfil de sítios (peso μ_n ∈ (0,1) em cada sítio): a
  GENERALIZAÇÃO que dá o mesmo objeto para o perfil constante (III_λ) e o
  alternado (III₁, a marca log-densa da pedra 72);
* `towerW`/`tState`/`tInner` — pesos, estado e produto GNS por andar, em
  FORMA DE SOMA explícita (sem traço-matriz: a positividade fica elementar);
* ★★ `tState_towerStep` — a coerência de Araki–Woods no perfil geral;
* ★★ `tPush` — o empurrão N ≤ M via `Nat.leRecOn`: aditivo, multiplicativo,
  estrelado, INJETIVO, isométrico para o estado e o produto;
* ★★★ `TowerPre P` — O COLIMITE como quociente do Σ-tipo pela relação de
  empurrão comum; `tof`, `tof_towerStep`, `exists_tof`; instâncias
  `AddCommGroup` + `Module ℂ` construídas à mão (andar comum);
* ★★★ `towerPreCore : PreInnerProductSpace.Core ℂ (TowerPre P)` — o produto
  interno DESCE ao colimite (hermitiano, positivo, sesquilinear) ⟹
  instâncias `SeminormedAddCommGroup` + `InnerProductSpace ℂ` (o molde GNS
  da mathlib, `InnerProductSpace.ofCore`);
* ★★★ `towerPre_definite` — A FORMA É DEFINIDA: ⟪x,x⟫ = 0 ⟹ x = 0 — o
  radical é zero no colimite INTEIRO (pesos positivos); a pedra 83 do plano;
* `towerOmega` — Ω = [1] com ⟪Ω,Ω⟫ = 1.

O QUE RESTA (as pedras 84–87): o completamento H_φ, a ação π estendida, o
objeto M_TGL = (π(torre))'' e a assinatura no limite. β jamais literal.
Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix
open scoped ComplexConjugate

noncomputable section

/-! ## A — o perfil de sítios e os pesos da torre -/

/-- o perfil de sítios: o peso do estado base em cada sítio, em (0,1). -/
structure SiteProfile where
  w : ℕ → ℝ
  pos : ∀ n, 0 < w n
  lt_one : ∀ n, w n < 1

/-- os dois pesos de um sítio: (t, 1−t). -/
def siteW (t : ℝ) : Fin 2 → ℝ := fun i => if i = 0 then t else 1 - t

theorem siteW_pos {t : ℝ} (h0 : 0 < t) (h1 : t < 1) (i : Fin 2) :
    0 < siteW t i := by
  unfold siteW
  by_cases hi : i = 0
  · rw [if_pos hi]; exact h0
  · rw [if_neg hi]; linarith

theorem siteW_sum (t : ℝ) : ∑ i, siteW t i = 1 := by
  rw [Fin.sum_univ_two]
  unfold siteW
  rw [if_pos rfl, if_neg (show ¬(1 : Fin 2) = 0 by decide)]
  ring

/-- os pesos da torre no perfil P (produto dos pesos de sítio). -/
def towerW (P : SiteProfile) : (N : ℕ) → chainIdx N → ℝ
  | 0 => fun i => siteW (P.w 0) i
  | N + 1 => fun p => towerW P N p.1 * siteW (P.w (N + 1)) p.2

theorem towerW_pos (P : SiteProfile) : ∀ (N : ℕ) (i : chainIdx N), 0 < towerW P N i
  | 0, i => siteW_pos (P.pos 0) (P.lt_one 0) i
  | N + 1, p =>
      mul_pos (towerW_pos P N p.1) (siteW_pos (P.pos (N + 1)) (P.lt_one (N + 1)) p.2)

theorem towerW_sum (P : SiteProfile) : ∀ N : ℕ, ∑ i, towerW P N i = 1
  | 0 => siteW_sum (P.w 0)
  | N + 1 => by
      have key : (∑ p : chainIdx N × Fin 2,
          towerW P N p.1 * siteW (P.w (N + 1)) p.2) = 1 := by
        rw [Fintype.sum_prod_type]
        have h : ∀ k : chainIdx N,
            ∑ s : Fin 2, towerW P N k * siteW (P.w (N + 1)) s
              = towerW P N k := by
          intro k
          rw [← Finset.mul_sum, siteW_sum, mul_one]
        rw [Finset.sum_congr rfl (fun k _ => h k)]
        exact towerW_sum P N
      exact key

/-! ## B — o estado e o produto GNS por andar (forma de soma) -/

/-- o estado da torre no andar N (forma de soma explícita). -/
def tState (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : ℂ :=
  ∑ k, ((towerW P N k : ℝ) : ℂ) * a k k

/-- o produto GNS do andar: ⟨a,b⟩ = φ(a†b). -/
def tInner (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) : ℂ :=
  tState P N (aᴴ * b)

theorem tState_add (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P N (a + b) = tState P N a + tState P N b := by
  unfold tState
  rw [← Finset.sum_add_distrib]
  congr 1
  funext k
  rw [Matrix.add_apply, mul_add]

theorem tState_smul (P : SiteProfile) (N : ℕ) (c : ℂ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P N (c • a) = c * tState P N a := by
  unfold tState
  rw [Finset.mul_sum]
  congr 1
  funext k
  rw [Matrix.smul_apply, smul_eq_mul]
  ring

theorem tState_one (P : SiteProfile) (N : ℕ) :
    tState P N (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1 := by
  unfold tState
  have h : ∀ k : chainIdx N,
      ((towerW P N k : ℝ) : ℂ) * (1 : Matrix (chainIdx N) (chainIdx N) ℂ) k k
        = ((towerW P N k : ℝ) : ℂ) := by
    intro k
    rw [one_apply_eq, mul_one]
  rw [Finset.sum_congr rfl (fun k _ => h k)]
  exact_mod_cast congrArg (fun t : ℝ => (t : ℂ)) (towerW_sum P N)

/-- a fórmula de coordenadas do produto GNS. -/
theorem tInner_apply (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a b
      = ∑ k, ((towerW P N k : ℝ) : ℂ) * ∑ j, conj (a j k) * b j k := by
  unfold tInner tState
  refine Finset.sum_congr rfl fun k _ => ?_
  congr 1

theorem tInner_conj_symm (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    conj (tInner P N b a) = tInner P N a b := by
  rw [tInner_apply, tInner_apply, map_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [map_mul, Complex.conj_ofReal, map_sum]
  congr 1
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [map_mul, Complex.conj_conj]
  ring

theorem tInner_add_left (P : SiteProfile) (N : ℕ)
    (a b c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (a + b) c = tInner P N a c + tInner P N b c := by
  unfold tInner
  rw [conjTranspose_add, add_mul, tState_add]

theorem tInner_add_right (P : SiteProfile) (N : ℕ)
    (a b c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a (b + c) = tInner P N a b + tInner P N a c := by
  unfold tInner
  rw [mul_add, tState_add]

theorem tInner_smul_left (P : SiteProfile) (N : ℕ) (c : ℂ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (c • a) b = conj c * tInner P N a b := by
  unfold tInner
  rw [conjTranspose_smul, smul_mul_assoc, tState_smul]
  rfl

theorem tInner_smul_right (P : SiteProfile) (N : ℕ) (c : ℂ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a (c • b) = c * tInner P N a b := by
  unfold tInner
  rw [mul_smul_comm, tState_smul]

/-- a norma GNS ao quadrado, em coordenadas: soma pesada de |·|². -/
theorem tInner_self_eq (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a a
      = ((∑ k, towerW P N k * ∑ j, Complex.normSq (a j k) : ℝ) : ℂ) := by
  rw [tInner_apply]
  push_cast
  refine Finset.sum_congr rfl fun k _ => ?_
  congr 1
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [← Complex.normSq_eq_conj_mul_self]

theorem tInner_self_nonneg (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ (tInner P N a a).re := by
  rw [tInner_self_eq, Complex.ofReal_re]
  apply Finset.sum_nonneg
  intro k _
  apply mul_nonneg (le_of_lt (towerW_pos P N k))
  apply Finset.sum_nonneg
  intro j _
  exact Complex.normSq_nonneg _

/-- ★ A DEFINITUDE POR ANDAR: pesos positivos ⟹ radical zero. -/
theorem tInner_self_definite (P : SiteProfile) (N : ℕ)
    {a : Matrix (chainIdx N) (chainIdx N) ℂ}
    (h : tInner P N a a = 0) : a = 0 := by
  rw [tInner_self_eq] at h
  have hre : (∑ k, towerW P N k * ∑ j, Complex.normSq (a j k)) = 0 := by
    exact_mod_cast h
  have hterm : ∀ k ∈ Finset.univ,
      (0 : ℝ) ≤ towerW P N k * ∑ j, Complex.normSq (a j k) := by
    intro k _
    apply mul_nonneg (le_of_lt (towerW_pos P N k))
    apply Finset.sum_nonneg
    intro j _
    exact Complex.normSq_nonneg _
  have hz := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp hre
  ext j k
  have hk := hz k (Finset.mem_univ k)
  have hwne : towerW P N k ≠ 0 := ne_of_gt (towerW_pos P N k)
  have hsum : (∑ j, Complex.normSq (a j k)) = 0 :=
    (mul_eq_zero.mp hk).resolve_left hwne
  have hterm2 : ∀ j ∈ Finset.univ, (0 : ℝ) ≤ Complex.normSq (a j k) :=
    fun j _ => Complex.normSq_nonneg _
  have hj := (Finset.sum_eq_zero_iff_of_nonneg hterm2).mp hsum j (Finset.mem_univ j)
  rw [Matrix.zero_apply]
  exact Complex.normSq_eq_zero.mp hj

/-! ## C — a coerência do estado e o empurrão da torre -/

/-- ★★ A COERÊNCIA DE ARAKI–WOODS no perfil geral: φ_{N+1}(a⊗1) = φ_N(a). -/
theorem tState_towerStep (P : SiteProfile) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P (N + 1) (towerStep a) = tState P N a := by
  unfold tState towerStep
  rw [Fintype.sum_prod_type]
  have h : ∀ (k : chainIdx N) (s : Fin 2),
      ((towerW P (N + 1) (k, s) : ℝ) : ℂ)
          * (a ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)) (k, s) (k, s)
        = ((towerW P N k : ℝ) : ℂ) * a k k
            * ((siteW (P.w (N + 1)) s : ℝ) : ℂ) := by
    intro k s
    rw [kroneckerMap_apply, one_apply_eq, mul_one]
    rw [show towerW P (N + 1) (k, s)
        = towerW P N k * siteW (P.w (N + 1)) s from rfl]
    push_cast
    ring
  rw [Finset.sum_congr rfl (fun k _ => Finset.sum_congr rfl (fun s _ => h k s))]
  have h2 : ∀ k : chainIdx N,
      ∑ s : Fin 2, ((towerW P N k : ℝ) : ℂ) * a k k
          * ((siteW (P.w (N + 1)) s : ℝ) : ℂ)
        = ((towerW P N k : ℝ) : ℂ) * a k k := by
    intro k
    rw [← Finset.mul_sum, ← Complex.ofReal_sum, siteW_sum, Complex.ofReal_one,
      mul_one]
  rw [Finset.sum_congr rfl (fun k _ => h2 k)]

theorem towerStep_add {N : ℕ} (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerStep (a + b) = towerStep a + towerStep b := by
  unfold towerStep
  exact Matrix.add_kronecker a b 1

theorem towerStep_smul {N : ℕ} (c : ℂ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerStep (c • a) = c • towerStep a := by
  unfold towerStep
  exact Matrix.smul_kronecker c a 1

theorem towerStep_zero (N : ℕ) :
    towerStep (0 : Matrix (chainIdx N) (chainIdx N) ℂ) = 0 := by
  unfold towerStep
  exact Matrix.zero_kronecker 1

/-- o degrau nomeado (constante de primeira ordem para a unificação). -/
def tNext {k : ℕ} (x : Matrix (chainIdx k) (chainIdx k) ℂ) :
    Matrix (chainIdx (k + 1)) (chainIdx (k + 1)) ℂ := towerStep x

/-- o empurrão da torre: N ≤ M degraus de towerStep. -/
def tPush {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx M) (chainIdx M) ℂ :=
  Nat.leRecOn (C := fun m => Matrix (chainIdx m) (chainIdx m) ℂ) h
    (fun {k} => tNext (k := k)) a

theorem tPush_self {N : ℕ} (h : N ≤ N) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h a = a := by
  unfold tPush
  exact @Nat.leRecOn_self (fun m => Matrix (chainIdx m) (chainIdx m) ℂ) N
    (fun {k} => tNext (k := k)) a

theorem tPush_succ {N M : ℕ} (h1 : N ≤ M) (h2 : N ≤ M + 1)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h2 a = towerStep (tPush h1 a) := by
  unfold tPush
  exact @Nat.leRecOn_succ (fun m => Matrix (chainIdx m) (chainIdx m) ℂ) N M h1 h2
    (fun {k} => tNext (k := k)) a

theorem tPush_trans {N M K : ℕ} (h1 : N ≤ M) (h2 : M ≤ K)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h2 (tPush h1 a) = tPush (h1.trans h2) a := by
  induction K, h2 using Nat.le_induction with
  | base => rw [tPush_self]
  | succ K hK ih =>
      rw [tPush_succ hK (hK.trans (Nat.le_succ K)),
        tPush_succ (h1.trans hK) (h1.trans (hK.trans (Nat.le_succ K))), ih]

theorem tPush_add {N M : ℕ} (h : N ≤ M)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h (a + b) = tPush h a + tPush h b := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self, tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_add]

theorem tPush_smul {N M : ℕ} (h : N ≤ M) (c : ℂ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h (c • a) = c • tPush h a := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_smul]

theorem tPush_zero {N M : ℕ} (h : N ≤ M) :
    tPush h (0 : Matrix (chainIdx N) (chainIdx N) ℂ) = 0 := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_zero]

theorem tPush_neg {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h (-a) = - tPush h a := by
  have h1 : (-a) = (-1 : ℂ) • a := by rw [neg_one_smul]
  rw [h1, tPush_smul, neg_one_smul]

theorem tPush_mul {N M : ℕ} (h : N ≤ M)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h (a * b) = tPush h a * tPush h b := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self, tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_mul]

theorem tPush_star {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h aᴴ = (tPush h a)ᴴ := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_star]

theorem tPush_one {N M : ℕ} (h : N ≤ M) :
    tPush h (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1 := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)), ih, towerStep_one]

theorem tPush_injective {N M : ℕ} (h : N ≤ M) :
    Function.Injective (tPush (N := N) (M := M) h) := by
  induction M, h using Nat.le_induction with
  | base =>
      intro a b hab
      rw [tPush_self, tPush_self] at hab
      exact hab
  | succ M hM ih =>
      intro a b hab
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M))] at hab
      exact ih (towerStep_injective M hab)

theorem tState_tPush (P : SiteProfile) {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P M (tPush h a) = tState P N a := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)), tState_towerStep, ih]

/-- ★★ A ISOMETRIA DO EMPURRÃO: o produto GNS é invariante ao subir. -/
theorem tInner_tPush (P : SiteProfile) {N M : ℕ} (h : N ≤ M)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P M (tPush h a) (tPush h b) = tInner P N a b := by
  unfold tInner
  rw [← tPush_star, ← tPush_mul]
  exact tState_tPush P h (aᴴ * b)

/-! ## D — o colimite: o quociente pelo empurrão comum -/

/-- um ponto da torre: um andar e uma matriz nele. -/
def TowerPt : Type := Σ N : ℕ, Matrix (chainIdx N) (chainIdx N) ℂ

/-- a relação do colimite: empurrados a um andar comum, coincidem. -/
def towerEqv (x y : TowerPt) : Prop :=
  ∃ (K : ℕ) (hx : x.1 ≤ K) (hy : y.1 ≤ K), tPush hx x.2 = tPush hy y.2

theorem towerEqv_refl (x : TowerPt) : towerEqv x x :=
  ⟨x.1, le_rfl, le_rfl, rfl⟩

theorem towerEqv_symm {x y : TowerPt} (h : towerEqv x y) : towerEqv y x := by
  obtain ⟨K, hx, hy, e⟩ := h
  exact ⟨K, hy, hx, e.symm⟩

/-- a caracterização em QUALQUER andar comum (usa a injetividade). -/
theorem towerEqv_iff {x y : TowerPt} {K : ℕ} (hx : x.1 ≤ K) (hy : y.1 ≤ K) :
    towerEqv x y ↔ tPush hx x.2 = tPush hy y.2 := by
  constructor
  · rintro ⟨K0, h1, h2, e⟩
    have hK : K ≤ K ⊔ K0 := le_sup_left
    have hK0 : K0 ≤ K ⊔ K0 := le_sup_right
    apply tPush_injective hK
    rw [tPush_trans hx hK, tPush_trans hy hK]
    rw [show hx.trans hK = h1.trans hK0 from rfl,
      show hy.trans hK = h2.trans hK0 from rfl]
    rw [← tPush_trans h1 hK0, ← tPush_trans h2 hK0, e]
  · intro e
    exact ⟨K, hx, hy, e⟩

theorem towerEqv_trans {x y z : TowerPt} (h1 : towerEqv x y)
    (h2 : towerEqv y z) : towerEqv x z := by
  obtain ⟨K1, hx1, hy1, e1⟩ := h1
  obtain ⟨K2, hy2, hz2, e2⟩ := h2
  have hK1 : K1 ≤ K1 ⊔ K2 := le_sup_left
  have hK2 : K2 ≤ K1 ⊔ K2 := le_sup_right
  refine ⟨K1 ⊔ K2, hx1.trans hK1, hz2.trans hK2, ?_⟩
  rw [← tPush_trans hx1 hK1, ← tPush_trans hz2 hK2, e1, ← e2]
  rw [tPush_trans hy1 hK1, tPush_trans hy2 hK2]

instance towerSetoid : Setoid TowerPt :=
  ⟨towerEqv, towerEqv_refl, towerEqv_symm, towerEqv_trans⟩

set_option linter.unusedVariables false in
/-- ★★★ O COLIMITE DA TORRE (fantasma no perfil: o produto interno depende
    de P; o espaço subjacente é o mesmo). -/
@[nolint unusedArguments]
def TowerPre (P : SiteProfile) : Type := Quotient towerSetoid

variable {P : SiteProfile}

/-- a inclusão do andar N no colimite. -/
def tof (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : TowerPre P :=
  Quotient.mk towerSetoid ⟨N, a⟩

theorem tof_towerStep (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tof P (N + 1) (towerStep a) = tof P N a := by
  apply Quotient.sound
  refine ⟨N + 1, le_rfl, Nat.le_succ N, ?_⟩
  rw [tPush_self, tPush_succ le_rfl (Nat.le_succ N), tPush_self]

theorem tof_tPush {N M : ℕ} (h : N ≤ M)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tof P M (tPush h a) = tof P N a := by
  apply Quotient.sound
  exact ⟨M, le_rfl, h, by rw [tPush_self]⟩

theorem exists_tof (x : TowerPre P) :
    ∃ (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ), tof P N a = x := by
  obtain ⟨⟨N, a⟩, rfl⟩ := Quotient.exists_rep x
  exact ⟨N, a, rfl⟩

theorem tof_eq_iff {N M : ℕ} {K : ℕ} (hN : N ≤ K) (hM : M ≤ K)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    tof P N a = tof P M b ↔ tPush hN a = tPush hM b := by
  constructor
  · intro h
    exact (towerEqv_iff hN hM).mp (Quotient.exact h)
  · intro h
    exact Quotient.sound ((towerEqv_iff hN hM).mpr h)

/-! ## E — as operações do colimite -/

instance : Add (TowerPre P) :=
  ⟨Quotient.map₂
    (fun x y => ⟨x.1 ⊔ y.1, tPush le_sup_left x.2 + tPush le_sup_right y.2⟩)
    (by
      rintro x x' hx y y' hy
      have hK : (x.1 ⊔ y.1) ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_left
      have hK' : (x'.1 ⊔ y'.1) ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_right
      have ex := (towerEqv_iff (x := x) (y := x')
        (K := (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1))
        (le_sup_left.trans hK) (le_sup_left.trans hK')).mp hx
      have ey := (towerEqv_iff (x := y) (y := y')
        (K := (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1))
        (le_sup_right.trans hK) (le_sup_right.trans hK')).mp hy
      refine (towerEqv_iff hK hK').mpr ?_
      show tPush hK (tPush le_sup_left x.2 + tPush le_sup_right y.2)
        = tPush hK' (tPush le_sup_left x'.2 + tPush le_sup_right y'.2)
      rw [tPush_add, tPush_add, tPush_trans, tPush_trans, tPush_trans,
        tPush_trans, ex, ey])⟩

instance : Neg (TowerPre P) :=
  ⟨Quotient.map (fun x => ⟨x.1, -x.2⟩)
    (by
      rintro x x' hx
      obtain ⟨K, h1, h2, e⟩ := hx
      exact ⟨K, h1, h2, by rw [tPush_neg, tPush_neg, e]⟩)⟩

instance : Zero (TowerPre P) := ⟨tof P 0 0⟩

instance : SMul ℂ (TowerPre P) :=
  ⟨fun c => Quotient.map (fun x => ⟨x.1, c • x.2⟩)
    (by
      rintro x x' hx
      obtain ⟨K, h1, h2, e⟩ := hx
      exact ⟨K, h1, h2, by rw [tPush_smul, tPush_smul, e]⟩)⟩

theorem tof_add_hetero (N M : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    tof P N a + tof P M b
      = tof P (N ⊔ M) (tPush le_sup_left a + tPush le_sup_right b) := rfl

theorem tof_neg (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    - tof P N a = tof P N (-a) := rfl

theorem tof_smul (c : ℂ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    c • tof P N a = tof P N (c • a) := rfl

theorem tof_zero (N : ℕ) : tof P N 0 = (0 : TowerPre P) := by
  show tof P N 0 = tof P 0 0
  rw [tof_eq_iff (le_refl N) (Nat.zero_le N)]
  rw [tPush_zero, tPush_zero]

/-- a soma em QUALQUER andar comum. -/
theorem tof_add_at {N M K : ℕ} (hN : N ≤ K) (hM : M ≤ K)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    tof P N a + tof P M b = tof P K (tPush hN a + tPush hM b) := by
  rw [tof_add_hetero]
  have hs : N ⊔ M ≤ (N ⊔ M) ⊔ K := le_sup_left
  have hk : K ≤ (N ⊔ M) ⊔ K := le_sup_right
  rw [tof_eq_iff hs hk]
  rw [tPush_add, tPush_add, tPush_trans, tPush_trans, tPush_trans, tPush_trans]

theorem tof_add_same (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tof P N a + tof P N b = tof P N (a + b) := by
  rw [tof_add_at (le_refl N) (le_refl N), tPush_self, tPush_self]

instance : AddCommGroup (TowerPre P) where
  add := (· + ·)
  add_assoc := by
    intro x y z
    obtain ⟨Nx, a, rfl⟩ := exists_tof x
    obtain ⟨Ny, b, rfl⟩ := exists_tof y
    obtain ⟨Nz, c, rfl⟩ := exists_tof z
    have hx : Nx ≤ Nx ⊔ Ny ⊔ Nz := le_sup_left.trans le_sup_left
    have hy : Ny ≤ Nx ⊔ Ny ⊔ Nz := le_sup_right.trans le_sup_left
    have hz : Nz ≤ Nx ⊔ Ny ⊔ Nz := le_sup_right
    have hK : Nx ⊔ Ny ⊔ Nz ≤ Nx ⊔ Ny ⊔ Nz := le_rfl
    rw [tof_add_at hx hy, tof_add_at hK hz, tof_add_at hy hz,
      tof_add_at hx hK, tPush_self, tPush_self, add_assoc]
  zero := 0
  zero_add := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    show (tof P 0 0) + tof P N a = tof P N a
    rw [tof_add_at (Nat.zero_le N) (le_refl N), tPush_zero, tPush_self,
      zero_add]
  add_zero := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    show tof P N a + (tof P 0 0) = tof P N a
    rw [tof_add_at (le_refl N) (Nat.zero_le N), tPush_zero, tPush_self,
      add_zero]
  nsmul := nsmulRec
  neg := Neg.neg
  zsmul := zsmulRec
  neg_add_cancel := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    rw [tof_neg, tof_add_same, neg_add_cancel, tof_zero]
  add_comm := by
    intro x y
    obtain ⟨Nx, a, rfl⟩ := exists_tof x
    obtain ⟨Ny, b, rfl⟩ := exists_tof y
    have hx : Nx ≤ Nx ⊔ Ny := le_sup_left
    have hy : Ny ≤ Nx ⊔ Ny := le_sup_right
    rw [tof_add_at hx hy, tof_add_at hy hx, add_comm]

instance : Module ℂ (TowerPre P) where
  one_smul := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    rw [tof_smul, one_smul]
  mul_smul := by
    intro c d x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    rw [tof_smul, tof_smul, tof_smul, mul_smul]
  smul_zero := by
    intro c
    show c • (tof P 0 0) = tof P 0 0
    rw [tof_smul, smul_zero]
  smul_add := by
    intro c x y
    obtain ⟨Nx, a, rfl⟩ := exists_tof x
    obtain ⟨Ny, b, rfl⟩ := exists_tof y
    have hx : Nx ≤ Nx ⊔ Ny := le_sup_left
    have hy : Ny ≤ Nx ⊔ Ny := le_sup_right
    rw [tof_add_at hx hy, tof_smul, tof_smul, tof_smul, tof_add_at hx hy,
      tPush_smul, tPush_smul, smul_add]
  add_smul := by
    intro c d x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    rw [tof_smul, tof_smul, tof_smul, tof_add_same, add_smul]
  zero_smul := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    rw [tof_smul, zero_smul, tof_zero]

/-! ## F — o produto interno desce ao colimite -/

/-- o produto interno do colimite (andar comum mínimo). -/
def innerPre (P : SiteProfile) : TowerPre P → TowerPre P → ℂ :=
  Quotient.lift₂
    (fun x y => tInner P (x.1 ⊔ y.1) (tPush le_sup_left x.2)
      (tPush le_sup_right y.2))
    (by
      rintro x y x' y' hx hy
      have h1 : x.1 ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_left.trans le_sup_left
      have h2 : y.1 ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_right.trans le_sup_left
      have h3 : x'.1 ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_left.trans le_sup_right
      have h4 : y'.1 ≤ (x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1) := le_sup_right.trans le_sup_right
      have ex := (towerEqv_iff h1 h3).mp hx
      have ey := (towerEqv_iff h2 h4).mp hy
      calc tInner P (x.1 ⊔ y.1) (tPush le_sup_left x.2) (tPush le_sup_right y.2)
          = tInner P ((x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1))
              (tPush le_sup_left (tPush le_sup_left x.2))
              (tPush le_sup_left (tPush le_sup_right y.2)) :=
            (tInner_tPush P le_sup_left _ _).symm
        _ = tInner P ((x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1)) (tPush h1 x.2)
              (tPush h2 y.2) := by rw [tPush_trans, tPush_trans]
        _ = tInner P ((x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1)) (tPush h3 x'.2)
              (tPush h4 y'.2) := by rw [ex, ey]
        _ = tInner P ((x.1 ⊔ y.1) ⊔ (x'.1 ⊔ y'.1))
              (tPush le_sup_right (tPush le_sup_left x'.2))
              (tPush le_sup_right (tPush le_sup_right y'.2)) := by
            rw [tPush_trans, tPush_trans]
        _ = tInner P (x'.1 ⊔ y'.1) (tPush le_sup_left x'.2)
              (tPush le_sup_right y'.2) := tInner_tPush P le_sup_right _ _)

/-- o produto interno em QUALQUER andar comum. -/
theorem innerPre_tof_at {N M K : ℕ} (hN : N ≤ K) (hM : M ≤ K)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    innerPre P (tof P N a) (tof P M b)
      = tInner P K (tPush hN a) (tPush hM b) := by
  show tInner P (N ⊔ M) (tPush le_sup_left a) (tPush le_sup_right b)
    = tInner P K (tPush hN a) (tPush hM b)
  calc tInner P (N ⊔ M) (tPush le_sup_left a) (tPush le_sup_right b)
      = tInner P ((N ⊔ M) ⊔ K)
          (tPush le_sup_left (tPush le_sup_left a))
          (tPush le_sup_left (tPush le_sup_right b)) :=
        (tInner_tPush P le_sup_left _ _).symm
    _ = tInner P ((N ⊔ M) ⊔ K)
          (tPush le_sup_right (tPush hN a))
          (tPush le_sup_right (tPush hM b)) := by
        rw [tPush_trans, tPush_trans, tPush_trans, tPush_trans]
    _ = tInner P K (tPush hN a) (tPush hM b) := tInner_tPush P le_sup_right _ _

theorem innerPre_tof_same (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    innerPre P (tof P N a) (tof P N b) = tInner P N a b := by
  rw [innerPre_tof_at (le_refl N) (le_refl N), tPush_self, tPush_self]

instance : Inner ℂ (TowerPre P) := ⟨innerPre P⟩

theorem towerPre_inner_def (x y : TowerPre P) :
    (inner ℂ x y : ℂ) = innerPre P x y := rfl

/-- ★★★ O CORE PRÉ-HILBERT DO COLIMITE (o molde GNS da mathlib). -/
@[reducible] def towerPreCore (P : SiteProfile) :
    PreInnerProductSpace.Core ℂ (TowerPre P) where
  inner := innerPre P
  conj_inner_symm := by
    intro x y
    obtain ⟨N, a, rfl⟩ := exists_tof x
    obtain ⟨M, b, rfl⟩ := exists_tof y
    show conj (innerPre P (tof P M b) (tof P N a))
      = innerPre P (tof P N a) (tof P M b)
    have hN : N ≤ N ⊔ M := le_sup_left
    have hM : M ≤ N ⊔ M := le_sup_right
    rw [innerPre_tof_at hM hN, innerPre_tof_at hN hM, tInner_conj_symm]
  re_inner_nonneg := by
    intro x
    obtain ⟨N, a, rfl⟩ := exists_tof x
    show 0 ≤ (innerPre P (tof P N a) (tof P N a)).re
    rw [innerPre_tof_same]
    exact tInner_self_nonneg P N a
  add_left := by
    intro x y z
    obtain ⟨Nx, a, rfl⟩ := exists_tof x
    obtain ⟨Ny, b, rfl⟩ := exists_tof y
    obtain ⟨Nz, c, rfl⟩ := exists_tof z
    have hx : Nx ≤ Nx ⊔ Ny ⊔ Nz := le_sup_left.trans le_sup_left
    have hy : Ny ≤ Nx ⊔ Ny ⊔ Nz := le_sup_right.trans le_sup_left
    have hz : Nz ≤ Nx ⊔ Ny ⊔ Nz := le_sup_right
    show innerPre P (tof P Nx a + tof P Ny b) (tof P Nz c)
      = innerPre P (tof P Nx a) (tof P Nz c)
        + innerPre P (tof P Ny b) (tof P Nz c)
    rw [tof_add_at hx hy, innerPre_tof_at le_rfl hz, tPush_self,
      innerPre_tof_at hx hz, innerPre_tof_at hy hz, tInner_add_left]
  smul_left := by
    intro x y r
    obtain ⟨N, a, rfl⟩ := exists_tof x
    obtain ⟨M, b, rfl⟩ := exists_tof y
    have hN : N ≤ N ⊔ M := le_sup_left
    have hM : M ≤ N ⊔ M := le_sup_right
    show innerPre P (r • tof P N a) (tof P M b)
      = conj r * innerPre P (tof P N a) (tof P M b)
    rw [tof_smul, innerPre_tof_at hN hM, innerPre_tof_at hN hM, tPush_smul,
      tInner_smul_left]

noncomputable instance : SeminormedAddCommGroup (TowerPre P) :=
  InnerProductSpace.Core.toSeminormedAddCommGroup (c := towerPreCore P)

noncomputable instance : InnerProductSpace ℂ (TowerPre P) :=
  InnerProductSpace.ofCore (towerPreCore P)

/-! ## G — a DEFINITUDE do colimite e o vetor Ω -/

/-- ★★★ A PEDRA 83: A FORMA É DEFINIDA NO COLIMITE INTEIRO — pesos positivos
    em todo andar ⟹ o radical GNS é ZERO. O quociente da pedra 78 é trivial
    aqui: o colimite JÁ é o pré-Hilbert genuíno. -/
theorem towerPre_definite (x : TowerPre P)
    (h : innerPre P x x = 0) : x = 0 := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  rw [innerPre_tof_same] at h
  rw [tInner_self_definite P N h, tof_zero]

/-- Ω = [1]: o vetor do Nome no colimite. -/
def towerOmega (P : SiteProfile) : TowerPre P := tof P 0 1

theorem towerOmega_inner_self :
    innerPre P (towerOmega P) (towerOmega P) = 1 := by
  unfold towerOmega
  rw [innerPre_tof_same]
  unfold tInner
  rw [conjTranspose_one, one_mul, tState_one]

/-- Ω é unitário e o colimite habitado: o pré-Hilbert do fator está pronto
    para o completamento (pedra 84). -/
theorem towerOmega_norm_sq :
    (innerPre P (towerOmega P) (towerOmega P)).re = 1 := by
  rw [towerOmega_inner_self]
  rfl

end

end TGLExt
