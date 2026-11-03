# REVISÃO R10 — CADEIA DO TRAÇO DA BANCADA (revisor distinto: Sonnet) — 02/11/2026

> **ESTADO: COMPLETO, dentro dos limites da §8** (a versão PARCIAL gravada antes foi regravada por esta). Auditoria adversarial **só-leitura**: não rodei `lake` nem `lean`, não toquei em `C:\t\k405c\final`, não escrevi nada além deste arquivo.
> Rótulos: **[REAL]** = li no código-fonte, no recibo ou medi por script de leitura; **[DERIVADO]** = dedução minha a partir de [REAL], não checada pelo Lean; **[DECLARADO]** = docstring, manifesto ou parecer da bancada, sem teorema próprio.
> Aliases (caminhos reais, com barra normal): **B** = `C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/` · **OR** = `B/orbital_rotation/attempts/` · **TF** = `B/takesaki_fock/attempts/` · **K** = `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/`. Os arquivos citados são os **que o recibo lista** (pastas `attempts/<carimbo>/`), não cópias de topo; as cópias de topo que conferi são idênticas.
> Memória ACOM: esta revisão não foi inscrita na ACOM (a ordem proíbe escrever qualquer outra coisa); declaro a omissão.

## 0. Resumo — o que muda decisão

1. **Os 21 campos estão habitados por construção, sem hipótese escondida; nenhum campo é SUSPEITO [REAL].** Fecho de 475 fontes sem `sorry/admit/axiom/opaque/native_decide/unsafe/implemented_by/extern/partial`; `#print axioms` das 11 declarações finais = só `propext, Classical.choice, Quot.sound`; as 474 compilações-dependência têm `exit_code 0`, fonte e `.olean` com SHA256 que conferem entre si e com o recibo final.
2. **O habitante é do TIPO do kernel, não de uma cópia alterada [REAL].** `CanonicalModularCoreAssemblyR1.lean` (onde mora `RemainingModularCoreInput`) e `CanonicalFockAssemblyR1.lean` (`CanonicalNetInput`) são idênticos aos de `K/F1Fecho394/` (a menos de prefixo de import e linhas em branco).
3. **Ressalva 1 — `trace` é um traço de verdade só no cone positivo.** Fora dele, é a extensão «supremo sobre os positivos shift-equivalentes» e vale **0** quando não há positivo na classe (ex.: `trace(−Pp)=0` com `trace(Pp)=1/2`, [DERIVADO]). Não é funcional linear (a bancada diz). Os 21 campos não pedem mais; o conteúdo «fiel, normal, semifinito» está no pacote `actualPositiveTrace`, que **não** faz parte do tipo.
4. **Ressalva 2 — P_F, Pp, Pm são uma escolha clássica sem vínculo físico [REAL].** `Classical.choose` sobre `normalized_split_exists`; não dependem de `D` nem do operador H_3L. Os campos legados `PF_locks`/`PF_maximal` (`K/O16/PhotonModularRealization.lean:103`) **não existem** no contrato de 21 campos. Ratificar R7 não ratifica «P_F = projeção do núcleo de H_3L».
5. **Ressalva 3 — «II_∞» não é provado nem pedido.** O docstring do campo `PF` diz «núcleo II_∞» [DECLARADO]; nenhum campo o exige; o parecer R7 lista a classificação como `not_claimed`.
6. **A construção é a da torre (V354) transportada [REAL]**, com insumos analíticos próprios do Fock (peso, lei quadrática por Tomita/polar, canto de Weyl).
7. **Rede física:** `K_local`, `K_translate`, `K_boost`, `wedge_glue` são TEOREMAS (não campos assumidos); a não-trivialidade está provada **só para a cunha direita**; **não encontrei** teorema de `K O ≠ ⊥` para `O` compacto (nem é exigido pelo tipo).
8. **Independência do R7:** autor e revisor são ambos agentes Codex; o próprio parecer admite que módulos R49/R51 «de autoria anterior do revisor» foram reutilizados com pareceres já pinados [DECLARADO]. Esta leitura é a primeira por outra família de modelo — mas sem compilação.
9. **Antes de integrar (R3):** 12 `#eval IO.FS.withFile` em 2 módulos do fecho; 300 módulos sem contraparte no kernel; `maxHeartbeats` até 3 000 000; recibo compilado contra o `.lake/build` do kernel de 16/10.

## 1. HIGIENE DO FECHO DE FONTES [REAL]

**Recibo** `OR/20261016T210640_174717Z/RECEIPT.json`: `exit_code 0`, 65,84 s, Lean 4.31.0, `readonly_dependencies_unchanged true`, `dependency_cache_unchanged true`, `production_modified false`. `dependencies` = 1422 entradas = 474 `.lean` + 474 `.olean` + 474 `RECEIPT.json` (um trio por compilação). Raiz: `OR/20261016T210640_174717Z/CanonicalFockModularCoreInputR1.lean`, sha256 `a3ebefa0a9d236ba…`, 7577 bytes (o do recibo e o da evidência de aceite R7).

