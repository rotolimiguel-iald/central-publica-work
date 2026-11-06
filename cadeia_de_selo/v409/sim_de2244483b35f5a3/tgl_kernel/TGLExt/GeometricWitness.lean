import TGLExt.ReducedEmergence

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA GEOMÉTRICA: a metade tipável de FullWitnessData HABITADA
  [TGLExt — v112, o incremento 33 do programa SemifiniteAnalysis]

A parede da testemunha (v104) pedia AÇÃO GEOMÉTRICA genuína nas
regiões + covariância + lei do fluxo. Esta pedra a habita:

* Region := ℤ × ℕ — o eixo ℤ é GEOMÉTRICO (o grupo ℤ TRANSLADA:
  act g (a,i) = (a+g, i) — genuinamente não-trivial: gO ≠ O para
  g ≠ 0); o eixo ℕ é a ISOTONIA (fibras-caudas ∞-dim do v106,
  inclusões genuinamente não-sobrejetivas);
* locks = restrições de T = 1−P₀ às caudas (v106); fluxo GENUÍNO
  exp(isT) por fibra com a LEI do v102 (lockFlow_add) — `flow_law`
  PROVADA; covariância U∘ι = ι∘U exata;
* ★★★ `theGeometricWitness : FullWitnessData` — A METADE TIPÁVEL DA
  TESTEMUNHA COMPLETA TEM HABITANTE, sob nome NÃO-reservado (a ordem
  do rito);
* ★ `witness_action_moves_regions_not_fibers` — A HONESTIDADE COMO
  TEOREMA: neste habitante a ação move as REGIÕES mas as fibras não a
  sentem (H(gO) = H(O) por construção) — a ação é geométrica no
  índice, não dinâmica nas fibras.

O QUE AINDA FALTA (a parede, encolhida e nomeada): ação
FIBRO-SENSÍVEL de um grupo de POINCARÉ genuíno + fator III₁ +
H3-derivado + spin-2 contínuo — o espírito inteiro do
`qgClosureCertificateV2`, que segue RESERVADO (lição v103, quarta
aplicação). β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a região geométrica e as fibras -/

/-- a região: o eixo ℤ é geométrico (translação); o eixo ℕ é a
    profundidade da cauda (isotonia). -/
abbrev GeoRegion : Type := ℤ × ℕ

/-- a ordem: mesma posição geométrica; cauda mais funda ⊆ mais rasa. -/
def geoLe (O₁ O₂ : GeoRegion) : Prop := O₁.1 = O₂.1 ∧ O₂.2 ≤ O₁.2

/-- as fibras: as caudas ∞-dim do v106, pela profundidade. -/
abbrev geoFiber (O : GeoRegion) : Type := tailSub O.2

/-! ## B — a rede geométrica -/

/-- [KERNEL] ★★ A REDE GEOMÉTRICA: PhysicalNetData com o grupo
    Multiplicative ℤ TRANSLADANDO as regiões (genuinamente
    não-trivial) e isotonia genuína nas caudas. -/
@[reducible] def theGeometricNet :
    PhysicalNetData GeoRegion geoLe geoFiber geoFiber where
  net :=
    { locks := fun O => tailLock O.2
      internal := fun O s => lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s
      internalW := fun O s =>
        (lockFlow (tailLock O.2) (tailLock_selfadjoint O.2) s).toLinearIsometry
      internal_intertwines := fun O s x =>
        lockFlow_commutes (tailLock O.2) (tailLock_selfadjoint O.2) s x
      G := Multiplicative ℤ
      act := fun g O => (O.1 + Multiplicative.toAdd g, O.2)
      external := fun _ _ => LinearIsometryEquiv.refl ℂ _
      externalW := fun _ _ => (LinearIsometryEquiv.refl ℂ _).toLinearIsometry
      external_intertwines := fun _ _ _ => rfl
      incl := fun h => tailIncl h.2
      inclW := fun h => tailIncl h.2
      incl_intertwines := fun _ x => Subtype.ext rfl }
  genuinely_isotone :=
    ⟨((0 : ℤ), 1), ((0 : ℤ), 0), ⟨rfl, Nat.zero_le 1⟩,
      tailIncl_not_surjective⟩
  external_nontrivial := inferInstanceAs (Nontrivial (Multiplicative ℤ))

