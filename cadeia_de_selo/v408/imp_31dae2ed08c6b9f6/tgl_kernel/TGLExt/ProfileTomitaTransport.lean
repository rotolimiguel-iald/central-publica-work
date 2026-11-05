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
import TGLExt.UnitaryPartialTransport

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt ChatgptAudit.Profile026
noncomputable section

def profilePairHomeomorph (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    (TowerHilbert Q×TowerHilbert Q) ≃ₜ (TowerHilbert P×TowerHilbert P) :=
  (profileGNSUnitary P Q hpos).toHomeomorph.prodCongr (profileGNSUnitary P Q hpos).toHomeomorph

def profileTomitaGraph (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Set (TowerHilbert P×TowerHilbert P) :=
  {p | ∃ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A∈theFactorObject P ∧
      p=(A (globalProfileVector P Q hpos),(star A) (globalProfileVector P Q hpos))}

theorem profile_tomita_graph_image (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profilePairHomeomorph P Q hpos '' tomitaGraph Q=profileTomitaGraph P Q hpos := by
  ext p
  constructor
  · rintro ⟨q,⟨A,hA,rfl⟩,rfl⟩
    refine ⟨profileFactorConjugation P Q hpos A,(profile_factor_conjugation_iff P Q hpos A).mp hA,?_⟩
    change (profileGNSUnitary P Q hpos (A (hOmega Q)),
      profileGNSUnitary P Q hpos ((star A) (hOmega Q)))=_
    rw [←map_star (profileFactorConjugation P Q hpos) A]
    simp only [profile_factor_conjugation_vector]
  · rintro ⟨A,hA,rfl⟩
    refine ⟨((profileFactorConjugation P Q hpos).symm A (hOmega Q),
      (star ((profileFactorConjugation P Q hpos).symm A)) (hOmega Q)),
      ⟨(profileFactorConjugation P Q hpos).symm A,profile_factor_inverse_mem P Q hpos A hA,rfl⟩,?_⟩
    change (profileGNSUnitary P Q hpos ((profileFactorConjugation P Q hpos).symm A (hOmega Q)),
      profileGNSUnitary P Q hpos ((star ((profileFactorConjugation P Q hpos).symm A)) (hOmega Q)))=_
    rw [←profile_factor_conjugation_vector,←profile_factor_conjugation_vector]
    simp only [map_star,StarAlgEquiv.apply_symm_apply]

theorem profile_tomita_closed_graph_image (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profilePairHomeomorph P Q hpos '' closure (tomitaGraph Q)=closure (profileTomitaGraph P Q hpos) := by
  rw [(profilePairHomeomorph P Q hpos).image_closure,profile_tomita_graph_image]

theorem profile_tomita_closed_graph_iff (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x y : TowerHilbert P) :
    (x,y)∈closure (profileTomitaGraph P Q hpos) ↔
      ((profileGNSUnitary P Q hpos).symm x,(profileGNSUnitary P Q hpos).symm y)∈closure (tomitaGraph Q) := by
  rw [←profile_tomita_closed_graph_image]
  change (x,y)∈profilePairHomeomorph P Q hpos '' closure (tomitaGraph Q) ↔
    (profilePairHomeomorph P Q hpos).symm (x,y)∈closure (tomitaGraph Q)
  constructor
  · rintro ⟨p,hp,hp'⟩
    rw [←hp',(profilePairHomeomorph P Q hpos).symm_apply_apply]
    exact hp
  · intro hp
    exact ⟨(profilePairHomeomorph P Q hpos).symm (x,y),hp,
      (profilePairHomeomorph P Q hpos).apply_symm_apply (x,y)⟩

def profileTomitaDomain (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Submodule ℂ (TowerHilbert P) :=
  unitaryPartialDomain (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)

def profileTomita (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    profileTomitaDomain P Q hpos →ₛₗ[starRingEnd ℂ] TowerHilbert P :=
  (profileGNSUnitary P Q hpos).toLinearEquiv.toLinearMap.comp
    ((closedTomita Q).comp
      (unitaryPartialInput (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)))

theorem profile_tomita_apply (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : profileTomitaDomain P Q hpos) :
    profileTomita P Q hpos x=profileGNSUnitary P Q hpos
      (closedTomita Q (unitaryPartialInput (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q) x)) := rfl

theorem profile_tomita_graph (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : profileTomitaDomain P Q hpos) :
    ((x : TowerHilbert P),profileTomita P Q hpos x)∈closure (profileTomitaGraph P Q hpos) := by
  apply (profile_tomita_closed_graph_iff P Q hpos _ _).mpr
  rw [profile_tomita_apply,LinearIsometryEquiv.symm_apply_apply]
  exact closedTomita_graph (unitaryPartialInput (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q) x)

theorem profile_tomita_domain_iff (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x : TowerHilbert P) :
    x∈profileTomitaDomain P Q hpos ↔ ∃ y, (x,y)∈closure (profileTomitaGraph P Q hpos) := by
  constructor
  · intro hx
    exact ⟨profileTomita P Q hpos ⟨x,hx⟩,profile_tomita_graph P Q hpos ⟨x,hx⟩⟩
  · rintro ⟨y,hxy⟩
    exact ⟨(profileGNSUnitary P Q hpos).symm y,
      (profile_tomita_closed_graph_iff P Q hpos x y).mp hxy⟩

theorem profile_tomita_graph_single_valued (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (x y z : TowerHilbert P)
    (hy : (x,y)∈closure (profileTomitaGraph P Q hpos))
    (hz : (x,z)∈closure (profileTomitaGraph P Q hpos)) : y=z := by
  apply (profileGNSUnitary P Q hpos).symm.injective
  exact tomita_graph_closure_single_valued _ _ _
    ((profile_tomita_closed_graph_iff P Q hpos x y).mp hy)
    ((profile_tomita_closed_graph_iff P Q hpos x z).mp hz)

theorem profile_tomita_closed_graph_eq (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    range (fun x : profileTomitaDomain P Q hpos =>
      ((x : TowerHilbert P),profileTomita P Q hpos x))=closure (profileTomitaGraph P Q hpos) := by
  ext p
  constructor
  · rintro ⟨x,rfl⟩
    exact profile_tomita_graph P Q hpos x
  · intro hp
    let x : profileTomitaDomain P Q hpos :=
      ⟨p.1,(profile_tomita_domain_iff P Q hpos p.1).mpr ⟨p.2,hp⟩⟩
    refine ⟨x,Prod.ext rfl ?_⟩
    exact profile_tomita_graph_single_valued P Q hpos p.1 _ p.2
      (profile_tomita_graph P Q hpos x) hp

theorem profile_tomita_is_closed (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    IsClosed (range (fun x : profileTomitaDomain P Q hpos =>
      ((x : TowerHilbert P),profileTomita P Q hpos x))) := by
  rw [profile_tomita_closed_graph_eq]
  exact isClosed_closure

theorem profile_tomita_domain_dense (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Dense (profileTomitaDomain P Q hpos : Set (TowerHilbert P)) :=
  unitary_partial_domain_dense (profileGNSUnitary P Q hpos) (closedModulatorCandidate Q)
    (modulatorCandidate_domain_dense (P := Q))

theorem profile_factor_vector_mem_tomita (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P) :
    A (globalProfileVector P Q hpos)∈profileTomitaDomain P Q hpos := by
  rw [profile_tomita_domain_iff]
  exact ⟨(star A) (globalProfileVector P Q hpos),subset_closure ⟨A,hA,rfl⟩⟩

theorem profile_tomita_extends_star (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P) :
    profileTomita P Q hpos ⟨A (globalProfileVector P Q hpos),profile_factor_vector_mem_tomita P Q hpos A hA⟩=
      (star A) (globalProfileVector P Q hpos) :=
  profile_tomita_graph_single_valued P Q hpos _ _ _
    (profile_tomita_graph P Q hpos ⟨_,profile_factor_vector_mem_tomita P Q hpos A hA⟩)
    (subset_closure ⟨A,hA,rfl⟩)

#print axioms profile_tomita_graph_image
#print axioms profile_tomita_closed_graph_image
#print axioms profile_tomita_closed_graph_iff
#print axioms profileTomita
#print axioms profile_tomita_apply
#print axioms profile_tomita_graph
#print axioms profile_tomita_domain_iff
#print axioms profile_tomita_graph_single_valued
#print axioms profile_tomita_closed_graph_eq
#print axioms profile_tomita_is_closed
#print axioms profile_tomita_domain_dense
#print axioms profile_factor_vector_mem_tomita
#print axioms profile_tomita_extends_star
end
end ChatgptAudit.Transport027
