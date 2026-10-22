[REAL — 1 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Balanço dos cortes no resolvente modular original

2026-09-15T02:56:29.401036-03:00

Um teorema público, nove auxiliares privados, zero definições. Para todo perfil P e epsilon,eta positivos, no GNS original, o resultado prova a comutação de T_nu com C_epsilon=pi(B_epsilon) e D_eta=J pi(B_eta) J^-1 e o balanço (1-T_nu) C_epsilon q_eta = T_nu p_epsilon D_eta. Consome a igualdade dos implementadores32, as potências regulares e a separação de frequências já existentes. O argumento por caracteres trata os extremos antes de dividir; cancela operadores amortecedores por injetividade. As identidades dos resolventes e B_1=R transportam o balanço aos cortes, usando a inclusão no comutante anteriormente provada. PhaseFrequencySeparation e V350CorePolarInclusion foram recompilados das fontes antigas preservadas, sem contá-los como novos teoremas. As comutações incluídas no mesmo resultado servem ao próximo consumidor quadrático sem rederivar os auxiliares privados.

Q, tracialidade de scalarInverseLimitWeight e o contrato completo do traço permanecem abertos. O próximo consumidor retira um corte de cada vez por convergência forte e compara supremos ENNReal, incluindo infinito. O controle negativo troca (1-T_nu) por T_nu e precisa ser recusado por incompatibilidade de tipo, com imports válidos. A prova não identifica h com Delta_nu. Monólito e gate inalterados.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\modular_cut_balance_attempts\20260915_024019_253150\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1ModularCutBalance']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\independent_20260915_024700_042435\run.json`. `711` objetos próprios anteriores; `2` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ModularCutBalance` | `98fddf5844aa540589735b7bcdd82f5961525d7aac5dcc34ded758c39cad502b` | `7fa922b9f37ba3ffd2bb3ea0f7d3b1677f1b7ca5a7f8e8cc0ff3c687e5f08d4b` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarTomitaResolvent_double_cut_balance (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) :
  have π := TGLV350.Regular.scalarGNSRepresentation P;
  have J := TGLV350.Regular.scalarTomitaPolarFactor P;
  have C := π (Subtype.mk.{1} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) ⋯);
  have D :=
    TGLV350.Regular.antiunitaryConjugate J (π (Subtype.mk.{1} (TGLV350.Regular.regularInverseGeneratorCutoff P η) ⋯));
  Commute.{0} (TGLV350.Regular.scalarTomitaResolvent P) C ∧
    Commute.{0} (TGLV350.Regular.scalarTomitaResolvent P) D ∧
      Eq.{1}
        (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HSub.hSub.{0, 0, 0} 1 (TGLV350.Regular.scalarTomitaResolvent P)) C)
          (TGLV350.Regular.antiunitaryConjugate J (π (TGLV350.Regular.regularDomainCut P η))))
        (HMul.hMul.{0, 0, 0}
          (HMul.hMul.{0, 0, 0} (TGLV350.Regular.scalarTomitaResolvent P) (π (TGLV350.Regular.regularDomainCut P ε))) D)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json` — SHA256 `0b10e7e0bc2aaae7cb3375fb61a86fd8ee584833439f8c06ff6e1eaa98699a47`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\REVIEW_A1_MODULAR_CUT_BALANCE_FINAL.json` — SHA256 `d961cf1f2e4916a60fd0926d3da43896cb78484b497c3879468fd80ea65cdf8c`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\compilation.json` — SHA256 `3ca3c0a318bec9c9fe59c979b19df58287e089362d23b0601e14dbc18a115bd2`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_MODULAR_CUT_BALANCE.json` — SHA256 `bdaa6454d4da4df617a55b81fcabc17629b3cabacacb299586c39df720302a77`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

2026-09-15T02:54:00.388937-03:00

**A1_MODULAR_CUT_BALANCE_REVIEW_ACCEPTED__QUADRATIC_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Fonte final e auditor próprios rc0; controle negativo próprio rc1 por Type mismatch com imports válidos. Aceite independente33, limitado ao balanço e suas duas comutações.

