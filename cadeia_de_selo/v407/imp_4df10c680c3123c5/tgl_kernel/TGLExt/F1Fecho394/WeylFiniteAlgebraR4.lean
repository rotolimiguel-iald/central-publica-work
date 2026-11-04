import TGLExt.F1Fecho394.ExponentialTomitaInclusionR2
import TGLExt.F1Fecho394.BicommutantTwoVectorR2
/-! The complex span of the actual field Weyl operators is a unital star
algebra. Its vacuum graph is contained in the constructed exponential Tomita
graph. All operators act on the same concrete bosonic Fock space. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.WeylFiniteAlgebra
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.WeylExponentialCore
open F1Rede.CanonicalWedge F1Fecho.WeylCoefficients F1Fecho.ExponentialTomitaInclusion

def finiteSpan : Submodule ℂ (F →L[ℂ] F) :=
  Submodule.span ℂ (F1Fecho.WeylNet.generators FieldWeyl.W K)
theorem generator_mem (k : H1) (hk : k ∈ K) : FieldWeyl.W k ∈ finiteSpan :=
  Submodule.subset_span ⟨k,hk,rfl⟩
theorem one_mem : (1 : F →L[ℂ] F) ∈ finiteSpan := by
  simpa only [FieldWeyl.W_zero] using generator_mem 0 K.zero_mem
theorem generator_mul_mem (k : H1) (hk : k ∈ K)
    (b : F →L[ℂ] F) (hb : b ∈ finiteSpan) : FieldWeyl.W k * b ∈ finiteSpan := by
  induction hb using Submodule.span_induction with
  | mem b hb =>
    obtain ⟨f,hf,rfl⟩ := hb
    rw [FieldWeyl.W_ccr]
    exact finiteSpan.smul_mem _ (generator_mem _ (K.add_mem hk hf))
  | zero => simpa only [mul_zero] using finiteSpan.zero_mem
  | add b c hb hc ihb ihc =>
    rw [mul_add]; exact finiteSpan.add_mem ihb ihc
  | smul c b hb ih =>
    rw [mul_smul_comm]; exact finiteSpan.smul_mem c ih
theorem mul_mem (a b : F →L[ℂ] F) (ha : a ∈ finiteSpan) (hb : b ∈ finiteSpan) :
    a*b ∈ finiteSpan := by
  induction ha using Submodule.span_induction with
  | mem a ha =>
    obtain ⟨k,hk,rfl⟩ := ha
    exact generator_mul_mem k hk b hb
  | zero => simpa only [zero_mul] using finiteSpan.zero_mem
  | add a c ha hc iha ihc =>
    rw [add_mul]; exact finiteSpan.add_mem iha ihc
  | smul c a ha ih =>
    rw [smul_mul_assoc]; exact finiteSpan.smul_mem c ih
theorem star_mem (a : F →L[ℂ] F) (ha : a ∈ finiteSpan) : star a ∈ finiteSpan := by
  induction ha using Submodule.span_induction with
  | mem a ha =>
    obtain ⟨k,hk,rfl⟩ := ha
    rw [FieldWeyl.W_star]
    exact generator_mem _ (K.neg_mem hk)
  | zero => simpa only [star_zero (F →L[ℂ] F)] using finiteSpan.zero_mem
  | add a b ha hb iha ihb =>
    rw [StarAddMonoid.star_add a b]; exact finiteSpan.add_mem iha ihb
  | smul c a ha ih =>
    rw [star_smul]; exact finiteSpan.smul_mem (star c) ih

def finiteAlgebra : StarSubalgebra ℂ (F →L[ℂ] F) where
  toSubalgebra := finiteSpan.toSubalgebra one_mem mul_mem
  star_mem' := fun ha => star_mem _ ha

theorem finite_mem_R (a : F →L[ℂ] F) (ha : a ∈ finiteAlgebra) : a ∈ FieldWeyl.R K := by
  have hs : finiteSpan ≤ (FieldWeyl.R K).toStarSubalgebra.toSubalgebra.toSubmodule := by
    apply Submodule.span_le.mpr
    rintro a ⟨k,hk,rfl⟩
    exact FieldWeyl.W_mem_R K k hk
  exact hs ha

theorem R_bicommutant_finite (a : F →L[ℂ] F) (ha : a ∈ FieldWeyl.R K) :
    ∀ b : F →L[ℂ] F, (∀ c ∈ finiteAlgebra, b*c=c*b) → a*b=b*a := by
  change a ∈ F1Fecho.WeylNet.generatedAlgebra (F1Fecho.WeylNet.generators FieldWeyl.W K) at ha
  rw [← SetLike.mem_coe,F1Fecho.WeylNet.generatedAlgebra_coe _
    (F1Fecho.WeylNet.generators_star_closed FieldWeyl.W FieldWeyl.W_star K)] at ha
  intro b hb
  apply (ha b ?_).symm
  rintro c ⟨k,hk,rfl⟩
  exact (hb _ (generator_mem k hk)).symm

