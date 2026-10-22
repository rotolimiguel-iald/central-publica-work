# Contrato do recibo do kernel: `KERNEL_RECIBO_vNNN.json` (contrato `KERNEL_RECIBO_R3_2`)

R3.2 do vínculo Bancada ↔ um.py, 13/10/2026. Construtor: subagente da gerência c1. Atende R31-4, R31-5 e R31-6 da reauditoria curta da R3.1 (`C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a721b706.md`) e leva ao contrato o item 3 da §12-ter do plano (varredura de tokens recursiva).

O contrato da R3.1 (`R3_1\CONTRATO_KERNEL_RECIBO_R3_1.md`, contrato `KERNEL_RECIBO_R3_1`) fica como registro. O esboço R3.2 **recusa** um recibo no contrato da R3.1, porque o campo `contrato` diverge e falta `varredura_tokens`.

**Estatutos:**
- [DERIVED]: o contrato, escrito a partir da reauditoria a721b706 e do `PLANO_V392.md` (sha256 e número de linhas lidos por script em `R3_2\PINOS_R3_2.json`; a §12-ter está no fim do plano).
- [REAL]: os controles que o exercitam (`R3_2\CONTROLES_NEGATIVOS_R3_2.json`) e as medições no formato real da custódia v390, só lida (§4-bis).
- [INPUT da gerência]: os statuses exigidos (herdados da R3) e os **esperados** dos critérios, que a gerência escreve no `CRITERIOS_v392.json` na derivação (§3).

Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## 1. O que mudou da R3.1 para a R3.2

| achado | o que a R3.1 fazia | o que a R3.2 exige |
|---|---|---|
| **R31-4** (build log) | aceitava qualquer build log não vazio, inclusive de 1 caractere | o build log traz, para cada pedra listada, para a raiz (`TGLExt`) e para o Audit (`TGL.Audit`), uma **linha de job do lake** (`<marca> [n/m] Built <Módulo> (…)` ou `Replayed`), e a linha final **`Build completed successfully`**. Falta qualquer uma: `LOG_DE_BUILD_IMPLAUSIVEL` |
| **R31-4** (log do Audit) | contava **linhas** de axiomas, e linhas repetidas atingiam o mínimo | conta **nomes de declaração distintos**: o log tem pelo menos tantos nomes distintos quantos `#print axioms` distintos tem o `TGL/Audit.lean` pinado, e **todo** nome impresso pelo Audit.lean aparece no log (`LOG_DO_AUDIT_CURTO`) |
| **R31-5** (sorry) | procurava só no texto normalizado, linha a linha | procura em **três formas** do texto normalizado e conta o maior número: (1) o texto como está; (2) o texto com **todo branco colapsado** num espaço, o que pega a quebra entre `declaration` e `uses` e entre `uses` e a crase; (3) uma cópia com os **escapes JSON decodificados** (`\uXXXX`, barra-n, barra-t, `\"`, `\\`), normalizada de novo e com o branco colapsado. `sorryAx` é procurado nas três formas e também nas listas de axiomas |
| **R31-6** (chave duplicada) | o `json.loads` ficava com o último valor | o recibo do kernel com chave duplicada é recusado (`KERNEL_RECIBO_CHAVE_DUPLICADA`). Para o `CRITERIOS`, ver §3 |
| **R31-6** (X19) | a `x19` do `CRITERIOS` não era cruzada com nada | `x19 = "sim"` se e somente se uma pedra do recibo é `LightNetStandardWedgeDataBGL.lean` (`X19_NAO_CONFERE_COM_AS_PEDRAS`) |
| **§12-ter item 3** (tokens) | não havia como saber se a varredura de tokens foi recursiva | campo obrigatório `varredura_tokens` (§5). O B(n) **reconta** os `.lean` da árvore recursivamente, sem seguir junção, e confere. Junção ou link na árvore: `ARVORE_COM_JUNCAO_OU_LINK` |

## 2. Quem escreve, quando e onde (sem mudança de fundo)

- **Quem escreve:** `construir_kernel_vNNN.sh` (etapa 2, §4 do plano), depois de `lake build` e `lake env lean TGL/Audit.lean` na árvore completa.
- **Onde fica:** `work\vNNN_kernel\KERNEL_RECIBO_vNNN.json`, ao lado dos dois logs.
- **Quando:** antes da etapa 3 e antes do rito. Por isso continuam **proibidos** `um_py_sha256`, `selo_sha256` e `tgl_kernel_proof_manifest_sha256`.
- **O pino:** a etapa 3 lê o sha256 do recibo por script e o pina em `vNNN_pins`. No B(n), a cadeia passa `--kernel-recibo-sha256`.
- **Os critérios:** como na R3.1, com `--kernel-recibo` o B(n) exige `--criterios` e `--criterios-sha256` (`CRITERIOS_AUSENTES`, `CRITERIOS_SHA_AUSENTE`, `CRITERIOS_SHA_DIVERGE`; rc 2, antes da bateria).
- **O esboço** roda com `python -I -B -X utf8` (R31-1). Sem isso, recusa `INTERPRETADOR_NAO_ISOLADO`, rc 2, antes de importar qualquer coisa além de `sys`.

