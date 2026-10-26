import TGLExt.TracialDissipativeTorsion

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false

/-!
# O FORNECEDOR DE CARTAN: A = ½ d ln F ALIMENTA A CONTORÇÃO TRACIAL
  [TGLExt — o ramo condicional Cartan F(ψ)R da bancada (17/09/2026), a parte algébrica;
   pedra da gerência, v370 (ramo condicional Cartan F(ψ)R; recompilada; 15 teoremas), 23/09/2026;
   docstrings corrigidas após o cético (D1: hipóteses nomeadas hdF/htan; D2: o FLRW prova só o SE)]

A bancada (CARTAN_F_PSI_E_FONTE.md, sha16 cd2ba33320d7ec0a; revisão condicional Hooke) resolveu a
equação da conexão de ∫√|g| F R(Γ) em formulação de Cartan — 4D, F > 0 independente da conexão,
coframe invertível, sem fonte de spin — e achou Dω(F eᵃ∧eᵇ) = 0 ⟹ Tᵃ = ½ eᵃ ∧ d ln F, isto é, a
torção TRACIAL com o vetor v = A = ½ d ln F. Esta pedra prova, ponto a ponto (F e dF avaliados no
ponto; F : ℝ, dF : ι → ℝ), o que é álgebra:

* `contortion` (TracialDissipativeTorsion.lean:96) com A = ½ dF/F tem a forma da bancada
  K_{abc} = (g_{ab} ∂_cF − g_{bc} ∂_aF)/(2F); a torção mista é Tᵃ_{bc} = (δᵃ_b ∂_cF − δᵃ_c ∂_bF)/(2F);
* o resíduo de Cartan (dF − 2F·A) é nulo componente a componente, e SÓ para este A (o sinal errado
  −½ deixa 2·dF — o controle negativo dos 18 recusados pela bancada);
* A PAREDE: F constante (dF = 0) ⟹ A = 0 ⟹ contorção e torção NULAS; e a instância σ, sob DUAS
  hipóteses NOMEADAS — hdF (∂_cF = 2ξ ψ·∂_cψ, a regra da cadeia de F = F₀ + ξ|ψ|²) e htan
  (ψ·∂_cψ = 0, a tangência de |ψ|² ≡ 1) — dF = 0 ⟹ torção nula. O kernel NÃO vê |ψ|² = 1 nem
  F = F₀ + ξ|ψ|²: a passagem de |ψ|² = 1 a htan e de F = F₀ + ξ|ψ|² a hdF fica [DERIVED, elementar]
  FORA do kernel (IDENTIFICACAO_PSI_SIGMA_E_TORSAO.md) — o fundo Einstein–σ continua curvo, só a
  torção morre;
* A é gradiente ⟹ a parte antissimétrica G_[bd] de `einstein_antisymmetric_part` (l.457) é ZERO;
* em n = 4 o escalar de `scalar_closed_form` (l.407) lê R(Γ) = R(g) − 6∇·A − 6A², e os termos
  induzidos valem F·(−6∇·A − 6A²) = (3/(2F))(∂F)² − 3□F (a regra da cadeia dos 9 controles);
* o habitante FLRW, SÓ o SE: F(t) = F₀·exp(2at) tem A_t = a (na convenção v364 A = α n com n_t = −1,
  a = −α). O SÓ SE — A = a n_t com A espacial nula ⟹ F = F₀·exp(2at) — pede a unicidade da EDO
  F'/F = 2a e fica [DERIVED] fora do kernel.

O que esta pedra NÃO faz: não prova a unicidade da solução de Cartan (que usa o coframe reescalado
ẽ = √F e, fora do kernel), não prova o cancelamento conforme (pede um lema de Ricci conforme que o
kernel não tem), não deriva hdF/htan de |ψ|² = 1, não prova o SÓ SE do habitante FLRW, não escolhe
Cartan contra métrica, não tipa Ψ (escalar ou forma) e não identifica ψ — isso é do operador [INPUT].
O ½ daqui NÃO é a Meia-Nat. Nada move gate ou bandeira.
-/

namespace TGLExt.CartanTracialSupplier

open TGLExt.TracialTorsion Finset

variable {ι : Type} [Fintype ι] [DecidableEq ι]

