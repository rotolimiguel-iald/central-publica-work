import TGLExt.GenericAntilinearAdjoint
/-! The upper-boundary exchange used after spectral-strip analyticity.
This is a Hilbert-space identity, using the genuine antiunitary and commuting
unitary. Application to a Weyl/vacuum pair must supply its actual half-modular
domain and the identities G(A*Omega)=J(AOmega), G(BOmega)=J(B*Omega). -/
set_option autoImplicit false
namespace F1Fecho.KMSBoundaryExchange
open ChatgptAudit.Continuous050
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem exchange (J : H ≃ₗᵢ⋆[ℂ] H) (u : H ≃ₗᵢ[ℂ] H)
    (hcomm : ∀ x, u (J x)=J (u x)) (x y : H) :
    inner ℂ (J x) (u (J y)) = inner ℂ y (u.symm x) := by
  rw [hcomm,antiunitary_inner_conj]
  change (starRingEnd ℂ) (inner ℂ x (u y)) = _
  rw [inner_conj_symm]
  conv_lhs => rw [← u.apply_symm_apply x]
  exact u.inner_map_map y (u.symm x)

theorem exchange_from_pair_values (J : H ≃ₗᵢ⋆[ℂ] H) (u : H ≃ₗᵢ[ℂ] H)
    (hcomm : ∀ x, u (J x)=J (u x)) (a b gaStar gb : H)
    (ha : gaStar=J a) (hb : gb=J b) :
    inner ℂ gaStar (u gb) = inner ℂ b (u.symm a) := by
  rw [ha,hb]
  exact exchange J u hcomm a b

end F1Fecho.KMSBoundaryExchange
#print axioms F1Fecho.KMSBoundaryExchange.exchange
#print axioms F1Fecho.KMSBoundaryExchange.exchange_from_pair_values
