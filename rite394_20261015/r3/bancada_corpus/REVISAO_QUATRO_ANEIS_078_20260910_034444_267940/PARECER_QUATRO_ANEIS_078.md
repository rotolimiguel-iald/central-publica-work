# Revisão independente — quatro anéis e os limites da torre auxiliar078

[DERIVED — revisão matemática escrita] Li integralmente LIM1_POLINOMIAL_ANALITICO_FORMAL_E_SUAVE.md e seu manifesto. Conferi as construções de Δ, dos quocientes, a realização por cortes, a divisão suave e o limite plano. A nota anterior sobre potência/ML e seu adendo de domínio são consumidos no alcance já revisto.

**Parecer favorável, sem correção material necessária.** A tabela é demonstrada para a torre auxiliar de espaços vetoriais reais com mapa de transição multiplicação por x. Não é uma classificação da torre BRST Einstein–sigma.

## 1. Categoria e não estabilização

A categoria foi especificada corretamente: produtos, núcleo e cokernel são algébricos, sobre ℝ. Para uma torre contável, o modelo por Δa=(a_N−xa_(N+1)) fornece os limites indicados. O parecer não usa um funtor derivado de espaços topológicos nem exige imagens fechadas em alguma topologia.

As inclusões ℝ[x] e ℝ{x} em ℝ[[x]] são inclusões aditivas. Em particular, não são ideais: contêm 1 e são subespaços próprios. Assim as expressões ℝ[[x]]/ℝ[x] e ℝ[[x]]/ℝ{x} devem ser lidas como quocientes vetoriais/aditivos, exatamente como a nota declara. A multiplicação por x também é aqui uma aplicação linear, sem tratá-la como homomorfismo unital de anéis.

A cadeia de imagens x^mA é estritamente decrescente em cada anel. Nos três primeiros, comparar ordens na origem exclui x^m∈x^(m+1)A. Nos germes suaves, a igualdade forçaria uma função igual a 1/x numa vizinhança perfurada, incompatível com continuidade na origem. Portanto nenhuma das quatro torres é ML. O fato de duas terem lim¹=0 não contradiz uma implicação suficiente ML⇒lim¹=0; mostra que a recíproca não vale nessa generalidade.

## 2. Cokernel nos três anéis com Taylor injetivo

Para y_N∈A, a série Φ(y)=Σx^N J(y_N) é bem definida formalmente, pois seu coeficiente de grau k só recebe N≤k. Não há convergência analítica disfarçada nesse passo, nem é preciso um raio de convergência comum para a sequência de germes analíticos.

Se y=Δa, a soma parcial telescopa para J(a0)−x^(N+1)J(a_(N+1)); o segundo termo desaparece coeficiente a coeficiente. O mapa y↦[Φ(y)] é sobrejetivo, tomando y_N constantes iguais aos coeficientes de uma série arbitrária.

Se Φ(y)=J(a0), o numerador a0−Σ_(j<N)x^j y_j tem ordem pelo menos N. A divisão por x^N permanece em A para polinômios, séries convergentes e séries formais. A expressão a_N é, portanto, legítima no mesmo anel. A subtração finita dá exatamente a_N−xa_(N+1)=y_N. Foram conferidos os sinais e os índices, inclusive N=0, onde a soma é vazia.

Isso prova o cokernel como quociente aditivo:
- ℝ[[x]]/ℝ[x] no caso polinomial;
- ℝ[[x]]/ℝ{x} no caso analítico;
- zero no caso formal.

Σx^N não é polinomial. ΣN!x^N tem raio de convergência zero e não pertence a ℝ{x}. Os dois quocientes, portanto, são não nulos. A notação x⁻N descreve uma divisão exata; não se adiciona um coeficiente singular ao anel.

## 3. Construção suave por cortes

A estimativa usada na nota é correta. Para f_n(x)=c_n x^nχ(x/r_n), escreva x=r_n z. Sua derivada de ordem j tem a forma c_n r_n^(n−j)∂_z^j(z^nχ(z)). A norma da última função é finita, por suporte compacto. Para os finitíssimos j<n, reduzir r_n torna todas as normas menores que 2⁻n; pode-se impor também r_n<r_(n−1)/2.

Fixado j, a cauda n>j da série de derivadas é uniformemente somável. Os n≤j dão apenas finitíssimos termos suaves. Logo a série define F∈C∞ e todas as derivadas podem ser calculadas por essa convergência. Como χ é igual a 1 perto de zero, a contribuição ao jato de ordem k vem somente de n=k, dando F^(k)(0)=k!c_k. O termo c0χ trata separadamente n=0.

