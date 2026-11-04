# RELATÓRIO DA PREPARAÇÃO DA v407 — O psíon, o canto e o par

Agente de preparação `claude-prep-v407` · 2026-11-03 18:48 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (o psion, o canto e o par, v407) FOI revisado por terceiro: Claude Sonnet (agente revisor de terceiro; rodada R5; nao construi a v407; mesma familia da R1 a R4 e da revisao de 02/11, outra instancia), rodada R5, aprovada, 0 ALTO, 0 MEDIO, 5 BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v407.md, sha16 bdc0d5d80aea3b88); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; as ressalvas BAIXAS estao escritas no caderno e valem como ditas (sem terceira rodada para BAIXO); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `833121339e649f71` (43,065,098 B; base v406 `ddcb91930982d614`): `pronta` = **true**.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k407c\final`) | True: build + Audit rc 0, 98 bandeiras novas, escada 11860 → 11958, 9 módulos no recibo; `KERNEL_RECIBO_v407.json` |
| candidato | True: 41 patches; refazer limpo = True |
| AST v406 × v407 | True: 1175 nós, 1150 iguais, 25 mudados (explicados), 0 removidos, 15 novos; 17 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 1 apontada(s) à gerência (ver §4) |
| guarda das frases | True (controle negativo e as 9 pedras) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 115/115 checagens OK; pendentes: 0 |
| B(n) pré-selo | True: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria BATERIA_PASSA; produção intacta = True; recibo `6fc53a82f7a4d7f2` |
| serviço da Bancada (estático) | True: 37/37 condições; toda mutação pega = True |
| harness dos textos | True: 576 controles da leitura, 69 do parágrafo novo |
| harness do fechar | True: 31 controles do fechar |
| regeneração limpa | True: `refazer_out_v407.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | True: `purga_v407.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | True: `purga_v407.json`, zero ocorrências |

## 3. O que NÃO passou ou fica para depois

- p00 reprova 0 checagem(ns): nenhuma; pendentes (0): nenhum.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `kernel.v407_preparacao_03nov`, seq 1743 (ROTA).

## 4. Avisos e desvios ditos

- os nomes das nove pedras sao do operador (PsionCanto aceito, Par dado, as sete de 02/11 ratificados em 03/11/2026); o sufixo R1 dos arquivos de origem era marca de revisao e saiu (BUNDLE_v407.json guarda nome_antigo, sha256 da origem e o numero de linhas #print axioms removidas na normalizacao)
- a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma passa de literal False (v396 a v406) a LEITURA do kernel do rito (errata E18 AO LADO; o texto selado das versoes anteriores nao e' reescrito); as quatro chaves da v406 seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396 e fechamento_v406 NAO mudam (nenhuma troca dita de texto: os que carregam a escada mudam so' em numeros)
- ressalvas ditas em todo texto: o elo das duas faces e' de ESTRUTURA (Omega e Phi+ nao sao identificados: espacos distintos); a face de Fock do par segue [OPEN] (o FockCertificate nao tem operadores de criacao como termo); a ponte entre o espaco de Bell e o setor TT do spin 2 nao e' termo; K(O) != bot so' na cunha; o teste (d) so' consta por CITACAO do pre-registro V1.1 (D44); o motor continuo fica fora (D45)
- APONTADO a gerencia, NAO corrigido (o agente nao edita pedra revista): 1 trecho(s) de pedra que a regra lexical F16 da guarda das frases reprova (o trecho de OUmInscrito sobre o setor de uma particula; o enunciado esta em guarda_frases_v407.APONTADAS_A_GERENCIA e nao e' repetido aqui para nao reprovar este relatorio na mesma guarda); a gerencia decide se reescreve (BAIXO)
- a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto; nenhum teste com a natureza entra nesta versao; o pilar reusa a chave de cache
- o B(n) pre-selo da v407 (passo simples B16; a Bancada de producao pina B15-v406-20261103-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v407.json aponta 1 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): registros_v407.py: |G> como produto nao emaranhado; o agente nao corrige texto da gerencia
- build a frio dos 9 modulos no sandbox k407c: 337 s, Audit 271 s (kernel/POS_BUILD_v407.json, medidos); 33863 declaracoes no axiom_report (+131 decl, +116 teoremas sobre a v406), nenhuma fora do trio; escada 11860 -> 11958
- revisao de terceiro (Sonnet D47): este candidato (o psion, o canto e o par, v407) FOI revisado por terceiro: Claude Sonnet (agente revisor de terceiro; rodada R5; nao construi a v407; mesma familia da R1 a R4 e da revisao de 02/11, outra instancia), rodada R5, aprovada, 0 ALTO, 0 MEDIO, 5 BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v407.md, sha16 bdc0d5d80aea3b88); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; as ressalvas BAIXAS estao escritas no caderno e valem como ditas (sem terceira rodada para BAIXO); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato
- ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): [DITO pela gerencia: a ordem de intercalacao de stderr nunca foi contr | [CARREGADO da R4, nao tocado nesta rodada] pos_rito/textos_v407.py (by | [CARREGADO da R4, nao tocado nesta rodada] orquestrador/pos_treino_v40 | [CARREGADO da R4, nao tocado nesta rodada] runtime_v407.py:105 (c16 de | [CARREGADO da R4, nao tocado nesta rodada] RESIDUAL da R1 (aspas): ped

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D47), nesta ordem, antes de qualquer publicação: `delta_v407.py` (moldura, erratas E18 a E20, decisões D41 a D47), `registros_v407.py`, `runtime_v407.py` (as 16 checagens de `psion_canto_v407`), `pedra/PsionCanto.lean` e `pedra/Par.lean` (as outras sete foram revistas em parte em 02/11), as seções do artigo (`artigo_pt_v407.pysnip`, `artigo_en_v407.pysnip`) e `pos_rito/textos_v407.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v407 NÃO entrega: validade no kernel não é creditação; o lema liga as duas faces do psíon por ESTRUTURA (Omega e Phi+ não são identificados); a face de Fock do par segue aberta e a ponte entre o espaço de Bell e o setor TT não é termo; K(O) ≠ ⊥ só vale na cunha; as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza e nenhum teste novo entra nesta versão.
3. O orquestrador lê `PREPARACAO_v407_PRONTA.json` e segue: `instalar_v407.py`, `rito_v407.sh`, `pos_rito/chain_pos_rito_v407.sh` (0 → 10, 10a, 10b, 10c → 14), com a trava S1b aberta só pela revisão aprovada.
4. Se o rito cair: `reverter_v407.py` é decisão da gerência; `refazer_candidato_v407.sh --regerar` refaz o candidato.

