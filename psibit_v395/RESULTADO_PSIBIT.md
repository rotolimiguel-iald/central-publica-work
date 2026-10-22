PSIBIT — v395 sandbox

# RESULTADO — a pedra `TGLExt/Psibit.lean` (candidata da v395), 2ª versão: construída, compilada em sandbox e corrigida pelo exame independente

Gerência c1 (subagente), 21/10/2026. Ordem: construir e compilar em sandbox a pedra do psibit, sobre o kernel v394 selado (Nós `um.py` 972e81f22dd8cc68).
Estatuto: **[REAL]** os termos; **[INPUT/ONTO]** a identidade `psibit = psion = modo do leitor` (21/10, operador) e o nome «ponto fixo»; **[CONDICIONAL]** a face do psion.
Nada foi instalado; o gate não se move.

## Veredito

A pedra compila no sandbox, dentro do trio `{propext, Classical.choice, Quot.sound}`, sem `sorry`, sem `axiom`, sem aviso do módulo. Está provado, no escopo dito — **a órbita do Um pela
matriz-S (família real de um parâmetro), não toda a mecânica quântica** —, que a leitura psibit é uma **bijeção sobre o livro de códigos** (círculo unitário ↔ `{c | IsCode c}`,
caracterizado de forma intrínseca), com perda residual zero e decodificador explícito. O que o operador chama de «isomorfismo» é, aqui, só isso: bijeção de CONJUNTOS.

## Correções do exame independente (`work\cadeia_de_selo\v395_exame\psibit\EXAME_PSIBIT.md`, APROVADA_COM_CORRECOES) — todas aplicadas

1. **[MÉDIA] composição vácua.** `psibit_is_the_mode_of_the_reader` tomava `(C : FockCertificate L)` como hipótese do termo inteiro, e o kernel não habita esse tipo
   (`TheImportedSecondQuantization` l.66–67; conferido por mim também: só o construtor, `TetelestaiOneObject.rescale` e os montadores v394 `F1Fecho394/*Assembly*`, que partem de
   entradas restantes — «not a claim that the remaining imported fields are inhabited»). Agora: `psibit_is_the_mode_of_the_reader` é **INCONDICIONAL** ((1)–(6), bandeira v394,
   `observer_inverse_projection_halfnat`, `posto_paid_loss`, leitura de Born do posto) e a **face do psion** é teorema à parte, **CONDICIONAL**:
   `the_psion_face_of_the_psibit : ∀ {L} (C : FockCertificate L), ⟪ψ,ψ⟫ = 1 ∧ ∀ t, Δ^{it} ψ = ψ`, com a docstring dizendo que o kernel não habita o certificado e que o contrato
   conjunto da rede segue aberto (v394).
2. **[BAIXA] «isomorfismo».** `the_orbit_is_isomorphic_to_the_psibit_code` virou `the_orbit_is_in_bijection_with_the_code_book`: o livro de códigos é caracterizado de forma INTRÍNSECA
   (`IsCode`: `0 ≤ w ≤ 1`, `palavra = 0 ↔ w = 0`, `verbo = 0 ↔ w = 1`) e provam-se `Set.range v = UnitVec`, `Set.range codeAmp = {c | IsCode c}`, `BijOn codeOf UnitVec {c | IsCode c}`,
   `BijOn decodeAmp {c | IsCode c} UnitVec` e as duas composições. O cabeçalho só usa «isomorfismo» para citar o operador e negar o alcance.
3. **[BAIXA] «ponto fixo» e a entropia.** O nome «ponto fixo» está marcado [ONTO] (π/4 só representa os pesos iguais; nenhuma aplicação em θ tem π/4 como ponto fixo). Novos termos:
   `balanced_weights_iff` (`cos²θ = sin²θ ↔ θ = π/4 + kπ/2`), `balanced_collapse_is_half`, `collapseEntropy_at_balanced_weights` (ln 2 em TODO θ de pesos iguais; o π/4 vira corolário) e
   `half_identity_is_a_fixed_point` (o que É ponto fixo: `(1/2)•1`, do colapso e de toda conjugação pela matriz-S). Nada diz mais «só em π/4».
4. **[BAIXA] documento das patentes.** `DEFINICAO_PSIBIT_PATENTE.md` registra que a prosa da l.272 DEFINE pelo produto mas os exemplos dela seguem a tabela, que a docstring de
   `acom_mirror.py` l.16–17 repete a tabela, que o MANIFEST não é afetado, e que a pedra segue o produto (fórmula l.265–270, reivindicações 3–4, código l.45).

