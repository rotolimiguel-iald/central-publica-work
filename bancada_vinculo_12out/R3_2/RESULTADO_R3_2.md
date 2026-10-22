VINCULO R3.2 — 13/10

# Resultado da R3.2 do esboço `sincronizar_bancada.py` (F0.6, elo B(n) da cadeia de selo)

Construtor: subagente da gerência c1.

**A base.** A R3.1 em `..\R3_1\`, com os pinos conferidos por script antes de tocar [REAL]:
- `sincronizar_bancada.py` `a85be74ffd7a1dee`;
- `montar_sandbox.py` `15c699b5a4fcc83d`;
- `controles_negativos_r3_1.py` `a7614fe341b1461a`;
- `CONTROLES_NEGATIVOS_R3_1.json` `6e27894064399966`.

**A ordem.** Veio da reauditoria curta `AUDITORIA_F0_6_C1_a721b706.md`, com a decisão da gerência [INPUT] de fechar todos os achados nesta rodada. Cada achado tem um controle negativo que reproduz o caso exato do auditor e pelo menos uma variante.

**Estatutos.** [REAL] = medido aqui por script. [DERIVED] = composto. [INPUT da gerência] = a decisão e os esperados do `CRITERIOS_v392.json`. [DECLARADO] = números do plano transcritos sem conferir. [CONJECTURE] = não medido.

Nada aqui move o gate. Nenhum dado observado. NOT_FALSIFIED nunca é creditação.

## 1. Veredito

**`TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO`: 399/399 em 710 s, rodados com `python -I -B -X utf8`** [REAL, `CONTROLES_NEGATIVOS_R3_2.json`, sha16 `65b397e4a8b43135`]:
- os 337 da R3.1 estão presentes, 337/337, com os mesmos nomes; os 235 da R3 também;
- há 62 controles novos (prefixo `R32_`);
- 42 controles da R3.1 mudaram de formato, com o motivo de cada um no JSON. São 37 motivos R31-3 (32 controles pela injeção de `--selo-anterior`/`--kernel-manifesto-anterior` e 5 pelas chamadas unitárias do pré-selo) e 5 motivos R31-1 (a flag do interpretador). Há também 3 mudanças gerais: todo subprocesso com `-I`, a fixture `KERNEL_RECIBO_R3_2` e a custódia v391 do sandbox;
- o próprio script dos controles roda com `-I -B -X utf8`, e as chamadas em processo de `main()` conferem o interpretador corrente.

**A rodada 1 falhou num controle e achou uma regressão real minha.** Fica como registro em `CONTROLES_NEGATIVOS_R3_2_rodada1_397de398.json` (`31679735d62973f4`).
- **O que falhou.** 397/398: o controle `N5_modulo_sombra_ao_lado_da_fonte` (da R3) reprovou.
- **A causa.** Sob `-I`, o `site.ENABLE_USER_SITE` é falso no processo do esboço. Com isso, `sombreaveis()` deixava de listar os módulos do site do usuário, e um `numpy.py` ao lado de fonte pinada deixava de ser visto. Os testes ainda recebem o site do usuário como caminho, pelo lançador.
- **O conserto.** `sombreaveis()` passa a incluir o site achado pela pasta conhecida do Windows e o do `APPDATA` herdado, independentemente da flag. Há um controle novo para isso: `R32_R31_1_sob_I_o_site_do_usuario_segue_sombreavel`.
- **A rodada 2** deu 399/399.

## 2. Os runs refeitos, todos com `-I -B -X utf8` [REAL, sandbox `C:\t\vb7`; cópias em `evidencias_sandbox\`]

| run | o que é | resultado | recibo (sha16) |
|---|---|---|---|
| 1a | pré-selo, ensaio, b1 (manifesto pina o Nós real), bateria inteira | `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA`; 13 PASSA, 0 FALHA, T17 fora da fase | `378340624a19e36f` |
| 1b | o mesmo contra b2 | idem; é o recibo pré-selo que o B3 encadeia | `f3fbb6af9983752e` |
| 2 | pós-selo, aplicar `--sandbox` em b2, com tudo pinado e com `--selo-anterior`/`--kernel-manifesto-anterior` | `REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`; 13 PASSA (detalhe abaixo da tabela) | `1a1dd21e08ea1b14` |
| 2bis | o B3 de novo | `JA_SINCRONIZADA__NADA_A_GRAVAR`; o pré-selo foi cruzado também pelo `sincronizacao.anterior.kernel_manifesto_sha256` que o manifesto B3 gravou (`afd57149c5b26928`) | `cf7e382440ee575b` |

**O T17 do run 2.** Contrato `KERNEL_RECIBO_R3_2`, com:
- os jobs do lake das pedras, da raiz e do Audit no build log;
- o log do Audit cobrindo os 2 `#print axioms` distintos por nome;
- a varredura de tokens recursiva recontada: 5 `.lean`, 1 em `TGLExt/O16`;
- a `x19 = «nao»` cruzada com as pedras.

