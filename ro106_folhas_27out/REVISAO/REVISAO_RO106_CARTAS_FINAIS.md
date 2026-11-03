> [nota operacional do operador — omitida no retrato público]

> [nota operacional do operador — omitida no retrato público]

## VEREDITO

| PCT | cartas revistas (sha16 lido por script) | veredito |
|---|---|---|
| PCT/BR2026/050576 (Aprendizado Contínuo) | `CARTA_REGRA_26_4_050576_FINAL.pdf` `3d205224aea35c0d`; `.md` `28cfb7dc4d267def` | **ACEITA** |
| PCT/BR2026/050579 (MQC) | `CARTA_REGRA_26_4_050579_FINAL.pdf` `085019f414653fac`; `.md` `99e009ffd6ea4c38` | **ACEITA** |

> [nota operacional do operador — omitida no retrato público]

## A partitura, lida antes do resultado (regra do posto do assistente)

Na língua do operador: esta revisão decide só quatro coisas, e todas são de fato, não de opinião. (1) A carta final é a carta aceita mais as quatro mudanças que ele autorizou, e nada além. (2) Não sobrou rascunho nem dado pessoal. (3) Os números, as datas, o anexo e a tabela de cada carta pertencem àquele pedido e não ao outro, e conferem com o formulário do INPI. (4) A frase nova sobre a altura das letras no MQC diz o que foi medido. Ela NÃO decide se o INPI vai aceitar a resposta (isso é do agente de PI), NÃO libera a frase B4 (essa é dele), NÃO envia nada e NÃO mede de novo as folhas. Um RECUSADA significaria um defeito material que eu consigo apontar com número ou trecho na carta, nunca uma falsificação de teoria; ACEITA significa o contrário: procurei e não achei. As escolhas do meu desenho, ditas antes: comparei o texto por palavra com dois extratores de PDF (PyMuPDF e poppler) e por caractere sem espaço nem hífen, ignorando só quebra de linha, hifenização e paginação (pontuação, dígitos e acentos contam); li as páginas também como imagem; medi a altura das letras pelo contorno da fonte vezes o corpo do texto, não pelo pixel, em quatro classes (algarismo, maiúscula, minúscula com ascendente, minúscula sem ascendente), lendo «letras com haste» como a gerência lê (ascendente) e testando também a leitura larga de «haste» (ver O1). Onde a leitura larga muda o resultado, digo qual dos dois é: ambiguidade de palavra (parede medida), não falsificação da afirmação pretendida.

## Mapa de rotas (consulta feita antes, só leitura)

> [nota operacional do operador — omitida no retrato público]

## C1 — diferenças de conteúdo além das quatro

**Resposta: não há.** [REAL]

Método: texto dos PDFs por PyMuPDF e, de controle, por `pdftotext -raw`; NFC; hifenização de fim de linha unida; hífen interno de compostos tirado; linha de cabeçalho da tabela (repetida na 2.ª página) tirada e contada; `difflib.SequenceMatcher` por palavra; depois, a prova mais forte: o multiconjunto de palavras removidas (aceita menos final) é IGUAL ao das palavras da nota «Minuta…», de «[local], [data]», do marcador «[ASSINATURA…]» (e, no MQC, da frase antiga do 3(c)) e o multiconjunto das acrescentadas é IGUAL ao de «Goiânia, 4 de novembro de 2026», do bloco do requerente (e, no MQC, da frase nova do 3(c)); qualquer palavra a mais ou a menos quebraria a igualdade (o script a verifica com `assert`: `evidencias_FINAIS\rf_11_relatorio.py`).

| | 050576 | 050579 |
|---|---|---|
| PDF aceita → final (palavras normalizadas) | 1050 → 1024; removidas 40, acrescentadas 14; 6 blocos de diferença, todos nas diferenças (1), (2), (3) | 1116 → 1093; removidas 45, acrescentadas 22; 9 blocos, todos em (1), (2), (3), (4) |
| md aceita → final | 6 blocos; `diff` literal por linha: aceita 3-5 -> final 3-3; aceita 43-43 -> final 41-42 | 9 blocos; `diff` literal por linha: aceita 3-5 -> final 3-3; aceita 32-32 -> final 30-30; aceita 42-42 -> final 40-41 |
| parágrafo 4 («não acrescentam matéria nova») | idêntico: sha16 `d238a4b6668f4b73` nas quatro cartas (aceita e final, os dois PCT) | idêntico (mesmo sha16) |
| linhas da tabela de figuras | 11 linhas idênticas, uma a uma | 10 linhas idênticas, uma a uma |
| controle cruzado | o mesmo vale no texto de `pdftotext -raw`, por multiconjunto de caracteres sem espaço nem hífen (o poppler desfaz a hifenização à sua maneira: removido = nota + local/data + marcador; acrescentado = data + bloco do requerente); a comparação por caractere sem espaço nem hífen só acusa esses mesmos trechos e a mudança de lugar do cabeçalho repetido da tabela (paginação) | idem, mais o 3(c) |

