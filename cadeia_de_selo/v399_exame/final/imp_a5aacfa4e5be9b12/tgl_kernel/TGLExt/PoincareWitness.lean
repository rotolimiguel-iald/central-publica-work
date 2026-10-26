import TGLExt.PoincareGroup

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA DE POINCARÉ: as dez direções agem na rede — e a fibra sente
  [TGLExt — v116, o incremento 38 do programa SemifiniteAnalysis]

O v114 fez a fibra sentir UM flip (ℤ × ℤ/2). Esta pedra troca o grupo
de brinquedo pelo GRUPO DE POINCARÉ inteiro (v116, à mão):

* `PoinRegion` = (ℝ⁴) × ℕ — a base é o ESPAÇO-TEMPO (não mais ℤ);
  Poincaré age pela ação afim x ↦ Λx + a; o eixo ℕ é a isotonia
  (caudas ∞-dim do v106);
* ★★ `thePoincareNet` — PhysicalNetData com G = PoincareGroup: as DEZ
  direções agem nas regiões; a fibra representa o setor DESCONEXO
  (det Λ = −1 ⟹ flip genuíno; det Λ = 1 ⟹ identidade);
* ★★★ `thePoincareWitness : FullWitnessData` — A TESTEMUNHA COM O
  GRUPO DE POINCARÉ GENUÍNO habitada, sob nome NÃO-reservado (lei de
  grupo, monotonia, não-trivialidade, lei do fluxo, covariância);
* ★★ `poincare_witness_fiber_sensitive` — A FIBRA SENTE POINCARÉ:
  a PARIDADE (0, P) FIXA a região da origem e MOVE a fibra
  (flip e₀ = −e₀ ≠ e₀) — o teste do v114, agora com o grupo real;
* ★★ `poincare_witness_boost_moves` — o BOOST move as regiões
  (sinh χ ≠ 0); ★★ `poincare_witness_faithful` — quem fixa TODAS as
  regiões é a identidade: NENHUMA das dez direções é cega na rede;
* ★ `proper_sector_fibers_blind` — HONESTIDADE COMO TEOREMA: neste
  habitante o setor próprio (det = 1) age trivialmente nas fibras — a
  representação fibrada fatora pela paridade. A representação unitária
  FIEL do setor conexo é ∞-dim (não há rep unitária f.d. de boosts) e
  segue NOMEADA com III₁: é exatamente o resíduo do V2, que continua
  RESERVADO (lição v103, sétima aplicação).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped Classical

noncomputable section

/-! ## A — a região de Poincaré e a ação afim -/

/-- a região: base = ponto do espaço-tempo ℝ⁴; profundidade = isotonia. -/
abbrev PoinRegion : Type := (Fin 4 → ℝ) × ℕ

/-- a ordem: mesma base; cauda mais funda ⊆ mais rasa. -/
def poinLe (O₁ O₂ : PoinRegion) : Prop := O₁.1 = O₂.1 ∧ O₂.2 ≤ O₁.2

/-- as fibras: as caudas ∞-dim do v106. -/
abbrev poinFiber (O : PoinRegion) : Type := tailSub O.2

/-- a ação nas regiões: Poincaré age na base, preserva a profundidade. -/
def poinAct (g : PoincareGroup) (O : PoinRegion) : PoinRegion :=
  (pAct g O.1, O.2)

theorem poinAct_one (O : PoinRegion) : poinAct 1 O = O := by
  unfold poinAct
  rw [pAct_one]

theorem poinAct_mul (g h : PoincareGroup) (O : PoinRegion) :
    poinAct (g * h) O = poinAct g (poinAct h O) := by
  unfold poinAct
  rw [pAct_mul]

theorem poinAct_mono (g : PoincareGroup) {O₁ O₂ : PoinRegion}
    (h : poinLe O₁ O₂) : poinLe (poinAct g O₁) (poinAct g O₂) :=
  ⟨by unfold poinAct; rw [h.1], h.2⟩

/-! ## B — a rede de Poincaré (fibra = setor desconexo) -/

/-- [KERNEL] ★★ A REDE DE POINCARÉ: as dez direções agem nas regiões;
    a fibra representa o setor desconexo (paridade ⟹ flip). -/
