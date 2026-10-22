# EXAME FINAL ANTES DO SELO — cadeia v394 (gerência c1, modelo forte, 19/10/2026)

Objeto: `um_v394_candidato.py`, sha256 `4022ad521dc7293da17a5b03848830da093fdedcfb88445300c391e43a629297`, 38.015.246 B, relido por script. O `um.py` do Nós é a v393 `18be2ddb06c60f90`, relido. Molde: `v393_exame\EXAME_FINAL_V393.md`.

Escrevi só nesta pasta. Nada foi instalado. Nenhum rito, selo ou `lake` rodou. O Nós, o túnel, a Bancada e o sandbox foram só lidos. O único processo externo que lancei foi a sonda de ambiente do pilar (`python -c "import torch…"`), com PID próprio.

## VEREDITO: PODE_COM_CORRECOES

Há **um bloqueante**, já enviado à gerência e decidido por ela (opção a, no delta). O resto são ressalvas BAIXAS.

### O bloqueante: o h8 de `kh_n1_cobertura_v394` [REAL, simulado]

**A causa.**
- A pasta `Nós\tgl_kernel\_check_damming.lean` (226 B, de 31/08) não está no corpo embutido.
- O `sha256_directory` só exclui pelo nome o `ExtrairDeps.lean`, logo conta esse arquivo.
- O core v393 real já trazia `formal_files_sha256` com 1233 entradas, ele incluído.
- No rito v394 serão 1422 entradas. O pino h8 tem 1421 e usa `op "igual"` sobre o dict inteiro.
- O ensaio a seco e o meu `exame_pontos` passam porque materializam só o embutido.

**A prova.** `simular_arvore_do_nos.py` deu `TGL_KH_N1_COBERTURA_V394__NOT_SEALED_THIS_RUN__CHECK_h8`. O resultado está em `SIMULACAO_ARVORE_NOS_4022ad521dc7293d.json`. Tempo, quadrática, rede, cunhagens e índice seguem verdes.

**O efeito.** O conferidor daria NAO BATE em dois pontos: "registros por spec v394 SELARAM" e `not_sealed_this_run.formais == []`.

**A correção decidida (a).**
- O preparador gera o pino h8 a partir do dict da árvore simulada, com o script acima rodado sobre o candidato final.
- Depois refaz o candidato, o ensaio, os esperados e o controle negativo.
- `simular_arvore_do_nos.py` passa a ser etapa obrigatória do ensaio.
- O pino fica preso também ao `_check_damming.lean`: se alguém mexer nele antes do rito, o h8 recusa de novo, fail-closed.

**Outras checagens "igual" sobre conjuntos da árvore (pergunta da gerência).** Só o h8 [REAL, varredura AST de todos os `_SPECS` e leitura do código].
- **Specs da v392.** As checagens pa27, lc32–lc35, ag16 e x1a–x1d comparam o sha de UM arquivo. O residual não as afeta.
- **h6.** `axiom_report tamanho_igual 29025` vem do Audit, não da árvore. Muda com o módulo do delta e deve ser regenerado.
- **Índice e rede.** Leem o sha por arquivo de declaração. A simulação deu verde com o residual.
- **Varredura.** Só cobra `n > 1000`, e só sobre `TGL/` e `TGLExt/`.
- **Tokens proibidos.** A checagem é por conteúdo e passou na v393 com os mesmos residuais.
- **Conferidor.** Confere por arquivo (os 189, a raiz e o Audit). `ESPERADOS.formal_files_n` não é usado.
- **Fora do meu escopo.** O recibo do kernel do B(n) (`pos_build_kernel_v394.py`) lê o `formal_files_sha256` do manifesto real, que inclui o residual, e por isso é coerente com ele. Não o auditei.

## 1. Rito e tempo: sem estouro [REAL]

**Tempos-limite do candidato** (lidos por AST, comparados com a v393):

| chamada | limite | medido no sandbox | folga |
|---|---|---|---|
| `lake build` | 3600 s | 1386 s | 2,6× |
| Audit | 1800 s | 258 s | 7× |
| probes | 1800 s | — | — |
| motor do pilar (`_qp_engine_now`) | 900 s | — | — |
| pdflatex | 180 s | igual à v393 | — |