**A aplicação do run 2.** As duas conferências pós-troca deram o manifesto novo, `fd8284e648c10d37`. O pré-selo foi cruzado com o selo anterior `95061f18c7102248` e com o manifesto do kernel anterior `afd57149c5b26928` da custódia do sandbox.

Em todos os recibos, `python_isolado` diz `isolated`, `safe_path`, `utf8_mode` e `dont_write_bytecode` verdadeiros. A bateria inteira da R2 passou com o esboço em `-I`, inclusive os testes que importam numpy, scipy e torch, e os netos.

## 3. Os consertos e os controles novos

| achado | conserto | caso exato do auditor → resultado | variantes (todas recusam como esperado) |
|---|---|---|---|
| **R31-1** (MÉDIA) | o esboço exige `python -I -B -X utf8`. A guarda vem na 1ª linha de código, antes de qualquer `import` além de `sys`, e recusa com `INTERPRETADOR_NAO_ISOLADO` (rc 2), sem nada gravado. `main()` confere de novo (chamada em processo); `sombreaveis()` vê o site do usuário sob `-I` | o `json.py` do auditor ao lado do esboço, chamado com `-s`: **recusa, 0 marcas** (na R3.1 executava no processo que grava a produção) | com `-I`, `json.py`, `argparse.py` e `sitecustomize.py` ao lado não executam (0 marcas) e o esboço roda; `-s -P` recusa; `-I` sem `-B` recusa; `-I` sem `-X utf8` recusa; `-E -s` sem `-I` recusa; em processo com flags simuladas, recusa; no código, só `import sys` vem antes da guarda; A4 com `APPDATA` de ataque e `-I`: 0 marcas em processo nenhum; A9 com `-I -B`: nenhum `__pycache__` |
| **R31-2** | depois da última sonda o manifesto é relido e tem de ser o novo, byte a byte, antes do recibo em `estado\`; depois de gravá-lo, é relido de novo. Se diverge: os bytes estranhos ficam em `--saida` com sha, o recibo em `estado\` sai, há rollback e a sonda depois do rollback | mudança do manifesto (mesmo tamanho e mtime) durante a 6ª sonda: **`APLICACAO_REVERTIDA: MANIFESTO_MUDOU_APOS_A_TROCA`**. O disco volta ao anterior, a evidência tem o sha mudado e não há recibo em `estado\` (na R3.1: rc 0, APLICADA) | mudança logo depois do recibo em `estado\` (`…MANIFESTO_MUDOU_APOS_O_RECIBO_EM_ESTADO`, o recibo em `estado\` retirado); serviço no ar depois desse rollback (`SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`, a causa no texto); a ordem no código; a contraprova aplica com as duas conferências |
| **R31-3** | o recibo pré-selo é cruzado com o pino do kernel que o **selo anterior** grava. O selo anterior vem de `--selo-anterior` (sha == o selo pinado no manifesto da Bancada) e o manifesto do kernel, de `--kernel-manifesto-anterior` (sha == esse pino). A raiz, o Audit e a impressão são recalculados. A partir do B4, o pino gravado no manifesto da Bancada também confere | selo certo, pino do kernel e raiz, Audit e impressão forjados de forma consistente no próprio recibo: **recusa `RECIBO_PRE_SELO_NAO_CORRESPONDE`**, unitário e no decoy de produção, e a recusa vem do selo anterior (na R3.1: aceito) | pino verdadeiro com raiz, Audit e impressão forjados; selo anterior forjado; manifesto do kernel de outro rito; sem selo anterior (unitário e subprocesso); flag sem `--recibo-pre-selo`; manifesto da Bancada que registra outro kernel; o manifesto B3 grava o pino; o 2bis cruza por ele; a contraprova (1b) aceita |
| **R31-4** | o build log exige a linha de job do lake de cada pedra, da raiz e do Audit, e `Build completed successfully` (`LOG_DE_BUILD_IMPLAUSIVEL`). O log do Audit conta **nomes distintos**, e todo nome do Audit.lean pinado tem de aparecer | build log de 1 caractere: **recusa** (unitário e caminho inteiro). Audit.lean de 5 `#print axioms` com uma linha repetida 3×: **recusa `LOG_DO_AUDIT_CURTO`** (na R3.1: aceitos) | só a linha final; sem a linha final; sem o job de uma pedra; 2 nomes distintos com um estranho ao Audit; a mesma declaração 2×; a contraprova do auditor segue recusada; o **formato real** da custódia v390 (só lida) passa nas regras: 956 jobs, os 3 mudados como `Built`, 8.523 nomes distintos no Audit.lean e no log, 0 sorry |
| **R31-5** | o sorry é procurado em três formas (normalizado, branco colapsado e escapes JSON decodificados), e a contagem é a maior; `sorryAx` e os axiomas também nas três | aviso partido entre `declaration` e `uses`: **recusa**; JSON com a crase `\u0060`: **recusa** (unitário e caminho inteiro) (na R3.1: aceitos) | várias quebras CRLF com recuo; JSON com barra-n e `\u0027`; `sorryAx` com uma letra escapada no log do Audit; a contraprova (as palavras soltas, sem o aviso) aceita; no log **real** do Nós, as três formas contam o mesmo (4, 4, 4) |
| **R31-6** | `json_estrito` (`object_pairs_hook`): chave duplicada recusa no `CRITERIOS` (`CRITERIOS_CHAVE_DUPLICADA`) e no recibo do kernel. A `x19` é cruzada com as pedras: `"sim"` se e somente se existe `LightNetStandardWedgeDataBGL.lean` (`X19_NAO_CONFERE_COM_AS_PEDRAS`) | `j1_declaracoes` 159 e depois 2: **recusa**. `x19 = «sim»` sem a pedra: **recusa** (na R3.1: aceitos) | `x19` duplicada no topo; caminho inteiro com a chave duplicada (rc 2); `rc` duplicado no recibo do kernel; `x19 = «nao»` com a pedra; `x19 = «sim»` pelo caminho inteiro (T17 FALHA, rc 3); a **contraprova** `x19 = «sim»` com a pedra coerente em tudo (árvore, manifesto re-pinado, logs, pedras == diff formal) aceita |
| **§12-ter item 3** | campo `varredura_tokens {recursiva, arquivos_lean, arquivos_lean_em_TGLExt_O16}`; o B(n) reconta os `.lean` recursivamente, sem seguir junção (`TOKENS_VARREDURA_NAO_RECURSIVA`, `ARVORE_COM_JUNCAO_OU_LINK`) | a contagem **não recursiva** declarada (4, sem `TGLExt/O16`): **recusa** (unitário e caminho inteiro) | `recursiva = false`; campo ausente; contagem em texto; junção dentro da árvore (recusada e nunca seguida; desfeita no fecho); o **formato real** v390: 1.212 `.lean` recursivos, 156 em `TGLExt/O16`, 1.026 em `TGLExt/*.lean` |

