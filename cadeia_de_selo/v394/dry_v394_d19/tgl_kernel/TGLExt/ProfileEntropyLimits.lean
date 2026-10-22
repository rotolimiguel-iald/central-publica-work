-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_028 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.RelativeEntropyProductBounds

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Response028
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def siteRelativeEntropy (P Q : SiteProfile) (n : ℕ) : ℝ :=
  diagonalRelativeEntropy (siteW (Q.w n)) (siteW (P.w n))

def prefixRelativeEntropy (P Q : SiteProfile) (N : ℕ) : ℝ :=
  diagonalRelativeEntropy (towerW Q N) (towerW P N)

def prefixModularIncrement (P Q : SiteProfile) (N : ℕ) : ℝ :=
  modularIncrement (towerW P N) (towerW Q N)

def prefixEntropyIncrement (P Q : SiteProfile) (N : ℕ) : ℝ :=
  finiteEntropy (towerW Q N)-finiteEntropy (towerW P N)

def profileRelativeTotal (P Q : SiteProfile) : ℝ := ∑' n, siteRelativeEntropy P Q n

theorem site_relative_nonnegative (P Q : SiteProfile) (n : ℕ) :
    0 ≤ siteRelativeEntropy P Q n :=
  diagonal_relative_nonnegative _ _ (siteW_pos (P.pos n) (P.lt_one n))
    (siteW_pos (Q.pos n) (Q.lt_one n)) (siteW_sum _) (siteW_sum _)

theorem prefix_relative_nonnegative (P Q : SiteProfile) (N : ℕ) :
    0≤prefixRelativeEntropy P Q N :=
  diagonal_relative_nonnegative _ _ (towerW_pos P N) (towerW_pos Q N)
    (towerW_sum P N) (towerW_sum Q N)

theorem prefix_relative_succ (P Q : SiteProfile) (N : ℕ) :
    prefixRelativeEntropy P Q (N+1)=prefixRelativeEntropy P Q N+siteRelativeEntropy P Q (N+1) := by
  change diagonalRelativeEntropy
    (productWeights (towerW Q N) (siteW (Q.w (N+1))))
    (productWeights (towerW P N) (siteW (P.w (N+1))))=_
  exact relative_entropy_product _ _ _ _ (towerW_pos P N)
    (siteW_pos (P.pos _) (P.lt_one _)) (towerW_sum P N) (siteW_sum _)
    (towerW_sum Q N) (siteW_sum _)

theorem prefix_relative_sum (P Q : SiteProfile) (N : ℕ) :
    prefixRelativeEntropy P Q N=∑ n∈Finset.range (N+1), siteRelativeEntropy P Q n := by
  induction N with
  | zero => simp [prefixRelativeEntropy,siteRelativeEntropy,towerW]
  | succ N ih => rw [prefix_relative_succ,Finset.sum_range_succ,ih]

theorem prefix_modular_succ (P Q : SiteProfile) (N : ℕ) :
    prefixModularIncrement P Q (N+1)=prefixModularIncrement P Q N+
      modularIncrement (siteW (P.w (N+1))) (siteW (Q.w (N+1))) := by
  change modularIncrement
    (productWeights (towerW P N) (siteW (P.w (N+1))))
    (productWeights (towerW Q N) (siteW (Q.w (N+1))))=_
  exact modular_increment_product _ _ _ _ (towerW_pos P N)
    (siteW_pos (P.pos _) (P.lt_one _)) (towerW_sum P N) (siteW_sum _)
    (towerW_sum Q N) (siteW_sum _)

theorem prefix_modular_sum (P Q : SiteProfile) (N : ℕ) :
    prefixModularIncrement P Q N=
      ∑ n∈Finset.range (N+1), modularIncrement (siteW (P.w n)) (siteW (Q.w n)) := by
  induction N with
  | zero => simp [prefixModularIncrement,towerW]
  | succ N ih => rw [prefix_modular_succ,Finset.sum_range_succ,ih]

theorem prefix_entropy_identity (P Q : SiteProfile) (N : ℕ) :
    prefixEntropyIncrement P Q N=prefixModularIncrement P Q N-prefixRelativeEntropy P Q N := by
  unfold prefixEntropyIncrement prefixModularIncrement prefixRelativeEntropy
  rw [relative_entropy_identity]
  ring