[REAL — tipo e objetos] Um teorema público, nove auxiliares privados e zero definições. O público recebe somente P:SiteProfile, epsilon/eta reais e suas positividades. Conclui Commute T C_epsilon, Commute T D_eta e (1-T) C_epsilon q_eta = T p_epsilon D_eta no MESMO ScalarGNSHilbert P. T é scalarTomitaResolvent P; A=pi(regularSpectralResolvent P) e B=J A J^-1 são distintos. Não recebe balanço, comutação, tracialidade ou igualdade h=Delta_nu como premissas.

[REAL — fases concretas e sinal] regularPositiveGenerator_imaginaryPower e resolventImaginaryPower_damping dão a fase amortecida do resolvente regular; closed_representation_cfc transporta essa igualdade pela pi original. antiunitaryConjugate_complex_cfc e resolventPhaseFunction_star produzem a fase de B em -t, em conformidade com scalarTomitaPolar_regular_generator. A igualdade efetiva dos implementadores32 é consumida, junto da comutação da ação direita com pi: não se infere igualdade de grupos apenas de covariância.

[REAL — comutações] T comuta com as translações representadas pelo fornecedor direito antigo e pelo flip J T J^-1=1-T. As janelas seno, CFC e convergência forte uniformemente limitada transportam isso a A. O mesmo flip dá TB=BT; AB=BA vem de scalarTomitaPolar_core_commutes, válido para todo core. As duas novas conclusões públicas usam o CFC do MESMO corte e hTA já obtido, seguido da conjugação por J. Nenhuma nova hipótese de CompleteSpace da VNA: fechamento normado é deduzido do bicomutante e fornece a instância do subtipo.

[REAL — extremos e cancelamento] No cálculo escalar, o produto dos amortecimentos nulo é tratado primeiro. Somente no caso não nulo se deduz interioridade e positividade dos argumentos de log/divisões e se aplica modular_phase_frequency_separation. A subálgebra comutativa fechada dos três resolventes usa Gelfand e map_cfc existentes; positividade ambiente é refletida explicitamente por raiz no subtipo, sem pressupor identificação de ordens. O produto amortecedor é cancelado como composição de aplicações vetoriais injetivas. Não se exige gap, inversa limitada, sobrejetividade ou densidade dos caracteres interiores.

[REAL — injetividade representada e cortes] A injetividade de a.val passa por dualAmbient, pelas duas igualdades a.e. de operatorFieldLift para cada par de vetores e pela restrição original a H_I. Não se confunde fidelidade de pi com injetividade de pi(a) como operador. Os complementos são tratados do mesmo modo. B_1=R e regularDomainCut_inverse_product dão A p=(1-A) C; a conjugação dá B q=(1-B) D. O lema puramente de anel explicita a ordem dos fatores e as comutações usadas. A igualdade multiplicada à esquerda por AB é cancelada por hiA.comp hiB, sem declarar que toda álgebra de operadores não tem divisores de zero.

[REAL — metadados e história] A auditoria inicial truncou o resultado no primeiro let :=. A versão TIPO_COMPLETO modifica somente esse enunciado nos metadados; o tipo completo já estava no stdout Lean e a auditoria anterior permanece pinada. O tipo extraído desta revisão termina no := by que inicia a prova e coincide com o tipo completo corrigido; o auditor próprio imprime ambas as comutações e a identidade, com universos. As tentativas DEV e sucessos apenas parciais são inventariados separadamente, com pins dos snapshots reais e a localização histórica apenas textual. Nenhum print de rc1 nem sucesso parcial foi contado como aceite33.

[REAL — independência] Lake no V, com LEAN_PATH/LEAN_SRC_PATH externos removidos, reutiliza os objetos próprios anteriores e o cache de pacotes já pinado. Fontes dos fornecedores antigos ausentes foram copiadas da base preservada e comparadas com K; nenhum olean K/DEV foi copiado. Os traces registram somente V e seus pacotes nos caminhos Lean. A ressalva de autoria histórica dos dois módulos antiunitários e a inspeção independente pelo principal permanecem as dos40; esta revisão não as reclassifica.

