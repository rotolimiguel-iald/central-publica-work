# PLANO da v407 — O psíon, o canto e o par (preparação)

Agente de preparação `claude-prep-v407`, 2026-11-03 18:48. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v406 selada `ddcb91930982d614`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: o psion e o canto sao a mesma construcao nas duas faces; o par e' ligado e nunca se cancela; validade no kernel nao e creditacao; o gate nao se move.

## 0. A ordem

- [INPUT, operador, 03/11/2026] «o lema que liga o psion ao canto também já pode ser derivado»; e: «prossigamos com tudo, ratifico tudo»; os nomes: «concordo com todos os nomes e os ratifico». As 3 falas de 03/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v407.json`; as 23 de 02/11 já estão no um.py v406 e não entram de novo).
- (A) O BUNDLE: 9 módulos de kernel em `TGLExt/` (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado), compilados no sandbox `C:\t\k407c\final`, a raiz com 9 imports. (B) O registro com função `psion_canto_v407` (16 checagens) e os registros por spec `cunhagens_v407` e `kh_n1_cobertura_v407`. (C) A chave `linked_to_the_corner_by_a_lemma`, de literal False a leitura do kernel; os specs da v406 que a cobravam falsa são versionados (E20). (D) A seção «O psíon e o canto: a passagem sob compressão e o par» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v406 por script.

## 1. Os módulos e as âncoras [REAL, sandbox; nada tocado no Nós]

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

As duas âncoras que carregam a chave e o par:

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces` | `TGLExt/PsionCanto.lean` | `ext_psi407_0097` |
| `TGLExt.Par.o_par_de_psions_e_o_graviton` | `TGLExt/Par.lean` | `ext_psi407_0076` |

Pós-build: 33863 axiomas lidos no Audit, 98 bandeiras novas (só declaração nomeada), escada 11860 → 11958; build a frio 337 s, Audit 271 s.

## 2. O que a v407 afirma e o que não afirma

