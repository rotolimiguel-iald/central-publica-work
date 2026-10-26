import TGLExt.ModularFlow
import TGLExt.CornerFamily
import TGLExt.GravitonPolarization

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A testemunha é o transporte: Euler–Lagrange, a lei 𝒯_{t,s} e a holonomia
  [TGLExt — v54, derivação do operador tipada]

Derivação do operador (14/07/2026, `DERIVACAO_OPERADOR_A_TESTEMUNHA_E_O_
TRANSPORTE.md`): a testemunha completa é a LAGRANGIANA; e "o ponto físico
crítico não é ponto — é o TRANSPORTE". Faces finitas tipadas aqui:

* ★ SETOR DA AÇÃO (a Lagrangiana dos Three Locks): `⟨v, DᴴD v⟩ = ⟨Dv, Dv⟩`
  (cada setor é um quadrado — `lock_pairing_eq`); a ação dos três locks
  anula SSE cada lock anula (`action_locks_zero_iff` — Euler–Lagrange
  SELECIONA o núcleo: `ker H_{3L} = ∩ ker Dᵢ`, e `P_F` projeta os
  MINIMIZADORES da ação, não uma escolha posterior);
* ★ EULER–LAGRANGE COMO DERIVADA GENUÍNA (`action_hasDerivAt`):
  `d/dε ⟨v+εη, H(v+εη)⟩|₀ = 2·re⟨η, Hv⟩` — e crítico em TODA direção ⟺
  `Hv = 0` (`critical_pairing_iff`): as equações de EL são o certificado;
* ★ O TRANSPORTE (`transport ρ t s := σ_{t−s}`): reflexividade e a LEI DE
  COMPOSIÇÃO `𝒯_{t,r}∘𝒯_{r,s} = 𝒯_{t,s}`; o NOME é fixado pelo próprio
  transporte (`transport_fixes_name` — KMS dinâmico); o traço é preservado
  (`transport_trace` — `c_{t,s} = 1` interno, o par honesto da escala dual
  `e^{−s}` do v45); o canto espectral é COVARIANTEMENTE CONSTANTE
  (`transport_corner` — `P_F(t) = P_F` sob o transporte do próprio gerador);
* `NamedTransportData` + ★ o TERMO `canonicalNamedTransport` (o tipo admite
  habitantes triviais — o CONTEÚDO está no termo canônico sobre o fluxo
  modular e nos teoremas acima; a lição do v22/v23 declarada);
* ★ HOLONOMIA INFINITESIMAL (`excite_holonomy`): `δ_A∘δ_B − δ_B∘δ_A =
  δ_{[A,B]}` — a curvatura do transporte infinitesimal FECHA no comutador
  dos geradores ("gravidade = curvatura do transporte", face infinitesimal;
  ponte com `[h₊,h×] = 2J` do v49); geradores comutantes ⟹ transporte
  PLANO (`excite_holonomy_flat`).

HONESTIDADE. Isto NÃO fecha a testemunha contínua: a família covariante
não-trivial de cantos exige transporte EXTERNO ao gerador (`U(g)` de
Poincaré — o gate do canto covariante, memorando §4); a reconstrução
holonomia ⟶ `R_{μνρσ}` completa segue ABERTA; a guarda anti-`S_fake`
(a ação não pode ser a soma das conclusões desejadas) é princípio de
design registrado no módulo do runtime. β JAMAIS entra: ρ, H genéricos.
Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — o setor da ação: cada lock é um quadrado; EL seleciona o núcleo -/

/-- [KERNEL] O PAREAMENTO DO LOCK: `⟨v, DᴴD v⟩ = ⟨Dv, Dv⟩` — cada setor da
    ação dos Three Locks é um quadrado perfeito (a positividade é estrutural,
    não postulada). -/
theorem lock_pairing_eq (D : Matrix n n ℂ) (v : n → ℂ) :
    star v ⬝ᵥ (Dᴴ * D).mulVec v = star (D.mulVec v) ⬝ᵥ D.mulVec v := by
  rw [← Matrix.mulVec_mulVec, dotProduct_mulVec, Matrix.star_mulVec]

/-- [KERNEL] ★ EULER–LAGRANGE SELECIONA O NÚCLEO: a ação dos três locks
    `S_{3L}[v] = ⟨v, (D_cᴴD_c + D_bᴴD_b + D_zᴴD_z) v⟩` anula SSE cada lock
    anula — `ker H_{3L} = ker D_c ∩ ker D_b ∩ ker D_z`. `P_F = 1_{{0}}(H_{3L})`
    é o projetor sobre os MINIMIZADORES da ação (derivação do operador:
    o canto não é escolhido depois da Lagrangiana; é o suporte do mínimo). -/