[OPEN — alcance] Balanço limitado e suas duas comutações estão pagos neste delta. O transporte para a igualdade quadrática Q, tracialidade de scalarInverseLimitWeight e contrato completo do traço ainda não estão provados por esta entrega. Não identifica h com Delta_nu, não atribui domínio a produto ilimitado e não move gate. Nenhum monólito, writer, memória, recibo ou fonte autoral foi executado/modificado.

[REAL — execução] 711 objetos próprios preservados; 4 novos (alvo, auditor, PhaseFrequencySeparation e V350CorePolarInclusion), total 715. Os dois fornecedores antigos imprimem 11 declarações já existentes, não contadas como novidade. 139.701 s no Lake; 20.115 s no negativo. Zero avisos do alvo/auditor; 178 mensagens herdadas/de fornecedores discriminadas em supplierwarnings. O aviso aesop de alterações locais pertence ao cache de pacotes herdado e está preservado no stderr. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui a recusa esperada.

[REAL — histórico] 37 DEV preservados: 30 rc1 recusados, 6 rc0 de snapshots parciais/superados, e um final rc0. Os limites locais de elaboração do fonte final são 1800000, 6000000, 4000000, 6000000, 6000000 heartbeats; não se declara orçamento uniforme de200k. Nenhuma recompilação independente inalterada foi repetida.

| Artefato | Bytes | SHA256 lido |
|---|---:|---|
| Fonte K=snapshot=V | 33098 | 98fddf5844aa540589735b7bcdd82f5961525d7aac5dcc34ded758c39cad502b |
| .olean próprio | 3030600 | 7fa922b9f37ba3ffd2bb3ea0f7d3b1677f1b7ca5a7f8e8cc0ff3c687e5f08d4b |
| .olean autoral, só comparação | 3030600 | 7fa922b9f37ba3ffd2bb3ea0f7d3b1677f1b7ca5a7f8e8cc0ff3c687e5f08d4b |

Igualdade binária medida: True.

Tipo público completo, confrontado com #check próprio com universos:

~~~lean
theorem scalarTomitaResolvent_double_cut_balance (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    let π := scalarGNSRepresentation P
    let J := scalarTomitaPolarFactor P
    let C := π ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    let D := antiunitaryConjugate J
      (π ⟨regularInverseGeneratorCutoff P η,regularInverseGeneratorCutoff_mem P η⟩)
    Commute (scalarTomitaResolvent P) C ∧ Commute (scalarTomitaResolvent P) D ∧
      (1-scalarTomitaResolvent P)*C*antiunitaryConjugate J (π (regularDomainCut P η)) =
        scalarTomitaResolvent P * π (regularDomainCut P ε) * D
~~~

Axiomas públicos próprios: propext, Classical.choice, Quot.sound. Os nove privados foram impressos no build próprio; cut_balance_after_multiplication usa apenas propext, os outros permanecem no trio. Tipos-fonte completos dos privados e respectivos axiomas estão no type_axiom_audit.json.

[OPEN] Aceite33 restrito a um público de balanço e duas comutações, nove privados, zero defs; dois fornecedores antigos reconstruídos e discriminados separadamente. Q, tracialidade de scalarInverseLimitWeight e contrato completo do traço permanecem OPEN; h não foi identificado com Delta_nu. 19 V351 são subconjunto das940 entradas de base, não959; fontes e predecessores relidos por bytes. A execução de publicação/entrega e atualização de memória cabe ao principal após ler este parecer. Nenhum writer, monólito ou memória foi executado/modificado.

Evidências:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\compilation.json>) — SHA256 3ca3c0a318bec9c9fe59c979b19df58287e089362d23b0601e14dbc18a115bd2.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\independent_20260915_024700_042435\run.json>) — SHA256 c51c8d2719bb875e24dc75ebe682aef5cc22628b337358d5a25d367b08de1e42.
- [tipos e axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\independent_20260915_024700_042435\type_axiom_audit.json>) — SHA256 a9665d5b09eccd87ba8c7bcd4b310ad9321801878b4f97d379ab5e3b7a5747f1.
- [negativo próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\negative_20260915_025007_012495\run.json>) — SHA256 5a3a2b01d66c98172254cb4dc0879cb1f6436f02ea82c637e0c426d5e6534816.
- [preservação19/940](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\preservation_19_940.json>) — SHA256 927d3a974c9ebbe64755c87af43ab3c86ba0be62443c2c436fbd8f7f9fdc2d21.
- [fichas e fornecedores](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\provider_checks.json>) — SHA256 be1e91b0cf81f8d1a67f4cfe80229ae1b52f4d6477b3001af29c3da4dbe19c6c.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_balanco_dos_cortes\history_read.json>) — SHA256 7cf38ba0685f380eeaab979b1febf636fdf86be9ed70d35d2c0a80dc181931be.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES

[OPEN — ficha anterior ao balanço limitado dos cortes]

2026-09-15T01:17:59.404386-03:00

ADAPTAR/OPEN: proposed next exact bounded balance for epsilon,eta>0 in SAME H_nu: (1-T) C_epsilon q_eta = T p_epsilon D_eta, where T=scalarTomitaResolvent P, C_epsilon=pi(B_epsilon), D_eta=antiunitaryConjugate J (pi(B_eta)), p_epsilon=1-epsilon C_epsilon, q_eta=1-eta D_eta, B_epsilon=regularInverseGeneratorCutoff P epsilon. Names C,D,p,q here are notation, not new global definitions. This identity is NOT paid by equal group names or commutation. Delta32 equality of original groups has author rc0 and independent review pending at fiche time. CorePolarInclusion already pays C/D cross commutation on the SAME GNS: do not reprove right action or commutant inclusion. The real missing step is recovering the bounded balance from the actual spectral/group realization, or an equally concrete quadratic equality directly on finiteDualStarCore. Next consumption: original root graph x=sqrt(T)u, B_nu*x=sqrt(1-T)u plus positive_sqrt_intertwines, two cut limits -> Q(B_nu Lambda(a))=Q(J Lambda(a)), including infinity; existing tracial_iff_core then extends. This is a proof strategy, not a compiled consequence. No h=Delta_nu, new GNS, arbitrary product of unbounded operators, new field assuming balance, or full joint CFC unless a located concrete consumer truly requires it. Existing regularSineResolvent_tendsto is a particular regular spectral construction, NOT a generic inverse theorem recovering T_nu from U_t. Do not count conditional form rearrangements as payment of balance.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ModularImplementation.lean:16` — `3d16720656388fc14f70b5e5ded6a8a4d3fc6f72034992bbeee10364c8202a9f`

```lean
theorem scalarTomitaImaginaryPower_eq_regular_implementation (P : SiteProfile)
    (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t x =
      scalarGNSRepresentation P (regularRightCoreElement P t) (regularRightGNS P (-t) x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CorePolarInclusion.lean:52` — `4d5d416c82894dcc93562986ce8eae7ebc2c11f313eb658dc18e356af37dbd8d`

```lean
theorem scalarTomitaPolar_core_commutes (P : SiteProfile)
    (A B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P A)) (scalarGNSRepresentation P B)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:17` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_mem (P : SiteProfile) (ε : ℝ) :
    regularInverseGeneratorCutoff P ε ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPositiveRoot.lean:15` — `721afac12bff6654a1f1cdeadc1077d8df9a531d81dc1eac91a017e9bdec59b2`

```lean
def scalarTomitaPositiveRoot : ScalarGNSHilbert P →ₗ.[ℂ] ScalarGNSHilbert P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean:37` — `6a1ad3a2fa7041aa45d56b2448e18a5fce6b90e9e069f045df89483ecb1e3f90`

```lean
theorem resolventSquareRoot_domain (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).domain = (CFC.sqrt R).range
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350PositiveRootIntertwining.lean:50` — `f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5`

```lean
theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : A*U=U*B) :
    CFC.sqrt A * U = U * CFC.sqrt B
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113` — `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9`

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean:37` — `9b4edeb94844ded88ec595b50160936d42e34637f4432493d02894dd7731bab9`

```lean
theorem scalarWeight_inverseCutoff_perturbed_norm (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (A : scalarWeightLeftIdeal P) :
    ∃ hb : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      dualQuadraticIntegral
        (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) *
          (star A.val.val * A.val.val) *
          hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P) =
      ENNReal.ofReal (‖scalarGNSRepresentation P
        (star (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hb⟩ :
          (regularCoreAlgebra P).toStarSubalgebra))
        ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))‖^2)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitTracialExtension.lean:125` — `b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3`

```lean
theorem scalarInverseLimitWeight_tracial_iff_core (P : SiteProfile) :
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A))) ↔
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra, A ∈ finiteDualStarCore P →
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A)))
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_double_cut_balance\20260915_011735_080466\searches.json. Ausência nominal não é ausência universal. Consulta curta do revisor após31 e antes32 lida: balanço limitado proposto, não provado. Principal relê CorePolarInclusion para evitar nova prova de comutação já disponível. Novo extrator respeita parênteses antes de procurar :=, evitando truncamento em argumentos nomeados; fichas históricas preservadas.


