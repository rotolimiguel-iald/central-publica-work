-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_045 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ChainSiteOperators
import TGLExt.CentralizerLocal
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Algebra.BigOperators.Fin

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Horizons045

open TGLExt Matrix
open scoped Kronecker
noncomputable section

/-- Level N contains exactly N+1 binary sites, in their original order. -/
def chainWord : (N : ℕ) → chainIdx N → (Fin (N+1) → Fin 2)
  | 0, x => fun _ => x
  | N+1, x => Fin.snoc (chainWord N x.1) x.2

def chainUnword : (N : ℕ) → (Fin (N+1) → Fin 2) → chainIdx N
  | 0, f => f 0
  | N+1, f => (chainUnword N (Fin.init f), f (Fin.last (N+1)))

theorem chain_unword_word (N : ℕ) (x : chainIdx N) :
    chainUnword N (chainWord N x) = x := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rcases x with ⟨x,y⟩
    simp only [chainWord, chainUnword, Fin.init_snoc, Fin.snoc_last, ih]

theorem chain_word_unword (N : ℕ) (f : Fin (N+1) → Fin 2) :
    chainWord N (chainUnword N f) = f := by
  induction N with
  | zero =>
    funext i
    have hi : i = 0 := by apply Fin.ext; omega
    subst i
    rfl
  | succ N ih =>
    simp only [chainWord, chainUnword, ih, Fin.snoc_init_self]

def chainWordEquiv (N : ℕ) : chainIdx N ≃ (Fin (N+1) → Fin 2) where
  toFun := chainWord N
  invFun := chainUnword N
  left_inv := chain_unword_word N
  right_inv := chain_word_unword N

theorem chain_word_injective (N : ℕ) : Function.Injective (chainWord N) :=
  (chainWordEquiv N).injective

