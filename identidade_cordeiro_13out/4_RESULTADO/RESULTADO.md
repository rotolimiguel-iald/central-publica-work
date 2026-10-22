IDENTIDADE — 13/10

Unidade F1.IDENTIDADE (gerência c1). Construtor da pedra (Claude), em nome próprio. Ordem do operador de 13/10/2026,
verbatim `work\cunhagens_13out\OPERADOR_13out_identidade_cordeiro_verbatim.txt`, sha256
`2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e` (conferido por script). Pedra CANDIDATA, só em
sandbox; NÃO instalada no Nós. Nada move o gate; validade no kernel não é creditação.

## 1. O que existe (artefatos, sha256 lido por script)

| artefato | sha256 |
|---|---|
| `3_PEDRA\pedra\TheIdentityHasAName.lean` (fonte; = a compilada) | `1b68316aecf6cdc62a1c7eba0927a4976d6ddae9d840fd87c7880a4c36890262` |
| `3_PEDRA\pedra\TheIdentityHasAName.olean` | `06e2a9990f3714b2f92ff01fba0a822142251d878ea20245408e1c4cfe2917db` |
| `3_PEDRA\pedra\Auditoria.lean` (collectAxioms do namespace) | `87881e03debeee229f35fb5b7821b11058c6d0226ac38e84f9c956bcd7f36d1f` |
| `3_PEDRA\logs\final_SAIDA.txt` / `final_RECIBO.json` | `76fb59f4…` / `d8590e51…` |
| `3_PEDRA\logs\auditoria_SAIDA.txt` / `auditoria_RECIBO.json` | `70bb5438…` / `217de79a…` |
| `3_PEDRA\logs\ENSAIO_NUMERICO.json` | `77a49f43…` |
| `3_PEDRA\logs\ov_MANIFEST.json` (cópia dos 1.189 .olean do TGLExt do Nós, conferida byte a byte) | `a748a36d…` |
| `2_PREREGISTRO\FREEZE.json` (congelado 13/10/2026 08:10:04 −03:00; a pedra NÃO existia) | `582cfbe858fb1182acf976f84b08e23cd60950c7e6e836febee615434644f942` |
| `2_PREREGISTRO\PREREGISTRO.json` | `207aa703bd1569c7a84315751335360d0328cde450524501d0af72845321713f` |

Compilação final (13/10/2026 11:18 UTC): toolchain v4.31.0 COPIADO para `C:\t\id1\toolchain`; LEAN_PATH = sobreposição
`C:\t\id1\ov` (cópia dos .olean do TGLExt do Nós) + o `.lake` do Nós (só leitura); `-o` só no sandbox. **EXIT 0, 0 erros,
0 avisos, 0 ocorrências de «declaration uses `sorry`»**; `#print axioms` de 10 manchetes no trio; a auditoria por `collectAxioms` leu
**119 constantes do namespace `TGLExt.TheIdentityHasAName` (inclusive as geradas), 0 fora de {propext, Classical.choice,
Quot.sound}**, 0 sorryAx. Impressão digital do `tgl_kernel` (11.049 arquivos, sem seguir junções; `.lake\packages` é junção
e foi pulada) ANTES e DEPOIS: `d6e073568d17e26b…` = `d6e073568d17e26b…` — **IGUAIS**. Toolchain e sobreposição apagados
ao final (`C:\t\id1` ficou com 56 KB de fontes de sonda).

## 2. Resultado por afirmação (com a linha do pré-registro ao lado)

