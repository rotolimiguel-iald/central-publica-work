# Consulta — ordem dos reguladores originais
Data: 2026-09-14T22:23:53.011072-03:00

[DERIVED] A rota mínima é **CFC real no mesmo R**, usando a extensão com max já definida. Hipóteses: P arbitrário e **0 < ε ≤ η**. Conclusão proposta: regularInverseGeneratorCutoff P η ≤ regularInverseGeneratorCutoff P ε. Esta consulta não compila nem acrescenta teorema; a formalização dessa conclusão permanece [OPEN].

[REAL — leitura de fontes] A identificação exata Bε = cfc Fε R já está em [regularInverseGeneratorCutoff_cfc](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351InverseCutoffCFC.lean:62>), com ε>0. A função Fε é complexa de valor real, dada em :12 pela razão x/max(min(1,ε),1+(ε−1)x), x=Re z. Não é preciso redefinir corte, grupo ou gerador.

## Passo mínimo

Escreva apenas na demonstração fε(x)=x/dε(x), dε(x)=max(min(1,ε),1+(ε−1)x), para x real. Para x≥0 e ε≤η:

1. min(1,ε)≤min(1,η) e 1+(ε−1)x≤1+(η−1)x; portanto dε(x)≤dη(x).
2. 0<min(1,ε)≤dε(x), por ε>0.
3. Logo x/dη(x)≤x/dε(x), exatamente a orientação de [div_le_div_of_nonneg_left](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Algebra/Order/GroupWithZero/Basic.lean:1275>): (ha : 0 ≤ a) (hc : 0 < c) (h : c ≤ b) : a / b ≤ a / c.

**Manter o max é mais econômico:** não precisamos removê-lo, calcular sigmoid, restringir a x≤1 ou inverter um operador. A comparação vale em todo x≥0. O espectro real de R está nessa semirreta: [regularSpectralResolvent_nonneg](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351RegularPositiveGraph.lean:84>) e [spectrum_nonneg_of_nonneg](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Algebra/Algebra/Spectrum/Quasispectrum.lean:414>) já fornecem o requisito.

A continuidade real de fε vem da expressão com denominador positivo, ou da composição real de inverseCutoffFunction_continuous. Converter as duas igualdades complexas para CFC real com [cfc_real_eq_complex](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean:352>), usando a auto-adjunção decorrente de R≥0. Seu tipo é cfc f a = cfc (fun x ↦ f x.re : ℂ → ℂ) a; esta é precisamente a forma de Fε após desdobrar a definição. Há uso local desse adaptador em [scaledResolventCoordinate_cfc](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351ScaledResolventCalculus.lean:27>).

Aplicar então [cfc_mono](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean:926>) com f=fη, g=fε, a=R. Ele pede desigualdade pontual **no espectro** e ContinuousOn das duas funções. A desigualdade resulta na ordem dos CLM do Hilbert regular; a conversão anterior identifica esses CLM com os B originais. cfc_le_iff (:1037 do mesmo arquivo) também serve, mas traz uma equivalência e hipótese de auto-adjunção explícita desnecessárias para a etapa final. Trabalhar no ambiente B(H) aproveita as instâncias existentes; não instalar CompleteSpace no subtipo N.

## Alternativa pelo grafo

[DERIVED] É válida, mas acrescenta passos para obter somente ordem. Do fornecedor [regularInverseGeneratorCutoff_graph](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351InverseGeneratorCutoff.lean:50>) aplicado a Bηx e do [graph_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/TGLExt/V351InverseGeneratorCutoff.lean:99>) com ε resulta:
Bε(x + (ε−η) Bηx) = Bηx.
Por linearidade e extensionalidade:
Bε − Bη = (η−ε) • (Bε * Bη).

Ainda é preciso demonstrar que Bε e Bη comutam e que o produto é positivo. A comutação pode vir do mesmo CFC; [Commute.mul_nonneg](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/v/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean:292>) dá então positividade a partir das duas positividades e da comutação. Com η−ε≥0, a identidade fornece a ordem. Isso exige identidade de CLM, comutação e produto positivo além dos adaptadores. É útil se o próximo consumidor também exigir a identidade resolvente; para a ordem isolada, recomendo a primeira rota. Não se usa inversa limitada de h nem positividade de produto arbitrário não comutante.

## Fronteira e proveniência

[REAL] Nomes, tipos, linhas e hashes dos oito arquivos consultados estão no JSON anexo. Busca delimitada aos módulos dos cortes e APIs pertinentes; não é inventário exaustivo de toda a casa. Não localizei nos dois módulos dos cortes um lema pronto de antitonia; a ligação escalar/CFC acima é a obrigação residual concreta.

[OPEN] A ordem não é afirmada para parâmetros sem positividade; a definição totalizada em ε=0 não autoriza tal extensão. Esta consulta não paga ordem de pesos por si só nem tracialidade, não revisa V351AllPositiveWeightOrder e não modifica os 19 deltas entregues. Nenhuma execução Lean/Lake, monólito, auditoria autoral ou memória.
