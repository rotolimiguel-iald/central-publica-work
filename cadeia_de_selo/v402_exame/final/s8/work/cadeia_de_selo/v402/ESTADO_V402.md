CADEIA v402 — preparada; a ponte da escala dual, a queda sem geometria e a esperança condicional

**Resumo.** Gerência c1, subagente de preparação, fecho da preparação em 26-27/10/2026 (00:13). Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [OPEN] em aberto; [INPUT]/[ONTO] fala ou leitura do operador; [KNOWN] literatura; [LEGAL] a conferir com a agente de PI. Nada foi instalado e nada foi selado; o `um.py` real não rodou; o Nós não foi tocado (o `um.py` do Nós segue `1925cb691e933ae8`, a v401 selada, conferido contra a base de ESPERADOS; o selo do Nós diz `v401`); o gate não se move; NOT_FALSIFIED nunca é a palavra da creditação; validade no kernel não é creditação.

## 0. Resumo em números

- **O candidato:** `um_v402_candidato.py` sha16 `6a5033dc3f29324c` (arquivo) = CANDIDATO `6a5033dc3f29324c` = ESPERADOS `6a5033dc3f29324c`: **um só**; 38,945,032 B (+256,498 B sobre a v401 selada `1925cb691e933ae8`), 23 patches, determinístico. Ajuste do controle N10: 0 espaço(s) no fim do comentário da linha UM_VERSION.
- **As três pedras** (nomes PROVISÓRIOS; o operador nomeia): `TGLExt/PonteDaEscalaDual.lean` sha16 `0e55b6e448adbd91` (40 bandeiras; composição `core_positive_realization_exists` = `ext_pde402_0005`, estrela `lift_mass_not_selected` = `ext_pde402_0016`); `TGLExt/QuedaSemGeometria.lean` sha16 `0ffce7f1d564d271` (60 bandeiras; composição `a_queda_sem_geometria` = `ext_qsg402_0040`, estrela `the_fall_is_strictly_anti` = `ext_qsg402_0056`); `TGLExt/EsperancaCondicional.lean` sha16 `8579115333f84428` (18 bandeiras; composição `esperanca_condicional_e_nome` = `ext_ecn402_0002`, estrela `the_name_of_the_unit_is_the_diagonal_expectation` = `ext_ecn402_0012`). Escada 9561 -> 9679 (+118 bandeiras, só de declaração nomeada: 40 PonteDaEscalaDual + 60 QuedaSemGeometria + 18 EsperancaCondicional); cobertura do Audit 29464 constantes, 23412 teoremas, 0 fora do trio; build 438 s + Audit 358 s no sandbox `C:\t\k402c`.
- **Kernel (pós-build):** `POS_BUILD_v402.json` ok = true (41 sinais conferidos); 118 bandeiras, 29464 declarações no Audit, 29464 axiomas lidos; `KERNEL_RECIBO_v402.json` (contrato `KERNEL_RECIBO_R3_2`) rc 0, sorry 0, erros 0, J1 = 146 declarações e 106 teoremas a mais que a v401, 0 fora do trio, 9405 entradas antigas do Audit idênticas; tokens proibidos: 0.
- **Os registros com FUNÇÃO** (leem do kernel do rito a composição e a estrela de cada pedra e CALCULAM, com β = α·√e em runtime): `ponte_da_escala_dual_v402` 10 checagens, selou=true; `queda_sem_geometria_v402` 8 checagens, selou=true; `esperanca_condicional_v402` 7 checagens, selou=true.
  - ponte: β = `0.012031300400803`; p₊ escala por e^(−s); m² = p₊p₋ invariante; massas μ² = 1, 4, 9 com o MESMO p₊ dão levantamentos distintos (a massa não é selecionada); deslocamento mínimo da energia no estado nulo 0.2212 e no repouso 0.0628; fator de p₊ em s = β: 0.988040786.
  - queda: custo mínimo t·β·g = `6.016e-04`; defasagem máxima `0.999398616` (< 1); perda por unidade `0.011959214`; período angular `6.283185` (periódico, sem limite); ordem do grupo finito do modelo: 12.
  - esperança: θ_M = `0.109908430778`; sin²θ_M = β = `0.012031300400803`; índice CONDICIONAL do Nome 1/β = `83.1165` (nenhuma instância construída); índice da esperança diagonal de M₂ = 2; dimensão GNS 4.
