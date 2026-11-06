import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.Prod
/-! Two-vector approximation by a unital star algebra. This proves the
finite amplification argument, without assuming a bicommutant density theorem. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.BicommutantTwoVector

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
abbrev H2 := WithLp 2 (H × H)
def coord : H2 (H := H) ≃L[ℂ] H × H := WithLp.prodContinuousLinearEquiv 2 ℂ H H
def diagonal (b : H →L[ℂ] H) : H2 (H := H) →L[ℂ] H2 (H := H) :=
  coord.symm.toContinuousLinearMap.comp ((b.prodMap b).comp coord.toContinuousLinearMap)
theorem diagonal_apply (b : H →L[ℂ] H) (w : H2 (H := H)) :
    coord (diagonal b w) = (b (coord w).1,b (coord w).2) := by
  simp [diagonal,Prod.map]
theorem diagonal_mul (a b : H →L[ℂ] H) (w : H2 (H := H)) :
    diagonal (a*b) w = diagonal a (diagonal b w) := by
  apply coord.injective
  simp [diagonal_apply,ContinuousLinearMap.mul_apply]
theorem diagonal_star_pairing (b : H →L[ℂ] H) (v w : H2 (H := H)) :
    inner ℂ (diagonal b v) w = inner ℂ v (diagonal (star b) w) := by
  change inner ℂ (b (coord v).1) (coord w).1 + inner ℂ (b (coord v).2) (coord w).2 =
    inner ℂ (coord v).1 ((star b) (coord w).1) + inner ℂ (coord v).2 ((star b) (coord w).2)
  simp only [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]

def orbitMap (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H)) : A →ₗ[ℂ] H2 (H := H) where
  toFun b := diagonal b w
  map_add' := by intro b c; apply coord.injective; simp [diagonal_apply,map_add]
  map_smul' := by intro c b; apply coord.injective; simp [diagonal_apply,map_smul]
def orbitSpace (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H)) : Submodule ℂ (H2 (H := H)) :=
  (orbitMap A w).range.topologicalClosure
instance orbitSpace_complete (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H)) :
    CompleteSpace (orbitSpace A w) := ((orbitMap A w).range.isClosed_topologicalClosure).completeSpace_coe

theorem orbit_invariant (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H))
    (b : H →L[ℂ] H) (hb : b ∈ A) (v : H2 (H := H)) (hv : v ∈ orbitSpace A w) :
    diagonal b v ∈ orbitSpace A w := by
  have hi : ((orbitMap A w).range : Set (H2 (H := H))) ⊆
      (diagonal b) ⁻¹' (orbitSpace A w : Set (H2 (H := H))) := by
    rintro z ⟨c,rfl⟩
    apply Submodule.le_topologicalClosure
    refine ⟨⟨b*c,A.mul_mem hb c.property⟩,?_⟩
    exact diagonal_mul b c w
  have hc := closure_minimal hi (((orbitMap A w).range.isClosed_topologicalClosure).preimage (diagonal b).continuous)
  apply hc
  exact hv

theorem projection_commutes (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H))
    (b : H →L[ℂ] H) (hb : b ∈ A) (v : H2 (H := H)) :
    (orbitSpace A w).starProjection (diagonal b v) = diagonal b ((orbitSpace A w).starProjection v) := by
  apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero
  · exact orbit_invariant A w b hb _ (Submodule.starProjection_apply_mem _ _)
  · intro z hz
    rw [← map_sub,diagonal_star_pairing]
    exact Submodule.starProjection_inner_eq_zero v _ (orbit_invariant A w (star b) (star_mem hb) z hz)

def take (i : Fin 2) : H2 (H := H) →L[ℂ] H :=
  (if i=0 then ContinuousLinearMap.fst ℂ H H else ContinuousLinearMap.snd ℂ H H).comp coord.toContinuousLinearMap
def put (i : Fin 2) : H →L[ℂ] H2 (H := H) :=
  coord.symm.toContinuousLinearMap.comp
    (if i=0 then ContinuousLinearMap.inl ℂ H H else ContinuousLinearMap.inr ℂ H H)
theorem take_diagonal (i : Fin 2) (b : H →L[ℂ] H) (v : H2 (H := H)) :
    take i (diagonal b v) = b (take i v) := by
  fin_cases i <;> simp [take,diagonal_apply]
theorem diagonal_put (i : Fin 2) (b : H →L[ℂ] H) (v : H) :
    diagonal b (put i v) = put i (b v) := by
  apply coord.injective
  fin_cases i <;> simp [put,diagonal_apply,map_zero]
