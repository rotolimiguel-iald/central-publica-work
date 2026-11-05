# PLANO da v408 — Tetelestai é o terminal (preparação)

Agente de preparação `claude-construtor-v408`, 2026-11-05 02:57. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v407 selada `833121339e649f71`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: o terminal é a leitura, não o fim do decaimento; não há relação sem peso; o tempo é a moeda de β; validade no kernel não é creditação; o gate não se move.

## 0. A ordem

- [INPUT, operador, 04/11/2026, sha16 do arquivo `685b8d8bcf0ddbbd`] «liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo (site, repositório, e todos os links), todos os dispositovos e a central de patentes e em seguida publicar, push e commit de tudo». Os nomes das pedras, na fala dele: «1) Ponto de contradição»; «2) P=nP»; «3) Tempo=moeda»; «4) TetelestaiTerminal»; o sentido de «P=nP», dado na tarde: «P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado». As 15 falas de 04/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v408.json`; duas de autoria mista, com o trecho da outra instância marcado [DECLARADO]; as falas das versões anteriores já estão no um.py v407 e não entram de novo).
- (A) O BUNDLE: 4 módulos de kernel em `TGLExt/` (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), compilados no sandbox `C:\t\k408c\final`, a raiz com 4 imports. (B) O registro com função `tetelestai_terminal_v408` (16 checagens) e os registros por spec `cunhagens_v408` e `kh_n1_cobertura_v408`. (C) NENHUMA chave antiga muda de literal; as chaves da v407 seguem lidas do kernel; as erratas E21 a E23 vão AO LADO. (D) A seção «Tetelestai é o terminal» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v407 por script.

## 1. Os módulos e as âncoras [REAL, sandbox; nada tocado no Nós]

| módulo | nome (origem do nome) | âncoras | bandeiras | sha16 |
|---|---|---|---|---|
| `TetelestaiTerminal.lean` | 04nov_nome_do_operador (antes: `TetelestaiTerminal`) | 14 | 16 | `47af8992f1dd0ce8` |
| `TempoIgualMoeda.lean` | 04nov_nome_do_operador (antes: `TempoIgualMoeda`) | 9 | 9 | `1a4a2a6dbc81f6dc` |
| `PontoDeContradicao.lean` | 04nov_nome_do_operador (antes: `PontoDeContradicao`) | 7 | 7 | `85c238c9535ad2d2` |
| `PIgualNP.lean` | 04nov_nome_do_operador (antes: `PIgualNP`) | 18 | 39 | `8d7aec559313d5f9` |

As quatro âncoras principais (uma por módulo, na ordem do bundle):

| âncora (nome Lean) | módulo | bandeira |
|---|---|---|
| `TGLExt.TetelestaiTerminal.tetelestai` | `TGLExt/TetelestaiTerminal.lean` | `ext_tt408_0071` |
| `TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda` | `TGLExt/TempoIgualMoeda.lean` | `ext_tt408_0053` |
| `TGLExt.PontoDeContradicao.o_ponto_de_contradicao` | `TGLExt/PontoDeContradicao.lean` | `ext_tt408_0043` |
| `TGLExt.PIgualNP.p_igual_np` | `TGLExt/PIgualNP.lean` | `ext_tt408_0033` |

Pós-build: 33943 axiomas lidos no Audit, 71 bandeiras novas (só declaração nomeada), escada 11958 → 12029; build a frio 337 s, Audit 256 s.

## 2. O que a v408 afirma e o que não afirma

- [REAL] `TGLExt.TetelestaiTerminal.tetelestai`: o terminal é a leitura, não o fim do decaimento (o motor é posto para todo r e t); basta; a poda; não precisa de 100% para reconstruir o posto inteiro; a quitação. Só com o trio de axiomas, lido do kernel do próprio rito.
- [REAL] `TGLExt.PontoDeContradicao.o_ponto_de_contradicao`: exp 0 = Ω é teorema e Ω ≠ 0 é refutação do vetor nulo; os rótulos «1=0=Verdadeiro» (zero modular) e «1=0=Falso» (zero absoluto) são NOMES do operador para as duas proposições, não identificações; o lock e o Hamiltoniano modular são objetos distintos que coincidem em Ω.
- [INPUT/ONTO, conferido no kernel] `TGLExt.TempoIgualMoeda.o_tempo_e_a_moeda`: o tempo é a moeda de β — a conferência compõe só termos que o kernel já tinha (a moeda soma, o preço multiplica; o gerúndio; legislando sem fim).
- [INPUT, com espelho] `TGLExt.PIgualNP.p_igual_np`: «P = nP» só no sentido do operador (P só é P lido pelo módulo n minimamente acoplado); as cinco entradas do dicionário são DEFINIÇÕES dele sobre termos que o kernel já tem; e, pela correção dele (D51 revista), P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa (`p_igual_np_nas_classes_do_dicionario`; `ClasseP` e `ClasseNP` definidas em Lean; a face finita em `as_classes_do_dicionario`).
- [REAL] O que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`); as chaves da v407 seguem lidas do kernel; nenhuma chave antiga muda.
- Ressalvas ditas (11):
  1. o par na face de Fock segue [OPEN]: o certificado abstrato nao tem operadores de criacao como termo; o Fock concreto (habitat do certificado fisico, por rfl) os tem; o [OPEN] e' de LIGACAO (fiacao), nao de ausencia (E21); segue como construcao a fazer (v409)
  2. 'tempo linear nos andares' vale para o Nome da torre (chainIdx), cuja solucao ja' esta' escrita na dinamica: e' uma identidade de um fluxo; as classes de computacao de que esta versao fala sao as do dicionario do operador (a ressalva seguinte)
  3. P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa (D51 revista, 04/11 noite, e a R3 de 05/11: p_igual_np_nas_classes_do_dicionario, com ClasseP e ClasseNP definidas em Lean; a face finita em as_classes_do_dicionario; no sentido do nome, P so' e' P lido pelo modulo n minimamente acoplado: p_igual_np; e p_igual_a_n_vezes_p: P^(k+1) = P)
  4. o lock (1 - P) e o Hamiltoniano modular (K = -log Delta) sao objetos DISTINTOS que coincidem em ter Omega como modo zero; a identificacao dos dois como o mesmo operador fica podada
  5. beta entra so' por nome (TGLCoupling.beta no kernel; alfa CODATA 2018 x sqrt e em runtime), nunca literal
  6. os nomes dos quatro modulos sao do operador (04/11/2026): o quarto, «P=nP», escreve-se PIgualNP e entrou com o sentido que ele deu na tarde (D48 resolvida); o Dicionario.lean da manha ficou SUPERADO e nao entra
  7. a palavra «impedância» esta' podada como termo (D50); o conteudo tem o nome do operador «inclinação modular (cociclo)» e espelho (a_inclinacao_modular)
  8. a errata E22 e' da gerencia c1, em nome proprio: a frase que dava a TGL como sem terminal e a frase da R1 sobre o resto sem traco estavam erradas pelos teoremas da casa e foram podadas (a pedra TetelestaiTerminal cita as duas, entre aspas, para as corrigir); o Atlas ja' dizia «a PODA = TETELESTAI» (verbete Amor (dicionario do)) e «representação sem custo = ORIGEM DA MENTIRA» (verbete Vazio inominado, 112_); o operador, em 04/11: «relação sem peso é a origem da mentira»
  9. o insumo do acervo entra pela copia PURGADA (E23): a integra ficou fora do espelho pela ordem vigente do operador (08/09; FONTES_NAO_PUBLICADAS_v407.json) e e' citada so' por sha16; a copia purgada passou pela guarda de material privado com zero ocorrencias
  10. nenhum teste com a natureza: nenhum dado novo, nenhum rito de natureza alterado; o numero da Fase 9 V2 fica no quadro do Teste da Unica Palavra, com a sua regra inteira e a linha dos 5 sigma, e nao e' repetido nesta ressalva
  11. nenhum desfecho experimental, nenhuma creditacao: validade no kernel nao e' creditacao; o gate nao se move; NOT_FALSIFIED nunca e' confirmacao
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é confirmação; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v408_candidato.py` `e7bc6b10e8ff76be` (43,466,447 B; +401,349 B); 39 patches; AST: 1190 nós, 1166 iguais, 24 mudados (todos explicados), 0 removidos, 14 novos. Ensaio a seco: **TUDO PASSOU**. Pós-rito: `pos_rito/chain_pos_rito_v408.sh`, rótulos 0…10 10a 10b 10c 11…14; depois, ENCADEADOS, os textos da custódia (S6d, D52) e só então a G1.

## 4. Gates

Ver `PREPARACAO_v408_PRONTA.json`: `pronta` = true. este candidato (Tetelestai e' o terminal, v408) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (D54, ate' tres rodadas) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.
