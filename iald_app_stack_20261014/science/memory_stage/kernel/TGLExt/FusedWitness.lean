import TGLExt.SemifiniteWeight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A FUSÃO: a representação fiel DENTRO das fibras — nenhuma direção cega
  [TGLExt — v123, o incremento 42 do programa SemifiniteAnalysis]

O v118 construiu a rep fiel U(g) em L²(ℝ⁴) e nomeou o resíduo curto da
testemunha: "a FUSÃO da rep às fibras da rede". Esta pedra a executa:

* `fusedFiber` = cauda × L²(ℝ⁴) com a norma L² do produto (WithLp 2) —
  a fibra carrega a ISOTONIA (caudas ∞-dim, v106) E a REPRESENTAÇÃO
  (L², v118) simultaneamente;
* `regularRepEquiv` — U(g) elevado a equivalência isométrica (inversa
  U(g⁻¹), pela lei de grupo provada);
* `prodL2CongrLI`/`prodL2MapLI` — (equi)isometrias componente a
  componente no produto L² (norma preservada pelo produto interno de
  ProdL2 + inner_map_map);
* ★★★ `theFusedWitness : FullWitnessData` — a testemunha FUNDIDA:
  Poincaré age nas regiões (fiel, v116) E DENTRO das fibras (fiel,
  pela componente L² do v118);
* ★★★ `fused_fiber_faithful` — NENHUMA DIREÇÃO É CEGA NAS FIBRAS:
  para TODO g ≠ 1 existe ξ na fibra com U_g ξ ≠ ξ; ★★
  `fused_boost_moves_fiber` — o corolário que SUPERA a honestidade do
  v116 (`proper_sector_fibers_blind`): o boost agora move vetores
  DENTRO da fibra da rede covariante.

O QUE RESTA (nomeado, sem véu): o resíduo formal da testemunha é
AGORA SÓ III₁ (o fator sem peso semifinito — Araki–Woods). O
`qgClosureCertificateV2` segue RESERVADO (lição v103, 11ª aplicação):
a fusão é necessária, não suficiente.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped Classical ENNReal

noncomputable section

/-! ## A — U(g) como equivalência isométrica -/

theorem regularRep_left_inv (g : PoincareGroup) (F : SpacetimeL2) :
    regularRep g⁻¹ (regularRep g F) = F := by
  rw [← regularRep_mul, inv_mul_cancel, regularRep_one]

theorem regularRep_right_inv (g : PoincareGroup) (F : SpacetimeL2) :
    regularRep g (regularRep g⁻¹ F) = F := by
  rw [← regularRep_mul, mul_inv_cancel, regularRep_one]

