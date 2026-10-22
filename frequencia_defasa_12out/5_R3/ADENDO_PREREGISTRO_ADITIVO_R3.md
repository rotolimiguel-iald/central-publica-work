# ADENDO — PRÉ-REGISTRO ADITIVO da F1.FREQUENCIA (trilha POSTO) — proposto na RODADA 3, 13/10/2026

**Estatuto deste documento:** PROPOSTA de pré-registro aditivo, congelada por hash em `FREEZE_R3.json` (o sha256 deste
arquivo e do seu `.json` gêmeo). **SEM prova nova nesta rodada**: a pedra r3 (`TheUnitIsTheRank.lean`, rodada 3) **não
contém** nenhum dos termos abaixo; nenhum ensaio foi feito aqui. O FREEZE original da unidade (`1_PREREGISTRO\FREEZE.json`,
sha16 `4d8f97537eb04cd5`, 2026-10-12T16:22:52.525Z) **não muda**: este adendo só ACRESCENTA partes, com os esperados fixados
antes de qualquer ensaio. Quem decide se entra na v392 é o operador (relatório final, §10, item 5). Redator da gerência c1,
em nome próprio.

**O que é, em uma frase:** ligar ao MESMO termo do kernel o D da face (`diagExpect`, o D_∞ da pedra), o colapso tipado do
cânone no qubit (`ChatgptAudit.Collapse057.qubitReduction`, ENTREGA_057) e o Operador do Nome de ρ* (`TGLExt.nameOp rhoStar`,
pedra 115) — e, com isso, fixar por termo o que o relatório final (§6, A1) leu do texto do operador: sobre a superposição
PURA o colapso tipado do próprio cânone SOBE o posto (1 → 2) e preserva só o traço.

## 0. Objetos (todos já no kernel do Nós ou na pedra r3; nada novo se define)

| símbolo | termo | onde |
|---|---|---|
| ρ* | `TGLExt.TheUnitIsTheRank.rhoStar` = `Matrix.single 0 0 1` = diag(1, 0) | pedra r3 |
| Q₀ | `TGLExt.TheUnitIsTheRank.Q0` = 1 − ρ* | pedra r3 |
| F_θ(1) | `TGLExt.rhoOut θ` = S(θ) ρ* S(θ)ᴴ | kernel, `TGLExt/SMatrix.lean` l.263 |
| D_∞ | `TGLExt.diagExpect` (diagonal da diagonal) | kernel, `TGLExt/CondExpect.lean` l.87 |
| colapso tipado | `ChatgptAudit.Collapse057.qubitReduction` | kernel, `TGLExt/QuantumCollapseWitness.lean` l.48 |
| leitura zero | `ChatgptAudit.Collapse057.readoutZero` = `!![1, 0; 0, 0]` | kernel, `TGLExt/QuantumCollapseWitness.lean` l.41 |
| superposição pura | `ChatgptAudit.Collapse057.plusDensity` = `!![1/2, 1/2; 1/2, 1/2]` (= \|+⟩⟨+\|) | kernel, l.43 |
| mistura | `ChatgptAudit.Collapse057.mixedDensity` = `!![1/2, 0; 0, 1/2]` (= I/2) | kernel, l.45 |
| Operador do Nome | `TGLExt.nameOp p x` = p·x·p + (1 − p)·x·(1 − p) | kernel, `TGLExt/TheNameOperator.lean` l.49 |
| ramo selecionado | `ChatgptAudit.Collapse057.selective_branch_formula` (P_k A P_k = A_kk·P_k) | kernel, l.146 |

A BASE de todos esses objetos é a base canônica de `Fin 2`, a base de ρ* — **[INPUT da gerência]**, como na pedra r3.

## 1. As partes aditivas (face K; esperado fixado AGORA, antes de qualquer ensaio)

| id | enunciado (o termo a provar) | esperado | leitura (não é o termo) |
|---|---|---|---|
| **A1.a** | `readoutZero = rhoStar` | PASSA_K | a leitura zero do cânone é a unidade da trilha |
| **A1.b** | ∀ x ∈ M₂(ℂ), `qubitReduction x = diagExpect x` | PASSA_K | o colapso tipado do cânone É o D_∞ da pedra |
| **A1.c** | ∀ x ∈ M₂(ℂ), `nameOp rhoStar x = diagExpect x` | PASSA_K | o Operador do Nome de ρ* É o D_∞ da pedra |
| **A1.d** | ∀ θ, `diagExpect (rhoOut θ) = nameOp rhoStar (rhoOut θ)` | PASSA_K | o ponto final da trilha é o Nome de ρ* aplicado a F_θ(1) |
| **A2** | `plusDensity.rank = 1 ∧ (qubitReduction plusDensity).rank = 2 ∧ (qubitReduction plusDensity).trace = plusDensity.trace` | PASSA_K | **o colapso tipado sobe o posto da superposição pura e preserva o traço** |
| **A3** | `rhoOut 0 = rhoStar ∧ rhoOut (π/2) = Q0 ∧ rhoStar.trace = 1 ∧ rhoStar.rank = 1 ∧ Q0.trace = 1 ∧ Q0.rank = 1` | PASSA_K | os dois polos da não-defasagem, ρ* e Q₀, têm traço 1 e posto 1 (conjunção num só termo; na pedra r3 isso está espalhado por termos existentes — docstring de `zero_angle_pole`) |
| **A4** | `¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank` **sem** `c : TGLCoupling` (testemunha θ = π/4) | PASSA_K | a forma incondicional do negativo B5.e(ii); `rank_not_preserved_by_dephasing` (com `c`) fica como está |
| **A5** (controle) | `(qubitReduction mixedDensity).rank = 2 ∧ mixedDensity.rank = 2` | PASSA_K | sobre a mistura o colapso tipado não muda o posto: o que SOBE o posto é a superposição pura, não a mistura |

