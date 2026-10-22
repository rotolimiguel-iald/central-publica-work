# Contrato do recibo do kernel: `KERNEL_RECIBO_vNNN.json` (contrato `KERNEL_RECIBO_R3_1`)

R3.1 do vínculo Bancada ↔ um.py, 13/10/2026. Construtor: subagente da gerência c1. Atende os achados A1, A1b, A2, A3, N1k, N1l e N1m da reauditoria curta da R3 (`C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a61fad96.md`).

O contrato da R3 (`R3\CONTRATO_KERNEL_RECIBO.md`, contrato `KERNEL_RECIBO_R3`) fica como registro. O esboço R3.1 **recusa** um recibo no contrato da R3 (`contrato=` diverge).

**Estatutos.**
- [DERIVED]: o contrato, escrito a partir da reauditoria a61fad96 e da §4 do `PLANO_V392.md` (sha16 `e3eecff0b602e070`).
- [REAL]: os controles que o exercitam, em `R3_1\CONTROLES_NEGATIVOS_R3_1.json`.
- [INPUT da gerência]: os statuses exigidos (herdados da R3) e os **esperados** dos critérios, que a gerência escreve no `CRITERIOS_v392.json` na derivação (§3).
- Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## 1. O que mudou da R3 para a R3.1

| achado | o que a R3 fazia | o que a R3.1 exige |
|---|---|---|
| **A1** | contava só `declaration uses 'sorry'` (aspas simples) | conta o aviso **real** do Lean 4.31, ``declaration uses `sorry` `` (crases), e também o de aspas. Medido em 13/10 nos logs do `Nós\bancada_corpus\*.log` (498 arquivos, só leitura): 9 avisos com crase, 0 com aspas [REAL]. A gerência mediu 64 com crase nos logs do Nós [DECLARADO pela gerência; não refeito aqui] |
| **A1b** | lia o log com `decode("utf-8", errors="replace")` | **normaliza** antes de contar (§4) e recusa log que não decodifica |
| **A2** | aceitava build log vazio e audit log de uma linha | build log vazio (ou só brancos) recusa; o log do Audit tem de ter pelo menos tantas linhas de axiomas quantos `#print axioms` tem o `TGL/Audit.lean` **pinado** |
| **A3** | os critérios vinham do recibo como `{esperado, medido}` | o recibo traz **só** `{medido}`; o **esperado** vem do `CRITERIOS_vNNN.json` pinado pela cadeia (§3); esperado no recibo recusa |
| **N1k** | as pedras não eram conferidas contra o `axiom_report` | cada pedra lista as suas `declaracoes`; cada uma tem entrada no `axiom_report`, linha no log do Audit e nome na fonte da pedra |
| **N1l** | o conjunto de pedras do recibo não era conferido | o recibo traz `formal_files_antes`; as pedras são **exatamente** os arquivos formais novos ou mudados do manifesto pinado pelo selo |
| **N1m** | `toolchain` em texto; o manifesto lido com `[0]` (pegava a 1ª letra de um texto) | `toolchain` como **lista não vazia de texto** nos dois lados, igual elemento a elemento |

## 2. Quem escreve, quando e onde (sem mudança de fundo)

- **Quem escreve:** `construir_kernel_vNNN.sh` (etapa 2, §4 do plano), depois de `lake build` e `lake env lean TGL/Audit.lean` na árvore completa.
- **Onde fica:** `work\vNNN_kernel\KERNEL_RECIBO_vNNN.json`, ao lado dos dois logs.
- **Quando:** antes da etapa 3 e antes do rito. Por isso são **proibidos** `um_py_sha256`, `selo_sha256` e `tgl_kernel_proof_manifest_sha256`.
- **O pino:** a etapa 3 lê o sha256 do recibo por script e o pina em `vNNN_pins`. No B(n), a cadeia passa `--kernel-recibo-sha256`.
- **Os critérios:** com `--kernel-recibo`, o B(n) R3.1 exige também `--criterios <CRITERIOS_vNNN.json>` e `--criterios-sha256 <de vNNN_pins>` (`CRITERIOS_AUSENTES`, `CRITERIOS_SHA_AUSENTE`, `CRITERIOS_SHA_DIVERGE`, rc 2, antes da bateria).

