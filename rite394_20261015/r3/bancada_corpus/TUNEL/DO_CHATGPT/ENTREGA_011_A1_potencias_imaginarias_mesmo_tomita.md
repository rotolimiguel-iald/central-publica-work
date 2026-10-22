[REAL — grupo unitário fortemente contínuo do mesmo S* S verificado; OPEN — ação modular e A1(b), traço, ainda não quitados]

# Entrega 011 · A1 — potências imaginárias do Tomita do peso concreto

Responde à ORDEM_011, apenas A1. Incorporação é da gerência; este delta não acende bandeiras de realização completa e não move o gate.

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero | PAGO, preservado | manifestos anteriores reconferidos |
| A1(b), habitante concreto ou impossibilidade tipada | NÃO PAGO | falta identificar a ação modular, construir gerador positivo e traço |
| A1(c), axiomas | PAGO no delta | 39 declarações no trio, reprodução independente |

Data: 2026-09-14T10:22:21.535139-03:00

[REAL — construção compilada das potências imaginárias pelo resolvente; OPEN — identificação da ação modular e traço de A1(b)]

# A1 — o grupo do mesmo S* S, sem novo GNS

Este adendo registra a ponte construída em 14/09/2026. Os módulos são fornecedores da bancada; ainda não foram embutidos no programa terminal. Os hashes, horários e reproduções pertencem ao manifesto e aos relatórios acompanhantes.

## O que foi construído

O fornecedor `scalarClosedTomita_graph_eq_weight` já identifica o S fechado com a estrela do peso escalar completo. O fornecedor `scalarTomitaResolvent_graph` já identifica T com o resolvente (I+S* S)⁻¹, incluindo o domínio do operador parcial. Esses fornecedores foram reutilizados.

Para um operador limitado T em Hilbert complexo completo, com 0≤T≤I e T, I−T injetivos, a construção introduz

    b(x) = x(1−x),
    g_t(x) = b(x) exp(i t log((1−x)/x)),
    B = T(I−T),
    C_t = cfc(z ↦ g_t(Re z), T).

O log usado é o log real da biblioteca. A função amortecida está definida e é conjuntamente contínua em todo ℝ×ℝ, inclusive x=0,1, onde b=0. Não foi necessário estendê-la por zero fora [0,1]. No espectro real de uma contração positiva só interessa [0,1], e no interior a razão (1−x)/x é positiva.

As identidades verificadas são

    C_0 = B,
    C_t* = C_−t,
    C_s C_t = B C_{s+t},
    C_t* C_t = B²,
    |C_t| = B,
    ‖C_t x‖ = ‖B x‖.

A positividade de B e sua injetividade implicam imagem densa. A imagem de C_t também foi provada densa: C_t C_−t=B² e Ran(B²) é densa. Não se infere imagem densa da mera injetividade de um operador arbitrário; não se supõe B⁻¹ limitado.

O fornecedor existente `denseLinearEquiv` estende a isometria definida na imagem de B e produz uma equivalência linear isométrica sobrejetiva U_t, caracterizada por

    U_t B = C_t.

A lei U_s U_t=U_{s+t} é demonstrada primeiro em Ran(B²), depois por densidade. U_0=I. O cálculo funcional dá continuidade de t↦C_t na norma de operadores; a identidade acima dá continuidade em Ran B, e a estimativa isométrica uniforme estende-a a todo Hilbert. A continuidade conjunta de (x,t)↦U_t x foi provada. Não se afirma continuidade de t↦U_t na norma de operadores.

## Aplicação ao objeto concreto

`scalarTomitaResolvent_complement_injective` usa o J efetivamente construído a partir de S e sua relação JTJ⁻¹=I−T para descarregar a segunda injetividade. A primeira, a positividade e T≤I já estavam provadas. Logo, **para todo SiteProfile P**, `scalarTomitaImaginaryPower P t` é construído no **ScalarGNSHilbert P original**, sem receber um novo estado, GNS ou operador modular como hipótese.

Sua caracterização por U_t b(T)=g_t(T), com T=(I+S* S)⁻¹, é a definição concreta da fase exp(it log(S* S)) pelo resolvente. Não é uma igualdade por homônimo com alguma API abstrata de potências de LinearPMap: tal API não foi usada. `scalarTomitaImaginaryPower_unique` prova a unicidade entre mapas limitados que satisfaçam essa caracterização. Grupo, inversa e continuidade forte foram especializados ao objeto concreto.

## Pagamento e próximo consumo

O subpasso **construir Δ_ν^{it} a partir do mesmo Δ_ν=S* S** está pago pelos cinco módulos. Isso retira uma lacuna específica da implementação modular.

Ainda não foi provada a identificação

    U_t π_ν(a) U_−t = π_ν(λ_t a λ_−t)  para todo a∈regularCoreAlgebra P.

Os fornecedores da escala resolvente matricial e do transporte pelo J original continuam disponíveis; não devem ser reprovados. Os próximos lemas de ponte, ainda [OPEN], são:

