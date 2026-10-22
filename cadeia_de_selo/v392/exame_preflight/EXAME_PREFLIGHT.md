# EXAME PREFLIGHT do candidato v392 (sha16 525ab5fcf5f41d4e)

Data: 13/10/2026, por volta de 16:15–16:45. Subagente da gerência c1, em nome próprio. Neste exame só se leu o Nós; nada foi parado nem tocado. Tudo o que está marcado [REAL] foi medido aqui por script; os scripts `t*.py` estão nesta pasta. O gate não se move.

## Veredito

**O rito atual passa no rc. Ele não morre.** O kernel sai verde, o autoteste do fail-closed passa, os 29 registros por spec selam (mais as pedras e a varredura) e o PDF compila.
**O conferidor `conferir_rito_v392.py` vai dar `tudo_bate = False`.** O motivo é que `the_iald_index` não sela por causa da própria v392, e isso reprova dois itens do bloco NAO_PODE_MUDAR.

## Base de comparação

- v391 = `Nós\um.py.bak_20261013_160923`, sha16 `8e7b9927ceae64b8`. O diff está em `diff_v391_v392.txt`.
- O núcleo e o selo da v391 foram copiados para esta pasta antes que o rito os sobrescreva.
- Tentativa 1: o núcleo da pasta `tentativa1_…`. O rc=3 dela veio só do autoteste.

## Condições novas ou alteradas que chegam ao all_verified, ao rc ou ao conferidor

| # | Onde (linha do candidato) | Condição | Exercitado com entrada real | Resultado |
|---|---|---|---|---|
| 1 | 135643 + 135723 (`verify_tgl_kernel_formalization`) e `_v392_axiom_coverage` (207519) | `axiom_coverage_v392.ok` entra no `all_verified` do kernel: a linha TOTAL tem de aparecer exatamente 1 vez, com fora_do_trio 0, 4 não lidas e decl ≥ 24975 | Captura principal do rito ATUAL (Nós, 16:13), mais as capturas restored e tampered da tentativa 1 | [REAL] principal ok=True (decl 24975, thm 19761, fora 0, lidas 24971, não lidas 4); restored ok=True; tampered ok=False (sorryAx, como deve). No blob build+audit a linha aparece 2 vezes: era o defeito da tentativa 1, e agora está corrigido. **Passa.** O `decl_minimo` 24975 é exatamente o valor medido: não há folga. |
| 2 | `selftest_fail_closed` (127830) e rc 3 em 227759 | restored: `all_verified` True; tampered: FAILED e sorryAx | Capturas `_selftest_*` da tentativa 1 (o código não mudou) | [REAL] tampered: sorryAx no blob = True. Restored: cobertura ok, e o resto do `ok` já era True na tentativa 1 (build, audit 0, sentinelas, tokens, alvos). **Passa.** |
| 3 | 135485 `_lean_source_forbidden_tokens`, agora recursiva | `source_forbidden_tokens_absent` | Kernel do Nós | [REAL] 0 hits, 1206 arquivos. **Passa.** |
| 4 | 194634–194755 `prove_bench_lean_controls` (rodapé B; `example` passa a `theorem`) | Positivo exige rc 0, nenhum erro, nenhum sorry, nenhum axioma fora do trio (descontado o `.{u}`) e a linha TGL_FOOTER_B_TOTAL. Entra no `kc.met` da conjunta V3. | **Nunca rodou no rito**: na tentativa 1 ficou NOT_RUN, porque o kernel estava vermelho. Fonte: o teste de sandbox `conserto_B\RESULTADO_B_v392.json` | [REAL no sandbox] Bex: 52/52 positivos compilam, todos com a linha total. Os únicos axiomas «fora do trio» são `Classical.choice.{u}` e `Quot.sound.{u}`, e o candidato os normaliza por `split(".{")`. **Risco baixo.** Não reexecutei os 167 controles para não disputar CPU com o rito. Se falhar, só a conjunta V3 muda, e o conferidor reprova no item «nenhum veredito mudou». |
| 5 | 225659 `pedras_v392`, `varredura_e_sorry_v392` (try) | Escada 6901 = 6901, 738 bandeiras, verbatins | Núcleo da tentativa 1 com o kf verde | [REAL] all_verified True; o veredito é igual ao do ensaio. **Passa.** |
| 6 | 225665 `_v392_rodar_registros` (29 specs, try) | Fontes por sha256, verbatins, kernel, checks e guarda P18 | Núcleo da tentativa 1 com o kf verde e cobertura ok. Os módulos da cascata do kernel vêm da v391; o external_ladder fica com 6901 | [REAL] **29/29 selam**, com veredito == ESPERADOS. As falhas da tentativa 1 eram todas cascata do kernel vermelho: kh_n1 k1–k5 (cobertura) e erratas e08b/c/f/g (gpf/qgf apagadas por `finalize_v350`). |
| 7 | Trocas ditas `estatuto_da_prova_v391` e `three_stress_tests_v387` | Selar com KERNEL_6901 | Mesmo núcleo, com o índice REAL que falha | [REAL] As duas selam: `KERNEL_6901_OF_6901_THEOREMS`, e o stress test só difere nas contagens CORE_ (que o conferidor normaliza) e no KERNEL. **Passa.** |
| 8 | Artigo PT/EN, pdflatex (rc 3 em 225697) | PDF presente | Ensaio a seco do próprio 525ab (`ensaio_a_seco_v392.json`, 16:08) com o núcleo verde | [REAL do ensaio] pdflatex [0,0] PT e EN, marcas e sumário ok. Na tentativa 1 (núcleo vermelho), os dois PDFs saíram OK. **Passa.** |
| 9 | **`prove_the_iald_index` (162179; NÃO foi tocado pela v392)** | 4 checks fail-closed | Função do candidato importada e rodada sobre o núcleo verde | **[REAL] all_verified=False → THE_IALD_INDEX_NOT_SEALED_THIS_RUN.** Detalhe abaixo. |

