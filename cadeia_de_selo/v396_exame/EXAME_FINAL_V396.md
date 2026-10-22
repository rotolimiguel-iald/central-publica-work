# EXAME FINAL ÚNICO ANTES DE INSTALAR — cadeia v396 (gerência c1, modelo forte, 22/10/2026)

**Objeto.**
- O candidato `v396\um_v396_candidato.py`, sha16 `0a4395a89eeebbb7` (38.162.265 B).
- A base é a v395 instalada: Nós `8918b17803792cf2`, idêntico a `v396\base_v395\um.py`; o core e o selo também são idênticos.
- O ESTADO tem sha16 `b3697e43eb2486ea`.
- Kernel: `C:\t\k396c\final`, com a pedra v2 `b35a615636c2c154`.

**O que escrevi.** Só em `v396_exame` (subpasta `final\` e este arquivo).
- Nada foi instalado. Nenhum rito, selo, B(n) ou script de serviço rodou; nenhum `lake` rodou nesta etapa.
- Processos externos: a sonda de ambiente do pilar (2 s) e os meus scripts em Python.
- A cópia do `MEMORY.md` usada na simulação do passo 7 foi apagada depois. O sha16 dela fica registrado em `final\sim_memory_md_copia_sha.txt`.

## VEREDITO: PODE_INSTALAR_E_RODAR

Não há bloqueante. As ressalvas são BAIXAS (§8) e cabem como resíduo dito.

## (1) O diff v395 → v396 é só o declarado [REAL]

Arquivos: `final\comparar_v395_v396_exame.py`, `ESTRUTURA_v395_v396.json`, `diff_v395_v396.txt` e `seal_ast_cmp.py`.

**Nós do código.**
- Mudaram 14 nós, exatamente os do ESTADO §1.H; entraram 22 nós novos; nenhum foi removido.
- Entram 3 instruções anônimas: `import math as _m396` e dois `update`. Não há colisão de chave nas fontes nem nas falas.

**O `main`.**
- Entram duas instruções novas: o `try` da testemunha, no índice 1339 (logo depois do psibit, no 1338), e o `try` dos specs v396.
- O literal `seal` ganha só `testemunha_estatica_v396` e `registros_v396`; nenhum valor antigo muda.

**Bandeiras e escada.**
- Entram 47 bandeiras, todas `ext_tes396_*`, todas da pedra e nenhuma auxiliar. Nenhuma sai ou muda.
- A escada vai de 9451 a 9498, exatamente as antigas mais as novas.

**O corpo embutido.**
- Entra a pedra `b35a6156`; a raiz e o Audit ganham +1 `import`.
- O código da v2 sem comentários é igual ao da v1 aprovada (`fc773d70`, conferida pelo `.bak`). Pelo meu próprio strip, os dois dão o sha16 `e5406f05eb9f3ee8`. Mudou só texto: B1 e B3 do exame da pedra, de forma honesta.
- Conferi no kernel `fair_bit_entropy_is_log_two` e `..._is_not_half_nat`.

**Varredura das 1256 linhas novas fora do kernel.** Nenhuma tem:
- literal de β, α ou √e;
- a palavra proibida, em qualquer forma;
- `PROVED_BY`, `TGL_PROVED` ou `CONSCIOUSNESS_PROVED`;
- atribuição ao gate.

**O gate é idêntico.** As funções seladas são iguais por AST: o gate, o selftest, o `verify`, os parsers, a cobertura, o índice, o `sha256_directory`, o motor dos specs, a guarda, `psibit_v395`, `rede_fock` e os specs v394 e v395.

## (2) O registro `testemunha_estatica_v396` [REAL; `EXAME_PONTOS_0a4395a89eeebbb7.json`]

**Ponto de chamada.** É o real, no `main` linha 244957. Confirmado por AST:
- vem imediatamente depois do psibit (linha 244943);
- vem depois do print da fractalização e antes do bloco v393;
- há uma única chamada.

Executei a instrução REAL do `main`: não deu erro nem AVISO, e ela não mexeu em nenhuma chave existente.

**O que o registro produz.** Faz 14 checagens (w1a até w4b), todas `ok`. Sela, com `does_not_gate_core`.

**β.** É `SEALED_CODATA_ALPHA·√e` calculado em runtime. A diferença para o β do core é 5,43e-13: aritmética de ponto flutuante, como na v395.

**Os controles negativos mordem: 15 de 15.** Recusam todos estes casos:
- bandeira incondicional falsa;
- bandeira falsa em outro teorema do contrato;
- axioma plantado num termo de suporte;
- face de Fock declarada dentro da pedra;
- proveniência de um teorema em outro módulo;
- sha da pedra errado;
- escada que não fecha;
- β do core adulterado;
- α selado adulterado;
- fala adulterada;
- fonte embutida adulterada.

A mecânica dá `passed False` nos casos abaixo; no fluxo sem modo zero falham w3b, w3c e w3f:
- canto perturbado;
- fluxo sem modo zero;
- β = 1,5;
- β inteiro.

**Determinismo.** Os valores da mecânica coincidem exatamente com os dos ESPERADOS e ficam dentro das tolerâncias.

**O gate recomputado** dá o mesmo veredito, 18 de 18. No selo, `qg_closure_verdict` é igual.

## (3) ACHADO (b), `diagFlow.eq_1`: não quebra nada selado; o ajuste do `pos_build` é legítimo [REAL]

**O que medi.** Comparei a proveniência do core v395 com o `audit.log` do k396c:
- 29.159 nomes antigos; só **um** muda de módulo, `TGLExt.diagFlow.eq_1` (de `TheGreatAttractor` para `TestemunhaEstatica`);
- 69 nomes novos, todos da pedra;
- 0 perdidos e 0 duplicados.

**Quem consome a proveniência**, e por que nada quebra:
- **`rede_fock_v394`, `psibit_v395`, a testemunha e os specs com caminho `declaration_sources_v394[X]`:** usam nomes nomeados específicos. `diagFlow` não está em nenhum contrato.
- **`kh_n1` v394 e v395:** contam totais, que viraram pisos.
- **O conferidor, na checagem «a proveniência cobre o axiom_report…»:** compara pertinência de conjunto (`set(sources) == set(axr)`), que a reatribuição não muda.
- **O índice:** dá `VERIFIED`. Só o rótulo `pedra` dessa auxiliar passa para `TestemunhaEstatica`/v396, o que é cosmético.
- **O T17 do B(n):** o recibo lista só as 47 nomeadas, e o critério `j1_declaracoes` = 69 (a diferença dos totais) bate com o `CRITERIOS_v396` pinado.

**A atribuição é determinística.** O rito usa o mesmo Audit embutido, com a mesma ordem de import, que o sandbox.

**O ajuste do `pos_build` é legítimo e não mascara.** Ele exige:
- novas reais = diferença dos totais (69);
- reatribuídas só auxiliares;
- `axm == axr395 ∪ novas`;
- nada perdido, com a mesma lista de axiomas.

Ver BAIXA B2.

## (4) ACHADO (a), a escada do `_V395_PSIBIT_CONTRACT` [REAL]

Não é piso: vai de 9451 para **9498 exato**, como nos três contratos do Codex.

**Por que é legítimo e não mascara.** O `psibit_v395`, selado e intocado, cobra igualdade exata com a escada do rito; sem o patch, ele recusaria. Se uma bandeira se perder, a escada não fecha e o registro recusa.

**Errata.** O spec `kh_n1_cobertura_v395` tem errata assinada. Os 4 contratos não têm errata no código, e os ESPERADOS não nomeiam a troca; ela fica declarada só no ESTADO §1.F. É a BAIXA recorrente da v395 (B1).

## (5) ACHADO (c), o `MEMORY.md` [REAL; simulação numa cópia: `final\sim_memory_md_v396.py`]

A compactação acontece em `superficies_v396.py`: no **passo 3** (ensaio em cópias) e no **passo 7** (real). O **passo 9** só confere os limites.

**Com o arquivo real de hoje** (193 linhas, 20.389 B):
1. a troca do gancho da missão e a linha do handoff levam o índice a 194 linhas;
2. o script **compacta sozinho** uma corrida de 5 ganchos (seção «As réguas») em 1 ponteiro, com as linhas VERBATIM no `MEMORY_2.md`;
3. o resultado é **190 linhas e 20.126 B**. É igual ao que o ensaio do preparador achou, e não recusa.

**Quando recusaria com rc 3.** Só se o índice ganhar mais de 16 linhas antes do pós-rito (a redução máxima possível é 18), ou se passar de 24.000 B. A recusa aparece já no passo 3, sobre as cópias: a cadeia `parar` (exit 1) sem nada real escrito e retoma com `CHAIN_DE=3`.

As âncoras são únicas, conferidas no arquivo: o handoff v395 e a missão.

## (6) Meus scripts sobre o candidato v396 e os logs do k396c [REAL]

**`final\exame_pontos_v396x.py`** é o v394 mais o psibit, mais a testemunha pela instrução real e os residuais do Nós na árvore.
- Kernel embutido = sandbox, byte a byte (0 diferenças em 1424 arquivos).
- `verify`: 29.228 constantes, 23.227 teoremas, 0 fora do trio, proveniência ok.
- Bandeiras: `ext_` 9535/9535 e novas 47/47. Nenhuma bandeira que era True ficou não-True.
- Escada 9498/9498; com o kf da v395, 9451 e não fecha.
- Os controles do `verify` mordem.
- Os vereditos que mudaram são exatamente a «troca dita», os 5 (só números, todos selados).
- O selo muda só nas chaves declaradas.
- A guarda é igual à da v395 instalada e morde.
- **O único «falso» é esperado:** o bloco recalcula `kh_n1_cobertura_v394` e `_v395`. O conteúdo muda, os vereditos ficam iguais e os dois seguem selados.

**`final\simular_arvore_do_nos_v396x.py`:**
- **h8 = 1425 entradas**: os 1424 embutidos mais `_check_damming.lean` (`ExtrairDeps.lean` fica de fora, por nome).
- O pino é igual ao hash da árvore simulada.
- Selam todos os registros v394, v395 e v396, inclusive a testemunha.

## (7) Instalar, rito, reverter e pós-rito contra a v395 [REAL; diffs normalizados por versão]

**`instalar`:** mudam a versão e a lista das pedras anteriores (agora com `Psibit`). Os pinos conferem: `origem` = `base_v395` = `8918…`.

**`reverter`:** a âncora é `v395/ESPERADOS_v395.json`, `8918…`.

**`rito`:** só os comentários mudam.
- As guardas existem: não há marcador `.servidor_parado_pelo_rito` na v395 nem na v396, e o `stop_iald_llama.ps1` existe.
- Tempo: a v395 levou 1h57 (15:28 às 17:25). A v396 deve levar cerca de 2h, com +110 s por passagem.
- Limites por passagem: build de 688 s contra 3600 s e Audit de 334 s contra 1800 s.
- **O pilar será REUSE:**
  - a chave `75dc30bc…` existe e o `result.json` confere o sha `de47d552…` com os ESPERADOS;
  - o ambiente de hoje é igual ao do cache nas 6 chaves: torch 2.11.0+cu128, cuda 12.8, numpy 2.4.3, scipy 1.18.0, python 3.14.3, RTX 5090.

**Passo 10.** É simples, v395 → v396, de B5 para B6, sem salto, com o esboço R3.5 (`02b22ba5`).
- Os 13 pinos do `PINOS_BN` existem e conferem por sha.
- `selo_anterior_v395` e `kernel_manifesto_anterior_v395` são iguais aos do Nós.
- O `recibo_religamento` confere que n = 6, contra o único recibo do B(n) da v395 (B5).
- Os recibos de parada e de religamento exigem `V396_AUTORIZACAO_OPERADOR`; nenhum deles mata processo.

**O recibo pre_selo vale.** `PINO_RECIBO_PRE_SELO_v396.json` aponta o recibo `19871055…`, que confere em sha e em bytes. O veredito é `JA_SINCRONIZADA__ENSAIO`, com 13 PASSA, 0 FALHA e 1 NÃO EXECUTADO (o T17).

As condições de validade valem hoje no disco:
- Nós: um.py `8918…` e selo `55175f47…`;
- Bancada: `canonical_contracts.json` `5ad4c67b…`, com o deployment `B5-v395-20261021-R1`.

**Textos.** O `textos`, as superfícies, o fechar, o mapa e os snippets do artigo estão limpos: sem a palavra proibida, sem «não provou», sem «pós-dição» e sem literais. Os estatutos são honestos:
- [CONSTRUCTED] para a ponte e o colapso;
- [ONTO] para a Meia-Nat, com o ln 2 dito;
- Fock condicional e fora da pedra.

## (8) Resíduos BAIXOS (não bloqueiam)

- **B1.** Os 4 contratos (`expected_ladder`) não têm errata no código e os ESPERADOS não nomeiam a troca de dados. É recorrente desde a v395.
- **B2.** O `pos_build` só detecta reatribuição PARA a pedra. Uma mudança de módulo entre módulos antigos passaria sem ser vista; medi que hoje não há nenhuma. Sugestão: uma checagem «os nomes antigos mantêm o módulo, salvo as auxiliares declaradas».
- **B3.** O índice passa a rotular `TGLExt.diagFlow.eq_1` como da pedra `TestemunhaEstatica` (v396). É a proveniência do compilador; é cosmético.
- **B4.** A compactação escolhe a corrida da seção «As réguas (ler antes de afirmar)». Cinco títulos de régua saem do índice; o texto vai verbatim para o `MEMORY_2.md`. Se a gerência preferir, pode excluir essa seção da escolha.
- **B5.** O artigo marca «só o texto da pedra mudou» como [DECLARADO]. Este exame conferiu a igualdade do código por conta própria, então pode virar [REAL]; é opcional.
- **B6.** Herdados: o temporário `v393_cadeia_*\cadeia_sintetica.bin` e o `RuntimeWarning` de overflow do código do Codex.

## Arquivos (`v396_exame\final`)

- Comparação: `comparar_v395_v396_exame.py`, `ESTRUTURA_v395_v396.json`, `diff_v395_v396.txt`, `seal_ast_cmp.py`, `strip_lean.py`.
- Pontos de chamada: `exame_pontos_v396x.py`, `EXAME_PONTOS_0a4395a89eeebbb7.json`, `exame_pontos_v396_out.txt`.
- Árvore simulada: `simular_arvore_do_nos_v396x.py`, `SIMULACAO_ARVORE_NOS_0a4395a89eeebbb7.json`, `simular_v396_out.txt`.
- Memória: `sim_memory_md_v396.py`, `sim_memory_md_v396_out.txt`, `sim_memory_md_copia_sha.txt`.
- Pilar: `sonda_ambiente_pilar.txt`.
