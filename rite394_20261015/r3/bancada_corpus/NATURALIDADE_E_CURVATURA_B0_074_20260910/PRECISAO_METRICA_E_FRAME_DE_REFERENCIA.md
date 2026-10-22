# Precisão: apresentação métrica e frame de referência no ponto

10/09/2026, frente 074. [DERIVED — precisão de escopo]. Este arquivo novo acompanha `NORMALIZACAO_S_E_OBSTRUCAO_EULER.md` e restringe explicitamente o lema de sua seção2 à apresentação **métrica mínima**, com gauge de difeomorfismos. Não modifica a fonte.

O frame usado para normalizar g₀ é um frame ortonormal **do espectador no ponto de avaliação**. Os dois sistemas de coordenadas normais que ele determina, quando esse frame é mudado no mesmo ponto, diferem por uma transformação Lorentz constante entre suas coordenadas. É esse grupo de índices que aparece na projeção tensorial finita. Não é uma escolha de gauge local para um vielbein dinâmico.

Se se começa com se=L_c e+λe e faz uma mudança de frame A(x) inerte por s, então a equivariância exige

\[
\lambda'=A\lambda A^{-1}-(c^\mu\partial_\mu A)A^{-1}.
\]

Portanto o ghost Lorentz cru não transforma tensorialmente sob essas mudanças locais. Não se pode tratá-lo como uma variável tensorial adicional cuja normalização comuta automaticamente com todo o BRST de vielbein. Tampouco uma receita b_Nλ=0 é tornada equivariante apenas por uma projeção Lorentz no ponto.

Para importar o lema a partir de uma apresentação de vielbein, é preciso primeiro usar a equivalência BRST/BV **formal e local** métrica–vielbein já delimitada nas entregas anteriores, mantendo os pares contráteis e seus jatos até a retirada legítima. Alternativamente, deve-se construir o ghost covariantizado e conferir seu diferencial. Nenhuma dessas duas opções é demonstrada novamente nesta nota e o ghost cru não é consumido como se já obedecesse a ela.

Na apresentação métrica mínima, todos os campos/ghosts/antifields relevantes têm a lei natural de transformação por coordenadas. A transformação para coordenadas normais depende somente de B₀, que é s-inerte; por isso a demonstração N₀s=s_NN₀ conserva exatamente seu sentido. Não há um ghost adicional de gauge de frame nesse enunciado.

Os resultados da forma de Euler e de sua transgressão são métricos, invariantes por mudança de frame e permanecem inalterados. O critério de grau cinco continua condicionado ao complexo natural correto; ele não importa a conjugação b_N em uma apresentação de vielbein com λ cru.