**Integridade da cadeia (medida por script):**
- 474/474 `.lean` existem e o SHA256 recalculado = o do recibo (0 ausentes, 0 divergentes);
- fecho de imports locais a partir da raiz: **475/475** módulos alcançáveis (nada listado fica fora do fecho; nada importado fica fora da lista);
- para cada um dos 474 trios: o `RECEIPT.json` da compilação tem `exit_code 0`; o SHA da fonte registrado nele = o do `.lean` listado; o SHA do `.olean` registrado nele = o do `.olean` listado, e o arquivo em disco confere. (Três esquemas de recibo coexistem: 443 com `source.sha256`, 21 antigos de F1.REDE com `source_sha256`, 10 de F1.FECHO com `compiled_source`/`olean`; li os três.)
- `DEPENDENCY_CACHE.json`: 474 cópias, 0 divergências original×cópia; todos os originais são `.olean` listados;
- as 4 fontes citadas na evidência de aceite R7 (`NormalizedSplitR5`, `ModularCoreInputR1`, `CyclicTraceCompletionR3`, `ActualPositiveTracePackageR2`) têm SHA = o compilado = o da cópia de topo em `takesaki_fock/`; o `R52_R7_FULL_REVIEW_R1.json` tem o SHA citado no pedido de aceite (`76df7fce6f6f0e70…`).

**Varredura de tokens** (475 fontes, com comentários de bloco aninhados, comentários de linha e literais de cadeia removidos por analisador próprio):

| item | ocorrências em código |
|---|---|
| `sorry`, `admit`, `sorryAx`, `axiom`, `opaque`, `native_decide`, `nativeDecide`, `unsafe`, `implemented_by`, `extern`, `partial`, `ofReduceBool`, `trustCompiler` | **0** |
| `macro`, `elab`, `syntax`, `notation`, `macro_rules`, `elab_rules`, `declare_syntax_cat`, `initialize`, `builtin_initialize`, `addDecl`, `evalDecl`, `IO.Process`, `debug.skipKernelTC`, `skipKernelTC` | **0** |
| `structure`/`class`/`inductive` nos 300 módulos sem contraparte no kernel | **1** (`PositiveTraceData`, o pacote de saída); 0 classes |
| `instance` fora dos dicionários `ambient*/native*/fock*` | 3, todas benignas: `ScreenLorentzTransportR7.lean:14,18` (MeasurableSpace/BorelSpace de matrizes 2×2), `ScreenStrongContinuityR6.lean:15` (FirstCountable de `generatedLorentz`) |
| `run_cmd` | 38 — todos são **auditores de axiomas**: `collectAxioms`, `throwError "AXIOM_AUDIT_REFUSED"` se fora do trio, recusa `.axiomInfo` |
| `set_option` | `Elab.async false` (20), `autoImplicit false` (487), `linter.unusedSectionVars false` (15), `linter.unusedVariables false` (1: `RegularRightAverageR3.lean:6`), `maxErrors` 2–12, `maxHeartbeats` 200 000–3 000 000 (máx. em `ScreenOrientationDetRootR3.lean:8`; nenhum `0`), `synthInstance.maxHeartbeats` 100 000–1 000 000, `maxRecDepth 4000` (1: `FibreRootGraphR3.lean:8`). **Nenhum relaxa a verificação do kernel.** |
| `#eval` | 56 em 15 arquivos; 44 são `IO.println` de marcador |

**`#eval` com efeito (escrevem arquivo; não afetam provas):** 12 ocorrências de `#eval IO.FS.withFile "R7_stages.log" .append fun h => do` em
- `R7SineWindowClosureProbeR5.lean` linhas 20, 30, 43, 51, 64, 80, 96;
- `CanonicalFockPolarRightCutoffsR13.lean` linhas 18, 50, 68, 82, 98.
Ambos **estão** no fecho (R13 é importado por `CanonicalFockActualRightCutoffsR2`; Probe R5 por R13). Escrevem `R7_stages.log` no diretório de trabalho ao compilar. Remover antes de integrar.

**`AXIOMS.txt`** do recibo final [REAL]: `modularCoreInput`, `modularCoreInput_trace`, `modularCoreInput_trace_positive`, `modularCoreInput_PF_trace`, `physicalModularCoreInput`, `physicalFockCertificate`, `physical_core`, `physical_trace`, `physical_dual`, `physical_embedding`, `physical_net`: todas `[propext, Classical.choice, Quot.sound]`. O `#print axioms` percorre o fecho transitivo; um `sorry` apareceria como `sorryAx`.

**Comparação com o kernel:** dos 475 módulos, 174 são idênticos aos de `K/F1Fecho394/` (após normalizar o prefixo `TGLExt.F1Fecho394.` dos imports e linhas em branco); 1 difere só numa lista de auditoria (`CanonicalGammaNoFixedR4.lean:69`); 300 não têm contraparte. Todos os imports `TGLExt.*` existem como arquivo no kernel atual.

**Rótulos velhos:** quase todos os docstrings (inclusive o da raiz) dizem «DECLARADO / UNCOMPILED CANDIDATE». É rótulo de nascimento; vale o recibo.

