import TGLExt.GravitonReading

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# OS ESTILHAÇOS DO CONTÍNUO: a onda do gráviton e a fibra que sente
  [TGLExt — v114, o incremento 35 do programa SemifiniteAnalysis]

Mandato: "resolva Poincaré e o contínuo". As duas paredes ENCOLHEM:

PAREDE DO CONTÍNUO: ★★★ `graviton_wave_equation` — para QUALQUER
perfil w duas vezes derivável, h(x) = w(x₁−x₀) satisfaz ∂₀²h = ∂₁²h
EM TODA PARTE: a EQUAÇÃO DE ONDA no contínuo — propagação à
velocidade da luz, provada. [Resta: TT/ghost-free contínuos — a
polarização é a face finita v75.]

PAREDE DE POINCARÉ: ★★ `theSensitiveWitness : FullWitnessData` — o
grupo Mult ℤ × Mult (ZMod 2): ℤ TRANSLADA regiões; ZMod 2 implementa
o FLIP nas fibras FIXANDO a região; ★★ `witness_fiber_sensitive` — o
elemento (1, flip) fixa a região e MOVE a fibra (flip e₀ = −e₀ ≠ e₀):
A FIBRA SENTE O GRUPO. [Resta: Poincaré 10-dim + endurecimento geral
com transporte + III₁.]

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a onda do gráviton no contínuo -/

/-- a derivada parcial direcional sobre ℝ⁴. -/
def pd (i : Fin 4) (f : (Fin 4 → ℝ) → ℝ) (x : Fin 4 → ℝ) : ℝ :=
  fderiv ℝ f x (Pi.single i 1)

/-- o funcional do cone de luz: L(x) = x₁ − x₀ (linear contínuo). -/
def lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (1 : Fin 4))
    - (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : Fin 4 => ℝ) (0 : Fin 4))

theorem lightCone_apply (x : Fin 4 → ℝ) : lightCone x = x 1 - x 0 := by
  unfold lightCone
  simp [ContinuousLinearMap.sub_apply]

theorem lightCone_single_zero :
    lightCone (Pi.single (0 : Fin 4) 1) = -1 := by
  rw [lightCone_apply]
  simp

theorem lightCone_single_one :
    lightCone (Pi.single (1 : Fin 4) 1) = 1 := by
  rw [lightCone_apply]
  simp

/-- a onda unidirecional: h(x) = w(x₁ − x₀). -/
def lightWave (w : ℝ → ℝ) (x : Fin 4 → ℝ) : ℝ := w (lightCone x)

