# Contrato do recibo do kernel: `KERNEL_RECIBO_vNNN.json` (contrato `KERNEL_RECIBO_R3`)

R3 do vínculo Bancada ↔ um.py, 13/10/2026. Construtor: subagente da gerência c1. Atende o achado **N1 (ALTA)** da re-auditoria da R2 (`C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a645d974.md`, §5).

**O problema.** Na R2 o T17 era autodeclarado. Um recibo com 4 campos passava:
- `versao`;
- `rc`;
- `sorry`;
- um `build_full_log_sha256` qualquer.

**O conserto.** O T17 passa a ser um vínculo entre dois artefatos:
- a **etapa 2** da cadeia (`construir_kernel_vNNN.sh`);
- o **kernel que o rito selou** (`tgl_kernel_proof_manifest.json`, pinado no selo em `sha256["tgl_kernel_proof_manifest.json"]`).

Quem confere é `sincronizar_bancada.py` R3, na função `verificar_kernel_recibo`. Ela lê o recibo por hash, sem subprocesso.

**Estatutos.**
- [DERIVED]: o contrato, escrito a partir do §5 da re-auditoria e da §4 do `PLANO_V392.md`.
- [REAL]: os controles que o exercitam, em `CONTROLES_NEGATIVOS_R3.json`.
- [INPUT da gerência]: a escolha dos `statuses` exigidos (abaixo).
- Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## 1. Quem escreve, quando e onde

- **Quem escreve:** `construir_kernel_vNNN.sh` (etapa 2, §4 do plano), depois de `lake build` e `lake env lean TGL/Audit.lean` na árvore completa.
- **Onde fica:** ao lado do log: `work\vNNN_kernel\KERNEL_RECIBO_vNNN.json`.
- **Quando:** **antes** da etapa 3 (o candidato) e **antes** do rito. Por isso o recibo **não pode** citar nada que só existe depois:
  - o sha do um.py vNNN;
  - o sha do selo;
  - o sha do `tgl_kernel_proof_manifest.json` vNNN.

  Esses três campos são **proibidos**. Se aparecerem, o T17 dá FALHA.
- **O pino:** a etapa 3 (`gerar_candidato_vNNN.py`) lê o sha256 do recibo **por script** e o pina em `vNNN_pins` junto com os demais. No elo B(n), a cadeia passa esse sha em `--kernel-recibo-sha256`.
- **Em aplicar:** a flag `--kernel-recibo-sha256` é obrigatória sempre que houver `--kernel-recibo`, inclusive em `--sandbox`. Sem ela, a recusa é `KERNEL_RECIBO_SHA_AUSENTE`.
- **Fora do sandbox:** em aplicar na fase `pos_selo`, o recibo também é obrigatório. Sem ele, a recusa é `KERNEL_RECIBO_AUSENTE`.

## 2. Os campos (todos obrigatórios, salvo `quando_utc`, `nota` e `escopo`)

