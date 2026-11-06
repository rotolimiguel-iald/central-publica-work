import TGLExt.F1Fecho394.CanonicalFockFiniteProjectionR3
import TGLExt.F1Fecho394.CanonicalFockMatrixCornerR2

/-! DECLARADO / UNCOMPILED CANDIDATE, R52, 2026-10-16.
Composition of the actual Fock corner, finite subprojection and existing
inverse-supremum tracial law. Reuses the proof of V354FiniteEqualSplit and
V354NormalizedSplit with the actual Fock suppliers, never SiteProfile.
The trace normalization is performed by the actual dual action. No corner,
finite projection, type-II property, equality of halves, or trace law is an
input to the final existence theorems. The two imported R51 suppliers have
terminal EXIT0 receipts. This consumer remains DECLARADO and uncompiled; it
does not claim a total cyclic trace or a complete RemainingModularCoreInput.
Require EXIT0 and all three public axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockNormalizedSplitR5
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeight (PositiveInput add positiveDual)
open F1Fecho.CanonicalFockInverseSupremum (value value_dual)
open F1Fecho.CanonicalFockActualInverseAdditivityR2 (value_add)
open F1Fecho.CanonicalFockActualPositiveTracePackageR2 (positiveSquare value_tracial)
open F1Fecho.CanonicalFockFiniteProjectionR3 (finite_subprojection_exists dual_calibration)
open F1Fecho.CanonicalFockMatrixCornerR2 (core_matrix_corner)
open scoped ENNReal

