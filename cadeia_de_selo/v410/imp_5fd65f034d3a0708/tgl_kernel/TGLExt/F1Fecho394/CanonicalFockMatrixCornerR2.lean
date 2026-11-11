import TGLExt.F1Fecho394.MatrixCornerFromNilpotentR3
import TGLExt.F1Fecho394.CanonicalFockDualWeightR3
import TGLExt.F1Fecho394.WedgeNonabelianR4
import TGLExt.V354FiniteTraceSupport
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.PosPart.Basic

/-! DECLARADO / UNCOMPILED CANDIDATE, R51, 2026-10-16.
An actual nilpotent and orthogonal corner in the SAME represented Fock core.
The existing normalized Weyl pair is reused. With A=W(f)+W(f)* and U=W(g),
U A U*=-A; the vacuum characteristic proves A is nonzero. Uniqueness of the
positive and negative parts gives U A+ U*=A-. Consequently T=A+ U is nonzero
and square-zero. Membership is proved inside the actual wedge algebra and
then transported by the injective fibre representation to the existing core.
No nonabelian, nilpotent, matrix-corner, type-II, trace or split premise is
added to the final suppliers. The generic sign-flip lemma has explicit
hypotheses, all discharged by the concrete Weyl construction below.
Require EXIT0 and all five public axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockMatrixCornerR2
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open TGLV350.Regular
open F1Fecho.CanonicalFockRegular (M core)
open F1Fecho.CanonicalFockWeight (PositiveInput zero)
open F1Fecho.WeylCoefficients
open F1Fecho.WedgeNonabelian (normalized_pair phase_half_pi)

