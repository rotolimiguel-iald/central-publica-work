MOTOR R2 — 13/10

# A pedra TGLExt.IALD (o motor único, nome provisório), rodada 2: as oito correções C1–C8

> **De:** construtor da rodada 2, gerência c1 (sessão `6da8f00d`), subagente. **Escrito só** em
> `work\organismo_iald_12out\6_R2_CORRECOES` e no sandbox curto `C:\t\mo2`.
> **Base:** `4_RELATORIO\O_ORGANISMO_E_A_PROVA_DISTINTIVA.md` §1.3–1.5 e §5.2 (tabela C1–C8); `3_AUD_REPRO\RELATORIO_AUD_REPRO.md`;
> `3_AUD_ESTATUTO\AUDITORIA_ESTATUTO.md`; pedra r1 `2_CONSTRUCAO\sandbox\TGLExt\IALD.lean` (sha256 `a267bc6d2aedf2fa…`);
> porte `3_AUD_REPRO\sandbox_atual\IALD_porte.lean` (`1211e76bd1d8ac35…`).
> **Estatutos:** [REAL] = compilado aqui ou medido por script · [DERIVED] · [ONTO] = leitura · [OPEN] · [INPUT] = do operador · [DECLARADO].
> **A régua:** PROVADA = validade; a confirmação recusada é a creditação; o único elo pendente da QG é β_TGL na natureza a 5σ;
> NOT_FALSIFIED nunca é a palavra proibida; o gate não se move aqui; nada foi instalado.

## 0. Em poucas linhas

1. **A pedra r2 compila** contra o kernel v391 do Nós (só leitura): EXIT 0, 0 erros, 0 `sorry`, 10 avisos (todos de deprecação
   da Mathlib, `ContinuousLinearMap.*_apply`), 38,5 s. **62 declarações, 62/62 `#print axioms` no trio**
   {propext, Classical.choice, Quot.sound}. Fonte `fonte\TGLExt\IALD.lean` sha256
   `9b0e9260b208beef05342a04cadc8a8812dca3b620dcdbc5b8fbd4dd9708d268` (43.264 B, 733 linhas). `.olean`
   `d37804a344beb186022867317fbdd8c6236c7d4984b25423692004ba1890b5e4`, **reproduzido bit a bit** numa segunda compilação
   para outro caminho. [REAL]
2. **r1 → r2** (por script, `COMPARACAO_R1_R2.json`, `TABELA_R1_R2.md`): 49 MANTIDAS (mesmo enunciado; 38 delas só com
   docstring nova), 1 RENOMEADA (`anchor_is_necessary` → `unitarity_is_not_enough`, mesmo enunciado), 1 TIPO_MUDOU
   (`motor_idempotent_under_anchor` perdeu `ha : ‖a‖ = 1`), 11 NOVAS, 0 REMOVIDAS. [REAL]
3. **Achado novo (C1)** [REAL]: a frase da auditoria de reprodução "a condição exata é a âncora fraca" vale só fora do motor
   nulo. A condição exata, provada aqui sem norma e sem unitariedade, é
   `(∀ ψ, motor(motor ψ) = motor ψ) ↔ (post a (U a) = a ∨ ∀ ψ, motor ψ = 0)`; o disjunto nulo tem peso (U = 0, a ≠ 0: sem
   âncora fraca e idempotente). Fora do motor nulo, a âncora fraca é exata.
4. **Ensaio numérico refeito** (o tipo de T2 mudou): **112/112 PASSA** (as 84 verificações r1, com rótulos corrigidos, + 28
   novas), com β de runtime. É sanidade da matemática, não veredito sobre a natureza. [REAL]
5. **Kernel intocado:** impressão digital do `tgl_kernel` antes = depois (132.088 arquivos; metadados `a15d5e02d4f22bd6…`;
   fontes `22557eadef61ef50…`). Toolchain e sobreposição copiados foram apagados do sandbox ao final. [REAL]
6. **Nada decidido do que é do operador:** U unitário por tipo (pergunta 3), o `DualScalingData` do motor (pergunta 4), o nome
   e a entrada na v392 (pergunta 6), Π_N (pergunta 2). A pedra não move o gate.

## 1. Higiene [REAL]

- **um.py v391** (sha256 `8e7b9927ceae64b8b681…`): NÃO executado. β = ALPHA_FINE_CODATA_2018 = `7.2973525693e-3`, lido dos
  bytes da linha única 5557, × √e = **0.012031300400803142** (dentro de `numerico\RESULTADO_NUMERICO_R2.json`). β não é
  literal em nenhum entregável (conferido por script, `medidas\CONFERENCIA_REGUA.json`).
