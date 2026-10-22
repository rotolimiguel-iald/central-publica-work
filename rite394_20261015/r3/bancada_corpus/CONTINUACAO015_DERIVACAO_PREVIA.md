[DERIVED / INPUT / OPEN] Continuação 015 — existência de geodésicas nulas e fluxo no espaço de fases

06/09/2026. Derivação anterior ao código. O turno anterior foi progresso: a entrega 014 foi concluída e sua custódia foi reconferida agora (527 hashes, nove módulos Lean). Nenhuma ordem gerencial posterior à 007 foi encontrada. O objetivo amplo permanece ativo e não foi alcançado.

O alvo seguinte é reduzir a hipótese de existência geométrica da entrega 014. Uma curva geodésica nula e um campo geodésico suave numa região são objetos diferentes. Esta etapa tentará construir o fluxo de geodésicas para dados iniciais gerais e localizar precisamente a passagem ainda necessária para um campo de congruência. Não se atribuirá à primeira construção o tipo da segunda.

## Derivação

No espaço de fases \(\mathbb R^4\times\mathbb R^4\), definimos
\[
\mathcal G_\Gamma(x,v)=(v,-\Gamma_x(v,v)),\qquad
\Gamma_x(v,v)=\left(\sum_i v^i\Gamma_i(x)\right)v.
\]
Uma conexão suave no aberto U torna esse campo suave em U×R⁴, pois suas componentes são somas finitas de produtos suaves. A existência de Picard–Lindelöf fornece uma solução local \((x(t),v(t))\) e uma família contínua para dados iniciais próximos, com \(x'=v\) e \(v'=-\Gamma(v,v)\). O teorema de continuidade conjunta da mathlib local pode ser aplicado após obter os parâmetros de Picard a partir de C¹. Restringiremos o domínio a um produto de bola de dados iniciais e intervalo de tempo, mantendo x(t) em U.

Para uma métrica suave g compatível com Γ, a diferenciação efetiva dá
\[
\frac{d}{dt}g_{x(t)}(v(t),v(t))
=g(v',v)+(\partial_vg)(v,v)+g(v,v').
\]
Com \(L=\sum_i v^i\Gamma_i\), compatibilidade implica \(\partial_vg=L^Tg+gL\), e \(v'=-Lv\). Os três termos se cancelam. A energia g(v,v) é constante no intervalo, logo dados iniciais nulos produzem geodésicas nulas. Se v inicial é não nulo, continuidade permite reduzir o intervalo para preservar v(t)≠0. A família deverá preservar essa propriedade uniformemente em dados iniciais próximos, se construída no aberto de velocidades não nulas.

No caso de uma solda suave invertível E,D, as entregas anteriores já provam a compatibilidade e suavidade de \(\Gamma=\mathrm{LC}(E^T\eta E)\). O teorema final deve receber a solda e o vetor nulo inicial, sem receber um campo V pronto. A assinatura e a dimensão continuam INPUT.

A biblioteca contém um teorema de regularidade da solução no tempo: uma solução de ODE cujo campo é suave é suave em intervalos fechados internos ao domínio. Tentaremos usá-lo para a curva de fase. A busca nos diretórios Analysis e Geometry não localizou um teorema pronto que dê suavidade conjunta em relação aos dados iniciais; isso é uma observação da busca, não uma prova de inexistência de tal resultado na biblioteca.

## Passagem que ainda precisa ser paga

Para obter o V suave usado em 014, é preciso escolher dados iniciais numa hipersuperfície transversal, provar regularidade conjunta do fluxo, mostrar invertibilidade local da projeção \((s,t)\mapsto x_s(t)\) e então definir \(V(x_s(t))=v_s(t)\). A condição de equilíbrio do horizonte exige controle do primeiro jato dessa escolha. A existência contínua de um fluxo no espaço de fases não fornece, por si só, essas etapas.

Se essa passagem não puder ser formalizada nesta etapa, o manifesto registrará o enunciado que de fato foi provado e manterá congruência suave, imersão e equilíbrio como OPEN. A área e a ligação entropia–área não serão substituídas por literais.

## Controles previstos

- Conexão zero: geodésicas afins com posição \(x+tv\), velocidade constante, energia conservada.
- Conexão conformal curva já usada em 014: instância a partir dos dados \((0,(1,1,0,0))\), demonstrando aceleração coordenada não nula no início e nulidade preservada.
- Dados iniciais diferentes em velocidade podem ocupar a mesma posição: distinguir o fluxo de fase da escolha de um campo no espaço-tempo.
- Compilação conjunta dos novos módulos com o resultado 014 e impressão dos axiomas de todos os teoremas.

## Fonte de contexto e limites

[KNOWN] Jacobson usa uma congruência nula normal a uma superfície espacial, com expansão e cisalhamento nulos no ponto, e assume a relação de entropia com área e o equilíbrio de Clausius. A fonte não resolve essas hipóteses microscópicas: [Thermodynamics of Spacetime, 1995](https://arxiv.org/html/gr-qc/9504004). As provas geométricas locais desta etapa serão verificadas pelas definições e pela mathlib, sem novo axioma importado de física.

[OPEN] Entropia–área microscópica, coeficiente físico, corrente de calor, Clausius/H3, ponte modular–geométrica, seleção de assinatura/dimensão e globalização continuam no objetivo amplo. Nenhuma confirmação da gravidade quântica é declarada.

Escrita só em Chatgpt. Backup exato de bytes antes de revisões próprias; artefatos anteriores imutáveis; nenhum um.py executado/importado/editado. Kernel canônico, Atlas, memórias, selos e gate não são tocados. Tentativas falhas e avisos serão preservados. Auditoria adversarial da gerência continua necessária antes de incorporação.
