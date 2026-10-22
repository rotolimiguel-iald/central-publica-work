[REAL — 3 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — O mesmo grafo é a multiplicação exponencial em coordenadas espectrais

2026-09-14T19:55:57.144661-03:00

Para x,y no espaço regular original, (x,y) pertence ao grafo positivo já construído se e somente se V⁻¹y(ξ)=e^(−2πξ)V⁻¹x(ξ) quase em toda parte. A condição especifica o domínio da multiplicação não limitada em classes L². Consome a equação resolvente existente e as identidades de sigmoid; não cria outro gerador, grafo ou domínio.

A identificação do grafo não substitui a identificação de suas potências imaginárias, afiliação, escala dual ou construção do traço.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\spectral_graph_attempts\20260914_192122_411832\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1SpectralGraph']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\independent_20260914_194823_963478\run.json`. `640` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularSpectralGraph` | `2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642` | `d1b7901ef767d9a92cd5f4a58e5c85c8a4dde7e88b1cff74b1928d75cea6e5ac` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.sigmoid_resolvent_equation_iff {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  (a : ℝ) (u v : H) :
  Eq.{1} (HSMul.hSMul.{0, 0, 0} (↑(HSub.hSub.{0, 0, 0} 1 a.sigmoid)) u) (HSMul.hSMul.{0, 0, 0} (↑a.sigmoid) v) ↔
    Eq.{1} v (HSMul.hSMul.{0, 0, 0} (↑(Real.exp (Neg.neg.{0} a))) u)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularSpectralResolvent_coordinate (P : TGLExt.SiteProfile)
  (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Eq.{1}
    ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P))
      ((TGLV350.Regular.regularSpectralResolvent P) x))
    ((TGLV350.Regular.realScalarMultiplier (fun ξ => (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) ξ).sigmoid) ⋯
        ⋯ ⋯)
      ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P)) x))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularPositiveGenerator_graph_iff (P : TGLExt.SiteProfile)
  (x y : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P)) (Prod.mk.{0, 0} x y) ↔
    ∀ᵐ (ξ : ℝ),
      Eq.{1} (↑↑((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P)) y) ξ)
        (HSMul.hSMul.{0, 0, 0} (↑(Real.exp (Neg.neg.{0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) ξ))))
          (↑↑((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P)) x) ξ))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_GRAFO_ESPECTRAL_A1B.json` — SHA256 `af2e0319102f2294cbf4f7860d19536075aae87b444be58129c780ebff797e18`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\REVIEW_A1_SPECTRAL_GRAPH_FINAL.json` — SHA256 `521cf614f37d6f67b8a2ac48194c20f6ba3c7edfd8ac81be57a9cadf2d56c4e8`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\compilation.json` — SHA256 `0380419a293a636c7bbe3267d92de570a9f9ad973fb4bf9a8573b8d063fa851e`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_SPECTRAL.json` — SHA256 `9e9aa1033b4ed797b0ec7b7a015463dce64717742a75799742f10c740764722a`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — grafo espectral do gerador regular

2026-09-14T19:54:13.228176-03:00

**A1_SPECTRAL_GRAPH_REVIEW_ACCEPTED__POWERS_AFFILIATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 3 declarações (3 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] A leitura integral confrontou as três declarações com a ficha anterior ao DEV e com o grafo resolvente já reproduzido. regularSpectralResolvent_coordinate usa exatamente regularSpectralCoordinates e regularSpectralResolvent do delta15; regularPositiveGenerator_graph_iff conserva o mesmo operador parcial e o mesmo L² vetorial.

[REAL] A equivalência escalar cancela sigmoid(a)>0 ponto a ponto e usa (1−sigmoid a)/sigmoid a=exp(−a). O sinal resultante é exp(−2πξ), compatível com R=(1+h)⁻¹. Esse cancelamento não presume inversa limitada do multiplicador nem gap espectral.

