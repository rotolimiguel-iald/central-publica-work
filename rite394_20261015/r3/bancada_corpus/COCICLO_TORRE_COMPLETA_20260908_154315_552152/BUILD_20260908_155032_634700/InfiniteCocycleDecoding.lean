import GeometricLikelihoodSeparation
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.CocycleRealization
open Filter Topology Set TGLExt ChatgptAudit.Response028 ChatgptAudit.Cocycle030
noncomputable section

def digitTerm (a : ℕ → ℝ) (u : ℕ → Bool) (n : ℕ) : ℝ :=
  if u n then a n else 0

def binaryCode (a : ℕ → ℝ) (u : ℕ → Bool) : ℝ :=
  ∑' n, digitTerm a u n

theorem digit_term_bounds {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (u : ℕ → Bool) (n : ℕ) :
    0 ≤ digitTerm a u n ∧ digitTerm a u n ≤ a n := by
  cases h : u n <;> simp [digitTerm,h,ha n]

theorem digit_summable {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) :
    Summable (digitTerm a u) :=
  Summable.of_nonneg_of_le (fun n => (digit_term_bounds ha u n).1)
    (fun n => (digit_term_bounds ha u n).2) hs

theorem digit_tail_summable {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    Summable (fun k => digitTerm a u (n+1+k)) :=
  (digit_summable ha hs u).comp_injective (fun _ _ h => Nat.add_left_cancel h)

theorem code_prefix_tail {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    binaryCode a u = (∑ k ∈ Finset.range n, digitTerm a u k) +
      digitTerm a u n + ∑' k, digitTerm a u (n+1+k) := by
  have h := (digit_summable ha hs u).sum_add_tsum_nat_add (n+1)
  rw [Finset.sum_range_succ] at h
  simpa only [binaryCode,Nat.add_comm] using h.symm

theorem digit_tail_bounds {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    0 ≤ (∑' k, digitTerm a u (n+1+k)) ∧
    (∑' k, digitTerm a u (n+1+k)) ≤ ∑' k, a (n+1+k) := by
  constructor
  · exact tsum_nonneg (fun k => (digit_term_bounds ha u (n+1+k)).1)
  · exact Summable.tsum_le_tsum (fun k => (digit_term_bounds ha u (n+1+k)).2)
      (digit_tail_summable ha hs u n)
      (hs.comp_injective (fun _ _ h => Nat.add_left_cancel h))

theorem first_difference_strict {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (hd : ∀ n, (∑' k, a (n+1+k)) < a n)
    (u v : ℕ → Bool) (n : ℕ)
    (hp : ∀ k, k<n → u k=v k) (hu : u n=false) (hv : v n=true) :
    binaryCode a u < binaryCode a v := by
  have he : (∑ k ∈ Finset.range n, digitTerm a u k) =
      ∑ k ∈ Finset.range n, digitTerm a v k := by
    apply Finset.sum_congr rfl
    intro k hk
    simp only [digitTerm,hp k (Finset.mem_range.mp hk)]
  rw [code_prefix_tail ha hs u n,code_prefix_tail ha hs v n,he]
  have htu := (digit_tail_bounds ha hs u n).2
  have htv := (digit_tail_bounds ha hs v n).1
  have hdn := hd n
  simp only [digitTerm,hu,hv,Bool.false_eq_true,if_false,if_true,add_zero]
  linarith

theorem binary_code_injective {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (hd : ∀ n, (∑' k, a (n+1+k)) < a n) :
    Function.Injective (binaryCode a) := by
  intro u v huv
  by_contra hne
  have hex : ∃ n, u n≠v n := by
    by_contra hn
    apply hne
    funext n
    by_contra hnv
    exact hn ⟨n,hnv⟩
  let n := Nat.find hex
  have hn : u n≠v n := Nat.find_spec hex
  have hp : ∀ k, k<n → u k=v k := by
    intro k hk
    exact of_not_not (Nat.find_min hex hk)
  cases hu : u n <;> cases hv : v n
  · exact hn (hu.trans hv.symm)
  · exact (ne_of_lt (first_difference_strict ha hs hd u v n hp hu hv)) huv
  · exact (ne_of_lt (first_difference_strict ha hs hd v u n
      (fun k hk => (hp k hk).symm) hv hu)) huv.symm
  · exact hn (hu.trans hv.symm)

theorem geometric_code_injective {t : ℝ} (ht : t≠0) :
    Function.Injective (binaryCode (geometricContrast t)) :=
  binary_code_injective (geometric_contrast_nonnegative t)
    (geometric_contrast_summable t) (geometric_contrast_dominates_entire_tail ht)

def geometricLogReading (t : ℝ) (u : ℕ → Bool) : ℝ :=
  (∑' n, logOneRatio (geometricArgument t n)) -
    binaryCode (geometricContrast t) u

def geometricSiteReading (t : ℝ) (u : ℕ → Bool) (n : ℕ) : ℝ :=
  if u n then logZeroRatio (geometricArgument t n)
    else logOneRatio (geometricArgument t n)

theorem geometric_log_one_summable (t : ℝ) :
    Summable (fun n => logOneRatio (geometricArgument t n)) := by
  apply Summable.of_nonneg_of_le
    (fun n => (log_one_ratio_bounds _ (geometric_argument_bounds t n).1).1)
    (fun n => ?_) (geometricAmplitude.summable.mul_left (2*regularParameter t))
  have h := (log_one_ratio_bounds _ (geometric_argument_bounds t n).1).2
  simpa only [geometricArgument,mul_comm,mul_left_comm,mul_assoc] using h

theorem geometric_site_reading_eq (t : ℝ) (u : ℕ → Bool) (n : ℕ) :
    geometricSiteReading t u n =
      logOneRatio (geometricArgument t n) - digitTerm (geometricContrast t) u n := by
  cases h : u n <;> simp [geometricSiteReading,digitTerm,h,geometricContrast,logContrast]

theorem geometric_site_reading_summable (t : ℝ) (u : ℕ → Bool) :
    Summable (geometricSiteReading t u) := by
  have h := (geometric_log_one_summable t).sub
    (digit_summable (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u)
  simpa only [← geometric_site_reading_eq] using h

theorem geometric_log_reading_eq_actual_series (t : ℝ) (u : ℕ → Bool) :
    geometricLogReading t u = ∑' n, geometricSiteReading t u n := by
  rw [geometricLogReading,binaryCode,← Summable.tsum_sub
    (geometric_log_one_summable t)
    (digit_summable (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u)]
  exact tsum_congr (fun n => (geometric_site_reading_eq t u n).symm)

theorem geometric_log_reading_injective {t : ℝ} (ht : t≠0) :
    Function.Injective (geometricLogReading t) := by
  intro u v h
  apply geometric_code_injective ht
  dsimp [geometricLogReading] at h
  linarith

#print axioms digitTerm
#print axioms binaryCode
#print axioms digit_term_bounds
#print axioms digit_summable
#print axioms digit_tail_summable
#print axioms code_prefix_tail
#print axioms digit_tail_bounds
#print axioms first_difference_strict
#print axioms binary_code_injective
#print axioms geometric_code_injective
#print axioms geometricLogReading
#print axioms geometricSiteReading
#print axioms geometric_log_one_summable
#print axioms geometric_site_reading_eq
#print axioms geometric_site_reading_summable
#print axioms geometric_log_reading_eq_actual_series
#print axioms geometric_log_reading_injective

end
end ChatgptAudit.CocycleRealization
