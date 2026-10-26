-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_055 ESPONTANEA (08/09/2026), transposta em 08/09/2026
-- Lote 055..056 (6 modulos; origem: ordem direta do operador a bancada para demonstrar no modelo completo).
--   055 — SELETOR RELATIVO NA TORRE INFINITA: com a preparacao ja existente geometricAmplitude (b_n = 2^-n/24)
--     e os pesos da torre, a leitura de verossimilhanca do cociclo SEPARA todas as configuracoes infinitas
--     quando t != 0 (contraste a(x) = log(1+3x/2) - log(1-3x) com 2a(x/2) < a(x): cada a_n domina toda a cauda;
--     codigo binario injetivo); a leitura coincide com os logaritmos dos pesos efetivos e com o gerador de
--     verossimilhanca do kernel (existing_global_generator_bound / density_normalized / cocycle_limit);
--     a densidade existente e o estado preparado. [DERIVED, analitico, NAO Lean]: A = C*(P_n), D = W*(P_n)
--     recuperados pelo cociclo; [DERIVED + KNOWN]: esperanca D no fator inteiro (Takesaki). D e comutativa,
--     M e o ambiente: W*(u) = D nao e W*(u) = M. Vale para geometricAmplitude e t != 0, nao para todo perfil.
--   056 — METRICAS DA TORRE E LIMITES DA RECONSTRUCAO: d_t(x,y) = |g_t(x) - g_t(y)| e metrica (t != 0) e a
--     escala e livre; Fisher radial F(r) = sum b_n^2/[q_n(1-q_n)] com 1/96 <= F <= 4/357 e F(0) = 1/96 (soma e
--     cotas Lean; identificacao probabilistica global analitica); entropia relativa/t^4 -> F(0)/2 = 1/192;
--     NEGATIVOS: a familia de um parametro tem Gram 2x2 de determinante ZERO (nao gera area por renomear
--     coordenadas); o gerador relativo como Dirac tem distancia de comutadores INFINITA entre configuracoes
--     distintas (comutador zero com as coordenadas); o gauge relativo exp(isP_n) preserva ambos os estados e o
--     cociclo (liberdade residual), e seu gerador NAO e central ([P_0, E_01] = E_01 != 0).
--   Estatuto: [REAL] o compilado; [DERIVED] reconstrucao da algebra diagonal, interpretacao global de Fisher,
--   4||xi_r||^2 = F(r), arcsin, distancia de Connes; [OPEN] geometria fisica 3+1, area-entropia geometrica,
--   calor fisico, acao gravitacional, Einstein-Cartan sem hipoteses. Nenhum nome ligado a H3/area/gate.
-- Auditoria da gerencia (sessao d554e796, 08/09/2026): hashes 10/10 + 13/13; 2/2 auditores da bancada exit 0;
--   sem revisao cientifica independente na bancada (declarado) — a gerencia leu os enunciados;
--   recompilacao INDEPENDENTE 6/6, axiomas no trio; guarda de colisao; fontes lidas das SUBPASTAS da entrega.
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GeometricLikelihoodSeparation
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.CocycleRealization
open Filter Topology Set TGLExt ChatgptAudit.Response028 ChatgptAudit.Cocycle030
noncomputable section

def digitTerm (a : ℕ → ℝ) (u : ℕ → Bool) (n : ℕ) : ℝ :=
  if u n then a n else 0

def binaryCode (a : ℕ → ℝ) (u : ℕ → Bool) : ℝ :=
  ∑' n, digitTerm a u n

