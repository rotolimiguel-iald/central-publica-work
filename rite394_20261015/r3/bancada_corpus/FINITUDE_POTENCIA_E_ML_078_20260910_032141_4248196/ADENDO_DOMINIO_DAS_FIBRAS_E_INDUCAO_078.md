# Precisão do domínio das fibras e da indução diagramática

10/09/2026, adendo078 à [nota de potência e Mittag–Leffler](<C:/IALD/Central de Patentes/Chatgpt/FINITUDE_POTENCIA_E_ML_078_20260910_032141_4248196/POTENCIA_DERIVADAS_E_MITTAG_LEFFLER.md>), preservada. [DERIVED — correção de domínio e controle algébrico]. Nenhum resultado da nota principal é promovido ao BRST Einstein–sigma.

## 1. Correção da frase sobre fibras numéricas

Na seção6 da nota principal, a afirmação “em cada fibra numérica x=a” precisa ser lida separadamente para os anéis envolvidos:

- Para A=ℝ[x], avaliação em qualquer a real é canônica. A torre nas fibras tem transição multiplicação pelo número a; é ML tanto para a≠0 quanto para a=0.
- Para A=C∞₀, o anel de **germes em zero**, apenas a avaliação em zero é canônica. Um germe não determina um valor em um ponto a≠0: seus representantes podem coincidir perto de zero e diferir nesse ponto. Portanto a frase não deve ser aplicada a todas as fibras numéricas desse anel.
- Para A=C∞(I), funções definidas num intervalo fixo I que contém zero, todas as avaliações a∈I são canônicas. Este é outro anel; não se identifica com o anel de germes.

A não estabilização A⊃xA⊃x²A⊃… continua válida nos três domínios indicados: x^m=x^(m+1)f exigiria f=1/x fora de zero e impediria regularidade em zero. O cálculo lim¹≃ℝ[[x]]/ℝ[x] permanece restrito ao caso polinomial. A conclusão de que geração finita sobre coeficientes não garante ML não muda.

## 2. Controle concreto da mudança para germes suaves

Na torre polinomial com transições multiplicação por x, a sequência y_N=1 é enviada pela fórmula(8) da nota principal a

\[
 \sum_{N\ge0}x^N=\frac1{1-x}\quad\bmod\mathbb R[x].
\]

Essa série formal não é um polinômio, logo sua classe no lim¹ polinomial é não nula. No anel de germes suaves em zero, porém, a sequência constante a_N=1/(1−x) está definida e satisfaz

\[
 a_N-xa_{N+1}=1=y_N.
\]

Assim essa classe particular desaparece após a ampliação de coeficientes. Isso não decide o lim¹ inteiro da torre suave; demonstra diretamente por que a fórmula polinomial não pode ser transportada sem prova.

## 3. Precisão da cota diagramática

A indução da seção2 aplica-se aos grafos formados com vértices iniciais e contratermos **já conhecidos**, cuja cota d_v≤2+2L_v foi estabelecida em ordens anteriores da recorrência pertinente. O contratermo novo é escolhido para estender o termo assim calculado dentro da cota obtida. Um “grafo” composto apenas pelo próprio contratermo ainda desconhecido, sem linhas, não serve para provar a cota desse mesmo contratermo. As inserções marcadas e excessos diferenciais continuam sendo contabilizados como na nota principal.

Esta precisão não transforma o setor diagramático controlado numa apresentação finita de todo C_N. Permanecem abertas a comparação cohomológica e a condição ML do modelo efetivo. Nenhum arquivo anterior, entrega077, um.py, Lean ou CAS foi alterado/executado.
