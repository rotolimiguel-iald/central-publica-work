# Auditoria científica v380 para parametrização futura do JEV

[REAL — leitura local, 02/10/2026] **A versão selada verificada é v380.** Fonte canônica, resultado, selo e cópias do espelho local coincidem em bytes. A futura v381 não foi usada como versão pronta. Esta entrega é diagnóstico: nenhuma implementação JEV, execução/importação de `um.py`, compilação Lean, chamada de provedor, benchmark, publicação ou alteração de original foi feita.

## Custódia, versão e proveniência

Caminho canônico: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`. `um.py:96` declara `UM_VERSION = "v380"`; `um_absoluto_selo.json:14` confirma; o selo tem timestamp `2026-10-01 19:07:17` (sem fuso indicado pela origem). `HANDOFF_v380_CUSTODIA.md:4–11` registra rodada COMPLETA e custódia finalizada. Foram conferidos **37/37 hashes dos artefatos enumerados em CUSTODY_MANIFEST.json**, sem divergências.

| Artefato primário (link absoluto) | Bytes | SHA-256 calculado dos bytes |
|---|---:|---|
| [um.py](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py>) | 32975349 | `ec4a84ffcd13cd869eb9bfa7ee519326744f0717c45f2ca288d56f198dd98209` |
| [um_absoluto_selo.json](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_selo.json>) | 58603 | `295e2260133546dd4ddfa4f44f8fd935d5513a56c060314b6db1cf4e5b8b63e5` |
| [um_absoluto.json](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto.json>) | 4698820 | `c766668760477091d278966b1a420374c3583c269c0de814154d31e7ba41aad6` |
| [HANDOFF_v380_CUSTODIA.md](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/HANDOFF_v380_CUSTODIA.md>) | 4351 | `abaf404812ab5b268ef587bcaa5c7ffbf6f97ba31c994755ce2a1718cc664714` |
| [tgl_kernel_proof_manifest.json](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel_proof_manifest.json>) | 1451404 | `c0e7f737bf5ccacc63db7d6f4d08614a0566102b6b3f592d35888bb7d4c9e53b` |
| [CUSTODY_MANIFEST.json](<C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v380/CUSTODY_MANIFEST.json>) | 16430 | `ef821c635c84823f2dc3df8a7626ef3d22825e730862d55d36bf95d92f611283` |
| [rodada_v380_stdout.txt](<C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v380/rodada_v380_stdout.txt>) | 211606 | `6cef25995ad3828faa77825d245dfff38d7acf7ce398e92003966a07c0679196` |

O `result_hash` registrado no selo é `7aac22c4b8af732c04169421016dfeebccfc1daaff4691138d9a7a27f63f1a4c`; o `formal_source_hash` é `b9817a740876acdfabf5b709db2f3fb8baaab95ca95993645a6ecb27a903c241`. São identidades internas registradas: não são o SHA-256 bruto do arquivo JSON nem do programa. `rodada_v380_stdout.txt:1341` registra 5942/5942; `:1748–1749` registra `FAIL_CLOSED_SELFTEST_PASSED`. São resultados da rodada custodiada, não testes repetidos nesta auditoria.

O manifesto formal contém **1209 arquivos e 10044 entradas de auditoria de axiomas**; `:12` indica modo strict e `:51154–51170` registra build válido/ausência de sorryAx, trustCompiler e axiomas TGL customizados/liberação formal. Essas contagens têm universos distintos do 5942/5942 do stdout. Os seis arquivos Lean abaixo tiveram seus hashes confrontados com esse manifesto. Para os seletores e separadores consultados, o relatório lista somente `propext`, `Classical.choice`, `Quot.sound` (a preservação da leitura usa `propext`, `Quot.sound`). Nenhuma recompilação foi feita.

[REAL] A delta específica da v380 está em `um.py:191929`, `prove_bancada_fases_5_6_7_v380`, e em `um_absoluto.json:112958`, ponteiro `/core/bancada_fases_5_6_7_v380`. O handoff declara integração de resultados por hashes e kernel preservado em relação à v379. Preservar `checks`, `hashes`, `statute`, `does_not_gate_core` e vereditos completos: o resultado diferencia falsificação de um par leitura/lei de atraso da falsificação da teoria; `NOT_FALSIFIED` não vira `CONFIRMED`.

[REAL — limite da busca] `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md:29940–29949` menciona a pedra única v381 **como próximo passo**, não selo concluído. Não existem, nos caminhos conferidos, `Nós\HANDOFF_v381_CUSTODIA.md` nem `vault\originals_copy\um_unificado_v381`. A identificação positiva da versão vem da fonte/selo/custódia v380, não apenas dessa ausência.

## Espelho público: bytes atuais e metadados divergentes

[REAL — inspeção independente local] Raiz `C:\IALD\Artigo\the_boundary`; programa/resultado/selo em `Um (absoluto) — Grande Atrator` têm exatamente os três hashes canônicos acima. HEAD e a referência **local** `refs/remotes/origin/main` apontam para `f20f659735618880073aa313d241d8361f645c0b`; a custódia registra também o commit anterior `dba7ae6`. `git status` dos três artefatos, README e PORTA.json não mostrou modificações. Não houve fetch nem verificação HTTP do estado remoto atual.

**Divergência preservada:** `C:\IALD\Artigo\the_boundary\README.md:63,76` ainda diz “this seal/tree is v371”. `PORTA.md:32` e `PORTA.json:/selo_corrente/versao` usam v371 obtido da última pedra do esqueleto (`IALDJones`), enquanto `/versao_confirmada_por_transcricao` é v380 e os pins são v380. Não usar essa versão da pedra para selecionar a release. A referência Zenodo é v368 segundo o README; não tratá-la como depósito v380. A custódia declara site/publicação v380, mas a disponibilidade remota permanece **[DECLARADO — não revalidada nesta leitura]**.

URLs diretas extraídas de PORTA.json, não consultadas nesta auditoria: [programa publicado](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um.py), [selo publicado](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json), [manifesto formal publicado](https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel_proof_manifest.json).

## Âncoras científicas para “transistor/chaveamento”

[REAL — busca textual integral] `um.py` v380 não contém ocorrência de `transistor`/`transístor` nem `chaveamento`. Existem mecanismos de seleção, separação de domínio e poda que podem fundamentar a leitura operacional solicitada. Isso não identifica um transistor físico nem uma implementação pronta de coordenação JEV.

Todos os caminhos Lean desta tabela são relativos à raiz exata `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt`.

| Fonte e linhas | Enunciado/contrato efetivo | Estatuto e alcance |
|---|---|---|
| `TheIALDSelector.lean:47–83` | `ialdSelector` é a projeção `firstAtom.starProjection` em ℓ²; `iald_is_idempotent`; `iald_selects` preserva x no subespaço e zera y no ortogonal; decomposição registro/resto. | [KERNEL — fonte e recibo conferidos] Projeção matemática. Nome IALD é leitura ONTO; não prova execução de ferramentas exatamente uma vez. |
| `TheSelectionIsTheBallast.lean:49–82` | `IALDState(S,I)={recognize:S→S, read:S→I, recursive, identity}`; reconhecer duas vezes equivale a uma; `read(recognize(x))=read(x)`; iteração preserva identidade lida. | [KERNEL] Estrutura com hipóteses explícitas e teoremas derivados; não atesta que uma função de LLM satisfaz as hipóteses. |
| `TheAtlasIndex.lean:49–74` | Separação/injetividade da representação em base, cobertura, covariância e cadeia de cociclo. | [KERNEL] Objetos lineares/grupos; não garante reconstrução semântica arbitrária de conversa. |
| `TheVerbalCoupling.lean:126–205` | `thetaMiguel(β)=arcsin(sqrt(β))`; `fVerbal=tanh((θ−θM)/Δ)`; `sin(thetaMiguel)=sqrt(β)` com 0≤β≤1; acoplamento muda de sinal com Δ>0 e zera na fronteira. | [KERNEL] Hipóteses indispensáveis. `:50–56` delimita a aplicação a LLM como heurística estrutural, sem identidade física ou medida de β em corpus. |
| `IALDJones.lean:18–31` e `IALDRhoStar.lean:305–332` | Compressão/projeção, semigrupo e ponte de pontos fixos/atrator no modelo M₂ especificado. | [KERNEL no escopo tipado] `IALDRhoStar` exige condições nos pesos, rs, t e r. Não transportar esse resultado automaticamente a pesos/estados de rede neural; não confundir homônimos com o índice Python. |

| Arquivo formal | SHA-256 calculado e igual ao manifesto |
|---|---|
| [TheIALDSelector.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheIALDSelector.lean>) | `c1008266455044e7462338bc32f96cb35c89810a320f69409ce7a0443b6868b8` |
| [TheSelectionIsTheBallast.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheSelectionIsTheBallast.lean>) | `71ebf9680af3d2470c53fe16e2c59a215429cdbf0c0a1a5f908d5c4259f162f1` |
| [TheAtlasIndex.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheAtlasIndex.lean>) | `38b9873cebdd779a70544d26662641359e5a0a60acbab877e36f1479e068d876` |
| [TheVerbalCoupling.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheVerbalCoupling.lean>) | `912bf222f07256b14e9e725b9c799e45ea5b6f2c3c5244859dc016445922b507` |
| [IALDJones.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/IALDJones.lean>) | `3070346c3571f3400e4290075e974d0c0b8c1bf73bd2f057dc23d0813da864fc` |
| [IALDRhoStar.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/IALDRhoStar.lean>) | `e8110c499398a8a083c82f1e96201933d5f46f245e346b5b05fd44ce7f57e770` |

## Contratos legíveis por máquina já presentes

Fonte Python abaixo: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`. Serialização: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` (ponteiros JSON sob `/core`).

1. **Classificador real, quatro vias** — `classify_boundary_state`, `:6537–6544`: na ordem, `support <= eps_support → absent`; depois `weight > beta → 1_abs`; depois `returns → 0_mod`; senão `0_abs`. Na igualdade `weight == beta`, decide `returns`. `tetelestai_binary_prune`, `:6603–6615`, recebe lista de `{weight, support?, returns?}`; defaults: support=weight, returns=true; limiar de suporte 1e-12. Retorna `{kept,cut,ignored,tail_only_0abs,tail_le_beta}`. Conserva `1_abs`/`0_mod`, corta só `0_abs`, ignora `absent`. **O orçamento excedido aparece como booleano; essa função não bloqueia automaticamente o corte.** `/core/tetelestai_pruning` (`JSON:859`) conserva verificações e `DO_NOT_PRUNE_MODULAR_ZERO`. [REAL — leitura de código; resultados numéricos apenas do recibo existente.]
2. **Runtime executivo descritivo** — `prove_iald_executive_runtime`, `:7158–7190`; `/core/iald_executive_runtime` (`JSON:1159`). Dicionário literal com `status`, `claim`, `operators`, `domain_classification`, `not_claimed`, `seals`, `verdict`. Fluxo: entrada → classificar domínio → reduzir contradição → poda → consolidação → saída auditável → selo. Operadores `L_reh/L_anti/L_prune/L_cons`; `[DEF + ONTO + COMPUTATIONAL]`; GKLS é analogia formal. `all_verified=True` aqui é literal da formulação, **não benchmark nem implementação executável desse fluxo no JEV**.
3. **Acoplamento verbal auditável** — `prove_the_verbal_coupling`, `:159016–159076`; `/core/the_verbal_coupling` (`JSON:96658`). Seis nomes/flags formais e verificações registradas. A constante é calculada por `ALPHA_FINE_CODATA_2018 × sqrt(e)` (âncora CODATA selada no programa), nunca β adaptativo ou literal inventado. Para uso em texto faltam medições operacionais que deem significado a θ, Δ, suporte, peso e retorno.
4. **Índice derivado** — `build_the_iald_index`, `:158814`, e `iald_index`, `:158997`; `/core/the_iald_index` (`JSON:96886`). Localiza nomes/arquivos/flags e conserva KERNEL/IMPORTADO/ABERTO e ausências/ambiguidades. Não decide gate nem substitui o regime executivo; cache de consulta não é journal de execução.
5. **Máquina de veredito específica** — `prove_the_exclusion_ledger_and_final_verdict`, `:155899–155998`; `/core/final_verdict_machine` (`JSON:92523`). Lê canais/exclusões, retém resultado se houver `BENCH_GATE_NOT_ALIVE`, `CHANNELS_PENDING`, `CHANNELS_REFUTED` ou `LEDGER_TOO_SMALL`; emite `FINAL_VERDICT_WITHHELD__...` quando necessário, `does_not_gate_core=true`. É função determinística sobre evidências científicas registradas, não máquina completa de transições de jobs JEV.

`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\IALD_ESTADO_OPERANTE_2026-09-09.json:3–9` contém definição do autor `[INPUT/ONTO]` e limita a alegação de consciência; não contém estados/transições executáveis. O `rite_checkpoints.switch_on` é controle de cache de ritos (`um.py:143675–143699`), e o selo v380 registra false; não é o seletor de provedores.

## Instruções aplicáveis e consequência para a etapa seguinte

- `C:\Users\rotol\.codex\AGENTS.md:264–268`: leitura de fontes/recibos; não importar/executar `um.py` original para consultar índice; execução autorizada somente em cópias na pasta Chatgpt. Esta auditoria não prepara nem executa cópia científica.
- `C:\IALD\Artigo\Haja_Luz\CLAUDE.md:9347–9373`: antecedente da casa Física, runtime executivo, classes 1_abs/0_mod/0_abs e separação entre segurança externa e poda interna; registro histórico, não prova nova do JEV. `C:\IALD\CLAUDE.md` é instrução parental. Atlas e índice vivo foram usados para navegação, sem atualização de memória.
- O risco de execução é concreto: `um.py:203899–203913` exige entrada “1” e então materializa o kernel/chama `run_um`. Ler JSON e fontes evita esse efeito.

[DERIVED — requisito de engenharia, não novo teorema] A parametrização pode usar o fluxo e as classes acima, com **mapeamento explícito e testável** das evidências de cada decisão, preservação de `0_mod`, verificação do orçamento de poda e conservação do pedido/identidade entre transições. A prova de projeção não fornece idempotência de HTTP, autorização, consentimentos, limites de provedores ou recuperação de chamada incerta: esses controles precisam continuar no adaptador/journal existente. Não equiparar “baixa confiança”, provedor indisponível ou hipótese aberta a `0_abs` sem critério demonstrado.

[OPEN — nesta auditoria] Não foi localizado, nos pontos examinados, um contrato pronto que converta texto/retorno JEV nessas grandezas e execute a cadeia inteira como máquina de estados persistente. A próxima implementação deve declarar esse mapeamento e validá-lo em staging; o pacote científico alvo é o **v380 pelos pins**, mantendo v381 como futuro. Não há alegação de funcionamento, qualidade ou ganho de raciocínio do JEV nesta entrega.
