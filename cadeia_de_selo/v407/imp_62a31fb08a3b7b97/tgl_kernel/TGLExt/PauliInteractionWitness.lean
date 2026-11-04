-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummablePauliInteraction
import TGLExt.ChainLocality

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.InteractionWitness
open TGLExt ChatgptAudit ChatgptAudit.Observable035
  ChatgptAudit.SummableInteraction
noncomputable section

def interactionProbe (P : SiteProfile) (j : ℕ) : InteractionOperator P :=
  sitePauliY P j * sitePauliX P (j+1)

theorem interaction_probe_mem_factor (P : SiteProfile) (j : ℕ) :
    interactionProbe P j ∈ theFactorObject P :=
  mul_mem (site_pauli_y_mem_factor P j) (site_pauli_x_mem_factor P (j+1))

theorem bond_times_probe (P : SiteProfile) (j : ℕ) :
    pauliBond P j * interactionProbe P j = Complex.I • sitePauliZ P j := by
  have hc := (site_pauli_xy_commute P (Nat.ne_of_gt (Nat.lt_succ_self j))).eq
  unfold pauliBond interactionProbe
  calc
    sitePauliX P j * sitePauliX P (j+1) * (sitePauliY P j * sitePauliX P (j+1)) =
        sitePauliX P j * (sitePauliX P (j+1) * sitePauliY P j) * sitePauliX P (j+1) := by noncomm_ring
    _ = sitePauliX P j * (sitePauliY P j * sitePauliX P (j+1)) * sitePauliX P (j+1) := by rw [hc]
    _ = (sitePauliX P j * sitePauliY P j) *
        (sitePauliX P (j+1) * sitePauliX P (j+1)) := by noncomm_ring
    _ = Complex.I • sitePauliZ P j := by rw [site_pauli_xy, site_pauli_x_square, mul_one]

theorem probe_times_bond (P : SiteProfile) (j : ℕ) :
    interactionProbe P j * pauliBond P j = (-Complex.I) • sitePauliZ P j := by
  have hc := (site_pauli_xx_commute P (Nat.ne_of_gt (Nat.lt_succ_self j))).eq
  unfold pauliBond interactionProbe
  calc
    sitePauliY P j * sitePauliX P (j+1) * (sitePauliX P j * sitePauliX P (j+1)) =
        sitePauliY P j * (sitePauliX P (j+1) * sitePauliX P j) * sitePauliX P (j+1) := by noncomm_ring
    _ = sitePauliY P j * (sitePauliX P j * sitePauliX P (j+1)) * sitePauliX P (j+1) := by rw [hc]
    _ = (sitePauliY P j * sitePauliX P j) *
        (sitePauliX P (j+1) * sitePauliX P (j+1)) := by noncomm_ring
    _ = (-Complex.I) • sitePauliZ P j := by rw [site_pauli_yx, site_pauli_x_square, mul_one]

theorem bond_not_in_centralizer (P : SiteProfile) (j : ℕ) (hp : P.w j ≠ 1/2) :
    pauliBond P j ∉ omegaCentralizer P := by
  intro h
  have he := h.2 (interactionProbe P j) (interaction_probe_mem_factor P j)
  rw [bond_times_probe, probe_times_bond, ChatgptAudit.Density033.omega_state_smul,
    ChatgptAudit.Density033.omega_state_smul, site_pauli_z_state] at he
  have him := congrArg Complex.im he
  norm_num [Complex.mul_im] at him
  apply hp
  linarith

theorem first_prefix_is_one_bond (P : SiteProfile) (c : ℕ → ℝ) (hc : c 0=1) :
    interactionPrefix P c 1 = pauliBond P 0 := by
  simp [interactionPrefix, interactionTerm, hc]

theorem first_prefix_not_in_centralizer (P : SiteProfile) (c : ℕ → ℝ)
    (hc : c 0=1) (hp : P.w 0≠1/2) :
    interactionPrefix P c 1 ∉ omegaCentralizer P := by
  rw [first_prefix_is_one_bond P c hc]
  exact bond_not_in_centralizer P 0 hp

theorem interaction_pauli_xz :
    pauliXMatrix * pauliZMatrix = (-Complex.I) • pauliYMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix,pauliYMatrix,pauliZMatrix,Matrix.mul_apply,
      Fin.sum_univ_two,Matrix.smul_apply]

theorem interaction_pauli_zx :
    pauliZMatrix * pauliXMatrix = Complex.I • pauliYMatrix := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [pauliXMatrix,pauliYMatrix,pauliZMatrix,Matrix.mul_apply,
      Fin.sum_univ_two,Matrix.smul_apply]

