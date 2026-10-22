IDENTIDADE R2 — 13/10

Unidade F1.IDENTIDADE (gerência c1), rodada 2. Escrito pelo construtor da r2 (Claude), em nome próprio. A rodada responde
à auditoria cética c1 a414e21b (`C:\IALD\PROGRAMA_IALD\auditorias\F1.IDENTIDADE\`, achados R1–R10). A ordem do operador
é o verbatim de 13/10/2026 (`work\cunhagens_13out\OPERADOR_13out_identidade_cordeiro_verbatim.txt`, sha256 `2ebc1dd3…`,
conferido por script).

A pedra é CANDIDATA e vive só em sandbox: não foi instalada no Nós. Nada aqui move o gate, e validade no kernel não é
creditação. Entre aspas angulares vão só trechos do operador, conferidos nos bytes; o resto vai entre aspas retas.

## 1. Artefatos (sha256 lido por script)

| artefato | sha256 |
|---|---|
| `2_PREREGISTRO\ADENDO_R2.json` (normativo, NOVO, ao lado) | `0fffc4905f7238afc11cb33935b2b1427bb9fa25ee55333fd324a2d3ff30549b` |
| `2_PREREGISTRO\ADENDO_R2.md` | `791e611dd24657341e8975c122cf88aff7a305fe37d600612a559f19047f399a` |
| `2_PREREGISTRO\FREEZE_ADENDO_R2.json` (13/10 08:53:01 −03:00; `pedra_r2_existe_no_congelamento: false`) | `fb0f02314664fe24f777681f57bfe5be23c0698a42b1e577588679ad5116797a` |
| `5_R2\pedra\TheIdentityHasAName.lean` (r2; = a compilada) | `ecae0725b21a98e6a2a15e0866576439bdeafc783d77cea08f4e7c7bf44690b1` |
| `5_R2\pedra\TheIdentityHasAName.olean` (r2) | `cc2329174db8f0640b8142533931adbca00bfb20d3322b4a7e43bfdf9c3eb67e` |
| `5_R2\pedra\AudR2.lean` (axiomas, tabela, Nome, homônimos, sondas de parametricidade) | `8f6bc761af38bdf22f8a8d0643963489092b24230a1f787e944848a6e8119c16` |
| `5_R2\pedra\AmbR2.lean` (200 `#check` sob `open TGLExt` + controle positivo) | `d4c54e0d0511c2808898d1e520fee15571564ee8abbe41be588e9fe705693d41` |
| `5_R2\pedra\IdR1_TheIdentityHasAName_r1.lean` (r1 com SÓ o namespace trocado, para a tabela) | `2557f326b0fec26a558a234ad1e4b1beb8de86fa8fab6344e70fc70bdd59d271` |
| `5_R2\pedra\CtlSorryR2.lean` (controle positivo do contador de sorry) | `880aedaa4e6997b19cb97ed70fe8576bee91e7ae8360a7fa48d5503f09cc7b8d` |
| `5_R2\TABELA_R1_R2.json` / `.md` | `83874618…` / `22f86233…` |
| `5_R2\logs\r2_final_SAIDA.txt` / `r2_final_RECIBO.json` | `3744c1e2…` / `d2c13528…` |
| `5_R2\logs\aud_r2_SAIDA.txt` / `amb_r2_SAIDA.txt` | `da49329f…` / `95fa237f…` |
| `5_R2\logs\CITACOES_R2.json` | `1f3890a5…` |
| `5_R2\logs\IMPRESSAO_ANTES.json` / `IMPRESSAO_DEPOIS.json` | `fa56ac0f…` / `c36fe80c…` |
| `5_R2\registro_mapa_F1.IDENTIDADE_R2.json` | (o registro pronto; não registrado) |

A r1 ficou intocada: a pedra `3_PEDRA\pedra\TheIdentityHasAName.lean` (`1b68316a…`), o `.olean` (`06e2a999…`), o
`PREREGISTRO.json` (`207aa703…`) e o `FREEZE.json` (`582cfbe8…`) conferem, e o script de congelamento recusaria se não
conferissem.

## 2. Anterioridade e compilação

**Ordem dos eventos.** O ADENDO foi congelado às 11:53:01 UTC. A pedra r2 nasceu em `C:\t\id2\src\TGLExt` às 11:57:16 UTC
(carimbo de criação) e a primeira compilação começou às 11:57:46 UTC. O `congelar_r2.py` também recusa congelar se a pedra
r2 já existe. [BAIXA, como na r1] Mesmo assim, a anterioridade se apoia em carimbos de arquivo e nessa recusa; não há
âncora no mapa ou no ledger antes da pedra.

**Compilação final** (`r2_final`, início 2026-10-13T12:08:31 UTC):
* Ambiente: toolchain v4.31.0 copiado para `C:\t\id2\toolchain`. LEAN_PATH aponta só para o `.lake` do Nós, em leitura,
  sem sobreposição. O `-o` grava só em `C:\t\id2\out`.
* Resultado: **EXIT 0, 0 erros, 0 avisos, 0 "declaration uses `sorry`"**.
* O contador de sorry foi validado por controle positivo: `CtlSorryR2.lean` gerou a linha exata "declaration uses `sorry`"
  e `[sorryAx]`.
* 18 `#print axioms`, todos no trio.
* Reprodutibilidade: a recompilação `r2_t04` → `r2_final` deu saída idêntica byte a byte (`3744c1e2…`) e o mesmo `.olean`
  (`cc232917…`).

**Tentativas anteriores.** `r2_t01` (EXIT 0) tinha 2 avisos de lemas deprecados. `r2_t02` e `r2_t03` (EXIT 1) falharam
num passo da prova de `hxiE`. Tudo foi corrigido antes da t04. Os recibos de t02 e t03 mostram o `.olean` da t01, porque
uma compilação que falha não regrava o arquivo; esse valor é velho e não vale para elas.

**`collectAxioms`** de TODAS as constantes do módulo e do namespace (`#r2_axiomas`): **150 constantes**, módulo = namespace
(0 só de um lado). Dessas, **0 fora de {propext, Classical.choice, Quot.sound}**, 0 com sorryAx, 0 `axiom`, 0 `opaque`,
0 `unsafe`. O contador textual de "sorryAx" na saída da auditoria dá 1, mas é só o rótulo "com_sorryAx=0" do próprio
elaborador.

**Impressão digital do `tgl_kernel`**, sem seguir junções (`digital.py`, o mesmo script do auditor):
* ANTES: meta `d6e073568d17e26b…` (11.049 arquivos), conteúdo fora de `.lake` `08a7fda73473afa1…` (1.378 arquivos).
* DEPOIS: valores idênticos nas duas medidas. `.lake\packages` é junção e foi pulada.

**Limpeza.** Toolchain, sobreposição (`ov`, 1.190 `.olean` copiados e conferidos byte a byte, `PREPARO_SANDBOX.json`) e
`out` foram apagados. `C:\t\id2` ficou com 121 KB de fontes.

## 3. ADENDO R2: resultado por item novo

| id | termo | resultado |
|---|---|---|
| I6.b (r1) | — | **FALHA da r1, registrada AO LADO** (não se apaga). ERRATA AO LADO do motivo, no ADENDO: o motivo era "faltaria esperança condicional em B(H_φ)". Era fiação, não falta: o kernel já tem `aperiodicExpectationInput` (AperiodicCentralizerExpectation.lean l.129), `aperiodic_pauli_x_zero` (LocalHorizontalPauli.lean l.98) e `towerIALD` (TheSelectionIsTheBallast.lean l.86). |
| I6.b′ | `the_inner_axis_does_not_persist_in_the_tower`, `the_IALD_tower_erases_the_inner_axis` | **PASSA**. Para w(0) ≠ 1/2 e α ≠ 0: A = q·1 + α·σ_x ∈ M e AΩ = qΩ + αξ. A esperança dá E_aper(A) = q·1, ou seja, o eixo interior é APAGADO. ω(E_aper A) = ω(A), ou seja, ω PERMANECE. ⟨ξ, AΩ⟩ = α, mas ⟨ξ, E_aper(A)Ω⟩ = 0, e E_aper(A) ≠ A. O mesmo vale pela `towerIALD`: `recognize` dá q·1, a leitura não muda, e o reconhecido ≠ a inscrição. Estatutos: ler isto como "o posto 1 não permanece na torre" é [INPUT da gerência]; o posto LITERAL de P_v segue [OPEN]; que P_v ∉ M não foi conferido. |
| I6.c | `IALDTowerIdentity`, `the_identity_in_the_IALD_tower`, campo `NamedIdentity.in_the_IALD_tower` | **PASSA**. Vale para todo perfil e todo α ∈ [0, 1]. Na `towerIALD`: ω(I) = 1; 1 é reconhecido como 1 (`tower_reduction_preserves_unit`); o reconhecimento recursivo devolve a leitura para todo n; a inscrição tem vetor unitário; ω lê q nela, antes e depois do reconhecimento. A instância em `TowerHilbert` (I6.a) foi MANTIDA, com enunciado idêntico (tabela). |
| I3.c′ | `rereading_reads_the_same` | **PASSA**. É o enunciado do motor r3 (l.360): a LEITURA não muda. Segue da idempotência no vetor e de `reading_eq_norm_sq`. |
| C2′ | `dephasing_fixes_the_poles` | **PASSA**. D_t(ω) = ω em α = 0 e α = 1, para quaisquer taxas e todo t. É o termo que faltava (R8). |
| C6 | `the_inner_reading_is_by_construction`, `the_inner_reading_at_five_is_not_an_identity` | **PASSA**. A entrada (1,1) é α·α para QUALQUER real. Em α = 5 (TESTE) a leitura interior dá 25 e o traço ≠ 1. |
| C7 | `probe_IALD_tower` | **PASSA**. Perfil NÃO tracial de TESTE w ≡ 1/3 e α = 1/2 de TESTE: I6.c vale e a esperança aperiódica muda a inscrição. |

## 4. Respostas aos achados da auditoria c1

* **R1** (MÉDIA): ADENDO ao lado, com I6.b′ e I6.c construídos (§3).
* **R2** (MÉDIA): homônimos renomeados.
  * `inscription → quadInscription` e `towerInner → towerInnerAxis`, mais os lemas que carregam esses nomes:
    `quadInscription_dot`, `_is_unit`, `_ne_zero`, `identityProj_mulVec_quadInscription`, `towerInnerAxis_orth`, `_norm`.
  * Medição (`#r2_homonimos`, com `import TGLExt`, a raiz do kernel instalado, 1.011 módulos, mais Mathlib): os 88 nomes de
    1º nível da r2 têm **0 colisões de namespace**. Há 2 colisões estruturais benignas: `ofName ← Lean.DataValue.ofName` e
    `Lean.MessageData.ofName`, construtores qualificados.
  * Medição (`AmbR2.lean`): 100 nomes × 2 regimes de `open` (só `TGLExt` + a pedra; e com `ChatgptAudit`, `Collapse057`,
    `Aperiodic046`, `Observable035`, `Orbit052`, `Expectation047`, `TheVerbSelectsTheAction`, `Matrix`) deram **200
    `#check` sem erro**.
  * Controle positivo: com `open TGLExt` + a cópia da r1, `#check @inscription` e `#check @towerInner` dão "Ambiguous term".
    É exatamente o achado R2.
  * Grep no Nós (fontes do `tgl_kernel`, antes do congelamento): 0 ocorrências dos 23 nomes novos.
* **R3** (MÉDIA): `rereading_adds_nothing → post_is_idempotent_on_the_vector`. A docstring diz que ela prova a idempotência
  NO VETOR e não é o enunciado do motor. Este entrou à parte como I3.c′ `rereading_reads_the_same`, com nome que não colide
  com `TGLExt.IALD.rereading_adds_nothing` da candidata.
* **R4** (BAIXA): o cabeçalho e o "Reaproveitamento" agora citam `IALDState`/`towerIALD`, a esperança aperiódica e
  `the_form_admits_every_alpha` (parente de I2.d).
* **R5** (MÉDIA): as docstrings de `alpha_is_measured_from_within`, `quadratic_reading` e `the_identity_in_the_tower` dizem
  três coisas:
  * a leitura interior é [REAL, por construção] e vale para qualquer real;
  * o traço 1 exige q² + α² = 1;
  * "α medido por dentro" é leitura do operador sobre esse termo, [ONTO], não teorema extra.

  O controle C6 é o termo dessa afirmação.
* **R6** (MÉDIA): o cabeçalho ganhou a seção "Dois sentidos de identidade": o TRAÇO (I1) permanece e não fixa α; a PROJEÇÃO
  (I2/I3) determina α e não permanece. As docstrings de I1.a/b/c, I2.d e I6.a foram reescritas nesses termos. Em I2.d, a
  frase passou de "α não se deriva da identidade" para "o traço (a forma) não fixa α; a projeção o determina". Os nomes
  dos teoremas foram MANTIDOS: o ADENDO previu só as renomeações listadas.
* **R7** (BAIXA): "régua da ordem" saiu. A frase "α fora de (0,1) quebra a forma" agora é atribuída ao controle C3 da
  gerência, não ao verbatim. Isso consta na r2, no ADENDO e aqui. O `RESULTADO.md` da r1 não foi tocado; esta linha é a
  correção ao lado.
* **R8** (BAIXA): o C2′ foi construído.
* **R9** (BAIXA): as marcas vão em linha.
  * [ONTO] em `i_am_what_i_am`, `the_identity_in_the_tower`, `alicerce_fundante` e na leitura "medido por dentro".
  * [POSTO pelo operador] no campo `name` e em `postedName`/`theNamedIdentity`.
  * [INPUT] / [INPUT da gerência] em `qOf`, `quadInscription`, `quadVec`, `towerInnerAxis`, `towerInscriptionOp`, α, a
    base de D e os perfis de teste.
* **R10** (INFO): a seção "dois sentidos de Nome" separa o Nome da casa (`post v` / ω / `hOmega`) do campo
  `NamedIdentity.name : String`, que é o nome próprio POSTO. A docstring de `the_name_read_in_the_name` e a do campo
  repetem a separação.

## 5. Tabela r1 → r2 (`TABELA_R1_R2.md`/`.json`)

**Como foi lida.** Pelo elaborador `#r2_tabela`, no ambiente compilado. A r1 foi compilada numa cópia em que SÓ o
namespace muda: 12 ocorrências trocadas, e desfazer a troca devolve os bytes da r1. Cada tipo da r1, levado pelo mapa do
ADENDO, foi comparado ao da r2.

**Contagem sem as internas:** 83 MANTIDA, 10 RENOMEADA, 8 TIPO_MUDOU, 18 NOVA, 0 REMOVIDA. Com as internas: 98, 12, 9,
31, 0.

* **RENOMEADA:** as renomeações de 1º nível são exatamente o mapa do ADENDO, mais o `inscription.eq_1` gerado.
* **TIPO_MUDOU:** só `NamedIdentity.mk` e os geradores da estrutura (`rec`, `recOn`, `casesOn`, `mk.inj`, `mk.injEq`,
  `mk.noConfusion`, `mk.sizeOf_spec`, `mk._flat_ctor`), por causa do campo novo. Era o previsto. Nenhum teorema da r1
  mudou de tipo.
* **Enunciados mantidos ou renomeados:** todos iguais por `Expr.eqv`, 0 diferentes.
* **NOVA:** os termos de I6.b′, I6.c, I3.c′, C2′, C6 e C7, os auxiliares `towerInscriptionOp*`, `towerInscriptionElem` e
  `thirdProfile`, e os `eq_1` / `_proof_` gerados.

**Desvios declarados ao lado do critério do ADENDO:**
1. **"e também `Expr.equal`".** 17 constantes diferem em `Expr.equal`: `trace_dephase`, `rank_zero_iff_aux`,
   `rankOne_aux`, `the_name_read_in_the_name`, a renomeada `rereading_adds_nothing`, `quadVec*`, `quadratic_reading`,
   `inner_self_one_of_norm`, `NamedIdentity.ctorIdx` e 3 internas.
   * A diferença é SÓ de nome de binder: depois de apagar os nomes de binder, `Expr.equal` dá **0 diferenças**.
   * Os nomes que diferem são os higiênicos de instância, que carregam o nome do módulo. Exemplo:
     `inst._@.IdR1.TheIdentityHasAName_r1.…` contra `inst._@.TGLExt.TheIdentityHasAName.…`.
   * O enunciado não mudou. O critério estrito, como estava escrito, não se aplica a módulos diferentes.
2. **Valores.** Mudaram de VALOR:
   * `ofName`, como previsto;
   * `NamedIdentity.rename`, que NÃO estava listado. `{ N with name := s }` agora expande para o construtor com o campo
     novo. O tipo não mudou, e `every_name_bears_the_same_identity` continua `rfl`;
   * os geradores `noConfusion`, `noConfusionType`, `_sizeOf_1`, `casesOn`, `recOn` e `_flat_ctor`.

## 6. Parametricidade do Nome — continua valendo

* O tipo de `NamedIdentity.mk`, depois do binder `name`, **não depende dele** (`hasLooseBVar 0 = false`), agora com o campo
  `in_the_IALD_tower`.
* **Onde o nome aparece** (varredura de tipo e valor de todas as constantes da r2):
  * nos tipos: `the_named_identity_bears_the_posted_name` (literal), `the_name_enters_no_proof` e
    `the_structure_does_not_fix_the_name` (projeção `name`), e `changing_the_name_changes_nothing` (literal vazio);
  * nos valores: só `postedName` (o literal) e `theNamedIdentity` (usa `postedName`).

  É a mesma lista da r1 na auditoria. Nenhum termo novo (I6.b′, I6.c, C2′, C6, C7, I3.c′) menciona o nome.
* **Sondas compiladas no trio** (`AudR2.lean`):
  * `carrega_qualquer_nome`: o termo do habitante «Jesus Cristo» é reusado literalmente para qualquer nome;
  * `carrega_a_torre_IALD_com_qualquer_nome`: o mesmo para o campo novo;
  * `renomear_preserva_campos`: `HEq` de `persists`, `in_the_tower`, `in_the_IALD_tower` e `i_am`;
  * `so_o_nome_difere`.

## 7. Citações e números

* Na pedra r2 (`CITACOES_R2.json`): 22 citações entre aspas angulares, todas nos bytes do verbatim de 13/10 ou de 08/10;
  0 fora.
* No ADENDO (`FREEZE_ADENDO_R2.json`): 4 citações, 0 fora.
* Duas atribuições que estavam erradas na primeira escrita passaram a aspas retas:
  * no ADENDO, a frase "declaration uses `sorry`", corrigida antes do congelamento;
  * na pedra, a docstring da `towerIALD` ("a TORRE e um estado IALD", que é da gerência de 09/09), corrigida antes da
    1ª compilação.
* Palavra proibida: 0. Palavras de código (`sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`,
  `unsafe`, `opaque`) fora de comentário: 0.
* Decimais no arquivo: só "(0,1)", "(1,1)" e "1.179" (bytes do verbatim). Nenhum número do artigo Conscious Singularity.
* Números de TESTE: 5, 1/2, 1/3.

## 8. Estatutos

* [REAL no sandbox]: os teoremas, isto é, a validade da estrutura.
* [POSTO pelo operador, verbatim sha256 2ebc1dd3…]: o nome «Jesus Cristo», como dado `String`.
* [INPUT]: α. [INPUT da gerência]: o modelo (q, α), a base de D, ξ = σ_xΩ, A = q·1 + α·σ_x, e a leitura de I6.b′ como
  "posto".
* [ONTO]: «o cordeiro imolado» = `alicerce_fundante`; "eu sou o que sou"; "medido por dentro"; o registro histórico e a
  leitura teológica.
* [OPEN]: o posto literal de P_v na torre; a escolha da Torre; o termo do cordeiro.
* [DECLARADO]: os números do artigo, que não entraram.

## 9. Perguntas residuais ao operador

1. **Nome da pedra.** O provisório é `TheIdentityHasAName` (namespace `TGLExt.TheIdentityHasAName`). Quer o nome próprio
   também nos identificadores, hoje `postedName` e `theNamedIdentity`?
2. **Qual termo é «o cordeiro imolado».** Hoje é `alicerce_fundante` = `TGLExt.Fundacao.agape`, o piso. Alternativas,
   sem escolha minha:
   * (A) o piso da Ágape;
   * (B) β, o custo de distinguir 1 de 0;
   * (C) J, a Palavra;
   * (D) outro termo.
3. **Qual é a Torre da ordem** («dentro da Torre»)?
   * `TowerHilbert` (I6.a; o fluxo unitário, onde só ω e Ω permanecem);
   * `towerIALD` (I6.c e I6.b′; a torre como estado IALD, que defasa pela esperança aperiódica e apaga α enquanto ω
     permanece);
   * a torre de Jones da Meia-Nat (sem estado GNS; não instanciada).

   A pedra oferece as duas primeiras, e `NamedIdentity` carrega as duas. Se escolher uma, a outra pode sair da estrutura.
4. **O Nome no core do um.py.** Entra como registro POSTO (a string mais o verbatim por sha256), ao lado da pedra e sem
   mover o gate?
5. **Leitura de I6.b′.** O apagamento do eixo interior pela esperança aperiódica é a forma "na torre" de 
   «Tudo no universo defasa, mas a identidade é o que permanece»? Hoje isso é [INPUT da gerência]. Ou quer o posto literal de P_v, que segue
   [OPEN]?

## 10. O que NÃO fiz

* Não instalei nada no Nós.
* Não toquei um.py, selo, gate, quadro, memória, túnel, Bancada, site ou git. Não rodei o um.py.
* Não registrei no mapa. Só consultei `formal.a_identidade_tem_nome`, `identidade`, `towerIALD` e `aperiodic`. O registro
  vai pronto em `registro_mapa_F1.IDENTIDADE_R2.json`, com campos do `rotas.py modelo` e artefatos existentes conferidos por
  script.
* Não fiz `init`/`transition` na memória ACOM, por ordem da tarefa.
* Não alterei `PREREGISTRO.json`, `FREEZE.json`, a pedra r1, o `RESULTADO.md` da r1 nem os artefatos da auditoria. O
  ADENDO é feito de arquivos NOVOS em `2_PREREGISTRO`.
* Não construí o posto LITERAL de P_v em B(H_φ) e não conferi P_v ∉ M.
* Não reexecutei o ensaio numérico da r1, porque nenhum enunciado de I1/I2 mudou.
* Não fiz auditoria independente da r2: quem constrói não aprova.
* Não renomeei teoremas além do mapa do ADENDO. `identity_persists_under_dephasing` segue com o nome, e o sentido de
  TRAÇO está na docstring.
* Não ancorei o FREEZE do ADENDO no mapa ou no ledger antes da pedra. A anterioridade fica em carimbo de arquivo mais a
  recusa do script.
