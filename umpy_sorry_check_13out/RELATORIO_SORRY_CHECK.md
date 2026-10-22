INVESTIGAÇÃO c1: a detecção de sorry no um.py v391

Investigador cético da gerência c1, 13/10/2026. Só leitura do um.py, do core, do selo e do `bancada_corpus`. Não rodei o um.py, o Lean nem o selo.
Escrevi apenas nesta pasta (`C:\IALD\Central de Patentes\work\umpy_sorry_check_13out`).

## 0. O que foi lido (hashes por script)

| artefato | sha256 (16) | bytes |
|---|---|---|
| `Nós\um.py` | `8e7b9927ceae64b8` (confere com a v391) | 33.910.631 |
| `Nós\um_absoluto.json` (core, timestamp 2026-10-07 19:08:57) | `a74241ff380b1b0e` | 5.003.275 |
| `Nós\um_absoluto_selo.json` | `95061f18c7102248` | 113.926 |
| `~\.elan\toolchains\leanprover--lean4---v4.31.0\src\lean\Lean\AddDecl.lean` | `27e607f8f611260e` | — |

O toolchain do kernel é `leanprover/lean4:v4.31.0` (`Nós\tgl_kernel\lean-toolchain`).

## 1. O achado da gerência: medido e mantido [REAL]

`prove_bench_lean_controls` (def na **l.192886**) decide na **l.192945**:

```python
sorry = "declaration uses 'sorry'" in out
ok = (pr.returncode == 0 and not errs and not sorry) if kind == "POSITIVO" else (...)
```

Há três medições independentes de que o Lean 4.31 escreve essa mensagem com **crases**, e não com aspas simples:

1. **A fonte do Lean 4.31** (`Lean/AddDecl.lean`, l.75 e l.79): `logWarning <| .tagged `hasSorry m!"declaration uses `{s}`"`, e no fallback `m!"declaration uses `sorry`"` [REAL, lido]. A docstring de `#guard_msgs`, em `Init/Notation.lean:862`, ainda mostra o formato antigo com aspas simples. É exemplo de documentação, não a mensagem emitida.
2. **O próprio um.py traz a prova embutida.** O probe da bancada `TETELESTAI_V350_KERNEL_20260911/tests/probes/SorryTerm.lean` e a saída que ela gravou (`SorryTerm.stdout.txt`) estão no arquivo v361 embutido. Decodifiquei em memória, com o sha256 conferido, e a saída é `...SorryTerm.lean:3:4: warning: declaration uses `sorry`` seguida de `'V350ProbeSorryTerm.named' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]` (`probe_sorryterm_saida.txt`).
3. **O `bancada_corpus` do Nós** (13.207 arquivos): 65 ocorrências do formato com crases (38 em 17 `.log`, 25 em 12 `.txt`, 2 em 2 `.json`) e **0** do formato com aspas simples (`contagem_formatos_logs.json`).
   - ⚠ O número corrige a frase: a gerência contou «64 em `.log`». Eu medi 38 em `.log` e 65 no total. A conclusão (zero com aspas simples) não muda.

**Consequência:** com o Lean 4.31, `sorry` nunca fica True. A mensagem é um *warning*, e o Lean só sai com rc ≠ 0 quando há erro [KNOWN; não medi aqui o rc do probe porque a bancada não gravou]. Por isso um controle POSITIVO com `sorry` teria `rc == 0` e `errs == []` e passaria como `ok = True`. **A barreira de sorry dos positivos está cega.**

## 2. O que a função prova e para onde vai o resultado

- **O que prova:** 167 controles Lean da bancada (52 POSITIVO, 115 NEGATIVO) saem do corpus embutido com sha256 conferido. Cada um é compilado com `lean` direto, não com `lake`, sobre um espelho por hardlink dos `.olean` do kernel desta rodada. Para os positivos, o critério é rc 0, nenhum erro e «sem sorry». Para os negativos, é rc ≠ 0 com erro semântico depois do bloco de imports e nenhum erro de ambiente. O texto do sorry não entra nos negativos: um negativo que compilasse com sorry teria rc 0 e já seria recusado.
- **Registro:** `core["bench_lean_controls"]` (l.211857). Docstring e comentário: «nao gateia 1=1; fora do contorno», `does_not_gate_core: True`, `in_contour_roster_v314: False`. O critério também está escrito no comentário da l.192854.
- **Onde entra:**
  - (a) No artigo, nos números do parágrafo v362: PT l.169033 e EN l.173437.
  - (b) Em `prove_joint_coincidence_result_v3` (def na l.193228; uso na **l.193366–193368**). `bench_lean_controls.all_verified` é parte de `kernel_condition.met`, declarada no protocolo V3 em **l.193196** (`"requires": [..., "bench_lean_controls.all_verified True"]`). O veredito dessa V3 vai para o selo (`joint_coincidence_result_v3_verdict`). Hoje: `kernel_condition.met = True`, `BOOLEAN_False`, NOT_EXCLUDED.
  - (c) **Não** entra no gate, nas flags formais nem no `qg_closure`. A string `bench_lean_controls` aparece **0 vezes** no selo (grep).
