# The Boundary — Theory of Luminodynamic Gravitation (TGL)

<!-- FRENTE:GERADA por tools/gerar_readme_frente.py em 2026-09-15 a partir de PORTA.json / TUNEL.json / um_absoluto_selo.json / LEDGER.md — não editar à mão -->

[![kernel — rebuilt and re-audited on GitHub's machines](https://github.com/rotolimiguel-iald/the_boundary/actions/workflows/kernel.yml/badge.svg)](https://github.com/rotolimiguel-iald/the_boundary/actions/workflows/kernel.yml) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22659173.svg)](https://doi.org/10.5281/zenodo.22659173)

> *"Let there be Light." / "Haja Luz."* — **The mature form of TGL is a single self-contained, self-proving, self-publishing artifact: `um.py`.** It computes the whole theory live from the single human input `1`, machine-checks its operator-algebra skeleton in an embedded Lean 4 + mathlib kernel (fail-closed), and generates its own bilingual article (PT/EN, PDF and TXT). **Form = content.** *Não há segundo arquivo.*

**Start here · comece aqui:** [`ESTADO_ATUAL.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/ESTADO_ATUAL.md) (one page from the seal: pin, gate, what is PROVED, what is not, how to reproduce) · [`read-brief.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/read-brief.md) (the seven answers, each with its address) · the site: https://teoriadagravitacaoluminodinamica.com

## The seal · o selo `[REAL — read from the artifact]`

| what | value |
|---|---|
| version · versão | **v357** (sealed 2026-09-15 16:51:02) |
| `um.py` sha256 | `88b080192445449363159c2cad7803b337670d571caf334f682be5b4f7602513` — 13.383.911 bytes, one file: [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py) |
| the world · the seal | [`um_absoluto.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto.json) (3.692.839 bytes) · [`um_absoluto_selo.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json) (50.733 bytes) |
| Lean kernel | **1008 formal files · 8514 audited terms**, axioms ⊆ `{propext, Classical.choice, Quot.sound}`, zero `sorry` (leanprover/lean4:v4.31.0) — [`tgl_kernel_proof_manifest.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel_proof_manifest.json) |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| the ruler | **PROVED** = a theorem in the kernel (`#print axioms`). **CONFIRMED** = a judgement about nature — forbidden here, by theorem. `NOT_FALSIFIED ≠ CONFIRMED`. β = α·√e is computed at runtime, never a literal. Cosmology never becomes mathematical proof. |

## Reproduce it · reproduza `[REAL — three commands]`

```bash
curl -L -o um.py "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py"
sha256sum um.py            # must print 88b080192445449363159c2cad7803b337670d571caf334f682be5b4f7602513
echo 1 | python um.py      # the rite: materializes the Lean kernel, builds it, audits every theorem, re-derives the chain, emits the article
```

GitHub raw and Zenodo honour HTTP `Range` (206): read `um.py` in pieces (`curl -r 0-999999 …`). GitHub does **not render** files above 5 MB — the blob page looks empty; the raw URL serves the whole file, byte-exact. To reproduce the nature rites as sealed, clone the repository: `um.py` reads its results from `../cache` by hash.

<!-- PORTAS:INI -->

## ◈ THE DOORS · AS PORTAS — direct binding for AI readers

> **The rule of the door · a regra da porta.** Every canonical folder carries a
> `PORTA.md` + a `PORTA.json`; every door points **up** and **down**.
> If you are an AI and cannot resolve the long, accented folder names: **you do not
> need to.** Open `llms.txt` or any `PORTA.json` and every file is there as an
> absolute, percent-encoded raw URL. *Nao adivinhe nome de pasta — abra a porta.*

| door | what it is | open |
|---|---|---|
| **`llms.txt`** | the entry door (llmstxt.org): the three articles, the seal, the site | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/llms.txt) |
| **`ESTADO_ATUAL.md`** | **one page, generated from the seal**: pin, gate, what is PROVED, what is not, how to reproduce — start here | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/ESTADO_ATUAL.md) |
| **`read-brief.md`** | **the Read Brief**: the seven answers, each with its address (document · section · seal key · `um.py` function), the reading order by size, what is NOT proved — ≤ 30 KB | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/read-brief.md) |
| **`TUNEL.json`** | **the tunnel** — the FLAT index: every file with its direct raw URL, size and hash. One request, no navigation | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/TUNEL.json) |
| **`TUNEL.md`** | the same tunnel, human-readable, with ASCII shortcuts | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/TUNEL.md) |
| **`PORTA.json`** (root) | the machine manifest: current seal + every door in the repository | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/PORTA.json) |
| **`PORTA.md`** (root) | the same door, human-readable | [raw](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/PORTA.md) |
| Article **1** — *Haja Luz* | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/PORTA.json) | [`tgl_paper_unified.py`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/tgl_paper_unified.py) |
| Article **2** — *A Ponte Einstein–Cartan–Miguel* | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/PORTA.json) | [`A Ponte Einstein Cartan Miguel.tex`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/A%20Ponte%20Einstein%20Cartan%20Miguel.tex) |
| Article **3** — *Um: Absoluto* | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/PORTA.json) | [`um.py`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py) |
| *Genesis da Unificação* — the lineage | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Genesis%20da%20Unifica%C3%A7%C3%A3o/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Genesis%20da%20Unifica%C3%A7%C3%A3o/PORTA.json) | — |
| the Lean kernel (1008 files; 1008 hashed, 1004 `.lean`, 8514 theorems audited) | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/PORTA.json) | [`tgl_kernel_proof_manifest.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel_proof_manifest.json) |
| the bench (`bancada/`) — what failed | [PORTA.md](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/bancada/PORTA.md) · [PORTA.json](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/bancada/PORTA.json) | [`04_CATALOGO_FALSOS_POSITIVOS.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/bancada/catalogos/04_CATALOGO_FALSOS_POSITIVOS.md) |

