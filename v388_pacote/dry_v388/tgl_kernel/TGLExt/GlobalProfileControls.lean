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
import TGLExt.ProfileAffinityBound

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024 ChatgptAudit.Thermal025
noncomputable section

theorem global_profile_vector_cyclic (P Q : SiteProfile) (hpos : 0<profileAffinityLimit P Q) :
    Dense ((fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A (globalProfileVector P Q hpos)) ''
      (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) := by
  let S := (fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A (globalProfileVector P Q hpos)) ''
    (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))
  have hl : range (fun p : TowerPt => towerPi P p.2 (hOmega P)) ⊆ closure S := by
    rintro _ ⟨p,rfl⟩
    have ht := (towerPi P p.2).continuous.continuousAt.tendsto.comp
      (global_profile_inverse_tendsto P Q hpos)
    apply isClosed_closure.mem_of_tendsto ht
    filter_upwards [] with N
    apply subset_closure
    refine ⟨towerPi P p.2*towerPi P (relativeFilter (towerW Q N) (towerW P N)),
      (theFactorObject P).mul_mem (towerPi_mem_factor _) (towerPi_mem_factor _),?_⟩
    rfl
  have hi := closure_minimal hl isClosed_closure
  rw [(towerPi_orbit_dense (P := P)).closure_range] at hi
  intro x
  exact hi (mem_univ x)

def gradualProfile : SiteProfile where
  w n := 1/3+1/(12*((n:ℝ)+1))
  pos n := by positivity
  lt_one n := by
    have hn : (1:ℝ)≤(n:ℝ)+1 := le_add_of_nonneg_left (Nat.cast_nonneg n)
    have hd : (0:ℝ)<12*((n:ℝ)+1) := by positivity
    have hb : 1/(12*((n:ℝ)+1))≤(1/12:ℝ) := by
      apply (div_le_iff₀ hd).mpr
      nlinarith
    linarith

theorem gradual_profile_diff (n : ℕ) :
    gradualProfile.w n-thirdThermalReference.w n=1/(12*((n:ℝ)+1)) := by
  simp only [gradualProfile,thirdThermalReference]
  ring

theorem gradual_profile_changes_every_site (n : ℕ) :
    gradualProfile.w n≠thirdThermalReference.w n := by
  have hp : 0<gradualProfile.w n-thirdThermalReference.w n := by
    rw [gradual_profile_diff]; positivity
  exact ne_of_gt (sub_pos.mp hp)

theorem gradual_profile_square_summable :
    Summable (fun n => (thirdThermalReference.w n-gradualProfile.w n)^2) := by
  have hs : Summable (fun n : ℕ => 1/(n:ℝ)^2) :=
    Real.summable_one_div_nat_pow.mpr (by decide)
  have ht : Summable (fun n : ℕ => 1/((n:ℝ)+1)^2) := by
    simpa only [Nat.cast_add,Nat.cast_one] using (summable_nat_add_iff 1).mpr hs
  apply (ht.mul_left (1/144:ℝ)).congr
  intro n
  dsimp [gradualProfile,thirdThermalReference]
  field_simp
  ring

theorem gradual_profile_diff_not_summable :
    ¬Summable (fun n => gradualProfile.w n-thirdThermalReference.w n) := by
  intro hs
  have ht : Summable (fun n : ℕ => 1/((n:ℝ)+1)) := by
    apply (hs.mul_left 12).congr
    intro n
    rw [gradual_profile_diff]
    field_simp
  have hn : Summable (fun n : ℕ => 1/(n:ℝ)) :=
    (summable_nat_add_iff 1).mp (by simpa only [Nat.cast_add,Nat.cast_one] using ht)
  exact Real.not_summable_one_div_natCast hn

theorem gradual_profile_affinity_positive :
    0<profileAffinityLimit thirdThermalReference gradualProfile := by
  apply profile_square_summable_positive _ _ (9/4)
  · intro n
    exact binary_third_affinity_bound (gradualProfile.w n) (gradualProfile.pos n) (gradualProfile.lt_one n)
  · exact gradual_profile_square_summable

def gradualState : (TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) → ℂ :=
  globalProfileState thirdThermalReference gradualProfile gradual_profile_affinity_positive

theorem gradual_state_local (L : ℕ) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    gradualState (towerPi thirdThermalReference a)=tState gradualProfile L a :=
  global_profile_state_local _ _ _ L a

theorem gradual_state_faithful
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) (hz : gradualState (star A*A)=0) : A=0 :=
  global_profile_state_faithful _ _ _ A hA hz

theorem gradual_state_not_reference : gradualState≠omegaState thirdThermalReference := by
  intro he
  have hh := congrFun he (towerPi thirdThermalReference (N := 0) (Matrix.single 0 0 (1:ℂ)))
  rw [gradual_state_local,omegaState_pi,tState_single_diag,tState_single_diag] at hh
  norm_num [gradualProfile,thirdThermalReference,towerW,siteW] at hh

