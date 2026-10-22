import IndependentSubstitution
set_option autoImplicit false
open TGLExt IndependentB1Prime

example (c : TGLCoupling) (xi eta : ℝ) (h : eta ≠ xi) :
    ({ fixedData c xi with xi := eta } : ActionCouplingData Unit).EOM c probe := by
  exact baseline c xi
