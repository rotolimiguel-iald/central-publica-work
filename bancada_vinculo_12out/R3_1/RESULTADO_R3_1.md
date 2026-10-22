VINCULO R3.1 — 13/10

# Resultado da R3.1 do esboço `sincronizar_bancada.py` (F0.6, elo B(n) da cadeia de selo)

Construtor: subagente da gerência c1. Base: a R3 em `..\R3\`. As três fontes foram conferidas por sha antes de tocar: `sincronizar_bancada.py` `8894b74cb1e6d5a0`, `montar_sandbox.py` `518cd2af4f67093b`, `controles_negativos_r3.py` `9815086af0547a7f` [REAL]. A ordem veio da reauditoria curta `AUDITORIA_F0_6_C1_a61fad96.md`, que aprovou a R3 com ressalvas sob a condição de uma R3.1.

**Estatutos.** [REAL] = medido aqui por script. [DERIVED] = composto. [INPUT da gerência] = os esperados do `CRITERIOS_v392.json`. [DECLARADO] = números do plano transcritos sem conferir no Lean.

Nada aqui move o gate. Nenhum dado observado. NOT_FALSIFIED nunca é creditação.

## 1. Veredito

**`TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO`: 337/337 em 610 s** [REAL, `CONTROLES_NEGATIVOS_R3_1.json`, sha16 `6e27894064399966`].
- Os 235 da R3 estão presentes, 235/235, com os mesmos nomes.
- Há 102 controles novos.
- 88 controles da R3 mudaram de formato; a lista, com o motivo de cada um, está no JSON (§4).

**Duas rodadas anteriores falharam por defeito do CONTROLE, não do esboço.** Ficam como registro:
- **Rodada 1** (`CONTROLES_NEGATIVOS_R3_1_rodada1_336de337.json`, `bedecfc5f67445df`): 336/337. O controle `R31_A1_contagem_no_log_real_do_Nos` esperava contar só os avisos de sorry do log real e esqueceu os 2 `sorryAx` das linhas `#print axioms` do mesmo log. O esboço contou 4 (2 avisos + 2 `sorryAx`), e contou certo.
- **Rodada 2** (`CONTROLES_NEGATIVOS_R3_1_rodada2_336de337.json`, `6b8a06d84794e33e`): 336/337, mesmo controle. A correção levou `\b` como caractere de backspace para a regex do controle, que então contou 0 `sorryAx`.
- **Correção.** A lógica foi conferida isolada contra o log real (2 avisos, 0 aspas, 2 `sorryAx`). A rodada 3 deu 337/337.
- **Interrupção.** Entre as rodadas a conexão caiu. A rodada que estava em curso terminou sozinha e gravou o JSON; nada foi refeito por causa disso.

## 2. Os runs refeitos [REAL, sandbox `C:\t\vb5`; cópias em `evidencias_sandbox\`]

| run | o que é | resultado | recibo (sha16) |
|---|---|---|---|
| 1a | pré-selo, ensaio, b1 (manifesto pina o Nós real), bateria inteira | `JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA`; 13 PASSA, 0 FALHA, T17 fora da fase; todos os testes com `-E -P -s` pelo lançador | `be662bd0bc06411a` |
| 1b | o mesmo contra b2 (pina a cópia do Nós) | idem; é o recibo pré-selo que o B3 encadeia | `f26005e2b034e246` |
| 2 | pós-selo, aplicar `--sandbox` em b2, com tudo pinado: evento e hash, pré-selo e sha, recibo do kernel e sha, **critérios e sha** | `REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`; 13 PASSA. T17: contrato `KERNEL_RECIBO_R3_1`, 2 pedras e 2 declarações conferidas, pedras == diff formal, log do Audit ≥ 2 `#print axioms`, critérios == CRITERIOS `3a4ce6f0b4f817f2` (x19 = «nao»), ANTES cruzado com o recibo pré-selo | `b1e90da687282128` |
| 2bis | o B3 de novo | `JA_SINCRONIZADA__NADA_A_GRAVAR`; o recibo pré-selo foi cruzado pelo `seal_sha_pinado` que o manifesto B3 da R3.1 grava | `067f285180b8533b` |

O run 1a passou a bateria inteira da R2 com o isolamento novo (`-s`, lançador, APPDATA vazio, site do usuário só como caminho), inclusive os testes que importam numpy, scipy e torch, e os netos (T03, T12–T14, T16).

