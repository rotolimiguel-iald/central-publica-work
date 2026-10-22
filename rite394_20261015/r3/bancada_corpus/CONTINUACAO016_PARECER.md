[REAL / INPUT / OPEN] CONTINUAÇÃO 016 — diferencial efetivo e regularidade conjunta C1 do fluxo

06/09/2026. Continuação espontânea de 015. O turno anterior foi progresso verificável; esta etapa também acrescenta prova. Nenhuma ordem gerencial posterior à 007 foi encontrada. Auditoria adversarial independente pendente; a bancada não declara gate.

## Resultado exato

Foram compilados seis módulos, com 41 teoremas declarados e quatro definições construtivas com axiomas impressos separadamente. Todas as declarações impressas dependem apenas de propext, Classical.choice e Quot.sound; as compilações finais não contêm erros, avisos ou sorryAx. Contagens, hashes e caminhos dos logs são produzidos por audit_continuation016.py e registrados no manifesto.

O resultado central é:

\[
D_{(q,t)}\Phi(q,t)[h,\tau]=J(q,t)h+\tau f(\Phi(q,t)),
\quad J(q,0)=I,\quad \partial_tJ=Df(\Phi)J.
\]

A igualdade significa uma derivada de Fréchet efetiva, expressa por HasStrictFDerivAt, acompanhada da continuidade dessa derivada. O fluxo é ContDiffOn ℝ 1 no produto aberto de uma bola de dados iniciais por um intervalo temporal comum. O teorema flow_initial_hasFDerivAt cobre ambos os sinais do tempo.

J foi obtido pela ODE variacional. Sua identificação com a derivada não foi assumida: foi demonstrada pelo resto de Taylor e pela estimativa de Grönwall.

## Cadeia comprovada

| Módulo | Teoremas | Definições impressas | Conteúdo |
|---|---:|---:|---|
| DifferentialFlowExistence | 3 | 1 | Fluxo local com constante uniforme de Lipschitz nos dados; construção de Picard adaptada ao espaço de Banach. |
| VariationalFlow | 11 | 1 | Campo ampliado (f,Df∘J), solução Φ e operador J, condições iniciais, derivadas temporais e continuidade conjunta. |
| FlowLinearizationError | 5 | 0 | Equação exata do resto R e Grönwall com controle normalizado. |
| FlowDifferentiability | 7 | 0 | Taylor uniforme derivado, controle de Df em tempo compacto, derivada nos dados para tempos positivos e negativos. |
| GeodesicInitialRegularity | 8 | 2 | Derivada conjunta estrita, continuidade, C1 e construção geodésica com preservação da nulidade. |
| FlowDifferentiabilityControls | 7 | 0 | Resto linear nulo, fluxo do campo zero, bloco plano do diferencial e controle curvo C1. |

Essas são contagens de declarações, não de descobertas matemáticas novas. A existência adapta os argumentos de Picard de 015; a conservação de energia e da nulidade reutiliza os teoremas gerais de 015. A curvatura do fundo conformal e sua aceleração inicial também vêm das provas de 014–015. O avanço desta etapa é a formalização da dependência diferenciável dos dados e sua incorporação ao fluxo geodésico.

### Resto e uniformidade

Para h=q-r, definiu-se
\[
R(t)=\Phi(q,t)-\Phi(r,t)-J(r,t)h.
\]
A derivada provada é
\[
R'=Df(\Phi(r,t))R+
f(\Phi(q,t))-f(\Phi(r,t))-Df(\Phi(r,t))(\Phi(q,t)-\Phi(r,t)).
\]

A suavidade de f implica diferenciabilidade estrita e continuidade de Df perto de cada ponto da trajetória. A continuidade conjunta de Φ transporta essa estimativa aos parâmetros (q,t). A compacidade do intervalo temporal uniformiza a escolha do dado q próximo de r. Nenhuma compacidade de bolas em espaço infinito-dimensional foi usada. Também se deduz um limite M para a norma de Df sobre a trajetória temporal compacta.

Assim,
\[
\|R(T)\|\le \varepsilon C\,G(M,|T|)\|q-r\|.
\]
Como epsilon pode ser escolhido arbitrariamente pequeno, R(T)=o(‖q-r‖). As estimativas de Taylor e do operador não são hipóteses adicionais do teorema final.

