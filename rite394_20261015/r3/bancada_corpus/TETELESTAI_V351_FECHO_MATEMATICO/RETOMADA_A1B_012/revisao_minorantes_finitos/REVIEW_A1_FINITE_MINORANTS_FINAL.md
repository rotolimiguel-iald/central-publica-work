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
