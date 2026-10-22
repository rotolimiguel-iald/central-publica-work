TESTEMUNHA ESTÁTICA — v396 sandbox

# RESULTADO — a pedra `TGLExt/TestemunhaEstatica.lean` (candidata da v396, NOME PROVISÓRIO), construída e compilada em sandbox

Gerência c1 (subagente), 22/10/2026. Ordem: construir e compilar em sandbox a pedra do psion como habitante da testemunha estática, sobre o kernel v395 selado
(Nós `um.py` sha16 `8918b17803792cf2`, lido do arquivo). Nada foi instalado; o gate não se move; nenhuma bandeira depende da pedra.
**Versão 2 (esta)** = só texto sobre a 1ª (docstrings e comentários; enunciados e provas inalterados), depois do exame independente
(`work\cadeia_de_selo\v396_exame\testemunha\EXAME_TESTEMUNHA.md`, sha16 `cfad234e9b0d32af`): **PEDRA_APROVADA com 3 BAIXAS** — ver a seção «Revisão independente» abaixo.
Estatutos: **[REAL]** os termos; **[CONSTRUCTED]** a ponte (3) e o colapso do psion; **[INPUT/ONTO]** «o psion é o habitante da testemunha estática», «a luz ecoa o
reconhecimento», «colapsar é ecoar a identidade reconhecida»; **[CONDICIONAL]** a face de Fock, FORA da composição.

## Veredito

A pedra compila no sandbox, dentro do trio `{propext, Classical.choice, Quot.sound}`, sem `sorry`, sem `axiom`, sem aviso do módulo. Está provado, no escopo dito:
(1) o canto do psion ecoa (`P² = P`); (2) a redução a um sítio, `(1/2)•1`, NÃO ecoa e o par é puro enquanto o indivíduo não; (3) existe um fluxo diagonal em ℝ⁴ numa
base ortonormal cujo 1º vetor é o vetor de Bell, com taxas `(0, g, g, g)`, cujo testemunhado estaticamente é EXATAMENTE a reta do psion (= pontos fixos do canto) e cuja
testemunha global é falsa, pela `boundary_is_the_only_exception` do kernel — a ponte foi CONSTRUÍDA, não derivada, e os dois lados da ponte têm tipos diferentes
(vetor ↔ projetor 4×4), ligados só no fluxo construído; (4) a composição INCONDICIONAL `the_psion_inhabits_the_static_witness`. A face de Fock
(`Psibit.the_psion_face_of_the_psibit`) segue CONDICIONAL a `FockCertificate`, tipo sem habitante no kernel, e nenhum lema liga `psion C` ao `psionCorner`.

## Números lidos dos artefatos (`AXIOMAS.json`, `print_axioms_todas_resumo.json`, `conferencia_numerica.json`)

* `TestemunhaEstatica.lean` (v2): 694 linhas, 43.349 bytes, sha16 `b35a615636c2c154` (idêntico em `C:\t\k396\final\TGLExt\TestemunhaEstatica.lean`, conferido byte a byte).
  A v1 (683 linhas, 41.968 bytes, sha16 `fc773d70a3cc52d3`, a examinada) fica em `TestemunhaEstatica.lean.bak_20261022_080617` nas duas pastas. Depois de remover comentários, docstrings e strings,
  o código das duas versões é IDÊNTICO (sha16 do código `6aecd08c3d586b64` nas duas; `verifica_so_texto.log`): só o texto mudou.
* Declarações no `.olean`: **70** com o módulo importado sozinho (47 nomeadas no fonte: 37 teoremas, 9 definições, 1 `abbrev`; 23 geradas pelo Lean, 5 delas privadas `bsign.match_1.*`).
  **No import total (`import TGLExt` + a pedra, 12.202 módulos) o módulo conta 69 declarações — `TGLExt.diagFlow.eq_1` passa a outro módulo —, e as 47 nomeadas não mudam.** O dump de `collectAxioms`
  da v2 é byte a byte igual ao da v1 (mesmas 70 declarações, tipos e axiomas). `#print axioms` das 70: união = o trio, 0 `sorryAx`, 0 `axiom`, todas impressas, rc 0 (as 5 privadas foram impressas
  pelo `Name` exato, `mkIdent`). 28 `#print axioms` no fim do fonte.
