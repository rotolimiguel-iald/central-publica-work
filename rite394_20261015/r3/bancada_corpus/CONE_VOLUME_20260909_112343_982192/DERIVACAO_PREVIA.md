# Cone nulo, volume e unicidade métrica — derivação prévia

[DERIVED — a verificar em Lean] Para A simétrico e g lorentziano, anular os vetores nulos de g força A=c g pelo lema canônico lorentz_tensor_null_rigidity. Positividade de ambas as formas numa mesma direção implica c>0. Igualdade dos volumes coordenados sqrt|det A|=sqrt|det g|, com det g não nulo, implica |c⁴ det g|=|det g|, logo c⁴=1. Portanto c=1 e A=g. Isso vale ponto a ponto, com fator potencialmente variável, sem ansatz de métrica.

O registro matemático conterá o conjunto de direções nulas, a densidade de volume coordenada e uma direção na qual a forma deve ser positiva. O teorema demonstrará que no máximo uma métrica realiza esse registro; não demonstrará que todo registro é realizável nem construirá tais leituras do estado quântico.

Controles: 2g conserva cone e positividade, evidenciando a necessidade da normalização de volume. -g conserva cone e volume em dimensão quatro, evidenciando a necessidade da convenção de sinal quando apenas uma candidata foi declarada LorentzByCongruence. A direção positiva fixa sinal da forma; não equivale a orientar temporalmente o espaço-tempo.

[OPEN] A seleção atual reconstrói probabilidades e amplitudes nas famílias declaradas. Ainda falta uma correspondência com direções tangentes/causalidade física e uma medida volumétrica independente; a injetividade do cociclo e a inclusão das álgebras de sítios não fornecem por si esses dados. Nenhuma lei de Einstein, Clausius, área ou conservação entra no registro deste módulo. A passagem a conexão/curvatura exige regularidade do campo recuperado; a passagem a cartas exige suas leis de transformação. A invariância de tétradas por Lorentz impede unicidade de E, mesmo quando g está fixada.

Pesquisa primária consultada: Parrikar e Surya, https://arxiv.org/html/1102.0936 , enunciado MHKML no início: a reconstrução conformal a partir da relação causal pressupõe espaços-tempos futuros e passados distinguíveis de dimensão maior que dois. Isso orienta uma futura lei de correspondência; não foi importado como prova Lean.
