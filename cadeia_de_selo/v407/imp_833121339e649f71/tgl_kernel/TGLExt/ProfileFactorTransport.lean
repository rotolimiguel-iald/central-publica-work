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
import TGLExt.ProfileGNSUnitary

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Transport027
open Matrix Filter Topology Set TGLExt ChatgptAudit.Profile026
noncomputable section

theorem star_equiv_centralizer_transport
    {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
    (e : (E →L[ℂ] E) ≃⋆ₐ[ℂ] (F →L[ℂ] F))
    (s : Set (E →L[ℂ] E)) (t : Set (F →L[ℂ] F))
    (hst : ∀ a, a∈s ↔ e a∈t) (a : E →L[ℂ] E) :
    a∈StarSubalgebra.centralizer ℂ s ↔ e a∈StarSubalgebra.centralizer ℂ t := by
  simp only [StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro ha b hb
    have hpre : e.symm b∈s := (hst _).mpr (by simpa only [StarAlgEquiv.apply_symm_apply] using hb)
    obtain ⟨h1,h2⟩ := ha (e.symm b) hpre
    exact ⟨by simpa only [map_mul,StarAlgEquiv.apply_symm_apply] using congrArg e h1,
      by simpa only [map_mul,map_star,StarAlgEquiv.apply_symm_apply] using congrArg e h2⟩
  · intro ha b hb
    obtain ⟨h1,h2⟩ := ha (e b) ((hst b).mp hb)
    constructor
    · apply e.injective
      change e (b*a)=e (a*b)
      simpa only [map_mul] using h1
    · apply e.injective
      change e (star b*a)=e (a*star b)
      simpa only [map_mul,map_star] using h2

def profileFactorConjugation (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    (TowerHilbert Q →L[ℂ] TowerHilbert Q) ≃⋆ₐ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  (profileGNSUnitary P Q hpos).conjStarAlgEquiv

theorem profile_factor_conjugation_apply (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert Q →L[ℂ] TowerHilbert Q) (x : TowerHilbert P) :
    profileFactorConjugation P Q hpos A x=
      profileGNSUnitary P Q hpos (A ((profileGNSUnitary P Q hpos).symm x)) := rfl

theorem profile_factor_conjugation_local (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileFactorConjugation P Q hpos (towerPi Q a)=towerPi P a := by
  ext x
  rw [profile_factor_conjugation_apply,profile_gns_unitary_intertwines,
    LinearIsometryEquiv.apply_symm_apply]

theorem profile_factor_conjugation_tower (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert Q →L[ℂ] TowerHilbert Q) :
    A∈towerImage Q ↔ profileFactorConjugation P Q hpos A∈towerImage P := by
  constructor
  · rintro ⟨N,a,rfl⟩
    rw [profile_factor_conjugation_local]
    exact towerPi_mem_towerImage _
  · rintro ⟨N,a,ha⟩
    refine ⟨N,a,?_⟩
    apply (profileFactorConjugation P Q hpos).injective
    change profileFactorConjugation P Q hpos A=profileFactorConjugation P Q hpos (towerPi Q a)
    rw [ha,profile_factor_conjugation_local]

theorem profile_factor_conjugation_iff (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert Q →L[ℂ] TowerHilbert Q) :
    A∈theFactorObject Q ↔ profileFactorConjugation P Q hpos A∈theFactorObject P :=
  star_equiv_centralizer_transport (profileFactorConjugation P Q hpos) _ _
    (star_equiv_centralizer_transport (profileFactorConjugation P Q hpos) _ _
      (profile_factor_conjugation_tower P Q hpos)) A

theorem profile_factor_inverse_mem (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P) :
    (profileFactorConjugation P Q hpos).symm A∈theFactorObject Q := by
  apply (profile_factor_conjugation_iff P Q hpos _).mpr
  simpa only [StarAlgEquiv.apply_symm_apply] using hA

theorem profile_factor_conjugation_vector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert Q →L[ℂ] TowerHilbert Q) :
    profileFactorConjugation P Q hpos A (globalProfileVector P Q hpos)=
      profileGNSUnitary P Q hpos (A (hOmega Q)) := by
  rw [profile_factor_conjugation_apply,←profile_gns_unitary_omega,
    LinearIsometryEquiv.symm_apply_apply]

theorem profile_factor_state_transport (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert Q →L[ℂ] TowerHilbert Q) :
    globalProfileState P Q hpos (profileFactorConjugation P Q hpos A)=omegaState Q A := by
  change inner ℂ (globalProfileVector P Q hpos)
    (profileFactorConjugation P Q hpos A (globalProfileVector P Q hpos))=_
  rw [profile_factor_conjugation_vector,←profile_gns_unitary_omega,
    LinearIsometryEquiv.inner_map_map]
  rfl

#print axioms star_equiv_centralizer_transport
#print axioms profileFactorConjugation
#print axioms profile_factor_conjugation_apply
#print axioms profile_factor_conjugation_local
#print axioms profile_factor_conjugation_tower
#print axioms profile_factor_conjugation_iff
#print axioms profile_factor_inverse_mem
#print axioms profile_factor_conjugation_vector
#print axioms profile_factor_state_transport
end
end ChatgptAudit.Transport027
