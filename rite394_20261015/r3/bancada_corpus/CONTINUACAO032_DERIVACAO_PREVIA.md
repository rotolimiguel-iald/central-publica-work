[INPUT / DERIVED / OPEN] CONTINUAÇÃO 032 — comutação modular com domínio

06/09/2026. Derivação anterior ao código. A etapa 031 foi progresso efetivo, reconferido por auditor somente leitura: PASS, quatro módulos limpos, 51 teoremas e 13 definições impressas, 753 hashes de bytes. A ordem vigente continua 007; não há ordem nova na via de ida. Os originais e as etapas seladas permanecem somente leitura.

[INPUT] A etapa 031 construiu o fecho efetivo S_rel=S_omega R e o operador relativo Delta_rel=R Delta_omega R, com domínio {x: R x em D(Delta_omega)}. O filtro R=exp(L/2) e seu inverso V=exp(-L/2) são limitados, autoadjuntos e inversos em M. A etapa 030 prova R fixo por sigma_omega. Esta etapa pretende pagar a invariância de domínio e a comutação, não atribuí-las por nome.

[DERIVED — rota espectral da torre original] A torre tem uma família total de vetores locais v_Nij, com Delta v=lambda v e U_s v=exp(i s log lambda)v. O domínio e a auto-adjunticidade de Delta foram pagos por testes fracos em todos os andares; weak_delta_mem_graph é a ponte disponível para reconhecer um novo par no gráfico.

Primeiro provar que duas frequências reais são iguais quando exp(i s a)c=exp(i s b)c para todo s e c não nulo. A derivada em s=0 dá i a c=i b c e permite os cancelamentos. Isso não usa igualdade apenas em tempos discretos nem ignora a ambiguidade de período.

Segundo, se U_s x=exp(i s r)x para todo s, o transporte unitário do produto interno mostra que <v_Nij,x> é zero ou log(lambda_Nij)=r. Logo os testes fracos de Delta com todos os v_Nij dão o par (x,exp(r)x). Estender os testes a qualquer matriz local pela decomposição finita em unidades matriciais. O teorema de gráfico fraco então prova x em D(Delta), além do valor Delta x=exp(r)x.

Terceiro, se um operador limitado B comuta com cada U_s, Bv_Nij tem a mesma frequência que v_Nij e satisfaz Delta Bv=B Delta v. A extensão ao domínio inteiro deve usar o núcleo de gráfico já construído: x_N=P_N x, Delta x_N=P_N Delta x, com ambos convergindo. A continuidade de B e o fechamento de Delta passam o par (B x_N,B Delta x_N) ao limite. Uma rota equivalente para B autoadjunto usa diretamente os testes fracos; declarar qual foi formalizada.

Quarto, aplicar a R e V: sigma_s(R)=R equivale à comutação com U_s. Demonstrar o mesmo para V, por inversão ou pela exponencial de -L/2. Como RV=VR=I, a preservação em ambos sentidos identifica os domínios originais e relativos. Então Delta_rel x=R Delta(Rx)=R² Delta x=exp(L) Delta x em D(Delta). O produto tem esse domínio explícito; sua positividade e auto-adjunticidade vêm da igualdade com o operador da 031.

[OPEN] Essa comutação no domínio é uma etapa para o cálculo espectral, não a identificação automática de potências imaginárias. Para Connes pode-se formalizar o cálculo relativo ou uma caracterização equivalente, como Pedersen–Takesaki. O cone natural é via possível, não pré-requisito obrigatório. A igualdade com o J polar exige prova própria se utilizada.

[OPEN] A inscrição angular e a área física continuam distintas. Nenhuma resposta nova à operação pretendida pelo operador foi recebida. Esta etapa não seleciona superfície, escala, mapa região-álgebra ou dinâmica estabilizadora. A reconstrução gravitacional geral e a prova ampla seguem abertas.

Verificação: limites de cálculo moderados; operadores explícitos nos argumentos para evitar inferência explosiva; usar lemas genéricos de transporte em vez de expandir a torre dentro de provas de domínio. Cada teorema com axiomas impressos; fontes finais limpas; erros, interrupções e backups dos bytes preservados. Escrita somente em Chatgpt, entrega aditiva pelo túnel; sem executar ou editar originais, memórias, kernel canônico, um.py ou gates.