@[reducible] def thePoincareNet :
    PhysicalNetData PoinRegion poinLe poinFiber poinFiber where
  net :=
    { locks := fun O => tailLock O.2
      internal := fun O s => lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s
      internalW := fun O s =>
        (lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s).toLinearIsometry
      internal_intertwines := fun O s x =>
        lockFlow_commutes (tailLock O.2) (tailLock_selfadjoint O.2) s x
      G := PoincareGroup
      act := poinAct
      external := fun g O =>
        if g.lor.1.det = 1 then LinearIsometryEquiv.refl ℂ _
        else tailFlip O.2
      externalW := fun g O =>
        if g.lor.1.det = 1 then
          (LinearIsometryEquiv.refl ℂ _).toLinearIsometry
        else (tailFlip O.2).toLinearIsometry
      external_intertwines := fun g O x => by
        by_cases hdet : g.lor.1.det = 1
        · simp only [hdet, if_pos]
          rfl
        · simp only [hdet, if_neg, not_false_iff]
          exact Subtype.ext (by
            show eraseFirst (theFlip (x : ellTwo))
              = theFlip (eraseFirst (x : ellTwo))
            calc eraseFirst (theFlip (x : ellTwo))
                = (eraseFirst * theFlip) (x : ellTwo) := rfl
              _ = (theFlip * eraseFirst) (x : ellTwo) := by
                  rw [theFlip_comm_eraseFirst]
              _ = theFlip (eraseFirst (x : ellTwo)) := rfl)
      incl := fun h => tailIncl h.2
      inclW := fun h => tailIncl h.2
      incl_intertwines := fun _ x => Subtype.ext rfl }
  genuinely_isotone :=
    ⟨((fun _ => 0 : Fin 4 → ℝ), 1), ((fun _ => 0 : Fin 4 → ℝ), 0),
      ⟨rfl, Nat.zero_le 1⟩, tailIncl_not_surjective⟩
  external_nontrivial := by
    show Nontrivial PoincareGroup
    refine ⟨⟨⟨(fun _ => 1 : Fin 4 → ℝ), 1⟩, 1, fun h => ?_⟩⟩
    have htr := congrArg PoincareGroup.tr h
    have h0 := congrArg (fun v : Fin 4 → ℝ => v 0) htr
    simp only [poincare_one_tr] at h0
    norm_num at h0

/-! ## C — o certificado forte e A TESTEMUNHA -/

/-- o certificado forte sobre a rede de Poincaré. -/
@[reducible] def thePoincareStrong : QGClosureCertificateStrong where
  Region := PoinRegion
  leR := poinLe
  H := poinFiber
  W := poinFiber
  core := thePoincareNet
  core_infinite := ⟨((fun _ => 0 : Fin 4 → ℝ), 0), tailSub_not_finiteDimensional 0⟩
  ℍ := ellTwo
  dirac := theGenuineDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := genuineDirac_corner_pos
  corner_finite := genuineDirac_corner_finite
  frame := theCurvedFrame
  frame_nonconstant := curvedFrame_nonconstant

/-- [KERNEL] ★★★ A TESTEMUNHA DE POINCARÉ: FullWitnessData com o GRUPO
    DE POINCARÉ genuíno (as dez direções) — sob nome NÃO-reservado
    (o V2 segue reservado: falta a rep unitária fiel do setor conexo
    e o fator III₁). -/
def thePoincareWitness : FullWitnessData where
  toQGClosureCertificateStrong := thePoincareStrong
  act_one := fun O => poinAct_one O
  act_mul := fun g h O => poinAct_mul g h O
  act_mono := fun g {O₁ O₂} h => poinAct_mono g h
  geometric_nontrivial := by
    dsimp only [thePoincareStrong, thePoincareNet]
    refine ⟨⟨(fun _ => 1 : Fin 4 → ℝ), 1⟩,
      ((fun _ => 0 : Fin 4 → ℝ), 0), fun h => ?_⟩
    have hfst := congrArg Prod.fst h
    have h0 := congrArg (fun v : Fin 4 → ℝ => v 0) hfst
    unfold poinAct pAct at h0
    simp only [lorentzGrp_one_val, Matrix.one_mulVec] at h0
    norm_num at h0
  flow_law := fun O s t x =>
    lockFlow_add (tailLock O.2) (tailLock_selfadjoint O.2) s t x
  covariant_inclusions := fun g {O₁ O₂} hle x => by
    by_cases hdet : g.lor.1.det = 1
    · dsimp only [thePoincareStrong, thePoincareNet]
      simp only [hdet, if_pos]
      exact Subtype.ext rfl
    · dsimp only [thePoincareStrong, thePoincareNet]
      simp only [hdet, if_neg, not_false_iff]
      exact Subtype.ext rfl

/-! ## D — os teoremas: a fibra sente, o boost move, ninguém é cego -/

/-- o elemento de paridade em Poincaré: (0, P). -/
def parityElement : PoincareGroup := ⟨0, theParity⟩

/-- [KERNEL] ★ a paridade FIXA a região da origem. -/
theorem parity_fixes_origin :
    poinAct parityElement ((0 : Fin 4 → ℝ), (0 : ℕ))
      = ((0 : Fin 4 → ℝ), (0 : ℕ)) := by
  unfold poinAct pAct parityElement
  rw [Matrix.mulVec_zero]
  simp