/-! ## 1. O fornecedor e a forma da bancada -/

/-- [DEF] o fornecedor de Cartan, ponto a ponto: A_c = ½ ∂_c ln F = ∂_c F / (2F) -/
noncomputable def cartanA (F : ℝ) (dF : ι → ℝ) (c : ι) : ℝ := dF c / (2 * F)

/-- [KERNEL] ★ a contorção da pedra v364 (l.96) com A = ½ d ln F tem a forma da bancada -/
theorem contortion_cartan (g : ι → ι → ℝ) (F : ℝ) (dF : ι → ℝ) (a b c : ι) :
    contortion g (cartanA F dF) a b c = (g a b * dF c - g b c * dF a) / (2 * F) := by
  unfold contortion cartanA; ring

/-- [KERNEL] a torção mista: Tᵃ_{bc} = (δᵃ_b ∂_cF − δᵃ_c ∂_bF)/(2F) — é Tᵃ = ½ eᵃ ∧ d ln F em componentes -/
theorem torsion_cartan (F : ℝ) (dF : ι → ℝ) (a b c : ι) :
    torsion (cartanA F dF) a b c = (kd a b * dF c - kd a c * dF b) / (2 * F) := by
  unfold torsion cartanA; ring

/-- [KERNEL] o traço da torção de Cartan é V = (n−1)·½ d ln F (a bancada: V = (3/2) d ln F em n = 4) -/
theorem torsion_trace_cartan (F : ℝ) (dF : ι → ℝ) (c : ι) :
    ∑ a, torsion (cartanA F dF) a a c = ((Fintype.card ι : ℝ) - 1) * (dF c / (2 * F)) :=
  torsion_trace (cartanA F dF) c

/-! ## 2. O resíduo de Cartan e o controle negativo -/

/-- [KERNEL] ★ o resíduo de Cartan Dω(F e∧e) = (dF − 2F·A)∧e∧e é nulo componente a componente -/
theorem cartan_residual_zero (F : ℝ) (hF : F ≠ 0) (dF : ι → ℝ) (c : ι) :
    dF c - 2 * F * cartanA F dF c = 0 := by
  unfold cartanA
  field_simp
  ring

/-- [KERNEL] o resíduo nulo FORÇA o fornecedor (unicidade do vetor; não da solução de Cartan inteira) -/
theorem residual_zero_forces_cartanA (F : ℝ) (hF : F ≠ 0) (dF A : ι → ℝ)
    (h : ∀ c, dF c - 2 * F * A c = 0) : A = cartanA F dF := by
  funext c
  unfold cartanA
  have hc := h c
  field_simp
  linarith

/-- [CONTROLE NEGATIVO] o sinal errado (−½ d ln F) deixa resíduo 2·∂_cF — os 18 recusados da bancada -/
theorem wrong_sign_residual (F : ℝ) (hF : F ≠ 0) (dF : ι → ℝ) (c : ι) :
    dF c - 2 * F * (- cartanA F dF c) = 2 * dF c := by
  unfold cartanA
  field_simp
  ring

/-! ## 3. A PAREDE: F constante ⟹ torção nula; a instância σ sob hdF e htan -/

/-- [KERNEL] ★ F constante no ponto (dF = 0) ⟹ o fornecedor é zero -/
theorem const_F_supplier_zero (F : ℝ) (dF : ι → ℝ) (h0 : ∀ c, dF c = 0) :
    cartanA F dF = fun _ => 0 := by
  funext c; unfold cartanA; rw [h0 c]; simp

/-- [KERNEL] ★ F constante ⟹ contorção NULA -/
theorem const_F_contortion_zero (g : ι → ι → ℝ) (F : ℝ) (dF : ι → ℝ) (h0 : ∀ c, dF c = 0) (a b c : ι) :
    contortion g (cartanA F dF) a b c = 0 := by
  rw [const_F_supplier_zero F dF h0]; unfold contortion; ring

/-- [KERNEL] ★ F constante ⟹ torção NULA -/
theorem const_F_torsion_zero (F : ℝ) (dF : ι → ℝ) (h0 : ∀ c, dF c = 0) (a b c : ι) :
    torsion (cartanA F dF) a b c = 0 := by
  rw [const_F_supplier_zero F dF h0]; unfold torsion; ring

