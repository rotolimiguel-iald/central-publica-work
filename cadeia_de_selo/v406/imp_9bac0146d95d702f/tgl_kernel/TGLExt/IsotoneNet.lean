import TGLExt.ProgrammerRule

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A REDE ISÓTONA: PhysicalNetData HABITADA
  [TGLExt — v101, o incremento 18 do programa SemifiniteAnalysis]

O v99 tipou a rede FÍSICA exigida pelo certificado (`PhysicalNetData`:
HilbertHomeData + isotonia GENUÍNA + grupo externo não-trivial) e provou
em kernel que os habitantes de então NÃO a alimentavam. Esta pedra a
HABITA — o primeiro campo do certificado ganha termo:

* as FIBRAS CRESCEM de verdade: H_n = span{e₀,…,e_n} ⊂ ℓ² (submódulos
  gerados pelas inscrições; dimensão finita, completos);
* as inclusões são as CANÔNICAS (isométricas) e a de 0→1 NÃO é
  sobrejetiva (e₁ está fora — pela ortonormalidade): isotonia GENUÍNA;
* os locks são as RESTRIÇÕES de T = 1−P₀ a cada fibra (T preserva as
  fibras; auto-adjunto por simetria herdada) e ENTRELAÇAM com as
  inclusões (𝒟_m ∘ ι = ι ∘ 𝒟_n);
* o fluxo interno é o GENUÍNO exp(isT_n) por fibra (lockFlow, v96);
* o grupo externo é Bool NÃO-TRIVIAL, agindo pelo flip U = 1−2P₀
  (involução: U² = 1; comuta com os locks: TU = UT = 1−P).

HONESTIDADE: as fibras são FINITO-dimensionais e a ação externa não é
geométrica (age trivialmente nas regiões) — o nível III₁/Poincaré segue
sendo o conteúdo do certificado v2; o nome `qgCertificate_core` fica
RESERVADO (nenhuma flag se move). Mas a exigência tipada do v99 —
isotonia genuína + grupo não-trivial — está SATISFEITA por termo.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## As fibras crescentes -/

/-- a fibra n: o span das inscrições e₀,…,e_n. -/
def fiber (n : ℕ) : Submodule ℂ ellTwo :=
  Submodule.span ℂ (inscriptions '' {k | k ≤ n})

instance fiber_fd (n : ℕ) : FiniteDimensional ℂ (fiber n) :=
  FiniteDimensional.span_of_finite ℂ
    ((Set.finite_Iic n).image inscriptions)

instance fiber_complete (n : ℕ) : CompleteSpace (fiber n) :=
  FiniteDimensional.complete ℂ (fiber n)

theorem fiber_mono {n m : ℕ} (h : n ≤ m) : fiber n ≤ fiber m :=
  Submodule.span_mono (Set.image_mono fun _ hk => le_trans hk h)

theorem firstAtom_le_fiber (n : ℕ) : firstAtom ≤ fiber n := by
  unfold firstAtom firstInscription
  rw [Submodule.span_singleton_le_iff_mem]
  exact Submodule.subset_span ⟨0, Nat.zero_le n, rfl⟩

/-- T = 1 − P₀ preserva cada fibra. -/
theorem eraseFirst_mem_fiber {n : ℕ} {x : ellTwo} (hx : x ∈ fiber n) :
    eraseFirst x ∈ fiber n := by
  have hP : firstAtom.starProjection x ∈ fiber n :=
    firstAtom_le_fiber n (Submodule.starProjection_apply_mem firstAtom x)
  have h : eraseFirst x = x - firstAtom.starProjection x := rfl
  rw [h]
  exact Submodule.sub_mem _ hx hP

/-! ## Os locks restritos -/

