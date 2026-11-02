import TGLExt

open scoped InnerProductSpace
open TGLExt.ImportedSQ

/-- Revisor terceiro: em todo FockCertificate existe chi unitario ortogonal ao vacuo. -/
theorem revisor_chi_existe {L : LightOneParticle} (C : FockCertificate L) :
    ∃ χ : C.F, ‖χ‖ = 1 ∧ ⟪C.Ω, χ⟫_ℂ = 0 := by
  by_contra h
  push_neg at h
  have hbot : (ℂ ∙ C.Ω)ᗮ = ⊥ := by
    rw [Submodule.eq_bot_iff]
    intro x hx
    by_contra hne
    have hx0 : ‖x‖ ≠ 0 := norm_ne_zero_iff.mpr hne
    have hn : ‖((‖x‖ : ℂ)⁻¹) • x‖ = 1 := by
      rw [norm_smul, norm_inv, Complex.norm_real, norm_norm]
      field_simp
    apply h _ hn
    rw [inner_smul_right]
    have : ⟪C.Ω, x⟫_ℂ = 0 := (Submodule.mem_orthogonal_singleton_iff_inner_right).mp hx
    rw [this, mul_zero]
  have htop : (ℂ ∙ C.Ω) = ⊤ := (Submodule.orthogonal_eq_bot_iff).mp hbot
  apply C.F_infinite
  have h3 : FiniteDimensional ℂ (ℂ ∙ C.Ω : Submodule ℂ C.F) := inferInstance
  rw [htop] at h3
  exact Module.Finite.of_surjective (Submodule.topEquiv (R := ℂ) (M := C.F)).toLinearMap (Submodule.topEquiv (R := ℂ) (M := C.F)).surjective

#print axioms revisor_chi_existe
#print axioms TGLExt.LeiDoDiminuto.the_diminished_law_closes
#print axioms TGLExt.LeiDoDiminuto.mesmas_razoes_iff_transposicao
#print axioms TGLExt.LeiDoDiminuto.modular_nao_e_transposicao
#print axioms TGLExt.LeiDoDiminuto.resolver_modular
#print axioms TGLExt.LeiDoDiminuto.um_tom_vira_terca_menor
#print axioms TGLExt.LeiDoDiminuto.meioTom_e_o_pedagio_local
#print axioms TGLExt.LeiDoDiminuto.tonica_e_o_volume_da_face
#print axioms TGLExt.LeiDoDiminuto.Lei.E0_e_a_leitura
#print axioms TGLExt.PontoZeroDoPsion.lock_no_angulo_de_miguel
#print axioms TGLExt.PontoZeroDoPsion.o_lock_tem_gap_um
#print axioms TGLExt.PontoZeroDoPsion.the_gap_closes
#print axioms TGLExt.PontoZeroDoPsion.o_relogio_do_retido
#print axioms TGLExt.PontoZeroDoPsion.o_gap_com_unidade
#print axioms TGLExt.PontoZeroDoPsion.o_retido_e_o_valor_esperado_do_lock
#print axioms TGLExt.PontoZeroDoPsion.HminMic_e_o_lock
#print axioms TGLExt.PontoZeroDoPsion.lock_no_angulo
#print axioms TGLExt.PontoZeroDoPsion.a_frequencia_do_sistema_e_a_do_psion_iff
#print axioms TGLExt.PontoZeroDoPsion.a_qualidade_nao_depende_da_unidade
#print axioms TGLExt.TonicaDoHamiltoniano.the_ratio_survives_the_rescaling
#print axioms TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law
#print axioms TGLExt.ObservadorTerminal.the_omega_pole_reads_one
#print axioms TGLExt.ObservadorTerminal.the_observers_posto_is_the_terminal
#print axioms TGLExt.PonteDaMassa.TransicaoParaAMassa.massa_derivada_eq_form
#print axioms TGLExt.Identidade.a_identidade_fecha
#print axioms TGLExt.MassaTensaoPura.massa_e_tensao_pura
#check @TGLExt.alpha_transport
#check @TGLExt.zero_mode_weight_is_one
#check @TGLExt.Sonico.the_pin_is_not_the_half_nat
#print ChatgptAudit.Collapse057.CollapseCostLaw

#check @TGLExt.PontoZeroDoPsion.lockDe
example {L : LightOneParticle} (C : FockCertificate L) : TGLExt.QGReaderUVLock.HminMic C = TGLExt.PontoZeroDoPsion.lockDe C.Ω := rfl
example {L : LightOneParticle} (C : FockCertificate L) (χ : C.F) (hχ : ‖χ‖ = 1) (hort : ⟪C.Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    ⟪(Real.cos θ : ℂ) • C.Ω + (Real.sin θ : ℂ) • χ, TGLExt.QGReaderUVLock.HminMic C ((Real.cos θ : ℂ) • C.Ω + (Real.sin θ : ℂ) • χ)⟫_ℂ = ((Real.sin θ ^ 2 : ℝ) : ℂ) :=
  TGLExt.PontoZeroDoPsion.lock_no_angulo C.Ω χ hχ hort θ