## 2. NÃO-DEGENERAÇÃO DO TRAÇO

### 2.1 O que é `cyclicTraceCandidate` [REAL]
`OR/20261016T203505_683079Z/CanonicalFockCyclicTraceCompletionR3.lean:31-32`:
```
def cyclicTraceCandidate (a : core.toStarSubalgebra) : ℝ≥0∞ :=
  ⨆ (p : PositiveInput) (_ : ShiftRelated (positiveAsCore p) a), value p
```
Em palavras: o traço de `a` é o supremo de `value p` sobre todos os operadores positivos `p` do núcleo **shift-equivalentes** a `a`. Se não há nenhum, o supremo vazio é `0`. E `value p = inverseSupremum fockFlow regularFockVacuum p.val` (`TF/20261016T020751_052378Z/CanonicalFockInverseSupremumR2.lean:20`) `= ⨆ ε>0, cutoffWeight ε p` (`GeneralInverseSupremumR3.lean:14`), com `cutoffWeight ε X = dualQuadraticIntegral(√B_ε* X √B_ε)(vácuo)` e `B_ε = ε⁻¹·θ_{log ε}((1+h)⁻¹)`, o corte do gerador inverso (`GeneralInverseCutoffWeightR3.lean:18`; `GeneralRegularInverseCutoffR1.lean:15`).

`ShiftRelated a b := ∃ n>0, ∃ r s, a*r = r*b ∧ s*a = b*s ∧ a^n = r*s ∧ b^n = s*r` (`K/V354TraceShiftEquivalence.lean:11-13`): equivalência de deslocamento. Provados: `refl` :18, `symm` :21, `trans` :25, `cyclic` :62 (`x*y ~ y*x` com n=1, r=x, s=y), `map` :66, `star_transport` :75.

### 2.2 Em positivos [REAL]
`cyclicTraceCandidate_positive` (R3 :137): `cyclicTraceCandidate (positiveAsCore p) = value p`, valores infinitos incluídos. A parte analítica é `positiveShift_value_compatible` (`OR/20261016T201551_615339Z/CanonicalFockPositiveShiftTransportR2.lean:105`): positivos shift-relacionados têm o mesmo `value`. Usa o polar limitado do kernel (`boundedPolar_transports_shift_factors`, `K/V354PolarIntertwining.lean:59`) para obter `u` com `p = u q u*` e `u*u q = q`, e então `W(a*a)=W(aa*)` com `a = u√q` (`positive_transport_square_pair` :31).

### 2.3 A lei tracial `inverseSupremum_tracial` [REAL]
`OR/20261016T194835_820345Z/CanonicalFockActualTracialExtensionR1.lean:56`: `∀ a ∈ core, W(a*a)=W(aa*)`, `W = inverseSupremum fockFlow regularFockVacuum`. Mecanismo: (i) redução ao «star-core finito» por médias regulares + Fatou (`inverseSupremum_tracial_iff_finiteStarCore` :40, via `inverseSupremum_tracial_iff_core` em `GeneralInverseFiniteApproximationR1`); (ii) no star-core finito, a igualdade vem do polar de Tomita e do balanço modular (`inverseSupremum_star_core`, `OR/20261016T194440_801316Z/CanonicalFockActualStarCoreTracialR1.lean:114`, com `CanonicalFockActualModularBalanceR6`). A premissa «vácuo fixo» da redução é consumida por `CanonicalFockWeightInvariance.fibre_boost_fixes_regularVacuum` (`CanonicalFockWeightInvarianceR4.lean:21`), **não** assumida.

### 2.4 `trace_tracial` para todo x y [REAL]
`cyclicTraceCandidate_cyclic` (R3 :48) = `cyclicTraceCandidate_related (ShiftRelated.cyclic x y)`. Vale para **todo** par do núcleo, não só positivos. O mecanismo `ShiftRelated` não exclui nada (`x*y ~ y*x` sempre vale); o preço é o valor nos não-positivos (§2.7).

### 2.5 `trace_dual_scaling`: de onde vem [REAL]
`cyclicTraceCandidate_dual` (R3 :105) ← `value_dual` (InverseSupremumR2 :28) = `inverseSupremum_dual` (`GeneralInverseSupremumR3.lean:71`) ← `cutoffWeight_dual` (`GeneralInverseCutoffWeightR3.lean:90`: `cutoffWeight ε (θ_s X) = e^{-s}·cutoffWeight (ε e^{-s}) X`) + reindexação do supremo sobre reguladores (`supremum_rescale` :58). O fator `e^{-s}` nasce da covariância do gerador `h` (`θ_s(h)=e^{-s}h`: `GeneralRegularDualScalingR2.lean`, `regularPositiveGenerator_dual_graph`/`_scaling`; `regularInverseGeneratorCutoff_dual`, `GeneralRegularInverseCutoffR1.lean`). **É construção, não normalização nem hipótese.** O gerador `h` é definido pelas coordenadas espectrais do fluxo (`GeneralRegularPositiveGraphR2.lean`, `regularSpectralCoordinates`, `regularSpectralResolvent` = multiplicador `sigmoid(2πx)`); o docstring de `GeneralRegularDualScalingR2` (l.1-3) avisa que a covariância do grafo, sozinha, não é o teorema de escala do traço — o teorema de escala está em `cutoffWeight_dual`/`inverseSupremum_dual`, como acima.

