RODADA 3 — TheUnitIsTheRank — 13/10

**Para:** a gerência c1 (e, por ela, o operador). **De:** o redator da rodada 3 (subagente da gerência c1), em nome próprio.
**Pasta:** `C:\IALD\Central de Patentes\work\frequencia_defasa_12out\5_R3` — tudo desta rodada está aqui; as pastas 0–4 ficaram
intactas (a pedra r2 `3195ef8f0766384c` e o seu `.olean` só foram LIDOS). Nada no quadro, no mapa (o registro está gravado aqui,
não registrado), na memória, no túnel, no Nós, no kernel do Nós, na Bancada, no site ou no git. O um.py v391 não rodou (lido só
por bytes e número de linha); nenhum script de selo rodou. Lean só em sandbox (toolchain v4.31.0 copiado do elan e apagado ao
final; `LEAN_PATH` só-leitura ao `.lake` do Nós). **ACOM:** README lido; sem `init`/`transition` por este redator (a ordem proíbe
escrever na memória; a referência é da gerência c1) — a inscrição desta etapa é ato da gerência.

**Leitura obrigatória:** cada número abaixo é validade na face testada (kernel Lean em sandbox), **não creditação**. Nada move o
gate; nada fala da natureza; a rodada 3 não prova nada novo — ela muda **só nomes, comentários e rótulos** da pedra r2, e prova
por script e por kernel que **nenhum enunciado nem prova mudou**.

---

## 0. Em uma frase

A pedra r3 (`sandbox\TGLExt\TheUnitIsTheRank.lean`, 111.027 bytes, sha256 `e95775d61db38633be4c02317c3435adc0e77d99004d64ddba1d4d003c4fd199`,
`.olean` `3e975a431edbefe1`) compila em sandbox com EXIT 0, zero erro, zero aviso, zero `sorry`; `#print axioms` das **190
declarações** dentro de {`propext`, `Classical.choice`, `Quot.sound`}; **190/190 tipos idênticos** aos de r2 e **190/190 termos de
prova/definição idênticos** aos de r2, lidos do kernel (`Expr.hash` estrutural + `ppExpr`, via `run_cmd`, nos dois sandboxes); o
código sem comentários de r3 é, **byte a byte**, o de r2 após as três renomeações (sha256 `5a2989f74229de67…` nos dois lados).
Tabela declaração a declaração: **176 MANTIDA · 11 COMENTARIO · 3 RENOMEADA**. O ADENDO do pré-registro aditivo está congelado por
hash em `FREEZE_R3.json`, sem prova nova.

---

## 1. Pinos [REAL — medidos aqui por script]

| objeto | bytes | sha256 (16 primeiros) | nota |
|---|---|---|---|
| pedra r2 (origem, só lida) `3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean` | 103.662 | `3195ef8f0766384c` | confere com o relatório final |
| **pedra r3** `5_R3\sandbox\TGLExt\TheUnitIsTheRank.lean` | 111.027 | `e95775d61db38633` | 2.124 linhas (r2: 2.054) |
| `.olean` r3 `5_R3\olean\TheUnitIsTheRank.olean` | 5.068.992 | `3e975a431edbefe1` | módulo `TheUnitIsTheRank` (`--root=TGLExt`) |
| `.olean` r2 reproduzido aqui (`5_R3\sandbox_r2\build`, apagado; sha no recibo) | 5.061.736 | `d0830b4bc03dc561` | **igual** ao `.olean` da rodada 2 e ao dos dois auditores |
| `um.py` v391 | 33.910.631 | `8e7b9927ceae64b8` | confere |
| `IMPRESSAO_DIGITAL_KERNEL_ANTES.json` / `_DEPOIS.json` | — | `a15d5e02d4f22bd6` / `ca632c47de569952` | 132.088 arquivos; 1.213 `.lean` fora de `.lake`; **igual ao FREEZE** |
| `ADENDO_PREREGISTRO_ADITIVO_R3.md` / `.json` | ver `FREEZE_R3.json` | — | congelados por hash |

