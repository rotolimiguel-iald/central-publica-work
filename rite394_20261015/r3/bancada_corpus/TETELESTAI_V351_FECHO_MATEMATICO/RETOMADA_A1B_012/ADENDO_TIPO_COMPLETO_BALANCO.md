[REAL — correção documental ao lado]

O extrator anterior parou no primeiro let := do resultado. O auditor Lean já imprimiu o enunciado inteiro e o código passou. Nenhuma fonte Lean, olean ou resultado de teste foi alterado ou reexecutado. A auditoria anterior é preservada, com seu pin; o consumidor deve usar AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json.

```lean
theorem scalarTomitaResolvent_double_cut_balance (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    let π := scalarGNSRepresentation P
    let J := scalarTomitaPolarFactor P
    let C := π ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    let D := antiunitaryConjugate J
      (π ⟨regularInverseGeneratorCutoff P η,regularInverseGeneratorCutoff_mem P η⟩)
    Commute (scalarTomitaResolvent P) C ∧ Commute (scalarTomitaResolvent P) D ∧
      (1-scalarTomitaResolvent P)*C*antiunitaryConjugate J (π (regularDomainCut P η)) =
        scalarTomitaResolvent P * π (regularDomainCut P ε) * D
```