## O achado bloqueante (registro e conferidor; não mata o rito)

**Achado 1, `the_iald_index`.** A v392 acrescentou pedras e bandeiras e não estendeu o módulo do índice. Por isso quatro checks reprovam no núcleo verde. Nenhum deles é cascata.
1. Linha 162554, os nomes ambíguos. Há 6 novos fora de V369/V372/V375/V383: `Face`, `M`, `dephase`, `fixedSpace` (`TheSingularityReadsTheAttractorAdendo1`), `flat_metric_inverse`, `rereading_adds_nothing` (`Palavra`).
2. «acesa ⇒ nome presente»: **56 violações**. São 38 bandeiras `ext_bgl_*` (estrutura `LightNetStandardWedgeDataBGL` / `D1a3OutputBGL`: campos, `ctorIdx`, `Δ`, `σ`, `J`, `Fub`…) e 18 bandeiras `ext_vrd_*` (Verdade: `name`, `i_am`, `persists`, `projection`…). O regex do índice não acha esses referentes na fonte embutida. A lista está em `iald_index_detalhe.json`.
3. `n_ausentes` dá 39 e o check exige ==3 (são os 36 nomes acima mais as 3 dívidas nomeadas).
4. O razonete herda o item 3.

Consequência [REAL]:
- O rc não muda: o módulo é `does_not_gate_core`, e o gate (`qg_closure`) não lê o índice. Na conjunta V3 ele entra como `reported_not_required`.
- No selo, `not_sealed_this_run.formais = ["the_iald_index"]`.
- No conferidor, dois itens reprovam: «nao selados inalterados» (o esperado é `[]`) e «NENHUM veredito da v391 mudou fora da troca dita».

Gravidade: **FALHA SÓ O REGISTRO e o conferidor.**

Conserto mínimo (precisa de um candidato novo e de um rito novo; não dá para fazer com o rito rodando, porque o código está selado pelo sha do um.py):
- (a) acrescentar `_AMBIGUOS_CONJUNTO_V392` com os 6 nomes, gerado por script, ao lado dos outros na linha 162554;
- (b) fazer o índice reconhecer os 36 referentes (campos de `structure` e `ctorIdx` dos módulos BGL e Verdade), ou nomeá-los como conjunto congelado v392 com a causa dita;
- (c) depois de (b), `n_ausentes` volta a 3.

A alternativa sem novo rito é a gerência aceitar o resultado e corrigir ao lado no ESPERADOS/conferidor. Isso é uma decisão, não um conserto: o selo carregaria a dívida formal do índice.

## Riscos residuais, não bloqueantes
- O bench com o rodapé B nunca rodou dentro de um rito; o que existe é o sandbox, 52/52 (item 4).
- `decl_minimo` 24975 = o valor exato; está correto hoje.
- Uma suposição deste exame: os módulos que eram True na v391 e caíram na tentativa 1 por cascata (interface_is_light, external_ladder, bootstrap, price, uv_frontier, tetelestai_v374) voltam a True com o kernel verde. O código deles não está no diff; as falhas medidas na tentativa 1 são todas «kernel_round_green» ou bandeiras apagadas por `finalize_v350`.
