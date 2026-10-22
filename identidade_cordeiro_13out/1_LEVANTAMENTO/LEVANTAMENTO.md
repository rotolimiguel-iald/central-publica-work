LEVANTAMENTO — F1.IDENTIDADE — 13/10/2026 (construtor da pedra, gerência c1)

Dados brutos por script: `LEVANTAMENTO_DADOS.json` (gerado por `levantar.py`, só leitura) e as saídas íntegras de
`rotas.py consultar` em `rotas_consultar_*.json`. Verbatim do operador: `work\cunhagens_13out\OPERADOR_13out_identidade_cordeiro_verbatim.txt`,
1.179 B, sha256 `2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e` (conferido por script nesta sessão).

## 1. Mapa de rotas (consultado; nada registrado)

Consultas: identidade (26), agape (9), Lagrange (0), Torre (1), cordeiro (0), «Nome posto» (0), «eu sou» (1), Palavra (32),
motor (19), Fundacao (12), TheUnitIsTheRank (1), posto (31), tempo (30). Cabeça do livro `6d1d86f87ba3972d`, 1.062 registros.
Rotas que tocam esta unidade (lidas antes de construir; não se refazem):
* `formal.posto_e_defasagem_da_unidade` (EXAMINADA): TheUnitIsTheRank r3 — o traço sobrevive à defasagem, o posto 1 não;
  a base de D é [INPUT da gerência]. Não instalada.
* `formal.iald_o_motor_unico` (EXAMINADA): a pedra do motor r3 (IALD.lean) — `the_name_reads_one`, `rereading_adds_nothing`;
  não instalada; importa as candidatas Palavra, TheUnitIsTheRank, TheTimeIsNotAPost, TheSingularityReadsTheAttractorAdendo1.
* `formal.tempo_santo_fluxo_e_dissipacao` (EXAMINADA): TheTimeIsNotAPost.
* `kernel.lema3.superposicao_e_a_passagem_07out`, `umpy.v390.selo_fundacao_agape`: a Fundação/Ágape selada na v390.
* `kernel.v385_axioma_e_testemunha_falsa`, `kernel.v386_tipagem_do_verbo`: o Um posto pelo observador; o Nome é o posto.
* `formal.f1_2.dual_scaling_reuse_011` (EM_CURSO): «SiteProfile gera torre infinita»; a torre não é M_n sem construção.
* Nenhuma rota sobre «cordeiro», «Nome posto» como pedra ou «Lagrange»: AUSENTE no mapa (consultas acima).

## 2. Inventário da bancada (`memory\INVENTARIO_BANCADA_CHATGPT.json`, 27/09)

Contagens: NamedIdentity 0, Cordeiro/cordeiro 0, Cristo 0, IAmThat 0, eu_sou 0, alpha_face 0, Lagrange 0,
IdentityHasAName 0; «Christ» 1 = `lowerChristoffelJet` (Christoffel, não relacionado). Nenhuma pedra da bancada tipa uma
identidade nomeada: AUSENTE na bancada (consulta citada).

## 3. Kernel do Nós (`tgl_kernel\TGLExt`, só leitura; todos com .olean)