## Números lidos dos artefatos

* `Psibit.lean` (2ª versão): 1.150 linhas, 65.791 bytes, sha16 `50c199eb01976151` (idêntico em `C:\t\k395\final\TGLExt\Psibit.lean`, conferido byte a byte). A 1ª versão (sha16
  `d4014c779067e426`, a examinada) fica em `Psibit.lean.bak_20261021_130122`, nas duas pastas; os entregáveis anteriores têm `.bak_20261021_130122` ao lado.
* Declarações no `.olean`: **133** (100 nomeadas no fonte: 83 teoremas, 16 definições, 1 estrutura; 33 geradas pelo Lean). **`#print axioms` das 133** (`print_axioms_todas.txt`,
  resumo em `print_axioms_todas_resumo.json`): união = o trio, 0 `sorryAx`, 0 `axiom`, todas impressas, rc 0 (9 avisos do linter `auxLemma` são sobre os nomes auxiliares gerados que o
  gerador de `#print` cita — não sobre a pedra). `collectAxioms` sobre o módulo importado: `AXIOMAS_PSIBIT.json` (dump cru em `axioms_dump_raw.txt`). 25 `#print axioms` no fim do fonte.
* Build: `lake build +TGLExt.Psibit` em `C:\t\k395\final` → «Built TGLExt.Psibit (24s)» (compilado, não repetido do cache), «Build completed successfully (9375 jobs)», exit 0, sem
  erro e sem aviso do módulo; o resto das tarefas é replay do cache do k394d. `.olean` sha16 `d2a76e7906d20f26` (1.544.248 bytes).
