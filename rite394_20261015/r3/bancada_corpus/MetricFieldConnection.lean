import CovariantScalarConservation

set_option autoImplicit false
namespace ChatgptAudit
open Matrix
noncomputable section

def leviCivitaField (g gInv : TensorField4) (x : Coordinate4) :
    Fin 4 → Matrix (Fin 4) (Fin 4) ℝ :=
  leviCivitaJet (gInv x) (tensorFieldJet g x)

theorem inverse_symmetric_of_symmetric
    (g gInv : Matrix (Fin 4) (Fin 4) ℝ) (hg : gᵀ=g) (hleft : gInv*g=1) : gInvᵀ=gInv := by
  calc
    gInvᵀ = (gInv*g)*gInvᵀ := by rw [hleft,one_mul]
    _ = gInv*(g*gInvᵀ) := Matrix.mul_assoc _ _ _
    _ = gInv*(gInv*g)ᵀ := by rw [Matrix.transpose_mul,hg]
    _ = gInv := by rw [hleft,Matrix.transpose_one,mul_one]

theorem levi_civita_field_metric_compatible (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hleft : ∀ x∈U, gInv x*g x=1) (hright : ∀ x∈U, g x*gInv x=1) :
    ∀ x∈U, ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (leviCivitaField g gInv x) i=0 := by
  intro x hx
  exact levi_civita_jet_metric_compatible (g x) (gInv x)
    (inverse_symmetric_of_symmetric (g x) (gInv x) (hs x hx) (hleft x hx))
    (hleft x hx) (hright x hx) (tensorFieldJet g x)
    (tensorFieldJet_symmetric_on U hU g hs x hx)

theorem levi_civita_field_torsion_free (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (hs : ∀ x∈U, (g x)ᵀ=g x) :
    ∀ x∈U, ∀ i j l, leviCivitaField g gInv x i l j=leviCivitaField g gInv x j l i := by
  intro x hx i j l
  exact levi_civita_jet_torsion_free (gInv x) (tensorFieldJet g x)
    (tensorFieldJet_symmetric_on U hU g hs x hx) i j l

theorem levi_civita_conserved_scalar_is_constant (U : Set Coordinate4) (hU : IsOpen U)
    (hconn : IsPreconnected U) (g gInv : TensorField4)
    (hs : ∀ x∈U, (g x)ᵀ=g x)
    (hleft : ∀ x∈U, gInv x*g x=1) (hright : ∀ x∈U, g x*gInv x=1)
    (f : Coordinate4 → ℝ) (hf : DifferentiableOn ℝ f U)
    (hg : ∀ j k, DifferentiableOn ℝ (fun y => g y j k) U)
    (hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence gInv (leviCivitaField g gInv)
      (fun y => f y • g y) x j=0) : ∃ c : ℝ, ∀ x∈U, f x=c := by
  exact conserved_pure_trace_is_constant U hU hconn g gInv (leviCivitaField g gInv) f hf hg
    hleft (levi_civita_field_metric_compatible U hU g gInv hs hleft hright) hdiv

#print axioms inverse_symmetric_of_symmetric
#print axioms levi_civita_field_metric_compatible
#print axioms levi_civita_field_torsion_free
#print axioms levi_civita_conserved_scalar_is_constant
end
end ChatgptAudit
