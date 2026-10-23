import TGLExt.NumberSelfAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A REDE DE CAUDAS: fibras ∞-DIMENSIONAIS — o último campo do Strong
  [TGLExt — v106, o incremento 25 do programa SemifiniteAnalysis]

O v101 habitou PhysicalNetData com fibras finito-dim (a honestidade
declarada); o tipo FORTE exige `core_infinite`. Esta pedra constrói a
rede que o satisfaz: as CAUDAS H_n = {x ∈ ℓ² | x_k = 0 ∀ k < n}, com
Region = ℕ e a ordem REVERSA (leR a b := b ≤ a):

* cada cauda é FECHADA (interseção de kernels de funcionais-coordenada
  contínuos) ⟹ COMPLETA; e ∞-DIMENSIONAL (contém e_k para k ≥ n);
* as inclusões são as canônicas (isométricas); a de 1→0 NÃO é
  sobrejetiva (e₀ fora da imagem) — isotonia GENUÍNA;
* os locks são as restrições de T = 1−P₀ (T preserva as caudas);
  fluxo genuíno exp(isT_n) por fibra; grupo externo Bool pelo flip;
* ★★ `theTailNet : PhysicalNetData ...` + ★★ `tailSub_not_finiteDimensional`
  — o PRIMEIRO núcleo com fibra ∞-dim: `core_infinite` TEM testemunha.

HONESTIDADE: a ação nas REGIÕES segue trivial (a geometria é o nível
da testemunha v2, não do Strong); III₁ segue no v2.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — as caudas -/

/-- a cauda n: as sequências nulas abaixo de n. -/
def tailSub (n : ℕ) : Submodule ℂ ellTwo where
  carrier := {x | ∀ k < n, x k = 0}
  zero_mem' := by
    intro k _
    show (0 : ellTwo) k = 0
    rw [lp.coeFn_zero]
    rfl
  add_mem' := by
    intro a b ha hb k hk
    show (a + b) k = 0
    rw [lp.coeFn_add, Pi.add_apply, ha k hk, hb k hk, add_zero]
  smul_mem' := by
    intro c x hx k hk
    show (c • x) k = 0
    rw [lp.coeFn_smul, Pi.smul_apply, hx k hk, smul_zero]

theorem mem_tailSub_iff {n : ℕ} {x : ellTwo} :
    x ∈ tailSub n ↔ ∀ k < n, x k = 0 := Iff.rfl

/-- a coordenada é o inner com a inscrição (a leitura contínua). -/
theorem coord_eq_inner (k : ℕ) (x : ellTwo) :
    inner ℂ (inscriptions k) x = x k := by
  rw [lp.inner_eq_tsum]
  have hsupp : ∀ j ≠ k, inner ℂ ((inscriptions k) j) (x j) = 0 := by
    intro j hj
    rw [inscriptions_apply, if_neg hj]
    simp
  rw [tsum_eq_single k hsupp, inscriptions_apply, if_pos rfl,
    RCLike.inner_apply, map_one, mul_one]

theorem tailSub_isClosed (n : ℕ) : IsClosed (tailSub n : Set ellTwo) := by
  have h : (tailSub n : Set ellTwo)
      = ⋂ k ∈ Finset.range n, (innerSL ℂ (inscriptions k)) ⁻¹' {0} := by
    ext x
    simp only [Set.mem_iInter, Set.mem_preimage, Set.mem_singleton_iff,
      Finset.mem_range, SetLike.mem_coe, mem_tailSub_iff]
    constructor
    · intro hx k hk
      show inner ℂ (inscriptions k) x = 0
      rw [coord_eq_inner]
      exact hx k hk
    · intro hx k hk
      have := hx k hk
      rwa [show (innerSL ℂ (inscriptions k)) x = inner ℂ (inscriptions k) x
        from rfl, coord_eq_inner] at this
  rw [h]
  exact isClosed_biInter fun k _ =>
    (isClosed_singleton).preimage (innerSL ℂ (inscriptions k)).continuous

instance tailSub_complete (n : ℕ) : CompleteSpace (tailSub n) :=
  (tailSub_isClosed n).completeSpace_coe

/-- e_m mora na cauda n para m ≥ n. -/
theorem inscription_mem_tailSub {n m : ℕ} (h : n ≤ m) :
    inscriptions m ∈ tailSub n := by
  intro k hk
  rw [inscriptions_apply, if_neg]
  omega

/-- [KERNEL] ★★ cada cauda é GENUINAMENTE ∞-dim (contém a família
    ortonormal e_{n+m}). -/
