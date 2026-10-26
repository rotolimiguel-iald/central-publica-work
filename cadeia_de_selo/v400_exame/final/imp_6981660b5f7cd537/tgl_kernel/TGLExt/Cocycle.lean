import TGLExt.ModularFlow
import TGLExt.SMatrix

set_option autoImplicit false

/-!
# O cociclo de Connes na sombra finita   [TGLExt — a face finita do Lema 3]

O cociclo de Connes `[Dφ : Dψ]_t := φ^{it}·ψ^{-it}` entre dois estados de
`Mₙ(ℂ)`, montado sobre o fluxo modular de `ModularFlow.lean`. Provamos
[KERNEL], com φ/ψ/χ GENÉRICOS:

* (C0) trivialidades: `[Dφ:Dφ]_t = 1` e `[Dφ:Dψ]_0 = 1`;
* (E1) COLAGEM MULTIPLICATIVA (chain rule de Connes):
  `[Dφ:Dψ]_t · [Dψ:Dχ]_t = [Dφ:Dχ]_t`;
* (E4) holonomia do triângulo: `[Dφ:Dψ]_t · [Dψ:Dχ]_t · [Dχ:Dφ]_t = 1`;
* (E2) IDENTIDADE TEMPORAL σ-TORCIDA — a lei estrutural do cociclo:
  `u_{s+t} = u_s · σ^ψ_s(u_t)`;
* (U) unitariedade: `(u_t)ᴴ = [Dψ:Dφ]_t` e `u_t ∈ unitary`;
* (E3c) gerador no caso comutante: `u_t = exp(it·(log φ − log ψ))`;
* (E6) COVARIÂNCIA UNITÁRIA: `[D(VφVᴴ) : D(VψVᴴ)]_t = V·[Dφ:Dψ]_t·Vᴴ` —
  conjugar os ESTADOS é conjugar o COCICLO (rota: `logRho_conj` pelo
  cálculo funcional contínuo, `StarAlgHomClass.map_cfc` + automorfismo
  interno `Unitary.conjStarAlgAut`; depois `Matrix.exp_conj`).

**HONESTIDADE.** Isto é a SOMBRA FINITA das leis do cociclo de Connes: o
v16 da casa as verificou numericamente (~1e-15) e aqui elas viram KERNEL.
O levantamento GLOBAL — III₁ genuína sem projeções minimais, hipóteses
U/T1/T3, covariância do cociclo ⟹ `G_μν + Λg_μν = 8πG·𝒫_μν[K_∂]` — SEGUE
sendo O TEOREMA ABERTO do programa: este arquivo NÃO o fecha; fecha o
esqueleto algébrico da sua face finita. PosDef entra só onde o cálculo
funcional exige (E6); β JAMAIS entra. Sem sorry, sem axiom. Negativo
honesto é resultado.
-/

namespace TGLExt

open Matrix NormedSpace
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n] (phi psi chi : Matrix n n ℂ)

/-- O COCICLO DE CONNES na sombra finita: `[Dφ : Dψ]_t = φ^{it}·ψ^{-it}` —
    a derivada de Radon–Nikodym não-comutativa entre os estados φ e ψ,
    escrita com os unitários modulares `modPow` de `ModularFlow.lean`. -/
def cocycle (t : ℝ) : Matrix n n ℂ := modPow phi t * modPow psi (-t)

/-! ## C0 — trivialidades -/

/-- [KERNEL] `[Dφ:Dφ]_t = 1`: o cociclo de um estado consigo mesmo é trivial. -/
theorem cocycle_self (t : ℝ) : cocycle phi phi t = 1 :=
  modPow_mul_neg phi t

/-- [KERNEL] `[Dφ:Dψ]_0 = 1`: em `t = 0` nada foi transportado. -/
theorem cocycle_zero : cocycle phi psi 0 = 1 := by
  simp only [cocycle, neg_zero, modPow_zero, mul_one]

/-! ## E1 — colagem multiplicativa (chain rule de Connes) -/

/-- [KERNEL] CHAIN RULE DE CONNES: `[Dφ:Dψ]_t · [Dψ:Dχ]_t = [Dφ:Dχ]_t` —
    as derivadas de Radon–Nikodym modulares COLAM multiplicativamente
    através do estado intermediário. -/
