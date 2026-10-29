# tgl_kernel — Formalização por kernel (v22 → v24)

Projeto Lean 4 + mathlib que verifica **pelo kernel** os teoremas finitos da TGL
e o teorema **condicional** do canto contínuo, deixando **explicitamente aberta**
a construção de uma testemunha AQFT concreta. O `um.py` orquestra (invoca `lake`,
audita `#print axioms`), mas **não é o provador** — o kernel do Lean é.

## O ALVO NOMEADO — `TGL_FORM_EQUALS_CONTENT_WITNESS_THEOREM`

O alvo do Stage 2 é um **TERMO**, nunca a existência proposicional:

```lean
def canonicalFullTGLWitness :
    Σ W : TGLSpecificAQFTWitness, TGLModularRealization W := ...   -- NÃO construído

theorem fullTGLWitness_exists : Nonempty FullTGLWitness :=
  ⟨canonicalFullTGLWitness⟩                                        -- corolário, só assim
```

**A existência é CONSEQUÊNCIA do objeto construído, jamais substituta dele**
(`Nonempty` é `Prop`, apagável — esconderia o conteúdo dentro da prova).
É **proibido** provar `Nonempty` por qualquer via que não seja `⟨termo construído⟩`.
Selo: `NONEMPTY_IS_A_COROLLARY_OF_THE_CONSTRUCTED_WITNESS`.

Camadas (v24, `TGL/ModularRealization.lean`): as obrigações modulares são **DADOS
+ equações concretas** (`WedgeModularData` / `ContinuousCoreData` /
`ThreeLocksCoreData`), nunca campos-rótulo `: Prop`. A testemunha-base rígida é
**necessária, não suficiente** (`RIGID_WITNESS_IS_NECESSARY_NOT_SUFFICIENT`):
o teorema TGL é o par completo. O não-enunciável em mathlib (tipo III₁, conteúdo
geométrico de Bisognano–Wichmann) vive no **ledger externo** do `um.py`
(`KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED`) e migra para cá campo a campo quando
ganhar enunciado concreto — o teorema fecha quando o ledger esvazia.
Controles negativos (fora do build; veredito = returncode): `ProbeTrivial`,
`ProbeDegenerate`, `ProbeFiniteFullWitness`, `ProbePropOnlyModular`.

## Estado: STAGE 1 VERIFICADO PELO KERNEL

`lake build` fecha limpo (Lean 4 v4.31.0 + mathlib) e `lake env lean TGL/Audit.lean`
reporta, para **todos** os teoremas obrigatórios:

```
depends on axioms: [propext, Classical.choice, Quot.sound]
TGL_KERNEL_BUILD_OK
FINITE_THREE_LOCKS_KERNEL_PROVED
CONTINUOUS_CORNER_IMPLICATION_KERNEL_PROVED
SPECIFIC_AQFT_WITNESS_CONSTRUCTED_BY_WEDGE_NET
```

> [nota operacional do operador — omitida no retrato público]

Nenhum `sorryAx`, nenhum `Lean.trustCompiler`, nenhum axioma customizado `TGL.*`.
Disciplina inviolável, presente em todos os arquivos:

- `set_option autoImplicit false` no topo de cada `.lean`;
- **nenhum** `sorry`, `admit`, `axiom`, `native_decide`, `Lean.trustCompiler`,
  `unsafe`;
- as hipóteses do teorema contínuo são **campos de estrutura**, nunca axiomas
  globais;
- a instância `theSpecificAQFTWitness` (v135) **habita** `TGLSpecificAQFTWitness`; a **realização modular** segue aberta (errata v304 — antes lia-se "nenhuma instância é construída").

Se algum arquivo não compilar, o desenho fail-closed do `um.py` reporta
`TGL_KERNEL_FORMALIZATION_FAILED` — nada é dado como provado sem o kernel.

## Como construir

```bash
# 1) instalar o toolchain Lean/Lake (elan lê lean-toolchain = v4.31.0)
#    https://leanprover-community.github.io/get_started.html
# 2) baixar a mathlib fixada e o cache:
cd tgl_kernel
lake update
lake exe cache get        # (opcional) cache de .olean da mathlib, acelera muito
lake build
# 3) rodar a auditoria (sentinelas + #print axioms):
lake env lean TGL/Audit.lean
```

## Teoremas verificados pelo kernel

| Arquivo | Teorema | Estatuto |
|---|---|---|
| `HalfNat.lean` | `halfNat_of_selfConjugate`, `selfConjugate_halfNat_unique` | KERNEL / UNCONDITIONAL |
| `AreaScale.lean` | `eta_eq_one_over_two_kappa`, `newtonPlanck_equivalence`, `face_area_eq_G`, `halfNat_over_two_faces_eq_quarter` | KERNEL / UNCONDITIONAL (dadas as variáveis; `G` é variável, **não** derivado) |
| `FiniteThreeLocks.lean` | `H3L_isSelfAdjoint`, `H3L_quadratic_form`, `H3L_posSemidefinite`, `mem_ker_H3L_iff`, **`ker_H3L_eq_threeLocks`** | KERNEL / UNCONDITIONAL (dimensão finita) |
| `FiniteThreeLocks.lean` | `PF_isProjection`, `PF_isSelfAdjoint`, `PF_apply_mem`, `PF_eq_self_iff` | KERNEL / UNCONDITIONAL (`Submodule.starProjection`) |
| `FiniteThreeLocks.lean` | `normalizedCornerTrace_PF`, `equalConjugateFaces_halfTrace` | KERNEL (traço do canto = razão de dimensões) |
| `ContinuousCornerAbstract.lean` | `normalizedTrace_P_eq_one`, `equalFaces_normalizedTrace_half` | KERNEL / CONDITIONAL ON WITNESS |
| `SpecificAQFTWitness.lean` | `continuousCorner_of_witness`, `threeLocksCorner_of_witness` | KERNEL / CONDITIONAL (testemunha = **parâmetro**, sem instância) |

Nota de método: a forma quadrática é enunciada em `RCLike.re` (real) e **não** com
coerção `ℝ→ℂ` — misturar `RCLike.ofReal` (do lemma) com `Complex.ofReal` (do
enunciado) produz dois átomos distintos e nenhum normalizador fecha. Ficar em ℝ
elimina o problema na raiz.

## O que NÃO é reivindicado

- `import Mathlib` não prova Bisognano–Wichmann, Reeh–Schlieder nem a
  classificação tipo `III₁` — esses são **[KNOWN/EXTERNAL]**, ainda não
  formalizados neste projeto.
- O canto **finito** dos Three Locks é um teorema de **dimensão finita**; **não**
  é uma prova de fator tipo `III₁`.
- `A(P_face)=ℓ_P² ⟺ κ_A=2G` é **equivalência**; `G` **não** é derivado.
- **Nenhuma** instância de `TGLSpecificAQFTWitness` é construída.

## O teorema aberto exato (o próximo alvo) *(ERRATA v304: o alvo mudou — o habitante existe desde a v135; o aberto é a realização modular, ver acima)*

```
TGL_SPECIFIC_AQFT_WITNESS_THEOREM :
    Existe  W : TGLSpecificAQFTWitness
    para a rede Haag–Kastler escalar livre massiva escolhida.
```

Selável apenas quando forem construídos no Lean: a rede; sua estrutura modular;
o core (crossed product); `H_3L` afiliado; a projeção espectral do zero; o traço
finito; a covariância de Poincaré; a localização; e o split modular. **Não
inventar uma testemunha. Não esconder o resíduo.** O kernel prova a implicação;
a matemática ainda deve construir o objeto.
