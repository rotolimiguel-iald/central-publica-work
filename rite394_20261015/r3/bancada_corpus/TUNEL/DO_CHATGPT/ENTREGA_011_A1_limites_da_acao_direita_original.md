[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A ação direita original atravessa limites fortes dos operadores e adjuntos

2026-09-14T20:47:26.994891-03:00

A identidade direita de cada Λ_t é ligada ao mesmo J polar e à mesma π para todo nν. Para uma família existente b_i que satisfaz essa identidade, limitada em norma e convergente fortemente junto com seus adjuntos, a continuidade da π aplicada aos adjuntos produz a convergência em norma dos vetores direitos. O fechamento GNS produz A b∈nν e a identidade no limite. NeBot é explícito; a família aproximante ainda é entrada.

Nenhuma família aproximante de R foi produzida neste delta. A ação de R e de sqrt(Bε), o limite das avaliações perturbadas e a tracialidade são posteriores. A1(b) completo continua aberto, sem mudança de gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\right_action_limits_attempts\20260914_203855_891872\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RightActionLimits']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\independent_20260914_204429_089232\run.json`. `659` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ScalarRightActionLimits` | `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d` | `1ec351f6e5e7b47c345af3f2eb480c26c9fc98bd134203515c1b5bfcb4cab779` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarRightAction_regular (P : TGLExt.SiteProfile) (t : ℝ)
  (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  Eq.{1} ((TGLV350.Regular.scalarWeightGNSEmbedding P) (TGLV350.Regular.scalarRegularRightProduct P t A))
    ((TGLV350.Regular.antiunitaryConjugate (TGLV350.Regular.scalarTomitaPolarFactor P)
        ((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} (TGLV350.Regular.regularRightCoreElement P t))))
      ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarRightAction_closed_of_bounded_strongStar.{u_1} (P : TGLExt.SiteProfile) {ι : Type u_1}
  {l : Filter.{u_1} ι} [Filter.NeBot.{u_1} l]
  (b : ι → ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (B : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) (C : ℝ)
  (hbound : ∀ (i : ι), LE.le.{0} (norm.{0} ↑(b i)) C)
  (hstrong :
    ∀ (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
      Filter.Tendsto.{u_1, 0} (fun i => ↑(b i) x) l (nhds.{0} (↑B x)))
  (hadjoint :
    ∀ (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
      Filter.Tendsto.{u_1, 0} (fun i => ↑(star.{0} (b i)) x) l (nhds.{0} (↑(star.{0} B) x)))
  (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P))
  (hact :
    ∀ (i : ι),
      ∃ (hi : Membership.mem.{0, 0} (TGLV350.Regular.scalarWeightLeftIdeal P) (HMul.hMul.{0, 0, 0} (↑A) (b i))),
        Eq.{1} ((TGLV350.Regular.scalarWeightGNSEmbedding P) (Subtype.mk.{1} (HMul.hMul.{0, 0, 0} (↑A) (b i)) hi))
          ((TGLV350.Regular.antiunitaryConjugate (TGLV350.Regular.scalarTomitaPolarFactor P)
              ((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} (b i))))
            ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))) :
  ∃ (hAB : Membership.mem.{0, 0} (TGLV350.Regular.scalarWeightLeftIdeal P) (HMul.hMul.{0, 0, 0} (↑A) B)),
    Eq.{1} ((TGLV350.Regular.scalarWeightGNSEmbedding P) (Subtype.mk.{1} (HMul.hMul.{0, 0, 0} (↑A) B) hAB))
      ((TGLV350.Regular.antiunitaryConjugate (TGLV350.Regular.scalarTomitaPolarFactor P)
          ((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} B)))
        ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_LIMITES_ACAO_DIREITA_A1B.json` — SHA256 `085242874bacd9b3ee80f042b55de245902d3986a7b399586c7e74a373075cb0`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\REVIEW_A1_RIGHT_ACTION_LIMITS_FINAL.json` — SHA256 `84b068d634e395014c7b7396551c1d81f299cdb4a87f10a25541eb6ed450d941`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\compilation.json` — SHA256 `a557bdb9457310b7a8d6f8ce5f92af36814ad3e583aeeebd24b044670caa1b59`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_RIGHT_ACTION_LIMITS.json` — SHA256 `b8cbb3ca6859616819c0f431c641b3ada1e3baea6431ddb082f6d2cd042dfda8`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — limites da ação direita original

2026-09-14T20:46:30.809527-03:00

**A1_RIGHT_ACTION_LIMITS_REVIEW_ACCEPTED__CUTOFF_RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 2 declarações (2 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Dois teoremas, zero definições. Fonte e ficha MD/JSON relidas integralmente. A notação antiunitaryConjugate usa o mesmo scalarTomitaPolarFactor P, π é scalarGNSRepresentation P, e o domínio inicial é scalarWeightLeftIdeal P completo. Não há troca pelo J da torre nem por um GNS auxiliar.

[REAL] scalarRightAction_regular é uma ligação efetiva entre regularRightGNS_intertwines e scalarTomitaPolarFactor_regular_left: a estrela no elemento regular está presente e a inversa do antiunitário cancela pela isometria. O produto regular já contém sua prova de pertença ao ideal; nenhuma hipótese adicional de ação direita é introduzida para esse grupo.

[REAL] scalarRightAction_closed_of_bounded_strongStar recebe uma família b_i no mesmo core, uma cota C, convergência forte de b_i e de b_i*, um filtro arbitrário de universo arbitrário não trivial, e a identidade direita em cada aproximante. A existência dessa família continua INPUT. Para cada A∈nν, escolhe apenas as provas de pertença de A b_i ao ideal; a independência desses testemunhos é proposicional.

[REAL] A convergência GNS NÃO é premissa oculta nem consequência atribuída à forte isolada: norm_star mantém a mesma cota C nos adjuntos, scalarGNSRepresentation_tendsto_of_uniformly_bounded aplica-se a b_i* no vetor J⁻¹Λ(A), e a continuidade de J produz convergência em norma de Jπ(b_i*)J⁻¹Λ(A). A hipótese hadjoint é usada exatamente nesse ponto.

[REAL] A rede A b_i tem cota ||A|| C e converge fortemente a A B pela continuidade do operador A. O fechamento GNS já reproduzido recebe essas duas convergências e devolve A B∈nν e a identidade desejada. Não se presume continuidade da estrela para a topologia forte em geral, nem positividade de A ou dos b_i.

[REAL] A ficha anterior aos fontes descreve corretamente o consumidor dos cortes inversos, sem prometer aproximantes. Os pins dos sete fornecedores e da busca são verificados pelo finalizador. Os objetos próprios anteriores são reaproveitados, sem DEV autoral; os tipos universais e axiomas são capturados em auditor próprio separado.

[REAL] Histórico autoral preservado em history_read.json: a tentativa rc1 por binder i é excluída, inclusive quaisquer prints parciais; somente 20260914_203706_719663 rc0 é aceito. O negativo BadRightActionMissingStar é relido no stream autoral: trocar π(b*) por π(b) resulta em Type mismatch, com importações válidas. Nenhum negativo autoral foi reexecutado.

[REAL] Execução própria rc0 em 64.81 s. 659 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarRightActionLimits | `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d` | `1ec351f6e5e7b47c345af3f2eb480c26c9fc98bd134203515c1b5bfcb4cab779` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] A rede aproximante e a ação de R ou sqrt(Bε) não são construídas neste delta. A revisão não declara toda W*(Λ) coberta, nem tracialidade, nova perturbação do peso ou pagamento de A1(b). Nenhuma memória, programa, gate, fonte autoral ou relatório anterior foi alterado. A consulta CFC/seno é separada e não acrescenta alvo Lean ao aceite.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\independent_20260914_204429_089232\run.json>) — SHA256 `76a2ce5bbb468c688a449bfd060ad615657002cbdf66f1b9720bc4c00d41e92a`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\compilation.json>) — SHA256 `a557bdb9457310b7a8d6f8ce5f92af36814ad3e583aeeebd24b044670caa1b59`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_limites_direita\independent_20260914_204429_089232\type_axiom_audit.json>) — SHA256 `597393c78470c8cf71518490608bddec9c072d9e00be982784aaf2ce855cb47a`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_LIMITES_ACAO_DIREITA