theorem interaction_site_xz (P : SiteProfile) (j : ℕ) :
    sitePauliX P j * sitePauliZ P j = (-Complex.I) • sitePauliY P j := by
  change siteOperator P j pauliXMatrix * siteOperator P j pauliZMatrix = _
  rw [← siteOperator_mul, interaction_pauli_xz, site_operator_smul]
  rfl

theorem interaction_site_zx (P : SiteProfile) (j : ℕ) :
    sitePauliZ P j * sitePauliX P j = Complex.I • sitePauliY P j := by
  change siteOperator P j pauliZMatrix * siteOperator P j pauliXMatrix = _
  rw [← siteOperator_mul, interaction_pauli_zx, site_operator_smul]
  rfl

theorem bond_times_left_z (P : SiteProfile) (j : ℕ) :
    pauliBond P j * sitePauliZ P j = (-Complex.I) • interactionProbe P j := by
  have hc : sitePauliX P (j+1) * sitePauliZ P j =
      sitePauliZ P j * sitePauliX P (j+1) :=
    siteOperators_commute (Nat.ne_of_gt (Nat.lt_succ_self j)) _ _
  unfold pauliBond interactionProbe
  rw [mul_assoc, hc, ← mul_assoc, interaction_site_xz, smul_mul_assoc]

theorem left_z_times_bond (P : SiteProfile) (j : ℕ) :
    sitePauliZ P j * pauliBond P j = Complex.I • interactionProbe P j := by
  unfold pauliBond interactionProbe
  rw [← mul_assoc, interaction_site_zx, smul_mul_assoc]

theorem bond_left_commutator (P : SiteProfile) (j : ℕ) :
    pauliBond P j * sitePauliZ P j - sitePauliZ P j * pauliBond P j =
      (-2*Complex.I) • interactionProbe P j := by
  rw [bond_times_left_z, left_z_times_bond, ← sub_smul]
  congr 1
  ring

theorem probe_times_right_z (P : SiteProfile) (j : ℕ) :
    interactionProbe P j * sitePauliZ P (j+1) =
      (-Complex.I) • (sitePauliY P j * sitePauliY P (j+1)) := by
  unfold interactionProbe
  rw [mul_assoc, interaction_site_xz, mul_smul_comm]

theorem right_z_times_probe (P : SiteProfile) (j : ℕ) :
    sitePauliZ P (j+1) * interactionProbe P j =
      Complex.I • (sitePauliY P j * sitePauliY P (j+1)) := by
  have hc : sitePauliZ P (j+1) * sitePauliY P j =
      sitePauliY P j * sitePauliZ P (j+1) :=
    siteOperators_commute (Nat.ne_of_gt (Nat.lt_succ_self j)) _ _
  unfold interactionProbe
  rw [← mul_assoc, hc, mul_assoc, interaction_site_zx, mul_smul_comm]

theorem probe_right_commutator (P : SiteProfile) (j : ℕ) :
    interactionProbe P j * sitePauliZ P (j+1) -
      sitePauliZ P (j+1) * interactionProbe P j =
      (-2*Complex.I) • (sitePauliY P j * sitePauliY P (j+1)) := by
  rw [probe_times_right_z, right_z_times_probe, ← sub_smul]
  congr 1
  ring

theorem bond_double_commutator (P : SiteProfile) (j : ℕ) :
    (pauliBond P j * sitePauliZ P j - sitePauliZ P j * pauliBond P j) *
        sitePauliZ P (j+1) -
      sitePauliZ P (j+1) *
        (pauliBond P j * sitePauliZ P j - sitePauliZ P j * pauliBond P j) =
      (-4 : ℂ) • (sitePauliY P j * sitePauliY P (j+1)) := by
  rw [bond_left_commutator, smul_mul_assoc, mul_smul_comm,
    ← smul_sub, probe_right_commutator, smul_smul]
  congr 1
  calc
    _ = (4 : ℂ) * (Complex.I * Complex.I) := by ring
    _ = -4 := by norm_num

theorem tower_operator_one_ne_zero (P : SiteProfile) :
    (1 : InteractionOperator P)≠0 := by
  intro h
  have he := congrArg (fun A : InteractionOperator P => A (hOmega P)) h
  change hOmega P = 0 at he
  have hn := hOmega_norm (P := P)
  rw [he, norm_zero] at hn
  norm_num at hn