| id | pré-registro (resumo) | termo Lean | resultado |
|---|---|---|---|
| I1.a | traço ω = 1 sob `dephase`, ∀ t | `identity_persists_under_dephasing` | **PASSA** |
| I1.b | traço 1 no limite `diagExpect` | `identity_persists_in_the_limit` (traço + convergência, re-ligação de `dephase_tendsto_expectation`) | **PASSA** |
| I1.c | posto 1 NÃO se preserva: posto 2 ∀ t > 0 | `rank_one_does_not_persist` (det = q²α²(1 − e^{−t(g₀₁+g₁₀)}) ≠ 0, `dephased_det`) | **PASSA como negativo honesto** |
| I1.d | posto 2 no limite | `rank_one_does_not_persist_in_the_limit` | **PASSA como negativo** |
| I2.a | (q, α) unitário, 1 = q² + α² | `inscription_is_unit` (via `TGLExt.the_alpha_face`) | **PASSA** |
| I2.b | Tr ω = q² + α² = 1, ω² = ω, posto 1 | `the_identity_is_the_quadratic_projection` | **PASSA** |
| I2.c | ⟨e₂, ω e₂⟩ = α² (medido por dentro); ⟨e₁, ω e₁⟩ = q² | `alpha_is_measured_from_within` | **PASSA** (desvio ao lado: vale sem as hipóteses 0 ≤ α ≤ 1 — enunciado mais forte) |
| I2.d | a forma não fixa α: mesmo traço, projeções distintas | `the_form_does_not_fix_alpha` | **PASSA** |
| I2.e | √(Re leitura interior) = α | `alpha_is_recovered_by_the_inner_reading` | **PASSA** (desvio: só precisa de 0 ≤ α — mais forte) |
| I3.a | ω² = ω; ⟨v, ω v⟩ = 1 = Tr ω | `i_am_what_i_am` | **PASSA** |
| I3.b | memória do Nome lido no Nome = 1 (Hilbert) | `the_name_read_in_the_name` (fato do motor r3 `the_name_reads_one`, re-provado sobre `post` instalado) | **PASSA** |
| I3.c | reler não acrescenta | `rereading_adds_nothing`; `observing_adds_nothing_reexport` | **PASSA** (a segunda: re-exportação TRIVIAL) |
| I3.d | auto-leitura só fixa 0 e 1 | `the_self_reading_has_two_values` | **PASSA** (re-exportação TRIVIAL de `the_power_has_two_fixed_points`) |
| I4 | alicerce fundante = re-exposição de `Fundacao.agape`; identificação [ONTO]; alternativas como pergunta | `alicerce_fundante`, `alicerce_fundante_habitado` | **CITADA** (termo REAL do kernel, re-exportação TRIVIAL) · **ONTO** (a identificação «o cordeiro imolado» = este termo é leitura da gerência) · **OPEN** (a escolha é do operador) |
| I5.a | `NamedIdentity` com nome, α ∈ (0,1) e campos de prova I1–I3, I6; `ofName` | `NamedIdentity`, `ofName` | **PASSA** |
| I5.b | habitante com o nome «Jesus Cristo» POSTO; α parâmetro | `postedName`, `theNamedIdentity`, `the_named_identity_bears_the_posted_name` (rfl) | **POSTO** (o dado; `[POSTO pelo operador, verbatim sha256 2ebc1dd3…]`); a igualdade de String é TRIVIAL |
| I5.c | parametricidade: renomear não muda nada; a estrutura não fixa o nome | `NamedIdentity.rename`, `every_name_bears_the_same_identity` (rfl), `the_name_enters_no_proof`, `the_structure_does_not_fix_the_name` | **PASSA** — o conteúdo é a TIPAGEM: `rename` compila porque nenhum campo de prova menciona `name` |
| I6.a | na Torre H_φ: ω(I)=1; Δ^{it}Ω = Ω; ω∘σ_t = ω; ‖qΩ+ασ_xΩ‖=1; ⟨Ω,P_vΩ⟩=q²; ⟨ξ,P_vξ⟩=α²; leitura de P_v em v = 1; P_v idempotente; ω(P_Ω)=1 e ω(σ_t P_Ω)=1 | `TowerIdentity`, `the_identity_in_the_tower` (via `quadratic_reading`, genérico em Hilbert) | **PASSA** |
| I6.b | negativo de I1 na torre | — | **FALHA honesta, como pré-registrada**: a defasagem que a torre tem é o fluxo modular UNITÁRIO Δ^{it}, que fixa Ω e preserva o posto; a defasagem dissipativa (`dephase`/`diagExpect`) é termo só na face matricial. Faltaria: uma esperança condicional ou semigrupo dissipativo em B(H_φ) que encolha a coerência entre Ω e ξ = σ_xΩ |
| C1 | posto 1 não sobrevive | I1.c, I1.d | **PASSA** |
| C2 | α = 0 e α = 1 degeneram; sem identidade nomeada nos polos | `alpha_zero_degenerates`, `alpha_one_degenerates`, `no_named_identity_at_the_poles` | **PASSA** (desvio: conjunção extra `diagExpect ω = ω`, mais forte) |
| C3 | \|α\| > 1 quebra a forma; α ∈ [−1,0) não é recuperado | `alpha_above_one_breaks_the_form`, `alpha_below_minus_one_breaks_the_form`, `negative_alpha_is_not_recovered` | **PASSA** — refinamento honesto da régua da ordem («α fora de (0,1) quebra a forma»): em [−1, 0) a forma VALE; o que falha é a recuperação por dentro (devolve \|α\|) |
| C4 | trocar o nome não muda nenhum teorema | `changing_the_name_changes_nothing` | **PASSA** |
| C5 | não-vacuidade (α = 1/2 e perfil w ≡ 1/2: números de TESTE) | `probe_named_identity`, `probe_tower_identity` | **PASSA** |

