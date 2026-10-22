import FiniteCoordinateMap

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.FiniteLeviCivita
open Matrix Filter Topology Set TGLExt ChatgptAudit.FiniteCoordinates
  ChatgptAudit.GeneralMetric ChatgptAudit.MetricLie
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {U W : Set Coordinate4}

def connectionPullbackJet (J D : Tensor4) (H Gamma : ConnectionMatrix4)
    (i : Fin 4) : Tensor4 :=
  D * ((∑ a : Fin 4, J a i • Gamma a) * J + H i)

def pullbackConnection (C : SmoothCoordinateChange U W) (Gamma : ConnectionField4) :
    ConnectionField4 :=
  fun x => connectionPullbackJet (changeJacobian C x) (inverseChangeJacobian C x)
    (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))

theorem metric_torsion_free_connection_unique (g gi : Tensor4)
    (dg Gamma : ConnectionMatrix4) (hg : gᵀ = g) (hi : gi*g = 1)
    (hm : ∀ i, dg i = (Gamma i)ᵀ*g + g*Gamma i)
    (ht : ∀ i j a, Gamma i a j = Gamma j a i) :
    Gamma = leviCivitaJet gi dg := by
  have hl (i j k : Fin 4) : (g*Gamma i) j k = (g*Gamma k) j i := by
    simp only [Matrix.mul_apply]
    apply Finset.sum_congr rfl
    intro a _
    rw [ht i k a]
  have hc (i j k : Fin 4) : dg i j k = (g*Gamma i) k j + (g*Gamma i) j k := by
    rw [hm i]
    have he : (Gamma i)ᵀ*g = (g*Gamma i)ᵀ := by rw [Matrix.transpose_mul,hg]
    rw [he]
    rfl
  have hh (i : Fin 4) : lowerChristoffelJet dg i = g*Gamma i := by
    ext j k
    unfold lowerChristoffelJet
    rw [hc i j k,hc k i j,hc j i k,hl k j i,hl k i j,hl j k i]
    ring
  funext i
  rw [leviCivitaJet,hh i,← Matrix.mul_assoc,hi,one_mul]

theorem connection_pullback_torsion_free (J D : Tensor4) (H Gamma : ConnectionMatrix4)
    (hH : ∀ i a j, H i a j = H j a i)
    (hG : ∀ i j a, Gamma i a j = Gamma j a i) :
    ∀ i j a, connectionPullbackJet J D H Gamma i a j =
      connectionPullbackJet J D H Gamma j a i := by
  have hin (i j b : Fin 4) :
      ((∑ a : Fin 4, J a i • Gamma a)*J + H i) b j =
        ((∑ a : Fin 4, J a j • Gamma a)*J + H j) b i := by
    simp only [Matrix.add_apply,Matrix.mul_apply,Matrix.sum_apply,Matrix.smul_apply,
      smul_eq_mul,Finset.sum_mul]
    rw [hH i b j]
    congr 1
    calc
      (∑ a : Fin 4, ∑ k : Fin 4, (J a i * Gamma a b k) * J k j) =
        ∑ k : Fin 4, ∑ a : Fin 4, (J a i * Gamma a b k) * J k j :=
          Finset.sum_comm
      _ = ∑ a : Fin 4, ∑ k : Fin 4, (J a j * Gamma a b k) * J k i := by
        apply Finset.sum_congr rfl
        intro k _
        apply Finset.sum_congr rfl
        intro a _
        rw [hG a k b]
        ring
  intro i j a
  unfold connectionPullbackJet
  simp only [Matrix.mul_apply]
  apply Finset.sum_congr rfl
  intro b _
  rw [hin i j b]

theorem connection_pullback_metric_identity (g J D : Tensor4)
    (dg H Gamma : ConnectionMatrix4) (hJD : J*D = 1)
    (hm : ∀ a, dg a = (Gamma a)ᵀ*g + g*Gamma a) (i : Fin 4) :
    (H i)ᵀ*g*J + Jᵀ*(∑ a : Fin 4, J a i • dg a)*J + Jᵀ*g*H i =
      (connectionPullbackJet J D H Gamma i)ᵀ*(Jᵀ*g*J) +
        (Jᵀ*g*J)*connectionPullbackJet J D H Gamma i := by
  let A : Tensor4 := ∑ a : Fin 4, J a i • Gamma a
  have ht : Dᵀ*Jᵀ = 1 := by rw [← Matrix.transpose_mul,hJD,Matrix.transpose_one]
  have hd : (∑ a : Fin 4, J a i • dg a) = Aᵀ*g + g*A := by
    simp_rw [hm]
    exact connection_metric_sum (fun _ => Gamma) 0 (fun a => J a i) g
  have hl : (connectionPullbackJet J D H Gamma i)ᵀ*(Jᵀ*g*J) =
      Jᵀ*Aᵀ*g*J + (H i)ᵀ*g*J := by
    change (D*(A*J+H i))ᵀ*(Jᵀ*g*J) = _
    calc
      _ = ((Jᵀ*Aᵀ+(H i)ᵀ)*(Dᵀ*Jᵀ))*g*J := by
        simp only [Matrix.transpose_mul,Matrix.transpose_add]
        noncomm_ring
      _ = _ := by rw [ht]; noncomm_ring
  have hr : (Jᵀ*g*J)*connectionPullbackJet J D H Gamma i =
      Jᵀ*g*A*J + Jᵀ*g*H i := by
    change (Jᵀ*g*J)*(D*(A*J+H i)) = _
    calc
      _ = Jᵀ*g*(J*D)*(A*J+H i) := by noncomm_ring
      _ = _ := by rw [hJD]; noncomm_ring
  rw [hd,hl,hr]
  noncomm_ring