O `rito_v394.sh` não tem limite global (`wait`). O vigia sai em 8 h, e isso não é fatal.

**O ESTADO subestima o tempo** ("build recompilado só na 1ª", ~36 min de lake). O autoteste injeta `sorry` em `TGL/HalfNat.lean`, e o fecho reverso dele tem agora 22 módulos.
- Entram TimeGravitonScalar (207 s), TimeGravitonMatrix (218 s), Flow, Kraus, RuleQuadraticResidual e TGL.Audit (204 s).
- O caminho crítico medido é de cerca de 650 s por build do autoteste. Na v393 eram 17 módulos e cerca de 350 s.
- Lake no total: 27 min (principal) + 2 × cerca de 15 min (autoteste) ≈ 60 min.
- Rito inteiro: cerca de 1h45. A v393 levou 69 min.

**A lição v372 não se aplica.** O rito escreve exatamente 191 arquivos no Nós (189 novos, a raiz e o Audit). Os 1230 antigos são idênticos byte a byte. Desde o rito v393, nada mudou em `Nós\tgl_kernel`.

**O pilar.** A chave `75dc30bc…` tem cache íntegro, com sha conferido. O ambiente de hoje (torch 2.11.0+cu128, cuda 12.8, numpy 2.4.3, scipy 1.18.0, py 3.14.3, RTX 5090) é igual ao do cache, logo o pilar é reaproveitado. Disco: 806 GB livres.

## 2. Diff v393 → v394: só o que o ESTADO lista [REAL, `diff_v393_v394.txt`]

**O tamanho.** 41 blocos, com 61 linhas trocadas e 18.785 acrescentadas. Todos são patches declarados (K00–V03, W01–W07, C01–C10, N01–N02).

**Nós de topo.** Por AST: 35 nomeados novos, 0 removidos, 0 redefinições. Há 2 mutações de topo novas, `_V392_FONTES.update(_V394_FONTES)` e o mesmo para os verbatins, sem colisão de chave entre as versões v392, v393 e v394.

**Varredura das linhas acrescentadas.**
- 0 literal de β ou de √e.
- 1 literal de α, l.216110: o default de `v394_physical_parameters`, com o mesmo valor de `SEALED_CODATA_ALPHA`. O rito passa α explicitamente, e β é sempre α·√e em runtime. É uma ressalva BAIXA de higiene.
- 0 ocorrência da palavra proibida, em qualquer forma (também nos `.pysnip` e nas 46 falas de `insumos`).
- 0 atribuição ao gate.

**O gate não se move.** Recomputei o gate com o kf novo e o feed V11 da v393: o veredito é idêntico, 18 de 18, com as bandeiras iguais. Os registros v394 não mexem em nenhuma chave existente. No selo, `qg_closure_verdict` é igual.

**Os 10 nós que diferem do r8.** Conferi com uma AST independente (`COMPARACAO_R8_EXAME.json`). Todos estão justificados:
- k5 e h5 corrigidos (o r8 ainda tem `== 4`);
- os registros v394 separados em listas `_V394`;
- `baseline_candidate` = v393 selada;
- o `try`/AVISO no `main` e `registros_v394` no selo;
- a seção do artigo e a linha do `.md`.

Há um sexto ponto, mais conservador que o r8: o derivado mantém o `veredito_sufixo` da v393, que o r8 alterava.

## 3. Erratas k5 (v392) e h2/h3/h5 (v393): legítimas, sem mascarar [REAL]

Os pisos (`<= 4`, `>=`) não escondem regressão. Os valores exatos são cobrados por `kh_n1_cobertura_v394`:
- h2 = 29025 e h3 = 23068;
- h5 = 0 nomes não lidos;
- h6 = 29025;
- h8 = árvore exata;
- h12 = proveniência.

A própria cobertura (`ok`) exige `lidas == decl`, ausência de conflito e 0 não lidas. O conferidor exige decl == 29025, não lidas == 0 e `len(axiom_report) == 29025`.

Os vereditos de `kh_n1_cobertura_v392` e `v393` saem iguais aos da v393, e as erratas estão assinadas por c1, 19/10. A troca não é veredito, e por isso não está na `troca_dita`. Ela está declarada no ESTADO e nas erratas dos specs.

## 4. Política de bandeiras: 3707 é coerente com a escada; a descrição do ESTADO está errada [REAL]