- **Os registros por spec:** `cunhagens_v402` (as 3 inscrições do operador de 26/10 por sha256: `5d3976cd0cc10dc8`, `36cfa0027565dcff`, `a1c4bae4a87aa173`; as decisões D11 a D16 da gerência; as erratas E1 a E4) e `kh_n1_cobertura_v402` (cobertura exata do Audit).
- **Ensaio a seco: TUDO PASSOU** — 150 verificações de unidade (150 verdadeiras); guardas ESTÁTICAS da Bancada sobre o candidato: GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA__DEFEITO_REAL_DA_V399_REPRODUZIDO__CONTROLES_NEGATIVOS_TODOS_RECUSAM (alfa na linha 5584; 9 controles negativos recusam; a v399 selada reproduz a recusa do recibo da Bancada: true); comparação AST com a v401: 1042 iguais, 18 mudados (sem explicação: 0), 17 novos, 0 removidos; troca dita: estatuto_da_prova_v391, pedras_v392, pedras_v393, three_stress_tests_v387, varredura_e_sorry_v392.
- **Conferidor do rito (emulação):** controle negativo (Nós ainda v401) `tudo_bate = false` (o esperado é false); caminho positivo (Nós FALSO do ensaio) `tudo_bate = true` (itens C1 a C16 e o round trip); **citações:** TODAS CONFEREM; **pré-condições (p00):** TODAS OK (87 checagens).
- **Recibo pre_selo GERADO E PINADO antes da instalação** (ensaio contra a Bancada de produção, que pinava `B10-v401-20261025-R1`; nada gravado nela): veredito `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA`, sha16 `36aaf247165536ed`, bateria 14 testes: 13 PASSA, 0 FALHA, 1 nao executado (BATERIA_PASSA); conferido pelo próprio esboço R3.5: aceita=true, 23/23 condições, 5 controles negativos; produção intacta: true; **utilizável como recibo pre_selo do B(n): true**; **válido enquanto a Bancada pinar `B10-v401-20261025-R1`**: a Bancada pina AGORA `B10-v401-20261025-R1` (versão `v401`) -> AINDA VÁLIDO.
- **`memoria.py` pinado** (o helper da fila da memória que o pós-rito usa): sha16 `7c4fc5853f41f1d3`, 87642 B, igual ao declarado pela gerência: true.
- **Serviço da Bancada:** 27/27 condições estáticas (parada e religamento exigem `V402_AUTORIZACAO_OPERADOR`; nada executado). **`MEMORY.md` real:** 192 linhas hoje (o handoff soma +1; teto 195).

## 1. O que a v402 muda e o que NÃO muda

