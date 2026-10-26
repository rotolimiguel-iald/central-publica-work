# G1 — lições da primeira custódia CONJUNTA (v399 + v400), 25/10/2026 (gerência a7)

Registro do que a custódia viva da v400 ensinou ao G1. Cada item: o defeito, o conserto (ou o que falta), o patch.

1. **Título PT sem módulo novo**: o cabeçalho do handoff dizia «nenhum módulo novo» e o RE_CAB só aceitava dígitos. Conserto: `(?P<k>\d+|nenhum)` em nos.py (patch_g1_v400_textos_e_cabecalho.py).
2. **Textos que o handoff não traz** (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN/PT, COMMIT): agora lidos de `work/custodia_<v>_*/TEXTOS_<v>.md` (mesmo patch). O portão de texto continua valendo sobre eles.
3. **Custódia conjunta** (anterior do handoff = v399 selada sem cofre; maior cofre = v398): fatos.py reconhece `conjunta: [v399, v400]` e lê kh/cunhagens do registro mais novo entre (anterior, N] (patch_g1_v400_conjunta.py).
4. **E03 exigia os pares _vK_FONTES/_VERBATINS2** para versões sem registros: relaxado em espelho_pares.py (`_fontes_pinadas`).
5. **C3 (registros novos) saiu vazio** na conjunta: central.py passa a contar `_ka < K <= _kv`. A primeira tentativa do cofre foi movida para fora (`cofre_v400_tentativa1_registros_vazios/`), nunca commitada.
6. **C4 S3_blocos_bem_formados**: `_checks_ok` aceita pares `[str, True]` (4 cópias: generico e runner da fronteira; camada generica e a da fórmula completa).
7. **C5 lançou snapshots duplicados**: `_ap_c5` volta cedo se `_ja_c5` diz «em curso». Os duplicados foram encerrados pelo PID que o próprio G1 criou.
8. **C8 CRLF**: regex `\)\r?$` em `_camada_no_texto`.
9. **C17A ACOM recusou registro sem fonte**: memorias.py dá fonte explícita a d1_gatilho (ordem verbatim + handoff) e p1_do_operador (handoff) (patch_g1_acom_fontes.py).
10. **C15 a conferência final pegou o Atlas pendente** (as mudanças pós-rito da c1 + o append do C13): commit de memory/ antes de retomar. Lição: o G1 deveria commitar as superfícies de memória que ELE tocou antes do C15, ou dizer quais ficaram pendentes e de quem são.

## A fazer (não feito ainda)

- **--trabalho relativo** quebrou o commit (E10): exigir caminho absoluto no argparse (recusa visível).
- **Letras gregas no assunto do commit** viraram vazio («o  de uma linha so»): transliterar (α→alfa, β→beta) em vez de apagar. O commit b8e028fb fica como está (sem reescrever histórico).
- **E08 marcou APLICADO sem regenerar o README** (o laço da frente foi rodado à mão): o E08 deve conferir o BLOB do README contra o gerado, não só o arquivo existir.
- **E08: o README passou de 40 KB** (41.179 B): o gerador tem o assert; o G1 deve tratar a falha do assert como BLOQUEADO com a mensagem, não seguir.
- **Escrita no túnel durante a cópia do E03**: a gerência gravou um adendo no túnel no meio da cópia e a conferência falhou. O E03 deve tirar a lista de arquivos e os hashes num instante só, e reconferir só essa lista.

## Depois da primeira retomada (25/10, 06h)

11. **C18 parou na conferência do delta do work** (REPROVADO, certo): o ambiente conda/mamba do teste de voz dos filmes V7 (`work/filmes_v7_20261024/voice_test/mamba_root`, 21.927 arquivos de pacotes de terceiros) entrou no preparo; os 3 «credenciais em texto» eram da biblioteca padrão do Python. Conserto: `excluir_do_preparo.py` tirou os 21.927 do preparo e do índice com o motivo registrado (não voltam por rodada incremental), e o EXCL_DIR dos dois construtores de região ganhou os marcadores de ambiente conda (`patch_excl_ambientes_conda_25out.py`). A conferência independente fez o seu papel: parou antes de publicar.
12. **Cartão de estado no E15** (ORDEM 023): `gerar_cartao_estado.py` gera `estado.json`, `estado.txt` e `read-brief.txt` depois do push do espelho, com o commit imutável conferido pelo blob do git; o `_ja_e15` exige o pin16 nos dois cartões (`patch_g1_cartao_estado_e15.py`).
13. **E17 parou nos arquivos novos do cartão** (L10, certo: o ensaio só pode diferir no que a custódia escreve): o conjunto ESPERADOS de site.py ganhou `read-brief.(md|txt)` e `estado.(json|txt)`. Os três consertos do «A fazer» (gregas no assunto, --trabalho absoluto, frente do README no E08) foram aplicados com o G1 parado (`patch_g1_licoes_v400.py`); o E08 segue APLICADO com a conferência nova.

