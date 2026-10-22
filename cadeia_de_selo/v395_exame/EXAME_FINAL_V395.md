# EXAME FINAL ANTES DO SELO — cadeia v395 (gerência c1, modelo forte, 21/10/2026)

**Objeto.** O candidato `v395\um_v395_candidato.py`, sha16 `8918b17803792cf2`, sobre a v394 instalada (Nós `972e81f22dd8cc68`, igual a `v395\base_v394\um.py`). O kernel é `C:\t\k395c`.

**O que escrevi.** Só em `v395_exame\final` e neste arquivo. Nada foi instalado; nenhum rito, selo, `lake`, B(n) ou script de serviço rodou. O único processo externo foi a sonda de ambiente do pilar.

## VEREDITO: PODE_INSTALAR_E_RODAR

Não há bloqueante. As ressalvas abaixo são BAIXAS e cabem como resíduo dito.

## (1) O diff v394 → v395 é só o declarado [REAL]

Arquivos: `diff_v394_v395.txt`, `DIFF_POR_NO_v394_v395.json`, `ESTRUTURA_v394_v395.json`.

**O que mudou.** São 13 nós mudados e 18 novos, como diz o ESTADO §1.H; nenhum nó foi removido. Entram três instruções anônimas: `import math as _m395` e os dois `update` das fontes e das falas, sem colisão de chave.

**Bandeiras e escada.** Entram 119 bandeiras `ext_psb395_*`, todas de `TGLExt.Psibit`; nenhuma sai ou muda. A escada vai de 9332 para 9451, a soma exata das antigas com as novas.

**O corpo embutido.** Entra `Psibit.lean` com o sha16 `50c199eb01976151` aprovado; a raiz e o Audit ganham +1 `import`.

**Varredura das 2441 linhas novas.**
- Nenhum literal de β, α ou √e.
- Nenhuma ocorrência da palavra proibida, em nenhuma forma.
- Nenhuma atribuição ao gate.

**O gate não se move.** Recomputei-o com o kf novo: veredito idêntico e 18 de 18. No selo, `qg_closure_verdict` é igual.

**O β.** O registro calcula `SEALED_CODATA_ALPHA · √e` em runtime e confere `_v376_same_alpha_literal`. A diferença relativa de 5,43e-13 para o β do core é aritmética de ponto flutuante [REAL]:
- a forma de Lagrange calcula α_form = √(1 − q²) com q² ≈ 1 − 5,3e-5, o que gera cancelamento; o limite do erro é ε/α² ≈ 4e-12;
- em aritmética exata (50 dígitos), α_form = α;
- o β de runtime erra 7e-17 contra o valor exato; o β do core erra 5,43e-13.

## (2) `psibit_v395` no ponto de chamada real [REAL, `EXAME_PONTOS_8918b17803792cf2.json`]

**Onde é chamado.** No `main`, logo depois do bloco que imprime o «PRINCIPIO DA DEFASAGEM FRACTAL» (`Tudo = D_β(F(1))`). O registro calcula ρ_out(θ_M) = F_θ(1), que é a «fractalização do Um igual» do kernel (`Posto.fractal_one_is_rank_one`), e faz 19 checagens.

**O que produz.** Sela; não mexe em nenhuma chave existente; `does_not_gate_core`.

**Os controles negativos mordem**, nos seis casos que testei:
- bandeira incondicional falsa;
- β do core adulterado;
- α selado adulterado;
- sha da pedra errado no kernel;
- escada que não fecha;
- mecânica com β fora de (0, 1) dá `passed False`.

**BAIXA.** O registro não lê `core["fractal_dephasing"]`: recalcula θ_M a partir de β, e a amarração ao estágio é só pela posição no código. Sugestão para uma próxima versão: conferir s² contra `fd["leak_sin2_thetaM"]`.

## (3) As igualdades da v394 que viram pisos: legítimas, sem mascarar [REAL]

**Nos três contratos do Codex,** `expected_ladder` passa de 9332 a 9451. A igualdade continua exata, agora cobrada contra a escada 9451.

**Em `kh_n1_cobertura_v394`:**
- h2, h3 e h6 viram pisos;
- h8 passa de «igual ao dict de 1423 entradas» para «pelo menos 1423 entradas»;
- tem errata assinada, e o veredito dele não muda.

**Onde ficaram os valores exatos.** Em `kh_n1_cobertura_v395`: h2 = 29159, h3 = 23170, h4 = 0, h5 = 0, h6 = 29159, e h8 com o dict de 1424 entradas, que é igual aos embutidos mais o residual `_check_damming.lean`.

**BAIXA.** O conferidor e os ESPERADOS não nomeiam essa troca de dados (não há chave `mudanca_de_dados_v394`). Ela está declarada no ESTADO §1.F e na errata do spec; a mudança dos contratos não tem errata no código.