Assim o Taylor suave é sobrejetivo. A construção depende dos coeficientes e das escolhas de raios; não fornece, pelo argumento dado, dependência analítica/natural em parâmetros. Uma afirmação posterior desse tipo exigiria outra prova.

[KNOWN — referência conferida] Consultei Borel, página impressa44, que afirma a possibilidade de prescrever arbitrariamente as derivadas em zero de uma função suave. A nota usa sua própria prova por cortes para o resultado necessário; não atribui esse método específico à página histórica. [Borel1895](https://www.numdam.org/article/ASENS_1895_3_12__9_0.pdf).

## 4. Sobrejetividade de Δ nos germes suaves

Para uma sequência arbitrária y_N, a sobrejetividade de Taylor permite escolher um germe a0 com Taylor Φ(y). O numerador na fórmula (1) tem seus primeiros N coeficientes nulos.

Para N≥1, o resto integral
b(x)/x^N=1/(N−1)!∫₀¹(1−t)^(N−1)b^(N)(tx)dt
é suave em zero. A dependência suave do integrando num intervalo compacto permite derivar sob a integral em cada ordem. Para N=0, não se usa essa fórmula: a0 já foi escolhido.

Cada a_N é assim um germe suave. A identidade Δa=y decorre de subtração de expressões finitas, antes de aplicar Taylor; por isso inclui também as partes planas. Não se está confundindo igualdade de Taylor com igualdade de germes. Cada identidade usa finitos representantes e vale numa vizinhança apropriada; o produto de germes não exige uma vizinhança única para todos os N.

A demonstração cobre todas as sequências e estabelece lim¹=0 no anel suave. O exemplo y_N=1 é apenas uma instância, não o fundamento da sobrejetividade geral.

## 5. Limite inverso e ideal plano

A multiplicação por x é injetiva em todos os anéis usados. Nos germes suaves isso continua verdadeiro apesar de haver outros divisores de zero: xf=0 implica f=0 fora da origem e, por continuidade, na origem.

Uma sequência compatível é determinada por a0 e existe precisamente se a0∈∩_N x^N A. Essa interseção é zero nos casos polinomial, analítico e formal. Para germes suaves, equivale à nulidade de todos os coeficientes de Taylor. A divisão integral fornece os quocientes suaves, e a injetividade de x garante sua compatibilidade. O resultado é o ideal dos germes planos.

O exemplo e^(−1/x²), completado por zero na origem, é um germe suave não nulo com essa propriedade. Isso explica por que o limite inverso suave é não trivial mesmo quando seu lim¹ é zero, e por que a sobrejetividade de Taylor não identifica os sistemas suave e formal.

## 6. Estatuto e limites

A prova confirma a tabela inteira no alcance anunciado. Não produz uma normalização que dependa naturalmente de B0, não preserva automaticamente a classe analítica de Q2 e não estabelece cotas de jatos, valência, contatos ou aridade de suas primitivas. A torre auxiliar continua sem identificação com H²/H³(C_N) gravitacionais.

[REAL — documental] O pin da nota e os pins das duas dependências coincidem com o manifesto. Os quatro arquivos lidos foram relidos e permanecem iguais. Nenhum original foi recapturado; nenhum script da fonte, CAS, Lean ou um.py foi executado/importado. Somente este parecer e seu recibo são novos.

**PASS_WRITTEN_FOUR_RINGS_REVIEW.** Não se declara ML do modelo real, remoção de anomalia, QME, resultado UV ou reconstrução geral.

## Pins medidos

- [LIM1_POLINOMIAL_ANALITICO_FORMAL_E_SUAVE.md](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_LIM1_COEFICIENTES_078_20260910/LIM1_POLINOMIAL_ANALITICO_FORMAL_E_SUAVE.md>) — 7194 bytes; SHA-256 2e0fd0a513cccdff8c9b647cd72f2447f515e975db1220eb7feb586078ed90a8.
- [MANIFESTO_LIM1_COEFICIENTES_078.json](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_LIM1_COEFICIENTES_078_20260910/MANIFESTO_LIM1_COEFICIENTES_078.json>) — 1572 bytes; SHA-256 c352a5651d686c496db2cff3f56fbe18c5087825e4ca3d51bad4b1ec6431aefa.
