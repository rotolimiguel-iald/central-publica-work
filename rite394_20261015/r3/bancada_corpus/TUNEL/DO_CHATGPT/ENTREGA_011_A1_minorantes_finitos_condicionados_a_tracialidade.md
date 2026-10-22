[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Os minorantes finitos do mesmo peso, sob a hipótese tracial explícita

2026-09-15T00:28:08.109113-03:00

Dois teoremas públicos, quatro auxiliares privados, zero definições novas. A sequência concreta E_n=e_n q_n tem norma no máximo um, quadrados de peso limite finito e converge fortemente à identidade, sem assumir tracialidade. Sob a hipótese EXPLÍCITA htr para esse mesmo peso, os quadrados (E_n a)*(E_n a) fornecem o supremo dos minorantes positivos finitos de X=a*a, exatamente como exige o contrato existente.

A hipótese htr continua OPEN. Este resultado não a prova, não atribui minorantes ao peso dual não tracial, não afirma que E_n sejam positivos ou crescentes e não constrói o traço final. A redução anterior à igualdade no finiteDualStarCore é reutilizada. Nenhum peso, GNS, raiz independente, normalização, monólito, dado empírico ou gate foi introduzido ou alterado.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | NÃO PAGO por esta entrega. |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\finite_minorants_attempts\20260915_000942_447303\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseLimitFiniteMinorants']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\independent_20260915_001804_103532\run.json`. `697` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseLimitFiniteMinorants` | `fca7ff37994a84ee7cc5707f66d670c6cf46dadf9500da10f4f06fa932cc296c` | `50d723b08387ae93ebb573ca4cd83c29046da6bf6e504f91e4b8982e7b5c2c76` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarInverseLimitWeight_finite_contractions (P : TGLExt.SiteProfile) :
  ∃ E,
    (∀ (n : ℕ), LE.le.{0} (norm.{0} ↑(E n)) 1) ∧
      (∀ (n : ℕ), LT.lt.{0} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (E n))) Top.top.{0}) ∧
        ∀ (v : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
          Filter.Tendsto.{0, 0} (fun n => ↑(E n) v) Filter.atTop.{0} (nhds.{0} v)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_finite_minorants (P : TGLExt.SiteProfile)
  (htr :
    ∀ (a : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))),
      Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P a))
        (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (star.{0} a))))
  (X : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P X)
    (⨆ Y,
      ⨆ (_ : LE.le.{0} Y X),
        ⨆ (_ : LT.lt.{0} (TGLV350.Regular.scalarInverseLimitWeight P Y) Top.top.{0}),
          TGLV350.Regular.scalarInverseLimitWeight P Y)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_MINORANTES_FINITOS_A1B.json` — SHA256 `c3fc2cdfdab2175c10e5a2e0bb68abcd6ef182903bc509683d56ab0c64551aa3`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\REVIEW_A1_FINITE_MINORANTS_FINAL.json` — SHA256 `519ea4ee2cef2ce8f678dd2aa2fd3b5b4896df7551ab3f1e755ec98866dda4b1`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\compilation.json` — SHA256 `e1f4935bebe4f978c89908e23cd19922fa7ca03a45a89909ebffbf818829188b`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_FINITE_MINORANTS.json` — SHA256 `08c5ae584626e293e25de695845dd2749544a87ed583bbf1ad48e84e960fe095`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

2026-09-15T00:26:23.984933-03:00

**A1_FINITE_MINORANTS_REVIEW_ACCEPTED__TRACIALITY_PREMISE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Módulo e auditor próprios rc0; dois tipos completos com universos, axiomas do trio. Controle negativo próprio rc1 por Type mismatch.

[REAL — contrações incondicionais] O primeiro teorema recebe somente P. Constrói E_n=e_n q_n, com δ_n=1/(n+1)>0, média regular e_n e corte de domínio q_n antigos. Normas≤1 dão a contração; e_n∈nν e domainCut_finite do delta26 dão τ(E_n*E_n)<∞. bounded_application_tendsto combina q_n v→v e e_n v→v. Não exige tracialidade nem afirma que E_n seja positivo, projeção, crescente ou convergente em norma de operadores.

