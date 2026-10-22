# Revisão parcial A1 — funções e CFC da fase do resolvente

Data: 2026-09-14T10:09:50.764238-03:00. **[REAL — inspeção independente somente leitura de dois fontes e evidências autorais]**. Escopo fechado desta leitura: **19 declarações = 9 + 10, quatro definições e quinze teoremas**. Nenhum P0, P1 ou P2 identificado nesse escopo.

**Limite da evidência:** não executei Lean nesta rodada, em respeito à solicitação de revisão somente leitura. Os dois rc0 e os 19 relatórios de axiomas são das execuções autorais identificadas abaixo, relidos e confrontados por script independente. Não há nova recompilação/auditor Lean próprio a reivindicar. A toolchain é a mesma nos dois comandos autorais (Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)); seu executável foi relido e pinado no JSON. O terceiro módulo, continuidade dos operadores e especialização ao T do peso ficam fora deste parecer.

| Módulo | SHA256 fonte corrente | SHA256 olean corrente | Alvos |
|---|---|---|---:|
| `V351ResolventPhaseFunctions` | `8eb2f7fb43b753d739c276b9e98655529860084586e311d94c8984cde361aea5` | `4ea76e6e501af3a9b56d9f02d2263c210ab68806e287ab74c001380eb059eebd` | 9 |
| `V351ResolventPhaseCalculus` | `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818` | `774314761aedd48f91114349db843d8d23c674cbb73b741915c258d20790aff6` | 10 |

Os snapshots das tentativas finais são byte a byte iguais às fontes atuais. Tentativas aceitas para leitura: `20260914_095907_662952` e `20260914_100402_294282`. Ambos os run.json têm rc0, stderr vazio, stdout sem warning/error e exatamente os nomes esperados; todos os 19 conjuntos de axiomas estão no trio `propext`, `Classical.choice`, `Quot.sound`. Foram identificadas 5 tentativas anteriores com snapshots dos mesmos módulos; seus códigos constam do JSON e nenhuma foi usada como aceite final. O hash do olean corrente foi medido; run.json não fornece um hash histórico do binário para confronto, logo não alego comparação com um olean independente ou com snapshot binário da tentativa.

## Significado e hipóteses

1. **Functions:** b(x)=x(1−x) e g(t,x)=b(x)·exp(i·t·Real.log((1−x)/x)). Os sete teoremas são universais em parâmetros reais, sem pressupor 0≤x≤1. As identidades de norma, tempo zero, soma, estrela e Gram estão orientadas corretamente. A continuidade demonstrada é conjunta em ℝ×ℝ, portanto fornece também a continuidade global em x para cada t.