**A escada.** 7045 + 3707 = 10752, e medi 10752/10752. Com o kf da v393, a escada dá 7045 de 10752 e não fecha.

**As bandeiras.** As 3707 são as do contrato do Codex (108 + 18 + 3581) e NÃO são "teoremas e declarações nomeadas":
- 2245 são nomeadas;
- 1462 são auxiliares geradas pelo compilador: 1345 `_proof_N`/`_simp_N_N`/`match_N`/`_sunfold`, 91 `eq_N` e 26 `congr_simp`.

**As 141 públicas sem bandeira.** São 41 nomeadas (por exemplo `TimeGravitonFlow.flow`, `generator`, `RuleQuadraticResidual.residual` e `anchor`), 79 auxiliares, 20 `eq_N` e 1 `congr_simp`. Todas estão no trio e cobertas pelo KH-N1. Há ainda 16 privadas.

**A prática anterior.** A v392 (738 de 969) e a v393 (144 de 186) não marcavam nenhuma auxiliar. Seguindo essa prática, seriam 2286 bandeiras e a escada daria 9331.

**O token "THEOREMS".** Os módulos novos têm 3864 declarações e 3167 teoremas, logo pelo menos 540 das 3707 bandeiras não são teoremas. Mesmo assim, o token de `estatuto_da_prova_v391` diz "10752 … THEOREMS".

**Recomendação BAIXA.** Manter 3707 na v394: é decisão reversível, e nenhum registro novo depende das bandeiras, porque leem o `axiom_report`. Mas o ESTADO §2.2 e §4.3 e o texto novo devem dizer "bandeiras (declarações)", não "teoremas".

## 5. Músculo: tudo é consumido pelo próprio registro; nada alimenta o gate, por desenho [REAL, código lido]

| módulos | registro que consome | o que o veredito exige |
|---|---|---|
| TimeGraviton×4 (108) | `tempo_frequencia_v394` | 108 no `axiom_report` dentro do trio, 4 sha de fonte, escada exata, `kf.all_verified` e as falas. Roda o consumidor numérico: 5716 checagens, 0 falhas, medido aqui; as "14 recusas" são [DECLARADO] pelo Codex. É uma reimplementação sintética do M2/GKLS em Python, sem extração do Lean. |
| RuleQuadraticResidual (18) | `regra_quadratica_v394` | O mesmo padrão, mais `v394_quadratic_checks` (274 checagens, 0 falhas, medido aqui). Exige o tempo verde. |
| F1Fecho394 (184 módulos, 3581 declarações) | `rede_fock_v394` | Só presença, trio, proveniência por declaração, sha das 184 fontes, escada exata, rc 0 e a quadrática verde. Não há uso numérico ou estrutural (`whole_certificate_inhabited=False`). |
| NetworkProofAuditR3/R7/R8 | o próprio `lake build` | Sem declarações: são guardas de compilação (`throwError` se um axioma sai do trio). Nenhum Python lê `BUNDLE_DECL`. |

`cunhagens_v394` lê os três vereditos acima.

Os vizinhos `estatuto_v391`, `pedras_v392`, `pedras_v393` e `three_stress_v387` só levam a contagem da escada.

## 6. Pontos de chamada reais: nenhum dá False [REAL, `exame_pontos_v394.py` → `EXAME_PONTOS_4022ad521dc7293d.json`]

**verify, com os logs crus do sandbox.**
- Veredito `STAGE1_VERIFIED`, `all_verified` True.
- Cobertura 29025/23068/0, com 0 não lidas. Proveniência 29025 == 29025.
- Bandeiras: 10789 `ext_` True, das quais 3707 novas, e 10827 `_LEAN_THEOREM_FLAGS` True. Nenhuma bandeira True da v393 caiu. Os qgc/qgp/qgf são iguais.
- Os 25157 nomes antigos têm listas idênticas.

**Controles negativos.**
- O Audit com o build junto recusa.
- Um axioma fora do trio plantado nos dois logs derruba a bandeira, a cobertura e o `all_verified`.

**Escada.** 10752/10752.

**Índice da IALD.** `QUALIFIED…VERIFIED`, `all_verified` True.