Os documentos:
- **`CONTRATO_KERNEL_RECIBO_R3_2.md`** (`b8e803193690108a`): o contrato `KERNEL_RECIBO_R3_2`, com o §8 que leva o item 3 da §12-ter ao critério `tokens_proibidos`;
- **`REMISSOES_PLANO_R3_2.md`** (`738416feb005c12d`): cita o plano vigente, `ca30438e2481df33`, 555 linhas, com a §12-ter na l.546. Troca `-s` por `-I` nos comandos. Traz a errata ao lado da R3.1-5 (R31-3) e do sha do plano (R31-7) e o `core.autocrlf` (R31-8).

**O diff.**
- `DIFF_R3_1_R3_2.patch` (`de368c29f565175b`, 4 `.py`) reproduz a R3.2 bit a bit por `git -c core.autocrlf=false apply` [REAL, `VERIFICACAO_DIFF_R3_2.json`, `9c0f2e4068edcfbe`, que agora diz `requer_core_autocrlf_false`].
- Pinos do esboço: `a408d49292f55008`, `montar_sandbox.py` `c85e93469caf23e0`, `controles_negativos_r3_2.py` `1643c7c62999c4e9`, `medir_pinos_r3_2.py` `71fb4e6193cd0837`.
- Tudo o que esta R3.2 cita está em `PINOS_R3_2.json`, medido por script, com as 54 fontes da bateria conferidas.

## 4. Garantias [REAL]