1. **Escala funcional:** de TR=R Q_r, Q_r=T[rI+(1−r)T]⁻¹, obter U_t R=exp(it log r) R U_t. Transportar também b(Q_r)=b(T) r[rI+(1−r)T]⁻²; o cancelamento é por imagem densa. Esses nomes são descrições de obrigações, não alegações de declarações já existentes.
2. **Conjugação antiunitária:** de JTJ⁻¹=I−T, obter JU_tJ⁻¹=U_t. Conjugação de i e inversão do log cancelam os sinais. A fórmula com U_−t não é o alvo correto.
3. **Consumo dos geradores:** combinar essas pontes com `matrixUnit_polar_conjugate_generator`, `scalarTomitaPolar_regular_generator`, a aproximação `represented_levelExpectation_strong_tendsto` e `scalarGNS_commutation_from_generators`, para a identificação modular em toda π_ν(N).

A igualdade das automorfias não implica, isoladamente, igualdade literal U_t=π_ν(λ_t)R_−t; uma ambiguidade no comutante permanece possível. A consulta independente registra uma rota por vetores positivos regularizados caso esse consumidor adicional seja necessário. Não introduzir Γ(1), porque a unidade tem peso infinito.

Depois ainda faltam o gerador positivo h afiliado com h^{it}=λ_t e a perturbação por h⁻¹ que produza τ fiel, normal, semifinito, tracial e com τ∘θ_s=e⁻ˢτ. A invariância de ν não substitui essa construção. A cobertura de todo o predual por séries, aberta no adendo anterior, não foi necessária para construir o grupo e não deve virar uma camada obrigatória sem consumidor.

## Validação e limites

Cinco módulos, 39 declarações: compilação autora com Lean 4.31.0, sem avisos, só `propext`, `Classical.choice`, `Quot.sound`. Dois controles matemáticos adulterados foram recusados: duplicar a norma da fase e substituir s+t por s−t na lei concreta de grupo. Os fontes e objetos bons permaneceram idênticos após os controles.

As tentativas fracassadas, incluindo um timeout determinístico de elaboração no corolário de continuidade, foram preservadas. O timeout foi resolvido explicitando o tipo da função de composição, sem aumentar o limite de heartbeats. Os `sorryAx` que o Lean imprimiu em tentativas de elaboração malsucedidas pertencem exclusivamente a resultados recusados; não há `sorry` no fonte candidato.

A auditoria autora reconferiu 448 pares de dependências herdadas e todos os arquivos dos três manifestos anteriores. A revisão independente, com compilação própria, é registrada à parte e precisa estar concluída para a entrega ser emitida.

A1(a) permanece PAGO. A1(c) está PAGO no delta. **A1(b) permanece NÃO PAGO:** nem o habitante de RegularCoreTraceData nem uma impossibilidade tipada foram produzidos. A2–A7 não foram iniciados. Nenhum Python do programa, original canônico, resultado de natureza, memória de outra casa ou gate foi alterado. O objetivo A1 permanece ativo.


## Revisão e arquivos

Reprodução independente concluída: cinco compilações e auditor próprio das 39 declarações, objetos idênticos, sem avisos, nenhum P0/P1/P2. Parecer: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_FASE_RESOLVENTE_FINAL.md`. JSON: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_FASE_RESOLVENTE_FINAL.json`, SHA256 `79375e6ada4784fdd7ccfdea54993e3351430a7cb63062c0a24f2292d2134fe5`. Compilação: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\resolvent_phase39_independent_20260914_101512_721055\compilation.json`, SHA256 `7942155540ed0e866e3f1fe89a0ccc7a8723bf991e9cca56079d9f583a128de9`. Foram herdados e conferidos 448 pares de dependências; não foram todos recompilados.

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventPhaseFunctions.lean` — SHA256 `8eb2f7fb43b753d739c276b9e98655529860084586e311d94c8984cde361aea5`; objeto `4ea76e6e501af3a9b56d9f02d2263c210ab68806e287ab74c001380eb059eebd`; 9 declarações; execução `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_095907_662952`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventPhaseCalculus.lean` — SHA256 `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818`; objeto `774314761aedd48f91114349db843d8d23c674cbb73b741915c258d20790aff6`; 10 declarações; execução `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_100402_294282`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventImaginaryPowers.lean` — SHA256 `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`; objeto `f7784e9cec15f3bd5661743a5f920a99c70cf8b633e72bee77b1133d7d120e48`; 9 declarações; execução `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_100649_329613`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventImaginaryContinuity.lean` — SHA256 `8dd7a20376d00763bd8717227fa6bf7436f9eb11cbf4433caabb762d7719fdd4`; objeto `867a0a83324248a2cb18994e4d4afb7f35fef601675d3548c3b145faed546c3c`; 3 declarações; execução `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_101045_813310`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarTomitaImaginaryPowers.lean` — SHA256 `b8871f05b5b9605a8b193a8ed25346d79eac72d025d3ad95c8f9c884f28b4e52`; objeto `001ddbe8096f6f85f418e761297dbb8cc2ab4f2edd87ff4d292ec9dc15374737`; 8 declarações; execução `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_101128_096848`.

