import TGLExt.V350PartialOperatorSquare

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The square identity transfers energy on the full domain of the square. -/
theorem partialSquare_energy (B A : H →ₗ.[ℂ] H) (hs : B.IsFormalAdjoint B)
    (hsq : partialOperatorSquare B=A) (x : A.domain) :
    ∃ u : B.domain, (u : H)=(x : H) ∧ ‖B u‖^2=(inner ℂ (x : H) (A x)).re := by
  have hg : ((x : H),A x) ∈ (partialOperatorSquare B).graph := by
    rw [hsq]
    exact A.mem_graph x
  obtain ⟨z,hxz,hzA⟩ := (partialOperatorSquare_graph_iff B _ _).mp hg
  obtain ⟨u,hu,hBu⟩ := (LinearPMap.mem_graph_iff B).mp hxz
  obtain ⟨v,hv,hBv⟩ := (LinearPMap.mem_graph_iff B).mp hzA
  dsimp only [Prod.fst,Prod.snd] at hu hBu hv hBv
  have hi := hs u v
  rw [hBu,hv,hu,hBv] at hi
  have hr := congrArg Complex.re hi
  have hn : (inner ℂ z z).re=‖z‖^2 := (norm_sq_eq_re_inner (𝕜 := ℂ) z).symm
  refine ⟨u,hu,?_⟩
  rw [hBu]
  exact hn.symm.trans hr

#print axioms partialSquare_energy
end
end TGLV350.Regular