## (4) Meus scripts, rodados sobre o v395 e os logs do k395c [REAL]

**`exame_pontos_v395x.py`** é o meu `exame_pontos_v394.py` mais duas coisas: roda o `psibit_v395` na ordem real e acrescenta os controles negativos dele.
- Rodei com os residuais do Nós já copiados para a árvore.
- verify 29159/23170/0, proveniência ok, `ext_` 9488/9488, novas 119/119.
- Escada 9451/9451; com o kf da v394, 9332 de 9451 e não fecha.
- Índice verde, guarda limpa, selo com o mesmo `qg_closure_verdict`.
- O único «falso» apontado é esperado. É `kh_n1_cobertura_v394`, que o bloco do `main` recalcula com os pisos novos: muda o conteúdo, mas o veredito fica igual e ele continua selado.

**`simular_arvore_do_nos_v395x.py`:** a árvore tem 1424 entradas, e todos os registros v394 e v395 selam, inclusive o `psibit_v395`.

## (5) instalar, rito e reverter, linha a linha contra a v394 [REAL]

- **`rito`:** mudam só os rótulos e a lista de guardas (v394, v395).
- **`instalar`:**
  - exige o recibo pre_selo pinado e utilizável, do `um.py` que está no Nós;
  - exige as pedras da v394 presentes e a `Psibit.lean` ausente;
  - lê o número de módulos da lista;
  - faz backup de bytes dos 8 arquivos, como na v394.
- **`reverter`:**
  - restaura os 8 arquivos e põe a lista de módulos novos em quarentena;
  - a âncora é `v394/ESPERADOS_v394.json`;
  - cobre tudo o que o instalador grava.
- **Tempos.** Por passagem: build de 617 s contra o limite de 3600 s e Audit de 295 s contra 1800 s. A pedra entra no fecho reverso de `HalfNat`, mas não está no caminho crítico.
- **Pilar.** O ambiente é igual ao do cache (`75dc30bc…`, sha ok) e a v394 o reaproveitou (REUSE).

## (6) Pós-rito [REAL]

**O passo 10** é simples, de v394 para v395:
- usa o esboço R3.5 (`02b22ba5…`, que já fechou com lista de permissão o desvio M que apontei na R3.4) e o recibo do kernel R3_2;
- gera a bateria da v395 depois do selo, a partir do `PINOS_BN_v395`, cujo candidato é o `8918…`;
- recusa se houver cadeia de selos.

**Recibos de parada e religamento.** São atos do operador e exigem `V395_AUTORIZACAO_OPERADOR`; nenhum dos scripts mata processo.

**Textos.** Nenhum número digitado. Os estatutos são fiéis: escopo da órbita; bijeção de conjuntos; face do psion condicional; `psibit = psion = modo do leitor` como [INPUT/ONTO]; a travessia perde a paridade e a leitura do par perde zero.

## (7) O recibo pre_selo vale [REAL]

`PINO_RECIBO_PRE_SELO_v395.json` → o recibo `9a467db6…` bate com o arquivo. O veredito é `JA_SINCRONIZADA__ENSAIO`, com bateria v394 de 13 PASSA / 0 FALHA / 1 NÃO EXECUTADO.

Os pinos dele conferem hoje no disco:
- Nós: um.py `972e…`, selo `993e26f1…`, manifesto do kernel `f3ec495e…`;
- Bancada: `canonical_contracts.json` `eda4b550…` (B4-v394).

O recibo vale até a instalação, desde que nada mude desse lado antes dela.

## Resíduos BAIXOS (não bloqueiam)

1. As bandeiras incluem a maquinaria que o compilador gera para a estrutura `Code` (`mk`, `rec`, `casesOn`, `noConfusion`…). É a mesma política e o mesmo resíduo da v394.
2. O ESTADO estima 45,6 min só de lake. É coerente, porque o build medido foi incremental.
3. O temporário `v393_cadeia_*\cadeia_sintetica.bin` é escrito e apagado pela própria `regra_v393`, como na v394.

## Arquivos (em `v395_exame\final`)

- Diffs e comparações: `diff_v394_v395.txt`, `DIFF_POR_NO_v394_v395.json`, `comparar_v394_v395_exame.py`, `ESTRUTURA_v394_v395.json`.
- Pontos de chamada: `exame_pontos_v395x.py`, `EXAME_PONTOS_8918b17803792cf2.json`, `exame_pontos_v395_out.txt`.
- Árvore simulada: `simular_arvore_do_nos_v395x.py`, `SIMULACAO_ARVORE_NOS_8918b17803792cf2.json`, `simular_v395_out.txt`.