/- All star-ring rewrites occur here, on a generic Hilbert space. The
concrete Fock theorem below only specializes these identities. The double
star form of the returned projection matches positiveSquare (star a)
definitionally, without a concrete adjoint rewrite. -/
private theorem compressed_corner_algebra {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (e v q : H →L[ℂ] H) (hq : IsStarProjection q)
    (hv : star v*v=e) (hev : e*v=0) (hqe : q*e=q) :
    star (v*q)*(v*q)=q ∧
      IsStarProjection (star (star (v*q))*star (v*q)) ∧
      q*(star (star (v*q))*star (v*q))=0 := by
  let a := v*q
  have hqs := hq.isSelfAdjoint.star_eq
  have hqq : q*q=q := hq.isIdempotentElem
  have ha2 : star a*a=q := by
    change star (v*q)*(v*q)=q
    calc
      _ = q*(star v*v)*q := by rw [star_mul,hqs]; noncomm_ring
      _ = q := by rw [hv,hqe,hqq]
  have haq : a*q=a := by
    change (v*q)*q=v*q
    rw [mul_assoc,hqq]
  have hqv : q*v=0 := by
    calc
      _ = (q*e)*v := by rw [hqe]
      _ = 0 := by rw [mul_assoc,hev,mul_zero]
  have hqa : q*a=0 := by
    change q*(v*q)=0
    rw [← mul_assoc,hqv,zero_mul]
  have hr : IsStarProjection (a*star a) := by
    constructor
    · change (a*star a)*(a*star a)=a*star a
      calc
        _ = a*(star a*a)*star a := by noncomm_ring
        _ = a*star a := by rw [ha2,haq]
    · change star (a*star a)=a*star a
      rw [star_mul,star_star]
  have hqr : q*(a*star a)=0 := by
    rw [← mul_assoc,hqa,zero_mul]
  refine ⟨ha2,?_,?_⟩
  · simpa only [star_star] using hr
  · simpa only [star_star] using hqr

private theorem mapped_orthogonal {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (phi : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (q r : H →L[ℂ] H) (hqr : q*r=0) : phi q * phi r = 0 := by
  calc
    _ = phi (q*r) := (map_mul phi q r).symm
    _ = phi 0 := congrArg phi hqr
    _ = 0 := map_zero phi

/- R5 keeps existential elimination and projection/weight composition at
an abstract Hilbert carrier. PositiveCone is literally the subtype used by
PositiveInput; all generic premises are supplied by existing concrete laws. -/
private abbrev PositiveCone {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) :=
  {B : H →L[ℂ] H // B ∈ N ∧ 0 ≤ B}

private theorem finite_equal_split_generic {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (W : PositiveCone N → ℝ≥0∞)
    (square : N.toStarSubalgebra → PositiveCone N)
    (hsquare : ∀ a, (square a).val=star a.val*a.val)
    (htr : ∀ a, W (square a)=W (square (star a)))
    (hfinite : ∀ e : PositiveCone N, IsStarProjection e.val →
      e ≠ ⟨0,N.zero_mem,le_rfl⟩ →
      ∃ q : PositiveCone N, IsStarProjection q.val ∧
        0<W q ∧ W q<⊤ ∧ q.val*e.val=q.val)
    (hcorner : ∃ (e : PositiveCone N) (v : N.toStarSubalgebra),
      IsStarProjection e.val ∧ e ≠ ⟨0,N.zero_mem,le_rfl⟩ ∧
      star v.val*v.val=e.val ∧ e.val*v.val=0) :
    ∃ q r : PositiveCone N,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      W q=W r ∧ 0<W q ∧ W q<⊤ := by
  obtain ⟨e,v,he,hene,hv,hev⟩ := hcorner
  obtain ⟨q,hq,hpos,hfin,hqe⟩ := hfinite e he hene
  let a : N.toStarSubalgebra := v*⟨q.val,q.property.1⟩
  let r := square (star a)
  have hcomp := compressed_corner_algebra e.val v.val q.val hq hv hev hqe
  have ha2 : star a.val*a.val=q.val := hcomp.1
  have hrv : r.val=star (star a.val)*star a.val := hsquare (star a)
  have hr : IsStarProjection r.val := by
    rw [hrv]
    exact hcomp.2.1
  have hqr : q.val*r.val=0 := by
    rw [hrv]
    exact hcomp.2.2
  have hA : square a=q := Subtype.ext ((hsquare a).trans ha2)
  have ht : W q=W r := by
    simpa only [hA] using htr a
  exact ⟨q,r,hq,hr,hqr,ht,hpos,hfin⟩

private theorem finite_split_support_generic {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (W : PositiveCone N → ℝ≥0∞)
    (plus : PositiveCone N → PositiveCone N → PositiveCone N)
    (hplus : ∀ q r, (plus q r).val=q.val+r.val)
    (hadd : ∀ q r, W (plus q r)=W q+W r)
    (hsplit : ∃ q r : PositiveCone N,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      W q=W r ∧ 0<W q ∧ W q<⊤) :
    ∃ q r : PositiveCone N,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      IsStarProjection (plus q r).val ∧ 0<W (plus q r) ∧ W (plus q r)<⊤ ∧
      W q=W r ∧ 0<W q := by
  obtain ⟨q,r,hq,hr,hqr,ht,hpos,hfin⟩ := hsplit
  have hp : IsStarProjection (plus q r).val := by
    rw [hplus]
    exact hq.add hr hqr
  refine ⟨q,r,hq,hr,hqr,hp,?_,?_,ht,hpos⟩
  · rw [hadd]
    exact hpos.trans_le (le_add_right le_rfl)
  · rw [hadd,← ht]
    exact ENNReal.add_lt_top.mpr ⟨hfin,hfin⟩

private theorem normalized_split_generic {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (W : PositiveCone N → ℝ≥0∞)
    (plus : PositiveCone N → PositiveCone N → PositiveCone N)
    (hplus : ∀ q r, (plus q r).val=q.val+r.val)
    (phi : ℝ → (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H))
    (dual : ℝ → PositiveCone N → PositiveCone N)
    (hdual : ∀ s p, (dual s p).val=phi s p.val)
    (hscale : ∀ s p, W (dual s p)=ENNReal.ofReal (Real.exp (-s))*W p)
    (hcalibrate : ∀ p, 0<W p → W p<⊤ → W (dual (Real.log (W p).toReal) p)=1)
    (hsplit : ∃ q r : PositiveCone N,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      IsStarProjection (plus q r).val ∧ 0<W (plus q r) ∧ W (plus q r)<⊤ ∧
      W q=W r ∧ 0<W q) :
    ∃ q r : PositiveCone N,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      W (plus q r)=1 ∧ W q=W r := by
  obtain ⟨q,r,hq,hr,hqr,_,hpos,hfin,ht,_⟩ := hsplit
  let s := Real.log (W (plus q r)).toReal
  let Q := dual s q
  let R := dual s r
  have hQ : IsStarProjection Q.val := by
    rw [hdual]
    exact hq.map (phi s)
  have hR : IsStarProjection R.val := by
    rw [hdual]
    exact hr.map (phi s)
  have hQR : Q.val*R.val=0 := by
    rw [hdual,hdual]
    exact mapped_orthogonal (phi s) q.val r.val hqr
  have hsum : plus Q R=dual s (plus q r) := by
    apply Subtype.ext
    rw [hplus,hdual,hdual,hdual,hplus,map_add]
  refine ⟨Q,R,hQ,hR,hQR,?_,?_⟩
  · rw [hsum]
    exact hcalibrate (plus q r) hpos hfin
  · change W (dual s q)=W (dual s r)
    rw [hscale,hscale,ht]

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder

theorem finite_equal_split :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      value q=value r ∧ 0<value q ∧ value q<⊤ :=
  @finite_equal_split_generic AmbientHilbert ambientNormedAddCommGroup
    ambientInnerProductSpace ambientCompleteSpace core value positiveSquare
    (fun _ => rfl) value_tracial finite_subprojection_exists core_matrix_corner
#print axioms finite_equal_split

/-- The sum is a positive finite projection with equal positive faces. -/
theorem finite_split_support :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      IsStarProjection (add q r).val ∧ 0<value (add q r) ∧ value (add q r)<⊤ ∧
      value q=value r ∧ 0<value q :=
  @finite_split_support_generic AmbientHilbert ambientNormedAddCommGroup
    ambientInnerProductSpace ambientCompleteSpace core value add
    (fun _ _ => rfl) value_add finite_equal_split
#print axioms finite_split_support

/-- Exact positive-data interface for PF=Q+R in RemainingModularCoreInput. -/
theorem normalized_split_exists :
    ∃ q r : PositiveInput,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      value (add q r)=1 ∧ value q=value r :=
  @normalized_split_generic AmbientHilbert ambientNormedAddCommGroup
    ambientInnerProductSpace ambientCompleteSpace core value add (fun _ _ => rfl)
    (fun s => dualAmbient (H := F1Rede.BosonicFock.F) s) positiveDual
    (fun _ _ => rfl) value_dual dual_calibration finite_split_support
#print axioms normalized_split_exists

end F1Fecho.CanonicalFockNormalizedSplitR5
