-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_026 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.AffinityVectorCriterion

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt
open scoped ComplexOrder
noncomputable section

def globalProfileVector (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) : TowerHilbert P :=
  Classical.choose ((profile_vectors_limit_iff P Q).mpr hpos)

def globalProfileState (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) : ℂ :=
  inner ℂ (globalProfileVector P Q hpos) (A (globalProfileVector P Q hpos))

theorem global_profile_vector_tendsto (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Tendsto (profileVector P Q) atTop (𝓝 (globalProfileVector P Q hpos)) :=
  Classical.choose_spec ((profile_vectors_limit_iff P Q).mpr hpos)

theorem global_profile_vector_norm (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    ‖globalProfileVector P Q hpos‖=1 := by
  have ht : Tendsto (fun _N : ℕ => (1:ℝ)) atTop (𝓝 ‖globalProfileVector P Q hpos‖) := by
    simpa only [profile_vector_norm] using (global_profile_vector_tendsto P Q hpos).norm
  exact tendsto_nhds_unique ht tendsto_const_nhds

theorem global_profile_state_limit (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    Tendsto (fun N => profileState P Q N A) atTop (𝓝 (globalProfileState P Q hpos A)) := by
  have ht := global_profile_vector_tendsto P Q hpos
  exact ht.inner (𝕜 := ℂ) (A.continuous.continuousAt.tendsto.comp ht)

theorem global_profile_state_local (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (L : ℕ) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    globalProfileState P Q hpos (towerPi P a)=tState Q L a := by
  have he : (fun N => profileState P Q N (towerPi P a)) =ᶠ[atTop] fun _ => tState Q L a := by
    filter_upwards [eventually_ge_atTop L] with N hN
    exact profile_state_marginal P Q hN a
  exact tendsto_nhds_unique (global_profile_state_limit P Q hpos (towerPi P a))
    (tendsto_const_nhds.congr' he.symm)

theorem global_profile_state_one (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    globalProfileState P Q hpos 1=1 := by
  rw [←towerPi_one (P := P) 0,global_profile_state_local,tState_one]

theorem global_profile_state_add (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    globalProfileState P Q hpos (A+B)=
      globalProfileState P Q hpos A+globalProfileState P Q hpos B := by
  simp [globalProfileState,inner_add_right]

theorem global_profile_state_smul (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (c : ℂ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    globalProfileState P Q hpos (c • A)=c*globalProfileState P Q hpos A := by
  simp [globalProfileState,inner_smul_right]

theorem global_profile_square_value (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    globalProfileState P Q hpos (star A*A)=
      inner ℂ (A (globalProfileVector P Q hpos)) (A (globalProfileVector P Q hpos)) := by
  change inner ℂ (globalProfileVector P Q hpos)
    (ContinuousLinearMap.adjoint A (A (globalProfileVector P Q hpos)))=_
  rw [ContinuousLinearMap.adjoint_inner_right]

theorem global_profile_state_positive (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    0≤globalProfileState P Q hpos (star A*A) := by
  rw [global_profile_square_value,inner_self_eq_norm_sq_to_K]
  positivity

theorem global_profile_state_seqWOT (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    SeqWOTContinuous (theFactorObject P) (globalProfileState P Q hpos) := by
  intro T Tinf C _ _ _ hWOT
  exact hWOT (globalProfileVector P Q hpos) (globalProfileVector P Q hpos)

theorem global_profile_inverse_norm (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (L : ℕ) :
    ‖towerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos)‖=1 := by
  have hh := global_profile_square_value P Q hpos
    (towerPi P (relativeFilter (towerW Q L) (towerW P L)))
  have hv : globalProfileState P Q hpos
      (star (towerPi P (relativeFilter (towerW Q L) (towerW P L)))*
        towerPi P (relativeFilter (towerW Q L) (towerW P L)))=1 := by
    change globalProfileState P Q hpos
      (ContinuousLinearMap.adjoint (towerPi P _)*towerPi P _)=1
    rw [←towerPi_star,relative_filter_self_adjoint,←towerPi_mul,global_profile_state_local,
      profile_filter_square_state]
  have hn : ‖towerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos)‖^2=1 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ),←hh,hv]; rfl
  nlinarith [norm_nonneg (towerPi P (relativeFilter (towerW Q L) (towerW P L))
    (globalProfileVector P Q hpos))]

#print axioms globalProfileVector
#print axioms global_profile_vector_tendsto
#print axioms global_profile_vector_norm
#print axioms global_profile_state_limit
#print axioms global_profile_state_local
#print axioms global_profile_state_one
#print axioms global_profile_state_add
#print axioms global_profile_state_smul
#print axioms global_profile_square_value
#print axioms global_profile_state_positive
#print axioms global_profile_state_seqWOT
#print axioms global_profile_inverse_norm
end
end ChatgptAudit.Profile026
