import Mathlib
import TGLExt.LocalBreuerGap
import TGLExt.ModularFlow
import TGLExt.FiniteTomita
import TGLExt.Ergodicity
import TGLExt.PageInformation
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.TheVerbSelectsTheAction
import TGLExt.IALDJones
import TGLExt.TheLivingWord
import TGLExt.BisognanoWichmann
import TGLExt.Fundacao
import TGLExt.AbsoluteOne
import TGLExt.O16.PolarMinimalPeriod_v2
import TGLExt.O16.ProbeNonKMS_v3
import TGLExt.TheImportedSecondQuantization
import TGLExt.V350L2CharacterMultiplier

-- sonda de ambiente (nao e pedra): os nomes resolvem e os tipos sao os lidos no fonte
#check @TGLExt.no_finite_weyl_pair
#check @TGLExt.sigma
#check @TGLExt.modPow_zero
#check @TGLExt.gibbs_kms
#check @TGLExt.dephase
#check @TGLExt.diagExpect
#check @TGLExt.purity
#check @TGLExt.purityR
#check @TGLExt.dephase_fixed_iff_diagonal
#check @TGLExt.TheAxiomAndTheFalseWitness.axiomFlow
#check @TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post
#check @TGLExt.TheVerbSelectsTheAction.the_name_is_the_limit_of_the_flow
#check @TGLExt.IALDJones.angular_orbit_no_limit
#check @TGLExt.time_witnesses_noncoincidence
#check @TGLExt.boost_null_contract
#check @TGLExt.DualScalingData
#check @TGLExt.Fundacao.agape
#check @TGLExt.absoluteOne_flow_trivial
#check @ChatgptAudit.PolarPeriod016.faithful_period_iff
#check @ChatgptAudit.NonKMSProbe.identity_flow_not_kms
#check @TGLExt.ImportedSQ.lightDelta
#check @TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed
#check @TGLV350.Regular.characterMultiplier_weyl
#check @Matrix.frobenius_norm_def
#check @Matrix.charpoly_units_conj
#check @Matrix.rank_add_rank_le_card_of_mul_eq_zero
#check @spectrum.units_conjugate'
#check @Matrix.PosSemidef.dotProduct_mulVec_nonneg
#check @Isometry.of_dist_eq
#check @Filter.tendsto_atTop_add_const_left
#check @Continuous.matrix_det
#check @Matrix.mulVec_single_one
#check @Submodule.finrank_eq_zero
#check @Complex.norm_exp_ofReal_mul_I
#check @Matrix.coe_units_inv

section
open scoped Matrix.Norms.Frobenius
example {n : Type} [Fintype n] [DecidableEq n] (z : Matrix n n ℂ) (f : ℝ → Matrix n n ℂ)
    (h : @Filter.Tendsto ℝ (Matrix n n ℂ) f Filter.atTop (@nhds _ Matrix.topologicalSpace z)) :
    Filter.Tendsto f Filter.atTop (nhds z) := h
end