/-- The row permutation is contravariant; its permutation matrix acts covariantly. -/
def siteIndexPermutation (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    Equiv.Perm (chainIdx N) where
  toFun x := chainUnword N (fun n => chainWord N x (σ n))
  invFun x := chainUnword N (fun n => chainWord N x (σ.symm n))
  left_inv x := by simp only [chain_word_unword, Equiv.apply_symm_apply,
    chain_unword_word]
  right_inv x := by simp only [chain_word_unword, Equiv.symm_apply_apply,
    chain_unword_word]

theorem site_index_permutation_word (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (x : chainIdx N) (n : Fin (N+1)) :
    chainWord N (siteIndexPermutation N σ x) n = chainWord N x (σ n) := by
  change chainWord N (chainUnword N _) n = _
  rw [chain_word_unword]

theorem site_index_permutation_one (N : ℕ) :
    siteIndexPermutation N 1 = 1 := by
  ext x
  apply chain_word_injective N
  funext n
  simp only [site_index_permutation_word, Equiv.Perm.one_apply]

theorem site_index_permutation_mul (N : ℕ) (σ τ : Equiv.Perm (Fin (N+1))) :
    siteIndexPermutation N (σ * τ) =
      siteIndexPermutation N τ * siteIndexPermutation N σ := by
  ext x
  apply chain_word_injective N
  funext n
  simp only [Equiv.Perm.mul_apply, site_index_permutation_word]

def finiteSiteMatrix (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  (siteIndexPermutation N σ).permMatrix ℂ

theorem finite_site_matrix_one (N : ℕ) : finiteSiteMatrix N 1 = 1 := by
  simp only [finiteSiteMatrix, site_index_permutation_one, Matrix.permMatrix_one]

theorem finite_site_matrix_mul (N : ℕ) (σ τ : Equiv.Perm (Fin (N+1))) :
    finiteSiteMatrix N (σ * τ) = finiteSiteMatrix N σ * finiteSiteMatrix N τ := by
  simp only [finiteSiteMatrix, site_index_permutation_mul, Matrix.permMatrix_mul]

theorem finite_site_matrix_unitary_left (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    (finiteSiteMatrix N σ)ᴴ * finiteSiteMatrix N σ = 1 := by
  unfold finiteSiteMatrix
  rw [Matrix.conjTranspose_permMatrix, ← Matrix.permMatrix_mul, mul_inv_cancel,
    Matrix.permMatrix_one]

theorem finite_site_matrix_unitary_right (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteMatrix N σ * (finiteSiteMatrix N σ)ᴴ = 1 := by
  unfold finiteSiteMatrix
  rw [Matrix.conjTranspose_permMatrix, ← Matrix.permMatrix_mul, inv_mul_cancel,
    Matrix.permMatrix_one]

theorem finite_site_matrix_inverse (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    finiteSiteMatrix N σ⁻¹ = (finiteSiteMatrix N σ)ᴴ := by
  have h := finite_site_matrix_mul N σ⁻¹ σ
  rw [inv_mul_cancel, finite_site_matrix_one] at h
  calc
    finiteSiteMatrix N σ⁻¹ =
        finiteSiteMatrix N σ⁻¹ * (finiteSiteMatrix N σ *
          (finiteSiteMatrix N σ)ᴴ) := by
            rw [finite_site_matrix_unitary_right, mul_one]
    _ = (finiteSiteMatrix N σ⁻¹ * finiteSiteMatrix N σ) *
        (finiteSiteMatrix N σ)ᴴ := (mul_assoc _ _ _).symm
    _ = (finiteSiteMatrix N σ)ᴴ := by rw [← h, one_mul]

theorem finite_site_matrix_conjugation (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (A : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    (finiteSiteMatrix N σ * A * (finiteSiteMatrix N σ)ᴴ) i j =
      A (siteIndexPermutation N σ i) (siteIndexPermutation N σ j) := by
  unfold finiteSiteMatrix
  rw [Matrix.conjTranspose_permMatrix]
  simp only [Equiv.Perm.permMatrix, PEquiv.toMatrix_toPEquiv_mul,
    PEquiv.mul_toMatrix_toPEquiv]
  rfl

/-- Entries of the literal tensor of all N+1 site matrices. -/
def siteTensorMatrix (N : ℕ)
    (A : Fin (N+1) → Matrix (Fin 2) (Fin 2) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  fun i j => ∏ n, A n (chainWord N i n) (chainWord N j n)

theorem site_tensor_matrix_succ (N : ℕ)
    (A : Fin (N+2) → Matrix (Fin 2) (Fin 2) ℂ) :
    siteTensorMatrix (N+1) A =
      siteTensorMatrix N (fun n => A n.castSucc) ⊗ₖ A (Fin.last (N+1)) := by
  ext i j
  simp only [siteTensorMatrix, Fin.prod_univ_castSucc, chainWord,
    Fin.snoc_castSucc, Fin.snoc_last, Matrix.kroneckerMap_apply]

theorem site_tensor_matrix_one (N : ℕ) :
    siteTensorMatrix N (fun _ => 1) = 1 := by
  induction N with
  | zero =>
    ext i j
    change (∏ _ : Fin 1, (1 : Matrix (Fin 2) (Fin 2) ℂ) i j) =
      (1 : Matrix (Fin 2) (Fin 2) ℂ) i j
    simp
  | succ N ih =>
    rw [site_tensor_matrix_succ, ih, Matrix.one_kronecker_one]

def singleSiteTensor (N : ℕ) (n : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  siteTensorMatrix N (fun k => if k = n then a else 1)

theorem single_site_tensor_last (N : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    singleSiteTensor (N+1) (Fin.last (N+1)) a = lastSiteMatrix (N+1) a := by
  unfold singleSiteTensor
  rw [site_tensor_matrix_succ]
  have h : (fun n : Fin (N+1) =>
      if n.castSucc = Fin.last (N+1) then a else 1) = fun _ => 1 := by
    funext n
    simp
  rw [h, site_tensor_matrix_one]
  simp only [ite_true, lastSiteMatrix]

theorem single_site_tensor_castSucc (N : ℕ) (n : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    singleSiteTensor (N+1) n.castSucc a = towerStep (singleSiteTensor N n a) := by
  unfold singleSiteTensor
  rw [site_tensor_matrix_succ]
  have h : (fun k : Fin (N+1) =>
      if k.castSucc = n.castSucc then a else 1) =
      (fun k => if k = n then a else 1) := by
    funext k
    simp only [Fin.castSucc_inj]
  rw [h]
  have hlast : Fin.last (N+1) ≠ n.castSucc := by
    intro he
    have hv := congrArg Fin.val he
    simp only [Fin.val_last, Fin.val_castSucc] at hv
    omega
  simp only [hlast, ite_false, towerStep]

theorem single_site_tensor_pi (P : SiteProfile) (N : ℕ) (n : Fin (N+1))
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    towerPi P (singleSiteTensor N n a) = siteOperator P n.val a := by
  induction N with
  | zero =>
    have hn : n = 0 := by apply Fin.ext; omega
    subst n
    change towerPi P (singleSiteTensor 0 0 a) = towerPi P (lastSiteMatrix 0 a)
    congr 1
    ext i j
    simp [singleSiteTensor, siteTensorMatrix, chainWord, lastSiteMatrix]
  | succ N ih =>
    induction n using Fin.lastCases with
    | last => rw [single_site_tensor_last]; rfl
    | cast n =>
      rw [single_site_tensor_castSucc, towerPi_step, ih]
      rfl

theorem finite_site_matrix_tensor_action (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (A : Fin (N+1) → Matrix (Fin 2) (Fin 2) ℂ) :
    finiteSiteMatrix N σ * siteTensorMatrix N A * (finiteSiteMatrix N σ)ᴴ =
      siteTensorMatrix N (fun n => A (σ.symm n)) := by
  ext i j
  rw [finite_site_matrix_conjugation]
  simp only [siteTensorMatrix, site_index_permutation_word]
  apply Fintype.prod_equiv σ
  intro n
  simp only [Equiv.symm_apply_apply]

theorem finite_site_matrix_site_action (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (n : Fin (N+1)) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    finiteSiteMatrix N σ * singleSiteTensor N n a * (finiteSiteMatrix N σ)ᴴ =
      singleSiteTensor N (σ n) a := by
  unfold singleSiteTensor
  rw [finite_site_matrix_tensor_action]
  congr 1
  funext k
  have h : σ.symm k = n ↔ k = σ n := by
    constructor
    · intro hk
      simpa only [Equiv.apply_symm_apply] using congrArg σ hk
    · intro hk
      rw [hk, Equiv.symm_apply_apply]
  simp only [h]

theorem tower_weight_word_product (P : SiteProfile) (N : ℕ) (i : chainIdx N) :
    towerW P N i = ∏ n : Fin (N+1), siteW (P.w n.val) (chainWord N i n) := by
  induction N with
  | zero => simp [towerW, chainWord]
  | succ N ih =>
    rw [Fin.prod_univ_castSucc]
    simp only [chainWord, Fin.snoc_castSucc, Fin.snoc_last, Fin.val_castSucc,
      Fin.val_last, towerW, ih]

theorem stationary_weight_permutation (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (i : chainIdx N) :
    towerW P N (siteIndexPermutation N σ i) = towerW P N i := by
  simp only [tower_weight_word_product, site_index_permutation_word, hp]
  exact Equiv.prod_comp σ (fun n => siteW p (chainWord N i n))

theorem finite_site_matrix_entry (N : ℕ) (σ : Equiv.Perm (Fin (N+1)))
    (i j : chainIdx N) :
    finiteSiteMatrix N σ i j = if j = siteIndexPermutation N σ i then 1 else 0 := by
  simp [finiteSiteMatrix, Equiv.Perm.permMatrix, PEquiv.toMatrix_apply,
    Equiv.toPEquiv_apply, eq_comm]

theorem stationary_density_commutes (P : SiteProfile) (p : ℝ)
    (hp : ∀ n, P.w n = p) (N : ℕ) (σ : Equiv.Perm (Fin (N+1))) :
    Commute (rhoD (towerW P N)) (finiteSiteMatrix N σ) := by
  change rhoD (towerW P N) * finiteSiteMatrix N σ =
    finiteSiteMatrix N σ * rhoD (towerW P N)
  ext i j
  simp only [rhoD, Matrix.diagonal_mul, Matrix.mul_diagonal,
    finite_site_matrix_entry]
  by_cases h : j = siteIndexPermutation N σ i
  · subst j
    rw [stationary_weight_permutation P p hp]
    simp
  · simp [h]

#print axioms chainWord
#print axioms chainUnword
#print axioms chain_unword_word
#print axioms chain_word_unword
#print axioms chainWordEquiv
#print axioms chain_word_injective
#print axioms siteIndexPermutation
#print axioms site_index_permutation_word
#print axioms site_index_permutation_one
#print axioms site_index_permutation_mul
#print axioms finiteSiteMatrix
#print axioms finite_site_matrix_one
#print axioms finite_site_matrix_mul
#print axioms finite_site_matrix_unitary_left
#print axioms finite_site_matrix_unitary_right
#print axioms finite_site_matrix_inverse
#print axioms finite_site_matrix_conjugation
#print axioms siteTensorMatrix
#print axioms site_tensor_matrix_succ
#print axioms site_tensor_matrix_one
#print axioms singleSiteTensor
#print axioms single_site_tensor_last
#print axioms single_site_tensor_castSucc
#print axioms single_site_tensor_pi
#print axioms finite_site_matrix_tensor_action
#print axioms finite_site_matrix_site_action
#print axioms tower_weight_word_product
#print axioms stationary_weight_permutation
#print axioms finite_site_matrix_entry
#print axioms stationary_density_commutes

end
end ChatgptAudit.Horizons045
