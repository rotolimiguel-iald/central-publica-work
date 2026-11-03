> [nota operacional do operador — omitida no retrato público]

> [nota operacional do operador — omitida no retrato público]

## VEREDITO

| PCT | carta revista (sha16 lido por script) | veredito |
|---|---|---|
| PCT/BR2026/050576 (Aprendizado Contínuo) | `CARTA_REGRA_26_4_050576_FINAL.pdf` `c07e08b7f9adabea`; `.md` `a1bf28d8c393f1bb` | **ACEITA** |
| PCT/BR2026/050579 (MQC) | `CARTA_REGRA_26_4_050579_FINAL.pdf` `849615590437ff97`; `.md` `eaf51ffc0927f110` | **ACEITA** |

Nenhum reparo necessário. As cartas r2 diferem das r1 aceitas SÓ nas duas frases permitidas (C1); a frase nova é verdadeira contra os dois JSON e contra a medida por glifo que refiz (C2); não sobrou gênero errado nem rascunho (C3); os anexos têm os hashes esperados (C4); li as duas cartas inteiras e não achei erro de concordância certo, frase quebrada nem conteúdo impróprio, só observações de estilo e de diagramação, todas já presentes na r1 aceita (C5, N1 a N9). ACEITA aqui quer dizer: procurei defeito material e não achei; não quer dizer que o INPI aceitará (isso é [LEGAL], do agente de PI).

## A partitura, lida antes do resultado (regra do posto do assistente)

Na língua do operador: esta revisão decide só isto. (1) A carta nova é a carta aceita com duas palavras trocadas e mais nada. (2) A frase nova sobre a altura das letras diz o que foi medido. (3) Não ficou «a requerente» nem rascunho. (4) Os dois anexos são os mesmos já aceitos. (5) Nada na carta inteira que um revisor de português jurídico barraria. Ela NÃO decide se o INPI aceita a resposta, NÃO decide as escolhas [LEGAL] herdadas (colchetes, altura-x, data), NÃO envia nada e NÃO remede as folhas por inteiro. RECUSADA significaria um defeito material que eu aponto com número ou trecho; ACEITA significa o contrário. Escolhas do meu desenho, ditas antes: comparei por palavra com dois extratores (PyMuPDF e poppler `-raw`/`-layout`), por caractere sem espaço nem hífen, por byte (md), por pixel (páginas renderizadas) e, para os hífens, por palavras com hífen interno; ignorei só quebra de linha, hifenização e paginação. Medi a altura pelo contorno do glifo na fonte EMBUTIDA no PDF do anexo (yMax × corpo), e li «haste ascendente» como b d f h k l e glifos de mesma altura de ascendente (também i, j, t em separado); testei ainda a leitura larga. Onde algo depende de leitura de palavra, digo qual é: ambiguidade (parede medida), não falsificação.

## Mapa de rotas (consulta só leitura, antes)

> [nota operacional do operador — omitida no retrato público]

## C1 — há outra diferença de conteúdo além das duas permitidas?

**Resposta: não.** [REAL]

