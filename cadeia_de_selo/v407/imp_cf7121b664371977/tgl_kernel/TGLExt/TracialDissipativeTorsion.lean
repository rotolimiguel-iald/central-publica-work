import Mathlib

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TORÇÃO TRACIAL-DISSIPATIVA, DO LADO DE LEVI-CIVITA
  [TGLExt — a Face C da Ponte Einstein–Cartan–Miguel, parte algébrica]

A Ponte escreve Γ = Γ_LC + K_β, com K_β a contorção da torção tracial-dissipativa
T^a_{bc} = (δ^a_b V_c − δ^a_c V_b)/(n−1). Esta pedra prova, ponto a ponto e em qualquer
dimensão finita, o que a álgebra dessa escolha entrega:

* a contorção K_{abc} = g_{ab} A_c − g_{bc} A_a (A = V/(n−1)) reproduz a torção e é
  compatível com a métrica;
* o traço da torção é (n−1)·A = V; a parte axial é nula; o termo quadrático da primeira
  identidade de Bianchi é nulo;
* a curvatura de Riemann–Cartan decompõe-se na de Levi-Civita mais ∇̊K e KK
  (Γ̊ simétrica); contraídas, as partes de contorção dão o Ricci
  R_{bd} − R̊_{bd} = −(n−2)∇̊_d A_b − g_{bd}∇̊·A + (n−2)(A_b A_d − g_{bd} A²);
* a derivada covariante da contorção sai da compatibilidade métrica e da regra de Leibniz
  (`covK_Kmix`), e o Ricci da conexão Γ̊ + K fecha sem hipótese extra
  (`ricci_of_tracial_connection`);
* o escalar R = R̊ − 2(n−1)∇̊·A − (n−1)(n−2)A²; o Einstein
  G_{bd} = G̊_{bd} − (n−2)[∇̊_d A_b − g_{bd}∇̊·A − A_b A_d − ((n−3)/2)g_{bd}A²];
  a parte antissimétrica G_{[bd]} = −((n−2)/2)(∇̊_d A_b − ∇̊_b A_d);
* O FORNECEDOR: κT^{tors/diss}_{bd} = (n−2)[∇̊_{(d}A_{b)} − g_{bd}∇̊·A − A_b A_d − ((n−3)/2)g_{bd}A²];
* no fundo FLRW com A = α·n: 3(H−α)² = κρ ⟺ 3H² = κρ + (6αH − 3α²), e a lei em dimensão m.

O que esta pedra NÃO faz: não fixa a escala ℓ de α = θ_M/((n−1)ℓ) [INPUT], não identifica
a torção com um grau físico, não move gate nem bandeira. A primeira identidade de Bianchi
completa (com λ = −1) e a leitura de fluido estão verificadas numericamente fora do kernel.
β jamais literal. Nenhuma lacuna de prova e nenhum axioma novo.
-/

namespace TGLExt.TracialTorsion

open Finset

variable {ι : Type} [Fintype ι] [DecidableEq ι]

/-- o delta de Kronecker real -/
def kd (a b : ι) : ℝ := if a = b then 1 else 0

