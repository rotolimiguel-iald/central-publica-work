# Remissões R3.2, ao lado das remissões R3 e R3.1 do `PLANO_V392.md`

Texto pronto para a gerência aplicar **ao lado**. Nem o plano, nem o `R3\REMISSOES_PLANO_R3.md`, nem o `R3_1\REMISSOES_PLANO_R3_1.md` foram editados aqui. Este arquivo fica ao lado dos dois e corrige o que a reauditoria curta da R3.1 apontou.

**Origem.** Reauditoria curta da R3.1, `C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a721b706.md` (relatório completo em `art_a721b706\AUDITORIA_VINCULO_R3_1_C1.md`):
- R31-1 (MÉDIA): o comando;
- R31-2 a R31-6 (BAIXA): o código;
- R31-7 e R31-8 (BAIXA, documentais): o sha do plano, a §12-ter e o `core.autocrlf`.

**Decisão da gerência [INPUT]:** fechar todos os achados nesta rodada.

**O que se lê.** O plano vigente é `C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md`, **sha16 `ca30438e2481df33`, 555 linhas** [REAL, sha256 por script; repetido em `R3_2\PINOS_R3_2.json`]. A §12-ter está na l.546; a §12-bis, na l.529; a §14, na l.444; a §11, na l.342; a §4, na l.135; a §3, na l.120.

**Estatutos:**
- [DERIVED]: composto a partir do esboço R3.2, da reauditoria e do plano;
- [REAL]: onde cita um hash ou um resultado medido;
- [INPUT da gerência]: a decisão de fechar os achados nesta rodada; os esperados do `CRITERIOS_v392.json`;
- [DECLARADO]: os números do plano transcritos sem conferir no Lean.

Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## Errata ao lado do cabeçalho das remissões R3.1 (R31-7)

> ⚠ **R3.2, ao lado (13/10/2026). O cabeçalho da R3.1 fica como registro.**
>
> As `REMISSOES_PLANO_R3_1.md` citam o plano em `e3eecff0b602e070`, com 541 linhas. Esse é o estado de antes da §12-ter, o mesmo do `PLANO_V392.md.bak_20261013_073035`.
>
> O plano vigente está em **`ca30438e2481df33`, com 555 linhas**. A §12-ter (l.546–555) foi acrescentada no fim, às 07:30, e por isso as âncoras de linha da R3.1 (l.39, 97, 147, 160–169, 178, 180, 225, 245, 448) continuam certas [REAL, conferido pelo auditor e aqui por script].

---

## R3.2-0: ao lado do R3.1-0 (os comandos)