## 6. Módulos e âncoras

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `PsionCanto.lean` | 03nov_nome_aceito (antes: `PsionCantoR1`) | 8 | 18 | `55f30fe7d63e88c6` |
| `Par.lean` | 03nov_nome_Par (antes: `OParDePsionsR1`) | 5 | 5 | `fa4945d78e1a9f6c` |
| `APonteDoAtrito.lean` | 02nov_ratificada (antes: `APonteDoAtritoCandidata`) | 12 | 15 | `bd8ae49e7341fcdb` |
| `OUmInscrito.lean` | 02nov_ratificada (antes: `OUmInscritoCandidata`) | 7 | 7 | `acae38720f7e9204` |
| `KEhATangente.lean` | 02nov_ratificada (antes: `KEhATangenteCandidata`) | 12 | 15 | `fe263ee12920e04f` |
| `AChaveDaGuarda.lean` | 02nov_ratificada (antes: `AChaveDaGuardaCandidata`) | 7 | 8 | `135361a9105e11de` |
| `OGuarda.lean` | 02nov_ratificada (antes: `OGuardaCandidata`) | 9 | 11 | `d1362e297540b159` |
| `LeituraPreservada.lean` | 02nov_ratificada (antes: `LeituraPreservadaCandidata`) | 4 | 4 | `aeab7e30d907f562` |
| `OIgual.lean` | 02nov_ratificada (antes: `OIgualCandidata`) | 12 | 15 | `b60fa5c49d8b0a79` |

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces` | `TGLExt/PsionCanto.lean` | `ext_psi407_0097` |
| `TGLExt.Par.o_par_de_psions_e_o_graviton` | `TGLExt/Par.lean` | `ext_psi407_0076` |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v407_candidato.py` | 43,065,098 | `833121339e649f71` |
| `CANDIDATO_v407.json` | 121,166 | `8cee850183098f16` |
| `ESPERADOS_v407.json` | 1,023,706 | `c7afcff02580e3a9` |
| `ensaio_a_seco_v407.json` | 368,929 | `5910f6d7ca8b05c9` |
| `COMPARACAO_V406_v407.json` | 11,116 | `fcce158e5e66a02d` |
| `PINOS_BN_v407.json` | 5,085 | `59ed55a4a4043d31` |
| `PINO_RECIBO_PRE_SELO_v407.json` | 6,215 | `6fc53a82f7a4d7f2` |
| `PROVA_PRODUCAO_INTACTA_v407_pre_selo.json` | 10,061 | `11d09094a7855b03` |
| `PRECONDICOES_v407.json` | 22,132 | `2a3ea14ca5e4375c` |
| `GUARDA_FRASES_v407.json` | 14,411 | `e67e08c084b96540` |
| `VERBATIM_CONGELADO_v407.json` | 591 | `129aef7d14fb9f75` |
| `BUNDLE_v407.json` | 5,644 | `6121ff5a51334dc3` |
| `kernel_modulos_novos_v407.json` | 585 | `d2bc58a04a974273` |
| `CONTRATO_DA_CADEIA_v407.md` | 13,660 | `93e4eb01da17e381` |
| `DESENHO_v407.md` | 17,789 | `044cf92590aa36a7` |
| `PLANO_v407_GERENCIA.md` | 5,898 | `4927effb89ac9f6f` |
| `delta_v407.py` | 38,792 | `58f280bc19863cf3` |
| `registros_v407.py` | 38,717 | `016106f0ccc29019` |
| `runtime_v407.py` | 19,910 | `bd623db2bf04c136` |
| `guarda_frases_v407.py` | 15,345 | `15a373c3a499fd2d` |
| `guarda_ordem_de_chamada_v407.py` | 16,323 | `7f9a9b5b7b3b1598` |
| `gerar_candidato_v407.py` | 50,354 | `9d2638e63c8dc94a` |
| `gerar_esperados_v407.py` | 34,569 | `6e99ffe7ceefc746` |
| `artigo_pt_v407.pysnip` | 11,047 | `a80f672d8f3c7ec7` |
| `artigo_en_v407.pysnip` | 11,573 | `38203865cb7900d6` |
| `comparar_v406_v407.py` | 28,841 | `4651222591e4f708` |
| `instalar_v407.py` | 10,960 | `19981c6e6fe7a0b9` |
| `reverter_v407.py` | 5,505 | `aa85f2c2d2f1e9bf` |
| `rito_v407.sh` | 25,872 | `7464bc49ee85af41` |
| `conferir_rito_v407.py` | 83,369 | `fd636f57f2d1e29f` |
| `conferir_citacoes_v407.py` | 30,690 | `c5f3e91d60c3e0df` |
| `p00_precondicoes_v407.py` | 36,263 | `e1094da7bdd3ed0d` |
| `pos_rito/textos_v407.semente` | 127,502 | `1a40fdc7a0a0ca50` |
| `pos_rito/montar_textos_v407.py` | 6,293 | `e46472aa893b317a` |
| `pos_rito/leitura_v407.py` | 124,433 | `b36c6b5e903e074c` |
| `pos_rito/fechar_v407.py` | 25,208 | `a395b7c56a344f0e` |
| `pos_rito/registrar_mapa_v407.py` | 48,548 | `f62887c008641e00` |
| `pos_rito/superficies_v407.py` | 18,689 | `630aada257d70fea` |
| `pos_rito/harness_textos_ensaio_v407.py` | 165,348 | `a280751a25f0b5b0` |
| `pos_rito/harness_fechar_sandbox_v407.py` | 109,670 | `705392ba571b36e6` |
| `pos_rito/chain_pos_rito_v407.sh` | 39,835 | `dcbdab71a8db20c1` |
| `pos_rito/gerar_x_custodia_v407.py` | 5,084 | `d616b6a19f3f26f1` |
| `pedra/PsionCanto.lean` | 14,452 | `55f30fe7d63e88c6` |
| `pedra/Par.lean` | 7,229 | `fa4945d78e1a9f6c` |
| `pedra/APonteDoAtrito.lean` | 9,855 | `bd8ae49e7341fcdb` |
| `pedra/OUmInscrito.lean` | 4,164 | `acae38720f7e9204` |
| `pedra/KEhATangente.lean` | 8,463 | `fe263ee12920e04f` |
| `pedra/AChaveDaGuarda.lean` | 4,859 | `135361a9105e11de` |
| `pedra/OGuarda.lean` | 5,486 | `d1362e297540b159` |
| `pedra/LeituraPreservada.lean` | 3,036 | `aeab7e30d907f562` |
| `pedra/OIgual.lean` | 6,717 | `b60fa5c49d8b0a79` |
| `kernel/KERNEL_RECIBO_v407.json` | 203,202 | `210ad396fc6494cf` |
| `kernel/FLAGS_v407.json` | 41,530 | `19d1622c530910d7` |
| `kernel/KH_N1_v407.json` | 1,131 | `7fb73fa70cc8335e` |
| `kernel/POS_BUILD_v407.json` | 27,005 | `f647800c5194c80c` |