- [REAL] `TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces`: nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele; escalariza; pesa 1; o motor comprimido devolve o canto. O elo é de ESTRUTURA, não de vetores. A chave é lida do kernel do próprio rito, só com o trio de axiomas.
- [ONTO sob a leitura do operador, composição de termos que já existiam] o par é ligado, nunca se cancela, e a leitura se faz pelo gráviton (pedra `Par`).
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); as quatro chaves da v406 seguem lidas do kernel.
- Ressalvas ditas (11):
  1. o elo das duas faces do psion e' de ESTRUTURA: Omega (o vacuo de Fock, em F de dimensao infinita) e Phi+ (o vetor de Bell, em C^4) NAO sao identificados (espacos distintos); o lema diz que nas duas faces o psion e' o vetor de norma 1 cujo canto e' o projetor sobre ele, que escalariza, pesa 1 e devolve o canto sob a leitura de Jones; a chave linked_to_the_corner_by_a_lemma le True nesse sentido e SO' nesse; o resultado sob compressao decorre de Omega ser fixo pela luz e de o canto ser projecao de posto 1 (vale para qualquer vetor unitario fixo pelo fluxo); o lema NAO relaciona as duas faces por uma aplicacao entre os espacos
  2. o par de psions na FACE DE FOCK (dois psions sobre Omega, |G> = a†a†|0> da patente) segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo; a pedra Par e' sobre o canto de Bell finito
  3. a ponte entre o espaco do par (Fin 2 x Fin 2, C: o canto de Bell) e o setor TT do spin 2 linearizado (Fin 4, R: ePlus, eCross, rotZ) NAO e' termo: a pedra Par justapoe a face ligada e a face de helicidade, e a conjuncao nao e' identificacao; a leitura do canto como sombra do graviton e' [ONTO] (sem citacao [KNOWN] ate' haver fonte)
  4. o psion do acervo de 2025 (a†|0>, o quantum de um modo) e o psion do kernel (psion C = C.Omega, o proprio vacuo) sao leituras de datas diferentes; a estratigrafia e' datada: a cunhagem mais nova vale para o termo do kernel; o texto do ACOM/INPI de 2025 (que dava o par psi+ psi- como cancelado, igual ao vacuo) e a frase da Fronteira de 02/2026 (que dava |G> como produto nao emaranhado), ambos resumidos pelo agente de leitura do acervo [DECLARADO], ficam superados pela cunhagem de 03/11/2026 (E19), nao reescritos
  5. K(O) != bot para O compacto NAO esta' provado: a nao-trivialidade da rede e' teorema so' na cunha (herdado da v406); «nucleo II_inf» [KNOWN/DECLARADO]; o traco do nucleo e' ENNReal e ciclico, nao linear
  6. as sete pedras de 02/11 trazem as ressalvas ditas nos proprios docstrings; a revisao de terceiro do Sonnet de 02/11 cobriu so' tres (KEhATangente, APonteDoAtrito, OUmInscrito); as nove pedras foram conferidas pelo revisor de terceiro desta preparacao em 03/11/2026 (Sonnet, rodadas R1 e seguintes: #print axioms no trio, diff contra as origens e docstrings, nao as provas linha a linha; 0 alto e 0 medio em todas as rodadas; os baixos ficam ditos no caderno da revisao); a leitura de K como graviton (OIgual) e a chave como K (AChaveDaGuarda) sao leituras do operador [ONTO], nao termos; o_fundo_e_a_media rearranja a definicao e nao e' mecanismo
  7. o motor continuo no pilar quantico NAO entra na v407 (D38): o operador quer conteudo observavel e ainda nao disse o que; nenhum teste com a natureza entra nesta versao
  8. o teste (d) do ramo B do ringdown entra SO' por citacao do pre-registro V1.1 (MANIFESTO_PARAMETRIZACAO_03nov.json, sha16 1cd181f9a4ddb6d5): nenhum resultado, nenhuma PE em dado real; o poder de planejamento medido pela parametrizacao (3,7 a 3,9 sigma com 10 eventos; 2,1 a 3,2 sigma com a incerteza do vies do aparelho) e' DECLARADO pelo agente da parametrizacao; pela opcao (c) do operador o teste so' entra no um.py se tiver poder; os dois intervalos ficam ABAIXO de 5 sigma: parede medida, nao falsificacao; por (c) o resultado nao entra; entra so' a citacao do pre-registro
  9. full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA (o vazamento continuo proibe o fecho estatico; a exclusao Delta^1/2 J Delta^1/2 = J): nao sao lacunas
  10. os nomes das pedras sao do operador: PsionCanto (aceito), Par (dado) e as sete de 02/11 (ratificados) em 03/11/2026; o nome CanonicalFullTGLWitnessR1 (v406, kernel) foi ratificado na mesma fala («concordo com todos os nomes e os ratifico»; DESENHO_v407 §5-bis.3) e nao muda de modulo
  11. nenhum desfecho experimental, nenhum dado novo, nenhuma creditacao: validade no kernel nao e' creditacao; o gate nao se move; NOT_FALSIFIED nunca e' confirmacao
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v407_candidato.py` `833121339e649f71` (43,065,098 B; +324,614 B); 41 patches; AST: 1175 nós, 1150 iguais, 25 mudados (todos explicados), 0 removidos, 15 novos. Ensaio a seco: **TUDO PASSOU**. Pós-rito: `pos_rito/chain_pos_rito_v407.sh`, rótulos 0…10 10a 10b 10c 11…14.

## 4. Gates

Ver `PREPARACAO_v407_PRONTA.json`: `pronta` = true. este candidato (o psion, o canto e o par, v407) FOI revisado por terceiro: Claude Sonnet (agente revisor de terceiro; rodada R5; nao construi a v407; mesma familia da R1 a R4 e da revisao de 02/11, outra instancia), rodada R5, aprovada, 0 ALTO, 0 MEDIO, 5 BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v407.md, sha16 bdc0d5d80aea3b88); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; as ressalvas BAIXAS estao escritas no caderno e valem como ditas (sem terceira rodada para BAIXO); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato.