theorem prefix_relative_tendsto (P Q : SiteProfile)
    (hs : Summable (siteRelativeEntropy P Q)) :
    Tendsto (prefixRelativeEntropy P Q) atTop (𝓝 (profileRelativeTotal P Q)) := by
  have h := hs.hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)
  change Tendsto (fun N => prefixRelativeEntropy P Q N) _ _
  simpa only [Function.comp_def,prefix_relative_sum,profileRelativeTotal] using h

theorem prefix_relative_le_total (P Q : SiteProfile)
    (hs : Summable (siteRelativeEntropy P Q)) (N : ℕ) :
    prefixRelativeEntropy P Q N≤profileRelativeTotal P Q := by
  rw [prefix_relative_sum]
  exact hs.sum_le_tsum (Finset.range (N+1)) (fun n _ => site_relative_nonnegative P Q n)

theorem profile_relative_total_nonnegative (P Q : SiteProfile) :
    0≤profileRelativeTotal P Q := tsum_nonneg (site_relative_nonnegative P Q)

theorem third_relative_sites_summable (Q : SiteProfile)
    (hs : Summable (fun n => (Q.w n-1/3)^2)) :
    Summable (siteRelativeEntropy thirdThermalReference Q) :=
  Summable.of_nonneg_of_le (site_relative_nonnegative _ _)
    (fun n => (third_binary_relative_bound (Q.w n) (Q.pos n) (Q.lt_one n)).2)
    (hs.mul_left (9/2))

theorem third_relative_total_bound (Q : SiteProfile)
    (hs : Summable (fun n => (Q.w n-1/3)^2)) :
    profileRelativeTotal thirdThermalReference Q≤(9/2)*∑' n, (Q.w n-1/3)^2 := by
  have h := (third_relative_sites_summable Q hs).tsum_le_tsum
    (fun n => (third_binary_relative_bound (Q.w n) (Q.pos n) (Q.lt_one n)).2)
    (hs.mul_left (9/2))
  simpa only [profileRelativeTotal,siteRelativeEntropy,thirdThermalReference,tsum_mul_left] using h

theorem third_prefix_modular_formula (Q : SiteProfile) (N : ℕ) :
    prefixModularIncrement thirdThermalReference Q N=
      Real.log 2*(∑ n∈Finset.range (N+1), (Q.w n-1/3)) := by
  rw [prefix_modular_sum,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro n _
  change modularIncrement (siteW (1/3)) (siteW (Q.w n))=_
  rw [third_binary_modular_increment]
  ring

theorem third_prefix_modular_tendsto (Q : SiteProfile)
    (hs : Summable (fun n => Q.w n-1/3)) :
    Tendsto (prefixModularIncrement thirdThermalReference Q) atTop
      (𝓝 (Real.log 2*∑' n, (Q.w n-1/3))) := by
  have h := (hs.hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)).const_mul (Real.log 2)
  change Tendsto (fun N => prefixModularIncrement thirdThermalReference Q N) _ _
  simpa only [Function.comp_def,third_prefix_modular_formula] using h

theorem prefix_entropy_tendsto (P Q : SiteProfile) (K : ℝ)
    (hK : Tendsto (prefixModularIncrement P Q) atTop (𝓝 K))
    (hD : Summable (siteRelativeEntropy P Q)) :
    Tendsto (prefixEntropyIncrement P Q) atTop (𝓝 (K-profileRelativeTotal P Q)) := by
  have h := hK.sub (prefix_relative_tendsto P Q hD)
  change Tendsto (fun N => prefixEntropyIncrement P Q N) _ _
  simpa only [prefix_entropy_identity] using h

#print axioms site_relative_nonnegative
#print axioms prefix_relative_nonnegative
#print axioms prefix_relative_succ
#print axioms prefix_relative_sum
#print axioms prefix_modular_succ
#print axioms prefix_modular_sum
#print axioms prefix_entropy_identity
#print axioms prefix_relative_tendsto
#print axioms prefix_relative_le_total
#print axioms profile_relative_total_nonnegative
#print axioms third_relative_sites_summable
#print axioms third_relative_total_bound
#print axioms third_prefix_modular_formula
#print axioms third_prefix_modular_tendsto
#print axioms prefix_entropy_tendsto
end
end ChatgptAudit.Response028
