import ChainSiteOperators

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

def shiftedProfile (P : SiteProfile) : SiteProfile where
  w := fun n => P.w (n+1)
  pos := fun n => P.pos (n+1)
  lt_one := fun n => P.lt_one (n+1)

def siteFlow (P : SiteProfile) (t : ℝ) (n : ℕ)
    (a : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  fun i j => modularPhase t (Real.log (siteW (P.w n) i) - Real.log (siteW (P.w n) j)) * a i j

theorem flow_lastSite (t : ℝ) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    flowLevel P t n (lastSiteMatrix n a) = lastSiteMatrix n (siteFlow P t n a) := by
  cases n with
  | zero => rfl
  | succ n =>
    ext ⟨i,u⟩ ⟨j,v⟩
    by_cases hij : i=j
    · subst j
      have hw := ne_of_gt (towerW_pos P n i)
      have hu := ne_of_gt (siteW_pos (P.pos (n+1)) (P.lt_one (n+1)) u)
      have hv := ne_of_gt (siteW_pos (P.pos (n+1)) (P.lt_one (n+1)) v)
      simp only [flowLevel, towerW, Real.log_mul hw hu, Real.log_mul hw hv]
      simp [lastSiteMatrix,Matrix.kroneckerMap_apply,siteFlow]
    · simp [flowLevel,lastSiteMatrix,Matrix.kroneckerMap_apply,Matrix.one_apply_ne hij]

theorem modularConjugation_site (t : ℝ) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    modularConjugation P t (siteOperator P n a) = siteOperator P n (siteFlow P t n a) := by
  unfold siteOperator
  rw [modularConjugation_local,flow_lastSite]

theorem shifted_site_flow (t : ℝ) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteFlow (shiftedProfile P) t n a = siteFlow P t (n+1) a := rfl

theorem shifted_generator_intertwining (t : ℝ) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    modularConjugation P t (siteOperator P (n+1) a) =
      siteOperator P (n+1) (siteFlow (shiftedProfile P) t n a) := by
  rw [modularConjugation_site,shifted_site_flow]

theorem uniform_generator_intertwining (hp : ∀ n, P.w (n+1) = P.w n)
    (t : ℝ) (n : ℕ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    modularConjugation P t (siteOperator P (n+1) a) =
      siteOperator P (n+1) (siteFlow P t n a) := by
  rw [modularConjugation_site]
  apply congrArg (siteOperator P (n+1))
  unfold siteFlow
  rw [hp n]

#print axioms shifted_generator_intertwining
#print axioms uniform_generator_intertwining
end
end ChatgptAudit
