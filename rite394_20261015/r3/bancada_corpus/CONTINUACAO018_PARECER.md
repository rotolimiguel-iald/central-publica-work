[REAL / INPUT / OPEN] CONTINUAÇÃO 018 — congruência nula local construída

06/09/2026. Continuação espontânea de 017. O turno anterior e esta etapa produziram progresso formal. O túnel contém as ordens gerenciais 001–007; não há ordem gerencial 018. A auditoria independente da gerência permanece pendente. Nenhum gate é declarado.

## Resultado e hipóteses

O teorema local_levi_civita_null_congruence prova:

Se U⊆Coordinate4 é aberto, A e B são campos matriciais suaves com A(x)B(x)=B(x)A(x)=I em U, p∈U e v≠0 satisfaz tensorQuad(frameMetricField A p,v)=0, então existem N aberto com p∈N⊆U e um campo V tal que:

- SmoothVectorOn N V;
- V(p)=v;
- V(x)≠0 e tensorQuad(frameMetricField A x,V(x))=0 para todo x∈N;
- vectorAcceleration(frameLeviCivita A B,V)=0 em N.

A conclusão usa a aceleração covariante efetiva definida pelos derivados de coordenadas. Não a troca por um campo novo definido como zero. O campo V e seu domínio local são construídos; nenhum campo espacial geodésico é recebido como hipótese no enunciado final.

[INPUT] Permanecem a dimensão quatro, a forma lorentziana η, a solda A, seu inverso suave B, o aberto e uma tangente inicial nula não nula. O resultado é local em coordenadas e não demonstra que esses dados vêm do fluxo modular.

## Prova e passagem do espaço de fases ao campo espacial

A derivação foi registrada antes da implementação em CONTINUACAO018_DERIVACAO_PREVIA.md.

1. Escolhe-se uma coordenada não nula de v e constrói-se uma forma linear contínua ℓ com ℓ(v)=1. A projeção Π=I−v⊗ℓ satisfaz Πv=0 e Πz+ℓ(z)v=z. Os pontos P(z)=p+Πz estão no hiperplano ℓ(x−p)=0. O parâmetro z reúne as direções transversais e o tempo ℓ(z).

2. A velocidade inicial W(x)=B(x)A(p)v é suave. W(p)=v e A(x)W(x)=A(p)v; portanto sua norma quadrática para g(x)=A(x)ᵀηA(x) é zero. As identidades de inversão também dão W(x)≠0.

3. Constrói-se o fluxo variacional da equação geodésica no domínio regular {(x,u):x∈U,u≠0}. A entrada é ((P(z),W(P(z))),ℓ(z)). Define-se D como o interior do conjunto onde P(z)∈U e a entrada pertence à bola e ao intervalo do fluxo. Há prova de 0∈D. As projeções de posição X e velocidade Y são C∞ em D, pela suavidade conjunta paga em 017.

4. X(0)=p e Y(0)=v. A fórmula efetiva do diferencial do fluxo de 016, junto a DqΦ(q,0)=I e ∂tΦ=(velocidade,aceleração), dá DX(0)h=Πh+ℓ(h)v=h. A derivada do termo W na seção não acrescenta termo à projeção de posição no tempo zero.

5. smoothLocalChart aplica o teorema da função inversa da mathlib. A carta é restringida ao interior de D∩{z:IsUnit(DX(z))}. A continuidade de DX e a abertura dos operadores invertíveis mostram que essa restrição contém zero. Em cada ponto da fonte, a derivada é um isomorfismo contínuo; isso fornece C∞ da inversa em todo o alvo, não apenas no ponto p.

6. No alvo N da carta define-se V(x)=Y(X⁻¹(x)). Os lemas congruence_smooth, congruence_target_subset, congruence_base_value, congruence_nonzero e congruence_null transportam as propriedades efetivas do fluxo.

7. Para z na fonte e s próximo de zero, P(z+sv)=P(z) e ℓ(z+sv)=ℓ(z)+s. Logo c(s)=X(z+sv) percorre uma geodésica com dados iniciais fixos. As derivadas provadas são c′(0)=Y(z) e (Y(z+sv))′|₀=−Γ(X(z))(Y(z),Y(z)). A igualdade local V(c(s))=Y(z+sv) vem da inversão na fonte aberta. Pela regra da cadeia e unicidade das derivadas, obtém-se ∇_V V=0. O lema velocity_along_flow_derivative de 014 faz a ponte com a definição em coordenadas; os termos de conexão cancelam por igualdade vetorial.

