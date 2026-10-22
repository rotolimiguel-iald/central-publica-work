import TGLExt.V351ModularCutBalance
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    let π := scalarGNSRepresentation P
    let J := scalarTomitaPolarFactor P
    let C := π ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    let D := antiunitaryConjugate J
      (π ⟨regularInverseGeneratorCutoff P η,regularInverseGeneratorCutoff_mem P η⟩)
    scalarTomitaResolvent P*C*antiunitaryConjugate J (π (regularDomainCut P η)) =
      scalarTomitaResolvent P * π (regularDomainCut P ε) * D :=
  (scalarTomitaResolvent_double_cut_balance P ε η hε hη).2.2
