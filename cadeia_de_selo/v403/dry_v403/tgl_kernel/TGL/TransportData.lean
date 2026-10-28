import Mathlib

set_option autoImplicit false

/-!
# O transporte do seletor   [KERNEL]   (v26 -- rodada 2 do especialista, auditada)

Q1 (`P_F ∈ C_W`) reformulada pelo operador: TRANSPORTE. "Q1 nao tem geometria --
e' pura resistencia que permite a geracao do contraste." Confirmado (Q1c): a
geometria fixa o core A MONTANTE; o teste de descida do seletor e' pura algebra
de inclusoes + esperancas. Por isso esta camada NAO referencia W/AQFT: e'
geometry-free por construcao.

Leitura do operador [ONTO, estatutos no um.py]: o transporte e' a CONDICAO DE
CONTORNO DO CUSTO -- em si nao ha contorno; e' o contorno que impoe a obrigacao
do custo = LEI (norma em sentido estrito): a esperanca condicional E' a regra de
causalidade coercitiva que regula o comportamento modular. `Δ > 0` = a
termodinamica como custo da existencia.

Kernel-checked aqui (correcao fiscal do especialista ENCODADA):
  - `descent_iff_defect_zero` [NEW->KERNEL]: para esperanca FIEL e `p` projecao,
    `Δ := E(p) − E(p)² = 0  ⟺  p desce (p = ι(E p))`. A resistencia e' exatamente
    a distancia operatorial entre o seletor superior e sua descida.
  - `transport_defect_of_jones` [KERNEL]: dados Markov (`E₁(e) = β·1`), o peso
    transportado e' `β` e o DEFEITO e' `β(1−β)·1` -- β e' o peso que atravessa,
    NAO o defeito (β(1−β) ≈ β so' como aproximacao, jamais identidade).
  - `jones_selector_not_descended` [KERNEL]: se `0 < β < 1`, o seletor de Jones
    NAO desce -- `selector_lives_upstairs` como TEOREMA condicional aos dados.
    O contraste nasce porque a passagem nao e' multiplicativa: a porta nao
    apenas impede -- ela mede.

Permanece [CONJ] (ledger): a identificacao do indice `[M:N] = 1/β` para a
inclusao dos Three Locks (`N_3L ⊆ C_W`); normalidade da esperanca
(nao-enunciavel sem topologia de von Neumann -- so' a FIDELIDADE, que e'
enunciavel e e' o que a descida usa, entra como equacao).
Nenhuma instancia e' construida.
-/

namespace TGL.TransportData

/-- Esperanca condicional FIEL como DADOS + equacoes (Tomiyama): inclusao
    *-algebrica injetiva, retracao linear unital, estrela-equivariante,
    bimodular sobre a imagem, e FIEL (`E(x*x)=0 ⟹ x=0`). A normalidade fica no
    ledger externo (nao-enunciavel aqui); a descida so' precisa da fidelidade. -/
structure ConditionalExpectationData (M Ext : Type)
    [Ring M] [StarRing M] [Algebra ℂ M]
    [Ring Ext] [StarRing Ext] [Algebra ℂ Ext] where
  incl : M →⋆ₐ[ℂ] Ext
  incl_injective : Function.Injective incl
  E : Ext →ₗ[ℂ] M
  E_unital : E 1 = 1
  E_star : ∀ x : Ext, E (star x) = star (E x)
  E_bimodular : ∀ (a b : M) (x : Ext), E (incl a * x * incl b) = a * E x * b
  E_faithful : ∀ x : Ext, E (star x * x) = 0 → x = 0

variable {M Ext : Type}
  [Ring M] [StarRing M] [Algebra ℂ M]
  [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]

/-- A imagem transportada do seletor: `A_F = E(p)` (o que desce ao core). -/
def transported (D : ConditionalExpectationData M Ext) (p : Ext) : M := D.E p

/-- O DEFEITO DE TRANSPORTE (a resistencia): `Δ = E(p) − E(p)²`. -/
def transportDefect (D : ConditionalExpectationData M Ext) (p : Ext) : M :=
  D.E p - D.E p * D.E p

/-- A esperanca retrai a inclusao: `E(ι a) = a` (derivada da bimodularidade). -/
theorem E_retract (D : ConditionalExpectationData M Ext) (a : M) :
    D.E (D.incl a) = a := by
  have h := D.E_bimodular a 1 1
  simpa [D.E_unital] using h

/-- [KERNEL -- teorema da descida do seletor, rodada 2 do especialista]
    Para `E` fiel e `p` projecao: `Δ = 0 ⟺ p desce` (`p = ι(E p)`).
    A resistencia e' exatamente a distancia operatorial entre o seletor
    superior e sua descida. -/
theorem descent_iff_defect_zero (D : ConditionalExpectationData M Ext)
    (p : Ext) (hp2 : p * p = p) (hps : star p = p) :
    transportDefect D p = 0 ↔ p = D.incl (D.E p) := by
  unfold transportDefect
  constructor
  · intro hDelta
    set A := D.E p with hA
    have hAstar : star A = A := by rw [hA, ← D.E_star, hps]
    have hstar_q : star (p - D.incl A) = p - D.incl A := by
      rw [star_sub, hps, ← map_star, hAstar]
    have hexp : star (p - D.incl A) * (p - D.incl A)
        = p * p - p * D.incl A - D.incl A * p + D.incl A * D.incl A := by
      rw [hstar_q]; noncomm_ring
    have hkey : D.E (star (p - D.incl A) * (p - D.incl A)) = 0 := by
      rw [hexp]
      have h1 : D.E (p * p) = A := by rw [hp2]
      have h2 : D.E (p * D.incl A) = A * A := by
        have := D.E_bimodular 1 A p
        simpa [one_mul] using this
      have h3 : D.E (D.incl A * p) = A * A := by
        have := D.E_bimodular A 1 p
        simpa [mul_one] using this
      have h4 : D.E (D.incl A * D.incl A) = A * A := by
        rw [← map_mul, E_retract]
      rw [map_add, map_sub, map_sub, h1, h2, h3, h4]
      calc A - A * A - A * A + A * A = A - A * A := by noncomm_ring
        _ = 0 := hDelta
    have hq : p - D.incl A = 0 := D.E_faithful _ hkey
    exact sub_eq_zero.mp hq
  · intro hp
    have h1 : D.incl (D.E p * D.E p) = D.incl (D.E p) := by
      rw [map_mul, ← hp, hp2, hp]
    have h2 : D.E p * D.E p = D.E p := D.incl_injective h1
    rw [h2, sub_self]

/-- Dados da torre de Jones-Markov: a esperanca inferior `E₀ : M → N`
    (implementada pela projecao de Jones `e`: `e·x·e = ι(E₀ x)·e`) e a esperanca
    DUAL `E₁ : Ext → M` que transporta o seletor de volta, com o peso de Markov
    `E₁(e) = β·1`. O peso `β` entra como VARIAVEL REAL (nunca literal; o valor
    de runtime e' do um.py), com `indice · peso = 1`. -/
structure JonesTowerData (N M Ext : Type)
    [Ring N] [StarRing N] [Algebra ℂ N]
    [Ring M] [StarRing M] [Algebra ℂ M]
    [Ring Ext] [StarRing Ext] [Algebra ℂ Ext] where
  lower : ConditionalExpectationData N M
  upper : ConditionalExpectationData M Ext
  eJones : Ext
  eJones_idem : eJones * eJones = eJones
  eJones_star : star eJones = eJones
  jones_relation : ∀ x : M,
    eJones * upper.incl x * eJones = upper.incl (lower.incl (lower.E x)) * eJones
  markovWeight : ℝ
  markovWeight_pos : 0 < markovWeight
  markovWeight_lt_one : markovWeight < 1
  dual_expectation_jones : upper.E eJones = (markovWeight : ℂ) • (1 : M)
  indexVal : ℝ
  index_eq_inverse_weight : indexVal * markovWeight = 1

variable {N : Type} [Ring N] [StarRing N] [Algebra ℂ N]

/-- [KERNEL -- a correcao fiscal do especialista, encodada] O peso transportado
    e' `β` (`E₁(e) = β·1`) e o DEFEITO de multiplicatividade e' `β(1−β)·1`:
    β NAO e' o defeito; e' o peso que atravessa. -/
theorem transport_defect_of_jones (T : JonesTowerData N M Ext) :
    transportDefect T.upper T.eJones
      = ((T.markovWeight : ℂ) * (1 - (T.markovWeight : ℂ))) • (1 : M) := by
  unfold transportDefect
  rw [T.dual_expectation_jones, smul_mul_smul_comm, one_mul, ← sub_smul]
  ring_nf

/-- [KERNEL] `selector_lives_upstairs` como TEOREMA (condicional aos dados):
    com `0 < β < 1` e `M` nao-trivial, o defeito e' NAO-nulo. -/
theorem jones_defect_ne_zero (T : JonesTowerData N M Ext) [Nontrivial M] :
    transportDefect T.upper T.eJones ≠ 0 := by
  rw [transport_defect_of_jones]
  have hb0 : (T.markovWeight : ℂ) ≠ 0 := by
    exact_mod_cast T.markovWeight_pos.ne'
  have hb1 : (1 : ℂ) - (T.markovWeight : ℂ) ≠ 0 := by
    have : (T.markovWeight : ℂ) ≠ 1 := by exact_mod_cast T.markovWeight_lt_one.ne
    exact sub_ne_zero.mpr (Ne.symm this)
  have hc : (T.markovWeight : ℂ) * (1 - (T.markovWeight : ℂ)) ≠ 0 := mul_ne_zero hb0 hb1
  rw [← Algebra.algebraMap_eq_smul_one]
  intro h
  exact hc ((algebraMap ℂ M).injective (h.trans (map_zero (algebraMap ℂ M)).symm))

/-- [KERNEL] O seletor de Jones NAO desce: `e ≠ ι(E₁ e)`. O contraste nasce
    porque a passagem nao e' multiplicativa: a porta nao apenas impede --
    ela mede. -/
theorem jones_selector_not_descended (T : JonesTowerData N M Ext) [Nontrivial M] :
    T.eJones ≠ T.upper.incl (T.upper.E T.eJones) := by
  intro h
  exact jones_defect_ne_zero T
    ((descent_iff_defect_zero T.upper T.eJones T.eJones_idem T.eJones_star).mpr h)

/-! ## O split das faces (Q3 da rodada 2, formalizado)

A hipotese concreta que substitui o rotulo abstrato "split modular": um ELEMENTO
DE TROCA `U` no canto (`U* = U`, `U·U = P`, `P·U = U·P = U`). Entao
`P_± = (P ± U)/2` sao projecoes ortogonais que somam `P` -- as duas faces.
(A troca `J P_± J = P_∓` e a igualdade de tracos permanecem nos DADOS do core,
onde `J` e o traco vivem.) -/
section FaceSplit

variable {A : Type} [Ring A] [StarRing A] [Algebra ℂ A]

/-- As duas faces do canto, geradas pelo elemento de troca. -/
noncomputable def facePlus (P U : A) : A := (2⁻¹ : ℂ) • (P + U)

noncomputable def faceMinus (P U : A) : A := (2⁻¹ : ℂ) • (P - U)

/-- [KERNEL] `P_+` e' idempotente. -/
theorem facePlus_idem (P U : A) (hP2 : P * P = P) (hU2 : U * U = P)
    (hPU : P * U = U) (hUP : U * P = U) :
    facePlus P U * facePlus P U = facePlus P U := by
  unfold facePlus
  rw [smul_mul_smul_comm, mul_add, add_mul, add_mul, hP2, hU2, hPU, hUP]
  module

/-- [KERNEL] `P_−` e' idempotente. -/
theorem faceMinus_idem (P U : A) (hP2 : P * P = P) (hU2 : U * U = P)
    (hPU : P * U = U) (hUP : U * P = U) :
    faceMinus P U * faceMinus P U = faceMinus P U := by
  unfold faceMinus
  rw [smul_mul_smul_comm, mul_sub, sub_mul, sub_mul, hP2, hU2, hPU, hUP]
  module

/-- [KERNEL] As faces sao ortogonais. -/
theorem faces_orthogonal (P U : A) (hP2 : P * P = P) (hU2 : U * U = P)
    (hPU : P * U = U) (hUP : U * P = U) :
    facePlus P U * faceMinus P U = 0 := by
  unfold facePlus faceMinus
  rw [smul_mul_smul_comm, mul_sub, add_mul, add_mul, hP2, hU2, hPU, hUP]
  module

/-- [KERNEL] As faces somam o canto: `P_+ + P_− = P`. -/
theorem faces_sum (P U : A) : facePlus P U + faceMinus P U = P := by
  unfold facePlus faceMinus
  module

/-- [KERNEL] As faces sao auto-adjuntas (dados `P* = P`, `U* = U`). -/
theorem faces_selfAdjoint [StarModule ℂ A] (P U : A) (hPs : star P = P) (hUs : star U = U) :
    star (facePlus P U) = facePlus P U ∧ star (faceMinus P U) = faceMinus P U := by
  constructor
  · simp [facePlus, star_smul, star_add, hPs, hUs, star_inv₀]
  · simp [faceMinus, star_smul, star_sub, hPs, hUs, star_inv₀]

end FaceSplit

end TGL.TransportData