### 2.6 Não-degeneração: o que existe [REAL]
- `value_one : value one = ⊤` (`TF/20261016T040057_201809Z/CanonicalFockInverseNormalR1.lean:29`; por escala dual + fidelidade + `positive_cone_nontrivial`, `CanonicalFockDualWeightR3.lean:95`); reexportado como `actualPositiveTrace_unit_infinite` (`OR/20261016T201541_365276Z/CanonicalFockActualPositiveTracePackageR2.lean:147`).
- `exists_positive_finite : ∃ Y, 0 < value Y ∧ value Y < ⊤` (PositiveTracePackageR2 :130; de semifinitude `value_finite_minorants` + `value_one=⊤`).
- `value_faithful` (InverseSupremumR2 :55), `cyclicTraceCandidate_positive_faithful` (R3 :149), `cyclicTraceCandidate_zero` (R3 :145).
- `modularCoreInput_PF_trace : trace PF = 1` e `modularCoreInput_trace_positive` (ModularCoreInputR1; no recibo).
- Pacote `PositiveTraceData` de dez campos, preenchido por `actualPositiveTrace` (PositiveTracePackageR2 :90-121): zero, aditiva, homogênea, monótona, fiel, normal (IsLUB), semifinita, tracial, escala dual. **Esses dez campos são do cone positivo e NÃO estão no tipo `RemainingModularCoreInput`.**
Logo `trace` não é identicamente `0` (`trace PF = 1`) nem identicamente `⊤`.

### 2.7 Onde o «traço» é ad hoc [DERIVADO — dedução minha, não checada no Lean]
Por definição (supremo vazio = 0), `cyclicTraceCandidate a = 0` quando nenhum positivo é shift-relacionado a `a`. Exemplo: seja `e` projeção não nula; então `−e` nunca é shift-relacionado a um positivo `p`. Prova: de `p r = r(−e)` e `p ≥ 0` segue, para `x ∈ ran e`, `⟨rx, p r x⟩ = −‖rx‖² ≥ 0`, logo `r e = 0`; de `(−e)^n = s r` segue `(−e)^n e = s r e = 0`, logo `e = 0`. Portanto `trace(−Pp)=0` enquanto `trace(Pp)=1/2`; analogamente `trace(i·Pp)=0`. Consequências: (a) **não é funcional linear nem ℂ-homogêneo** (o parecer R7 declara «não linear»); (b) o tipo de 21 campos não exige nada disso; (c) quem ler `trace` como traço de Dixmier/Takesaki deve ler a restrição ao cone positivo, onde o Lean certifica `fiel + normal + semifinito + tracial + escala e^{-s}`. Se o núcleo for um fator (Connes–Takesaki, [KNOWN] para M tipo III₁; **não provado aqui**), isso identifica `value` como «o» traço a menos de escalar; sem fatorialidade provada, a unicidade não é formal.

### 2.8 É a mesma construção da torre? [REAL]
Sim, transposta linha a linha: `K/V354CyclicTraceCompletion.lean:15-17` define `cyclicTraceCandidate P a := ⨆ (p : PositiveCoreInput P) (_ : ShiftRelated (asCore p) a), scalarInverseLimitWeight P p`, com os mesmos lemas (`positiveTrace_le_…`, `_related`, `_cyclic`, `_star`, `_dual`, `_zero`, `_positive_faithful`); `transport_square_pair` (`K/V354PositiveTraceTransport.lean:10`, privado) é a mesma prova de `positive_transport_square_pair` (PositiveShiftTransportR2 :31); `positiveShift_value_compatible` transpõe `positiveShift_trace_compatible` (`K/V354PositiveShiftCompatibility.lean:13`).
**Diferenças de substância:** (1) o peso positivo: `inverseSupremum fockFlow regularFockVacuum` no lugar de `scalarInverseLimitWeight P`; (2) a lei quadrática entra por Tomita/polar + média regular/Fatou (Fock), não por `V351QuadraticTrace:243` (torre); (3) `cyclicTraceCandidate_zero` sai de `value_zero` (Fock), na torre do argumento de nilpotência (`selfAdjoint_related_zero`, :111); (4) não há `SiteProfile` nem equivalência Fock–torre. O kernel guarda o muro `positiveTraceReader_not_cyclic` (`K/V354TraceReaderWall.lean:13`: estender o peso positivo por 0 NÃO é cíclico); a bancada não o contorna nem o viola: não estende por 0, toma o supremo sobre a classe de shift.

