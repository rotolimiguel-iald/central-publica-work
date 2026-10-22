# Continuação049 — multiplicadores contínuos e conjugação no L²
[DERIVED — derivação registrada antes da fonte; elaboração Lean pendente]

Autoria: agente review_global_cocycle. Escopo: construir um novo modelo matemático concreto em H=L²(ℝ,dξ;ℂ), sem transportá-lo da torre-produto e sem alegar identificação geométrica/BW.

Para c real, escrevemos D(ξ)=√(e^(cξ)+e^(-cξ)), a(ξ)=e^(cξ/2)/D(ξ), b(ξ)=e^(-cξ/2)/D(ξ). O denominador é estritamente positivo. As funções são contínuas, estritamente positivas, satisfazem a²+b²=1 e, portanto, são limitadas por 1. Além disso a(-ξ)=b(ξ), b(-ξ)=a(ξ), e b=e^(-cξ)a. Essa forma é igual a a=(1+e^(-2cξ))^(-1/2), b=e^(-cξ)a.

Multiplicação por a e por b define operadores complexos lineares contínuos A e B em H: a dominação pontual dá ‖Af‖≤‖f‖ e ‖Bf‖≤‖f‖. Igualdades quase em toda parte provam AB=BA e A²+B²=I. A realidade dos pesos, aplicada à fórmula integral do produto interno L², prova autoadjunticidade. A positividade estrita de a prova injetividade de A. A mesma fórmula integral dá Re〈Ah,Bh〉=∫ab|h|²≥0.

A reflexão ξ↦−ξ preserva Lebesgue. Sua composição com conjugação complexa fornece a anti-isometria involutiva Jf(ξ)=conj(f(-ξ)). A troca dos pesos por reflexão prova JA=BJ e JB=AJ.

O módulo abstrato BoundedGraphOperator construirá T com domínio range A e grafo {(Ah,Bh)}. As identidades acima pagam suas hipóteses de domínio denso, fechamento, autoadjunticidade e positividade. Logo T é aqui um operador efetivamente construído a partir de multiplicadores. A integração S=JT e o subespaço padrão Fix(S) serão feitas pelo módulo genérico do coordenador.

A identificação efetiva do domínio usa b=ma, m=e^(-cξ). Se f=Ah, então mf=Bh está em L². Reciprocamente, dado f e mf em L², h=Af+B(mf) está em H e Ah=f por a²+abm=a²+b²=1. Essa identidade evita presumir multiplicação limitada por 1/a. Para c≠0, mf=λf concentra f no conjunto {ξ:mξ=λ}; esse conjunto é vazio ou singleton, logo nulo para Lebesgue, e f=0.

[OPEN neste registro] A elaboração dos dois últimos alvos dependerá das APIs efetivamente implementadas e compiladas. O núcleo A/B/J terá prioridade. A construção não identifica Δ^it por nome, não usa Fourier sem sua convenção 2π e não prova inclusão semilateral, BW, rede de álgebras, seleção da dimensão, H3 ou gravidade quântica. O parâmetro c e o modelo L² são INPUT matemáticos explícitos.

Custódia: apenas novos arquivos049 em Chatgpt. Nenhum canônico, Atlas, memória ou selo≤048 será alterado. Revisões preservam os bytes anteriores em backup imediato; publicação de estatuto REAL exige elaboração medida e revisão independente.
