**A cópia vira referência na Central pública (decisão do operador, 11/11/2026; vale a partir da publicação da v411).** Pedido dele: «Precisamos resolver a questão da central de patentes com o github, pq ele não aceita mais de 100MB e talvez estejamos subindo alguns arquivos desnecessários para a pretensão, ou ao menos, fazer de uma forma que possamos subir tudo sem ultrapassar o limite do github». Escolhas dele (AskUserQuestion): «Cópia vira referência (Recomendado)» e «Na publicação da v411 (Recomendado)». Verbatim: `work\cunhagens_13out\OPERADOR_11nov_central_publica_copia_vira_referencia_verbatim.txt`.

**A medição [REAL]** (`work\github_limites_11nov\MEDICAO_11nov.txt`; rota `infra.github.limites_central_publica_11nov`, registro 1988):
- **Limites do GitHub** (documentação oficial, lida em 11/11): obrigatórios, 100 MB por arquivo e 2 GB por push; recomendados, 10 GB em disco e 3.000 entradas por pasta.
- **Tamanho:** os cinco repositórios ocupam de 0,30 a 0,68 GB no GitHub. Nenhum arquivo passa de 50 MB; só o índice gerado do work passou de 100 MB (resolvido em partes na v410).
- **Cópias:** nos três públicos, 698.235 dos 843.319 arquivos (83%) são cópias idênticas de arquivo já publicado. Com a referência só dentro do mesmo repositório, sobram 170.202: central-publica 15.620, bancada 55.714, work 98.868.
- **O `um.py`:** 45,9 MB, crescendo de 0,7 a 1,1 MB por versão. O aviso de 50 MB vem em umas 5 versões e não bloqueia; o bloqueio de 100 MB, em umas 50, e pede decisão própria quando chegar (LFS não serve: o raw passa a devolver o ponteiro).

**O que foi construído [REAL], em `work\central_publica_22out`:**
- `copias_referencia.py`, o passo novo `referenciar_copias_<repo>`, logo antes do `readmes`. A entrada da cópia ganha `igual_a`, e o arquivo físico sai do preparo.
  - O original é estável: fica o que já era original, já publicado, e só depois o menor caminho.
  - Os arquivos fixos (raiz gerada, partes do índice, esteira do work) nunca viram referência.
  - Antes de apagar, confere o sha256 do original e o da cópia.
  - Grupo sem arquivo físico volta do HEAD do preparo: primeiro pelos caminhos do grupo, depois por qualquer blob de mesmo tamanho, sempre conferido pelo sha256.
  - Se o original foi excluído pela esteira, PARA: as cópias têm os mesmos bytes e a decisão é humana.
  - É tudo ou nada, e grava `RECONSTRUIR_COPIAS.py` na raiz, que recria as cópias num clone e lê as partes do índice.
- `conferir_preparos.py`, a conferência independente, que não importa o construtor. Verifica que:
  - toda referência aponta para um original não referência do mesmo índice, com os mesmos bytes;
  - o arquivo do original tem esse sha256 (cada original é lido uma vez);
  - a cópia física não ficou no preparo e a raiz traz o script;
  - a falta física da cópia não conta como «índice sem arquivo».
- `atualizar_repo_publico.py` leva ao git só o que não é referência, e o commit diz quantas cópias ficaram só no índice. O `gerar_readmes_publicos.py` explica `igual_a` e o script. O `reparar_indice_sem_arquivo_25out.py` não toca as referências.
- **Testes:** `testar_copias_referencia.py` passa em todos os casos, com publicação real num remoto local e um clone reconstruído, também com o índice em partes. `testar_indice_partes.py` segue passando.
- **Simulação nos preparos reais** (só leitura; `work\github_limites_11nov\SIMULACAO_11nov.txt`), sem nenhuma parada e com toda cópia e todo original conferidos pelo sha256:
  - central-publica: 50.403 referências, 2.923 originais, 176 s;
  - bancada: 160.751 referências, 10.114 originais, 508 s;
  - work: 461.963 referências, 14.326 originais, 11,27 GB conferidos, 1.242 s.
  - A primeira aplicação soma cerca de 32 min ao C18 da v411; depois, só as cópias novas.
- **Links:** nenhum dos 24 links públicos para os três repositórios (no the_boundary, no site e nos README e llms.txt da raiz) aponta para um caminho que vira referência, e nenhum link de pasta fica vazio.

**Errata na G1 [REAL]:** na v410, a primeira chamada do C18 levou 14.322 s, contra o timeout de 14.400 s (78 s de folga). No timeout, `util.rodar` mata só o encadeador, e o `git push` aberto segue órfão. O timeout subiu de 4 h para 8 h em `tools\custodia_g1\publica.py` (commit `27167a7c4`, no GitHub).

**How to apply:** a primeira aplicação é na v411 (C18); antes, nada muda no ar. Ela apaga do preparo e da árvore do GitHub cerca de 673 mil cópias. O conteúdo segue no original, e o histórico do git guarda tudo. Na v412 em diante, só as cópias novas. A c1 já anotou a outra metade, do lado da preparação: tirar de `work` as cópias do kernel por rodada. [[licoes-custodia-v410-11nov]] [[central-publica-22out]] [[git-e-vitrine-nao-backup]]