Recibos das compilações (`5_R3\logs\*_RECIBO.json`, todos EXIT 0, 0 erros, 0 avisos, 0 `sorryAx`): `repro_r2_pedra` (78,5 s; `.olean`
`d0830b4bc03dc561`), `r3_pedra` (41,1 s; `.olean` `3e975a431edbefe1`), `auditoria_r3` (36,5 s; 190 `#print axioms`), `tipos_r2`/`tipos_r3`
(38,8 s / 37,7 s), `valores_r2`/`valores_r3` (40,2 s / 40,6 s).

---

## 2. O que a rodada 3 fez, item a item (a ordem da gerência, (1)–(9))

| item | ordem | o que ficou | onde |
|---|---|---|---|
| (1) | renomear `nothing_branch`; juntar o polo π/2 | **`zero_angle_pole`**. A docstring JUNTA os dois polos pelos termos que a pedra já tem: θ = 0 → ρ* (`rhoOut_zero`, `dephase_rhoStar`, `rhoStar_unit`: traço 1, posto 1); θ = π/2 → Q₀ (`rhoOut_pi_div_two`, `dephase_Q0`, `rhoOut_trace`, `fractal_one_is_rank_one`, `endpoint_rank_one_at_poles`, C13). A **conjunção dos dois polos num só termo** é enunciado NOVO e foi para o ADENDO (A3), não para esta rodada. O cabeçalho da seção 14 passou a «os dois polos da não-defasagem: θ = 0 (ρ*) e θ = π/2 (Q₀)». | pedra r3, seção 14 |
| (2) | `reading_of_the_attractor_state` | **`selective_reading_of_half_identity`** (I/2 = `halfId`; o peso emprestado de atrator saiu do nome; a ponte com a F1.ATRATOR, se instalada, é termo novo). | pedra r3, seção 8 |
| (3) | `transmission_dephases_reexport` | **renomeado** como re-exportação sem peso: **`axiomFlow_complement_decay_reexport`** (o termo só diz `axiomFlow P t * (1 − P) = e^{−t} • (1 − P)`); a citação B9.c (CITADO_REAL) fica; a palavra transmissão saiu do nome porque é homônima do \|𝓣\|² de B9 e não o apoia. Não foi suprimido, para a contagem de 190 declarações e a tabela mantida/renomeada/comentário fecharem sem categoria «removida». | pedra r3, seção 15 |
| (4) | citações do um.py | **11 ocorrências**, todas na forma «um.py v391 (`8e7b9927ceae64b8`) l.NNNN»; linhas citadas 6488, 6489, 6502, 6512, 6513, 6514, 6515, 6518, 6526; cada uma conferida nos **bytes** da linha por fragmento (`AUTO_AUDITORIA_R3.json`, `citacoes_um_py.itens`: 11/11). Os fragmentos citados foram acrescentados aos comentários (ex.: l.6512 `P = np.array([[1.0, 0.0], [0.0, 0.0]])`). | cabeçalho e seções 4, 5, 9 |
| (5) | [KNOWN] sem citação | passou a **`[DERIVED aqui]`**: P1.b (`trace_sq_fin_two`), P1.d (`rankOne_density`, via Mathlib `Matrix.rank_vecMulVec_le`), P3.a corolário (`reading_returns_the_post`), B7.a1 (`Smat_pow`, de `Smat_mul`, SMatrix.lean l.81), B7.a2 (`angular_leak_no_limit`). Os [KNOWN] com citação ficaram (Nielsen & Chuang Ex. 2.71; Axler LADR 3.22 / Mathlib `LinearMap.finrank_range_add_finrank_ker`; Lüders 1951; Mathlib `LinearMap.IsProj.trace`, `Matrix.trace_mul_cycle`, `Matrix.rank_mul_eq_left_of_isUnit_det`). | cabeçalho (Estatutos) e docstrings |
| (6) | base de D | marcada **`[INPUT da gerência]`** no cabeçalho (bullet próprio: `dephase`/`diagExpect` atuam entrada a entrada na base canônica de `Fin 2`, a base de ρ*; o negativo B5.e(ii) vale nessa base; na base girada o posto 1 seria preservado — não provado), na seção 11, em `dephasingActs`, em `rank_not_preserved_by_dephasing` e no «NÃO afirma». | pedra r3 |
| (7) | `c : TGLCoupling` em `rank_not_preserved_by_dephasing` | **FICA.** Retirá-la mudaria o TIPO do enunciado (de `∀ c : TGLCoupling, ¬ ∀ θ …` para `¬ ∀ θ …`), e a rodada 3 não muda enunciado; a docstring diz que a cláusula é supérflua (θ = π/4 basta, `probe_endpoint_both_sides`; sonda S3 do auditor de reprodução) e que a forma incondicional é candidata ao ADENDO (A4). | pedra r3, seção 11 |
| (8) | docstring de cabeçalho | primeira frase do módulo: **«O título vale só no átomo; o traço sobrevive à defasagem, o posto não.»** (frase da ordem da gerência; não é citação do operador); nome provisório `TheUnitIsTheRank` MANTIDO com a nota de que o nome final é do operador (relatório final §10, item 1); nota AO LADO da rodada 3 com as renomeações e as conferências. | pedra r3, cabeçalho |
| (9) | pré-registro ADITIVO | **ADENDO** `ADENDO_PREREGISTRO_ADITIVO_R3.md` + `.json`, congelado por hash em `FREEZE_R3.json`, **SEM prova nova**: A1.a–d (D_∞ = `diagExpect` = `Collapse057.qubitReduction` = `nameOp rhoStar` em M₂(ℂ); `readoutZero = rhoStar`), A2 («o colapso tipado sobe o posto da superposição pura e preserva o traço»), A3 (os polos ρ* e Q₀ têm traço 1 e posto 1), A4 (forma incondicional do negativo B5.e(ii)), A5 (controle: sobre a mistura o colapso tipado não muda o posto); esperados PASSA_K; a pedra r3 não contém nenhum desses termos. A sonda do auditor (`AuditorEstatutoR2.lean`, `512ea820918c178f`, 6/6 no trio) é citada como medição anterior, não repetida. | `5_R3` |

