import Lean
import TGLExt.O16.ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.FieldMutations
open TGL.SpecificAQFT TGL.ModularRealization TGLExt TGLExt.ContratoQGv31
open Matrix MeasureTheory Set
noncomputable section

structure H2WithoutSmooth (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) where
  /-- (A) a normalização do campo de Killing — determinada por N (`observer_unit`). -/
  kappa : ℝ
  kappa_pos : 0 < kappa
  /-- (Δ) o implementador do fluxo de R em vetores. -/
  Δit : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  /-- (Δ) o fluxo da camada 1A de R É Ad(Δ^{it}). -/
  flow_implemented : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
    ((R.modular.modularFlow t) a).val = (Δit t).conjStarAlgEquiv a.val
  /-- (KMS) Δit é o grupo modular de (W.net rightWedge, W.vac): KMS a β = 1 para t ↦ Δit(−t). -/
  kms : KMSAt W (fun t => Δit (-t)) 1
  /-- (S) o grupo de boosts da cunha, representado em W.H. -/
  boost : WedgeBoostRep W
  /-- (S) BISOGNANO–WICHMANN COMO CAMPO: Δ^{it} = V(Λ(−2πt)). -/
  bw : ∀ t : ℝ, Δit t = boost.V (-(2 * Real.pi * t))
  /-- (P) translações fortemente contínuas. -/
  translations_continuous : ∀ ψ : W.H, Continuous (fun a : Fin 4 → ℝ => W.U a ψ)
  /-- (P) O DENTE DE FIDELIDADE: só a translação nula age trivialmente. -/
  translations_faithful : ∀ a : Fin 4 → ℝ, W.U a = 1 → a = 0
  /-- (P) energia positiva (condição espectral), forma analítica. -/
  positive_energy : PositiveEnergy W
  /-- (P) ergodicidade nula: os invariantes da translação nula são múltiplos do vácuo. -/
  null_ergodic : ∀ ψ : W.H, (∀ l : ℝ, W.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ W.vac)
  /-- (K) ★ NOVO: |ξ_κ| = 1 no ponto de referência de N — κ é a aceleração própria do relógio externo. -/
  observer_unit : minkowskiSq (killingField kappa N.point) = 1
  /-- (C) o campo de frames, REGIONAL. -/
  E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  smooth_on : True
  det_unit_on : ∀ x ∈ rightWedge, IsUnit (E x).det
  /-- (D) o jato: arrasto pelo diferencial da ação geométrica do boost. -/
  dragged : ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
    E (wedgeBoostMap s x) = boostMat s * E x
  /-- (E) a fiducial é a direção do tempo modular, positivamente. -/
  fiducial_is_modular : ∀ x ∈ rightWedge,
    ∃ c : ℝ, 0 < c ∧ (fun i => E x i 0) = c • killingField kappa x

structure H3WithoutUnit (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) where
  /-- o MESMO horizonte: o contrato H2 sobre o MESMO par (W, R) e a MESMA normalização N. -/
  H2 : ContratoH2 W R N
  /-- G [INPUT na rota de Jacobson: G = 1/(4ħη)]. -/
  G : ℝ
  G_pos : 0 < G
  /-- a classe admissível de estados (vetores unitários), fechada por translações. -/
  admissible : Set W.H
  admissible_unit : True
  vac_admissible : W.vac ∈ admissible
  admissible_translate : ∀ (a : Fin 4 → ℝ) (ψ : W.H), ψ ∈ admissible → W.U a ψ ∈ admissible
  /-- ★ O ELO MATÉRIA ↔ FLUXO MODULAR: a energia modular (bilateral) é 2π × a carga nula de T. -/
  modular_charge : ∀ ψ ∈ admissible, ∀ k : ℝ, HasModularEnergy H2.Δit ψ k →
    k = 2 * Real.pi * nullPlaneCharge T ψ
  /-- o balanço não é vazio: há estado admissível de energia modular ≠ 0. -/
  admissible_nontrivial : ∃ ψ ∈ admissible, ∃ k : ℝ, HasModularEnergy H2.Δit ψ k ∧ k ≠ 0
  /-- regularidade: T_nn é contínua ao longo de cada gerador nulo. -/
  energy_continuous : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir))
  /-- o fundo da linearização É o de H2: a tela do frame de H2 é plana (−1₂) na cunha. -/
  background_screen_flat : ∀ x ∈ rightWedge, screenBlockV31 (solderMetric4 (H2.E x)⁻¹) = -1
  /-- ★ O PROPAGADOR: a lei FIXA (antes de todo ψ) que leva o campo de tensão à perturbação de métrica. -/
  propagator : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  /-- fonte nula, resposta nula. -/
  propagator_zero : propagator 0 = 0
  /-- ★ COVARIÂNCIA DO PROPAGADOR: fonte transladada, resposta transladada. -/
  propagator_covariant : ∀ (a : Fin 4 → ℝ) (f : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ),
    propagator (fun x => f (x - a)) = fun x => propagator f (x - a)
  /-- a resposta dos estados admissíveis é simétrica. -/
  response_symm : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    (propagator (T.T ψ) x)ᵀ = propagator (T.T ψ) x
  /-- gauge do cone de luz ao longo do gerador: h·n = 0 (λ afim; a(h) é a área). -/
  lightcone_gauge : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ, (propagator (T.T ψ) x).mulVec nullDir = 0
  /-- a expansão θ_ψ(x) := d/dλ a(h_ψ)(x + λn)|₀. -/
  theta : W.H → (Fin 4 → ℝ) → ℝ
  theta_is_expansion : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => areaDensity (propagator (T.T ψ)) (x + l • nullDir)) (theta ψ x) 0
  /-- ★★ A LEI LOCAL (Raychaudhuri linear + Einstein nn), em TODO ponto: dθ/dλ = −8πG·T_nn. -/
  raychaudhuri_einstein : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => theta ψ (x + l • nullDir))
      (-(8 * Real.pi * G) * nullEnergy T ψ x) 0


variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization}

def roughFrame (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![x 1, x 0, 0, 0; x 0, x 1, 0, 0;
     0, 0, 1 + |x 2|, 0; 0, 0, 0, 1]

theorem roughFrame_det (x : Fin 4 → ℝ) :
    (roughFrame x).det = (x 1 ^ 2 - x 0 ^ 2) * (1 + |x 2|) := by
  have h : Fin.succAbove (1 : Fin 4) (2 : Fin 3) = 3 := by decide
  simp [roughFrame, Matrix.det_succ_row_zero, Fin.sum_univ_succ]
  rw [h]
  simp
  ring

theorem roughFrame_det_unit (x : Fin 4 → ℝ) (hx : x ∈ rightWedge) :
    IsUnit (roughFrame x).det := by
  rw [roughFrame_det]
  have hx' : |x 0| < x 1 := hx
  obtain ⟨h1,h2⟩ := abs_lt.mp hx'
  have hpos : 0 < x 1 ^ 2 - x 0 ^ 2 := by nlinarith
  exact isUnit_iff_ne_zero.mpr (ne_of_gt (mul_pos hpos (by positivity)))

theorem roughFrame_dragged (s : ℝ) (x : Fin 4 → ℝ) :
    roughFrame (wedgeBoostMap s x) = boostMat s * roughFrame x := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [roughFrame, wedgeBoostMap, boostMat, Matrix.mul_apply, Matrix.mulVec,
      dotProduct, Fin.sum_univ_four] <;> ring

theorem roughFrame_fiducial (κ : ℝ) (hκ : 0 < κ) (x : Fin 4 → ℝ) :
    ∃ c : ℝ, 0 < c ∧ (fun i => roughFrame x i 0) = c • killingField κ x := by
  refine ⟨κ⁻¹, inv_pos.mpr hκ, ?_⟩
  funext i
  fin_cases i <;> simp [roughFrame, killingField, Pi.smul_apply, smul_eq_mul,
    ← mul_assoc, inv_mul_cancel₀ hκ.ne']

theorem roughFrame_not_smooth :
    ¬ ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => roughFrame x i j) rightWedge := by
  intro hs
  let p : Fin 4 → ℝ := ![0,1,0,0]
  have hopen : IsOpen rightWedge :=
    isOpen_lt (continuous_apply 0).abs (continuous_apply 1)
  have hp : p ∈ rightWedge := by change |(0:ℝ)| < 1; norm_num
  have hd : DifferentiableAt ℝ (fun x => roughFrame x 2 2) p :=
    ((hs 2 2).contDiffAt (hopen.mem_nhds hp)).differentiableAt (by simp)
  have hpath : DifferentiableAt ℝ (fun t : ℝ => (![0,1,t,0] : Fin 4 → ℝ)) 0 := by
    apply differentiableAt_pi.mpr
    intro i
    fin_cases i <;> simp <;> fun_prop
  have hcomp := (hd.comp 0 hpath).sub_const 1
  apply not_differentiableAt_abs_zero
  simpa [roughFrame, Function.comp_def] using hcomp

def replaceFrame (C : ContratoH2 W R N) : H2WithoutSmooth W R N where
  kappa := C.kappa
  kappa_pos := C.kappa_pos
  Δit := C.Δit
  flow_implemented := C.flow_implemented
  kms := C.kms
  boost := C.boost
  bw := C.bw
  translations_continuous := C.translations_continuous
  translations_faithful := C.translations_faithful
  positive_energy := C.positive_energy
  null_ergodic := C.null_ergodic
  observer_unit := C.observer_unit
  E := roughFrame
  smooth_on := True.intro
  det_unit_on := roughFrame_det_unit
  dragged := fun s x _ => roughFrame_dragged s x
  fiducial_is_modular := fun x _ => roughFrame_fiducial C.kappa C.kappa_pos x

theorem zero_modular_energy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : ℝ → (H ≃ₗᵢ[ℂ] H)) (k : ℝ) (hk : HasModularEnergy D 0 k) : k = 0 := by
  have hk' : HasDerivAt (fun _ : ℝ => (0:ℂ)) (-(Complex.I * (k:ℂ))) 0 := by
    simpa [HasModularEnergy] using hk
  have he := hk'.unique (hasDerivAt_const (0:ℝ) (0:ℂ))
  have hc : (k:ℂ) = 0 := by simpa using he
  exact_mod_cast hc