lemma sum_kd_left (f : ι → ℝ) (d : ι) : ∑ a, kd a d * f a = f d := by
  simp [kd, Finset.sum_ite_eq']

lemma sum_kd_right (f : ι → ℝ) (d : ι) : ∑ a, kd d a * f a = f d := by
  simp [kd, Finset.sum_ite_eq]

lemma sum_kd_self : ∑ a : ι, kd a a = (Fintype.card ι : ℝ) := by
  simp [kd]

/-! ## 1. A torção tracial e a sua contorção -/

/-- [DEF] a torção tracial mista T^a_{bc} = δ^a_b A_c − δ^a_c A_b (A = V/(n−1)) -/
def torsion (A : ι → ℝ) (a b c : ι) : ℝ := kd a b * A c - kd a c * A b

/-- [KERNEL] antissimetria nos índices baixos -/
theorem torsion_antisymm (A : ι → ℝ) (a b c : ι) :
    torsion A a b c = - torsion A a c b := by
  unfold torsion; ring

/-- [KERNEL] o traço da torção: ∑_a T^a_{ac} = (n − 1)·A_c = V_c -/
theorem torsion_trace (A : ι → ℝ) (c : ι) :
    ∑ a, torsion A a a c = ((Fintype.card ι : ℝ) - 1) * A c := by
  unfold torsion
  rw [Finset.sum_sub_distrib, ← Finset.sum_mul, sum_kd_self, sum_kd_left]
  ring

/-- [KERNEL] o termo quadrático da primeira identidade de Bianchi é NULO, em toda dimensão
    e para todo A: ∑_e (T^e_{bc} T^a_{de} + T^e_{cd} T^a_{be} + T^e_{db} T^a_{ce}) = 0 -/
theorem torsion_quadratic_bianchi_zero (A : ι → ℝ) (a b c d : ι) :
    ∑ e, (torsion A e b c * torsion A a d e + torsion A e c d * torsion A a b e
          + torsion A e d b * torsion A a c e) = 0 := by
  have expand : ∀ x y z : ι, ∑ e, torsion A e x y * torsion A a z e
      = kd a z * A y * A x - kd a x * A y * A z - kd a z * A x * A y + kd a y * A x * A z := by
    intro x y z
    unfold torsion
    have h1 : ∑ e, (kd e x * A y - kd e y * A x) * (kd a z * A e - kd a e * A z)
        = ∑ e, kd e x * (A y * (kd a z * A e - kd a e * A z))
          - ∑ e, kd e y * (A x * (kd a z * A e - kd a e * A z)) := by
      rw [← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl (fun e _ => ?_)
      ring
    rw [h1, sum_kd_left (fun e => A y * (kd a z * A e - kd a e * A z)) x,
      sum_kd_left (fun e => A x * (kd a z * A e - kd a e * A z)) y]
    ring
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, expand b c d, expand c d b, expand d b c]
  ring

/-- [DEF] a contorção com todos os índices baixos: K_{abc} = g_{ab} A_c − g_{bc} A_a
    (b é o índice de derivada) -/
def contortion (g : ι → ι → ℝ) (A : ι → ℝ) (a b c : ι) : ℝ := g a b * A c - g b c * A a

/-- [KERNEL] a contorção reproduz a torção tracial baixada: K_{abc} − K_{acb} = g_{ab}A_c − g_{ac}A_b -/
theorem contortion_gives_torsion (g : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i) (A : ι → ℝ) (a b c : ι) :
    contortion g A a b c - contortion g A a c b = g a b * A c - g a c * A b := by
  unfold contortion; rw [hg c b]; ring

/-- [KERNEL] a contorção é compatível com a métrica: K_{abc} + K_{cba} = 0 -/
theorem contortion_metric_compatible (g : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i) (A : ι → ℝ) (a b c : ι) :
    contortion g A a b c + contortion g A c b a = 0 := by
  unfold contortion; rw [hg c b, hg b a]; ring

/-- [KERNEL] a parte axial (totalmente antissimétrica) da torção tracial é NULA -/
theorem torsion_axial_zero (g : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i) (A : ι → ℝ) (a b c : ι) :
    (g a b * A c - g a c * A b) + (g b c * A a - g b a * A c) + (g c a * A b - g c b * A a) = 0 := by
  rw [hg b a, hg c a, hg c b]; ring

/-! ## 2. A decomposição da curvatura de Riemann–Cartan -/

/-- [DEF] Riemann de uma conexão (índice de derivada primeiro):
    R^a_{bcd} = ∂_c Γ^a_{db} − ∂_d Γ^a_{cb} + Γ^a_{ce}Γ^e_{db} − Γ^a_{de}Γ^e_{cb};
    `dGam e a x y` = ∂_e Γ^a_{xy} -/
def riemann (Gam : ι → ι → ι → ℝ) (dGam : ι → ι → ι → ι → ℝ) (a b c d : ι) : ℝ :=
  dGam c a d b - dGam d a c b + ∑ e, (Gam a c e * Gam e d b - Gam a d e * Gam e c b)

/-- [DEF] a derivada covariante de Levi-Civita da contorção: ∇̊_c K^a_{db} -/
def covK (G0 K : ι → ι → ι → ℝ) (dK : ι → ι → ι → ι → ℝ) (c a d b : ι) : ℝ :=
  dK c a d b + ∑ e, (G0 a c e * K e d b - G0 e c d * K a e b - G0 e c b * K a d e)

/-- [KERNEL] ★★ A DECOMPOSIÇÃO DE RIEMANN–CARTAN: com Γ = Γ̊ + K e Γ̊ simétrica,
    R^a_{bcd}(Γ) = R^a_{bcd}(Γ̊) + ∇̊_c K^a_{db} − ∇̊_d K^a_{cb} + K^a_{ce}K^e_{db} − K^a_{de}K^e_{cb} -/
theorem riemann_cartan_decomposition (G0 K : ι → ι → ι → ℝ) (dG0 dK : ι → ι → ι → ι → ℝ)
    (hsym : ∀ e x y, G0 e x y = G0 e y x) (a b c d : ι) :
    riemann (fun x y z => G0 x y z + K x y z) (fun w x y z => dG0 w x y z + dK w x y z) a b c d
      = riemann G0 dG0 a b c d + covK G0 K dK c a d b - covK G0 K dK d a c b
        + ∑ e, (K a c e * K e d b - K a d e * K e c b) := by
  simp only [riemann, covK]
  have key : (∑ e, ((G0 a c e + K a c e) * (G0 e d b + K e d b) - (G0 a d e + K a d e) * (G0 e c b + K e c b)))
      = ∑ e, ((G0 a c e * G0 e d b - G0 a d e * G0 e c b)
          + (G0 a c e * K e d b - G0 e c d * K a e b - G0 e c b * K a d e)
          - (G0 a d e * K e c b - G0 e d c * K a e b - G0 e d b * K a c e)
          + (K a c e * K e d b - K a d e * K e c b)) := by
    refine Finset.sum_congr rfl (fun e _ => ?_)
    rw [hsym e c d]; ring
  rw [key, Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_add_distrib]
  ring

/-- [DEF] a contração de Ricci R_{bd} = ∑_a R^a_{bad} -/
def ricciOf (Gam : ι → ι → ι → ℝ) (dGam : ι → ι → ι → ι → ℝ) (b d : ι) : ℝ :=
  ∑ a, riemann Gam dGam a b a d

/-! ## 3. As contrações do Ricci para a contorção tracial -/

section Ricci

variable (g gi : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i)
  (hinv : ∀ i j, ∑ k, g i k * gi k j = kd i j)
  (hinv' : ∀ i j, ∑ k, gi i k * g k j = kd i j)

/-- [DEF] o vetor com índice alto A^a = g^{ad} A_d -/
def raise (A : ι → ℝ) (a : ι) : ℝ := ∑ d, gi a d * A d

/-- [DEF] a contorção mista K^a_{bc} = δ^a_b A_c − g_{bc} A^a -/
def Kmix (A : ι → ℝ) (a b c : ι) : ℝ := kd a b * A c - g b c * raise gi A a

include hinv in
/-- [KERNEL] baixar o índice levantado devolve o vetor: ∑_e g_{de} A^e = A_d -/
theorem lower_raise (A : ι → ℝ) (d : ι) : ∑ e, g d e * raise gi A e = A d := by
  unfold raise
  have : ∑ e, g d e * ∑ f, gi e f * A f = ∑ f, (∑ e, g d e * gi e f) * A f := by
    simp_rw [Finset.mul_sum, Finset.sum_mul]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun f _ => Finset.sum_congr rfl (fun e _ => ?_))
    ring
  rw [this]
  simp_rw [hinv]
  exact sum_kd_right A d

include hg hinv in
/-- [KERNEL] o traço da contorção mista: ∑_a K^a_{ae} = (n − 1)·A_e -/
theorem Kmix_trace (A : ι → ℝ) (e : ι) :
    ∑ a, Kmix g gi A a a e = ((Fintype.card ι : ℝ) - 1) * A e := by
  unfold Kmix
  rw [Finset.sum_sub_distrib, ← Finset.sum_mul, sum_kd_self]
  have h : ∑ a, g a e * raise gi A a = A e := by
    rw [← lower_raise g gi hinv A e]
    refine Finset.sum_congr rfl (fun a _ => ?_)
    rw [hg a e]
  rw [h]; ring

/-- [DEF] A² = A_a A^a -/
def normSq (A : ι → ℝ) : ℝ := ∑ a, A a * raise gi A a

include hg hinv in
/-- [KERNEL] ★ a parte quadrática do Ricci:
    ∑_{a,e} (K^a_{ae}K^e_{db} − K^a_{de}K^e_{ab}) = (n − 2)(A_b A_d − g_{db} A²) -/
theorem ricci_KK (A : ι → ℝ) (d b : ι) :
    ∑ a, ∑ e, (Kmix g gi A a a e * Kmix g gi A e d b - Kmix g gi A a d e * Kmix g gi A e a b)
      = ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A) := by
  have hlr := lower_raise g gi hinv A
  -- primeira parte: ∑_e (∑_a K^a_{ae}) K^e_{db} = (n−1) ∑_e A_e K^e_{db}
  have p1 : ∑ a, ∑ e, Kmix g gi A a a e * Kmix g gi A e d b
      = ((Fintype.card ι : ℝ) - 1) * (A d * A b - g d b * normSq gi A) := by
    rw [Finset.sum_comm]
    have : ∀ e, ∑ a, Kmix g gi A a a e * Kmix g gi A e d b
        = ((Fintype.card ι : ℝ) - 1) * (A e * Kmix g gi A e d b) := by
      intro e
      rw [← Finset.sum_mul, Kmix_trace g gi hg hinv A e]; ring
    simp_rw [this, ← Finset.mul_sum]
    congr 1
    unfold Kmix normSq
    have q1 : ∑ e, A e * (kd e d * A b - g d b * raise gi A e)
        = ∑ e, kd e d * (A e * A b) - g d b * ∑ e, A e * raise gi A e := by
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl (fun e _ => ?_); ring
    rw [q1, sum_kd_left (fun e => A e * A b) d]
  -- segunda parte: ∑_{a,e} K^a_{de} K^e_{ab} = A_d A_b − g_{db} A²
  have p2 : ∑ a, ∑ e, Kmix g gi A a d e * Kmix g gi A e a b
      = A d * A b - g d b * normSq gi A := by
    unfold Kmix normSq
    have r : ∀ a, ∑ e, (kd a d * A e - g d e * raise gi A a) * (kd e a * A b - g a b * raise gi A e)
        = kd a d * (A a * A b) - kd a d * (g a b * normSq gi A)
          - raise gi A a * A b * g d a + g a b * raise gi A a * A d := by
      intro a
      have e1 : ∑ e, (kd a d * A e - g d e * raise gi A a) * (kd e a * A b - g a b * raise gi A e)
          = kd a d * A b * ∑ e, kd e a * A e - kd a d * g a b * ∑ e, A e * raise gi A e
            - raise gi A a * A b * ∑ e, kd e a * g d e + g a b * raise gi A a * ∑ e, g d e * raise gi A e := by
        simp_rw [Finset.mul_sum, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
        refine Finset.sum_congr rfl (fun e _ => ?_); ring
      rw [e1, sum_kd_left A a, sum_kd_left (fun e => g d e) a, hlr d]
      unfold normSq; ring
    simp_rw [r]
    rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_sub_distrib]
    rw [sum_kd_left (fun a => A a * A b) d, sum_kd_left (fun a => g a b * normSq gi A) d]
    have t3 : ∑ a, raise gi A a * A b * g d a = A d * A b := by
      rw [← hlr d, Finset.sum_mul]
      refine Finset.sum_congr rfl (fun a _ => ?_); ring
    have t4 : ∑ a, g a b * raise gi A a * A d = A b * A d := by
      rw [← hlr b, Finset.sum_mul]
      refine Finset.sum_congr rfl (fun a _ => ?_); rw [hg a b]
    rw [t3, t4, hg d b]; unfold normSq; ring
  simp only [Finset.sum_sub_distrib]
  rw [p1, p2]
  ring

