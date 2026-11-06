import TGLExt.F1Fecho394.ClosedSubmoduleRestrictionR2
set_option autoImplicit false
noncomputable section
namespace F1Fecho.ClosedSubmoduleRestriction
variable {E:Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (S:Submodule ℂ E) [CompleteSpace S]
theorem endomorphismStar_mul (A B:S→L[ℂ]S) :
    @star _ (endomorphismStar S) (A*B)=
      @star _ (endomorphismStar S) B * @star _ (endomorphismStar S) A :=
  star_mul A B
end F1Fecho.ClosedSubmoduleRestriction
#print axioms F1Fecho.ClosedSubmoduleRestriction.endomorphismStar_mul