theorem profile_thermal_preparation (P : SiteProfile) (s : ℝ) (N : ℕ) :
    profileVector P (thermalProfile P s) N=towerGibbsVector P N s := by
  rw [profileVector,thermal_profile_tower_weights]
  rfl

theorem thermal_preparation_limit_iff (P : SiteProfile) (s : ℝ) :
    (∃ v : TowerHilbert P, Tendsto (fun N => towerGibbsVector P N s) atTop (𝓝 v)) ↔
      0<profileAffinityLimit P (thermalProfile P s) := by
  have he : profileVector P (thermalProfile P s)=(fun N => towerGibbsVector P N s) :=
    funext (profile_thermal_preparation P s)
  rw [←he]
  exact profile_vectors_limit_iff P (thermalProfile P s)

theorem profile_affinity_self (P : SiteProfile) (N : ℕ) : profileAffinity P P N=1 :=
  diagonal_affinity_self _ (fun i => (towerW_pos P N i).le) (towerW_sum P N)

theorem profile_affinity_limit_self (P : SiteProfile) : profileAffinityLimit P P=1 := by
  have ht := profile_affinity_tendsto P P
  change Tendsto (fun N => profileAffinity P P N) atTop (𝓝 (profileAffinityLimit P P)) at ht
  simp only [profile_affinity_self] at ht
  exact tendsto_nhds_unique ht tendsto_const_nhds

theorem profile_affinity_stationary (P Q : SiteProfile) (p q : ℝ)
    (hP : ∀ n, P.w n=p) (hQ : ∀ n, Q.w n=q) (N : ℕ) :
    profileAffinity P Q N=(diagonalAffinity (siteW p) (siteW q))^(N+1) := by
  induction N with
  | zero => simp [profileAffinity,towerW,hP,hQ]
  | succ N ih =>
    rw [profile_affinity_succ,ih]
    change _*diagonalAffinity (siteW (P.w (N+1))) (siteW (Q.w (N+1)))=_
    rw [hP,hQ]
    exact (pow_succ _ (N+1)).symm

theorem third_half_site_affinity_lt_one :
    diagonalAffinity (siteW (1/3)) (siteW (1/2))<1 := by
  apply lt_of_le_of_ne
  · exact diagonal_affinity_le_one _ _
      (fun i => (siteW_pos (by norm_num : (0:ℝ)<1/3) (by norm_num) i).le)
      (fun i => (siteW_pos (by norm_num : (0:ℝ)<1/2) (by norm_num) i).le)
      (siteW_sum _) (siteW_sum _)
  · intro he
    have hf := (diagonal_affinity_eq_one_iff _ _
      (fun i => (siteW_pos (by norm_num : (0:ℝ)<1/3) (by norm_num) i).le)
      (fun i => (siteW_pos (by norm_num : (0:ℝ)<1/2) (by norm_num) i).le)
      (siteW_sum _) (siteW_sum _)).mp he
    have hh := congrFun hf 0
    norm_num [siteW] at hh

theorem stationary_changed_affinity_zero :
    profileAffinityLimit thirdThermalReference halfThermalReference=0 := by
  have hp : 0<diagonalAffinity (siteW (1/3)) (siteW (1/2)) :=
    diagonal_affinity_positive _ _ (siteW_pos (by norm_num) (by norm_num))
      (siteW_pos (by norm_num) (by norm_num))
  have ht := (tendsto_pow_atTop_nhds_zero_of_lt_one hp.le third_half_site_affinity_lt_one).comp
    (tendsto_add_atTop_nat 1)
  have hc : Tendsto (profileAffinity thirdThermalReference halfThermalReference) atTop (𝓝 0) := by
    change Tendsto (fun N => profileAffinity thirdThermalReference halfThermalReference N) atTop (𝓝 0)
    simpa only [Function.comp_def,profile_affinity_stationary thirdThermalReference halfThermalReference
      (1/3) (1/2) (fun _ => rfl) (fun _ => rfl)] using ht
  exact tendsto_nhds_unique (profile_affinity_tendsto _ _) hc

theorem stationary_changed_no_preparation_limit (v : TowerHilbert thirdThermalReference) :
    ¬Tendsto (profileVector thirdThermalReference halfThermalReference) atTop (𝓝 v) :=
  profile_zero_affinity_no_limit _ _ stationary_changed_affinity_zero v

#print axioms global_profile_vector_cyclic
#print axioms gradualProfile
#print axioms gradual_profile_diff
#print axioms gradual_profile_changes_every_site
#print axioms gradual_profile_square_summable
#print axioms gradual_profile_diff_not_summable
#print axioms gradual_profile_affinity_positive
#print axioms gradual_state_local
#print axioms gradual_state_faithful
#print axioms gradual_state_not_reference
#print axioms profile_thermal_preparation
#print axioms thermal_preparation_limit_iff
#print axioms profile_affinity_self
#print axioms profile_affinity_limit_self
#print axioms profile_affinity_stationary
#print axioms third_half_site_affinity_lt_one
#print axioms stationary_changed_affinity_zero
#print axioms stationary_changed_no_preparation_limit
end
end ChatgptAudit.Profile026
