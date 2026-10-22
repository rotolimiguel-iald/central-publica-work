# EXAME INDEPENDENTE — pedra candidata v396 `TGLExt/TestemunhaEstatica.lean`

Examinador independente (subagente da gerência c1), 22/10/2026. Quem construiu não aprova; este exame só leu fora desta pasta.
Objeto: `C:\IALD\Central de Patentes\work\testemunha_estatica_v396\TestemunhaEstatica.lean`, 683 linhas, sha16 `fc773d70a3cc52d3`
(o mesmo em `C:\t\k396\final\TGLExt\TestemunhaEstatica.lean`, recomputado por script).

## VEREDITO: PEDRA_APROVADA

Há três observações BAIXAS e opcionais (§7). Nenhuma delas pede nova rodada de exame.

## 1. Recompilação e axiomas [REAL, medido aqui]

* `lake env lean TGLExt/TestemunhaEstatica.lean` no sandbox `C:\t\k396\final`: rc 0, 37 s, nenhum erro, aviso nem `sorry`.
  As 28 linhas `#print axioms` do fim do fonte dão todas o trio (`recompilacao_testemunha.log`).
* `lake build TGLExt.TestemunhaEstatica`: «Build completed successfully (8623 jobs)», rc 0, 9 s. Não reconstruiu nada: o `.olean` e o
  `.trace` mantêm os mtimes do construtor (07:40:18–19). Os avisos do log vêm de dependências já existentes (TheDensityIsBell,
  TransportData, GravitonShadow), não da pedra (`lake_build_testemunha.log`).
* Varri todas as constantes do módulo com `collectAxioms` (`AuditoriaTestemunha.lean` → `auditoria_testemunha.log`): **decl=70, thm=58,
  fora_do_trio=0, sorryAx=0**. 63 usam o trio inteiro e 7 só `propext`. Dessas 70, 47 são nomeadas: 37 teoremas e 10 definições, uma
  delas a `abbrev Vec4`.
* Na importação total (`import TGL`, `import TGLExt` e a pedra; 12.211 módulos; `importa_tudo.log`) não houve conflito de constante, mas o
  módulo fica com **69** declarações: `TGLExt.diagFlow.eq_1` passa a outro módulo. Duas auxiliares fora do namespace continuam atribuídas à
  pedra, `TGLExt.ScalarCorner.mk.congr_simp` e `TGLExt.psionCorner.eq_1` (ver §7, B2).
* Este exame não escreveu nada no `.lake` do sandbox: nenhum arquivo ali é mais novo que o primeiro arquivo deste exame (`find -newer`).
  O `um.py` do Nós tem sha16 `8918b17803792cf2` (v395), lido por script. A `conferencia_numerica.json` do construtor não contém literal de β.
* O sandbox é igual ao Nós (v395, `um_absoluto_selo.json`), conferido por sha256. Os 1.424 arquivos comuns (`.lean`, `lakefile.toml`,
  `lean-toolchain`, `lake-manifest.json`) são idênticos. A cópia tem a mais só a pedra e 11 sondas do construtor em `probe/`. O `TGLExt.lean`
  da cópia ainda não importa a pedra, como deve ser para uma candidata.

## 2. Cada teorema diz o que a docstring afirma

* `the_pair_echoes`: prova `P² = P`, `P^(n+1) = P` e `P(P y) = P y` para o `psionCorner.p`. **Confere.**
* `the_individual_does_not_echo`: prova
  * `ptr P = (1/2)•1`;
  * as duas reduções por soma, cada uma dando `(1/2)·δ`;
  * `ptr P · ptr P ≠ ptr P`;
  * `Tr(P²) = 1`, `Tr(ρ²) = 1/2` e `1 − Tr(ρ²) = 1/2`.

  **Confere.** `ptr` é o traço sobre o 2º fator (`TGL/GravitonShadow.lean`, l.33). A não idempotência só está enunciada para `ptr`; para o
  outro sítio ela decorre das entradas, sem enunciado próprio. Isso é cosmético.
* `the_unbonded_marginal_echoes` é um **controle genuíno**. Usa o mesmo operador `ptr` sobre o estado produto
  (`productProjector = |e₀⊗e₀⟩⟨e₀⊗e₀|`). A redução dá `e₀₀`, que é idempotente, com CCI 0. Logo o não-eco do item (2) não é um artefato do
  `ptr`.