**Vizinhos recomputados.** v385, v386, v387, v388, v389, v390, v391, v392 e os 29 specs da v392 estão verdes. Só mudam os 5 da troca dita (só números) e o índice (mudança declarada).

**Bloco do `main`** (v393 → v394, executado como está no candidato).
- 10 chaves recriadas ou novas, todas verdes, nenhum AVISO.
- 0 chaves existentes mexidas.

**Selo.** Mudam 9 chaves, todas declaradas. Entram 4 novas. `qg_closure_verdict` é igual.

**Guarda de veredito proibido.** Lida do `main`, morde no controle, não acha nenhum veredito proibido e é idêntica à da v393.

**Sem efeito colateral.** Nenhum arquivo foi escrito fora da pasta do exame, salvo um temporário do sistema criado e apagado pela própria `regra_v393`.

**Ressalvas BAIXAS.**
- O `all_verified` do kf não depende da proveniência: tirar uma linha `TGL_DECL_SOURCE` dá proveniência False com kf True. A proveniência é cobrada pelo índice, por h12, pela rede e pelo conferidor.
- O `RuntimeWarning` de overflow que aparece no stdout vem do teste deliberado `refuse_overflow` (l.216583).

## 7. instalar / rito / reverter, linha a linha contra a v393 [REAL]

**rito.** Muda só nos rótulos, no PK, na lista de guardas (v393, v394) e num comentário de tempo. Não há marcador `.servidor_parado` nem `.pid` velho.

**instalar.** Faz backup de BYTES dos 8 arquivos com releitura. Copia o pilar com o sha conferido. Grava em temporário, confere e faz `os.replace`. Confere a presença das 3 pedras da v393 e a ausência dos 189 novos.

**reverter.** Confere todos os backups ANTES de escrever. Restaura os 8 arquivos, põe os 189 em quarentena com o caminho relativo e usa a âncora `ESPERADOS_v393` (sem digitar o hash). Cobre tudo o que o instalar grava.

**BAIXA, como no molde.** Não restaura `tgl_kernel_proof_manifest.json`, os artigos, as capturas nem o `.lake`. Há cópia em `base_v393`.

**Para o delta.** `derivar_instalar_rito_v394.py`, `instalar_v394.py` e `reverter_v394.py` têm o número 189 digitado. O assert falha de forma visível, mas é preciso re-derivar. Os três contratos pinam `expected_ladder` = 10752, e o `kh_n1_v394` pina 29025, 23068 e as 1421 entradas. Tudo isso deve ser regenerado pelo `gerar_candidato`, nunca à mão.

## 8. Toolchain [REAL, `OLEAN_v394.json`]

- Todos os 191 `.olean` novos do sandbox estão em 4.31.0 com githash `68218e876d2a…`.
- Também em 4.31.0: amostra de 300 antigos do sandbox, 300 do Nós e 100 de `packages`.
- `lean-toolchain` é v4.31.0 no sandbox e no Nós.
- Não rodei `lake`.

## Riscos que já existiam (não são da v394), para a janela até o rito

O rito lê arquivos fora do selo, e esses arquivos não podem mudar antes dele:
- o scratchpad desta sessão (`…\scratchpad\v386\RESPOSTAS_operador_05out.*`, `VERBO_operador_05out.txt`, `ramo_b\…`);
- a memória (`beta-escalar-limitado-inferiormente-06out.md`);
- o túnel do Codex (F0.3.B2, F1.ATRATOR, F5.2, F7.2, F8.2.*).

Hoje todos eles conferem (213 arquivos lidos).

## Scripts re-executáveis (para o delta)

- `python -B -X utf8 exame_pontos_v394.py --candidato <um.py> --logs <pasta com lake_build.log e audit.log> [--flags FLAGS_vNNN.json] [--sha256 …] [--sandbox …] [--core0 …] [--selo0 …]`
  Faz o verify com os logs crus e os controles negativos, a escada, o gate, o índice, os vizinhos, o bloco do `main` da v393 até `emit_figures` (pega um registro novo sem editar o script), o selo, a guarda e o rastreio de arquivos. Termina com `ALGUM FALSO`.
- `python -B -X utf8 simular_arvore_do_nos.py --candidato <um.py> --logs <pasta>`
  Monta a árvore que o rito real vai hashear (o embutido mais os residuais do Nós) e roda o índice e os registros v394 sobre ela.