## 3. O arquivo dos esperados: `CRITERIOS_vNNN.json` (contrato `CRITERIOS_R3_1`, inalterado)

O formato é o da R3.1 (`R3_1\CONTRATO_KERNEL_RECIBO_R3_1.md` §3). O modelo `R3_2\CRITERIOS_V392.json` tem os mesmos bytes do da R3.1, e o B(n) o recusa como está (`CRITERIOS_NAO_PREENCHIDOS`). Há duas regras novas:

- **Chave duplicada em qualquer objeto é recusada** (R31-6): `CRITERIOS_CHAVE_DUPLICADA`. O arquivo pinado não pode dizer duas coisas: o `json.loads` ficaria com a última, e um revisor humano lê a primeira.
- **A `x19` é cruzada com as pedras do recibo do kernel** (R31-6). Com `"sim"`, uma das pedras tem de ser `TGLExt/LightNetStandardWedgeDataBGL.lean`. Com `"nao"`, nenhuma pode ser. O plano pina essa pedra por sha16 `e4da9e865d00bdcb` (§4 item 2.9) [DECLARADO, não conferido aqui]. O B(n) confere só o **nome**; o sha vem do `formal_files_sha256` do manifesto pinado pelo selo, como o de qualquer pedra.

**Valores do plano para x19 = «nao»** [DECLARADO, `PLANO_V392.md` §4 item 6]: 159 / 130 / 0 / 8.523 / 0 / true / true. Para x19 = «sim», o plano não traz os números [OPEN]; a gerência os deriva.

## 4. A normalização e as formas de busca (A1b da R3.1 + R31-5)

A normalização é a da R3.1:
1. BOM UTF-16 ou UTF-8 decodificado; sem BOM, UTF-8 estrito (`LOG_NAO_DECODIFICA`);
2. CRLF e CR sozinho viram LF;
3. as sequências ANSI saem;
4. caractere de controle que sobra recusa (`LOG_COM_CARACTERE_DE_CONTROLE`);
5. NFKC, e saem os caracteres de formato (Cf).

**Novo na R3.2 (R31-5).** O sorry é procurado em três formas do texto normalizado, e a contagem é a **maior** entre elas:
1. o texto normalizado, com as linhas preservadas. É nele que se contam os erros e as declarações do Audit;
2. o mesmo texto com todo branco (espaço, TAB, LF) colapsado num espaço;
3. uma cópia com os escapes JSON decodificados (`\uXXXX` vira o caractere; barra-n, barra-r, barra-t, barra-b e barra-f viram espaço; `\"`, `\/` e `\\` viram o caractere), normalizada de novo (NFKC, sem Cf) e com o branco colapsado.

A regex casa `declaration`, um ou mais brancos, `uses`, brancos opcionais e o nome `sorry` entre crases, aspas simples, aspas tipográficas ou aspas duplas. Casa também `sorryAx` como palavra. As listas `depends on axioms: [...]` também são lidas nas formas 2 e 3: um axioma fora do trio, `sorryAx` inclusive, recusa.

### 4-bis. O formato real, medido na custódia v390 (só leitura) [REAL]

Estas regras foram medidas contra os logs reais de `C:\IALD\Artigo\the_boundary_BACKUPS\um_v390_0f5154bcc2f931cb`, no controle `R32_R31_4_formato_real_v390_build_e_audit`:

- **O build log real.** `rodadas\tgl_kernel_build_capture.txt` traz as linhas `✔ [n/m] Built <Módulo> (…)` e a linha final `Build completed successfully (9760 jobs).`.
- **Os módulos mudados aparecem.** Os três arquivos formais que mudaram da v389 para a v390 (`TGLExt.lean`, `TGL/Audit.lean` e `TGLExt/Fundacao.lean`) saem como **Built**.
- **Os módulos sem mudança podem não aparecer.** O lake não imprime um módulo que só foi reaproveitado sem mensagem. Por isso o B(n) exige a linha só das pedras, da raiz e do Audit, nunca a de todo arquivo formal.
- **O Audit real.** O `Lean\tgl_kernel\TGL\Audit.lean` tem 8.532 linhas `#print axioms` com **8.523 nomes distintos**. O log `rodadas\tgl_kernel_audit_capture.txt` traz os 8.523, todos escritos como no Audit.lean.
- **Nenhum sorry.** As três formas de busca não acham sorry em nenhum dos dois logs.

