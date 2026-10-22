[DERIVED / INPUT / OPEN] CONTINUAÇÃO 024 — perturbação térmica do estado da torre

06/09/2026. Derivação antes do código. A etapa 023 é classificada como PROGRESSO: seu auditor reconferiu 650 hashes, sete módulos, 63 teoremas e uma definição impressa. A leitura atual do túnel encontrou ordens 001–007. A árvore canônica v316 continua distinguindo H3, a origem modular da geometria, dimensão/assinatura e globalização. O objetivo amplo permanece ativo.

A etapa 023 construiu uma família unitária escolhida. Agora é preciso ligar a resposta a estados do próprio fator da torre. Há uma distinção inicial que não deve ser apagada: o fluxo modular real de omega preserva omega. O arquivo ModularPower.lean já contém modularFlow_fixes_omega e preservação de omegaState. Esta continuação reutilizará esses resultados, não os contará como descobertas novas.

Alvo: demonstrar a estacionariedade das restrições locais sob esse fluxo e construir uma família diferente, de PERTURBAÇÕES de estado, dentro da representação canônica. A família será definida do gerador modular local K_i=-log(p_i), sem eixo Hamiltoniano extra. Não será chamada de evolução unitária nem de dinâmica selecionada pelo acervo.

Para pesos estritamente positivos normalizados p em um andar finito, definir:

    K_i = -log(p_i)
    Z(s) = sum_i p_i exp(-s K_i)
    r_i(s) = p_i exp(-s K_i)/Z(s)
    mu(s) = sum_i r_i(s) K_i
    V_p(K) = sum_i p_i (K_i-mu(0))².

Z(s)>0 e r_i(s)>0 para todo s real. A normalização é efetiva. O parâmetro s desloca a potência da densidade: r_i(s) é proporcional a p_i^(1+s). O nome térmico refere-se a essa forma, sem atribuir temperatura física.

Derivadas esperadas:

    r_i'(s)=r_i(s)[mu(s)-K_i]
    mu'(0)=-V_p(K)
    S'(0)=-V_p(K)
    D'(0)=0.

A primeira lei de entropia refere-se à variação do estado, e não ao fluxo modular que o mantém fixo. A variância é não negativa; é zero exatamente quando K é constante no suporte estritamente positivo, ou seja, quando a referência é tracial. O código deve provar a condição exata ou declarar qualquer limitação.

Aplicar s=(ell_x(d)t)², onde ell_x(d)=w_x(d) vem de um covetor comum, como em 023. A trajetória resultante deve ter tangente inicial zero e:

    DeltaK(t)/t² → -ell_x(d)² V_p(K)
    DeltaS(t)/t² → -ell_x(d)² V_p(K)
    D(t)/t² → 0.

Essa parametrização quadrática é INPUT, escolhida para a resposta de equilíbrio de segunda ordem. A escolha não deve ser ocultada sob o nome de derivação modular. O sinal negativo, porém, deverá vir da variância do gerador local, sem escolher o eixo de 022.

Realização no fator original, para p=towerW(P,N):

    a_s = diag(sqrt(r_i(s)/p_i))
    Psi_s = towerPi(P,a_s) Omega
    omega_s(A)=<Psi_s,A Psi_s>.

Verificar norma um, positividade do estado vetorial, matriz reduzida do andar N e fidelidade no fator quando o filtro é invertível, com as hipóteses já disponíveis. Provar que o funcional é o mesmo ao representar um observável em um andar maior (coerência das inclusões). A família usa estados vetoriais no MESMO H da torre, não apenas um novo perfil com outro espaço de Hilbert. Não confundir coerência da representação de um observável com independência da escolha do andar N da perturbação. Normalidade só será afirmada no sentido/topologia efetivamente provado.

O fluxo modular real mantém os funcionais locais constantes; quando a variância é positiva, a curva térmica quadrática tem resposta não nula e não pode ser identificada com essa órbita de estado. A classe de estados foi ampliada por uma operação positiva normalizada, não por um novo tempo físico provado.

Ligação à gravitação:

    kappa_p = V_p(K)/pi
    T = kappa_p [w⊗w - (gInv(w,w)/2)g].

Usar os teoremas de conservação de 023, a área e calor efetivos de 020, e a identidade de entropia relativa de 021. A correspondência calor–modular deverá ser demonstrada para esse T e essa trajetória. A conservação ainda depende de fechamento/onda; a correspondência de área ainda equivale ao balanço nulo de Ricci. Não incluir como hipótese aquilo que o novo cálculo promete construir, nem declarar Einstein sem o antecedente de área.

Controles: referência tracial, que não muda; referência binária fiel não tracial com variância positiva; comparação com a órbita modular estacionária; conservação e obstrução de área anteriores continuam válidas. O caso N arbitrário deve estar nos enunciados da realização no fator, sem restringir todo o trabalho a um exemplo binário.

Fontes e estatuto: a família de Gibbs, a resposta por variância e a primeira lei para variações do estado são matemática conhecida. Jacobson, Entanglement Equilibrium and the Einstein Equation (arXiv:1505.04753), trabalha com variações da geometria e do estado e hipóteses de equilíbrio, não com uma afirmação de que o fluxo modular estacionário sozinho produz a equação de campo. A consulta é orientação conceitual; nenhum resultado físico será introduzido como axioma Lean.

Limites explícitos: a seleção física da família, do andar, do covetor, da parametrização quadrática, da equação de onda e da lei de área permanece INPUT/OPEN. Não há nova afirmação de dinâmica canônica, globalização, origem da dimensão/assinatura, superação da obstrução de Borchers ou resolução completa da gravidade quântica.

Escrita somente em Chatgpt. Originais, entregas anteriores, um.py, kernel canônico, memórias, Atlas, diários e gate intocados. Backups imediatos dos bytes antes de revisar artefatos próprios; fonte estável durante a compilação; tentativas falhas preservadas. A entrega deve citar hipóteses, axiomas e hashes medidos; incorporação e auditoria independente cabem à gerência.
