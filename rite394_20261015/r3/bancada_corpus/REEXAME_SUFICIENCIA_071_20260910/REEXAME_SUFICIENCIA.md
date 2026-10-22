# Continuidade da suficiência — entrega 071

10/09/2026, horário de Brasília. [DERIVED — demonstrações escritas e revisadas] [KNOWN — importações delimitadas] [REAL — leitura de artefatos]. Arquivos novos somente na bancada Chatgpt; originais preservados.

**Avanço central:** o resíduo suave identificado na entrega 070 recebeu uma demonstração. Primeiro foi construída a primitiva relativa ordinária M₂ com coeficientes suaves nos valores e dependência polinomial finita nos jatos diferenciados. Depois foi demonstrado seu transporte até

\[
H^2_{\mathrm{char,cov}}=0
\]

para a ação ambiente Einstein–sigma, com alvo S³, na classe natural indicada. A prova inclui a colagem no alvo. Ela não avalia uma série formal em y nem divide pelo gradiente da matéria.

**O próximo elo mudou:** agora é necessário ligar esse resultado ao complexo admissível da anomalia efetivamente produzida pela construção causal Q2. A classe de campos completos e a família de fundos mantidos fixos sob o BRST quântico precisam ser comparadas. A identidade quântica causal, o setor físico interagente e a conclusão UV não são consequências automáticas do novo resultado.

## 1. Estado canônico conferido

[REAL] A [captura 071](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/ESTADO_CANONICO_071.json>) relê quatro artefatos canônicos e encontra os mesmos bytes da entrega 070. O um.py v338 contém 683 arquivos embutidos. Dos 98 módulos do conjunto de comparação, 77 estão presentes e 21 continuam pendentes. O selo confere com o programa.

Nenhum um.py foi executado ou importado. Nenhuma compilação Lean, cálculo CAS, cálculo novo de diagramas ou teste de natureza foi feito nesta entrega. Os controles de integridade documental não são contagem de teoremas. Registro de fase e ramo, seletor, H3 interno e falsificadores existentes permanecem preservados.

## 2. A primitiva suave ordinária foi construída

A [demonstração por compatibilidade e Spencer](<C:/IALD/Central de Patentes/Chatgpt/M2_SUAVE_RELATIVO_071_20260910_000347/M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md>) trabalha primeiro em

\[
\mathcal A_{\rm coord}=C^\infty(x,g,y)
   [\text{jatos diferenciados e antifields}],
\]

numa carta contrátil dos valores, com cada elemento polinomial e de ordem finita nos jatos diferenciados. As primitivas intermediárias podem depender explicitamente de coordenadas e suavemente da métrica, além da classe racional natural.

O split estacionário de 069 fornece o complexo de compatibilidade da Hessiana e das identidades de Noether. O núcleo do último adjunto é o parâmetro universal de reducibilidade, já anulado pelos quatro covetores (dphi¹,dphi²,dphi³,dQ). A comparação com formas de contato e a homotopia

\[
\sigma h+h\sigma=(r+4-q)I
\]

eliminam a ordem superior do argumento auxiliar em passos finitos. Duas correções de contato transformam a 2-forma horizontal fechada em uma forma total fechada. A contração polinomial das fibras estacionárias e a integração suave nos valores fornecem a primitiva. O retorno pela KT dá

\[
\delta a_2^4+d_Ha_1^3=0
\quad\Longrightarrow\quad
a_2^4=\delta b_3^4+d_Hb_2^3.
\]

O [corolário de graus zero e um](<C:/IALD/Central de Patentes/Chatgpt/M2_SUAVE_RELATIVO_071_20260910_000347/COROLARIO_H0_H1_E_FINITUDE.md>) fornece as entradas de colagem. A [precisão de fatoração](<C:/IALD/Central de Patentes/Chatgpt/M2_SUAVE_RELATIVO_071_20260910_000347/PRECISAO_FATORACAO_FINITA_OPERADORES.md>) identifica os levantamentos finitos dos operadores. A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_071_20260910/PARECER_M2_SUAVE_ORDINARIO.md>) conferiu classe, finitude e sinais.

## 3. Covariantização e colagem em S³

A [demonstração de transporte](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COVARIANTIZACAO_E_H2_GLOBAL.md>) parte das entradas ordinárias anteriores e efetua quatro operações necessárias.

Primeiro, a descida compara as classes relativas negativas à cohomologia de zeroformas BRST. A dependência explícita em x é tratada nessa comparação; não se avalia x numa identidade que ainda contenha d_H. Segundo, os pares de escolha de referencial U,V são projetados num vielbein invertível. A parte suave arbitrária em valores métricos torna-se numérica, enquanto os jatos covariantes continuam polinomiais.

Após essa projeção, restam quatro ghosts de translação e seis de Lorentz. Para um termo de ghost q, antigh≤10−q. Assim a possível expansão intermediária em antifields termina efetivamente. Para uma primitiva beta de alpha com gh(alpha)=2, gh(beta)=1 e o teto é nove; não se usa o grau de alpha para cortar beta.