/-- o lock da fibra: a restrição de T = 1 − P₀. -/
def fiberLock (n : ℕ) : (fiber n) →L[ℂ] (fiber n) :=
  { toFun := fun x => ⟨eraseFirst (x : ellTwo), eraseFirst_mem_fiber x.2⟩
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

theorem fiberLock_symmetric (n : ℕ) :
    ((fiberLock n : (fiber n) →L[ℂ] (fiber n))
      : (fiber n) →ₗ[ℂ] (fiber n)).IsSymmetric := by
  intro x y
  have hsym : ((eraseFirst : ellTwo →L[ℂ] ellTwo)
      : ellTwo →ₗ[ℂ] ellTwo).IsSymmetric :=
    (ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric).mp eraseFirst_isSelfAdjoint
  exact hsym (x : ellTwo) (y : ellTwo)

theorem fiberLock_selfadjoint (n : ℕ) : IsSelfAdjoint (fiberLock n) :=
  (fiberLock_symmetric n).isSelfAdjoint

/-! ## As inclusões canônicas (isométricas; a genuína NÃO-sobrejetividade) -/

/-- a inclusão isométrica entre fibras. -/
def fiberIncl {n m : ℕ} (h : n ≤ m) : (fiber n) →ₗᵢ[ℂ] (fiber m) :=
  ⟨Submodule.inclusion (fiber_mono h), fun _ => rfl⟩

/-- [KERNEL] ★★ A ISOTONIA É GENUÍNA: a inclusão 0→1 NÃO é sobrejetiva
    (e₁ está na fibra 1 e fora da imagem — pela ortonormalidade). -/
theorem fiberIncl_not_surjective :
    ¬ Function.Surjective (fiberIncl (Nat.zero_le 1)) := by
  intro hsurj
  have h1 : inscriptions 1 ∈ fiber 1 :=
    Submodule.subset_span ⟨1, le_refl 1, rfl⟩
  obtain ⟨y, hy⟩ := hsurj ⟨inscriptions 1, h1⟩
  have hy' : (y : ellTwo) = inscriptions 1 := congrArg Subtype.val hy
  have hy0 : inscriptions 1 ∈ fiber 0 := hy' ▸ y.2
  have hfib0 : fiber 0 = Submodule.span ℂ {inscriptions 0} := by
    unfold fiber
    congr 1
    rw [show {k : ℕ | k ≤ 0} = {0} from Set.ext fun k => by simp [Nat.le_zero]]
    exact Set.image_singleton
  rw [hfib0] at hy0
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hy0
  have horto := inscriptions_orthonormal
  rw [orthonormal_iff_ite] at horto
  have h01 := horto 0 1
  rw [if_neg (by decide)] at h01
  have h00 : inner ℂ (inscriptions 0) (inscriptions 0) = (1 : ℂ) := by
    have h := horto 0 0
    rwa [if_pos rfl] at h
  have hkey : inner ℂ (inscriptions 0) (inscriptions 1) = c := by
    rw [← hc, inner_smul_right, h00, mul_one]
  have hc0 : c = 0 := by rw [← hkey, h01]
  rw [hc0, zero_smul] at hc
  exact (inscriptions_orthonormal.ne_zero 1) hc.symm

/-! ## O flip externo: U = 1 − P₀ − P₀ (involução; comuta com os locks) -/

/-- o flip ambiente: U = 1 − P₀ − P₀ (= 1 − 2P₀, escrito em anel puro). -/
def theFlip : ellTwo →L[ℂ] ellTwo :=
  1 - firstAtom.starProjection - firstAtom.starProjection

theorem theFlip_sq : theFlip * theFlip = 1 := by
  have hP : firstAtom.starProjection * firstAtom.starProjection
      = firstAtom.starProjection :=
    firstAtom.isIdempotentElem_starProjection
  unfold theFlip
  have h : ∀ A : ellTwo →L[ℂ] ellTwo, A * A = A →
      (1 - A - A) * (1 - A - A) = 1 := by
    intro A hA
    have e1 : (1 - A - A) * (1 - A - A)
        = 1 - A - A - A - A + (A * A + A * A + A * A + A * A) := by
      noncomm_ring
    rw [e1, hA]
    abel
  exact h _ hP

theorem theFlip_comm_eraseFirst :
    theFlip * eraseFirst = eraseFirst * theFlip := by
  unfold theFlip eraseFirst
  noncomm_ring

theorem theFlip_apply (x : ellTwo) :
    theFlip x = x - firstAtom.starProjection x - firstAtom.starProjection x := rfl

theorem theFlip_symmetric (x y : ellTwo) :
    inner ℂ (theFlip x) y = inner ℂ x (theFlip y) := by
  have hsymP : ((firstAtom.starProjection : ellTwo →L[ℂ] ellTwo)
      : ellTwo →ₗ[ℂ] ellTwo).IsSymmetric :=
    (ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric).mp
      (isSelfAdjoint_starProjection firstAtom)
  have hsymP' : ∀ a b : ellTwo,
      inner ℂ (firstAtom.starProjection a) b
        = inner ℂ a (firstAtom.starProjection b) := fun a b => hsymP a b
  rw [theFlip_apply, theFlip_apply, inner_sub_left, inner_sub_left,
    inner_sub_right, inner_sub_right, hsymP' x y]

/-- U preserva as fibras. -/
theorem theFlip_mem_fiber {n : ℕ} {x : ellTwo} (hx : x ∈ fiber n) :
    theFlip x ∈ fiber n := by
  have hP : firstAtom.starProjection x ∈ fiber n :=
    firstAtom_le_fiber n (Submodule.starProjection_apply_mem firstAtom x)
  rw [theFlip_apply]
  exact Submodule.sub_mem _ (Submodule.sub_mem _ hx hP) hP

/-- o flip preserva o produto interno (simétrico com U² = 1). -/
theorem theFlip_inner (x y : ellTwo) :
    inner ℂ (theFlip x) (theFlip y) = inner ℂ x y := by
  calc inner ℂ (theFlip x) (theFlip y)
      = inner ℂ x (theFlip (theFlip y)) := theFlip_symmetric x (theFlip y)
    _ = inner ℂ x ((theFlip * theFlip) y) := rfl
    _ = inner ℂ x ((1 : ellTwo →L[ℂ] ellTwo) y) := by rw [theFlip_sq]
    _ = inner ℂ x y := rfl

/-- o flip na fibra, como equivalência isométrica (involução). -/
def fiberFlip (n : ℕ) : (fiber n) ≃ₗᵢ[ℂ] (fiber n) :=
  { toFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_fiber x.2⟩
    invFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_fiber x.2⟩
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

/-! ## O HABITANTE -/

/-- [KERNEL] ★★★★ PhysicalNetData HABITADA: fibras crescentes com
    inclusões genuinamente não-sobrejetivas, locks restritos que
    entrelaçam, fluxo interno exp(isT_n) genuíno por fibra, e grupo
    externo Bool NÃO-TRIVIAL agindo pelo flip U = 1−2P₀. -/
def theIsotoneNet :
    PhysicalNetData ℕ (· ≤ ·) (fun n => fiber n) (fun n => fiber n) where
  net :=
    { locks := fun n => fiberLock n
      internal := fun n s => lockFlow (fiberLock n) (fiberLock_selfadjoint n) s
      internalW := fun n s =>
        (lockFlow (fiberLock n) (fiberLock_selfadjoint n) s).toLinearIsometry
      internal_intertwines := fun n s x =>
        lockFlow_commutes (fiberLock n) (fiberLock_selfadjoint n) s x
      G := Bool
      act := fun _ O => O
      external := fun g n =>
        if g then fiberFlip n else LinearIsometryEquiv.refl ℂ _
      externalW := fun g n =>
        if g then (fiberFlip n).toLinearIsometry
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
      incl := fun h => fiberIncl h
      inclW := fun h => fiberIncl h
      incl_intertwines := fun h x => Subtype.ext rfl }
  genuinely_isotone := ⟨0, 1, Nat.zero_le 1, fiberIncl_not_surjective⟩
  external_nontrivial := ⟨⟨true, false, by decide⟩⟩

end

end TGLExt