| campo | tipo | o que é | quem confere, e contra o quê |
|---|---|---|---|
| `contrato` | str | `"KERNEL_RECIBO_R3"` | igualdade exata |
| `versao` | str | `"vNNN"`, a versão alvo | igual a `--versao` |
| `rc` | **int** | código de saída do `lake build` **e** do `lean TGL/Audit.lean`: 0 só se os dois forem 0 | `type(x) is int` e `== 0`. `0.0`, `False` e `"0"` são recusados |
| `sorry` | **int** | ocorrências de `declaration uses 'sorry'` e de `sorryAx` nos dois logs, **contadas por script** | o B(n) **reconta** nos logs e exige o mesmo número, que tem de ser 0 |
| `erros` | **int** | linhas de erro nos dois logs (`<arq>:<l>:<c>: error` ou linha que começa por `error:`), **contadas por script** | o B(n) reconta, exige o mesmo número, que tem de ser 0 |
| `build_full_log` | `{path, sha256}` | o log do `lake build`, em caminho absoluto | o arquivo existe, o sha bate, e ele é **lido** |
| `audit_log` | `{path, sha256}` | o log do `lake env lean TGL/Audit.lean` (as linhas `#print axioms`). Arquivo **distinto** do anterior | idem. Além disso: pelo menos uma linha `depends on axioms: [...]` ou `does not depend on any axioms`; todo axioma impresso ∈ {propext, Classical.choice, Quot.sound}; nenhum `sorryAx` |
| `toolchain` | `{lean_version, lake_version}` | a primeira linha de `lean --version` e de `lake --version` | igual a `lean_version[0]` e `lake_version[0]` do manifesto do kernel pinado pelo selo |
| `arvore` | str (absoluto) | a raiz da árvore do build (onde estão `TGLExt.lean`, `TGL/Audit.lean` e `TGLExt/*.lean`) | existe; cada arquivo abaixo é **re-hasheado** nela |
| `raiz` | `{path: "TGLExt.lean", sha256_antes, sha256_depois}` | a raiz do kernel antes da etapa 2 (bytes do Nós vigente) e depois (com os `import` novos) | **depois** == `formal_files_sha256["TGLExt.lean"]` do manifesto pinado pelo selo == sha do arquivo na árvore. **antes** == `nos.kernel.raiz_sha256` do recibo pré-selo |
| `audit` | `{path: "TGL/Audit.lean", sha256_antes, sha256_depois}` | o Audit antes e depois (com os `#print axioms` novos) | idem, com `formal_files_sha256["TGL/Audit.lean"]` e `nos.kernel.audit_sha256` |
| `pedras` | lista não vazia de `{path: "TGLExt/<Nome>.lean", sha256}` | as pedras novas da versão (8 ou 9 na v392), sem repetição | cada uma: `path` começa por `TGLExt/` e acaba em `.lean`; sha == `formal_files_sha256[path]` do manifesto pinado pelo selo == sha do arquivo na árvore |
| `axiomas` | lista de str | o conjunto de axiomas que o Audit imprime | ⊆ {propext, Classical.choice, Quot.sound} e ⊇ os axiomas lidos no `audit_log` |
| `criterios` | objeto `{nome: {esperado, medido}}` | os critérios da §4 item 6 do plano, **medidos** | o B(n) exige `medido == esperado`, com o **mesmo tipo**, para cada nome obrigatório |
| `nos_kernel_impressao` | `{definicao, antes, depois}` | a impressão digital do kernel do Nós, antes e depois da etapa 2 | `antes == depois` (o kernel do Nós não mudou), e `antes` == `nos.kernel.impressao_formal` do recibo pré-selo |

**Os critérios obrigatórios** (`KERNEL_CRITERIOS_EXIGIDOS`), com o `esperado` da v392 tirado do plano (§4, item 6):

| nome | esperado na v392 | o que mede |
|---|---|---|
| `j1_declaracoes` | 159 | declarações novas (J1) |
| `j1_teoremas` | 130 | teoremas novos (J1) |
| `j1_fora_do_trio` | 0 | declarações novas com axioma fora do trio |
| `audit_entradas_antigas_identicas` | 8523 | entradas antigas do Audit idênticas |
| `tokens_proibidos` | 0 | tokens proibidos nas fontes |
| `r1_ausente` | true | a R1 do atrator não entra |
| `declaracoes_novas_no_trio` | true | todas as declarações novas no trio |

Os números do `esperado` vêm do plano e da F_KERNEL. Como o recibo é pinado por sha, o `esperado` também fica pinado.

**A impressão formal (definição fixa).** É o sha256 do JSON canônico do mapa `formal_files_sha256 {caminho relativo: sha256}`:

```
json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
```

- **Na etapa 2:** o `construir_kernel_vNNN.sh` a calcula **antes** e **depois** do build, sobre os arquivos do `Nós\tgl_kernel` re-hasheados, e confere cada um contra o manifesto do Nós vigente.
- **No B(n):** ele a recebe do recibo pré-selo. A etapa 1 grava esse valor ao ler o manifesto do kernel da versão anterior, pinado pelo selo anterior.

## 3. O que o B(n) confere, em ordem (fail-closed; a primeira falha dá T17 FALHA e nada se grava)

1. **O pino.** O sha do recibo é igual a `--kernel-recibo-sha256`.
   - Sem a flag, só `--sandbox` passa.
   - Em `main`, a mesma conferência acontece antes da bateria (`KERNEL_RECIBO_SHA_DIVERGE`, rc 2).
2. **A forma.**
   - `contrato` certo;
   - nenhum campo proibido;
   - todos os obrigatórios presentes;
   - `versao` igual à alvo;
   - `rc`, `sorry` e `erros` como int igual a 0.
3. **Os logs, lidos.**
   - O sha de cada log confere.
   - A recontagem de `sorry` e de `erros` dá o valor declarado.
   - As linhas de axiomas do Audit estão no trio.
   - Os axiomas declarados cobrem os do log.
