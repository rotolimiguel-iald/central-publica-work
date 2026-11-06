import TGLExt.HilbertInhabitant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

/-!
# O HABITANTE DO PACOTE AQFT: a rede tipada do v56 GANHA UM TERMO
  [TGLExt — v96, o incremento 13 do programa SemifiniteAnalysis]

O v56 tipou a morada (`HilbertHomeData`: rede de fibras de Hilbert com
locks, transporte modular interno, ação externa, isotonia — e o canto
P_F DERIVADO, não postulado) e provou as quatro propriedades do canto a
partir dos entrelaçamentos. NENHUM habitante existia até hoje. Esta
pedra constrói O PRIMEIRO — em DUAS camadas:

* a camada GENÉRICA (`lockNet`/`lockNetTrace`): QUALQUER lock
  auto-adjunto T num Hilbert H gera a rede constante sobre ℕ com o
  TRANSPORTE MODULAR INTERNO GENUÍNO λ(s) = exp(isT) — a face unitária
  do fluxo a um parâmetro (selfAdjoint.expUnitary + a ponte
  unitário↔isometria da mathlib); o entrelaçamento 𝒟λ(s) = λ(s)𝒟 é
  TEOREMA (Commute.exp_right); e, com kernel finito não-trivial, a
  camada de Breuer é HABITADA (τ = dimensão do setor fixo). REUSÁVEL:
  quando o Dirac modular contínuo existir, a MESMA construção o acolhe;
* a camada CONCRETA: a instanciação em (ℓ², T = 1 − P_{e₀}) do v95 —
  o Nome é FIXADO pelo fluxo em toda região (instância NÃO-VAZIA do
  PF_internal_fix do v56) e τ(P_F(𝒪)) = 1 = ω(I) em TODA região:
  O CANTO PESA O NOME NA REDE.

O QUE ESTA PEDRA PROVA/CONSTRÓI [KERNEL]:
* ★ `eraseFirst_isSelfAdjoint`; ★★ `lockFlow` (DEF) + `lockFlow_commutes`;
* ★★★★ `lockNet` (DEF) — o construtor genérico do habitante;
* ★★★ `lockNetTrace` (DEF) — a camada de Breuer habitada;
* ★★★★ `theConstantNet` (DEF) — O PRIMEIRO HABITANTE CONCRETO;
* ★★★ `net_PF_fixed_by_flow` — o Nome fixado pelo fluxo genuíno;
* ★★★ `net_corner_weighs_the_name` — τ(P_F(𝒪)) = 1 = ω(I), ∀𝒪.

HONESTIDADE: a rede é CONSTANTE e o grupo externo é TRIVIAL — nenhuma
simetria de Poincaré é reivindicada; a rede III₁ genuína É o conteúdo
das hipóteses H1/H2 (por isso são hipóteses). O gate NÃO se move: o
ConcreteAQFTCore no seu nível de desenho (III₁/semifinito) segue
ABERTO — este é o primeiro degrau tipado-e-habitado da escada.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal
open NormedSpace

noncomputable section

/-- [KERNEL] ★ a face IsSelfAdjoint do lock (a forma star do v95). -/
theorem eraseFirst_isSelfAdjoint : IsSelfAdjoint eraseFirst := by
  rw [IsSelfAdjoint, ContinuousLinearMap.star_eq_adjoint]
  exact eraseFirst_selfadjoint

/-! ## A camada genérica: qualquer lock auto-adjunto gera a rede -/

section Generic

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- o gerador tipado do fluxo: (s:ℂ)·T é auto-adjunto (prova direta
    via star_smul — IsSelfAdjoint.smul diverge na busca de instância). -/