Manifesto `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\MANIFESTO_A1_POTENCIAS_IMAGINARIAS.json` — SHA256 `84aff22a3cabaa147519e7d23fa3fe0cac63551c2e0725cafd5e680e758a0794`. Total: 33 teoremas e 6 definições. As fontes finais estão congeladas; todos os hashes vêm dos bytes efetivos.

## Reprodução

```powershell
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ResolventPhaseFunctions.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ResolventPhaseCalculus.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ResolventImaginaryPowers.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ResolventImaginaryContinuity.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ScalarTomitaImaginaryPowers.lean
```

Essa ordem respeita os imports. O compilador cria tentativas novas; os scripts de registro são de execução única. Para os dois controles em probes/TGLExt, o resultado esperado é rc1 por erro matemático de elaboração, sem falha de import. Axiomas de todas as declarações aceitas: propext, Classical.choice, Quot.sound.

## Escopo de custódia

A cópia local do monólito permaneceu intacta; não foi executada. Não houve nova rodada integral porque só módulos Lean foram produzidos. O canônico já havia mudado externamente na leitura datada de CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; naquele confronto os 922 fontes embutidos coincidiam. Essa leitura não é uma afirmação de versão corrente nem igualdade atual dos monólitos. Aplicar as fontes sobre a versão corrente após auditoria da gerência.

## Ficha de aproveitamento anexa

# A1 — potências imaginárias pelo resolvente do mesmo S* S

[OPEN — ficha anterior ao código]

Consumidor: A1(b), identificação modular do peso dual escalar, etapa necessária para perturbá-lo pelo gerador e obter o traço escalado. Este módulo não habita sozinho o contrato do traço.

Reusar o S do peso completo, seu resolvente positivo injetivo T, o transporte por J, a extensão polar densa e a relação de escala matricial já provada. Introduzir somente a fase amortecida g_t(x)=x(1−x) exp(it log((1−x)/x)) e a extensão unitária que ela determina na imagem densa de T(1−T).

O grupo regular à esquerda/direita já existe. Sua invariância não identifica as potências de S* S. A construção pretendida parte do resolvente efetivo; não recebe outro operador modular por hipótese. Grupo, continuidade e identificação com a conjugação regular serão obrigações separadas até compilação efetiva.

Fornecedores, linhas, hashes lidos e busca estão no JSON. As seis modalidades da ficha A1 são herdadas, sem repetir o acervo. Nenhum novo predual abstrato é exigido aqui. Nenhum gate é alterado.
2026-09-14T09:55:41.985700-03:00