As quatro diferenças, onde caem: (1) nota «Minuta preparada pela Central… Não enviada.» removida; (2) «[local], [data]» → «Goiânia, 4 de novembro de 2026»; (3) «[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]» → «ROTOLI MIGUEL, Luiz Antonio — Requerente» + «Assinado eletronicamente no envio pelo ePCT.»; (4) só no 050579, item 3(c): «todos os números, letras e sinais de referência com altura mínima de 0,32 cm» → «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)». Paginação mudou (3 → 2 páginas no 050576; o bloco de assinatura agora fica na 2.ª página junto do último parágrafo; 2 → 2 no 050579), como permitido. PDF final × md final: 1 bloco (050576) e 3 (050579), todos de apresentação e já presentes nos PDFs aceitos: cabeçalho da tabela («Figura / Folha substituída (como depositada)» no md, «Fig. / Folha substituída» no PDF), «𝒜_C» (md) × «A_C» (PDF), «α²» × «α2» (sobrescrito extraído como dígito). Também li as quatro páginas finais como imagem (`pg_*_final_p*.png`): conferem com o texto.

## C2 — marcas de rascunho nos PDFs finais

> [nota operacional do operador — omitida no retrato público]

## C3 — a frase nova do item 3(c) do MQC contra `CONFERENCIA_050579.json`

**Resposta: verdadeira.** [REAL] E a frase antiga era falsa para as minúsculas sem ascendente, como a gerência diz. Duas medidas, a do preparador e a minha:

- No JSON do preparador: `medidas_das_folhas_novas`: 393 linhas de texto classificadas maiúscula/algarismo/ascendente, mínimo **0,351 cm**, **0** linhas abaixo de 0,32 cm; a única linha só de altura-x abaixo de 0,32 é «v = c» na folha 6, **0,267 cm**. O critério declarado lá (`obs_altura`): «letras minusculas sem haste (altura-x) nao entram [LEGAL: leitura usual da Regra 11.13(h)]»; note que o preparador chama «sem haste» justamente as de altura-x (a c e m n o r s u v w x z), o que sustenta a leitura pretendida «com haste = ascendente».
- Minha medida independente (não usa o p90 por linha dele): altura de cada glifo de texto vivo acima da linha de base = contorno da fonte (FreeType; Arial Narrow do Windows, STIXGeneral do matplotlib) × corpo do trecho no PDF. Todos os trechos do anexo do MQC têm 14 ou 15 pt (nenhum sub ou sobrescrito reduzido; nenhum trecho abaixo de 13,5 pt):

| classe (anexo `FOLHAS_SUBSTITUTIVAS_050579.pdf`) | glifos | mínimo | abaixo de 0,32 cm |
|---|---:|---:|---:|
| algarismos | 658 | **0,3487 cm** | 0 |
| maiúsculas (latinas e gregas; o mínimo é 𝒜 em STIX, folha 5) | 381 | **0,3328 cm** | 0 |
| minúsculas com ascendente (b d f h k l) | 253 | **0,3535 cm** | 0 |
| minúsculas SEM ascendente (a c e m n o r s u v w x z) | 1192 | **0,2561 a 0,2621 cm** | todos |

Logo: a frase nova («algarismos, maiúsculas e letras com haste … 0,32 cm») é verdadeira na leitura «haste = ascendente» (mínimos por classe: maiúsculas 0,3328, algarismos 0,3487, ascendentes 0,3535 cm; todos acima de 0,32). A frase antiga («todos os números, letras e sinais de referência com altura mínima de 0,32 cm») era falsa se «altura» da minúscula for a altura-x: 1192 glifos medem 0,2561 a 0,2621 cm. (Se o critério de «altura» for a das maiúsculas e ascendentes da fonte, e não a altura-x das minúsculas, a antiga também seria verdadeira; essa é a escolha [LEGAL] «altura-x» que as revisões anteriores já registraram.) Mesma conta no Aprendizado, para a frase que lá já estava aceita: algarismos mín. 0,3361 cm (227), maiúsculas 0,3432 (376), ascendentes 0,3514 (76), sem ascendente 0,2234 a 0,2798 cm (483); os 14 «ℓ» e 2 «ϕ» não foram mapeados pelo contorno (ver «não conferido»). «Inclusive nos sinais de referência»: no MQC não há sinal de referência numérico nem entre colchetes (o JSON lista `colchetes: []`); as designações de painel «(a)…(d)» têm «a» e «c» sem ascendente (0,2561 cm), que a frase, por dizer «com haste», não afirma (ver O1).

## C4 — número do pedido, referência, datas, requerente, folhas, anexo, tabela

