import SchwartzMaxwellSmearingR3
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension

/-! A genuine spacetime Schwartz test with nonzero H1 image. The witness is
obtained by inverse Minkowski Fourier from a compact smooth momentum bump.
It does not claim compact spacetime support or spacetime locality. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter Matrix SchwartzMap Set
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def tensorUnit01 : TensorValue :=
  fun μ ν => if μ=0 ∧ ν=1 then 1 else if μ=1 ∧ ν=0 then -1 else 0

theorem tensor01_coefficient (f : SchwartzTensor) (b : Spacetime→ℂ)
    (hf : ∀ p,f p=b p•tensorUnit01) (y : MomentumCoordinates) :
    globalCoefficient f y 0=b (shellEmbedding y)*(transverseMass 0 y.1:ℂ) := by
  change (1/2:ℂ)*(∑ μ,∑ ν,(cartesianStrength y 0 μ ν:ℂ)*f (shellEmbedding y) μ ν)=_
  rw [hf]
  have h20 : (2:Fin 4)≠0 := by decide
  have h21 : (2:Fin 4)≠1 := by decide
  have h30 : (3:Fin 4)≠0 := by decide
  have h31 : (3:Fin 4)≠1 := by decide
  norm_num [Fin.sum_univ_four,tensorUnit01,h20,h21,h30,h31,cartesianStrength,
    Matrix.cons_val_zero',Matrix.cons_val_succ',Pi.smul_apply,smul_eq_mul]
  ring

theorem momentumSmear_nonzero_tensor01 (f : SchwartzTensor) (b : Spacetime→ℂ)
    (hb : Continuous b) (hf : ∀ p,f p=b p•tensorUnit01)
    (y : MomentumCoordinates) (hy : b (shellEmbedding y)*(transverseMass 0 y.1:ℂ)≠0) :
    momentumSmear f≠0 := by
  intro hz
  have hcoe := (globalCoefficient_memLp f).coeFn_toLp
  change momentumSmear f =ᵐ[orbitalMeasure 0] globalCoefficient f at hcoe
  rw [hz] at hcoe
  have ha : globalCoefficient f =ᵐ[orbitalMeasure 0] (fun _ => (0:Fib)) :=
    hcoe.symm.trans (Lp.coeFn_zero Fib 2 (orbitalMeasure 0))
  have hscalar : (fun z => b (shellEmbedding z)*(transverseMass 0 z.1:ℂ)) =ᵐ[orbitalMeasure 0]
      (fun _ => (0:ℂ)) := by
    filter_upwards [ha] with z hz
    have ht:=congrArg (fun v : Fib => v 0) hz
    simpa only [tensor01_coefficient f b hf] using ht
  letI := orbitalMeasure_openPos 0
  have hc : Continuous (fun z : MomentumCoordinates =>
      b (shellEmbedding z)*(transverseMass 0 z.1:ℂ)) :=
    (hb.comp shellEmbedding_continuous).mul (by unfold transverseMass; fun_prop)
  have he := (hc.ae_eq_iff_eq (orbitalMeasure 0) continuous_const).mp hscalar
  exact hy (congrFun he y)

theorem exists_nonzero_momentumSmear : ∃ f : SchwartzTensor,momentumSmear f≠0 := by
  let y : MomentumCoordinates := (![1,0],0)
  obtain ⟨b,_,hbc,hbs,_,hb1⟩ := exists_contDiff_tsupport_subset
    (x:=shellEmbedding y) (n:=⊤) (s:=Set.univ) (Filter.univ_mem)
  let v : Spacetime→TensorValue := fun p => (b p:ℂ)•tensorUnit01
  have hvC : HasCompactSupport v := hbc.of_isClosed_subset (isClosed_tsupport _) (by
    apply closure_mono
    intro p hp
    contrapose! hp
    simp only [Function.mem_support] at hp ⊢
    simp [v,hp])
  have hvD : ContDiff ℝ ⊤ v := (Complex.ofRealCLM.contDiff.comp hbs).smul contDiff_const
  let f : SchwartzTensor := hvC.toSchwartzMap hvD
  refine ⟨f,momentumSmear_nonzero_tensor01 f (fun p => (b p:ℂ))
    (Complex.continuous_ofReal.comp hbs.continuous) (fun _ => rfl) y ?_⟩
  simp [hb1,y,transverseMass]

theorem exists_nonzero_spacetimeSmear : ∃ f : SchwartzTensor,spacetimeSmear f≠0 := by
  obtain ⟨g,hg⟩ := exists_nonzero_momentumSmear
  obtain ⟨f,hf⟩ := minkowskiFourier_surjective g
  exact ⟨f,by simpa only [spacetimeSmear,hf] using hg⟩

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.tensor01_coefficient
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_momentumSmear
#print axioms F1Fecho.MaxwellGlobal.exists_nonzero_spacetimeSmear
