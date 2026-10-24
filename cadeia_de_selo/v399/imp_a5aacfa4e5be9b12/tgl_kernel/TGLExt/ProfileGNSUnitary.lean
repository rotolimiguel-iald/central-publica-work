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
import TGLExt.ProfileGNSPre

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt UniformSpace ChatgptAudit.Profile026
noncomputable section

def profileGNSMap (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert Q → TowerHilbert P :=
  Completion.extension (profileGNSPre P Q hpos)

theorem profile_gns_map_coe (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerPre Q) :
    profileGNSMap P Q hpos (x : TowerHilbert Q)=profileGNSPre P Q hpos x :=
  Completion.extension_coe (profileGNSPreIsometry P Q hpos).isometry.uniformContinuous x

theorem profile_gns_map_continuous (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Continuous (profileGNSMap P Q hpos) := Completion.continuous_extension

theorem profile_gns_map_add (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x y : TowerHilbert Q) :
    profileGNSMap P Q hpos (x+y)=profileGNSMap P Q hpos x+profileGNSMap P Q hpos y := by
  refine Completion.induction_on₂ x y (isClosed_eq
    ((profile_gns_map_continuous P Q hpos).comp (continuous_fst.add continuous_snd))
    (((profile_gns_map_continuous P Q hpos).comp continuous_fst).add
      ((profile_gns_map_continuous P Q hpos).comp continuous_snd))) ?_
  intro a b
  rw [←Completion.coe_add,profile_gns_map_coe,profile_gns_pre_add,
    profile_gns_map_coe,profile_gns_map_coe]

theorem profile_gns_map_smul (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (c : ℂ) (x : TowerHilbert Q) :
    profileGNSMap P Q hpos (c • x)=c • profileGNSMap P Q hpos x := by
  refine Completion.induction_on x (isClosed_eq
    ((profile_gns_map_continuous P Q hpos).comp (continuous_const.smul continuous_id))
    (continuous_const.smul (profile_gns_map_continuous P Q hpos))) ?_
  intro a
  rw [←Completion.coe_smul,profile_gns_map_coe,profile_gns_pre_smul,profile_gns_map_coe]

theorem profile_gns_map_norm (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert Q) : ‖profileGNSMap P Q hpos x‖=‖x‖ := by
  refine Completion.induction_on x (isClosed_eq
    (continuous_norm.comp (profile_gns_map_continuous P Q hpos)) continuous_norm) ?_
  intro a
  rw [profile_gns_map_coe,profile_gns_pre_norm,Completion.norm_coe]

def profileGNSIsometry (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert Q →ₗᵢ[ℂ] TowerHilbert P where
  toFun := profileGNSMap P Q hpos
  map_add' := profile_gns_map_add P Q hpos
  map_smul' := profile_gns_map_smul P Q hpos
  norm_map' := profile_gns_map_norm P Q hpos

theorem profile_gns_map_intertwines (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (x : TowerHilbert Q) :
    profileGNSMap P Q hpos (towerPi Q a x)=towerPi P a (profileGNSMap P Q hpos x) := by
  refine Completion.induction_on x (isClosed_eq
    ((profile_gns_map_continuous P Q hpos).comp (towerPi Q a).continuous)
    ((towerPi P a).continuous.comp (profile_gns_map_continuous P Q hpos))) ?_
  intro b
  rw [towerPi_coe,profile_gns_map_coe,profile_gns_pre_left,profile_gns_map_coe]

theorem profile_gns_map_omega (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profileGNSMap P Q hpos (hOmega Q)=globalProfileVector P Q hpos := by
  change profileGNSMap P Q hpos ((tof Q 0 1 : TowerPre Q) : TowerHilbert Q)=_
  rw [profile_gns_map_coe,profile_gns_pre_tof,towerPi_one]
  rfl

theorem profile_gns_range_closed (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    IsClosed (range (profileGNSMap P Q hpos)) :=
  (profileGNSIsometry P Q hpos).isometry.isClosedEmbedding.isClosed_range

theorem profile_gns_range_local_invariant (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) {y : TowerHilbert P}
    (hy : y∈range (profileGNSMap P Q hpos)) :
    towerPi P a y∈range (profileGNSMap P Q hpos) := by
  obtain ⟨x,rfl⟩ := hy
  exact ⟨towerPi Q a x,profile_gns_map_intertwines P Q hpos N a x⟩

theorem profile_gns_range_omega (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    hOmega P∈range (profileGNSMap P Q hpos) := by
  apply (profile_gns_range_closed P Q hpos).mem_of_tendsto (global_profile_inverse_tendsto P Q hpos)
  filter_upwards [] with N
  refine ⟨((tof Q N (relativeFilter (towerW Q N) (towerW P N)) : TowerPre Q) : TowerHilbert Q),?_⟩
  rw [profile_gns_map_coe,profile_gns_pre_tof]

theorem profile_gns_surjective (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Function.Surjective (profileGNSMap P Q hpos) := by
  have hl : range (fun p : TowerPt => towerPi P p.2 (hOmega P)) ⊆ range (profileGNSMap P Q hpos) := by
    rintro _ ⟨p,rfl⟩
    exact profile_gns_range_local_invariant P Q hpos p.1 p.2 (profile_gns_range_omega P Q hpos)
  have hc := closure_minimal hl (profile_gns_range_closed P Q hpos)
  rw [(towerPi_orbit_dense (P := P)).closure_range] at hc
  intro x
  exact hc (mem_univ x)

def profileGNSUnitary (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerHilbert Q ≃ₗᵢ[ℂ] TowerHilbert P :=
  LinearIsometryEquiv.ofSurjective (profileGNSIsometry P Q hpos) (profile_gns_surjective P Q hpos)

theorem profile_gns_unitary_apply (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert Q) : profileGNSUnitary P Q hpos x=profileGNSMap P Q hpos x := rfl

theorem profile_gns_unitary_omega (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profileGNSUnitary P Q hpos (hOmega Q)=globalProfileVector P Q hpos :=
  profile_gns_map_omega P Q hpos

theorem profile_gns_unitary_local (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileGNSUnitary P Q hpos ((tof Q N a : TowerPre Q) : TowerHilbert Q)=
      towerPi P a (globalProfileVector P Q hpos) := by
  rw [profile_gns_unitary_apply,profile_gns_map_coe,profile_gns_pre_tof]

theorem profile_gns_unitary_intertwines (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (x : TowerHilbert Q) :
    profileGNSUnitary P Q hpos (towerPi Q a x)=
      towerPi P a (profileGNSUnitary P Q hpos x) :=
  profile_gns_map_intertwines P Q hpos N a x

#print axioms profile_gns_map_coe
#print axioms profile_gns_map_continuous
#print axioms profile_gns_map_add
#print axioms profile_gns_map_smul
#print axioms profile_gns_map_norm
#print axioms profileGNSIsometry
#print axioms profile_gns_map_intertwines
#print axioms profile_gns_map_omega
#print axioms profile_gns_range_closed
#print axioms profile_gns_range_local_invariant
#print axioms profile_gns_range_omega
#print axioms profile_gns_surjective
#print axioms profileGNSUnitary
#print axioms profile_gns_unitary_apply
#print axioms profile_gns_unitary_omega
#print axioms profile_gns_unitary_local
#print axioms profile_gns_unitary_intertwines
end
end ChatgptAudit.Transport027
