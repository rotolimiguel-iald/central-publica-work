import TGLExt.TheCornerOfThePackage
import TGLExt.TailNet
import TGLExt.FusedWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A REDE LARGA — isotonia genuína, fibras ∞-dim, e o canto pesando o Nome
  [TGLExt — a pedra de 28/08/2026 · PEÇA 1 da solda]

## O que faltava, e por que as tentativas óbvias falhavam

A medida da solda nomeou três peças. Esta é a primeira: uma rede que seja
**simultaneamente** genuinamente isótona, de fibras **∞-dimensionais**, e com canto de
Breuer **finito não-nulo**. O acervo tinha as combinações erradas:

| rede | isótona? | fibra | canto |
|---|---|---|---|
| `theConstantNet` | ✗ (inclusão = id) | ∞-dim | ✓ `τ = 1` |
| `theIsotoneNet` | ✓ | **finita** | ✓ (v280) |
| `theTailNet` | ✓ | ∞-dim | ✗ |
| `theFusedNet` | ✓ | ∞-dim | ✗ |
| **`theWideNet`** | **✓** | **∞-dim** | **✓ `τ ≡ 1`** |

★ **O erro das tentativas óbvias era sempre o mesmo**: usar TODAS as coordenadas para a
filtração. `span{e_k : k=0 ∨ k≥n}` **decresce**; `span{e₀} + cauda` é **constante**. A
correção é congelar um sub-reticulado **infinito** presente em TODAS as fibras e crescer
apenas no complementar — `ℓ²` tem coordenadas de sobra para as duas coisas.

`wideSub n` anula-se nos **ÍMPARES ≥ n**: os **pares nunca são cortados** (garantem ∞-dim
em toda região), e o crescimento acontece só nos ímpares (dá a isotonia genuína).

## O que se prova `[REAL]`

* ★★★ `wideSub_not_finiteDimensional` — **∞-dim em TODA região** (contém `{e_{2m}}`);
* ★★★ `wideIncl_not_surjective` — **isotonia GENUÍNA**: `e₁ ∈ wideSub 2` (1 é ímpar mas
  `1 < 2`) e `e₁ ∉ wideSub 0`;
* ★★★★ `wide_ker_eq` — o núcleo do lock é **exatamente** a reta do Nome;
* ★★★★★ `wide_corner_weighs_one` — **`τ ≡ 1 = ω(I)`**. Não só `0 < τ < ∞`: **o peso É o
  Nome**, e em fibra infinita;
* ★★★★★ `theWideNet` / `theWideNetTrace` — os termos, e `wide_net_has_all_three`.

## E os dois NEGATIVOS que a construção mediu de passagem

* ★★★ `tailLock_ker_eq_bot` — **por que a cauda falha**: para `n ≥ 1` tem-se `x₀ = 0` na
  fibra, logo `P₀x = 0`, logo **o lock É A IDENTIDADE** e o núcleo é `⊥`.
  ⚠ **Correção ao relatório**: em `n = 0` o núcleo **não** é trivial (`tailSub 0 = ℓ²`).
  O defeito é **não-uniformidade**, não trivialidade — `BreuerTraceData` pede `∀ O`, e a
  cauda perde o Nome assim que sobe uma região. Ela cresce **removendo** coordenadas, e a
  primeira que remove é justamente a que carrega o núcleo;
* ★★★ `fused_ker_contains_L2` — **por que a fundida falha**: o lock ignora a segunda
  componente, e o núcleo contém uma cópia isométrica inteira de `L²(ℝ⁴)`.

## ⚠ O QUE ISTO NÃO FAZ

**Não solda.** As outras duas peças nomeadas pela medida **não caem daqui**, e ambas
resultaram negativas: a identificação `dirac.D = locks` é **impossível por tipo**
(limitado contra não-limitado), e a covariância do frame é **falsa** (colide com
`frame_nonconstant`, já selado).

`gpf_tower_act_III_inhabitant_constructed` **continua apagada**. Nada aqui a acende.
β jamais literal. Sem sorry, sem axiom. O gate não se move.
-/

namespace TGLExt

noncomputable section

/-- a fibra LARGA n: anula-se nas coordenadas ÍMPARES ≥ n. -/
def wideSub (n : ℕ) : Submodule ℂ ellTwo where
  carrier := {x | ∀ k, Odd k → n ≤ k → x k = 0}
  zero_mem' := by
    intro k _ _
    show (0 : ellTwo) k = 0
    rw [lp.coeFn_zero]
    rfl
  add_mem' := by
    intro a b ha hb k hk hn
    show (a + b) k = 0
    rw [lp.coeFn_add, Pi.add_apply, ha k hk hn, hb k hk hn, add_zero]
  smul_mem' := by
    intro c x hx k hk hn
    show (c • x) k = 0
    rw [lp.coeFn_smul, Pi.smul_apply, hx k hk hn, smul_zero]