[REAL — hipótese explícita] O segundo teorema recebe htr : ∀a∈N, τ(a*a)=τ(aa*) e X : PositiveCoreInput P. Prova exatamente o campo de minorantes positivos finitos para o MESMO τ, condicionado a htr. Não fornece esse antecedente, não impõe tal propriedade ao peso dual não tracial ν e não constrói um habitante de RegularCoreTraceData.

[REAL — raiz e ordem] O auxiliar hilbert_core_square_source usa CFC.sqrt ambiental já existente, cfcₙ_mem e fechamento normado de N para obter a∈N com a*a=X. Não instala CompleteSpace no subtipo N nem cria outra raiz. Y_n=(E_n a)*(E_n a)≤X decorre de E_n*E_n≤I por conjugação positiva. Não comuta a com E_n ou com os reguladores; não usa ordem falsa dos conjugadores.

[REAL — usos de htr] Primeiro htr(E_n a) troca τ(Y_n) por τ((E_n a)(E_n a)*). A cota (E_n a)(E_n a)*≤‖a‖²E_n E_n* vem de a a*≤‖a‖²I. Monotonicidade e homogeneidade dão o bound; htr(E_n) troca τ(E_n E_n*) pelo valor finito τ(E_n*E_n). O escalar NNReal ‖a‖² é finito. Esses dois usos são explícitos, sem conversão de infinito para real ou finitude presumida de τ(X).

[REAL — passagem ao limite] E_n a→a fortemente. O bound sequencial de quadrados do delta27, com C o supremo de todos os minorantes finitos de X, dá τ(X)≤C porque cada Y_n participa dele. Não se exige que Y_n cresça, nem convergência dos adjuntos ou finitude de C. O sentido contrário é monotonicidade. A prova cobre τ(X)=∞.

[REAL — auxiliares e histórico] Quatro helpers privados genéricos: hilbert_square_norm_bound, hilbert_compressed_square_bound, hilbert_smul_one_le_one e hilbert_core_square_source. Auditados transitivamente pelos dois alvos. As 11 entradas da ficha e três do adendo foram conferidas por fonte/linha/pin; a ficha precede o código, o adendo declara posterioridade ao DEV e os adaptadores de instâncias. Quatro DEV rc1 por síntese de instâncias/coerções/rewrites foram preservados e excluídos. Pins históricos apontam os snapshots reais.

[REAL — controle próprio] BadFiniteMinorantsTraceRemoved foi copiado em bytes para V/ReviewControls e reproduzido após o Lake positivo. Retornou rc1 por Type mismatch ao omitir htr; imports funcionaram, sem erro de ambiente ou timeout. O controle autoral também foi relido e pinado. A recusa não demonstra impossibilidade de provar htr futuramente.

[REAL — proveniência] 697 objetos próprios preservados; 2 novos (alvo+auditor), total 699. Nenhum fornecedor antigo recompilado, nenhum objeto K/DEV herdado. Run 37.571 s; negativo 21.941 s. Zero avisos do alvo/auditor; 178 mensagens de fornecedores herdadas discriminadas. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui o negativo esperado. LEAN_PATH dos traces restrito a V/pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte K=snapshot=V | fca7ff37994a84ee7cc5707f66d670c6cf46dadf9500da10f4f06fa932cc296c |
| .olean próprio | 50d723b08387ae93ebb573ca4cd83c29046da6bf6e504f91e4b8982e7b5c2c76 |
| .olean autoral, só comparação | 50d723b08387ae93ebb573ca4cd83c29046da6bf6e504f91e4b8982e7b5c2c76 |

Igualdade binária medida: True.

[OPEN] Aceite dos dois tipos, quatro helpers transitivos e zero defs. Contrações finitas incondicionais; minorantes finitos condicionados a htr. Nenhum contrato habitado, nenhuma prova tracial global ou no núcleo. A1(b) continua aberto. 19 V351 são subconjunto das 940 entradas da base (937 Lean e três configurações), não 959 arquivos. Apenas novas saídas em V e nesta revisão. Fontes autorais, originais, V353, memórias, monólito, writers e pareceres anteriores preservados.

Tipos lidos:

~~~lean
theorem scalarInverseLimitWeight_finite_contractions (P : SiteProfile) :
    ∃ E : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, ‖(E n).val‖ ≤ 1) ∧
      (∀ n, scalarInverseLimitWeight P (positiveSquare P (E n)) < ⊤) ∧
      (∀ v, Tendsto (fun n => (E n).val v) atTop (𝓝 v))
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