- **Sandbox `C:\t\mo2`** (`scripts\montar_sandbox.py`, recibo `medidas\SANDBOX_MONTAGEM.json`):
  - `toolchain\` = cópia do elan `leanprover--lean4---v4.31.0`, 14.627 arquivos, agregado `afdb950a8e7e1ef3…` igual na origem e na cópia;
  - `ov\` = cópia verificada de `tgl_kernel\.lake\build\lib\lean`, 6.040 arquivos, agregado `34a70b881a2a2abb…` igual;
  - `src\TGLExt\` = as quatro candidatas, sha conferido ANTES da cópia.
  - Motivo da sobreposição (medido em 12/10 e repetido aqui): o lean resolve a raiz `TGLExt` na primeira pasta do LEAN_PATH
    que a contém; as candidatas não instaladas têm de morar na mesma raiz que o kernel.
  - LEAN_PATH: `ov` e depois os pacotes do `.lake` do Nós, só leitura. `-o` só dentro do sandbox. Ao final apaguei
    `toolchain\`, `ov\` e `rep\`; ficam só as fontes (`src\`, 308 KB).
- **Impressão digital do tgl_kernel** (receita da construção, `scripts\impressao_digital_kernel.py`): ANTES 09:04:35Z =
  DEPOIS, nos quatro campos (`IMPRESSAO_DIGITAL_KERNEL_ANTES.json`, `…_DEPOIS.json`).
- **Mapa de rotas:** só `consultar` (rota `formal.iald_o_motor_unico` existe, EXAMINADA_COM_DEFEITO, próximo passo "correções
  C1–C8"; 1.053 registros, cabeça `652c1b77d22c8fa3`). Nada registrado: o registro proposto está em
  `registro_mapa_F1.MOTOR_R2.json`, para a gerência.
- **Memória ACOM:** NÃO executei init nem transition. A unidade proíbe escrever na memória, e o banco grava cópia a cada operação.
  Inscrever esta etapa cabe à gerência, com a referência dela.

## 2. As candidatas re-pinadas (C7) [REAL]

| candidata | fonte sha256 (conferido antes da cópia) | `.olean` deste sandbox | `#print axioms` no arquivo |
|---|---|---|---|
| `TGLExt.Palavra` | `33184b49a8bba7e7…` | `d52ebd0943e96192…` (igual ao da construção e ao do auditor) | 7/7 no trio |
| `TGLExt.TheSingularityReadsTheAttractorAdendo1` | `433d13c223b03971…` | `8cf8b1726c588cac…` (igual) | 14/14 no trio |
| `TGLExt.TheUnitIsTheRank` **r3** | `e95775d61db38633…` (`frequencia_defasa_12out\5_R3`) | `6364ea0b0c43e512…` | 0 no arquivo (as auditorias dela estão em arquivo à parte) |
| `TGLExt.TheTimeIsNotAPost` (F1.TEMPO R2) | `4d8a82591badd010…` (`tempo_santo_12out\5_R2\1_PEDRA`) | `3e591a5b494ed315…` (igual ao do auditor) | 150 únicos lidos, 0 fora do trio |

O `.olean` de `TheTimeIsNotAPost` não se compara ao da F1.TEMPO (`b52382ec…`) porque o nome de módulo aqui é `TGLExt.TheTimeIsNotAPost`.
A r1 pinava `TheUnitIsTheRank` r2 (`3195ef8f…`) e `TheTimeHasNoRank` (`a68539d8…`): ambos saíram do sandbox desta rodada.

## 3. As oito correções, uma a uma

**C1 — a âncora.** [REAL]
- `anchor_is_necessary` → **`unitarity_is_not_enough`**: mesmo enunciado; a docstring diz que prova só isto (a fase i·1 é
  unitária e quebra a idempotência).
- NOVAS:
  - `motor_idempotent_under_weak_anchor`: a âncora fraca basta, sem norma; sonda C1 do auditor, reaproveitada;
  - `anchor_not_necessary`: U = 1 + |b⟩⟨a|; sonda A1 do auditor, reaproveitada;
  - **`motor_idempotent_iff_weak_anchor_or_null`**: a condição exata;
  - `motor_idempotent_iff_weak_anchor`: a âncora fraca é exata fora do motor nulo;
  - `null_transport_is_idempotent_without_weak_anchor`: U = 0; o disjunto nulo tem peso.
- O cabeçalho diz que a pedra NÃO exige U unitário (`U : H →L[ℂ] H`). Se U deve ser unitário por tipo é a pergunta 3 do
  operador; não decidi.