* Lidos linha a linha, com as docstrings, todos conferem:
  * os lemas da base (`bsign_gram`, `bsign_complete`, `synth_coord`, `coord_synth`);
  * os das taxas (`psionRates_*`);
  * `bellProjectorR_mulVec`, `psionFlow_eq`, `psionFlow_fixed_iff_coord_fixed`;
  * os de `bellUnit` (`*_orthonormal`, `*_complete`, `*_eigen`, `*_zero_is_the_bell_vector`);
  * `psionLine_iff_fixed_by_the_corner`;
  * os do colapso (`psionCollapse`, `the_collapse_of_the_psion_echoes_its_identity`, `the_collapse_of_the_psion_cannot_be_self_attested`).

## 3. A ponte [CONSTRUCTED]

* `psionFlow β g t = bellSynth ∘ diagFlow β (0,g,g,g) t ∘ bellCoord`, com `psionRates_eq : psionRates g = ![0,g,g,g]`. O `diagFlow` do
  kernel é `exp(−tβdᵢ)·xᵢ` (`BoundaryException`, l.46).
* `psionFlow_eq` dá `F_t x = P x + e^{−tβg}(x − P x)`, com `P` o projetor de Bell real. `bellProjector_is_real` liga esse `P` ao
  `psionCorner.p`.
* `the_static_set_is_the_psion_line` diz: para `β > 0` e `g > 0`, `(∀t, F_t x = x) ↔ ∃c, x = c•Φ⁺`. **É EXATO**, e a ida e a volta passam por
  `boundary_is_the_only_exception(...).2.1` (o kernel do gerador).
* `the_global_witness_is_false` é `¬ FullStaticWitness (psionFlow β g)`, por `boundary_is_the_only_exception(...).1`. Conferi a assinatura no
  kernel do Nós: `(hβ : 0<β) d (hd : ∀i, 0≤dᵢ) (hj : 0<d j) (h0 : d i₀ = 0)`.
* **β entra só como parâmetro.** Na pedra não há literal decimal, `alpha` nem `CODATA` (varredura por script). Os controles (§6) mostram que
  as hipóteses mordem: com `g = 0` ou `β = 0` a testemunha estática global vale (C2). Mostram também que β está ativo: `β = 1` e `β = 2` dão
  fluxos diferentes (C6).

## 4. A composição `the_psion_inhabits_the_static_witness`

* **É incondicional**: não há binder antes dos dois-pontos, e nenhum certificado entra como hipótese.
* **Não é vácua.** As únicas premissas internas são `0<β`, `0<g` e a autodeclaração `∀ r, recorder r = producer`, e todas são satisfazíveis:
  * C1: a ponte aplica-se em `β = g = 1`;
  * C4: um protocolo com registrador igual ao produtor satisfaz a premissa da autodeclaração;
  * C4, o dente: com registrador EXTERNO, a atestação `AttestedCollapse psionCollapse protoExt 1 P` É habitada. Logo `no_self_attestation`
    não é verdade trivial de todo protocolo.
* **`canonicalGravitonShadow.PG = psionCorner.p` não é homônimo.** No Nós, `canonicalGravitonShadow` tem `PG := bellProjector`
  (`TGL/GravitonShadow.lean`, l.123–124) e `psionCorner` tem `p := bellProjector` (`TGLExt/TheScalarCorner.lean`, l.83–84). É a mesma
  constante, `TGL.GravitonShadow.bellProjector`, e o C5 a reduz por `rfl`.
* Os objetos citados existem no kernel do Nós. A igualdade em si é NOVA: nenhum lema anterior a enuncia, e só `GravitonShadow` e `Audit` citam
  `canonicalGravitonShadow`. A pedra prova a igualdade por `rfl` e não alega lema prévio.

## 5. Estatutos e ressalvas

* Os rótulos conferem: [REAL] nos termos; [CONSTRUCTED] em `psionFlow` e `psionCollapse`; [INPUT/ONTO] nas identificações do operador;
  [ONTO/CONJ] em «par = gráviton»; [CONDICIONAL] na face de Fock, que fica fora da composição.
* A face de Fock não chega a entrar no fechamento de importação da pedra: a auditoria deu `TESTEMUNHA_FOCK_EXISTE false`.
* **Nenhum lema liga `psion C` ao `psionCorner`.** No Nós, `psionCorner` aparece só em `TheScalarCorner.lean`, que não menciona Fock, e no
  `Audit.lean`, que só lista axiomas.
