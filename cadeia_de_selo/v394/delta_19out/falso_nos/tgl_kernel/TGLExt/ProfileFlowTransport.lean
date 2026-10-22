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
import TGLExt.ProfileModularTransport

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt ChatgptAudit.Profile026
noncomputable section

def profileModularFlow (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (t : ℝ) :
    TowerHilbert P ≃ₗᵢ[ℂ] TowerHilbert P :=
  (profileGNSUnitary P Q hpos).symm.trans ((modularFlowUnitary Q t).trans (profileGNSUnitary P Q hpos))

theorem profile_flow_apply (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (x : TowerHilbert P) :
    profileModularFlow P Q hpos t x=profileGNSUnitary P Q hpos
      (modularFlow Q t ((profileGNSUnitary P Q hpos).symm x)) := rfl

theorem profile_flow_on_unitary (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (x : TowerHilbert Q) :
    profileModularFlow P Q hpos t (profileGNSUnitary P Q hpos x)=
      profileGNSUnitary P Q hpos (modularFlow Q t x) := by
  rw [profile_flow_apply,LinearIsometryEquiv.symm_apply_apply]

theorem profile_flow_group (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (s t : ℝ) (x : TowerHilbert P) :
    profileModularFlow P Q hpos s (profileModularFlow P Q hpos t x)=profileModularFlow P Q hpos (s+t) x := by
  simp only [profile_flow_apply,LinearIsometryEquiv.symm_apply_apply,modularFlow_group]

theorem profile_flow_zero (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert P) : profileModularFlow P Q hpos 0 x=x := by
  rw [profile_flow_apply,modularFlow_zero_time,LinearIsometryEquiv.apply_symm_apply]

theorem profile_flow_fixes_vector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (t : ℝ) :
    profileModularFlow P Q hpos t (globalProfileVector P Q hpos)=globalProfileVector P Q hpos := by
  rw [←profile_gns_unitary_omega,profile_flow_on_unitary,modularFlow_fixes_omega]

theorem profile_flow_strongly_continuous (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert P) : Continuous (fun t : ℝ => profileModularFlow P Q hpos t x) := by
  change Continuous (fun t => profileGNSUnitary P Q hpos (modularFlow Q t ((profileGNSUnitary P Q hpos).symm x)))
  exact (profileGNSUnitary P Q hpos).continuous.comp (modularFlow_strongly_continuous _)

def profileFlowConjugation (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (t : ℝ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) ≃⋆ₐ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  (profileModularFlow P Q hpos t).conjStarAlgEquiv

theorem profile_flow_conjugation_eq (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    profileFlowConjugation P Q hpos t A=
      profileFactorConjugation P Q hpos
        (modularConjugation Q t ((profileFactorConjugation P Q hpos).symm A)) := by
  ext x
  rfl

theorem profile_flow_preserves_factor (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    A∈theFactorObject P ↔ profileFlowConjugation P Q hpos t A∈theFactorObject P := by
  rw [profile_flow_conjugation_eq,←profile_factor_conjugation_iff,←modularConjugation_preserves_factor]
  simpa only [StarAlgEquiv.apply_symm_apply] using
    (profile_factor_conjugation_iff P Q hpos ((profileFactorConjugation P Q hpos).symm A)).symm

theorem profile_flow_preserves_state (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    globalProfileState P Q hpos (profileFlowConjugation P Q hpos t A)=globalProfileState P Q hpos A := by
  rw [profile_flow_conjugation_eq,profile_factor_state_transport,modularConjugation_preserves_state]
  simpa only [StarAlgEquiv.apply_symm_apply] using
    (profile_factor_state_transport P Q hpos ((profileFactorConjugation P Q hpos).symm A)).symm

theorem profile_flow_local_conjugation (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileFlowConjugation P Q hpos t (towerPi P a)=towerPi P (flowLevel Q t N a) := by
  rw [profile_flow_conjugation_eq,←profile_factor_conjugation_local P Q hpos N a,
    StarAlgEquiv.symm_apply_apply,modularConjugation_local,profile_factor_conjugation_local]

theorem profile_flow_local_vector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileModularFlow P Q hpos t (towerPi P a (globalProfileVector P Q hpos))=
      towerPi P (flowLevel Q t N a) (globalProfileVector P Q hpos) := by
  rw [←profile_gns_unitary_local P Q hpos N a,profile_flow_on_unitary,
    modularFlow_coe,flowPre_tof,profile_gns_unitary_local]

def profileEigenvector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (i j : chainIdx N) : TowerHilbert P :=
  profileGNSUnitary P Q hpos (localEigenvector Q N i j)

theorem profile_eigenvector_mem_delta (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (i j : chainIdx N) :
    profileEigenvector P Q hpos N i j∈(profileDeltaOperator P Q hpos).domain := by
  change (profileGNSUnitary P Q hpos).symm
    (profileGNSUnitary P Q hpos (localEigenvector Q N i j))∈modularSquareDomain Q
  rw [LinearIsometryEquiv.symm_apply_apply]
  exact localEigenvector_mem N i j

theorem profile_delta_eigenvector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (i j : chainIdx N) :
    profileDeltaOperator P Q hpos ⟨profileEigenvector P Q hpos N i j,profile_eigenvector_mem_delta P Q hpos N i j⟩=
      (localEigenvalue Q N i j:ℂ) • profileEigenvector P Q hpos N i j := by
  have hi : unitaryPartialInput (profileGNSUnitary P Q hpos) (towerDeltaClosed Q)
      ⟨profileEigenvector P Q hpos N i j,profile_eigenvector_mem_delta P Q hpos N i j⟩=
      (⟨localEigenvector Q N i j,localEigenvector_mem N i j⟩ : modularSquareDomain Q) := by
    apply Subtype.ext
    exact (profileGNSUnitary P Q hpos).symm_apply_apply _
  change profileGNSUnitary P Q hpos (towerDeltaClosed Q
    (unitaryPartialInput (profileGNSUnitary P Q hpos) (towerDeltaClosed Q)
      ⟨profileEigenvector P Q hpos N i j,profile_eigenvector_mem_delta P Q hpos N i j⟩))=_
  rw [hi]
  exact (congrArg (profileGNSUnitary P Q hpos) (delta_eigenvector (P := Q) N i j)).trans
    ((profileGNSUnitary P Q hpos).map_smul (localEigenvalue Q N i j : ℂ) (localEigenvector Q N i j))

theorem profile_flow_eigenvector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (N : ℕ) (i j : chainIdx N) :
    profileModularFlow P Q hpos t (profileEigenvector P Q hpos N i j)=
      modularPhase t (Real.log (localEigenvalue Q N i j)) • profileEigenvector P Q hpos N i j := by
  rw [profileEigenvector,profile_flow_on_unitary,modularFlow_eigenvector,map_smul]

theorem profile_flow_spectral_unique (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (t : ℝ) (T : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hT : ∀ (N : ℕ) (i j : chainIdx N), T (profileEigenvector P Q hpos N i j)=
      modularPhase t (Real.log (localEigenvalue Q N i j)) • profileEigenvector P Q hpos N i j)
    (x : TowerHilbert P) : T x=profileModularFlow P Q hpos t x := by
  let e := profileGNSUnitary P Q hpos
  let R := (profileFactorConjugation P Q hpos).symm T
  have hr : ∀ (N : ℕ) (i j : chainIdx N), R (localEigenvector Q N i j)=
      modularPhase t (Real.log (localEigenvalue Q N i j)) • localEigenvector Q N i j := by
    intro N i j
    apply e.injective
    change e (e.symm (T (e (localEigenvector Q N i j))))=
      e (modularPhase t (Real.log (localEigenvalue Q N i j)) • localEigenvector Q N i j)
    rw [e.apply_symm_apply,e.map_smul]
    exact hT N i j
  calc
    T x=profileFactorConjugation P Q hpos R x := by
      change T x=profileFactorConjugation P Q hpos ((profileFactorConjugation P Q hpos).symm T) x
      rw [StarAlgEquiv.apply_symm_apply]
    _=e (R (e.symm x)) := profile_factor_conjugation_apply P Q hpos R x
    _=e (modularFlow Q t (e.symm x)) := by rw [modularFlow_spectral_unique t R hr]
    _=profileModularFlow P Q hpos t x := rfl

#print axioms profileModularFlow
#print axioms profile_flow_apply
#print axioms profile_flow_on_unitary
#print axioms profile_flow_group
#print axioms profile_flow_zero
#print axioms profile_flow_fixes_vector
#print axioms profile_flow_strongly_continuous
#print axioms profileFlowConjugation
#print axioms profile_flow_conjugation_eq
#print axioms profile_flow_preserves_factor
#print axioms profile_flow_preserves_state
#print axioms profile_flow_local_conjugation
#print axioms profile_flow_local_vector
#print axioms profile_eigenvector_mem_delta
#print axioms profile_delta_eigenvector
#print axioms profile_flow_eigenvector
#print axioms profile_flow_spectral_unique
end
end ChatgptAudit.Transport027
