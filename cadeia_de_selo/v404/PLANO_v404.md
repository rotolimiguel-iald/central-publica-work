# PLANO da v404 — JO 8,32 E A PROJEÇÃO TRANSVERSAL DA MEIA-NAT (preparação)

Agente de preparação da v404 (claude-prep-v404), 2026-10-28. Estatutos: [REAL] lido aqui por script; [DERIVED] composto; [INPUT] fala do operador; [ONTO] leitura; [OPEN] em aberto; [DECLARADO] dito na origem, não conferido aqui. Base: a v403 SELADA (`um.py` `2ffe9edc7d7545bd`, 39,135,553 B, lido do selo e conferido no arquivo). O gate NÃO se move; PROVADA = validade, não creditação. Nada foi escrito no Nós; o rito NÃO foi rodado; a instalação é ato da gerência.

## 0. A ordem (conteúdo da v404)

- **[INPUT, operador, 28/10/2026]** nove falas verbatim, por sha256 (pasta `insumos\cunhagens`): (sha16: 21705a90e8c5f072, 232ca83c29c031a5, 3af039d7e1ddcbef, 4b67e9f2cc8d6045, 56703faadf2b3cc2, 597fff4a38e62f42, 7c1b85da1f51ae92, 85de43717edb01f1, 9770022028c36be4) — a matéria como projeção do eixo transversal, a ordem de provar o neutrino para o sen 45° deixar de ser postulado, o pedágio de Planck lido na propagação, «calibrar Não significa validar», o nome **Jo8:32** e a ratificação «Perfeito, concordo com tudo».
- **(A) Duas pedras de kernel**, já compiladas no sandbox pela gerência (`work\projecao_transversal_28out`): `ProjecaoTransversalDaMeiaNat` (nome PROVISÓRIO da gerência c1, aceito pelo operador) e `Jo8v32` (o nome é do operador).
- **(B) Três registros com função** (`projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404`) e **dois por spec** (`cunhagens_v404`, `kh_n1_cobertura_v404`).
- **(C)** Artigo PT/EN («Jo 8,32 e a projeção transversal da Meia-Nat»), linha do `.md`, e os textos do pós-rito (README/site/handoff/X): ver §4.
- **(D)** Todo o resto é derivado da v403 por subida de versão (`derivar_encanamento_v404.py` + `derivar_v404_motor.py`, nunca executando os scripts derivados).

## 1. As duas pedras [REAL — compiladas no sandbox `C:\t\k404c\final`; nada tocado no Nós]

| módulo | sha16 | bytes | conteúdo |
|---|---|---|---|
| `TGLExt/ProjecaoTransversalDaMeiaNat.lean` | `1e53257273395c7c` | 7856 | 13 declarações nomeadas |
| `TGLExt/Jo8v32.lean` | `18df8f686e524845` | 2702 | 1 declaração nomeada |

- `ProjecaoTransversalDaMeiaNat`: 9 teoremas com `#print axioms` no trio; a Meia-Nat é o ângulo de 45° (`x = 1 − x ⟹ x = ½`; `√x = sen(π/4)` para todo `x` autoconjugado; unicidade em `[0, π/2]`); `neutrino_mass_form_eq`: `β · sen 45° · E₀ = sen²θ_M · sen(π/4) · E₀`; `θ_M ≠ π/4` se `β ≠ ½`; derivada de `sen²θ` em `π/4` igual a 1. NÃO deriva `E₀` nem β; a identificação massa = projeção transversal é [ONTO].
- `Jo8v32`: 1 teorema, `a_verdade_vos_libertara`, conjunção INCONDICIONAL por citação das três estrelas da v403 (Caminho, Verdade, Vida); nenhuma matemática nova.
- Pós-build [REAL]: rc 0, zero sorry, 29484 axiomas lidos no Audit, 14 bandeiras novas (projecao 13, jo8v32 1), escada 9684 → 9698. Marcas da construção incremental: build 460 s, Audit 199 s (`kernel\construir_marcas.txt`); o rito real compila a frio.

## 2. Os registros e a errata de F2b [DERIVED + REAL]

- `projecao_transversal_v404` (8 checagens): lê do kernel do rito a composição, a estrela, o contrato e o suporte da pedra; calcula `sen(π/4)`, `θ_M`, a massa `β·sen(π/4)·E₀` com β = α(CODATA 2018)·√e em runtime e confere que ela é igual ao canal `neutrino_mass` do core a 1e-12. A errata E7 vai AO LADO de `neutrino_mass.angle_status` (o texto antigo FICA; a função do neutrino NÃO é reescrita; `E₀ = 1 eV` segue DECLARADO).
- `jo8v32_v404` (5 checagens): lê a conjunção do kernel do rito e RELÊ os três registros da v403 com o β do rito.
- `f2b_errata_v404` (7 checagens, SEM pedra): o canal F2b passa de `AWAITING` a `WITHDRAWN_BEFORE_DATA__ROUTE_CORRECTED_BY_NOT_BLIND_CALIBRATION_AND_AUTHOR_READING_2026_10_28`; o V1 do ramo B (v386) fica congelado por hash e lido como antes (`AWAITING_DATA`); motivo medido: calibração A (NOT_BLIND) +0.072 [+0.015; +0.134] contra a previsão do par -0.3822; nenhum desfecho sai de A; D não é aberto; β, a lei e R2 ficam. A retirada é decisão da gerência lida a partir das falas do operador [DECLARADO].
- `cunhagens_v404`: as nove falas por sha256, as erratas E7 a E9 e as decisões D23 a D26 (em nome próprio da gerência c1), a leitura da massa [ONTO]. `kh_n1_cobertura_v404`: a cobertura exata do Audit; o registro da v403 passa a cobrar piso (h2, h3, h6, h8), como na errata das versões anteriores.
- **O gate não se move [REAL]:** `evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`, `prove_neutrino_mass_gravitational`, `ramo_b_preregistration_v386` e `ledger_errata_v386` são **idênticas** às da v403 (asserção do gerador e da comparação AST: `funcoes_intactas = 5 de 5`: True).