/-- [KERNEL sob DUAS hipóteses NOMEADAS] ★★ A PAREDE σ, a parte algébrica: dadas hdF (∂_cF = 2ξ ψ·∂_cψ —
    a regra da cadeia de F = F₀ + ξ|ψ|², NÃO derivada aqui) e htan (ψ·∂_cψ = 0 — a tangência de
    |ψ|² ≡ 1, NÃO derivada aqui), dF = 0 em todo ponto. O kernel não vê |ψ|² = 1 nem F = F₀ + ξ|ψ|²;
    a passagem a hdF/htan é [DERIVED, elementar] fora do kernel (IDENTIFICACAO_PSI_SIGMA_E_TORSAO.md) -/
theorem sigma_norm_one_dF_zero {κ : Type} [Fintype κ] (ξ : ℝ) (ψ : κ → ℝ) (dψ : ι → κ → ℝ)
    (dF : ι → ℝ) (hdF : ∀ c, dF c = 2 * ξ * ∑ i, ψ i * dψ c i)
    (htan : ∀ c, ∑ i, ψ i * dψ c i = 0) (c : ι) : dF c = 0 := by
  rw [hdF c, htan c]; ring

/-- [KERNEL sob hdF e htan] ★★ com as duas hipóteses nomeadas da parede σ (a leitura: ψ = φ de norma 1)
    a torção de Cartan é NULA (em toda a família, não só em primeira ordem); o fundo Einstein–σ segue
    curvo — só a torção morre -/
theorem sigma_norm_one_torsion_zero {κ : Type} [Fintype κ] (F ξ : ℝ) (ψ : κ → ℝ) (dψ : ι → κ → ℝ)
    (dF : ι → ℝ) (hdF : ∀ c, dF c = 2 * ξ * ∑ i, ψ i * dψ c i)
    (htan : ∀ c, ∑ i, ψ i * dψ c i = 0) (a b c : ι) :
    torsion (cartanA F dF) a b c = 0 :=
  const_F_torsion_zero F dF (sigma_norm_one_dF_zero ξ ψ dψ dF hdF htan) a b c

/-! ## 4. O consumidor na pedra v364: gradiente ⟹ G_[bd] = 0; o escalar em n = 4 -/

/-- [KERNEL] ★ se A é gradiente (∂_cA_b simétrico: Schwarz para ½ ln F) e Γ̊ é simétrica, a parte
    antissimétrica de Einstein de `einstein_antisymmetric_part` é ZERO: o setor antissimétrico da
    equação de campo some sem hipótese sobre o fluxo -/
theorem gradient_supplier_antisymmetric_part_zero (g gi : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i)
    (G0 : ι → ι → ι → ℝ) (hsym : ∀ e x y, G0 e x y = G0 e y x)
    (A : ι → ℝ) (dA : ι → ι → ℝ) (hgrad : ∀ c b, dA c b = dA b c)
    (Ric Ric0 : ι → ι → ℝ) (hRic0 : ∀ b d, Ric0 b d = Ric0 d b)
    (hRic : ∀ b d, Ric b d = Ric0 b d
        - ((Fintype.card ι : ℝ) - 2) * (dA d b - ∑ e, G0 e d b * A e)
        - g d b * divA gi (fun x y => dA x y - ∑ e, G0 e x y * A e)
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A)) (b d : ι) :
    (einsteinOf g gi Ric b d - einsteinOf g gi Ric d b) / 2 = 0 := by
  have h := einstein_antisymmetric_part g gi hg Ric Ric0 A
    (fun x y => dA x y - ∑ e, G0 e x y * A e) hRic0 hRic b d
  have hs : ∑ e, G0 e d b * A e = ∑ e, G0 e b d * A e :=
    Finset.sum_congr rfl (fun e _ => by rw [hsym e d b])
  rw [h]
  rw [hgrad d b, hs]
  ring