theorem mem_wideSub_iff {n : ℕ} {x : ellTwo} :
    x ∈ wideSub n ↔ ∀ k, Odd k → n ≤ k → x k = 0 := Iff.rfl

theorem wideSub_isClosed (n : ℕ) : IsClosed (wideSub n : Set ellTwo) := by
  have h : (wideSub n : Set ellTwo)
      = ⋂ k ∈ {k : ℕ | Odd k ∧ n ≤ k},
          (innerSL ℂ (inscriptions k)) ⁻¹' {0} := by
    ext x
    simp only [Set.mem_iInter, Set.mem_preimage, Set.mem_singleton_iff,
      Set.mem_setOf_eq, SetLike.mem_coe, mem_wideSub_iff]
    constructor
    · intro hx k hk
      show inner ℂ (inscriptions k) x = 0
      rw [coord_eq_inner]
      exact hx k hk.1 hk.2
    · intro hx k hk hn
      have := hx k ⟨hk, hn⟩
      rwa [show (innerSL ℂ (inscriptions k)) x = inner ℂ (inscriptions k) x
        from rfl, coord_eq_inner] at this
  rw [h]
  exact isClosed_biInter fun k _ =>
    (isClosed_singleton).preimage (innerSL ℂ (inscriptions k)).continuous

instance wideSub_complete (n : ℕ) : CompleteSpace (wideSub n) :=
  (wideSub_isClosed n).completeSpace_coe

theorem wide_mono {n m : ℕ} (h : n ≤ m) : wideSub n ≤ wideSub m :=
  fun _ hx k hk hm => hx k hk (le_trans h hm)

theorem even_mem_wideSub (n m : ℕ) : inscriptions (2 * m) ∈ wideSub n := by
  intro k hk _
  rw [inscriptions_apply, if_neg]
  rintro rfl
  exact (Nat.not_odd_iff_even.mpr ⟨m, by omega⟩) hk

theorem wideSub_not_finiteDimensional (n : ℕ) :
    ¬ FiniteDimensional ℂ (wideSub n) := by
  intro hfd
  set d := Module.finrank ℂ (wideSub n) with hd
  have hli0 : LinearIndependent ℂ (fun m : ℕ => inscriptions (2 * m)) :=
    inscriptions_orthonormal.linearIndependent.comp _ (fun a b hab => by omega)
  have hli : LinearIndependent ℂ
      (fun m : ℕ => (⟨inscriptions (2 * m), even_mem_wideSub n m⟩ : wideSub n)) :=
    hli0.of_comp (wideSub n).subtype
  have hli2 : LinearIndependent ℂ
      ((fun m : ℕ => (⟨inscriptions (2 * m), even_mem_wideSub n m⟩ : wideSub n))
        ∘ (fun i : Fin (d + 1) => (i : ℕ))) :=
    hli.comp _ Fin.val_injective
  have hcard := hli2.fintype_card_le_finrank
  rw [Fintype.card_fin] at hcard
  omega

def wideIncl {n m : ℕ} (h : n ≤ m) : (wideSub n) →ₗᵢ[ℂ] (wideSub m) :=
  ⟨Submodule.inclusion (wide_mono h), fun _ => rfl⟩

theorem wideIncl_not_surjective :
    ¬ Function.Surjective (wideIncl (show 0 ≤ 2 from Nat.zero_le 2)) := by
  intro hsurj
  have h1 : inscriptions 1 ∈ wideSub 2 := by
    intro k _ hk
    rw [inscriptions_apply, if_neg]
    omega
  obtain ⟨y, hy⟩ := hsurj ⟨inscriptions 1, h1⟩
  have hy2 : (y : ellTwo) = inscriptions 1 := congrArg Subtype.val hy
  have hy0 : (y : ellTwo) 1 = 0 := y.2 1 ⟨0, by omega⟩ (Nat.zero_le 1)
  rw [hy2] at hy0
  rw [inscriptions_apply, if_pos rfl] at hy0
  exact one_ne_zero hy0

theorem firstAtom_coord_zero {y : ellTwo} (hy : y ∈ firstAtom) {k : ℕ}
    (hk : k ≠ 0) : y k = 0 := by
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hy
  rw [← hc, lp.coeFn_smul, Pi.smul_apply]
  unfold firstInscription
  rw [inscriptions_apply, if_neg hk]
  simp