theorem two_site_yy_square (P : SiteProfile) (j : ℕ) :
    (sitePauliY P j * sitePauliY P (j+1)) *
      (sitePauliY P j * sitePauliY P (j+1)) = 1 := by
  have hc := (site_pauli_yy_commute P (Nat.ne_of_lt (Nat.lt_succ_self j))).eq
  calc
    (sitePauliY P j * sitePauliY P (j+1)) * (sitePauliY P j * sitePauliY P (j+1)) =
      sitePauliY P j * (sitePauliY P (j+1) * sitePauliY P j) * sitePauliY P (j+1) := by noncomm_ring
    _ = sitePauliY P j * (sitePauliY P j * sitePauliY P (j+1)) * sitePauliY P (j+1) := by rw [← hc]
    _ = (sitePauliY P j * sitePauliY P j) * (sitePauliY P (j+1) * sitePauliY P (j+1)) := by noncomm_ring
    _ = 1 := by rw [site_pauli_y_square, site_pauli_y_square, one_mul]

theorem bond_double_commutator_ne_zero (P : SiteProfile) (j : ℕ) :
    (pauliBond P j * sitePauliZ P j - sitePauliZ P j * pauliBond P j) *
        sitePauliZ P (j+1) -
      sitePauliZ P (j+1) *
        (pauliBond P j * sitePauliZ P j - sitePauliZ P j * pauliBond P j) ≠ 0 := by
  rw [bond_double_commutator]
  intro h
  have hy : sitePauliY P j * sitePauliY P (j+1)=0 :=
    (smul_eq_zero.mp h).resolve_left (by norm_num)
  have hs := two_site_yy_square P j
  rw [hy, zero_mul] at hs
  exact tower_operator_one_ne_zero P hs.symm


def singleBondCoupling (j : ℕ) : ℝ := if j=0 then 1 else 0

theorem single_bond_coupling_summable :
    Summable (fun j => |singleBondCoupling j|) := by
  have he : (fun j => |singleBondCoupling j|) =
      (fun j : ℕ => if j=0 then (1 : ℝ) else 0) := by
    funext j
    by_cases h : j=0 <;> simp [singleBondCoupling, h]
  rw [he]
  exact (hasSum_ite_eq (0 : ℕ) (1 : ℝ)).summable

theorem single_bond_limit (P : SiteProfile) :
    interactionLimit P singleBondCoupling = pauliBond P 0 := by
  have he : interactionTerm P singleBondCoupling =
      (fun j : ℕ => if j=0 then pauliBond P 0 else 0) := by
    funext j
    by_cases h : j=0
    · subst j
      simp [interactionTerm, singleBondCoupling]
    · simp [interactionTerm, singleBondCoupling, h]
  unfold interactionLimit
  rw [he]
  exact (hasSum_ite_eq (0 : ℕ) (pauliBond P 0)).tsum_eq

theorem single_bond_limit_not_in_centralizer (P : SiteProfile) (hp : P.w 0≠1/2) :
    interactionLimit P singleBondCoupling ∉ omegaCentralizer P := by
  rw [single_bond_limit]
  exact bond_not_in_centralizer P 0 hp

theorem single_bond_limit_interacts (P : SiteProfile) :
    (interactionLimit P singleBondCoupling * sitePauliZ P 0 -
        sitePauliZ P 0 * interactionLimit P singleBondCoupling) * sitePauliZ P 1 -
      sitePauliZ P 1 * (interactionLimit P singleBondCoupling * sitePauliZ P 0 -
        sitePauliZ P 0 * interactionLimit P singleBondCoupling) ≠ 0 := by
  rw [single_bond_limit]
  exact bond_double_commutator_ne_zero P 0

#print axioms interactionProbe
#print axioms interaction_probe_mem_factor
#print axioms bond_times_probe
#print axioms probe_times_bond
#print axioms bond_not_in_centralizer
#print axioms first_prefix_is_one_bond
#print axioms first_prefix_not_in_centralizer
#print axioms interaction_pauli_xz
#print axioms interaction_pauli_zx
#print axioms interaction_site_xz
#print axioms interaction_site_zx
#print axioms bond_times_left_z
#print axioms left_z_times_bond
#print axioms bond_left_commutator
#print axioms probe_times_right_z
#print axioms right_z_times_probe
#print axioms probe_right_commutator
#print axioms bond_double_commutator
#print axioms tower_operator_one_ne_zero
#print axioms two_site_yy_square
#print axioms bond_double_commutator_ne_zero
#print axioms singleBondCoupling
#print axioms single_bond_coupling_summable
#print axioms single_bond_limit
#print axioms single_bond_limit_not_in_centralizer
#print axioms single_bond_limit_interacts
end
end ChatgptAudit.InteractionWitness