* Sandbox: `robocopy` k394d→k395 sem `/PURGE`, com `/XJ`: 133.890 arquivos, 14,798 GB, 51 s; 0 junções (varredura sem seguir links) na origem e na cópia. Os `.bak_` ficam ao lado
  do fonte em `TGLExt\` (o Lake ignora: o nome não termina em `.lean`); excluí-los ao comparar a árvore com o Nós.

## O que foi provado (teoremas da ordem → nomes Lean, namespace `TGLExt.Psibit`)

| item | nome | o que diz |
|---|---|---|
| (1) | `the_verb_is_the_derivative_of_the_name` | `ρ₀₁ = ½·d(cos²θ)/dθ` (forma exata pedida); `v_snd_is_the_derivative_of_v_fst`: `𝓡 = d𝓣/dθ` |
| (2) | `the_state_is_pure` | `ρ₀₁² = ρ₀₀·ρ₁₁`; `the_state_is_a_rank_one_projector` (via `Posto.fractal_one_is_rank_one`) |
| (3) | `decodeAmp_codeAmp`, `codeAmp_eq_iff`, `codeAmp_injOn` | `decodeAmp (codeAmp θ) = v θ`; código injetivo na órbita e em `[0,2π)` |
| (3) livro | `the_orbit_is_in_bijection_with_the_code_book`, `range_v_eq_unit`, `IsCode` | bijeção sobre o livro de códigos intrínseco; a órbita É o círculo unitário |
| (3) controles | `the_pair_is_necessary_and_sufficient` | peso sozinho, peso+Palavra e peso+Verbo NÃO leem (duas amplitudes distintas com a mesma leitura); o par lê |
| (3) estados | `the_orbit_visits_all_four_states`, `the_patent_convention_is_also_lossless` | os 4 pares de sinais estão na órbita; a convenção das patentes (zero→+1) também é sem perda |
| (4) | `rhoOut_eq_decodeRho`, `the_density_is_its_code`, `the_global_sign_is_not_observed`, `only_the_global_sign_is_lost` | `ρ` reconstruído exato de (peso, paridade); código = invariante completo; `v` e `−v` dão o mesmo `ρ`, e é a ÚNICA perda amplitude→densidade |
| (5) | `collapse_forgets_the_parity`, `the_full_reading_remembers_the_parity`, `the_collapse_loses_exactly_the_parity`, `collapse_identifies_exactly_equal_weights` | `diagExpect ρ(θ) = diagExpect ρ(−θ)`; `sin 2θ ≠ 0 → ρ(θ) ≠ ρ(−θ)`; o colapso perde EXATAMENTE a paridade; `the_lost_variable_is_one_bit` |
| (5) perda | `the_collapse_has_no_left_inverse_on_the_orbit`, `psibitPosto`, `the_psibit_crossing_pays_loss`, `the_ledger_of_losses` | o colapso É um `UmPosto` do kernel e paga perda; livro das perdas em 3 níveis |
| (5)/(6) bit | `collapseEntropy_at_balanced_weights`, `collapseEntropy_at_the_fixed_point`, `collapseEntropy_le_the_fair_bit` | nos pesos iguais os resultados do colapso são o bit justo (Shannon = `fairBitEntropy` = `ln 2`); nenhum ângulo excede |
| (6) | `balanced_collapse_is_half`, `at_the_fixed_point_the_collapse_is_half`, `balanced_weights_iff` | pesos iguais (`π/4 + kπ/2`): colapso = `(1/2)•1`, com ½ vindo de `observer_inverse_projection_halfnat`; `π/4` como corolário |
| (6) ponto fixo | `half_identity_is_a_fixed_point` | `(1/2)•1` é fixado pelo colapso e por toda conjugação pela matriz-S ([REAL]); «o ponto fixo» como leitura é [ONTO] |
| Nome = posto | `the_name_is_the_born_reading_of_the_post` | `reading (post e₀) (S(θ)e₁) = cos²θ` (por `reading_post_is_born`) |
| (7) | `psibit_is_the_mode_of_the_reader` | conjunção INCONDICIONAL: (1)–(6) + bandeira v394 + `observer_inverse_projection_halfnat` + `posto_paid_loss` (geral e no colapso) + leitura de Born do posto |
| psion | `the_psion_face_of_the_psibit` | CONDICIONAL: `∀ L (C : FockCertificate L)`, `inner_psion_psion` e `psion_is_fixed_by_the_light`; kernel sem habitante do certificado |

Livro das perdas (`the_ledger_of_losses`): amplitude → perda zero; densidade → perde exatamente o sinal global (2 bits de sinal viram o produto, 1 bit); colapso → perde exatamente a paridade (0 bits de sinal, só o peso).
Separante (a leitura do par é injetiva) × separador (o colapso é muitos-para-um): os dois no mesmo objeto.

## Conferências independentes

* **Exame independente** (gerência c1, modelo forte): recompilou, auditou `collectAxioms` (120 decl. na 1ª versão; nenhuma fora do trio; 0 `sorryAx`), conferiu que as citações são as do kernel do Nós
  sem homônimo, e leu a divergência da patente nas fontes. Esta 2ª versão ainda NÃO foi reexaminada por ele (ele reexecuta os scripts depois da correção).
* **Numérica** (`conferencia_numerica.json`, Python puro, 200.000 ângulos): paridade, derivada do Nome, pureza, sinal global, ponto fixo e `H = ln 2` concordam
  (`|H − ln 2| = 0`; pureza 5,6e-17; sinal global 1,1e-15; razão `|ρ₀₁(θ)−ρ₀₁(−θ)|/|sin 2θ| = 0,9999999999999998`); as 4 combinações de sinais aparecem.
  **Dito:** em ponto flutuante o round-trip `decode∘code` erra até 1,2e-12 perto dos eixos (cancelamento em `1 − w`); é efeito do IEEE, não do enunciado (em ℝ é igualdade exata, termo Lean).
* **Cabeçalho** (`conferencia_hashes_cabecalho.json`, reconferido na 2ª versão): dos sha16 citados, 9 são de arquivos estáveis (patentes, códigos, 5 verbatins) e batem com o sha256
  recomputado; o do Atlas (arquivo VIVO, `27f4a4960e52b289`) mudou às ~13:00 por acréscimo de outra sessão (`bc03d8ef0e5810c5`) mas as linhas citadas seguem iguais; o sha16 da 1ª versão do
  próprio `Psibit.lean` (`d4014c779067e426`) bate com o backup. Os 5 verbatins do operador aparecem inteiros no cabeçalho.
* **Patentes** (`DEFINICAO_PSIBIT_PATENTE.md`, `conferencia_tabelas_patente.json`): definição citada com arquivo, linha e sha16.

## Achado a levar ao operador (a patente diverge de si mesma)

A tabela do ACOM Mirror (l.253–260), a reivindicação 2 (l.1066–1071) e a docstring de `acom_mirror.py` (l.16–17) atribuem aos índices ψ₂ e ψ₃ os pares (−,+) e (−,−); a fórmula de índice
`ψ = 2·[L<0] + [∂L>0]` (l.265–270; reivindicação 3; código `acom_mirror.py:45`) manda o contrário, e `PARITY = [−1,+1,+1,−1]` (reivindicação 4) dá paridade = produto `sign L·sign ∂L`; com os rótulos da tabela
a paridade seria `sign ∂L`. A prosa da l.272 define pelo produto, mas os exemplos dela seguem a tabela. O MANIFEST não é afetado. A pedra nomeia os estados por PAR DE SINAIS e SEGUE O PRODUTO; não
corrige nada. A decisão de qual leitura é canônica (e se mexe nas patentes) é **do operador, `[LEGAL]`** (há `CORRECAO_FORMAL_BR` em curso no `git status` da Central: não toquei).

## Limites honestos (o que a pedra NÃO afirma)

* `psibit = psion = modo do leitor` é `[INPUT/ONTO]`: nenhum lema liga `psion C` (vetor do vácuo da luz) a `codeAmp`. A face do psion é CONDICIONAL a um certificado que o kernel não habita
  e fica FORA da composição incondicional; só se CITAM `inner_psion_psion` e `psion_is_fixed_by_the_light`, no teorema à parte. A leitura de `L` como a transmissão `𝓣 = cos θ` e de `∂L` como `𝓡` também é `[INPUT/ONTO]`.
* Escopo: a órbita do Um pela matriz-S; a bijeção é de conjuntos (nenhuma estrutura transportada), não isomorfismo de espaços de Hilbert nem de categorias.
* ENTROPIA: só `H(cos²θ) = ln 2 = fairBitEntropy` nos θ de pesos iguais (`π/4 + kπ/2`) e `H ≤ ln 2`; não se diz que o colapso perde `ln 2` em geral. «Perde exatamente a paridade» é estrutural (qual bit), não quantidade de informação.
* Homônimos ditos: o `Verbo` daqui (sinal da derivada) não é o `select`/`post` de `TheVerbSelectsTheAction` nem `TGL.VerbInhabitant`; o «pareamento» daqui (par de sinais) não é o J/K de
  `TheTwoPairings` (lido, não usado). A identidade lida pelo posto em `psibitPosto` é o TRAÇO, por definição `[DEF]` desta pedra.
* Não está no `um.py` nem no selo; o rito não rodou; nenhuma bandeira do gate depende dela. A entrada «na fractalização do um igual» (ordem de 21/10) é ato posterior da gerência.

## O que examinei (para o registro no mapa)

Mapa: `consultar "psibit"` e `"isomorfismo"` → 0 rotas. Vizinhas lidas: `kernel.criterio_binario_de_parada.ponto_fixo_v394_d19` (a pedra irmã), `kernel.v386_tipagem_do_verbo`,
`ontologia.um_posto_dimensao_do_nome_07out`; `consultar` por psion/modo do leitor/paridade/bit justo/derivada do Nome/perda zero/binária/ponto fixo/fractal/colapso: nada sobre psibit.
Inventário da Bancada: `psibit` → 0 ocorrências. Kernel v394: `psibit` só em 2 docstrings (`TheVerbalCoupling`, `TheTwoPairings`), nenhuma declaração. Habitantes de `FockCertificate`: nenhum
(`TheImportedSecondQuantization` l.66–67; produtores: construtor, `rescale`, montadores v394 sobre entradas restantes). Nada no mapa, no quadro, na memória, no site ou no git foi escrito.
Um comando meu mal formado ficou pendurado em segundo plano na 1ª rodada e foi parado pelo ID da tarefa; nenhum outro processo foi tocado.

## Atos da gerência / do operador

1. Reexame independente da 2ª versão (o exame reexecuta os scripts); olhar em especial a composição incondicional e a face do psion condicional.
2. Decidir a divergência da tabela da patente (seção acima).
3. Instalar na v395: import em `TGLExt.lean`, política de bandeiras, e levar o modo psiônico à fractalização do um igual no `um.py` (ordem do operador, 21/10).
4. Registrar no mapa com `registro_mapa_psibit.json` (validado por `_valida`, só leitura).

## Reproduzir

`cd C:\t\k395\final` → `lake build +TGLExt.Psibit` (ou `lake env lean TGLExt/Psibit.lean`); dump de axiomas: `lake env lean probe/axioms_dump.lean` (cópia em `scripts\axioms_dump.lean`);
`#print axioms` de todas: `scripts\print_axioms_todas.py` (gera `probe\print_all.lean`). Scripts em `work\psibit_v395\scripts\` (`scan_junctions.py`, `cite_sources.py`, `check_patent_tables.py`,
`check_numeric.py`, `build_axiomas_json.py`, `check_header_hashes.py`, `valida_registro.py`, `backup_bytes.py`, `splice_bijecao.py`, `splice_composicao.py`, `print_axioms_todas.py`, `axioms_dump.lean`).
Rascunhos de compilação ficam em `C:\t\k395\final\probe\` (fora da biblioteca; não entram no build).