/-- [DEF] a derivada covariante de Levi-Civita da contorção mista, com `DA c b` = ∇̊_c A_b
    (∇̊g = 0 e ∇̊δ = 0): ∇̊_c K^a_{db} = δ^a_d ∇̊_c A_b − g_{db} ∇̊_c A^a -/
def DKmix (DA : ι → ι → ℝ) (c a d b : ι) : ℝ :=
  kd a d * DA c b - g d b * ∑ e, gi a e * DA c e

/-- [DEF] a divergência ∇̊·A = g^{ae} ∇̊_a A_e -/
def divA (DA : ι → ι → ℝ) : ℝ := ∑ a, ∑ e, gi a e * DA a e

include hg hinv in
/-- [KERNEL] ★ a parte derivativa do Ricci:
    ∑_a (∇̊_a K^a_{db} − ∇̊_d K^a_{ab}) = −(n − 2)∇̊_d A_b − g_{db} ∇̊·A -/
theorem ricci_DK (DA : ι → ι → ℝ) (d b : ι) :
    ∑ a, (DKmix g gi DA a a d b - DKmix g gi DA d a a b)
      = -((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA := by
  unfold DKmix divA
  rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, Finset.sum_sub_distrib]
  rw [sum_kd_left (fun a => DA a b) d, ← Finset.sum_mul, sum_kd_self, ← Finset.mul_sum]
  have h : ∑ a, g a b * ∑ e, gi a e * DA d e = DA d b := by
    have := lower_raise g gi hinv (fun e => DA d e) b
    unfold raise at this
    rw [← this]
    refine Finset.sum_congr rfl (fun a _ => ?_); rw [hg a b]
  rw [h]; ring

include hinv hinv' in
/-- [KERNEL] ★ a derivada covariante da contorção mista SAI da compatibilidade métrica:
    se ∂_c g_{db} = Γ̊^e_{cd} g_{eb} + Γ̊^e_{cb} g_{de}, ∂_c g^{ae} = −g^{af}(∂_c g_{fh})g^{he}
    e dK é a derivada (Leibniz) de K^a_{db} = δ^a_d A_b − g_{db}A^a, então
    ∇̊_c K^a_{db} = δ^a_d ∇̊_c A_b − g_{db} g^{ae} ∇̊_c A_e, com ∇̊_c A_b = ∂_c A_b − Γ̊^e_{cb} A_e -/
theorem covK_Kmix (G0 : ι → ι → ι → ℝ) (A : ι → ℝ) (dg dgi : ι → ι → ι → ℝ) (dA : ι → ι → ℝ)
    (dK : ι → ι → ι → ι → ℝ)
    (hdg : ∀ c d b, dg c d b = ∑ e, (G0 e c d * g e b + G0 e c b * g d e))
    (hdgi : ∀ c a e, dgi c a e = - ∑ f, ∑ h, gi a f * dg c f h * gi h e)
    (hdK : ∀ c a d b, dK c a d b = kd a d * dA c b - dg c d b * raise gi A a
        - g d b * (∑ e, dgi c a e * A e + ∑ e, gi a e * dA c e))
    (c a d b : ι) :
    covK G0 (Kmix g gi A) dK c a d b
      = DKmix g gi (fun x y => dA x y - ∑ e, G0 e x y * A e) c a d b := by
  have hlr := lower_raise g gi hinv A
  have hsplit : covK G0 (Kmix g gi A) dK c a d b
      = dK c a d b + (∑ e, G0 a c e * Kmix g gi A e d b - ∑ e, G0 e c d * Kmix g gi A a e b
          - ∑ e, G0 e c b * Kmix g gi A a d e) := by
    unfold covK
    rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib]
  have s1 : ∑ e, G0 a c e * Kmix g gi A e d b
      = G0 a c d * A b - g d b * ∑ e, G0 a c e * raise gi A e := by
    unfold Kmix
    have h : ∑ e, G0 a c e * (kd e d * A b - g d b * raise gi A e)
        = ∑ e, kd e d * (G0 a c e * A b) - g d b * ∑ e, G0 a c e * raise gi A e := by
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl (fun e _ => ?_); ring
    rw [h, sum_kd_left (fun e => G0 a c e * A b) d]
  have s2 : ∑ e, G0 e c d * Kmix g gi A a e b
      = G0 a c d * A b - raise gi A a * ∑ e, G0 e c d * g e b := by
    unfold Kmix
    have h : ∑ e, G0 e c d * (kd a e * A b - g e b * raise gi A a)
        = ∑ e, kd a e * (G0 e c d * A b) - raise gi A a * ∑ e, G0 e c d * g e b := by
      rw [Finset.mul_sum, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl (fun e _ => ?_); ring
    rw [h, sum_kd_right (fun e => G0 e c d * A b) a]
  have s3 : ∑ e, G0 e c b * Kmix g gi A a d e
      = kd a d * ∑ e, G0 e c b * A e - raise gi A a * ∑ e, G0 e c b * g d e := by
    unfold Kmix
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl (fun e _ => ?_); ring
  have hdg' : dg c d b = ∑ e, G0 e c d * g e b + ∑ e, G0 e c b * g d e := by
    rw [hdg c d b, Finset.sum_add_distrib]
  have K1 : ∑ e, dgi c a e * A e = - ∑ f, ∑ h, gi a f * dg c f h * raise gi A h := by
    simp only [hdgi]
    unfold raise
    simp only [Finset.mul_sum, Finset.sum_mul, neg_mul, Finset.sum_neg_distrib]
    congr 1
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun f _ => ?_)
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun h _ => Finset.sum_congr rfl (fun e _ => ?_))
    ring
  have T1 : ∑ f, ∑ h, ∑ k, gi a f * G0 k c f * g k h * raise gi A h
      = ∑ f, gi a f * ∑ k, G0 k c f * A k := by
    refine Finset.sum_congr rfl (fun f _ => ?_)
    rw [Finset.sum_comm, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun k _ => ?_)
    rw [← hlr k, Finset.mul_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl (fun h _ => ?_); ring
  have T2 : ∑ f, ∑ h, ∑ k, gi a f * G0 k c h * g f k * raise gi A h
      = ∑ h, G0 a c h * raise gi A h := by
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun h _ => ?_)
    rw [Finset.sum_comm]
    have hk : ∀ k, ∑ f, gi a f * G0 k c h * g f k * raise gi A h
        = kd a k * (G0 k c h * raise gi A h) := by
      intro k
      rw [← hinv' a k, Finset.sum_mul]
      refine Finset.sum_congr rfl (fun f _ => ?_); ring
    simp only [hk]
    exact sum_kd_right (fun k => G0 k c h * raise gi A h) a
  have K2 : ∑ f, ∑ h, gi a f * dg c f h * raise gi A h
      = ∑ f, gi a f * ∑ k, G0 k c f * A k + ∑ h, G0 a c h * raise gi A h := by
    rw [← T1, ← T2, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun f _ => ?_)
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl (fun h _ => ?_)
    rw [← Finset.sum_add_distrib, hdg c f h, Finset.mul_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl (fun k _ => ?_); ring
  have key : ∑ e, dgi c a e * A e + ∑ e, G0 a c e * raise gi A e
      = - ∑ e, gi a e * ∑ f, G0 f c e * A f := by
    rw [K1, K2]; ring
  have hR : ∑ e, gi a e * (dA c e - ∑ f, G0 f c e * A f)
      = ∑ e, gi a e * dA c e - ∑ e, gi a e * ∑ f, G0 f c e * A f := by
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl (fun e _ => ?_); ring
  simp only [DKmix]
  linear_combination hsplit + s1 - s2 - s3 + hdK c a d b - raise gi A a * hdg'
    + g d b * hR - g d b * key

include hg hinv in
/-- [KERNEL] ★★ O RICCI FECHADO da conexão Γ̊ + K (K tracial), dada a derivada covariante
    da contorção: R_{bd} = R̊_{bd} − (n−2)∇̊_d A_b − g_{db}∇̊·A + (n−2)(A_b A_d − g_{db}A²) -/
theorem ricci_closed_form (G0 : ι → ι → ι → ℝ) (dG0 dK : ι → ι → ι → ι → ℝ) (A : ι → ℝ)
    (DA : ι → ι → ℝ) (hsym : ∀ e x y, G0 e x y = G0 e y x)
    (hcov : ∀ c a d b, covK G0 (Kmix g gi A) dK c a d b = DKmix g gi DA c a d b) (b d : ι) :
    ricciOf (fun x y z => G0 x y z + Kmix g gi A x y z) (fun w x y z => dG0 w x y z + dK w x y z) b d
      = ricciOf G0 dG0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A) := by
  have h : ∀ a, riemann (fun x y z => G0 x y z + Kmix g gi A x y z)
        (fun w x y z => dG0 w x y z + dK w x y z) a b a d
      = riemann G0 dG0 a b a d + (DKmix g gi DA a a d b - DKmix g gi DA d a a b)
        + ∑ e, (Kmix g gi A a a e * Kmix g gi A e d b - Kmix g gi A a d e * Kmix g gi A e a b) := by
    intro a
    have e1 := riemann_cartan_decomposition G0 (Kmix g gi A) dG0 dK hsym a b a d
    rw [hcov a a d b, hcov d a a b] at e1
    linear_combination e1
  unfold ricciOf
  have hsum : ∑ a, riemann (fun x y z => G0 x y z + Kmix g gi A x y z)
        (fun w x y z => dG0 w x y z + dK w x y z) a b a d
      = ∑ a, (riemann G0 dG0 a b a d + (DKmix g gi DA a a d b - DKmix g gi DA d a a b)
        + ∑ e, (Kmix g gi A a a e * Kmix g gi A e d b - Kmix g gi A a d e * Kmix g gi A e a b)) :=
    Finset.sum_congr rfl (fun a _ => h a)
  rw [hsum, Finset.sum_add_distrib, Finset.sum_add_distrib]
  linear_combination ricci_DK g gi hg hinv DA d b + ricci_KK g gi hg hinv A d b

include hg hinv hinv' in
/-- [KERNEL] ★★ o Ricci da conexão tracial SEM hipótese sobre ∇̊K: só a compatibilidade
    métrica de Γ̊, a derivada da inversa e a regra de Leibniz -/
theorem ricci_of_tracial_connection (G0 : ι → ι → ι → ℝ) (dG0 dK : ι → ι → ι → ι → ℝ)
    (A : ι → ℝ) (dg dgi : ι → ι → ι → ℝ) (dA : ι → ι → ℝ) (hsym : ∀ e x y, G0 e x y = G0 e y x)
    (hdg : ∀ c d b, dg c d b = ∑ e, (G0 e c d * g e b + G0 e c b * g d e))
    (hdgi : ∀ c a e, dgi c a e = - ∑ f, ∑ h, gi a f * dg c f h * gi h e)
    (hdK : ∀ c a d b, dK c a d b = kd a d * dA c b - dg c d b * raise gi A a
        - g d b * (∑ e, dgi c a e * A e + ∑ e, gi a e * dA c e))
    (b d : ι) :
    ricciOf (fun x y z => G0 x y z + Kmix g gi A x y z) (fun w x y z => dG0 w x y z + dK w x y z) b d
      = ricciOf G0 dG0 b d - ((Fintype.card ι : ℝ) - 2) * (dA d b - ∑ e, G0 e d b * A e)
        - g d b * divA gi (fun x y => dA x y - ∑ e, G0 e x y * A e)
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A) :=
  ricci_closed_form g gi hg hinv G0 dG0 dK A (fun x y => dA x y - ∑ e, G0 e x y * A e) hsym
    (fun c a d b => covK_Kmix g gi hinv hinv' G0 A dg dgi dA dK hdg hdgi hdK c a d b) b d

/-- [DEF] o escalar de curvatura R = g^{bd} R_{bd} -/
def scalarOf (Ric : ι → ι → ℝ) : ℝ := ∑ b, ∑ d, gi b d * Ric b d

/-- [DEF] o tensor de Einstein G_{bd} = R_{bd} − ½ g_{bd} R -/
noncomputable def einsteinOf (Ric : ι → ι → ℝ) (b d : ι) : ℝ := Ric b d - g b d * scalarOf gi Ric / 2

include hg hinv in
/-- [KERNEL] ★ o escalar fechado: R = R̊ − 2(n−1)∇̊·A − (n−1)(n−2)A² -/
theorem scalar_closed_form (hgi : ∀ i j, gi i j = gi j i) (Ric Ric0 : ι → ι → ℝ) (A : ι → ℝ)
    (DA : ι → ι → ℝ)
    (hRic : ∀ b d, Ric b d = Ric0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A)) :
    scalarOf gi Ric = scalarOf gi Ric0 - 2 * ((Fintype.card ι : ℝ) - 1) * divA gi DA
      - ((Fintype.card ι : ℝ) - 1) * ((Fintype.card ι : ℝ) - 2) * normSq gi A := by
  have c1 : ∑ b, ∑ d, gi b d * DA d b = divA gi DA := by
    unfold divA
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl (fun x _ => Finset.sum_congr rfl (fun y _ => ?_))
    rw [hgi y x]
  have c2 : ∑ b, ∑ d, gi b d * g d b = (Fintype.card ι : ℝ) := by
    rw [Finset.sum_comm, ← (sum_kd_self (ι := ι))]
    refine Finset.sum_congr rfl (fun x _ => ?_)
    rw [← hinv x x]
    refine Finset.sum_congr rfl (fun y _ => ?_); ring
  have c3 : ∑ b, ∑ d, gi b d * (A b * A d) = normSq gi A := by
    unfold normSq raise
    refine Finset.sum_congr rfl (fun x _ => ?_)
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun y _ => ?_); ring
  have e : ∀ b d, gi b d * Ric b d = gi b d * Ric0 b d
      - ((Fintype.card ι : ℝ) - 2) * (gi b d * DA d b) - divA gi DA * (gi b d * g d b)
      + ((Fintype.card ι : ℝ) - 2) * (gi b d * (A b * A d))
      - ((Fintype.card ι : ℝ) - 2) * normSq gi A * (gi b d * g d b) := by
    intro b d; rw [hRic b d]; ring
  unfold scalarOf
  simp only [e, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]
  linear_combination (-((Fintype.card ι : ℝ) - 2)) * c1
    + (-(divA gi DA) - ((Fintype.card ι : ℝ) - 2) * normSq gi A) * c2
    + ((Fintype.card ι : ℝ) - 2) * c3