A derivação prévia partiu do caso finito-dimensional. As provas finais são gerais para espaços normados reais, recebendo um fluxo variacional com as propriedades declaradas; a construção existencial desse fluxo requer um espaço de Banach real e um campo C∞ num aberto.

### Geometria

c1GeodesicFlow constrói um novo LocalPhaseFlow no domínio aberto de posições em U e velocidades diferentes de zero. Sua primeira projeção obedece x′=v e sua segunda obedece v′=−Γ(v,v). local_c1_metric_null_geodesics reúne C1 conjunto e preservação da nulidade para cada dado inicialmente nulo da bola.

local_c1_levi_civita_null_geodesics instancia a construção para a conexão de Levi-Civita produzida por uma solda suave e seu inverso. A inversibilidade, a suavidade e a assinatura lorentziana da construção anterior continuam INPUT. A família completa no espaço de fases contém também dados não nulos; a conclusão de nulidade tem a hipótese inicial explícita.

A construção é existencial e local: o novo fluxo vem do sistema ampliado escolhido por Picard. Não foi provada uma igualdade literal entre essa escolha e a função selecionada por Classical.choice na entrega 015. Os lemas gerais de conservação de 015 são aplicáveis ao novo habitante, o que basta para os enunciados entregues.

## Controles exatos

1. Um campo linear limitado tem resto de Taylor exatamente zero.
2. Para o campo nulo, a solução permanece no dado inicial e J=I em todo o intervalo.
3. Para Γ=0, o diferencial foi identificado por uma prova independente da solução afim:
   J(t)(h_x,h_v)=(h_x+t h_v,h_v). A identidade é confrontada com a derivada obtida pelo argumento variacional.
4. No fundo conformal curvo previamente construído, há um fluxo conjunto C1, inicialmente nulo, cuja aceleração em t=0 é −2(1,1,0,0). A nulidade persiste em todo o intervalo local.

Não foram usados dados observacionais ou aproximações numéricas para esses controles.

## O que continua aberto

A regularidade C1 não satisfaz por si só o predicado SmoothVectorOn de 014, que exige C∞. A indução da regularidade superior por prolongamentos variacionais ainda não foi formalizada.

Também faltam a seleção de dados numa seção transversal, a inversão local da projeção para a posição, o campo nulo geodésico suave no espaço-tempo, o primeiro jato de equilíbrio, a imersão e área integrada do horizonte. O resultado atual fornece a primeira derivada necessária para essa rota; não constrói esses objetos.

A ponte microscópica entre região e álgebra, a identificação entropia–área, seu coeficiente físico, o fluxo de calor e Clausius/H3, a ligação modular–geométrica e a globalização continuam OPEN. A hipótese física de proporcionalidade entropia–área e a relação de Clausius entram explicitamente no argumento de [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004), especialmente nos parágrafos das equações (2)–(6). Esta etapa não deduz essas hipóteses.

Portanto, há uma prova matemática local com hipóteses nomeadas; o objetivo amplo de gravidade quântica continua não alcançado.

## Custódia e reprodução

O manifesto fixa os bytes das fontes, binários locais, metadados de compilação, logs, backups e dependências locais pertinentes. As compilações foram feitas com Lean 4.31.0 e a mathlib resolvida pelo wrapper verify_stage.ps1. Não se declara um pacote portátil completo da biblioteca externa.

Reprodução da conferência sem escrita:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation016.py'
```

A ordem de compilação nova é a ordem da tabela. O módulo final importa toda a árvore 016 e os controles 015. A gerência deve recompilar em seu ambiente independente, preservando os artefatos entregues. O auditor local verifica a custódia e as evidências registradas; não substitui essa auditoria.

As falhas intermediárias de elaboração de tipos, composição de derivadas e continuidade, bem como avisos de argumentos redundantes, permanecem em logs próprios e backups de bytes. Só as compilações finais limpas sustentam os resultados declarados.

As entregas 014 e 015 foram reconferidas por seus auditores, respectivamente com 527 e 518 hashes, sem alterações. Escritas exclusivamente em Chatgpt; nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados.