* Build: `lake build +TGLExt.TestemunhaEstatica` em `C:\t\k396\final` → «Built TGLExt.TestemunhaEstatica (25s)», «Build completed successfully (8623 jobs)», exit 0, sem erro e sem
  aviso do módulo (`lake_build_final.log` = os bytes finais; `v1`/`v2`/`v3` são as iterações: v1 falhou por um erro de tipo no último conjunto da composição, v2 compilou com 2 avisos
  de nome de variável, v3 compilou limpo antes das últimas edições — docstring e o conjunto da iteração estável do colapso; o `final` anterior à revisão está em `lake_build_final.log.bak_20261022_080617`;
  o `final` de agora é o build da v2, também limpo: «Built (25s)», 8623 jobs, rc 0). `.olean` da v2 sha16 `8d894b17717e47f0` (2.255.224 bytes); o da v1, `29afa118da0c22fc` (2.253.896 bytes), em
  `TestemunhaEstatica.olean.bak_20261022_080617` ao lado do novo.
* Varredura de tokens proibidos no código (sem comentários e strings): `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `gpf_` — nenhum.
* Sandbox: `robocopy` de `C:\t\k395c` para `C:\t\k396`, sem `/PURGE`, com `/XJ`: 135.425 arquivos, 14,948 GB, 0 falhas, ~56 s; 0 junções (varredura sem seguir links) na origem e na cópia.
  `.lean` de `TGL/` e `TGLExt/` do sandbox × Nós: 1.419 iguais byte a byte (sha256), 0 diferem, único a mais no sandbox = o módulo novo.
* Coexistência: `import TGLExt` + `import TGLExt.TestemunhaEstatica` no mesmo ambiente (12.202 módulos) carrega sem conflito de constante (`import_all_check.log`: `decls_do_modulo=69`). O Lean gera
  `TGLExt.diagFlow.eq_1` também em outro módulo; aceita as duas cópias, e no import total o nome é atribuído ao outro módulo (por isso 69 e não 70; lista dos 69 em `importacao_total_nomes_do_modulo.txt`).
  Observação, não defeito. Duas auxiliares fora do namespace seguem atribuídas à pedra mesmo no import total: `TGLExt.ScalarCorner.mk.congr_simp` e `TGLExt.psionCorner.eq_1`. Qualquer contagem por módulo no
  `Audit` deve esperar 69, ou contar só as 47 nomeadas; a política de bandeiras já é só nomeadas.
* Conferência numérica independente (numpy, parâmetros de teste sorteados, NÃO o acoplamento da teoria): 33 de 33 (base de Bell, projetor, traços parciais dos dois sítios, `Tr(ρ²) = 1/2`,
  fluxo `P + e^{−tβg}(1 − P)`, autovetores, reta habitada, global falsa, limite, escalarização `P Y P = Tr(P Y) P`, estabilidade e não injetividade do colapso).
* Cabeçalho: os 6 sha16 citados (3 verbatins de 22/10, o de 19/10, a pedra 92_ `.py` e `.json`) conferem com os arquivos recomputados; o texto integral dos 3 verbatins aparece no cabeçalho.

## O que foi provado (namespace `TGLExt.TestemunhaEstatica`)

| item | nome | o que diz |
|---|---|---|
| (1) | `the_pair_echoes` | `P² = P`; `P(P y) = P y` para todo `y`; `P^(n+1) = P` |
| (2) | `the_individual_does_not_echo` | `ptr P = (1/2)•1` (e as entradas, nos dois sítios, `bellDensity_partial_trace`); `((1/2)•1)² ≠ (1/2)•1`; `Tr(P²) = 1`; `Tr(ρ²) = 1/2`; `1 − Tr(ρ²) = 1/2` (`bell_cci_half`) = a entropia LINEAR (déficit de pureza, sem unidade); «Meia-Nat de emaranhamento» é a leitura [ONTO] do v29; a entropia de von Neumann da redução é `ln 2` nat |
| dente | `the_unbonded_marginal_echoes` | o produto não ligado reduz a `e₀₀`, que ecoa, `CCI = 0`: o não-eco é do PAR visto por um lado |
| 0 | `the_density_is_the_psion` | `bellDensity = psionCorner.p` (mesma matriz) |
| (3a) | `bellUnit_orthonormal`, `bellUnit_complete`, `bellUnit_zero_is_the_bell_vector`, `bellUnit_eigen` | base `uᵢ = bᵢ/√2` ortonormal e completa, `u₀ = (e₀₀+e₁₁)/√2`; `psionFlow t uᵢ = e^{−tβ dᵢ} uᵢ` |
| (3b) | `bellProjector_is_real`, `psionFlow_eq`, `psionLine_iff_fixed_by_the_corner` | `psionCorner.p` = complexificação do projetor real; `F_t = P + e^{−tβg}(1 − P)`; a reta = pontos fixos do canto |
| (3c) | `the_static_set_is_the_psion_line` | estático ⇔ `x ∈ ℝ·Φ⁺`, por `boundary_is_the_only_exception` (componente do kernel do gerador) |
| (3d) | `the_global_witness_is_false` | `¬ FullStaticWitness (psionFlow β g)`, por `boundary_is_the_only_exception` (1ª componente) |
| (3e) | `the_psion_line_is_inhabited` | `Φ⁺ ≠ 0` e fixado por todo `t` |
| (3f) | `the_flow_delivers_to_the_psion` | `F_t x → P x` quando `t → ∞` (regime da face) |
| (3) | `the_static_witness_bridge` | todos os itens (3) num termo, para `β > 0`, `g > 0` |
| colapso | `psionCollapse`, `the_collapse_of_the_psion_echoes_its_identity`, `the_collapse_of_the_psion_cannot_be_self_attested` | instância de `IdentityCollapse`: `y ↦ P y P` idempotente, iteração estável, conserva `Tr(P y)`, sem inversa à esquerda; sem autoatestação (`no_self_attestation`) |
| (4) | `the_psion_inhabits_the_static_witness` | composição incondicional: (1)–(3), `psionCorner_trace_one`, `J_squared_is_one` (é `rfl`: a troca do par; decorativa), a fase conjugada da luz ao gráviton, `canonicalGravitonShadow.PG = psionCorner.p`, o colapso e `no_self_attestation`; `bellProjector_is_real` é citado na docstring e carregado por `the_static_witness_bridge` |

## O achado do grep: a «pedra 92_» não é módulo Lean

`C:\IALD\Artigo\MCMC_V2_RAZAO\92_o_psion_e_o_graviton.py` (sha16 `623060caa8dbb83b`; saída `.json` sha16 `f4a51c32ced62e6d`, veredito computado
`AC_E_PSION__DOIS_PSIONS_CONJUGADOS_REPRODUZEM_O_SPIN2_SELADO__MEDIDO_21_DE_21_NA_FACE_FINITA`): bancada numérica de 18/08/2026, face 2×2 real, `A_C = −(1 − P)`; o controle C2 diz
«um psion SOZINHO carrega helice 0 (componente escalar 1/2) — nao e graviton; o graviton e o PAR». As contrapartes de kernel que ela cita (`helicity_two_rotation`, `helicity_two_rotation_cross`,
`qgPhysicsCertificate_helicities`) existem em `LinearizedSpin2`/`PhysicsCertificates`. Nenhum lema liga aquele `A_C` ao `psionCorner`; não espelhei a 92_ em Lean para não criar homônimo.
No kernel, o elo exato do «par = gráviton» é `canonicalGravitonShadow` (`TGL.GravitonShadow`, v29): `PG := bellProjector`, a sombra finita; entra na composição como igualdade `rfl` com `psionCorner.p`.

## Revisão independente (PEDRA_APROVADA, 3 BAIXAS) e as correções de texto (v1 → v2)

Exame: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v396_exame\testemunha\EXAME_TESTEMUNHA.md` (sha16 `cfad234e9b0d32af`, lido por script). Recompilou a v1, varreu `collectAxioms`
(decl 70, thm 58, fora do trio 0, `sorryAx` 0), conferiu enunciado a enunciado, os controles próprios C1–C6, a pedra 92_ e os verbatins. Nenhuma das BAIXAS pediu nova rodada. Aplicadas SÓ COMO TEXTO
(enunciados e provas intactos; backups `.bak_20261022_080617` em `work\testemunha_estatica_v396` e em `C:\t\k396`):