> ⚠ **R3.2, ao lado (13/10/2026). O R3.1-0 fica como registro; valem estes comandos.**
>
> **O esboço é o R3.2:** `work\bancada_vinculo_12out\R3_2\sincronizar_bancada.py`, com o sha256 em `R3_2\PINOS_R3_2.json`.
>
> **O interpretador do esboço roda com `python -I -B -X utf8`** (R31-1). O R3.1-0 mandava `-s`, e isso deixava a pasta do esboço em `sys.path[0]`: um `json.py` posto ao lado dele executava dentro do processo que grava a produção.
>
> Na R3.2:
> - o esboço **confere** o próprio interpretador na primeira linha de código, antes de qualquer `import` além de `sys`;
> - sem `-I` (que liga `-E`, `-P` e `-s`), sem `-B` ou sem `-X utf8`, ele recusa com `INTERPRETADOR_NAO_ISOLADO` (rc 2) e nada é gravado;
> - um `json.py` ou `argparse.py` ao lado do esboço nunca chega a ser importado: nem com `-I`, nem na chamada errada, porque a recusa vem antes [REAL, controles `R32_R31_1_*`].
>
> ### Etapa 1 (pré-selo, ensaio)
>
> ```
> python -I -B -X utf8 "<V>\sincronizar_bancada.py" ^
>   --bancada C:\IALD\Bancada_Um --producao ^
>   --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
>   --versao v391 --fase pre_selo --modo ensaio ^
>   --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <sha da bateria> ^
>   --saida "C:\IALD\Central de Patentes\work\v392_bateria\pre_selo"
> ```
>
> **Na mesma etapa 1, antes do selo** (R31-3, novo), a cadeia copia, byte a byte e conferindo o sha por script, o selo e o manifesto do kernel da v391 para `work\v392_bateria\anterior_v391\`. Copia `Nós\um_absoluto_selo.json` e `Nós\tgl_kernel_proof_manifest.json`, ou as cópias da custódia v391, se existirem.
>
> Depois do selo, o Nós já tem os da v392. O B(3) confere essas cópias contra fontes externas a elas:
> - o selo, contra o selo pinado no manifesto vigente da Bancada;
> - o manifesto do kernel, contra o pino desse selo.
>
> Por isso a cópia não precisa de pino próprio em `v392_pins`. Pinar não faz mal.
>
> ### Elo B(3) (pós-selo, aplicar; passo 10-bis da cadeia)
>
> ```
> python -I -B -X utf8 "<V>\sincronizar_bancada.py" ^
>   --bancada C:\IALD\Bancada_Um --producao ^
>   --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
>   --versao v392 --fase pos_selo --modo aplicar ^
>   --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <v392_pins> ^
>   --evento <seq> --evento-hash <hash16 do elo, do retorno de iald.py anotar> ^
>   --recibo-pre-selo <RECIBO_SINCRONIZACAO_v391_*.json da etapa 1> --recibo-pre-selo-sha256 <v392_pins> ^
>   --selo-anterior "C:\IALD\Central de Patentes\work\v392_bateria\anterior_v391\um_absoluto_selo.json" ^
>   --kernel-manifesto-anterior "C:\IALD\Central de Patentes\work\v392_bateria\anterior_v391\tgl_kernel_proof_manifest.json" ^
>   --kernel-recibo "C:\IALD\Central de Patentes\work\v392_kernel\KERNEL_RECIBO_v392.json" --kernel-recibo-sha256 <v392_pins> ^
>   --criterios "<V>\CRITERIOS_v392.json" --criterios-sha256 <v392_pins> ^
>   --saida "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\bancada_B3"
> ```
>
> ### `<V>` (ressalva do auditor, opcional)
>
> Com `-I`, a pasta `<V>` não entra no `sys.path`, e um arquivo a mais nela não executa. A derivação pode, além disso, conferir por script que `<V>` só contém os três arquivos pinados: o esboço, a bateria e o `CRITERIOS`. Isso é defesa em profundidade, não condição [DERIVED].
>
> ### As flags novas da R3.2
>
> | flag | quando é obrigatória | recusa se faltar ou não bater |
> |---|---|---|
> | `--selo-anterior` (R31-3) | sempre que houver `--recibo-pre-selo` | `SELO_ANTERIOR_AUSENTE`; `SELO_ANTERIOR_NAO_E_O_PINADO` (sha ≠ o selo pinado no manifesto da Bancada, ou `um_version` ≠ a versão anterior); `SELO_ANTERIOR_SEM_PINO_DO_KERNEL` |
> | `--kernel-manifesto-anterior` (R31-3) | sempre que houver `--recibo-pre-selo` | `SELO_ANTERIOR_AUSENTE`; `KERNEL_MANIFESTO_ANTERIOR_NAO_E_O_DO_SELO` |
> | (as duas sem `--recibo-pre-selo`) | — | `SELO_ANTERIOR_SEM_RECIBO_PRE_SELO` |
>
> Também recusa:
> - o `CRITERIOS` com chave duplicada (`CRITERIOS_CHAVE_DUPLICADA`, R31-6);
> - um recibo do kernel no contrato da R3.1, porque o contrato agora é `KERNEL_RECIBO_R3_2` (ver `R3_2\CONTRATO_KERNEL_RECIBO_R3_2.md`).

---

## R3.2-1: ao lado da R3.1-1 (o isolamento dos testes)

> ⚠ **R3.2, ao lado (13/10/2026).** O isolamento dos testes não muda: `-E -P -s` pelo lançador pinado, `APPDATA` vazio por teste, o site do usuário só como caminho.
>
> Muda o **resíduo do próprio esboço**. Na R3.1, sem `-s`, o processo do esboço executava os `.pth` e o `usercustomize` do `APPDATA` herdado. Na R3.2, o esboço só roda sob `-I`, que não processa o site do usuário.
>
> Numa chamada **errada** (sem `-I`), o interpretador ainda executa esse código **antes** da primeira linha do esboço. O esboço então recusa sem gravar nada. Isso é resíduo da chamada errada, e não do B(n) [REAL, controles `R31_A4_*` e `R32_A4_appdata_de_ataque_esboco_com_I`].
>
> O run 1a da R3.2 passou a bateria inteira da R2 com o esboço em `-I`, numpy, scipy e torch inclusive (ver `RESULTADO_R3_2.md`).

---

## R3.2-2: ao lado da R3.1-2 (§4, etapa 2): o contrato do kernel e a §12-ter item 3

> ⚠ **R3.2, ao lado (13/10/2026).** O contrato do recibo agora é o `KERNEL_RECIBO_R3_2` (`R3_2\CONTRATO_KERNEL_RECIBO_R3_2.md`). Mudam estes pontos:
>
> - **R31-4.** O build log tem de trazer a linha de job do lake (`Built`/`Replayed`) de cada pedra, da raiz e do Audit, e a linha `Build completed successfully` (`LOG_DE_BUILD_IMPLAUSIVEL`). O log do Audit cobre os `#print axioms` do Audit.lean pinado por **nome distinto**: linha repetida não conta duas vezes, e todo nome impresso pelo Audit.lean aparece no log.
>   - Medido na custódia v390 [REAL]: os três arquivos formais mudados saem como `Built`; os 8.523 nomes distintos do Audit.lean real estão todos no log real.
> - **R31-5.** O sorry é procurado também com o branco colapsado (uma quebra entre `declaration` e `uses` não esconde) e com os escapes JSON decodificados (a crase como `\u0060`). `sorryAx` é procurado nas três formas.
> - **R31-6.** A `x19` do `CRITERIOS` pinado é cruzada com as pedras do recibo. Com `"sim"`, a pedra `LightNetStandardWedgeDataBGL.lean` tem de estar lá; com `"nao"`, não pode estar (`X19_NAO_CONFERE_COM_AS_PEDRAS`).
> - **§12-ter item 3 → critério `tokens_proibidos` e contrato §8.** O `construir_kernel_v392.sh` varre os tokens proibidos de forma **recursiva**, inclusive os `.lean` de `TGLExt/O16`.
>   - O `medido` de `tokens_proibidos` é o dessa varredura.
>   - O recibo traz `varredura_tokens = {recursiva: true, arquivos_lean, arquivos_lean_em_TGLExt_O16}`.
>   - O B(n) reconta os `.lean` da árvore recursivamente, sem seguir junção, e recusa se os números não batem (`TOKENS_VARREDURA_NAO_RECURSIVA`) ou se a árvore tem junção (`ARVORE_COM_JUNCAO_OU_LINK`).
>   - Sem isso, o «medido = 0» do critério podia ser o número não recursivo, o que deixa 150 arquivos de fora (§12-ter item 3) [DECLARADO pela §12-ter; que a recursão importa foi medido na custódia v390].
> - **A captura.** A captura do log é pelo bash (`> build_full.log 2>&1`) ou com `Out-File -Width 100000 -Encoding utf8`, nunca com o `Out-File` sem `-Width` (R31-5). O log não pode ser saída `--json` do Lean.
>
> **Errata ao lado do item (4) da R3.1-2.** Onde diz «o contrato do recibo agora é o `KERNEL_RECIBO_R3_1`», lê-se `KERNEL_RECIBO_R3_2`.