~~~lean
theorem scalarInverseLimitWeight_finite_minorants (P : SiteProfile)
    (htr : ∀ a : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P a) =
        scalarInverseLimitWeight P (positiveSquare P (star a)))
    (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

Evidências:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\compilation.json>) — SHA256 e1f4935bebe4f978c89908e23cd19922fa7ca03a45a89909ebffbf818829188b.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\independent_20260915_001804_103532\run.json>) — SHA256 48d35240d4aa2d408ffa0b39303aed471f0aa620ba3b2e1cbc9910589361e6a6.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\independent_20260915_001804_103532\type_axiom_audit.json>) — SHA256 f1bc5210be9a230dd1861913576d75404630e7335d8563cf49e368dfb8365cfb.
- [negativo próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\negative_20260915_001942_763122\run.json>) — SHA256 11e4218228b5eefda81927dd5451ab2d5616651907f0986dc8e09cb960262cf1.
- [preservação19/940](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\preservation_19_940.json>) — SHA256 11606473972e5f0981846d0757cd6cb278403afcf7587fe0b6e5ef73abafb872.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_minorantes_finitos\history_read.json>) — SHA256 2216274f62af67ed7a6bf310422cf98f8f9f1acd223d0f6d42c102b13240c413.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_MINORANTES_FINITOS

[OPEN — ficha anterior aos minorantes finitos, condicional à tracialidade]

2026-09-14T23:59:19.278836-03:00

Same scalarInverseLimitWeight. First construct a sequence of contractions E_n=regularAverage(delta_n)*regularDomainCut(delta_n) with finite square weight and strong limit I using existing bounds/density. Then, EXPLICITLY conditional on traciality, prove the exact finite-positive-minorants field: tau(X)=sup{tau(Y):0<=Y<=X,tau(Y)<infinity}. For X=a*a with its existing CFC square root, use Y_n=(E_n a)*(E_n a) <= X. Finiteness follows by traciality, a a*<=norm(a)^2 I and positive homogeneity. Existing strong-square bound gives tau(X)<=sup tau(Y_n). No assumption that tau is tracial has been discharged here; no extra trace/GNS/root, no independent normalization, no completion of A1(b). Delta27 is author-validated, independent review pending at fiche creation; final acceptance of this consumer waits for27.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitSemifiniteness.lean:78` — `0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1`

```lean
theorem scalarInverseLimitWeight_domainCut_finite (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ)
    (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) < ⊤
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:38` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_bounds (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    0 ≤ (regularDomainCut P δ).val ∧ (regularDomainCut P δ).val ≤ 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongBoundedApplication.lean:15` — `dd68e70d90c4c475bfbe1770df5428666fd9345ed28b81c2addfef16f56017a0`

