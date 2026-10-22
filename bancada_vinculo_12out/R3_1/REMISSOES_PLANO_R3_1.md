# Remissões R3.1, ao lado das remissões R3 do `PLANO_V392.md`

Texto pronto para a gerência aplicar **ao lado**. Nem o plano nem o `R3\REMISSOES_PLANO_R3.md` foram editados aqui: este arquivo fica ao lado do da R3 e corrige o que a reauditoria curta apontou.

**Origem.** Reauditoria curta da R3, `C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a61fad96.md`:
- §4: três ressalvas documentais BAIXA na Remissão 2;
- §3: os consertos A1–A3, N1k/l/m, N2c, N3a, N4b e A4, que mudam o comando e os pinos.

**O que se lê.** O plano é o mesmo da R3: `C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md`, sha16 `e3eecff0b602e070`, 541 linhas. As remissões R3 citadas são as de `R3\REMISSOES_PLANO_R3.md`, sha16 `1806fdb58a589886` [REAL, sha256 por script].

**Estatutos:**
- [DERIVED]: composto a partir do esboço R3.1, da reauditoria e do plano;
- [REAL]: onde cita um hash ou um resultado medido;
- [INPUT da gerência]: os esperados do `CRITERIOS_v392.json` e a hora em que a gerência os escreve;
- [DECLARADO]: os números do plano que este texto transcreve sem conferir no Lean.

Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## R3.1-0: ao lado do §0 da R3 (os comandos)