theorem action_locks_zero_iff (Dc Db Dz : Matrix n n ℂ) (v : n → ℂ) :
    star v ⬝ᵥ (Dcᴴ * Dc + Dbᴴ * Db + Dzᴴ * Dz).mulVec v = 0 ↔
      Dc.mulVec v = 0 ∧ Db.mulVec v = 0 ∧ Dz.mulVec v = 0 := by
  have hsplit : star v ⬝ᵥ (Dcᴴ * Dc + Dbᴴ * Db + Dzᴴ * Dz).mulVec v
      = star (Dc.mulVec v) ⬝ᵥ Dc.mulVec v
        + star (Db.mulVec v) ⬝ᵥ Db.mulVec v
        + star (Dz.mulVec v) ⬝ᵥ Dz.mulVec v := by
    rw [Matrix.add_mulVec, Matrix.add_mulVec, dotProduct_add, dotProduct_add,
      lock_pairing_eq, lock_pairing_eq, lock_pairing_eq]
  rw [hsplit]
  constructor
  · intro h
    have h1 : (0 : ℂ) ≤ star (Dc.mulVec v) ⬝ᵥ Dc.mulVec v :=
      dotProduct_star_self_nonneg _
    have h2 : (0 : ℂ) ≤ star (Db.mulVec v) ⬝ᵥ Db.mulVec v :=
      dotProduct_star_self_nonneg _
    have h3 : (0 : ℂ) ≤ star (Dz.mulVec v) ⬝ᵥ Dz.mulVec v :=
      dotProduct_star_self_nonneg _
    have h12 := (add_eq_zero_iff_of_nonneg (add_nonneg h1 h2) h3).mp h
    have hcb := (add_eq_zero_iff_of_nonneg h1 h2).mp h12.1
    exact ⟨dotProduct_star_self_eq_zero.mp hcb.1,
      dotProduct_star_self_eq_zero.mp hcb.2,
      dotProduct_star_self_eq_zero.mp h12.2⟩
  · rintro ⟨h1, h2, h3⟩
    rw [h1, h2, h3]
    simp

/-! ## B — Euler–Lagrange como derivada genuína: o certificado -/

/-- [KERNEL] Simetria hermitiana do pareamento (parte real):
    `re⟨v, Hη⟩ = re⟨η, Hv⟩` para `H` hermitiana. -/
theorem hermitian_pairing_re (H : Matrix n n ℂ) (hH : H.IsHermitian)
    (v η : n → ℂ) :
    (star v ⬝ᵥ H.mulVec η).re = (star η ⬝ᵥ H.mulVec v).re := by
  have hconj : star (star η ⬝ᵥ H.mulVec v) = star v ⬝ᵥ H.mulVec η := by
    rw [star_dotProduct, star_star, Matrix.star_mulVec, hH.eq,
      ← dotProduct_mulVec]
  calc (star v ⬝ᵥ H.mulVec η).re
      = (star (star η ⬝ᵥ H.mulVec v)).re := by rw [hconj]
    _ = (star η ⬝ᵥ H.mulVec v).re := by
        rw [Complex.star_def, Complex.conj_re]

/-- [KERNEL] ★ EULER–LAGRANGE COMO DERIVADA GENUÍNA: ao longo de QUALQUER
    direção `η`, `d/dε S[v + εη]|_{ε=0} = 2·re⟨η, Hv⟩` (`HasDerivAt`, não
    forma-check). A variação da ação quadrática é o pareamento com `Hv` —
    "as equações de Euler–Lagrange são o certificado". -/
