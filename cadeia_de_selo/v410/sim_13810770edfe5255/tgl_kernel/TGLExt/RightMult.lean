import TGLExt.TheCoinage

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 96a — RightMult: a multiplicação à direita e o SEPARADOR
  [TGLExt — v135, a chave da cunha]

Ω é cíclico para M_TGL (pedra 86). Esta pedra prova que Ω é SEPARADOR:

* `tState_kms` — a lei KMS do perfil geral: φ(ab) = φ(b·ρaρ⁻¹), com a
  densidade diagonal EXPLÍCITA (computação de pesos, sem análise);
* `rmulPre`/`rmulCLM`/`rTowerPi` — a multiplicação à DIREITA, limitada no
  colimite (bound UNIFORME: Cauchy–Schwarz por entrada + pesos somando 1 +
  a cauda ⊗1 fatorizada por indução de fatiamento espelhada) e estendida
  a B(H_φ);
* ★★ `rTowerPi_star` — o ADJUNTO MODULAR da direita: star(r_y) = r_{ρy†ρ⁻¹}
  — o adjunto da direita é OUTRA direita, torcida pela densidade (KMS);
* ★★ `rTowerPi_mem_commutant` — r(y) ∈ π(torre)′; e todo A ∈ M_TGL =
  π(torre)′′ comuta com toda direita (`factor_comm_rTowerPi`);
* ★ `rTowerPi_omega` — r(y)Ω = [y]: a órbita direita do Nome é a torre;
* ★★★ `factor_omega_separating` — O SEPARADOR: A ∈ M_TGL, AΩ = 0 ⟹
  A[y] = A(r(y)Ω) = r(y)(AΩ) = 0 no denso ⟹ A = 0.
  Ω cíclico E separador para o fator — o par de Reeh–Schlieder da casa.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Kronecker Matrix UniformSpace
open scoped ComplexConjugate

noncomputable section

variable {P : SiteProfile}

/-! ## A0 — habitação dos índices -/

instance chainIdx_nonempty : ∀ N, Nonempty (chainIdx N)
  | 0 => ⟨(0 : Fin 2)⟩
  | (N + 1) => ⟨((chainIdx_nonempty N).some, (0 : Fin 2))⟩

/-! ## A — a densidade explícita e a lei KMS do perfil -/