- **md r1 → md r2, por byte.** Cada frase antiga aparece 1 vez na r1 e 0 na r2; cada frase nova, 0 na r1 e 1 na r2. Aplicando as duas substituições ao md r1 obtém-se o md r2 **byte a byte igual** nas duas cartas (+11 bytes cada: «ascendente» com espaço). Linhas diferentes (1-based): 050576 linhas 15 e 31; 050579 linhas 15 e 30. Diff por palavra: `a`→`o` e `+ascendente`, nada mais.
- **PDF r1 → PDF r2.** PyMuPDF: 1048→1049 palavras (050576) e 1117→1118 (050579), exatamente 2 blocos (`a`→`o`; inserção de `ascendente`); caractere comprimido: os mesmos 2 blocos, nos três extratores (PyMuPDF, poppler `-raw`, `-layout`). No poppler aparecem blocos extras de palavra (`re produção`/`repro dução`, `posiciona dos`/`posi cionados`, `pontil hada`): são só a hifenização que mudou com o refluxo do parágrafo 3 e o poppler partindo palavras; somem na forma comprimida.
- **Hifens.** Palavras com hífen interno: iguais em md r1 = md r2 e PDF r1 = PDF r2, e md r2 = PDF r2. Quebras de fim de linha: iguais, exceto no parágrafo 3 (050576: `re-produção`→`repro-dução`, `posiciona-dos`→`posi-cionados`; 050579: `re-produção`→`repro-dução` e some `pontil-hada`, que partia o dígrafo «lh»; a r2 ficou melhor).
- **Pixel.** Páginas renderizadas a 110 dpi, r1 × r2: página 1 de cada carta difere em 36 pixels, uma caixa de 8 × 9 px (o `a`→`o` de «o requerente»); página 2 só no bloco do item 3 (refluxo; itens 4, 5, anexo e assinatura não se mexem); cabeçalho, tabela e bloco de assinatura idênticos.
- **PDF × md na r2.** Resíduo idêntico ao da r1 (4 blocos na 050576, 6 na 050579, PyMuPDF): cabeçalho da tabela («Figura»/«Fig.» e «(como depositada)» ausente do PDF, cabeçalho repetido na 2.ª página), `𝒜_C` (md, linha da Fig. 5) × `A_C` (PDF), `α²` × `α2` (sobrescrito extraído como dígito; na imagem é sobrescrito). Todos de apresentação, já na r1 aceita.
- Parágrafo 4 («não acrescentam matéria nova»): sha16 `d238a4b6668f4b73` em r1 e r2, nas duas cartas (mesmo método e mesmo valor da R1); linhas da tabela: 11 e 10, idênticas.
- O gerador `fontes\carta_final.py` (`434d7393bab6b462`; a R1 registrou `3e828e63dd5c452b`) declara só as duas substituições novas (`SUBS`), com `assert` de ocorrência única; coerente com o medido.
- A r1 de referência em `superseded_finais_r1\` é a aceita: os 4 arquivos têm sha256 iguais aos do `MOVED_MANIFEST.json` e aos do `REVISAO_RO106_CARTAS_FINAIS.json`.

## C2 — a frase nova é verdadeira contra os JSON?

**Resposta: sim, nas duas.** [REAL] Frase (2): «algarismos, maiúsculas e letras com haste ascendente com altura mínima de 0,32 cm (inclusive nos sinais de referência)».

- `CONFERENCIA_050576.json`: 6 folhas, 196 linhas de texto cap/alg/asc medidas, mínimo **0,334 cm**, **0** linhas abaixo de 0,32. Única linha só de altura-x abaixo de 0,32: «α», 0,229 cm (folha 2).
- `CONFERENCIA_050579.json`: 8 folhas, 393 linhas, mínimo **0,351 cm**, **0** abaixo de 0,32. Única linha só de altura-x abaixo de 0,32: «v = c», 0,267 cm (folha 6).
- O critério dos dois JSON (`criterios.obs_altura`) é «maiúscula/algarismo/ascendente»; «letras minúsculas sem haste (altura-x) não entram [LEGAL: leitura usual da Regra 11.13(h)]». O vocabulário bate com a frase nova: «haste ascendente» é a classe «ascendente» do JSON e «sem haste» é a altura-x. O sha256 do anexo gravado em cada JSON é igual ao do anexo atual; os JSON são mais novos que os anexos.
- **Corroboração minha, por glifo** (contorno na fonte embutida × corpo; não usa o p90 por linha do preparador; refiz o que a R1 fez e fechei a lacuna dos glifos de fonte CM):

| classe | 050576 (glifos; mín. cm) | 050579 (glifos; mín. cm) |
|---|---|---|
| algarismos | 227; 0,3361 | 658; 0,3487 |
| maiúsculas (latinas e gregas) | 376; 0,3431 | 381; 0,3329 (𝒜 em STIX, folha 5) |
| minúsculas com ascendente (b d f h k l) | 76; 0,3512 | 253; 0,3535 |
| ascendentes gregas/script (β θ ϕ ℓ; θ λ) | 32; 0,3512 (inclui os 14 «ℓ» e 2 «ϕ», 0,3563 e 0,3512) | θ 0,3596 e λ 0,3535 |
| i, j, t | 115; 0,3689 | 261; 0,3456 |
| minúsculas SEM ascendente (a c e m n o r s u v w x z, mais α etc.) | 483; 0,2232 a 0,2796 | 1192; 0,2561 a 0,2619 |

Nenhum algarismo, maiúscula nem letra com ascendente fica abaixo de 0,32 cm (menor valor de todo o conjunto: 0,3329 cm). Corpos: 050576 14,94 pt (texto) e 14,35 pt (símbolos CM); 050579 14 pt e 15 pt (só o número da folha); sem sub/sobrescrito reduzido. Todo o texto é vivo (sem imagem). As letras de altura-x (e φ, ψ em Arial Narrow, que não têm ascendente) ficam abaixo de 0,32 e a frase nova não as afirma. A frase ANTIGA («letras com haste com altura…») só era verdadeira na leitura estreita de «haste» e agora o texto diz isso.

- «Inclusive nos sinais de referência»: 050576, os sinais são `[1]` a `[7]` (algarismos, mín. 0,3361 cm): verdadeiro. 050579: o JSON lista **zero** sinais de referência (`colchetes: []`); as designações (a) a (d) estão como «painéis», e «a» e «c» são altura-x, fora da frase; a cláusula é verdadeira por não haver o que medir, não falsa (N8).

## C3 — gênero errado ou rascunho

**Resposta: não sobrou.** [REAL] Em md e nos três extratores dos PDFs r2: «a requerente» = 0; ocorrem só «o requerente» (item 1) e «do requerente». O mesmo teste na r1 acha «a requerente» nas quatro fontes (controle positivo). Rótulos e assinatura («Requerente», «ROTOLI MIGUEL, Luiz Antonio — Requerente»; «Assinado eletronicamente…») são neutros ou masculinos; nenhum outro marcador de pessoa feminina (depositante, signatária, qualificada, ela, sua…). Rascunho: zero de «minuta», «não enviada», «a preencher», `[LEGAL`, `[local]`, `[data]`, `[ASSINATURA`, «operador», «rascunho», «TODO» (como palavra), «XXX», «preench», nomes de IA ou de ferramenta; as ocorrências de substring que a busca acusa são `br2026`, «método», «IALD» (nome de série na legenda da Fig. 5 do MQC) e «script» (letra cursiva). Colchetes que restam: 050576 `[1]` `[3]` `[4]` `[5]` (rótulos da Fig. 1), `[033]`, `[15]`; 050579 `[0056]`, `[15]` (todos conteúdo; O5 da R1). PDFs: 2 páginas A4, fontes todas embutidas, sem título, autor, XMP, anotação, link, anexo, JavaScript, criptografia, imagem, texto branco nem caminho de arquivo.

## C4 — hashes dos anexos, lidos por script

> [nota operacional do operador — omitida no retrato público]

## C5 — leitura de português jurídico da carta inteira

**Resposta: nenhum erro de concordância certo, nenhuma frase quebrada, nada impróprio a um organismo oficial.** Listo, sem consertar (nenhum é reparo necessário; todos já estão na r1 aceita, salvo onde digo):

- **N1 [item 4, as duas cartas, discutível].** «Mudaram apenas a apresentação (cor, espessura de traço, …)»: verbo no plural com «a apresentação» no singular. Lido como intransitivo, pediria «Mudou»; lido como transitivo com sujeito indeterminado («mudaram [alguém] a apresentação») está correto. É o parágrafo pinado (sha16 `d238a4b6668f4b73`); não é reparo, é decisão de redação do operador.
- **N2 [diagramação, as duas].** A tabela do item 2 é mais larga que o texto: o log do XeLaTeX registra `Overfull \hbox (42.78917pt too wide)` nas duas; a borda direita da tabela fica a 20,50 cm, 0,50 cm da borda da página, e o texto corrido termina por volta de 19,0 cm. Tudo dentro da página, legível; igual na r1.
- **N3 [tipografia].** Hifenização automática dentro de rótulos de figura em caixa-alta, citados entre aspas: «VAC-UUM/GRAV/PHO» (050576, Fig. 1), FRON-TIER (050576, Fig. 6), LO-CAL (050579, Fig. 7). Igual na r1; pode parecer hífen do rótulo.
- **N4 [estilo, 3(c)].** «letras com haste ascendente com altura mínima»: dois «com» seguidos; correto e claro, só pesado.
- **N5 [estilo, tabela do MQC e do Aprendizado].** «áreas translúcidas viram hachura» (Fig. 3 do MQC; a Fig. 2 diz «substituída por hachura»); «Entram 6 folhas»; «7a» (Fig. 7 do MQC) frente a «3(a)», «4(a)»; «R.11.13(j)» na tabela e «Regra 11.13(j)» no texto; «2x2».
- **N6 [notação].** `A_C` e `E_Ψ` saem no PDF com sublinhado (notação de código); «em script», «buckets» e «PCT» como atalho de «pedido internacional» («variante do PCT», «como no PCT»); o md usa `𝒜_C` na Fig. 5 e o PDF `A_C`. (O6 da R1.)
- **N7 [precisão].** «corpo 15 pt» (050576, Figs. 1 a 4): medido 14,94 pt no texto e 14,35 pt nos símbolos CM; arredondamento.
- **N8 [050579, 3(c)].** «(inclusive nos sinais de referência)» não tem objeto no MQC (ver C2); inofensivo.
- **N9 [fonte JSON, novo].** `legendas_figura.altura_medida_cm` dos JSON (0,212 cm no Aprendizado, 0,195 no MQC, para «Figura N») é outra métrica (tinta no retângulo do trecho, `a5.measure_text_span`), não o critério cap/alg/asc; por contorno de fonte o «F» da legenda mede 0,35 a 0,38 cm. A carta não cita esse campo; quem ler o JSON pode estranhar.

> [nota operacional do operador — omitida no retrato público]

## O que NÃO foi conferido

> [nota operacional do operador — omitida no retrato público]

## Hashes (sha16 lidos por script; sha256 completo no `.json`)

- r2: `CARTA_REGRA_26_4_050576_FINAL.pdf` `c07e08b7f9adabea` · `.md` `a1bf28d8c393f1bb`; `CARTA_REGRA_26_4_050579_FINAL.pdf` `849615590437ff97` · `.md` `eaf51ffc0927f110`
- r1 aceita (`superseded_finais_r1\`): 050576 `3d205224aea35c0d` · `28cfb7dc4d267def`; 050579 `085019f414653fac` · `99e009ffd6ea4c38`
- anexos: `884d978a39b20d1a`, `4faa43ca81442fc5`; conferências: `d171e2bc9be9668e`, `529ca8412ad6baa1`; gerador `434d7393bab6b462`

## Para registro no Mapa (a gerência registra)

`pi.pct.ro106_cartas_finais_r2_02nov` (PATENTES, EXAMINADA; REAL no medido, LEGAL na suficiência): veredito `CARTAS_FINAIS_R2_050576_050579_ACEITAS_DUAS_FRASES_SO`; defeito: nenhum necessário (N1 a N9); não refazer: a comparação com a r1, a medida por glifo; próximo passo: frase B4 do operador, uma por PCT, enviando só a carta `_FINAL.pdf` e o anexo de cada PCT.