2. **Continuidade global:** a implementação dispensa corretamente a extensão por zero sugerida como opção na consulta. Mathlib define o log real de número negativo como log do módulo, e o de zero como zero. Fora de x=0,1, o quociente é não nulo e `Real.continuousAt_log` se aplica sem exigir positividade. Nas pontas, ||g(t,x)||=||b(x)||→0 controla qualquer variação de t. Não se atribui continuidade à fase não amortecida. O comportamento escolhido fora de [0,1] não afeta a interpretação futura para um resolvente positivo contrativo. Referências: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\Log\Basic.lean` linhas 120 e 378, hash no JSON.

3. **Calculus:** H está declarado como `Type`, com `NormedAddCommGroup H`, `InnerProductSpace ℂ H` e `CompleteSpace H`. Não há SiteProfile nem escolha de outro peso nesta camada genérica. T é um operador complexo limitado em H. C_t é efetivamente `cfc (fun z : ℂ => g(t,z.re)) T`; a função é contínua complexa, não holomorfa, que é precisamente o requisito do CFC contínuo utilizado.

4. **Hipóteses por resultado:** identificação de b(T), tempo zero, produto e Gram recebem `IsSelfAdjoint T`; positividade de b(T), identificação do módulo e identidade das normas vetoriais recebem `0≤T` e `T≤1`. `resolventPhaseOperator_star` é formulado para todo T, conforme a operação CFC total da biblioteca; isso não amplia os demais resultados a T arbitrário. Injetividade de T ou de 1−T **não é premissa nem conclusão deste par de módulos**.

5. O resultado é C_s C_t=b(T)C_(s+t), C_0=b(T) e C_t* C_t=b(T)²; não é ainda a lei de um grupo unitário. A mesma lei de produto com (t,−t), combinada com estrela, também fornece C_t C_t*=b(T)² por derivação curta, ainda não como alvo separado. A igualdade `boundedMapModulus C_t=b(T)` usa corretamente positividade de b(T) e `CFC.sqrt_mul_self`. `resolventPhaseOperator_norm` é igualdade de **normas de vetores**, para cada x, não uma alegação de ||C_t||=1.

6. Casos T=0 ou T=I fazem b(T)=C_t=0 e não contradizem os teoremas. Seriam incompatíveis com concluir unitariedade nesta camada; tal conclusão não está no código. A aplicação futura à fase de Δ precisa pagar as duas injetividades/imagem densa. O sinal +it log((1−x)/x) coincide com λ^it quando x=(1+λ)^−1, λ>0. Nenhum gap ou inversa limitada de b(T) é introduzido.

## Proveniência e fronteira

Li integralmente os dois fontes e a ficha MD/JSON. O script relê os pares fonte/objeto das **448 entradas** de DEPENDENCIAS_A1_FASE_RESOLVENTE.json: todos correspondem aos pins declarados. Isso verifica bytes, não recompila nem reanalisa matematicamente as 448 dependências. Os oito fornecedores listados na ficha também correspondem aos hashes lidos. As fontes novas não contêm comandos `axiom`, `sorry`, `native_decide` ou `trustCompiler`, segundo inspeção e busca independente; a ausência de axiomas proibidos foi conferida também no stdout final.

A ficha anterior ao código conserva corretamente o alvo mais amplo como OPEN e separa construção unitária, grupo, continuidade forte e identificação da ação. Esses pagamentos não são atribuídos aos 19 alvos. Não há identificação nova com scalarTomitaSquare, modularidade/KMS, traço, predual completo ou promoção de gate. A1(b) continua **[OPEN]**. Originais, fontes, objetos autorais, monólito e memórias não foram modificados ou executados; apenas este relatório, script e evidência própria em revisao foram escritos.

## Inventário exato dos alvos

Namespace de todos: `TGLV350.Regular`. Enunciados completos extraídos da fonte, hipóteses de seção, comandos, hashes de streams e mapa de axiomas estão no JSON acompanhante.

| Declaração | Tipo | Locador |
|---|---|---|
| `resolventDamping` | def | V351ResolventPhaseFunctions.lean:14 |
| `resolventPhaseFunction` | def | V351ResolventPhaseFunctions.lean:17 |
| `resolventPhaseFunction_norm` | theorem | V351ResolventPhaseFunctions.lean:20 |
| `resolventPhaseFunction_zero_time` | theorem | V351ResolventPhaseFunctions.lean:24 |
| `resolventPhaseFunction_add` | theorem | V351ResolventPhaseFunctions.lean:28 |
| `resolventPhaseFunction_star` | theorem | V351ResolventPhaseFunctions.lean:34 |
| `resolventPhaseFunction_gram` | theorem | V351ResolventPhaseFunctions.lean:44 |
| `resolventPhaseFunction_joint_continuous` | theorem | V351ResolventPhaseFunctions.lean:51 |
| `resolventPhaseFunction_continuous` | theorem | V351ResolventPhaseFunctions.lean:79 |
| `resolventDampingOperator` | def | V351ResolventPhaseCalculus.lean:13 |
| `resolventPhaseOperator` | def | V351ResolventPhaseCalculus.lean:15 |
| `resolventDampingOperator_cfc` | theorem | V351ResolventPhaseCalculus.lean:18 |
| `resolventDampingOperator_nonneg` | theorem | V351ResolventPhaseCalculus.lean:26 |
| `resolventPhaseOperator_zero` | theorem | V351ResolventPhaseCalculus.lean:31 |
| `resolventPhaseOperator_star` | theorem | V351ResolventPhaseCalculus.lean:37 |
| `resolventPhaseOperator_mul` | theorem | V351ResolventPhaseCalculus.lean:43 |
| `resolventPhaseOperator_gram` | theorem | V351ResolventPhaseCalculus.lean:54 |
| `resolventPhaseOperator_modulus` | theorem | V351ResolventPhaseCalculus.lean:60 |
| `resolventPhaseOperator_norm` | theorem | V351ResolventPhaseCalculus.lean:67 |