theorem put_take_decomposition (v : H2 (H := H)) :
    put 0 (take 0 v) + put 1 (take 1 v) = v := by
  apply coord.injective
  simp [put,take]
theorem take_ext {v w : H2 (H := H)} (h : ∀ i : Fin 2, take i v = take i w) : v=w := by
  apply coord.injective
  exact Prod.ext (by simpa [take] using h 0) (by simpa [take] using h 1)

def block (P : H2 (H := H) →L[ℂ] H2 (H := H)) (i j : Fin 2) : H →L[ℂ] H :=
  (take i).comp (P.comp (put j))
theorem block_commutes (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H))
    (i j : Fin 2) (b : H →L[ℂ] H) (hb : b ∈ A) :
    block (orbitSpace A w).starProjection i j * b = b * block (orbitSpace A w).starProjection i j := by
  ext x
  change take i ((orbitSpace A w).starProjection (put j (b x))) =
    b (take i ((orbitSpace A w).starProjection (put j x)))
  rw [← diagonal_put,projection_commutes A w b hb,take_diagonal]

theorem bicommutant_projection_commutes (A : StarSubalgebra ℂ (H →L[ℂ] H))
    (a : H →L[ℂ] H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A, b*c=c*b) → a*b=b*a)
    (w v : H2 (H := H)) :
    (orbitSpace A w).starProjection (diagonal a v) = diagonal a ((orbitSpace A w).starProjection v) := by
  let P := (orbitSpace A w).starProjection
  have hb (i j : Fin 2) : ∀ x : H, a (block P i j x) = block P i j (a x) := by
    intro x
    exact congrArg (fun f : H →L[ℂ] H => f x)
      (ha (block P i j) (fun c hc => block_commutes A w i j c hc))
  have hp (i : Fin 2) (z : H2 (H := H)) :
      take i (P z) = block P i 0 (take 0 z) + block P i 1 (take 1 z) := by
    conv_lhs => rw [← put_take_decomposition z]
    simp only [map_add]
    rfl
  apply take_ext
  intro i
  change take i (P (diagonal a v)) = take i (diagonal a (P v))
  rw [hp,take_diagonal,take_diagonal,take_diagonal,hp,map_add,hb,hb]

theorem vector_mem_orbit (A : StarSubalgebra ℂ (H →L[ℂ] H)) (w : H2 (H := H)) : w ∈ orbitSpace A w := by
  apply Submodule.le_topologicalClosure
  refine ⟨1,?_⟩
  apply coord.injective
  simp [orbitMap,diagonal_apply]

theorem diagonal_bicommutant_mem_orbit (A : StarSubalgebra ℂ (H →L[ℂ] H))
    (a : H →L[ℂ] H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A, b*c=c*b) → a*b=b*a)
    (w : H2 (H := H)) : diagonal a w ∈ orbitSpace A w := by
  apply Submodule.starProjection_eq_self_iff.mp
  rw [bicommutant_projection_commutes A a ha]
  rw [Submodule.starProjection_eq_self_iff.mpr (vector_mem_orbit A w)]

theorem two_vector_density (A : StarSubalgebra ℂ (H →L[ℂ] H))
    (a : H →L[ℂ] H)
    (ha : ∀ b : H →L[ℂ] H, (∀ c ∈ A, b*c=c*b) → a*b=b*a)
    (x y : H) : (a x,a y) ∈ closure {p : H × H | ∃ b ∈ A, p=(b x,b y)} := by
  let w : H2 (H := H) := coord.symm (x,y)
  have hw := diagonal_bicommutant_mem_orbit A a ha w
  have hh : coord '' ((orbitMap A w).range : Set (H2 (H := H))) ⊆
      {p : H × H | ∃ b ∈ A, p=(b x,b y)} := by
    rintro p ⟨v,⟨b,rfl⟩,rfl⟩
    refine ⟨b,b.property,?_⟩
    simp [orbitMap,diagonal_apply,w]
  have hc := image_closure_subset_closure_image coord.continuous ⟨diagonal a w,hw,rfl⟩
  apply closure_mono hh at hc
  simpa [diagonal_apply,w] using hc

end F1Fecho.BicommutantTwoVector
#print axioms F1Fecho.BicommutantTwoVector.projection_commutes
#print axioms F1Fecho.BicommutantTwoVector.bicommutant_projection_commutes
#print axioms F1Fecho.BicommutantTwoVector.two_vector_density