1. **Muda (o `um.py`):** +3 módulos no kernel (as três pedras: a ponte da escala dual, que é a do Codex, ORDEM 025, copiada **byte a byte** [só o `.lean` entra, condição C1 do exame]; a queda sem geometria; a esperança condicional); +118 bandeiras e a escada 9561 -> 9679; os registros com função `ponte_da_escala_dual_v402`, `queda_sem_geometria_v402`, `esperanca_condicional_v402`; os registros por spec `cunhagens_v402` e `kh_n1_cobertura_v402`; a seção «A ponte da escala dual, a queda sem geometria e a esperança condicional» no artigo PT/EN e as linhas no `.md`; `UM_VERSION`; os 7 contratos que pinam a escada sobem para 9679.
2. **A ponte (ORDEM 025):** a lei de escala (Takesaki, [KNOWN], campo de `DualScalingData`) é REALIZADA como o boost longitudinal sobre (E, p); a massa² = p₊p₋ é o invariante; a energia é a LEITURA e muda com o observador; **a lei de escala NÃO seleciona a massa** (`lift_mass_not_selected`; `positive_weight_cannot_be_invariant_mass`). Pendências NOMEADAS [OPEN]: H_BW, H_cal, H3, a assinatura ((4,0), não (1,3)) e rank c = 4 (H2).
3. **A queda sem geometria:** o peso cai estritamente (em nats, a queda é s); a seta é o sinal de s, não uma direção do espaço; o chão é o POSTO (peso 1 = ω(I)), nunca o ínfimo 0 (o 0 é o abismo); a entrega custa; o regime angular só lê (periódico, sem limite). `IsotropicPost` é hipótese NOMEADA [OPEN] e é carga; a dimensão 3 NÃO é provada; o 1 + 3 é leitura [ONTO].
4. **A esperança condicional é o Nome:** em M₂(ℂ) o `nameOp` de ρ* É a esperança diagonal; preserva o Um (E(1) = 1); reler não acrescenta; a memória é uma subálgebra; o índice 1/β é CONDICIONAL (sem instância). As três faces de um objeto fixo (o operador, o projetor de Jones, o posto) são leitura [ONTO] (D13); o kernel prova as LIGAÇÕES.
5. **NÃO muda:** a seção do selo pela própria tecnologia (o runtime dela é o da v401), o quadro «O Teste da Única Palavra» no topo (a regra do 4,44: nunca sem o p calibrado e sem a linha dos 5 sigma), o gate, o piso dos vazios, o perfil, o sidecar (o rito o reescreve), nenhum módulo já instalado (D15: as erratas vão AO LADO).

## 2. Erratas E1 a E4 (gerência c1, em nome próprio, 26/10/2026) e decisões D11 a D16

- E1 -- H_tau na forma literal («tau e' a massa de Newton e a metrica de Einstein», como a v401 a escreveu) e' REFUTADA no kernel: positive_weight_cannot_be_invariant_mass (um peso positivo que escala por e^{-s} nunca e' invariante na propria orbita) e lift_mass_not_selected (dois invariantes mu^2 distintos dao duas realizacoes equivariantes DISTINTAS com o MESMO p+). tau so' pode ser p+ (a energia da frente de luz) e a massa e' dado livre. H_tau decompoe-se em pendencias NOMEADAS [OPEN]: H_BW (a rapidez e' o tempo modular de Bisognano-Wichmann, 2 pi), H_cal (este p+ e' a energia de UM corpo; a escolha de mu^2), H3 (Clausius em toda direcao nula) e as dividas do adendo de 03-04/09 (a positividade completa da a metrica induzida (4,0), nao (1,3); rank c = 4, o H2 nao sai de graca)
- E2 -- «Inertial» nesta instancia (momentumScaling) e' o VETOR ZERO (fixo por todo boost: p+ = 0 e p- = 0), nao «movimento livre»: a leitura de que a inercia implica p+ = 0 nao e' fisica da primeira lei; a lacuna de que a rapidez nao e' automaticamente o tempo modular de BW e' H_BW, NOMEADA [OPEN]
- E3 -- nunca ler como E = mc^2 composta da escala: rest_energy_eq_mc2 e' algebra real com premissas explicitas (casca, repouso, E >= 0, m >= 0; c > 0 nao e' usado); a composicao e' lift_rest_energy (c = 1), do REPOUSO, condicionada a mu^2 e a tau = m
- E4 -- proveniencia: a entrega do Codex compilou contra o kernel do Nos v400 e contra a copia superada da pedra FalsidadeDaInercia (8a3a1c0baa8b7faf, so' docstrings diferem); o revisor recompilou no kernel v401 com a pedra instalada (9f6efcb2a0987e18): rc 0, 40 #print axioms no trio, .olean identico

- **D11:** o CHAO e' o POSTO (peso 1 = omega(I), o corte a = 0, the_floor_fixes_the_cut; na Fundacao «o piso limita», cunhagem de 07/10), NUNCA o infimo 0: o 0 e' o abismo (sem fundo) e «a consequencia da poda» (recorte de 25/10); a queda de que fala a fala («porque vc sabe que tem um chão, então relaxa») e' a queda do que NAO e' o posto [decisao da gerencia c1, 26/10/2026; ratificavel pelo operador]
- **D12:** IsotropicPost fica como hipotese NOMEADA (o operador ratificou a rota com «é isso, faça a prova, prossiga.»): a isotropia e' CARGA, nao enfeite (AuditF23Flat.s8_h3_is_load_bearing: a H3 falha com fonte anisotropica); o 1 + 3 fica como leitura [ONTO]; a dimensao 3 NAO e' provada [decisao da gerencia c1, 26/10/2026]
- **D13:** o Nome e' nameOp (a esperanca condicional, o OPERADOR que le: unital, idempotente, memoria-subalgebra); o projetor de Jones e' a MESMA coisa vista como projetor no espaco GNS (a compressao pelo espelho) e o posto e' o PESO que ela preserva (E(1) = 1): tres faces de um objeto fixo, nao tres definicoes; o kernel prova as LIGACOES, nao uma igualdade de tipos [decisao da gerencia c1, 26/10/2026]
- **D14:** o B(n) da v402 e' um PASSO SIMPLES v401 -> v402: a Bancada de producao JA pina a v401 (B10); o recibo pre_selo e' GERADO e PINADO antes da instalacao, em ensaio contra a producao (nada gravado nela)
- **D15:** a ponte do Codex (ORDEM 025) entra SO' como o arquivo .lean (condicao C1 do exame: nenhum outro arquivo da entrega e' copiado), byte a byte, sem edicao; as erratas E1-E4 vao ao lado, no registro, no artigo e no handoff; nenhum modulo ja' instalado e' editado
- **D16:** os nomes dos tres modulos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) e dos cinco registros da v402 sao PROVISORIOS: o operador nomeia