## Ficha/adendo integral: ADENDO_PRE_CODIGO_BALANCO_ESPECTRAL

[OPEN — adendo anterior ao código do balanço espectral]

2026-09-15T01:33:06.753698-03:00

Delta32 já aceito e entregue. O balanço limitado e Q permanecem abertos. Estratégia em exame: usar a álgebra comutativa fechada gerada pelos três resolventes originais, transportar as fases amortecidas por map_cfc e aplicar os caracteres. A separação das frequências JÁ ESTÁ em modular_phase_frequency_separation: não refazer sua derivada. A igualdade escalar deve valer após multiplicação pelos amortecimentos, cobrindo os extremos 0 e 1 sem cancelamento falso. Só depois se cancela o operador com imagem densa, quando esta estiver provada na representação original. A conversão para cortes gerais é racional; não se introduz h=Delta_nu nem se assume o balanço desejado. Fornecedores abaixo relidos integralmente ou no trecho do enunciado antes de editar Lean33. Ausência em buscas não é prova de ausência universal.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\PhaseFrequencySeparation.lean:58
```lean
theorem modular_phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    a=b := by
  apply phase_frequency_separation a b c hc
  intro s
  simpa only [modular_phase_exponential] using h s

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseFunctions.lean:14
```lean
def resolventDamping (x : ℝ) : ℝ := x * (1-x)

/-- Only this damped function is fed to bounded continuous functional calculus. -/
def resolventPhaseFunction (t x : ℝ) : ℂ :=
  (resolventDamping x : ℂ) * modularPhase t (Real.log ((1-x)/x))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\GelfandDuality.lean:144
```lean
theorem gelfandTransform_isometry : Isometry (gelfandTransform ℂ A) := by
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Star\Subalgebra.lean:588
```lean
theorem isMulCommutative_adjoin {s : Set A} (hcomm : ∀ x ∈ s, ∀ y ∈ s, x * y = y * x)
    (hcomm_star : ∀ a ∈ s, ∀ b ∈ s, a * star b = star b * a) :
    IsMulCommutative (adjoin R s) := by
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\Algebra\StarSubalgebra.lean:137
```lean
abbrev commRingTopologicalClosure {R A} [CommRing R] [StarRing R] [TopologicalSpace A] [Ring A]
    [Algebra R A] [StarRing A] [StarModule R A] [IsSemitopologicalRing A] [ContinuousStar A]
    [T2Space A] (s : StarSubalgebra R A) (hs : ∀ x y : s, x * y = y * x) :
    CommRing s.topologicalClosure :=
  fast_instance% s.toSubalgebra.commRingTopologicalClosure hs
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:461
```lean
lemma StarAlgHomClass.map_cfc (φ : F) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac)
    (hφ : Continuous φ := by fun_prop) (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a) := by
  let ψ : A →⋆ₐ[R] B := (φ : A →⋆ₐ[S] B).restrictScalars R
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:14
```lean
theorem scalarTomitaResolvent_regular_right_commutes (P : SiteProfile) (t : ℝ) :
    Commute (scalarTomitaResolvent P) (regularRightGNS P t) := by
  apply ContinuousLinearMap.ext
  intro z
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CorePolarInclusion.lean:52
```lean
theorem scalarTomitaPolar_core_commutes (P : SiteProfile)
    (A B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P A)) (scalarGNSRepresentation P B) :=
  scalarGNS_commutation_from_generators P _ (scalarTomitaPolar_commutes_generators P A) B