Terceiro, a colagem de Čech usa H²(S³;R)=0 e mantém explicitamente os termos sρ das partições de unidade. O volume de grau três do alvo permanece intacto. Quarto, a primitiva completa é convertida em primitiva independente dos ghosts de Lorentz pela fórmula finita

\[
\widehat\beta=\beta_0+\widehat F^I(\beta_I)_0
       +\widehat F^I\widehat F^J(\beta_{IJ})_0.
\]

A semissimplicidade elimina o possível covetor constante; o resto cúbico em F tem seis ghosts de translação e é zero em dimensão quatro. A componente sem antifields devolve uma 1-forma natural com rho₂≈d_H beta₁.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_071_20260910/PARECER_COVARIANTIZACAO.md>) examina essa composição. O resultado alcança coeficientes suaves globais no alvo e primitivas naturais na classe declarada, incluindo jatos degenerados de matéria. A ação contém g e phi independentes e conexão de Levi-Civita; não inclui automaticamente uma ação restrita por g[P],phi[P], torção ou novos gauges.

A redução de graus da entrega 070 pode agora consumir H²_char,cov=0 no complexo covariante dos campos completos. Uma classificação de H^(1,4)(s|d) deve manter explícita sua classe de contratermos: permitir funções suaves do vielbein e exigir apenas expressões racionais são escolhas distintas. Nenhuma passagem entre elas é feita pelo nome do grupo de cohomologia.

## 4. A simetria rígida da quebra pode ser imposta na própria Q2

A [prova da normalização O(4)](<C:/IALD/Central de Patentes/Chatgpt/NORMALIZACAO_O4_CAUSAL_071_20260910_000602_682931/PROVA_NORMALIZACAO_O4_E_ANOMALIA.md>) constrói uma prescrição causal exatamente equivariante. Com as aridades inferiores fixas e equivariantes, as diferenças na ordem corrente têm suporte na diagonal. A média é feita nessa liberdade local afim; o teorema de renormalização reconstrói os produtos superiores compatíveis. Causalidade e unitariedade são preservadas.

A anomalia extraída dessa prescrição é equivariante como família sobre fundos transportados conjuntamente. Isso paga uma condição que em 070 era apenas hipotética: a simetria da própria quebra produzida. A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_071_20260910/PARECER_NORMALIZACAO_O4.md>) conferiu a indução.

O resultado não elimina dependência de fundo. Uma função do produto interno entre phi e phi_bar pode ser invariante sob O(4) diagonal e ainda depender de phi_bar. O grupo inteiro transporta o centro da expansão; num fundo fixo, somente o estabilizador atua diretamente nessa mesma expansão. Portanto a simetria rígida não identifica, sozinha, a classe da quebra com o complexo dos campos completos da seção 3.

## 5. Rota dimensional adicional

A [ação BV em dimensão continuada](<C:/IALD/Central de Patentes/Chatgpt/CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md>) fornece a identidade clássica (Sigma_D,Sigma_D)=0 exatamente no regulador tensorial, incluindo fontes e o gauge. A construção usa invariância por difeomorfismos e nilpotência sem operações especiais de quatro dimensões; não é somente uma igualdade até O(epsilon).

Isso verifica a entrada algébrica da rota de renormalização de Anselmi identificada na nota. Sua aplicação conserva as condições do esquema dimensional, de truncatura e de tratamento infravermelho. A [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CME_DIMENSIONAL_071_20260910_001300_721043/PARECER_CME_DIMENSIONAL.md>) conferiu esses limites.

Ainda falta realizar a comparação com os produtos, fontes e contatos da Q2 curva. A extensão EFT admite novos parâmetros e pode afetar representantes de gauge; não fixa valores finitos, não garante invariância RG de κc=4 e não entrega um estado físico. A redução de quatro dimensões do coeficiente de calor não deve ser aplicada antes da extração de polos dimensionais: termos evanescentes precisam permanecer tipados.

## 6. Próximo elo e alcance restante

**Retirar da lista de lacunas, no alcance das provas escritas:** M₂ relativo suave ordinário em cartas; retorno até H²_char,cov natural global no alvo S³; existência de uma normalização causal O(4)-equivariante; identidade BV clássica dimensional exata.

**Manter como trabalho efetivo:** comparar a classe de campos completos com o espaço de contratermos da família Q2, que contém dados de fundo; fornecer a primitiva admissível da quebra produzida e satisfazer a identidade quântica em todas as ordens. A rota dimensional é uma alternativa cuja realização causal também exige comparação. Não se toma uma dessas comparações como já construída porque os campos têm os mesmos nomes.

Depois permanecem o setor e estado físico interagentes, positividade, independência entre fundos, questões globais ou discretas, condições de renormalização finitas e controle UV. A reconstrução gravitacional geral conserva seus contratos de correspondência física e de alcance; uma medida independente e um BRST vertical para probabilidades P, se alegados, precisam de construção própria. Os 21 módulos anteriores e as formalizações novas continuam pendentes de integração no programa vivo.

O avanço é matemático e localizado em obrigações precisas. Não equivale ao término do objetivo geral. Memória, desenho, pareceres, resultado estruturado e manifesto são novos arquivos da bancada; a entrega no túnel aponta para eles. Atlas e memórias canônicas permanecem somente leitura.