> ⚠ **R3.1, ao lado (13/10/2026). O §0 da R3 fica como registro; valem estes comandos.**
>
> **O esboço é o R3.1:** `work\bancada_vinculo_12out\R3_1\sincronizar_bancada.py` (sha256 em `R3_1\PINOS_R3_1.json`).
>
> **O interpretador do esboço roda com `-s`** (A4). Sem `-s`, o próprio processo do esboço executa os `.pth` e o `usercustomize` do site do usuário dele. Isso é resíduo declarado: os processos de teste não os executam mais, com ou sem `-s` no esboço [REAL, controles `R31_A4_*`].
>
> ### Etapa 1 (pré-selo, ensaio)
>
> ```
> python -s -B -X utf8 "<V>\sincronizar_bancada.py" ^
>   --bancada C:\IALD\Bancada_Um --producao ^
>   --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
>   --versao v391 --fase pre_selo --modo ensaio ^
>   --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <sha da bateria> ^
>   --saida "C:\IALD\Central de Patentes\work\v392_bateria\pre_selo"
> ```
>
> ### Elo B(3) (pós-selo, aplicar; passo 10-bis da cadeia)
>
> ```
> python -s -B -X utf8 "<V>\sincronizar_bancada.py" ^
>   --bancada C:\IALD\Bancada_Um --producao ^
>   --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
>   --versao v392 --fase pos_selo --modo aplicar ^
>   --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <v392_pins> ^
>   --evento <seq> --evento-hash <hash16 do elo, do retorno de iald.py anotar> ^
>   --recibo-pre-selo <RECIBO_SINCRONIZACAO_v391_*.json da etapa 1> --recibo-pre-selo-sha256 <v392_pins> ^
>   --kernel-recibo "C:\IALD\Central de Patentes\work\v392_kernel\KERNEL_RECIBO_v392.json" --kernel-recibo-sha256 <v392_pins> ^
>   --criterios "<V>\CRITERIOS_v392.json" --criterios-sha256 <v392_pins> ^
>   --saida "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\bancada_B3"
> ```
>
> ### `<V>`: quando a cópia acontece (ressalva documental 3 da reauditoria)
>
> `<V>` é `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\`, como na R3. A R3 dizia **onde**; falta dizer **quando**:
> - a derivação (`derivar_cadeia_v392.py`) copia para `<V>` o `sincronizar_bancada.py` R3.1 e a `BATERIA_VINCULO.json`, com o sha conferido contra `R3_1\PINOS_R3_1.json`, **antes da etapa 1**. A etapa 1 já roda o esboço a partir de `<V>`;
> - o `CRITERIOS_v392.json` entra em `<V>` **depois** da decisão X19 do operador e **antes da etapa 2**. A X19 muda a árvore do kernel (uma pedra a mais) e os números J1;
> - nenhum dos três muda depois de copiado. O `v392_pins` (etapa 3) pina os três por sha256, lido por script.
>
> ### As flags novas da R3.1
>
> | flag | quando é obrigatória | recusa se faltar ou não bater |
> |---|---|---|
> | `--criterios` (A3) | sempre que houver `--kernel-recibo` | `CRITERIOS_AUSENTES` |
> | `--criterios-sha256` (A3) | sempre que houver `--criterios` | `CRITERIOS_SHA_AUSENTE` / `CRITERIOS_SHA_DIVERGE` |
>
> Também recusam o arquivo de critérios: `CRITERIOS_NAO_PREENCHIDOS` (o modelo `R3_1\CRITERIOS_V392.json` como está), `CRITERIOS_SEM_DECISAO_X19`, `CRITERIOS_DE_OUTRA_VERSAO`, `CRITERIOS_CONTRATO_INVALIDO`, `CRITERIOS_CHAVES_DIVERGEM`, `CRITERIOS_ESPERADO_INVALIDO`, `CRITERIOS_SEM_ESPERADOS` e `CRITERIOS_ILEGIVEIS`. Todas dão rc 2, antes da bateria.

---

## R3.1-1: ao lado da Remissão 1 da R3 (§3, etapa 1), no item «Como rodam os testes»

> ⚠ **R3.1, ao lado (13/10/2026).** Cada teste roda com **`python -E -P -s`** por um **lançador pinado** (`_lancador_isolado_r3_1.py`, cujo sha256 vai no recibo):
> - o `APPDATA` do teste é uma **pasta vazia nova** sob `--saida`;
> - os netos recebem `PYTHONNOUSERSITE=1`;
> - o site do usuário entra **só como caminho**, sem `.pth` e sem `usercustomize`. O esboço o acha pela pasta conhecida do Windows (`SHGetKnownFolderPath`), não pelo `APPDATA` herdado; nos netos, ele vai no `PYTHONPATH`;
> - o recibo traz, com sha256, os `.pth`/customize do site do **sistema** que ainda executam (hoje: nenhum [REAL, 13/10]) e os `.pth` do site do usuário que deixaram de executar (hoje: 3, `distutils-precedence`, `protobuf-3.20.3-nspkg` e `pywin32` [REAL]).
>
> **Resíduo declarado (A4).** O código dos pacotes do site do usuário (numpy, scipy, torch) segue importável e **não pinado**. O run 1a da R3.1 passou a bateria inteira assim: 13 PASSA, 0 FALHA [REAL].

---

## R3.1-2: ao lado da Remissão 2 da R3 (§4, etapa 2). As três ressalvas documentais da reauditoria

> ⚠ **R3.1, ao lado (13/10/2026). Errata ao lado da Remissão 2 da R3, que fica como registro.**
>
> **(1) O B(n) não confere os critérios contra o Lean** (ressalva 1). A Remissão 2 da R3 dava os critérios «J1 159/130/0, 8.523 entradas antigas idênticas, tokens 0, R1 ausente, declarações novas no trio» como parte do recibo e, por isso, como conferidos. Na R3 eles eram **autodeclarados**: o recibo trazia o esperado e o medido, e um recibo com esperado = medido = 7 passava (achado A3).
>
> Na R3.1:
> - o recibo traz **só o medido** de cada critério;
> - o **esperado** vem do `CRITERIOS_v392.json`, escrito pela gerência e pinado pela cadeia (`--criterios-sha256`);
> - esperado dentro do recibo é **recusado** (`CRITERIO_AUTODECLARADO`).
>
> Mesmo assim, o B(n) **não reconta** J1 nem as 8.523 entradas no Lean. Ele confere que o medido declarado pela etapa 2 é igual ao esperado pinado pela gerência. A contagem é responsabilidade do `construir_kernel_v392.sh` e do rito.
>
> **(2) Os números estão condicionados à X19** (ressalva 2). Os valores 159 / 130 / 0 / 8.523 são os do plano **sem** a X19 [DECLARADO, `PLANO_V392.md` §4 item 6]. O próprio plano diz que a X19 muda os números: +1 pedra (K09) e +87 bandeiras, com a escada indo de 6285 para 6372 (l.39, l.147, l.178, l.180). Por isso:
> - o `CRITERIOS_v392.json` traz `x19 ∈ {"sim", "nao"}`. Sem a decisão, a recusa é `CRITERIOS_SEM_DECISAO_X19`;
> - com x19 = «sim», a gerência deriva os números novos [OPEN no plano].
>
> **(3) A cópia do esboço para `<V>` acontece antes da etapa 1** (ressalva 3). Ver R3.1-0.
>
> **(4) O contrato do recibo agora é o `KERNEL_RECIBO_R3_1`** (`R3_1\CONTRATO_KERNEL_RECIBO_R3_1.md`). Mudam estes campos:
> - `toolchain` em lista;
> - `pedras[].declaracoes`;
> - `formal_files_antes`;
> - `criterios` só com `{medido}`.
>
> O sorry é contado no formato **real** do Lean 4.31 (crases), sobre o log normalizado. O build log vazio e o log do Audit curto são recusados.
>
> **(5) Sobre «35 recibos inválidos recusados»** (ressalva 4). O número era da R3 e o auditor não o conferiu. Na R3.1, a contagem é por script, em `R3_1\CONTROLES_NEGATIVOS_R3_1.json`. O número exato está em `R3_1\RESULTADO_R3_1.md`.

---

## R3.1-3: ao lado da Remissão 3 da R3 (§5, etapa 3, `v392_pins`)

> ⚠ **R3.1, ao lado (13/10/2026).** O `v392_pins` pina também o sha256 do `CRITERIOS_v392.json` de `<V>`. A cadeia o passa em `--criterios-sha256` no passo 10-bis. O esboço pinado é o R3.1, não o R3.

---

## R3.1-4: ao lado da Remissão 4 da R3 (§11), no passo 10-bis e no 10-ter

> ⚠ **R3.1, ao lado (13/10/2026).**
>
> **10-bis: a ordem da última gravação (N4b).** Na R3, a ordem era comparar os bytes, sondar o serviço (até 1,5 s com a porta fechada) e trocar. Uma mudança feita durante a sonda era sobrescrita e não ficava no `.bak`.
>
> Na R3.1 a ordem é: **sondar → comparar os bytes do manifesto com os lidos no passo 3 → `os.replace`**. Entre a comparação e a troca não há sonda nem espera.
>
> **10-bis: o rollback com o serviço no ar (N3a).** O esboço não trava o arquivo nem a porta. Um `um_bancada.py` que suba no instante do `os.replace` lê o manifesto **novo** e o guarda em RAM; depois o rollback devolve o **anterior** ao disco.
>
> Por isso:
> - depois de qualquer rollback, o B(n) sonda o serviço de novo. Se ele responde, a recusa tem código próprio: `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`. O recibo traz os dois sha (`manifesto_novo_sha256`, `manifesto_em_disco_sha256`) e a nota;
> - **depois de QUALQUER rollback** (`APLICACAO_REVERTIDA…`), o serviço tem de ser reiniciado com recibo de identidade (o molde do 10-ter) antes de outro B(n). O recibo do aplicar traz essa nota em `servico_e_manifesto_em_ram`.
>
> **10-ter.** Depois da última sonda, nada é visível ao esboço. O recibo de identidade do religamento continua sendo a única prova de qual manifesto o serviço carregou.

---

## R3.1-5: ao lado da Remissão 1 da R3, no parágrafo «O recibo» (N2c)

> ⚠ **R3.1, ao lado (13/10/2026).** No B(3), o recibo pré-selo passa a ser cruzado também com o **selo pinado no manifesto anterior da Bancada**:
> - o `nos.selo.sha256` do recibo tem de ser igual ao `canonical.seal.sha256` do manifesto B2 vigente;
> - o `nos.kernel.sha256` do recibo tem de ser igual ao `tgl_kernel_proof_manifest.json` que esse selo pina.
>
> Um pino forjado em `v392_pins` deixa de bastar para trocar o ANTES do T17.
>
> Na re-execução idempotente, a referência é o `sincronizacao.anterior.seal_sha_pinado`, que o manifesto B3 da R3.1 grava. Um manifesto sem esse campo não serve de referência (`RECIBO_PRE_SELO_SEM_REFERENCIA`).

---

## R3.1-6: ao lado da Remissão 7 da R3 (§14)

> ⚠ **R3.1, ao lado (13/10/2026).** No texto ao operador, o comando do B(3) é o do R3.1-0, com `--criterios`/`--criterios-sha256` e com o esboço chamado com `-s`.
>
> Fica dito também, por inteiro:
> - **a X19 é decisão dele antes da etapa 2**, porque o `CRITERIOS_v392.json` depende dela;
> - **depois de um rollback**, o religamento com recibo de identidade é obrigatório antes de outro B(n).
>
> Os atos do operador são os mesmos da R3:
> - a B3;
> - o 10-bis-a, a parada com recibo;
> - o 10-ter, o religamento com recibo de identidade e a reconexão MCP;
> - a implantação B3 de código;
> - se a ordem de 12/10 vale da v393 em diante.

---

Nada aqui é leitura física. NOT_FALSIFIED nunca é creditação.
