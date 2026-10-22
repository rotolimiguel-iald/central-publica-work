[REAL / INPUT / OPEN] CONTINUAÇÃO 019 — primeiro jato de equilíbrio construído

06/09/2026. Continuação espontânea de 018. O turno anterior foi progresso, com custódia reconferida nesta sessão. Permanecem as ordens gerenciais 001–007 no túnel. O objetivo amplo continua ativo e não alcançado. Auditoria independente da gerência pendente; nenhum gate declarado.

## Resultado principal

local_levi_civita_equilibrium_congruence fortalece o teorema de 018:

Dados um aberto U⊆Coordinate4, campos A e B suaves com AB=BA=I em U, p∈U e v≠0 nulo para g(p)=A(p)ᵀηA(p), existem um aberto p∈N⊆U e um campo V suave em N com:

- V(p)=v;
- V(x)≠0 e g(x)(V(x),V(x))=0 para todo x∈N;
- ∇_V V=0 em N;
- ∇V(p)=0.

A última igualdade é covariantVectorGradient(frameLeviCivita A B,V,p)=0, calculada com as derivadas de coordenadas da casa. O campo e seu primeiro jato de equilíbrio são construídos. Não se recebe um campo espacial nem a condição de equilíbrio como hipótese no teorema final.

[INPUT] Dimensão quatro, assinatura lorentziana fixada, solda A e inversa B suaves, aberto e tangente inicial nula não nula. Não se identifica a origem desses dados com a teoria modular por esta prova.

A condição ∇V(p)=0 é pontual. Ela não afirma que V seja paralelo num aberto, nem que a curvatura seja zero.

## Derivação efetivamente formalizada

A derivação foi gravada antes do código em CONTINUACAO019_DERIVACAO_PREVIA.md.

1. Define-se o mapa linear contínuo J(h)=−∑ᵢhᵢΓᵢ(p)v e o campo afim R(x)=v+J(x−p). affine_seed_derivative demonstra sua derivada efetiva. affine_seed_gradient_zero mostra ∇R(p)=0.

2. Para q(x)=g(x)(R(x),R(x)), a compatibilidade métrica fornece
   ∂ᵢq(p)=2g(p)(R(p),∇ᵢR(p))=0.
   Todas as derivadas parciais são reunidas em Dq(p)=0, com diferenciabilidade provada. Não se usa o valor convencional de fderiv para uma função sem diferenciabilidade.

3. O referencial nulo normalizado de 013 fornece um companheiro n₀ com g(p)(n₀,n₀)=0 e g(p)(v,n₀)=−1. O transporte n(x)=B(x)A(p)n₀ é suave e nulo. Assim d(p)=2g(p)(R(p),n(p))=−2. O domínio D é o interior de {x∈U:g(x)(R(x),n(x))≠0}; a continuidade prova p∈D.

4. Define-se W(x)=R(x)−[q(x)/d(x)]n(x). A expansão bilinear dá
   g(W,W)=q−2(q/d)g(R,n)+(q/d)²g(n,n)=0.
   Como q(p)=Dq(p)=0 e d(p)≠0, a correção tem valor e derivada zero. null_correction_preserves_derivative prova esse fato pela regra do produto e pela diferenciabilidade da inversão escalar. Portanto W(p)=v, DW(p)=J e ∇W(p)=0. local_null_seed_with_zero_covariant_jet reúne a construção a partir de A e B.

5. No shooting de 018, X é a posição e Y a velocidade. A derivada já paga é DX(0)=I. Agora shooting_velocity_derivative_zero prova
   DY(0)h=DW(p)(Πh)+ℓ(h)·sprayAcceleration Γ p v.
   Como J(v)=−Γ(p)(v,v) e Πh+ℓ(h)v=h, esse valor é J(h).

6. shooting_inverse_derivative_base demonstra D(X⁻¹)(p)=I na carta construída. A regra da cadeia aplicada a V=Y∘X⁻¹ dá DV(p)=J, além de V(p)=v. A igualdade das derivadas é então transportada para a definição de covariantVectorGradient; congruence_prescribed_gradient_zero conclui ∇V(p)=0.

O J deste cálculo é connectionInitialJet, um mapa linear de dados iniciais. Não é a conjugação modular de Tomita.

## Tela construída, forma óptica e focalização

EquilibriumScreenData é um objeto exclusivamente geométrico. Reúne aberto, campo, nulidade, não anulação, geodesicidade, jato zero, curva e tela transportada. Sua definição não contém calor, entropia nem Clausius.

localEquilibriumScreen habita esse tipo pela construção nova e pelo transporte da tela de 014. A escolha é formal e não computável, usando Classical.choice, explicitamente conferida pelo Lean.

Para esse objeto:

