> [nota operacional do operador — omitida no retrato público]

> [nota operacional do operador — omitida no retrato público]

## Entregas (por script, com sha16 lido do arquivo)

| arquivo | o que é | sha16 |
|---|---|---|
| `FOLHAS_SUBSTITUTIVAS_050576.pdf` | Aprendizado: 6 folhas A4 (substituem as 5 depositadas), vetorial; caixa [1] = «VACUUM/GRAV/PHO» (o que o depositado mostra) | `884d978a39b20d1a` |
| `ALTERNATIVA_FOLHA_1_050576_PHOT.pdf` | só a folha 1/6 com «PHOT» inteiro, para o agente de PI escolher (as folhas 2-6 são as mesmas) | `c60f4e9ca17c0e22` |
| `FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf` | VARIANTE PHOT completa: 6 folhas (1/6 alternativa + 2/6 a 6/6 iguais às principais), para ser enviada sozinha | `4417390dcbd5b998` |
| `CARTA_REGRA_26_4_050576.md` | carta Regra 26.4 (Aprendizado, folhas principais), minuta, assinatura em branco | `dbe1caff15ed32e4` |
| `CARTA_REGRA_26_4_050576.pdf` | idem, PDF | `a72a89c3571cb828` |
| `CARTA_REGRA_26_4_050576_PHOT.md` | carta da variante PHOT (frase da caixa [1] coerente com a folha alternativa) | `cff588eaff8c0a3e` |
| `CARTA_REGRA_26_4_050576_PHOT.pdf` | idem, PDF | `453663db5c4c0ff8` |
| `CONFERENCIA_050576.json` | medidas, testes novos, provas de identidade, cotejo de palavras, reparos antes/depois, sha256 de entradas e saídas | `d171e2bc9be9668e` |
| `FOLHAS_SUBSTITUTIVAS_050579.pdf` | MQC: 8 folhas A4 (substituem as 3 depositadas), vetorial | `4faa43ca81442fc5` |
| `CARTA_REGRA_26_4_050579.md` | carta Regra 26.4 (MQC), minuta, assinatura em branco | `29029f0a6e2b0c4c` |
| `CARTA_REGRA_26_4_050579.pdf` | idem, PDF | `2378f978494f2fdf` |
| `CONFERENCIA_050579.json` | idem para o MQC | `529ca8412ad6baa1` |