/-- [KERNEL] ★ em n = 4 o escalar de Cartan: R(Γ) = R(g) − 6∇̊·A − 6A² (a bancada: −6∇v − 6v²) -/
theorem scalar_cartan_four (g gi : ι → ι → ℝ) (hg : ∀ i j, g i j = g j i)
    (hinv : ∀ i j, ∑ k, g i k * gi k j = kd i j) (hgi : ∀ i j, gi i j = gi j i)
    (Ric Ric0 : ι → ι → ℝ) (A : ι → ℝ) (DA : ι → ι → ℝ)
    (hRic : ∀ b d, Ric b d = Ric0 b d - ((Fintype.card ι : ℝ) - 2) * DA d b - g d b * divA gi DA
        + ((Fintype.card ι : ℝ) - 2) * (A b * A d - g d b * normSq gi A))
    (h4 : Fintype.card ι = 4) :
    scalarOf gi Ric = scalarOf gi Ric0 - 6 * divA gi DA - 6 * normSq gi A := by
  have h := scalar_closed_form g gi hg hinv hgi Ric Ric0 A DA hRic
  rw [h, h4]; push_cast; ring

/-- [KERNEL] a regra da cadeia dos 9 controles: com ∇·A = □F/(2F) − (∂F)²/(2F²) e A² = (∂F)²/(4F²),
    F·(−6∇·A − 6A²) = (3/(2F))(∂F)² − 3□F — os termos induzidos de F R(Γ) = F R(g) + (3/(2F))(∂F)² − 3□F
    (identidade de ESCALARES; a de densidades pede √|g|, errata da bancada) -/
theorem induced_scalar_terms (F boxF gradsq : ℝ) (hF : F ≠ 0) :
    F * (-6 * (boxF / (2 * F) - gradsq / (2 * F ^ 2)) - 6 * (gradsq / (4 * F ^ 2)))
      = 3 / (2 * F) * gradsq - 3 * boxF := by
  field_simp
  ring

/-! ## 5. O habitante FLRW (SÓ o SE) -/

/-- [KERNEL — SÓ o SE] F(t) = F₀·exp(2at) é um F cujo fornecedor temporal é A_t = a: a derivada existe e
    vale F₀·exp(2at)·2a, e ½·F'/F = a. Na convenção v364 (A = α n, n_t = −1) isto é a = −α, F = F₀e^{−2αt}.
    O SÓ SE (todo F = F(t) com ½F'/F = a é deste tipo) pede a unicidade da EDO F'/F = 2a e NÃO está
    nesta pedra: fica [DERIVED] fora do kernel -/
theorem flrw_habitant (F0 a t : ℝ) (hF0 : F0 ≠ 0) :
    HasDerivAt (fun s : ℝ => F0 * Real.exp (2 * a * s)) (F0 * (Real.exp (2 * a * t) * (2 * a))) t ∧
    F0 * (Real.exp (2 * a * t) * (2 * a)) / (2 * (F0 * Real.exp (2 * a * t))) = a := by
  constructor
  · have h1 : HasDerivAt (fun s : ℝ => 2 * a * s) (2 * a) t := by
      simpa using (hasDerivAt_id t).const_mul (2 * a)
    exact h1.exp.const_mul F0
  · have he : Real.exp (2 * a * t) ≠ 0 := (Real.exp_pos _).ne'
    field_simp

end TGLExt.CartanTracialSupplier

#print axioms TGLExt.CartanTracialSupplier.contortion_cartan
#print axioms TGLExt.CartanTracialSupplier.torsion_cartan
#print axioms TGLExt.CartanTracialSupplier.torsion_trace_cartan
#print axioms TGLExt.CartanTracialSupplier.const_F_supplier_zero
#print axioms TGLExt.CartanTracialSupplier.sigma_norm_one_dF_zero
#print axioms TGLExt.CartanTracialSupplier.cartan_residual_zero
#print axioms TGLExt.CartanTracialSupplier.residual_zero_forces_cartanA
#print axioms TGLExt.CartanTracialSupplier.wrong_sign_residual
#print axioms TGLExt.CartanTracialSupplier.const_F_contortion_zero
#print axioms TGLExt.CartanTracialSupplier.const_F_torsion_zero
#print axioms TGLExt.CartanTracialSupplier.sigma_norm_one_torsion_zero
#print axioms TGLExt.CartanTracialSupplier.gradient_supplier_antisymmetric_part_zero
#print axioms TGLExt.CartanTracialSupplier.scalar_cartan_four
#print axioms TGLExt.CartanTracialSupplier.induced_scalar_terms
#print axioms TGLExt.CartanTracialSupplier.flrw_habitant