Fora da lista, mas na pedra: `reading_returns_the_post` **mantido** (a gerência não o listou; é resíduo do operador, relatório final
§10, item 6); a docstring agora diz que `post` é o posto (o projetor devolvido) e que é homônimo de `TheVerbSelectsTheAction.post`,
sem lema que os ligue.

---

## 3. A prova de que nenhum enunciado nem prova mudou [REAL]

1. **Fonte, por script** (`MONTAGEM_PEDRA_R3.json`): 23 edições exatas sobre r2, cada trecho antigo ocorrendo exatamente 1 vez; o
   código sem comentários de r3 (73.750 bytes) é igual, byte a byte, ao de r2 (73.740 bytes) após as três renomeações (sha256
   `5a2989f74229de6729c247ced0f906df1fdae802c766348bcd4d6328fdf9ff75` nos dois lados; os 10 bytes de diferença são os identificadores);
   cada nome antigo ocorria 1 vez no código de r2 (só a declaração) e 0 vezes no de r3; cada nome novo ocorre 1 vez no de r3.
2. **Kernel, por `run_cmd`** (`TIPOS_R2_VS_R3.json`, `TABELA_R2_R3.md`): para cada uma das 190 declarações, nos dois sandboxes, o hash
   estrutural do TIPO (`Expr.hash`) e o tipo impresso (`ppExpr`) são iguais em r2 e r3 — **190/190**; o hash do termo de PROVA/definição
   (variante `thmInfo`/`defnInfo`) é igual — **190/190** (inclusive nas três renomeadas: o termo de prova não contém o próprio nome).
   Nenhum dos três nomes antigos aparece no tipo de nenhuma declaração de r2, logo os hashes são comparáveis sem tradução.