```



## Ficha/adendo integral: ADENDO_PRE_ADAPTADORES_CONCRETOS_BALANCO

[OPEN] Adaptadores concretos para consumir o balanço limitado

2026-09-15T01:51:43.575821-03:00

A consulta independente localizou a via pontual: injetividade de a.val passa às conjugações unitárias dualAmbient, ao operatorFieldLift por duas igualdades a.e. para cada par de vetores, e à restrição no GNS original por Subtype.ext. Não usar fidelidade da representação como substituta de injetividade vetorial. O cálculo funcional deve ser transportado pela inclusão da álgebra normativamente fechada e pela mesma pi contínua, usando map_cfc existente. A identidade de fases concreta e as comutações necessárias continuam abertas. Os três adaptadores privados já escritos passaram apenas DEV; não são uma entrega33 nem a tracialidade. Balanço de cortes reais e Q permanecem OPEN.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:23
```lean
theorem dualAmbient_apply (s : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s A = characterMultiplier s * A * star (characterMultiplier (H := H) s) := rfl
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:94
```lean
/-- D_s, as a bounded complex-linear operator on the actual Lebesgue L² space. -/
def characterMultiplier (s : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  (characterMultiplierIsometry s).toContinuousLinearMap
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68
```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x) := operatorFieldLp_ae F f
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightCuts.lean:14
```lean
def dualIntegralFamily (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    StrongIntegral.Family (H := RegularHilbert H) where
  op := fun s => dualAmbient s A
  continuous_apply := dualAmbient_strongly_continuous A
  bound := ‖A‖
  bound_nonneg := norm_nonneg A
  norm_bound := fun s => le_of_eq
    ((StarAlgEquiv.isometry (dualAmbient (H := H) s)).norm_map_of_map_zero
      (map_zero (dualAmbient (H := H) s)) A)

/-- A finite strong integral of the dual action. This is unnormalized, and is
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ReducingStarRepresentation.lean:13
```lean
Invariance is required for every algebra element, hence also for adjoints. -/
def reducingStarRepresentation (ρ : A →⋆ₐ[ℂ] (H →L[ℂ] H))
    (S : Submodule ℂ H) [CompleteSpace S]
    (h : ∀ a, ∀ v ∈ S, ρ a v ∈ S) : A →⋆ₐ[ℂ] (S →L[ℂ] S) where
  toFun a := (ρ a).restrict (h a)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSRepresentation.lean:14
```lean
def scalarGNSRepresentation (P : SiteProfile) :
    (regularCoreAlgebra P).toStarSubalgebra →⋆ₐ[ℂ]
      (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) :=
  reducingStarRepresentation
    (dualOrbitRepresentation.comp (regularCoreAlgebra P).toStarSubalgebra.subtype)
    (scalarGNSSubspace P) (scalarGNSAmbientAction_preserves P)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSCompletion.lean:48
```lean
theorem scalarGNSAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) : ‖scalarGNSAction P B‖ ≤ ‖B.val‖ := by
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
  intro v
  exact (scalarGNSAmbientAction P B).le_of_opNorm_le
    (scalarGNSAmbientAction_norm_le P B) v.val
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:98
```lean
theorem regularSpectralResolvent_injective (P : SiteProfile) :
    Function.Injective (regularSpectralResolvent P) :=
  (regularSpectralCoordinates P).injective.comp
    ((realScalarMultiplier_injective _ _ _ _ (fun _ => Real.sigmoid_pos _)).comp
      (regularSpectralCoordinates P).symm.injective)

theorem regularSpectralResolvent_complement_injective (P : SiteProfile) :
    Function.Injective (1-regularSpectralResolvent P :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) := by
  let g : ℝ → ℝ := fun x => Real.sigmoid (2*Real.pi*x)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ x, 0 ≤ g x := fun x => Real.sigmoid_nonneg _
  have h1 : ∀ x, g x ≤ 1 := fun x => Real.sigmoid_le_one _
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:486
```lean
lemma StarAlgHom.map_cfc (φ : A →⋆ₐ[S] B) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac) (hφ : Continuous φ := by fun_prop)
    (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a) :=
  StarAlgHomClass.map_cfc φ f a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\Classes.lean:50
