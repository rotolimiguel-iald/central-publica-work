import CartesianMaxwellBivectorR6

/-! Exact on-shell polarization identities needed by a future Plancherel
charge calculation. These identities alone do not establish an integrated
charge or fix the physical Fourier normalization. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix ChatgptAudit.WignerRapidityMeasure016

def screenEnergyPair (y z : MomentumCoordinates) (j k : Fin 2) : ℝ :=
  cartesianStrength y j 0 1*cartesianStrength z k 0 1+
  cartesianStrength y j 0 2*cartesianStrength z k 0 2+
  cartesianStrength y j 0 3*cartesianStrength z k 0 3+
  cartesianStrength y j 1 2*cartesianStrength z k 1 2+
  cartesianStrength y j 1 3*cartesianStrength z k 1 3+
  cartesianStrength y j 2 3*cartesianStrength z k 2 3

theorem transverseRatio_sq_sum (y : MomentumCoordinates) (hy : y.1≠0) :
    transverseRatio y 0^2+transverseRatio y 1^2=1 := by
  have hr:transverseMass 0 y.1≠0:=(transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hs:=transverseMass_sq 0 y.1
  dsimp [transverseRatio]
  field_simp [hr]
  nlinarith

theorem screenEnergyPair_diagonal (y : MomentumCoordinates) (hy : y.1≠0) (j k : Fin 2) :
    screenEnergyPair y y j k=if j=k then 2*shellEnergy y^2 else 0 := by
  have hr:=transverseRatio_sq_sum y hy
  have he:=shellEnergy_sq y
  have ht:=transverseMass_sq 0 y.1
  have h1:=congrArg (fun z : ℝ=>z*shellEnergy y^2) hr
  have h2:=congrArg (fun z : ℝ=>z*y.2^2) hr
  fin_cases j <;> fin_cases k <;>
    simp [screenEnergyPair,cartesianStrength] <;> nlinarith

theorem transverseMass_neg (q : Transverse) : transverseMass 0 (-q)=transverseMass 0 q := by
  simp [transverseMass]

theorem shellEnergy_neg (y : MomentumCoordinates) : shellEnergy (-y)=shellEnergy y := by
  simp [shellEnergy,energy,transverseMass_neg]

theorem transverseRatio_neg (y : MomentumCoordinates) (j : Fin 2) :
    transverseRatio (-y) j= -transverseRatio y j := by
  simp [transverseRatio,transverseMass_neg,neg_div]

theorem screenEnergyPair_opposite (y : MomentumCoordinates) (hy : y.1≠0) (j k : Fin 2) :
    screenEnergyPair y (-y) j k=0 := by
  have hr:=transverseRatio_sq_sum y hy
  have he:=shellEnergy_sq y
  have ht:=transverseMass_sq 0 y.1
  have h1:=congrArg (fun z : ℝ=>z*shellEnergy y^2) hr
  have h2:=congrArg (fun z : ℝ=>z*y.2^2) hr
  fin_cases j <;> fin_cases k <;>
    simp [screenEnergyPair,cartesianStrength,transverseMass_neg,shellEnergy_neg,
      transverseRatio_neg] <;> nlinarith

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.transverseRatio_sq_sum
#print axioms F1Fecho.MaxwellGlobal.screenEnergyPair_diagonal
#print axioms F1Fecho.MaxwellGlobal.screenEnergyPair_opposite