Pergunta e resposta de 26/10 [INPUT (a pergunta, do operador, na sessao de 26/10/2026) / ONTO (a resposta, leitura da gerencia c1)]: «o Um posto tem direcao?» / «a seta da queda da fase, nao do espaco» — a pergunta e a resposta nao tem arquivo verbatim no acervo desta cadeia: sao registradas como a gerencia c1 as guardou [DECLARADO]; a fala 1 (sha16 36cfa0027565dcff) traz a base verbatim: «então tem direção, mas não é gemétrica»

## 3. B(n) da Bancada Um: passo SIMPLES v401 -> v402

- A Bancada de produção JÁ pina a v401 (`B10-v401-20261025-R1` no recibo; `B10-v401-20261025-R1` lido agora do `canonical_contracts.json`); o recibo pre_selo foi **GERADO** nesta cadeia e pinado antes de qualquer instalação (`PINO_RECIBO_PRE_SELO_v402.json`), com a produção só lida. Vale enquanto a Bancada pinar B10/v401 (manifesto `9d21d7f394953847`); um re-pino o torna obsoleto e o instalador o recusa.
- O B(n) grava **B11** (veredito esperado `REPINADA_B11__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`); sem salto, sem cadeia de selos; os pinos estão em `PINOS_BN_v402.json`. Parada e religamento do serviço (porta 18777) e o evento c1 são ATOS DA GERÊNCIA/OPERADOR, com `V402_AUTORIZACAO_OPERADOR` no ambiente; nada foi executado.
- **Hoje:** a porta 18777 responde (HTTP 200); o sistema subiu em `2026-10-26 22:08:14` [lido agora do relógio do Windows].

## 4. Achados desta preparação

1. **A Bancada caiu com o reboot de 26/10 às 22:08 e foi religada** [DECLARADO pela gerência no briefing do A2; conferido agora: sistema no ar desde `2026-10-26 22:08:14`, porta 18777 responde (HTTP 200), `canonical_contracts.json` pina `B10-v401-20261025-R1` (`v401`)]. O recibo pre_selo continua válido? **SIM** (a Bancada pinava `B10-v401-20261025-R1` quando o recibo foi gerado).
2. **O Nós está intacto** [REAL, lido agora]: `um.py` `1925cb691e933ae8` (38,688,534 bytes, mtime 25/10 12:50), selo com `um_version = v401`; a v402 NÃO foi instalada.
3. **Pré-condições (p00):** TODAS OK. **`sh -n` do `chain_pos_rito_v402.sh` medido AGORA:** rc 0. **`refazer_out_v402.txt`:** d9031564b21ce9f2.
4. **A fila da memória:** o pós-rito pina o `MEMORY.md` por `memoria.py` (a gerência c1 é a única que escreve no diretório real; nenhum agente escreveu nele nesta preparação); o ensaio dela em CÓPIA está em `pos_rito\FILA_MEMORIA_ENSAIO_v402.json` (tudo_passou = true).

