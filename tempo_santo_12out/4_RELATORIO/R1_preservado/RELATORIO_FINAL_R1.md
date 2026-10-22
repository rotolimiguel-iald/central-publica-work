# F1.TEMPO — o tempo que não se deixa nomear: relatório final

**Unidade:** F1.TEMPO (trilha TEMPO) da gerência c1, programa IALD (a TGL). Workflow posto-e-tempo.
**Data:** 12/10/2026. **Autor:** o redator da unidade, subagente do workflow. Escrevi só em `4_RELATORIO`.
**Para:** Luiz (o operador) e a gerência c1.
**Estatuto do documento:** [REAL] onde cito número ou teorema conferido por script ou recompilado pelos auditores; [INPUT da gerência] onde há escolha de protocolo; [KNOWN] onde há citação de literatura; [ONTO] onde há leitura ontológica. Este relatório **não dá veredito global**. A regra congelada não permite.

> **Como ler um PASSA.** Um PASSA é validade matemática na face testada: a face finita do kernel, num sandbox, e um modelo ótico sintético. A recusa da régua é da creditação, não da validade (o operador, 07/10, verbatim `5dffde4644139da5`). Nada aqui move o gate. β na natureza a 5σ não é tocado. Nenhum dado observado foi usado.

---

## 0. Resumo para o Luiz

1. **O que se testou.** Testei a segunda parte do seu texto de 12/10, de «O que mais me fascina…» até o fim. A gerência a dividiu em 23 frases e 11 afirmações com forma matemática (T1–T11), com controles e sondas fixados antes por hash. Cada afirmação foi ensaiada em duas faces: o kernel, com uma pedra candidata em sandbox, sem tocar o Nós; e o modelo ótico sintético, com β lido em runtime dos bytes do um.py. Depois, dois auditores independentes refizeram tudo: um reproduziu, o outro conferiu estatuto e regra.

2. **O que deu (tabela na §2).**
   - **PASSA** na face finita (kernel e ótico): T1, T3, T4, T5, T6, T7, T8, T10 e T11.
   - **T2** (Pauli em dimensão infinita) fica **CITADA** [KNOWN], como pré-registrado. O kernel não tem o teorema e nunca teve.
   - **T9** («o tempo não tem posto») fica **FALHA** pela regra congelada. Os cinco subitens de kernel passam. A falha está num único critério numérico do modelo ótico: a tolerância de 1e−13 ficou abaixo do piso de arredondamento do float64. Não é contraexemplo; a identidade é exata, e o kernel a prova.
   - O **ciclo limite** segue **ABERTO** [OPEN].

3. **O que o número põe ao lado das suas frases** (o seu texto fica como está; a correção vai ao lado):
   - **Liouville proíbe a bacia, não o pouso.** Um boost de determinante 1, que é simplético e hamiltoniano, faz uma trajetória pousar: na direção nula passada, B(s)ᵏ(1, −1) → 0. O que o volume conservado proíbe é um atrator com volume (T4.e, T4.f; sonda AUD-8).
   - **O conjunto fixo da defasagem pura é a diagonal inteira, não um ponto.** Toda a diagonal fica fixa, e cada estado pousa na sua própria diagonal (T5.b). Ponto único só sob hipótese nomeada (F1.ATRATOR, A4).
   - **«Repousar» e «ser lembrada» não cabem no mesmo estado** na face finita. O relógio modular só para se as populações forem iguais (T11). Populações distintas, que são a memória, fazem o relógio girar (sonda AUD-7).
   - **Pauli vale na forma de Weyl** (covariância), não na de Heisenberg. Na forma de Heisenberg há contraexemplo (Galapon 2002) [KNOWN].
   - **«Defasar» tem dois sentidos que não se encadeiam.** Sob a sua fórmula de 05/10, V(t) = e^{−iHt}V(0)e^{iHt}, a fase gira e nada se perde. A seta só nasce no semigrupo dissipativo (T6, T7). Por isso «Nome = lim V(t)», com a fórmula unitária, só converge se V(0) já for fixo (T4.b).

4. **A pedra não entra no um.py como está.** O nome provisório é `TheTimeHasNoRank`.
   - Ela atribui a você três frases que você não escreveu:
     - «o tempo é o Verbo»;
     - «O tempo é o Verbo, não o Nome»;
     - «o atrator é onde o tempo repousa».
   - O título «o relógio mede a sombra» troca o seu verbo «registra».
   - Pelo seu texto de 05/10, o Verbo é «um operador de projeção», e o tempo é «a defasagem do verbo» e «o parâmetro da transmissão».
   - Três nomes afirmam mais do que o termo prova.
   - O cabeçalho estende a regra dos dois regimes além do cânone.
   - Corrigir isso muda o hash da pedra e pede nova compilação e nova auditoria.

5. **A unidade não pode fechar ainda** (§9). Falta pouco e é concreto:
   - a pedra corrigida e reauditada;
   - a decisão da gerência sobre T9: registrar a FALHA como resultado, ou um ADENDO uniforme congelado antes de reensaiar;
   - as erratas ao lado;
   - o seu resíduo: o nome da pedra e as leituras (§8).

---

## 1. O que foi testado e como

| etapa | onde | hash (sha256, lido por script) |
|---|---|---|
| texto do operador de 12/10 (verbatim) | `work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt` | `2c8b7b712aa9ad7f…` (6.673 B). Segunda parte: byte 2853, 3.820 B, `6dcefdbe5c6a7752…` |
| levantamento | `0_LEVANTAMENTO\LEVANTAMENTO.md` | `6508945d7d57ad44…` |
| pré-registro congelado | `1_PREREGISTRO\FREEZE.json` (2026-10-12T16:09:07Z) | FREEZE `6b29d4c9b09e5553…`; PREREGISTRO.json `64b1c38637befddf…`; PREREGISTRO.md `0261dc06a5fe513b…` |
| face ótica | `2_OPTICO\RESULTADO_OPTICO.json` (tentativa 003, runner `fcc289889ec418ba…`) | `2c67b7ea6f118630…`; achados `a4549cd9ecbd4743…`; diagnóstico T9c `26a68eff64aeb7e4…` |
| face kernel | `3_KERNEL\RESULTADO_KERNEL.json`; pedra `3_KERNEL\sandbox\TheTimeHasNoRank.lean` | resultado `5a56eab2ce56ddaa…`; pedra `7105eda468b60309…` (97.656 B); .olean `9f473a088262b073…` |
| auditoria de reprodução | cópia de bytes em `4_RELATORIO\AUDITORIAS\TEMPO_AUD_REPRO` | manifesto da cópia em `AUDITORIAS\MANIFESTO_COPIA_AUDITORIAS.json` (71 arquivos idênticos) |
| auditoria de estatuto | cópia de bytes em `4_RELATORIO\AUDITORIAS\TEMPO_AUD_ESTATUTO` | idem |