theorem digit_term_bounds {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (u : ℕ → Bool) (n : ℕ) :
    0 ≤ digitTerm a u n ∧ digitTerm a u n ≤ a n := by
  cases h : u n <;> simp [digitTerm,h,ha n]

theorem digit_summable {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) :
    Summable (digitTerm a u) :=
  Summable.of_nonneg_of_le (fun n => (digit_term_bounds ha u n).1)
    (fun n => (digit_term_bounds ha u n).2) hs

theorem digit_tail_summable {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    Summable (fun k => digitTerm a u (n+1+k)) :=
  (digit_summable ha hs u).comp_injective (fun _ _ h => Nat.add_left_cancel h)

theorem code_prefix_tail {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    binaryCode a u = (∑ k ∈ Finset.range n, digitTerm a u k) +
      digitTerm a u n + ∑' k, digitTerm a u (n+1+k) := by
  have h := (digit_summable ha hs u).sum_add_tsum_nat_add (n+1)
  rw [Finset.sum_range_succ] at h
  simpa only [binaryCode,Nat.add_comm] using h.symm

theorem digit_tail_bounds {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (u : ℕ → Bool) (n : ℕ) :
    0 ≤ (∑' k, digitTerm a u (n+1+k)) ∧
    (∑' k, digitTerm a u (n+1+k)) ≤ ∑' k, a (n+1+k) := by
  constructor
  · exact tsum_nonneg (fun k => (digit_term_bounds ha u (n+1+k)).1)
  · exact Summable.tsum_le_tsum (fun k => (digit_term_bounds ha u (n+1+k)).2)
      (digit_tail_summable ha hs u n)
      (hs.comp_injective (fun _ _ h => Nat.add_left_cancel h))

theorem first_difference_strict {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (hd : ∀ n, (∑' k, a (n+1+k)) < a n)
    (u v : ℕ → Bool) (n : ℕ)
    (hp : ∀ k, k<n → u k=v k) (hu : u n=false) (hv : v n=true) :
    binaryCode a u < binaryCode a v := by
  have he : (∑ k ∈ Finset.range n, digitTerm a u k) =
      ∑ k ∈ Finset.range n, digitTerm a v k := by
    apply Finset.sum_congr rfl
    intro k hk
    simp only [digitTerm,hp k (Finset.mem_range.mp hk)]
  rw [code_prefix_tail ha hs u n,code_prefix_tail ha hs v n,he]
  have htu := (digit_tail_bounds ha hs u n).2
  have htv := (digit_tail_bounds ha hs v n).1
  have hdn := hd n
  have du : digitTerm a u n=0 := by simp [digitTerm,hu]
  have dv : digitTerm a v n=a n := by simp [digitTerm,hv]
  rw [du,dv,add_zero]
  linarith

theorem binary_code_injective {a : ℕ → ℝ} (ha : ∀ n, 0 ≤ a n)
    (hs : Summable a) (hd : ∀ n, (∑' k, a (n+1+k)) < a n) :
    Function.Injective (binaryCode a) := by
  intro u v huv
  by_contra hne
  have hex : ∃ n, u n≠v n := by
    by_contra hn
    apply hne
    funext n
    by_contra hnv
    exact hn ⟨n,hnv⟩
  let n := Nat.find hex
  have hn : u n≠v n := Nat.find_spec hex
  have hp : ∀ k, k<n → u k=v k := by
    intro k hk
    exact of_not_not (Nat.find_min hex hk)
  cases hu : u n <;> cases hv : v n
  · exact hn (hu.trans hv.symm)
  · exact (ne_of_lt (first_difference_strict ha hs hd u v n hp hu hv)) huv
  · exact (ne_of_lt (first_difference_strict ha hs hd v u n
      (fun k hk => (hp k hk).symm) hv hu)) huv.symm
  · exact hn (hu.trans hv.symm)

theorem geometric_code_injective {t : ℝ} (ht : t≠0) :
    Function.Injective (binaryCode (geometricContrast t)) :=
  binary_code_injective (geometric_contrast_nonnegative t)
    (geometric_contrast_summable t) (geometric_contrast_dominates_entire_tail ht)

def geometricLogReading (t : ℝ) (u : ℕ → Bool) : ℝ :=
  (∑' n, logOneRatio (geometricArgument t n)) -
    binaryCode (geometricContrast t) u

def geometricSiteReading (t : ℝ) (u : ℕ → Bool) (n : ℕ) : ℝ :=
  if u n then logZeroRatio (geometricArgument t n)
    else logOneRatio (geometricArgument t n)

theorem geometric_log_one_summable (t : ℝ) :
    Summable (fun n => logOneRatio (geometricArgument t n)) := by
  apply Summable.of_nonneg_of_le
    (fun n => (log_one_ratio_bounds _ (geometric_argument_bounds t n).1).1)
    (fun n => ?_) (geometricAmplitude.summable.mul_left (2*regularParameter t))
  have h := (log_one_ratio_bounds _ (geometric_argument_bounds t n).1).2
  simpa only [geometricArgument,mul_comm,mul_left_comm,mul_assoc] using h

theorem geometric_site_reading_eq (t : ℝ) (u : ℕ → Bool) (n : ℕ) :
    geometricSiteReading t u n =
      logOneRatio (geometricArgument t n) - digitTerm (geometricContrast t) u n := by
  cases h : u n <;> simp [geometricSiteReading,digitTerm,h,geometricContrast,logContrast]

theorem geometric_site_reading_summable (t : ℝ) (u : ℕ → Bool) :
    Summable (geometricSiteReading t u) := by
  have h := (geometric_log_one_summable t).sub
    (digit_summable (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u)
  simpa only [← geometric_site_reading_eq] using h

theorem geometric_log_reading_eq_actual_series (t : ℝ) (u : ℕ → Bool) :
    geometricLogReading t u = ∑' n, geometricSiteReading t u n := by
  rw [geometricLogReading,binaryCode,← Summable.tsum_sub
    (geometric_log_one_summable t)
    (digit_summable (geometric_contrast_nonnegative t) (geometric_contrast_summable t) u)]
  exact tsum_congr (fun n => (geometric_site_reading_eq t u n).symm)

theorem geometric_log_reading_injective {t : ℝ} (ht : t≠0) :
    Function.Injective (geometricLogReading t) := by
  intro u v h
  apply geometric_code_injective ht
  dsimp [geometricLogReading] at h
  linarith

#print axioms digitTerm
#print axioms binaryCode
#print axioms digit_term_bounds
#print axioms digit_summable
#print axioms digit_tail_summable
#print axioms code_prefix_tail
#print axioms digit_tail_bounds
#print axioms first_difference_strict
#print axioms binary_code_injective
#print axioms geometric_code_injective
#print axioms geometricLogReading
#print axioms geometricSiteReading
#print axioms geometric_log_one_summable
#print axioms geometric_site_reading_eq
#print axioms geometric_site_reading_summable
#print axioms geometric_log_reading_eq_actual_series
#print axioms geometric_log_reading_injective

end
end ChatgptAudit.CocycleRealization
