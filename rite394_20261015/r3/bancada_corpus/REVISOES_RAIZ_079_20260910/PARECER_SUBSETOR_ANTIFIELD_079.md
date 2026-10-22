# Revisão da raiz — fatoração do subsetor puro em antifields079

10/09/2026. [DERIVED — revisão matemática escrita independente da autoria]. Li integralmente ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md. Parecer favorável no alcance declarado.

A identificação p=g0g0 h*/v0, q=−C*/(2v0) respeita s0p=Hh e s0q=div p. No fundo Einstein com mapa sigma constante, variar a identidade de Bianchi dá div H=0; os termos de variação de conexão multiplicam a equação de fundo nula.

Conferi o lema de símbolo. Para p²≠0, o núcleo do símbolo de Einstein é p⊙B. A dupla curl polinomial então zera no aberto denso e, portanto, identicamente. Com N=n+r, a contração de duas derivadas em p fornece
N(N−1)A−(N−1)(p⊙D)+ppS=0.
A expressão B=(D−pS/(2(N−1)))/N reproduz A=p⊙B. Ela é polinomial, natural, linear nos coeficientes e não divide por p². Em grau zero, A=0.

Para uma identidade de operadores PH=0, a autoadjunticidade do símbolo identifica o símbolo superior de P com esse núcleo. A contração com tensor simétrico produz o fator 2B para a divergência. Quantizar com derivadas covariantes simetrizadas e subtrair B_(r−1)div reduz a ordem e preserva a identidade, pois div H=0. A indução termina no grau zero. Todos os termos inferiores de curvatura permanecem no próximo resto; não foi suposta uma covariantização de uma primitiva coordenada.

Assim P=B div, e χ5=Bq tem ghost2, valência cinco, espécie C*C⁴. Temos s0χ5=b5 e s1b5=−s0s1χ5. A correção é +s1χ5 e pode conter h*hC⁴ e C*C⁵. O argumento sigma por símbolo de onda invertível exclui identidades adicionais nesse bloco constante.

Essa prova trata CICLOS PUROS com b4=Q=0. Não elimina uma contribuição antifield que só fecha junto com P ou Q. Não afirma ausência de soluções Killing, nem exatidão global de equações hiperbólicas, nem exatidão relativa módulo divergências, nem admissibilidade automática de contratermos Q2.

[KNOWN — definição conferida] A noção de operador de compatibilidade universal exige fatorar qualquer identidade diferencial; ela não se reduz a verificar uma composição nula. Conferi essa definição na seção2 de [Khavkine](https://arxiv.org/pdf/1805.03751). A nota distingue a compatibilidade do operador Killing, tratada naquela fonte, da fatoração particular para o Hessiano Einstein demonstrada aqui. Não se importou um teorema homônimo.

Aceito a demonstração natural finita no domínio declarado. Zero execução CAS/Lean nesta revisão; hashes no registro. Cancelamento da classe residual inteira e QME permanecem abertos.