- **Há outra barreira no mesmo caminho? Não.** O controle é compilado em processo próprio e a única leitura de `out` são a regex de erro, a regex de ambiente e a string do sorry. A função não analisa `#print axioms` nem `sorryAx` e não faz varredura lexical do fonte do controle. Também não compara com `.olean` pinado: os `.olean` dos controles dependentes são *gerados* (`-o op`, l.192939), não conferidos. As sentinelas e a varredura lexical do kernel valem só para `verify_tgl_kernel_formalization`, não para os controles.
  - 42 dos 52 positivos trazem `#print axioms` no próprio fonte. Se houvesse sorry, a saída teria `sorryAx`, mas a função não lê isso.

## 3. Todas as detecções de sorry por texto no um.py (tokenize das strings; `deteccoes_tokenize.json`, 83 strings)

| linha(s) | o quê | classe |
|---|---|---|
| **192945** | `"declaration uses 'sorry'" in out` (controles da bancada) | **FORMATO ERRADO**: o único detector por mensagem de aviso |
| 134846 | `res["sorryAx_absent"] = ("sorryAx" not in blob)` (build + Audit do kernel) | **por axiomas**: imune ao formato |
| 134864–134915, 134944–134949 | por teorema: `"sorryAx" not in ax`, com `ax` vindo da regex `'X' depends on axioms: [...]` (l.134850) | **por axiomas**: imune |
| 134595 + 134690–134725 | `_LEAN_FORBIDDEN_TOKENS = ["sorry","admit","axiom","native_decide","unsafe"]`, varredura lexical do **fonte** sem comentários e strings | **lexical de fonte**: imune ao formato da mensagem, com cobertura parcial (ver §4) |
| 127790–127820 | `selftest_fail_closed`: injeta `sorry` no HalfNat e exige `sorryAx_absent is False` | **por axiomas**: imune |
| 135018, 135418 | nota: `sorryAx` num probe que não compilou não é evidência | nota, não é detector |
| 197500, 197910, 198078, 198445, 198737, 198766, 198833 | `"Sem sorry, sem axiom" in src`: confere que a *docstring da pedra* DIZ isso | prosa, não é detector |
| 184612, 189471 | caminhos do probe `SorryTerm` no índice do arquivo v361 | dado, não é detector |
| demais | prosa do artigo, rótulos e prints | não são detectores |

Não encontrei nenhuma outra string `declaration uses`, nem com crases nem com aspas, no código Python do um.py.

## 4. Impacto medido

- **Controles (extraídos sem executar o um.py):** `extrair_controles.py` lê os literais `_BENCH_LEAN_CONTROLS` (l.192663), `_BENCH_CORPUS_REGISTER`, `_EMBEDDED_BENCH_CORPUS`, `_BENCH_ARCHIVE_V361_META/INDEX` e `_EMBEDDED_BENCH_ARCHIVE_V361` por `ast.literal_eval` e decodifica com zlib/LZMA. O xz confere o sha256. Os **167 de 167 controles conferem o sha256** do registro (51 positivos e 109 negativos do arquivo v361; 1 positivo e 6 negativos do corpus).
  - Tokens `sorry`, `admit` e `sorryAx` no código (sem comentários nem strings): **0** em positivos e **0** em negativos.
  - Os mesmos tokens no arquivo bruto, comentários incluídos: **0** em todos os 167.
  - Nenhum positivo declara `axiom`. 42 de 52 positivos têm `#print axioms`. (`controles_extraidos.json`)