/-- [KERNEL] ★★ A FIBRA SENTE POINCARÉ: a paridade (0, P) — det = −1,
    o setor desconexo — fixa a região da origem e MOVE a fibra
    (flip e₀ = −e₀ ≠ e₀). O v114 tinha o flip de brinquedo; agora é o
    grupo REAL. -/
theorem poincare_witness_fiber_sensitive :
    thePoincareNet.net.external parityElement
        ((fun _ => 0 : Fin 4 → ℝ), (0 : ℕ)) e0tail ≠ e0tail := by
  dsimp only [thePoincareNet]
  have hne : parityElement.lor.1.det ≠ 1 := by
    unfold parityElement
    rw [parity_det]
    norm_num
  simp only [hne, if_neg, not_false_iff]
  intro h
  have hcoe := congrArg Subtype.val h
  have hflip : theFlip (firstInscription : ellTwo) = -firstInscription := by
    have hP : firstAtom.starProjection (firstInscription : ellTwo)
        = firstInscription :=
      Submodule.starProjection_eq_self_iff.mpr
        (Submodule.mem_span_singleton_self _)
    show (firstInscription : ellTwo) - firstAtom.starProjection firstInscription
        - firstAtom.starProjection firstInscription = -firstInscription
    rw [hP]
    abel
  have h2 : (-firstInscription : ellTwo) = firstInscription := by
    calc (-firstInscription : ellTwo)
        = theFlip firstInscription := hflip.symm
      _ = firstInscription := hcoe
  have h3 : (firstInscription : ellTwo) + firstInscription = 0 := by
    nth_rewrite 2 [← h2]
    simp
  have h4 : (firstInscription : ellTwo) = 0 := by
    have h5 : (2 : ℂ) • (firstInscription : ellTwo) = 0 := by
      rw [two_smul]
      exact h3
    have h6 := congrArg (fun y => (2 : ℂ)⁻¹ • y) h5
    simpa [smul_smul] using h6
  exact (inscriptions_orthonormal.ne_zero 0) h4

/-- [KERNEL] ★★ O BOOST MOVE AS REGIÕES: χ ≠ 0 ⟹ (0, B(χ)) desloca a
    região baseada em e₀ (a entrada sinh χ da coluna 0 não é nula). -/
theorem poincare_witness_boost_moves (χ : ℝ) (hχ : χ ≠ 0) :
    poinAct ⟨0, theBoost χ⟩ ((Pi.single (0 : Fin 4) 1 : Fin 4 → ℝ), (0 : ℕ))
      ≠ ((Pi.single (0 : Fin 4) 1 : Fin 4 → ℝ), (0 : ℕ)) := by
  intro h
  have hfst := congrArg Prod.fst h
  unfold poinAct pAct at hfst
  have h1 := congrArg (fun v : Fin 4 → ℝ => v 1) hfst
  simp only [Pi.add_apply] at h1
  have hmv : (theBoost χ).1.mulVec (Pi.single (0 : Fin 4) 1)
      = fun i => (theBoost χ).1 i 0 := by
    rw [Matrix.mulVec_single_one]
    rfl
  rw [hmv] at h1
  have hb10 : (theBoost χ).1 1 0 = Real.sinh χ := by
    show boostMat χ 1 0 = Real.sinh χ
    unfold boostMat
    simp
  have hs0 : (Pi.single (0 : Fin 4) 1 : Fin 4 → ℝ) 1 = 0 := by
    rw [Pi.single_eq_of_ne]
    decide
  simp only [hb10, hs0, Pi.zero_apply, add_zero] at h1
  exact (Real.sinh_ne_zero.mpr hχ) h1

/-- [KERNEL] ★★ NENHUMA DIREÇÃO É CEGA: quem fixa TODAS as regiões da
    rede é a identidade de Poincaré (a fidelidade desce à rede). -/
theorem poincare_witness_faithful (g : PoincareGroup)
    (h : ∀ O : PoinRegion, poinAct g O = O) : g = 1 := by
  apply poincare_faithful
  intro x
  have hx := h (x, 0)
  have hfst := congrArg Prod.fst hx
  exact hfst

/-- [KERNEL] ★ HONESTIDADE COMO TEOREMA: o setor PRÓPRIO (det = 1) age
    trivialmente nas fibras — a rep fibrada deste habitante fatora pela
    paridade; a rep unitária FIEL do setor conexo (∞-dim, sem versão
    f.d.) + III₁ = o resíduo NOMEADO do V2 reservado. -/
theorem proper_sector_fibers_blind (g : PoincareGroup)
    (hdet : g.lor.1.det = 1) (O : PoinRegion) :
    thePoincareNet.net.external g O = LinearIsometryEquiv.refl ℂ _ := by
  dsimp only [thePoincareNet]
  simp only [hdet, if_pos]

end

end TGLExt
