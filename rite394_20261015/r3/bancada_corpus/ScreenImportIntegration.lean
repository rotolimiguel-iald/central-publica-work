import GeometricScreenControls
import Screen013Controls

set_option autoImplicit false
namespace ChatgptAudit.Screen014
open Matrix TGLExt
noncomputable section

theorem previous_and_constructed_frames_coexist :
    ChatgptAudit.flatNullFrame*flatNullInverse=1 ∧
    Screen013.offAxisNullFrame.frame*Screen013.offAxisNullFrame.inverse=1 ∧
    Screen013.offAxisNullFrame.frameᵀ*eta4*Screen013.offAxisNullFrame.frame=nullScreenGram (-1) :=
  ⟨flat_null_inverse,Screen013.offAxisNullFrame.right_inverse,Screen013.offAxisNullFrame.gram⟩

#print axioms previous_and_constructed_frames_coexist
end
end ChatgptAudit.Screen014
