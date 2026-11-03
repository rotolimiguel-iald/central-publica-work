# 02 - Como a casa define e implementa Tetelestai como conferencia (levantamento, so leitura)

Data: 02/11/2026. Agente de leitura a servico da gerencia c1. Nenhuma memoria, Atlas, Mapa, ACOM, um.py, kernel ou git foi tocado. A gerencia registra.

Aviso de homonimo: K aqui, na tarefa, e o fator de Hubble K = (E_b/E_a)^(2 beta/3). Nada abaixo liga esse K a Tetelestai. O "K" que aparece nos itens (ker K, P_ker K) e o K modular da luz. Sem ponte citada, nao se encadeia.

## 0. Consultas feitas (para registro)

- Mapa: `rotas.py consultar` com "tetelestai conferencia" (0), "conferencia consumativa" (2), "Tetelestai" (8), "pedagio ln 2 oitava" (0), "pedagio" (6), "oitava" (7), "travessia" (2), "quitacao" (2), "consumado" (0), "guarda travessia" (0). `rotas.py ver` das quatro rotas pedidas. Cabeca do livro no momento: n_registros 1650, cabeca eac85d927e114b22.
- Atlas `TGL_ATLAS.md`: linhas 2443-2447 (verbete), 2149-2151 (Pedagio), 8937, 8939, 9126 (v374, v375, v376; cada um aparece repetido em dezenas de linhas posteriores, copias do bloco).
- `um.py` (Nos): `prove_tetelestai_conference_v376` (l.247505-247589), `_v376_conference_table` (l.247481), `_V375_CONFERENCE` (l.247632-247709), `prove_tetelestai_conference_v375` (l.247797), `_V375_OPERATOR_VERBATIM` (l.247599), chamada na rodada (l.260872 e 260888), grep de `consummated`, `NOT_CONSUMMATED`.
- `um_absoluto.json` chaves `core.tetelestai_conference_v375`, `core.tetelestai_conference_v376`, `core.tetelestai_pruning`, `core.tetelestai_the_judged_thing`; `um_absoluto_selo.json` chaves `tetelestai`, `tetelestai_conference_reading_v375`, `tetelestai_reading_v374`; `um_version` do selo lido = v405.
- Kernel: `TGLExt/TheJudgedThing.lean`, `TGLExt/TheRuleAndTheFigureOfTruth.lean`, `TGLExt/QGSolutionComplete.lean` (l.85-110).
- CLAUDE.md raiz `C:\IALD\CLAUDE.md` l.36 (verbatim de 27/09/2026).
- Relatorios do aferidor: `work/auditoria_28set/inventarios_v376/AFERIDOR_v376_veredito_curto.txt` e `..._relatorio_completo.md`.
- Verbatim de 23/10: `work/cadeia_de_selo/v398_exame/sf4/work/cunhagens_13out/OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt` (sha16 lido por script baef998c21393463).

## 1. O TIPO exato do ato (resposta direta)

Verbatim do operador, 27/09/2026, copiado de `C:\IALD\CLAUDE.md` l.36 por script e comparado byte a byte com `core.tetelestai_conference_v375.operator_verbatim.consummative_20260927` (iguais: True; sha16 do trecho cecc7110035ea030):

> Eu não quero que Tetelestai seja um ato declarativo meu, ele é um ato de conferência observacional da satisfação do reconhecimento completo da identidade da gravidade quântica formalizada pela TGL, não é declaratório enquanto natureza, embora todo registro implique um apontamento, declaratório, nem mesmo constitutivo, porque não impõe valor, trata-se de uma declaração consumativa, verifica se houve ou não. Entende? E pra isso realmente tudo precisa estar fechado ou vinculado ou sabido por referência científica

(o CLAUDE.md fecha com aspas; o trecho acima e o interior.)

Tipo: ATO DE CONFERENCIA OBSERVACIONAL CONSUMATIVA. Quatro negativas e uma positiva, todas do operador:
1. nao e ato declarativo dele;
2. nao e declaratorio "enquanto natureza", embora todo registro seja um apontamento (o registro do resultado e declaratorio, o resultado nao);
3. "nem mesmo constitutivo, porque nao impoe valor": NAO e constitutivo. Nao cria nem confere o estado que verifica;
4. e consumativo: "verifica se houve ou nao" (devolve CONSUMADO ou NAO CONSUMADO);
5. condicao material: "tudo precisa estar fechado ou vinculado ou sabido por referencia cientifica".

