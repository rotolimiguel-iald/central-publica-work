# Derivação prévia — distribuição normalizada do registro angular

[INPUT] Um registro do codec contém 16 probabilidades Bernoulli, não uma distribuição única. A ponte proposta rotula explicitamente a componente (i,j) e o resultado b∈Fin 2, formando 32 resultados. A convenção é reflexão b=1, transmissão b=0.

Defina Q(x,(i,j),1)=p_ij(x)/16 e Q(x,(i,j),0)=(1−p_ij(x))/16. Cada par soma 1/16 e os 16 pares somam 1, mesmo fora de U. Em U, 0<p_ij<1 demonstra positividade de todos os 32 pesos. Suavidade resulta da composição afim componente a componente.

[DERIVED — a verificar] A recuperação p_ij=16·Q(x,(i,j),1) é exata, logo dois registros têm os mesmos pesos exatamente quando têm as mesmas probabilidades. A igualdade local em U também se transporta nos dois sentidos. A decodificação tensorial do codec pode consumir as probabilidades recuperadas e devolve o mesmo campo.

A imagem desta representação é o conjunto de pesos cujo par rotulado tem massa exatamente 1/16. A existência de um vetor normalizado arbitrário não basta para afirmar que ele pertence a essa imagem; o certificado de massa por par é explícito.

[OPEN] A escolha de rótulo uniforme 1/16 é representacional. Não demonstra produção física, observação efetiva, frequência estatística, modularidade do parâmetro de amostragem nem extração do vetor completo por um resultado único. Não identifica Fisher positivo com métrica lorentziana.

O núcleo entregará recordState, normalização global, positividade em U, suavidade em U, recuperação e injetividade. A forma média de Fisher poderá ser acrescentada apenas se ficar completamente ligada às hipóteses e não atrasar a interface exigida. Nenhum módulo anterior, original, Atlas ou um.py será alterado ou executado.