theorem pullback_metric_jet (C : SmoothCoordinateChange U W) (g : TensorField4)
    (hg : SmoothMatrixOn W g) (x : Coordinate4) (hx : x ∈ U) (i : Fin 4) :
    tensorFieldJet (pullbackMetric C g) x i =
      (tensorFieldJet (changeJacobian C) x i)ᵀ * g (C.forward x) * changeJacobian C x +
        (changeJacobian C x)ᵀ * (∑ a : Fin 4,
          changeJacobian C x a i • tensorFieldJet g (C.forward x) a) * changeJacobian C x +
        (changeJacobian C x)ᵀ * g (C.forward x) * tensorFieldJet (changeJacobian C) x i := by
  have hJ := change_jacobian_smooth C
  have hJt := SmoothMatrixOn.transpose U _ hJ
  have hGc := matrix_composition_smooth C g hg
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U C.source_open A hA x hx
  unfold pullbackMetric
  rw [tensorFieldJet_mul _ _ x (hdiff _ (SmoothMatrixOn.mul U _ _ hJt hGc))
    (hdiff _ hJ) i]
  rw [tensorFieldJet_mul _ _ x (hdiff _ hJt) (hdiff _ hGc) i]
  rw [tensorFieldJet_transpose,tensor_jet_composition C g hg x hx i]
  noncomm_ring

theorem pullback_connection_metric_formula (C : SmoothCoordinateChange U W)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn W g) (hm : MetricCompatibleOn W g Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i : Fin 4) :
    tensorFieldJet (pullbackMetric C g) x i =
      (pullbackConnection C Gamma x i)ᵀ * pullbackMetric C g x +
        pullbackMetric C g x * pullbackConnection C Gamma x i := by
  rw [pullback_metric_jet C g hg x hx i]
  exact connection_pullback_metric_identity (g (C.forward x)) (changeJacobian C x)
    (inverseChangeJacobian C x) (tensorFieldJet g (C.forward x))
    (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))
    (jacobian_mul_inverse_jacobian C x hx)
    (metric_compatibility_formula W g Gamma hm (C.forward x) (C.forward_maps hx)) i

theorem pullback_connection_metric_compatible (C : SmoothCoordinateChange U W)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn W g) (hm : MetricCompatibleOn W g Gamma) :
    MetricCompatibleOn U (pullbackMetric C g) (pullbackConnection C Gamma) := by
  intro x hx i
  rw [covariantTensorJet,pullback_connection_metric_formula C g Gamma hg hm x hx i]
  abel

theorem pullback_connection_torsion_free (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4)
    (ht : ∀ y ∈ W, ∀ i j a, Gamma y i a j = Gamma y j a i)
    (x : Coordinate4) (hx : x ∈ U) :
    ∀ i j a, pullbackConnection C Gamma x i a j = pullbackConnection C Gamma x j a i :=
  connection_pullback_torsion_free _ _ _ _
    (change_jacobian_hessian_symmetry C x hx) (ht (C.forward x) (C.forward_maps hx))

theorem levi_civita_finite_coordinate_transformation (C : SmoothCoordinateChange U W)
    (g : TensorField4) (hg : SmoothMatrixOn W g)
    (hl : ∀ y ∈ W, LorentzByCongruence (g y))
    (x : Coordinate4) (hx : x ∈ U) :
    leviCivitaField (pullbackMetric C g) (metricInverse (pullbackMetric C g)) x =
      pullbackConnection C (leviCivitaField g (metricInverse g)) x := by
  have hs : ∀ y ∈ W, (g y)ᵀ = g y :=
    fun y hy => lorentz_metric_symmetric (g y) (hl y hy)
  have hi : ∀ y ∈ W, metricInverse g y * g y = 1 :=
    fun y hy => constructed_metric_inverse_left g y (hl y hy)
  have hir : ∀ y ∈ W, g y * metricInverse g y = 1 :=
    fun y hy => constructed_metric_inverse_right g y (hl y hy)
  have hm := levi_civita_field_metric_compatible W C.target_open g (metricInverse g) hs hi hir
  have ht := levi_civita_field_torsion_free W C.target_open g (metricInverse g) hs
  have hpg := pullback_metric_lorentz C g x hx (hl (C.forward x) (C.forward_maps hx))
  exact (metric_torsion_free_connection_unique (pullbackMetric C g x)
    (metricInverse (pullbackMetric C g) x) (tensorFieldJet (pullbackMetric C g) x)
    (pullbackConnection C (leviCivitaField g (metricInverse g)) x)
    (lorentz_metric_symmetric _ hpg)
    (constructed_metric_inverse_left (pullbackMetric C g) x hpg)
    (pullback_connection_metric_formula C g _ hg hm x hx)
    (pullback_connection_torsion_free C _ ht x hx)).symm

#print axioms connectionPullbackJet
#print axioms pullbackConnection
#print axioms metric_torsion_free_connection_unique
#print axioms connection_pullback_torsion_free
#print axioms connection_pullback_metric_identity
#print axioms pullback_metric_jet
#print axioms pullback_connection_metric_formula
#print axioms pullback_connection_metric_compatible
#print axioms pullback_connection_torsion_free
#print axioms levi_civita_finite_coordinate_transformation
end
end ChatgptAudit.FiniteLeviCivita
