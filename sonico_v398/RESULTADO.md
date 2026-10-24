SÔNICO — v398 sandbox

Pedra candidata `TGLExt/Sonico.lean` (nome do operador, 23/10/2026). Compilada em sandbox (`C:\t\k398\final`); NÃO instalada; nada no quadro, no mapa, na memória, no site nem no git.

## Veredito

TGL_SONICO_STONE_V398_CANDIDATE__COMPILED_IN_SANDBOX__TRIO_ONLY__ZERO_SORRY__ONE_OCTAVE_IS_THE_FAIR_BIT_ENTROPY__THE_OCTAVE_IS_A_DOUBLING__THE_SELECTOR_PINS__VERB_IS_THE_PINNED_OCTAVE_CONTROL_IS_INPUT_ONTO__SONIC_IS_THE_LOGARITHMIC_OCTAVE_STRUCTURE_NOT_WAVE_PHYSICS__NOT_INSTALLED__GATE_UNMOVED

## A pedra

- Fonte: `C:\IALD\Central de Patentes\work\sonico_v398\Sonico.lean`, sha16 `a317094e337fd8b7` (23854 bytes, 275 linhas); cópia idêntica em `C:\t\k398\final\TGLExt\Sonico.lean`. Gerada por `gerar_sonico.py` a partir de `Sonico.lean.tmpl`; as versões anteriores estão em `*.bak_*` na pasta.
- Módulo `TGLExt.Sonico`; importa TheVerbSelectsTheAction, CanonicalSelectorBorn, CollapseCostAndAttestation, TheStokesContour, Psibit, CollapseContract, Palavra.
- Seis teoremas, nenhuma definição:
  1. `one_octave_is_the_parity_bit` — `K.octaveNats 1 = fairBitEntropy` (= ln 2), para todo `K : CollapseCostLaw`.
  2. `pinning_n_octaves_costs_n_bits` — `K.octaveNats n = n * fairBitEntropy`.
  3. `the_octave_is_a_doubling` — `Real.exp (K.octaveNats 1) = 2` (por `TGLExt.the_provable_toll_names_the_octave`).
  4. `the_selector_pins` — `select a (select a ψ) = select a ψ` e `select a a = a`.
  5. `the_pin_is_not_the_half_nat` — `K.octaveNats 1 ≠ K.localNats`.
  6. `sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory` — a conjunção incondicional: (4) + `ialdSelector = post (inscriptions 0)` (por `rfl`) + `normalized_selected_scalar_is_fixed`; (1), (2), (3), (5); o bit da paridade da Psibit (o colapso perde exatamente a paridade; a variável perdida é um bit; nos pesos iguais a entropia do colapso é `K.octaveNats 1`, e nunca a excede); a memória (`collapse_iteration_is_stable` e `Palavra.rereading_adds_nothing`).

## Compilação e axiomas