include hg hinv in
/-- [KERNEL] ★★ O EINSTEIN FECHADO:
    G_{bd} = G̊_{bd} − (n−2)[∇̊_d A_b − g_{bd}∇̊·A − A_b A_d − ((n−3)/2) g_{bd} A²] -/
theorem einstein_closed_form (hgi : ∀ i j, gi i j = gi j i) (Ric Ric0 : ι → ι → ℝ) (A : ι → ℝ)
    (DA : ι → ι → ℝ)
    (hRic : ∀ b d, Ric b d = Ric0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A)) (b d : ι) :
    einsteinOf g gi Ric b d = einsteinOf g gi Ric0 b d
      - ((Fintype.card ι : ℝ) - 2) * (DA d b - g b d * divA gi DA - A b * A d
          - ((Fintype.card ι : ℝ) - 3) / 2 * (g b d * normSq gi A)) := by
  have hs := scalar_closed_form g gi hg hinv hgi Ric Ric0 A DA hRic
  unfold einsteinOf
  linear_combination hRic b d - (g b d / 2) * hs
    - (divA gi DA + ((Fintype.card ι : ℝ) - 2) * normSq gi A) * hg d b

include hg in
/-- [KERNEL] ★ a parte antissimétrica: G_{[bd]} = −((n−2)/2)(∇̊_d A_b − ∇̊_b A_d) —
    nula se e só se A é localmente um gradiente (F = dA = 0) -/