- Nota [DERIVED, não formalizado]: se U for isometria e ‖a‖ = 1, a âncora fraca equivale à forte por Cauchy–Schwarz, como o
  auditor já disse.

**C2 — H-N fora de T2.** [REAL]
- `motor_idempotent_under_anchor` agora é `(a) (U) (hU : U a = a) (r t) (ψ)`, sem `ha`.
- O enunciado r2 tem menos hipóteses, logo implica o r1. Os dois chamadores (`probe_ellTwo`, `probe_the_light`) mantêm o tipo.
- H-N fica onde pesa: T4 (`the_name_reads_one`, docstring diz isso), T5/T5′ (norma de ψ), T6′ e T11 (`ha`), e
  `unitarity_is_not_enough`.

**C3 — a Fundação.** [REAL]
- Cortado o `import TGLExt.Fundacao`.
- T7′ (`second_face_iff_leak`), com o mesmo enunciado, prova-se agora por `Real.exp_eq_one_iff` (a injetividade da exponencial
  real) + `linarith`.
- Saíram as frases "a cláusula Ágape entra por termo" e "Q15 resolvida". O cabeçalho diz: a Ágape NÃO entra (0 usos de
  `agape`, `abismo`, `DualScalingData`), a Q15 não está resolvida, e a Fundação só continua no fecho de importação de forma
  TRANSITIVA, porque `TheTimeIsNotAPost` a importa. Nenhum termo dela é usado na pedra.
- A docstring de T8 deixou de citar `the_fall_never_lands`.
- NÃO construí o `DualScalingData` (pergunta 4).

**C4 — o homônimo defasagem.** [REAL]
- O cabeçalho nomeia os quatro objetos:
  1. `IALD.dephase` = `axiomFlow (post a) (r·t)`, sobre vetores;
  2. `TGLExt.diagExpect`, `CondExpect.lean:87`;
  3. `TGLExt.IALDRhoStar.eJ`;
  4. `TGLExt.dephase`, `Ergodicity.lean:184`, que não aparece na pedra.
- Diz também que nenhum lema da pedra liga (1) a (2), (3) ou (4).
- Rótulo explícito "não é a defasagem do motor" em B8(iii), no bloco B8 e em T12. O nome inglês `dephasing_alone_does_not_keep_the_rank`
  foi mantido (C4 pede rótulo, não renome); a docstring diz que ali dephasing designa o pinching.
- A frase r1 "No motor a leitura R é estação obrigatória — por isso T3′ vale" saiu: T3′ é provado sem B8.
- Lema-ponte verdadeiro e curto: **`the_jones_pinching_is_diagExpect`** (`eJ ξ = diagExpect ξ`, `rfl`). Os objetos (2) e (3)
  são o MESMO pinching em M₂.
- Dois lemas de separação:
  - `the_motor_dephasing_is_invertible`: (1) é invertível em todo (r, t), via `TheTimeIsNotAPost.flow_isUnit`;
  - `the_pinching_kills_a_coherence`: `diagExpect E₀₁ = 0` com E₀₁ ≠ 0.
- Não há lema que ligue (1) ao pinching. Não é verdadeiro na forma de igualdade (tipos e comportamentos distintos), por isso
  não o escrevi.
- Ensaio: a face FREQ passou a se chamar PINCHING (`FREQ_rank_after_PINCHING_not_motor_D`). Acrescentei o contraste: a
  defasagem do motor, como canal ρ ↦ DρD†, guarda o posto 1 do estado puro (det D = e^{−βt(n−1)} > 0).

**C5 — [ONTO] marcado.** [REAL por grep]
- As docstrings marcam [ONTO] em:
  - EU SOU = IALD (T5, T5′);
  - santo (T9);
  - Zenão (T8, T8′, B6);
  - a singularidade (B4);
  - a leitura que cria o objeto (T6′).
- T5′ diz que é fato geral de espaço de Hilbert.
- Citações ajustadas aos bytes dos verbatins:
  - r1 citava "A singularidade é a leitura do atrator", com maiúscula, que não está nos bytes; r2 cita
    «a singularidade é a leitura do atrator», que está em `cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt`
    (`1d9dd9a65fdacf68…`);
  - r1 citava "O tempo é santo", que não está nos bytes; r2 cita só «santo»
    (`cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt`, `2c8b7b712aa9ad7f…`);
  - a cunhagem de 07/10 sobre a leitura que cria o objeto não está nos verbatins de 10–12/10, e saiu das aspas.
- Conferência por script: 2 citações na fonte, 2 nos bytes, 0 fora.

