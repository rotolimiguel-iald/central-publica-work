[DERIVED / INPUT / OPEN] Continuação 016 — dependência do fluxo nos dados iniciais

06/09/2026. Derivação anterior ao código. O turno anterior foi progresso: entrega 015 concluída e reconferida nesta sessão (518 hashes). Não chegou ordem gerencial posterior à 007. O objetivo de gravidade quântica geral permanece ativo e não alcançado.

## Alvo

A entrega 015 construiu um fluxo geodésico contínuo nos dados iniciais, suave no tempo, que preserva a nulidade. A entrega 014 precisa de um campo nulo geodésico suave no espaço-tempo. A passagem exige regularidade nos dados iniciais e inversão local de uma família transversal. Esta etapa trabalha na primeira exigência.

Não se tomará a matriz variacional como derivada por definição. O alvo é uma afirmação efetiva HasFDerivAt do mapa de fluxo em relação ao dado inicial.

## Rota analítica

Considere um campo suave f num aberto Q de um espaço real finito-dimensional E, e sua solução \(\Phi(p,t)\).

1. Reobter a existência local preservando a estimativa de Lipschitz da mathlib nos dados iniciais. O domínio será um produto de bola de dados iniciais e intervalo aberto comum; o fluxo permanecerá em Q. Generalizar o argumento de vizinhanças de 015 ao espaço de Banach necessário para o sistema variacional. Essa generalização será identificada como reutilização do argumento de Picard, não como descoberta matemática nova.

2. No espaço ampliado \(E\times L(E,E)\), usar o campo
\[
\mathcal V(p,J)=(f(p),Df(p)\circ J).
\]
Se f é suave, esse campo é suave. Com dado inicial \((p,I)\), Picard fornece simultaneamente \(\Phi(p,t)\) e \(J(p,t)\), com \(J(p,0)=I\) e \(J'=Df(\Phi)J\). A projeção de posição satisfaz a ODE original. A continuidade conjunta de J é consequência da existência ampliada.

3. Para dois dados p e q, denotar \(h=p-q\), \(D(t)=\Phi(p,t)-\Phi(q,t)\) e
\[
R(t)=D(t)-J(q,t)h.
\]
Derivar efetivamente:
\[
R'=Df(\Phi(q,t))R+
[f(\Phi(p,t))-f(\Phi(q,t))-Df(\Phi(q,t))D(t)].
\]
A estimativa de Lipschitz dá \(\|D(t)\|\le C\|h\|\). A continuidade de Df, uniformizada sobre um conjunto compacto que contém os trajetos, deve dar resto de Taylor menor que \(\varepsilon\|D(t)\|\) para dados suficientemente próximos.

4. Logo \(\|R'\|\le M\|R\|+\varepsilon C\|h\|\), com R(0)=0. Grönwall dá
\[
\|R(t)\|\le \varepsilon C\|h\|\,G(M,|t|),
\]
onde G é finito no intervalo local. Como \(\varepsilon>0\) é arbitrário, \(R(t)=o(\|h\|)\); isso identifica J com a derivada de \(\Phi(\cdot,t)\). O caso de tempos negativos exige reversão explícita do parâmetro ou uma estimativa simétrica.

5. Combinar a derivada nos dados iniciais com a derivada no tempo e sua continuidade. Para regularidade superior, a equação ampliada e a regularidade do campo permitem uma indução por prolongamento. Não se afirmará C∞ nos dados iniciais antes de esse passo estar provado.

## Critérios e controles

A construção variacional, a equação efetiva do resto, o limite de Grönwall e a identificação com a derivada devem ter enunciados distintos. Toda hipótese ainda recebida — por exemplo uma estimativa uniforme de Taylor não derivada — permanecerá nomeada. Se uma parte não fechar, o relatório indicará exatamente qual, sem promover existência de J a diferenciabilidade do fluxo.

Controles previstos: campo linear, cujo resto é zero; campo nulo, cujo diferencial do fluxo é a identidade; ligação do campo de fase geodésico de 015 à construção variacional. As provas finais serão compiladas conjuntamente e terão seus axiomas impressos. Tentativas falhas serão preservadas.

## Limites do objetivo

Mesmo com regularidade inicial provada, restam a escolha transversal, a inversão local da posição, o primeiro jato de equilíbrio, o horizonte imerso, a ligação microscópica entropia–área, o coeficiente físico, calor/Clausius/H3, a ponte modular e a globalização. Esses itens permanecem OPEN; não se declara gravidade quântica geral provada ou confirmada.

Escrita exclusivamente em Chatgpt, com backups exatos de bytes antes de revisões próprias. Entregas anteriores, um.py, kernel canônico, Atlas, memórias, selos e gate intocados. Nenhum dado observacional. A auditoria independente continua a cargo da gerência.

## Adendo posterior à implementação — 06/09/2026

[REAL] A etapa alcançou HasFDerivAt em ambos os sinais do tempo, HasStrictFDerivAt conjunto e ContDiffOn ℝ 1. O Taylor uniforme foi deduzido da suavidade, da continuidade conjunta e da compacidade apenas do intervalo temporal, sem exigir compacidade de bolas espaciais. Por isso o argumento final admite o espaço de Banach real da construção, além do caso finito-dimensional previsto.

[REAL] Foram verificados os controles do campo nulo, do resto linear nulo e do bloco de derivada da geodésica plana, além de um fluxo curvo C1 com nulidade preservada. A contagem foi lida dos fontes: seis módulos, 41 teoremas e quatro definições com axiomas impressos separadamente.

[OPEN] A indução de C∞ nos dados iniciais não está nesta entrega. O detalhe dos limites e a ligação à geometria constam de CONTINUACAO016_PARECER.md. Este adendo registra o resultado posterior; o texto da derivação prévia acima permanece preservado.

