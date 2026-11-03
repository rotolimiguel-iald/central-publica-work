# DERIVAÇÃO v405 -> v406 (encanamento): notas do executor mecânico

Data: 02/11/2026. Executor mecânico a serviço da gerência c1. Receita seguida: `work\fechamento_02nov\RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md`, seções 1(a), 4 e 5.
Escreveu só em `PK6 = work\cadeia_de_selo\v406\` e em `C:\t\k406c\`. Não tocou no Nós, no `k405c`, em `v405\`; não rodou `um.py`, `lake` nem `lean`; não editou memória.
Resumo e números: `DERIVACAO_v406_RESULTADO.json` (esta pasta). Estatuto: tudo aqui é [REAL] medido por mim ao rodar; os ajustes são escolhas minhas, ditas abaixo para a gerência desfazer se discordar.

## 1. O que fiz de diferente da cópia literal (cada ajuste, arquivo:linha, e por quê)

Os arquivos de `v405\` não foram copiados: os da família `derivar_*` foram gerados pelo mapa mecânico do motor (origem única `v405`; mapa 404 -> 405 e 405 -> 406; nomes nascidos no `um.py` ficam).

**`_mk_motor_v406.py` -> `derivar_v406_motor.py`** (molde `_mk_motor_v405.py`, que lia o motor da v404; este lê `v405\derivar_v405_motor.py`):
- l.16-25: docstring do motor reescrita para a v406.
- l.26 `ORIGENS`, l.27 `NUM3` com 405, l.28 `MAPAS = {"v405": {"404": "405", "405": "406"}}`, l.29-39 docstrings/`base_v405`/comentário de `copiar_base_v406.py`, l.32 (2x) e l.35 e l.44: `fullmatch` com 405, l.33-34, l.36-37, l.42-43: defaults `origem="v405"`, l.38: comentário do E402, l.39: `linhas_com` até 406. Todas com contagem exata asserida (o `_mk` aborta se a contagem não bater).
- l.40-41 **ajuste meu, fora da receita:** `derivar()` do motor da v405 substituía um derivado existente com `--refazer` sem backup; no v406 grava `.bak_<ts>` de bytes antes de substituir (regra do backup imediato). Efeito: aparecem `.bak_*` de derivados refeitos em `pos_rito\` e dos JSON.

**`_mk_lotes_v406.py` (novo, 1 script)** gera os 12 lotes `derivar_encanamento_v406_regras*.py` a partir dos 12 de `v405\` pelo mesmo `bump` do motor (origem v405). Os lotes não podem ser cópia literal: nomes-fonte (`pos_build_kernel_v404.py`) precisam virar `..._v405.py` (a origem agora é a pasta v405). Três correções com contagem exata, todas no próprio script:
- l.15: lote E3, o par de nomes do comparador. `comparar_v403_v404.py` (origem da v405) subiria para `comparar_v403_v405.py`, que não existe (403 não está no mapa); corrigido para `comparar_v404_v405.py` (2 ocorrências). O destino sai `comparar_v405_v406.py`.
- l.17-22: lote F (pós-rito). A regra `_NOTA` põe uma nota de estado no topo e a `_tira_nota_antiga` tira a anterior por regex com data `28/10/2026`; no texto da v405 a nota antiga tem `01/11/2026`. Sem a correção a regra "passa" (o `re.sub count=1` não falha quando não acha) e 9 dos derivados do pós-rito saíam com DUAS notas, a nova AFIRMANDO uma adaptação que na v406 ainda não existe. Corrigido: data da nota antiga 28/10 -> 01/11 (2 ocorrências) e a nota nova passou a dizer "SUBIDA MECÂNICA ... AINDA NÃO adaptada" (1 ocorrência cada).
- l.24: assevera que são exatamente 12 lotes na v405.

**`derivar_encanamento_v406.py`** (escrito por mim, molde `derivar_encanamento_v405.py`):
- l.11-16: importa `derivar_v406_motor`; `entrada(..., origem="v405")`.
- l.20-30 **ajuste meu:** a v405 fazia `exec` de todos os lotes no import, e um lote cujo PREÂMBULO não carrega derrubava tudo. Agora o lote que não carrega é registrado (`LOTES_NAO_CARREGADOS`, com a linha do lote), suas entradas parciais saem e os demais seguem. Nenhuma regra é forçada; a falha de entrada continua abortando (como na v405).
- l.47-50: o JSON de saída sai por `.tmp` + `os.replace`, com backup de bytes se já existir (a v405 usava `open(..., "w")` direto).
- `derivar_encanamento_v406.py --refazer` (o comando da receita) devolve rc 1 na primeira entrada que não casa (ver 3.1) e por isso NÃO grava `DERIVACAO_ENCANAMENTO_v406.json`.

**`rodar_por_entrada_v406.py` (novo)** tenta cada entrada separadamente e grava `DERIVACAO_ENCANAMENTO_v406_POR_ENTRADA.json` (é o "siga com os lotes que passam" da ordem). Uma entrada que aborta não grava nada (o motor só grava depois de todas as regras e do `ast.parse`).

**Lote novo `derivar_encanamento_v406_regrasI_base_kernel.py`** (a v405 escrevia estes dois scripts à mão; os passos 3 e 4 da ordem os exigem):
- l.7: o sha16 que entra no docstring de `copiar_base_v406.py` é LIDO do `um.py` do Nós na hora (não digitado).
- l.17-20: `copiar_base_v405.py` -> `copiar_base_v406.py` (a Bancada: `B13` -> `B14, B14-v405-20261102-R1 [DECLARADO pela receita]`).
- l.21-24: `preparar_kernel_v405.py` -> `preparar_kernel_v406.py` (junção continua descrita para o `k404c`, não para o `k405c`; banner: só o modo `copiar` está pronto).

**`delta_v406.py` (esqueleto, escrito por mim):** só as constantes que `copiar_base` e `preparar_kernel copiar` leem (`NOS`, `V405`, `BASE_DIR="base_v405"`, `BASE_VERSION="v405"`, `BASE_SHA16_DA_ORDEM`, `SANDBOX=C:\t\k406c\final`, `PACKAGES_ORIGEM=C:\t\k404c\...`). Não importa o `delta_v405` (não executa a cadeia herdada). `BASE_SHA16_DA_ORDEM` é o valor da ordem da gerência (a mensagem de tarefa e a receita); conferi com `sha256sum` independente do `um.py` do Nós e com o selo/ESPERADOS dentro do `copiar_base`. O delta completo (os ~300 módulos, STONES, ROOT_SUFFIX...) é da gerência e SUBSTITUI este arquivo.

**`copiar_k406c.sh` (escrito por mim; a receita o lista como autoral):** igual ao `copiar_k405c.sh` com `k406c` e origem = Nós v405; a junção `.lake\packages` aponta para `C:\t\k404c\final\.lake\packages` (NÃO para o `k405c`: bumpar o `k404c` mecanicamente daria `k405c`, que a receita manda não reusar).

## 2. O que passou (24 de 35 entradas) e o que isso vale

Passaram mecanicamente (só o mapa, ou o mapa + regras que casaram): `purga`, `guarda_p18`, `acom_conferencias`, `runtime_quadro_v397`, `quadro_v397` (regra do `import delta_v406`), `refazer_candidato.sh`, `refazer_sandbox_..._pos_selo.sh`, `refazer_arvore_..._pos_selo.py`, `pino_memoria_py`, os 12 de `pos_rito\` (incluída `textos_v406.semente`; só b3_recibo falhou) e `bateria_pre_selo\rodar_bn_pre_selo_v406.sh`, `copiar_base_v406.py`, `preparar_kernel_v406.py`.
**Cuidado, é só subida de rótulo:** o corpo ainda é o da v405 (OITO pedras, textos, especificações). "Passou" não quer dizer "adaptado à v406". Em 9 dos 12 de `pos_rito\` (os que têm a regra `_NOTA`) há a nota de estado no topo dizendo isso.

## 3. O que falhou (fail-closed) e o que a gerência tem de reescrever

### 3.1 Entradas cuja regra não casa (11). Contagem esperada 1 em todas, contagem achada 0
Causa comum: as regras de contagem exata dos lotes da v405 descrevem o TEXTO DA V404 (padrões como «DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32)»); no texto da v405 elas já foram aplicadas, então não existem mais. Quantas regras de cada entrada casam sozinhas / quantas não (de `DIAGNOSTICO_REGRAS_v406.json`; cada regra testada isoladamente):

| entrada (lote) | regras | casam | não casam | primeira que falha (índice, trecho) |
|---|---|---|---|---|
| `pos_build_kernel_v406.py` (A) | 6 | 1 | 5 | #1 «a lista dos modulos novos (preparar_kernel_v406.py) tem de ser so' as DUAS pedras...» |
| `conferir_rito_v406.py` (D1) | 38 | 2 | 36 | #1 `RN405 = sorted(ESP["registros_v402"]); RN406 = ...` |
| `teste_conferidor_positivo_v406.py` (D1) | 2 | 0 | 2 | #0 `import hashlib, importlib.util, io, json, os, shutil, subprocess, sys` |
| `gerar_esperados_v406.py` (D1) | 21 | 2 | 19 | #1 AssertionError «ancora inicial nao unica», regra «marcas do artigo» (`TW406 = "Jo 8,32 e a projeção transversal da Meia-Nat"`), contagem 0 |
| `diff_e_pinos_v406.py` (D3) | 2 | 0 | 2 | #0 «o diff do kernel nao e' so' as duas pedras + a raiz...» |
| `conferir_citacoes_v406.py` (D3) | 13 | 2 | 11 | #2 `alvo = {"_V404_VERBATINS2", "_V404_SPECS", "_V404_CONTRACTS"}` |
| `p00_precondicoes_v406.py` (E1) | 17 | 1 | 16 | #0 `not any(k.endswith("_v404") for k in core) and all(k in core for k in ("caminho_v403", ...` |
| `regras_v406.py` (E2) | 1 | 0 | 1 | #0 «ESCRITO em 27/10/2026 pela preparacao» |
| `regerar_v406.sh` (E2) | 2 | 0 | 2 | #0 «tudo o que depende das TRES PEDRAS (work\cadeia_de_selo\v406_kernel\pedras\Caminho.lean...» |
| `comparar_v405_v406.py` (E3) | 6 | 0 | 6 | #0 «Os nos NOVOS esperados sao so' os da v406 (os tres registros com funcao...» |
| `pos_rito/b3_recibo_v406.py` (F) | 2 | 1 | 1 | #1 «pina a v405, B12, deployment B12-v405-20261028-R1, e o Nos passou a v406...» (a v405 já traz B13/B14) |

**Aviso importante sobre "casam":** as regras que casam isoladamente são em grande parte do tipo `entre(...)`, que substitui um trecho inteiro pelo texto da v405 (bumpado). Se a gerência consertar as que não casam e rodar, essas passam em silêncio injetando narrativa da v405 («OITO pedras», `_DOC_PB` etc.). Reescrever TODAS as regras de cada entrada, não só as que falham.

### 3.2 Lotes que nem carregam (3), registrados em `lotes_nao_carregados`
- `derivar_encanamento_v406_regrasC.py` (ensaio: `simular_arvore_do_nos`, `exame_pontos`, `guardas_estaticas_bancada`), linha 11 do lote: `AttributeError: module 'delta_v406_regras' has no attribute 'D4'`. O lote compara o delta novo com o predecessor (`DL5.D4`, `D4 = delta_v404`); o delta da v406 precisa expor o predecessor (por convenção seria `D5 = delta_v405`) e o lote trocar `D4` por `D5`. Só a gerência escreve o delta. Entradas deste lote NÃO foram derivadas.
- `derivar_encanamento_v406_regrasC2_ensaio.py` (`ensaio_a_seco`), linha 208 do lote: `ValueError: substring not found` (a âncora `# (6i) [v404] os TRES registros com FUNCAO da v405` do texto original da v405 não existe como escrita; é lote que injeta blocos do ensaio por índice de âncora).
- `derivar_encanamento_v406_regrasD2_instalar.py` (`instalar`, `reverter`, `rito_v406.sh`, `conferir_instalar_rito`), linha 7 do lote: `FileNotFoundError ... v406\kernel\construir_marcas.txt`. O lote lê os tempos MEDIDOS do build do sandbox novo (`epoch_inicio`, `epoch_build_fim`, `epoch_audit_fim`), que só existem depois do `construir_kernel_v406.sh` (passo da gerência). Por desenho não deriva antes disso: `instalar_v406.py`, `reverter_v406.py`, `rito_v406.sh` e `conferir_instalar_rito_v406.py` NÃO existem em PK6.

### 3.3 Narrativa que o mapa não corrige (comentários e docstrings dos derivados)
Os rótulos sobem, mas o conteúdo dos comentários continua o da v405: ex. nos lotes, «Mapa: 403 -> 405, 405 -> 406» (o 403 não sobe), «(a que rodou em 28/10)», «OITO pedras» no docstring de `preparar_kernel_v406.py`, «rito de 28/10» em vez de 01/11. Não afeta a execução; precisa de revisão antes de a gerência assinar qualquer derivado.

## 4. O sandbox `C:\t\k406c\final`
Criado por `preparar_kernel_v406.py copiar` -> `copiar_k406c.sh` (robocopy do `Nós\tgl_kernel`, sem `.bak_*`, sem junções). Conferido depois: 1412 `.lean` em `TGLExt` (= Nós), 184 em `TGLExt\F1Fecho394` (= Nós; **o bundle dos 300 NÃO foi gerado**), 27 em `TGL` (= Nós), raiz `TGLExt.lean` com o mesmo sha16 do Nós (`5dd444489d5547e0`, lido por `sha256sum`), 0 `.bak_*`, `.lake\build` com 8,2 GB; junção `.lake\packages` -> `C:\t\k404c\final\.lake\packages` (mount point; `Mathlib.olean` alcançável). Não rodei `gerar`, `conferir`, `construir`, `regerar`.

## 5. O que ficou para a gerência, na ordem da receita
1. Escrever o `delta_v406.py` completo (substitui o esqueleto) com a lista dos ~300 módulos e a decisão da raiz (receita 5.1.3).
2. Decidir o `D4`/`D5` do lote C e reescrever as regras dos lotes A, C, C2, D1, D2, D3, E1, E2, E3 e F (b3_recibo) para o texto da v405, entrada por entrada (3.1 e 3.2).
3. Só depois: `copiar_pedras`, `gerar_pino_das_pedras`, `preparar_kernel_v406.py gerar/conferir`, `construir_kernel_v406.sh` (medir o tempo; o lote D2 lê o resultado), `pos_build_kernel_v406.py`...
