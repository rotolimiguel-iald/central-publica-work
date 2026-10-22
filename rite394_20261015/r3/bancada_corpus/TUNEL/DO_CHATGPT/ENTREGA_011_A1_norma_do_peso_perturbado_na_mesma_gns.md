[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A norma do peso perturbado na inscrição GNS original

2026-09-14T21:49:26.533724-03:00

Dois teoremas, sem definições nem auxiliares privados novos. Para A no domínio nν e b na álgebra direita construída, ν(b* A*A b) é a norma quadrada de π(b*)J⁻¹Λν(A). A igualdade consome o domínio/ação direita, a norma da inscrição GNS e a isometria do mesmo fator polar. A raiz original do corte inverso instancia o resultado com ε>0; sua pertença e a ação direita são produzidas pelos fornecedores aceitos.

O enunciado vale nos quadrados de elementos de nν. Não afirma a extensão a todos os positivos, a monotonicidade em ε, a tracialidade ou um habitante do contrato final. J⁻¹ é preservado e não é identificado com outro espelho por nome. A1(b) completo permanece aberto, sem mudança de gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\perturbed_weight_norm_attempts\20260914_214125_787904\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1PerturbedWeightNorm']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\independent_20260914_214502_008278\run.json`. `667` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351PerturbedWeightNorm` | `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9` | `255acd9ac47731cd2392d5232faa392029577d41be032960974820cdec316dad` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarWeight_right_perturbed_norm (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) b)
  (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  Eq.{1}
    (TGLV350.Regular.dualQuadraticIntegral
      (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (star.{0} ↑b) (HMul.hMul.{0, 0, 0} (star.{0} ↑↑A) ↑↑A)) ↑b)
      (TGLV350.Regular.regularVacuum P))
    (ENNReal.ofReal
      (HPow.hPow.{0, 0, 0}
        (norm.{0}
          (((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} b))
            ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.scalarTomitaPolarFactor P))
              ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))))
        2))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarWeight_inverseCutoff_perturbed_norm (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε)
  (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  ∃ (hb :
    Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P)
      (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε))),
    Eq.{1}
      (TGLV350.Regular.dualQuadraticIntegral
        (HMul.hMul.{0, 0, 0}
          (HMul.hMul.{0, 0, 0}
            (star.{0} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε)))
            (HMul.hMul.{0, 0, 0} (star.{0} ↑↑A) ↑↑A))
          (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε)))
        (TGLV350.Regular.regularVacuum P))
      (ENNReal.ofReal
        (HPow.hPow.{0, 0, 0}
          (norm.{0}
            (((TGLV350.Regular.scalarGNSRepresentation P)
                (star.{0}
                  (Subtype.mk.{1}
                    (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε)) hb)))
              ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.scalarTomitaPolarFactor P))
                ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))))
          2))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_NORMA_PESO_PERTURBADO_A1B.json` — SHA256 `431157059098d6f9dde92388c847cd0616a4bd7e93254a72e543d40014e3a45e`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\REVIEW_A1_PERTURBED_WEIGHT_NORM_FINAL.json` — SHA256 `405f2e3961cd999cd28d90f2cfb618bf34447210ec929addb552b0ce2f20557a`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\compilation.json` — SHA256 `387dd19d888f93cbd67566918840300d114999e5fd41da394ff218fcef82fac7`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_PERTURBED_WEIGHT_NORM.json` — SHA256 `f3775f9e8f83a526dd164ee220f2d382237d38f4abb4692b80f26b4afd845e3e`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — norma do peso perturbado

2026-09-14T21:48:34.069683-03:00

**A1_PERTURBED_WEIGHT_NORM_REVIEW_ACCEPTED__ALL_POSITIVE_EXTENSION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado: **2 teoremas públicos, 0 definições, 0 helpers privados**. Fonte inteiro relido, Lake próprio rc0 e auditor independente com #check completo, pp.universes e #print axioms: somente propext, Classical.choice e Quot.sound.

[REAL — leitura e reprodução] O primeiro teorema recebe P, b pertencente à álgebra de ação direita já construída e A no ideal escalar completo nν. hb.1 fornece Ab∈nν e sua inscrição. A norma-quadrado existente identifica o mesmo dualQuadraticIntegral, com regularVacuum e Haar herdados; star_mul e associatividade dão (Ab)*(Ab)=b*(A*A)b. congrArg transporta a igualdade vetorial; a isometria do mesmo scalarTomitaPolarFactor elimina apenas o J externo. O J inverso interno e π(b*) permanecem no resultado.

[REAL — aplicação concreta] O segundo teorema exige ε>0 e A∈nν. regularInverseGeneratorCutoff_sqrt_right fornece a pertinência ao core e a propriedade de ação direita da raiz positiva ORIGINAL do MESMO Bε. O testemunho existencial hb é apenas a prova de pertinência necessária à coerção; não pressupõe a conclusão de norma. Nenhuma hipótese residual de ação direita fica na aplicação concreta. Não se usa PositiveCoreInput.conjugate, cujo argumento pertence ao dualFixedCore, para tratar cortes por homonímia.

