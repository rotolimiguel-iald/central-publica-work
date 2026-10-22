import GeometricScreenTransport
import BoundaryEntropyBridge

set_option autoImplicit false
set_option maxHeartbeats 2800000
namespace ChatgptAudit
open Matrix TGLExt Filter Topology
noncomputable section

theorem equal_past_entropy_area_derivatives (entropy area : ℝ → ℝ) (eta t ds da : ℝ)
    (hs : HasDerivAt entropy ds t) (ha : HasDerivAt area da t)
    (h0 : entropy t=eta*area t)
    (he : ∀ᶠ s in 𝓝[<] t, entropy s=eta*area s) : ds=eta*da := by
  have heq : entropy =ᶠ[𝓝[<] t] (fun s => eta*area s) := he
  have hright : HasDerivWithinAt entropy (eta*da) (Set.Iio t) t :=
    (ha.const_mul eta).hasDerivWithinAt.congr_of_eventuallyEq heq h0
  exact (hs.hasDerivWithinAt.derivWithin (uniqueDiffWithinAt_Iio t)).symm.trans
    (hright.derivWithin (uniqueDiffWithinAt_Iio t))

theorem constant_entropy_forces_zero_area_rate (entropy eta : ℝ) (area : ℝ → ℝ)
    (t da : ℝ) (heta : eta≠0) (ha : HasDerivAt area da t)
    (h0 : entropy=eta*area t)
    (he : ∀ᶠ s in 𝓝[<] t, entropy=eta*area s) : da=0 := by
  have hd := equal_past_entropy_area_derivatives (fun _ => entropy) area eta t 0 da
    (hasDerivAt_const t entropy) ha h0 he
  exact (mul_eq_zero.mp hd.symm).resolve_left heta

theorem constant_entropy_forces_zero_expansion (entropy eta theta : ℝ)
    (area : ℝ → ℝ) (t : ℝ) (heta : eta≠0) (harea : area t≠0)
    (ha : HasDerivAt area (theta*area t) t)
    (h0 : entropy=eta*area t)
    (he : ∀ᶠ s in 𝓝[<] t, entropy=eta*area s) : theta=0 := by
  have hz := constant_entropy_forces_zero_area_rate entropy eta area t _ heta ha h0 he
  exact (mul_eq_zero.mp hz).resolve_right harea

theorem fixed_tower_entropy_forces_zero_expansion (P : SiteProfile) (N : ℕ)
    (eta theta : ℝ) (area : ℝ → ℝ) (t : ℝ) (heta : eta≠0) (harea : area t≠0)
    (ha : HasDerivAt area (theta*area t) t)
    (h0 : reducedDiagonalEntropy (towerCutDensity P N)=eta*area t)
    (he : ∀ᶠ s in 𝓝[<] t, reducedDiagonalEntropy (towerCutDensity P N)=eta*area s) : theta=0 :=
  constant_entropy_forces_zero_expansion _ eta theta area t heta harea ha h0 he

theorem finite_entropy_area_rate_constraint {ι : Type} [Fintype ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∑ i, q i=0)
    (eta theta : ℝ) (area : ℝ → ℝ)
    (ha : HasDerivAt area (theta*area 0) 0)
    (h0 : finiteEntropy p=eta*area 0)
    (he : ∀ᶠ s in 𝓝[<] (0:ℝ), finiteEntropy (fun i => p i+s*q i)=eta*area s) :
    (∑ i, q i*(-Real.log (p i)))=eta*theta*area 0 := by
  have hd := equal_past_entropy_area_derivatives
    (fun s => finiteEntropy (fun i => p i+s*q i)) area eta 0 _ _
    (finite_entropy_first_law p q hp hq) ha (by simpa using h0) he
  calc
    _=eta*(theta*area 0) := hd
    _=_ := by ring

theorem geometric_expansion_excludes_frozen_tower_entropy (P : SiteProfile) (N : ℕ)
    (g : ℝ → Tensor4) (S : ℝ → ScreenVectors) (D B F L : Tensor4)
    (h : ScreenMatrix) (t eta : ℝ) (heta : eta≠0) (htrace : Matrix.trace B≠0)
    (hFD : F*D=1) (hgram : Fᵀ*g t*F=nullScreenGram h)
    (hcols : S t=screenColumns F) (hp : 0<h.det)
    (hk : ∀ a, (B*F) a 0=0) (hn : (Fᵀ*g t*B*F) 0 1=0)
    (hg : HasMatrixDerivAt g (Lᵀ*g t+g t*L) t)
    (hS : HasMatrixDerivAt S ((B-L)*S t) t) :
    ¬ (reducedDiagonalEntropy (towerCutDensity P N)=eta*screenArea (screenGram (g t) (S t)) ∧
      ∀ᶠ s in 𝓝[<] t, reducedDiagonalEntropy (towerCutDensity P N)=
        eta*screenArea (screenGram (g s) (S s))) := by
  rintro ⟨h0,he⟩
  have hv : screenGram (g t) (S t)=h := by
    rw [hcols,screen_gram_in_frame,hgram,null_gram_screen_block]
  have ha := geometric_screen_area_derivative g S D B F L h t hFD hgram hcols hp hk hn hg hS
  have harea : screenArea (screenGram (g t) (S t))≠0 := by
    rw [hv]
    exact ne_of_gt (screen_area_positive h hp)
  exact htrace (fixed_tower_entropy_forces_zero_expansion P N eta (Matrix.trace B)
    (fun s => screenArea (screenGram (g s) (S s))) t heta harea ha h0 he)

#print axioms equal_past_entropy_area_derivatives
#print axioms constant_entropy_forces_zero_area_rate
#print axioms constant_entropy_forces_zero_expansion
#print axioms fixed_tower_entropy_forces_zero_expansion
#print axioms finite_entropy_area_rate_constraint
#print axioms geometric_expansion_excludes_frozen_tower_entropy
end
end ChatgptAudit