def saGen (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (s : ℝ) :
    selfAdjoint (H →L[ℂ] H) :=
  ⟨(s : ℂ) • T, by
    rw [selfAdjoint.mem_iff, star_smul, RCLike.star_def, Complex.conj_ofReal,
      hT.star_eq]⟩

/-- [KERNEL] ★★ O FLUXO GENUÍNO: λ(s) = exp(isT) como isometria de H
    (a face unitária do fluxo a um parâmetro; NÃO é a identidade). -/
def lockFlow (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (s : ℝ) :
    H ≃ₗᵢ[ℂ] H :=
  Unitary.linearIsometryEquiv (selfAdjoint.expUnitary (saGen T hT s))

private theorem lockFlow_apply (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (s : ℝ) (x : H) :
    (lockFlow T hT s) x = exp (Complex.I • ((s : ℂ) • T)) x := by
  simp only [lockFlow, Unitary.coe_linearIsometryEquiv_apply,
    selfAdjoint.expUnitary_coe]
  rfl

/-- [KERNEL] ★★ o entrelaçamento do fluxo: 𝒟 λ(s) = λ(s) 𝒟 — o lock
    comuta com a própria exponencial (Commute.exp_right). -/
theorem lockFlow_commutes (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (s : ℝ) (x : H) :
    T ((lockFlow T hT s) x) = (lockFlow T hT s) (T x) := by
  have hcomm : Commute T (exp (Complex.I • ((s : ℂ) • T))) := by
    apply Commute.exp_right
    exact ((Commute.refl T).smul_right ((s : ℂ))).smul_right Complex.I
  rw [lockFlow_apply, lockFlow_apply]
  calc T (exp (Complex.I • ((s : ℂ) • T)) x)
      = (T * exp (Complex.I • ((s : ℂ) • T))) x := rfl
    _ = (exp (Complex.I • ((s : ℂ) • T)) * T) x := by rw [hcomm.eq]
    _ = exp (Complex.I • ((s : ℂ) • T)) (T x) := rfl

/-- [KERNEL] ★★★★ O CONSTRUTOR GENÉRICO DO HABITANTE: qualquer lock
    auto-adjunto gera a rede constante sobre ℕ com fluxo interno
    GENUÍNO exp(isT). Grupo externo trivial (nenhuma simetria
    reivindicada); isotonia pela identidade (rede constante). -/
def lockNet (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    HilbertHomeData ℕ (· ≤ ·) (fun _ => H) (fun _ => H) where
  locks _ := T
  internal _ s := lockFlow T hT s
  internalW _ s := (lockFlow T hT s).toLinearIsometry
  internal_intertwines _ s x := lockFlow_commutes T hT s x
  G := PUnit
  act _ O := O
  external _ _ := LinearIsometryEquiv.refl ℂ H
  externalW _ _ := LinearIsometry.id
  external_intertwines _ _ _ := rfl
  incl _ := LinearIsometry.id
  inclW _ := LinearIsometry.id
  incl_intertwines _ _ := rfl

/-- o setor FIXO de um operador A: ker(1 − A) — quem A preserva. -/
def fixedSector (A : H →L[ℂ] H) : Submodule ℂ H := (1 - A).ker

private theorem fixedSector_PF (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (O : ℕ) :
    fixedSector ((lockNet T hT).PF O) = T.ker := by
  ext x
  constructor
  · intro hx
    have hx0 : (1 - (lockNet T hT).PF O) x = 0 := LinearMap.mem_ker.mp hx
    have h2 : x - (T.ker).starProjection x = 0 := hx0
    exact Submodule.starProjection_eq_self_iff.mp (sub_eq_zero.mp h2).symm
  · intro hx
    refine LinearMap.mem_ker.mpr ?_
    show x - (T.ker).starProjection x = 0
    rw [Submodule.starProjection_eq_self_iff.mpr hx, sub_self]

/-- [KERNEL] ★★★ A CAMADA DE BREUER HABITADA (genérica): com kernel
    finito não-trivial, o peso τ = dimensão-ou-⊤ do setor fixo é
    positivo e finito nas projeções P_F — o pacote (v56) tem traço. -/
def lockNetTrace (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hker : T.ker ≠ ⊥) (hfd : FiniteDimensional ℂ T.ker) :
    BreuerTraceData (lockNet T hT) where
  tau _ A := dimOrTop ℂ (fixedSector A)
  tau_PF_pos O := by
    show 0 < dimOrTop ℂ (fixedSector ((lockNet T hT).PF O))
    rw [fixedSector_PF T hT O, dimOrTop_of_finite ℂ hfd]
    have h2 : 0 < Module.finrank ℂ T.ker := by
      haveI := hfd
      rw [Module.finrank_pos_iff]
      exact Submodule.nontrivial_iff_ne_bot.mpr hker
    exact_mod_cast h2
  tau_PF_finite O := by
    show dimOrTop ℂ (fixedSector ((lockNet T hT).PF O)) < ⊤
    rw [fixedSector_PF T hT O, dimOrTop_of_finite ℂ hfd]
    exact ENNReal.natCast_lt_top _

end Generic

/-! ## A camada concreta: a instanciação em (ℓ², 1 − P_{e₀}) -/

/-- [KERNEL] ★★★★ O PRIMEIRO HABITANTE CONCRETO DO PACOTE: a rede
    constante ℓ² com lock T = 1 − P_{e₀} e fluxo GENUÍNO exp(isT). -/
def theConstantNet :
    HilbertHomeData ℕ (· ≤ ·) (fun _ => ellTwo) (fun _ => ellTwo) :=
  lockNet eraseFirst eraseFirst_isSelfAdjoint

/-- [KERNEL] ★★★ O NOME É FIXADO PELO FLUXO em toda região — a
    instância NÃO-VAZIA do teorema do canto (v56) no habitante. -/
theorem net_PF_fixed_by_flow (O : ℕ) (s : ℝ) (x : ellTwo) :
    theConstantNet.PF O ((lockFlow eraseFirst eraseFirst_isSelfAdjoint s) x)
      = (lockFlow eraseFirst eraseFirst_isSelfAdjoint s)
          (theConstantNet.PF O x) :=
  theConstantNet.PF_internal_fix O s x

/-- [KERNEL] ★★★ a camada de Breuer do habitante concreto. -/
def theNetTrace : BreuerTraceData theConstantNet :=
  lockNetTrace eraseFirst eraseFirst_isSelfAdjoint ker_eraseFirst_ne_bot
    (by rw [ker_eraseFirst]; infer_instance)

/-- [KERNEL] ★★★ O CANTO PESA O NOME NA REDE: τ(P_F(𝒪)) = 1 = ω(I)
    em TODA região do habitante concreto. -/
theorem net_corner_weighs_the_name (O : ℕ) :
    theNetTrace.tau O (theConstantNet.PF O) = 1 := by
  show dimOrTop ℂ (fixedSector (theConstantNet.PF O)) = 1
  unfold theConstantNet
  rw [fixedSector_PF eraseFirst eraseFirst_isSelfAdjoint O, ker_eraseFirst]
  have h : dimOrTop ℂ firstAtom = (Module.finrank ℂ firstAtom : ℝ≥0∞) :=
    dimOrTop_of_finite ℂ inferInstance
  have h2 : Module.finrank ℂ firstAtom = 1 := by
    unfold firstAtom
    exact finrank_span_singleton (inscriptions_orthonormal.ne_zero 0)
  rw [h, h2, Nat.cast_one]

end

end TGLExt