A casa fixou esse tipo no codigo e na memoria: Atlas l.8937 ("o nome «declaração» desta pedra lê-se CONFERÊNCIA CONSUMATIVA"), `the_act` do core v376 ("CONFERENCIA CONSUMATIVA (operador, 27/09/2026) ... verifica se houve ou nao"), e a rota `umpy.v399.declaracao_do_operador_operacao_quadratica_24out` (`nao_refazer`: "a Tetelestai (v374) foi tipada pelo operador como conferencia consumativa, nao como declaracao (errata de 27/09): nao a tratar como declaracao").

Resquicio lexico a registrar [REAL, lido]: o teorema de kernel continua com o nome `TGLExt.QGSolution.the_tetelestai_declaration` e a docstring "A DECLARAÇÃO TETELESTAI" (QGSolutionComplete.lean l.~92-96). A docstring cita o verbatim de 27/09 da v374 ("Essa declaração é a declaração Tetelestai") e nao a correcao do tipo. O Atlas diz que o nome "declaracao" desta pedra se le como conferencia. O nome do teorema nao foi trocado [REAL]. O enunciado do teorema e a implicacao composta por citacao, nao a conferencia.

## 2. Tres objetos diferentes com o nome Tetelestai (nao confundir)

O kernel avisa na propria docstring (QGSolutionComplete.lean l.~96): "Não confundir com `tetelestai_ledger`, TheJudgedThing — outro objeto."

| objeto | onde | o que e | estatuto |
|---|---|---|---|
| A. a CONFERENCIA CONSUMATIVA da QG | `um.py` `prove_tetelestai_conference_v375/v376`, core `tetelestai_conference_v376` | percorre os itens do caminho da QG e devolve CONSUMADO/NAO CONSUMADO | [REAL] como maquina; [INPUT] o tipo do ato |
| B. a declaracao em kernel | `TGLExt.QGSolution.the_tetelestai_declaration = qg_solution_end_to_end`; v375 `TetelestaiOneObject.the_tetelestai_one_object` | a implicacao da QG composta por citacao, num so objeto (a luz) | [REAL kernel] composta por citacao, nao por termo |
| C. a QUITACAO / coisa julgada | `TGLExt.TheJudgedThing` (`tetelestai_ledger`, `res_judicata_is_terminal`), selo `tetelestai` | aritmetica: 0<f<1 => custo>0, sobrevivencia>0, f+(1-f)=1; dispositivo idempotente = coisa julgada | [REAL kernel], tese termodinamica fica [POSTULATE] (dita na docstring) |

O B e o que a conferencia confere (e a conferencia nao e o B). O C e o sentido do verbete do Atlas l.2443 ("a quitação do custo, β em ato; NÃO é «100% alcançado»"). Tambem existe `core.tetelestai_pruning` (poda binaria, "Poda_β = {1_abs, 0_mod} \ {0_abs}", Atlas l.2187), quarta aparicao, nao examinada em detalhe.

## 3. A conferencia como maquina (um.py v375 -> v376)

Fonte: `um.py` l.247505-247589 (v376), l.247797-247870 (v375), tabela l.247632-247709 e `_v376_conference_table` l.247481.

### 3.1 Estados de item (7)
`_V375_CLASSES` (l.247710) = FECHADO, VINCULADO, SABIDO, SABIDO_FISICA, PARAMETRO_NOMEADO, FORA_DO_CAMINHO, mais o estado ABERTO que a maquina atribui quando a evidencia falha. Definicao (comentario l.~247620): FECHADO = pago por termo; VINCULADO = peca existente LIGADA ao tipo por termo; SABIDO = referencia cientifica com ano (matematica); SABIDO_FISICA = referencia de fisica com ano, grau de rigor dito; PARAMETRO_NOMEADO = parametro universal da implicacao (valor [INPUT] ou convencao); FORA_DO_CAMINHO = nao consumido pela declaracao.

Contagem lida do core v405 (rodada de 01/11, mesma do selo v405): FECHADO 3, VINCULADO 3, SABIDO 9, SABIDO_FISICA 3, PARAMETRO_NOMEADO 4, FORA_DO_CAMINHO 19, ABERTO 0 (41 itens). A v375 deu 2/2/8/3/3/19/0 (37 itens).