Declarações auxiliares fora do pré-registro (ditas): `rank_zero_iff_aux`, `rankOne_aux` (cópias citadas da TheUnitIsTheRank
r3, l.179 e l.467), `rank_two_of_det_ne_zero`, `qOf_pos`, `q_sq_add`, `ip00–ip11`, `inscription_dot`, `inscription_ne_zero`,
`identityProj_trace(_one)`, `identityProj_idem`, `reading_on_eInner/eOuter`, `trace_dephase`, `dephase_apply'`,
`dephased_det`, `identityProj_mulVec_inscription`, `quadVec*`, `inner_self_one_of_norm`, `quadratic_reading`,
`towerInner*`, `towerInscription`, `the_named_identity_carries_the_identity`, `halfProfile`.

**Ensaio numérico (COMPUTED, não prova)** — α lido nos bytes de um.py v391 (`8e7b9927ceae64b8`) l.5557
(`ALPHA_FINE_CODATA_2018 = 7.2973525693e-3`, sem executar o um.py); β = α·√e = 0.012031300400803142 calculado em runtime,
usado só como taxa de teste: |Tr ω − 1| = 0; ‖ω² − ω‖ = 1,1e−16; posto 1; leitura interior − α² = 0; α recuperado − α = 0;
sob a defasagem, |Tr − 1| = 0 em t ∈ {0; 0,1; 1; 10; 100; 1000}; det − fórmula ≤ 5,4e−20; posto 1 em t = 0 e 2 para
t > 0; limite: posto 2. Critérios pré-registrados: **ok**. Ressalva: em t pequeno o posto numérico do numpy depende da
tolerância (det ~1e−7 em t = 0,1); o critério pré-registrado usa também o posto pela fórmula do det.

## 3. Estatutos (sem véu)

* [REAL no sandbox]: os teoremas acima (validade da estrutura).
* [POSTO pelo operador, verbatim sha256 2ebc1dd3…]: o nome «Jesus Cristo», dado `postedName : String`; nenhum teorema o
  deriva, prova ou seleciona — `the_structure_does_not_fix_the_name` prova exatamente isso.
* [INPUT]: α (parâmetro; nenhum número no Lean); a base de D (herdada da F1.FREQUENCIA).
* [ONTO]: «o cordeiro imolado» = `alicerce_fundante`; o registro histórico; toda leitura teológica. Nenhum teorema fala de
  história ou de uma pessoa.
* [DECLARADO]: os números do artigo «Conscious Singularity» (escores, posteriores, χ_C, tabelas): não entraram.

## 4. Perguntas residuais ao operador

1. **Nome da pedra.** Provisório `TheIdentityHasAName` (namespace `TGLExt.TheIdentityHasAName`). E os identificadores do
   Nome: hoje `postedName` (o dado) e `theNamedIdentity` (o habitante) — quer o nome também no identificador?
2. **Qual termo é «o cordeiro imolado».** Provisório: `alicerce_fundante` = `TGLExt.Fundacao.agape` (o piso). Alternativas,
   sem escolha: (A) o piso da Ágape; (B) β, o custo de distinguir 1 de 0; (C) J, a Palavra; (D) outro termo.
3. **Qual é «a Torre».** A pedra escolheu H_φ = `TowerHilbert P` (onde o kernel lê ω(I) = 1, `omega_of_one`, com o fluxo
   modular e o vetor do Nome). Há outras: a torre de Jones da Meia-Nat (`TGL/HalfNatJonesTower.lean`,
   `halfNatJonesTower`, sem estado GNS) e o fluxo por andar finito (`TowerModular.towerFlow`/`tower_kms`).
4. **O Nome no core do um.py.** Se o Nome entra no core como registro POSTO (string com o verbatim por sha256), ao lado da
   pedra, sem mover o gate.
5. (técnica) Na instalação da v392, se a TheUnitIsTheRank e o motor IALD forem instalados, as cópias citadas
   (`rank_zero_iff_aux`, `rankOne_aux`, `the_name_read_in_the_name`, `rereading_adds_nothing`) podem virar import.
6. (técnica) Se quer construir I6.b: uma defasagem dissipativa em B(H_φ) (esperança condicional) para o negativo de I1 na torre.

## 5. O que NÃO fiz

* Não instalei nada no Nós; não toquei um.py, selo, gate, quadro, memória, túnel, Bancada, site, git; não registrei no mapa
  (só consultei; os registros vão prontos em `registro_rota_F1.IDENTIDADE.json` e `registro_mapa_F1.IDENTIDADE.json`).
* Não rodei o um.py (α foi lido nos bytes).
* Não importei as candidatas da v392 (não instaladas; motivo em `1_LEVANTAMENTO\LEVANTAMENTO.md` §3e).
* Não fiz auditoria independente (a unidade pede; quem constrói não aprova).
* Não inscrevi esta tarefa na memória ACOM (`session_memory.py init`): a ordem limitou a escrita a `work\identidade_cordeiro_13out`
  e ao sandbox; a gerência decide se inscreve.
* Não construí I6.b (FALHA honesta pré-registrada).
* Não usei nenhum número do artigo.