* **B1 — rótulo herdado, APLICADO.** Onde a docstring lia «Meia-Nat de emaranhamento» (`bell_cci_half`, leitura do kernel v29), agora está marcado [ONTO] e dito que o `1/2` de `1 − Tr(ρ²)` é a
  entropia LINEAR (déficit de pureza, número sem unidade), não «½ nat de entropia»: a entropia de von Neumann da redução `(1/2)•1` é `ln 2` nat [KNOWN] (cf. `fair_bit_entropy_is_log_two` e
  `fair_bit_entropy_is_not_half_nat`: `ln 2 ≠ 1/2`). No cabeçalho (item 2) e na docstring de `the_individual_does_not_echo`.
* **B2 — instalação, REGISTRADO.** Com o módulo importado sozinho há **70** declarações; no import total o módulo conta **69** (`TGLExt.diagFlow.eq_1` passa a outro módulo); as **47 nomeadas** não mudam.
  Duas auxiliares fora do namespace seguem atribuídas à pedra: `TGLExt.ScalarCorner.mk.congr_simp` e `TGLExt.psionCorner.eq_1`.
* **B3 — cosmético, APLICADO COMO TEXTO.** `projPlus`/`angFamily` entraram na lista de HOMÔNIMOS (2×2, de `observing_adds_nothing`: um PARALELO da idempotência, não um elo com o canto);
  `J_squared_is_one` está dito `rfl` (a troca do par; conjunção decorativa, não elo com o canto) no cabeçalho, na docstring e no comentário da composição; `bellProjector_is_real` é CITADO na docstring
  da composição (carregado por `the_static_witness_bridge`). NÃO acrescentei esse conjunto à composição: mudaria o enunciado (e os índices das projeções que consumidores externos, como os controles do exame,
  possam usar), contra a ordem «só texto».