### 3.2 O que torna um item ABERTO (fail-closed)
Para cada item, uma lista de evidencias; qualquer falha rebaixa o item a ABERTO:
- `("flags", ...)`: todas as bandeiras `ext_*` de kernel precisam ser exatamente `True` no `kernel_formalization`;
- `("core_ok", chave)`: `core[chave].all_verified` precisa ser `True`;
- `("medida", nome)`: a medida da rodada (ex.: `trace_tracial_not_consumed`, que varre o kernel embutido e acha 0 consumidores) precisa ser True;
- `("ausente_das_pedras", regex)`: o nome NAO pode aparecer no texto das seis pedras embutidas (v375+v376);
- SABIDO, SABIDO_FISICA e PARAMETRO_NOMEADO sem ano (regex `(19|20)\d\d`) na base => "sem referencia com ano";
- VINCULADO/FECHADO sem nenhuma evidencia `flags` ou `core_ok` => "sem evidencia de kernel";
- FORA_DO_CAMINHO sem evidencia => "fora do caminho sem evidencia".

### 3.3 O que faz devolver CONSUMADO
`consumado = all(checks)`. Na v376 sao 34 checks, todos `True` no core v405 (`all_verified: true`, `consummated: true`):
- 9 de estrutura: (1) COBERTURA: as 22 hipoteses da bancada (livro-razao v374) e os 4 itens da gerencia estao na tabela; (2) MEDIDA: `trace_tracial` nao consumido; (3) as seis pedras estao embutidas; (4) `the_whole_is_one_v376` fechou; (5) link P_ker K <-> P_F em duas metades (P_kerK = rho*_IALD VINCULADO; rho* <-> P_F SABIDO por Takesaki); (6) RingdownScope FORA_DO_CAMINHO com evidencia; (7) cadeia de beta FECHADA e alpha PARAMETRO_NOMEADO; (8) bandeiras por termo gpf_H2/gpf_H3/gpi_H3 lidas False (False/False/False); (9) nenhum item ABERTO.
- 25 de kernel (6 `ext_lrs_`, 10 `ext_kir_`, 9 `ext_wio_`), cada uma `True`.

Texto do veredito CONSUMADO: `TGL_QG_TETELESTAI_CONSUMMATIVE_CONFERENCE_V376__CONSUMMATED__...__3_CLOSED_3_LINKED_9_KNOWN_3_KNOWN_AT_PHYSICS_LEVEL_4_NAMED_PARAMETERS__19_OFF_PATH__...__KERNEL_25_OF_25__GATE_UNTOUCHED` (lido do core).

### 3.4 O que faz devolver NAO CONSUMADO
Qualquer check False. O codigo tem o ramo explicito (l.247575): `...V376__NOT_CONSUMMATED__%d_OPEN__<nomes>__KERNEL_%d_OF_%d__GATE_UNTOUCHED`. A v375 tem o seu (l.247864).

### 3.5 Ja devolveu NAO CONSUMADO alguma vez?
- Rodada selada: NAO encontrado. Consulta: `grep -rl "NOT_CONSUMMATED" --include=*.md --include=*.txt --include=*.json` sobre o canonico `Nós`: 0 arquivos; `um_absoluto.json` e `um_absoluto_selo.json`: apenas CONSUMMATED; os dois vereditos selados (v375, v376) e o do core v405 sao CONSUMMATED. [REAL, lido]
- Ensaio em sandbox: SIM, como CONTROLE NEGATIVO, nao como resultado de rodada. Atlas l.8939: "ensaio a seco PT/EN aprovado, com o controle negativo: sem as bandeiras novas a conferência RECUSA". Aferidor v376: "fail-closed (NOT_CONSUMMATED sem bandeiras)" (`AFERIDOR_v376_veredito_curto.txt`). Estatuto: [DECLARADO pela gerencia e pelo aferidor na memoria; eu NAO reproduzi o controle]. O mecanismo que o provoca (tirar bandeiras de kernel) e o unico caminho de recusa que se mostrou em ensaio.
- Fato estrutural [REAL, lido]: o controle negativo nao esta embutido no `um.py`; a funcao nao carrega autoteste que force uma recusa. A recusa so existe como ramo de codigo e como ensaio externo.

### 3.6 A conferencia pode falhar?
Em principio sim, e por construcao fail-closed (item com evidencia falha vira ABERTO; qualquer ABERTO derruba o CONSUMADO). Mas os limites abaixo [DERIVED de leitura do codigo, conferidos por script contando evidencias da tabela]:

