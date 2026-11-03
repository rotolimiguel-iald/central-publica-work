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
import TGLExt.ProfileTomitaTransport

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt ChatgptAudit.Profile026
noncomputable section

def profileJ (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert P ≃ₛₗᵢ[starRingEnd ℂ] TowerHilbert P :=
  (profileGNSUnitary P Q hpos).symm.trans ((towerJequiv Q).trans (profileGNSUnitary P Q hpos))

theorem profile_j_apply (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (x : TowerHilbert P) :
    profileJ P Q hpos x=profileGNSUnitary P Q hpos
      (towerJ Q ((profileGNSUnitary P Q hpos).symm x)) := rfl

theorem profile_j_involutive (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert P) : profileJ P Q hpos (profileJ P Q hpos x)=x := by
  rw [profile_j_apply,profile_j_apply,LinearIsometryEquiv.symm_apply_apply,
    towerJ_involutive,LinearIsometryEquiv.apply_symm_apply]

theorem profile_j_fixes_vector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profileJ P Q hpos (globalProfileVector P Q hpos)=globalProfileVector P Q hpos := by
  rw [profile_j_apply,←profile_gns_unitary_omega,LinearIsometryEquiv.symm_apply_apply,
    towerJ_fixes_hOmega]

def profileHalfOperator (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert P →ₗ.[ℂ] TowerHilbert P :=
  unitaryPartial (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)

def profileDeltaOperator (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert P →ₗ.[ℂ] TowerHilbert P :=
  unitaryPartial (profileGNSUnitary P Q hpos) (towerDeltaClosed Q)

theorem profile_half_domain (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    (profileHalfOperator P Q hpos).domain=profileTomitaDomain P Q hpos := rfl

theorem profile_js_equals_half (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : profileTomitaDomain P Q hpos) :
    profileJ P Q hpos (profileTomita P Q hpos x)=profileHalfOperator P Q hpos x := by
  rw [profile_j_apply,profile_tomita_apply,LinearIsometryEquiv.symm_apply_apply]
  rfl

theorem profile_tomita_polar (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : profileTomitaDomain P Q hpos) :
    profileTomita P Q hpos x=profileJ P Q hpos (profileHalfOperator P Q hpos x) := by
  rw [←profile_js_equals_half,profile_j_involutive]

theorem profile_half_selfadjoint (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    IsSelfAdjoint (profileHalfOperator P Q hpos) :=
  unitary_partial_selfadjoint _ _ (modulatorCandidate_domain_dense (P := Q))
    (modulatorCandidate_selfadjoint (P := Q))

theorem profile_half_positive (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : (profileHalfOperator P Q hpos).domain) :
    0≤(inner ℂ (x : TowerHilbert P) (profileHalfOperator P Q hpos x)).re :=
  unitary_partial_positive _ _ (modulatorCandidate_positive (P := Q)) x

theorem profile_half_closed (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    (profileHalfOperator P Q hpos).IsClosed :=
  unitary_partial_closed _ _ (modulatorCandidate_is_closed (P := Q))

theorem profile_delta_selfadjoint (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    IsSelfAdjoint (profileDeltaOperator P Q hpos) :=
  unitary_partial_selfadjoint _ _ (squareDomain_dense (P := Q)) (delta_selfadjoint (P := Q))

theorem profile_delta_positive (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : (profileDeltaOperator P Q hpos).domain) :
    0≤(inner ℂ (x : TowerHilbert P) (profileDeltaOperator P Q hpos x)).re :=
  unitary_partial_positive _ _ (delta_positive (P := Q)) x

theorem profile_delta_closed (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    (profileDeltaOperator P Q hpos).IsClosed :=
  unitary_partial_closed _ _ (delta_closed (P := Q))

theorem profile_delta_domain_dense (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Dense ((profileDeltaOperator P Q hpos).domain : Set (TowerHilbert P)) :=
  unitary_partial_domain_dense _ _ (squareDomain_dense (P := Q))

theorem profile_delta_domain_iff (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert P) :
    x∈(profileDeltaOperator P Q hpos).domain ↔
      ∃ hx : x∈(profileHalfOperator P Q hpos).domain,
        profileHalfOperator P Q hpos ⟨x,hx⟩∈(profileHalfOperator P Q hpos).domain := by
  change (profileGNSUnitary P Q hpos).symm x∈modularSquareDomain Q ↔ _
  rw [squareDomain_iff]
  constructor
  · rintro ⟨hx,hax⟩
    refine ⟨hx,?_⟩
    change (profileGNSUnitary P Q hpos).symm (profileGNSUnitary P Q hpos
      (closedModulatorCandidate Q (unitaryPartialInput (profileGNSUnitary P Q hpos)
        (closedModulatorCandidate Q) ⟨x,hx⟩)))∈(closedModulatorCandidate Q).domain
    rw [LinearIsometryEquiv.symm_apply_apply]
    exact hax
  · rintro ⟨hx,hax⟩
    refine ⟨hx,?_⟩
    change (profileGNSUnitary P Q hpos).symm (profileGNSUnitary P Q hpos
      (closedModulatorCandidate Q (unitaryPartialInput (profileGNSUnitary P Q hpos)
        (closedModulatorCandidate Q) ⟨x,hx⟩)))∈(closedModulatorCandidate Q).domain at hax
    rw [LinearIsometryEquiv.symm_apply_apply] at hax
    exact hax

def profileSquareInput (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : (profileDeltaOperator P Q hpos).domain) : (profileHalfOperator P Q hpos).domain :=
  ⟨x,((profile_delta_domain_iff P Q hpos (x : TowerHilbert P)).mp x.property).choose⟩

def profileSquareMid (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : (profileDeltaOperator P Q hpos).domain) : (profileHalfOperator P Q hpos).domain :=
  ⟨profileHalfOperator P Q hpos (profileSquareInput P Q hpos x),
    ((profile_delta_domain_iff P Q hpos (x : TowerHilbert P)).mp x.property).choose_spec⟩

theorem profile_delta_is_square (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : (profileDeltaOperator P Q hpos).domain) :
    profileDeltaOperator P Q hpos x=profileHalfOperator P Q hpos (profileSquareMid P Q hpos x) := by
  let e := profileGNSUnitary P Q hpos
  let z : modularSquareDomain Q := unitaryPartialInput e (towerDeltaClosed Q) x
  have hi : unitaryPartialInput e (closedModulatorCandidate Q) (profileSquareInput P Q hpos x)=
      squareInput Q z := Subtype.ext rfl
  have hm : unitaryPartialInput e (closedModulatorCandidate Q) (profileSquareMid P Q hpos x)=
      squareMid Q z := by
    apply Subtype.ext
    change e.symm (e (closedModulatorCandidate Q
      (unitaryPartialInput e (closedModulatorCandidate Q) (profileSquareInput P Q hpos x))))=
      closedModulatorCandidate Q (squareInput Q z)
    rw [e.symm_apply_apply,hi]
  change e (towerDeltaClosed Q z)=
    e (closedModulatorCandidate Q (unitaryPartialInput e (closedModulatorCandidate Q) (profileSquareMid P Q hpos x)))
  rw [delta_apply,hm]

theorem profile_local_mem_half (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P a (globalProfileVector P Q hpos)∈(profileHalfOperator P Q hpos).domain := by
  change (profileGNSUnitary P Q hpos).symm (towerPi P a (globalProfileVector P Q hpos))∈closedTomitaDomain Q
  rw [←profile_gns_unitary_local P Q hpos N a,LinearIsometryEquiv.symm_apply_apply]
  exact local_vector_mem_domain a

theorem profile_half_local (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileHalfOperator P Q hpos
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_half P Q hpos N a⟩=
        towerPi P (towerDeltaHalfLevel Q N a) (globalProfileVector P Q hpos) := by
  have hi : unitaryPartialInput (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_half P Q hpos N a⟩=
        (⟨((tof Q N a : TowerPre Q) : TowerHilbert Q),local_vector_mem_domain a⟩ : closedTomitaDomain Q) := by
    apply Subtype.ext
    change (profileGNSUnitary P Q hpos).symm (towerPi P a (globalProfileVector P Q hpos))=_
    rw [←profile_gns_unitary_local P Q hpos N a,LinearIsometryEquiv.symm_apply_apply]
  change profileGNSUnitary P Q hpos (closedModulatorCandidate Q
    (unitaryPartialInput (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_half P Q hpos N a⟩))=_
  rw [hi]
  exact (congrArg (profileGNSUnitary P Q hpos) (modulatorCandidate_local (P := Q) a)).trans
    (profile_gns_unitary_local P Q hpos N (towerDeltaHalfLevel Q N a))

theorem profile_local_mem_delta (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P a (globalProfileVector P Q hpos)∈(profileDeltaOperator P Q hpos).domain := by
  change (profileGNSUnitary P Q hpos).symm (towerPi P a (globalProfileVector P Q hpos))∈modularSquareDomain Q
  rw [←profile_gns_unitary_local P Q hpos N a,LinearIsometryEquiv.symm_apply_apply]
  exact levelSpace_mem_squareDomain (N := N) ⟨a,rfl⟩

theorem profile_delta_local (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileDeltaOperator P Q hpos
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_delta P Q hpos N a⟩=
        towerPi P (towerDeltaLevel Q N a) (globalProfileVector P Q hpos) := by
  have hi : unitaryPartialInput (profileGNSUnitary P Q hpos) (towerDeltaClosed Q)
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_delta P Q hpos N a⟩=
        (⟨((tof Q N a : TowerPre Q) : TowerHilbert Q),
          levelSpace_mem_squareDomain (N := N) ⟨a,rfl⟩⟩ : modularSquareDomain Q) := by
    apply Subtype.ext
    change (profileGNSUnitary P Q hpos).symm (towerPi P a (globalProfileVector P Q hpos))=_
    rw [←profile_gns_unitary_local P Q hpos N a,LinearIsometryEquiv.symm_apply_apply]
  change profileGNSUnitary P Q hpos (towerDeltaClosed Q
    (unitaryPartialInput (profileGNSUnitary P Q hpos) (towerDeltaClosed Q)
      ⟨towerPi P a (globalProfileVector P Q hpos),profile_local_mem_delta P Q hpos N a⟩))=_
  rw [hi]
  exact (congrArg (profileGNSUnitary P Q hpos) (square_local (P := Q) N a)).trans
    (profile_gns_unitary_local P Q hpos N (towerDeltaLevel Q N a))

#print axioms profileJ
#print axioms profile_j_apply
#print axioms profile_j_involutive
#print axioms profile_j_fixes_vector
#print axioms profileHalfOperator
#print axioms profileDeltaOperator
#print axioms profile_half_domain
#print axioms profile_js_equals_half
#print axioms profile_tomita_polar
#print axioms profile_half_selfadjoint
#print axioms profile_half_positive
#print axioms profile_half_closed
#print axioms profile_delta_selfadjoint
#print axioms profile_delta_positive
#print axioms profile_delta_closed
#print axioms profile_delta_domain_dense
#print axioms profile_delta_domain_iff
#print axioms profile_delta_is_square
#print axioms profile_local_mem_half
#print axioms profile_half_local
#print axioms profile_local_mem_delta
#print axioms profile_delta_local
end
end ChatgptAudit.Transport027