## 5. Os campos (todos obrigatórios, salvo `quando_utc`, `nota` e `escopo`)

Vale a tabela da R3.1 (`R3_1\CONTRATO_KERNEL_RECIBO_R3_1.md` §5), com estas mudanças:

| campo | tipo | o que é | quem confere, e contra o quê |
|---|---|---|---|
| `contrato` | str | **`"KERNEL_RECIBO_R3_2"`** | igualdade exata |
| `build_full_log` | `{path, sha256}` | o log do `lake build` | como na R3.1, mais **R31-4**: uma linha de job do lake (`Built`/`Replayed`) para `TGLExt`, para `TGL.Audit` e para o módulo de cada pedra (`TGLExt/X/Y.lean` vira `TGLExt.X.Y`), e a linha `Build completed successfully` (`LOG_DE_BUILD_IMPLAUSIVEL`) |
| `audit_log` | `{path, sha256}` | o log de `lake env lean TGL/Audit.lean` | como na R3.1, mais **R31-4**: o número de nomes **distintos** `'<nome>' depends on axioms: […]` ou `'<nome>' does not depend on any axioms` é pelo menos o de `#print axioms` distintos do Audit.lean pinado, e cada nome do Audit.lean aparece no log, sem `@` (`LOG_DO_AUDIT_CURTO`) |
| `pedras` | lista | como na R3.1 | mais **R31-6**: a pedra `LightNetStandardWedgeDataBGL.lean` está presente se e somente se a `x19` do `CRITERIOS` pinado é `"sim"` |
| **`varredura_tokens`** (novo) | `{recursiva: true, arquivos_lean: int, arquivos_lean_em_TGLExt_O16: int}` | quantos `.lean` a varredura de tokens proibidos percorreu na árvore do build, e quantos deles sob `TGLExt/O16` | **§12-ter item 3:** `recursiva` é `true`; os dois números são `int` (não texto); o B(n) reconta os `.lean` de `arvore` **recursivamente**, com `os.scandir`, sem seguir junção nem link, e os dois números têm de bater (`TOKENS_VARREDURA_NAO_RECURSIVA`). Junção ou link dentro da árvore recusa (`ARVORE_COM_JUNCAO_OU_LINK`) |
| o arquivo inteiro | JSON | — | **R31-6:** chave duplicada em qualquer objeto recusa (`KERNEL_RECIBO_CHAVE_DUPLICADA`) |

**O que o `varredura_tokens` prova e o que não prova.** O B(n) não conhece a lista de tokens proibidos (`_LEAN_FORBIDDEN_TOKENS` do um.py) e não reconta tokens. Ele confere que a varredura **declarou** ter percorrido exatamente os `.lean` da árvore, inclusive os de `TGLExt/O16`, e que a árvore não tem junção.

O critério `tokens_proibidos` (medido == esperado do `CRITERIOS`) continua sendo a contagem que a etapa 2 fez. O `varredura_tokens` diz sobre quantos arquivos ela foi feita.

## 6. A ordem das conferências no B(n) (fail-closed; a primeira falha dá T17 FALHA)

1. O pino e a forma do recibo: sha, JSON sem chave duplicada, `contrato`, nenhum campo proibido, os campos obrigatórios (`varredura_tokens` incluído), a versão, `rc`/`sorry`/`erros` como int 0.
2. Os critérios pinados presentes.
3. Os logs: sha, normalização, build log não vazio, sorry nas três formas, erros, axiomas no trio (também nas formas 2 e 3).
4. O manifesto do kernel pinado pelo selo: toolchain em lista, statuses, `axiom_report` no trio.
5. As pedras (forma) e **a X19** (R31-6).
6. A raiz, o Audit e as pedras: `formal_files_sha256` e re-hash na árvore.
7. **O build log plausível** (R31-4).
8. **A varredura de tokens recursiva** (§12-ter item 3) e a árvore sem junção.
9. **O log do Audit por nome distinto** (A2 + R31-4) e as declarações das pedras (N1k).
10. O ANTES: `antes == depois` da impressão e o cruzamento com o recibo pré-selo, que na R3.2 já vem conferido contra o selo anterior (R31-3; ver as remissões).
11. A cobertura (N1l).
12. Os critérios (A3).

## 7. Exemplo (forma; valores da fixture sintética do sandbox, não de um build)