**C6 — β não atua no motor.** [REAL]
- O cabeçalho e a docstring de T1 dizem que a saída do motor não depende de r (β por nome) nem de t.
- NOVAS:
  - `the_motor_ignores_rate_and_time`: `motor a U r t ψ = motor a U r′ t′ ψ`;
  - `the_leak_is_any_rate`: sonda C2 do auditor, `rfl`.
- A docstring de `the_leak_is_beta` diz que ele é `rfl` de nome.
- A pedra é validade, não prova distintiva.

**C7 — re-pino.** [REAL] Imports e os três termos de F1.TEMPO trocados, como no porte do auditor:
- `flow_isIdempotentElem_iff`;
- `the_post_is_only_the_limit` → `the_time_is_not_a_post`;
- `no_time_matrix_fin`.

`TheUnitIsTheRank` r3 entra pelo mesmo nome de módulo. Os enunciados de B8–B11 ficaram iguais.

**C8 — o homônimo aparente.** [REAL]
- O cabeçalho diz que as pontes P1–P3 são `rfl` e desfazem um homônimo aparente: unem a forma, não o referente.
- NOVA: `post_is_not_constant`, sonda A2 do auditor, reaproveitada.
- O cabeçalho diz ainda que o organismo segue sendo uma lista auditada fora desta pedra (0 referências a `QGSolutionComplete`,
  Tetelestai, `the_whole_is_one`, `the_matrix_rule`, livro de cobranças, `agape`, `DualScalingData`).
- A pedra r1 não dizia "Q16/Q17 resolvidas" no próprio arquivo (isso estava no ESPEC e no PREREGISTRO, que não toquei). A r2
  diz o contrário de forma explícita.

**Outras correções de texto que a régua pediu:**
- `probe_the_rate` (BAIXA-11 do estatuto): o kernel prova o fato para todo c, e a habitação pelo número é de runtime.
- `probe_the_light`: o certificado não tem habitante no kernel.
- Aspas que não eram citação do operador foram retiradas (chega, quarto nome, a memória, sse).
- O cabeçalho deixou de dizer "Transporte U (unitário)".

## 4. Tabela r1 → r2 e DIFF

- `TABELA_R1_R2.md` (`d60df96c019b10cd…`): uma linha por declaração, com classe, enunciado igual, docstring mudou,
  axiomas e motivo.
- `COMPARACAO_R1_R2.json` (`a1fbdc66a390be03…`): o mesmo em máquina, com os enunciados r1 e r2 inteiros.
- `DIFF_R1_R2.diff` (`8d64c34e39a66140…`): `diff -u` r1 → r2, 360 linhas trocadas.

| r1 | r2 | classe | o que mudou no tipo |
|---|---|---|---|
| `motor_idempotent_under_anchor` | `motor_idempotent_under_anchor` | TIPO_MUDOU (C2) | sai `(ha : ‖a‖ = 1)`; o resto igual |
| `anchor_is_necessary` | `unitarity_is_not_enough` | RENOMEADA (C1) | nada (mesmo enunciado) |
| — | 11 NOVAS | NOVA | C1 ×5, C6 ×2, C4 ×3, C8 ×1 |

Todo o resto (49) mantém o enunciado byte a byte, normalizado em espaços. Nenhuma declaração foi removida.

## 5. Ensaio numérico refeito [REAL; sanidade da matemática, não veredito]

`numerico\ensaio_motor_r2.py`, montado por `scripts\montar_ensaio_r2.py` a partir do r1 com 10 substituições contadas
(`medidas\MONTAGEM_ENSAIO_R2.json`). Saída `numerico\RESULTADO_NUMERICO_R2.json` (`8bf68cf9ca45bc19…`): **112/112 PASSA**
em n = 2, 3, 6, 12. Novos, por face:
- T2 sem norma: ‖a‖ = 2,7; erro 0.
- Âncora fraca: ‖Ua − a‖ = 1; motor idempotente.
- Lado genérico da condição exata: U unitário aleatório sem âncora fraca → defeito de idempotência 1,598 (n = 2) a 0,604 (n = 3).
- Lado nulo: U = (1 − P)W e U = 0 → motor ≡ 0, idempotente, defeito da âncora fraca = 1.
- C6: saída igual para (r, t) ∈ {(0, 0), (−3, 2), (17; 0,1), (β, 10³)}.
- Contraste C4: det D(5) = e^{−5β(n−1)} (0,9416 em n = 2), e o canal DρD† mantém o posto 1.

Os valores r1 de n = 2 se repetem (T2′ = √2; T9 = 0,0118162; controle β = 0: 0,0). Os de n ≥ 3 não são bit a bit os da r1,
porque as novas sorteações consomem o mesmo gerador (semente 20261012). Os checks r1 passam todos.