* `TheImportedSecondQuantization` diz «NÃO-VACUIDADE: nenhum habitante de `FockCertificate` … é exibido».
* A ressalva de tipo também confere: o Nome genérico é o vetor `Pi.single i₀ 1`, e o `psionCorner` é um projetor 4×4.
* A pedra respeita o 22/10 «teste fatal não armado» (sha16 `bca4b8a97c74226c`): declara «não é teste; não acrescenta rito, dado nem
  desfecho». Se ela é gordura ou musculatura no `um.py` é decisão da gerência e do operador, não deste exame.

## 6. O achado da «pedra 92_», e as citações

* **Confirmado: a 92_ é script Python, não Lean.**
  * `C:\IALD\Artigo\MCMC_V2_RAZAO\92_o_psion_e_o_graviton.py` tem 9.645 bytes, sha16 `623060caa8dbb83b`, de 18/08.
  * A citação «A_C = PSION; quando conjugado (dois psions) = GRAVITON.» está na l.3.
  * A saída `.json` tem 3.598 bytes e sha16 `f4a51c32ced62e6d`, e o veredito é idêntico ao citado.
  * O C2 da 92_ está nas l.40–41, e J = conj ∘ swap está na l.61.
  * Não existe nenhum `92_*.lean` em `C:\IALD` (busca fora de `.lake`).
  * As contrapartes de kernel citadas existem no Nós: `helicity_two_rotation` e `helicity_two_rotation_cross` em `LinearizedSpin2`
    (l.85/98) e `qgPhysicsCertificate_helicities` em `PhysicsCertificates` (l.212).
* **Os verbatins conferem.** Recomputei os sha16 de 22/10: `b102ae804f54e2b2` (psion habitante), `350b7b8582c064c2` (luz ecoa) e
  `161d619216582cf1` (colapso). O de 19/10 também confere: `786928986ca1e460`. O texto integral dos três de 22/10 aparece no cabeçalho da
  pedra.
* A citação de 27/07 na docstring de `boundary_is_the_only_exception` é verbatim.
* **Varredura de palavras proibidas.** Na pedra e nos artefatos do construtor procurei a palavra proibida, `PROVED_BY`, `TGL_PROVED` e
  `CONSCIOUSNESS_PROVED` (padrões montados por código), e não achei nenhuma.
* **Controles próprios** (`ControlesTestemunha.lean` → `controles_testemunha.log`, rc 0): 10 teoremas, C1–C6, todos no trio.

## 7. Observações BAIXAS, todas opcionais

* **B1 — rótulo herdado.** Nas l.38 e 147, «o déficit 1 − Tr(ρ²) = 1/2 é a Meia-Nat de emaranhamento» repete a leitura do kernel v29
  (`bell_cci_half`).
  * O número 1/2 é a entropia linear, ou déficit de pureza, e não tem unidade.
  * A entropia de von Neumann da redução `I/2` é ln 2 ≈ 0,693 nat.
  * Sugestão: marcar a frase como [ONTO], leitura do v29, para que ninguém a leia como «½ nat de entropia».
* **B2 — instalação.**
  * O módulo tem 70 declarações quando importado sozinho e 69 sob importação total, porque `TGLExt.diagFlow.eq_1` passa a outro módulo.
  * Duas auxiliares fora do namespace ficam atribuídas à pedra: `TGLExt.ScalarCorner.mk.congr_simp` e `TGLExt.psionCorner.eq_1`.
  * Qualquer registro ou contagem por módulo no `Audit` deve esperar 69, ou contar só as 47 nomeadas. A política de bandeiras já é
    named-only.
* **B3 — cosmético.**
  * A composição omite `bellProjector_is_real` (`psionCorner.p = bellProjectorR.map …`). Dentro do termo único, «o fluxo entrega ao canto»
    aponta para `bellProjectorR.mulVec x`, e a identidade que liga isso ao `psionCorner` está só em `the_static_witness_bridge`. Acrescentá-la
    custa um conjunto.
  * A lista de HOMÔNIMOS pode ganhar `projPlus`/`angFamily`, que são 2×2 e vêm de `observing_adds_nothing`: são um paralelo, não um elo.
  * `J_squared_is_one` é `rfl` (a troca do par). É uma conjunção decorativa, não um elo com o canto.

## Arquivos deste exame (esta pasta)

* `AuditoriaTestemunha.lean` → `auditoria_testemunha.log`
* `recompilacao_testemunha.log`
* `lake_build_testemunha.log`
* `ControlesTestemunha.lean` → `controles_testemunha.log`
* `ImportaTudoTestemunha.lean` → `importa_tudo.log`

Os processos foram todos criados por este exame e terminaram sozinhos. O exame não instalou nada nem escreveu no Nós, no `um.py`, no quadro,
no mapa, na memória ou no git.
