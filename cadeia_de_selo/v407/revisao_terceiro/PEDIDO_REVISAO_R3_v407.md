# PEDIDO DE REVISÃO DE TERCEIRO — v407, RODADA R3 (confinada ao diff; gerência c1, 03/11/2026, 17h)

> A R2 aprovou (0 ALTO, 0 MÉDIO, 8 BAIXO; candidato `cf7121b664371977`). Dos BAIXOS novos da R2, a gerência corrigiu, em nome próprio, os que eram FRASE AFIRMANDO MAIS DO QUE O MEDIDO ou ESTATUTO ERRADO em texto (não em pedra): pela régua, isso não entra no selo. Nenhuma pedra, prova, enunciado, nome ou módulo do kernel foi tocado; o kernel do sandbox é o mesmo (`kernel\POS_BUILD_v407.json` inalterado). Como `registros_v407.py`, `delta_v407.py` e os pysnips entram no candidato, o sha16 do candidato mudou e a sua R2 não vale mais para ele: esta R3 revê SÓ o diff abaixo e refaz a trava.

## O que mudou desde a R2 (script `r2_baixos_da_r2_03nov.py`; backups `.bak_r3_baixos_<ts>` e `.bak_r3_tempo_<ts>`, mesma pasta de cada arquivo)
1. `delta_v407.py` — RESSALVAS: «[KNOWN/ONTO]» → «[ONTO] (sem citação [KNOWN] até haver fonte)» na ponte Bell↔TT; «as nove pedras foram relidas inteiras pelo revisor…» → «as nove pedras foram conferidas pelo revisor de terceiro desta preparação em 03/11/2026 (Sonnet, rodadas R1 e seguintes: #print axioms no trio, diff contra as origens e docstrings, não as provas linha a linha; 0 alto e 0 médio em todas as rodadas; os baixos ficam ditos no caderno da revisão)».
2. `registros_v407.py` — o item «NÃO diz» sobre a revisão das pedras deixa de contradizer a ressalva (três por dentro em 02/11; as nove conferidas em 03/11 pelo revisor desta preparação, pelo mesmo método); os papéis dos recibos e saídas R1 (quatro FONTES) ganham «[registro R1: a fonte/saída vigente é a R2 …]». Nada mais.
3. `artigo_pt_v407.pysnip` / `artigo_en_v407.pysnip` — as mesmas duas trocas da ressalva (o [ONTO] e a frase da conferência das nove), em PT e EN.
4. `pos_rito\textos_v407.py` e `pos_rito\textos_v407_novo.pysnip` — «[KNOWN/ONTO]» → «[ONTO]» na frase «a leitura do canto como sombra do gráviton é …» (o texto do README/handoff). `textos_v407.py` está nos seus `arquivos_revisados`: a trava S1b está FECHADA agora, como deve, até você gravar o sha16 novo.
5. `rito_v407.sh:22` — só o comentário: «379 s + 245 s» e «Audit de 245 s» deram lugar aos medidos de `kernel\construir_marcas.txt`. `sh -n` limpo. Nenhum comando mudou.
6. Cadeia refeita do zero depois disso: `refazer_out_v407.txt` (== FIM, RC_REFAZER=0, «PRECONDICOES v407: TODAS PASSARAM») e `fim_de_cadeia_out_v407.txt` (RC_FIM=0); as saídas da R2 ficaram em `refazer_out_v407.R2g_aprovada_8baixos.txt` e `fim_de_cadeia_out_v407.R2g.txt`.

## O que se revisa (só isto)
A. O diff de cada arquivo do item 1–5 contra o seu `.bak_r3_*` é exatamente o declarado acima (e nada mais). `py_compile` limpo nos `.py`.
B. O candidato novo: sha16 lido do arquivo no início e no fim; `COMPARACAO_V406_v407.json` ok; as 25 `expected_ladder`, as funções intocadas e o kernel embutido (9 módulos == sandbox == `pedra\` == BUNDLE) iguais aos da R2 (`a_intocados.py`, `a2_mudados.py`, `d_kernel.py` podem ser rerodados; `f_hashes.py` para os hashes).
C. Os 4 BAIXOS novos da R2: estado ATENDIDO / DITO / NÃO ATENDIDO com evidência. Os BAIXOS da R1 que ficaram DITOS (aspas nas pedras; «virar essa chave» sem [ONTO] na pedra; os resumos do acervo) continuam DITOS: são das pedras, que não se tocam nesta versão (a gerência os leva ao caderno da v408).
D. A trava S1b: com os `arquivos_revisados` novos ela abre; com um arquivo de `pos_rito\` alterado ela fecha (ensaio só na cópia `_orq_sandbox`, ESTADO real intocado).

## Limites
Os da R2 (só leitura no Nós e no kernel canônico; nenhum `lake build`; nenhum POST à Bancada; nenhum git; nenhum processo morto por nome; não executar o orquestrador original, `refazer`, `fim_de_cadeia`, `instalar` nem `rito`; não escrever fora de `revisao_terceiro\`; hash sempre lido do arquivo). Gestão de tokens: não reler o um.py inteiro; não repetir o que a R2 aprovou e não mudou.

## Entrega
1. Guardar a R2 em bytes: `REVISAO_TERCEIRO_v407.R2.json` e `.R2.md`.
2. Gravar `REVISAO_TERCEIRO_v407.json` (rodada "R3") no mesmo formato, com `candidato_sha16` novo, `achados` (os que restarem), `baixos_da_r2` (os 4, com estado), `arquivos_revisados` refeitos (todos os da R2, com os sha16 atuais, inclusive `pos_rito\textos_v407.py`), `candidato_mudou_durante_a_revisao`, `nota`; e o `.md`. `aprovada: true` só com 0 ALTO e 0 MÉDIO.
3. Resposta em até 12 linhas: aprovada ou não; n_alto/n_medio/n_baixo; sha16 do candidato; os 4 BAIXOS da R2 e seu estado; os dois caminhos gravados.