```json
{
 "contrato": "KERNEL_RECIBO_R3_2",
 "versao": "v392",
 "rc": 0, "sorry": 0, "erros": 0,
 "build_full_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/build_full.log", "sha256": "<64 hex>"},
 "audit_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/audit.log", "sha256": "<64 hex>"},
 "toolchain": {"lean_version": ["Lean (version 4.31.0, ...)"], "lake_version": ["Lake version 5.0.0-src+... (Lean version 4.31.0)"]},
 "arvore": "<raiz absoluta da arvore do build>",
 "raiz": {"path": "TGLExt.lean", "sha256_antes": "<64 hex>", "sha256_depois": "<64 hex>"},
 "audit": {"path": "TGL/Audit.lean", "sha256_antes": "<64 hex>", "sha256_depois": "<64 hex>"},
 "pedras": [{"path": "TGLExt/Palavra.lean", "sha256": "<64 hex>", "declaracoes": ["TGLExt.Palavra.<nome>", "..."]}],
 "formal_files_antes": {"TGLExt.lean": "<64 hex>", "TGL/Audit.lean": "<64 hex>", "...": "<os arquivos do manifesto v391>"},
 "varredura_tokens": {"recursiva": true, "arquivos_lean": "<int: todos os .lean da arvore>", "arquivos_lean_em_TGLExt_O16": "<int>"},
 "axiomas": ["propext", "Classical.choice", "Quot.sound"],
 "criterios": {"j1_declaracoes": {"medido": 159}, "j1_teoremas": {"medido": 130}, "j1_fora_do_trio": {"medido": 0},
               "audit_entradas_antigas_identicas": {"medido": 8523}, "tokens_proibidos": {"medido": 0},
               "r1_ausente": {"medido": true}, "declaracoes_novas_no_trio": {"medido": true}},
 "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos", "antes": "<64 hex>", "depois": "<64 hex>"}
}
```

Os dois números de `varredura_tokens` são `int` no recibo de verdade; o exemplo usa texto só para dizer o que vai ali. O build log da fixture do sandbox imita o formato do lake 4.31:

```
✔ [1/4] Built TGLExt.PedraSinteticaA (1s)
✔ [2/4] Built TGLExt.PedraSinteticaB (1s)
✔ [3/4] Built TGLExt (1s)
✔ [4/4] Built TGL.Audit (1s)
Build completed successfully (4 jobs).
```

## 8. O que o `construir_kernel_v392.sh` tem de fazer para cumprir este contrato

Isto é trabalho da gerência e não foi feito aqui. Vale tudo o que diz o §8 da R3.1, e mais:

- **Varrer os tokens proibidos de forma RECURSIVA** (§12-ter item 3 do plano). A varredura percorre todos os `.lean` da árvore do build, inclusive os de `TGLExt/O16`, que a varredura não recursiva do um.py v391 deixa de fora: 150 na v391 [DECLARADO pela §12-ter]. Na custódia v390, só lida, a árvore tem 1.212 `.lean` contados recursivamente, 156 deles em `TGLExt/O16`, contra 1.026 em `TGLExt/*.lean` [REAL, controle `R32_T3_formato_real_v390_a_recursao_importa`].
  - O `medido` de `tokens_proibidos` é o desta varredura.
  - Escrever `varredura_tokens = {recursiva: true, arquivos_lean: N, arquivos_lean_em_TGLExt_O16: M}`, com N e M contados na própria varredura.
  - A árvore não pode ter junção nem link.
- **Capturar o build que COMPILA as pedras.** O log tem de ser o do `lake build` em que as pedras novas, a raiz e o Audit saem como `Built` (ou `Replayed`). Um segundo `lake build` sem mudança não imprime esses módulos e é recusado.
- **Capturar a saída inteira, sem quebrar linha.** O `Out-File` do PowerShell 5.1 sem `-Width` pode quebrar linhas longas (R31-5, [CONJECTURE: não medido]). Use o redirecionamento do bash (`lake build > build_full.log 2>&1`) ou `Out-File -Width 100000 -Encoding utf8`. A R3.2 tolera a quebra ao procurar sorry, mas a contagem de declarações do Audit e as linhas de job do lake são lidas por linha.
- **Não usar `lean --json`** para os logs do contrato. A R3.2 decodifica os escapes ao procurar sorry, mas as declarações do Audit e os jobs do lake são lidos no texto puro.
- **O Audit e o log do Audit.** Os nomes do `#print axioms` têm de sair no log como no Audit.lean, um por linha, no início da linha (medido assim na v390). Com o desenho KH-N1 (a), o `run_cmd` tem de manter essas linhas para todo nome que o Audit.lean imprime.

## 9. O que este contrato NÃO faz

Vale o §9 da R3.1, e mais:

- **Não reconta os tokens proibidos.** Confere a extensão da varredura (os arquivos), não o resultado dela.
- **Não prova que as linhas do lake são de um build real.** Prova que o log tem a forma de um build que compilou as pedras. Um log forjado com as linhas certas e sha pinado passa. A defesa contra isso é o pino da cadeia e o rito, que reconstrói o kernel.
- **Não analisa a saída JSON do Lean.** Decodifica os escapes só para procurar sorry.