theorem tailSub_not_finiteDimensional (n : ℕ) :
    ¬ FiniteDimensional ℂ (tailSub n) := by
  intro hfd
  set d := Module.finrank ℂ (tailSub n) with hd
  have hli0 : LinearIndependent ℂ
      (fun m : ℕ => inscriptions (n + m)) :=
    inscriptions_orthonormal.linearIndependent.comp _
      (fun a b hab => by omega)
  have hfam : ∀ m : ℕ, inscriptions (n + m) ∈ tailSub n :=
    fun m => inscription_mem_tailSub (Nat.le_add_right n m)
  have hli : LinearIndependent ℂ
      (fun m : ℕ => (⟨inscriptions (n + m), hfam m⟩ : tailSub n)) := by
    have hcomp : (fun m : ℕ => ((⟨inscriptions (n + m), hfam m⟩ :
        tailSub n) : ellTwo)) = fun m => inscriptions (n + m) := rfl
    exact (hli0.of_comp (tailSub n).subtype)
  have hli2 : LinearIndependent ℂ
      ((fun m : ℕ => (⟨inscriptions (n + m), hfam m⟩ : tailSub n))
        ∘ (fun i : Fin (d + 1) => (i : ℕ))) :=
    hli.comp _ Fin.val_injective
  have hcard := hli2.fintype_card_le_finrank
  rw [Fintype.card_fin] at hcard
  omega

/-! ## B — inclusões (ordem REVERSA: leR a b := b ≤ a) -/

theorem tail_mono {a b : ℕ} (h : b ≤ a) : tailSub a ≤ tailSub b :=
  fun _ hx k hk => hx k (lt_of_lt_of_le hk h)

/-- a inclusão isométrica cauda a → cauda b (b ≤ a). -/
def tailIncl {a b : ℕ} (h : b ≤ a) : (tailSub a) →ₗᵢ[ℂ] (tailSub b) :=
  ⟨Submodule.inclusion (tail_mono h), fun _ => rfl⟩

/-- [KERNEL] ★★ a isotonia é GENUÍNA: 1→0 NÃO é sobrejetiva (e₀ fora). -/
theorem tailIncl_not_surjective :
    ¬ Function.Surjective (tailIncl (Nat.zero_le 1)) := by
  intro hsurj
  have h0 : inscriptions 0 ∈ tailSub 0 := fun k hk => absurd hk (Nat.not_lt_zero k)
  obtain ⟨y, hy⟩ := hsurj ⟨inscriptions 0, h0⟩
  have hy' : (y : ellTwo) = inscriptions 0 := congrArg Subtype.val hy
  have hy0 : (y : ellTwo) 0 = 0 := y.2 0 Nat.one_pos
  rw [hy'] at hy0
  rw [inscriptions_apply, if_pos rfl] at hy0
  exact one_ne_zero hy0

/-! ## C — os locks restritos e o flip -/

theorem eraseFirst_mem_tail {n : ℕ} {x : ellTwo} (hx : x ∈ tailSub n) :
    eraseFirst x ∈ tailSub n := by
  intro k hk
  have hn : 0 < n := lt_of_le_of_lt (Nat.zero_le k) hk
  have hx0 : x 0 = 0 := hx 0 hn
  have hP : firstAtom.starProjection x = 0 := by
    unfold firstAtom
    rw [Submodule.starProjection_singleton ℂ]
    unfold firstInscription
    rw [coord_eq_inner, hx0]
    simp
  rw [eraseFirst_apply, hP, sub_zero]
  exact hx k hk

/-- o lock da cauda: a restrição de T = 1 − P₀. -/
def tailLock (n : ℕ) : (tailSub n) →L[ℂ] (tailSub n) :=
  { toFun := fun x => ⟨eraseFirst (x : ellTwo), eraseFirst_mem_tail x.2⟩
    map_add' := fun x y => Subtype.ext (by
      show eraseFirst ((x : ellTwo) + (y : ellTwo))
        = eraseFirst (x : ellTwo) + eraseFirst (y : ellTwo)
      exact map_add eraseFirst _ _)
    map_smul' := fun c x => Subtype.ext (by
      show eraseFirst (c • (x : ellTwo)) = c • eraseFirst (x : ellTwo)
      exact map_smul eraseFirst c _)
    cont := by
      apply Continuous.subtype_mk
      exact eraseFirst.continuous.comp continuous_subtype_val }

theorem tailLock_symmetric (n : ℕ) :
    ((tailLock n : (tailSub n) →L[ℂ] (tailSub n))
      : (tailSub n) →ₗ[ℂ] (tailSub n)).IsSymmetric := by
  intro x y
  have hsym : ((eraseFirst : ellTwo →L[ℂ] ellTwo)
      : ellTwo →ₗ[ℂ] ellTwo).IsSymmetric :=
    (ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric).mp eraseFirst_isSelfAdjoint
  exact hsym (x : ellTwo) (y : ellTwo)

theorem tailLock_selfadjoint (n : ℕ) : IsSelfAdjoint (tailLock n) :=
  (tailLock_symmetric n).isSelfAdjoint