4. **O manifesto do kernel pinado pelo selo.** O B(n) o lê em `ler_nos`, e o sha tem de bater com o pino do selo; se não bater, a recusa é `SELO_NAO_PINA_O_MANIFESTO_DO_KERNEL_DO_DISCO`.
   - A toolchain é igual.
   - Os `statuses` exigidos estão todos `true`.
   - O `axiom_report` inteiro está no trio.
5. **A raiz, o Audit e as pedras.**
   - O sha **depois** é igual ao de `formal_files_sha256` do manifesto.
   - O sha do arquivo na árvore do build é o mesmo.
6. **O ANTES.**
   - `raiz.sha256_antes`, `audit.sha256_antes` e `nos_kernel_impressao.antes` são iguais ao kernel anterior registrado no recibo pré-selo. Esse recibo é pinado em `--recibo-pre-selo-sha256`.
   - Vale também `antes == depois` da impressão.
   - Sem recibo pré-selo, só `--sandbox` passa, e o detalhe diz «ANTES não cruzado».
7. **Os critérios.** Para cada nome obrigatório, `medido == esperado`, com o mesmo tipo.

**Os `statuses` exigidos** (`KERNEL_STATUSES_EXIGIDOS`) [INPUT da gerência, R3]:
- `lake_build_ok`, `sorryAx_absent` e `trustCompiler_absent`;
- `custom_TGL_axioms_absent` e `source_forbidden_tokens_absent`;
- `sentinels_present`;
- `all_unconditional_targets_verified` e `all_conditional_implications_verified`;
- `formal_release_ready`.

Fica de fora `unconditional_type_III1_corner_proved`. Ele é `false` no manifesto v391 [REAL, lido] e é honesto por desenho, por isso não é exigido.

## 4. Exemplo (forma; os valores são da fixture sintética do sandbox, não de um build)

```json
{
 "contrato": "KERNEL_RECIBO_R3",
 "versao": "v392",
 "rc": 0, "sorry": 0, "erros": 0,
 "build_full_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/build_full.log", "sha256": "<64 hex>"},
 "audit_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/audit.log", "sha256": "<64 hex>"},
 "toolchain": {"lean_version": "Lean (version 4.31.0, ...)", "lake_version": "Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"},
 "arvore": "<raiz absoluta da arvore do build>",
 "raiz": {"path": "TGLExt.lean", "sha256_antes": "f4ce0554...", "sha256_depois": "08c5951e..."},
 "audit": {"path": "TGL/Audit.lean", "sha256_antes": "e7826e02...", "sha256_depois": "10286d59..."},
 "pedras": [{"path": "TGLExt/Palavra.lean", "sha256": "33184b49..."}],
 "axiomas": ["propext", "Classical.choice", "Quot.sound"],
 "criterios": {"j1_declaracoes": {"esperado": 159, "medido": 159}, "j1_teoremas": {"esperado": 130, "medido": 130},
               "j1_fora_do_trio": {"esperado": 0, "medido": 0}, "audit_entradas_antigas_identicas": {"esperado": 8523, "medido": 8523},
               "tokens_proibidos": {"esperado": 0, "medido": 0}, "r1_ausente": {"esperado": true, "medido": true},
               "declaracoes_novas_no_trio": {"esperado": true, "medido": true}},
 "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos", "antes": "<64 hex>", "depois": "<64 hex>"}
}
```

Os prefixos `f4ce0554…`, `e7826e02…`, `08c5951e…`, `10286d59…` e `33184b49…` são os que o plano cita (§4, itens 1–3) [DECLARADO aqui; o recibo real traz os 64 hex lidos por script]. Os 16 hex de `f4ce0554…` e `e7826e02…` conferem com o `formal_files_sha256` do manifesto v391 do Nós (`afd57149c5b26928`) [REAL, lido em 13/10].

## 5. O que este contrato NÃO faz

- **Não autentica quem escreveu o recibo.** O pino por sha prova que é o mesmo arquivo que a etapa 3 pinou; não prova quem o escreveu. A garantia vem da ordem da cadeia e da re-hasheagem na árvore.
- **Não recompila o kernel na Bancada.** A compilação é da etapa 2 e do rito; o B(n) só lê.
- **Não confere os números J1 e 8.523 contra o Lean.** Confere que o `medido` declarado iguala o `esperado` pinado, e cruza com o manifesto do kernel que o **rito** selou: raiz, Audit, pedras, statuses e axiomas. Se a etapa 2 mentir no `medido`, o rito ainda pega o que o manifesto cobre.
- **Fica para a gerência:** escrever este contrato dentro de `construir_kernel_v392.sh`. É o item 3 do «falta para fechar» da re-auditoria, e não é ato desta R3.
