import TGLExt.F1Fecho394.GenericQuadraticTraceFormsR1
/-! Quadratic-form consequence of a proved modular double-cut balance.
All commutation, positivity and convergence premises are explicit; no weight
or traciality is manufactured. The caller must supply the actual cut family. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.QuadraticTraceForms
open TGLV350.Regular Filter
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem root_cut_supremum
    (T : H →L[ℂ] H) (hT0 : 0≤T) (hT1 : T≤1) (hiT : Function.Injective T)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (C p : ℕ → H →L[ℂ] H)
    (hC : ∀n,0≤C n) (hp : ∀n,0≤p n ∧ p n≤1)
    (htp : ∀v,Tendsto (fun n=>p n v) atTop (𝓝 v))
    (hTC : ∀n,Commute T (C n)) (hTp : ∀n,Commute T (p n))
    (hflip : antiunitaryConjugate (H := H) J T=1-T)
    (hCq : ∀n m,Commute (C n) (antiunitaryConjugate (H := H) J (p m)))
    (hpD : ∀n m,Commute (p n) (antiunitaryConjugate (H := H) J (C m)))
    (hbalance : ∀n m,(1-T)*C n*antiunitaryConjugate (H := H) J (p m)=
      T*p n*antiunitaryConjugate (H := H) J (C m))
    (x : (resolventSquareRoot T hT0 hiT).domain) :
    (⨆n,ENNReal.ofReal (inner ℂ (resolventSquareRoot T hT0 hiT x)
      (C n (resolventSquareRoot T hT0 hiT x))).re) =
      ⨆n,ENNReal.ofReal (inner ℂ (x : H) (antiunitaryConjugate (H := H) J (C n) x)).re := by
  let D (n:ℕ) := antiunitaryConjugate (H := H) J (C n)
  let q (n:ℕ) := antiunitaryConjugate (H := H) J (p n)
  have hD (n:ℕ) : 0≤D n := antiunitaryConjugate_nonneg J (C n) (hC n)
  have hq (n:ℕ) : 0≤q n ∧ q n≤1 := by
    refine ⟨antiunitaryConjugate_nonneg J (p n) (hp n).1,?_⟩
    apply operator_le_of_sub_nonneg
    have hh := antiunitaryConjugate_nonneg J (1-p n)
      (hilbertComplement_nonneg (p n) (hp n).2)
    change 0≤(antiunitaryConjugateRealHom J) (1-p n) at hh
    simp only [map_sub,map_one] at hh
    exact hh
  have htq (v:H) : Tendsto (fun n=>q n v) atTop (𝓝 v) := by
    have hh := J.continuous.continuousAt.tendsto.comp (htp (J.symm v))
    change Tendsto (fun n=>J (p n (J.symm v))) atTop (𝓝 v)
    simpa only [LinearIsometryEquiv.apply_symm_apply,Function.comp_def] using hh
  have flip_commute (A:H→L[ℂ]H) (hA:Commute T A) :
      Commute T (antiunitaryConjugate (H := H) J A) := by
    have hh:=hA.map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate (H := H) J T) (antiunitaryConjugate (H := H) J A) at hh
    rw [hflip] at hh
    simpa only [sub_sub_cancel] using (Commute.one_left _).sub_left hh
  apply double_cut_form_supremum C D p q x (resolventSquareRoot T hT0 hiT x)
    hC hD hp hq hCq hpD htp htq
  intro n m
  have he := bounded_root_form_balance T (C n*q m) (p n*D m) hT0 hT1 hiT
    ((hTC n).mul_right (flip_commute (p m) (hTp m)))
    ((hTp n).mul_right (flip_commute (C m) (hTC m)))
    (by simpa only [mul_assoc] using hbalance n m) x
  exact congrArg Complex.re he
end F1Fecho.QuadraticTraceForms
#print axioms F1Fecho.QuadraticTraceForms.root_cut_supremum