```lean
theorem bounded_application_tendsto {ι : Type*} (l : Filter ι)
    (A : ι → H →L[ℂ] H) (C : ℝ) (hbound : ∀ i, ‖A i‖ ≤ C)
    (v : ι → H) (v₀ w : H) (hv : Tendsto v l (𝓝 v₀))
    (hfixed : Tendsto (fun i => A i v₀) l (𝓝 w)) :
    Tendsto (fun i => A i (v i)) l (𝓝 w)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:55` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem HasFiniteDualSquare.scalar_finite (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hf : HasFiniteDualSquare A) :
    dualQuadraticIntegral (star A * A) (regularVacuum P) < ⊤
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitTracialExtension.lean:46` — `b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3`

```lean
theorem scalarInverseLimitWeight_square_le_of_strong (P : SiteProfile)
    (A : ℕ → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hlim : ∀ v, Tendsto (fun n => (A n).val v) atTop (𝓝 (S.val v)))
    (C : ℝ≥0∞) (hb : ∀ n, scalarInverseLimitWeight P (positiveSquare P (A n)) ≤ C) :
    scalarInverseLimitWeight P (positiveSquare P S) ≤ C
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:104` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_scale (P : SiteProfile) (r : ℝ≥0) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.scale r) = (r : ℝ≥0∞) * scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:109` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_mono (P : SiteProfile) (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseLimitWeight P X ≤ scalarInverseLimitWeight P Y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:57` — `6ec762be7f9014e45f88ffa9971a0e1672618f6d4289fb7e6247e5159a21e6b5`

```lean
theorem vonNeumann_norm_closed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    IsClosed (M : Set (H →L[ℂ] H))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:205` — `07acc928827e7fafe0ac6baa7cea89010f8e74854cd2f77ba0d5314e1823c388`

```lean
lemma cfcₙ_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [NonUnitalSubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfcₙ f a ∈ s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Order.lean:195` — `0802a500623d378e8c953961cac3c6391932515a7236d44dbceea11e2eb4611b`

```lean
lemma CStarAlgebra.mul_star_le_algebraMap_norm_sq {a : A} :
    a * star a ≤ algebraMap ℝ A (‖a‖ ^ 2)
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_finite_minorants\20260914_235857_539749\searches.json. Ausência nominal não é ausência universal. O helper de raiz privado de V351AllPositiveWeightOrder não é refeito como novo teorema: seu consumidor usa diretamente cfcₙ_mem e sqrt_mul_sqrt_self.


## Ficha/adendo integral: ADENDO_FICHA_MINORANTES_FINITOS

[OPEN — complemento após DEV e antes do aceite]

{
  "timestamp": "2026-09-15T00:09:42.132274-03:00",
  "status": "FICHE_ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE",
  "providers": [
    {
      "name": "regularAverage_tendsto_identity",
      "source": {
        "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V350RegularApproximation.lean",
        "bytes": 5911,
        "sha256": "d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44"
      },
      "line": 68,
      "statement": "theorem regularAverage_tendsto_identity (P : TGLExt.SiteProfile)\n    (v : RegularHilbert (TGLExt.TowerHilbert P)) :\n    Tendsto (fun h : ℝ => regularAverage P h v) (𝓝[≠] 0) (𝓝 v)"
    },
    {
      "name": "regularAverage_hasFiniteDualSquare",
      "source": {
        "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V350DualSemifiniteIdeal.lean",
        "bytes": 6938,
        "sha256": "63c88763eaa1c837ed0a28057d044a7627e57f993f4fcc4c7bddf44dcea07cbe"
      },
      "line": 108,
      "statement": "theorem regularAverage_hasFiniteDualSquare (P : TGLExt.SiteProfile)\n    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage P h)"
    },
    {
      "name": "CStarAlgebra.star_mul_le_algebraMap_norm_sq",
      "source": {
        "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\.lake\\packages\\mathlib\\Mathlib\\Analysis\\CStarAlgebra\\ContinuousFunctionalCalculus\\Order.lean",
        "bytes": 28173,
        "sha256": "0802a500623d378e8c953961cac3c6391932515a7236d44dbceea11e2eb4611b"
      },
      "line": 200,
      "statement": "lemma CStarAlgebra.star_mul_le_algebraMap_norm_sq {a : A} :\n    star a * a ≤ algebraMap ℝ A (‖a‖ ^ 2)"
    }
  ],
  "correction": "A ficha previu uso direto de CFC, sem helper. A primeira execução expôs falhas de síntese das instâncias no Lp concreto. Foram necessários QUATRO helpers privados genéricos: bound quadrático de norma (API CStar), compressão, escala real da unidade e fonte de quadrado CFC dentro de N. Este último reproduz apenas a adaptação de tipos já vista no helper privado de AllPositiveWeightOrder (não exportável), não outra raiz nem outro cálculo espectral. Nenhum deles é contado entre os DOIS teoremas públicos. Operações reais ficam genéricas antes da instanciação; a tentativa de converter tudo a escala complexa gerou ciclos RCLike/SMul e foi abandonada. Não aumenta orçamento de heartbeats. Todos os DEV rc1 preservados, final000736rc0 limpo.",
  "old_adapter": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V351AllPositiveWeightOrder.lean",
    "bytes": 4675,
    "sha256": "e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb"
  },
  "exact_consumer": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V351RegularCoreTraceContract.lean",
    "bytes": 5624,
    "sha256": "3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0"
  },
  "scope": "The finite-positive-minorant field still requires htr explicitly. E_n are actual finite-square contractions; no top-toReal or hidden traciality. No contract inhabitant, no change to trace gate. Finiteness proved by htr twice, norm bound, monotonicity and homogeneity; no positive-minorant condition imposed on nu."
}