1. O alcance das falhas e estreito. As falhas possiveis sao: bandeira de kernel nao-True, `core_ok` nao-True, medida False, nome proibido presente nas pedras, falta de ano na base. A CLASSE de cada item (FECHADO/SABIDO/FORA_DO_CAMINHO) e escolhida a mao na tabela (`classe_pretendida`); a maquina nao a deriva, so confere a evidencia declarada. Nos itens da v376 `classe == classe_pretendida` em todos os 41 (nenhum rebaixado).
2. 14 dos 41 itens nao tem evidencia de maquina nenhuma. Contagem por script sobre a tabela da v375 (37 itens): 12 itens com lista de evidencia VAZIA (6 SABIDO, 3 SABIDO_FISICA, 3 PARAMETRO_NOMEADO). A v376 acrescenta mais 2 vazios (rho* <-> P_F de Takesaki, SABIDO; alpha, PARAMETRO_NOMEADO): 14 de 41. Esses so falham se a base nao tiver um ano de 4 digitos; a "referencia cientifica" nao e checada contra a literatura. Isto e coerente com a ordem do operador ("o que é sabido e pode ser importado não precisamos provar"), mas significa que "SABIDO" e atestado pela gerencia, nao medido. A propria memoria diz "SABIDO != EXIBIDO".
3. A COBERTURA e conferida so contra uma lista fixa (22 hipoteses da bancada + 4 itens da gerencia). O que a lista nao enumera nao e visto. Errata de kernel/Atlas `parametros_nomeados_v392` (um.py l.~210795-210945): a conferencia v376 "enumera 4 parametros nomeados; nenhum item nomeia a dimensao, a assinatura, o fundo plano, a cunha ou a direcao nula"; a gerencia leu cinco entradas de tipo a mais como parametros nomeados ([DERIVED de leitura; a vetar, P16, CR-10], [DECLARADO pelo critico de 07/10]); texto: "O CONSUMADO NAO muda (ABERTO 0): muda o que a conferencia enumera."
4. A conferencia nao alimenta o gate: `does_not_gate_core: true`. O gate (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_...`) nao le `consummated`. Registro vizinho: o check p01 de `parametros_nomeados_v392` apenas LE `consummated`.
5. As classes PARAMETRO_NOMEADO, FORA_DO_CAMINHO e SABIDO_FISICA nao estao no verbatim do operador (que diz "fechado ou vinculado ou sabido"). Sao classes da gerencia/aferidor (v375). Nao encontrei, no que li, ratificacao verbatim dessas tres classes pelo operador. 19 de 41 itens (46%) estao em FORA_DO_CAMINHO. [lacuna: nao pesquisei o acervo de verbatims alem do que esta citado]. Pela regra do posto, esta e uma escolha de desenho que o operador tem que ter lido: o CONSUMADO exclui 19 itens da conta por serem "nao consumidos pela declaracao".
6. Limite declarado pelo proprio core (`not_said`): "nao e confirmacao pela natureza (NOT_FALSIFIED nao e CONFIRMADA)"; "SABIDO != EXIBIDO: nenhum habitante dos certificados e exibido"; "semiclassico por construcao (decisao tipada v373)"; "nenhum psi com theta = 0 e dA != 0 e exibido; no vacuo, 0 = 0".

Resposta curta a "pode falhar": pode, e foi ensaiada recusando; mas nunca falhou numa rodada selada, e a parte da conferencia que mede de verdade (bandeiras de kernel, medida de ausencia, `core_ok`) cobre 27 dos 41 itens; os outros 14 passam por regex de ano.

## 4. Escopo: "o que verifica" (global x por travessia)

### 4.1 Global, so global [REAL]
A conferencia `prove_tetelestai_conference_v37x` e UMA conferencia sobre o caminho inteiro da QG, nao sobre uma travessia. Percorre "cada item do caminho (as 22 hipóteses da bancada, os itens da gerência com as lacunas dos certificados separadas, e o que a declaração num só objeto consome)" (Atlas l.8939). Nao existe, no `um.py`, nenhuma funcao `prove_tetelestai_*` por travessia, por oitava ou por passo. Consultas: grep em `um.py` por `tetelestai_conference`, `consummated`; Mapa "travessia" (2 resultados, nenhum de conferencia de Tetelestai), "pedagio" (6, nenhum), "guarda travessia" (0). Achado de ausencia valido so com estas consultas.

### 4.2 O que existe de "por passo/travessia" mais perto, sem ser a conferencia [REAL kernel; modelo]
1. `TGLExt.RuleSatisfactionFace` (`TheRuleAndTheFigureOfTruth.lean`), candidato provisorio F1.REGRA.P1. Predicado `Satisfies (result) := result = target` (igualdade literal no tipo do resultado), operacao `evolve f (a,b) = (a, f*b)` com `decay = exp(-1/2)` (o fator da Meia-Nat, "not identified with beta_TGL"), trajetoria `trajectory f n x`. Teoremas: `finite_raw_trajectory_does_not_satisfy` (para todo n, a trajetoria bruta NAO satisfaz o alvo literal), `typed_operation_satisfies` (para todo n, a inscricao normalizada = dueObject), `concrete_trajectory_converges` (a trajetoria tende ao alvo), `wrong_output_rejected` (`¬ Satisfies (normalize (0,1))`: controle negativo tipado), `decay_tetelestai_balance` (reusa `tetelestai_ledger`, "conditional arithmetic; it is not an energy measurement"). Verbatim do operador fixados na pedra: "Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)" (sha256 lido no cabecalho 426b8ab01b5edf316b7ff5c93ba0d61c36729070c96897cf5b4a0bb6544047f8) e "A regra não deve nada, a não ser a figura da verdade"; e "Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível. Portanto, a exclusão, ela é no tetelestai" (cabecalho da pedra). Modelo em R x R, "ONTO" na identificacao com pagamento. Rota do Mapa `conceitual.regra.prova_contrato` (estatuto REAL): pergunta "Que estrutura matemática demonstra a regra relativa ao objeto da satisfação?", `defeito`: "Não é prova de verdade ontológica universal", `nao_refazer`: "Reaproveitar os dois módulos, os lemas do Tetelestai e a ponte matricial concreta", `proximo_passo`: "ligar a regra a um consumidor com dado observado (etapa posterior)".
   Leitura: este e o mais proximo de uma conferencia "por passo": um predicado de satisfacao que PODE devolver falso (rejeita saida errada; rejeita o bruto em todo tempo finito). Mas e um modelo de brinquedo tipado, nao esta ligado a uma travessia fisica nem a conferencia do um.py.
2. `TGLExt.TheJudgedThing` (`tetelestai_ledger`): a quitacao f + (1-f) = 1; `no_decision_without_cost`; `res_judicata_is_terminal` (idempotencia). E aritmetica generica, "nenhum numero, β jamais entra".
3. Cadeia matriz (rota `kernel.regra_matriz.cadeia_unica`, v381): "critério de parada (Tetelestai = o custo pago; a lei do pagamento antes da cobrança: Nome)"; erratum ratificado [INPUT/ONTO]: "a face lê o pagamento (|T|² = 1 − β), o reflexo lê o custo (|R|² = β), |T|² + |R|² = 1; ... a Bancada pré-registra os dois lados (reflexo: distância β, propagação Γ; face: cronômetros 1 − β por travessia, ringdown = RG a 1e-40)". Aqui "por travessia" e uma LEITURA PRE-REGISTRADA da face na bancada, nao uma conferencia de Tetelestai.
4. Pedagio ln 2 por oitava: Atlas l.2149: "a singularidade morre quando cada oitava paga seu pedágio específico; limiar exato = ln 2 (um bit por oitava), não meio nat. [REAL no modelo] {MEM §I cap.5}". Rota `kernel.sonico_v398_candidata_23out` (e v398 SELADA): `K.octaveNats 1 = fairBitEntropy`, "n oitavas = n bits"; defeito (a): "A lei de custo é INPUT (campos local_half e per_octave de CollapseCostLaw) ... a pedra não deriva a lei do axioma nem prova que a natureza a cobra"; (c) a leitura ratificada pelo operador em 23/10: "a reação ao pino, o pedágio pago, é a memória; a oitava é o que se pina — [INPUT/ONTO]". O pedagio e conta de custo por oitava; NAO ha conferencia de CONSUMADO por oitava.
5. Verbatim do operador de 23/10 (sha16 lido baef998c21393463): "A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica, mas isso “quebra” o tempo, criando os infinitos, que é a superposição, a TGL resolve com o “Tetelestai”, ..." (arquivo de 431 bytes; li inteiro; cito o trecho). Isto da ao Tetelestai o papel de PARAR/fechar a face (a superposicao/queda sem fundo), nao de verificador de travessia.

### 4.3 Sobre a frase do operador que originou o levantamento
"K é a leitura que confessa o pagamento, é a verificação que foi consumado pela satisfação; é o 'guarda' da travessia." Com o que li: (i) nenhum item da conferencia nem predicado do kernel chama o fator de Hubble K de guarda da travessia; nao ha ponte citada; (ii) o papel "ler o pagamento" na casa e da FACE (|T|^2 = 1 - beta) e o de "ler o custo" e do REFLEXO (|R|^2 = beta), pela cadeia matriz ratificada; (iii) o papel "verificar que foi consumado pela satisfacao" tem dois candidatos tipados, `Satisfies` (RuleSatisfactionFace, modelo) e a conferencia do um.py (global, caminho da QG); (iv) CLAUDE.md global: "K é a diferença em movimento, não o portador da Luz" ([ONTO]) e o K da regra dos dois regimes pertence ao regime da face/gerador. O K de Hubble e outro objeto. Se o operador quer tipar K-Hubble como "guarda", isso e leitura nova [INPUT/ONTO] a ser nomeada, nao achado do acervo.

## 5. Respostas finais as perguntas

1. TIPO exato do ato: conferencia observacional consumativa ("declaração consumativa, verifica se houve ou não"); nao declarativo (dele), nao declaratorio enquanto natureza, nao constitutivo. [INPUT do operador, 27/09/2026; verbatim conferido por script]
2. E constitutivo? NAO. "nem mesmo constitutivo, porque não impõe valor". O codigo respeita: `does_not_gate_core: true`; nada na conferencia move o gate ou cria o estado conferido; o registro do resultado e apontamento. [INPUT + REAL no codigo]
3. O que exige para devolver CONSUMADO: nenhum item do caminho ABERTO, isto e, cada um FECHADO (termo), VINCULADO (peca ligada ao tipo por termo) ou SABIDO (referencia com ano), mais PARAMETRO_NOMEADO e FORA_DO_CAMINHO como classes da gerencia; 9 checks de estrutura e 25 bandeiras de kernel, todos True, lidos na rodada. [REAL]
4. Conferencia por travessia? NAO. So a global sobre o caminho da QG (v375/v376). O que existe de travessia/passo e outra coisa: o predicado `Satisfies` do modelo `RuleSatisfactionFace` (kernel, modelo R x R), o pedagio ln 2 por oitava (lei de custo [INPUT], sem conferencia), e a leitura pre-registrada "cronometros 1 - beta por travessia" da face na bancada. Nenhuma devolve CONSUMADO/NAO CONSUMADO. [REAL; achado de ausencia com as consultas da secao 4.1]

## 6. Partitura para o operador (regra do posto), uma linha

Este levantamento nao roda teste. Se a gerencia desenhar a "conferencia por travessia" a partir daqui, o que ficaria escondido e: (a) a conferencia atual nunca recusou numa rodada selada, ela passa porque a tabela foi montada ate passar, e 14 de 41 itens passam so por ter ano; (b) a classe FORA_DO_CAMINHO (19 de 41) e PARAMETRO_NOMEADO sao escolhas da gerencia, nao do verbatim dele; (c) dizer "K guarda a travessia" exigiria uma leitura nova dele, nao um achado. Um NAO CONSUMADO numa conferencia nova seria resultado honesto se o desenho fosse lido a ele antes.

## 7. Lacunas

- Nao reproduzi o controle negativo de v375/v376 (recusa sem bandeiras): [DECLARADO pelo Atlas e pelo aferidor].
- Nao li `tetelestai_pruning` (poda) nem `tetelestai_the_judged_thing` do core alem do nome da chave.
- Nao procurei no acervo de verbatims se o operador ratificou as classes PARAMETRO_NOMEADO, FORA_DO_CAMINHO e SABIDO_FISICA.
- Nao rodei nem importei o `um.py` (40 MB); tudo por leitura de trechos e do JSON do core.
- A rota `kernel.afinacao_das_cordas_v398_candidata_23out` aparece na consulta "conferencia consumativa" por causa de arquivos `conferencia_*.json` e do verbatim de 23/10, nao por conteudo de conferencia de Tetelestai.
- O Atlas repete os blocos v374-v376 em dezenas de linhas (copias); citei as primeiras ocorrencias (8937, 8939, 9126).