```lean
noncomputable instance StarSubalgebra.cstarAlgebra {S A : Type*} [CStarAlgebra A]
    [SetLike S A] [SubringClass S A] [SMulMemClass S ℂ A] [StarMemClass S A]
    (s : S) [h_closed : IsClosed (s : Set A)] : CStarAlgebra s where
  toCompleteSpace := h_closed.completeSpace_coe
  norm_mul_self_le x := CStarRing.norm_star_mul_self (x := (x : A)) |>.symm.le
```



## Ficha/adendo integral: ADENDO_APROVEITAMENTO_FASES_E_CORTES

[OPEN] Refinamento de aproveitamento — fases concretas e cortes

Sem mudança de escopo nem novo modelo. Complementa a ficha de sete canais já registrada.

A conjugação antiunitária preserva positividade por lema anterior. A identidade J pi(lambda_t) J^-1 = R_-t já existe; não deve ser reprovada. Transportar somente a identidade amortecida das potências imaginárias regulares pela pi existente e conjugar com o J existente.

[DERIVED — plano algébrico, ainda não compilado] Para o balanço de cortes, aproveitar B_1=R e a identidade de resolventes. Ela dá A p_e=(1-A) C_e e B q_h=(1-B) D_h. Com as comutações correspondentes, multiplicar a diferença desejada por A B reduz ao balanço básico (1-T) A (1-B)=T (1-A) B. Cancelar A B por injetividade vetorial, nunca por inversa limitada ou separação espectral uniforme. Isso dispensa construir um novo cálculo espectral para cada regulador. As hipóteses de comutação têm de ser descarregadas nos objetos originais.

[OPEN] Cinco auxiliares privados passaram apenas DEV. A sexta aplicação concreta ainda está sob correção de elaboração; não há entrega33, compilação independente33 ou tracialidade. Nenhum gate alterado.

2026-09-15T02:18:39.281217-03:00

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:33
```lean
theorem antiunitaryConjugate_nonneg (T : H →L[ℂ] H) (hT : 0 ≤ T) :
    0 ≤ antiunitaryConjugate U T := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply (ContinuousLinearMap.isPositive_iff_complex _).mpr
  intro x
  have hinner : inner ℂ (antiunitaryConjugate U T x) x =
      star (inner ℂ (T (U.symm x)) (U.symm x)) := by
    have h := antiunitary_inner_conj U (T (U.symm x)) (U.symm x)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularPolarCommutation.lean:50
```lean
theorem scalarTomitaPolar_regular_generator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularRightCoreElement P t)) =
        regularRightGNS P (-t) := by
  have h := scalarTomitaPolar_conjugate_regular_left P (-t)
  simpa only [regularRightCoreElement_star,neg_neg] using h

theorem scalarTomitaPolar_regular_generator_commutes (P : SiteProfile) (t : ℝ)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:90
```lean
theorem regularPositiveGenerator_imaginaryPower (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    resolventImaginaryPower (regularSpectralResolvent P)
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
      (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
      t u = regularUnitary P t u := by
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45
```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x :=
  denseLinearEquiv_apply _ _ _ _ _ x

theorem resolventImaginaryPower_zero (x : H) :
    resolventImaginaryPower T hT h1 hi hj 0 x = x := by
  refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43