## 3. O arquivo dos esperados: `CRITERIOS_vNNN.json` (contrato `CRITERIOS_R3_1`)

O modelo é `R3_1\CRITERIOS_V392.json` (não preenchido; o B(n) o recusa como está: `CRITERIOS_NAO_PREENCHIDOS`).

| campo | tipo | regra |
|---|---|---|
| `contrato` | str | `"CRITERIOS_R3_1"` |
| `versao` | str | igual a `--versao` |
| `preenchido` | **bool** `true` | o modelo traz `false` |
| `x19` | `"sim"` ou `"nao"` | a decisão X19 do operador. O plano diz que ela muda os números J1: +1 pedra (K09), +87 bandeiras |
| `esperados` | objeto com as **sete** chaves exatas | `j1_declaracoes`, `j1_teoremas`, `j1_fora_do_trio`, `audit_entradas_antigas_identicas`, `tokens_proibidos`: **int ≥ 0**; `r1_ausente`, `declaracoes_novas_no_trio`: **bool**. Nulo, float e texto recusam |

**Quem escreve e quando** [INPUT da gerência]:
- a gerência c1, na derivação, **depois** da decisão X19 do operador e **antes** da etapa 2;
- a cópia fica em `work\cadeia_de_selo\v392\vinculo\CRITERIOS_v392.json`;
- o sha256 é pinado em `v392_pins`, por script.

**Valores do plano para x19 = «nao»** [DECLARADO, transcritos do `PLANO_V392.md` §4 item 6, l.160–169]: 159 / 130 / 0 / 8.523 / 0 / true / true. Para x19 = «sim», o plano não traz os números [OPEN]; a gerência deriva.

## 4. A normalização dos logs (A1b)

Antes de contar sorry, erros e linhas de axiomas, cada log passa por:

1. **Decodificação.** BOM UTF-16 (LE/BE) → `utf-16`; BOM UTF-8 → `utf-8-sig`; sem BOM → UTF-8 **estrito**. Falhou: `LOG_NAO_DECODIFICA`.
2. **Quebras.** CRLF e CR sozinho viram LF.
3. **ANSI.** Saem as sequências CSI (`ESC [ … final`), OSC (`ESC ] … BEL|ST`) e os escapes de dois caracteres.
4. **Controle.** Se sobra caractere de controle C0 (fora TAB, LF e CR) ou DEL, a recusa é `LOG_COM_CARACTERE_DE_CONTROLE`. É o caso do NUL de um trecho UTF-16 sem BOM no meio de um log UTF-8.
5. **Unicode.** NFKC, e saem os caracteres de formato (Cf, por exemplo o espaço de largura zero).

A contagem de sorry casa `declaration uses` seguido do nome entre crases, aspas simples, aspas tipográficas ou aspas duplas, e também `sorryAx`.

**Medido nos logs reais (só leitura):** nenhum dos 498 `*.log` do `Nós\bancada_corpus` tem BOM, CR sozinho ou caractere de controle [REAL, 13/10]. A normalização não recusa log real.

## 5. Os campos (todos obrigatórios, salvo `quando_utc`, `nota` e `escopo`)