[REAL — ficha e histórico] A ficha anterior ao código descreve exatamente esta ponte para valores de quadrados no domínio finito, sem extensão automática a todos os positivos. Seus fornecedores e pins foram relidos. Duas tentativas DEV rc1 (21:37 e 21:38) permanecem excluídas; seus diagnósticos de elaboração foram preservados. A versão final usa congrArg explícito, com maxHeartbeats 1000000 no fonte. Não se atribui aos rc1 prova parcial aceita. Pins históricos apontam às respectivas cópias DEV retidas, com o caminho vivo anterior separado como historical_location.

[REAL — negativo relido] A auditoria autoral standalone rc0 foi conferida por bytes e streams. Remover J⁻¹ no controle BadPerturbedWeightWithoutJ produz rc1 Type mismatch, com imports resolvidos. Esta é evidência de recusa daquela prova adulterada, não demonstração universal da falsidade de toda fórmula sem J em casos especiais. O controle não foi reexecutado aqui.

[REAL — proveniência] 667 objetos anteriores do Lake próprio preservados; adicionados apenas módulo e auditor (total 669). Nenhum fornecedor antigo recompilado, nenhum objeto autoral/DEV importado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral da biblioteca. Run próprio rc0 em 55.773 s; zero avisos do alvo/auditor. 178 mensagens históricas de fornecedores constam no JSON; o stderr e avisos de cache, se presentes, foram preservados. LEAN_PATH dos traces contém somente V e seus pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte final | `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9` |
| .olean próprio | `255acd9ac47731cd2392d5232faa392029577d41be032960974820cdec316dad` |
| .olean cold autoral (comparação somente) | `255acd9ac47731cd2392d5232faa392029577d41be032960974820cdec316dad` |

Igualdade binária medida: True.

[OPEN — limites] A∈nν continua explícito; não há inscrição GNS declarada para A com ν(A*A)=∞. Não há novas definições, helpers privados, axiomas postulados, sorry, native_decide ou trustCompiler no candidato. Extensão e ordem dos pesos em TODOS os positivos, limite, semifinitude do limite e tracialidade permanecem obrigações posteriores. A propriedade falsa de minorantes positivos finitos de ν não é usada. A1(b) permanece aberto; esta revisão não modifica gate, memórias, programa ou fontes autorais.

Artefatos próprios:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\compilation.json>) — SHA256 `387dd19d888f93cbd67566918840300d114999e5fd41da394ff218fcef82fac7`.
- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\independent_20260914_214502_008278\run.json>) — SHA256 `575e7c90b449886e38f856f7c702e579ee91d258f4e6fee5a3ac973a4e63580f`.
- [tipos e axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\independent_20260914_214502_008278\type_axiom_audit.json>) — SHA256 `0e198cd21903e4d7f1a9c300fc5b488730fe81ce93fc25ef5809a1b64a66a43d`.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_peso_perturbado_norma\history_read.json>) — SHA256 `9d3c0edc2ce6921ab650754cf84baa8041d8846d9b01fee9640346a2480b34e2`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA

[OPEN — ficha anterior à identidade de norma do peso perturbado]

# A1(b): consumir a ação dos cortes nos valores do peso

2026-09-14T21:30:50.225336-03:00

For P, b in the same scalarPolarRightAlgebra and A in n_nu, prove dualQuadraticIntegral(star b.val*(star A.val.val*A.val.val)*b.val)(regularVacuum P) = ENNReal.ofReal(norm(scalarGNSRepresentation P (star b) ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)))^2). Obtain A*b membership from the already proved right identity, rewrite the GNS norm-square and use the isometry of the SAME J. Consumer: bounded cut perturbations with b=hilbertPositiveSqrt(B_epsilon), already constructed. This only gives values on squares of n_nu; do not claim it extends to all positive inputs, proves monotonicity in epsilon, or gives a trace. PositiveCoreInput.conjugate is only a pattern because it requires b in dualFixedCore, whereas our cut lies in regularCoreAlgebra; do not pass it by homonym or claim theta-fixity.

ADAPTAR: a identidade da ação direita já fornece Ab no domínio e seu vetor GNS. Basta a ponte algébrica para a norma do peso; não criar outra realização, peso escalar ou inscrição. A normalidade/aditividade de ν são fornecedores, não novos alvos. Não usar a caracterização falsa por minorantes positivos finitos para ν. A passagem a todos positivos e a tracialidade são obrigações posteriores nomeadas, não consequências deste lema isolado.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:14` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def ScalarPolarRight (P : SiteProfile) (b : (regularCoreAlgebra P).toStarSubalgebra) : Prop
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightAction.lean:44` — `7875ce91559689c1e951f28d3a1d005dc17aae2af1db677242a27d38e40dfb5c`

```lean
theorem scalarWeightGNSEmbedding_norm_sq (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ENNReal.ofReal (‖scalarWeightGNSEmbedding P A‖^2) =
      dualQuadraticIntegral (star A.val.val*A.val.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:25` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:15` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
def scalarDualWeight (P : SiteProfile) (A : PositiveCoreInput P) : ℝ≥0∞
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:46` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem scalarDualWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:38` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
def PositiveCoreInput.conjugate {P : TGLExt.SiteProfile}
    (A : PositiveCoreInput P)
    (B : (dualFixedCore P).toStarSubalgebra) : PositiveCoreInput P
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_perturbed_weight_norm\20260914_213020_145263\searches.json. Ausência nominal nos recortes não é ausência universal.