theorem einstein_antisymmetric_part (Ric Ric0 : ι → ι → ℝ) (A : ι → ℝ) (DA : ι → ι → ℝ)
    (hRic0 : ∀ b d, Ric0 b d = Ric0 d b)
    (hRic : ∀ b d, Ric b d = Ric0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A)) (b d : ι) :
    (einsteinOf g gi Ric b d - einsteinOf g gi Ric d b) / 2
      = -(((Fintype.card ι : ℝ) - 2) / 2) * (DA d b - DA b d) := by
  unfold einsteinOf
  linear_combination (1 / 2 : ℝ) * hRic b d - (1 / 2 : ℝ) * hRic d b + (1 / 2 : ℝ) * hRic0 b d
    + (scalarOf gi Ric / 4 - divA gi DA / 2 - ((Fintype.card ι : ℝ) - 2) * normSq gi A / 2) * hg d b

/-- [DEF] o FORNECEDOR DE TORÇÃO κ T^{tors/diss}_{bd}: a parte simétrica de G̊ − G
    (a geometria fica Levi-Civita e a torção vira fonte) -/
noncomputable def torsionSupplier (Ric Ric0 : ι → ι → ℝ) (b d : ι) : ℝ :=
  ((einsteinOf g gi Ric0 b d - einsteinOf g gi Ric b d)
    + (einsteinOf g gi Ric0 d b - einsteinOf g gi Ric d b)) / 2

