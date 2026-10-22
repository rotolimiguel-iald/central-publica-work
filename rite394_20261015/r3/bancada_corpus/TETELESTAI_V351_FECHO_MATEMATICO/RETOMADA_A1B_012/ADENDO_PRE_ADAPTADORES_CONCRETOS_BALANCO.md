[OPEN] Adaptadores concretos para consumir o balanço limitado

2026-09-15T01:51:43.575821-03:00

A consulta independente localizou a via pontual: injetividade de a.val passa às conjugações unitárias dualAmbient, ao operatorFieldLift por duas igualdades a.e. para cada par de vetores, e à restrição no GNS original por Subtype.ext. Não usar fidelidade da representação como substituta de injetividade vetorial. O cálculo funcional deve ser transportado pela inclusão da álgebra normativamente fechada e pela mesma pi contínua, usando map_cfc existente. A identidade de fases concreta e as comutações necessárias continuam abertas. Os três adaptadores privados já escritos passaram apenas DEV; não são uma entrega33 nem a tracialidade. Balanço de cortes reais e Q permanecem OPEN.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:23
```lean
theorem dualAmbient_apply (s : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s A = characterMultiplier s * A * star (characterMultiplier (H := H) s) := rfl
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:94
```lean
/-- D_s, as a bounded complex-linear operator on the actual Lebesgue L² space. -/
def characterMultiplier (s : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  (characterMultiplierIsometry s).toContinuousLinearMap
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68
```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x) := operatorFieldLp_ae F f
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightCuts.lean:14
```lean
def dualIntegralFamily (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    StrongIntegral.Family (H := RegularHilbert H) where
  op := fun s => dualAmbient s A
  continuous_apply := dualAmbient_strongly_continuous A
  bound := ‖A‖
  bound_nonneg := norm_nonneg A
  norm_bound := fun s => le_of_eq
    ((StarAlgEquiv.isometry (dualAmbient (H := H) s)).norm_map_of_map_zero
      (map_zero (dualAmbient (H := H) s)) A)

/-- A finite strong integral of the dual action. This is unnormalized, and is
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ReducingStarRepresentation.lean:13
```lean
Invariance is required for every algebra element, hence also for adjoints. -/
def reducingStarRepresentation (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) : A →⋆ₐ[ℂ] (S →L[ℂ] S) where
  toFun a := (ρ a).restrict (h a)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSRepresentation.lean:14
```lean
def scalarGNSRepresentation (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →⋆ₐ[ℂ]
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (regularCoreAlgebra P).toStarSubalgebra.subtype)
    (scalarGNSSubspace P) (scalarGNSAmbientAction_preserves P)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSCompletion.lean:48
```lean
theorem scalarGNSAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) : ‖scalarGNSAction P B‖ ≤ ‖B.val‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro v
  exact (scalarGNSAmbientAction P B).le_of_opNorm_le
    (scalarGNSAmbientAction_norm_le P B) v.val
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:98
```lean
theorem regularSpectralResolvent_injective (P : SiteProfile) :
    Function.Injective (regularSpectralResolvent P) :=
  (regularSpectralCoordinates P).injective.comp
    ((realScalarMultiplier_injective _ _ _ _ (fun _ => Real.sigmoid_pos _)).comp
      (regularSpectralCoordinates P).symm.injective)

theorem regularSpectralResolvent_complement_injective (P : SiteProfile) :
    Function.Injective (1-regularSpectralResolvent P :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) := by
  let g : ℝ → ℝ := fun x => Real.sigmoid (2*Real.pi*x)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ x, 0 ≤ g x := fun x => Real.sigmoid_nonneg _
  have h1 : ∀ x, g x ≤ 1 := fun x => Real.sigmoid_le_one _
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:486
```lean
lemma StarAlgHom.map_cfc (φ : A →⋆ₐ[S] B) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac) (hφ : Continuous φ := by fun_prop)
    (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a) :=
  StarAlgHomClass.map_cfc φ f a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\Classes.lean:50
```lean
noncomputable instance StarSubalgebra.cstarAlgebra {S A : Type*} [CStarAlgebra A]
    [SetLike S A] [SubringClass S A] [SMulMemClass S ℂ A] [StarMemClass S A]
    (s : S) [h_closed : IsClosed (s : Set A)] : CStarAlgebra s where
  toCompleteSpace := h_closed.completeSpace_coe
  norm_mul_self_le x := CStarRing.norm_star_mul_self (x := (x : A)) |>.symm.le
```

