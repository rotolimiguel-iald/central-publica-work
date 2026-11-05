import Mathlib.Tactic

set_option autoImplicit false
namespace ChatgptAudit

theorem equal_faces_half (w v : ℝ) (h : w + v = 1) (he : w = v) : w = 1/2 := by
  linarith

theorem ga_mass_conditional (b k r rn m : ℝ)
    (hn : rn = 2*b*r) (hm : m = k*b*rn) : m = 2*b^2*k*r := by
  rw [hm,hn]
  ring

theorem universal_compactness (b c g p r : ℝ) (hg : g ≠ 0) (hp : p ≠ 0)
    (hr : r ≠ 0) : g * (2*b^2*(c^2/(4*p*g))*r) / r = b^2*c^2/(2*p) := by
  field_simp
  ring

theorem two_domain_quadratic (x y b : ℝ) :
    (x-b)^2 + (y-b)^2 =
    (x-(x+y)/2)^2 + (y-(x+y)/2)^2 + 2*((x+y)/2-b)^2 := by
  ring

theorem aic_fixed_advantage_at_most_two (gain : ℝ) (h : 0 ≤ gain) : 2-gain ≤ 2 := by
  linarith

theorem aic_free_wins (gain : ℝ) : 2-gain < 0 ↔ 2 < gain := by
  constructor <;> intro h <;> linarith

theorem opposite_residuals_not_seen_by_mean (b d : ℝ) :
    ((b+d)+(b-d))/2 = b ∧ ((b+d)-b)^2+((b-d)-b)^2 = 2*d^2 := by
  constructor <;> ring

#print axioms equal_faces_half
#print axioms ga_mass_conditional
#print axioms universal_compactness
#print axioms two_domain_quadratic
#print axioms aic_fixed_advantage_at_most_two
#print axioms aic_free_wins
#print axioms opposite_residuals_not_seen_by_mean
end ChatgptAudit