include hg hinv in
/-- [KERNEL] ★★★ O FORNECEDOR EM FORMA FECHADA:
    κ T^{tors/diss}_{bd} = (n−2)[∇̊_{(d}A_{b)} − g_{bd}∇̊·A − A_b A_d − ((n−3)/2) g_{bd} A²] -/
theorem torsion_supplier_closed_form (hgi : ∀ i j, gi i j = gi j i) (Ric Ric0 : ι → ι → ℝ)
    (A : ι → ℝ) (DA : ι → ι → ℝ)
    (hRic : ∀ b d, Ric b d = Ric0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A)) (b d : ι) :
    torsionSupplier g gi Ric Ric0 b d = ((Fintype.card ι : ℝ) - 2) *
      ((DA d b + DA b d) / 2 - g b d * divA gi DA - A b * A d
        - ((Fintype.card ι : ℝ) - 3) / 2 * (g b d * normSq gi A)) := by
  have h1 := einstein_closed_form g gi hg hinv hgi Ric Ric0 A DA hRic b d
  have h2 := einstein_closed_form g gi hg hinv hgi Ric Ric0 A DA hRic d b
  unfold torsionSupplier
  linear_combination (-(1 / 2 : ℝ)) * h1 - (1 / 2 : ℝ) * h2
    - (((Fintype.card ι : ℝ) - 2) / 2 * (divA gi DA + ((Fintype.card ι : ℝ) - 3) / 2 * normSq gi A))
      * hg d b

