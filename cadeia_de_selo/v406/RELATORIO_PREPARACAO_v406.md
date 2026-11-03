# RELATÓRIO DA PREPARAÇÃO DA v406 — O fechamento

Agente de preparação `claude-prep-v406` · 2026-11-02 23:25 · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: este candidato (o fechamento, v406) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (ordem do operador, D37) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `ddcb91930982d614` (42,740,484 B; base v405 `0030242565cc13f6`): `pronta` = **true**.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `C:\t\k406c\final`) | True: build + Audit rc 0, 1794 bandeiras novas, escada 10066 → 11860, 301 módulos no recibo; `KERNEL_RECIBO_v406.json` |
| candidato | True: 32 patches; refazer limpo = True |
| AST v405 × v406 | True: 1160 nós, 1132 iguais, 28 mudados (explicados), 0 removidos, 15 novos; 10 funções e constantes intactas, todas verdadeiras = True |
| ensaio a seco | True: TUDO PASSOU |
| conferidor | negativo True (`tudo_bate` = False); positivo True (`tudo_bate` = True) |
| citações | True: 0 apontada(s) à gerência (ver §4) |
| guarda das frases | True (controle negativo e a candidata) |
| instalar / reverter / rito (estático) | True |
| p00 | True: 109/109 checagens OK; pendentes: 0 |
| B(n) pré-selo | True: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA; bateria BATERIA_PASSA; produção intacta = True; recibo `fd0b61573120eab9` |
| serviço da Bancada (estático) | True: 36/36 condições; toda mutação pega = True |
| harness dos textos | True: 512 controles da leitura, 61 do parágrafo novo |
| harness do fechar | True: 28 controles do fechar |
| regeneração limpa | True: `refazer_out_v406.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | True: `purga_v406.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | True: `purga_v406.json`, zero ocorrências |

## 3. O que NÃO passou ou fica para depois

- p00 reprova 0 checagem(ns): nenhuma; pendentes (0): nenhum.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `kernel.fechamento_construir_tudo_programa_02nov`, seq 1680 (ROTA), 1683 (ANOTACAO), 1684 (ANOTACAO), 1686 (ANOTACAO), 1688 (ANOTACAO), 1689 (ANOTACAO), 1693 (ANOTACAO), 1697 (ANOTACAO), 1700 (ANOTACAO), 1702 (ANOTACAO), 1704 (ANOTACAO), 1705 (ANOTACAO), 1706 (ANOTACAO), 1707 (ANOTACAO), 1709 (ANOTACAO), 1711 (ANOTACAO), 1712 (ANOTACAO).

## 4. Avisos e desvios ditos