theorem action_hasDerivAt (H : Matrix n n ℂ) (hH : H.IsHermitian)
    (v η : n → ℂ) :
    HasDerivAt
      (fun ε : ℝ => (star (v + (ε : ℂ) • η) ⬝ᵥ H.mulVec (v + (ε : ℂ) • η)).re)
      (2 * (star η ⬝ᵥ H.mulVec v).re) 0 := by
  have hpoly : ∀ ε : ℝ,
      (star (v + (ε : ℂ) • η) ⬝ᵥ H.mulVec (v + (ε : ℂ) • η)).re
        = (star v ⬝ᵥ H.mulVec v).re
          + ε * ((star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re)
          + ε ^ 2 * (star η ⬝ᵥ H.mulVec η).re := by
    intro ε
    have hstar : star (v + (ε : ℂ) • η) = star v + (ε : ℂ) • star η := by
      rw [star_add, star_smul]
      congr 1
      simp [Complex.conj_ofReal]
    rw [Matrix.mulVec_add, Matrix.mulVec_smul, hstar]
    simp only [add_dotProduct, dotProduct_add, smul_dotProduct,
      dotProduct_smul, smul_eq_mul]
    simp only [Complex.add_re, Complex.mul_re, Complex.ofReal_re,
      Complex.ofReal_im]
    ring
  have hfun : (fun ε : ℝ =>
      (star (v + (ε : ℂ) • η) ⬝ᵥ H.mulVec (v + (ε : ℂ) • η)).re)
      = fun ε : ℝ => (star v ⬝ᵥ H.mulVec v).re
          + ε * ((star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re)
          + ε ^ 2 * (star η ⬝ᵥ H.mulVec η).re :=
    funext hpoly
  rw [hfun]
  have hlin : HasDerivAt (fun ε : ℝ =>
      ε * ((star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re))
      ((star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re) 0 := by
    simpa using (hasDerivAt_id (0 : ℝ)).mul_const
      ((star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re)
  have hquad : HasDerivAt (fun ε : ℝ =>
      ε ^ 2 * (star η ⬝ᵥ H.mulVec η).re) 0 0 := by
    have := (hasDerivAt_pow 2 (0 : ℝ)).mul_const
      ((star η ⬝ᵥ H.mulVec η).re)
    simpa using this
  have htotal := (hlin.const_add ((star v ⬝ᵥ H.mulVec v).re)).add hquad
  have hval : (star η ⬝ᵥ H.mulVec v).re + (star v ⬝ᵥ H.mulVec η).re + 0
      = 2 * (star η ⬝ᵥ H.mulVec v).re := by
    rw [hermitian_pairing_re H hH v η]
    ring
  rw [← hval]
  exact htotal

/-- [KERNEL] ★ CRÍTICO ⟺ EQUAÇÃO DE EULER–LAGRANGE: o pareamento direcional
    anula em TODA direção sse `Hv = 0` (tome `η = Hv`: `⟨Hv, Hv⟩ = 0`).
    O físico não guarda um ponto — guarda a equação que o transporte resolve. -/
theorem critical_pairing_iff (H : Matrix n n ℂ) (v : n → ℂ) :
    (∀ η : n → ℂ, star η ⬝ᵥ H.mulVec v = 0) ↔ H.mulVec v = 0 := by
  constructor
  · intro h
    exact dotProduct_star_self_eq_zero.mp (h (H.mulVec v))
  · intro h η
    rw [h]
    simp

/-! ## C — o transporte 𝒯_{t,s}: reflexividade, composição, o Nome fixado -/

/-- O TRANSPORTE modular de dois parâmetros: `𝒯_{t,s} := σ_{t−s}` — a lei
    da passagem entre inscrições (VERBO = transporte). -/
def transport (ρ : Matrix n n ℂ) (t s : ℝ) (a : Matrix n n ℂ) :
    Matrix n n ℂ :=
  sigma ρ (t - s) a

/-- [KERNEL] `𝒯_{t,t} = id`: o transporte nulo é a identidade. -/
@[simp] theorem transport_refl (ρ : Matrix n n ℂ) (t : ℝ)
    (a : Matrix n n ℂ) : transport ρ t t a = a := by
  simp [transport, sigma, modPow_zero]

/-- [KERNEL] ★ A LEI DE COMPOSIÇÃO: `𝒯_{t,r} ∘ 𝒯_{r,s} = 𝒯_{t,s}` — a
    testemunha é uma lei de composição temporal/modular, não um habitante
    imóvel. -/
theorem transport_comp (ρ : Matrix n n ℂ) (t r s : ℝ) (a : Matrix n n ℂ) :
    transport ρ t r (transport ρ r s a) = transport ρ t s a := by
  unfold transport
  rw [sigma_sigma, sub_add_sub_cancel]

/-- [KERNEL] ★ O NOME É FIXADO PELO SEU PRÓPRIO TRANSPORTE:
    `ω(𝒯_{t,s}(a)) = ω(a)` — o estado crítico (KMS) é exatamente aquele cuja
    lei de transporte o preserva (o encontro do variacional v52 com o
    transporte: o físico é a relação, não o ponto). -/
theorem transport_fixes_name (ρ : Matrix n n ℂ) (t s : ℝ)
    (a : Matrix n n ℂ) :
    gibbs ρ (transport ρ t s a) = gibbs ρ a :=
  gibbs_sigma ρ (t - s) a

/-- [KERNEL] ★ O TRANSPORTE INTERNO PRESERVA O TRAÇO: `c_{t,s} = 1` — o par
    honesto da compatibilidade `τ ∘ 𝒯 = c·τ` (interno `c = 1` AQUI; dual
    `c = e^{−s}`, já tipado em `DualScalingData`, v45 — e é EXATAMENTE essa
    diferença que obstrui o traço nos degraus discretos). -/
theorem transport_trace (ρ : Matrix n n ℂ) (t s : ℝ) (a : Matrix n n ℂ) :
    (transport ρ t s a).trace = a.trace := by
  unfold transport sigma
  rw [Matrix.trace_mul_cycle, modPow_neg_mul, one_mul]

/-- [KERNEL] ★ O CANTO É COVARIANTEMENTE CONSTANTE: sob o transporte gerado
    pelo PRÓPRIO fluxo, `P_F(t) = 𝒯_{t,s}(P_F) = P_F` (canto espectral de
    gerador comutante). A família NÃO-trivial de cantos exige transporte
    EXTERNO (`U(g)` de Poincaré) — o gate aberto do canto covariante. -/
theorem transport_corner (ρ H : Matrix n n ℂ) (h : Commute ρ H)
    (f : ℝ → ℝ) (t s : ℝ) :
    transport ρ t s (cfc f H) = cfc f H :=
  corner_fixed_by_flow ρ H h f (t - s)

/-! ## D — a testemunha-transporte tipada e o termo canônico -/

/-- A LEI DO TRANSPORTE COM NOME: o tipo da testemunha do operador
    (`𝔚 = ({W_t}, {𝒯_{t,s}}, ℒ)` na face finita): transporte de dois
    parâmetros + funcional transportado. HONESTIDADE: o TIPO admite
    habitantes triviais (`T = id`); o conteúdo está no TERMO canônico
    sobre o fluxo modular (`canonicalNamedTransport`) e nos teoremas
    ★ acima — a mesma disciplina do v22/v23 (rigidez medida, não suposta). -/
structure NamedTransportData (M : Type) where
  /-- o transporte `𝒯_{t,s}`. -/
  T : ℝ → ℝ → M → M
  /-- o NOME transportado (o funcional). -/
  name : M → ℂ
  /-- `𝒯_{t,t} = id`. -/
  refl : ∀ (t : ℝ) (x : M), T t t x = x
  /-- `𝒯_{t,r} ∘ 𝒯_{r,s} = 𝒯_{t,s}`. -/
  comp : ∀ (t r s : ℝ) (x : M), T t r (T r s x) = T t s x
  /-- o Nome é constante ao longo do próprio transporte. -/
  name_transported : ∀ (t s : ℝ) (x : M), name (T t s x) = name x

/-- ★ O TERMO: o transporte modular canônico com o Nome de Gibbs —
    construído, não postulado (primeiro o termo; existência corolário). -/
noncomputable def canonicalNamedTransport (ρ : Matrix n n ℂ) :
    NamedTransportData (Matrix n n ℂ) where
  T := fun t s a => transport ρ t s a
  name := gibbs ρ
  refl := fun t x => transport_refl ρ t x
  comp := fun t r s x => transport_comp ρ t r s x
  name_transported := fun t s x => transport_fixes_name ρ t s x

/-- [KERNEL] ★ EXISTÊNCIA (corolário do termo): a testemunha-transporte
    com Nome existe sobre toda matriz densidade. -/
theorem canonicalNamedTransport_exists (ρ : Matrix n n ℂ) :
    Nonempty (NamedTransportData (Matrix n n ℂ)) :=
  ⟨canonicalNamedTransport ρ⟩

/-! ## E — a holonomia: a curvatura do transporte fecha no comutador -/

/-- [KERNEL] ★ A HOLONOMIA INFINITESIMAL FECHA NO COMUTADOR:
    `δ_A ∘ δ_B − δ_B ∘ δ_A = δ_{[A,B]}` — a falha de comutação de dois
    transportes infinitesimais É a excitação gerada pelo comutador dos
    geradores ("gravidade = curvatura do transporte", face infinitesimal;
    a ponte com `[h₊, h×] = 2J` do v49: a geometria fecha no gerador de
    helicidade). -/
theorem excite_holonomy (A B x : Matrix n n ℂ) :
    excite A (excite B x) - excite B (excite A x) = excite (excite A B) x := by
  simp only [excite]
  noncomm_ring

/-- [KERNEL] TRANSPORTE PLANO: geradores comutantes ⟹ holonomia zero —
    a curvatura mede exatamente a não-comutatividade (sem contraste,
    sem gravidade). -/
theorem excite_holonomy_flat (A B : Matrix n n ℂ) (h : Commute A B)
    (x : Matrix n n ℂ) :
    excite A (excite B x) - excite B (excite A x) = 0 := by
  rw [excite_holonomy]
  simp [excite, h.eq]

end

end TGLExt