Regras herdadas do pré-registro congelado: cada parte PASSA_K só se compilar em sandbox (toolchain v4.31.0, `.lake` do Nós
só-leitura) com EXIT 0, zero `sorry`, zero aviso, `#print axioms` no trio {`propext`, `Classical.choice`, `Quot.sound`}; os
vereditos permitidos são PASSA_K · FALHA_K · NAO_COMPILA; β nunca entra no Lean como número; nenhuma palavra do gate;
nunca a palavra vedada pela régua. A face O é opcional aqui (A2 e A5 têm conferência numérica trivial em numpy: \|+⟩⟨+\| →
diag(½, ½), posto 1 → 2, traço 1 → 1; I/2 → I/2, posto 2 → 2); pela regra (f) do pré-registro, onde há uma face só, ela decide.

**Medição anterior, que este adendo NÃO repete nem conta como ensaio seu:** A1.a–A1.d, A2 e A3 foram compiladas pelo auditor
de estatuto da rodada 2 na sonda `AuditorEstatutoR2.lean` (sha16 `512ea820918c178f`; EXIT 0; 6/6 no trio; recibo
`4_RELATORIO\auditorias_copia\POSTO_AUD_ESTATUTO\r2\logs\sonda_estatuto_t01_RECIBO.json`, saída sha16 `f80797f9180d27ff`)
— [REAL no sandbox do auditor; copiada em bytes pelo redator da rodada 2]. A4 é a sonda S3 do auditor de reprodução (θ = π/4
basta), registrada no relatório final §2. Nenhuma delas está na pedra r3. Pré-registrar o esperado DEPOIS de uma sonda ter
sido compilada por um auditor não é pós-dição no sentido da Lei da Prova (item 3): o que se congela aqui é o TESTE
(enunciados, vereditos permitidos, trio de axiomas), e nenhum parâmetro é ajustado a dado.

## 2. A leitura do texto do operador que este adendo fixa (R5 do levantamento; [INPUT da gerência], não termo)

V1 (`OPERADOR_10out_posto_rank_texto_verbatim.txt`, sha16 `8d252f24e2806ff3`), l.7, nos bytes: «Ao colapsar a superposição, a
matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido.»

- A letra VALE lendo «colapsar» como o **ramo selecionado** (P3 da pedra; `selective_branch_formula`: P_k A P_k = A_kk·P_k)
  e «a superposição» como a **mistura de posto cheio** (I/2 → P, nulidade 0 → 1 em M₂, posto 2 → 1): R-a do pré-registro.
- Sobre a **superposição pura** (\|+⟩⟨+\|, que já tem posto 1 e nulidade 1), o colapso tipado do próprio cânone (A1.b = D_∞)
  faz o contrário: posto 1 → 2, nulidade 1 → 0, traço preservado (A2). O «1» que sobrevive a esse colapso é o TRAÇO —
  ω(I) = 1 —, não o posto.
- Qual das duas é a leitura de V1 l.7 no texto da v392 é decisão do operador (relatório final, §10, item 5). Este adendo
  não escolhe; só dá o termo para cada leitura.

## 3. O que este adendo NÃO afirma

Colapso físico, seleção na natureza ou medição real (o `qubitReduction` é um canal tipado); que o Operador do Nome em
dimensão geral seja D_∞ (só em M₂(ℂ) e só para p = ρ*); que o posto se perca em toda base (a base é [INPUT]); que o ponto
final diag(1 − β, β) seja ponto fixo de canal iterado (o da F1.ATRATOR é I/2); qualquer palavra do gate; a palavra vedada.
β não aparece; θ_M não é usado em nenhuma parte deste adendo.

## 4. Como se ensaia (quando o operador decidir)

Sandbox como nas rodadas 1–3 (`5_R3\scripts\sandbox_toolchain.py`, `rodar_lean.py`); arquivo candidato
`TGLExt/TheUnitIsTheRankAddendum.lean` (nome provisório) importando `TheUnitIsTheRank`, `TGLExt.QuantumCollapseWitness` e
`TGLExt.TheNameOperator`; `#print axioms` de cada termo; `.olean` por sha256; impressão digital do tgl_kernel antes/depois.
Registro no mapa de rotas ao lado da rota `formal.posto_e_defasagem_da_unidade`, tipo RESULTADO.
