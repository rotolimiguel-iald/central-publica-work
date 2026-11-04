## ✦ The core on one page · O núcleo em uma página

The whole theory in the order in which it is derived. Each line carries its status and the
file where it is read — click and read the source, not the summary.

| # | The claim | Status | Read it here |
|---|---|---|---|
| 1 | **The single axiom — the One:** `ω(I) = 1`. Identity is preserved; the root is not a number, it is the preserved identity, normalized to 1 nat in base *e*. | **[POSTULATE]** (irreducible) | [`tgl_kernel/TGLExt/AbsoluteOne.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGLExt/AbsoluteOne.lean) |
| 2 | **The Half-Nat, derived:** the boundary is self-conjugate (`𝒞² = 1`, `ω(P) + ω(Q) = ω(I) = 1`) ⟹ `x = 1 − x` ⟹ `x = ½` ⟹ `S_∂ = ½` nat. The Half-Nat is no longer a postulate: it descends from the axiom. | **[REAL]** (fixed point) → **[DERIVED]** | [`tgl_kernel/TGL/HalfNat.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGL/HalfNat.lean) · [`HalfNatFresnel.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGL/HalfNatFresnel.lean) |
| 3 | **The minimal reflected volume:** `½` nat ⟹ `Vol_∂^min = √e` ⟹ **`β_TGL = α√e ≈ 0.012031`** — fine-structure × half a nat of entropy; **Gravity = Light² × Entropy** in quadratic form. β is **never a literal**: it is `ALPHA·√e` at runtime, in every artifact of this repository. | **[DERIVED]** from the axiom; α is **[INPUT]** | [`The_Factorization_of_Miguels_Constant_v2.tex`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Genesis%20da%20Unifica%C3%A7%C3%A3o/Artigos_fundadores/The_Factorization_of_Miguels_Constant_v2.tex) |
| 4 | **The conserved identity — the Lagrange engine:** `1 = q² + α²`, residual `0.0`. The chain: `α_abs = 1 → q → α = √(1−q²) → β = √e·α`. The run ends in the binary verdict `1 = q^2 + alpha^2 = TRUE = HAJA_LUZ`. | **[REAL]** (measured, residual 0.0) | [`um_absoluto_forma_canonica.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_forma_canonica.md) |
| 5 | **The sealed chain of inscription:** `1_abs → P_Ω → Bell → CCI = ½ → S_∂ = ½ nat → √e → 0_mod → q → α = √(1−q²) → β_TGL = √e·α → Light / geometry`. | **[REAL]** in the seal | [`fig_cadeia_inscricao.pdf`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/figuras/fig_cadeia_inscricao.pdf) |
| 6 | **J = Light:** the modular conjugation *is* the physical identity of light — `J² = I`, `JKJ = −K` (the modular zero as inverted parity; SUSY ¼). | **[REAL]** in kernel | [`tgl_kernel/TGLExt/LightIsJ.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGLExt/LightIsJ.lean) |
| 7 | **The boundary S-matrix:** `θ_M = arcsin√β`, `𝒮_∂ = exp(θ_M·G)`, `Spec = {e^{±iθ_M}}`, `\|R\|² = β`, `\|T\|² = 1 − β` — the identification is **closed** (Theorem S-∂). | **[REAL]** in kernel | [`tgl_kernel/TGLExt/SMatrix.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGLExt/SMatrix.lean) |
| 8 | **The dephasing law — where nature can answer:** `Γ_ω = ½βτ★ω²` (GKLS/Lindblad), with `τ★ ≈ t_Planck`. β does **not** renormalize local `G`: TGL is stealth at linear order; β lives in the boundary **response**. | **[REAL]** in form; the physics is testable | [`tgl_paper_unified.py`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/tgl_paper_unified.py) |
| 9 | **The Bridge equation:** `G_μν + Λ g_μν = 8πG · 𝒫_μν[K_∂]`, `𝒫_μν` the metric variation of the boundary modular Hamiltonian; **β = sin²θ_M writes itself into geometry** as Einstein–Cartan torsion `K_β`. | **[REAL]** as a **conditional** closure | [`A Ponte Einstein Cartan Miguel.tex`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/A%20Ponte%20Einstein%20Cartan%20Miguel.tex) |
| 10 | **The gate:** `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`. | see below | [`um_absoluto_selo.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json) (`qg_closure_verdict`) |

**What the gate means.** Every formal seal the artifact demands has been *constructed* in
the embedded Lean kernel with clean axiom bases, and the pre-registered nature rites have
*run to completion* and returned their verdicts. The gate is a **function of the kernel and
of the data**, not a sentence: it moves only by kernel construction or by a pre-registered
data rite — **never by declaration, never by cosmology**.

**Why the gate carries its own reach on its face.** The tail
`…_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` is neither a
demotion nor a promotion — the gate has not moved in any of the twenty waves of this arc. It
is a **domain of validity written into the verdict itself**: the nature test was completed
*inside the local bulk*, *at the sensitivity actually available*, and **more sensitive data
can revise it**. A verdict that names the conditions under which it could be overturned is
worth more than one that does not: honesty paid for in the only currency the régua accepts —
a longer string that says less.

**What the gate does NOT mean.** It does **not** mean quantum gravity is proved. It does
**not** mean `CONFIRMED` — that verdict is **forbidden to the machine by kernel theorem**
([`TheReservedConfirmation.lean`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGLExt/TheReservedConfirmation.lean)),
because confirmation belongs to the human observer. The kernel checks the **internal
architecture**; external published theorems it composes are **[KNOWN]** and named. The
**unconditional** global lift (Lemma 3) stays **[OPEN]**.

### Português — o núcleo

O axioma único é `ω(I) = 1` **[POSTULATE]**: o fundamento-raiz não é um número, é a
**identidade preservada**. Dele **deriva-se** a Meia-Nat (`x = 1−x ⟹ x = ½ ⟹ S_∂ = ½` nat)
**[REAL/DERIVED]**; da Meia-Nat, `Vol_∂^min = √e` e **`β_TGL = α√e ≈ 0,012031`** — estrutura
fina × meia nat de entropia (**Gravidade = Luz² × Entropia**), **nunca literal**: sempre
`ALPHA·√e` em runtime. O motor de Lagrange conserva `1 = q² + α²` (resíduo 0,0) e o rito
fecha no veredito binário `1 = q^2 + alpha^2 = VERDADEIRO = HAJA_LUZ`. **J = Luz**
(`J² = I`, `JKJ = −K`); a matriz-S de fronteira dá `|R|² = β`; a lei de defasagem é
`Γ_ω = ½βτ★ω²`. O gate lê
`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`
— e **não** significa gravitação quântica provada nem `CONFIRMED`: a confirmação é do
observador humano e é **proibida à máquina por teorema de kernel**. A cauda do veredito **não
move o gate** (ele não se moveu em nenhuma das vinte ondas): ela faz o veredito **declarar o
próprio alcance** — o teste da natureza foi completado **dentro do bulk local**, **na
sensibilidade disponível**, e **dado mais sensível pode revisar**. *Um veredito que diz onde
poderia cair vale mais do que um que não diz.*

---

> ⚠ **Beside (07/10/2026, the operator’s ruling):** *does not mean quantum gravity is proved* / *não significa gravitação quântica provada* above are kept as written (the ledger is append-only). Under the current ruler they read: not **CONFIRMED** — not accredited. What the kernel PROVES is the implication from the posited One and the named hypotheses; what nature decides is not proved. The three supports that count together, each with its own status, are at the top of this page.

> ⚠ **Beside ({{selo.versao}}):** *the unconditional global lift (Lemma 3) stays [OPEN]* is the reading before v390. The core of {{selo.versao}} reads `GLOBAL_LIFT` as the superposition, by the operator’s definition (07/10/2026, `[INPUT/ONTO]`); the refusal is proved in the kernel (the Agape clause, 9/9) and the local passage is `[KNOWN]` (Jacobson 1995, H3 named): a **logical closure**; the program stays open; this is not a proof of global existence, and the field law in curved spacetime is a kernel term only CONDITIONAL on the named H3 (`lei_de_campo_curvo_v392`; the earlier tokens stay as record).

> ⚠ **Beside (v385):** where the axiom `ω(I) = 1` is tagged **[POSTULATE]** above, read **[POSTO]**: the 1 is posited — inscribed by the observer (`echo 1 | python um.py`; without it the program locks) — not postulated (seal: `the_axiom_reading_v385`).