theorem theFlip_mem_tail {n : ℕ} {x : ellTwo} (hx : x ∈ tailSub n) :
    theFlip x ∈ tailSub n := by
  have h1 : eraseFirst x ∈ tailSub n := eraseFirst_mem_tail hx
  have h2 : theFlip x = eraseFirst x - firstAtom.starProjection x := rfl
  intro k hk
  have hn : 0 < n := lt_of_le_of_lt (Nat.zero_le k) hk
  have hx0 : x 0 = 0 := hx 0 hn
  have hP : firstAtom.starProjection x = 0 := by
    unfold firstAtom
    rw [Submodule.starProjection_singleton ℂ]
    unfold firstInscription
    rw [coord_eq_inner, hx0]
    simp
  rw [h2, hP, sub_zero]
  exact h1 k hk

/-- o flip restrito à cauda (equivalência isométrica: U² = 1). -/
def tailFlip (n : ℕ) : (tailSub n) ≃ₗᵢ[ℂ] (tailSub n) :=
  { toFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_tail x.2⟩
    invFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_tail x.2⟩
    map_add' := fun x y => Subtype.ext (by
      show theFlip ((x : ellTwo) + (y : ellTwo))
        = theFlip (x : ellTwo) + theFlip (y : ellTwo)
      exact map_add theFlip _ _)
    map_smul' := fun c x => Subtype.ext (by
      show theFlip (c • (x : ellTwo)) = c • theFlip (x : ellTwo)
      exact map_smul theFlip c _)
    left_inv := fun x => Subtype.ext (by
      show theFlip (theFlip (x : ellTwo)) = (x : ellTwo)
      calc theFlip (theFlip (x : ellTwo))
          = (theFlip * theFlip) (x : ellTwo) := rfl
        _ = (1 : ellTwo →L[ℂ] ellTwo) (x : ellTwo) := by rw [theFlip_sq]
        _ = (x : ellTwo) := rfl)
    right_inv := fun x => Subtype.ext (by
      show theFlip (theFlip (x : ellTwo)) = (x : ellTwo)
      calc theFlip (theFlip (x : ellTwo))
          = (theFlip * theFlip) (x : ellTwo) := rfl
        _ = (1 : ellTwo →L[ℂ] ellTwo) (x : ellTwo) := by rw [theFlip_sq]
        _ = (x : ellTwo) := rfl)
    norm_map' := fun x => by
      show ‖theFlip (x : ellTwo)‖ = ‖(x : ellTwo)‖
      have h := theFlip_inner (x : ellTwo) (x : ellTwo)
      rw [inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K] at h
      have hb : ‖theFlip (x : ellTwo)‖ ^ 2 = ‖(x : ellTwo)‖ ^ 2 := by
        exact_mod_cast h
      calc ‖theFlip (x : ellTwo)‖
          = Real.sqrt (‖theFlip (x : ellTwo)‖ ^ 2) :=
            (Real.sqrt_sq (norm_nonneg _)).symm
        _ = Real.sqrt (‖(x : ellTwo)‖ ^ 2) := by rw [hb]
        _ = ‖(x : ellTwo)‖ := Real.sqrt_sq (norm_nonneg _) }

/-! ## D — a rede -/

/-- [KERNEL] ★★ A REDE DE CAUDAS: PhysicalNetData com fibra ∞-DIM —
    o último campo do certificado FORTE tem testemunha. -/
def theTailNet :
    PhysicalNetData ℕ (fun a b => b ≤ a)
      (fun n => tailSub n) (fun n => tailSub n) where
  net :=
    { locks := fun n => tailLock n
      internal := fun n s => lockFlow (tailLock n) (tailLock_selfadjoint n) s
      internalW := fun n s =>
        (lockFlow (tailLock n) (tailLock_selfadjoint n) s).toLinearIsometry
      internal_intertwines := fun n s x =>
        lockFlow_commutes (tailLock n) (tailLock_selfadjoint n) s x
      G := Bool
      act := fun _ O => O
      external := fun g n =>
        if g then tailFlip n else LinearIsometryEquiv.refl ℂ _
      externalW := fun g n =>
        if g then (tailFlip n).toLinearIsometry
        else (LinearIsometryEquiv.refl ℂ _).toLinearIsometry
      external_intertwines := fun g n x => by
        cases g
        · rfl
        · exact Subtype.ext (by
            show eraseFirst (theFlip (x : ellTwo))
              = theFlip (eraseFirst (x : ellTwo))
            calc eraseFirst (theFlip (x : ellTwo))
                = (eraseFirst * theFlip) (x : ellTwo) := rfl
              _ = (theFlip * eraseFirst) (x : ellTwo) := by
                  rw [theFlip_comm_eraseFirst]
              _ = theFlip (eraseFirst (x : ellTwo)) := rfl)
      incl := fun h => tailIncl h
      inclW := fun h => tailIncl h
      incl_intertwines := fun h x => Subtype.ext rfl }
  genuinely_isotone := ⟨1, 0, Nat.zero_le 1, tailIncl_not_surjective⟩
  external_nontrivial := ⟨⟨true, false, by decide⟩⟩

end

end TGLExt