Também: `conferencia/prancha_antes_depois_<6>.png` (depositado em cima, substitutivo embaixo, mesma escala), `conferencia/reparos_rodada2.json` (medidas antes/depois), `conferencia/mqc_legendas_do_depositado.json`, `conferencia/*.json` (provas parciais), `ESTADO.json`, `entrada/`, `fontes/` (scripts), `_tmp/` (descartável; `_tmp\base\` guarda os PDFs da rodada 1 usados nas medidas «antes»).

## O que as folhas corrigem (e só isso)

Caixas marcadas, lidas nas imagens dos PDFs [REAL] — detalhe e método em `CONFERENCIA_<6>.json`:

> [nota operacional do operador — omitida no retrato público]

Corrigido: preto puro sobre branco, traço uniforme, letras e números com altura mínima de 0,32 cm, rótulos e legendas sem cobrir traço, A4 com margens 2,5/2,5/1,5/1,0 cm, sem moldura, numeração n/N centrada no alto, figuras numeradas como no depositado, **canto superior direito e margem inferior livres** para o carimbo do RO.

## Como foi feito

| | Aprendizado 050576 | MQC 050579 |
|---|---|---|
| desenhos como depositados | `04_DESENHOS.pdf` (5 folhas, sha16 1c09a448482ccc81); = páginas 19-23 do appb do ePCT (hash de imagem igual, folha a folha) | `04_DESENHOS_CINZA.pdf` do Codex (3 folhas, sha16 2ef675ed2a3d2a7c); = páginas 20-22 do appb do ePCT (idem) |
| fonte | LaTeX/TikZ de origem; **a compilação sem alteração reproduz o depositado** (correlação de forma 0,998-1,000 em 8/9; Fig. 4 = mesmo desenho) | funções de simulação do script de origem **sem alteração**; arrays de linhas/pontos/barras das Figs. 1-7 idênticos aos do script (max \|diff\| = 0, reconferido na rodada 2) e as 40 células da Fig. 8 idênticas |
| método | figuras redesenhadas em vetor (TikZ/pgfplots, xelatex, Arial Narrow 15 pt); nenhuma limiarização de raster | plotagem nova em matplotlib (Arial Narrow 14 pt), PDF vetorial montado com PyMuPDF |
| folhas | 5 -> 6 (Figs. 1 e 9 em paisagem) | 3 -> 8 (Figs. 1, 4 e 8 em paisagem) |
| altura mínima medida (maiúscula/algarismo/ascendente) | 0.334 cm (antes: mínimo por folha 0,059-0,173 cm; 182 de 184 linhas < 0,32 cm) | 0.351 cm (antes: mínimo por folha 0,068-0,069 cm; 372 de 372 linhas < 0,32 cm) |
| pixels nem pretos nem brancos (600 dpi, sem antialias) | 0 | 0 |
| margens / A4 / moldura | 6/6 folhas ok; nenhuma moldura | 8/8 folhas ok; nenhuma moldura |
| texto cruzado por traço / texto sobre texto | 0 / 0 | 0 / 0 |
| **oclusão** (fundo branco/opaco sobre traço ou marca) | **0** (rodada 1: 14) | **0** (rodada 1: 240) |
| **marcação do RO livre** (canto sup. direito, margem inferior) | 6/6 (rodada 1: folha(s) [6] ocupada(s)) | 8/8 |
| mesmas palavras | conjuntos iguais em 6/6; diferenças só «PHO» (principal) vs «PHOT» (fonte) e «vacuum» vs «cuum» cortado no depositado | iguais em 8/8 (diferenças = artefatos de extração, explicados no JSON) |

Por que mais folhas: letras de no mínimo 0,32 cm obrigam corpo 14-15 pt; os painéis e blocos de texto não cabem nas mesmas folhas. Total do pedido: Aprendizado 23 -> 24 páginas; MQC 22 -> 27 (ambos abaixo de 30; taxa por folha excedente [LEGAL/OPEN]).

## Os dois testes novos (rodada 2) — definição e resultado

1. **Oclusão** (`conferir.py: oclusao`, vetorial, em ordem de pintura): qualquer elemento de fundo branco/opaco (caixa de rótulo, legenda, caixa de texto, coluna, marcador vazado) que cubra um traço ou marca de dado pintado **antes** dele; conta pontos de traço (amostra a cada ~0,8 pt) dentro do polígono branco reduzido de 0,5 pt, ignorando o fundo da tela. Resultado: Aprendizado 0 (rodada 1: 14 ocorrências, 768 pontos), MQC 0 (rodada 1: 240 ocorrências, 33343 pontos). Os marcadores vazados do MQC passaram a ter face transparente; as colunas, face transparente; onde a grade passaria por legenda/caixa/coluna ela é desenhada com lacuna.
2. **Marcação do RO** (`conferir.py: marcacao_RO`): pela Seção 325 das Instruções Administrativas [DECLARADO pela coordenação, lido de wipo.int em 27/10/2026] o RO marca cada folha de substituição no canto superior direito (número do pedido, data de recebimento) e na margem inferior («SUBSTITUTE SHEET (RULE 26)»). Teste a 600 dpi sem antialias: nenhuma tinta no canto superior direito (x >= 12 cm, y < 3,5 cm), na margem superior (y < 2,5 cm), na margem inferior (y >= 28,7 cm) nem na margem direita (x >= 19,5 cm). Resultado: Aprendizado 6/6 folhas livres (rodada 1: a folha 6 tinha tinta no canto), MQC 8/8. A folha alternativa PHOT também passa.

## Rodada 3 (Aprendizado 050576; o MQC 050579 está ACEITA e congelado)

* **R2-1 (único bloqueio):** na Fig. 3 (folha 2/6) a linha horizontal da grade em θ = 20 tocava o pé do «V» de «VACUUM 6 bits» (28 px a 600 dpi, segundo a revisão). **Reparo:** lacuna da grade ampliada (θ = 20 interrompida entre x = 0,036 e 0,104; a vertical x = 0,1 interrompida entre θ = 15 e 75; o rótulo ocupa θ 18,7-71,6 e x 0,044-0,087 em unidades do eixo). **Medida antes -> depois:** teste de contato texto x gráfico (novo, abaixo) 2 componente(s), 25 px (folha 2, «VACUUM») -> **0** nas 6 folhas principais, nas 6 da variante PHOT e na folha alternativa; palavras cruzadas por traço (vetorial, ajustado): 0; oclusões: 0; marcação do RO livre: 6/6.
* **O teste agora pega o caso.** (1) *Contato texto x gráfico* (`conferir.py: contato_texto_grafico`): texto e gráfico renderizados em separado (600 dpi, sem antialias; redação em cópia na memória) e contato = pixel de tinta comum, componentes >= 3 px, excluída a régua do radical. Sobre o PDF da rodada 2 acusa a folha 2 («VACUUM», 25 px); sobre os PDFs desta rodada, 0 em todas as folhas. (2) O teste vetorial «palavras cruzadas por traço» **não via** o caso porque reduzia a caixa da palavra em 4% ao longo do texto e o pé do «V» fica na ponta de «VACUUM»; a redução ao longo do texto agora é 0% (a perpendicular segue 22%): acusa a folha 2 da rodada 2 e passa nas reparadas. Rodado sobre todas as folhas de ambas as variantes: 0. O MQC foi rodado só para leitura no teste de contato: 0 (`conferencia/contato_texto_grafico_r3.json`).
* **Sugestão 1 aplicada:** `FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf` (6 folhas: 1/6 alternativa + 2/6 a 6/6 iguais às principais — texto e pixels a 100 dpi conferidos), passa em todos os testes; a carta da variante PHOT cita esse arquivo como anexo.
* **Sugestão 2 aplicada:** item 3(c) das duas cartas do Aprendizado: «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)». A carta do MQC não foi tocada.
* **Sugestão da revisão (linha da Fig. 3, aplicada):** «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto).
* **MQC congelado:** hashes antes e depois desta rodada iguais (4faa43ca81442fc5, 2378f978494f2fdf, 529ca8412ad6baa1 -> 4faa43ca81442fc5, 2378f978494f2fdf, 529ca8412ad6baa1); `CONFERENCIA_050579.json`, folhas e carta do MQC não foram regenerados.
* Backups desta rodada: `*.bak_20261027_103927`.

## Numeração das folhas (achado da coordenação, registrado)

A Seção 207 das Instruções Administrativas **não prevê esquema de sufixo** para folhas acrescentadas: as folhas de desenhos são numeradas n/N com o **novo total**. As séries do kit (1/6 a 6/6 e 1/8 a 8/8) estão de acordo com o texto (lido de wipo.int, s207 e s325, em 27/10/2026 [DECLARADO pela coordenação; o preparador não tem rede e não releu a fonte]). Substituir **todo** o conjunto de desenhos continua sendo decisão [LEGAL] do operador/agente de PI.

## Rodada 2 — pontos reparados, com medidas antes -> depois (para a segunda revisão, só estes)

### Aprendizado 050576

| id | pedido da revisão | o que foi feito | medida antes -> depois |
|---|---|---|---|
| R1 | setas [1]-[3] e [4]-[5] da Fig. 1: decidir e documentar o sentido | a descrição é **silenciosa** sobre o fluxo [1]-[3] ([002], [031]-[033], [041]) e só **sugestiva e ambígua** sobre [4]-[5] ([045] o hash opera também sobre «certificados»; [046] a cadeia registra hashes): pela regra da coordenação, reproduzido o **sentido visível no depositado** ([3] para [1], [5] para [4]); a fonte TikZ ([1]->[3], [4]->[5]) fica comentada em uma linha cada. **[LEGAL]** | cabeças de seta lidas no vetor: antes [1]-[3] aponta para [3] (direita na figura); [4]-[5] aponta para [5] (direita na figura) -> depois [1]-[3] aponta para [1] (esquerda na figura); [4]-[5] aponta para [4] (esquerda na figura) |
| PHOT | ponto 3: o principal reproduz só o visível; alternativa para o agente de PI | principal: «VACUUM/GRAV/PHO» (a caixa [3] cobre o T no depositado); `ALTERNATIVA_FOLHA_1_050576_PHOT.pdf` com «PHOT»; duas cartas, cada uma com a frase da sua folha. «PHOT» não está na descrição (só «PHOTON», [033]). **[LEGAL]** | texto vivo da folha 1: «PHOT» -> «PHO» (principal) / «PHOT» (alternativa); folhas 2-6 idênticas nas duas |
| R2 | Fig. 5 «Próxima geração» cortava a borda da caixa CARGA | rótulo em duas linhas, sem fundo, abaixo do trecho horizontal da seta; borda contínua | oclusões da folha 3: 1 (29 pontos) -> 0; folga da caixa do texto ao traço: «Próxima» 0.09 -> 0.31 cm, «geração» 0.0 -> 0.82 cm |
| R3 | Fig. 8 «Vácuo angular» cortava moldura, marca de eixo e grade | rótulo **fora** do quadro, sem fundo, seta oblíqua para os buckets 13-14 vazios (como no depositado) | oclusões da folha 5: 1 (193 pontos) -> 0; folga «Vácuo» 0.0 -> 0.73 cm, «angular» 0.0 -> 0.1 cm (o traço mais próximo de «angular» é o início da própria seta, que nasce junto ao rótulo; a caixa medida é a da fonte, maior que a tinta) |
| R3b | Fig. 3: rótulos de fundo branco sobre a grade | grade pontilhada desenhada à mão com lacunas ao redor de «VACUUM 6 bits» e «GRAVITON 10 bits»; legenda acima do quadro | oclusões da folha 2: 5 (330 pontos, incl. Figs. 2 e 3) -> 0; palavras cruzadas por traço: 0 |
| extra | Fig. 6 (não pedida): colunas de fundo branco cobriam o limiar tracejado | limiares desenhados só entre as colunas | oclusões da folha 4: 7 (216 pontos) -> 0 |
| R4 | corrigir a carta (3(d), setas, Figs. 3, 5, 8) | cartas reescritas: 3(d) descreve o que foi feito; linhas das Figs. 1, 3, 5, 6, 8; VACUUM/PHOTON só por estarem na descrição; PHOT só na variante | `CARTA_REGRA_26_4_050576*.md/.pdf` |

Oclusões por folha (antes = rodada 1) e marcação do RO:

| folha | oclusões antes (pontos de traço cobertos) | depois | marcação do RO antes -> depois |
|---|---|---|---|
| 1 | 0 (0 pts) | 0 | livre -> livre |
| 2 | 5 (330 pts) | 0 | livre -> livre |
| 3 | 1 (29 pts) | 0 | livre -> livre |
| 4 | 7 (216 pts) | 0 | livre -> livre |
| 5 | 1 (193 pts) | 0 | livre -> livre |
| 6 | 0 (0 pts) | 0 | OCUPADO -> livre |

### MQC 050579

| id | pedido da revisão | o que foi feito | medida antes -> depois |
|---|---|---|---|
| R1 | legendas 3(a), 4(a), 4(b) e 4(d) escondiam dado ou encostavam em caixa | legenda **dentro** do quadro só em região sem dado (varredura de posições contra linhas, pontos, colunas e hachuras, folga de 6 px); onde não há região livre (3(a), 3(c), 4(a), 4(b), 4(d)) a legenda fica **acima** do quadro; a caixa de métricas de 4(d) vai à direita da linha vertical; grade com lacuna sob legenda/caixa | oclusões: 240 ocorrências (33343 pontos) -> 0 nas 8 folhas; 3(a) 12 de 82 pontos cobertos (revisão) -> 0 |
| R1b | listar na carta o que ficar visível e estava escondido no depositado | medido nas figuras do script de origem: **só a Fig. 4(d)**: a caixa de métricas do depositado cobria o trecho da curva α² 0,00167-0,00225 (η 0,99675-0,99760, 2 vértices); as demais legendas/caixas do depositado não cobriam dado. Figs. 5 e 7 (variante do PCT): legendas em cantos vazios. Está na carta (nota do item 3) | `conferencia/mqc_legendas_do_depositado.json` |
| R2 | a carta deve citar a troca de glifo ausente por 𝒜/ℰ na Fig. 8 | linha da Fig. 8 da carta cita: A_C (coluna «Equação Governante», linha «Controlador Hierárquico») e E_Ψ (colunas «Elemento Original» e «Equação Governante», linha «Correção de Erros Adaptativa»), com A_C no [0056]/eq. (22) e E_Ψ na Tabela 1 da descrição; 3(d) corrigido; graduação dos eixos e o limite superior de 4(c) citados | `CARTA_REGRA_26_4_050579.md/.pdf` |
| R3 | forma do glifo na Fig. 8 | **nota ao agente de PI [LEGAL]:** desenhados A em script regular (U+1D49C, igual ao A_C da Fig. 5 **depositada**) e E em script regular (U+2130); a descrição ([0056], eq. (22), Tabela 1) escreve A_C e E_Ψ em letra **romana** e nenhum desenho depositado traz E em script. Alternativa conservadora: romano (uma linha em `fontes\mqc_folhas.py`, `SPECIAL`). O preparador não decide. | texto das 40 células idêntico ao do script |
| R4 | conferência com teste de oclusão | incluído em `CONFERENCIA_050579.json` (por folha e no resumo), além do teste da marcação do RO | oclusões 0; marcação do RO 8/8 |

Oclusões por folha (antes = rodada 1) e marcação do RO:

| folha | oclusões antes (pontos de traço cobertos) | depois | marcação do RO antes -> depois |
|---|---|---|---|
| 1 | 18 (955 pts) | 0 | livre -> livre |
| 2 | 3 (1952 pts) | 0 | livre -> livre |
| 3 | 3 (1041 pts) | 0 | livre -> livre |
| 4 | 4 (4022 pts) | 0 | livre -> livre |
| 5 | 16 (844 pts) | 0 | livre -> livre |
| 6 | 3 (424 pts) | 0 | livre -> livre |
| 7 | 193 (24105 pts) | 0 | livre -> livre |
| 8 | 0 (0 pts) | 0 | livre -> livre |

## Pontos para decisão [LEGAL] (o preparador NÃO decidiu)

> [nota operacional do operador — omitida no retrato público]

## O que falta

Segunda rodada de revisão (só os pontos acima); liberação e assinatura do operador (e escolha PHO/PHOT com o agente de PI); parecer [LEGAL] nos itens acima; upload pelo Codex no ePCT só depois da REVISÃO ACEITA e da frase do operador (nome exato da ação [OPEN]). Nada disto foi feito.

## Reproduzir

```
python fontes\apr_01_originais.py ; python fontes\apr_02_identidade_fonte.py     # fonte do Aprendizado = depositado
python fontes\compilar.py aprendizado_folhas ; python fontes\compilar.py aprendizado_folhas 0 ALTPHOT   # xelatex (principal e PHOT)
python fontes\mqc_01_regenerar_originais.py ; python fontes\mqc_folhas.py ; python fontes\mqc_02_dados_identicos.py
copy _tmp\aprendizado_folhas\aprendizado_folhas.pdf FOLHAS_SUBSTITUTIVAS_050576.pdf ; copy _tmp\mqc_folhas\mqc_folhas.pdf FOLHAS_SUBSTITUTIVAS_050579.pdf
(a folha alternativa = pagina 1 de _tmp\aprendizado_folhas_ALTPHOT\aprendizado_folhas_ALTPHOT.pdf -> ALTERNATIVA_FOLHA_1_050576_PHOT.pdf)
python fontes\conferir.py FOLHAS_SUBSTITUTIVAS_050576.pdf 050576 --rot 1,6 --ref-pdf entrada\aprendizado\04_DESENHOS_como_depositado.pdf
python fontes\conferir.py FOLHAS_SUBSTITUTIVAS_050579.pdf 050579 --rot 1,4,8 --ref-pdf entrada\mqc\04_DESENHOS_CINZA_como_depositado.pdf
python fontes\conferir.py ALTERNATIVA_FOLHA_1_050576_PHOT.pdf ALT_PHOT --rot 1
python fontes\palavras.py apr FOLHAS_SUBSTITUTIVAS_050576.pdf ; python fontes\palavras.py mqc <caminho absoluto de FOLHAS_SUBSTITUTIVAS_050579.pdf>
python fontes\mqc_03_legendas_depositado.py ; python fontes\reparos_medidas.py     # antes = _tmp\base\*_antes.pdf
python fontes\contato_json.py ; python fontes\carta.py ; python fontes\prancha.py 050576 ; python fontes\finalizar.py     # rodada 3: carta.py so gera o Aprendizado (use `carta.py mqc` para o MQC)
```
Ferramentas: Python 3.14, PyMuPDF 1.28.0, numpy, scipy, matplotlib 3.11.0, fontTools, MiKTeX (xelatex, pdflatex), fonte Arial Narrow do Windows (embutida nos PDFs).