theorem cocycle_chain (t : ℝ) :
    cocycle phi psi t * cocycle psi chi t = cocycle phi chi t := by
  simp only [cocycle]
  calc modPow phi t * modPow psi (-t) * (modPow psi t * modPow chi (-t))
      = modPow phi t * ((modPow psi (-t) * modPow psi t) * modPow chi (-t)) := by
        simp only [mul_assoc]
    _ = modPow phi t * modPow chi (-t) := by
        rw [modPow_neg_mul, one_mul]

/-! ## E4 — holonomia do triângulo -/

/-- [KERNEL] HOLONOMIA TRIVIAL DO TRIÂNGULO:
    `[Dφ:Dψ]_t · [Dψ:Dχ]_t · [Dχ:Dφ]_t = 1` — o transporte modular ao
    longo de um circuito fechado de estados retorna à identidade. -/
theorem cocycle_triangle (t : ℝ) :
    cocycle phi psi t * cocycle psi chi t * cocycle chi phi t = 1 := by
  rw [cocycle_chain, cocycle_chain, cocycle_self]

/-! ## E2 — identidade temporal σ-torcida (a lei estrutural) -/

/-- [KERNEL] IDENTIDADE DE COCICLO: `u_{s+t} = u_s · σ^ψ_s(u_t)` — a
    composição temporal é TORCIDA pelo fluxo modular do estado de
    referência: é isto que faz de `u_t` um cociclo (e não um mero grupo
    a um parâmetro). Verificação:
    `u_s·σ^ψ_s(u_t) = φ^{is}ψ^{-is}·ψ^{is}φ^{it}ψ^{-it}·ψ^{-is}
    = φ^{i(s+t)}ψ^{-i(s+t)}`. -/
theorem cocycle_temporal (s t : ℝ) :
    cocycle phi psi (s + t)
      = cocycle phi psi s * sigma psi s (cocycle phi psi t) := by
  simp only [cocycle, sigma]
  calc modPow phi (s + t) * modPow psi (-(s + t))
      = modPow phi s * modPow phi t * (modPow psi (-t) * modPow psi (-s)) := by
        rw [modPow_add, neg_add_rev, modPow_add]
    _ = modPow phi s * ((modPow psi (-s) * modPow psi s) *
          (modPow phi t * (modPow psi (-t) * modPow psi (-s)))) := by
        rw [modPow_neg_mul, one_mul]
        simp only [mul_assoc]
    _ = modPow phi s * modPow psi (-s) *
          (modPow psi s * (modPow phi t * modPow psi (-t)) * modPow psi (-s)) := by
        simp only [mul_assoc]

/-! ## U — unitariedade -/

/-- [KERNEL] `([Dφ:Dψ]_t)ᴴ = [Dψ:Dφ]_t`: a adjunta INVERTE os estados no
    mesmo t — `(φ^{it}ψ^{-it})ᴴ = ψ^{it}φ^{-it}`. -/
theorem cocycle_conjTranspose (t : ℝ) :
    (cocycle phi psi t)ᴴ = cocycle psi phi t := by
  simp only [cocycle, conjTranspose_mul, modPow_conjTranspose, neg_neg]

/-- [KERNEL] `[Dφ:Dψ]_t` é UNITÁRIO: produto de unitários do fluxo modular. -/
theorem cocycle_mem_unitary (t : ℝ) :
    cocycle phi psi t ∈ unitary (Matrix n n ℂ) :=
  mul_mem (modPow_mem_unitary phi t) (modPow_mem_unitary psi (-t))

/-! ## E3c — gerador no caso comutante -/

/-- [KERNEL] GERADOR NO CASO COMUTANTE: se `log φ` e `log ψ` comutam,
    `[Dφ:Dψ]_t = exp(it·(log φ − log ψ))` — o cociclo é gerado pela
    DIFERENÇA dos hamiltonianos modulares (o caso geral exige a expansão
    de Dyson, fora da sombra finita comutante). -/
theorem cocycle_of_commute (h : Commute (logRho phi) (logRho psi)) (t : ℝ) :
    cocycle phi psi t
      = exp (((t : ℂ) * Complex.I) • (logRho phi - logRho psi)) := by
  have hneg : ((-t : ℝ) : ℂ) * Complex.I = -((t : ℂ) * Complex.I) := by
    push_cast
    ring
  have hcomm : Commute (((t : ℂ) * Complex.I) • logRho phi)
      (-(((t : ℂ) * Complex.I) • logRho psi)) :=
    ((h.smul_left _).smul_right _).neg_right
  simp only [cocycle, modPow]
  rw [hneg, neg_smul, ← Matrix.exp_add_of_commute _ _ hcomm, ← sub_eq_add_neg,
    ← smul_sub]

