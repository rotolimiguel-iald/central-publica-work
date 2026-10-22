# Derivação prévia045_B — dicotomia de relógios comuns

[INPUT] Frente B da ORDEM_010. Apenas arquivos novos na bancada Chatgpt; fontes anteriores, acervo e memórias permanecem somente leitura. Esta derivação precede a escrita do novo módulo e não registra compilação.

[DERIVED — reutilização037/040] Fixe uma amplitude somável b, B=amplitudeMass(b)>0 e eta>0. A calibração quadrática anterior escolhe r=2 log(2) B/eta>0. As telas com anisotropias sigma=0 e sigma=r/4 são admissíveis: os pares de maré são (r/2,r/2) e (3r/4,r/4). Têm o mesmo traço r, mas áreas de Jacobi distintas na quarta ordem. Nenhum desses dados geométricos é derivado aqui do estado.

Para uma função arbitrária g: R→R, mantenha o relógio óptico t e escreva o resíduo efetivo já definido na040:

    D_sigma,g(t) = amplitudeEntropyIncrement b (g(t))
                  - eta (geometricJacobiArea(r/2+sigma,r/2-sigma,t)-1).

[DERIVED — fortalecimento] Na diferença D_(r/4),g-D_0,g, a leitura entrópica cancela exatamente. Portanto a diferença coincide com aquela obtida para g(t)=t, independentemente de continuidade, monotonia, jato ou origem de g. Pelos limites efetivos037:

    lim_(t→0,t≠0) [D_(r/4),g(t)/t^4-D_0,g(t)/t^4]
       = eta r^2/96 > 0.

Logo, para TODO relógio comum g, ao menos uma dessas DUAS igualdades quárticas falha. O quantificador é “para todo g existe uma das duas telas em que falha”; não é “todo g falha em toda tela”. Um funcional da mesma história de estados, aplicado com a mesma referência e orientação, produz o mesmo g e está coberto por esse resultado mais forte. Não se presume que toda prescrição de relógio possua jato cúbico.

[DERIVED — classe admissível explícita] StateClock representará uma reparametrização orientada da curva, com g(0)=0, derivada bilateral g'(0)=1 e jato (g(t)-t)/t^3→lambda. A referência e a orientação são dados da escolha da curva; a estrutura não afirma intrinsecidade nem depende da tela. Relógios cúbicos g(t)=t+lambda t^3 tornam a classe não vazia. Para essa subclasse, a040 já prova o resíduo quártico C_sigma-2 lambda log(2)B e a preservação do limite quadrático zero.

[DERIVED — controle construtivo] Cada tela admissível separadamente admite o relógio cúbico com lambda=cancellingStateClock(b,eta,sigma), que anula o resíduo quártico. Entre as duas telas, a040 fornece exatamente lambda_(r/4)-lambda_0=r/96>0. Assim o resultado exclui uma escolha comum para ambas, sem excluir escolhas dependentes da geometria. Esses controles não selecionam um relógio físico.

[DERIVED — estado instantâneo e tempo modular] A curva efetiva amplitudeState(b,t) é par: um funcional apenas do estado instantâneo não pode ter derivada bilateral um na origem. Uma escolha de ramo orientado ou uma leitura da história pode escapar dessa primeira obstrução, mas continua sujeita à dicotomia se for comum às duas telas. O fluxo modular de um perfil fixo preserva seu estado e não realiza, por reparametrização normalizada, a curva não constante de amplitude. A040 já demonstra isso; não será criada uma instância modular falsa de StateClock. Os relógios Fisher e de leitura entrópica da040 envolvem referência, ramo e, no segundo caso quando usado como parametrização, uma hipótese de inversa local; não são funcionais bilaterais apenas do estado instantâneo.

[OPEN] A comparação quártica é mais forte que H3 infinitesimal. A preservação quadrática é compatível com a falha quártica; nenhum resultado daqui constrói calor microscópico, identifica a tela física, fecha H3 ou altera o gate. O módulo reutilizará os enunciados existentes e acrescentará a eliminação da hipótese de jato no teste de incompatibilidade entre as duas telas.