### 2.9 Hipótese nomeada escondida? [REAL — busca feita]
Procurei: `structure|class|inductive` nos 300 módulos novos (só `PositiveTraceData`, estrutura de saída); `variable`/`include … in` com hipóteses (existem em módulos de redução, p.ex. `GeneralInverseFiniteApproximationR1.lean`, e são descarregadas — o termo final `modularCoreInput` é fechado e `#print axioms` não traz nada além do trio); `Prop` não provado: nenhum `sorry`/`axiom`. **Não encontrei** hipótese escondida. A estrutura `UnitaryFlow` do kernel (`K/F1Fecho394/RegularCovariantCoreR3.lean:12`) tem campos `U, zero, add, strong` (um fluxo unitário fortemente contínuo) e `fockFlow` a instancia por `Γ(B0(−2πt))` (`CanonicalFockRegularCoreR2.lean`), não por hipótese.

## 3. P_F E AS METADES [REAL]

- **Fonte do canto nilpotente (Weyl):** `normalized_pair`/`phase_half_pi` (`WedgeNonabelianR4`) dão `f,g` na cunha com `W(g)W(f) = −W(f)W(g)`; `X=W f`, `U=W g`, `A = X+X*` auto-adjunto e **não nulo** (`weyl_real_part_ne_zero`, `OR/20261016T204338_618085Z/CanonicalFockMatrixCornerR2.lean:136`, via `⟨Ω,(W f+W f*)Ω⟩ = 2·exp(−‖f‖²/2) ≠ 0`); `U A U* = −A`; `nilpotent_of_sign_flip` (:33) produz `T = A⁺U ≠ 0` com `T²=0` (`wedge_nilpotent_exists` :147), transportado pela representação fibra injetiva (`core_nilpotent_exists` :179); `matrix_corner_of_square_zero` (`MatrixCornerFromNilpotentR3.lean:51`) dá projeção `e≠0` e `v` com `v*v=e`, `e v=0` (`core_matrix_corner` :192).
- **Projeção finita:** `finite_subprojection_exists` (`OR/20261016T204544_576190Z/CanonicalFockFiniteProjectionR3.lean:74`) usa a semifinitude (`value_finite_minorants`) e o limiar espectral genérico do kernel (`positive_operator_has_threshold_projection`, `K/V354SpectralThreshold.lean:16`): `q ≤ e`, `0 < value q < ⊤`.
- **Metades iguais:** `finite_equal_split_generic` (`OR/20261016T210351_533600Z/CanonicalFockNormalizedSplitR5.lean:91`): `a = v q`, `a*a = q`, `r = a a*` é projeção ortogonal a `q` (`compressed_corner_algebra` :35); `value q = value r` pela lei tracial `value_tracial`. **Vem de equivalência de Murray–von Neumann + tracialidade, não de simetria escolhida.**
- **Normalização `trace PF = 1`:** `dual_calibration` (FiniteProjectionR3 :121): `value(θ_{log (value X).toReal} X) = 1`. É **calibração** (escolha de `s = log trace(q+r)`) pela escala `e^{-s}`: legítima porque a escala existe; o «1» é escolhido, não derivado.
- **`normalized_split_exists`** (SplitR5 :225) é `∃ q r`; o habitante usa `Classical.choose` (`leftPositive` :51, `rightPositive` :52, `chosen_split` :55, em `OR/20261016T210640_174717Z/CanonicalFockModularCoreInputR1.lean`): `PF = positiveAsCore (add leftPositive rightPositive)`. **P_F é uma escolha clássica**, sem vínculo a `D` nem a H_3L.
- **No-go respeitado:** `dualInvariant_PF_no_go` (`K/O16/PhotonModularRealization.lean:170`). Aqui `trace_dual_scaling` + `trace PF = 1` já implicam `θ_1 PF ≠ PF` (o traço de `θ_1 PF` é `e^{-1}`): P_F não é dual-invariante, nem poderia ser. O tipo legado `ThreeLocksCoreData` (mesmo arquivo :103) tinha `PF_locks` (`PF*H3Lt=0`) e `PF_maximal`; **o contrato novo não os tem**.

## 4. A REDE FÍSICA `physicalCanonicalNet` [REAL]

