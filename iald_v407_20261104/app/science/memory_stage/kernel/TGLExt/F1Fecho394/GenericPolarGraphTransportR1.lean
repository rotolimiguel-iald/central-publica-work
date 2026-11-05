import TGLExt.F1Fecho394.CoefficientTomitaSquareR2

/-! Generic graph elimination before substitution of the concrete Fock GNS.
The root graph equality is a premise here; the concrete caller proves it. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericPolarGraphTransport
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

theorem root_to_polar_graph (T : H →ₗ.[ℂ] H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x y : H) (h : (x,y) ∈ T.graph) :
    (x,J y) ∈ CoefficientTomitaSquare.graph T J := by
  obtain ⟨w,hw,hy⟩ := (LinearPMap.mem_graph_iff T).mp h
  exact ⟨w,Prod.ext hw (congrArg J hy)⟩

theorem mapped_domain_of_polar_graph (V : H ≃ₗᵢ[ℂ] E)
    (T : H →ₗ.[ℂ] H) (U : E →ₗ.[ℂ] E)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hroot : ∀ x y, (V x,V y) ∈ U.graph ↔ (x,y) ∈ T.graph)
    (x y : H) (h : (x,y) ∈ CoefficientTomitaSquare.graph T J) :
    V x ∈ U.domain := by
  obtain ⟨w,hw⟩ := h
  have hx : (w:H)=x := congrArg Prod.fst hw
  have hg := (hroot (w:H) (T w)).mpr
    ((LinearPMap.mem_graph_iff T).mpr ⟨w,rfl,rfl⟩)
  obtain ⟨z,hz,_⟩ := (LinearPMap.mem_graph_iff U).mp hg
  exact Eq.mp (congrArg (fun a : E => a ∈ U.domain)
    (hz.trans (congrArg V hx))) z.property

end F1Fecho.GenericPolarGraphTransport
#print axioms F1Fecho.GenericPolarGraphTransport.root_to_polar_graph
#print axioms F1Fecho.GenericPolarGraphTransport.mapped_domain_of_polar_graph