theorem generator_graph (k : H1) (hk : k ∈ K) :
    (FieldWeyl.W k vacuum,(star (FieldWeyl.W k)) vacuum) ∈
      Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) := by
  apply (Sexp_graph_iff _).mpr
  have h : (exponential (Complex.I•k),exponential (Complex.I•Jcandidate k)) ∈ closedGraph TW :=
    (coreGraph TW).le_topologicalClosure (weylCore_le_core (Submodule.subset_span ⟨⟨k,hk⟩,rfl⟩))
  let q := amplitude (Complex.I•k) 0
  have hout : JF ((star (FieldWeyl.W k)) vacuum) = q • exponential (Complex.I•Jcandidate k) := by
    rw [FieldWeyl.W_star,FieldWeyl.W_vacuum]
    change JF (amplitude (Complex.I•(-k)) 0 • exponential (Complex.I•(-k))) = _
    rw [smul_neg,vacuum_amplitude_neg,JF.map_smulₛₗ]
    change star q • JF (exponential (-(Complex.I•k))) = _
    rw [vacuum_amplitude_star,JF_exponential,map_neg,Jcandidate.map_smulₛₗ]
    simp only [Complex.conj_I,neg_smul,neg_neg]
    rfl
  rw [hout,FieldWeyl.W_vacuum]
  exact (closedGraph TW).smul_mem q h

theorem finite_algebra_graph (a : F →L[ℂ] F) (ha : a ∈ finiteAlgebra) :
    (a vacuum,(star a) vacuum) ∈
      Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) := by
  change a ∈ finiteSpan at ha
  induction ha using Submodule.span_induction with
  | mem a ha =>
    obtain ⟨k,hk,rfl⟩ := ha
    exact generator_graph k hk
  | zero =>
    refine ⟨0,?_⟩
    simp only [ZeroMemClass.coe_zero,map_zero,star_zero (F →L[ℂ] F),ContinuousLinearMap.zero_apply]
  | add a b ha hb iha ihb =>
    obtain ⟨x,hx⟩ := iha
    obtain ⟨y,hy⟩ := ihb
    refine ⟨x+y,?_⟩
    have h1 : (x:F)=a vacuum := congrArg Prod.fst hx
    have h2 : Sexp x=(star a) vacuum := congrArg Prod.snd hx
    have h3 : (y:F)=b vacuum := congrArg Prod.fst hy
    have h4 : Sexp y=(star b) vacuum := congrArg Prod.snd hy
    apply Prod.ext
    · change (x:F)+(y:F) = _
      rw [h1,h3]; rfl
    · change Sexp (x+y) = (star (a+b)) vacuum
      rw [map_add,h2,h4,StarAddMonoid.star_add a b]
      rfl
  | smul c a ha ih =>
    obtain ⟨x,hx⟩ := ih
    refine ⟨c•x,?_⟩
    have h1 : (x:F)=a vacuum := congrArg Prod.fst hx
    have h2 : Sexp x=(star a) vacuum := congrArg Prod.snd hx
    apply Prod.ext
    · change c•(x:F) = _
      rw [h1]; rfl
    · change Sexp (c•x) = (star (c•a)) vacuum
      rw [Sexp.map_smulₛₗ,h2,star_smul]
      rfl

theorem R_two_vector_density (a : F →L[ℂ] F) (ha : a ∈ FieldWeyl.R K) (x y : F) :
    (a x,a y) ∈ closure {p : F × F | ∃ b ∈ finiteAlgebra, p=(b x,b y)} :=
  BicommutantTwoVector.two_vector_density finiteAlgebra a (R_bicommutant_finite a ha) x y

end F1Fecho.WeylFiniteAlgebra
#print axioms F1Fecho.WeylFiniteAlgebra.mul_mem
#print axioms F1Fecho.WeylFiniteAlgebra.star_mem
#print axioms F1Fecho.WeylFiniteAlgebra.finite_mem_R
#print axioms F1Fecho.WeylFiniteAlgebra.R_bicommutant_finite
#print axioms F1Fecho.WeylFiniteAlgebra.generator_graph
#print axioms F1Fecho.WeylFiniteAlgebra.finite_algebra_graph
#print axioms F1Fecho.WeylFiniteAlgebra.R_two_vector_density