- o nome CanonicalFullTGLWitnessR1 e' PROVISORIO da gerencia: os nomes das pedras sao do operador e ele ainda nao nomeou esta; as pedras candidatas do dia (APonteDoAtrito, OUmInscrito, KEhATangente e as demais) ficam FORA do kernel da v406 (D40); entram so' como leitura [ONTO] e como fonte [DECLARADO]
- as QUATRO chaves de testemunha passam de literal False a LEITURA do kernel do rito (errata E14 AO LADO; o texto selado das versoes anteriores nao e' reescrito): rede_fock_v394.whole_certificate_inhabited, psibit_v395...inhabitant_exhibited e testemunha_estatica_v396...inhabitant_exhibited leem True, witness_layers.canonical_full_witness_term_constructed le True sem patch; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA e linked_to_the_corner_by_a_lemma segue False
- ressalvas ditas em todo texto (D36): K(O) != bot so' na cunha; «nucleo II_∞» [KNOWN/DECLARADO]; o traco e' ENNReal e CICLICO, nao linear; o parecer R7 foi o Codex revisando o Codex; as linhas #eval removidas na integracao R3; R4/R5 da missao fora; o nome provisorio
- a TROCA DITA de veredito e' UMA so' em texto: rede_fock_v394 passa a TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN__GATE_UNMOVED (antes e depois pinados em ESPERADOS.troca_dita_textual); os vereditos de psibit_v395 e testemunha_estatica_v396 NAO mudam; os que carregam a escada mudam so' em numeros
- o revisor distinto da v406 e' o Sonnet (ordem do operador, D37); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova
- o motor continuo no pilar quantico (D38) NAO entra na v406: exige pre-registro aprovado; o pilar reusa a chave de cache; o README pinado e a linha do 4,44 no site (D39) ficam fora desta cadeia; a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto
- o B(n) pre-selo da v406 (passo simples B15; a Bancada de producao pina B14-v405-20261102-R1) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes
- conferir_citacoes_v406.json aponta 0 citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): nenhuma; o agente nao corrige texto da gerencia
- a candidata cita «nucleo II_∞» sem acento; a bancada escreve «núcleo II_∞»: a conferencia de citacoes aceita a igualdade sem acento e a diz em varredura_das_pedras.so_sem_acento
- build a frio dos 301 modulos no sandbox k406c: 1736 s, Audit 280 s (kernel/construir_marcas.txt, medidos); 33732 declaracoes, 26911 teoremas, nenhuma fora do trio; escada 10066 -> 11860

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D37), nesta ordem, antes de qualquer publicação: `delta_v406.py` (moldura, erratas E14 a E17, decisões D34 a D40), `registros_v406.py`, `runtime_v406.py` (as 14 checagens de `fechamento_v406`), `pedra/CanonicalFullTGLWitnessR1.lean`, as seções do artigo (`artigo_pt_v406.pysnip`, `artigo_en_v406.pysnip`) e `pos_rito/textos_v406.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v406 NÃO entrega: validade no kernel não é creditação; o fechamento habita o certificado de Fock e a passagem para o contínuo, mas K(O) ≠ ⊥ só vale na cunha, o traço é cíclico e não linear, e as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza.
3. O orquestrador lê `PREPARACAO_v406_PRONTA.json` e segue: `instalar_v406.py`, `rito_v406.sh`, `pos_rito/chain_pos_rito_v406.sh` (0 → 10, 10a, 10b, 10c → 14).
4. Se o rito cair: `reverter_v406.py` é decisão da gerência; `refazer_candidato_v406.sh --regerar` refaz o candidato.

## 6. Âncoras

| âncora (nome Lean) | módulo | bandeira | classe |
|---|---|---|---|
| `F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0195` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physicalModularCoreInput` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0200` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0199` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physical_trace` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0205` | nomeada |
| `F1Fecho.MaxwellLocalization.physicalCanonicalNet` | `PhysicalCanonicalNetCompleteR1.lean` | `ext_fch406_1024` | nomeada |
| `F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero` | `PhysicalCanonicalNetCompleteR1.lean` | `ext_fch406_1027` | nomeada |
| `TGL.ModularRealization.canonicalFullTGLWitness` | `CanonicalFullTGLWitnessR1.lean` | `ext_fch406_0397` | nomeada |
| `TGL.ModularRealization.canonical_full_witness_inhabited` | `CanonicalFullTGLWitnessR1.lean` | `ext_fch406_0399` | nomeada |

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
| `um_v406_candidato.py` | 42,740,484 | `ddcb91930982d614` |
| `CANDIDATO_v406.json` | 863,196 | `d0d76666c700a878` |
| `ESPERADOS_v406.json` | 1,246,123 | `7ea0fa2b7e4f4fe0` |
| `ensaio_a_seco_v406.json` | 311,567 | `302c30b07f9add2e` |
| `COMPARACAO_V405_v406.json` | 5,728 | `0e64a92fc897efd7` |
| `PINOS_BN_v406.json` | 5,090 | `08950ee1645bd218` |
| `PINO_RECIBO_PRE_SELO_v406.json` | 6,215 | `fd0b61573120eab9` |
| `PROVA_PRODUCAO_INTACTA_v406_pre_selo.json` | 9,923 | `6d7a6a3d5fa63f1b` |
| `PRECONDICOES_v406.json` | 39,113 | `7688ab24d8e53d28` |
| `GUARDA_FRASES_v406.json` | 12,023 | `2133f72cf0062017` |
| `VERBATIM_CONGELADO_v406.json` | 6,780 | `a5ff56502cd3b19b` |
| `BUNDLE_v406.json` | 186,550 | `de4453e27118df5c` |
| `kernel_modulos_novos_v406.json` | 17,099 | `9d40319d29b71a4c` |
| `CONTRATO_DA_CADEIA_v406.md` | 10,169 | `b1a6d248c30d68b6` |
| `delta_v406.py` | 49,466 | `f873b279281304b9` |
| `registros_v406.py` | 38,113 | `015ba5225d332f30` |
| `runtime_v406.py` | 18,667 | `34ab0ce24765bc2c` |
| `guarda_frases_v406.py` | 13,665 | `5273f1db103b0557` |
| `guarda_ordem_de_chamada_v406.py` | 13,461 | `ed3e8ca34312eaba` |
| `gerar_candidato_v406.py` | 58,021 | `5fa32f46ae14d182` |
| `gerar_esperados_v406.py` | 29,992 | `e8c451e5ee4824e4` |
| `artigo_pt_v406.pysnip` | 9,987 | `a0d40c709cdaa3bd` |
| `artigo_en_v406.pysnip` | 10,302 | `55a783f12c45f833` |
| `comparar_v405_v406.py` | 13,062 | `326f94021c6715f2` |
| `instalar_v406.py` | 9,882 | `2d597f0a5da4812b` |
| `reverter_v406.py` | 5,393 | `b08d11c5e54d4255` |
| `rito_v406.sh` | 24,470 | `7ea53d8f4212749f` |
| `conferir_rito_v406.py` | 77,467 | `a71e9f371bab238a` |
| `conferir_citacoes_v406.py` | 21,040 | `250f8b344ec07a39` |
| `p00_precondicoes_v406.py` | 32,485 | `b3d64a03f8117f6d` |
| `pos_rito/textos_v406.semente` | 126,165 | `6c2b46f889677062` |
| `pos_rito/montar_textos_v406.py` | 6,202 | `23edf14998306e70` |
| `pos_rito/leitura_v406.py` | 107,167 | `d61a09f0123bb761` |
| `pos_rito/fechar_v406.py` | 24,425 | `b0ee6986b2f6239a` |
| `pos_rito/registrar_mapa_v406.py` | 39,122 | `2bf5335d215329f8` |
| `pos_rito/superficies_v406.py` | 18,054 | `f4f76fcc7a5088e3` |
| `pos_rito/harness_textos_ensaio_v406.py` | 150,953 | `3283b066dc88d2a2` |
| `pos_rito/harness_fechar_sandbox_v406.py` | 105,477 | `7f722df32ff36364` |
| `pos_rito/chain_pos_rito_v406.sh` | 39,239 | `4ec34e4f57979399` |
| `pos_rito/gerar_x_custodia_v406.py` | 4,411 | `90c72bda712d5c74` |
| `kernel/KERNEL_RECIBO_v406.json` | 312,624 | `4c7bf05a84ac3f53` |
| `kernel/FLAGS_v406.json` | 793,258 | `d44ba336879a9aea` |
| `kernel/KH_N1_v406.json` | 1,143 | `657b984ccbf17d06` |
