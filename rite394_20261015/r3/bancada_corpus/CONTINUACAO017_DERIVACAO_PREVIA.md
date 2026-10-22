[DERIVED / INPUT / OPEN] CONTINUAÇÃO 017 — regularidade superior do fluxo

06/09/2026. Derivação anterior ao código. O turno 016 foi progresso: sua custódia foi reconferida nesta sessão, 538 hashes, seis módulos limpos, 41 teoremas e quatro definições impressas. Permanecem no túnel somente as ordens gerenciais 001–007. O objetivo amplo continua ativo e não alcançado.

## Objetivo e cuidado com quantificadores

016 identifica a derivada do fluxo e estabelece C1 conjunto. É necessário avançar para C∞ no domínio aberto usado pela construção da congruência geodésica. Não basta fornecer, para cada ordem n, uma bola cada vez menor e alegar que sua interseção ainda tem raio positivo.

A própria definição de ContDiffAt ∞ da mathlib admite vizinhanças diferentes para cada ordem finita. Portanto um germe C∞ em (p,0) e um fluxo C∞ num aberto fixo são obrigações diferentes. A entrega marcará separadamente o que estiver demonstrado.

## Rota analítica antes da implementação

1. **Unicidade de germes de fluxo.** Duas famílias contínuas que resolvem a mesma ODE suave e têm a mesma condição inicial coincidem num produto de vizinhanças de (p,0). Deduzir uma constante local de Lipschitz para f, usar continuidade conjunta para manter ambas as trajetórias nessa vizinhança e aplicar a unicidade da ODE em um intervalo aberto comum. Não se compara a seleção de Classical.choice por identidade nominal.

2. **Indução finita pela equação variacional.** Para cada n natural e cada campo suave num aberto de um espaço de Banach real, construir um fluxo local Cn no germe inicial. No passo n→n+1, aplicar a hipótese de indução ao campo ampliado (f,Df∘J). Suas projeções Φ e J são Cn no germe. O teorema efetivo de derivada conjunta de 016 fornece DΦ[h,τ]=Jh+τf(Φ); esse operador é Cn. Pelo critério da derivada, Φ é C(n+1).

3. **Fixar a escolha.** Comparar o fluxo escolhido em cada ordem com um único fluxo já existente, usando (1). Assim toda ordem finita vale para a mesma função em (p,0), dando ContDiffAt ∞ nesse ponto. Estender a qualquer dado inicial interior de sua bola.

4. **Propagar ao intervalo inteiro.** Para um tempo T interior, usar um fluxo local centrado na posição de fase Φ(p,T), e comparar a solução recomeçada com a família original. A expressão de transição é Φ(q,s)=Ψ(Φ(q,t0),s−t0). A regularidade finita deve ser transportada ao longo do intervalo conexo, com uma justificativa de cobertura/propagação que alcance cada T. Somente depois de provar esse passo para cada n no mesmo domínio se conclui ContDiffOn ∞.

5. **Geometria.** Instanciar no campo de fase geodésico e reutilizar a preservação da nulidade já provada. Regularidade não escolhe, sozinha, uma seção transversal nem fornece o primeiro jato de equilíbrio. A inversão local e a congruência espacial continuam exigindo suas próprias provas.

## Critérios e controles

Cada ponte recebe enunciado próprio e #print axioms. Controles: igualdade local entre escolhas distintas de fluxo; campo nulo; solução plana afim; caso geodésico curvo já construído. Derivações de ordem superior nunca são recebidas como hipótese disfarçada no teorema de manchete.

Se a propagação temporal não estiver paga, o relatório registrará apenas os germes e a obrigação precisa restante, sem promover esses germes a C∞ num aberto. Também não haverá promoção de reconstrução clássica condicional a gravidade quântica geral.

## Custódia

Todas as escritas ficam em Chatgpt. Fontes próprias desta etapa são revisadas com backup de bytes e temporário verificado. Entregas anteriores, um.py, kernel canônico, Atlas, memórias, selos e gate permanecem intocados. Nenhum dado observacional. Auditoria independente a cargo da gerência.

## Adendo posterior à implementação — 06/09/2026

[REAL] Os passos 1–4 foram concluídos. flow_smooth_on_domain prova ContDiffOn ℝ ∞ no mesmo produto aberto de bola e intervalo do fluxo recebido. A etapa não termina no germe: a propagação por unicidade e conexão do intervalo foi formalizada.

[REAL] O fluxo geodésico definido em 016 agora tem suavidade C∞ conjunta demonstrada, com a preservação da nulidade anteriormente provada. Os controles do campo nulo, do fluxo plano polinomial e do fundo curvo passaram. Contagens lidas dos fontes: seis módulos, 18 teoremas e uma definição com axiomas impressos.

[OPEN] A escolha transversal, a inversa local da posição e a congruência espacial ainda não foram construídas. O primeiro jato de equilíbrio e as ligações microscópicas permanecem obrigações distintas. Este adendo registra o resultado posterior; a derivação anterior acima permanece preservada.

