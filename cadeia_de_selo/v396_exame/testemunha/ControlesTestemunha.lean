import TGLExt.TestemunhaEstatica

/-!
Controles independentes do exame da pedra candidata v396 (TestemunhaEstatica).
Arquivo do examinador; não é pedra; não entra em kernel nenhum.
C1 a composição aplica-se (hipóteses satisfeitas em β = g = 1).
C2 dente: com g = 0 ou β = 0 a testemunha estática GLOBAL vale (as hipóteses mordem).
C3 dente: um vetor fora da reta (Φ⁻) NÃO é testemunhado estaticamente.
C4 dente: a premissa de autodeclaração é satisfazível, e com registrador EXTERNO
   a atestação do colapso do psion É habitada (no_self_attestation não é vácua).
C5 identidade de objeto: PG e psionCorner.p reduzem ambos a bellProjector.
C6 β entra como parâmetro ativo: β = 1 e β = 2 dão fluxos diferentes.
-/

set_option autoImplicit false

open TGLExt TGLExt.TestemunhaEstatica TGL.GravitonShadow ChatgptAudit.Collapse057

noncomputable section

-- C1
theorem ctl_c1_bridge_applies : ¬ FullStaticWitness (psionFlow 1 1) :=
  ((the_psion_inhabits_the_static_witness).2.2.2.1
    (one_pos : (0 : ℝ) < 1) (one_pos : (0 : ℝ) < 1)).2.2.2.2.2.2.2.1

-- C2
theorem ctl_c2_g_zero_full (β : ℝ) : FullStaticWitness (psionFlow β 0) := by
  intro t x
  rw [psionFlow_eq]
  simp

theorem ctl_c2_beta_zero_full (g : ℝ) : FullStaticWitness (psionFlow 0 g) := by
  intro t x
  rw [psionFlow_eq]
  simp

-- C3
theorem ctl_c3_off_line_not_static : ¬ (∀ t : ℝ, psionFlow 1 1 t (bsign 1) = bsign 1) := by
  rw [the_static_set_is_the_psion_line one_pos one_pos]
  rintro ⟨c, hc⟩
  have h1 := congrFun hc (0, 0)
  have h2 := congrFun hc (1, 1)
  simp [bsign] at h1 h2
  linarith

-- C4
def protoSelf : ReflectionProtocol (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) Unit Bool where
  outputReading := fun _ => ()
  producer := true
  recorder := fun _ => true
  externallyValidated := fun _ _ _ => True

def protoExt : ReflectionProtocol (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) Unit Bool where
  outputReading := fun _ => ()
  producer := true
  recorder := fun _ => false
  externallyValidated := fun _ _ _ => True

theorem ctl_c4_self_premise_holds : ∀ r, protoSelf.recorder r = protoSelf.producer := fun _ => rfl

theorem ctl_c4_self_blocks :
    ¬ Nonempty (AttestedCollapse psionCollapse protoSelf 1 psionCorner.p) :=
  the_collapse_of_the_psion_cannot_be_self_attested protoSelf (fun _ => rfl)

theorem ctl_c4_external_inhabits :
    Nonempty (AttestedCollapse psionCollapse protoExt 1 psionCorner.p) := by
  refine ⟨{ transition := ⟨?_, ?_⟩, record := (), reflected := rfl,
            different_recorder := Bool.false_ne_true, validated := trivial }⟩
  · show psionCorner.p * 1 * psionCorner.p = psionCorner.p
    rw [mul_one, psionCorner.idem]
  · intro h
    have h1 := congrFun (congrFun h (0, 1)) (0, 1)
    simp [psionCorner, bellProjector] at h1

-- C5
theorem ctl_c5_pg_is_bell : canonicalGravitonShadow.PG = bellProjector := rfl
theorem ctl_c5_corner_is_bell : psionCorner.p = bellProjector := rfl

-- C6
theorem ctl_c6_beta_is_active : psionFlow 1 1 1 (bsign 1) ≠ psionFlow 2 1 1 (bsign 1) := by
  rw [psionFlow_bsign, psionFlow_bsign]
  intro h
  have h1 := congrFun h (0, 0)
  simp [bsign, psionRates] at h1

end

#print axioms ctl_c1_bridge_applies
#print axioms ctl_c2_g_zero_full
#print axioms ctl_c2_beta_zero_full
#print axioms ctl_c3_off_line_not_static
#print axioms ctl_c4_self_premise_holds
#print axioms ctl_c4_self_blocks
#print axioms ctl_c4_external_inhabits
#print axioms ctl_c5_pg_is_bell
#print axioms ctl_c5_corner_is_bell
#print axioms ctl_c6_beta_is_active