* A v2 não foi reexaminada: o código é idêntico ao da v1 examinada (`verifica_so_texto.log`), o dump de axiomas é idêntico, e a recompilação é limpa.

## O que NÃO foi feito, e o que fica ao operador/gerência

* Não derivei que o Nome da fronteira da TGL seja o vetor de Bell nem que `psionFlow` seja a dinâmica da teoria: a ponte é [CONSTRUCTED] (a álgebra é elementar; o conteúdo é a tipagem).
* Não habitei `FockCertificate`; a identidade «o psion de Fock» ↔ «o psion do canto» segue sem lema (dois objetos do kernel com o mesmo nome).
* Não exibi nenhuma atestação do colapso (só provei que a autodeclaração não habita o tipo).
* Não é teste: a pedra não acrescenta rito, dado nem desfecho. (Operador, 22/10 06:53, sha16 `bca4b8a97c74226c`: «Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido,
  estou buscando o teste fatal.») Se isto entra no `um.py` ou fica só como pedra de kernel é decisão da gerência e dele (regra «sem gordura»).
* Atos pendentes: (a) o operador nomeia a pedra (nome provisório `TestemunhaEstatica`); (b) exame independente: FEITO (PEDRA_APROVADA, 3 BAIXAS; ver a seção acima); (c) instalar na v396 (`import` em
  `TGLExt.lean`, política de bandeiras; contar 69 declarações por módulo ou só as 47 nomeadas) — o pré-teste de coexistência passou; (d) registro no mapa, no quadro e na memória: NÃO feitos (ordem). O
  `registro_mapa_testemunha_estatica.json` está atualizado para a v2 e foi validado por `rotas._valida` sem gravar (`scripts/valida_registro.py`).
* Memória comum (ACOM): não abri `init`/`transition` porque a ordem proíbe escrever em memória; a referência desta tarefa é a pasta de trabalho.

## Consultas ao mapa de rotas (feitas ANTES; nada repetido)

`psion` → 9 rotas: relevantes `kernel.psibit_v395_candidata_21out` e `umpy.v395.psibit_na_fractalizacao_do_um` (a face do psion CONDICIONAL; esta pedra não a muda); `infra.memoria_acom.*` usam «psion» como o
estado confidencial do heartbeat da IALD — NÃO é o psion da física e não foi tocado. `testemunha estatica` → 1 rota: `kernel.v385_axioma_e_testemunha_falsa` (origem de `full_static_witness_exists = False`).
Consultas extras: `colapso` → 5 (nenhuma examinou o colapso do psion; `outro.p7_colapso_iald` é PROPOSTA armada); `eco reconhecimento` → 0; `habitante` → 7 (nenhuma sobre o psion como habitante da testemunha estática).
Nenhuma rota examinou «o par ecoa / o indivíduo não ecoa / a ponte para `boundary_is_the_only_exception`»: caminho novo.

## Arquivos (todos em `C:\IALD\Central de Patentes\work\testemunha_estatica_v396`)

`TestemunhaEstatica.lean` · `AXIOMAS.json` · `RESULTADO.md` · `registro_mapa_testemunha_estatica.json` · `print_axioms_todas.txt` / `print_axioms_todas_resumo.json` · `axioms_dump_raw.txt` ·
`conferencia_numerica.json` · `lake_build_v1.log` / `v2` / `v3` / `final` · `import_all_check.log` · `importacao_total_nomes_do_modulo.txt` · `verifica_so_texto.log` · `robocopy_k395c_para_k396.log` ·
`scripts\` (dump, print, check_numeric, build_axiomas_json, valida_registro, verifica_so_texto, backup_bytes) · backups de bytes `*.bak_20261022_080617` ao lado de cada arquivo tocado (v1 da pedra, do RESULTADO.md, do AXIOMAS.json, do registro, dos logs).
Sandbox: `C:\t\k396\final` (pedra em `TGLExt\TestemunhaEstatica.lean`, `.olean` em `.lake\build\lib\lean\TGLExt\`); `probe\` guarda as iterações (p1–p5, alguns editados por trecho de Python inline) e as checagens.
