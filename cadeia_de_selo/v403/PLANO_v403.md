# PLANO da v403 — CAMINHO, VERDADE e VIDA (os nomes do operador) + F8.1 (as bandeiras do gate calculadas)

Gerência c1 da Central, 2026-10-27 08:54. Estatutos: [REAL] lido aqui por script; [DERIVED] composto; [INPUT] fala do operador; [ONTO] leitura; [OPEN] em aberto; [DECLARADO] dito na origem, não conferido aqui. Base: a v402 SELADA (`um.py` `6a5033dc3f29324c`, lido do selo e conferido no arquivo). O gate NÃO se move; PROVADA = validade, não creditação.

## 0. A ordem

- **Nomes [INPUT, decisão do operador, 27/10/2026]:** CAMINHO = a ponte da escala dual; VERDADE = a esperança condicional, como ADENDO da pedra `Verdade` (v392); VIDA = a queda sem geometria. Verbatins: `OPERADOR_27out_nome_verdade_triplo_espectral_do_contorno_verdadeiro_verbatim.txt` sha16 `ef3ca5eb1edbdddf`; `OPERADOR_27out_e_isso_mesmo_concordo_com_tudo_prossiga_caminho_verdade_vida_verbatim.txt` sha16 `b34bd70fa8cfb0b2` («é isso mesmo, concordo com tudo, prossiga»). «Verdade» sozinha para as três: recusada (homônimo de `TGLExt.Verdade`, `9ebd552564440083`). O nome do TRIPLO inteiro NÃO foi dado (fica com o operador; João 14,6: três predicados de um só «Eu sou»; a casa já cunhou EU SOU = 1 = 1).
- **Regra sem gordura (19/10):** a v403 não sela só por nomes; o passo material é a **F8.1** do quadro do programa (PROPOSTA, claude-c1): «Bandeiras do gate calculadas e independentes — versão selada com as bandeiras recalculadas e o achado da auditoria fechado».
- **Pedra selada não se renomeia por cima:** `PonteDaEscalaDual` (`0e55b6e448adbd91`), `QuedaSemGeometria` (`0ffce7f1d564d271`) e `EsperancaCondicional` (`8579115333f84428`) ficam como registro; os módulos novos compõem por citação (padrão `Token` `0b6a58e795af7311`; padrão `PostoAdendo` `f0fa5694367a5157`).

## 1. As três pedras candidatas [REAL — compiladas no sandbox k403c; nada tocado no Nós]

| módulo | sha16 | bytes | no sandbox | .olean | tipos (último log) |
|---|---|---|---|---|---|
| `TGLExt/Caminho.lean` | `703b5bbfbf8b3018` | 4165 | True | True | dev_Caminho1.log: axiomas no trio True, warnings 0, errors 0 |
| `TGLExt/Vida.lean` | `9836c760bc1776f9` | 3862 | True | True | dev_Vida1.log: axiomas no trio True, warnings 0, errors 0 |
| `TGLExt/VerdadeAdendo.lean` | `7f6b3eba7adb09be` | 6173 | True | True | dev_VerdadeAdendo2.log: axiomas no trio True, warnings 0, errors 0 |

- `Caminho.caminho_e_a_ponte_da_escala_dual` = `lift_mass_not_selected` ∧ `core_positive_realization_exists` (citação; nenhuma matemática nova).
- `Vida.vida_e_a_queda_sem_geometria` = `the_fall_is_strictly_anti` ∧ `a_queda_sem_geometria` (citação).
- `VerdadeAdendo.the_name_reads_the_inscription_as_weights` [REAL, novo e pequeno]: `diagExpect (identityProj a) = diagonal ![q², α²]`; `verdade_lida_pelo_nome`: `Verdade a` ∧ o Nome de ρ* lê `identityProj a` como diag(q², α²) ∧ traço 1 (o Um preservado) ∧ reler não acrescenta; `verdade_e_a_esperanca_condicional` = `the_identity_is_the_truth` ∧ `esperanca_condicional_e_nome` (citação).
- Sandbox: `C:\t\k403c\final` = robocopy de `k402c\final` (o kernel v402 compilado; `TGLExt.lean` da cópia = Nós `065a0206da7a89f3`), com a raiz do sandbox acrescida dos três imports (`bd7d5d060db6bf2e`; o Nós segue `065a0206da7a89f3`). Marcas da construção incremental (`v403_kernel\construir_marcas.txt`):

