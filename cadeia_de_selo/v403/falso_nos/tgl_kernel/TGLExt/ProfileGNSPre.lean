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
import TGLExt.GlobalProfileControls
import TGLExt.NoNormalTrace

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt ChatgptAudit.Profile026
noncomputable section

def profileGNSPre (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerPre Q → TowerHilbert P :=
  Quotient.lift (fun p : TowerPt => towerPi P p.2 (globalProfileVector P Q hpos)) (by
    intro x y h
    obtain ⟨K,hx,hy,he⟩ := h
    rw [←towerPi_compat hx x.2,he,towerPi_compat])

theorem profile_gns_pre_tof (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileGNSPre P Q hpos (tof Q N a)=towerPi P a (globalProfileVector P Q hpos) := rfl

theorem profile_gns_pre_add (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x y : TowerPre Q) :
    profileGNSPre P Q hpos (x+y)=profileGNSPre P Q hpos x+profileGNSPre P Q hpos y := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  obtain ⟨M,b,rfl⟩ := exists_tof y
  rw [tof_add_at (show N≤N⊔M from le_sup_left) (show M≤N⊔M from le_sup_right),
    profile_gns_pre_tof,towerPi_add,towerPi_compat,towerPi_compat,
    profile_gns_pre_tof,profile_gns_pre_tof]
  rfl

theorem profile_gns_pre_smul (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (c : ℂ) (x : TowerPre Q) :
    profileGNSPre P Q hpos (c • x)=c • profileGNSPre P Q hpos x := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  rw [tof_smul,profile_gns_pre_tof,towerPi_smul,profile_gns_pre_tof]
  rfl

theorem profile_gns_local_inner (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ (towerPi P a (globalProfileVector P Q hpos))
      (towerPi P b (globalProfileVector P Q hpos))=tInner Q N a b := by
  have hh := global_profile_state_local P Q hpos N (aᴴ*b)
  change inner ℂ (globalProfileVector P Q hpos)
    (towerPi P (aᴴ*b) (globalProfileVector P Q hpos))=tState Q N (aᴴ*b) at hh
  rw [towerPi_mul,towerPi_star,mul_apply_eq_comp,ContinuousLinearMap.adjoint_inner_right] at hh
  exact hh

theorem profile_gns_pre_inner (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x y : TowerPre Q) :
    inner ℂ (profileGNSPre P Q hpos x) (profileGNSPre P Q hpos y)=inner ℂ x y := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  obtain ⟨M,b,rfl⟩ := exists_tof y
  rw [profile_gns_pre_tof,profile_gns_pre_tof,towerPre_inner_def,
    innerPre_tof_at (show N≤N⊔M from le_sup_left) (show M≤N⊔M from le_sup_right),
    ←profile_gns_local_inner P Q hpos (N⊔M),towerPi_compat,towerPi_compat]

theorem profile_gns_pre_norm (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerPre Q) : ‖profileGNSPre P Q hpos x‖=‖x‖ := by
  have hs : ‖profileGNSPre P Q hpos x‖^2=‖x‖^2 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ),norm_sq_eq_re_inner (𝕜 := ℂ),profile_gns_pre_inner]
  nlinarith [norm_nonneg (profileGNSPre P Q hpos x),norm_nonneg x]

def profileGNSPreIsometry (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    TowerPre Q →ₗᵢ[ℂ] TowerHilbert P where
  toFun := profileGNSPre P Q hpos
  map_add' := profile_gns_pre_add P Q hpos
  map_smul' := profile_gns_pre_smul P Q hpos
  norm_map' := profile_gns_pre_norm P Q hpos

theorem profile_gns_pre_left (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (x : TowerPre Q) :
    profileGNSPre P Q hpos (lmulPre Q a x)=towerPi P a (profileGNSPre P Q hpos x) := by
  obtain ⟨M,b,rfl⟩ := exists_tof x
  rw [lmulPre_tof_at (show N≤N⊔M from le_sup_left) (show M≤N⊔M from le_sup_right),
    profile_gns_pre_tof,towerPi_mul,towerPi_compat,towerPi_compat,
    mul_apply_eq_comp,profile_gns_pre_tof]

#print axioms profileGNSPre
#print axioms profile_gns_pre_tof
#print axioms profile_gns_pre_add
#print axioms profile_gns_pre_smul
#print axioms profile_gns_local_inner
#print axioms profile_gns_pre_inner
#print axioms profile_gns_pre_norm
#print axioms profileGNSPreIsometry
#print axioms profile_gns_pre_left
end
end ChatgptAudit.Transport027
