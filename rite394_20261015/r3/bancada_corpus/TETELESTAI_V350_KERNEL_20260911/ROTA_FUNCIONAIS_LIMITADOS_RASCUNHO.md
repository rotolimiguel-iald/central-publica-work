# Funcionais limitados dominados pelo peso dual

[REAL — DEV compilado, não integrado nem revisado independentemente]

Três módulos/11 alvos: DualCutLinearMap (3), ScalarBoundedCuts (6) e
ScalarCutNormality (2). São resultados posteriores ao pacote de
normalidade da representação GNS e não entram no parecer desse pacote.

O corte dual de raio R já construído agora é um mapa linear complexo
limitado sobre operadores, com cota |2R|. A construção continua usando
integrais fortes sobre vetores, sem assumir continuidade ou integrabilidade
de Bochner da órbita em norma de operador.

Para v no Hilbert regular, define-se o funcional complexo limitado
ψ_(R,v)(A)=c⟨v,C_R(A)v⟩, com o mesmo c=(2π)^(-1) do peso dual.
Para R≥0 e A≥0 seu valor é um real não negativo, provado na ordem
parcial ComplexOrder; não se verificou apenas a parte real. Para
v=η, A no cone positivo da mesma N, ofReal(Re ψ_(R,η)(A))≤ν(A).
Para os raios naturais, ν(A)=sup_n ofReal(Re ψ_(n,η)(A)). Cada
funcional é limitado; o supremo pode ser infinito. Não se afirma
fidelidade de qualquer corte individual, nem normalização ψ_n(1)=1.

Os funcionais preservam limites de leituras ao longo de redes monótonas
fortemente convergentes. No enunciado específico de N, uma rede positiva
crescente não vazia dirigida, com supremo B interno, tem leitura
Re ψ_R(A_i)→Re ψ_R(B); o limite forte é construído dentro da prova.
Esse é o critério de continuidade monótona relevante à normalidade dos
funcionais positivos. Não se construiu interface predual ou prova geral
de equivalência com continuidade ultra-fraca.

Tentativas falhadas preservadas: coerção da função do LinearMap na cota
de mkContinuous; escopo ComplexOrder inicialmente ausente. As fontes
finais compilaram com rc0 e apenas propext, Classical.choice, Quot.sound.

[OPEN] A aproximação por funcionais está construída; faltam os mapas
GNS/entrelaçadores correspondentes e a estimativa ou família separadora
que imponha (0,y)∈fecho(G)⇒y=0. Não se deduziu fechabilidade da simples
existência dos cortes. Não se afirmou que η seja separante para N.
A passagem ao domínio escalar máximo também permanece aberta.

Motivação bibliográfica: o esboço do Teorema 3.12 de Masuda usa funcionais
normais positivos dominados para a passagem de pesos a álgebras de
Hilbert. A aproximação concreta acima é prova local separada; a citação
não fornece o próximo lema de fechabilidade nem substitui seu kernel.
[Masuda, p. 45](https://www.math.okayama-u.ac.jp/mjou/mjou60/_02_Masuda.pdf).

KMS, traço canônico, Three Locks/H1–H3, setor quântico interagente,
certificado consumido pelo gate e runtime integral continuam abertos.
Nenhum original foi modificado ou executado.