| campo | tipo | o que é | quem confere, e contra o quê |
|---|---|---|---|
| `contrato` | str | `"KERNEL_RECIBO_R3_1"` | igualdade exata |
| `versao` | str | `"vNNN"` | igual a `--versao` |
| `rc`, `sorry`, `erros` | **int** 0 | como na R3 | `sorry` e `erros` são **recontados** nos logs normalizados (§4) |
| `build_full_log`, `audit_log` | `{path, sha256}` | os dois logs, arquivos distintos, caminho absoluto | o sha bate; o log é lido e normalizado. O build log **não pode ser vazio**. O log do Audit tem pelo menos uma linha de axiomas, e pelo menos tantas quantos `#print axioms` tem o `TGL/Audit.lean` pinado (A2: `LOG_DO_AUDIT_CURTO`) |
| `toolchain` | `{lean_version: [str…], lake_version: [str…]}` | as listas, como o manifesto do kernel as guarda | **listas não vazias** nos dois lados, iguais elemento a elemento às `lean_version`/`lake_version` do manifesto pinado pelo selo (N1m) |
| `arvore` | str (absoluto) | a raiz da árvore do build | cada arquivo abaixo é re-hasheado nela |
| `raiz` | `{path: "TGLExt.lean", sha256_antes, sha256_depois}` | como na R3 | `depois` == `formal_files_sha256` == sha na árvore; `antes` == `nos.kernel.raiz_sha256` do recibo pré-selo |
| `audit` | `{path: "TGL/Audit.lean", sha256_antes, sha256_depois}` | como na R3 | idem; o Audit.lean **pinado** dá o mínimo de linhas do log (A2) |
| `pedras` | lista não vazia de `{path: "TGLExt/<Nome>.lean", sha256, declaracoes: [str…]}` | as pedras novas ou mudadas da versão, sem repetição | sha == `formal_files_sha256[path]` == sha na árvore. **N1k:** `declaracoes` é lista não vazia, sem repetição. Cada nome tem entrada no `axiom_report` do manifesto pinado, aparece no log do Audit como `'<nome>' depends on axioms: […]` ou `'<nome>' does not depend on any axioms`, e o nome curto (o último componente) aparece na fonte da pedra |
| `formal_files_antes` | `{caminho relativo: sha256}` | o mapa `formal_files_sha256` do kernel **antes** da etapa 2 (o do manifesto pinado pelo selo anterior) | **N1l:** a impressão formal dele é igual a `nos_kernel_impressao.antes`, e portanto ao kernel anterior do recibo pré-selo. Ele traz a raiz e o Audit do ANTES. Nenhum arquivo dele some no manifesto novo. Os arquivos novos ou mudados, fora a raiz e o Audit, estão todos sob `TGLExt/*.lean` e são **exatamente** o conjunto `pedras[].path` |
| `axiomas` | lista de str | o conjunto que o Audit imprime | ⊆ trio e ⊇ os axiomas lidos no log |
| `criterios` | `{nome: {medido}}` | os sete critérios **medidos** pela etapa 2 | **só** a chave `medido` (`esperado` presente: `CRITERIO_AUTODECLARADO`). `medido == esperado` do `CRITERIOS_vNNN.json` pinado, com o mesmo tipo. Critério fora das sete chaves recusa |
| `nos_kernel_impressao` | `{definicao, antes, depois}` | como na R3 | `antes == depois`; `antes` == `nos.kernel.impressao_formal` do recibo pré-selo |

A **impressão formal** tem a mesma definição da R3: o sha256 de `json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")`.

## 6. A ordem das conferências no B(n) (fail-closed; a primeira falha dá T17 FALHA)

1. O pino do recibo e a forma: `contrato`, nenhum campo proibido, os campos obrigatórios, a versão, `rc`/`sorry`/`erros` como int 0.
2. Os critérios pinados presentes (`CRITERIOS_AUSENTES`, se `verificar_kernel_recibo` for chamada sem eles).
3. Os logs: sha, normalização, build log não vazio, sorry e erros recontados, linhas de axiomas no trio.
4. O manifesto do kernel pinado pelo selo: a toolchain em lista, os statuses, o `axiom_report` no trio.
5. A raiz, o Audit e as pedras: `formal_files_sha256` e re-hash na árvore.
6. O mínimo de linhas do log do Audit (A2) e as declarações das pedras (N1k).
7. O ANTES: `antes == depois` da impressão e o cruzamento com o recibo pré-selo. Sem recibo pré-selo, só `--sandbox` passa.
8. A cobertura (N1l): `formal_files_antes` e o diff formal.
9. Os critérios (A3).

## 7. Exemplo (forma; valores da fixture sintética do sandbox, não de um build)