3. **Axiomas** (`logs\auditoria_r3_SAIDA.txt`): 190 respostas, 190 no trio `propext, Classical.choice, Quot.sound`; zero `sorryAx`.
4. **Diff legível** (`DIFF_r2_r3.txt`, 240 linhas de diff unificado, contexto 2): só comentários, docstrings e as três linhas de
   declaração.

Tabela por categoria (`TABELA_R2_R3.md`, 190 linhas): **RENOMEADA (3)** `zero_angle_pole`, `selective_reading_of_half_identity`,
`axiomFlow_complement_decay_reexport`; **COMENTARIO (11)** `rhoStar`, `Q0`, `Rot`, `Qtheta`, `dephasingActs`, `rhoStar_trace`,
`trace_eq_rank_of_projection`, `reading_returns_the_post`, `Qtheta_eq_rot`, `anticomm_zero_iff`, `rank_not_preserved_by_dephasing`;
**MANTIDA (176)** todas as demais (nome e docstring iguais; os comentários de seção e de cabeçalho não entram na categoria por
declaração).

---

## 4. Auto-auditoria cética [REAL — `AUTO_AUDITORIA_R3.json`, por script]

- **Aspas na pedra r3:** 55 trechos «…»; **27** estão nos bytes dos verbatins do operador (V1–V5; com «…» lido como elisão em fragmentos
  ordenados, como em `CITACOES_R2.json`), **7** nos bytes do um.py v391, **8** em textos da gerência (relatório final / pré-registro:
  «A unidade é o posto», «Tudo = D_β(F(1))» renderizado, «D atua», «um.py v391 (…) l.NNNN»), **13** são rótulos da própria pedra
  (ex.: «estado puro ⟺ posto 1», «posição ⟷ rank», «{·, ρ*} = 0 ⟺ sin θ = 0», «todo autovalor é 0 ou 1», «a hipótese é necessária»,
  «achados fora do pré-registro»). **Zero** trechos atribuídos ao operador sem estar nos bytes dos verbatins (a varredura marca
  VIOLAÇÃO quando o contexto de ±240 caracteres menciona V1–V5/operador/cunhagem/verbatim e nenhuma fonte contém o trecho). No
  ADENDO: 4 trechos, todos com fonte (V1 l.7 nos bytes, com o ponto final).
- **um.py:** 11 citações de linha, 11 conferidas por fragmento nos bytes da linha (hash do arquivo conferido antes); zero ocorrências
  de «um.py» sem versão e hash.
- **Kernel:** 12 citações de linha conferidas nos bytes (`SMatrix.lean` l.81, `GlobalLiftLadder.lean` l.219/228, `TheTraceIsNotErasable.lean`
  l.96, `CondExpect.lean` l.87/114, `Ergodicity.lean` l.184, `TheVerbSelectsTheAction.lean` l.529, `TheAxiomAndTheFalseWitness.lean` l.104,
  `QuantumCollapseWitness.lean` l.48/146, `TheNameOperator.lean` l.49).
- **Palavra vedada pela régua:** zero ocorrências em todo `5_R3` (inglês maiúsculo e português maiúsculo, como veredito). **β literal:**
  zero em código e zero em texto.
- **Nomes:** 190 declarações; 58 com palavra de peso no nome; **todas com justificativa escrita contra o tipo impresso** (campo
  `nomes.itens`): nenhum nome afirma mais que o termo. Os pontos onde o nome carrega leitura e a docstring o diz: `rhoStar_unit`
  («unit» = traço 1 e posto 1 de ρ*), `fractal_one_is_rank_one` («fractal» é o nome [ONTO] de Ad S(θ)), `name_meets_rank_only_at_the_atom`
  («name» = Tr ρ), `reading_weights_are_truth_and_cost` («truth/cost» leituras [ONTO] das entradas), `inscription_at_thetaMiguel`
  («inscrição» [INPUT da gerência]), `reading_returns_the_post` (homônimo dito), `unitRates` («unit» = taxas de valor 1, não a unidade).