> [nota operacional do operador — omitida no retrato público]

> [nota operacional do operador — omitida no retrato público]

## C5 — as decisões do operador de 02/11/2026

**Resposta: batem.** [REAL] (registro das decisões: `work\decisoes_patentes_02nov\DECISOES_OPERADOR_02nov.md`; `EPCT\CONTROLE_GERAL.md`, adendo «decisoes_operador_02nov».)

- «PHO» como no depositado (050576): a folha 1/6 do anexo traz «VACUUM/GRAV/PHO» (nenhuma folha traz «PHOT»); o depositado 1/5, visto em imagem, mostra «VACUUM/GRAV/PHO»; a carta (Fig. 1) declara «VACUUM/GRAV/PHO». A variante PHOT não é a citada.
- Setas: na imagem da folha 1/6 (girada para leitura) a ponta entre [1] e [3] fica em [1] e a de [4]-[5] fica em [4]; o depositado 1/5, em imagem, mostra o mesmo; a carta diz «[3] para [1] e [5] para [4]» e, no 3(d), «as setas reproduzem o sentido visível no depositado».
- Colchetes: a folha 1/6 tem `[1]` a `[7]` em texto vivo; as demais folhas não têm colchetes; a carta usa os rótulos como estão e o item 4 declara os sinais de referência «os do pedido internacional tal como depositado».
- MQC, Figura 8: o anexo, folha 8/8, tem «𝒜» (U+1D49C, 1 vez) e «ℰ» (U+2130, 2 vezes) em script; o depositado, em imagem, mostra caixas vazias onde iriam o 𝒜 e o ℰ; a carta (quadro, Fig. 8) declara «nos símbolos A_C (…) e E_Ψ (…) o depositado mostra caixa de glifo ausente e as folhas desenham o símbolo em script» e indica onde constam na descrição ([0056], equação (22); Tabela 1).
- «Não acrescentam matéria nova»: parágrafo 4 idêntico ao aceito, byte a byte do trecho (sha16 `d238a4b6668f4b73`), nos dois PCT.

## C6 — dados pessoais nos PDFs finais

> [nota operacional do operador — omitida no retrato público]

## C7 — o que mais poderia embaraçar ou ficar inconsistente

> [nota operacional do operador — omitida no retrato público]

## Observações não bloqueantes (para a gerência; nenhuma é reparo necessário)

> [nota operacional do operador — omitida no retrato público]

## Escolhas [LEGAL] abertas (herdadas das revisões anteriores; não são minhas e não bloqueiam)

Substituição integral das folhas (5 → 6 e 3 → 8); critério da altura-x (O1); curva da Fig. 3 mantida como depositada; cores citadas nas descrições (MQC 9 menções, 6 pedidos, registrado no Mapa em 12/10); símbolos em script na Fig. 8 do MQC (leitura da Central, que o operador pode corrigir antes da B4); possível convite da Regra 26.3ter; a assinatura «eletronicamente no envio pelo ePCT» e a Regra 92.1; a citação «Regra 11.13(j)» (parágrafo da folha de lado, nas duas cartas). Seções 207 e 325 das Instruções Administrativas: [DECLARADO pela gerência].

## O que NÃO foi conferido

> [nota operacional do operador — omitida no retrato público]

## Hashes (sha16 lidos por script agora; sha256 completo no `.json`)

- `CARTA_REGRA_26_4_050576_FINAL.pdf` `3d205224aea35c0d` · `.md` `28cfb7dc4d267def`
- `CARTA_REGRA_26_4_050579_FINAL.pdf` `085019f414653fac` · `.md` `99e009ffd6ea4c38`
- aceitas (conferidas intactas): 050576 `.pdf` `a72a89c3571cb828`, `.md` `dbe1caff15ed32e4`; 050579 `.pdf` `2378f978494f2fdf`, `.md` `29029f0a6e2b0c4c`
- anexos: `FOLHAS_SUBSTITUTIVAS_050576.pdf` `884d978a39b20d1a`; `FOLHAS_SUBSTITUTIVAS_050579.pdf` `4faa43ca81442fc5` (os hashes aceitos)
- gerador `fontes\carta_final.py` `3e828e63dd5c452b`; base `fontes\carta.py` `854b1f5e64fb9c48`
- entrada (desenhos depositados): Aprendizado `1c09a448482ccc81`; MQC `2ef675ed2a3d2a7c`

## Para registro no Mapa (a gerência registra; eu não)

> [nota operacional do operador — omitida no retrato público]

## Evidências

Pasta `REVISAO\evidencias_FINAIS\` (scripts `rf_01` a `rf_11`, saídas `.json`, textos extraídos `txt_*`, páginas finais e imagens de conferência `pg_*`, `anexo_*`, `depositado_*`; sha16 de cada um no `.json`).