/-- a densidade diagonal do andar N (os pesos da torre). -/
def rhoMat (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  Matrix.diagonal (fun k => ((towerW P N k : ℝ) : ℂ))

/-- a inversa diagonal. -/
def rhoMatInv (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  Matrix.diagonal (fun k => (((towerW P N k)⁻¹ : ℝ) : ℂ))

theorem rhoMat_mul_inv (P : SiteProfile) (N : ℕ) :
    rhoMat P N * rhoMatInv P N = 1 := by
  unfold rhoMat rhoMatInv
  rw [Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  funext k
  rw [← Complex.ofReal_mul, mul_inv_cancel₀ (ne_of_gt (towerW_pos P N k))]
  norm_num

theorem rhoMatInv_mul (P : SiteProfile) (N : ℕ) :
    rhoMatInv P N * rhoMat P N = 1 := by
  unfold rhoMat rhoMatInv
  rw [Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
  congr 1
  funext k
  rw [← Complex.ofReal_mul, inv_mul_cancel₀ (ne_of_gt (towerW_pos P N k))]
  norm_num

theorem rhoMat_conjT (P : SiteProfile) (N : ℕ) :
    (rhoMat P N)ᴴ = rhoMat P N := by
  unfold rhoMat
  rw [Matrix.diagonal_conjTranspose]
  congr 1
  funext k
  simp [Complex.conj_ofReal]

theorem rhoMatInv_conjT (P : SiteProfile) (N : ℕ) :
    (rhoMatInv P N)ᴴ = rhoMatInv P N := by
  unfold rhoMatInv
  rw [Matrix.diagonal_conjTranspose]
  congr 1
  funext k
  simp [Complex.conj_ofReal]

/-- a torção modular de y: ρ·y†·ρ⁻¹ (o adjunto KMS da direita). -/
def modTwist (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  rhoMat P N * yᴴ * rhoMatInv P N

theorem modTwist_apply (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) (j k : chainIdx N) :
    modTwist P y j k
      = ((towerW P N j : ℝ) : ℂ) * star (y k j)
          * (((towerW P N k)⁻¹ : ℝ) : ℂ) := by
  unfold modTwist rhoMat rhoMatInv
  rw [Matrix.mul_diagonal, Matrix.diagonal_mul, Matrix.conjTranspose_apply]
  try ring

/-- desfazer a torção: ρ·(modTwist y)†·ρ⁻¹ = y. -/
theorem rho_conj_modTwist_star (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rhoMat P N * (modTwist P y)ᴴ * rhoMatInv P N = y := by
  unfold modTwist
  rw [Matrix.conjTranspose_mul, Matrix.conjTranspose_mul,
    rhoMat_conjT, rhoMatInv_conjT, Matrix.conjTranspose_conjTranspose]
  calc rhoMat P N * (rhoMatInv P N * (y * rhoMat P N)) * rhoMatInv P N
      = (rhoMat P N * rhoMatInv P N) * y * (rhoMat P N * rhoMatInv P N) := by
        noncomm_ring
    _ = y := by rw [rhoMat_mul_inv]; simp

/-- [KERNEL] ★★ A LEI KMS DO PERFIL: φ(a·b) = φ(b·ρaρ⁻¹) — computação
    direta de pesos; a estrutura de equilíbrio do estado, explícita. -/
theorem tState_kms (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P N (a * b)
      = tState P N (b * (rhoMat P N * a * rhoMatInv P N)) := by
  unfold tState
  have hL : ∀ k : chainIdx N,
      ((towerW P N k : ℝ) : ℂ) * (a * b) k k
        = ∑ j, ((towerW P N k : ℝ) : ℂ) * a k j * b j k := by
    intro k
    rw [Matrix.mul_apply, Finset.mul_sum]
    exact Finset.sum_congr rfl fun j _ => by ring
  have hR : ∀ j : chainIdx N,
      ((towerW P N j : ℝ) : ℂ)
          * (b * (rhoMat P N * a * rhoMatInv P N)) j j
        = ∑ k, ((towerW P N k : ℝ) : ℂ) * a k j * b j k := by
    intro j
    rw [Matrix.mul_apply, Finset.mul_sum]
    refine Finset.sum_congr rfl fun k _ => ?_
    have hmid : (rhoMat P N * a * rhoMatInv P N) k j
        = ((towerW P N k : ℝ) : ℂ) * a k j * (((towerW P N j)⁻¹ : ℝ) : ℂ) := by
      unfold rhoMat rhoMatInv
      rw [Matrix.mul_diagonal, Matrix.diagonal_mul]
      try ring
    rw [hmid]
    have hinv : ((towerW P N j : ℝ) : ℂ) * (((towerW P N j)⁻¹ : ℝ) : ℂ) = 1 := by
      rw [← Complex.ofReal_mul, mul_inv_cancel₀ (ne_of_gt (towerW_pos P N j))]
      norm_num
    calc ((towerW P N j : ℝ) : ℂ)
          * (b j k * (((towerW P N k : ℝ) : ℂ) * a k j
              * (((towerW P N j)⁻¹ : ℝ) : ℂ)))
        = (((towerW P N j : ℝ) : ℂ) * (((towerW P N j)⁻¹ : ℝ) : ℂ))
            * (((towerW P N k : ℝ) : ℂ) * a k j * b j k) := by ring
      _ = ((towerW P N k : ℝ) : ℂ) * a k j * b j k := by rw [hinv, one_mul]
  rw [Finset.sum_congr rfl (fun k _ => hL k),
    Finset.sum_congr rfl (fun j _ => hR j)]
  exact Finset.sum_comm

/-! ## B — a multiplicação à direita no colimite -/

/-- a multiplicação à direita por y (andar N) no colimite. -/
def rmulPre (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P → TowerPre P :=
  Quotient.map
    (fun q => ⟨N ⊔ q.1, tPush le_sup_right q.2 * tPush le_sup_left y⟩)
    (by
      rintro q q' hq
      have hK : (N ⊔ q.1) ≤ (N ⊔ q.1) ⊔ (N ⊔ q'.1) := le_sup_left
      have hK' : (N ⊔ q'.1) ≤ (N ⊔ q.1) ⊔ (N ⊔ q'.1) := le_sup_right
      have eq := (towerEqv_iff (x := q) (y := q')
        (K := (N ⊔ q.1) ⊔ (N ⊔ q'.1))
        (le_sup_right.trans hK) (le_sup_right.trans hK')).mp hq
      refine (towerEqv_iff hK hK').mpr ?_
      show tPush hK (tPush le_sup_right q.2 * tPush le_sup_left y)
        = tPush hK' (tPush le_sup_right q'.2 * tPush le_sup_left y)
      rw [tPush_mul, tPush_mul, tPush_trans, tPush_trans, tPush_trans,
        tPush_trans, eq])

theorem rmulPre_tof_at {N M K : ℕ} (hN : N ≤ K) (hM : M ≤ K)
    (y : Matrix (chainIdx N) (chainIdx N) ℂ)
    (b : Matrix (chainIdx M) (chainIdx M) ℂ) :
    rmulPre P y (tof P M b) = tof P K (tPush hM b * tPush hN y) := by
  show tof P (N ⊔ M) (tPush le_sup_right b * tPush le_sup_left y)
    = tof P K (tPush hM b * tPush hN y)
  have hs : N ⊔ M ≤ (N ⊔ M) ⊔ K := le_sup_left
  have hk : K ≤ (N ⊔ M) ⊔ K := le_sup_right
  rw [tof_eq_iff hs hk]
  rw [tPush_mul, tPush_mul, tPush_trans, tPush_trans, tPush_trans, tPush_trans]

/-- direita comuta com esquerda no pré-nível (associatividade da torre). -/
theorem rmulPre_comm_lmulPre {N M : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (y : Matrix (chainIdx M) (chainIdx M) ℂ) (v : TowerPre P) :
    rmulPre P y (lmulPre P x v) = lmulPre P x (rmulPre P y v) := by
  obtain ⟨B, b, rfl⟩ := exists_tof v
  have hN : N ≤ N ⊔ M ⊔ B := le_sup_left.trans le_sup_left
  have hM : M ≤ N ⊔ M ⊔ B := le_sup_right.trans le_sup_left
  have hB : B ≤ N ⊔ M ⊔ B := le_sup_right
  have hK : N ⊔ M ⊔ B ≤ N ⊔ M ⊔ B := le_rfl
  rw [lmulPre_tof_at hN hB, rmulPre_tof_at hM hK,
    rmulPre_tof_at hM hB, lmulPre_tof_at hN hK,
    tPush_self, tPush_self, mul_assoc]

/-! ## C — o bound uniforme da direita -/

/-- o menor peso do andar N (positivo; finito não-vazio). -/
def wminP (P : SiteProfile) (N : ℕ) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty (towerW P N)

theorem wminP_pos (P : SiteProfile) (N : ℕ) : 0 < wminP P N := by
  obtain ⟨k, _, hk⟩ :=
    Finset.exists_mem_eq_inf' Finset.univ_nonempty (towerW P N)
  rw [wminP, hk]
  exact towerW_pos P N k

theorem wminP_le (P : SiteProfile) (N : ℕ) (k : chainIdx N) :
    wminP P N ≤ towerW P N k := by
  unfold wminP
  exact Finset.inf'_le _ (Finset.mem_univ k)

theorem towerW_le_one (P : SiteProfile) (N : ℕ) (k : chainIdx N) :
    towerW P N k ≤ 1 := by
  have h := towerW_sum P N
  have hle : towerW P N k ≤ ∑ i, towerW P N i :=
    Finset.single_le_sum (fun i _ => le_of_lt (towerW_pos P N i))
      (Finset.mem_univ k)
  linarith

/-- [KERNEL] ★ o bound no andar de origem: ‖b·y‖²_φ ≤ (F(y)/wmin)·‖b‖²_φ. -/
theorem rmul_bound_base (P : SiteProfile) (N : ℕ)
    (y b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (tInner P N (b * y) (b * y)).re
      ≤ (frobSq y / wminP P N) * (tInner P N b b).re := by
  have hw0 := wminP_pos P N
  rw [tInner_self_eq, tInner_self_eq, Complex.ofReal_re, Complex.ofReal_re]
  set B : ℝ := ∑ l, ∑ j, Complex.normSq (b j l) with hB
  -- passo 1: CS por entrada + w_k ≤ 1
  have h1 : (∑ k, towerW P N k * ∑ j, Complex.normSq ((b * y) j k))
      ≤ ∑ k, (∑ l, Complex.normSq (y l k)) * B := by
    apply Finset.sum_le_sum
    intro k _
    have hjk : (∑ j, Complex.normSq ((b * y) j k))
        ≤ ∑ j, (∑ l, Complex.normSq (b j l))
            * (∑ l, Complex.normSq (y l k)) := by
      apply Finset.sum_le_sum
      intro j _
      rw [show (b * y) j k = ∑ l, b j l * y l k from Matrix.mul_apply]
      exact normSq_sum_mul_le _ _
    have hk1 : towerW P N k ≤ 1 := towerW_le_one P N k
    have hknn : 0 ≤ towerW P N k := le_of_lt (towerW_pos P N k)
    have hnn2 : 0 ≤ (∑ l, Complex.normSq (y l k))
        * ∑ j, ∑ l, Complex.normSq (b j l) := by
      apply mul_nonneg
      · exact Finset.sum_nonneg (fun l _ => Complex.normSq_nonneg _)
      · apply Finset.sum_nonneg
        intro j _
        exact Finset.sum_nonneg (fun l _ => Complex.normSq_nonneg _)
    calc towerW P N k * ∑ j, Complex.normSq ((b * y) j k)
        ≤ towerW P N k * ∑ j, (∑ l, Complex.normSq (b j l))
            * (∑ l, Complex.normSq (y l k)) :=
          mul_le_mul_of_nonneg_left hjk hknn
      _ = towerW P N k * ((∑ l, Complex.normSq (y l k))
            * ∑ j, ∑ l, Complex.normSq (b j l)) := by
          rw [← Finset.sum_mul]
          ring
      _ ≤ 1 * ((∑ l, Complex.normSq (y l k))
            * ∑ j, ∑ l, Complex.normSq (b j l)) :=
          mul_le_mul_of_nonneg_right hk1 hnn2
      _ = (∑ l, Complex.normSq (y l k)) * B := by
          rw [one_mul, hB, Finset.sum_comm]
  -- passo 2: Σ_k c_k = frobSq y
  have h2 : (∑ k, (∑ l, Complex.normSq (y l k)) * B) = frobSq y * B := by
    rw [← Finset.sum_mul]
    congr 1
    rw [frobSq, Finset.sum_comm]
  -- passo 3: B ≤ (1/wmin)·‖b‖²_φ
  have h3 : B ≤ (1 / wminP P N)
      * ∑ l, towerW P N l * ∑ j, Complex.normSq (b j l) := by
    rw [hB, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro l _
    have hnn : 0 ≤ ∑ j, Complex.normSq (b j l) :=
      Finset.sum_nonneg (fun j _ => Complex.normSq_nonneg _)
    have hww : 1 ≤ (1 / wminP P N) * towerW P N l := by
      rw [div_mul_eq_mul_div, one_mul, le_div_iff₀ hw0]
      simpa using wminP_le P N l
    calc (∑ j, Complex.normSq (b j l))
        = 1 * ∑ j, Complex.normSq (b j l) := (one_mul _).symm
      _ ≤ ((1 / wminP P N) * towerW P N l) * ∑ j, Complex.normSq (b j l) :=
          mul_le_mul_of_nonneg_right hww hnn
      _ = (1 / wminP P N)
            * (towerW P N l * ∑ j, Complex.normSq (b j l)) := by ring
  -- fecho
  have hFnn : 0 ≤ frobSq y := frobSq_nonneg y
  calc (∑ k, towerW P N k * ∑ j, Complex.normSq ((b * y) j k))
      ≤ frobSq y * B := le_trans h1 (le_of_eq h2)
    _ ≤ frobSq y * ((1 / wminP P N)
          * ∑ l, towerW P N l * ∑ j, Complex.normSq (b j l)) :=
        mul_le_mul_of_nonneg_left h3 hFnn
    _ = (frobSq y / wminP P N)
          * ∑ l, towerW P N l * ∑ j, Complex.normSq (b j l) := by
        ring

/-- [KERNEL] ★ o fatiamento espelhado: a fatia da ação DIREITA de y⊗1 é a
    ação direita de y na fatia. -/
theorem cSlice_mul_towerStep {M : ℕ} (t s : Fin 2)
    (y : Matrix (chainIdx M) (chainIdx M) ℂ)
    (c : Matrix (chainIdx (M + 1)) (chainIdx (M + 1)) ℂ) :
    cSlice t s (c * towerStep y) = cSlice t s c * y := by
  ext j k
  rw [cSlice_apply, Matrix.mul_apply, Matrix.mul_apply]
  rw [Fintype.sum_prod_type]
  refine Finset.sum_congr rfl fun i _ => ?_
  have hstep : ∀ u : Fin 2, towerStep y (i, u) (k, s)
      = y i k * (if u = s then 1 else 0) := by
    intro u
    unfold towerStep
    rw [kroneckerMap_apply, Matrix.one_apply]
  have hterm : ∀ u : Fin 2, c (j, t) (i, u) * towerStep y (i, u) (k, s)
      = if u = s then c (j, t) (i, u) * y i k else 0 := by
    intro u
    rw [hstep u]
    by_cases hu : u = s
    · rw [if_pos hu, if_pos hu, mul_one]
    · rw [if_neg hu, if_neg hu, mul_zero, mul_zero]
  rw [Finset.sum_congr rfl (fun u _ => hterm u),
    Finset.sum_ite_eq' Finset.univ s (fun u => c (j, t) (i, u) * y i k),
    if_pos (Finset.mem_univ s), cSlice_apply]

/-- [KERNEL] ★★ O BOUND UNIFORME da direita: a constante do andar de ORIGEM
    não cresce ao subir (indução de fatiamento espelhada). -/
theorem rmul_bound_push (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    ∀ {M : ℕ} (h : N ≤ M) (c : Matrix (chainIdx M) (chainIdx M) ℂ),
      (tInner P M (c * tPush h y) (c * tPush h y)).re
        ≤ (frobSq y / wminP P N) * (tInner P M c c).re := by
  intro M h
  induction M, h using Nat.le_induction with
  | base =>
      intro c
      rw [tPush_self]
      exact rmul_bound_base P N y c
  | succ M hM ih =>
      intro c
      rw [tPush_succ hM (hM.trans (Nat.le_succ M))]
      rw [tInner_self_slice P (c * towerStep (tPush hM y)),
        tInner_self_slice P c]
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro s _
      rw [Finset.mul_sum]
      apply Finset.sum_le_sum
      intro t _
      rw [cSlice_mul_towerStep]
      have hσ : 0 ≤ siteW (P.w (M + 1)) s :=
        le_of_lt (siteW_pos (P.pos (M + 1)) (P.lt_one (M + 1)) s)
      calc siteW (P.w (M + 1)) s
            * (tInner P M (cSlice t s c * tPush hM y)
                (cSlice t s c * tPush hM y)).re
          ≤ siteW (P.w (M + 1)) s * ((frobSq y / wminP P N)
              * (tInner P M (cSlice t s c) (cSlice t s c)).re) :=
            mul_le_mul_of_nonneg_left (ih (cSlice t s c)) hσ
        _ = (frobSq y / wminP P N) * (siteW (P.w (M + 1)) s
              * (tInner P M (cSlice t s c) (cSlice t s c)).re) := by ring

/-! ## D — a direita como operador de B(H_φ) -/

/-- a direita é LINEAR no colimite. -/
def rmulLin (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P →ₗ[ℂ] TowerPre P where
  toFun := rmulPre P y
  map_add' := by
    intro v w
    obtain ⟨A, a, rfl⟩ := exists_tof v
    obtain ⟨B, b, rfl⟩ := exists_tof w
    have hA : A ≤ A ⊔ B := le_sup_left
    have hB : B ≤ A ⊔ B := le_sup_right
    have hN : N ≤ N ⊔ (A ⊔ B) := le_sup_left
    have hAB : A ⊔ B ≤ N ⊔ (A ⊔ B) := le_sup_right
    rw [tof_add_at hA hB, rmulPre_tof_at hN hAB,
      rmulPre_tof_at hN (hA.trans hAB), rmulPre_tof_at hN (hB.trans hAB),
      tof_add_at (le_refl (N ⊔ (A ⊔ B))) (le_refl (N ⊔ (A ⊔ B))),
      tPush_self, tPush_self, tPush_add, add_mul, tPush_trans, tPush_trans]
  map_smul' := by
    intro cc v
    obtain ⟨A, a, rfl⟩ := exists_tof v
    have hN : N ≤ N ⊔ A := le_sup_left
    have hA : A ≤ N ⊔ A := le_sup_right
    rw [RingHom.id_apply, tof_smul, rmulPre_tof_at hN hA,
      rmulPre_tof_at hN hA, tof_smul, tPush_smul, smul_mul_assoc]

/-- [KERNEL] ★★ A CONTINUIDADE da direita no colimite inteiro. -/
theorem rmulPre_norm_le {N : ℕ} (y : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) :
    ‖rmulPre P y v‖ ≤ Real.sqrt (frobSq y / wminP P N) * ‖v‖ := by
  obtain ⟨M, b, rfl⟩ := exists_tof v
  have hN : N ≤ N ⊔ M := le_sup_left
  have hM : M ≤ N ⊔ M := le_sup_right
  set K := N ⊔ M
  set b' := tPush hM b with hb'
  have hv : tof P M b = tof P K b' := (tof_tPush hM b).symm
  rw [hv, rmulPre_tof_at hN (le_refl K), tPush_self]
  have hsq : ‖tof P K (b' * tPush hN y)‖ ^ 2
      ≤ (frobSq y / wminP P N) * ‖tof P K b'‖ ^ 2 := by
    rw [norm_tof_sq, norm_tof_sq]
    exact rmul_bound_push P y hN b'
  have h1 : ‖tof P K (b' * tPush hN y)‖
      = Real.sqrt (‖tof P K (b' * tPush hN y)‖ ^ 2) :=
    (Real.sqrt_sq (norm_nonneg _)).symm
  rw [h1]
  have hCnn : (0 : ℝ) ≤ frobSq y / wminP P N :=
    div_nonneg (frobSq_nonneg y) (le_of_lt (wminP_pos P N))
  calc Real.sqrt (‖tof P K (b' * tPush hN y)‖ ^ 2)
      ≤ Real.sqrt ((frobSq y / wminP P N) * ‖tof P K b'‖ ^ 2) :=
        Real.sqrt_le_sqrt hsq
    _ = Real.sqrt (frobSq y / wminP P N) * Real.sqrt (‖tof P K b'‖ ^ 2) :=
        Real.sqrt_mul hCnn _
    _ = Real.sqrt (frobSq y / wminP P N) * ‖tof P K b'‖ := by
        rw [Real.sqrt_sq (norm_nonneg _)]

/-- a direita como operador CONTÍNUO no pré-Hilbert. -/
def rmulCLM (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerPre P →L[ℂ] TowerPre P :=
  LinearMap.mkContinuous (rmulLin P y)
    (Real.sqrt (frobSq y / wminP P N)) (fun v => rmulPre_norm_le y v)

/-- ★★ r(y): a direita em B(H_φ), por extensão ao completamento. -/
def rTowerPi (P : SiteProfile) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  (rmulCLM P y).completion

theorem rTowerPi_coe {N : ℕ} (y : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : TowerPre P) :
    rTowerPi P y (v : TowerHilbert P)
      = ((rmulPre P y v : TowerPre P) : TowerHilbert P) :=
  ContinuousLinearMap.completion_apply_coe _ _

/-- [KERNEL] ★ r(y)Ω = [y]: a órbita direita do Nome é a torre. -/
theorem rTowerPi_omega (N : ℕ) (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P y (hOmega P) = ((tof P N y : TowerPre P) : TowerHilbert P) := by
  unfold hOmega
  rw [show towerOmega P = tof P 0 1 from rfl, rTowerPi_coe]
  congr 1
  rw [rmulPre_tof_at (le_refl N) (Nat.zero_le N), tPush_self, tPush_one,
    one_mul]

/-- [KERNEL] ★★ direita comuta com esquerda em B(H_φ). -/
theorem towerPi_comm_rTowerPi {N M : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ)
    (y : Matrix (chainIdx M) (chainIdx M) ℂ) :
    towerPi P x * rTowerPi P y = rTowerPi P y * towerPi P x := by
  ext c
  rw [ContinuousLinearMap.mul_apply, ContinuousLinearMap.mul_apply]
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih c =>
      rw [rTowerPi_coe, towerPi_coe, towerPi_coe, rTowerPi_coe,
        rmulPre_comm_lmulPre]

/-- o empurrão comuta com a torção modular. -/
theorem tPush_modTwist (P : SiteProfile) {N M : ℕ} (h : N ≤ M)
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tPush h (modTwist P y) = modTwist P (tPush h y) := by
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hM ih =>
      rw [tPush_succ hM (hM.trans (Nat.le_succ M)),
        tPush_succ hM (hM.trans (Nat.le_succ M)), ih]
      ext jk kl
      obtain ⟨j, u⟩ := jk
      obtain ⟨k, v⟩ := kl
      have hL : towerStep (modTwist P (tPush hM y)) (j, u) (k, v)
          = modTwist P (tPush hM y) j k
            * (1 : Matrix (Fin 2) (Fin 2) ℂ) u v := by
        unfold towerStep
        rw [kroneckerMap_apply]
      have hS : towerStep (tPush hM y) (k, v) (j, u)
          = tPush hM y k j * (1 : Matrix (Fin 2) (Fin 2) ℂ) v u := by
        unfold towerStep
        rw [kroneckerMap_apply]
      rw [hL, modTwist_apply, modTwist_apply, hS]
      rw [show towerW P (M + 1) (j, u)
          = towerW P M j * siteW (P.w (M + 1)) u from rfl,
        show towerW P (M + 1) (k, v)
          = towerW P M k * siteW (P.w (M + 1)) v from rfl]
      by_cases huv : u = v
      · subst huv
        simp only [Matrix.one_apply_eq, mul_one]
        have hs0 : ((siteW (P.w (M + 1)) u : ℝ) : ℂ) ≠ 0 :=
          Complex.ofReal_ne_zero.mpr
            (ne_of_gt (siteW_pos (P.pos (M + 1)) (P.lt_one (M + 1)) u))
        have hk0 : ((towerW P M k : ℝ) : ℂ) ≠ 0 :=
          Complex.ofReal_ne_zero.mpr (ne_of_gt (towerW_pos P M k))
        push_cast [mul_inv]
        field_simp
        try ring
      · have h1 : (1 : Matrix (Fin 2) (Fin 2) ℂ) u v = 0 := by
          rw [Matrix.one_apply, if_neg huv]
        have h2 : (1 : Matrix (Fin 2) (Fin 2) ℂ) v u = 0 := by
          rw [Matrix.one_apply, if_neg (fun h' => huv h'.symm)]
        rw [h1, h2, mul_zero, mul_zero, star_zero, mul_zero, zero_mul]

/-- [KERNEL] ★★ O ADJUNTO MODULAR: adjoint(r_y) = r_{ρy†ρ⁻¹} — via KMS. -/
theorem rTowerPi_star (N : ℕ) (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P (modTwist P y)
      = ContinuousLinearMap.adjoint (rTowerPi P y) := by
  refine ((ContinuousLinearMap.eq_adjoint_iff _ _).mpr ?_)
  intro u v
  induction u, v using Completion.induction_on₂ with
  | hp => apply isClosed_eq <;> fun_prop
  | ih u v =>
      rw [rTowerPi_coe, rTowerPi_coe, Completion.inner_coe,
        Completion.inner_coe]
      obtain ⟨A, a, rfl⟩ := exists_tof u
      obtain ⟨B, b, rfl⟩ := exists_tof v
      have hN : N ≤ N ⊔ A ⊔ B := le_sup_left.trans le_sup_left
      have hA : A ≤ N ⊔ A ⊔ B := le_sup_right.trans le_sup_left
      have hB : B ≤ N ⊔ A ⊔ B := le_sup_right
      show innerPre P (rmulPre P (modTwist P y) (tof P A a)) (tof P B b)
        = innerPre P (tof P A a) (rmulPre P y (tof P B b))
      rw [rmulPre_tof_at hN hA, rmulPre_tof_at hN hB,
        innerPre_tof_at (le_refl (N ⊔ A ⊔ B)) hB, tPush_self,
        innerPre_tof_at hA (le_refl (N ⊔ A ⊔ B)), tPush_self,
        tPush_modTwist]
      unfold tInner
      rw [Matrix.conjTranspose_mul]
      have hassoc1 : (modTwist P (tPush hN y))ᴴ * (tPush hA a)ᴴ * tPush hB b
          = (modTwist P (tPush hN y))ᴴ * ((tPush hA a)ᴴ * tPush hB b) := by
        noncomm_ring
      rw [hassoc1,
        tState_kms P (N ⊔ A ⊔ B) ((modTwist P (tPush hN y))ᴴ)
          ((tPush hA a)ᴴ * tPush hB b),
        rho_conj_modTwist_star P (tPush hN y)]
      congr 1
      noncomm_ring

/-- [KERNEL] ★★★ r(y) ∈ π(torre)′: comuta com toda esquerda e sua estrela
    é OUTRA direita (o adjunto modular) — o comutante é habitado. -/
theorem rTowerPi_mem_commutant {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P y ∈ StarSubalgebra.centralizer ℂ (towerImage P) := by
  rw [StarSubalgebra.mem_centralizer_iff]
  rintro T ⟨M, x, rfl⟩
  constructor
  · exact towerPi_comm_rTowerPi x y
  · rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star]
    exact towerPi_comm_rTowerPi xᴴ y

/-- [KERNEL] ★★ TODO elemento do fator comuta com toda direita (M_TGL é o
    duplo centralizador; a direita vive no primeiro). -/
theorem factor_comm_rTowerPi {A : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    A * rTowerPi P y = rTowerPi P y * A := by
  have hA' : A ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
          Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := hA
  rw [StarSubalgebra.mem_centralizer_iff] at hA'
  have h := hA' (rTowerPi P y)
    (SetLike.mem_coe.mpr (rTowerPi_mem_commutant y))
  exact h.1.symm

/-- [KERNEL] ★★★ O SEPARADOR: A ∈ M_TGL e AΩ = 0 ⟹ A = 0 — o vetor do
    Nome é cíclico (pedra 86) E separador para o fator: Reeh–Schlieder. -/
theorem factor_omega_separating
    {A : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hA : A ∈ theFactorObject P) (h0 : A (hOmega P) = 0) : A = 0 := by
  have hker : ∀ (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      A ((tof P N a : TowerPre P) : TowerHilbert P) = 0 := by
    intro N a
    have hc := factor_comm_rTowerPi hA a
    have h1 : A (rTowerPi P a (hOmega P))
        = rTowerPi P a (A (hOmega P)) := by
      have h2 := congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P =>
        T (hOmega P)) hc
      simpa [ContinuousLinearMap.mul_apply] using h2
    rw [rTowerPi_omega] at h1
    rw [h1, h0, map_zero]
  ext c
  rw [ContinuousLinearMap.zero_apply]
  induction c using Completion.induction_on with
  | hp => apply isClosed_eq <;> fun_prop
  | ih v =>
      obtain ⟨N, a, rfl⟩ := exists_tof v
      exact hker N a

end

end TGLExt