## 3. Os consertos, com os controles NOVOS no formato real

| achado | conserto | controles novos | exemplos do formato real |
|---|---|---|---|
| **A1** (MÉDIA) | `RE_LOG_SORRY` pega ``declaration uses `sorry` `` (crases), aspas simples, aspas tipográficas e `sorryAx` | 8 | linha **verbatim** de um log real: `Nós\bancada_corpus\ChainSiteOperators.20260905_150729.falha_lean.log` (sha16 `65139e029550bd86`, linha 13, com o CR do CRLF; só leitura). Nos 498 logs do `bancada_corpus` há 9 avisos com crase e 0 com aspas [REAL] |
| **A1b** | normalização: BOM UTF-16/UTF-8, UTF-8 estrito, CR sozinho → LF, sem ANSI, sem controle, NFKC, sem Cf | 12 | os ataques N1b/N1d/N1e do auditor refeitos; contraprovas com UTF-16+BOM e UTF-8+BOM limpos, aceitos |
| **A2** (MÉDIA) | build log vazio recusa; log do Audit ≥ `#print axioms` do Audit.lean pinado (`LOG_DO_AUDIT_CURTO`) | 7 | o N1f e o N1g do auditor (a mesma linha) |
| **A3** (MÉDIA) | esperados em `CRITERIOS_vNNN.json` pinado (`--criterios`, `--criterios-sha256`); o recibo traz só o `medido`; `CRITERIO_AUTODECLARADO` | 33 | o N1h do auditor (esperado = medido = 7); o modelo `CRITERIOS_V392.json` recusado; 15 malformações do arquivo de critérios; 6 pelo caminho inteiro (subprocesso); 2 no decoy |
| **N1k** | `pedras[].declaracoes`: no `axiom_report`, no log do Audit e na fonte | 7 | o ataque do auditor (declarações fora do `axiom_report` pinado) |
| **N1l** | `formal_files_antes`; pedras == diff formal | 8 | `TGLExt/PedraOculta.lean` selada e fora do recibo (o do auditor); arquivo removido; mudança fora de `TGLExt/` |
| **N1m** | toolchain como lista nos dois lados | 6 | manifesto sem toolchain; manifesto em texto com `"L"` no recibo (o `[0]` da R3 pegava a 1ª letra) |
| **N2c** | o pré-selo cruzado com o selo pinado no manifesto anterior, e o kernel com o pino desse selo; `seal_sha_pinado` gravado no manifesto B3 | 9 | o ataque «selo e kernel de outro rito» do auditor: unitário, subprocesso e decoy de produção |
| **N4b** | sonda → compara bytes → `os.replace` | 2 | decoy: mudança com o mesmo tamanho e o mesmo mtime durante a 5ª sonda. Recusa `MANIFESTO_MUDOU_DESDE_A_LEITURA`, a mudança fica, nenhum contrato nem temporário, e o `.bak` guarda os bytes do passo 3. Mais a ordem conferida no código |
| **N3a** | sonda depois do rollback; `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`; recibo com os dois sha e a nota `servico_e_manifesto_em_ram` | 3 | o serviço que sobe no `os.replace`; o rollback com o serviço já fora; a contraprova de que o recibo documenta a RAM |
| **A4** (resíduo) | filhos com `-E -P -s` por lançador pinado (`28011fd29878fb53`); APPDATA vazio por teste; `PYTHONNOUSERSITE=1` nos netos; site do usuário pela pasta conhecida do Windows, só como caminho | 6 | APPDATA de ataque (`.pth` e `usercustomize` que deixam marcas). Com o esboço em `-s`: **0 marcas** em processo nenhum. Sem `-s`: marcas **só** no processo do esboço, 0 em processo de teste (na R3 eram 4). Numpy importável no filho e no neto |

Mais um controle novo da família A1: `N1_unit_kernel_recibo_log_com_sorry_aspas`.

Os controles do recibo do kernel e dos critérios somam 128: 118 recusas e 10 contraprovas aceitas, todas como esperado [REAL]. Isso responde à ressalva sobre os «35 recibos inválidos» da R3, que o auditor não conferiu.

