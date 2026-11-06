-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_025 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.GibbsProductVariance

set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024
noncomputable section

def thermalProfile (P : SiteProfile) (s : ℝ) : SiteProfile where
  w n := gibbsWeights (siteW (P.w n)) s 0
  pos n := gibbs_weights_positive _ (siteW_pos (P.pos n) (P.lt_one n)) s 0
  lt_one n := by
    have hs := gibbs_weights_normalized (siteW (P.w n)) (siteW_pos (P.pos n) (P.lt_one n)) s
    rw [Fin.sum_univ_two] at hs
    have h1 := gibbs_weights_positive _ (siteW_pos (P.pos n) (P.lt_one n)) s 1
    linarith

theorem thermal_profile_site (P : SiteProfile) (s : ℝ) (n : ℕ) :
    siteW ((thermalProfile P s).w n)=gibbsWeights (siteW (P.w n)) s := by
  have hs := gibbs_weights_normalized (siteW (P.w n)) (siteW_pos (P.pos n) (P.lt_one n)) s
  rw [Fin.sum_univ_two] at hs
  funext i
  fin_cases i
  · rfl
  · change 1-gibbsWeights (siteW (P.w n)) s 0=gibbsWeights (siteW (P.w n)) s 1
    linarith

theorem thermal_profile_zero (P : SiteProfile) (n : ℕ) :
    (thermalProfile P 0).w n=P.w n := by
  change gibbsWeights (siteW (P.w n)) 0 0=P.w n
  rw [gibbs_weights_zero _ (siteW_sum _)]
  rfl

theorem thermal_profile_tower_weights (P : SiteProfile) (s : ℝ) (N : ℕ) :
    towerW (thermalProfile P s) N=gibbsWeights (towerW P N) s := by
  induction N with
  | zero => exact thermal_profile_site P s 0
  | succ N ih =>
    change productWeights (towerW (thermalProfile P s) N) (siteW ((thermalProfile P s).w (N+1)))=
      gibbsWeights (productWeights (towerW P N) (siteW (P.w (N+1)))) s
    rw [ih,thermal_profile_site,gibbs_weights_product _ _ (towerW_pos P N)
      (siteW_pos (P.pos _) (P.lt_one _))]

theorem thermal_global_local_state (P : SiteProfile) (s : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    omegaState (thermalProfile P s) (towerPi (thermalProfile P s) a)=
      towerGibbsState P N s (towerPi P a) := by
  rw [omegaState_pi,tower_gibbs_local_state]
  unfold tState
  rw [thermal_profile_tower_weights]

theorem thermal_tower_marginal (P : SiteProfile) (s : ℝ) {L N : ℕ} (hLN : L≤N)
    (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    towerGibbsState P N s (towerPi P a)=towerGibbsState P L s (towerPi P a) := by
  calc
    towerGibbsState P N s (towerPi P a)=
        towerGibbsState P N s (towerPi P (tPush hLN a)) := by rw [towerPi_compat]
    _=omegaState (thermalProfile P s) (towerPi (thermalProfile P s) (tPush hLN a)) :=
      (thermal_global_local_state P s N _).symm
    _=omegaState (thermalProfile P s) (towerPi (thermalProfile P s) a) := by rw [towerPi_compat]
    _=towerGibbsState P L s (towerPi P a) := thermal_global_local_state P s L a

theorem thermal_tower_marginal_weights (P : SiteProfile) (s : ℝ) {L N : ℕ} (hLN : L≤N)
    (i : chainIdx L) :
    towerGibbsState P N s (towerPi P (Matrix.diagonal (Pi.single i (1:ℂ))))=
      (gibbsWeights (towerW P L) s i:ℂ) := by
  rw [thermal_tower_marginal P s hLN,tower_gibbs_local_projection]

theorem thermal_global_state_faithful (P : SiteProfile) (s : ℝ)
    (A : TowerHilbert (thermalProfile P s) →L[ℂ] TowerHilbert (thermalProfile P s))
    (hA : A∈theFactorObject (thermalProfile P s))
    (hz : omegaState (thermalProfile P s) (star A*A)=0) : A=0 :=
  omega_definite hA hz

theorem thermal_profile_uniform (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (s : ℝ) (n : ℕ) :
    (thermalProfile P s).w n=gibbsWeights (siteW q) s 0 := by
  simp only [thermalProfile,hP]

theorem thermal_tower_entropy_uniform (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (s : ℝ) (N : ℕ) :
    finiteEntropy (gibbsWeights (towerW P N) s)=
      ((N:ℝ)+1)*finiteEntropy (gibbsWeights (siteW q) s) := by
  have hsite : gibbsWeights (siteW q) s=siteW (gibbsWeights (siteW q) s 0) := by
    have hh := thermal_profile_site P s 0
    simpa only [hP,thermalProfile] using hh.symm
  rw [←thermal_profile_tower_weights]
  change towerEntropy (thermalProfile P s) N=_
  rw [tower_entropy_uniform (thermalProfile P s) (gibbsWeights (siteW q) s 0)
    (thermal_profile_uniform P q hP s),hsite,site_entropy_binary]
  rfl

#print axioms thermalProfile
#print axioms thermal_profile_site
#print axioms thermal_profile_zero
#print axioms thermal_profile_tower_weights
#print axioms thermal_global_local_state
#print axioms thermal_tower_marginal
#print axioms thermal_tower_marginal_weights
#print axioms thermal_global_state_faithful
#print axioms thermal_profile_uniform
#print axioms thermal_tower_entropy_uniform
end
end ChatgptAudit.Thermal025
