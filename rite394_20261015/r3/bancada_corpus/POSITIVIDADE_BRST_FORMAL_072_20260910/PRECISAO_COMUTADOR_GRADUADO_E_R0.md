# Precisão do comutador graduado e da inversa R₀

10/09/2026, arco 072. [DERIVED — correção matemática ao lado]. A nota `ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md` e seu manifesto original permanecem intactos. Este adendo corrige a frase de tradução de convenções no §2; não modifica os resultados de positividade ou a recorrência dos vetores.

## 1. Ordem do comutador: o fator de paridade é necessário

Para Q ímpar e A homogêneo de paridade p,

\[
[A,Q]_{\rm gr}=AQ-(-1)^pQA
             =-(-1)^p[Q,A]_{\rm gr}.
\]

Mantemos como convenção desta nota a equação (2.3):

\[
d_zA={i\over\hbar_*}[Q,A]_{\rm gr}
    =-(-1)^p{i\over\hbar_*}[A,Q]_{\rm gr}.
\]

Logo a afirmação do §2 de que bastaria Q→−Q para inverter a ordem precisa ser limitada a **A par**, caso dos observáveis físicos considerados. Para A ímpar, os dois comutadores graduados são iguais; trocar também Q por −Q introduziria um sinal indevido. A tradução de uma referência que escreve a carga à direita deve conservar o fator graduado acima e as convenções de derivação esquerda/direita da referência.

As provas das seções 4–6 usam a convenção fixada (2.3), a simetria e a nilpotência de Q; não usam a frase de conversão incorreta. A identidade [Q,[Q,A]_gr]_gr=[Q²,A] continua válida para ambos os valores de p. A ação nos observáveis de ghost zero e a positividade do estado não mudam.

## 2. Escolha explícita de R₀ no certificado de quartetos

Na realização algébrica da seção 3, escolha

\[
R_0=\left.N_{\rm aux}^{-1}h_{\rm qt}\right|_{\operatorname{im}Q_0},
\]

onde N_aux⁻¹ vale 1/m no setor auxiliar m>0 e zero em m=0. Para v∈im Q₀, temos Q₀v=0 e Pv=0. Como Q₀ e h_qt preservam N_aux e {Q₀,h_qt}=N_aux,

\[
Q_0R_0v=N_{\rm aux}^{-1}(N_{\rm aux}-h_{\rm qt}Q_0)v=v.
\]

Essa é uma inversa direita no domínio declarado, suficiente para (5.2). Ela não envolve divisão por frequência física nem resolve, por si, a obrigação Hadamard/Wick de P₀. O pin deste adendo e os pins relidos dos dois arquivos congelados constam do novo manifesto complementar.