/-- [KERNEL] ★ a derivada parcial da onda: ∂ᵢh = w′(L x)·L(eᵢ). -/
theorem lightWave_pd (w w' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u) (i : Fin 4) (x : Fin 4 → ℝ) :
    pd i (lightWave w) x = w' (lightCone x) * lightCone (Pi.single i 1) := by
  unfold pd
  have h : HasFDerivAt (lightWave w)
      ((w' (lightCone x)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)) x :=
    (hw (lightCone x)).comp_hasFDerivAt x lightCone.hasFDerivAt
  rw [h.fderiv]
  simp [smul_eq_mul]

/-- [KERNEL] ★★★ A EQUAÇÃO DE ONDA DO GRÁVITON NO CONTÍNUO: para
    qualquer perfil w duas vezes derivável, h = w(x₁−x₀) satisfaz
    ∂₀²h = ∂₁²h em toda parte — propagação à velocidade da luz. -/
theorem graviton_wave_equation (w w' w'' : ℝ → ℝ)
    (hw : ∀ u, HasDerivAt w (w' u) u)
    (hw' : ∀ u, HasDerivAt w' (w'' u) u) (x : Fin 4 → ℝ) :
    pd 0 (pd 0 (lightWave w)) x = pd 1 (pd 1 (lightWave w)) x := by
  have hfun : ∀ i : Fin 4, pd i (lightWave w)
      = fun y => lightCone (Pi.single i 1) * lightWave w' y := by
    intro i
    funext y
    rw [lightWave_pd w w' hw i y]
    unfold lightWave
    ring
  have hpd2 : ∀ (j : Fin 4) (c : ℝ),
      pd j (fun y => c * lightWave w' y) x
        = c * (w'' (lightCone x) * lightCone (Pi.single j 1)) := by
    intro j c
    unfold pd
    have hf : HasFDerivAt (fun y => c * lightWave w' y)
        (c • ((w'' (lightCone x)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ))) x := by
      have hbase : HasFDerivAt (lightWave w')
          ((w'' (lightCone x)) • (lightCone : (Fin 4 → ℝ) →L[ℝ] ℝ)) x :=
        (hw' (lightCone x)).comp_hasFDerivAt x lightCone.hasFDerivAt
      exact hbase.const_smul c
    rw [hf.fderiv]
    simp [smul_eq_mul]
    try ring
  rw [hfun 0, hfun 1, hpd2 0 (lightCone (Pi.single (0 : Fin 4) 1)),
    hpd2 1 (lightCone (Pi.single (1 : Fin 4) 1)),
    lightCone_single_zero, lightCone_single_one]
  ring

/-! ## B — a fibra que sente o grupo -/

/-- [KERNEL] ★★ A REDE SENSÍVEL: Mult ℤ translada as regiões; Mult
    (ZMod 2) implementa o FLIP nas fibras fixando a região. -/
@[reducible] def theSensitiveNet :
    PhysicalNetData GeoRegion geoLe geoFiber geoFiber where
  net :=
    { locks := fun O => tailLock O.2
      internal := fun O s => lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s
      internalW := fun O s =>
        (lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s).toLinearIsometry
      internal_intertwines := fun O s x =>
        lockFlow_commutes (tailLock O.2) (tailLock_selfadjoint O.2) s x
      G := Multiplicative ℤ × Multiplicative (ZMod 2)
      act := fun g O => (O.1 + Multiplicative.toAdd g.1, O.2)
      external := fun g O =>
        if Multiplicative.toAdd g.2 = (0 : ZMod 2) then
          LinearIsometryEquiv.refl ℂ _
        else tailFlip O.2
      externalW := fun g O =>
        if Multiplicative.toAdd g.2 = (0 : ZMod 2) then
          (LinearIsometryEquiv.refl ℂ _).toLinearIsometry
        else (tailFlip O.2).toLinearIsometry
      external_intertwines := fun g O x => by
        by_cases h2 : Multiplicative.toAdd g.2 = (0 : ZMod 2)
        · simp only [h2, if_pos]
          rfl
        · simp only [h2, if_neg, not_false_iff]
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
    ⟨((0 : ℤ), 1), ((0 : ℤ), 0), ⟨rfl, Nat.zero_le 1⟩,
      tailIncl_not_surjective⟩
  external_nontrivial := by
    show Nontrivial (Multiplicative ℤ × Multiplicative (ZMod 2))
    infer_instance

/-- o certificado forte sobre a rede sensível. -/
@[reducible] def theSensitiveStrong : QGClosureCertificateStrong where
  Region := GeoRegion
  leR := geoLe
  H := geoFiber
  W := geoFiber
  core := theSensitiveNet
  core_infinite := ⟨((0 : ℤ), 0), tailSub_not_finiteDimensional 0⟩
  ℍ := ellTwo
  dirac := theGenuineDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := genuineDirac_corner_pos
  corner_finite := genuineDirac_corner_finite
  frame := theCurvedFrame
  frame_nonconstant := curvedFrame_nonconstant

/-- [KERNEL] ★★ A TESTEMUNHA SENSÍVEL: FullWitnessData com o grupo
    duplo — a geometria no fator ℤ, a sensibilidade da fibra no fator
    ZMod 2 — sob nome NÃO-reservado. -/
def theSensitiveWitness : FullWitnessData where
  toQGClosureCertificateStrong := theSensitiveStrong
  act_one := fun O => geo_act_one O
  act_mul := fun g h O => geo_act_mul g.1 h.1 O
  act_mono := fun g {O₁ O₂} h => geo_act_mono g.1 h
  geometric_nontrivial := by
    dsimp only [theSensitiveStrong, theSensitiveNet]
    exact ⟨(Multiplicative.ofAdd 1, 1), ((0 : ℤ), (0 : ℕ)), geo_nontrivial⟩
  flow_law := fun O s t x =>
    lockFlow_add (tailLock O.2) (tailLock_selfadjoint O.2) s t x
  covariant_inclusions := fun g {O₁ O₂} hle x => by
    by_cases h2 : Multiplicative.toAdd g.2 = (0 : ZMod 2)
    · dsimp only [theSensitiveStrong, theSensitiveNet]
      simp only [h2, if_pos]
      exact Subtype.ext rfl
    · dsimp only [theSensitiveStrong, theSensitiveNet]
      simp only [h2, if_neg, not_false_iff]
      exact Subtype.ext rfl

/-- e₀ como habitante da cauda 0. -/
def e0tail : tailSub 0 :=
  ⟨firstInscription, fun k hk => absurd hk (Nat.not_lt_zero k)⟩

/-- [KERNEL] ★★ A FIBRA SENTE O GRUPO: o elemento (1, flip) FIXA a
    região e MOVE a fibra — flip e₀ = −e₀ ≠ e₀. -/
theorem witness_fiber_sensitive :
    theSensitiveNet.net.external
        ((1 : Multiplicative ℤ), Multiplicative.ofAdd (1 : ZMod 2))
        ((0 : ℤ), (0 : ℕ)) e0tail ≠ e0tail := by
  dsimp only [theSensitiveNet]
  have hne : Multiplicative.toAdd (Multiplicative.ofAdd (1 : ZMod 2))
      ≠ (0 : ZMod 2) := by decide
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

end

end TGLExt