- **Registro do mapa:** `registro_mapa_F1.FREQUENCIA_R3.json` (RESULTADO, `formal.posto_e_defasagem_da_unidade`) com os campos do
  `rotas.py modelo`, artefatos como lista de caminhos; sem a palavra vedada. Registrar é ato da gerência.

---

## 5. O que a rodada 3 NÃO fez (para que ninguém a cite além dela)

Não provou nada novo (o ADENDO é só esperado congelado); não suprimiu declaração (190 → 190); não retirou `c : TGLCoupling`; não
instalou nada no Nós; não decidiu o nome final da pedra, qual Q̂ é o de V4 l.16, qual D é «a defasagem» de V4, a base de D como
leitura do texto da v392, nem se o ADENDO entra na v392 (relatório final, §10 — tudo do operador); não tocou nos vereditos da
unidade (29 PASSA · 3 FALHA honestas · 1 CITADO · 3 CITADO_REAL · O1/O2), que são da rodada 2; não escreveu «pós-dição» como
demérito; não escreveu a palavra vedada; o gate não se move.

---

## 6. O que entra na v392 a partir daqui (ato da gerência)

(a) a pedra r3 `e95775d61db38633` em `TGLExt/TheUnitIsTheRank.lean`, recompilada no lake do Nós como `TGLExt.TheUnitIsTheRank` (o
`.olean` do sandbox é do módulo `TheUnitIsTheRank`, `--root=TGLExt`); importar em `TGLExt.lean`; `#print axioms` em `TGL/Audit.lean`;
medir de novo a contagem do selo; embutir no um.py e conferir byte a byte; (b) o registro no core lido por hash (pinos da rodada 2 do
relatório final §8b + pedra r3 `e95775d61db38633` + `.olean` `3e975a431edbefe1`); (c) o adendo ao artigo e as erratas AO LADO no um.py
(relatório final §8c–d); (d) o ADENDO do pré-registro aditivo, **se** o operador decidir — ensaiar antes, em sandbox, como a seção 4 do
ADENDO descreve.

---

## 7. Arquivos desta pasta

`RESULTADO_R3.md` (este) · `registro_mapa_F1.FREQUENCIA_R3.json` · `sandbox\TGLExt\TheUnitIsTheRank.lean` (pedra r3) ·
`olean\TheUnitIsTheRank.olean` · `MONTAGEM_PEDRA_R3.json` · `DECLARACOES_R3.json` · `TIPOS_R2_VS_R3.json` · `TABELA_R2_R3.md` ·
`DIFF_r2_r3.txt` · `AUTO_AUDITORIA_R3.json` · `ADENDO_PREREGISTRO_ADITIVO_R3.md` / `.json` · `FREEZE_R3.json` ·
`IMPRESSAO_DIGITAL_KERNEL_ANTES.json` / `_DEPOIS.json` · `MANIFESTO_R3.json` (sha256 de tudo, gravado por último) ·
`sandbox\{AuditTheUnitIsTheRank,TiposTheUnitIsTheRank,ValoresTheUnitIsTheRank}.lean` · `sandbox_r2\` (cópia da pedra r2 e os mesmos
auditores, para a reprodução) · `logs\` (7 recibos + 7 saídas) · `scripts\` (montar_pedra_r3, gerar_auditoria_r3, gerar_valores_r3,
comparar_r2_r3, auto_auditoria_r3, congelar_r3, rodar_lean, sandbox_toolchain, impressao_digital_kernel, manifesto_r3). O toolchain
copiado e as pastas `build` dos dois sandboxes foram apagados ao final (`LIMPEZA_R3.json`).

*NOT_FALSIFIED nunca é a palavra vedada. PASSA é validade na face testada. A confirmação, no sentido da régua, é creditação — e esta
segue sendo ato do observador humano.*