```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P := by
  simp only [regularInverseGeneratorCutoff, Complex.ofReal_one, inv_one, Real.log_one,
    dualAmbient_zero, one_smul]
  rfl

/-- The image belongs to the domain of the same h and solves (h+epsilon)y=x. -/
theorem regularInverseGeneratorCutoff_graph (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:58
```lean
theorem regularDomainCut_inverse_product (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val =
      regularInverseGeneratorCutoff P δ - (ε : ℂ) •
        (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) := by
  have he := regularInverseGeneratorCutoff_resolvent_identity P ε δ hε hδ
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) = _
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:49
```lean
theorem regularDomainCut_commutes (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    Commute (regularInverseGeneratorCutoff P ε) (regularDomainCut P δ).val := by
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) =
    (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) * regularInverseGeneratorCutoff P ε
  simp only [mul_sub,sub_mul,mul_one,one_mul,mul_smul_comm,smul_mul_assoc,hc]

```


## Ficha/adendo integral: ADENDO_CONSUMIDOR_Q_DO_BALANCO

[OPEN] Consumidor Q e alcance mínimo da entrega do balanço

O balanço concreto passou DEV no snapshot indicado, com um teorema público, nove privados e zero definições. Ainda não é aceite independente33.

Para evitar que o consumidor seguinte rederive auxiliares privados, reforçar o MESMO teorema público com Commute T C_epsilon e Commute T D_eta, além da identidade limitada. A primeira vem da comutação T com pi(R) já provada, do auxiliar closed_representation_cfc já existente e de regularInverseGeneratorCutoff_cfc; a segunda pela conjugação original J T J^-1=1-T. Não adicionar outro gerador, outro estado, outra função pública ou premissa de tracialidade.

Consulta independente somente leitura localizou os fornecedores abaixo e refinou o próximo passo: escrever x=sqrt(T)u e B_nu x=sqrt(1-T)u no grafo original. Transportar comutações por positive_sqrt_intertwines para obter igualdade de formas Re<y,C_epsilon q_eta y>=Re<x,p_epsilon D_eta x>. Retirar um corte de cada vez pela convergência forte da sequência 1/(n+1), com 0<=p_n,q_n<=1, e comparar os supremos em ENNReal. Não converter para toReal nem pressupor finitude. Não é necessário construir limites das raízes dos cortes p/q, ou provar de novo que pi(sqrt B) é sqrt(pi B): a identidade de norma original, map_star/map_mul e sqrt_mul_sqrt_self bastam para identificar as formas.

Q e a tracialidade permanecem OPEN. Este é aproveitamento para um consumidor ainda não composto em Lean. O gate não mudou. A consulta independente não compilou nem certificou a entrega33.

2026-09-15T02:37:38.679127-03:00

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350PositiveRootIntertwining.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventSquareRoot.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSStrongContinuity.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightNorm.lean
C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350BoundedDualValues.lean


## Ficha/adendo integral: ADENDO_TIPO_COMPLETO_BALANCO

[REAL — correção documental ao lado]

O extrator anterior parou no primeiro let := do resultado. O auditor Lean já imprimiu o enunciado inteiro e o código passou. Nenhuma fonte Lean, olean ou resultado de teste foi alterado ou reexecutado. A auditoria anterior é preservada, com seu pin; o consumidor deve usar AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json.

```lean
theorem scalarTomitaResolvent_double_cut_balance (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    let π := scalarGNSRepresentation P
    let J := scalarTomitaPolarFactor P
    let C := π ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    let D := antiunitaryConjugate J
      (π ⟨regularInverseGeneratorCutoff P η,regularInverseGeneratorCutoff_mem P η⟩)
    Commute (scalarTomitaResolvent P) C ∧ Commute (scalarTomitaResolvent P) D ∧
      (1-scalarTomitaResolvent P)*C*antiunitaryConjugate J (π (regularDomainCut P η)) =
        scalarTomitaResolvent P * π (regularDomainCut P ε) * D
```