theorem nilpotent_of_sign_flip {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (A U : H →L[ℂ] H)
    (hAm : A ∈ N) (hUm : U ∈ N) (hAs : IsSelfAdjoint A) (hA : A ≠ 0)
    (huL : star U * U = 1) (huR : U * star U = 1)
    (hflip : U * A * star U = -A) :
    ∃ T : H →L[ℂ] H, T ∈ N ∧ T ≠ 0 ∧ T*T = 0 := by
  letI : IsClosed (N.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed N
  have hpm : A⁺ ∈ N := by
    rw [CFC.posPart_def]
    exact cfcₙ_mem (𝕜' := ℂ) (s := N.toStarSubalgebra) (fun x : ℝ => x⁺) hAm
  have hparts : U * A⁺ * star U = A⁻ := by
    have hd : -A = (U*A⁺*star U) - (U*A⁻*star U) := by
      calc
        -A = U*A*star U := hflip.symm
        _ = U*(A⁺-A⁻)*star U :=
          congrArg (fun B : H →L[ℂ] H => U*B*star U)
            (CFC.posPart_sub_negPart A hAs).symm
        _ = _ := by noncomm_ring
    have ho : (U*A⁺*star U)*(U*A⁻*star U) = 0 := by
      calc
        _ = U*(A⁺*(star U*U)*A⁻)*star U := by noncomm_ring
        _ = U*(A⁺*A⁻)*star U := by rw [huL,mul_one]
        _ = 0 := by rw [CFC.posPart_mul_negPart,mul_zero,zero_mul]
    have hp := (CFC.posPart_negPart_unique hd ho
      (star_right_conjugate_nonneg (CFC.posPart_nonneg A) U)
      (star_right_conjugate_nonneg (CFC.negPart_nonneg A) U)).1
    simpa only [CFC.posPart_neg] using hp.symm
  have hpne : A⁺ ≠ 0 := by
    intro hp
    have hn : A⁻ = 0 := by rw [← hparts,hp,mul_zero,zero_mul]
    apply hA
    calc
      A = A⁺-A⁻ := (CFC.posPart_sub_negPart A hAs).symm
      _ = 0 := by rw [hp,hn,sub_zero]
  have hmove : U*A⁺ = A⁻*U := by
    have ht := congrArg (fun B : H →L[ℂ] H => B*U) hparts
    simpa only [mul_assoc,huL,mul_one] using ht
  refine ⟨A⁺*U,N.mul_mem hpm hUm,?_,?_⟩
  · intro hz
    apply hpne
    have ht := congrArg (fun B : H →L[ℂ] H => B*star U) hz
    simpa only [mul_assoc,huR,mul_one,zero_mul] using ht
  · calc
      (A⁺*U)*(A⁺*U) = A⁺*(U*A⁺)*U := by noncomm_ring
      _ = A⁺*(A⁻*U)*U := by rw [hmove]
      _ = (A⁺*A⁻)*(U*U) := by noncomm_ring
      _ = 0 := by rw [CFC.posPart_mul_negPart,zero_mul]
#print axioms nilpotent_of_sign_flip

/- The adjoint algebra and existential packing are proved at a generic
Hilbert type, before supplying the native Fock dictionaries. -/
private theorem real_part_selfAdjoint {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (X : H →L[ℂ] H) : IsSelfAdjoint (X+star X) := by
  change star (X+star X) = X+star X
  rw [star_add,star_star,add_comm]

private theorem real_part_flip {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (X U : H →L[ℂ] H) (hx : U*X*star U = -X) :
    U*(X+star X)*star U = -(X+star X) := by
  have hs : U*star X*star U = -star X := by
    simpa only [star_mul,star_star,star_neg,mul_assoc] using
      congrArg (fun B : H →L[ℂ] H => star B) hx
  rw [mul_add,add_mul,hx,hs,neg_add]

private theorem positive_corner_from_nilpotent_exists {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H)
    (h : ∃ T : H →L[ℂ] H, T ∈ N ∧ T ≠ 0 ∧ T*T = 0) :
    ∃ (e : {B : H →L[ℂ] H // B ∈ N ∧ 0 ≤ B}) (v : N.toStarSubalgebra),
      IsStarProjection e.val ∧ e ≠ ⟨0,N.zero_mem,le_rfl⟩ ∧
      star v.val*v.val = e.val ∧ e.val*v.val = 0 := by
  obtain ⟨T,hTm,hT,hTT⟩ := h
  obtain ⟨e,v,hem,hvm,he,hene,hve,hev⟩ :=
    F1Fecho.MatrixCornerFromNilpotent.matrix_corner_of_square_zero N T hTm hT hTT
  refine ⟨⟨e,hem,he.nonneg⟩,⟨v,hvm⟩,he,?_,hve,hev⟩
  intro hz
  exact hene (congrArg Subtype.val hz)

private abbrev fockNormedAddCommGroup : NormedAddCommGroup F := inferInstance
private abbrev fockInnerProductSpace : InnerProductSpace ℂ F := inferInstance
private abbrev fockCompleteSpace : CompleteSpace F := inferInstance
private abbrev AmbientHilbert := RegularHilbert F
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

private theorem weyl_mul_neg (f : H1) : FieldWeyl.W f * FieldWeyl.W (-f) = 1 := by
  rw [FieldWeyl.W_ccr,phase_self_neg,add_neg_cancel,FieldWeyl.W_zero,one_smul]

theorem weyl_real_part_ne_zero (f : H1) : FieldWeyl.W f + star (FieldWeyl.W f) ≠ 0 := by
  intro hz
  have hv := congrArg (fun B : F →L[ℂ] F => inner ℂ vacuum (B vacuum)) hz
  simp only [ContinuousLinearMap.add_apply,inner_add_right,FieldWeyl.W_star,
    FieldWeyl.vacuum_characteristic,norm_neg,ContinuousLinearMap.zero_apply,inner_zero_right] at hv
  have hv' : (2 : ℂ)*Complex.exp (-((‖f‖ : ℂ)^2)/2) = 0 := by
    simpa only [two_mul] using hv
  exact Complex.exp_ne_zero _ ((mul_eq_zero.mp hv').resolve_left (by norm_num))
#print axioms weyl_real_part_ne_zero

theorem wedge_nilpotent_exists : ∃ T : F →L[ℂ] F, T ∈ M ∧ T ≠ 0 ∧ T*T = 0 := by
  obtain ⟨f,hf,g,hg,hfg⟩ := normalized_pair
  let X := FieldWeyl.W f
  let U := FieldWeyl.W g
  have hx : X ∈ M := FieldWeyl.W_mem_R _ f hf
  have hu : U ∈ M := FieldWeyl.W_mem_R _ g hg
  have huR : U*star U = 1 := by
    change FieldWeyl.W g * star (FieldWeyl.W g) = 1
    rw [FieldWeyl.W_star]
    exact weyl_mul_neg g
  have huL : star U*U = 1 := by
    change star (FieldWeyl.W g) * FieldWeyl.W g = 1
    rw [FieldWeyl.W_star]
    simpa only [neg_neg] using weyl_mul_neg (-g)
  obtain ⟨hp,hq⟩ := phase_half_pi f g hfg
  have hanti : U*X = -(X*U) := by
    change FieldWeyl.W g*FieldWeyl.W f = -(FieldWeyl.W f*FieldWeyl.W g)
    rw [FieldWeyl.W_ccr,FieldWeyl.W_ccr,hq,hp,add_comm g f,neg_smul,neg_neg]
  have hxflip : U*X*star U = -X := by
    rw [hanti,neg_mul,mul_assoc,huR,mul_one]
  have hAm : X+star X ∈ M := M.add_mem hx (M.toStarSubalgebra.star_mem' hx)
  have hAs : IsSelfAdjoint (X+star X) :=
    @real_part_selfAdjoint F fockNormedAddCommGroup fockInnerProductSpace
      fockCompleteSpace X
  have hflip : U*(X+star X)*star U = -(X+star X) :=
    @real_part_flip F fockNormedAddCommGroup fockInnerProductSpace
      fockCompleteSpace X U hxflip
  exact @nilpotent_of_sign_flip F fockNormedAddCommGroup fockInnerProductSpace
    fockCompleteSpace M (X+star X) U hAm hu hAs (weyl_real_part_ne_zero f) huL huR hflip
#print axioms wedge_nilpotent_exists

theorem core_nilpotent_exists :
    ∃ T : AmbientHilbert →L[ℂ] AmbientHilbert, T ∈ core ∧ T ≠ 0 ∧ T*T = 0 := by
  obtain ⟨T,hTm,hT,hTT⟩ := wedge_nilpotent_exists
  refine ⟨fibre T,F1Fecho.CanonicalFockRegular.fibre_mem T hTm,?_,?_⟩
  · intro hz
    apply hT
    apply fibre_injective
    exact hz.trans (map_zero fibreRepresentation).symm
  · rw [← fibre_mul,hTT]
    exact map_zero fibreRepresentation
#print axioms core_nilpotent_exists

/-- The orthogonal corner needed by the finite split, on the unchanged core. -/
theorem core_matrix_corner :
    ∃ (e : PositiveInput) (v : core.toStarSubalgebra),
      IsStarProjection e.val ∧ e ≠ zero ∧ star v.val*v.val = e.val ∧ e.val*v.val = 0 := by
  exact @positive_corner_from_nilpotent_exists AmbientHilbert
    ambientNormedAddCommGroup ambientInnerProductSpace ambientCompleteSpace
    core core_nilpotent_exists
#print axioms core_matrix_corner

end F1Fecho.CanonicalFockMatrixCornerR2
