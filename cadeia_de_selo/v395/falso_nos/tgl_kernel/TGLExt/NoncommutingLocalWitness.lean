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
import TGLExt.LocalInteractionData
import TGLExt.LocalInteractionGenerator

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace ChatgptAudit.NoncommutingLocal
open TGLExt Matrix Filter Topology Set ChatgptAudit
  ChatgptAudit.LocalInteraction ChatgptAudit.LocalGenerator ChatgptAudit.LocalCocycle
  ChatgptAudit.Observable035 ChatgptAudit.SummableInteraction ChatgptAudit.InteractionWitness
noncomputable section

def firstBond (P : SiteProfile) : InteractionOperator P := sitePauliX P 0 * sitePauliX P 1

def secondBond (P : SiteProfile) : InteractionOperator P := sitePauliZ P 1 * sitePauliZ P 2

def threeSiteWitness (P : SiteProfile) : InteractionOperator P :=
  sitePauliX P 0 * sitePauliY P 1 * sitePauliZ P 2

theorem operator_site_mem_level (P : SiteProfile) {j N : ℕ} (h : j ≤ N)
    (a : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P j a ∈ levelOperatorAlgebra P N := by
  refine ⟨tPush h (lastSiteMatrix j a), ?_⟩
  exact towerPi_compat h (lastSiteMatrix j a)

theorem first_bond_support (P : SiteProfile) :
    firstBond P ∈ levelOperatorAlgebra P 1 :=
  (levelOperatorAlgebra P 1).mul_mem
    (operator_site_mem_level P (by omega : 0 ≤ 1) _)
    (operator_site_mem_level P (by omega : 1 ≤ 1) _)

theorem second_bond_support (P : SiteProfile) :
    secondBond P ∈ levelOperatorAlgebra P 2 :=
  (levelOperatorAlgebra P 2).mul_mem
    (operator_site_mem_level P (by omega : 1 ≤ 2) _)
    (operator_site_mem_level P (by omega : 2 ≤ 2) _)

theorem first_bond_selfadjoint (P : SiteProfile) : IsSelfAdjoint (firstBond P) :=
  pauli_bond_selfadjoint P 0

theorem second_bond_selfadjoint (P : SiteProfile) : IsSelfAdjoint (secondBond P) := by
  change star (sitePauliZ P 1 * sitePauliZ P 2) = _
  rw [star_mul,(site_pauli_z_selfadjoint P 1).star_eq,(site_pauli_z_selfadjoint P 2).star_eq]
  exact siteOperators_commute (by omega : (2 : ℕ) ≠ 1) _ _

theorem first_times_second (P : SiteProfile) :
    firstBond P * secondBond P = (-Complex.I) • threeSiteWitness P := by
  unfold firstBond secondBond threeSiteWitness
  calc
    _ = sitePauliX P 0 * (sitePauliX P 1 * sitePauliZ P 1) * sitePauliZ P 2 := by noncomm_ring
    _ = _ := by rw [interaction_site_xz,mul_smul_comm,smul_mul_assoc]

theorem second_times_first (P : SiteProfile) :
    secondBond P * firstBond P = Complex.I • threeSiteWitness P := by
  have h20 : sitePauliZ P 2 * sitePauliX P 0 = sitePauliX P 0 * sitePauliZ P 2 :=
    siteOperators_commute (by omega : (2 : ℕ) ≠ 0) _ _
  have h10 : sitePauliZ P 1 * sitePauliX P 0 = sitePauliX P 0 * sitePauliZ P 1 :=
    siteOperators_commute (by omega : (1 : ℕ) ≠ 0) _ _
  have h21 : sitePauliZ P 2 * sitePauliX P 1 = sitePauliX P 1 * sitePauliZ P 2 :=
    siteOperators_commute (by omega : (2 : ℕ) ≠ 1) _ _
  unfold firstBond secondBond threeSiteWitness
  calc
    _ = sitePauliZ P 1 * (sitePauliZ P 2 * sitePauliX P 0) * sitePauliX P 1 := by noncomm_ring
    _ = sitePauliZ P 1 * (sitePauliX P 0 * sitePauliZ P 2) * sitePauliX P 1 := by rw [h20]
    _ = (sitePauliZ P 1 * sitePauliX P 0) * (sitePauliZ P 2 * sitePauliX P 1) := by noncomm_ring
    _ = (sitePauliX P 0 * sitePauliZ P 1) * (sitePauliX P 1 * sitePauliZ P 2) := by rw [h10,h21]
    _ = sitePauliX P 0 * (sitePauliZ P 1 * sitePauliX P 1) * sitePauliZ P 2 := by noncomm_ring
    _ = _ := by rw [interaction_site_zx,mul_smul_comm,smul_mul_assoc]

theorem three_site_witness_ne_zero (P : SiteProfile) : threeSiteWitness P ≠ 0 := by
  intro h
  have hi : (sitePauliZ P 2 * sitePauliY P 1 * sitePauliX P 0) * threeSiteWitness P = 1 := by
    unfold threeSiteWitness
    calc
      _ = sitePauliZ P 2 * (sitePauliY P 1 * (sitePauliX P 0 * sitePauliX P 0) *
          sitePauliY P 1) * sitePauliZ P 2 := by noncomm_ring
      _ = 1 := by rw [site_pauli_x_square,mul_one,site_pauli_y_square,mul_one,site_pauli_z_square]
  rw [h,mul_zero] at hi
  exact tower_operator_one_ne_zero P hi.symm

theorem two_bonds_commutator (P : SiteProfile) :
    firstBond P * secondBond P - secondBond P * firstBond P =
      (-2 * Complex.I) • threeSiteWitness P := by
  rw [first_times_second,second_times_first,←sub_smul]
  congr 1
  ring

theorem two_bonds_do_not_commute (P : SiteProfile) :
    ¬ Commute (firstBond P) (secondBond P) := by
  intro h
  have hz : firstBond P * secondBond P - secondBond P * firstBond P = 0 :=
    sub_eq_zero.mpr h.eq
  rw [two_bonds_commutator] at hz
  exact three_site_witness_ne_zero P ((smul_eq_zero.mp hz).resolve_left (by norm_num))

def twoBondTerm (P : SiteProfile) (j : ℕ) : InteractionOperator P :=
  if j=0 then firstBond P else if j=1 then secondBond P else 0

theorem two_bond_term_selfadjoint (P : SiteProfile) (j : ℕ) :
    IsSelfAdjoint (twoBondTerm P j) := by
  by_cases h0 : j=0
  · subst j
    simpa [twoBondTerm] using first_bond_selfadjoint P
  · by_cases h1 : j=1
    · subst j
      simpa [twoBondTerm] using second_bond_selfadjoint P
    · simp only [twoBondTerm,h0,h1,ite_false]
      change star (0 : InteractionOperator P) = 0
      exact star_zero _

theorem two_bond_term_support (P : SiteProfile) (j : ℕ) :
    twoBondTerm P j ∈ levelOperatorAlgebra P (j+1) := by
  by_cases h0 : j=0
  · subst j
    simpa only [twoBondTerm,ite_true,Nat.zero_add] using first_bond_support P
  · by_cases h1 : j=1
    · subst j
      simpa [twoBondTerm] using second_bond_support P
    · simp only [twoBondTerm,h0,h1,ite_false]
      exact ⟨0,(towerPiLinear P (j+1)).map_zero⟩

theorem two_bond_norm_summable (P : SiteProfile) :
    Summable (fun j => ‖twoBondTerm P j‖) := by
  have he : (fun j => ‖twoBondTerm P j‖) =
      (fun j => (if j=0 then ‖firstBond P‖ else 0) + (if j=1 then ‖secondBond P‖ else 0)) := by
    funext j
    by_cases h0 : j=0
    · subst j
      simp [twoBondTerm]
    · by_cases h1 : j=1
      · subst j
        simp [twoBondTerm]
      · simp [twoBondTerm,h0,h1]
  rw [he]
  exact (hasSum_ite_eq (0 : ℕ) ‖firstBond P‖).summable.add
    (hasSum_ite_eq (1 : ℕ) ‖secondBond P‖).summable

def noncommutingLocalData (P : SiteProfile) : LocalInteractionData P where
  term := twoBondTerm P
  selfadjoint := two_bond_term_selfadjoint P
  support := two_bond_term_support P
  norm_summable := two_bond_norm_summable P

theorem certified_terms_do_not_commute (P : SiteProfile) :
    ¬ Commute ((noncommutingLocalData P).term 0) ((noncommutingLocalData P).term 1) := by
  simpa [noncommutingLocalData,twoBondTerm] using two_bonds_do_not_commute P

theorem noncommuting_data_potential (P : SiteProfile) :
    localPotential P (noncommutingLocalData P) = firstBond P + secondBond P := by
  have he : twoBondTerm P =
      (fun j => (if j=0 then firstBond P else 0) + (if j=1 then secondBond P else 0)) := by
    funext j
    by_cases h0 : j=0
    · subst j
      simp [twoBondTerm]
    · by_cases h1 : j=1
      · subst j
        simp [twoBondTerm]
      · simp [twoBondTerm,h0,h1]
  change (∑' j, twoBondTerm P j) = _
  rw [he]
  exact ((hasSum_ite_eq (0 : ℕ) (firstBond P)).add
    (hasSum_ite_eq (1 : ℕ) (secondBond P))).tsum_eq

theorem noncommuting_data_has_actual_cocycle (P : SiteProfile) (s t : ℝ) :
    localCocycle P (noncommutingLocalData P) (s+t) =
      localCocycle P (noncommutingLocalData P) s *
        modularConjugation P s (localCocycle P (noncommutingLocalData P) t) :=
  local_cocycle_twisted P (noncommutingLocalData P) s t

theorem noncommuting_potential_ne_zero (P : SiteProfile) :
    localPotential P (noncommutingLocalData P) ≠ 0 := by
  rw [noncommuting_data_potential]
  intro h
  apply two_bonds_do_not_commute P
  change firstBond P * secondBond P = secondBond P * firstBond P
  have hb : secondBond P = -firstBond P := by
    calc
      _ = (firstBond P + secondBond P) - firstBond P := by abel
      _ = -firstBond P := by rw [h,zero_sub]
  rw [hb]
  noncomm_ring

theorem noncommuting_cocycle_nontrivial (P : SiteProfile) :
    ¬ ∀ t : ℝ, localCocycle P (noncommutingLocalData P) t = 1 :=
  nonzero_local_potential_has_nontrivial_cocycle P _ (noncommuting_potential_ne_zero P)


#print axioms firstBond
#print axioms secondBond
#print axioms threeSiteWitness
#print axioms operator_site_mem_level
#print axioms first_bond_support
#print axioms second_bond_support
#print axioms first_bond_selfadjoint
#print axioms second_bond_selfadjoint
#print axioms first_times_second
#print axioms second_times_first
#print axioms three_site_witness_ne_zero
#print axioms two_bonds_commutator
#print axioms two_bonds_do_not_commute
#print axioms twoBondTerm
#print axioms two_bond_term_selfadjoint
#print axioms two_bond_term_support
#print axioms two_bond_norm_summable
#print axioms noncommutingLocalData
#print axioms certified_terms_do_not_commute
#print axioms noncommuting_data_potential
#print axioms noncommuting_data_has_actual_cocycle
#print axioms noncommuting_potential_ne_zero
#print axioms noncommuting_cocycle_nontrivial
end
end ChatgptAudit.NoncommutingLocal