## 5. A suíte do pós-rito (lida agora, no fecho da preparação; os JSON de depuração das iterações anteriores ficam em `pos_rito/depuracao`)

21 arquivos em `pos_rito\` (fora os `.bak_`: 17 backups de bytes):

- `DERIVACAO_v402.json` `98f78370076653e1` (7,631 B, 22:51:55)
- `FILA_MEMORIA_ENSAIO_v402.json` `714b78db1d1b67b1` (22,495 B, 23:53:37)
- `HARNESS_FECHAR_SANDBOX_v402.json` `ac86c689e2056ab5` (15,594 B, 23:53:37)
- `HARNESS_FECHAR_SANDBOX_v402_SO_FILA.json` `cbc25a9d5c67fd8f` (887 B, 22:53:46)
- `HARNESS_TEXTOS_ENSAIO_v402.json` `773f1a0c1e91ac7c` (150,592 B, 23:52:25)
- `HARNESS_TEXTOS_ENSAIO_v402_SO_LEITURA.json` `9a26ac07dc292f1c` (109,691 B, 23:15:22)
- `b3_recibo_v402.py` `def0d18e299e1982` (8,309 B, 22:32:22)
- `chain_pos_rito_v402.sh` `ecbaab2692de0757` (37,343 B, 22:36:00)
- `fechar_v402.py` `e50533eea8f48a88` (23,052 B, 22:32:07)
- `fila_memoria_v402.py` `bff5440a39c6ae1e` (10,732 B, 22:29:16)
- `gerar_derivacao_pos_rito_v402.py` `6f06227777faa0ff` (5,838 B, 22:25:54)
- `harness_4c_novo.pysnip` `0c483ae8a2b2bb7f` (11,946 B, 23:36:31)
- `harness_fechar_sandbox_v402.py` `e73938f1be8194e2` (98,166 B, 22:52:37)
- `harness_textos_ensaio_v402.py` `a08dfa7bfe73d691` (121,365 B, 23:36:31)
- `leitura_v402.py` `e2626f9227c092b6` (71,142 B, 23:11:01)
- `montar_textos_v402.py` `a67cd5b755459506` (5,673 B, 23:31:34)
- `registrar_mapa_v402.py` `bd9cacd54dbb794d` (44,081 B, 23:19:36)
- `superficies_v402.py` `376282dab36c0f96` (17,254 B, 22:30:17)
- `textos_v402.py` `dbf48ce1b166ddee` (121,678 B, 23:37:03)
- `textos_v402.semente` `ee9629926cb634db` (115,125 B, 23:31:02)
- `textos_v402_novo.pysnip` `f10d4748083eb34d` (98,189 B, 23:36:58)

JSON de harness e de ensaio com veredito:

- `DERIVACAO_v402.json`: tudo_passou = n/a; veredito = n/a
- `FILA_MEMORIA_ENSAIO_v402.json`: tudo_passou = true; veredito = n/a
- `HARNESS_FECHAR_SANDBOX_v402.json`: tudo_passou = true; veredito = TUDO PASSOU: a FILA DA MEMORIA funciona em copia (pausa antes da escrita do indice, pinar rc 0, a pausa so' sai depois do pino, verificar rc
- `HARNESS_FECHAR_SANDBOX_v402_SO_FILA.json`: tudo_passou = true; veredito = TUDO PASSOU (so' a fila da memoria): o passo da fila funciona em COPIA na ordem do chain (pausa antes da escrita, pinar rc 0, pausa so' depo
- `HARNESS_TEXTOS_ENSAIO_v402.json`: tudo_passou = true; veredito = TUDO PASSOU: o conferidor da v402 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles neg
- `HARNESS_TEXTOS_ENSAIO_v402_SO_LEITURA.json`: tudo_passou = true; veredito = SO LEITURA: o conferidor bate no Nos emulado, a leitura le sem problema e os 223 controles negativos reprovam


## 6. O que é ATO da gerência/operador (nada disto foi feito)

1. **Instalar** (`instalar_v402.py`; confere o recibo pre_selo pinado, a Bancada ainda em v401 e a lista de módulos novos; backups de BYTES; troca por `os.replace`) — gerência.
2. **Rodar o rito** (`rito_v402.sh`) e **conferir** (`conferir_rito_v402.py`, SEM `-I`); **reverter** se falhar (`reverter_v402.py`) — gerência.
3. **Pós-rito** (`pos_rito\chain_pos_rito_v402.sh`: a leitura, a fila da memória, as superfícies, o fechar, o `registrar_mapa_v402.py` que MONTA e não registra) — gerência; o passo das superfícies PARA se o `MEMORY.md` passar de 195 linhas.
4. **B(n) com `V402_AUTORIZACAO_OPERADOR`** (parada e religamento do serviço na porta 18777; evento c1) — ato do operador.
5. **Revisão independente** do candidato, dos derivados e dos textos (quem constrói não aprova) — a gerência escolhe o revisor.
6. **Nomear as pedras** e **ratificar D11 e D13** (a D12 mantém `IsotropicPost` nomeada sobre uma rota que o operador aprovou; D16: os nomes são provisórios) — operador.
7. **Registrar no mapa** (`rotas.py registrar`): primeiro `registro_mapa_v402_prep.json` (a rota de preparação, já validada por `rotas._valida`), depois `pos_rito\registro_mapa_v402.json` (a rota selada, as anotações e as erratas com o seq corrigido) — gerência, `--quem` dela.
8. **Rodar `regras_v402.py`** (escrito, NÃO rodado) — gerência. **Commit/push**, **[LEGAL] D2** e **CC art. 125** — operador com a agente de PI.

## 7. O que FALTA e o que NÃO foi revisado

1. **Revisão independente:** o gerador, o runtime dos registros, as três pedras (a da ponte foi recompilada pelo revisor no kernel v401; as outras duas só no sandbox da preparação), os derivados e os textos NÃO tiveram cético independente [DECLARADO: só os controles negativos próprios, a comparação AST e os harness].
2. **O rito real** é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo do conferidor e os harness são EMULAÇÃO sobre o Nós falso (core e selo do ensaio, não do rito).
3. **Honestidade de escopo:** o cálculo de cada registro é numérico em dupla precisão e CONFERE os teoremas, não os prova; a lei de escala de Takesaki é dado [KNOWN]; H_τ na forma literal está REFUTADA no kernel (E1), e a v401 a escreveu: a correção vai ao lado, no mapa e nos registros; a ponte NÃO prova a primeira lei de Newton, nem a assinatura (1,3), nem rank c = 4, nem E = mc² composta da escala (E3).
4. **Pendências nomeadas [OPEN]:** H_BW, H_cal, H3, a assinatura, rank c = 4, `IsotropicPost` sobre o atlas curvo, a dimensão 3 e o índice 1/β sem instância.

## 8. Mapa de rotas consultado (antes) e o que devolveu

- `rotas.py consultar "v402"` -> 4 rota(s): `kernel.v402_esperanca_condicional_e_nome`, `kernel.v402_queda_sem_geometria`, `infra.memoria.fila_codex_ordem026`, `custodia.v401`
- `rotas.py consultar "ponte da escala dual"` -> 0 rota(s): nenhuma
- `rotas.py consultar "queda sem geometria"` -> 1 rota(s): `kernel.v402_queda_sem_geometria`
- `rotas.py consultar "esperanca condicional"` -> 3 rota(s): `quantica.inventario_gkls_um_py_kernel`, `kernel.v402_esperanca_condicional_e_nome`, `kernel.v402_queda_sem_geometria`
- `rotas.py consultar "ordem025"` -> 2 rota(s): `kernel.ordem025.ponte_escala_dual`, `kernel.v402_queda_sem_geometria`

Livro com 1454 registros, cabeça `b9006c88b9bd2afb`. Rotas relevantes lidas: a da entrega do Codex (`kernel.ordem025.ponte_escala_dual`: PONTE_PARCIAL; não identificar p₊ escalante com massa invariante) — **só aparece por «ordem025»**, o consultar «ponte da escala dual» não devolve nada; as das duas pedras construídas em sandbox (`kernel.v402_queda_sem_geometria`, `kernel.v402_esperanca_condicional_e_nome`: não reprovar a mesma composição); a da pedra anterior (`kernel.v401_falsidade_da_inercia`) e a da v401 selada (`umpy.v401.selada_falsidade_da_inercia_25out`); a do B(n) (`infra.bancada_um.sincronizacao_vnnn`). O registro desta preparação é `registro_mapa_v402_prep.json` (montado e validado por `rotas._valida`, NÃO registrado).

## 9. Arquivos principais (sha16 lido agora)

- `um_v402_candidato.py` `6a5033dc3f29324c`
- `CANDIDATO_v402.json` `8f2b776d99143b97`
- `ESPERADOS_v402.json` `ec60c52758f040e3`
- `ensaio_a_seco_v402.json` `d345099570a12b5b`
- `PINOS_BN_v402.json` `340d0be400260dd9`
- `PINO_RECIBO_PRE_SELO_v402.json` `80bf0483496059aa`
- `PINO_MEMORIA_PY_v402.json` `f18dd2eec0af1484`
- `PROVA_PRODUCAO_INTACTA_v402_pre_selo.json` `d2e7b44634366fc6`
- `PRECONDICOES_v402.json` `eec35648769d66bd`
- `COMPARACAO_V401_v402.json` `21c0af9863ba3f07`
- `GUARDAS_ESTATICAS_BANCADA_v402.json` `1cfdafd30b611e6a`
- `kernel/KERNEL_RECIBO_v402.json` `a37ebc3ab159e74a`
- `kernel/FLAGS_v402.json` `0638087a2977a88e`
- `kernel/KH_N1_v402.json` `d46600142d7429a3`
- `DIFF_KERNEL_v402.txt` `32cbe70dde342c76`
- `conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json` `2e6184740a912b8c`
- `conferencia_rito_v402_POSITIVO_FALSO_NOS.json` `9f2c20ef3e2d4210`
- `conferir_citacoes_v402.json` `162f19ced689e0b0`
- `registros_v402.py` `911e45c2baa84f30`
- `runtime_v402.py` `8c5b42e87e50199e`
- `delta_v402.py` `3d41517f0316e523`
- `gerar_candidato_v402.py` `d562716f9928315b`
- `gerar_esperados_v402.py` `96ba15c3786fbc55`
- `instalar_v402.py` `d3b907b82ac7d47b`
- `reverter_v402.py` `b3a100ec654517c2`
- `rito_v402.sh` `0412f09d976fad5b`
- `conferir_rito_v402.py` `e689438793afcbe3`
- `regras_v402.py` `901faedef6afde7a`
- `registro_mapa_v402_prep.json` `4eef1892e29de1f3`
- `gerar_registro_mapa_prep_v402.py` `ca034624d885d0ff`
- `pedra/PonteDaEscalaDual.lean` `0e55b6e448adbd91`
- `pedra/QuedaSemGeometria.lean` `0ffce7f1d564d271`
- `pedra/EsperancaCondicional.lean` `8579115333f84428`
- `pos_rito/chain_pos_rito_v402.sh` `ecbaab2692de0757`
- `pos_rito/textos_v402.py` `dbf48ce1b166ddee`
- `pos_rito/leitura_v402.py` `e2626f9227c092b6`
- `pos_rito/registrar_mapa_v402.py` `bd9cacd54dbb794d`
- `pos_rito/fechar_v402.py` `e50533eea8f48a88`
- `bateria_pre_selo/NOTAS_PRE_SELO_v402.txt` `30bb2e57be69b173`
- `bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v402.json` `919d2248926af591`

NOT_FALSIFIED não é a palavra da creditação; validade no kernel não é creditação; o gate não se move.
