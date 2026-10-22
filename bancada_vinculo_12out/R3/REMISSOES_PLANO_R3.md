# Remissões que faltam no `PLANO_V392.md`, versão R3

Texto pronto para a gerência aplicar **ao lado**. O plano **não** foi editado aqui.

**Origem.** Achado N7 da re-auditoria da R2, `C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a645d974.md`, §6:
- faltam remissões na §4, na §5, na §11 e na §12, item 1;
- o item 4 do 12-bis ainda traz a regra R1 do evento;
- os comandos omitem `--bancada`, `--bateria` e `--saida`;
- não está dito que a bateria R2 substitui a H12.

**O que este texto substitui.** Ele toma o lugar de `R2\REMISSOES_PLANO.md`. As duas remissões da R2 (§3 e §14) foram reescritas aqui com os comandos completos e com as flags da R3.

**Quem edita o plano.** A gerência c1:
- antes, backup de bytes;
- depois, acréscimo datado **ao lado**, nunca por cima.

**O plano lido** [REAL, sha256 por script]: `C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md`, sha16 `e3eecff0b602e070`, 541 linhas. Os números de linha abaixo valem para esse arquivo.

**Estatutos:**
- [DERIVED]: composto a partir do esboço R3, da re-auditoria e do plano;
- [REAL]: onde cita um hash ou um resultado medido;
- [INPUT da gerência]: as decisões N6, N8 e N15 tomadas na R3.

Nada aqui move o gate. NOT_FALSIFIED não é creditação.

---

## 0. O comando completo, uma vez (todas as remissões citam este)

### Etapa 1 (pré-selo, ensaio)

```
python -B -X utf8 "<V>\sincronizar_bancada.py" ^
  --bancada C:\IALD\Bancada_Um --producao ^
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
  --versao v391 --fase pre_selo --modo ensaio ^
  --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <sha da bateria> ^
  --saida "C:\IALD\Central de Patentes\work\v392_bateria\pre_selo"
```

### Elo B(3) (pós-selo, aplicar; passo 10-bis da cadeia)

```
python -B -X utf8 "<V>\sincronizar_bancada.py" ^
  --bancada C:\IALD\Bancada_Um --producao ^
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" ^
  --versao v392 --fase pos_selo --modo aplicar ^
  --bateria "<V>\BATERIA_VINCULO.json" --bateria-sha256 <v392_pins> ^
  --evento <seq> --evento-hash <hash16 do elo, do retorno de iald.py anotar> ^
  --recibo-pre-selo <RECIBO_SINCRONIZACAO_v391_*.json da etapa 1> --recibo-pre-selo-sha256 <v392_pins> ^
  --kernel-recibo "C:\IALD\Central de Patentes\work\v392_kernel\KERNEL_RECIBO_v392.json" --kernel-recibo-sha256 <v392_pins> ^
  --saida "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\bancada_B3"
```

### `<V>`: onde o esboço e a bateria ficam pinados