- **Produção e Nós.** A lista da produção e o seu manifesto (`54fc9e27e4599c49`) ficaram iguais antes e depois. A lista do Nós também.
- **Livro de eventos.** Só cresceu: nenhum elo novo de outra sessão nesta janela, e nenhum elo de sincronização nasceu.
- **O sandbox.** `C:\t\vb7` foi apagado. As 5 junções criadas foram desfeitas com `os.rmdir` no link, e nenhuma restou.
- **O que não fiz.** Não rodei o um.py nem o selo. Nada de HTTP nem MCP; nenhum serviço real foi parado ou religado; não fiz `init` nem `transition` no ACOM; não registrei no mapa; não toquei no quadro (o livro de eventos só foi lido) nem no túnel. Nenhum confidencial.
- **O que li fora do R3_2.** Do Nós, só leitura: a amostra de log do `bancada_corpus` e a cópia que o `montar_sandbox` faz do um.py, do selo, do core e do manifesto do kernel v391, como na R3.1. Da custódia v390, só leitura: os logs do build e do Audit, o Audit.lean e a árvore, para o formato real.
- **A palavra proibida.** Não aparece em nenhum arquivo da R3_2 (`grep` rc 1). Duas cópias do selo v391 que a traziam em textos de veredito do próprio selo foram tiradas das evidências: o selo v391 do sandbox fica pinado no recibo dos controles (`95061f18c7102248`), e o selo forjado era derivado dele.
- **As evidências.** As cópias dos módulos-sombra estão em `evidencias_sandbox\aud32_entradas\esboco_com_vizinhos\` com extensão `.txt`, inertes.

## 5. Resíduos declarados e o que NÃO foi feito

- **Chamada errada.** Sem `-I`, o interpretador ainda executa, antes da 1ª linha do esboço, um `usercustomize`/`.pth` do `APPDATA` herdado ou o site do sistema. O esboço então recusa sem gravar nada. É resíduo da chamada errada. Se código hostil rodar antes da guarda, pode falsear `sys.flags`: a defesa é a cadeia chamar com `-I` [DERIVED].
- **Gravação alheia.** O rollback da R31-2 sobrescreve a gravação alheia; os bytes dela ficam só em `--saida`. Depois da 2ª releitura, nada mais é visível ao esboço: o 10-ter segue sendo a última prova.
- **O selo anterior em produção.** A R31-3 depende de a cadeia guardar o selo e o manifesto do kernel v391 antes do selo da v392 (R3.2-0). Na custódia `the_boundary_BACKUPS`, as pastas `um_v39*` vão até a v390; não achei a v391 lá e não procurei além disso [OPEN].
- **Os tokens.** O B(n) confere a extensão da varredura de tokens, não os tokens. O build log forjado com as linhas certas e o sha pinado passa: a defesa é o pino da cadeia e o rito.
- **Não medido:**
  - o `Out-File` sem `-Width` [CONJECTURE];
  - o kernel real e o `construir_kernel_v392.sh` (não escritos);
  - aplicar na produção real;
  - link simbólico e corrida dentro de `caminho_canonico`;
  - a autenticação do evento (segue convenção);
  - a rota do sorry com aspas no um.py, l.192945, fora do escopo.
- Os ataques do script do auditor (`ataques_r3_1.py`) não foram reexecutados contra a R3.2. Os casos exatos foram refeitos nos controles `R32_*`.

## 6. Atos

**Gerência c1:**
- reauditoria curta da R3.2 por quem não construiu;
- aplicar as remissões (R3 + R3.1 + R3.2) ao lado no plano;
- escrever o `construir_kernel_v392.sh` no contrato `KERNEL_RECIBO_R3_2`, com a varredura recursiva, a captura sem quebra e sem `--json`, e o build que compila as pedras;
- copiar o selo e o manifesto do kernel v391 na etapa 1;
- preencher o `CRITERIOS_v392.json` depois da X19;
- derivar o esboço, a bateria e os critérios para `<V>` antes da etapa 1;
- registrar no mapa (`registro_mapa_F0.6_R3_2.json`, pronto e não registrado) e no ACOM.

**Operador:**
- a decisão X19, antes da etapa 2;
- autorizar a B3;
- o 10-bis-a, a parada com recibo;
- o 10-ter, o religamento com recibo de identidade, também depois de qualquer rollback, e a reconexão dos MCP;
- a implantação B3 de código;
- se a ordem de 12/10 vale da v393 em diante.