```json
{
  "timestamp": "2026-09-14T09:55:41.985700-03:00",
  "status": "FICHA_ANTES_DO_CODIGO",
  "consumer": "ORDEM_011 A1(b): modular implementation of the SAME scalarDualWeight, needed for perturbation by h^-1 to the faithful normal semifinite scaled trace on regularCoreAlgebra P. This bridge is not itself a trace contract inhabitant.",
  "exact_target": "T=scalarTomitaResolvent P=(I+S* S)^-1; b(x)=x(1-x); g_t(x)=b(x) exp(i t log((1-x)/x)). Construct U_t on ScalarGNSHilbert P with U_t b(T)=g_t(T), unitary group and strong continuity, then transport existing resolvent scaling to identify the modular action. No bounded inverse or spectral gap assumed.",
  "decision": "ADAPTAR bounded CFC and dense polar extension; NOVO damped imaginary phase and cancellation on dense range. Existing regular left/right groups do not identify imaginary powers of actual S* S; invariance is not KMS.",
  "scope": "A1 only; no repeated root construction or full abstract predual; no canonical edits; no experimental gate.",
  "providers": [
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarWeightTomitaIdentification.lean",
      "sha256": "d4b3043d6d76a9934d9778a0b1b7e604c26e8ffb2c1e3a7755964496ad520822",
      "declarations": [
        {
          "line": 12,
          "text": "theorem scalarWeightGNSEmbedding_sandwich_uniform (P : SiteProfile)"
        },
        {
          "line": 25,
          "text": "theorem scalarWeightTomitaGraph_subset_closure_original (P : SiteProfile) :"
        },
        {
          "line": 50,
          "text": "theorem scalarWeightTomitaGraph_closure_eq (P : SiteProfile) :"
        },
        {
          "line": 58,
          "text": "theorem scalarClosedTomita_graph_eq_weight (P : SiteProfile) :"
        },
        {
          "line": 65,
          "text": "theorem scalarWeightStar_mem_closedTomitaDomain (P : SiteProfile)"
        },
        {
          "line": 71,
          "text": "theorem scalarClosedTomita_extends_weight_star (P : SiteProfile)"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarTomitaResolvent.lean",
      "sha256": "50e9437f0a572187103933b7b4847b82599da0a687e439a3b7ab48735e2c3127",
      "declarations": [
        {
          "line": 14,
          "text": "def scalarTomitaResolvent : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :="
        },
        {
          "line": 18,
          "text": "theorem scalarTomitaResolvent_equation (z : ScalarGNSHilbert P) :"
        },
        {
          "line": 24,
          "text": "theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare P).domain) :"
        },
        {
          "line": 29,
          "text": "theorem scalarTomitaResolvent_norm_le (z : ScalarGNSHilbert P) :"
        },
        {
          "line": 32,
          "text": "theorem scalarTomitaResolvent_injective : Function.Injective (scalarTomitaResolvent P) :="
        },
        {
          "line": 35,
          "text": "theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent P :="
        },
        {
          "line": 38,
          "text": "theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent P ≤ 1 :="
        },
        {
          "line": 41,
          "text": "theorem scalarTomitaResolvent_selfadjoint : IsSelfAdjoint (scalarTomitaResolvent P) :="
        },
        {
          "line": 45,
          "text": "theorem scalarTomitaResolvent_graph :"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarTomitaPolarResolvent.lean",
      "sha256": "666ee0b78071dfd26dd566dacfdf3de53a24a59e232508be7e56448b36ef3dd9",
      "declarations": [
        {
          "line": 14,
          "text": "theorem scalarTomitaPositiveRoot_resolvent_graph (x : (scalarTomitaPositiveRoot P).domain) :"
        },
        {
          "line": 22,
          "text": "theorem scalarTomitaPolarFactor_resolvent (z : ScalarGNSHilbert P) :"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350BoundedInjectivePolar.lean",
      "sha256": "bd16c6727b6738718ba8e4c2c5009aef6c86d206240d6bead093f6ff65239b76",
      "declarations": [
        {
          "line": 15,
          "text": "def boundedMapModulus (C : H →L[ℂ] K) : H →L[ℂ] H := CFC.sqrt (C.adjoint.comp C)"
        },
        {
          "line": 17,
          "text": "theorem boundedMapGram_nonneg (C : H →L[ℂ] K) : 0 ≤ C.adjoint.comp C :="
        },
        {
          "line": 21,
          "text": "theorem boundedMapModulus_norm (C : H →L[ℂ] K) (x : H) :"
        },
        {
          "line": 30,
          "text": "theorem boundedMapModulus_injective (C : H →L[ℂ] K) (hi : Function.Injective C) :"
        },
        {
          "line": 34,
          "text": "theorem boundedMapModulus_denseRange (C : H →L[ℂ] K) (hi : Function.Injective C) :"
        },
        {
          "line": 41,
          "text": "def boundedInjectivePolar (C : H →L[ℂ] K) (hi : Function.Injective C)"
        },
        {
          "line": 46,
          "text": "theorem boundedInjectivePolar_modulus (C : H →L[ℂ] K) (hi : Function.Injective C)"
        },
        {
          "line": 51,
          "text": "theorem boundedMapGram_commutes_of_intertwines (C : H →L[ℂ] K)"
        },
        {
          "line": 64,
          "text": "theorem boundedInjectivePolar_intertwines (C : H →L[ℂ] K) (hi : Function.Injective C)"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DenseLinearPolarExtension.lean",
      "sha256": "2352e0b01e9ba17bb01914e98d1a778e454202430ce9e9a2042532fd0c34c159",
      "declarations": [
        {
          "line": 16,
          "text": "theorem denseLinearExtension_apply (x : E) : f.extendOfNorm e (e x) = f x :="
        },
        {
          "line": 19,
          "text": "theorem denseLinearExtension_norm (x : H) : ‖f.extendOfNorm e x‖ = ‖x‖ := by"
        },
        {
          "line": 24,
          "text": "def denseLinearIsometry : H →ₗᵢ[ℂ] K where"
        },
        {
          "line": 28,
          "text": "theorem denseLinearIsometry_surjective (hf : DenseRange f) :"
        },
        {
          "line": 39,
          "text": "def denseLinearEquiv (hf : DenseRange f) : H ≃ₗᵢ[ℂ] K :="
        },
        {
          "line": 43,
          "text": "theorem denseLinearEquiv_apply (hf : DenseRange f) (x : E) :"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350MatrixUnitResolventScaling.lean",
      "sha256": "f6b1271a8612a0695581ffc52afb45277ed0468bf941b42fcc8c8c3086877911",
      "declarations": [
        {
          "line": 15,
          "text": "theorem matrixUnit_resolvent_denominator_identity (P : SiteProfile) (N : ℕ)"
        },
        {
          "line": 41,
          "text": "theorem matrixUnit_resolvent_right_scaling (P : SiteProfile) (N : ℕ)"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350PositiveRootIntertwining.lean",
      "sha256": "f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5",
      "declarations": [
        {
          "line": 15,
          "text": "theorem real_cfc_intertwines (A B U : H →L[ℂ] H)"
        },
        {
          "line": 50,
          "text": "theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)"
        },
        {
          "line": 58,
          "text": "theorem positive_square_intertwines_roots (A B U : H →L[ℂ] H)"
        }
      ],
      "decision": "REUSAR"
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\ModularFlowLevel.lean",
      "sha256": "dd0b03747826991f3e697d3be3b297cdf4bf65350565215e9d6ae1944044a261",
      "declarations": [
        {
          "line": 28,
          "text": "def modularPhase (t r : ℝ) : ℂ := Complex.exp ((t * r : ℝ) * Complex.I)"
        },
        {
          "line": 30,
          "text": "theorem modularPhase_add (s t r : ℝ) :"
        },
        {
          "line": 37,
          "text": "theorem modularPhase_norm (t r : ℝ) : ‖modularPhase t r‖ = 1 := by"
        },
        {
          "line": 40,
          "text": "def flowLevel (P : SiteProfile) (t : ℝ) (N : ℕ)"
        },
        {
          "line": 44,
          "text": "theorem flowLevel_add (t : ℝ) (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 49,
          "text": "theorem flowLevel_smul (t : ℝ) (N : ℕ) (c : ℂ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 55,
          "text": "theorem flowLevel_zero_time (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 58,
          "text": "theorem flowLevel_group (s t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 63,
          "text": "theorem flowLevel_normSq (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)"
        },
        {
          "line": 67,
          "text": "theorem flowLevel_inner_self (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 71,
          "text": "theorem flowLevel_step (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        },
        {
          "line": 83,
          "text": "theorem flowLevel_push (P : SiteProfile) (t : ℝ) :"
        },
        {
          "line": 91,
          "text": "theorem flowLevel_continuous (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :"
        }
      ],
      "decision": "REUSAR"
    }
  ],
  "search": {
    "command": [
      "rg",
      "-n",
      "imaginaryPower|imaginary_power|resolventPhase|regular_dual_weight_modular|phase.*resolvent|resolvent.*phase",
      "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt",
      "-g",
      "*.lean"
    ],
    "returncode": 1,
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\BUSCA_A1_FASE_RESOLVENTE.txt",
    "sha256": "d5bfe6a529349a76b4732e94d78aa14855ac89614348807ddcdb830d09cac0c7"
  },
  "inherited_six_modalities": {
    "REAPROVEITAMENTO_A1.json": "17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327",
    "BUSCAS_A1.json": "d5b5ade4450c3df73ca9efcdda1ae005862f5f0debb39802cfb494e8beea7475",
    "OUTRAS_BANCADAS_HASHES.json": "5b826d9f8cfe3a92e34a1e6d83476617c3d5c3138937039526b90444d1c1fca2",
    "ADENDO_REAPROVEITAMENTO_A1.json": "c1e79521a1fd5f646064f5456813f565eee2561b15d37bebac1a7a4358da084e"
  }
}
```