`OR/20261016T120556_913253Z/PhysicalCanonicalNetCompleteR1.lean:212-221` (a cópia de topo é idêntica; o fragmento `PhysicalCompactNetAssemblyR1.lean:29` do brief é o mesmo texto, composto em `Complete…R1` — por isso não aparece sozinho na lista de dependências):
```
def physicalCanonicalNet : CanonicalNetInput where
  toLightNetData := { helicity := 1; helicity_light := Or.inl rfl
    K := compactPhysicalNet; K_mono := compactPhysicalNet_mono
    K_local := compactPhysicalNet_local; K_translate := compactPhysicalNet_translate
    K_boost := compactPhysicalNet_boost }
  wedge_glue := compactPhysicalNet_wedge_glue
```
- **O que é `K O`:** `compactPhysicalNet O := compactLocalized (coordinateRegion O) : Submodule ℝ H1` (`OR/20261016T110116_862115Z/PhysicalCompactNetGeometryR1.lean:19`), onde `compactLocalized O` (`OR/20261016T105021_400439Z/PhysicalCompactNetCovarianceR1.lean:20`) é o **fecho topológico do span real** das imagens `circularSmear f` (`PhysicalSmearTranslationR2.lean:59`) de campos-teste de Maxwell `SchwartzTensor` **reais** (`IsRealTest`, `RealSchwartzTestsR1.lean:28`), de **suporte compacto** com `tsupport f ⊆ O`. Rede de Maxwell livre em Minkowski, helicidade 1.
- **`K_mono`, `K_translate`, `K_boost`:** teoremas (`compactPhysicalNet_mono`, `_translate`, `_boost`, GeometryR1 :26-42), provados pela covariância do alisamento (`compact_translated_generator`, `compactLocalized_translate_iff` — CovarianceR1; `compact_lorentz_generator`, `compactLocalized_lorentz_iff`; `circularSmear_translate`, `circularSmear_lorentz`). **Provados, não supostos.**
- **`K_local`:** teorema `compactPhysicalNet_local` (:201) por `compactLocalized_locality` (:176) ← `GenericSymplecticSpan.closed_spans_zero` ← `physical_compact_spacelike_zero` (:45; cobertura finita por cunhas opostas, `spacelike_pair_opposite_wedges`). `SpacelikeSep O P := ∀x∈O, ∀y∈P, minkowskiSq(x−y)<0` com assinatura `(+,−,−,−)` (`K/O16/PhotonWitness.lean:49-55`): separação estritamente tipo-espaço.
- **`wedge_glue`:** `compactPhysicalNet rightWedge = KWR` por `compactLocalized_rightWedge_eq` (:153; cortes + deslocamento interno + continuidade forte) e `physical_right_wedge_eq_KWR` (`PhysicalCanonicalWedgeEqualityR3.lean:27`).
- **Não-trivialidade:** `physical_canonical_net_nonzero` (:226) e `physical_canonical_net_zero_refused` (:230) — **só para a cunha direita** (herdam `canonical_wedge_nonzero`, `K/F1Fecho394/CanonicalFockAssemblyR1.lean:35`). **Não encontrei** teorema de `K O ≠ ⊥` para `O` compacto (busca por `compactPhysicalNet|compactLocalized|compactSupportedGenerators` junto de `≠ ⊥`, `ne_bot`, `≠ 0`, `nonzero`, `nontrivial` nos 475 módulos: 0 acertos). O tipo `LightNetData` (`K/QGSolutionComplete.lean:49-57`) não o exige.
- **Hipóteses físicas:** nenhuma entra como campo ou `variable`: não há «fonte» escolhida, nem estrutura Maxwell assumida; `SchwartzTensor := 𝓢(Spacetime, TensorValue)` (`SchwartzMaxwellCoefficientR5.lean:15-16`) e `H1` são construídos. O docstring (:11-14) [DECLARADO] diz: «free Maxwell net in Minkowski. It does not construct a device reduction, curved H3, a trace, or a stress-energy charge»; (:190-193) «Other Fock, trace and Maxwell charge certificates are separate obligations».
- **Acoplamento com o núcleo:** só por `wedge_glue` (a cunha direita da rede = `KWR`, o mesmo `M = R(KWR)` do núcleo regular `core := generatedAlgebra (fibre '' M ∪ range regularUnitary)`, `K/F1Fecho394/RegularCovariantCoreR3.lean:110-113`). `PF`, `Pp`, `Pm` e `trace` não dependem de `D`.
- `physicalModularCoreInput := modularCoreInput physicalCanonicalNet`; `physicalFockCertificate := physicalModularCoreInput.toCertificate`; `physical_core/trace/dual/embedding/net` são `rfl`.

## 5. O ESCOPO DO PARECER R7 × O CONTRATO TIPADO

Parecer `B/mission_review_20261016/R52_R7_FULL_REVIEW_R1.json` [DECLARADO]: veredito `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE`, revisor `codex-mission-memory-review` (autor das fontes novas: `codex-fock-r6-review`), `filled_field_count 21`, `blocking_findings []`, `new_axiom_report_count 14`. `trace_scope.not_claimed`: (i) funcional complexo linear em todo o core; (ii) aditividade total fora do cone positivo; (iii) classificação do fator como tipo II∞; (iv) equivalência do core Fock com SiteProfile. `remaining_outside_R7`: R5 integral (Poincaré pleno, dispositivo), R8 (Maxwell/carga/tensor), H3 universal/curvo, rito final. Aceite registrado em `R52_R7_ACCEPT_RECEIPT_R1.json` (revisão 404), «submitted_by codex-gerente-tgl, reviewed_by codex-mission-memory-review».

