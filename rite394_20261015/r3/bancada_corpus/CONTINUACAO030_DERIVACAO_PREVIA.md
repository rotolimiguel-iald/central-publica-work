[INPUT / OPEN] CONTINUAÇÃO 030 — cociclo global e gerador de verossimilhança

06/09/2026. Derivação anterior ao código. Escrita apenas em Chatgpt. A ordem vigente é a 007; não há ordem 030. A pergunta do operador sobre cociclo, pi, área e túnel orienta esta etapa.

Revalidação: a entrega 029 existe e preserva H3 geral como OPEN. O Atlas agora declara incorporação das entregas 024–026 na v318; isso não é incorporação presumida de 027–029. A consulta imediatamente anterior trouxe evidência que muda a próxima ação: o artigo arXiv:2601.07915 relaciona ações de cociclo e área, mas sua seção 6.2 já usa a restrição gravitacional linearizada. Não pode ser importado como derivação de Einstein sem essas premissas. A consulta foi progresso de investigação, sem nova prova Lean.

Fontes externas consultadas: https://arxiv.org/html/2601.07915v1, seções 6.2 e 7.1; https://arxiv.org/html/2007.00230v1, seção 2. O primeiro trabalha perturbativamente com modos de borda e horizonte; sua eq. 7.6 compara valores esperados e o texto distingue o cociclo dependente do estado do operador de área. O segundo explicita a rapidez 2 pi s em uma identificação modular geométrica. Nenhum deles demonstra a identificação TGL.

Objeto que falta na bancada: as 026–029 construíram estados produto normais na mesma representação e transportaram seus operadores modulares. Não foi encontrada uma construção global do cociclo relativo na álgebra original. A sombra finita TGLExt.Cocycle não constitui essa construção.

Derivação proposta

Fixar a referência produto p=(1/3,2/3), amplitudes b_n entre 0 e 1/12 com soma finita, h(t)=t²/(1+t²) e q_n(t)=1/3-b_n h(t), como na 028. Manter t (variação do estado) e s (tempo modular) distintos.

Para a projeção e_n=pi_n(E00), definir
  ell0_n(t)=log(q_n(t)/(1/3));
  ell1_n(t)=log((1-q_n(t))/(2/3));
  L_n(t)=ell0_n(t)e_n+ell1_n(t)(1-e_n).
As projeções de sítios distintos comutam, são autoadjuntas e têm norma no máximo 1. As razões estão em intervalos positivos uniformes. As desigualdades de log dão |ell0|<=4 b_n h(t) e |ell1|<=2 b_n h(t); logo ||L_n||<=6 b_n h(t). Isso fornece convergência em norma da série L(t)=sum_n L_n(t), autoadjunção e pertinência à álgebra da torre e ao centralizador modular.

Para cortes finitos, a soma L_{<=N} deve coincidir com pi(diag(log q_{<=N}-log p_{<=N})). Esta igualdade precisa ser provada, não apenas nomeada. Definir u_t(s)=exp(i s L(t)). Verificar unitariedade, continuidade em norma no parâmetro s, lei de grupo no caso diagonal comutante, invariância pelo fluxo de referência e, consequentemente, a lei torcida u_t(s+r)=u_t(s) sigma_s(u_t(r)). Demonstrar que os cociclos finitos convergem a esse operador.

A comparação de estados deve usar R(t)=exp(L(t)/2): demonstrar R(t)Omega=amplitudeVector(b,t), usando os filtros de preparação e seu limite efetivo da 026. Assim omega(R A R)=amplitudeState(b,t)(A), com normalização medida, e não por redefinição do estado. Comparar a conjugação por u com os fluxos modulares locais da 027; promover ao fator somente com topologia e densidade justificadas.

Se houver tempo analítico suficiente nesta etapa, ligar a leitura de L ao limite de entropia relativa da 028. O enunciado exato de cada resultado deve distinguir o cociclo construído da identificação completa com o operador modular relativo não limitado e com a entropia de Araki; essas identificações exigem prova própria. Não dar a um operador unitário o nome de área. Não supor que pi fornece uma escala dimensional, nem que aperiocidade seleciona a métrica.

Controles obrigatórios: b=0 dá L=0 e u=1; distinguir t=0 de s=0; testar um perfil com infinitos sítios alterados, já existente na 028. Verificar se um único gerador positivo pode representar este cociclo: os logaritmos locais têm sinais opostos, portanto não promover L a área positiva sem prova. O controle plano de 028 continua impedindo a inferência H3 a partir só do estado e calor.

Critérios: fontes novas, compilação Lean com axiomas impressos, logs de todas as tentativas, hashes medidos e entrega para auditoria independente. A área geométrica, a seleção de região/álgebra, a dinâmica gravitacional e a prova ampla permanecem abertas até demonstrações correspondentes. Nenhum original ou arquivo já selado será alterado.


ADENDO 06/09/2026 — esclarecimento do operador, anterior ao teste angular

[INPUT] O operador esclareceu: a area candidata nao seria L, mas a leitura quadratica do fator de fase; chama L de cauda/poco e associa a angulacao ao retorno da luz e estabilizacao. Essa leitura fisica permanece [ONTO/CONJECTURE]. O L da bancada e definido como gerador de log-verossimilhanca; nao foi identificado formalmente com a algebra de cauda.

[DERIVED — proposta de teste] Para u(s)=exp(i s L), testar F(s)=(u(s)-I)* (u(s)-I), onde o primeiro fator recebe adjunta. F e positivo, vale 2I-u-u*, e F(s)/s^2 tende em norma a L^2 quando s vai a zero. Sua leitura vetorial e ||(u-I)xi||^2. Essa quantidade depende da referencia de fase; no espaco projetivo a metrica usa variancia, retirando a fase global. A identificacao com area de uma tela exige uma ponte adicional e escala dimensional.

A ordem dos parametros precisa ser testada: s e tempo modular; t varia o estado. Nesta familia regular L(t)=O(t^2), logo, para s fixo, F_t(s)=O(t^4); a resposta entropica anterior e em geral de ordem t^2. Essa obstrucao pertence a esta escolha de familia e leitura, nao a toda possivel interpretacao da proposta do operador. Nenhuma troca entre s, t, raiz quadrada ou normalizacao sera feita implicitamente.

Atualizacao de leitura: o Atlas passou a declarar v319 e incorporacao 027–028. Nao foi executado o programa original para certificar esse registro. A extensao da covariancia global foi feita pelo duplo comutante, dispensando a rota WOT sugerida inicialmente. O controle de sinal de L nao refuta a area quadratica esclarecida pelo operador; o teste relevante passa a ser positividade, invariancia de fase e ordem da resposta.
