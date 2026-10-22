# Identificação com o oscilador — demonstração escrita

[DERIVED — escrito, não formalização Fock/QFT em Lean nesta folha]

Seja H=ℓ²(N), com base ortonormal |n>. No domínio denso D das sequências de suporte finito, defina a|0>=0, a|n>=√n |n−1> para n≥1 e a†|n>=√(n+1)|n+1>. Todas as operações abaixo atuam em D, que é preservado por a e a†; não há produto de operadores fora do domínio.

Em cada vetor da base, aa†−a†a=I. Para X=a+a†, segue em D:

X² = a²+(a†)²+2a†a+I,
:X²: = a²+(a†)²+2a†a = X²−I.

O termo subtraído é o valor de vácuo <0|X²|0>=1. Isto é a normal ordenação relativa a esse vácuo, neste oscilador.

Considere S=span{|0>,|2>} e E:C²→H, E(z_0,z_1)=z_0|0>+z_1|2>. A ortonormalidade da base torna E isométrica. Temos:

a²|2>=√2|0>,  (a†)²|0>=√2|2>,
2a†a|0>=0,    2a†a|2>=4|2>.

Logo E† :X²: E = [[0,√2],[√2,4]] = O. Componentes em |4> saem da compressão; não se afirma invariância de S por :X²:.

Para ψ=(2√2/3,−1/3), o estado de Fock é |Eψ><Eψ|. Sua norma é um e sua matriz restrita a S é

ρ=[[8/9,−2√2/9],[−2√2/9,1/9]].

A positividade decorre de ρ=ψψ†. O traço vale 8/9+1/9=1 e as probabilidades na base |0>,|2> são 8/9 e 1/9. O estado é puro e de posto um: não é fiel/invertível na álgebra matricial M₂(C).

A expectativa de :X²: nesse vetor é exatamente a da compressão O:

Tr(ρO)=2(−2√2/9)√2+(1/9)4=−4/9.

A negatividade está no valor do observável relativo ao vácuo, não na probabilidade de um resultado. Como X é simétrico em D,

<Eψ,X²Eψ>=‖XEψ‖²=5/9.

Isso também segue da matriz: X|0>=|1> e X|2>=√2|1>+√3|3>. Assim, na base de saída |1>,|3>, a restrição X E tem matriz B=[[1,√2],[0,√3]]. Portanto

E†X²E=B†B=[[1,√2],[√2,5]]=O+I,
Tr(ρ(O+I))=5/9.

Esta é a compressão de X². Não é o quadrado da compressão de X: E†XE=0, porque X troca paridade. Confundir as duas operações apagaria precisamente a contribuição que está sendo calculada.

## Relação com a família Gibbs positiva

[REAL — identidade utilizada da biblioteca; ver recibo da folha para sua nova composição] Em direção g-nula, a soma finita de stresses covetoriais satisfaz T(v,v)=Σ_j weight_j c_j (w_j(v))². Com weight_j≥0 e c_j=k_j/(πcosh²k_j), k_j>0, todos os termos são não negativos. Portanto a família positiva não representa o número −4/9 como valor nulo desse tensor.

[DERIVED — limite de interpretação] O cálculo do oscilador não identifica O automaticamente com uma componente nula do stress renormalizado de uma teoria de campos. Ele mostra, por um estado positivo concreto, que a negatividade de uma expectativa renormalizada não exige probabilidades negativas. Uma proposta que queira abranger tais respostas precisa explicar seu observável e ampliar o protocolo quando a restrição algébrica anterior impedir a representação.

[KNOWN — contexto externo] Expectativas negativas de energias renormalizadas em teorias quânticas de campos e limites para suas médias são tratados em [C. J. Fewster, Lectures on quantum energy inequalities](https://arxiv.org/abs/1208.5399). Essa referência contextualiza a distinção; não é usada como substituto da dedução matricial acima nem como identificação entre O e o stress da TGL.

[OPEN] Não se deriva daqui quantização completa da gravidade, falsificação da TGL, validade física de cinética negativa ou liberdade ilimitada de energia negativa. A prova Lean associada formaliza a matriz finita e a restrição da família Gibbs; esta identificação Fock é uma demonstração matemática escrita separada.