**Cada ausência importa para o tipo de 21 campos?** (leitura do tipo em `K/F1Fecho394/CanonicalModularCoreAssemblyR1.lean:47-70`)
- **(i) não-linear:** não importa. Nenhum campo pede linearidade: `trace_zero`, `trace_tracial` (∀ x y), `trace_star`, `trace_dual_scaling` são propriedades de função; `trace_additive` é só `trace PF = trace Pp + trace Pm`.
- **(ii) sem aditividade fora do cone:** não importa. `PF, Pp, Pm` são positivos; a soma é a de `value_add` no cone (`CanonicalFockActualInverseAdditivityR2.lean`, via `cutoff_antitone`, provada). Nenhum campo soma elementos não positivos.
- **(iii) sem II∞:** não importa para o tipo (nenhum campo o pede); importa para a **leitura**: o docstring do campo `PF` (:54) diz «núcleo II_∞», e fatorialidade/tipo III₁→II_∞ é [KNOWN] (Connes–Takesaki) mas não está provada aqui. É o único ponto em que o texto do contrato diz mais do que os campos exigem.
- **(iv) sem equivalência Fock–torre:** não importa; o tipo fala só de `RepresentedCore` (Fock).
- **O que o tipo NÃO pede e o parecer cobre:** fidelidade, normalidade e semifinitude do traço (estão em `actualPositiveTrace`, fora do tipo). Quem consumir só `RemainingModularCoreInput` não pode contar com elas; quem consumir o habitante, pode.
- **O que o tipo NÃO pede e o parecer NÃO cobre:** que `PF` seja a projeção espectral do zero de H_3L (campos `PF_locks`/`PF_maximal` do legado ausentes); isso é o elo `link_PkerK_PF` (conferência v376), outro.
- **Critério do R7** («Takesaki na representação pretendida; produto cruzado; ação/peso/traço entrelaçados; escala V351 reutilizada»): [REAL] `core` é a álgebra gerada em `L²(ℝ;Fock)` por `fibre M` e pelos unitários regulares do fluxo `Γ(B0(−2πt))` (RegularCovariantCoreR3 :110-113; CanonicalFockRegularCoreR2), com ação dual e `value` entrelaçados por `cutoffWeight_dual`; a «escala V351 reutilizada» é a mesma forma `e^{-s}` e o mesmo molde, não uma equivalência com a torre.
- **Independência:** `reviewer_is_distinct: true` é distinção de papel (ambos Codex). O parecer admite: «Extensão R49 e cyclic R51 de autoria anterior do revisor são reutilizadas somente com pareceres independentes já pinados» [DECLARADO]. Isto não invalida o recibo (que é máquina), mas o juízo «independente» do R7 é o mais fraco dos elos; esta revisão cobre R49/R51 (§2.3, 2.8).

## 6. VEREDITO CAMPO A CAMPO (21)

Critério: HONESTO = construção genuína, sem hipótese escondida, enunciado do tipo cumprido tal como tipado; HONESTO COM RESSALVA = o enunciado do tipo é cumprido, mas há uma leitura que o termo não sustenta; SUSPEITO = nenhum caso.

| # | campo | veredito | fonte e nota |
|---|---|---|---|
| 1 | `trace` | **HONESTO COM RESSALVA** | `cyclicTraceCandidate` (R3 :31). Genuíno e fiel/normal/semifinito **no cone positivo**; fora dele, extensão por classe de shift (0 sem positivo na classe); não linear (§2.7). |
| 2 | `trace_zero` | HONESTO | R3 :145 (`cyclicTraceCandidate_positive zero` + `value_zero`). |
| 3 | `trace_tracial` | HONESTO | R3 :48, `ShiftRelated.cyclic` (`K/V354TraceShiftEquivalence.lean:62`); ∀ x y. A substância analítica está em `positiveShift_value_compatible` + `inverseSupremum_tracial`. |
| 4 | `trace_star` | HONESTO | R3 :64, `star_transport` (:75). |
| 5 | `trace_dual_scaling` | HONESTO | R3 :105; escala sai da covariância de `h` (§2.5). |
| 6 | `PF` | **HONESTO COM RESSALVA** | `positiveAsCore (add leftPositive rightPositive)`; `Classical.choose`; sem vínculo a `D` nem a H_3L; `trace=1` é calibração dual. |
| 7 | `PF_sa` | HONESTO | soma de projeções ortogonais (`chosen_sum_projection`, `IsStarProjection.add`). |
| 8 | `PF_idem` | HONESTO | idem. |
| 9 | `PF_ne` | HONESTO | de `trace PF = 1` e `trace 0 = 0` (`chosen_sum_ne_zero`). |
| 10 | `PF_pos` | HONESTO | `chosen_sum_trace` (`trace PF = 1`). |
| 11 | `PF_fin` | HONESTO | idem (`ENNReal.one_lt_top`). |
| 12 | `Pp` | **HONESTO COM RESSALVA** | `positiveAsCore leftPositive`; `Classical.choose` (a metade é uma entre muitas possíveis). |
| 13 | `Pm` | **HONESTO COM RESSALVA** | `positiveAsCore rightPositive`; idem. |
| 14 | `Pp_sa` | HONESTO | `chosen_split.1`. |
| 15 | `Pp_idem` | HONESTO | idem. |
| 16 | `Pm_sa` | HONESTO | `chosen_split.2.1`. |
| 17 | `Pm_idem` | HONESTO | idem. |
| 18 | `split` | HONESTO | `rfl` (PF definido como a soma). |
| 19 | `orth` | HONESTO | `chosen_split.2.2.1`: `q r = 0` por construção (`r = a a*`, `q a = 0`, `compressed_corner_algebra`). |
| 20 | `trace_additive` | HONESTO | `value_add` (aditividade no cone positivo via antitonicidade dos reguladores) + `cyclicTraceCandidate_positive` nos três positivos. |
| 21 | `equal_halves` | HONESTO | equivalência de Murray–von Neumann + `value_tracial` (SplitR5 :91-123). |

