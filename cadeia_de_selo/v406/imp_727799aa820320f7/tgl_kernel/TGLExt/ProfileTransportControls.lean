-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_027 (06/09/2026), transposta em 06/09/2026
-- Lote 027..028: EQUIVALENCIA UNITARIA entre os GNS de perfis com afinidade positiva e o TRANSPORTE
--   MODULAR com dominios — Tomita do estado global Phi no Hilbert original (grafo fechado, S, J, Delta,
--   JS = Delta^{1/2} positivo auto-adjunto), grupo modular fortemente continuo que preserva fator e
--   estado, instancia nao trivial (perfil gradual: autovalor transportado 5/7); RESPOSTA GLOBAL finita
--   sem corte (familia de amplitude somavel, fiel), limite conjunto corte/tempo, contraexemplo
--   HARMONICO (entropia relativa finita com incremento modular e entropia DIVERGENTES);
--   einstein_from_summable_area_matching (condicional). Estatuto [REAL / INPUT / OPEN]: a lei de area
--   microscopica NAO foi derivada da torre (controle plano o impede); selecao fisica, H3 dinamico,
--   assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 20/20 + 20/20; manifestos 231/238;
--   2/2 auditores da bancada exit 0; recompilacao INDEPENDENTE 16/16, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ProfileFlowTransport

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set UniformSpace TGLExt ChatgptAudit.Profile026 ChatgptAudit.Thermal025
noncomputable section

theorem relative_filter_same {ι : Type} [DecidableEq ι] (p : ι → ℝ) (hp : ∀ i, 0<p i) :
    relativeFilter p p=1 := by
  ext i j
  by_cases hij : i=j
  · subst j
    simp [relativeFilter,ne_of_gt (hp i)]
  · simp [relativeFilter,hij]

theorem profile_vectors_same (P : SiteProfile) (N : ℕ) :
    profileVector P P N=hOmega P := by
  rw [profileVector,relative_filter_same _ (towerW_pos P N),towerPi_one]
  rfl

theorem global_profile_vector_same (P : SiteProfile) (hpos : 0<profileAffinityLimit P P) :
    globalProfileVector P P hpos=hOmega P := by
  have ht := global_profile_vector_tendsto P P hpos
  change Tendsto (fun N => profileVector P P N) atTop (𝓝 (globalProfileVector P P hpos)) at ht
  simp only [profile_vectors_same] at ht
  exact tendsto_nhds_unique ht tendsto_const_nhds

theorem profile_unitary_self (P : SiteProfile) (hpos : 0<profileAffinityLimit P P)
    (x : TowerHilbert P) : profileGNSUnitary P P hpos x=x := by
  refine Completion.induction_on x
    (isClosed_eq (profileGNSUnitary P P hpos).continuous continuous_id) ?_
  intro a
  obtain ⟨N,b,rfl⟩ := exists_tof a
  rw [profile_gns_unitary_local,global_profile_vector_same,towerPi_omega]

theorem profile_unitary_self_symm (P : SiteProfile) (hpos : 0<profileAffinityLimit P P)
    (x : TowerHilbert P) : (profileGNSUnitary P P hpos).symm x=x := by
  have h := (profileGNSUnitary P P hpos).apply_symm_apply x
  rw [profile_unitary_self] at h
  exact h

theorem profile_factor_conjugation_self (P : SiteProfile) (hpos : 0<profileAffinityLimit P P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) : profileFactorConjugation P P hpos A=A := by
  ext x
  rw [profile_factor_conjugation_apply,profile_unitary_self_symm,profile_unitary_self]

theorem profile_j_self (P : SiteProfile) (hpos : 0<profileAffinityLimit P P)
    (x : TowerHilbert P) : profileJ P P hpos x=towerJ P x := by
  rw [profile_j_apply,profile_unitary_self_symm,profile_unitary_self]

theorem profile_flow_self (P : SiteProfile) (hpos : 0<profileAffinityLimit P P)
    (t : ℝ) (x : TowerHilbert P) : profileModularFlow P P hpos t x=modularFlow P t x := by
  rw [profile_flow_apply,profile_unitary_self_symm,profile_unitary_self]

theorem gradual_profile_vector_ne_reference :
    globalProfileVector thirdThermalReference gradualProfile gradual_profile_affinity_positive≠hOmega thirdThermalReference := by
  intro hv
  apply gradual_state_not_reference
  funext A
  change inner ℂ (globalProfileVector thirdThermalReference gradualProfile gradual_profile_affinity_positive)
      (A (globalProfileVector thirdThermalReference gradualProfile gradual_profile_affinity_positive))=
    inner ℂ (hOmega thirdThermalReference) (A (hOmega thirdThermalReference))
  rw [hv]

theorem old_modular_orbit_ne_gradual (t : ℝ) :
    modularFlow thirdThermalReference t (hOmega thirdThermalReference)≠
      globalProfileVector thirdThermalReference gradualProfile gradual_profile_affinity_positive := by
  rw [modularFlow_fixes_omega]
  exact Ne.symm gradual_profile_vector_ne_reference

theorem gradual_first_eigenvalue :
    localEigenvalue gradualProfile 0 (0 : Fin 2) 1=5/7 := by
  norm_num [localEigenvalue,towerW,siteW,gradualProfile]

theorem reference_first_eigenvalue :
    localEigenvalue thirdThermalReference 0 (0 : Fin 2) 1=1/2 := by
  norm_num [localEigenvalue,towerW,siteW,thirdThermalReference]

theorem gradual_eigenvalue_differs :
    localEigenvalue gradualProfile 0 (0 : Fin 2) 1≠
      localEigenvalue thirdThermalReference 0 (0 : Fin 2) 1 := by
  rw [gradual_first_eigenvalue,reference_first_eigenvalue]
  norm_num

theorem gradual_transported_delta_value :
    profileDeltaOperator thirdThermalReference gradualProfile gradual_profile_affinity_positive
      ⟨profileEigenvector thirdThermalReference gradualProfile gradual_profile_affinity_positive 0 0 1,
        profile_eigenvector_mem_delta _ _ _ 0 0 1⟩=
      (5/7 : ℂ) • profileEigenvector thirdThermalReference gradualProfile gradual_profile_affinity_positive 0 0 1 := by
  rw [profile_delta_eigenvector,gradual_first_eigenvalue]
  norm_num

theorem gradual_transported_flow_value (t : ℝ) :
    profileModularFlow thirdThermalReference gradualProfile gradual_profile_affinity_positive t
      (profileEigenvector thirdThermalReference gradualProfile gradual_profile_affinity_positive 0 0 1)=
      modularPhase t (Real.log (5/7)) •
        profileEigenvector thirdThermalReference gradualProfile gradual_profile_affinity_positive 0 0 1 := by
  rw [profile_flow_eigenvector,gradual_first_eigenvalue]

#print axioms relative_filter_same
#print axioms profile_vectors_same
#print axioms global_profile_vector_same
#print axioms profile_unitary_self
#print axioms profile_unitary_self_symm
#print axioms profile_factor_conjugation_self
#print axioms profile_j_self
#print axioms profile_flow_self
#print axioms gradual_profile_vector_ne_reference
#print axioms old_modular_orbit_ne_gradual
#print axioms gradual_first_eigenvalue
#print axioms reference_first_eigenvalue
#print axioms gradual_eigenvalue_differs
#print axioms gradual_transported_delta_value
#print axioms gradual_transported_flow_value
end
end ChatgptAudit.Transport027