## Na custódia da v401 (25/10, tarde)

14. **E08B (L01) resolvido pela gerência com a VAGA FIXA «última custódia»** na frente do README: a seção «Read in this order» (638 B) virou «Latest custody», com o título do parágrafo pronto mais novo lido por script do ESTADO_ATUAL.md; o E08B passou a APLICADO sem cortar nada (`work/custodia_v401_25out/patch_vaga_ultima_custodia_readme.py`; commit do espelho `f6036a7f`, empurrado antes do E03 porque o E03 exige árvore limpa e HEAD = origin/main).
15. **C3 procurou FATOS_CUSTODIA.json no Nós**: a v400 foi o primeiro cofre feito pelo G1, e ele guarda os documentos da própria custódia (FATOS_CUSTODIA.json, SEMANTICA_CUSTODIA.json). O C3 da v401 tomou esses arquivos do cofre base como artefatos a copiar do Nós. Conserto: os dois entram no EXCL_RAIZ de central.py.
16. **Escrita no túnel**: o adendo B dos filmes só entrou no túnel depois do E03 (a lição 5 da v400).
17. **O túnel é pasta viva** (Codex e gerência escrevem nele o tempo todo): o _ja_e03 comparava a cópia do espelho com o túnel vivo, e qualquer ordem ou entrega posterior reabria o E03, cujo reaplicar falhava nas pré-condições (espelho já na versão; árvore com o trabalho da própria custódia). Aconteceu na retomada da v400 e na v401. Conserto: com o espelho na versão, pares TUNEL com destino ausente ou tamanho diferente vão para a próxima custódia e não reabrem o E03 (`patch_g1_tunel_vivo_e03.py`). A lição 16 vira desnecessária.
18. **C4 quebrou com a cobertura da ANTERIOR vazia**: a v400 não trouxe `kh_n1_cobertura_v400`; o patch da conjunta só tratava a versão corrente, e a pedra genérica comparou 29318 >= None. Conserto: sem registro próprio da anterior, vale o mais novo até ela no core dela (`kh_registro_anterior`, aqui o da v399) (`patch_g1_kh_anterior.py`). Os fatos foram sondados de novo (o G1 não sobrescreve: gravou ao lado e a gerência adotou, com backup).
19. **Cofre parcial depois de falha**: duas tentativas do C3 deixaram cofre parcial; o G1 recusou sobrescrever (certo) e a gerência os moveu para a pasta de trabalho (`cofre_v401_tentativa1_PARCIAL_*`, `cofre_tentativa2_*_PARCIAL_*`), nunca apagou. A fazer: o C3 montar o cofre numa pasta temporária e renomear no fim, para que uma falha não deixe parcial no lugar do definitivo.
20. **C8 gerou `("v400",, "v401",)`**: a tupla CAMADAS_GENERICAS já terminava em vírgula e o gerador de patches.py somava outra. O G1 conferiu a sintaxe ANTES de trocar e não gravou nada (certo). Conserto: tirar a vírgula final antes de somar a versão.
21. **A errata da v401 saiu com «None -> 29318» e o registro v400 inexistente** (achado ALTA da revisão cética independente): o E04 gerou os textos com os fatos antigos, antes do conserto da cobertura da anterior, e o E04/E05 não se refazem sozinhos. Corrigido no gerador do ESTADO e no LEDGER pelos números dos fatos (`patch_errata_v401_revisao*.py`), ESTADO regerado, laço E08 rodado pela própria função do G1 (`rodar_e08_forcado.py`). Raiz: textos.py usa `kh_registro_anterior` e RECUSA cobertura anterior ausente (nunca mais «None» num texto público); o molde do LEDGER tira o ponto final do texto. Lição: quando os fatos mudam depois do E04, refazer E04→E05→E08 antes do E10.
22. **Queda de energia no meio da mescla da Central pública** (25/10, noite): o índice do preparo do work ficou com 10.339 entradas sem arquivo; a conferência independente reprovou (certo). Reparo `reparar_indice_sem_arquivo_25out.py`: copiar da origem só o que tem o sha256 do índice (10.332), tirar do índice o resto (7), backup do índice. A fazer: a mescla gravar o índice só DEPOIS de todas as cópias conferidas (já é a ordem) e fsync; e a conferência dizer «índice sem arquivo» como causa provável de queda.