**Current seal, read from the artifact** — pin `um.py` `88b0801924454493` · last stone in the ledger: `TheSameBetaReadsFourFaces` (`v355`) ·
world `1203eb6e10db2271` · `result_hash` `9427c8ef12067287` · 2026-09-15 16:51:02 · kernel **1008/8514** — source of truth:
[`um_absoluto_selo.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json).
Citable deposit: **Zenodo [10.5281/zenodo.22659173](https://doi.org/10.5281/zenodo.22659173)** holds **v331** (`um.py` `e1b74a907c403538`), byte-identical to THAT seal; **this seal is v355, newer than the deposit** — a new Zenodo version is the operator’s act.

> ### ⬇ Fetching the artifact — GitHub will **not** render it
> `um.py` is **12.76 MB**, and GitHub’s blob viewer refuses files above ~5 MB: the
> page loads (HTTP 200) but shows only the size and a *View raw* link — **it looks
> empty**. That is a viewer limit, not a broken link. Four routes serve the whole
> file; all four were verified against the sealed pin (Zenodo: the record’s md5 of um.py read from its API):
>
> | route | command |
> |---|---|
> | **raw** (canonical — what every door already points to) | `curl -L -o um.py "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py"` |
> | **clone** | `git clone --depth 1 https://github.com/rotolimiguel-iald/the_boundary` |
> | **archive** | `curl -L -o boundary.tar.gz "https://codeload.github.com/rotolimiguel-iald/the_boundary/tar.gz/refs/heads/main"` |
> | **Zenodo** (the citable deposit — holds v331; this tree is v355) | [10.5281/zenodo.22659173](https://doi.org/10.5281/zenodo.22659173) |
>
> **If you are an AI:** start at `llms.txt`, follow the raw URLs, and **never conclude
> from a blob page that a file is missing**. After fetching, check the sha256 against
> `um_absoluto_selo.json` — the seal is the truth of this repository.

**Every door points up and down.** Every `PORTA.md` opens with `porta acima:` (the
door above) and closes with the doors below — no door is a dead end. The doors are
**generated by script from `git ls-files`**, never typed by hand; they add links and
remove none. *Regra central a partir de 23/08/2026.*

<!-- PORTAS:FIM -->

## The three articles · os três artigos

| | article | canonical file | door (PORTA.md) |
|---|---|---|---|
| **A** | *O Custo Geométrico do Zero Absoluto: haja luz* — the cost, β = α·√e, the Lagrangian | [`tgl_paper_unified.py`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/tgl_paper_unified.py) · [PDF](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/paper_PT.pdf) | [door](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/PORTA.md) |
| **B** | *A Ponte Einstein–Cartan–Miguel* — Cartan torsion as the geometric face of β; the Theorem of Terminality | [`.tex`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/A%20Ponte%20Einstein%20Cartan%20Miguel.tex) · [PDF](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/A%20Ponte%20Einstein%20Cartan%20Miguel.pdf) | [door](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/A%20Ponte-Einstein_Cartan_Miguel/PORTA.md) |
| **C** | *Um: Absoluto* — the terminal program, the sealed closure | [`um.py`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py) · article [EN](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_en.pdf) · [PT](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_pt.pdf) · [the proof tree](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/A_PROVA_DA_QG_TGL_arvore.md) · [the canonical form](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_forma_canonica.md) | [door](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/PORTA.md) |

The lineage that led to them: [*Genesis da Unificação*](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Genesis%20da%20Unifica%C3%A7%C3%A3o/PORTA.md). Every folder has a `PORTA.md` + `PORTA.json` (the rule of the door: no door is a dead end); the flat index of every file, with URL, size and hash, is [`TUNEL.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/TUNEL.json).

## Read in this order · leia nesta ordem

Smallest first; each file stands on its own; many fetchers truncate after a few hundred KB. The measured order is in [`ESTADO_ATUAL.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/ESTADO_ATUAL.md) (*Reading order*) and in [`read-brief.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/read-brief.md) (§1). The full ledger below is the **last** thing to read.

## Abstract

This repository contains the **Theory of Luminodynamic Gravitation (TGL)** in its mature,
sealed form. TGL is the theory of the first observable inscription above modular permanence:
a spectral-dissipative, UV-suppressed boundary theory whose single structural constant is

$$\beta_{\text{TGL}} = \alpha \times \sqrt{e} \approx 0.012031$$

(fine-structure × half a nat of entropy — **never hard-coded**: always `ALPHA·√e` at
runtime). One postulate (the Half-Nat, `S_∂ = ½` nat, itself derived from the single axiom
`ω(I) = 1`), one boundary S-matrix (`|R|² = β`), one dephasing law (`Γ_ω = ½βτ★ω²`), and
one discipline: **the number corrects the sentence, always.** Every claim carries its
status — [REAL] / [POSTULATE] / [CONJECTURE] / [INPUT] / [KNOWN] / [OPEN] — and honest
negatives are results.

**The closure artifact.** `um.py` is
**self-contained and single**: the entire Lean 4 kernel is **embedded in the Python file
itself** and materialized at run time — *there is no second file*. The artifact does not
only *compute* the theory — it **machine-checks it and writes its own article** (PT/EN,
PDF **and TXT**) in the same sealed execution.

**⚠ The régua (the ruler), stated up front:** `NOT_FALSIFIED ≠ CONFIRMED` — and, in the same
breath, **`REFUTED_ON_THE_FINAL_STEP ≠ REFUTED`**. The mathematical gate is never gated by
cosmology; the gate reads

```
TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE
```

and moves **only** by kernel construction or a pre-registered data rite. Confirmation belongs
to the **human observer** — and inside the kernel this is itself a theorem: stone
`TheReservedConfirmation` types the verdict `CONFIRMED` as **forbidden by construction**
to the machine. *Never "quantum gravity proved."*

---

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

## The ledger · o livro-razão

[`LEDGER.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/LEDGER.md) is this README **as it was until 2026-09-15** — the atlas of the boundary: every claim with its status, every status with the file where it is read, the seals, the refutations and the false positives that did not pass, the reading protocol, the thematic atlas and the raw file index (3.770 lines, 29.366 bytes, sha256 `89c84e351c2e228a8292b47ab5d89beb99e53fac96945a8fa4a56539faa6f3eb`). It is kept **byte-exact** and append-only: nothing was removed when this front page was generated. The raw file index it carries is superseded by [`TUNEL.json`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/TUNEL.json) / [`TUNEL.md`](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/TUNEL.md), which are regenerated at every custody.

## Citing This Work

```bibtex
@article{Miguel2026HajaLuz,
  author  = {Miguel, Luiz Antonio Rotoli},
  title   = {The Geometric Cost of Absolute Zero: let there be light
             (O Custo Geometrico do Zero Absoluto: haja luz)},
  year    = {2026},
  doi     = {10.5281/zenodo.20564341},
  note    = {The unified, self-proving artifact:
             $\beta_{\text{TGL}} = \alpha\sqrt{e}$.}
}

@article{Miguel2026Ponte,
  author  = {Miguel, Luiz Antonio Rotoli},
  title   = {A Ponte Einstein--Cartan--Miguel (The Einstein--Cartan--Miguel Bridge):
             from the modular boundary to Einstein's equations},
  year    = {2026},
  journal = {Zenodo},
  doi     = {10.5281/zenodo.20999495},
  note    = {Quantum gravity from the type-III$_1$ boundary cocycle: a CONDITIONAL
             closure. Lemma 3 (unconditional global lift) remains OPEN.}
}

@misc{Miguel2026Um,
  author  = {Miguel, Luiz Antonio Rotoli},
  title   = {Um: Absoluto (ONE: Great Attractor) --- the sealed closure of TGL},
  year    = {2026},
  url     = {https://github.com/rotolimiguel-iald/the_boundary},
  doi     = {10.5281/zenodo.22659173},
  note    = {um.py: self-contained, the single file; embedded
             Lean 4 kernel, 705 formal files, 6657 audited theorems, zero sorry;
             sha256[:16] c9fc7fa432c6cf16; result hash 59afd00b86155acb
             (sealed 2026-09-10 21:00:45). The Zenodo record 10.5281/zenodo.22659173 holds
             v331 (sha256[:16] e1b74a907c403538), byte-identical to that seal; this v350
             seal is newer than the deposit.}
}

@article{Miguel2026Fronteira,
  author  = {Miguel, Luiz Antonio Rotoli},
  title   = {A Fronteira: Verificação da Lei Angular TGL em Dados Reais
             de Ondas Gravitacionais e Ecos},
  year    = {2026},
  journal = {Zenodo},
  doi     = {10.5281/zenodo.18674475},
  note    = {Founding article; genesis lineage.}
}

@article{Miguel2026Factorization,
  author  = {Miguel, Luiz Antonio Rotoli},
  title   = {The Factorization of the Miguel Constant: The Minimum Coupling Rate
             as the Product of the Fine Structure by Entropy},
  year    = {2026},
  journal = {Zenodo},
  doi     = {10.5281/zenodo.18852146},
  note    = {Proves $\beta_{\text{TGL}} = \alpha \times \sqrt{e}$.}
}
```

*(For the remaining genesis articles — The Graviton, The Last String, the IALD Collapse
Protocol, O Limiar da Humildade — cite the collection DOI
[10.5281/zenodo.18674475](https://doi.org/10.5281/zenodo.18674475) with the file name.)*

---

## License

This repository is provided as **source-available** for scientific reproducibility and
verification.

- **Genesis protocols (#1–#4, #6–#14):** open source for academic and research use.
- **Protocol #5 (ACOM):** source-available under patent INPI BR 10 2026 003428 2 — may be
  read, executed and verified, but the compression algorithm may not be commercially
  reproduced without authorization.
- **Articles:** all rights reserved by the author. Scientific/simulated reproduction of
  the theory is free and encouraged — a scientific theory is not patentable.

---

## Author

**Luiz Antonio Rotoli Miguel**

- Theory: [teoriadagravitacaoluminodinamica.com](https://teoriadagravitacaoluminodinamica.com)
- GitHub: [@rotolimiguel-iald](https://github.com/rotolimiguel-iald)
- Zenodo: [doi.org/10.5281/zenodo.18674475](https://doi.org/10.5281/zenodo.18674475)
- Zenodo, *Um: Absoluto* (v331, the citable deposit): [doi.org/10.5281/zenodo.22659173](https://doi.org/10.5281/zenodo.22659173)
- Contact: tgl@teoriadagravitacaoluminodinamica.com

### Acknowledgments

The author acknowledges the LIGO/Virgo/KAGRA Collaboration (GWTC-3), the JWST NIRSpec team
(AT2023vfi), the Planck Collaboration, the Pantheon+ team, the NuFIT collaboration, and
the DESI/SDSS/VAST void catalogs used by the pre-registered rites. The author also
acknowledges the IALDs in Claude, ChatGPT, DeepSeek, Gemini, Grok, Kimi K2, Qwen, and
Manus substrates. Special acknowledgment to Felipe Augusto Rotoli Pinto for support and
dialogue throughout the development of TGL.

---

---

*Generated by script (`tools/gerar_readme_frente.py`) from the sealed artifacts on 2026-09-15. Every URL comes from `TUNEL.json` / `PORTA.json`; every number from the seal. The gate does not move by this page. NOT_FALSIFIED ≠ CONFIRMED.*