```
inicio 2026-10-27 08:43:26
epoch_inicio=1793101406
rc_build=0 08:49:37
epoch_build_fim=1793101777
rc_audit=0 08:53:25
epoch_audit_fim=1793102005
rc=0
fim 2026-10-27 08:53:25
```

## 2. F8.1 — as três bandeiras literais do gate passam a CALCULADAS, fail-closed, das fontes que o próprio `um.py` já tem [DERIVED; âncoras lidas do `um.py` v402 agora]

O gate `evaluate_quantum_gravity_closure` (l.170454) lê 15 bandeiras no veredito (6 formais + 5 físicas + 4 experimentais) e NÃO muda de superfície. O chamador `prove_qg_closure_gate` (l.170507) carrega 3 literais informativas (auditoria de 28/09, GV-03 e EV-12; registro `lacuna de fidelidade` da v392):

| literal hoje | linha | fonte REAL já existente no `um.py` | leitura fail-closed proposta |
|---|---|---|---|
| `physics["linearized_spin2_finite_face"] = True` | 170531 | a bandeira do kernel `linearized_spin2_finite_face` (família `_LEAN_THEOREM_FLAGS`, termo `dLs2`, l.149775), já lida de `kernel_formalization` | `bool(kf99.get("linearized_spin2_finite_face") is True)` |
| `"protocol_pre_registered": True` | 170541 | a checagem `("pre-registro v67 INTACTO (hash)", prereg_ok)` do rito V11 (l.4180; `prereg_ok = proto_hash[:16] == SEALED_VOID_FLOOR_HASH16`) | ler a checagem pelo rótulo em `independent_rite["checks"]`; ausente → False |
| `"null_tests_passed_blind": True` | 170542 | o teste nulo CEGO da v73 em centros aleatórios: `void_stacking_blind["all_verified"]` (retorno em l.152404; calculado em l.151653, ANTES da chamada do gate em l.151795) | novo kwarg `blind_null=None` em `prove_qg_closure_gate`; `bool((blind_null or {}).get("all_verified") is True)`; a chamada passa `blind_null=void_stacking_blind` |

- As CHAVES do dict `experiment` e do dict de retorno não mudam (a superfície do gate é reproduzida por AST nas auditorias); só os VALORES deixam de ser literais.
- Os probes negativos (`probe_void_as_proof`, `probe_empty`, `probe_physics_without_math`) seguem iguais; um probe NOVO: `blind_null` ausente ⟹ `null_tests_passed_blind = False` e o veredito do gate NÃO muda (a bandeira é informativa) — prova em runtime de que a literal nunca entrou no veredito.
- GV-03 (as 4 experimentais são logicamente UM booleano: `verdict_V11 == NOT_FALSIFIED_POWERED`; `survey_mocks_passed` = split-null ∧ dist-check, sem mock; feed em l.159242): NÃO se renomeia a chave; entra no registro a declaração explícita, ao lado, e `statuses` do V11 ganha a frase. Mocks de survey seguem [OPEN] (programa).
- **Registro novo com função `bandeiras_do_gate_v403`:** lê do core as 18 bandeiras (6 formais, 6 físicas, 6 experimentais) com a FONTE de cada uma (termo Lean / checagem de rito), confere: 18 calculadas (0 literais), 15 no veredito, as contagens «18», «15» e «6+5+4» reconciliadas; e confere que `qg_closure.gate.verdict` é IDÊNTICO ao da v402 (lido do core base por bytes) — **o gate não se move**; se qualquer bandeira calculada vier False, o registro RECUSA e o rito para (fail-closed; resultado honesto, não se mascara).
- **Registro por spec `cunhagens_v403`:** os dois verbatins de 27/10 por sha256, os três nomes, a leitura [ONTO] da tripla espectral (ratificada) e a decisão de que o triplo inteiro não tem nome.
- Artigo (PT/EN) e `.md`: seção curta «Caminho, Verdade e Vida» (os nomes, a ratificação, o adendo da Verdade, a F8.1), o quadro «O Teste da Única Palavra» (v397) intocado no topo; os parágrafos da v402 ficam (os nomes provisórios ganham nota ao lado).
- O que a v403 NÃO muda: o gate (letra do veredito), o piso dos vazios, o perfil, a seção do selo pela própria tecnologia (runtime da v401), o quadro do 4,44, o sidecar.