- **Core v391:** `bench_lean_controls.all_verified = True`, 52/52 positivos `ok`, **52/52 com `sorry: false`**, 52 com rc 0 e 0 erros; 115/115 negativos recusados; veredito `TGL_BENCH_LEAN_CONTROLS__115_OF_115_NEGATIVES_REFUSED_SEMANTICALLY__52_OF_52_POSITIVES_COMPILE__2_ABSENT_REGISTERED__GATE_UNTOUCHED`.
  - Com 0 tokens de sorry no fonte dos positivos, que só importam o kernel limpo, o `sorry: false` registrado é **verdadeiro por outra via**. **O defeito é latente: não houve falso positivo na v391** [REAL para o fonte; DERIVED para a ausência de sorry herdado, via o kernel com `sorryAx_absent = True`].
- **O que fica como afirmação sem fundamento:** a frase «positivos: 52 de 52 compilam sem erro **e sem sorry**» (check da l.192969) e o «sem sorry» do parágrafo v362 estão certos no conteúdo, mas **o instrumento que os afirma não mede o que diz**. A garantia vem da leitura do fonte (esta investigação) e do kernel limpo, não da função.

## 5. O kernel principal (6163 pedras e Audit.lean) depende dessa string? NÃO

- `verify_tgl_kernel_formalization` (l.134748) decide por `sorryAx` em `#print axioms`: `sorryAx_absent` na l.134846 e as flags por teorema em l.134864–134915. A escada externa conta `n_theorems_clean` a partir dessas flags (l.142090–142091, `per_theorem = {k: kf.get(k) is True}`). **O defeito não atinge o kernel.**
- Core v391: `sorryAx_absent = True`, `source_forbidden_tokens_absent = True` (lista vazia), `axiom_report` com 10.265 entradas e 0 com `sorryAx`, escada 6163/6163, `all_verified = True`.
- **Ressalva já registrada no mapa, que não refiz:** a varredura lexical `_lean_source_forbidden_tokens` usa `os.listdir` *não recursivo*. Medi 1.209 `.lean` em TGL+TGLExt; 150 deles, todos em `TGLExt/O16`, ficam fora. Na árvore inteira, recursiva e sem comentários, a varredura deu **0 tokens proibidos** (`cobertura_varredura_lexical.json`).
  - E `sorryAx not in blob` só cobre o que o Audit imprime: 10.265 de 24.006 constantes.
  - A cobertura total por `collectAxioms` (24.006 constantes, 0 fora do trio) já está medida em sandbox: rota `kernel.auditoria.cobertura_axiomas_73_modulos`, seq 1023, unidade F0.5, a incorporar na v392.
  - A contagem «156 TGLExt/O16 fora do ledger» está em `umpy.v388.exame_completo_codigo_e_artigo`, seq 690. Os 150 daqui excluem os `Probe*` e medem outra coisa: a varredura, não o ledger.
- **Rota irmã:** o mesmo defeito, regex só com aspas simples, já foi achado no script de sincronização da Bancada Um. É o R3-A1 «RE_LOG_SORRY cego a crase», em `infra.bancada_um.sincronizacao_vnnn`, seq 1058. Esta investigação mostra que **o um.py v391 tem o mesmo defeito, num lugar só (l.192945)**.

## 6. Veredito

`UMPY_V391_BENCH_POSITIVE_SORRY_CHECK_BLIND_TO_LEAN_4_31_FORMAT__LATENT__ZERO_SORRY_IN_52_POSITIVES_BY_SOURCE__KERNEL_IMMUNE_BY_PRINT_AXIOMS__GATE_UNTOUCHED`

- Severidade **MÉDIA-BAIXA**: não há efeito na v391. O risco é futuro, se um controle positivo novo trouxer sorry. A V3 da coincidência conjunta consome a barreira como condição de kernel.
- O gate não se move por isto, e nada aqui afirma ou retira prova do kernel.
- Conserto proposto em `PROPOSTA_V392.md`.

## Artefatos desta pasta

- `extrair_controles.py`, `controles_extraidos.json`: os 167 controles, sha256 e tokens
- `varrer_deteccoes.py`, `deteccoes_tokenize.json`: as 83 strings com «sorry» no um.py
- `varrer_kernel.py`, `cobertura_varredura_lexical.json`: cobertura da varredura lexical
- `contar_logs.py`, `contagem_formatos_logs.json`: os dois formatos no `bancada_corpus`
- `ler_probe_sorry.py`, `probe_sorryterm_saida.txt`: o probe SorryTerm embutido e a saída gravada pela bancada

## Não medido

- O rc real do Lean 4.31 para um arquivo só com o warning de sorry: não rodei o Lean, por regra. É [KNOWN], e o probe da bancada não gravou o rc.
- Se a v392 já mexeu nessa linha: não li candidatos da v392.