**O resíduo A4 medido** [REAL, no recibo do run 2]:
- `.pth`/customize do site do **sistema** que ainda executam: **nenhum**;
- `.pth` do site do usuário que **deixaram** de executar: `distutils-precedence.pth` (`2638ce9e2500e572`), `protobuf-3.20.3-nspkg.pth` (`c47e604f1738522a`) e `pywin32.pth` (`e7cd73df98b91c40`);
- o código dos pacotes do site do usuário (numpy, scipy, torch) segue **importável e não pinado**. Fica como resíduo declarado;
- o site do usuário real só foi lido.

## 4. Os controles antigos que mudaram de formato (88; motivos no JSON)

- **A3:** todo comando antigo com `--kernel-recibo` recebe `--criterios` e `--criterios-sha256`. É o CRITERIOS sintético da versão do comando; para os que rodam com `--versao v391`, uma cópia com só a versão trocada, também pinada. A recusa esperada não mudou.
- **Fixture:** a fixture-base do recibo passou ao contrato `KERNEL_RECIBO_R3_1` e as verificações unitárias recebem o CRITERIOS pinado. O código esperado não mudou.
- **`N1_sub_kernel_recibo_log_com_sorry` e `N1_unit_kernel_recibo_log_com_sorry`:** usavam o aviso com **aspas simples**, o mesmo formato da regex da R3, e por isso se confirmavam a si mesmos. Agora usam a linha **verbatim real** com crases. O formato de aspas ganhou controle próprio.
- **`N1_unit_kernel_recibo_toolchain_diverge` e `N1_unit_manifesto_toolchain_diverge`:** a divergência agora é em lista.
- **`N3_decoy_servico_volta_antes_do_recibo_em_estado`:** com o serviço ainda no ar depois do rollback, o código passa a ser o próprio, `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`.
- **`N5_PYTHONPATH_injetado_nao_chega_ao_teste`:** o T00_AMBIENTE agora exige `-s`, APPDATA vazio, nenhum `usercustomize` e o neto sem site do usuário. O controle confere que o PYTHONPATH é o site **real**, não o do ataque.
- **RUN_1a, RUN_1b e RUN_2:** `isolado()` exige `-E -P -s`, o lançador e APPDATA vazio.

## 5. N3a, por escrito (também no recibo de todo aplicar, campo `servico_e_manifesto_em_ram`)

O esboço não trava o arquivo nem a porta. Um `um_bancada.py` que suba no instante do `os.replace` lê o manifesto **novo** e o guarda em RAM; se depois houver rollback, o disco volta ao **anterior** e a RAM não.

Por isso:
1. depois do rollback, o B(n) sonda o serviço. Se ele responde, a recusa é `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO`, e o recibo traz `manifesto_novo_sha256` e `manifesto_em_disco_sha256`;
2. depois de **qualquer** rollback, o serviço tem de ser reiniciado com recibo de identidade (10-ter) antes de outro B(n);
3. depois da última sonda nada é visível ao esboço. O 10-ter confere a identidade do serviço religado.

## 6. Entregas (sha16 lidos por script; a lista completa está em `PINOS_R3_1.json`)