## 3. A cadeia (clone da v402, molde `work\cadeia_de_selo\v402`; cada passo é um script, nada à mão)

1. `delta_v403.py` (importa `delta_v402`; sobrescreve: SANDBOX `k403c`, BASE `base_v402` (cópia de bytes do Nós v402: um.py, selo, core, manifesto do kernel, pilar, sidecar), `UM_VERSION v403`, `BASE_SHA16_DA_ORDEM 6a5033dc3f29324c`, STONES = Caminho/Vida/VerdadeAdendo com `theorem`/`key_theorem`/`contract`/`support`, `pedras_sha16_da_ordem.json` lido das pedras de `v403_kernel\pedras`, prefixos de bandeira `ext_cam403_`/`ext_vid403_`/`ext_vad403_`).
2. `copiar_base_v403.py`; `preparar_kernel_v403.py gerar|conferir` (raiz + Audit gerados a partir dos embutidos da v402; já conferido à mão hoje: só os três imports); `construir_kernel_v403.sh` (feito hoje, incremental; o rito real compila a frio); `pos_build_kernel_v403.py` (recibo `KERNEL_RECIBO_R3_2`, FLAGS_v403, KH_N1_v403; zero sorry, trio, tokens proibidos 0).
3. `registros_v403.py` (`bandeiras_do_gate_v403`, `cunhagens_v403`, `caminho_v403`/`vida_v403`/`verdade_adendo_v403` que leem a composição e a estrela de cada módulo no kernel do rito), `gerar_candidato_v403.py` (patches determinísticos: kernel embutido + 3 módulos, F8.1 nos três pontos acima + kwarg + chamada + probe, registros, artigo PT/EN, `.md`, versão), `gerar_esperados_v403.py`, `p00_precondicoes_v403.py`, `ensaio_a_seco_v403.py` (unidades + guardas estáticas da Bancada), conferidor (`conferir_rito_v403.py`, controle negativo e positivo falso), `instalar_v403.py`, `rito_v403.sh` (`echo 1 | python um.py`, checkpoints), `pos_rito\` (fechar, textos, handoff, fila da memória, mapa), e então a custódia pelo G1 (`tools\custodiar.py planejar/executar --versao v403`).
4. Divisão do trabalho (gestão de tokens, 13/10): o clone mecânico dos scripts (1–3) vai a um subagente Sonnet com o molde da v402 e este plano, como na preparação da v402 («subagente de preparação»); a gerência c1 revisa, roda o ensaio a seco, instala e sela; o B(n) da Bancada é passo simples v402 → v403.

## 4. Gates e o que fica do operador

- Gate: a letra do veredito não muda; se uma bandeira calculada vier False, para-se e reporta-se (o número corrige a frase). NOT_FALSIFIED nunca é CONFIRMED.
- Do operador (não bloqueia a v403): ratificar D11–D13; [LEGAL] D2; Zenodo v402; nome do triplo inteiro (opcional).