def admitZero {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hT0 : ∀ x, T.T 0 x = 0) (hθ0 : ∀ x, C.theta 0 x = 0) : H3WithoutUnit W R N T where
  H2 := C.H2
  G := C.G
  G_pos := C.G_pos
  admissible := insert 0 C.admissible
  admissible_unit := True.intro
  vac_admissible := mem_insert_of_mem _ C.vac_admissible
  admissible_translate := by
    intro a ψ hψ
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simp
    · exact mem_insert_of_mem _ (C.admissible_translate a ψ hψ)
  modular_charge := by
    intro ψ hψ k hk
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · rw [zero_modular_energy C.H2.Δit k hk]
      simp [nullPlaneCharge, nullEnergy, pairing, hT0]
    · exact C.modular_charge ψ hψ k hk
  admissible_nontrivial := by
    obtain ⟨ψ,hψ,k,hk,hne⟩ := C.admissible_nontrivial
    exact ⟨ψ,mem_insert_of_mem _ hψ,k,hk,hne⟩
  energy_continuous := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simpa [nullEnergy, pairing, hT0] using
        (continuous_const : Continuous (fun _ : ℝ => (0 : ℝ)))
    · exact C.energy_continuous ψ hψ x
  background_screen_flat := C.background_screen_flat
  propagator := C.propagator
  propagator_zero := C.propagator_zero
  propagator_covariant := C.propagator_covariant
  response_symm := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simp [hz, C.propagator_zero]
    · exact C.response_symm ψ hψ x
  lightcone_gauge := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simp [hz, C.propagator_zero]
    · exact C.lightcone_gauge ψ hψ x
  theta := C.theta
  theta_is_expansion := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · have hz : T.T 0 = 0 := funext hT0
      simpa [hz, C.propagator_zero, areaDensity, hθ0] using
        (hasDerivAt_const (0:ℝ) (0:ℝ))
    · exact C.theta_is_expansion ψ hψ x
  raychaudhuri_einstein := by
    intro ψ hψ x
    rcases mem_insert_iff.mp hψ with rfl | hψ
    · simpa [hθ0, nullEnergy, pairing, hT0] using
        (hasDerivAt_const (0:ℝ) (0:ℝ))
    · exact C.raychaudhuri_einstein ψ hψ x

theorem admitZero_not_unit {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hT0 : ∀ x, T.T 0 x = 0) (hθ0 : ∀ x, C.theta 0 x = 0) :
    ¬ ∀ ψ ∈ (admitZero C hT0 hθ0).admissible, ‖ψ‖ = 1 := by
  intro h
  have he := h 0 (by simp [admitZero])
  simpa using he

#print axioms roughFrame_det
#print axioms roughFrame_det_unit
#print axioms roughFrame_dragged
#print axioms roughFrame_fiducial
#print axioms roughFrame_not_smooth
#print axioms replaceFrame
#print axioms zero_modular_energy
#print axioms admitZero
#print axioms admitZero_not_unit
end
end ChatgptAudit.FieldMutations


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