- `lake build TGLExt.Sonico` (cwd `C:\t\k398\final`): Built TGLExt.Sonico (21s), 9403 tarefas, exit 0, nenhum aviso ou erro do módulo (`lake_build_sonico.log`). Só o módulo novo foi compilado; as dependências já estavam atuais (`lake build --no-build` de Psibit, Palavra e Token: 9402 tarefas, exit 0; `lake_no_build_deps.log`).
- `.olean`: sha16 `06437a57d2acf70f`. Lean 4.31.0; Mathlib `v4.31.0` (rev `fabf563a7c95a166`).
- `#print axioms` das 6 declarações (as 6 do fonte) e `collectAxioms` de cada declaração do módulo (6): união = `propext`, `Classical.choice`, `Quot.sound`; zero `sorryAx`; zero axioma próprio (`AXIOMAS.json`).
- Nomes citados nos docstrings: `#check` de 38 nomes (Lean e Mathlib) sem erro; instanciamento da composição em `EuclideanSpace ℂ (Fin 2)` com `proposedCollapseCost` compila (não-vacuidade); e dois ensaios (B1, B2) mostram que `TGLExt.IALD.ialdSelector_eq_post` prova exatamente o conjunto `ialdSelector = post (inscriptions 0)` da pedra e que `TGLExt.IALD.rereading_adds_nothing` tem o enunciado que a docstring cita — `nomes_citados_saida.txt`; tudo fora da pedra.
- Sandbox: `C:\t\k398\final` é cópia fiel de `C:\t\k397c\final` (133819 arquivos; k398 tem 133831: os 12 novos são Sonico e `probe\`); nenhum tamanho diferente, nenhum link; os 9 módulos citados têm `.lean` e `.olean` idênticos (`conferencia_sandbox.json`). Base: v397 selada, Nós `um.py` `388cc3742323421c` (lido agora).

## O que o pedido da gerência (docstring) acrescentou — feito, sem mudar enunciado

1. Isomorfismo dito com precisão: `log` é o isomorfismo de grupos `(ℝ₊,·) → (ℝ,+)` (Mathlib: `Real.log_mul`, `Real.exp_add`, `Real.exp_log`, `Real.log_exp`, `Real.log_pow`, todos conferidos por `#check`), leva a oitava (razão 2) a `ln 2` = um bit, e `n` oitavas a `n·ln 2`; é nisso que o léxico sônico é isomórfico ao conteúdo [REAL]. Equivalência de oitava ↔ identidade preservada sob o pino, eco ↔ «ecoar reconhecimento» (fala de 22/10, sha16 `350b7b8582c064c2`) [ONTO].
2. Os dois sentidos do som, com fonte: «som ontológico» = vibração LONGITUDINAL na profundidade, distinta do fóton (transversal) — `A_fronteira_v4.tex` l.962 (sha16 do arquivo `b473db2b652cf72f`; linha citada byte a byte; ela é a linha 962 do arquivo) [ONTO acervo]; no Atlas (II.S, l.2329–2332) o verbete é [DECLARADO]. E a escala acústica: o teste acústico (`teste_acustico_beta_tgl_v1`, fechamento `N2_INCAPAZ`, medida do instrumento) e o fundo BG1 da Fase 9 V2: `fundo.r_d_modelo = 147.38613794723423` Mpc (≈ 147,39), contra `fundo.fundo_livre.r_d = 148.0218760536698` (sigma `0.5277182199787567`), no resultado `fbac2908fa9ddb75` (lidos do arquivo, número conferido). A oitava pinada do Verbo e a régua acústica pinada do fundo são a mesma figura [ONTO, leitura da gerência, dita como tal; nenhum termo liga `octaveNats` a `r_d`].
3. Honestidade: «sônico» não afirma onda mecânica num meio; a isomorfia é da estrutura logarítmica/de oitava, não da física da onda.
4. Leitura ratificada (último acréscimo): no cabeçalho (seção própria) e no docstring da composição (6): leitura ratificada pelo operador em 23/10 (sha16 `b4483331019f96f8`, a fala «Sim quero, concordo com tudo»; a leitura da gerência está arquivada em `GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt`, sha16 `19eca91e5aab9d11`, e citada inteira no cabeçalho): a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina [INPUT/ONTO]. Mantido dito: a lei de custo é [INPUT] e nenhum termo diz que `select` paga `K.octaveNats 1`. Enunciados inalterados (o `.olean` foi refeito; os 6 teoremas seguem no trio).
5. Revisão independente (gerência c1, `EXAME_SONICO.md`, sha16 `61d8859aa65f3c9e`, sobre `1338622344dd80c7`): PEDRA_APROVADA, 3 BAIXAS de prosa, aplicadas só em docstring; o código fora dos comentários é byte a byte o revisado (`conferencia_codigo_identico.json`: sha16 do código `d171f0c5637d216c`, 4142 bytes). B1: a ponte `ialdSelector = post (inscriptions 0)` já existe no kernel, `TGLExt.IALD.ialdSelector_eq_post` (`IALD.lean:110`, `rfl`, «une a FORMA, não o referente»); citada e re-enunciada. B2: `TGLExt.IALD.rereading_adds_nothing : memory (post a) (post a ψ) = memory (post a) ψ` (`IALD.lean:370`) citado como o termo da memória sobre o mesmo `post`, e `rereading_adds_nothing_in_both_regimes` (`IALD.lean:675`) como a conjunção dos dois registros; NÃO entraram na conjunção (6): exigiriam `import TGLExt.IALD` (fecho de imports maior) e mudariam o enunciado revisado. `IALD.lean`: sha16 `884b327423888ddc`, igual no Nós e no k398; linhas 110, 370 e 675 conferidas por script. B3: a leitura da gerência, arquivada por sha em `GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt` (sha16 `19eca91e5aab9d11`), citada inteira.

## Conferências do cabeçalho (`conferencia_cabecalho.json`)

- 10 sha16 entre crases, todos iguais ao sha256 do arquivo lido agora; as três falas do operador e o arquivo da gerência (em bloco de código) aparecem inteiros; 23 citações «» de 12+ caracteres, todas achadas no corpus dos verbatins do operador ou no Atlas (mesma normalização da varredura da v397); nenhuma palavra proibida pela régua; nenhum parâmetro de acoplamento literal; comentários balanceados; zero `sorry` no código.

## Mapa de rotas (consultado antes; nada registrado)

- `oitava`: 3 rotas (quantica.c3_gamma_livre_oitava, custodia.v393_v394.conjunta, infra.grep_acom_camadas); a relevante é `quantica.c3_gamma_livre_oitava` (NO_UNIVERSAL_FLOOR para um observável dinâmico, não tocado). `sonico`: 2 rotas, nenhuma sobre o tema. `verbo`: 17 rotas; as relevantes, `kernel.v386_tipagem_do_verbo` e `kernel.psibit_v395_candidata_21out` (as pedras citadas). Saídas em `mapa_consulta_*.json`. Livro com 1365 registros na consulta (cabeça `0f800eb875552cb3`).
- `registro_mapa_sonico.json` está pronto e VALIDADO com `rotas._valida` (sem registrar); registrar é ato da gerência: `python C:\IALD\MAPA_DE_ROTAS\rotas.py registrar <arquivo> --quem "<IA/sessão>"`.

## Limites, ditos

- A lei de custo é [INPUT] (campos de `CollapseCostLaw`): a pedra prova o que ela implica, não a deriva do axioma.
- Nenhum termo diz que `select` PAGA `K.octaveNats 1`: verbo = controle de oitava pinada é definição do operador [INPUT/ONTO]; a conjunção põe as duas metades lado a lado.
- «que é memória» admitia duas leituras (a oitava? a reação?); a leitura ratificada pelo operador em 23/10 (relato da gerência; a resposta dele é o verbatim `b4483331019f96f8`) é: a REAÇÃO ao pino — o pedágio pago, `ln 2` por oitava — é a memória; a oitava é o que se pina [INPUT/ONTO]. O kernel entrega o preço e a permanência lado a lado, não a identidade entre eles.
- A entropia dos resultados do colapso do psibit vale `ln 2` só nos pesos iguais; nunca a excede.
- Homônimos e registros: dois «reler não acrescenta» (o do ângulo e o do colapso) lado a lado, nenhum lema desta pedra entre eles. A ponte `ialdSelector = post (inscriptions 0)` NÃO é nova: o kernel já a tem (`TGLExt.IALD.ialdSelector_eq_post`, `IALD.lean:110`, `rfl`, «une a FORMA, não o referente»); a pedra a re-enuncia por `rfl` e a cita. O termo do kernel da memória sobre o mesmo `post` (`TGLExt.IALD.rereading_adds_nothing`, `IALD.lean:370`) e a conjunção dos dois registros (`rereading_adds_nothing_in_both_regimes`, `IALD.lean:675`) estão citados no docstring; NÃO foram importados nem entraram na conjunção (6): importar `TGLExt.IALD` mudaria o fecho de imports e o enunciado revisado.
- Revisão independente feita (gerência c1, `EXAME_SONICO.md`, sha16 `61d8859aa65f3c9e`, sobre `1338622344dd80c7`): PEDRA_APROVADA, 3 BAIXAS de prosa, aplicadas só em docstring. Validade no kernel não é creditação; o gate não se move; nenhuma bandeira depende desta pedra.

## Ato da gerência / do operador

- Reexame independente; se aceita, instalar na v398 (`import TGLExt.Sonico` em `TGLExt.lean`, política de bandeiras, ledger de pedras); registrar a rota; decidir se a frase do operador pede um termo próprio (ver `proximo_passo`).