/-! ## C — o certificado forte geométrico e A TESTEMUNHA -/

/-- o certificado FORTE sobre a rede geométrica (Dirac genuíno v105 +
    canto do Nome + frame curvo v104). -/
@[reducible] def theGeometricStrong : QGClosureCertificateStrong where
  Region := GeoRegion
  leR := geoLe
  H := geoFiber
  W := geoFiber
  core := theGeometricNet
  core_infinite := ⟨((0 : ℤ), 0), tailSub_not_finiteDimensional 0⟩
  ℍ := ellTwo
  dirac := theGenuineDirac
  home_infinite := ellTwo_not_finiteDimensional
  corner_pos := genuineDirac_corner_pos
  corner_finite := genuineDirac_corner_finite
  frame := theCurvedFrame
  frame_nonconstant := curvedFrame_nonconstant

/-- [KERNEL] ★★★ A METADE TIPÁVEL DA TESTEMUNHA COMPLETA HABITADA:
    ação geométrica de GRUPO genuína (ℤ translada as regiões), lei de
    grupo, monotonia, LEI DO FLUXO (v102) e covariância exata — sob
    nome NÃO-reservado (a ordem do rito; o V2 segue reservado). -/
theorem geo_act_one (O : GeoRegion) :
    ((O.1 + Multiplicative.toAdd (1 : Multiplicative ℤ), O.2) : GeoRegion)
      = O := by
  simp

theorem geo_act_mul (g h : Multiplicative ℤ) (O : GeoRegion) :
    ((O.1 + Multiplicative.toAdd (g * h), O.2) : GeoRegion)
      = ((O.1 + Multiplicative.toAdd h) + Multiplicative.toAdd g, O.2) := by
  have hm : Multiplicative.toAdd (g * h)
      = Multiplicative.toAdd g + Multiplicative.toAdd h := rfl
  rw [hm]
  simp only [Prod.mk.injEq]
  refine ⟨by ring, ?_⟩
  try rfl
  try trivial

theorem geo_act_mono (g : Multiplicative ℤ) {O₁ O₂ : GeoRegion}
    (h : geoLe O₁ O₂) :
    geoLe (O₁.1 + Multiplicative.toAdd g, O₁.2)
      (O₂.1 + Multiplicative.toAdd g, O₂.2) :=
  ⟨by rw [h.1], h.2⟩

theorem geo_nontrivial :
    (((0 : ℤ) + Multiplicative.toAdd (Multiplicative.ofAdd (1 : ℤ)),
      (0 : ℕ)) : GeoRegion) ≠ (((0 : ℤ), (0 : ℕ)) : GeoRegion) := by
  intro h
  have h1 := congrArg Prod.fst h
  simp at h1

def theGeometricWitness : FullWitnessData where
  toQGClosureCertificateStrong := theGeometricStrong
  act_one := fun O => geo_act_one O
  act_mul := fun g h O => geo_act_mul g h O
  act_mono := fun g {O₁ O₂} h => geo_act_mono g h
  geometric_nontrivial := by
    dsimp only [theGeometricStrong, theGeometricNet]
    exact ⟨Multiplicative.ofAdd 1, ((0 : ℤ), (0 : ℕ)), geo_nontrivial⟩
  flow_law := fun O s t x =>
    lockFlow_add (tailLock O.2) (tailLock_selfadjoint O.2) s t x
  covariant_inclusions := fun g {O₁ O₂} hle x => Subtype.ext rfl

/-- [KERNEL] ★ A HONESTIDADE COMO TEOREMA: neste habitante as fibras
    NÃO sentem a translação — a profundidade da cauda é invariante
    (a ação é geométrica no índice; ação FIBRO-SENSÍVEL de Poincaré
    genuíno + III₁ = o espírito restante do V2, RESERVADO). -/
theorem witness_action_moves_regions_not_fibers (g : ℤ) (O : GeoRegion) :
    (theGeometricNet.net.act g O).2 = O.2 := rfl

end

end TGLExt
