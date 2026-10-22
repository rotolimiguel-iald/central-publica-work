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
import TGLExt.GlobalProfileState

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal025
noncomputable section

theorem push_diagonal_exists {L N : ℕ} (hLN : L≤N) (f : chainIdx L → ℂ) :
    ∃ g : chainIdx N → ℂ, tPush hLN (Matrix.diagonal f)=Matrix.diagonal g := by
  induction N, hLN using Nat.le_induction with
  | base => exact ⟨f,tPush_self _ _⟩
  | succ N h ih =>
    obtain ⟨g,hg⟩ := ih
    refine ⟨fun x => g x.1,?_⟩
    rw [tPush_succ h (Nat.le_succ_of_le h),hg,tower_step_diagonal]

theorem pushed_relative_commute (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    tPush hLN (relativeFilter (towerW Q L) (towerW P L))*
      relativeFilter (towerW P N) (towerW Q N)=
    relativeFilter (towerW P N) (towerW Q N)*
      tPush hLN (relativeFilter (towerW Q L) (towerW P L)) := by
  obtain ⟨g,hg⟩ := push_diagonal_exists hLN (fun i => (Real.sqrt (towerW P L i/towerW Q L i):ℂ))
  change tPush hLN (Matrix.diagonal _)*Matrix.diagonal _=
    Matrix.diagonal _*tPush hLN (Matrix.diagonal _)
  rw [hg,Matrix.diagonal_mul_diagonal,Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  exact mul_comm _ _

theorem profile_relative_right_left (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    rTowerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N)=
      towerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N) := by
  have hr :
      rTowerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N)=
        towerPi P (relativeFilter (towerW P N) (towerW Q N)*
          tPush hLN (relativeFilter (towerW Q L) (towerW P L))) (hOmega P) := by
    rw [profileVector,towerPi_omega,rTowerPi_coe,rmulPre_tof_at hLN (le_refl N),tPush_self,
      towerPi_omega]
  have hl :
      towerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N)=
        towerPi P (tPush hLN (relativeFilter (towerW Q L) (towerW P L))*
          relativeFilter (towerW P N) (towerW Q N)) (hOmega P) := by
    rw [profileVector,←towerPi_compat hLN (relativeFilter (towerW Q L) (towerW P L)),
      ←mul_apply_eq_comp,←towerPi_mul]
  rw [hr,hl,pushed_relative_commute P Q hLN]

theorem global_profile_right_left (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (L : ℕ) :
    rTowerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos)=
      towerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos) := by
  have ht := global_profile_vector_tendsto P Q hpos
  have hr := (rTowerPi P (relativeFilter (towerW Q L) (towerW P L))).continuous.continuousAt.tendsto.comp ht
  have hl := (towerPi P (relativeFilter (towerW Q L) (towerW P L))).continuous.continuousAt.tendsto.comp ht
  have he :
      (fun N => rTowerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N))
        =ᶠ[atTop]
      (fun N => towerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N)) := by
    filter_upwards [eventually_ge_atTop L] with N hN
    exact profile_relative_right_left P Q hN
  exact tendsto_nhds_unique hr (hl.congr' he.symm)

theorem global_profile_inverse_overlap (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (L : ℕ) :
    inner ℂ (hOmega P)
      (towerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos))=
        ((profileAffinityLimit P Q/profileAffinity P Q L:ℝ):ℂ) := by
  have ht := global_profile_vector_tendsto P Q hpos
  have hi := (tendsto_const_nhds (x := hOmega P)).inner (𝕜 := ℂ)
    ((towerPi P (relativeFilter (towerW Q L) (towerW P L))).continuous.continuousAt.tendsto.comp ht)
  have hc : Tendsto (fun N => ((profileAffinity P Q N/profileAffinity P Q L:ℝ):ℂ))
      atTop (𝓝 ((profileAffinityLimit P Q/profileAffinity P Q L:ℝ):ℂ)) := by
    exact (Complex.continuous_ofReal.tendsto _).comp
      ((profile_affinity_tendsto P Q).div_const (profileAffinity P Q L))
  have he :
      (fun N => inner ℂ (hOmega P)
        (towerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N)))
        =ᶠ[atTop] (fun N => ((profileAffinity P Q N/profileAffinity P Q L:ℝ):ℂ)) := by
    filter_upwards [eventually_ge_atTop L] with N hN
    exact profile_inverse_overlap P Q hN
  exact tendsto_nhds_unique hi (hc.congr' he.symm)

theorem global_profile_inverse_distance (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) (L : ℕ) :
    ‖hOmega P-towerPi P (relativeFilter (towerW Q L) (towerW P L))
      (globalProfileVector P Q hpos)‖^2=2-2*(profileAffinityLimit P Q/profileAffinity P Q L) := by
  rw [norm_sub_sq (𝕜 := ℂ),hOmega_norm,global_profile_inverse_norm,global_profile_inverse_overlap]
  change (1:ℝ)^2-2*(profileAffinityLimit P Q/profileAffinity P Q L)+1^2=_
  ring

theorem global_profile_inverse_tendsto (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Tendsto (fun L => towerPi P (relativeFilter (towerW Q L) (towerW P L))
      (globalProfileVector P Q hpos)) atTop (𝓝 (hOmega P)) := by
  have ht : Tendsto (fun L => ‖hOmega P-
      towerPi P (relativeFilter (towerW Q L) (towerW P L)) (globalProfileVector P Q hpos)‖^2)
      atTop (𝓝 (0:ℝ)) := by
    simp only [global_profile_inverse_distance]
    convert (tendsto_const_nhds (x := (2:ℝ))).sub
      ((profile_affinity_ratio_tendsto P Q hpos).const_mul 2) using 1
    norm_num
  apply tendsto_iff_norm_sub_tendsto_zero.mpr
  simpa only [Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,norm_sub_rev] using ht.sqrt

theorem global_profile_vector_separating (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P)
    (hz : A (globalProfileVector P Q hpos)=0) : A=0 := by
  have he : ∀ L, A (towerPi P (relativeFilter (towerW Q L) (towerW P L))
      (globalProfileVector P Q hpos))=0 := by
    intro L
    rw [←global_profile_right_left]
    have hc := congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P =>
      T (globalProfileVector P Q hpos))
      (factor_comm_rTowerPi hA (relativeFilter (towerW Q L) (towerW P L)))
    simpa only [mul_apply_eq_comp,hz,map_zero] using hc
  have ht := A.continuous.continuousAt.tendsto.comp (global_profile_inverse_tendsto P Q hpos)
  have hzero : Tendsto (fun _L : ℕ => (0:TowerHilbert P)) atTop (𝓝 (A (hOmega P))) := by
    simpa only [Function.comp_def,he] using ht
  exact factor_omega_separating hA (tendsto_nhds_unique hzero tendsto_const_nhds)

theorem global_profile_state_faithful (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P)
    (hz : globalProfileState P Q hpos (star A*A)=0) : A=0 := by
  rw [global_profile_square_value] at hz
  exact global_profile_vector_separating P Q hpos A hA (inner_self_eq_zero.mp hz)

#print axioms push_diagonal_exists
#print axioms pushed_relative_commute
#print axioms profile_relative_right_left
#print axioms global_profile_right_left
#print axioms global_profile_inverse_overlap
#print axioms global_profile_inverse_distance
#print axioms global_profile_inverse_tendsto
#print axioms global_profile_vector_separating
#print axioms global_profile_state_faithful
end
end ChatgptAudit.Profile026