/-- U(g) como equivalência isométrica de L². -/
def regularRepEquiv (g : PoincareGroup) : SpacetimeL2 ≃ₗᵢ[ℂ] SpacetimeL2 :=
  { toFun := regularRep g
    invFun := regularRep g⁻¹
    map_add' := (regularRep g).map_add
    map_smul' := (regularRep g).map_smul
    left_inv := regularRep_left_inv g
    right_inv := regularRep_right_inv g
    norm_map' := (regularRep g).norm_map }

theorem regularRepEquiv_apply (g : PoincareGroup) (F : SpacetimeL2) :
    regularRepEquiv g F = regularRep g F := rfl

/-! ## B — (equi)isometrias componente a componente no produto L² -/

section ProdMaps

variable {E F E' F' : Type}
variable [NormedAddCommGroup E] [InnerProductSpace ℂ E]
variable [NormedAddCommGroup F] [InnerProductSpace ℂ F]
variable [NormedAddCommGroup E'] [InnerProductSpace ℂ E']
variable [NormedAddCommGroup F'] [InnerProductSpace ℂ F']

/-- a equivalência isométrica componente a componente em WithLp 2. -/
def prodL2CongrLI (A : E ≃ₗᵢ[ℂ] E') (B : F ≃ₗᵢ[ℂ] F') :
    WithLp 2 (E × F) ≃ₗᵢ[ℂ] WithLp 2 (E' × F') :=
  { toLinearEquiv :=
      (WithLp.linearEquiv 2 ℂ (E × F)).trans
        ((A.toLinearEquiv.prodCongr B.toLinearEquiv).trans
          (WithLp.linearEquiv 2 ℂ (E' × F')).symm)
    norm_map' := fun x => by
      set y := ((WithLp.linearEquiv 2 ℂ (E × F)).trans
        ((A.toLinearEquiv.prodCongr B.toLinearEquiv).trans
          (WithLp.linearEquiv 2 ℂ (E' × F')).symm)) x with hy
      have hfst : (WithLp.ofLp y).1 = A (WithLp.ofLp x).1 := rfl
      have hsnd : (WithLp.ofLp y).2 = B (WithLp.ofLp x).2 := rfl
      have hinner : (inner ℂ y y : ℂ) = inner ℂ x x := by
        rw [WithLp.prod_inner_apply, WithLp.prod_inner_apply, hfst, hsnd,
          A.inner_map_map, B.inner_map_map]
      have hsq : ‖y‖ ^ 2 = ‖x‖ ^ 2 := by
        rw [inner_self_eq_norm_sq_to_K (𝕜 := ℂ),
          inner_self_eq_norm_sq_to_K (𝕜 := ℂ)] at hinner
        exact_mod_cast hinner
      calc ‖y‖ = Real.sqrt (‖y‖ ^ 2) := (Real.sqrt_sq (norm_nonneg _)).symm
        _ = Real.sqrt (‖x‖ ^ 2) := by rw [hsq]
        _ = ‖x‖ := Real.sqrt_sq (norm_nonneg _) }

theorem prodL2CongrLI_fst (A : E ≃ₗᵢ[ℂ] E') (B : F ≃ₗᵢ[ℂ] F')
    (x : WithLp 2 (E × F)) :
    WithLp.fst (prodL2CongrLI A B x) = A (WithLp.fst x) := rfl

theorem prodL2CongrLI_snd (A : E ≃ₗᵢ[ℂ] E') (B : F ≃ₗᵢ[ℂ] F')
    (x : WithLp 2 (E × F)) :
    WithLp.snd (prodL2CongrLI A B x) = B (WithLp.snd x) := rfl

/-- a isometria componente a componente (não-equivalência). -/
def prodL2MapLI (A : E →ₗᵢ[ℂ] E') (B : F →ₗᵢ[ℂ] F') :
    WithLp 2 (E × F) →ₗᵢ[ℂ] WithLp 2 (E' × F') :=
  { toLinearMap :=
      ((WithLp.linearEquiv 2 ℂ (E' × F')).symm.toLinearMap.comp
        ((A.toLinearMap.prodMap B.toLinearMap).comp
          (WithLp.linearEquiv 2 ℂ (E × F)).toLinearMap))
    norm_map' := fun x => by
      set y := (((WithLp.linearEquiv 2 ℂ (E' × F')).symm.toLinearMap.comp
        ((A.toLinearMap.prodMap B.toLinearMap).comp
          (WithLp.linearEquiv 2 ℂ (E × F)).toLinearMap))) x with hy
      have hfst : (WithLp.ofLp y).1 = A (WithLp.ofLp x).1 := rfl
      have hsnd : (WithLp.ofLp y).2 = B (WithLp.ofLp x).2 := rfl
      have hinner : (inner ℂ y y : ℂ) = inner ℂ x x := by
        rw [WithLp.prod_inner_apply, WithLp.prod_inner_apply, hfst, hsnd,
          A.inner_map_map, B.inner_map_map]
      have hsq : ‖y‖ ^ 2 = ‖x‖ ^ 2 := by
        rw [inner_self_eq_norm_sq_to_K (𝕜 := ℂ),
          inner_self_eq_norm_sq_to_K (𝕜 := ℂ)] at hinner
        exact_mod_cast hinner
      calc ‖y‖ = Real.sqrt (‖y‖ ^ 2) := (Real.sqrt_sq (norm_nonneg _)).symm
        _ = Real.sqrt (‖x‖ ^ 2) := by rw [hsq]
        _ = ‖x‖ := Real.sqrt_sq (norm_nonneg _) }

theorem prodL2MapLI_fst (A : E →ₗᵢ[ℂ] E') (B : F →ₗᵢ[ℂ] F')
    (x : WithLp 2 (E × F)) :
    WithLp.fst (prodL2MapLI A B x) = A (WithLp.fst x) := rfl

end ProdMaps

/-! ## C — a fibra fundida -/

/-- a fibra FUNDIDA: cauda (isotonia) × L²(ℝ⁴) (representação). -/
abbrev fusedFiber (O : PoinRegion) : Type :=
  WithLp 2 ((tailSub O.2) × SpacetimeL2)

theorem fused_ext {O : PoinRegion} {x y : fusedFiber O}
    (h1 : WithLp.fst x = WithLp.fst y) (h2 : WithLp.snd x = WithLp.snd y) :
    x = y := by
  apply (WithLp.equiv 2 _).injective
  exact Prod.ext h1 h2

theorem fusedFiber_not_finiteDimensional (O : PoinRegion) :
    ¬ FiniteDimensional ℂ (fusedFiber O) := by
  intro h
  have hsurj : Function.Surjective
      ((WithLp.fstL 2 ℂ (tailSub O.2) SpacetimeL2)) := by
    intro a
    exact ⟨WithLp.toLp 2 (a, 0), rfl⟩
  have hf : FiniteDimensional ℂ (tailSub O.2) :=
    Module.Finite.of_surjective
      ((WithLp.fstL 2 ℂ (tailSub O.2) SpacetimeL2).toLinearMap) hsurj
  exact tailSub_not_finiteDimensional O.2 hf

/-! ## D — a rede fundida -/

/-- [KERNEL] ★★ A REDE FUNDIDA: Poincaré nas regiões; nas fibras a
    paridade flipa a cauda E U(g) age na componente L² — a fusão. -/
@[reducible] def theFusedNet :
    PhysicalNetData PoinRegion poinLe fusedFiber (fun O => tailSub O.2) where
  net :=
    { locks := fun O =>
        (tailLock O.2).comp (WithLp.fstL 2 ℂ (tailSub O.2) SpacetimeL2)
      internal := fun O s =>
        prodL2CongrLI (lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s)
          (LinearIsometryEquiv.refl ℂ SpacetimeL2)
      internalW := fun O s =>
        (lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s).toLinearIsometry
      internal_intertwines := fun O s x =>
        lockFlow_commutes (tailLock O.2) (tailLock_selfadjoint O.2) s
          (WithLp.fst x)
      G := PoincareGroup
      act := poinAct
      external := fun g O =>
        prodL2CongrLI
          (if g.lor.1.det = 1 then LinearIsometryEquiv.refl ℂ _
           else tailFlip O.2)
          (regularRepEquiv g)
      externalW := fun g O =>
        if g.lor.1.det = 1 then
          (LinearIsometryEquiv.refl ℂ _).toLinearIsometry
        else (tailFlip O.2).toLinearIsometry
      external_intertwines := fun g O x => by
        by_cases hdet : g.lor.1.det = 1
        · simp only [hdet, if_pos]
          exact Subtype.ext rfl
        · simp only [hdet, if_neg, not_false_iff]
          exact Subtype.ext (by
            show eraseFirst (theFlip ((WithLp.fst x : tailSub O.2) : ellTwo))
              = theFlip (eraseFirst ((WithLp.fst x : tailSub O.2) : ellTwo))
            calc eraseFirst (theFlip ((WithLp.fst x : tailSub O.2) : ellTwo))
                = (eraseFirst * theFlip) ((WithLp.fst x : tailSub O.2) : ellTwo) := rfl
              _ = (theFlip * eraseFirst) ((WithLp.fst x : tailSub O.2) : ellTwo) := by
                  rw [theFlip_comm_eraseFirst]
              _ = theFlip (eraseFirst ((WithLp.fst x : tailSub O.2) : ellTwo)) := rfl)
      incl := fun h =>
        prodL2MapLI (tailIncl h.2)
          (LinearIsometryEquiv.refl ℂ SpacetimeL2).toLinearIsometry
      inclW := fun h => tailIncl h.2
      incl_intertwines := fun _ x => Subtype.ext rfl }
  genuinely_isotone := by
    refine ⟨((fun _ => 0 : Fin 4 → ℝ), 1), ((fun _ => 0 : Fin 4 → ℝ), 0),
      ⟨rfl, Nat.zero_le 1⟩, fun hsurj => ?_⟩
    apply tailIncl_not_surjective
    intro y
    obtain ⟨ξ, hξ⟩ := hsurj (WithLp.toLp 2 (y, 0))
    exact ⟨WithLp.fst ξ,
      congrArg (fun z : fusedFiber ((fun _ => 0 : Fin 4 → ℝ), 0) =>
        WithLp.fst z) hξ⟩
  external_nontrivial := by
    show Nontrivial PoincareGroup
    refine ⟨⟨⟨(fun _ => 1 : Fin 4 → ℝ), 1⟩, 1, fun h => ?_⟩⟩
    have htr := congrArg PoincareGroup.tr h
    have h0 := congrArg (fun v : Fin 4 → ℝ => v 0) htr
    simp only [poincare_one_tr] at h0
    norm_num at h0

/-! ## E — o certificado forte fundido e A TESTEMUNHA -/

@[reducible] def theFusedStrong : QGClosureCertificateStrong where
  Region := PoinRegion
  leR := poinLe
  H := fusedFiber
  W := fun O => tailSub O.2
  core := theFusedNet
  core_infinite := ⟨((fun _ => 0 : Fin 4 → ℝ), 0),
    fusedFiber_not_finiteDimensional _⟩
  ℍ := ellTwo
  dirac := theGenuineDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := genuineDirac_corner_pos
  corner_finite := genuineDirac_corner_finite
  frame := theCurvedFrame
  frame_nonconstant := curvedFrame_nonconstant

/-- [KERNEL] ★★★ A TESTEMUNHA FUNDIDA: Poincaré fiel nas regiões E
    dentro das fibras — sob nome NÃO-reservado (o V2 segue reservado:
    resta III₁). -/
def theFusedWitness : FullWitnessData where
  toQGClosureCertificateStrong := theFusedStrong
  act_one := fun O => poinAct_one O
  act_mul := fun g h O => poinAct_mul g h O
  act_mono := fun g {O₁ O₂} h => poinAct_mono g h
  geometric_nontrivial := by
    dsimp only [theFusedStrong, theFusedNet]
    refine ⟨⟨(fun _ => 1 : Fin 4 → ℝ), 1⟩,
      ((fun _ => 0 : Fin 4 → ℝ), 0), fun h => ?_⟩
    have hfst := congrArg Prod.fst h
    have h0 := congrArg (fun v : Fin 4 → ℝ => v 0) hfst
    unfold poinAct pAct at h0
    simp only [lorentzGrp_one_val, Matrix.one_mulVec] at h0
    norm_num at h0
  flow_law := fun O s t x => by
    dsimp only [theFusedStrong, theFusedNet]
    apply fused_ext
    · exact lockFlow_add (tailLock O.2) (tailLock_selfadjoint O.2) s t
        (WithLp.fst x)
    · rfl
  covariant_inclusions := fun g {O₁ O₂} hle x => by
    dsimp only [theFusedStrong, theFusedNet]
    apply fused_ext
    · by_cases hdet : g.lor.1.det = 1
      · simp only [hdet, if_pos]
        exact Subtype.ext rfl
      · simp only [hdet, if_neg, not_false_iff]
        exact Subtype.ext rfl
    · rfl

/-! ## F — os teoremas da fusão -/

/-- [KERNEL] ★★★ NENHUMA DIREÇÃO É CEGA NAS FIBRAS: todo g ≠ 1 move
    algum vetor DENTRO da fibra fundida (pela componente L² fiel). -/
theorem fused_fiber_faithful (g : PoincareGroup) (hg : g ≠ 1) :
    ∃ ξ : fusedFiber ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)),
      theFusedNet.net.external g ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)) ξ ≠ ξ := by
  obtain ⟨F, hF⟩ := regularRep_faithful g hg
  refine ⟨WithLp.toLp 2 (0, F), fun h => hF ?_⟩
  exact congrArg (fun ξ : fusedFiber ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)) =>
    WithLp.snd ξ) h

/-- [KERNEL] ★★ A HONESTIDADE DO v116 SUPERADA: o boost (setor próprio,
    antes CEGO nas fibras) agora MOVE vetores dentro da fibra fundida. -/
theorem fused_boost_moves_fiber (χ : ℝ) (hχ : χ ≠ 0) :
    ∃ ξ : fusedFiber ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)),
      theFusedNet.net.external (boostElement χ)
        ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)) ξ ≠ ξ :=
  fused_fiber_faithful (boostElement χ) (boostElement_ne_one χ hχ)

end

end TGLExt