[REAL] A igualdade de gráficos é uma equivalência para todos x,y do Hilbert regular. A passagem entre igualdade L² e igualdade quase em toda parte usa apenas interseções finitas dos eventos correspondentes a esse par. A multiplicação exponencial não é declarada limitada: a própria existência de y em L² expressa o domínio. Não se exige produto exponencial em L² para todo x, nem se escolhe um evento comum a vetores arbitrários.

[REAL] Ficha e pins de fornecedores são conferidos nos artefatos; a busca nominal documentada não é tomada como prova de ausência universal. O negativo autoral troca exp(−2πξ) por exp(+2πξ) e é recusado por Type mismatch, com imports válidos; leitura e hashes foram refeitos, sem executar o controle novamente.

[REAL] Execução própria rc0 em 297.15 s. 640 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularSpectralGraph | `2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642` | `d1b7901ef767d9a92cd5f4a58e5c85c8a4dde7e88b1cff74b1928d75cea6e5ac` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Este aceite é dos três teoremas de grafo, separado dos quinze anteriores. Não prova neste delta potências imaginárias, afiliação, escala dual ou existência de traço; não altera gate, memória ou fontes autorais. A herança da biblioteca e dos objetos próprios anteriores está identificada em compilation.json; não corresponde a nova reconstrução integral.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\independent_20260914_194823_963478\run.json>) — SHA256 `57515ae6d53fb48cc037e37955f16dc10399db61893fc089ee2f2dc507db39c5`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\compilation.json>) — SHA256 `0380419a293a636c7bbe3267d92de570a9f9ad973fb4bf9a8573b8d063fa851e`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_grafo_espectral\independent_20260914_194823_963478\type_axiom_audit.json>) — SHA256 `0e6d7e90b2e6151fddeee9a852e1f9670cbcb3218cd6ad22dd79744e0f2c383d`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_GRAFO_ESPECTRAL

[OPEN — ficha anterior à identificação espectral do grafo]

# A1(b): o mesmo grafo nas coordenadas espectrais

2026-09-14T19:08:08.583582-03:00

For every SiteProfile P and x,y in the existing regular Hilbert space: (x,y) in graph(regularPositiveGenerator P) iff almost everywhere xi, (V.symm y)(xi) = exp(-2*pi*xi) smul (V.symm x)(xi), with V=regularSpectralCoordinates P. No new Hilbert space, graph, multiplier, Fourier transform or generator. Exact identification needed by regular_unitary_positive_generator / future imaginary powers.

A busca nominal negativa não é ausência universal. A equação resolvente já foi paga: consumi-la. Novo módulo consumidor, sem editar o módulo de quinze declarações que está em revisão. Não promover prova DEV à aceitação.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:20` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_equation (R : H →L[ℂ] H) (hi : Function.Injective R) (x y : H) :
    (x,y) ∈ (resolventGraphOperator R hi).graph ↔ (1-R) x = R y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:30` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
theorem realScalarMultiplier_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) (f : RegularHilbert H) :
    realScalarMultiplier g hg h0 h1 f =ᵐ[volume] fun s => (g s : ℂ) • f s
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:122` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularPositiveGenerator (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →ₗ.[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:72` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralCoordinates (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) ≃ₗᵢ[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:113` — `01fafea90dcd4d58cfcb91454b618a3c55f9a26f347b729bb3cb8fadc3bf2df2`

```lean
lemma sigmoid_mul_rexp_neg (x : ℝ) : sigmoid x * exp (-x) = sigmoid (-x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Sigmoid.lean:108` — `01fafea90dcd4d58cfcb91454b618a3c55f9a26f347b729bb3cb8fadc3bf2df2`

```lean
lemma sigmoid_neg (x : ℝ) : sigmoid (-x) = 1 - sigmoid x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\InnerProductSpace\Adjoint.lean:885` — `d1636c8ae9160d3762630f6f99815134dbc4da51188d9e2e34dcc3c06c6c32fc`

```lean
@[simp] lemma conjStarAlgEquiv_apply_apply (e : H ≃ₗᵢ[𝕜] K) (x : H →L[𝕜] H) (y : K) :
    e.conjStarAlgEquiv x y = e (x (e.symm y))
```

Buscas nas seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_spectral_graph\20260914_190746_524794\searches.json.