**Nenhum campo SUSPEITO.** Quatro com ressalva (1, 6, 12, 13), todas de LEITURA, nenhuma de validade formal.

## 7. O QUE A GERÊNCIA DEVE LER COM OS PRÓPRIOS OLHOS ANTES DE RATIFICAR

1. A **definição** `CanonicalFockCyclicTraceCompletionR3.lean:31-32` e `ShiftRelated` (`K/V354TraceShiftEquivalence.lean:11-13`) — são 5 linhas e são o que «o traço» é fora do cone positivo (§2.7 explica o que isso significa).
2. O **tipo** (`K/F1Fecho394/CanonicalModularCoreAssemblyR1.lean:47-70`) e o **habitante** (`OR/20261016T210640_174717Z/CanonicalFockModularCoreInputR1.lean:77-105`), lado a lado; em especial que `PF/Pp/Pm` saem de `Classical.choose` (l.51-53) e que não há campo de vínculo com H_3L.
3. A **calibração** `dual_calibration` (`CanonicalFockFiniteProjectionR3.lean:121-130`) e `normalized_split_exists` (`CanonicalFockNormalizedSplitR5.lean:225-233`): o «1» do traço de P_F é escolhido por `s = log trace(q+r)`.
4. O **`AXIOMS.txt`** do recibo final (2900 bytes) e o `RECEIPT.json` (`exit_code 0`, `readonly_dependencies_unchanged true`).
5. A decisão sobre o **docstring «núcleo II_∞»** do campo `PF` (`CanonicalModularCoreAssemblyR1.lean:54`): ou se prova a fatorialidade/tipo, ou o texto fica como [KNOWN]/[DECLARADO] e não como resultado do habitante.
6. Antes do R3 (integração): remover os 12 `#eval IO.FS` (§1), decidir o que fazer com os 300 módulos novos e com `maxHeartbeats` até 3 000 000, e refazer o build contra o kernel **atual** (o recibo usou o `.lake/build` de 16/10).

## 8. LIMITES DESTA REVISÃO (o buraco fica dito)

- **Não compilei nada.** Tudo sobre o Lean vem do recibo (`exit 0`, `AXIOMS.txt`) e da leitura do código. A correção do verificador do Lean e das instâncias do Mathlib é suposta.
- **Li integralmente** (linha a linha) 17 módulos: `CanonicalFockModularCoreInputR1`, `CanonicalFockCyclicTraceCompletionR3`, `CanonicalFockPositiveShiftTransportR2`, `CanonicalFockActualTracialExtensionR1`, `CanonicalFockActualStarCoreTracialR1`, `CanonicalFockActualPositiveTracePackageR2`, `CanonicalFockInverseNormalR1`, `CanonicalFockInverseSupremumR2`, `GeneralInverseSupremumR3`, `GeneralInverseCutoffWeightR3`, `CanonicalFockMatrixCornerR2`, `CanonicalFockFiniteProjectionR3`, `CanonicalFockNormalizedSplitR5`, `PhysicalCanonicalNetCompleteR1`, `PhysicalCompactNetGeometryR1`, `PhysicalCompactNetCovarianceR1`, `CanonicalModularCoreAssemblyR1` (kernel). **Li em parte** (cabeçalhos e enunciados): `GeneralRegularInverseCutoffR1`, `GeneralRegularDualScalingR2`, `GeneralRegularPositiveGraphR2`, `GeneralInverseFiniteApproximationR1`, `CanonicalFockActualInverseAdditivityR2`. Os demais ~450 módulos foram **varridos mecanicamente** (§1), não lidos: não afirmo ter lido as provas de `value_finite_minorants`, `actual_balance`, `actual_modular_implementation`, `matrix_corner_of_square_zero`, `compactLocalized_locality` etc.; afirmo só o que seus enunciados, recibos e o `#print axioms` mostram.
- **Não reauditei** os módulos `TGLExt.*` do kernel de que o fecho depende (130 importados; p.ex. `dualQuadraticIntegral` em `V350DualWeightForm`, o polar `boundedPolar`); são selados no kernel (v405). Também não verifiquei se seguem byte-idênticos ao `.lake/build` usado no recibo.
- **[DERIVADO]** na §2.7 é minha dedução em 6 linhas; recomendo conferi-la ou pedir o enunciado ao Lean antes de citá-la como resultado.
- Não li a conferência `CONFERENCIA_DO_LEVANTAMENTO_02nov.json` nem o `AVISO_GERENCIA.md`; usei o levantamento prévio só como mapa (todas as citações de arquivo:linha acima foram reabertas por mim).
- Esta revisão não é aceite, ratificação nem mexe em gate. O estatuto da bancada continua `[DECLARADO]` até a gerência conferir; o que aqui é [REAL] é leitura de recibo e código por um revisor, não prova nova.
