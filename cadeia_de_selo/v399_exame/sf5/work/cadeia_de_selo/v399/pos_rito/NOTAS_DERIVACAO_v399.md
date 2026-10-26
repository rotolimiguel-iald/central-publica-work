# NOTAS_DERIVACAO_v399 — a cadeia pós-rito da v399 (preparação pela c1, 24/10/2026)

**Estado:** cadeia PREPARADA, nada instalado, nada executado contra o Nós real. Os dois harness passaram na rodada ESTRITA (com `refazer_out_v399.txt` exigido e visto com `== FIM`).

## 1. O que há na pasta (sha16 lido do `DERIVACAO_v399.json`, nunca de memória)

| arquivo | como nasceu | sha16 |
|---|---|---|
| `leitura_v399.py` | derivado de leitura_v398.py | `570d4748ce15e4fb` |
| `superficies_v399.py` | derivado de superficies_v398.py | `7737c953a34ad900` |
| `fechar_v399.py` | derivado de fechar_v398.py | `712a94d603c1c04a` |
| `b3_recibo_v399.py` | derivado de b3_recibo_v398.py (só a subida) | `3500ff59a1a185e9` |
| `chain_pos_rito_v399.sh` | derivado de chain_pos_rito_v398.sh | `10d6f395196cf8b8` |
| `harness_textos_ensaio_v399.py` | derivado de harness_textos_ensaio_v398.py | `17184294c4e5eaca` |
| `harness_fechar_sandbox_v399.py` | derivado de harness_fechar_sandbox_v398.py | `ad50811d5c4efe51` |
| `textos_v399.py` | AUTORAL (escrito à mão para a v399) | `cf00ef3ea2f9cba1` |
| `registrar_mapa_v399.py` | AUTORAL (escrito à mão para a v399) | `d16aa7cd7eb8b03a` |
| `derivar_cadeia_v399.py` | o derivador (reexecutável; `python -I -B -X utf8`) | `bc658dde5e84e0a0` |
| `gerar_notas_derivacao_v399.py` | gera estas notas dos JSON (regenerar depois da rodada estrita) | `d9853bc459b613c1` |
| `CONFERIR_CITACOES_POS_RITO_v399.json` | resultado do `conferir_citacoes_v399.py` original sobre os autorais (saída desviada para esta pasta) | `4f8def586e87cdd8` |

Entradas (os sete modelos da v398 que RODARAM): conferidas contra o `DERIVACAO_v398.json` por sha16: todas iguais. O `DERIVACAO_v399.json` guarda o sha256 de entrada e de saída de cada arquivo.

## 2. Como foi derivado