## 6. O que não fiz

- Não instalei nada. Não toquei Nós, um.py, quadro, mapa, memória, túnel, Bancada, site nem git.
- Não rodei o um.py nem uma nova auditoria independente. A re-auditoria da r2 é o passo seguinte do §5.2 e deve ser feita
  por quem não construiu.
- Não corrigi o ESPEC, o PREREGISTRO, o RESULTADO_CONSTRUCAO nem o relatório ao operador. A frase "Q16/Q17 resolvidas" e a
  "EU SOU = IALD como termo" do RESULTADO §6.1 continuam lá como registro, e a correção ao lado cabe à gerência.
- Não reprovei as sondas B1–B3 do auditor (as hipóteses de T5, T7′ e B9 têm peso). Não estavam em C1–C8; continuam provadas
  no sandbox do auditor.
- Não renomeei `dephasing_alone_does_not_keep_the_rank` nem `the_motor_post_is_only_the_limit`: C4 e C7 não exigem renome.
  Se o operador quiser o nome sem o homônimo, é decisão de nome.
- Não reescrevi a declaração-sonda S2 (`probe_the_light`). Segue condicional a um `FockCertificate` sem habitante.

## 7. O que é do operador (não decidi)

1. **U unitário por tipo?** (pergunta 3 / PA-1). Hoje a pedra não exige. Se exigir, a âncora fraca vira necessária para
   ‖a‖ = 1 (Cauchy–Schwarz), e T2 pode ganhar a forma iff.
2. **O `DualScalingData` do motor** (pergunta 4 / PA-2): construir a ponte por termo ao III₁ (aí a Ágape entraria de verdade)
   ou deixar como leitura.
3. **O nome e a entrada na v392** (pergunta 6), depois da re-auditoria da r2. Se entrar, entra ao lado das pedras do rank (r3)
   e do tempo, conforme «as pedras do rank e do tempo entram na v392» [INPUT, verbatim por sha256 `78ef70e6f9868281…`].
4. **Π_N := `post a`?** (pergunta 2). A sonda `post_is_not_constant` mostra que as pontes unem a forma; o referente único é decisão.

NOT_FALSIFIED nunca é a palavra proibida. A natureza decide; a creditação é ato do observador.

## 8. Arquivos (sha256 por script)

| arquivo | sha256 (16) |
|---|---|
| `fonte\TGLExt\IALD.lean` (pedra r2) | `9b0e9260b208beef` |
| `fonte\AuditIALD_R2.lean` (62 `#print axioms`) | `f99c3475b70a7b83` |
| `olean\IALD.olean` | `d37804a344beb186` |
| `olean\TheUnitIsTheRank.olean` (r3) · `TheTimeIsNotAPost.olean` · `Palavra.olean` · `TheSingularityReadsTheAttractorAdendo1.olean` | `6364ea0b0c43e512` · `3e591a5b494ed315` · `d52ebd0943e96192` · `8cf8b1726c588cac` |
| `logs\r2_iald_final_RECIBO.json` · `_SAIDA.txt` | `dffcd52c2ab84419` · `58b320087c3351e2` |
| `logs\r2_audit_final_RECIBO.json` · `_SAIDA.txt` | `96da086a2348e327` · `8d7114613016c27f` |
| `COMPARACAO_R1_R2.json` · `DECLARACOES_R2.json` · `TABELA_R1_R2.md` · `DIFF_R1_R2.diff` | `a1fbdc66a390be03` · `e0f16a5dbf9ce118` · `d60df96c019b10cd` · `8d64c34e39a66140` |
| `numerico\ensaio_motor_r2.py` · `RESULTADO_NUMERICO_R2.json` | `8f6db62fbd3f4892` · `8bf68cf9ca45bc19` |
| `IMPRESSAO_DIGITAL_KERNEL_ANTES.json` · `_DEPOIS.json` | `a8d598072f35154c` · `c54f4a55c89abe22` |
| `medidas\SANDBOX_MONTAGEM.json` · `MONTAGEM_ENSAIO_R2.json` · `CONFERENCIA_REGUA.json` | `315a3de2468458a3` · `6cc31fc21a4476ff` · (regravado na conferência final) |

Os logs das tentativas `r2_iald_t1` (EXIT 1: `CompleteSpace` omitido no lema de invertibilidade, corrigido) e `r2_iald_t2`
(EXIT 0, antes de trocar uma palavra de comentário) ficam em `logs\` como registro. O `.olean` válido é o da rodada `final`.