- equilibrium_screen_expansion_zero prova θ(p)=0;
- equilibrium_screen_optical_form_zero prova S(0)ᵀg(p)(∇V(p))S(0)=0;
- equilibrium_screen_area_initial prova A(0)=1 na normalização da base da tela;
- area_rate conserva a identidade A′=θA, eventualmente para t<0 perto de zero;
- equilibrium_screen_focusing aplica a identidade de Raychaudhuri já paga à conexão sem torção e ao jato agora construído.

local_equilibrium_screen_with_focusing reúne, para a conexão de Levi-Civita da solda, a existência dos dados de tela e:

θ(p)=0, A(0)=1, θ′(0)=−Ricₚ(v,v).

A forma óptica inteira é zero no ponto, o que é mais informação algébrica que apenas a expansão zero. Não foi criada uma definição independente de cisalhamento para esconder uma hipótese. O enunciado formal transportado é a forma matricial zero.

A área inicial um é normalização da tela, não escolha de unidade física ou valor do coeficiente de entropia por área.

## Controles

flat_equilibrium_congruence_control aplica o construtor à solda identidade, ao ponto zero e à direção (1,1,0,0). O resultado inclui o campo construído com jato zero.

curved_equilibrium_congruence_control constrói o campo em controlConformalMetric com sua conexão compatível. O companheiro nulo é explícito; a correção e o shooting produzem a congruência de equilíbrio. A componente coordinateCurvature Γ 0 1 2 1 2 vale 1.

Além disso, o campo construído no controle curvo é diferente de expandingNullVelocity, preservado desde 014. Esse campo anterior tinha expansão inicial 2; o novo tem gradiente e expansão zero no ponto. zero_gradient_differs_from_expanding_field prova a diferença. Nenhum resultado anterior foi apagado.

O controle curvo verifica que o equilíbrio pontual não implica geometria plana. Não foram usados dados observacionais.

## Arquivos e evidências

| Módulo | Teoremas declarados | Definições com axiomas impressos |
|---|---:|---:|
| NullJetAlgebra | 8 | 0 |
| PrescribedCovariantJet | 10 | 0 |
| NullSeedWithJet | 3 | 0 |
| ShootingJetTransfer | 5 | 0 |
| EquilibriumNullCongruence | 2 | 0 |
| EquilibriumScreenIntegration | 5 | 1 |
| EquilibriumCongruenceControls | 5 | 0 |
| Total | 38 | 1 |

Contagens lidas dos fontes por script. Incluem auxiliares, aplicações e controles; não são contagens de descobertas científicas. Reutilizam-se a carta e a congruência de 018, o diferencial do fluxo de 016, a suavidade de 017, o referencial de 013, a tela de 014 e as identidades geométricas anteriores.

As compilações finais dos sete módulos foram conferidas: exit 0, fontes estáveis, zero erros, zero avisos e nenhum sorryAx. Nove tentativas intermediárias rejeitadas por erros ou avisos foram preservadas com cópias exatas dos logs.

O auditor exige, para cada fonte final, log com exit 0, fonte estável, ausência de erros, avisos e sorryAx, e cobertura de todos os teoremas por #print axioms. Somente propext, Classical.choice e Quot.sound são admitidos. Falha em qualquer exigência impede a emissão do manifesto.

Tentativas intermediárias e avisos foram preservados, incluindo coerções entre instâncias de espaços, tipagem explícita de derivadas nulas, a correção da API de derivada de quociente, reescritas e simplificações. Cada versão compilada é recuperável pelo fonte final ou por backup de bytes.

Reprodução de custódia, somente leitura:
C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation019.py"

O manifesto registra hashes dos bytes, logs, metadados, fontes, oleans e dependências locais. A verificação registrada não substitui a recompilação independente da gerência. Lean 4.31.0 e a mathlib externa são resolvidos pelo wrapper; não se declara um pacote portátil integral.

## Obrigações restantes

[OPEN] Integrabilidade além do ponto, hipersuperfície nula imersa e área integrada sobre um horizonte. O jato zero e a carta do fluxo não pagam esses objetos por si.

[OPEN] Região–álgebra, entropia–área microscópica, unidade de área e coeficiente físico, evolução do estado, corrente de calor, Clausius/H3, identificação modular-geometria e globalização.

GeometricHorizonPencil ainda contém campos físicos de calor e Clausius. Esta etapa constrói EquilibriumScreenData e a focalização, mas não declara GeometricHorizonPencil habitado sem pagar aqueles campos. O objetivo amplo de gravidade quântica continua não alcançado.

Todas as escritas exclusivamente em Chatgpt. Nenhum um.py foi executado, importado ou editado. Kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. Entregas anteriores preservadas. Incorporação e auditoria independente pertencem à gerência; confirmação física é reservada ao observador.