[OPEN — ficha anterior à passagem da ação direita por limites]

# A1(b): ação direita e limites fortes-* limitados

2026-09-14T20:34:24.167831-03:00

Extend the existing right action through actual bounded strong-star limits. For A in n_nu, b_i and b in the same core, ||b_i||<=C, b_i and b_i* tending strongly to b and b*, and already proved Lambda_nu(A b_i)=J pi(b_i*) J Lambda_nu(A), construct A b in n_nu and the same identity at b. J is scalarTomitaPolarFactor, not the tower J by name. Derive norm convergence of the right vectors from existing normality of pi and continuity of J; then consume full GNS closedness. Also exhibit the initial identity for each regular unitary by consuming existing regularRightGNS_intertwines and scalarTomitaPolarFactor_regular_left. Consumer: actual action of sqrt(B_epsilon) for the inverse-generator weight perturbation, LACUNAS_A1 item4. Do not claim any approximating net has been constructed, or that all of W*(Lambda) is reached.

O fechamento do mapa GNS é fornecedor recém compilado, ainda em revisão. A continuidade forte limitada de π aplicada aos adjuntos produz a convergência dos vetores direitos. Não será inventada uma rede de aproximação de R: fornecê-la ou uma rota alternativa segue sendo a próxima obrigação. Sem novo tipo de representação.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:79` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarWeightGNSEmbedding_closed_of_bounded_strong (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → scalarWeightLeftIdeal P)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val.val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (T i).val.val x) l (𝓝 (A.val x)))
    (hgns : Tendsto (fun i => scalarWeightGNSEmbedding P (T i)) l (𝓝 v)) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSStrongContinuity.lean:16` — `a01a6e42e191d7bc7ce2a37e529fead8d04463b62d19f081fd640f249e2b3938`

```lean
theorem scalarGNSRepresentation_tendsto_of_uniformly_bounded (P : SiteProfile)
    {ι : Type*} {l : Filter ι}
    (T : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => (T i).val v) l (𝓝 (B.val v)))
    (v : ScalarGNSHilbert P) :
    Tendsto (fun i => scalarGNSRepresentation P (T i) v) l
      (𝓝 (scalarGNSRepresentation P B v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:98` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:30` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
def scalarRegularRightProduct (P : SiteProfile)
    (t : ℝ) (A : scalarWeightLeftIdeal P) : scalarWeightLeftIdeal P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:113` — `cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9`

```lean
theorem scalarTomitaPolarFactor_regular_left (P : SiteProfile) (t : ℝ)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (regularRightCoreElement P t)) z) =
        regularRightGNS P t (scalarTomitaPolarFactor P z)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarInvolution.lean:72` — `b7cecd7d64b40a7de3bb5cb81ad90feeed1883943c0e566442eeb12abc83984d`

```lean
theorem scalarTomitaPolarFactor_involutive : Function.Involutive (scalarTomitaPolarFactor P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:25` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_apply (T : H →L[ℂ] H) (x : H) :
    antiunitaryConjugate U T x=U (T (U.symm x))
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_right_action_limits\20260914_203357_459349\searches.json. Ausência nominal nos recortes não é ausência universal.
