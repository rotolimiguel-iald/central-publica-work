[DERIVED / INPUT / OPEN] Continuação espontânea 011 — entropia da torre, escala e purificação de corte. Derivação anterior ao código, 05/09/2026.

O turno anterior teve progresso: a entrega 010 ligou focalização e limite local de Clausius à reconstrução condicional de Einstein. H3, a lei entropia-área e sua origem no estado seguem abertos. O túnel ainda termina na ordem 007; o número 011 está livre.

## Pergunta que muda a próxima ação

O estado usado na torre é produto em seus sítios. A afirmação "a entropia é área" precisa dizer qual entropia, qual partição e qual área. Uma lei em número de sítios não é uma lei geométrica antes de haver uma correspondência. O trabalho desta rodada vai medir a entropia dos pesos efetivos towerW, sua relação com o gerador diagonal da primeira lei modular e as condições sob as quais uma contagem de corte pode lê-la como área.

## Rota e demonstração prévia

1. Definir S(p)=−Σ p_i log p_i, usando log natural e a convenção contínua 0 log 0=0. A identidade −xy log(xy)=y[−x log x]+x[−y log y] vale também quando um peso é zero. Para distribuições normalizadas, somar dá S(p⊗q)=S(p)+S(q). As marginais de p⊗q são p e q; sua informação mútua é zero. Essa entropia de densidade mista não será chamada indistintamente de emaranhamento.

2. Na torre canônica, towerW(P,N+1)=towerW(P,N)×siteW(P.w(N+1)), com normalização já provada. Por indução, S_N=Σ_{i=0}^N h(P.w_i), h=entropia binária. Para perfil constante p∈(0,1), S_N=(N+1)h(p), com h(p)>0. A ordem 003 já construiu um objeto de contagem normalizado com expectativa N+1; a igualdade será ligada a esse objeto efetivo.

3. Se uma área proposta A_N é sublinear na contagem, isto é, A_N/(N+1)→0, não pode satisfazer S_N=ηA_N para todos N com η constante finita. A prova é comparar os limites das duas densidades. Esse é um resultado CONDICIONAL à identificação de sítios com volume e à escala sublinear; não exclui toda leitura geométrica possível da torre. Se A_N=a(N+1), a mesma entropia admite S_N=[h(p)/a]A_N para qualquer a≠0: o estado não fixa a unidade de área.

4. Construir uma matriz de amplitudes bipartidas explícita Ψ(i,j)=δ_ij√p_i e a densidade pura ρ=|Ψ⟩⟨Ψ| no espaço completo. A positividade vem do produto externo; Σ|Ψ|²=1 pela normalização. A contração sobre o segundo índice produz ρ_L=diag(p), e a outra marginal também é diag(p). A densidade global é idempotente e de traço 1. Não se presume a redução como campo de uma estrutura: ela será calculada.

5. Instanciar p com towerW. A expectativa de qualquer observável esquerdo deve coincidir exatamente com tState(P,N). Isso fornece uma purificação correlacionada da mesma densidade canônica. Sua entropia reduzida é a soma de h dos pares; se os N+1 pares forem atribuídos a vínculos que cruzam um corte, S é proporcional ao número de vínculos. A atribuição ao corte e a área por vínculo são INPUT, não deduzidas.

6. O controle de custo é indispensável: a densidade pura no espaço bipartido completo não é fiel se há pelo menos dois índices. Um vetor de base (i,j), i≠j, é anulado; sua projeção tem expectativa zero. A restrição esquerda continua fiel porque seus pesos são positivos. Logo a purificação não entrega automaticamente a mesma construção modular em toda a álgebra bipartida e não remove o obstáculo de Borchers para a torre esquerda.

7. Controles: pesos (1/2,1/2) dão entropia reduzida log 2, pureza global, correlação não produto e informação mútua zero apenas para a densidade PRODUTO comparativa. Perfis p e 1−p têm entropia igual. A escala de área pode ser alterada enquanto η se altera reciprocamente, preservando o mesmo estado.

## Critérios e limites

Todos os teoremas novos terão #print axioms; somente propext, Classical.choice e Quot.sound passam. A entropia formalizada é a funcional diagonal −Σp log p, ligada ao operador diagonal −log p e à primeira lei canônica. Não se presumirá uma implementação de log de matrizes arbitrárias.

[KNOWN] A derivação termodinâmica de Jacobson recebe entropia de área como hipótese (https://arxiv.org/abs/gr-qc/9504004). A questão daqui é anterior àquela composição. A construção bipartida acima é calculada diretamente, não importada por citação.

[OPEN] Não há aqui mapa de regiões contínuas para fatores, área transversal geométrica, limite correlacionado com espectro modular contínuo, escolha de assinatura/dimensão, calor a partir da dinâmica ou demonstração de H3. Nenhum resultado de contagem será reclassificado como gravitação quântica concluída.

Escritas somente em Chatgpt. Originais, um.py, Atlas, memórias canônicas, selos, gate e entregas anteriores permanecem intactos. Sem dados observacionais. Backups de bytes e tentativas falhas serão preservados.