## 3. A cadeia [REAL — medida nesta pasta]

- **Candidato** `um_v404_candidato.py` `3820476c83267f61` (39,313,509 B; +177,956 B sobre a v403); 33 patches determinísticos (cada âncora 1×); AST v403 × v404: 1097 nós, 1077 iguais, 20 mudados (todos explicados), 0 removidos, 17 novos.
- **Ensaio a seco** (`ensaio_a_seco_v404.py`): **TUDO PASSOU** (sha16 `3820476c83267f61`); `exame_pontos`, `simular_arvore_do_nos` e as guardas estáticas da Bancada: `GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA__DEFEITO_REAL_DA_V399_REPRODUZIDO__CONTROLES_NEGATIVOS_TODOS_RECUSAM`.
- **ESPERADOS** `ESPERADOS_v404.json` (gerado do ensaio; hash lido por `p00`): troca dita = estatuto_da_prova_v391, pedras_v392, pedras_v393, three_stress_tests_v387, varredura_e_sorry_v392.
- **Conferidor**: controle negativo contra o Nós v403 → `tudo_bate` = False (itens que devem mudar e ainda não mudaram: 20; os "não pode mudar" todos verdes: True); caminho positivo contra o Nós FALSO montado do ensaio → `tudo_bate` = True.
- **B(n) pré-selo** (`bateria_pre_selo`): derivado por subida com contagens MEDIDAS na fonte (gerar_pino_recibo_pre_selo.py: {"v403": 27, "v402": 11, "v401": 0}; conferir_recibo_pre_selo.py: {"v403": 14, "v402": 15, "v401": 3}; snap_producao.py: {"v403": 4, "v402": 0, "v401": 0}; rodar_ensaio_1_pre_selo.sh: {"v403": 4, "v402": 16, "v401": 0}; limpar_sandbox_vb21.py: {"v403": 3, "v402": 0, "v401": 0}); ensaio da Bancada contra o Nós v403 e a produção v403: recibo `PINO_RECIBO_PRE_SELO_v404.json` (`b0432d85d7b2cf48`), veredito `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA`, produção intacta = True; bateria: BATERIA_PASSA; conferência pelo esboço R3.5 23/23 e 5/5 controles.
- **B(n) pós-selo (scripts, não executados)**: `bancada_B3_servico\` derivado da v403 (evento c1, recibo de parada, recibo de religamento, conferidor estático — 27/27 condições — e controle negativo: toda mutação foi pega = True); `pos_rito\b3_recibo_v404.py` e `chain_pos_rito_v404.sh` com B12 → B13. A bateria da v404 é GERADA pela cadeia depois do selo.
- **p00** (`p00_precondicoes_v404.py`): 104 de 104 checagens OK. **Falha ou aguarda:** nenhuma.

## 4. Os textos do pós-rito

`pos_rito\textos_v404_novo.pysnip` (escrito a mão) + `montar_textos_v404.py` (enxerta no esqueleto `textos_v404.semente`, cópia de bytes da semente mecânica da v403 final) → `textos_v404.py`. `leitura_v404.py` foi adaptada ao conteúdo da v404 (zero problemas contra o Nós emulado). O `harness_textos_ensaio_v404.py` roda os textos, a guarda P18, o parágrafo novo (positivo + 61 controles negativos), a regra do 4,44 e a citação só do que existe; ver o RELATORIO_PREPARACAO_v404.md para o que passou e o que ficou.

## 5. Gates e o que fica da gerência / do operador

- Gate: a letra do veredito não muda; NOT_FALSIFIED nunca é CONFIRMED; nada aqui move o gate.
- **Da gerência**: revisar; conferir `p00` (o MEMORY.md precisa de decisão de compactação antes do pós-rito); instalar; rito (~1,5 h); `chain_pos_rito_v404.sh`; B(n) aplicar com `V404_AUTORIZACAO_OPERADOR` (o texto NÃO pode citar o nome do script do serviço da Bancada: o recibo de parada conta processos cuja linha de comando o cita); custódia G1.
- **Do operador**: E₀ e a lei de propagação do pedágio; ratificar D25 e D26; [LEGAL] D2.