local_null_congruence_from_seed separa essa construção para qualquer conexão suave compatível e uma seção suave de vetores nulos. local_levi_civita_null_congruence constrói essa seção usando A e B e descarrega a hipótese W do enunciado final.

## Integração com a tela transportada

constructed_congruence_transported_screen restringe A e B ao aberto N e aplica local_levi_civita_transported_screen de 014 ao V construído.

Além do campo, produz uma curva por p com tangente inicial v e um objeto GeometricScreenAlong. O Gram inicial da tela é −1. Eventualmente para t<0 perto de zero, a área induzida da tela satisfaz A′(t)=θ(t)A(t).

Esse é o enunciado local já formalizado para a tela de 014. Não se afirma uma identidade integrada sobre uma hipersuperfície ou um horizonte, nem uma equação de Clausius.

## Controles e separação do equilíbrio

- flat_constructed_congruence_control instancia o construtor final com A=B=I, p=0 e v=(1,1,0,0). Há um campo local construído, suave, não nulo, nulo para η e geodésico para a conexão dessa solda constante.
- curved_constructed_congruence_control instancia o construtor com o fundo conformal de 014 e sua conexão compatível. A componente coordinateCurvature Γ 0 1 2 1 2 vale 1. Portanto a construção também é habitada em um fundo com curvatura não zero.
- geodesic_nullity_does_not_force_zero_expansion reutiliza o campo explícito expandingNullVelocity de 014: ele é suave, não nulo, nulo e geodésico, mas θ(0)=2. Não se identifica esse campo com toda escolha produzida pelo construtor. O controle demonstra que geodesicidade e nulidade, sozinhas, não pagam expansão zero.

Nenhum controle utiliza dados observacionais ou altera estatuto físico.

## Fontes, compilações e contagens

| Módulo | Teoremas declarados | Definições com axiomas impressos |
|---|---:|---:|
| TransverseInitialData | 11 | 0 |
| GeodesicShooting | 11 | 0 |
| ShootingLocalInverse | 0 | 1 |
| NullCongruenceField | 8 | 0 |
| ConstructedNullCongruence | 2 | 0 |
| CongruenceScreenIntegration | 1 | 0 |
| NullCongruenceControls | 4 | 0 |
| Total | 37 | 1 |

Contagens lidas dos fontes por script. Elas incluem auxiliares, aplicações e controles; não medem descobertas novas. Reutilizam-se o teorema da função inversa da mathlib, o diferencial do fluxo de 016, sua suavidade de 017, a preservação da nulidade de 015 e a tela/controles de 014.

Os sete módulos finais compilaram com fonte estável e exit 0. Todas as declarações impressas dependem apenas de propext, Classical.choice e Quot.sound; nenhum erro, aviso ou sorryAx nos logs finais. O inventário registra fontes, oleans, logs, metadados, dependências locais, backups e cópias das tentativas rejeitadas. Nenhuma falha intermediária é usada como prova.

A primeira versão do helper de revisão tinha uma quebra de linha ausente. O Python recusou sua execução antes de gravar documentos; o código defeituoso foi preservado em backup exato. Falhas intermediárias de reescrita dependente, simplificação e tipagem de vizinhanças também permanecem nos registros.

Reprodução de custódia, em modo somente leitura:
C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation018.py"

O auditor verifica bytes e evidências registradas. Não substitui a recompilação independente da gerência. Lean 4.31.0 e as dependências externas resolvidas pelo wrapper não formam um pacote portátil integral.

## Obrigações restantes

[OPEN] O primeiro jato de equilíbrio, incluindo expansão e cisalhamento nulos, ainda precisa de construção própria. A seção transversal usada aqui garante uma carta do fluxo, mas não garante que V seja normal a uma hipersuperfície nula. Integrabilidade, horizonte imerso e área integrada continuam separados.

[OPEN] A ponte região–álgebra, a identificação microscópica entropia–área, a unidade de área e seu coeficiente, a evolução do estado, o calor/Clausius/H3, a identificação modular-geometria e a colagem global não são descarregados por este resultado.

O objetivo amplo de gravidade quântica permanece ativo e não alcançado. O avanço desta entrega é a existência formal de uma congruência geodésica nula local sob as hipóteses geométricas explicitadas.

Todas as escritas ficaram em Chatgpt. O um.py não foi executado, importado ou editado. Kernel canônico, Atlas, memórias, selos e gate permaneceram intocados pela bancada. As custódias 016 e 017 foram reconferidas com seus auditores em modo de leitura.