end Ricci

/-! ## 4. O fundo FLRW -/

/-- [KERNEL] ★ a lei de expansão com torção tracial (A = α n, α constante, FLRW plano):
    a equação de Friedmann com a fonte de torção 6αH − 3α² é exatamente 3(H − α)² = κρ -/
theorem flrw_torsion_shift (H α κρ : ℝ) :
    3 * H ^ 2 = κρ + (6 * α * H - 3 * α ^ 2) ↔ 3 * (H - α) ^ 2 = κρ := by
  constructor <;> intro h <;> nlinarith [h]

/-- [KERNEL] no futuro vazio (κρ = 0) a taxa de expansão é H = α: a torção tracial com α
    constante faz o papel de uma taxa de de Sitter -/
theorem flrw_torsion_empty_limit (H α : ℝ) (h : 3 * (H - α) ^ 2 = 0) : H = α := by
  have : (H - α) ^ 2 = 0 := by linarith
  have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
  linarith

/-- [KERNEL] a lei em dimensão m: com ϑ = (m−1)H e a fonte κρ_tors = (m−2)[αϑ − ((m−1)/2)α²],
    ((m−1)(m−2)/2) H² = κρ + κρ_tors ⟺ ((m−1)(m−2)/2)(H − α)² = κρ -/
theorem flrw_torsion_shift_dim (m H α κρ : ℝ) :
    (m - 1) * (m - 2) / 2 * H ^ 2 = κρ + (m - 2) * (α * ((m - 1) * H) - (m - 1) / 2 * α ^ 2)
      ↔ (m - 1) * (m - 2) / 2 * (H - α) ^ 2 = κρ := by
  constructor <;> intro h <;> linear_combination h

end TGLExt.TracialTorsion