/-! ## E6 — covariância unitária (a face finita da covariância global) -/

/-- [KERNEL] CONJUGAÇÃO DO GERADOR: `log(VφVᴴ) = V·(log φ)·Vᴴ` para V
    unitário e φ positiva-definida — o cálculo funcional contínuo comuta
    com o automorfismo interno `Unitary.conjStarAlgAut`
    (`StarAlgHomClass.map_cfc`). -/
theorem logRho_conj (V : Matrix n n ℂ) (hV : V ∈ unitary (Matrix n n ℂ))
    (hphi : phi.PosDef) :
    logRho (V * phi * Vᴴ) = V * logRho phi * Vᴴ := by
  have ha : IsSelfAdjoint phi := hphi.isHermitian.isSelfAdjoint
  have hf : ContinuousOn Real.log (spectrum ℝ phi) :=
    Real.continuousOn_log.mono fun x hx =>
      (hphi.isStrictlyPositive.spectrum_pos hx).ne'
  have hcont : Continuous fun x : Matrix n n ℂ => V * x * star V :=
    (continuous_mul_const (star V)).comp (continuous_const_mul V)
  have hsa : IsSelfAdjoint (V * phi * star V) := ha.conjugate V
  have key := StarAlgHomClass.map_cfc (S := ℂ)
    (Unitary.conjStarAlgAut ℂ (Matrix n n ℂ) ⟨V, hV⟩) Real.log phi hf hcont ha hsa
  simp only [Unitary.conjStarAlgAut_apply] at key
  exact key.symm

/-- [KERNEL] COVARIÂNCIA DO FLUXO: `(VφVᴴ)^{it} = V·φ^{it}·Vᴴ` — conjugar
    o estado conjuga o unitário modular (`Matrix.exp_conj` sobre
    `logRho_conj`). -/
theorem modPow_conj (V : Matrix n n ℂ) (hV : V ∈ unitary (Matrix n n ℂ))
    (hphi : phi.PosDef) (t : ℝ) :
    modPow (V * phi * Vᴴ) t = V * modPow phi t * Vᴴ := by
  have h1 : Vᴴ * V = 1 := by
    rw [← Matrix.star_eq_conjTranspose]
    exact (Unitary.mem_iff.mp hV).1
  have h2 : V * Vᴴ = 1 := by
    rw [← Matrix.star_eq_conjTranspose]
    exact (Unitary.mem_iff.mp hV).2
  have hVu : IsUnit V := ⟨⟨V, Vᴴ, h2, h1⟩, rfl⟩
  have hVinv : V⁻¹ = Vᴴ := Matrix.inv_eq_left_inv h1
  unfold modPow
  rw [logRho_conj phi V hV hphi, ← smul_mul_assoc, ← mul_smul_comm, ← hVinv]
  exact Matrix.exp_conj _ _ hVu

/-- [KERNEL] COVARIÂNCIA UNITÁRIA DO COCICLO — a face finita da covariância
    global do Lema 3: conjugar os ESTADOS pelo unitário V conjuga o
    COCICLO, `[D(VφVᴴ) : D(VψVᴴ)]_t = V·[Dφ:Dψ]_t·Vᴴ`. O levantamento ao
    cociclo de Connes em III₁ genuína (sem projeções minimais) é o teorema
    aberto — aqui vive só o esqueleto algébrico. -/
theorem cocycle_covariance (V : Matrix n n ℂ) (hV : V ∈ unitary (Matrix n n ℂ))
    (hphi : phi.PosDef) (hpsi : psi.PosDef) (t : ℝ) :
    cocycle (V * phi * Vᴴ) (V * psi * Vᴴ) t = V * cocycle phi psi t * Vᴴ := by
  have h1 : Vᴴ * V = 1 := by
    rw [← Matrix.star_eq_conjTranspose]
    exact (Unitary.mem_iff.mp hV).1
  simp only [cocycle]
  rw [modPow_conj phi V hV hphi t, modPow_conj psi V hV hpsi (-t)]
  calc V * modPow phi t * Vᴴ * (V * modPow psi (-t) * Vᴴ)
      = V * (modPow phi t * ((Vᴴ * V) * (modPow psi (-t) * Vᴴ))) := by
        simp only [mul_assoc]
    _ = V * (modPow phi t * modPow psi (-t)) * Vᴴ := by
        rw [h1, one_mul]
        simp only [mul_assoc]

end

end TGLExt