`<V>` é `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\`. É lá que a derivação (`derivar_cadeia_v392.py`) copia o `sincronizar_bancada.py` R3 e a bateria, com o sha conferido. A subpasta própria tem um motivo [REAL, regra N8 da R3]: o `--saida` não pode cair na pasta do esboço nem na pasta da bateria. Por isso o esboço fica em `...\v392\vinculo\` e a saída em `...\v392\bancada_B3\`.

### As raízes de `--saida` admitidas (N8) [INPUT da gerência]

- `work\bancada_vinculo_12out`;
- `work\cadeia_de_selo\<alvo>`;
- `work\<alvo>_bateria`;
- o sandbox `C:\t\vb*`.

O `<alvo>` é a própria `--versao` na fase `pos_selo` e a **seguinte** na `pre_selo`. Exemplo: a etapa 1 roda com `--versao v391` e grava em `work\v392_bateria\`.

### As flags novas da R3, obrigatórias

| flag | quando é obrigatória | recusa se faltar ou não bater |
|---|---|---|
| `--evento-hash` (N6) | em todo evento numérico | `EVENTO_HASH_AUSENTE` / `EVENTO_HASH_DIVERGE` |
| `--recibo-pre-selo-sha256` (N2) | em `--producao` e em aplicar fora do sandbox | `RECIBO_PRE_SELO_SHA_AUSENTE` / `RECIBO_PRE_SELO_SHA_DIVERGE` |
| `--kernel-recibo-sha256` (N1) | em aplicar com `--kernel-recibo` | `KERNEL_RECIBO_SHA_AUSENTE` / `KERNEL_RECIBO_SHA_DIVERGE` |

Sem `--kernel-recibo`, o aplicar `pos_selo` fora do sandbox recusa com `KERNEL_RECIBO_AUSENTE`.

### Ambiente

O esboço recusa rodar com `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP` ou `PYTHONUSERBASE` no ambiente, salvo se chamado com `-E` (`AMBIENTE_PYTHON_INJETAVEL`, N5).

---

## Remissão 1: §3 (etapa 1). Substitui a Remissão 1 da R2

**Onde entra:** depois do item 5 da §3 (l.130) e antes de «Não há ato do operador nesta etapa» (l.132), como bloco «⚠ R3, ao lado».

> ⚠ **R3, ao lado (13/10/2026). Remissão ao §12-bis e errata ao lado do item 2.**
>
> **O que mudou.** Os «testes finais da Bancada» desta etapa passam a rodar pelo **`sincronizar_bancada.py` R3** (comando da etapa 1 em `work\bancada_vinculo_12out\R3\REMISSOES_PLANO_R3.md`, §0):
> - `--modo ensaio --fase pre_selo --versao v391`;
> - `--bancada C:\IALD\Bancada_Um --producao`;
> - `--bateria` com `--bateria-sha256`;
> - `--saida work\v392_bateria\pre_selo`, a raiz curta do T16, admitida pela regra N8.
>
> **A bateria vigente.** É a `BATERIA_VINCULO.json` da R2 (`work\bancada_vinculo_12out\R2\`, sha16 `61368649456cdd9f`), **inalterada na R3**. Ela **substitui** a `BATERIA_FINAL_PROPOSTA_H12.json` (`01814f73b9ffeb83`) citada no item 2: as mesmas fontes T01–T16, pinadas por sha e por teste, mais o T17 lido do recibo do kernel. Na cadeia, ela é copiada com o esboço para `cadeia_de_selo\v392\vinculo\` (derivação).
>
> **Como rodam os testes.** Cada teste roda isolado [REAL, run 1a da R3]:
> - `python -E -P`;
> - ambiente sem `PYTHON*`;
> - cwd numa pasta vazia nova;
> - recusa de módulo-sombra ao lado de fonte pinada.
>
> **O recibo.** A etapa deixa o `RECIBO_SINCRONIZACAO_v391_<stamp>.json` («JA_SINCRONIZADA__ENSAIO…»). Ele traz o **kernel v391** lido do manifesto do kernel pinado pelo selo: sha da raiz, sha do Audit e impressão formal. O B(3) do §12-bis exige esse recibo:
> - por **pino**: `--recibo-pre-selo-sha256`, lido de `v392_pins` (§5);
> - por **identidade**: versão anterior, um.py antes pinado, mesma Bancada.
>
> O ANTES do recibo do kernel da etapa 2 é cruzado com ele.
>
> **O T17 não corre aqui.** Entra no B(3) pelo `KERNEL_RECIBO_v392.json` da etapa 2, no contrato `KERNEL_RECIBO_R3` (`R3\CONTRATO_KERNEL_RECIBO.md`). Não vale mais o contrato de 4 campos da Remissão 1 da R2.
>
> **O que não muda:**
> - nenhum ato do operador nesta etapa;
> - nenhum dado observado;
> - o gate.

---

## Remissão 2: §4 (etapa 2), ao lado do item 5 (l.159) e do item 6 (l.160–169)

> ⚠ **R3, ao lado (13/10/2026). O recibo do kernel.**
>
> **O que o `construir_kernel_v392.sh` escreve.** Além do `build_full.log`:
> - o log do Audit, em arquivo próprio;
> - o **`work\v392_kernel\KERNEL_RECIBO_v392.json`** no contrato `KERNEL_RECIBO_R3` (`work\bancada_vinculo_12out\R3\CONTRATO_KERNEL_RECIBO.md`).
>
> **Os campos do recibo:**
> - `contrato` e `versao`;
> - `rc`, `sorry` e `erros` como **int**, com `sorry` e `erros` **contados por script nos logs**;
> - os dois logs com sha;
> - a toolchain;
> - a `arvore` do build;
> - a raiz e o Audit com sha ANTES e DEPOIS;
> - cada pedra com sha;
> - os axiomas, ⊆ {propext, Classical.choice, Quot.sound};
> - os critérios do item 6 **medidos**, cada um `{esperado, medido}`: J1 159/130/0, 8.523 entradas antigas idênticas, tokens 0, R1 ausente, declarações novas no trio;
> - a impressão formal do kernel do Nós, antes e depois.
>
> **O que o recibo NÃO traz:** `um_py_sha256`, o sha do selo nem o do manifesto do kernel v392. A etapa 2 roda antes do candidato e do rito. Se algum desses campos aparecer, o T17 dá FALHA.
>
> **Os dois pinos.**
> - O sha do recibo é pinado em `v392_pins` (§5).
> - O B(3) cruza raiz, Audit e pedras com o `tgl_kernel_proof_manifest.json` **que o selo v392 pinar** (`formal_files_sha256`, `statuses`, `axiom_report`, toolchain). Assim o T17 vira vínculo entre a etapa 2 e o kernel que o rito selou [REAL: 35 recibos inválidos recusados nos controles da R3, entre eles o de 4 campos que a R2 aceitava].

---

## Remissão 3: §5 (etapa 3), ao lado da linha 7 da tabela (W02_pinos, l.183)

> ⚠ **R3, ao lado (13/10/2026). O que `v392_pins` pina para o vínculo.** Todos os valores são lidos por script, nunca de memória:
> - o sha256 de `BATERIA_VINCULO.json` e o de `sincronizar_bancada.py` R3, já copiados para `cadeia_de_selo\v392\vinculo\`;
> - o sha256 do `RECIBO_SINCRONIZACAO_v391_*.json` da etapa 1;
> - o sha256 do `KERNEL_RECIBO_v392.json` da etapa 2;
> - o sha256 do manifesto B2 vigente na Bancada (`54fc9e27e4599c49` hoje [REAL]);
> - o sha256 do `CANAIS_v392.json`.
>
> **Como a cadeia os usa.** No passo 10-bis, a cadeia passa esses valores em `--bateria-sha256`, `--recibo-pre-selo-sha256` e `--kernel-recibo-sha256`.
>
> **Sem pino circular.** O um.py v392 **não** pina o manifesto que o pina (12-bis, item 5).

---

## Remissão 4: §11 (etapa 9), ao lado do item 9 (l.379), do item 10 «Fechar» (l.393) e do item 11 «Depois» (l.395)

> ⚠ **R3, ao lado (13/10/2026). A numeração nova da cadeia pós-rito, com o B(3).** A lista acima fica como registro. A vigente é:
>
> 9. `grep -c` / marcador do selo na linhagem, sem mudança.
> 10. **B(3) ensaio:** o comando do B(3) (§0) com `--modo ensaio`. Recibo em `cadeia_de_selo\v392\bancada_B3_ensaio\`.
> 10-bis-a. **Parada do serviço, com recibo** [ato do operador, autorizado na B3]:
>     - quiesce e parada do `um_bancada.py`, no molde do `restart_and_deploy.ps1` / `RESTART_RECEIPT_R1.json` da B2;
>     - o recibo diz o PID, a porta 18777 fechada e a hora.
>
>     Sem esse recibo, a cadeia **para aqui** (`AGUARDA_OPERADOR`).
> 10-bis. **B(3) aplicar:** o comando do B(3) (§0).
>     - O esboço sonda o serviço **no início e imediatamente antes de cada gravação** (N3): antes do backup, do contrato, do temporário, da troca e do recibo em `estado\sincronizacao\`.
>     - Se o serviço voltou, a gravação é recusada e desfeita (rollback do manifesto).
>     - Grava o manifesto B3 só se os bytes forem os lidos no passo 3 (N4).
>     - A cadeia **para em `AGUARDA_OPERADOR`** se a B3 não estiver autorizada.
> 10-ter. **Religamento e reconexão** [ato do operador]:
>     - religamento do `um_bancada.py` com recibo de identidade: a versão servida é a v392 e o sha do manifesto é o do recibo do 10-bis;
>     - reconexão dos adaptadores MCP das sessões.
> 11. **Fechar** (o antigo 10): `fechar_v392.py` **recusa** sem o `RECIBO_SINCRONIZACAO_v392_*.json` do 10-bis e sem os recibos do 10-bis-a e do 10-ter. O handoff cita os três por sha256.
> 12. **Depois** (o antigo 11), sem mudança de conteúdo.
>
> **No molde** (`chain_pos_rito_v391.sh`, `6b2a096424cde73c`): 9 = `grep -c`, 10 = fechar [REAL, re-auditoria §6]. A inserção desloca o fechar para 11. O molde não tem passo que espere o operador; o 10-bis-a cria esse passo. **Consequência:** sem a palavra do operador para a B3, a custódia (§13) da v392 espera.

---

## Remissão 5: §12, ao lado do item 1 (l.405) e do item 3 (l.415)

> ⚠ **R3, ao lado (13/10/2026). Errata ao lado.**
>
> **Item 1.** O texto põe a B3 «depois do selo e antes da custódia», fora da cadeia. Isso contradiz o §12-bis. Vale o §12-bis: a re-pinagem B3 é o **passo 10/10-bis/10-ter da cadeia** (§11, Remissão 4), antes do fechar.
>
> **O que o B(3) faz e o que não faz.**
> - Faz só a re-pinagem de identidade: manifesto, contrato B3 e recibo.
> - O resto do item 1 (a unicidade da linha de α e de `UM_VERSION` no `canonical.py`, a rota do alias ou do rótulo do MCP, a custódia da suíte junto da Bancada, a errata no README de 28/09) é uma **implantação B separada**, com plano, backup, testes e evento próprios.
> - O B(n) **recusa** deriva de código (`CODE_DRIFT_NAO_E_SINCRONIZACAO`).
> - Mudança de código não entra no B(3). Entra na implantação que o operador autorizar junto com a B3.
>
> **Item 3.** O religamento do serviço passa a ser o 10-ter da cadeia, com recibo de identidade.

---

## Remissão 6: §12-bis, errata ao lado do item 1 (l.533) e do item 4 (l.536)

> ⚠ **R3, ao lado (13/10/2026). Errata ao lado.**
>
> **(a) Item 1: o comando está incompleto.** O comando `sincronizar_bancada.py --modo aplicar --producao --fase pos_selo --versao vNNN --evento <seq>` omite flags **obrigatórias**:
> - `--bancada`, `--bateria` e `--saida`, que o script exige;
> - `--bateria-sha256`, `--evento-hash`, `--recibo-pre-selo` e `--recibo-pre-selo-sha256`;
> - `--kernel-recibo` e `--kernel-recibo-sha256`.
>
> O comando vigente é o do §0 de `R3\REMISSOES_PLANO_R3.md`. Os passos 10/10-bis/10-ter ganham o 10-bis-a (parada com recibo), como na Remissão 4.
>
> **(b) Item 4: a regra do evento.** O texto descreve a regra R1 do evento: «quem = claude-c1; cita a versão, `Bancada_Um` e a sincronização», conferida por substring. Ela foi substituída. A regra vigente é a R2, endurecida na R3:
> - o evento é um elo de `C:\IALD\PROGRAMA_IALD\eventos.jsonl` com cadeia de hash íntegra do primeiro elo até ele (`anterior` == hash do elo anterior; `hash` recalculado) e `seq` único;
> - `tipo == "SINCRONIZACAO_BANCADA"` e `quem == "claude-c1"`;
> - `dados` é JSON com chaves num **conjunto fechado**: `versao`, `bancada`, `acao`, `um_py`, `selo`, `reparo`, `gravacoes`, `unidade` e `nota`;
> - `versao` é igual à alvo;
> - `bancada` é a mesma pasta **por identidade** (samefile);
> - `acao == "sincronizacao"`;
> - `um_py` e `selo` são prefixos (≥ 16 hex) do sha do um.py e do selo lidos no Nós;
> - `reparo` é booleano;
> - nenhuma negação, procurada em **chaves e valores** depois de normalizar (NFKC; NFD sem marcas nem caracteres de formato; caixa dobrada);
> - **(R3, N6)** o hash do elo confere com `--evento-hash`, que a cadeia lê do retorno de `iald.py anotar`.
>
> **O que a regra não é.** [INPUT da gerência, N6] `quem == claude-c1` é **convenção do quadro, não autenticação**: `iald.py anotar` aceita `--quem` livre. A cadeia de hash prova integridade e ordem, não quem escreveu. O recibo do B(n) diz isso por escrito.
>
> **O serviço.** O serviço é sondado no início e **imediatamente antes de cada gravação** (N3). No ar a qualquer momento, a gravação é recusada e desfeita.

---

## Remissão 7: §14, logo abaixo da linha «depois do selo | **B3** …» (l.451). Substitui a Remissão 2 da R2

> | ⚠ R3 (13/10) · depois do selo | **B3, agora como passo nomeado da cadeia (§12-bis; §11 passos 10 → 10-ter).** Autorizar a gerência a executar o comando do B(3) (`R3\REMISSOES_PLANO_R3.md`, §0, com todas as flags: `--bancada`, `--producao`, `--bateria`/`--bateria-sha256`, `--evento`/`--evento-hash`, `--recibo-pre-selo`/`--recibo-pre-selo-sha256`, `--kernel-recibo`/`--kernel-recibo-sha256`, `--saida`), sob **evento c1** `SINCRONIZACAO_BANCADA`. Antes, a **parada do `um_bancada.py` com recibo** (10-bis-a). Depois, o **religamento com recibo de identidade** e a **reconexão dos adaptadores MCP** (10-ter). Dizer-lhe por inteiro: **sem a sua palavra para a B3, a cadeia da v392 para em 10-bis-a (`AGUARDA_OPERADOR`), e o fechar, o handoff e a custódia (§13) não acontecem.** Também é decisão sua o que entra na implantação B3 de código (§12, Remissão 5). Da v393 em diante, se o senhor assim decidir, o B(n) corre sob a ordem permanente de 12/10 (`78ef70e6f9868281`), com evento c1 e veto preservado | sem a B3, a Bancada recusa toda operação científica (`PIN_CHANGED`, provado), e a custódia da v392 espera |

---

## Ressalva documental, mantida da R2 (ao lado, não por cima)

O bloco colado a partir da l.523 traz o cabeçalho «Parágrafo a acrescentar ao PLANO_V392.md (só o texto; o plano não foi editado)». Dentro do próprio plano, essa frase agora é falsa.

**Conserto:** uma linha ao lado do cabeçalho, sem apagar nada:

> ⚠ R3: este cabeçalho era do rascunho (`work\bancada_vinculo_12out\PLANO_V392_paragrafo_B3.md`, `54134728176b45dd`); o bloco foi colado em 12/10; as remissões entram em 13/10 (R3).

Nada aqui é leitura física. NOT_FALSIFIED nunca é creditação.
