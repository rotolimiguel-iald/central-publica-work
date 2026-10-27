import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.PolarQuotientGeometry_v2

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.CalibrationReuse016
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization Matrix
open ChatgptAudit.PolarPeriod016
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/- Reused unchanged proof bodies from the named order source; source sha256 f4983661f5c3b76399d2adf8657a95e13887cc5e9ba37e7e716744501938cdc8 -/
theorem kms_product_is_two_pi (C : ContratoH2 W R N) :
    (2 * Real.pi / C.kappa) * C.kappa = 2 * Real.pi := by
  have := C.kappa_pos.ne'
  field_simp

/-- o raio de Rindler do relógio de N. -/
def refRadius (N : KillingNormalization) : ℝ := Real.sqrt (N.point 1 ^ 2 - N.point 0 ^ 2)

theorem refRadius_pos (N : KillingNormalization) : 0 < refRadius N := by
  have hx : |N.point 0| < N.point 1 := N.point_in_wedge
  obtain ⟨h1, h2⟩ := abs_lt.mp hx
  unfold refRadius
  apply Real.sqrt_pos.mpr
  nlinarith

/-- [DERIVED] κ·ρ(N) = 1. -/
theorem kappa_mul_radius (C : ContratoH2 W R N) : C.kappa * refRadius N = 1 := by
  have h := C.observer_unit
  simp [minkowskiSq, killingField] at h
  have hk : C.kappa ^ 2 * (N.point 1 ^ 2 - N.point 0 ^ 2) = 1 := by
    linear_combination h
  unfold refRadius
  rw [← Real.sqrt_sq C.kappa_pos.le, ← Real.sqrt_mul (sq_nonneg _), hk, Real.sqrt_one]

/-- [DERIVED] ★ κ = 1/ρ(N): o VALOR de κ é o do relógio externo. -/
theorem kappa_eq_inv_radius (C : ContratoH2 W R N) : C.kappa = 1 / refRadius N := by
  have h := kappa_mul_radius C
  have hne := (refRadius_pos N).ne'
  field_simp
  linarith [h]

/-- [DERIVED] ★★ κ FIXO DADO N: dois habitantes de `ContratoH2 W R N` têm o MESMO κ (o `rekappa` do cético 1 e
    o `regauge` do cético 2 NÃO habitam o mesmo tipo indexado). -/
theorem kappa_fixed (C C' : ContratoH2 W R N) : C.kappa = C'.kappa := by
  rw [kappa_eq_inv_radius C, kappa_eq_inv_radius C']

theorem no_rekappa (C : ContratoH2 W R N) {κ' : ℝ} (h : κ' ≠ C.kappa) :
    ¬ ∃ C' : ContratoH2 W R N, C'.kappa = κ' :=
  fun ⟨C', hC'⟩ => h (hC' ▸ kappa_fixed C' C)

/-- a unidade do Killing no relógio de N' com κ' = 1/ρ(N'). -/
theorem observer_unit_of_index (N' : KillingNormalization) :
    minkowskiSq (killingField (1 / refRadius N') N'.point) = 1 := by
  have hr := refRadius_pos N'
  have hsq : refRadius N' ^ 2 = N'.point 1 ^ 2 - N'.point 0 ^ 2 := by
    unfold refRadius
    have hx : |N'.point 0| < N'.point 1 := N'.point_in_wedge
    obtain ⟨h1, h2⟩ := abs_lt.mp hx
    rw [Real.sq_sqrt (by nlinarith)]
  simp [minkowskiSq, killingField]
  field_simp
  linarith [hsq]

/-- ★ RE-INDEXAR: de um habitante sobre N, outro sobre QUALQUER N' (mesmo Δit, boost, frame, bloco (P)). -/
def reindex (C : ContratoH2 W R N) (N' : KillingNormalization) : ContratoH2 W R N' where
  kappa := 1 / refRadius N'
  kappa_pos := by have := refRadius_pos N'; positivity
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := observer_unit_of_index N'
  E := C.E
  smooth_on := C.smooth_on
  det_unit_on := C.det_unit_on
  dragged := C.dragged
  fiducial_is_modular := by
    intro x hx
    obtain ⟨c, hc, h⟩ := C.fiducial_is_modular x hx
    have hk := C.kappa_pos
    have hr := refRadius_pos N'
    refine ⟨c * C.kappa * refRadius N', by positivity, ?_⟩
    rw [h]
    funext i
    simp only [killingField, Pi.smul_apply, smul_eq_mul]
    field_simp

/-- [DERIVED] ★★ HONESTO: o par (W, R) NÃO fixa κ — se há habitante sobre algum N, há sobre TODO N'. O valor
    de κ é o [INPUT] N; a v3.1 NÃO «fixa o parâmetro espectral» a partir do par. -/
theorem kappa_is_input (h : Nonempty (ContratoH2 W R N)) (N' : KillingNormalization) :
    Nonempty (ContratoH2 W R N') :=
  ⟨reindex h.some N'⟩


/-- Bridge from the constructed angular quotient to the existing contract reading.
The H2 witness remains a hypothesis; none is manufactured here. -/
theorem polar_period_matches_contract (C : ContratoH2 W R N) {period : ℝ}
    (hp : 0 < period) (h : AngularQuotientFaithful C.kappa period) :
    1/period = C.unruhTemperature := by
  exact reciprocal_temperature C.kappa_pos hp h

theorem same_normalization_same_angular_period (C C' : ContratoH2 W R N)
    {period period' : ℝ} (hp : 0 < period) (hp' : 0 < period')
    (h : AngularQuotientFaithful C.kappa period)
    (h' : AngularQuotientFaithful C'.kappa period') : period = period' := by
  rw [positive_faithful_period C.kappa_pos hp h,
    positive_faithful_period C'.kappa_pos hp' h', kappa_fixed C C']

#print axioms kms_product_is_two_pi
#print axioms refRadius
#print axioms refRadius_pos
#print axioms kappa_mul_radius
#print axioms kappa_eq_inv_radius
#print axioms kappa_fixed
#print axioms no_rekappa
#print axioms observer_unit_of_index
#print axioms reindex
#print axioms kappa_is_input
#print axioms polar_period_matches_contract
#print axioms same_normalization_same_angular_period
end ChatgptAudit.CalibrationReuse016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