**Conferências deste redator, todas por script** (`4_RELATORIO\saidas\`):
- **FREEZE.** Os 30 itens congelados batem por sha256 e tamanho. A pasta `1_PREREGISTRO` tem exatamente os arquivos esperados. Todos os arquivos de `2_OPTICO` (31) e de `3_KERNEL` (51) são posteriores ao freeze, com folga mínima de 269,0 s e 229,1 s (`CONFERENCIA_HASHES.json`). [REAL]
- **Trechos.** 20 trechos citados neste relatório foram achados nos bytes, com linha (`CONFERENCIA_HASHES.json → trechos`): o texto de 12/10, o verbatim do Verbo de 05/10, as linhas da pedra, o índice da memória e as docstrings do kernel. [REAL]
- **β em runtime.** O literal de `ALPHA_FINE_CODATA_2018` foi lido na l.5557 do um.py v391 (`8e7b9927ceae64b8…`, não executado). Ele é igual a `SEALED_CODATA_ALPHA` da l.95, a atribuição de topo. A l.5557 fica **dentro** do texto embutido `_NIVEL2_MCMC_FILES` (l.5511–6027). β = α·1·√e = 0,012031300400803142, com Δ = 0,0 contra a conferência lida do PREREGISTRO.json (`BETA_RUNTIME_RELATORIO.json`). [DERIVED: lido e calculado, não medido]
- **Kernel.** A impressão digital do tgl_kernel foi tomada antes e depois deste relatório (meta `b1b47447…`, src `911cb40b…`, 132.088 arquivos; `FINGERPRINT_RELATORIO_ANTES/DEPOIS.json`). Não compilei Lean e não copiei toolchain. [REAL]
- **Mapa e memória.**
  - Mapa de rotas: só `consultar`, `ver` e `modelo`. O livro (`29b8607006fe8a2a…`) ficou igual antes e depois (`saidas\rotas\RESUMO_CONSULTAS.json`).
  - ACOM: só projeção de leitura da referência c1 (revisão 2, estado `a5f688df…`). A resposta é byte a byte igual à dos construtores (`b0161de2…`), e o banco não mudou (`saidas\ACOM_RECIBO_PROJECAO_RELATORIO.json`). Não fiz init nem transition: a tarefa proíbe escrever fora desta pasta.

**O modelo ótico** [INPUT da gerência; identidades DERIVED]:
- S = Smat(θ_M), com sen²θ_M = β.
- C = D∘Ad(S)∘D. Nas populações, T = R + λ(I − R), com R = J/2 e λ = 1 − 2β.
- Estado de uma travessia ρ₁ = diag(1−β, β). Taxa de Davies g₀₁ = β·ω₁.
- Semente 20261012. É sintético: nenhuma identidade dele é evidência sobre a natureza.

---

## 2. Tabela por afirmação

Legenda da regra congelada (PREREGISTRO.md §8):
- **PASSA** exige todos os subitens obrigatórios de kernel e ótico em PASSA, e todos os controles ligados comportando-se como registrado.
- **FALHA** basta um subitem obrigatório em FALHA.
- **CITADA** e **LEITURA** nunca recebem PASSA de teste.
- **ABERTA** é o que fica [OPEN].

| | afirmação (forma testada) | pré-registrado | face ótica | face kernel (pedra candidata, sandbox) | auditoria de reprodução | auditoria de estatuto | **veredito final** |
|---|---|---|---|---|---|---|---|
| **T1** | não há operador de tempo em dimensão finita: TH − HT ≠ c·1 (c ≠ 0); forma de Weyl V⁻¹HV ≠ H + s·1 | PASSA | PASSA: \|tr[T,H]\| ≤ 2,3e−15; o mínimo de ‖TH−HT−i·1‖ é √n em 1.200 pares (desvio ≤ 4,4e−16) | PASSA (T1.a, T1.c; T1.b opcional PASSA); C-T1-a/b/c como registrado | confere (refaz bit a bit) | PASSA; ressalva: existem operadores de tempo *cíclicos* em dimensão finita (Pegg 1998, a conferir) | **PASSA** |
| **T2** | teorema de Pauli em dimensão infinita | CITADA (+T2.b opcional) | sem face ótica | T2.b PASSA (álgebra de Banach; não é Pauli) | confere; sonda A3: «não trivial» pesa | CITADA; nunca escrever «T2 PASSA» | **CITADA** (T2.b PASSA, opcional) |
| **T3** | o fluxo modular σ_t = Ad(ρ^{it}) é grupo de *-automorfismos; o estado é KMS; setor fixo = centralizador | PASSA | PASSA: lei de grupo 2,8e−15; KMS 1,4e−15; ω₁ = 4,4081393960414665; C-T3-a/b/c como registrado | PASSA (T3.a; T3.b por re-exportação de tipo idêntico) | confere; T3.b(iii) sem habitante exibido (V-GERAL-1) | PASSA; o nome `time_is_the_modular_flow` afirma o tempo térmico | **PASSA**, com ressalva em T3.b(iii) (§7) |
| **T4** | Liouville × dissipação: sob isometria nada pousa; volume conservado não impede pouso; bacia exige perda de volume | PASSA | PASSA: M_N ≥ 1 (≈ 1,41420); det T − (1−2β) = 2,2e−16; boost em decimal de 200 dígitos, rel 2e−197 | PASSA (T4.a–e; T4.f opcional PASSA; T4.b(iii) opcional e condicional, ver §7) | confere; A7: a separação métrica pesa | PASSA, com a correção de Liouville visível (AUD-2, AUD-8) | **PASSA** |
| **T5** | o conjunto fixo da defasagem pura é a diagonal inteira, não um ponto: dois estados fixos distintos | PASSA + CITADA | sem face ótica | PASSA (T5.a, T5.b); T5.c CITADA (F1.ATRATOR, A4) | confere; A4: i₀ ≠ j₀ pesa | PASSA; T5.c CITADA | **PASSA** (T5.c CITADA) |
| **T6** | a seta pela pureza: Σ\|(T_t x)ᵢⱼ\|² = Σ e^{−2tgᵢⱼ}\|xᵢⱼ\|²; cai estritamente com coerência; constante sob unitária | PASSA | PASSA: fórmula ≤ 2,2e−16; Tr(T₁ψ₊)² = 0,9496802613377202; C-T6-a/b/c como registrado | PASSA (T6.a–d) | confere; B3: `_hd` sem peso | PASSA | **PASSA** |
| **T7** | o inverso T₋ₜ existe mas não é positivo | PASSA | PASSA: λ_min = −0,006052 (γt = β), −0,85914 (1), −11012,73 (10); Davies −0,027234 | PASSA (T7.a, T7.b); C-T7-a/b/c como registrado | confere; A5: γ > 0 pesa | PASSA | **PASSA** |
| **T8** | a coerência do dephasing é instância da `DualScalingData` e herda as seis cláusulas da Ágape; o registro não escala | PASSA + LEITURA | PASSA: \|c_k − λᵏ\| ≤ 2,2e−15 (k ≤ 10⁴); k_ε = 95, 284, 568 | PASSA (T8.a–d); docstring citada em T8.d trocada (AF-01) | confere | PASSA + LEITURA; ponte de conteúdo mínimo (AUD-1) | **PASSA + LEITURA** |
| **T9** | F(t) = P + e^{−t}(1−P) é invertível e só é idempotente em t = 0; o posto só no limite | PASSA + LEITURA | **FALHA** em T9.o(c), entradas: 6,518e−13 > 1e−13 (k = 10⁴); 22 de 23 critérios ok | PASSA (T9.a, b, c, e; T9.d opcional PASSA) | confere, inclusive a FALHA: piso de representação k\|δ\|/2 | FALHA por afirmação; leitura T9.t atribuída ao operador sem verbatim; nome contradiz `flow_full_rank` | **FALHA** (só pelo critério numérico; subitens de kernel PASSA) |
| **T10** | o relógio lê t módulo P (κP = ±2π); o ângulo não tem limite; a face distingue instantes; o posto, Ω e ω não se movem | PASSA + LEITURA | PASSA: periodicidade 1,3e−15; \|σ_t(x)ᵢⱼ\| = \|xᵢⱼ\| a 8,9e−16; relógio da face injetivo | PASSA (T10.a–e) | confere; B1: κ ≠ 0 sem peso no enunciado | PASSA + LEITURA; o título troca «registra» por «mede» | **PASSA + LEITURA** |
| **T11** | no atrator tracial ½·1 = absoluteRho(Fin 2) o relógio modular para; ω_k = 2·artanh(λᵏ) → 0 | PASSA | PASSA: ω_k = 4,40814 / 2,11043 / 0,175525 / 5,28e−11 (k = 1, 10, 100, 1000); C-T11-a como registrado | PASSA (T11.a) | confere | PASSA, só face finita; ao longo do canal, só no limite (ω_k > 0 para todo k finito); nome sem canal no enunciado | **PASSA** (face finita) |
| **S46.3** | «ou um ciclo limite» | ABERTA | — | — | — | ABERTA | **ABERTA** [OPEN] |

Controles: os **22** se comportaram como registrado. Os 10 óticos foram reproduzidos pelo auditor, e as 18 declarações de controle do kernel compilam. A metade de kernel do C-T3-b repousa na re-exportação sem habitante (§7).
Sondas: as 13 por subitem compilam, e V-GERAL-2 compila (20 nomes re-exportam 19 termos, todos de tipo idêntico). **V-GERAL-1 ficou incompleta** em três declarações (§7).

---

## 3. O que é o quê

### 3.1 Teorema de kernel agora: [REAL] no sandbox, pedra candidata NÃO instalada

A pedra `TGLExt.TheTimeHasNoRank` (fonte `7105eda4…`) compila em Lean 4.31.0, com LEAN_PATH só de leitura no `.lake` do Nós. Dados da compilação:
- EXIT 0;
- 127 declarações com `#print axioms`, todas no trio {propext, Classical.choice, Quot.sound}; `post_not_isUnit` não depende de axioma algum;
- 0 sorry, 0 aviso, 0 erro, nenhum `native_decide`;
- .olean idêntico byte a byte nas duas auditorias.

As 127 declarações **não são 127 teoremas**: cerca de 20 são re-exportações e cerca de 25 são sondas, controles ou definições. É matemática conhecida, agora tipada nos objetos da casa (`dephase`, `sigma`, `axiomFlow`, `DualScalingData`). Nenhuma física entra, e β não entra no Lean.

Formas novas na casa:
- **Tempo sem matriz** (T1, T2.b):
  - `no_time_matrix` e `no_time_matrix_fin`: em dimensão finita não vazia, [T,H] ≠ c·1 para c ≠ 0, pelo traço;
  - `commutator_far_from_scalar`: ‖[T,H] − c·1‖² = ‖[T,H]‖² + |ι|·|c|²;
  - `no_finite_spectral_translation`: forma de Weyl;
  - `no_bounded_spectral_translation`: Banach, espectro compacto, **não** é Pauli.
- **Os três comportamentos** (T4):
  - `isometry_orbit_converges_only_if_fixed` e `isometric_flow_converges_only_if_fixed`;
  - `unitary_conj_isometry`, `modular_flow_is_isometry` (para todo ρ) e `modular_orbit_converges_iff_diagonal`;
  - `schurDiag`, `dephase_volume`, `dephase_volume_lt_one` e `modular_volume_one`;
  - `volume_kept_yet_lands`: o boost tem det 1 e pousa;
  - `global_attractor_needs_volume_loss`: Liouville linear.
- **A face fixa** (T5): `dephase_fixed_states_not_unique`.
- **A seta** (T6, T7):
  - `purityR_dephase`: a fórmula exata;
  - `purityR_dephase_lt`: a queda estrita;
  - `purityR_sigma`;
  - `dephase_inverse`;
  - `inverse_dephasing_not_positive`.
- **A Ágape na coerência** (T8): `coherenceScaling`, `the_coherence_obeys_agape` e `the_record_does_not_scale`.
- **O fluxo e o posto** (T9):
  - `flow_isIdempotentElem_iff`, `flow_isUnit` e `post_not_isUnit`;
  - `no_finite_instant_is_the_post`;
  - `flow_full_rank` (posto pleno) e `post_rank_lt`.
- **O relógio** (T10): `clock_reads_modulo_period`, `frozen_clock_not_faithful`, `face_clock_has_no_period` e `modular_clock_rotates_without_shrinking`.
- **O atrator tracial** (T11): `optical_attractor_is_the_absolute_one` e `optical_attractor_clock_stops`.
- **Duas cláusulas compostas**, só conjunção: `the_time_has_no_rank` e `the_two_regimes_of_time`.

**Condicionais, sem habitante exibido** (§7):
- `nontracial_state_rejects_the_identity_flow` exige uma testemunha AQFT W com A e B na cunha direita e contraste;
- `light_flow_group` e `light_modular_orbit_converges_iff_post` exigem um `FockCertificate`.

### 3.2 Número de runtime: [REAL] medido no modelo sintético; identidades [DERIVED]

Todos os números abaixo saem de β calculado em runtime a partir dos bytes do um.py. Nenhum é dado da natureza.

| grandeza | valor |
|---|---|
| λ = 1 − 2β = det T | 0,9759373991983937 |
| ω₁ = ln((1−β)/β) | 4,4081393960414665; período modular P₁ = 1,4253599404823543 |
| g₀₁ = β·ω₁ | 0,05303564928238982 |
| e^{−2g₀₁} | 0,8993605226754405 |
| Tr(T₁ψ₊)² | 0,9496802613377202 |
| λ_min de T₋ₜψ₊ | os quatro valores da tabela (T7) |
| k_ε | 95, 284 e 568 |
| ω_k | ω₁₀₀₀ = 5,284e−11 |
| M_N | ≈ 1,41420 |
| ‖B(1)¹⁰⁰(1,−1)‖ | 5,26098189834699494e−44 |

O auditor refez com mpmath a 50 dígitos e com construção própria (`AUDITORIAS\TEMPO_AUD_REPRO\saidas\A4_CALCULO_INDEPENDENTE.json`). Em k = 1000, ω₁₀₀₀ exato = 5,2843436040175e−11 contra o medido 5,2843174280781e−11: diferença de 2,6e−16, que é o piso do float.

**Sombras numéricas, não zeros** [informativo, RP18]: o posto numérico de Tᵏ cai a 1 em k = 1135, e o contraste fica abaixo de 1e−15 em k = 1441. O kernel decide que F(t) é invertível e que a coerência nunca zera em tempo finito: T9.b e T8.b(iv).

**A face ótica não conta como segunda evidência nem como rito.** Ela checa numericamente identidades que o kernel prova. O PASSA dela é consistência numérica (auditoria de estatuto).

### 3.3 [KNOWN] por citação: literatura, não teste

- **Pauli, forma de Weyl/covariância.** W. Pauli, *Handbuch der Physik* 24/1 (1933), nota na p. 140, e vol. V/1 (1958), p. 60, **páginas a conferir na fonte**.
- **Precisão na forma de Heisenberg:** E. A. Galapon, Proc. R. Soc. A 458 (2002) 451.
- **POVM covariantes:** Holevo (1982); Busch, Grabowski e Lahti, Phys. Lett. A 191 (1994) 357.
- **Operadores limitados:** Wintner (1947) e Wielandt (1949).
- **O tempo modular dilata a energia positiva** em vez de transladá-la: Borchers (1992).
- **Liouville clássico.** Em sistemas hamiltonianos não há equilíbrio assintoticamente estável; há centros estáveis no sentido de Lyapunov (elípticos), que giram sem pousar.
- **Hipótese do tempo térmico:** Connes e Rovelli, Class. Quantum Grav. 11 (1994) 2899. É **hipótese**, não teorema.
- **Exterioridade do fluxo em III₁**, com T(M) = {0}: Connes (1973).
- **Lei de escala de Takesaki** (1973), que entra como dado da `DualScalingData`.
- **Landauer** (1961) e **Bennett** (1982).
- **O segundo do SI** pela transição hiperfina do ¹³³Cs (BIPM, 2019).
- ***Kadosh***: BDB, HALOT; R. Otto, *Das Heilige* (1917); A. J. Heschel, *The Sabbath* (1951). A glosa «separado» é tradicional e debatida: [KNOWN com ressalva].
- **Operadores de tempo cíclicos em dimensão finita:** D. T. Pegg, Phys. Rev. A 58 (1998) 4307, **a conferir na fonte**. Eles leem o tempo módulo um período, o que reforça T10.
- **Resultados de unidades anteriores, citados e não refeitos:** F1.ATRATOR A4 (`RESULTADO_F1_ATRATOR_R1.json`, `6d7dc60c26d4fc78…`) e o atrator único GKLS v384, 672/672 [COMPUTED].

### 3.4 [ONTO]: leituras do operador, sem teste, marcadas como tais

- «santo» como nome do tempo (*Kadosh*: separado, irredutível, não profanável pela posse);
- «o agora permanece intocado»: a forma [REAL] é T10.e (o posto, Ω e ω não se movem); a identificação agora = conjunto fixo é leitura (R12);
- «O relógio registra a sombra do evento»: a forma [REAL] é o quociente módulo P (T10.b);
- «puro amor», «a física da doação fundamental», «generosidade contínua», «assinatura indelével» e «prova viva»;
- «ato contínuo da criação… redenção», «chão firme… do espaço inscritível», «intervalo sagrado» e «fotografia estática e morta»;
- «um lugar onde repousar e ser lembrada»;
- «o tempo não é uma peça do tabuleiro»;
- «Santo é aquilo que não se deixa colonizar pelo intelecto».

Há ainda uma leitura que **não é sua**, embora a gerência a tenha anotado como sua: «o tempo é o Verbo, não o Nome». Ela é leitura da gerência e precisa ser **corrigida**, não só marcada (§5, achado M2).

---

## 4. As sondas honestas, em poucas frases

- **Controles que tinham de falhar** (22). Todos falharam onde deviam:
  - **C-T4-a, o boost.** Ele conserva volume (det 1) e pousa no raio nulo passado. É a sonda que mais pesa contra a leitura literal de Liouville.
  - **C-T5-a.** Dois estados fixos distintos mostram que «o atrator é um ponto» é falso para a defasagem pura.
  - **C-T6-c.** Para t < 0, a pureza **cresce**: (1 + e²)/2 ≈ 4,19 > 1. A seta tem sentido.
  - **C-T7-c.** A unitária é reversível como canal; só a dissipação não é.
  - **C-T3-a.** Com a temperatura errada, a KMS falha em 200 de 200 pares (gap mediano 53,6).
  - **C-T11-a.** Fora do atrator, o relógio modular não para (|σ_{π/ω₁}(E₀₁)₀₁ − 1| = 2).
- **Sondas do auditor de reprodução** (15, no trio). Há três famílias:
  - **A, «cada hipótese pesa»:** sem a idempotência, o «se e só se» do T9.a cai (P = 2, F = 0 em t = −ln 2); sem «não trivial», T2.b vale trivialmente; em Fin 1 há um único estado; com γ = 0, o inverso é positivo; em t = 0 não há queda; num espaço só pseudométrico, a troca é isometria e a órbita converge a um ponto não fixo.
  - **B, «hipótese sem peso»:** κ ≠ 0 em `clock_reads_modulo_period` (em κ = 0, o x/0 = 0 do Lean torna a igualdade trivial); a idempotência em `no_finite_instant_is_the_post`; e `_hd` em `purityR_modular`.
  - **C:** as negações de T1, T9.a, T7.b, T4.b(ii) e T6.c são refutadas.
  
  As 6 tentativas diretas de provar o contrário falham, como tinham de falhar.
- **Sondas do auditor de estatuto** (AUD-1 a AUD-8, no trio). Elas medem o peso dos nomes:
  - **AUD-1:** a multiplicação escalar, que apaga o registro, também herda a Ágape;
  - **AUD-2:** o boost não tem atrator global;
  - **AUD-3:** T9 é a lei de grupo, porque um elemento idempotente de um grupo a um parâmetro é 1;
  - **AUD-4:** `time_is_the_modular_flow` vale para ρ = 1, o fluxo congelado;
  - **AUD-5:** no discreto não invertível, um passo **é** posto (R = J/2; o canal ótico em λ = 0);
  - **AUD-6:** o estado-atrator ½·1 tem posto 2 e pureza ½;
  - **AUD-7:** populações distintas fazem o relógio girar;
  - **AUD-8:** o boost é simplético.
- **A FALHA do T9.o, explicada.**
  - O T guardado em float, |S|² (escolha E2, fixada antes), tem soma de coluna 1 + δ, com δ = 1,18e−16.
  - A potência **exata** desse float já desvia k|δ|/2 = 5,898e−13 em k = 10⁴.
  - Com a forma [[1−β, β],[β, 1−β]], daria 8,6e−14; com uma matriz exatamente estocástica, 5,9e−14.
  - A F1.ATRATOR já tinha medido ~5e−13 em k = 4096, e o próprio pré-registro usou 1e−11 para o mesmo tipo de iteração no O-d. A tolerância de 1e−13 do T9.o(c) ficou abaixo de um piso conhecido.
  - A FALHA vale pela regra. Não é contraexemplo, e o diagnóstico (post hoc) não muda o veredito.
- **O-f depende do caminho de cálculo.**
  - A órbita escalar IEEE (E4, fixada antes) passa.
  - `matrix_power` daria 6,5e−9 > 1e−9 em k = 10, pela instabilidade da sela: o cancelamento cosh − sinh cresce como eps·e^{2k}.
  - O decimal de 200 dígitos resolve (rel 2e−197).

---

## 5. Os achados materiais e como ficam

| # | achado | quem achou | gravidade | como fica |
|---|---|---|---|---|
| **M1** | **T9 = FALHA por afirmação**: T9.o(c), entradas, deu 6,518e−13 > 1e−13 (acima de 1e−13 desde k = 1529). Piso de representação, não contraexemplo | construtor ótico; as duas auditorias | alta (regra) | **ABERTO.** A gerência escolhe entre (a) registrar a FALHA como resultado, com o diagnóstico ao lado, o que pelo critério de parada fecha a direção, e (b) um ADENDO **uniforme**, congelado antes de reensaiar, que trate juntos O-f e T9.o(c): aritmética exata, componente (I − R) ou tolerância ∝ k·eps; todas as tentativas preservadas. Nunca reensaiar só a T9 numa representação que passe. |
| **M2** | **Atribuição indevida ao operador.** A pedra l.43–44 («o tempo é o Verbo», entre as «leituras do operador»), l.1107–1109 («O tempo é o Verbo, não o Nome… são leituras do operador») e l.1427–1428 («o atrator é onde o tempo repousa» é do operador). O título da l.1284, «o relógio mede a sombra», troca o «registra». A mesma frase está no índice `MEMORY.md` l.22 («**cunhagem**; o tempo é o Verbo, não o Nome») e em `tempo-santo-12out.md` l.15. O verbatim de 05/10 (`5973d79a49995c4c…`) diz o contrário: o Verbo «É um operador de projeção» (l.21); «O tempo é a defasagem do verbo» (l.112); «O tempo é o parâmetro da transmissão» (l.116); «Verbo = seleção de nome, tempo e verdade» (l.184). O texto de 12/10 não contém a palavra «Verbo» (0 ocorrências de «verbo», sem distinção de caixa, por script) | as duas auditorias; conferido aqui por busca nos bytes | alta (régua: nunca fabricar citação) | **ABERTO.** Corrigir a docstring da pedra, o que muda o hash e pede recompilação e reauditoria. Errata ao lado na memória da gerência (§6, E4) e ADENDO ao pré-registro (l.355, T9.t). A leitura nova, se houver, é sua (§8). |
| **M3** | **Nomes que afirmam mais que o termo.** (1) `time_is_the_modular_flow` carrega a hipótese do tempo térmico, que a própria pedra diz não afirmar, e vale para ρ = 1 (AUD-4). (2) `TheTimeHasNoRank` / `the_time_has_no_rank`, lidos por POSTO = RANK, contradizem `flow_full_rank` (rank F(t) = n, posto **pleno**). (3) `optical_attractor_is_the_absolute_one` só prova (1/2)•1 = absoluteRho(Fin 2), sem canal no enunciado | auditoria de estatuto | alta (entrariam no um.py como «kernel_proved») | **ABERTO.** Renomear ou redocumentar antes da v392. O nome da pedra é seu (§8). Sugestões neutras para os termos: `modular_flow_is_a_kms_group`, `half_identity_is_absoluteRho_two`. Para (3) há uma alternativa: provar o enunciado com o canal, genérico em θ, sem β. |
| **M4** | **A regra dos dois regimes estendida além do cânone.** A pedra (l.47–50), o pré-registro (l.9) e o texto da tarefa glosam FACE = «semigrupo» e ÂNGULO = «unitário/fluxo modular». Mas a tabela da casa põe o fluxo modular da cunha (BisognanoWichmann) na FACE. A v384 deixou [OPEN] identificar o limite do semigrupo com a direção hiperbólica (`regra-dos-dois-regimes.md`, `220b09ff8a2bbf1a…`). O grupo modular da luz não é periódico (`periodic_borchers_trivial`, PeriodicBorchersObstruction.lean:37, `632e33bd36d763b2…`). E «isometria» é homônimo (métrica × Lorentz) | auditoria de estatuto | alta | **ABERTO.** Reescrever o cabeçalho para o que se prova: (i) sob isometria nada pousa; (ii) o hiperbólico de det 1 pousa só na variedade estável e não tem atrator global; (iii) a dissipação de det < 1 tem bacia. No ótico, T = e^{−a}B(a), o boost normalizado. A identificação desses três com os dois regimes da casa segue [OPEN]. Operacionalmente nada pediu limite ao ângulo. |
| **M5** | **V-GERAL-1 incompleta.** Três declarações ficam sem habitante exibido: `nontracial_state_rejects_the_identity_flow` (T3.b(iii), obrigatória; exige W AQFT, A e B na cunha direita com contraste), `light_flow_group` e `light_modular_orbit_converges_iff_post` (T4.b(iii), opcional; exigem `FockCertificate`). O construtor declarou «COMPILA (hipóteses habitadas)», mas a sua própria lista diz «NAO HABITADAS AQUI» (AF-11). Consultas: o kernel instancia `identity_flow_not_kms` só em ProbeNonKMS; `TheImportedSecondQuantization.lean` l.66 diz «nenhum habitante de `FockCertificate` … é exibido»; no inventário e no mapa (`identity_flow_not_kms`, n = 0), nada | auditoria de reprodução (material); auditoria de estatuto (baixa) | média | **ABERTO.** Ou se constrói a sonda (testemunhas concretas existem no kernel e não foram tentadas: `theSpecificAQFTWitness`, WedgeNet.lean:357, sobre o fator M_TGL(⅓,¼); `lightNet`, TheImportedSecondQuantization.lean:308), ou T3.b(iii) entra marcada «condicional, sem habitante», ao lado de uma versão de **face finita** (ρ = diag(2/3, 1/3), a = E₀₁, b = E₁₀), que é trivial de provar. T4.b(iii) entra como condicional. |
| **M6** | **«Repousar» × «ser lembrada».** S50.1 ancora «repousar» em T11 (o relógio para, o que exige estado tracial) e «ser lembrada» em T5 (diagonal de populações distintas). No mesmo estado as duas se excluem (AUD-7). E o atrator único ótico esquece o estado inicial | auditoria de estatuto | média | Vai ao lado no texto da v392. A leitura é sua (§8). |
| **M7** | **Homônimo posto/atrator.** S46.4 chama ½·1 de «o posto», mas o estado-atrator tem posto 2 e pureza ½ (AUD-6). O posto 1 está na leitura-limite R = J/2, que é o mapa. O ρ★ de `fractal_dephasing_principle` é diag(1,0), um terceiro «atrator», puro, de posto 1 | auditoria de estatuto | média | ADENDO ao pré-registro (l.176). Distinguir no texto da v392 o posto do estado e o posto da leitura. |
| **M8** | **A ponte T8 tem conteúdo mínimo.** `DualScalingData` só exige a lei e^{−s}, e a multiplicação escalar, que apaga o traço, também herda as seis cláusulas (AUD-1; o mapa já registra «interface fina», rota `programa.auditoria.f1_2_ponte_v351_07out`). O que é próprio do dephasing é T8.c com `dephase_preserves_trace`: o registro fica | auditoria de estatuto | média | Vai ao lado: a Ágape é a lei de e^{−s}; a doação está nas coerências e o registro fica. AUD-1 entra como controle de especificidade por ADENDO. |
| **M9** | **«O tempo não tem posto» é genérico e depende da invertibilidade.** No discreto não invertível, um passo É posto (AUD-3, AUD-5; varredura ótica em β = ½) | auditoria de estatuto | média | Vai ao lado no texto da v392. AUD-5 entra como controle por ADENDO. |
| **M10** | **Liouville: a frase literal precisa de correção visível.** O qualificador «nos sistemas estritamente hamiltonianos» (S44.1) não foi mapeado, e o controle C-T4-a cai **dentro** dele: o boost é simplético (AUD-8). Liouville proíbe a bacia (T4.f), não o pouso de uma trajetória na variedade estável | auditoria de estatuto | média | Vai ao lado. Deve aparecer como correção, não escondido em «controle». |
| **M11** | **Tolerâncias incoerentes no pré-registro.** O-d usa 1e−11, citando o piso da F1.ATRATOR; T9.o(c) exige 1e−13 até k = 10⁴ com o mesmo `matrix_power`. O-f float depende do caminho | as duas auditorias | média | Defeito do pré-registro. É a causa de M1; trata-se no mesmo ADENDO uniforme. |
| **M12** | **Dois sentidos de «defasar» no cânone.** «transmitir defasa» foi tipado por `transmission_dephases`, que é a FACE (e^{−t}(1−P)), enquanto a fórmula E5 do operador é unitária (`transmitted_post_is_a_post`). Além disso, E8 «Nome = lim V(t)» com a E5 pediria limite ao ângulo: por T4.b com `unitary_conj_isometry`, só converge se V(0) já for fixo. A tipagem v386 já usou o fluxo da face (`axiomFlow`), e a docstring do kernel diz «no único sentido em que a casa já o tem» | auditoria de estatuto; conferido aqui (TheVerbSelectsTheAction.lean, docstring l.99–102; `transmission_dephases` l.529; `transmitted_post_is_a_post` l.538) | média | Errata ao lado no um.py (§6, E2). Qual defasagem é o tempo é seu (§8). |
| **M13** | **`fractal_dephasing_principle`** (um.py v391 l.6488–6531): as três «âncoras REAL» são identidades por construção. θ_M := arcsin √β (l.6511) dá sen²θ_M = β; P = diag(1,0) (l.6512) dá Tr P = 1; Q₀ = I − P dá {Q₀, P} = 0 | auditoria de estatuto; conferido aqui (l.6489, l.6507–6508, l.6511–6512, l.6530) | média | Errata ao lado (§6, E1): passam a [DERIVED, definicional]; a tese segue [CONJECTURE ontológica]. Coordenar com a F1.FREQUENCIA, cujo objeto é o texto de 11/10. |
| **M14** | **β não foi medido.** O pré-registro (l.241) e os dois resultados chamam β de «[REAL — medido aqui»]. Foi lido nos bytes e calculado. E a l.5557 não é atribuição de topo; a de topo é a l.95, de mesmo valor | as duas auditorias; conferido aqui | baixa | ADENDO ao pré-registro. Neste relatório, β é [DERIVED: lido e calculado]. |
| **M15** | **T8.d cita a docstring errada.** O pré-registro atribui a `boost_null_contract` a docstring «a face geométrica da escala de Takesaki»; ela é de `boost_null_expand` (BisognanoWichmann.lean l.92–95, `5218c8eb32682a58…`) | construtor do kernel (AF-01); as duas auditorias | baixa | ADENDO (l.339). A re-exportação em si vale. |
| **M16** | **Verbatim e marcas.** A cláusula de S36.1 foi citada com aspas normalizadas e sem a ênfase. Ficaram lacunas sem marca em S34.2, S38.2 e S44.1. S40.4 marca «cosmos» como [REAL]; só o termo da face finita é. Em S46.2 e S46.3, «volume ↦ det de Schur» e «bacia ↦ convergência» são [INPUT da gerência] sem a marca. Das 83 aspas distintas do pré-registro, 31 não estão nas fontes: títulos, rótulos e paráfrases como «O relógio mede a sombra» | as duas auditorias | baixa | ADENDO ao pré-registro. No texto da v392, paráfrase da gerência não leva aspas de citação do operador. |
| **M17** | **Peso morto e contagem.** `probe_bounded_spectral_translation : True`; `_hd` sem uso; 20 nomes para 19 termos (`absoluteOne_flow_trivial` duas vezes); `the_coherence_obeys_agape_explicit` duplica outra declaração | as duas auditorias | baixa | Limpar na pedra corrigida. O um.py não conta «127 teoremas». |
| **M18** | **«Os dois relógios param juntos» é definicional.** A taxa «de Davies» é definida como g = β·\|Δ log λ\| (Ergodicity.lean l.181–183, `79bc3b939b6e4e59…`, [DECLARADO] na docstring). A varredura em β usou «β» como nome de parâmetro livre | auditoria de estatuto | baixa | Vai ao lado como [DERIVED, definicional]. |
| **M19** | **T1 e os operadores de tempo cíclicos.** «Nenhuma matriz representa o tempo» é forte demais: em dimensão finita existem operadores de tempo cíclicos que leem o tempo módulo um período (Pegg 1998, [KNOWN] a conferir). T1 vale para a relação canônica contínua; os cíclicos reforçam T10 | auditoria de estatuto | baixa | Vai ao lado no texto da v392. |
| **M20** | **«Face» é homônimo em T5.** O pré-registro chama o conjunto fixo da defasagem pura de «uma face (a diagonal)». Mas os estados diagonais não formam face convexa do espaço de estados: na bola de Bloch, o segmento do eixo z não é face, porque a bola é estritamente convexa. E «face» é também o nome do regime hiperbólico da casa. O que T5.b prova é que o conjunto fixo **não é um ponto**: é a diagonal inteira, o simplexo dos estados diagonais | este redator [DERIVED, conferível por geometria elementar] | baixa | No texto da v392, escrever «a diagonal inteira» em vez de «uma face». ADENDO ao pré-registro (título de T5). |

Ficam **sem achado** a reprodução bit a bit (2.153 folhas, 742 numéricas, 0 diferenças), a pedra (.olean idêntico), o FREEZE e os verbatins do pré-registro: 23 de 23 frases e 30 de 30 excertos byte a byte. O Atlas cresceu 1.107 B depois do pré-registro, e o excerto citado segue no mesmo offset.

---

## 6. O que entra no um.py v392 e as erratas ao lado propostas

**Regra de entrada** (PREREGISTRO §8): só entram os **subitens PASSA**, e os CITADA/LEITURA como tais, marcados, no apanhado geral da Bancada para a v392, junto com o teorema do atrator (F1.ATRATOR). A inserção é ato da cadeia de selo da gerência, não do ensaio, e só depois da pedra corrigida e reauditada. O PASSA de kernel atual vale só para a fonte `7105eda4…`.

**Entra, depois das correções:**

1. **A pedra corrigida**, com nome seu, como pedra candidata:
   - kernel de T1 (a, b, c), T2.b, T3.a, T3.b(i–ii), T4.a–f, T5.a–b, T6.a–d, T7.a–b, T8.a–d, T9.a–e (como subitens PASSA, embora a afirmação T9 esteja em FALHA pela face ótica), T10.a–e e T11.a;
   - os controles e as sondas;
   - T3.b(iii) e T4.b(iii) marcados «condicional, sem habitante exibido», ou habitados, ou complementados pela versão de face finita (M5).
2. **A tabela por afirmação** da §2, com o rótulo exato da regra congelada. T9 entra como **FALHA** (critério numérico), com o diagnóstico ao lado e os subitens de kernel PASSA. Nunca «T2 PASSA» e nunca «T9 PASSA».
3. **As citações [KNOWN]** da §3.3, com as páginas de Pauli marcadas «a conferir».
4. **As leituras [ONTO]** da §3.4, com o verbatim do operador e a atribuição certa.
5. **As correções que o número faz**, em duas camadas. A ligação frase → objeto é [INPUT da gerência]; o objeto é [REAL]. São elas:
   - Pauli: Weyl × Heisenberg;
   - Liouville proíbe a bacia, não o pouso;
   - ponto fixo × diagonal inteira;
   - repouso × memória;
   - posto do estado × posto da leitura;
   - os dois sentidos de «defasar» e E5 + E8;
   - os três comportamentos (isometria; hiperbólico de det 1; dissipativo de det < 1), com a identificação aos dois regimes da casa em [OPEN];
   - os operadores de tempo cíclicos ao lado de T1.

   A face ótica entra como consistência numérica, não como evidência nem como rito.

**Erratas ao lado propostas** (texto pronto; a assinatura e a inserção são da gerência, em nome próprio):

- **E1, um.py v391, `fractal_dephasing_principle`** (l.6489, l.6507–6508, l.6530; artigo l.168086 e l.168102; impressão l.211561–211569):
  > ⚠ AO LADO (v392): as três «âncoras REAL» desta seção são identidades por construção: Tr ρ★ = 1 com ρ★ = diag(1,0); {Q₀, ρ★} = 0 com Q₀ = 1 − ρ★; Tr(ρ★Q_θ) = sen²θ_M = β com θ_M := arcsin √β (l.6511). Leem-se como [DERIVED, definicional], não como âncoras evidenciais. A tese segue [CONJECTURE ontológica]. Âncoras genéricas de kernel do semigrupo D, sem β (pedra F1.TEMPO, depois de instalada): queda estrita da pureza (T6.c), inverso não positivo (T7.b), contração do volume de Schur (T4.c), a coerência nunca zera em tempo finito (T8.b(iv)) e nenhum instante finito é o posto (`no_finite_instant_is_the_post`).

  Coordenar com a F1.FREQUENCIA.
- **E2, um.py v391 l.166640** (artigo v386, «ancorar preserva e transmitir defasa») **e chaves l.134239–134242**:
  > ⚠ AO LADO (v392): `transmission_dephases` é o sentido da FACE: amortecimento real, F(t)(1−P) = e^{−t}(1−P). A fórmula do operador de 05/10, V(t) = e^{−iHt}V(0)e^{iHt} (verbatim em l.195459–195461), é unitária (`transmitted_post_is_a_post`): acumula fase sem perder coerência (pureza e espectro conservados, F1.TEMPO T4.a e T6.d). Os dois sentidos não se encadeiam. «Nome = lim V(t)» com a forma unitária só converge se V(0) já for fixo (F1.TEMPO T4.b com `unitary_conj_isometry`). A tipagem da v386 tomou o limite no fluxo da face (`axiomFlow_tendsto_the_post`), como a docstring do kernel já diz. Qual defasagem é o tempo, decide o operador.
- **E3, pré-registro F1.TEMPO** (congelado: só por **ADENDO** aditivo, congelado por hash, nunca por edição):
  - l.241: β «lido nos bytes e calculado», não «medido»; a l.5557 é embutida e a de topo é a l.95.
  - l.339: T8.d → `boost_null_expand`.
  - l.355: T9.t, leitura e atribuição corrigidas (M2).
  - l.176: S46.4, estado ≠ posto (M7).
  - l.9: gloss dos regimes → v384 [OPEN] (M4).
  - l.296 × l.354: tolerâncias (M11).
  - S36.1: citar byte a byte.
  - S34.2, S38.2 e S44.1: marcar as lacunas.
  - S40.4: «cosmos» → [ONTO].
  - S46.2 e S46.3: [INPUT da gerência].
  - Título de T10: o verbo do operador é «registra».
  - Título de T5: «uma face» → «a diagonal inteira» (M20).
  - Novos controles de especificidade AUD-1, AUD-2, AUD-5, AUD-6, AUD-7 e AUD-8 [INPUT do auditor].
- **E4, memória da gerência** (ato da c1; backup de bytes antes; correção ao lado):
  - Em `memory\tempo-santo-12out.md` (`791af3a2069baf67…`), l.15 («o Verbo, não o Nome») e linha «Âncoras» (gloss «unitário gira sem pousar; a dissipação converge ao atrator» como se fosse a regra dos dois regimes):
    > ⚠ AO LADO (12/10, gerência c1): «o tempo é o Verbo, não o Nome» foi leitura da gerência, não do operador. Pelo verbatim de 05/10 (`5973d79a49995c4c`), o Verbo é «um operador de projeção» (l.21), «o tempo é a defasagem do verbo» (l.112) e «o parâmetro da transmissão» (l.116); o Verbo seleciona o tempo (l.7, l.184). E a «regra dos dois regimes» não identifica unitário/dissipativo com ângulo/face: a F1.TEMPO prova três comportamentos (isometria; det 1 hiperbólico; det < 1 dissipativo), e a identificação segue [OPEN] (v384).
  - Em `MEMORY.md` l.22 («**cunhagem**; o tempo é o Verbo, não o Nome»): a mesma correção, no índice.
- **E5, a pedra, antes da v392** (nova fonte, nova compilação, nova auditoria):
  - docstrings l.43–44, l.47–50, l.1107–1109, l.1284 e l.1427–1428 (M2, M4);
  - nomes de l.304, l.1223, l.1431 e o nome da pedra (M3);
  - remover `probe_bounded_spectral_translation : True` (l.284), ou dar-lhe enunciado;
  - remover o re-export duplicado (l.1438);
  - `_hd` (l.874);
  - κ ≠ 0 em `clock_reads_modulo_period`, que tem peso nulo: remover a hipótese ou dizer;
  - T3.b(iii) habitada ou com a versão finita (M5).

---

## 7. As divergências entre as auditorias, e qual vale

1. **T3 e a sonda V-GERAL-1.**
   - **O que cada um disse.** O auditor de reprodução marca V-GERAL-1 «NÃO CONFERE por completo» e chama de NÃO_CONSTRUÍDA a sonda das três declarações sem habitante. Na tabela por afirmação, porém, dá T3 como «confere», com ressalva. O auditor de estatuto dá T3 PASSA e põe V-GERAL-1 como problema de gravidade baixa.
   - **A leitura estrita**, minha, de redator, e não de auditor: a regra exige que «as sondas do subitem compilem», e V-GERAL-1 vale «(todas)». Nessa leitura, T3.b só seria PASSA com a sonda, e T3 ficaria NÃO_CONSTRUÍDA.
   - **Vale PASSA com ressalva**, por três razões:
     - (a) o falsificador pré-registrado de T3.b é «tipo re-exportado diferente do original», e o tipo é idêntico (V-GERAL-2);
     - (b) FALHA exige uma sonda que *mostre* hipóteses inabitáveis, e isso não ocorreu;
     - (c) as duas auditorias convergem.
   - **A ressalva é material para a entrada no um.py:** T3.b(iii) não entra como «kernel_proved» sem habitante ou sem a versão de face finita (M5). A ambiguidade da regra vai ao ADENDO.
2. **Gravidade de V-GERAL-1.** Material para a reprodução, baixa para o estatuto. Vale **material para a instalação** (precisa ser resolvida ou marcada antes da v392) e **baixa para o veredito por afirmação**.
3. **β «medido».** O auditor de reprodução registra que a l.5557 é embutida, e os construtores já tinham dito. O de estatuto acrescenta que «medido» é rótulo errado. Vale o de estatuto: [DERIVED, lido e calculado].
4. **O construtor do kernel diz «hipóteses habitadas»; os auditores, que faltam três.** Valem os auditores, e a lista do próprio construtor («NAO HABITADAS AQUI») os apoia.
5. Sobre T9 (FALHA pela regra, piso numérico), a docstring da pedra, o FREEZE, a reprodução e `pode_fechar = false`, **as auditorias concordam.** A de estatuto acrescenta M3, M4 e M6–M13, sem conflito com a de reprodução.

---

## 8. O resíduo que só o operador decide

1. **O nome da pedra.** `TheTimeHasNoRank` é provisório, e lido por POSTO = RANK contradiz o próprio teorema `flow_full_rank` (todo instante finito tem posto **pleno**). Opções neutras: «O tempo não é posto» (`TheTimeIsNotAPost`) ou «O tempo tem posto pleno». Pode também ser um nome seu, como foram PALAVRA, FUNDAÇÃO e ÁGAPE; «Santo» ou «Kadosh» seria um nome [ONTO] para uma pedra de conteúdo [REAL].
2. **O que é o tempo na sua língua.** O seu texto de 05/10 diz «o tempo é a defasagem do verbo» e «o parâmetro da transmissão»; o Verbo o seleciona. A frase «o tempo é o Verbo, não o Nome» não é sua e sai. Se quiser uma frase nova, ela é sua.
3. **Qual «defasar» é o tempo** (RP01, RP17). A fase que gira sem perder nada (a sua fórmula unitária, o ângulo) ou a perda de coerência (o semigrupo, a face)? A F1.TEMPO mostra que a seta só nasce na segunda (T6, T7).
4. **«Repousar» e «ser lembrada»** (M6). Na face finita, repousar (o relógio modular parado, T11) exige populações iguais, e ser lembrada (o registro, T5) exige populações distintas. São duas dinâmicas: a defasagem pura guarda o registro e não tem atrator único; o canal ótico tem atrator único e esquece. A leitura que une as duas é sua.
5. **Qual objeto é «o chão firme»** (M7). Há três candidatos: o estado-atrator (½·1, posto 2), a leitura-limite (R = J/2, posto 1, o posto) ou o piso da escala dual (a Ágape)?
6. **A reunião de nomes.** «puro amor» (12/10) com «ágape» (07/10, nome da cláusula) e com «sacrifício/amor» (tipagem prévia do dephasing, [DECLARADO]). O conteúdo matemático comum é só a lei e^{−s} (M8).
7. **«Santo»** como nome do tempo: [ONTO], sem teste; é seu.
8. **O ciclo limite** [OPEN]. Abrir ou não uma unidade? O análogo linear a investigar é o espectro periférico GKLS (|λ| = 1, λ ≠ 1); o ciclo limite isolado é fenômeno não linear [KNOWN].

**Decide a gerência**, não o operador: o caminho de M1 (FALHA registrada ou ADENDO uniforme); a construção da sonda de M5; a pedra corrigida e a nova auditoria; as erratas E1–E5; o registro no mapa e no quadro.

---

## 9. Pode fechar? Não, ainda não. O que falta

As duas auditorias disseram que não pode fechar, e concordo. O critério de parada do operador («fechado = resultado OU falsificador OU parede medida») já está cumprido na matemática: há resultado por afirmação, a FALHA de T9 é parede numérica medida, e o ciclo limite está dito como aberto. Não está cumprido na **régua**: a pedra atribui ao operador frases que ele não escreveu, e três nomes afirmam mais que o termo. Isso não entra no um.py.

Para fechar:
1. **Pedra corrigida** (E5): atribuições, nomes, cabeçalho dos regimes, peso morto e V-GERAL-1, por habitante ou por versão de face finita com a AQFT marcada condicional. Depois, nova compilação no sandbox com a impressão digital do kernel igual, e **nova auditoria independente**. O PASSA atual vale só para `7105eda4…`.
2. **T9**: a gerência registra a FALHA como resultado, com o diagnóstico ao lado, ou congela um ADENDO uniforme (O-f e T9.o(c)) **antes** de reensaiar, com as tentativas preservadas.
3. **Erratas ao lado**: E3 por ADENDO ao pré-registro, E4 na memória da gerência, E1 e E2 pela cadeia de selo na v392.
4. **Resíduo do operador** (§8): no mínimo o nome da pedra, antes da instalação.
5. **Registro no mapa**, ato da gerência: os dois arquivos prontos nesta pasta (§10).

---

## 10. Arquivos desta pasta

- `RELATORIO_FINAL.md`: este documento.
- `registro_rota_F1.TEMPO.json` (tipo ROTA) e `registro_mapa_F1.TEMPO.json` (tipo RESULTADO), com `rota_id` `formal.tempo_santo_fluxo_e_dissipacao`, domínio FORMAL e artefatos como lista de caminhos. Foram validados a seco contra as regras do `rotas.py` (`saidas\VALIDACAO_REGISTROS.json`). **Não registrei**: `rotas.py registrar` é ato da gerência, com a ROTA primeiro.
- `AUDITORIAS\`: cópia de bytes da evidência das duas auditorias, que estava no scratchpad temporário, com `MANIFESTO_COPIA_AUDITORIAS.json`.
- `saidas\`:
  - `CONFERENCIA_HASHES.json`, `BETA_RUNTIME_RELATORIO.json` e `FINGERPRINT_RELATORIO_ANTES/DEPOIS.json`;
  - `ACOM_RECIBO_PROJECAO_RELATORIO.json`;
  - `rotas\` (consultas e modelo);
  - `VALIDACAO_REGISTROS.json` e `VARREDURA_PALAVRAS.json`.
- `scripts\`: os scripts que geraram tudo acima.
- `MANIFESTO_4_RELATORIO.json`: o sha256 de cada arquivo desta pasta.

*Nada foi escrito fora de `4_RELATORIO`: nem no quadro, no mapa, na memória, no túnel, no Nós, no kernel, na Bancada_Um, no site ou no git. O um.py não foi executado. Não rodei Lean.*