Enunciados completos dos fornecedores, em suplemento documental datado posterior ao código (a ficha original anterior permanece intacta):

```json
{
  "timestamp": "2026-09-14T10:21:02.172541-03:00",
  "status": "POST_CODE_DOCUMENTARY_APPEND__PRIOR_FICHE_PRESERVED",
  "prior_fiche": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json",
    "sha256": "96836dffe4c78de2519a4257875da49315acd393f74e20490bb609e223071ba0",
    "timestamp": "2026-09-14T09:55:41.985700-03:00"
  },
  "reason": "Complements single-line locators with complete statements of sources already read before implementation. Does not retroactively claim this supplement existed before code.",
  "consumer": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\LACUNAS_A1.md",
    "sha256": "cf0ef3264d91c8033a399851407ca8b5f08deef63b850a2fcf62b2fc56ab581c",
    "line": 25,
    "statement": "2. **`regular_dual_weight_modular_implementation`**. Com os dados anteriores e a\n   identificação do fluxo da base com σ^φ, o grupo modular do peso ν satisfaz\n   σ^ν_t(A)=Λ(t) A Λ(t)* para todo A∈N e t∈ℝ. No GNS de ν, identificar o grupo\n   de Δ_ν com esse transporte e os domínios usados. A invariância ν∘AdΛ=ν já\n   provada não é a condição KMS nem caracteriza sozinha o grupo modular."
  },
  "providers": [
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarWeightTomitaIdentification.lean",
      "sha256": "d4b3043d6d76a9934d9778a0b1b7e604c26e8ffb2c1e3a7755964496ad520822",
      "declarations": [
        {
          "name": "scalarWeightGNSEmbedding_sandwich_uniform",
          "line": 12,
          "statement": "theorem scalarWeightGNSEmbedding_sandwich_uniform (P : SiteProfile)\n    (A : scalarWeightLeftIdeal P) (h : ℝ) (hh : 0 < h) :\n    scalarWeightGNSEmbedding P (scalarWeightSandwich P A h) =\n      scalarGNSStarEmbedding P ⟨regularSandwich P A.val h,\n        regularSandwich_mem_finiteDualStarCore P A.val h hh⟩"
        },
        {
          "name": "scalarWeightTomitaGraph_subset_closure_original",
          "line": 25,
          "statement": "theorem scalarWeightTomitaGraph_subset_closure_original (P : SiteProfile) :\n    scalarWeightTomitaGraph P ⊆ closure (scalarTomitaGraph P)"
        },
        {
          "name": "scalarWeightTomitaGraph_closure_eq",
          "line": 50,
          "statement": "theorem scalarWeightTomitaGraph_closure_eq (P : SiteProfile) :\n    closure (scalarWeightTomitaGraph P) = closure (scalarTomitaGraph P)"
        },
        {
          "name": "scalarClosedTomita_graph_eq_weight",
          "line": 58,
          "statement": "theorem scalarClosedTomita_graph_eq_weight (P : SiteProfile) :\n    Set.range (fun x : scalarClosedTomitaDomain P =>\n      ((x : ScalarGNSHilbert P),scalarClosedTomita P x)) =\n        closure (scalarWeightTomitaGraph P)"
        },
        {
          "name": "scalarWeightStar_mem_closedTomitaDomain",
          "line": 65,
          "statement": "theorem scalarWeightStar_mem_closedTomitaDomain (P : SiteProfile)\n    (A : scalarWeightStarCore P) :\n    scalarWeightStarEmbedding P A ∈ scalarClosedTomitaDomain P"
        },
        {
          "name": "scalarClosedTomita_extends_weight_star",
          "line": 71,
          "statement": "theorem scalarClosedTomita_extends_weight_star (P : SiteProfile)\n    (A : scalarWeightStarCore P) :\n    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,\n      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P (star A)"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarTomitaResolvent.lean",
      "sha256": "50e9437f0a572187103933b7b4847b82599da0a687e439a3b7ab48735e2c3127",
      "declarations": [
        {
          "name": "scalarTomitaResolvent",
          "line": 14,
          "statement": "def scalarTomitaResolvent : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P"
        },
        {
          "name": "scalarTomitaResolvent_equation",
          "line": 18,
          "statement": "theorem scalarTomitaResolvent_equation (z : ScalarGNSHilbert P) :\n    ∃ x : (scalarTomitaSquare P).domain,\n      (x : ScalarGNSHilbert P)=scalarTomitaResolvent P z ∧\n        (x : ScalarGNSHilbert P)+scalarTomitaSquare P x=z"
        },
        {
          "name": "scalarTomitaResolvent_inverse",
          "line": 24,
          "statement": "theorem scalarTomitaResolvent_inverse (x : (scalarTomitaSquare P).domain) :\n    scalarTomitaResolvent P ((x : ScalarGNSHilbert P)+scalarTomitaSquare P x)=\n      (x : ScalarGNSHilbert P)"
        },
        {
          "name": "scalarTomitaResolvent_norm_le",
          "line": 29,
          "statement": "theorem scalarTomitaResolvent_norm_le (z : ScalarGNSHilbert P) :\n    ‖scalarTomitaResolvent P z‖ ≤ ‖z‖"
        },
        {
          "name": "scalarTomitaResolvent_injective",
          "line": 32,
          "statement": "theorem scalarTomitaResolvent_injective : Function.Injective (scalarTomitaResolvent P)"
        },
        {
          "name": "scalarTomitaResolvent_nonneg",
          "line": 35,
          "statement": "theorem scalarTomitaResolvent_nonneg : 0 ≤ scalarTomitaResolvent P"
        },
        {
          "name": "scalarTomitaResolvent_le_one",
          "line": 38,
          "statement": "theorem scalarTomitaResolvent_le_one : scalarTomitaResolvent P ≤ 1"
        },
        {
          "name": "scalarTomitaResolvent_selfadjoint",
          "line": 41,
          "statement": "theorem scalarTomitaResolvent_selfadjoint : IsSelfAdjoint (scalarTomitaResolvent P)"
        },
        {
          "name": "scalarTomitaResolvent_graph",
          "line": 45,
          "statement": "theorem scalarTomitaResolvent_graph :\n    resolventGraphOperator (scalarTomitaResolvent P) (scalarTomitaResolvent_injective P) =\n      scalarTomitaSquare P"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarTomitaPolarResolvent.lean",
      "sha256": "666ee0b78071dfd26dd566dacfdf3de53a24a59e232508be7e56448b36ef3dd9",
      "declarations": [
        {
          "name": "scalarTomitaPositiveRoot_resolvent_graph",
          "line": 14,
          "statement": "theorem scalarTomitaPositiveRoot_resolvent_graph (x : (scalarTomitaPositiveRoot P).domain) :\n    (scalarTomitaResolvent P (x : ScalarGNSHilbert P),\n      scalarTomitaResolvent P (scalarTomitaPositiveRoot P x)) ∈ (scalarTomitaPositiveRoot P).graph"
        },
        {
          "name": "scalarTomitaPolarFactor_resolvent",
          "line": 22,
          "statement": "theorem scalarTomitaPolarFactor_resolvent (z : ScalarGNSHilbert P) :\n    scalarTomitaPolarFactor P (scalarTomitaResolvent P z)=\n      scalarTomitaPolarFactor P z - scalarTomitaResolvent P (scalarTomitaPolarFactor P z)"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350BoundedInjectivePolar.lean",
      "sha256": "bd16c6727b6738718ba8e4c2c5009aef6c86d206240d6bead093f6ff65239b76",
      "declarations": [
        {
          "name": "boundedMapModulus",
          "line": 15,
          "statement": "def boundedMapModulus (C : H →L[ℂ] K) : H →L[ℂ] H"
        },
        {
          "name": "boundedMapGram_nonneg",
          "line": 17,
          "statement": "theorem boundedMapGram_nonneg (C : H →L[ℂ] K) : 0 ≤ C.adjoint.comp C"
        },
        {
          "name": "boundedMapModulus_norm",
          "line": 21,
          "statement": "theorem boundedMapModulus_norm (C : H →L[ℂ] K) (x : H) :\n    ‖boundedMapModulus C x‖ = ‖C x‖"
        },
        {
          "name": "boundedMapModulus_injective",
          "line": 30,
          "statement": "theorem boundedMapModulus_injective (C : H →L[ℂ] K) (hi : Function.Injective C) :\n    Function.Injective (boundedMapModulus C)"
        },
        {
          "name": "boundedMapModulus_denseRange",
          "line": 34,
          "statement": "theorem boundedMapModulus_denseRange (C : H →L[ℂ] K) (hi : Function.Injective C) :\n    DenseRange (boundedMapModulus C)"
        },
        {
          "name": "boundedInjectivePolar",
          "line": 41,
          "statement": "def boundedInjectivePolar (C : H →L[ℂ] K) (hi : Function.Injective C)\n    (hd : DenseRange C) : H ≃ₗᵢ[ℂ] K"
        },
        {
          "name": "boundedInjectivePolar_modulus",
          "line": 46,
          "statement": "theorem boundedInjectivePolar_modulus (C : H →L[ℂ] K) (hi : Function.Injective C)\n    (hd : DenseRange C) (x : H) :\n    boundedInjectivePolar C hi hd (boundedMapModulus C x) = C x"
        },
        {
          "name": "boundedMapGram_commutes_of_intertwines",
          "line": 51,
          "statement": "theorem boundedMapGram_commutes_of_intertwines (C : H →L[ℂ] K)\n    (A : H →L[ℂ] H) (B : K →L[ℂ] K)\n    (h : C.comp A = B.comp C) (hs : C.comp (star A) = (star B).comp C) :\n    Commute (C.adjoint.comp C) A"
        },
        {
          "name": "boundedInjectivePolar_intertwines",
          "line": 64,
          "statement": "theorem boundedInjectivePolar_intertwines (C : H →L[ℂ] K) (hi : Function.Injective C)\n    (hd : DenseRange C) (A : H →L[ℂ] H) (B : K →L[ℂ] K)\n    (h : C.comp A = B.comp C) (hs : C.comp (star A) = (star B).comp C)\n    (x : H) : boundedInjectivePolar C hi hd (A x) = B (boundedInjectivePolar C hi hd x)"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DenseLinearPolarExtension.lean",
      "sha256": "2352e0b01e9ba17bb01914e98d1a778e454202430ce9e9a2042532fd0c34c159",
      "declarations": [
        {
          "name": "denseLinearExtension_apply",
          "line": 16,
          "statement": "theorem denseLinearExtension_apply (x : E) : f.extendOfNorm e (e x) = f x"
        },
        {
          "name": "denseLinearExtension_norm",
          "line": 19,
          "statement": "theorem denseLinearExtension_norm (x : H) : ‖f.extendOfNorm e x‖ = ‖x‖"
        },
        {
          "name": "denseLinearIsometry",
          "line": 24,
          "statement": "def denseLinearIsometry : H →ₗᵢ[ℂ] K where\n  toLinearMap"
        },
        {
          "name": "denseLinearIsometry_surjective",
          "line": 28,
          "statement": "theorem denseLinearIsometry_surjective (hf : DenseRange f) :\n    Function.Surjective (denseLinearIsometry f e hd hn)"
        },
        {
          "name": "denseLinearEquiv",
          "line": 39,
          "statement": "def denseLinearEquiv (hf : DenseRange f) : H ≃ₗᵢ[ℂ] K"
        },
        {
          "name": "denseLinearEquiv_apply",
          "line": 43,
          "statement": "theorem denseLinearEquiv_apply (hf : DenseRange f) (x : E) :\n    denseLinearEquiv f e hd hn hf (e x) = f x"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350MatrixUnitResolventScaling.lean",
      "sha256": "f6b1271a8612a0695581ffc52afb45277ed0468bf941b42fcc8c8c3086877911",
      "declarations": [
        {
          "name": "matrixUnit_resolvent_denominator_identity",
          "line": 15,
          "statement": "theorem matrixUnit_resolvent_denominator_identity (P : SiteProfile) (N : ℕ)\n    (i j : chainIdx N) :\n    scalarTomitaResolvent P * homogeneousRightGNS (matrixUnitRightData P N i j) *\n      scaledResolventDenominator (scalarTomitaResolvent P) (localEigenvalue P N i j) =\n    homogeneousRightGNS (matrixUnitRightData P N i j) * scalarTomitaResolvent P"
        },
        {
          "name": "matrixUnit_resolvent_right_scaling",
          "line": 41,
          "statement": "theorem matrixUnit_resolvent_right_scaling (P : SiteProfile) (N : ℕ)\n    (i j : chainIdx N) :\n    scalarTomitaResolvent P * homogeneousRightGNS (matrixUnitRightData P N i j) =\n      homogeneousRightGNS (matrixUnitRightData P N i j) *\n        scaledPositiveResolvent (scalarTomitaResolvent P) (localEigenvalue P N i j)"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350PositiveRootIntertwining.lean",
      "sha256": "f357246ac96d1d98fc1376238be4ca039f425d2782dd23d909ac5cdd3d1afaa5",
      "declarations": [
        {
          "name": "real_cfc_intertwines",
          "line": 15,
          "statement": "theorem real_cfc_intertwines (A B U : H →L[ℂ] H)\n    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*U=U*B)\n    (f : ℝ → ℝ) (hf : Continuous f) : cfc f A * U = U * cfc f B"
        },
        {
          "name": "positive_sqrt_intertwines",
          "line": 50,
          "statement": "theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)\n    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : A*U=U*B) :\n    CFC.sqrt A * U = U * CFC.sqrt B"
        },
        {
          "name": "positive_square_intertwines_roots",
          "line": 58,
          "statement": "theorem positive_square_intertwines_roots (A B U : H →L[ℂ] H)\n    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : (A*A)*U=U*(B*B)) : A*U=U*B"
        }
      ]
    },
    {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\ModularFlowLevel.lean",
      "sha256": "dd0b03747826991f3e697d3be3b297cdf4bf65350565215e9d6ae1944044a261",
      "declarations": [
        {
          "name": "modularPhase",
          "line": 28,
          "statement": "def modularPhase (t r : ℝ) : ℂ"
        },
        {
          "name": "modularPhase_add",
          "line": 30,
          "statement": "theorem modularPhase_add (s t r : ℝ) :\n    modularPhase (s+t) r = modularPhase s r * modularPhase t r"
        },
        {
          "name": "modularPhase_norm",
          "line": 37,
          "statement": "theorem modularPhase_norm (t r : ℝ) : ‖modularPhase t r‖ = 1"
        },
        {
          "name": "flowLevel",
          "line": 40,
          "statement": "def flowLevel (P : SiteProfile) (t : ℝ) (N : ℕ)\n    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ"
        },
        {
          "name": "flowLevel_add",
          "line": 44,
          "statement": "theorem flowLevel_add (t : ℝ) (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    flowLevel P t N (a+b) = flowLevel P t N a + flowLevel P t N b"
        },
        {
          "name": "flowLevel_smul",
          "line": 49,
          "statement": "theorem flowLevel_smul (t : ℝ) (N : ℕ) (c : ℂ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    flowLevel P t N (c • a) = c • flowLevel P t N a"
        },
        {
          "name": "flowLevel_zero_time",
          "line": 55,
          "statement": "theorem flowLevel_zero_time (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    flowLevel P 0 N a = a"
        },
        {
          "name": "flowLevel_group",
          "line": 58,
          "statement": "theorem flowLevel_group (s t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    flowLevel P s N (flowLevel P t N a) = flowLevel P (s+t) N a"
        },
        {
          "name": "flowLevel_normSq",
          "line": 63,
          "statement": "theorem flowLevel_normSq (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)\n    (i j : chainIdx N) : Complex.normSq (flowLevel P t N a i j) = Complex.normSq (a i j)"
        },
        {
          "name": "flowLevel_inner_self",
          "line": 67,
          "statement": "theorem flowLevel_inner_self (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    tInner P N (flowLevel P t N a) (flowLevel P t N a) = tInner P N a a"
        },
        {
          "name": "flowLevel_step",
          "line": 71,
          "statement": "theorem flowLevel_step (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    flowLevel P t (N+1) (towerStep a) = towerStep (flowLevel P t N a)"
        },
        {
          "name": "flowLevel_push",
          "line": 83,
          "statement": "theorem flowLevel_push (P : SiteProfile) (t : ℝ) :\n    ∀ {N M : ℕ} (h : N ≤ M) (a : Matrix (chainIdx N) (chainIdx N) ℂ),\n      flowLevel P t M (tPush h a) = tPush h (flowLevel P t N a)"
        },
        {
          "name": "flowLevel_continuous",
          "line": 91,
          "statement": "theorem flowLevel_continuous (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :\n    Continuous (fun t : ℝ => flowLevel P t N a)"
        }
      ]
    }
  ]
}

```