theorem eraseFirst_mem_wide {n : ℕ} {x : ellTwo} (hx : x ∈ wideSub n) :
    eraseFirst x ∈ wideSub n := by
  intro k hk hn
  have hk0 : k ≠ 0 := by
    rintro rfl
    exact (Nat.not_odd_iff_even.mpr ⟨0, rfl⟩) hk
  show (x - firstAtom.starProjection x) k = 0
  rw [lp.coeFn_sub, Pi.sub_apply,
    firstAtom_coord_zero (Submodule.starProjection_apply_mem firstAtom x) hk0,
    hx k hk hn, sub_zero]

theorem theFlip_mem_wide {n : ℕ} {x : ellTwo} (hx : x ∈ wideSub n) :
    theFlip x ∈ wideSub n := by
  intro k hk hn
  have hk0 : k ≠ 0 := by
    rintro rfl
    exact (Nat.not_odd_iff_even.mpr ⟨0, rfl⟩) hk
  have hP : (firstAtom.starProjection x) k = 0 :=
    firstAtom_coord_zero (Submodule.starProjection_apply_mem firstAtom x) hk0
  show (x - firstAtom.starProjection x - firstAtom.starProjection x) k = 0
  rw [lp.coeFn_sub, Pi.sub_apply, lp.coeFn_sub, Pi.sub_apply, hP,
    hx k hk hn, sub_zero, sub_zero]