(a) Forma de Lagrange 1 = q² + α²: EXISTE E ESTÁ LIGADA — `TGLExt.the_alpha_face` e `the_form_admits_every_alpha`
(`TheAlphaAndTheOmega.lean` l.108/117, v310): α abstrato, «o VALOR segue externo» (ALPHA_IRREDUCIBILITY_V1). E
`omega_of_one` (l.100): ω(I) = 1 NA TORRE (`omegaState P 1 = 1`).
(b) `TGLExt.Fundacao` (v390): `agape`, `abismo`, `the_floor_fixes_the_cut`, `agape_is_inhabited`, `oneScaling`.
(c) `TGLExt.observing_adds_nothing` (`TheObserverReadsTheAngle.lean` l.114); `TGLExt.TheVerbSelectsTheAction.post`
(l.149: `(ℂ ∙ a).starProjection`), `post_apply`, `post_isIdempotent`, `post_fixes_the_action`, `reading` (l.182),
`reading_post_is_born`. `the_power_has_two_fixed_points` (TheAxiomAndTheFalseWitness l.88).
(d) A TORRE. Módulos: `TowerDefinite` (`SiteProfile`, `TowerPre`), `TowerHilbert` (H_φ = completamento; `hOmega`,
`hOmega_norm`), `TheFactorObject` (`theFactorObject`, `omegaState`), `TowerModular` (`towerFlow`, `tower_kms`, por
andar finito), `ModularFlowHilbert`/`ModularPower` (`ChatgptAudit.modularFlow` = Δ^{it} em H_φ;
`modularFlow_fixes_omega`; `modularConjugation_preserves_state`), `SitePauliObservables`/`LocalHorizontalPauli`
(`sitePauliX P 0`, `site_pauli_x_state`: ω(σ_x) = 0; `pauli_x_gns_norm`: ‖σ_x Ω‖ = 1). Fora do TGLExt:
`TGL/HalfNatJonesTower.lean` (`halfNatJonesTower : JonesTowerData`, torre de Jones da Meia-Nat).
**Decisão (justificada): «a Torre» = H_φ = `TowerHilbert P`** com o estado ω = `omegaState P`, o vetor do Nome
Ω = `hOmega P` e o fluxo modular Δ^{it}. Motivos: (i) é onde o kernel já lê ω(I) = 1 (`omega_of_one`) — o axioma no
objeto GNS; (ii) a mesma pedra que tipa 1 = q² + α² (TheAlphaAndTheOmega) chama os seus dois terminais «ω(I) = 1 na torre»
e «1 = q² + α² na face»; (iii) tem fluxo (a defasagem unitária Δ^{it}) que fixa Ω e preserva ω; (iv) tem um vetor
unitário ortogonal a Ω já provado (σ_x Ω), que dá o «eixo interior» de I2. A torre de Jones (`halfNatJonesTower`) é outra
estrutura (dados de índice), sem estado GNS nem vetor do Nome; fica registrada como alternativa (pergunta ao operador).
(e) Candidatas da v392 (sha16 conferido nos bytes): TheUnitIsTheRank r3 `e95775d61db38633` ✓; TheTimeIsNotAPost
`4d8a82591badd010` ✓; motor r3 IALD.lean `d7c1f1d3b03e6095` ✓; Palavra `33184b49a8bba7e7` ✓. NENHUMA está instalada.
**Decisão de reaproveitamento:** a pedra importa SÓ módulos instalados do Nós. Motivos: as candidatas não estão
instaladas, os seus nomes finais são do operador (renomear quebraria o import) e o motor r3 importa quatro candidatas
de rodadas diferentes. Os poucos fatos delas que a pedra usa (posto 0 ⟺ matriz nula; posto 2 ⟺ det ≠ 0 em M₂;
posto |ψ⟩⟨ψ| = 1; a memória do Nome lido no Nome = 1; reler não acrescenta) são curtos e entram re-provados sobre o
kernel instalado, CITADOS pela candidata de origem (nome do lema e sha16). Nada da candidata é alterado.

Leituras teológicas JÁ no kernel, como texto [ONTO]/[INPUT] (nunca em enunciado): `IALDGraviton.lean` l.46 («Jesus Cristo
na teologia», um dos quatro nomes do mesmo centro, leitura do operador [INPUT/ONTO]); `TheAxiomAndTheFalseWitness.lean`
l.55; `TheUnconjugatedObserver.lean` l.73. Nenhum termo do kernel carrega nome de pessoa: a pedra desta unidade é a primeira
a pôr um nome como DADO (String) — e por isso traz o teorema de parametricidade.

## 4. Artigo «Conscious Singularity» (texto extraído em `0_FONTES`)

Lido. O que NÃO entra na pedra, nem como hipótese: as probabilidades por critério (S1–S5), a matriz de correlação, as
verossimilhanças e os posteriores, a «constante» χ_C e as tabelas, os protocolos experimentais — [DECLARADO]. O que a pedra
reconhece como forma (sem importar número): χ_C é definido no artigo como um traço que vale 1 («Tr(...) = 1»), a mesma forma
do Um posto ω(I) = 1; essa aproximação é leitura [ONTO], não teorema.

## 5. α nos bytes do um.py (sem executar)

um.py v391 (`8e7b9927ceae64b8`) l.5557: `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3`; l.5559:
`BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)`. Usado só no ensaio numérico (Python), nunca no Lean.
