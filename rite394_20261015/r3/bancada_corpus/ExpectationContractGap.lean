import ExpectationProjection

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem offdiagonal_not_centralizer (h : P.w 0 ≠ 1/2) :
    towerPi P (N := 0) (Matrix.single (0 : Fin 2) 1 (1 : ℂ)) ∉ omegaCentralizer P := by
  intro hc
  have he := hc.2 (towerPi P (N := 0) (Matrix.single (1 : Fin 2) 0 (1 : ℂ)))
    (towerPi_mem_factor _)
  rw [omegaState_pi_mul, omegaState_pi_mul, tState_E01_E10, tState_E10_E01] at he
  have hr := Complex.ofReal_injective he
  apply h
  linarith

theorem expectation_not_imported_into (h : P.w 0 ≠ 1/2) (N : ℕ) :
    ¬ (∀ x ∈ theFactorObject P, towerExpectation P N x ∈ omegaCentralizer P) := by
  intro hall
  let a : Matrix (chainIdx N) (chainIdx N) ℂ :=
    tPush (Nat.zero_le N) (Matrix.single (0 : Fin 2) 1 (1 : ℂ))
  have ha := hall (towerPi P a) (towerPi_mem_factor a)
  rw [expectation_fixes] at ha
  dsimp [a] at ha
  rw [towerPi_compat] at ha
  exact offdiagonal_not_centralizer h ha

theorem expectation_not_imported_contract (h : P.w 0 ≠ 1/2) (N : ℕ) :
    ¬ ∃ I : ExpectationInput P, ∀ x ∈ theFactorObject P, I.E x = towerExpectation P N x := by
  rintro ⟨I,he⟩
  apply expectation_not_imported_into h N
  intro x hx
  rw [← he x hx]
  exact I.into x hx

#print axioms expectation_not_imported_contract
end
end ChatgptAudit