def wideLock (n : ℕ) : (wideSub n) →L[ℂ] (wideSub n) :=
  { toFun := fun x => ⟨eraseFirst (x : ellTwo), eraseFirst_mem_wide x.2⟩
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

theorem wideLock_symmetric (n : ℕ) :
    ((wideLock n : (wideSub n) →L[ℂ] (wideSub n))
      : (wideSub n) →ₗ[ℂ] (wideSub n)).IsSymmetric := by
  intro x y
  have hsym : ((eraseFirst : ellTwo →L[ℂ] ellTwo)
      : ellTwo →ₗ[ℂ] ellTwo).IsSymmetric :=
    (ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric).mp eraseFirst_isSelfAdjoint
  exact hsym (x : ellTwo) (y : ellTwo)

theorem wideLock_selfadjoint (n : ℕ) : IsSelfAdjoint (wideLock n) :=
  (wideLock_symmetric n).isSelfAdjoint

theorem first_mem_wide (n : ℕ) : firstInscription ∈ wideSub n := by
  intro k hk _
  unfold firstInscription
  rw [inscriptions_apply, if_neg]
  rintro rfl
  exact (Nat.not_odd_iff_even.mpr ⟨0, rfl⟩) hk

def wideAtom (n : ℕ) : wideSub n := ⟨firstInscription, first_mem_wide n⟩

theorem wideAtom_ne_zero (n : ℕ) : wideAtom n ≠ 0 := by
  intro h
  have h2 := congrArg Subtype.val h
  exact inscriptions_orthonormal.ne_zero 0 h2

theorem wide_ker_eq (n : ℕ) : (wideLock n).ker = ℂ ∙ (wideAtom n) := by
  apply le_antisymm
  · intro v hv
    have h0 : eraseFirst ((v : ellTwo)) = 0 :=
      congrArg Subtype.val (LinearMap.mem_ker.mp hv)
    have hmem : (v : ellTwo) ∈ firstAtom := by
      have h1 : (v : ellTwo) ∈ eraseFirst.ker := LinearMap.mem_ker.mpr h0
      rwa [ker_eraseFirst] at h1
    obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hmem
    exact Submodule.mem_span_singleton.mpr ⟨c, Subtype.ext hc⟩
  · rw [Submodule.span_singleton_le_iff_mem]
    refine LinearMap.mem_ker.mpr (Subtype.ext ?_)
    show eraseFirst firstInscription = 0
    have hk : firstInscription ∈ eraseFirst.ker := by
      rw [ker_eraseFirst]
      exact Submodule.mem_span_singleton_self _
    exact LinearMap.mem_ker.mp hk

instance wide_ker_fd (n : ℕ) : FiniteDimensional ℂ ((wideLock n).ker) := by
  rw [wide_ker_eq]
  infer_instance

theorem wide_ker_ne_bot (n : ℕ) : (wideLock n).ker ≠ ⊥ := by
  rw [wide_ker_eq]
  intro h
  exact wideAtom_ne_zero n ((Submodule.span_singleton_eq_bot).mp h)

theorem wide_corner_weighs_one (n : ℕ) :
    dimOrTop ℂ ((wideLock n).ker) = 1 := by
  rw [dimOrTop_of_finite ℂ (wide_ker_fd n)]
  have h : Module.finrank ℂ ((wideLock n).ker) = 1 := by
    rw [wide_ker_eq]
    exact finrank_span_singleton (wideAtom_ne_zero n)
  rw [h, Nat.cast_one]

def wideFlip (n : ℕ) : (wideSub n) ≃ₗᵢ[ℂ] (wideSub n) :=
  { toFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_wide x.2⟩
    invFun := fun x => ⟨theFlip (x : ellTwo), theFlip_mem_wide x.2⟩
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

def theWideNet :
    PhysicalNetData ℕ (· ≤ ·) (fun n => wideSub n) (fun n => wideSub n) where
  net :=
    { locks := fun n => wideLock n
      internal := fun n s => lockFlow (wideLock n) (wideLock_selfadjoint n) s
      internalW := fun n s =>
        (lockFlow (wideLock n) (wideLock_selfadjoint n) s).toLinearIsometry
      internal_intertwines := fun n s x =>
        lockFlow_commutes (wideLock n) (wideLock_selfadjoint n) s x
      G := Bool
      act := fun _ O => O
      external := fun g n =>
        if g then wideFlip n else LinearIsometryEquiv.refl ℂ _
      externalW := fun g n =>
        if g then (wideFlip n).toLinearIsometry
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
      incl := fun h => wideIncl h
      inclW := fun h => wideIncl h
      incl_intertwines := fun h x => Subtype.ext rfl }
  genuinely_isotone := ⟨0, 2, Nat.zero_le 2, wideIncl_not_surjective⟩
  external_nontrivial := ⟨⟨true, false, by decide⟩⟩

def theWideNetTrace : BreuerTraceData theWideNet.net where
  tau n _ := dimOrTop ℂ (wideLock n).ker
  tau_PF_pos n := by
    rw [wide_corner_weighs_one n]
    exact zero_lt_one
  tau_PF_finite n := by
    rw [wide_corner_weighs_one n]
    exact ENNReal.one_lt_top

theorem wide_net_has_all_three :
    (¬ FiniteDimensional ℂ (wideSub 0))
    ∧ (¬ Function.Surjective
          (theWideNet.net.incl (show (0 : ℕ) ≤ 2 from Nat.zero_le 2)))
    ∧ (0 < theWideNetTrace.tau 0 (theWideNet.net.PF 0)
        ∧ theWideNetTrace.tau 0 (theWideNet.net.PF 0) < ⊤)
    ∧ theWideNetTrace.tau 0 (theWideNet.net.PF 0) = 1 :=
  ⟨wideSub_not_finiteDimensional 0, wideIncl_not_surjective,
    ⟨theWideNetTrace.tau_PF_pos 0, theWideNetTrace.tau_PF_finite 0⟩,
    wide_corner_weighs_one 0⟩

/-! ## PROBES NEGATIVOS sobre as redes que o gate lê -/

theorem tailLock_ker_eq_bot {n : ℕ} (hn : 0 < n) : (tailLock n).ker = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro v hv
  have h0 : eraseFirst ((v : ellTwo)) = 0 :=
    congrArg Subtype.val (LinearMap.mem_ker.mp hv)
  have hmem : (v : ellTwo) ∈ firstAtom := by
    have h1 : (v : ellTwo) ∈ eraseFirst.ker := LinearMap.mem_ker.mpr h0
    rwa [ker_eraseFirst] at h1
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hmem
  have hv0 : (v : ellTwo) 0 = 0 := v.2 0 hn
  rw [← hc] at hv0
  have hc0 : c = 0 := by
    rw [lp.coeFn_smul, Pi.smul_apply] at hv0
    unfold firstInscription at hv0
    rw [inscriptions_apply, if_pos rfl] at hv0
    simpa using hv0
  apply Subtype.ext
  show (v : ellTwo) = 0
  rw [← hc, hc0, zero_smul]

theorem fused_ker_contains_L2 (O : PoinRegion) (F : SpacetimeL2) :
    (WithLp.toLp 2 ((0 : tailSub O.2), F)) ∈ (theFusedNet.net.locks O).ker := by
  refine LinearMap.mem_ker.mpr ?_
  show (tailLock O.2) (0 : tailSub O.2) = 0
  exact map_zero _

end

end TGLExt