- `sincronizar_bancada.py` R3.1: `a85be74ffd7a1dee`.
- `montar_sandbox.py`: `15c699b5a4fcc83d`.
- `controles_negativos_r3_1.py`: `a7614fe341b1461a`.
- `medir_pinos_r3_1.py`: `9040b1e386fb1410`.
- `CONTROLES_NEGATIVOS_R3_1.json`: `6e27894064399966`.
- `CONTRATO_KERNEL_RECIBO_R3_1.md`: `c658115b360c82e4`.
- `CRITERIOS_V392.json` (modelo, não preenchido; recusado como está): `148f7ac7248e3e79`.
- `REMISSOES_PLANO_R3_1.md` (ao lado das da R3; corrige as três ressalvas da Remissão 2): `1b89232aa619786f`.
- `DIFF_R3_R3_1.patch` (os 4 `.py`; renome de `controles_negativos_r3.py` → `_r3_1.py` e de `medir_pinos_r3.py` → `_r3_1.py`): `33a47e9ba2bfc8c5`. O `git apply` sobre uma cópia da R3 reproduz a R3.1 **bit a bit** (`VERIFICACAO_DIFF_R3_1.json`, `202a10eb5e35876d`).
- `_construcao\`: os patches exatos que derivaram a R3.1 da R3, os blocos inseridos, `gerar_diff_r3_1.py`, `limpar_sandbox.py` e os stdout das rodadas 1 e 2.
- `evidencias_sandbox\`: os recibos dos runs 1a/1b/2/2bis, os recibos dos controles N3a, N4b e A4, o recibo do kernel e o CRITERIOS sintéticos, o manifesto do sandbox e o stdout da rodada 3.
- `registro_mapa_F0.6_R3_1.json`: o RESULTADO para a rota `infra.bancada_um.sincronizacao_vnnn`. **Não registrado no mapa** (a escrita estava restrita).

## 7. Garantias e limpeza [REAL]

- **Produção.** Simulada só por decoy em processo (`pd\`). A produção real foi só lida (a lista e o manifesto): lista igual e manifesto `54fc9e27e4599c49` antes e depois.
- **Nós.** Só lido: a cópia do v391 para o sandbox, como na R3, e o log de amostra do `bancada_corpus`.
- **Livro de eventos.** Só cresceu: o prefixo foi preservado, entrou o elo 721 (`avancar`, de outra sessão) e não nasceu nenhum elo de sincronização.
- **Sandbox.** `C:\t\vb5` foi apagado. As junções de cada rodada foram desfeitas com `os.rmdir` no link: na rodada 3, 0 restantes; da rodada interrompida para corrigir C4, `jb1` e `jprod` foram desfeitas por `limpar_sandbox.py`, sem seguir o alvo.
- **O que não rodei nem toquei.** Não rodei um.py nem selo. Sem HTTP nem MCP. Não parei nem religuei serviço real. Não toquei o quadro, o mapa, a memória de arquivo nem o túnel. Nenhum confidencial. A palavra guardada não aparece em nenhum arquivo meu: os controles a montam em RAM.
- **Memória ACOM.** Inscrição desta tarefa por `init` (`_memoria\ORIGEM_R3_1.md`, `17cb472f8230d83e`; referência em `_memoria\REFERENCIA_R3_1.json`). As etapas foram registradas por `transition`, como pede a instrução global do operador.

## 8. O que NÃO fiz

- **Kernel real.** Não construí kernel nenhum. O recibo do kernel e o CRITERIOS do sandbox são fixtures sintéticas de duas pedras.
- **Lean real.** O formato das linhas `'<nome>' depends on axioms` foi tomado do Lean 4.31 tal como o log real do Nós mostra. Com o desenho KH-N1 (a), o `run_cmd` pode imprimir em outra forma; o contrato §8 diz o que o `construir_kernel_v392.sh` tem de garantir.
- **`construir_kernel_v392.sh` e `derivar_cadeia_v392.py`.** Não os escrevi; não preenchi o `CRITERIOS_v392.json`; não apliquei as remissões ao plano.
- **Aplicar em produção.** Não apliquei; o serviço real não foi tocado.
- **Fora do alcance.** Não cobri link simbólico (sem privilégio), a corrida dentro de `caminho_canonico` nem a autenticação do evento (convenção, N6).
- **Rota aberta, fora do escopo.** O próprio `um.py` (Nós, l.192945, segundo o auditor) procura sorry com aspas simples. Não conferi nem mexi.
- **Contagem da gerência.** Os 64 avisos com crase medidos pela gerência não foram refeitos aqui; medi 9 no `bancada_corpus`.

## 9. O que é da gerência e o que é ato do operador

**Gerência c1:**
- reauditoria curta da R3.1 por quem não construiu;
- aplicar as remissões ao lado (R3 + R3.1);
- escrever o `construir_kernel_v392.sh` no contrato `KERNEL_RECIBO_R3_1`: sorry com crases, `formal_files_antes`, declarações por pedra, toolchain em lista, só o medido;
- preencher o `CRITERIOS_v392.json` [INPUT] depois da X19;
- derivar o esboço, a bateria e os critérios para `cadeia_de_selo\v392\vinculo\` antes da etapa 1;
- chamar o esboço com `-s`;
- registrar no mapa;
- abrir a rota do sorry com aspas no `um.py`.

**Operador:**
- a **decisão X19**, antes da etapa 2, porque fixa os critérios;
- autorizar a **B3**;
- a parada do `um_bancada.py` com recibo (10-bis-a);
- o religamento com recibo de identidade e a reconexão dos MCP (10-ter), **obrigatório também depois de qualquer rollback**;
- o que entra na implantação B3 de código;
- se a ordem de 12/10 vale da v393 em diante.