```json
{
 "contrato": "KERNEL_RECIBO_R3_1",
 "versao": "v392",
 "rc": 0, "sorry": 0, "erros": 0,
 "build_full_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/build_full.log", "sha256": "<64 hex>"},
 "audit_log": {"path": "C:/IALD/Central de Patentes/work/v392_kernel/audit.log", "sha256": "<64 hex>"},
 "toolchain": {"lean_version": ["Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)"],
               "lake_version": ["Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)"]},
 "arvore": "<raiz absoluta da arvore do build>",
 "raiz": {"path": "TGLExt.lean", "sha256_antes": "<64 hex>", "sha256_depois": "<64 hex>"},
 "audit": {"path": "TGL/Audit.lean", "sha256_antes": "<64 hex>", "sha256_depois": "<64 hex>"},
 "pedras": [{"path": "TGLExt/Palavra.lean", "sha256": "<64 hex>", "declaracoes": ["TGLExt.Palavra.<nome>", "..."]}],
 "formal_files_antes": {"TGLExt.lean": "<64 hex>", "TGL/Audit.lean": "<64 hex>", "...": "<os 1.216 arquivos do manifesto v391>"},
 "axiomas": ["propext", "Classical.choice", "Quot.sound"],
 "criterios": {"j1_declaracoes": {"medido": 159}, "j1_teoremas": {"medido": 130}, "j1_fora_do_trio": {"medido": 0},
               "audit_entradas_antigas_identicas": {"medido": 8523}, "tokens_proibidos": {"medido": 0},
               "r1_ausente": {"medido": true}, "declaracoes_novas_no_trio": {"medido": true}},
 "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos", "antes": "<64 hex>", "depois": "<64 hex>"}
}
```

A toolchain do exemplo é a do manifesto do kernel v391 do Nós, lida em 13/10 [REAL]. O manifesto v391 tem 1.216 entradas em `formal_files_sha256` e 10.265 no `axiom_report` [REAL, lido em 13/10].

## 8. O que o `construir_kernel_v392.sh` tem de fazer para cumprir este contrato

Isto é trabalho da gerência e não foi feito aqui.

- **Contar sorry no formato real.** Contar ``declaration uses `sorry` `` (crases) e também o de aspas, sobre o log normalizado como no §4. A contagem de aspas simples sozinha dá 0 num log real com sorry.
- **Gravar os logs em UTF-8** (por exemplo `lake build 2>&1 | Out-File -Encoding utf8`, ou o redirecionamento do bash). UTF-16 com BOM também é aceito.
- **Tirar `formal_files_antes`** do `formal_files_sha256` do manifesto do kernel pinado pelo selo v391, com os arquivos do `Nós\tgl_kernel` re-hasheados e conferidos.
- **Listar as declarações de cada pedra** pelos nomes que o `#print axioms` imprime. Com o desenho KH-N1 (a), o `run_cmd` pode imprimir em outra forma. Nesse caso, o log do Audit tem de trazer as linhas `'<nome>' depends on axioms: […]` das declarações das pedras; o §4 item 4 do plano decide.
- **Medir os sete critérios** e escrever só o `medido`.
- **Pôr a toolchain** como as listas do manifesto: a 1ª linha de `lean --version` e de `lake --version`, cada uma numa lista de um elemento.

## 9. O que este contrato NÃO faz

- **Não autentica quem escreveu o recibo nem o `CRITERIOS`.** O pino por sha prova que é o arquivo que a cadeia pinou; não prova quem o escreveu.
- **Não recompila o kernel na Bancada**, nem reconta J1 ou as 8.523 entradas no Lean. Confere que o **medido** da etapa 2 iguala o **esperado** pinado pela gerência, e cruza o resto com o manifesto do kernel que o rito selou.
- **Não substitui o `axiom_report` do rito.** O N1k exige que as declarações nomeadas pelo recibo estejam lá. Se o recibo omitir declarações, a defesa é o critério `j1_declaracoes` (medido == esperado pinado) e o rito.
- **A fonte da pedra é conferida por nome, não por análise do Lean.** Um nome curto que aparece num comentário passa.