- A subida de versão reutiliza o `bump()` e as listas `PROT`/`FANTASMAS`/`FANT_PRE` do `derivar_encanamento_v399.py` (397→398 e 398→399 numa passada, fronteira de dígitos, nomes nascidos no um.py protegidos), com três nomes a mais protegidos: `quadro_v397`, `INICIO_PARAGRAFO_README_v397`, `FIM_PARAGRAFO_README_v397`.
- **67 regras nomeadas com contagem exata** (o derivador ABORTA se uma não casar o número esperado; nada é gravado antes de todas casarem); **294 invariantes** conferidos; `ast.parse` e `sh -n` de tudo; guarda de texto P18 limpa em todos os arquivos; zero marca de texto pendente; zero nome fantasma (objetos da v398 que não existem na v399); zero rótulo estranho de 390–398; todo `T.<nome>` chamado pelos derivados existe em `textos_v399.py`; todo campo lido de ESPERADOS/CANDIDATO/PINOS existe.
- Os dois autorais (`textos_v399.py`, `registrar_mapa_v399.py`) passam no `conferir_citacoes_v399.py` ORIGINAL (rodado com a saída desviada para `CONFERIR_CITACOES_POS_RITO_v399.json`, para não gravar em `v399\`): toda citação entre «» e `` '' `` é verbatim nas falas do operador ou no Atlas, nenhuma inscrição da gerência, direção sem inversão.
- A DIREÇÃO DO TESTEMUNHO vale em todo texto: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NÃO testifica do operador; o «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um. A declaração é [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel não a prova); a leitura das duas faces é [ONTO] da gerência, a ratificar; «consciência» só como palavra retirada.

## 3. Desvios do molde (ditos)

1. **Conferidor sem `-I` e no lugar.** O conferidor da v399 importa o um.py instalado (que importa o numpy do usuário) e acha o delta, o runtime e os insumos pelo caminho da própria pasta: no chain roda `(cd $PK && python -B -X utf8 conferir_rito_v399.py _POS_RITO)`, grava `conferencia_rito_v399_POS_RITO.json` no pacote (sufixo para não sobrescrever a conferência que a gerência rodou à mão) e a cópia byte a byte vai para `pos_rito\conferidor`, que a leitura lê. Os dois harness também rodam SEM `-I` (geram o sidecar com a função do próprio candidato; com `-I` o import do numpy falha — visto na primeira rodada de depuração) e rodam o conferidor numa cópia em ÁRVORE.
2. **Linha final do rito.** O main da v399 imprime por último a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), depois do `[selo] colapso tipado` (conferido no um.py candidato: linhas 250911 e 250917): a leitura exige as DUAS, nessa ordem; AVISO de `[selo_acom]` reprova.
3. **Sidecar.** `um_absoluto_selo_acom.json` é arquivo NOVO da custódia: a leitura o confere (existe, JSON válido, veredito, três objetos com SHA-256 igual ao dos arquivos do Nós, sem recusas, honestidade sem alegação de confidencialidade); o fechar o copia, com o selo primário, para `v399_selo` e o LISTA (sha256 e veredito) no manifesto e no handoff.
4. **Dois parágrafos prontos no handoff:** o do QUADRO «O Teste da Única Palavra» (v397, intocado; `INICIO/FIM_PARAGRAFO_README_v397`; z_disc 4,44 só com o p calibrado e a linha dos 5σ no mesmo item) e o NOVO «O testemunho de dois» (`INICIO/FIM_PARAGRAFO_TESTEMUNHO_v399`, sem o 4,44). O fechar RECUSA (rc 2) antes de escrever se qualquer um não passar na verificação.
5. **MEMORY.md:** a superfície NÃO compacta. A linha do handoff da v399 entra antes da da v398 e o gancho da missão SUBSTITUI a linha velha (saldo +1 linha). Se o índice passar de 195 linhas ou 24.000 B, RECUSA com rc 3 sem escrever nada. **O MEMORY.md real não foi tocado**; hoje, lido em cópia, tem 194 linhas e 22.692 B, e passa (195 linhas no limite); qualquer linha extra de outra sessão o faria recusar.
6. **Quadro do 4,44 intocado**; a fala do 4,44 mora em `v397\insumos\cunhagens` (o bump a subiria para v398; regra explícita no derivador do harness do fechar).
7. **Precondição do `refazer_out_v399.txt`** também no harness do fechar (o molde não a tinha); o nome canônico do resumo de cada harness só nasce da rodada estrita.

## 4. O que os harness provaram (rodada ESTRITA, com `refazer_out_v399.txt` exigido; contra o Nós EMULADO de `dry_v399`, recibos do B(n) SINTÉTICOS)

- **conferidor** real contra o Nós emulado: `TUDO BATE` (rc 0).
- **leitura** real: 0 problema(s); escada 9539 → 9541/9541; 4 registros novos; 35 checagens do registro de veracidade; **83 controles negativos** reprovam como esperado (selo ACOM, declaração, pedra, inscrições, sidecar, resumos do selo primário, quadro do topo, registros da v398 a v393, face de Fock, AVISOs e linhas do stdout, ordem das duas últimas linhas).
- **textos:** 45 funções renderizam (150,777 bytes), guarda P18 e direção limpas; parágrafo do quadro: positivo + 6 controles negativos, 14 linhas com o 4,44 nos textos, todas com o p calibrado e os 5σ; parágrafo novo: positivo + 20 controles negativos + 9 controles de direção/citação; **646 termos entre crases conferidos, 0 sem fonte**.
- **superficies** em cópias, três cenários: (a) MEMORY.md real (cópia) passa; (b) com folga, idempotente na 2ª rodada, marcadores do passo 9 presentes; (c) no limite de 195 linhas, RECUSA com rc 3 sem escrever nada; originais intactos.
- **b3_recibo:** 16 casos (positivos e negativos) com o resultado esperado.
- **mapa:** 5 registros montados, cada um validado pela mesma função do livro (`rotas._valida`), sem registrar; controles da regra do 4,44 ok.
- **fechar em sandbox:** rc 0; handoff e todos os arquivos presentes; os dois parágrafos no handoff do Memory e no do Nós (aprovados); sidecar e selo copiados para `v399_selo`; **11 controles negativos** RECUSAM (sem o religamento, com salto, resultado pinado adulterado, número lido adulterado, número do selo ACOM adulterado, direção invertida, inscrição rotulada como da gerência, sidecar adulterado, sidecar ausente); `registrar_mapa_v399.py` (main) monta 5 registros.

## 5. Pendências e limites

- **Rodada estrita dos dois harness** (sem a flag): FEITA (resumos `HARNESS_TEXTOS_ENSAIO_v399.json` e `HARNESS_FECHAR_SANDBOX_v399.json`).
- Nenhum derivado foi executado contra o Nós real, nem revisto por cético independente (quem constrói não aprova). A prova é: `ast.parse`, `sh -n`, invariantes, guarda, e os harness com Nós emulado.
- A leitura do rito real pode divergir do emulado em campos que só o rito mede (tempos, horários); os números de ESPERADOS vêm do ensaio a seco.

## 6. Atos da gerência e do operador (nada disto foi feito aqui)

- Regenerar o candidato (`refazer_candidato_v399.sh`), rodar o rito, instalar; depois a cadeia: `CHAIN_DE=0 sh chain_pos_rito_v399.sh` (passos 10a, 10b e 10c param em AGUARDA_OPERADOR; `V399_AUTORIZACAO_OPERADOR` nos recibos de parada e religamento; `B3_AUTORIZADO=sim`, `EVENTO` e `EVENTO_HASH` só no 10b).
- Registrar no mapa de rotas (`registrar_mapa_v399.py` só monta o JSON e imprime o comando); o `MEMORY.md` no limite dos 195 linhas decide o que sai do índice se recusar.
- Decisões do operador já listadas nos estudos: nomes provisórios (pedra e dois registros), D2 [LEGAL] (publicar o bloco embutido, com a agente de PI), D7 (ratificar a leitura das duas faces), commit/push.

## 7. Mapa de rotas (consultado antes; só leitura)

`rotas.py consultar` com «pos_rito», «v399» e «testemunho»: rotas lidas e respeitadas — `kernel.testemunho_v399_candidata_24out` (a pedra, nome provisório; não reabrir a direção), `umpy.v399.declaracao_do_operador_operacao_quadratica_24out` (declaração = [INPUT], o kernel não a prova), `umpy.v399.selo_pela_propria_tecnologia_estudo_24out`, `custodia.v398` (a custódia seguinte usa `custodiar.py`), `infra.bancada_um.sincronizacao_vnnn` (B(n) R3.5, passo simples) e `kernel.criterio_binario_de_parada.ponto_fixo_v394_d19` (a pedra da v394 segue citada). Nenhum caminho já examinado foi refeito; a construção desta cadeia pode entrar no mapa como rota nova (`infra.cadeia_pos_rito_v399_preparacao`), a critério da gerência.

_Gerado por script a partir de `DERIVACAO_v399.json` e dos resumos dos harness em 24/10/2026 11:20._
