import TGLExt
set_option autoImplicit false

-- Revisor terceiro v406 (agente Claude Sonnet): #print axioms das oito ancoras (DL.ANCORAS) + exemplos proprios que instanciam o certificado e a testemunha canonica.

#print axioms F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput
#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physicalModularCoreInput
#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate
#print axioms F1Fecho.CanonicalFockModularCoreInputR1.physical_trace
#print axioms F1Fecho.MaxwellLocalization.physicalCanonicalNet
#print axioms F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero
#print axioms TGL.ModularRealization.canonicalFullTGLWitness
#print axioms TGL.ModularRealization.canonical_full_witness_inhabited

-- exemplos do revisor: instanciam o certificado e a testemunha (nao dependem dos teoremas da candidata)
noncomputable def revisorCertificado :=
  F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate
#print axioms revisorCertificado

noncomputable def revisorTestemunha : TGL.ModularRealization.FullTGLWitness :=
  TGL.ModularRealization.canonicalFullTGLWitness
#print axioms revisorTestemunha

example : Nonempty TGL.ModularRealization.FullTGLWitness :=
  ⟨TGL.ModularRealization.canonicalFullTGLWitness⟩

-- a montagem: a primeira componente da testemunha e' a rede da luz sobre o certificado fisico (rfl)
theorem revisor_fst :
    TGL.ModularRealization.canonicalFullTGLWitness.1
      = TGLExt.ImportedSQ.lightNet F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate := rfl
#print axioms revisor_fst

-- o traco do certificado fisico e' o traco ciclico candidato (rfl)
theorem revisor_trace :
    F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate.trace
      = F1Fecho.CanonicalFockCyclicTraceCompletionR3.cyclicTraceCandidate := rfl
#print axioms revisor_trace