---

## R3.2-3: ao lado da R3.1-3 (§5, etapa 3, `v392_pins`)

> ⚠ **R3.2, ao lado (13/10/2026).** O `v392_pins` pina:
> - o esboço **R3.2**, não o R3.1;
> - o sha do `KERNEL_RECIBO_v392.json` no contrato `KERNEL_RECIBO_R3_2`.
>
> Pode pinar também as cópias `anterior_v391\` (ver R3.2-0), mas o B(3) não depende disso: ele cruza essas cópias com o manifesto da Bancada.

---

## R3.2-4: ao lado da R3.1-4 (§11, passos 10-bis e 10-ter)

> ⚠ **R3.2, ao lado (13/10/2026).**
>
> **10-bis: a conferência depois da troca (R31-2).** Na R3.1, depois do `os.replace` vinha a última sonda do serviço (até 1,5 s), e o recibo era gravado sem nova comparação de bytes. Uma mudança no manifesto durante essa sonda terminava em rc 0, APLICADA, com o disco diferente do que o recibo declarava.
>
> Na R3.2 a ordem é: **`os.replace` → reconferência pelo `canonical.py` → sonda → releitura do manifesto (tem de ser o novo, byte a byte) → recibo em `estado\sincronizacao` → releitura de novo**.
>
> Se uma das duas releituras diverge:
> - os bytes estranhos ficam em `--saida` (`MANIFESTO_ESTRANHO_APOS_A_TROCA_B<n>_<stamp>.json`), com o sha no recibo;
> - o recibo em `estado\` sai, se já tinha sido gravado;
> - o rollback devolve o manifesto anterior, e o serviço é sondado depois do rollback.
>
> A recusa é `APLICACAO_REVERTIDA: MANIFESTO_MUDOU_APOS_A_TROCA…` ou `…MANIFESTO_MUDOU_APOS_O_RECIBO_EM_ESTADO…`. Se o serviço responde depois do rollback, a recusa é `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`, com a causa no texto.
>
> **Resíduo declarado:** o rollback sobrescreve a gravação alheia, que só fica preservada na evidência em `--saida`. Depois da segunda releitura, nada mais é visível ao esboço; o 10-ter, o recibo de identidade do religamento, segue sendo a última prova.
>
> **Como antes:** depois de QUALQUER rollback, o religamento com recibo de identidade é obrigatório antes de outro B(n).

---

## R3.2-5: errata ao lado da R3.1-5 (N2c, o recibo pré-selo) (R31-3)

> ⚠ **R3.2, ERRATA ao lado (13/10/2026). A R3.1-5 fica como registro; ela EXAGERAVA.**
>
> **O que a R3.1-5 dizia.** Que o `nos.kernel.sha256` do recibo pré-selo tinha de ser igual ao manifesto do kernel que o selo pina, e que «um pino forjado em `v392_pins` deixa de bastar».
>
> **O que o código da R3.1 fazia.** Só o `nos.selo.sha256` era cruzado com uma fonte externa, o selo pinado no manifesto da Bancada. O `nos.kernel.sha256` era comparado com o `nos.selo.tgl_kernel_proof_manifest_sha256` **do próprio recibo**.
>
> Uma forja consistente desses dois campos, e da raiz, do Audit e da impressão, passava. O auditor mediu isso [REAL, `ATAQUES_R3_1_AUDITOR.json`, `N2c_novo_selo_certo_mas_o_pino_do_kernel_vem_do_proprio_recibo`].
>
> **Leitura vigente (R3.2).** O pino do manifesto do kernel é o que o **selo anterior** grava, lido de fonte externa ao recibo:
> - `--selo-anterior` tem o sha do selo pinado no manifesto vigente da Bancada (`canonical.seal.sha256`) e a `um_version` da versão anterior;
> - `--kernel-manifesto-anterior` tem o sha do pino desse selo;
> - a raiz, o Audit e a impressão formal são **recalculados** desse manifesto, e o recibo tem de bater com os cinco valores;
> - a partir do B4, o manifesto vigente da Bancada, gravado por um B(n) R3.2, registra também o manifesto do kernel (`sincronizacao.kernel_manifesto_sha256`; na re-execução, `sincronizacao.anterior.kernel_manifesto_sha256`), e esse registro também confere.
>
> **Controles.** O caso exato do auditor (unitário e no decoy de produção) e as variantes recusam: pino verdadeiro com raiz e impressão forjadas, selo anterior forjado, manifesto do kernel de outro rito, ausência e registro divergente no manifesto da Bancada. A contraprova, o recibo verdadeiro, passa [REAL, controles `R32_R31_3_*`].

---

## R3.2-6: ao lado da R3.1-6 (§14, o texto ao operador)

> ⚠ **R3.2, ao lado (13/10/2026).** No texto ao operador, o comando do B(3) é o do R3.2-0: o esboço chamado com **`-I -B -X utf8`**, com `--criterios` e `--criterios-sha256`, e com `--selo-anterior` e `--kernel-manifesto-anterior`.
>
> Fica dito também:
> - **a X19 é decisão dele antes da etapa 2.** O `CRITERIOS_v392.json` depende dela, e agora o B(3) a cruza com as pedras do recibo;
> - **depois de um rollback**, por qualquer causa (a R31-2 inclusive), o religamento com recibo de identidade é obrigatório antes de outro B(n).
>
> Os atos do operador são os mesmos da R3 e da R3.1:
> - a B3;
> - o 10-bis-a, a parada com recibo;
> - o 10-ter, o religamento com recibo de identidade e a reconexão dos MCP;
> - a implantação B3 de código;
> - se a ordem de 12/10 vale da v393 em diante.

---

## R3.2-7: o diff e o `core.autocrlf` (R31-8)

> ⚠ **R3.2, ao lado (13/10/2026).** O `R3_2\DIFF_R3_1_R3_2.patch` reproduz os `.py` da R3.2 bit a bit a partir dos da R3.1 **só com `git -c core.autocrlf=false apply`**. O git desta máquina tem `autocrlf=true`, e com ele os arquivos sairiam com CRLF.
>
> O `R3_2\VERIFICACAO_DIFF_R3_2.json` diz isso em `requer_core_autocrlf_false` e no comando de verificação. Vale também, ao lado, para o `VERIFICACAO_DIFF_R3_1.json`.

---

Nada aqui é leitura física. NOT_FALSIFIED nunca é creditação.
